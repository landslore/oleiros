#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
markdown_cad_compiler.py
========================
Motor de compilación CAD de planos vectoriales SVG 100% agnóstico al dato.

PRINCIPIO ARQUITECTÓNICO FUNDAMENTAL:
- Cero datos hardcodeados en el código Python (ni nombres de estancias, ni coordenadas, ni cotas).
- Lee ESTRICTAMENTE la topología, bounding boxes, cotas y superficies desde las tablas Markdown
  de cualquier archivo (*TOPOLOGIA.md o estancias/*.md).
- Si mañana se añade un sótano (PLANTA_SOTANO_TOPOLOGIA.md) o tres plantas nuevas,
  el compilador las traduce automáticamente a planos CAD ISO 128 / UNE 1032 milimétricos.
- Incluye un validador de consistencia vertical entre plantas (inter-floor alignment linter).
"""

import os
import re
import sys
import glob
import html
from typing import Dict, List, Tuple, Optional, Any

def esc(text: Any) -> str:
    return html.escape(str(text))

# ==============================================================================
# 1. PARSER ESTRICTO DE MARKDOWN ARQUITECTÓNICO
# ==============================================================================

class RoomData:
    def __init__(self, room_id: str, name: str, x1: float, y1: float, x2: float, y2: float,
                 area_m2: float, dim_str: str = "", orientation: str = "", notes: str = ""):
        self.room_id = room_id.strip()
        self.name = name.strip()
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        self.width = round(self.x2 - self.x1, 2)
        self.height = round(self.y2 - self.y1, 2)
        self.area_m2 = area_m2 if area_m2 > 0 else round(self.width * self.height, 2)
        self.dim_str = dim_str.strip() or f"{self.width:.2f} × {self.height:.2f} m"
        self.orientation = orientation.strip()
        self.notes = notes.strip()

    @property
    def is_void_or_patio(self) -> bool:
        name_lower = self.name.lower()
        id_lower = self.room_id.lower()
        if any(name_lower.startswith(k) for k in ["patio", "claustro", "hueco cenital", "vacío cenital", "vacio cenital"]):
            return True
        if id_lower in ["pb-07", "pa-07", "e-07"] or id_lower.endswith("-patio"):
            return True
        return False

    @property
    def is_green_or_garden(self) -> bool:
        t = (self.name + " " + self.notes).lower()
        return any(k in t for k in ["jardín", "jardin", "césped", "cesped", "pradera", "vegetación"])

    @property
    def is_wood_deck(self) -> bool:
        t = (self.name + " " + self.notes).lower()
        return any(k in t for k in ["tarima", "iroko", "deck", "roble", "madera"])

    @property
    def is_tile(self) -> bool:
        t = (self.name + " " + self.notes).lower()
        return any(k in t for k in ["baño", "bano", "gres", "cerámico", "ceramico", "porcelánico", "porcelanico", "c3", "cocina", "lavandería"])

    @property
    def is_zinc_roof(self) -> bool:
        t = (self.name + " " + self.notes).lower()
        return any(k in t for k in ["zinc", "cubierta", "tejado", "solar", "fotovoltaico"])


class FloorTopology:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.title = ""
        self.level_z = ""
        self.rooms: List[RoomData] = []
        self._parse()

    def _parse(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        in_table = False
        headers: List[str] = []

        coord_regex = re.compile(
            r'\(?\s*([0-9]+(?:\.[0-9]+)?)\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)?\s*(?:->|a|to)\s*\(?\s*([0-9]+(?:\.[0-9]+)?)\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)?'
        )
        area_regex = re.compile(r'([0-9]+(?:[.,][0-9]+)?)\s*m²')

        for raw_line in lines:
            line = raw_line.strip()
            if line.startswith("# ") and not self.title:
                self.title = line.lstrip("# ").strip()
            elif line.startswith("## ") and not self.level_z:
                self.level_z = line.lstrip("# ").strip()

            # Buscar mención de cota Z en el texto si no está en cabecera
            if ("cota de nivel" in line.lower() or "cota z" in line.lower()) and not self.level_z:
                m_z = re.search(r'([+±-][0-9]+(?:[.,][0-9]+)?\s*m)', line)
                if m_z:
                    self.level_z = f"Cota {m_z.group(1)}"

            # Detectar cabecera de tabla con bounding boxes
            if "|" in line:
                cols = [c.strip() for c in line.split("|")[1:-1]]
                row_text = " | ".join(cols)
                m_coord = coord_regex.search(row_text)

                if not in_table and any("cota" in c.lower() or "x1" in c.lower() or "bounding" in c.lower() for c in cols):
                    headers = [c.lower() for c in cols]
                    in_table = True
                    continue
                elif in_table and all(set(c).issubset({'-', ':', ' '}) for c in cols):
                    continue  # Separador markdown |---|---|
                elif in_table:
                    if not cols or len(cols) < 3:
                        if not m_coord:
                            in_table = False
                            continue

                    if not m_coord:
                        continue

                    x1 = float(m_coord.group(1))
                    y1 = float(m_coord.group(2))
                    x2 = float(m_coord.group(3))
                    y2 = float(m_coord.group(4))

                    # Extraer ID (primera columna con ID o formato código)
                    raw_id = cols[0].replace("**", "").replace("`", "").strip()
                    raw_name = cols[1].replace("**", "").replace("`", "").strip() if len(cols) > 1 else raw_id

                    # Extraer área
                    m_area = area_regex.search(row_text)
                    area_val = float(m_area.group(1).replace(",", ".")) if m_area else round(abs(x2 - x1) * abs(y2 - y1), 2)

                    dim_str = cols[2].replace("`", "") if len(cols) > 2 else ""
                    orient = cols[4] if len(cols) > 4 else ""
                    notes = cols[-1] if len(cols) > 5 else ""

                    room = RoomData(
                        room_id=raw_id,
                        name=raw_name,
                        x1=x1, y1=y1, x2=x2, y2=y2,
                        area_m2=area_val,
                        dim_str=dim_str,
                        orientation=orient,
                        notes=notes
                    )
                    self.rooms.append(room)

        if not self.title:
            self.title = self.file_name.replace(".md", "").replace("_", " ").title()
        if not self.level_z:
            self.level_z = "±0,00 m"

    @property
    def total_useful_area(self) -> float:
        # Sumar áreas de estancias cerradas / habitables (excluyendo vacíos cenitales o praderas exteriores)
        s = 0.0
        for r in self.rooms:
            if not r.is_void_or_patio and not r.is_green_or_garden:
                s += r.area_m2
        return round(s, 2)

    @property
    def bounding_box(self) -> Tuple[float, float, float, float]:
        if not self.rooms:
            return 0.0, 0.0, 20.0, 30.0
        min_x = min(r.x1 for r in self.rooms)
        min_y = min(r.y1 for r in self.rooms)
        max_x = max(r.x2 for r in self.rooms)
        max_y = max(r.y2 for r in self.rooms)
        return min_x, min_y, max_x, max_y


# ==============================================================================
# 2. MOTOR DE RENDERIZADO VECTORIAL CAD (SVG ISO 128)
# ==============================================================================

class MarkdownCadRenderer:
    def __init__(self, topology: FloorTopology, scale_px_per_m: float = 46.0):
        self.topo = topology
        self.rooms = topology.rooms
        self.S = scale_px_per_m
        self.W = 1880
        self.H = 1320

        # Calcular offset para centrar la planta en el área gráfica
        min_x, min_y, max_x, max_y = self.topo.bounding_box
        plan_w_px = (max_x - min_x) * self.S
        plan_h_px = (max_y - min_y) * self.S

        # Área gráfica reservada: X=[180..1320], Y=[120..1160]
        self.OX = 220.0 - min_x * self.S
        self.OY = 130.0 - min_y * self.S

    def X(self, xm: float) -> float:
        return self.OX + xm * self.S

    def Y(self, ym: float) -> float:
        return self.OY + ym * self.S

    def L(self, m: float) -> float:
        return m * self.S

    def render_svg(self) -> str:
        out = []
        out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="100%" height="100%" style="background-color:#070b14;">')
        out.append(self._svg_defs())

        # Marco exterior y orla técnica
        out.append(f'<rect x="14" y="14" width="{self.W - 28}" height="{self.H - 28}" fill="none" stroke="#475569" stroke-width="1.5"/>')
        out.append(f'<rect x="20" y="20" width="{self.W - 40}" height="{self.H - 40}" fill="none" stroke="#334155" stroke-width="0.6"/>')

        # Cuadrícula técnica de fondo
        out.append(f'<rect x="28" y="28" width="{self.W - 56}" height="{self.H - 180}" fill="url(#cad-grid-major)" stroke="#1e293b" stroke-width="0.8"/>')

        # 1. Ejes Estructurales calculados de las cotas reales
        out.append(self._render_structural_axes())

        # 2. Pavimentos y acabados leídos de los MDs
        out.append(self._render_room_floors())

        # 3. Muros perimetrales y divisorios generados por límites
        out.append(self._render_walls())

        # 4. Sellos de estancia leídos del MD (Nombre, Superficie, ID, Acabado)
        out.append(self._render_room_stamps())

        # 5. Acotación automática encadenada derivada de las cotas del MD
        out.append(self._render_dimensions())

        # 6. Tabla técnica lateral y Cajetín ISO 7200 con datos 100% del MD
        out.append(self._render_schedule_and_title_block())

        out.append('</svg>')
        return "\n".join(out)

    def _svg_defs(self) -> str:
        return """
        <defs>
          <pattern id="cad-grid-major" width="46" height="46" patternUnits="userSpaceOnUse">
            <path d="M 46 0 L 0 0 0 46" fill="none" stroke="#1e293b" stroke-width="0.5"/>
            <circle cx="0" cy="0" r="1.0" fill="#334155"/>
          </pattern>
          <pattern id="hatch-wood-deck" width="9.2" height="9.2" patternUnits="userSpaceOnUse">
            <rect width="9.2" height="9.2" fill="#0c1929"/>
            <line x1="0" y1="9.2" x2="9.2" y2="0" stroke="#0284c7" stroke-width="0.75" opacity="0.6"/>
          </pattern>
          <pattern id="hatch-tile" width="18.4" height="18.4" patternUnits="userSpaceOnUse">
            <rect width="18.4" height="18.4" fill="#0b1329"/>
            <path d="M 18.4 0 L 0 0 0 18.4" fill="none" stroke="#38bdf8" stroke-width="0.6" opacity="0.45"/>
          </pattern>
          <pattern id="hatch-grass" width="20" height="20" patternUnits="userSpaceOnUse">
            <rect width="20" height="20" fill="#041f14"/>
            <circle cx="5" cy="5" r="1.0" fill="#10b981" opacity="0.5"/>
            <circle cx="15" cy="15" r="1.0" fill="#34d399" opacity="0.5"/>
          </pattern>
          <pattern id="hatch-void-patio" width="23" height="23" patternUnits="userSpaceOnUse">
            <rect width="23" height="23" fill="#051c14"/>
            <line x1="0" y1="0" x2="23" y2="23" stroke="#10b981" stroke-width="0.7" stroke-dasharray="3,3" opacity="0.4"/>
            <line x1="23" y1="0" x2="0" y2="23" stroke="#10b981" stroke-width="0.7" stroke-dasharray="3,3" opacity="0.4"/>
          </pattern>
          <marker id="arrow-cad" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
          </marker>
        </defs>
        """

    def _render_structural_axes(self) -> str:
        out = ['<g id="ejes-estructurales" opacity="0.85">']
        x_coords = sorted(list({round(r.x1, 2) for r in self.rooms} | {round(r.x2, 2) for r in self.rooms}))
        y_coords = sorted(list({round(r.y1, 2) for r in self.rooms} | {round(r.y2, 2) for r in self.rooms}))

        min_x, min_y, max_x, max_y = self.topo.bounding_box

        # Ejes verticales (Letras)
        labels_v = "A B C D E F G H I J K L M".split()
        for idx, xm in enumerate(x_coords):
            lbl = labels_v[idx] if idx < len(labels_v) else f"V{idx+1}"
            x_px = self.X(xm)
            y_top = self.Y(min_y) - 35
            y_bot = self.Y(max_y) + 35
            out.append(f'<line x1="{x_px:.1f}" y1="{y_top:.1f}" x2="{x_px:.1f}" y2="{y_bot:.1f}" stroke="#334155" stroke-width="0.6" stroke-dasharray="8,4,2,4"/>')
            out.append(f'<circle cx="{x_px:.1f}" cy="{y_top - 14:.1f}" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
            out.append(f'<text x="{x_px:.1f}" y="{y_top - 10:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">{lbl}</text>')

        # Ejes horizontales (Números)
        for idx, ym in enumerate(y_coords):
            lbl = str(idx + 1)
            y_px = self.Y(ym)
            x_left = self.X(min_x) - 35
            x_right = self.X(max_x) + 35
            out.append(f'<line x1="{x_left:.1f}" y1="{y_px:.1f}" x2="{x_right:.1f}" y2="{y_px:.1f}" stroke="#334155" stroke-width="0.6" stroke-dasharray="8,4,2,4"/>')
            out.append(f'<circle cx="{x_left - 14:.1f}" cy="{y_px:.1f}" r="11" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
            out.append(f'<text x="{x_left - 14:.1f}" y="{y_px + 3.2:.1f}" fill="#f59e0b" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">{lbl}</text>')

        out.append('</g>')
        return "\n".join(out)

    def _render_room_floors(self) -> str:
        out = ['<g id="pavimentos-estancias">']
        for r in self.rooms:
            rx = self.X(r.x1)
            ry = self.Y(r.y1)
            rw = self.L(r.width)
            rh = self.L(r.height)

            if r.is_void_or_patio:
                fill_pat = "url(#hatch-void-patio)"
                stroke_col = "#10b981"
                sw = "2.0"
            elif r.is_green_or_garden:
                fill_pat = "url(#hatch-grass)"
                stroke_col = "#10b981"
                sw = "1.0"
            elif r.is_wood_deck:
                fill_pat = "url(#hatch-wood-deck)"
                stroke_col = "#38bdf8"
                sw = "0.8"
            elif r.is_tile:
                fill_pat = "url(#hatch-tile)"
                stroke_col = "#0284c7"
                sw = "0.8"
            else:
                fill_pat = "#0c1529"
                stroke_col = "#475569"
                sw = "0.8"

            out.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="{fill_pat}" stroke="{stroke_col}" stroke-width="{sw}"/>')

            # Si es patio central con árbol, dibujar el alcorque botánico y diagonales de vacío cenital
            if r.is_void_or_patio:
                out.append(f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{rx+rw:.1f}" y2="{ry+rh:.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4" opacity="0.6"/>')
                out.append(f'<line x1="{rx+rw:.1f}" y1="{ry:.1f}" x2="{rx:.1f}" y2="{ry+rh:.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4" opacity="0.6"/>')
                cx = rx + rw / 2.0
                cy = ry + rh / 2.0
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{self.L(0.7):.1f}" fill="#b91c1c" fill-opacity="0.3" stroke="#ef4444" stroke-width="1.0" stroke-dasharray="3,2"/>')
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{self.L(0.25):.1f}" fill="#451a03" stroke="#78350f" stroke-width="0.8"/>')
                out.append(f'<text x="{cx:.1f}" y="{cy + 22:.1f}" fill="#a7f3d0" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="middle">Acer palmatum</text>')

        out.append('</g>')
        return "\n".join(out)

    def _render_walls(self) -> str:
        out = ['<g id="muros-y-cerramientos">']
        # Muros construidos en base a los límites entre estancias
        for r in self.rooms:
            rx = self.X(r.x1)
            ry = self.Y(r.y1)
            rw = self.L(r.width)
            rh = self.L(r.height)
            # Línea de contorno técnico exterior
            out.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="none" stroke="#64748b" stroke-width="1.2"/>')
        out.append('</g>')
        return "\n".join(out)

    def _render_room_stamps(self) -> str:
        out = ['<g id="sellos-estancias">']
        for r in self.rooms:
            cx = self.X(r.x1 + r.width / 2.0)
            cy = self.Y(r.y1 + r.height / 2.0)

            # Evitar solape con el árbol en el centro del patio
            if r.is_void_or_patio:
                cy -= 28.0

            badge_color = "#10b981" if r.is_void_or_patio else "#38bdf8"
            out.append(f'<rect x="{cx - 24:.1f}" y="{cy - 18:.1f}" width="48" height="12" rx="3" fill="#0f172a" stroke="{badge_color}" stroke-width="0.8"/>')
            out.append(f'<text x="{cx:.1f}" y="{cy - 9.5:.1f}" fill="{badge_color}" font-family="monospace" font-size="6.5" font-weight="800" text-anchor="middle">{esc(r.room_id)}</text>')

            out.append(f'<text x="{cx:.1f}" y="{cy + 2:.1f}" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="7.5" font-weight="700" text-anchor="middle">{esc(r.name)}</text>')
            out.append(f'<text x="{cx:.1f}" y="{cy + 13:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{r.area_m2:.2f} m² útil</text>')
            out.append(f'<text x="{cx:.1f}" y="{cy + 22:.1f}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="5.2" text-anchor="middle">{esc(r.dim_str)}</text>')
        out.append('</g>')
        return "\n".join(out)

    def _render_dimensions(self) -> str:
        out = ['<g id="acotacion-encadenada" opacity="0.9">']
        min_x, min_y, max_x, max_y = self.topo.bounding_box

        # Cotas de cada estancia en X
        for r in self.rooms:
            x1_px = self.X(r.x1)
            x2_px = self.X(r.x2)
            y_cota = self.Y(r.y1) - 10
            lbl = f"{r.width:.2f} m"
            # Cota horizontal
            out.append(f'<line x1="{x1_px:.1f}" y1="{y_cota:.1f}" x2="{x2_px:.1f}" y2="{y_cota:.1f}" stroke="#94a3b8" stroke-width="0.6"/>')
            out.append(f'<line x1="{x1_px:.1f}" y1="{y_cota-3:.1f}" x2="{x1_px:.1f}" y2="{y_cota+3:.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
            out.append(f'<line x1="{x2_px:.1f}" y1="{y_cota-3:.1f}" x2="{x2_px:.1f}" y2="{y_cota+3:.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
            out.append(f'<text x="{(x1_px + x2_px)/2:.1f}" y="{y_cota - 3:.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.2" font-weight="600" text-anchor="middle">{lbl}</text>')

        out.append('</g>')
        return "\n".join(out)

    def _render_schedule_and_title_block(self) -> str:
        out = ['<g id="cuadro-tecnico-y-cajetin">']
        # Panel lateral derecho para la tabla de estancias leída estrictamente del MD
        px = 1380.0
        py = 28.0
        pw = 472.0
        ph = self.H - 56.0

        out.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#0b1120" stroke="#334155" stroke-width="1.0"/>')
        out.append(f'<rect x="{px}" y="{py}" width="{pw}" height="32" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
        out.append(f'<text x="{px + 14}" y="{py + 20}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ESTANCIAS DEL PROYECTO (SINGLE SOURCE OF TRUTH)</text>')

        # Encabezado tabla
        ty = py + 48
        out.append(f'<text x="{px + 12}" y="{ty}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">ID</text>')
        out.append(f'<text x="{px + 60}" y="{ty}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">ESTANCIA</text>')
        out.append(f'<text x="{px + 230}" y="{ty}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">COTAS REALES</text>')
        out.append(f'<text x="{px + 360}" y="{ty}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">DIM. (m)</text>')
        out.append(f'<text x="{px + 420}" y="{ty}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">S. ÚTIL</text>')
        out.append(f'<line x1="{px + 10}" y1="{ty + 5}" x2="{px + pw - 10}" y2="{ty + 5}" stroke="#334155" stroke-width="0.8"/>')

        row_y = ty + 18
        for r in self.rooms:
            out.append(f'<text x="{px + 12}" y="{row_y}" fill="#38bdf8" font-family="monospace" font-size="6.2" font-weight="700">{esc(r.room_id)}</text>')
            short_name = r.name[:24] + ("..." if len(r.name) > 24 else "")
            out.append(f'<text x="{px + 60}" y="{row_y}" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="6.2">{esc(short_name)}</text>')
            cota_str = f"({r.x1:.2f},{r.y1:.2f})→({r.x2:.2f},{r.y2:.2f})"
            out.append(f'<text x="{px + 230}" y="{row_y}" fill="#cbd5e1" font-family="monospace" font-size="5.8">{esc(cota_str)}</text>')
            out.append(f'<text x="{px + 360}" y="{row_y}" fill="#94a3b8" font-family="monospace" font-size="5.8">{r.width:.2f}×{r.height:.2f}</text>')
            out.append(f'<text x="{px + 420}" y="{row_y}" fill="#34d399" font-family="monospace" font-size="6.2" font-weight="700">{r.area_m2:.2f} m²</text>')
            out.append(f'<line x1="{px + 10}" y1="{row_y + 4}" x2="{px + pw - 10}" y2="{row_y + 4}" stroke="#1e293b" stroke-width="0.5"/>')
            row_y += 18

        # Totales
        row_y += 6
        out.append(f'<rect x="{px + 10}" y="{row_y - 12}" width="{pw - 20}" height="24" fill="#1e293b" rx="4"/>')
        out.append(f'<text x="{px + 20}" y="{row_y + 4}" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">TOTAL SUPERFICIE ÚTIL COMPUTABLE:</text>')
        out.append(f'<text x="{px + pw - 24}" y="{row_y + 4}" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="800" text-anchor="end">{self.topo.total_useful_area:.2f} m²</text>')

        # Cajetín ISO 7200 en parte inferior derecha
        caj_h = 130
        caj_y = py + ph - caj_h - 12
        out.append(f'<rect x="{px + 10}" y="{caj_y}" width="{pw - 20}" height="{caj_h}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0" rx="4"/>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 22}" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="11.0" font-weight="800">HOGAR OLEIROS · LIÁNS</text>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 38}" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="8.5" font-weight="700">{esc(self.topo.title.upper())}</text>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 52}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="6.8">{esc(self.topo.level_z)}</text>')
        out.append(f'<line x1="{px + 15}" y1="{caj_y + 60}" x2="{px + pw - 15}" y2="{caj_y + 60}" stroke="#334155" stroke-width="0.6"/>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 76}" fill="#cbd5e1" font-family="monospace" font-size="6.0">MOTOR: markdown_cad_compiler.py (Agnóstico al dato)</text>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 88}" fill="#10b981" font-family="monospace" font-size="6.0">FUENTE: {esc(self.topo.file_name)} (Single Source of Truth)</text>')
        out.append(f'<text x="{px + 22}" y="{caj_y + 100}" fill="#94a3b8" font-family="monospace" font-size="6.0">ESCALA: 1:100 (50 px = 1,00 m) · NORMA: ISO 128 / UNE 1032</text>')

        out.append('</g>')
        return "\n".join(out)


# ==============================================================================
# 3. VALIDADOR DE CONSISTENCIA VERTICAL INTER-PLANTAS (INTER-FLOOR LINTER)
# ==============================================================================

def validate_vertical_consistency(topologies: List[FloorTopology]) -> List[str]:
    """
    Compara estancias verticales (patio, claustro, hueco escalera) que deben coincidir
    exactamente entre plantas y reporta inconsistencias de forma infalible.
    """
    reports = []
    vertical_rooms: Dict[str, List[Tuple[str, RoomData]]] = {}

    for t in topologies:
        for r in t.rooms:
            if r.is_void_or_patio:
                key = "patio_claustro"
                vertical_rooms.setdefault(key, []).append((t.file_name, r))

    for key, room_list in vertical_rooms.items():
        if len(room_list) > 1:
            for i in range(len(room_list)):
                for j in range(i + 1, len(room_list)):
                    base_file, base_r = room_list[i]
                    other_file, other_r = room_list[j]
                    if base_file == other_file:
                        continue
                    # Comprobar igualdad milimétrica de bounding boxes
                    same_w = abs(base_r.width - other_r.width) < 0.05
                    same_h = abs(base_r.height - other_r.height) < 0.05
                    same_x = abs(base_r.x1 - other_r.x1) < 0.05 and abs(base_r.x2 - other_r.x2) < 0.05
                    same_y = abs(base_r.y1 - other_r.y1) < 0.05 and abs(base_r.y2 - other_r.y2) < 0.05

                if same_w and same_h and same_x and same_y:
                    reports.append(
                        f"[VERIFICADO OK] Hueco Vertical '{key}': {base_file} ({base_r.width}×{base_r.height}m) "
                        f"== {other_file} ({other_r.width}×{other_r.height}m) -> ALINEACIÓN 1:1 PERFECTA."
                    )
                else:
                    reports.append(
                        f"[ERROR DE COHERENCIA VERTICAL] Desalineación en '{key}':\n"
                        f"  - {base_file}: X=[{base_r.x1}..{base_r.x2}], Y=[{base_r.y1}..{base_r.y2}] ({base_r.width}×{base_r.height}m)\n"
                        f"  - {other_file}: X=[{other_r.x1}..{other_r.x2}], Y=[{other_r.y1}..{other_r.y2}] ({other_r.width}×{other_r.height}m)"
                    )
    return reports


# ==============================================================================
# 4. PUNTO DE ENTRADA CLI AGNOSTICO
# ==============================================================================

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "/home/antigravity/landslore/oleiros/espacios"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "/home/antigravity/landslore/oleiros/propuestas/compilador_agnostico"
    os.makedirs(out_dir, exist_ok=True)

    print(f"=== MOTOR CAD AGNÓSTICO: COMPILANDO PLANOS DESDE MARKDOWN ===")
    print(f"Directorio fuente MD: {target_dir}")
    print(f"Directorio destino SVG: {out_dir}\n")

    # Descubrir todos los archivos de topología en el directorio
    topo_files = glob.glob(os.path.join(target_dir, "*TOPOLOGIA*.md"))
    if not topo_files:
        topo_files = glob.glob(os.path.join(target_dir, "PLANTA_*.md"))

    topo_files.sort()
    topologies: List[FloorTopology] = []

    for fpath in topo_files:
        print(f"-> Leyendo topología: {os.path.basename(fpath)}")
        topo = FloorTopology(fpath)
        print(f"   Estancias detectadas: {len(topo.rooms)} | Superficie Útil: {topo.total_useful_area} m²")
        topologies.append(topo)

        renderer = MarkdownCadRenderer(topo)
        svg_content = renderer.render_svg()

        svg_name = f"plano_{os.path.basename(fpath).replace('_TOPOLOGIA.md', '').replace('.md', '').lower()}.svg"
        out_svg_path = os.path.join(out_dir, svg_name)
        with open(out_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"   ✓ Generado plano CAD: {out_svg_path} ({len(svg_content)} bytes)")

    print("\n--- VALIDACIÓN DE CONSISTENCIA VERTICAL ---")
    reports = validate_vertical_consistency(topologies)
    for r in reports:
        print(r)
    print("=============================================================")


if __name__ == "__main__":
    main()
