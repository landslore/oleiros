#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor CAD Técnico ISO 128 / UNE 1032 para Generación de Planos Arquitectónicos de Ejecución (SVG).
Sin emojis ni dibujos esquemáticos: espesores de línea normalizados, sombreado ANSI31 de muros,
ejes estructurales, acotaciones encadenadas con trazos a 45°, bloques CAD de carpintería,
mobiliario, aparatos sanitarios e instalaciones MEP.
"""

import math


def cad_defs(bg_mode="technical"):
    """
    Define patrones técnicos ISO/ANSI (ANSI31 ladrillo/muro, aislamiento, hormigón,
    retícula milimetrada, marcadores de cota a 45° y flechas técnicas).
    """
    return """
  <defs>
    <!-- Retícula técnica milimetrada CAD (0.50m y 1.00m) -->
    <pattern id="cad-grid-minor" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M 25 0 L 0 0 0 25" fill="none" stroke="#1e293b" stroke-width="0.35" opacity="0.55"/>
    </pattern>
    <pattern id="cad-grid-major" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#cad-grid-minor)"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#334155" stroke-width="0.7" opacity="0.7"/>
    </pattern>

    <!-- Rayado ANSI31 (45 grados) para muros seccionados -->
    <pattern id="hatch-ansi31" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#94a3b8" stroke-width="0.8"/>
    </pattern>

    <!-- Rayado cruzado ANSI37 para pilares estructurales de hormigón/acero -->
    <pattern id="hatch-pillar" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="5" stroke="#e2e8f0" stroke-width="1.1"/>
      <line x1="0" y1="0" x2="5" y2="0" stroke="#e2e8f0" stroke-width="1.1"/>
    </pattern>

    <!-- Patrón de aislamiento térmico SATE / XPS -->
    <pattern id="hatch-insulation" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M 0 4 Q 2 0 4 4 T 8 4" fill="none" stroke="#38bdf8" stroke-width="0.6" opacity="0.85"/>
    </pattern>

    <!-- Patrón de pavimento cerámico / porcelánico técnico (cuadrícula ortogonal fina) -->
    <pattern id="hatch-tile-60" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M 18 0 L 0 0 0 18" fill="none" stroke="#334155" stroke-width="0.45" opacity="0.6"/>
    </pattern>

    <!-- Patrón de tarima de madera (Iroko / Roble) -->
    <pattern id="hatch-wood-deck" width="40" height="6" patternUnits="userSpaceOnUse">
      <line x1="0" y1="6" x2="40" y2="6" stroke="#475569" stroke-width="0.45" opacity="0.65"/>
      <line x1="15" y1="0" x2="15" y2="6" stroke="#475569" stroke-width="0.35" opacity="0.5"/>
    </pattern>

    <!-- Patrón de terreno / grava drenante -->
    <pattern id="hatch-gravel" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="4" r="0.7" fill="#64748b" opacity="0.6"/>
      <circle cx="9" cy="3" r="0.9" fill="#64748b" opacity="0.5"/>
      <circle cx="6" cy="10" r="0.8" fill="#64748b" opacity="0.6"/>
      <circle cx="12" cy="11" r="0.6" fill="#64748b" opacity="0.5"/>
    </pattern>

    <!-- Patrón de lámina de agua (piscina) -->
    <pattern id="hatch-water" width="24" height="12" patternUnits="userSpaceOnUse">
      <path d="M 0 6 Q 6 3 12 6 T 24 6" fill="none" stroke="#0284c7" stroke-width="0.5" opacity="0.55"/>
    </pattern>

    <!-- Patrón de serpentín de suelo radiante PEX Ø16mm -->
    <pattern id="hatch-radiant" width="16" height="16" patternUnits="userSpaceOnUse">
      <path d="M 0 4 L 16 4 M 0 12 L 16 12" fill="none" stroke="#f43f5e" stroke-width="0.45" stroke-dasharray="3,2" opacity="0.45"/>
    </pattern>

    <!-- Marcadores de acotación arquitectónica (Trazo oblicuo a 45° ISO 129) -->
    <marker id="tick-45" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#38bdf8" stroke-width="1.2"/>
    </marker>
    <marker id="tick-45-amber" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#f59e0b" stroke-width="1.2"/>
    </marker>
    <marker id="tick-45-white" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#cbd5e1" stroke-width="1.1"/>
    </marker>
    <marker id="arrow-tech" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M 0 1 L 6 3.5 L 0 6 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrow-sec" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M 0 0.5 L 7 4 L 0 7.5 z" fill="#f43f5e"/>
    </marker>
  </defs>
"""


def fmt_m(val, decimals=2):
    """Formatea metros con coma decimal según norma española UNE."""
    return f"{val:.{decimals}f}".replace(".", ",")


def draw_structural_axis(x1, y1, x2, y2, label, bubble_at="start", col="#64748b"):
    """Dibuja un eje estructural de replanteo (línea de trazo y punto fino con círculo de código)."""
    out = [
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{col}" stroke-width="0.65" stroke-dasharray="14,4,2,4" opacity="0.75"/>'
    ]
    bx, by = (x1, y1) if bubble_at == "start" else (x2, y2)
    out.append(
        f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9.5" fill="#0b1120" stroke="{col}" stroke-width="1.1"/>'
        f'<text x="{bx:.1f}" y="{by + 3.2:.1f}" fill="#e2e8f0" font-family="monospace" '
        f'font-size="9" font-weight="700" text-anchor="middle">{label}</text>'
    )
    return "\n".join(out)


def draw_pillar(cx, cy, size_px=12, label=""):
    """Dibuja un pilar estructural (hormigón armado o HEB) con sombreado cruzado y ejes."""
    half = size_px / 2.0
    s = (
        f'<rect x="{cx - half:.1f}" y="{cy - half:.1f}" width="{size_px:.1f}" height="{size_px:.1f}" '
        f'fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>'
    )
    if label:
        s += (
            f'<text x="{cx + half + 3:.1f}" y="{cy - half - 2:.1f}" fill="#94a3b8" '
            f'font-family="monospace" font-size="6.5" font-weight="700">{label}</text>'
        )
    return s


def draw_wall_segment(x, y, w, h, kind="ext"):
    """
    Dibuja un tramo de muro arquitectónico:
    - 'ext': Muro de cerramiento multicapa (35-40 cm) con doble línea, cámara SATE y rayado ANSI31.
    - 'int': Tabique interior PYL/acústico (10-12 cm) con doble línea y relleno técnico.
    - 'acoustic': Tabique acústico de alta masa (Rw >= 50 dB) con línea central de lana mineral.
    """
    if kind == "ext":
        out = [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#1e293b" stroke="none"/>',
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="url(#hatch-ansi31)" stroke="#e2e8f0" stroke-width="1.35"/>',
        ]
        # Línea interior de hoja SATE / cámara (a 1/3 del espesor)
        if w > h and h >= 8:
            yi = y + h * 0.32
            out.append(f'<line x1="{x:.1f}" y1="{yi:.1f}" x2="{x + w:.1f}" y2="{yi:.1f}" stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="4,2"/>')
        elif h >= w and w >= 8:
            xi = x + w * 0.32
            out.append(f'<line x1="{xi:.1f}" y1="{y:.1f}" x2="{xi:.1f}" y2="{y + h:.1f}" stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="4,2"/>')
        return "\n".join(out)
    elif kind == "acoustic":
        out = [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>',
        ]
        if w > h:
            ym = y + h / 2.0
            out.append(f'<line x1="{x:.1f}" y1="{ym:.1f}" x2="{x + w:.1f}" y2="{ym:.1f}" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="3,2"/>')
        else:
            xm = x + w / 2.0
            out.append(f'<line x1="{xm:.1f}" y1="{y:.1f}" x2="{xm:.1f}" y2="{y + h:.1f}" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="3,2"/>')
        return "\n".join(out)
    else:
        return (
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'fill="#334155" stroke="#cbd5e1" stroke-width="0.95"/>'
        )


def draw_dim_h(x1, x2, y_wall, y_dim, text=None, scale=40.0, col="#38bdf8", marker="tick-45", font_size=7.5):
    """Dibuja una cota horizontal ISO 129 con líneas auxiliares de referencia y trazo a 45°."""
    if x2 < x1:
        x1, x2 = x2, x1
    val_m = (x2 - x1) / scale
    label = text if text is not None else fmt_m(val_m)
    ext_dir = -1 if y_dim < y_wall else 1
    y_start = y_wall + ext_dir * 3
    y_end = y_dim + ext_dir * 4
    mx = (x1 + x2) / 2.0
    tw = max(len(label) * (font_size * 0.62) + 6, 22)
    return f"""<g class="cad-dim">
      <line x1="{x1:.1f}" y1="{y_start:.1f}" x2="{x1:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="0.45" opacity="0.75"/>
      <line x1="{x2:.1f}" y1="{y_start:.1f}" x2="{x2:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="0.45" opacity="0.75"/>
      <line x1="{x1:.1f}" y1="{y_dim:.1f}" x2="{x2:.1f}" y2="{y_dim:.1f}" stroke="{col}" stroke-width="0.75" marker-start="url(#{marker})" marker-end="url(#{marker})"/>
      <rect x="{mx - tw/2:.1f}" y="{y_dim - font_size - 1.5:.1f}" width="{tw:.1f}" height="{font_size + 3:.1f}" fill="#0b1120" opacity="0.9"/>
      <text x="{mx:.1f}" y="{y_dim - 1.5:.1f}" fill="{col}" font-family="monospace" font-size="{font_size}" font-weight="700" text-anchor="middle">{label}</text>
    </g>"""


def draw_dim_v(y1, y2, x_wall, x_dim, text=None, scale=40.0, col="#38bdf8", marker="tick-45", font_size=7.5):
    """Dibuja una cota vertical ISO 129 con líneas auxiliares de referencia y texto rotado -90°."""
    if y2 < y1:
        y1, y2 = y2, y1
    val_m = (y2 - y1) / scale
    label = text if text is not None else fmt_m(val_m)
    ext_dir = -1 if x_dim < x_wall else 1
    x_start = x_wall + ext_dir * 3
    x_end = x_dim + ext_dir * 4
    my = (y1 + y2) / 2.0
    tw = max(len(label) * (font_size * 0.62) + 6, 22)
    return f"""<g class="cad-dim">
      <line x1="{x_start:.1f}" y1="{y1:.1f}" x2="{x_end:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="0.45" opacity="0.75"/>
      <line x1="{x_start:.1f}" y1="{y2:.1f}" x2="{x_end:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.45" opacity="0.75"/>
      <line x1="{x_dim:.1f}" y1="{y1:.1f}" x2="{x_dim:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.75" marker-start="url(#{marker})" marker-end="url(#{marker})"/>
      <g transform="translate({x_dim:.1f}, {my:.1f}) rotate(-90)">
        <rect x="{-tw/2:.1f}" y="{-font_size - 1.5:.1f}" width="{tw:.1f}" height="{font_size + 3:.1f}" fill="#0b1120" opacity="0.9"/>
        <text x="0" y="-1.5" fill="{col}" font-family="monospace" font-size="{font_size}" font-weight="700" text-anchor="middle">{label}</text>
      </g>
    </g>"""


def draw_door_swing(hinge_x, hinge_y, length_px, WallDir, SwingDir, code="", dim_txt=""):
    """
    Dibuja una puerta batiente CAD con hoja de espesor real (2 líneas), jambas y arco de 90°:
    WallDir: 'E' (hueco hacia +X), 'W' (hueco hacia -X), 'S' (hueco hacia +Y), 'N' (hueco hacia -Y)
    SwingDir: 'N', 'S', 'E', 'W' (hacia dónde abre la hoja)
    """
    dx_open, dy_open = 0.0, 0.0
    if SwingDir == "E":
        dx_open = length_px
    elif SwingDir == "W":
        dx_open = -length_px
    elif SwingDir == "S":
        dy_open = length_px
    elif SwingDir == "N":
        dy_open = -length_px

    dx_closed, dy_closed = 0.0, 0.0
    if WallDir == "E":
        dx_closed = length_px
    elif WallDir == "W":
        dx_closed = -length_px
    elif WallDir == "S":
        dy_closed = length_px
    elif WallDir == "N":
        dy_closed = -length_px

    open_x = hinge_x + dx_open
    open_y = hinge_y + dy_open
    closed_x = hinge_x + dx_closed
    closed_y = hinge_y + dy_closed

    # Determinar sweep-flag del arco entre (closed_x, closed_y) y (open_x, open_y) con centro en (hinge_x, hinge_y)
    cross = dx_closed * dy_open - dy_closed * dx_open
    sweep = 1 if cross > 0 else 0

    # Grosor de hoja de puerta perpendicular a SwingDir
    tx, ty = 0.0, 0.0
    if SwingDir in ("N", "S"):
        tx = 2.5 if WallDir == "E" else -2.5
    else:
        ty = 2.5 if WallDir == "S" else -2.5

    s = [
        f'<g class="cad-door">',
        # Hoja de puerta (rectángulo de espesor real)
        f'<polygon points="{hinge_x:.1f},{hinge_y:.1f} {open_x:.1f},{open_y:.1f} '
        f'{open_x + tx:.1f},{open_y + ty:.1f} {hinge_x + tx:.1f},{hinge_y + ty:.1f}" '
        f'fill="#0b1120" stroke="#f8fafc" stroke-width="1.0"/>',
        # Arco de abatimiento 90°
        f'<path d="M {closed_x:.1f} {closed_y:.1f} A {length_px:.1f} {length_px:.1f} 0 0 {sweep} {open_x:.1f} {open_y:.1f}" '
        f'fill="none" stroke="#94a3b8" stroke-width="0.65" stroke-dasharray="3,2"/>',
    ]
    if code:
        mx = hinge_x + (dx_closed + dx_open) * 0.38
        my = hinge_y + (dy_closed + dy_open) * 0.38
        s.append(
            f'<text x="{mx:.1f}" y="{my:.1f}" fill="#f59e0b" font-family="monospace" '
            f'font-size="6.5" font-weight="700" text-anchor="middle">{code}</text>'
        )
    if dim_txt:
        mx = hinge_x + (dx_closed + dx_open) * 0.38
        my = hinge_y + (dy_closed + dy_open) * 0.38 + 7
        s.append(
            f'<text x="{mx:.1f}" y="{my:.1f}" fill="#cbd5e1" font-family="monospace" '
            f'font-size="5.8" text-anchor="middle">{dim_txt}</text>'
        )
    s.append("</g>")
    return "\n".join(s)


def draw_sliding_door(x1, y1, x2, y2, wall_thick=10, leaves=2, code="", dim_txt=""):
    """Dibuja una carpintería corredera elevable o puerta corredera empotrada con hojas solapadas y flechas de apertura."""
    is_horiz = abs(x2 - x1) >= abs(y2 - y1)
    s = ['<g class="cad-sliding">']
    if is_horiz:
        xa, xb = min(x1, x2), max(x1, x2)
        L = xb - xa
        y = y1
        # Marco/hueco limpio
        s.append(f'<rect x="{xa:.1f}" y="{y - wall_thick/2:.1f}" width="{L:.1f}" height="{wall_thick:.1f}" fill="#0b1120" stroke="#64748b" stroke-width="0.6"/>')
        # Carriles y hojas de vidrio
        s.append(f'<line x1="{xa:.1f}" y1="{y - 1.8:.1f}" x2="{xa + L*0.55:.1f}" y2="{y - 1.8:.1f}" stroke="#38bdf8" stroke-width="1.6"/>')
        s.append(f'<line x1="{xa + L*0.45:.1f}" y1="{y + 1.8:.1f}" x2="{xb:.1f}" y2="{y + 1.8:.1f}" stroke="#38bdf8" stroke-width="1.6"/>')
        # Jambas laterales
        s.append(f'<rect x="{xa:.1f}" y="{y - wall_thick/2:.1f}" width="3" height="{wall_thick:.1f}" fill="#e2e8f0"/>')
        s.append(f'<rect x="{xb - 3:.1f}" y="{y - wall_thick/2:.1f}" width="3" height="{wall_thick:.1f}" fill="#e2e8f0"/>')
        if code:
            s.append(f'<text x="{(xa+xb)/2:.1f}" y="{y - wall_thick/2 - 3:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{code} {dim_txt}</text>')
    else:
        ya, yb = min(y1, y2), max(y1, y2)
        L = yb - ya
        x = x1
        s.append(f'<rect x="{x - wall_thick/2:.1f}" y="{ya:.1f}" width="{wall_thick:.1f}" height="{L:.1f}" fill="#0b1120" stroke="#64748b" stroke-width="0.6"/>')
        s.append(f'<line x1="{x - 1.8:.1f}" y1="{ya:.1f}" x2="{x - 1.8:.1f}" y2="{ya + L*0.55:.1f}" stroke="#38bdf8" stroke-width="1.6"/>')
        s.append(f'<line x1="{x + 1.8:.1f}" y1="{ya + L*0.45:.1f}" x2="{x + 1.8:.1f}" y2="{yb:.1f}" stroke="#38bdf8" stroke-width="1.6"/>')
        s.append(f'<rect x="{x - wall_thick/2:.1f}" y="{ya:.1f}" width="{wall_thick:.1f}" height="3" fill="#e2e8f0"/>')
        s.append(f'<rect x="{x - wall_thick/2:.1f}" y="{yb - 3:.1f}" width="{wall_thick:.1f}" height="3" fill="#e2e8f0"/>')
        if code:
            s.append(
                f'<g transform="translate({x - wall_thick/2 - 3:.1f}, {(ya+yb)/2:.1f}) rotate(-90)">'
                f'<text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{code} {dim_txt}</text>'
                f'</g>'
            )
    s.append("</g>")
    return "\n".join(s)


def draw_window_cad(x1, y1, x2, y2, wall_thick=14, code="", dim_txt=""):
    """Dibuja una ventana técnica CAD con jambas, alféizar exterior e interior y triple vidrio."""
    is_horiz = abs(x2 - x1) >= abs(y2 - y1)
    s = ['<g class="cad-window">']
    if is_horiz:
        xa, xb = min(x1, x2), max(x1, x2)
        L = xb - xa
        y = y1
        s.append(f'<rect x="{xa:.1f}" y="{y - wall_thick/2:.1f}" width="{L:.1f}" height="{wall_thick:.1f}" fill="#0b1120" stroke="#cbd5e1" stroke-width="0.8"/>')
        s.append(f'<line x1="{xa:.1f}" y1="{y - 1.8:.1f}" x2="{xb:.1f}" y2="{y - 1.8:.1f}" stroke="#38bdf8" stroke-width="1.1"/>')
        s.append(f'<line x1="{xa:.1f}" y1="{y + 1.8:.1f}" x2="{xb:.1f}" y2="{y + 1.8:.1f}" stroke="#38bdf8" stroke-width="1.1"/>')
        s.append(f'<line x1="{(xa+xb)/2:.1f}" y1="{y - wall_thick/2:.1f}" x2="{(xa+xb)/2:.1f}" y2="{y + wall_thick/2:.1f}" stroke="#cbd5e1" stroke-width="0.8"/>')
        if code:
            s.append(f'<text x="{(xa+xb)/2:.1f}" y="{y - wall_thick/2 - 3:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{code} {dim_txt}</text>')
    else:
        ya, yb = min(y1, y2), max(y1, y2)
        L = yb - ya
        x = x1
        s.append(f'<rect x="{x - wall_thick/2:.1f}" y="{ya:.1f}" width="{wall_thick:.1f}" height="{L:.1f}" fill="#0b1120" stroke="#cbd5e1" stroke-width="0.8"/>')
        s.append(f'<line x1="{x - 1.8:.1f}" y1="{ya:.1f}" x2="{x - 1.8:.1f}" y2="{yb:.1f}" stroke="#38bdf8" stroke-width="1.1"/>')
        s.append(f'<line x1="{x + 1.8:.1f}" y1="{ya:.1f}" x2="{x + 1.8:.1f}" y2="{yb:.1f}" stroke="#38bdf8" stroke-width="1.1"/>')
        s.append(f'<line x1="{x - wall_thick/2:.1f}" y1="{(ya+yb)/2:.1f}" x2="{x + wall_thick/2:.1f}" y2="{(ya+yb)/2:.1f}" stroke="#cbd5e1" stroke-width="0.8"/>')
        if code:
            s.append(
                f'<g transform="translate({x - wall_thick/2 - 3:.1f}, {(ya+yb)/2:.1f}) rotate(-90)">'
                f'<text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{code} {dim_txt}</text>'
                f'</g>'
            )
    s.append("</g>")
    return "\n".join(s)


def draw_room_stamp(cx, cy, code, name, area_m2, pav_txt, z_txt="±0,00"):
    """Dibuja el sello técnico de estancia (código, nombre, superficie útil, pavimento y cota Z)."""
    return f"""<g class="room-stamp">
      <rect x="{cx - 48:.1f}" y="{cy - 18:.1f}" width="96" height="35" rx="1.5" fill="#0b1120" fill-opacity="0.88" stroke="#475569" stroke-width="0.7"/>
      <line x1="{cx - 48:.1f}" y1="{cy - 6:.1f}" x2="{cx + 48:.1f}" y2="{cy - 6:.1f}" stroke="#334155" stroke-width="0.6"/>
      <text x="{cx:.1f}" y="{cy - 9:.1f}" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">[{code}] {name}</text>
      <text x="{cx:.1f}" y="{cy + 3:.1f}" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">S.Útil: {fmt_m(area_m2)} m²</text>
      <text x="{cx:.1f}" y="{cy + 12.5:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{pav_txt} · Z={z_txt}m</text>
    </g>"""


def draw_nhg_circle(cx, cy, diam_m, scale, label="Ø1,50m NHG"):
    """Dibuja el círculo reglamentario de inscripción libre según Normas do Hábitat Galego (Decreto 29/2010)."""
    r = (diam_m * scale) / 2.0
    return f"""<g class="nhg-circle" opacity="0.65">
      <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#10b981" stroke-width="0.7" stroke-dasharray="4,3"/>
      <line x1="{cx - 4:.1f}" y1="{cy:.1f}" x2="{cx + 4:.1f}" y2="{cy:.1f}" stroke="#10b981" stroke-width="0.5"/>
      <line x1="{cx:.1f}" y1="{cy - 4:.1f}" x2="{cx:.1f}" y2="{cy + 4:.1f}" stroke="#10b981" stroke-width="0.5"/>
      <text x="{cx:.1f}" y="{cy + r - 3:.1f}" fill="#10b981" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="middle">{label}</text>
    </g>"""


def draw_wc_block(x, y, w, h, orient="N"):
    """Dibuja un inodoro suspendido Geberit en planta CAD (cisterna oculta + taza ovalada + pulsador)."""
    s = [f'<g class="cad-sanitary" stroke="#cbd5e1" stroke-width="0.85" fill="#0f172a">']
    if orient == "N":
        # Adosado a pared Norte (y arriba)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h*0.22:.1f}" fill="#1e293b"/>')
        s.append(f'<path d="M {x + w*0.1:.1f} {y + h*0.22:.1f} L {x + w*0.9:.1f} {y + h*0.22:.1f} Q {x + w*0.95:.1f} {y + h:.1f} {x + w*0.5:.1f} {y + h:.1f} Q {x + w*0.05:.1f} {y + h:.1f} {x + w*0.1:.1f} {y + h*0.22:.1f} Z"/>')
        s.append(f'<ellipse cx="{x + w*0.5:.1f}" cy="{y + h*0.62:.1f}" rx="{w*0.28:.1f}" ry="{h*0.25:.1f}" fill="none" stroke="#64748b" stroke-width="0.6"/>')
    elif orient == "S":
        s.append(f'<rect x="{x:.1f}" y="{y + h*0.78:.1f}" width="{w:.1f}" height="{h*0.22:.1f}" fill="#1e293b"/>')
        s.append(f'<path d="M {x + w*0.1:.1f} {y + h*0.78:.1f} L {x + w*0.9:.1f} {y + h*0.78:.1f} Q {x + w*0.95:.1f} {y:.1f} {x + w*0.5:.1f} {y:.1f} Q {x + w*0.05:.1f} {y:.1f} {x + w*0.1:.1f} {y + h*0.78:.1f} Z"/>')
        s.append(f'<ellipse cx="{x + w*0.5:.1f}" cy="{y + h*0.38:.1f}" rx="{w*0.28:.1f}" ry="{h*0.25:.1f}" fill="none" stroke="#64748b" stroke-width="0.6"/>')
    elif orient == "E":
        s.append(f'<rect x="{x + w*0.78:.1f}" y="{y:.1f}" width="{w*0.22:.1f}" height="{h:.1f}" fill="#1e293b"/>')
        s.append(f'<ellipse cx="{x + w*0.38:.1f}" cy="{y + h*0.5:.1f}" rx="{w*0.36:.1f}" ry="{h*0.38:.1f}"/>')
    else:
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w*0.22:.1f}" height="{h:.1f}" fill="#1e293b"/>')
        s.append(f'<ellipse cx="{x + w*0.62:.1f}" cy="{y + h*0.5:.1f}" rx="{w*0.36:.1f}" ry="{h*0.38:.1f}"/>')
    s.append("</g>")
    return "\n".join(s)


def draw_sink_block(x, y, w, h, basins=1, orient="N"):
    """Dibuja un mueble de lavabo suspendido con 1 o 2 senos, desagüe y grifería empotrada."""
    s = [
        f'<g class="cad-sanitary" stroke="#cbd5e1" stroke-width="0.85" fill="#0f172a">',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1"/>',
    ]
    if basins == 1:
        cx, cy = x + w * 0.5, y + h * 0.52
        rx, ry = w * 0.34, h * 0.32
        s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>')
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.5" fill="#38bdf8"/>')
    else:
        for f in (0.27, 0.73):
            cx, cy = x + w * f, y + h * 0.52
            rx, ry = w * 0.18, h * 0.32
            s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>')
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.5" fill="#38bdf8"/>')
    s.append("</g>")
    return "\n".join(s)


def draw_shower_block(x, y, w, h, drain_side="E", label="DUCHA COTA 0 (p=2%)"):
    """Dibuja un plato de ducha walk-in a cota cero con líneas de pendiente al 2%, sumidero lineal y mampara 8mm."""
    dx = x + w - 4 if drain_side == "E" else x + 4
    cy = y + h / 2.0
    return f"""<g class="cad-shower">
      <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#0f172a" stroke="#64748b" stroke-width="0.8"/>
      <!-- Líneas de caída de pendiente 2% hacia sumidero lineal -->
      <line x1="{x:.1f}" y1="{y:.1f}" x2="{dx:.1f}" y2="{y + 3:.1f}" stroke="#475569" stroke-width="0.5" stroke-dasharray="3,2"/>
      <line x1="{x:.1f}" y1="{y + h:.1f}" x2="{dx:.1f}" y2="{y + h - 3:.1f}" stroke="#475569" stroke-width="0.5" stroke-dasharray="3,2"/>
      <line x1="{x + w*0.15:.1f}" y1="{cy:.1f}" x2="{dx - 3:.1f}" y2="{cy:.1f}" stroke="#38bdf8" stroke-width="0.6" marker-end="url(#arrow-tech)"/>
      <!-- Sumidero lineal oculto AISI 316 -->
      <rect x="{dx - 1.5:.1f}" y="{y + 3:.1f}" width="3" height="{h - 6:.1f}" fill="#38bdf8" opacity="0.8"/>
      <!-- Rociador cenital Ø25cm -->
      <circle cx="{x + w*0.5:.1f}" cy="{cy:.1f}" r="5" fill="none" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="2,1"/>
      <text x="{x + w*0.45:.1f}" y="{y + h - 3:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{label}</text>
    </g>"""


def draw_bed_block(x, y, w, h, orient="N", kind="double", label=""):
    """Dibuja una cama técnica CAD con cabecero, almohadas, pliegue de sábana y cotas."""
    s = [f'<g class="cad-bed" stroke="#94a3b8" stroke-width="0.8" fill="#0f172a">']
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1.5"/>')
    if orient == "N":
        # Cabecero al Norte (arriba)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h*0.07:.1f}" fill="#334155"/>')
        if kind == "double":
            s.append(f'<rect x="{x + w*0.08:.1f}" y="{y + h*0.10:.1f}" width="{w*0.38:.1f}" height="{h*0.16:.1f}" rx="1.5" fill="#1e293b"/>')
            s.append(f'<rect x="{x + w*0.54:.1f}" y="{y + h*0.10:.1f}" width="{w*0.38:.1f}" height="{h*0.16:.1f}" rx="1.5" fill="#1e293b"/>')
        else:
            s.append(f'<rect x="{x + w*0.12:.1f}" y="{y + h*0.10:.1f}" width="{w*0.76:.1f}" height="{h*0.16:.1f}" rx="1.5" fill="#1e293b"/>')
        s.append(f'<line x1="{x:.1f}" y1="{y + h*0.32:.1f}" x2="{x + w:.1f}" y2="{y + h*0.32:.1f}" stroke="#64748b" stroke-width="0.6"/>')
    elif orient == "W":
        # Cabecero al Oeste (izquierda)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w*0.07:.1f}" height="{h:.1f}" fill="#334155"/>')
        s.append(f'<rect x="{x + w*0.10:.1f}" y="{y + h*0.12:.1f}" width="{w*0.16:.1f}" height="{h*0.76:.1f}" rx="1.5" fill="#1e293b"/>')
        s.append(f'<line x1="{x + w*0.32:.1f}" y1="{y:.1f}" x2="{x + w*0.32:.1f}" y2="{y + h:.1f}" stroke="#64748b" stroke-width="0.6"/>')
    if label:
        s.append(f'<text x="{x + w/2:.1f}" y="{y + h*0.68:.1f}" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">{label}</text>')
    s.append("</g>")
    return "\n".join(s)


def draw_wardrobe_block(x, y, w, h, label="ARMARIO H=2,60m"):
    """Dibuja un armario empotrado en planta CAD (líneas diagonales cruzadas / barra de colgar)."""
    is_horiz = w >= h
    s = [
        f'<g class="cad-wardrobe" stroke="#94a3b8" stroke-width="0.75" fill="#131c31">',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>',
        f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + w:.1f}" y2="{y + h:.1f}" stroke="#475569" stroke-width="0.45"/>',
        f'<line x1="{x + w:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y + h:.1f}" stroke="#475569" stroke-width="0.45"/>',
    ]
    if is_horiz:
        s.append(f'<line x1="{x + 3:.1f}" y1="{y + h/2:.1f}" x2="{x + w - 3:.1f}" y2="{y + h/2:.1f}" stroke="#64748b" stroke-width="0.6" stroke-dasharray="2,2"/>')
        s.append(f'<text x="{x + w/2:.1f}" y="{y + h/2 + 2:.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.5" text-anchor="middle">{label}</text>')
    else:
        s.append(f'<line x1="{x + w/2:.1f}" y1="{y + 3:.1f}" x2="{x + w/2:.1f}" y2="{y + h - 3:.1f}" stroke="#64748b" stroke-width="0.6" stroke-dasharray="2,2"/>')
        s.append(
            f'<g transform="translate({x + w/2 + 2:.1f}, {y + h/2:.1f}) rotate(-90)">'
            f'<text x="0" y="0" fill="#cbd5e1" font-family="monospace" font-size="5.5" text-anchor="middle">{label}</text>'
            f'</g>'
        )
    s.append("</g>")
    return "\n".join(s)


def draw_mep_symbol(cx, cy, kind, code="", h_cm=None):
    """
    Dibuja símbolos normalizados de instalaciones (REBT / CTE):
    - 'schuko': Base de enchufe 16A con toma de tierra lateral
    - 'rj45': Toma doble de datos Cat 6A
    - 'switch': Interruptor / conmutador unipolar
    - 'vmc_imp': Boca de impulsión VMC (aire nuevo)
    - 'vmc_ext': Boca de extracción VMC (aire viciado)
    - 'thermostat': Termostato digital zonal
    - 'downlight': Punto de luz cenital LED
    - 'drain': Bajante / sumidero sanitario Ø110 / Ø50
    """
    lbl = code + (f" (h={h_cm})" if h_cm else "")
    if kind == "schuko":
        return f"""<g class="mep-sym">
          <circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2" fill="#0b1120" stroke="#f59e0b" stroke-width="1.1"/>
          <line x1="{cx - 4.2:.1f}" y1="{cy:.1f}" x2="{cx + 4.2:.1f}" y2="{cy:.1f}" stroke="#f59e0b" stroke-width="0.8"/>
          <text x="{cx + 6:.1f}" y="{cy + 2:.1f}" fill="#f59e0b" font-family="monospace" font-size="5.5" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "rj45":
        return f"""<g class="mep-sym">
          <polygon points="{cx:.1f},{cy-4.5:.1f} {cx+4.5:.1f},{cy+3.5:.1f} {cx-4.5:.1f},{cy+3.5:.1f}" fill="#0b1120" stroke="#a855f7" stroke-width="1.1"/>
          <text x="{cx + 6:.1f}" y="{cy + 2:.1f}" fill="#c084fc" font-family="monospace" font-size="5.5" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "switch":
        return f"""<g class="mep-sym">
          <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
          <line x1="{cx:.1f}" y1="{cy - 3.5:.1f}" x2="{cx + 4.5:.1f}" y2="{cy - 7:.1f}" stroke="#38bdf8" stroke-width="1.0"/>
          <text x="{cx + 6:.1f}" y="{cy + 2:.1f}" fill="#38bdf8" font-family="monospace" font-size="5.5" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "vmc_imp":
        return f"""<g class="mep-sym">
          <circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="#0b1120" stroke="#10b981" stroke-width="1.1"/>
          <path d="M {cx-3:.1f} {cy:.1f} L {cx+3:.1f} {cy:.1f} M {cx:.1f} {cy-3:.1f} L {cx:.1f} {cy+3:.1f}" stroke="#10b981" stroke-width="0.8"/>
          <text x="{cx + 7:.1f}" y="{cy + 2:.1f}" fill="#10b981" font-family="monospace" font-size="5.8" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "vmc_ext":
        return f"""<g class="mep-sym">
          <rect x="{cx - 5:.1f}" y="{cy - 5:.1f}" width="10" height="10" fill="#0b1120" stroke="#06b6d4" stroke-width="1.1"/>
          <line x1="{cx - 5:.1f}" y1="{cy - 5:.1f}" x2="{cx + 5:.1f}" y2="{cy + 5:.1f}" stroke="#06b6d4" stroke-width="0.8"/>
          <text x="{cx + 7:.1f}" y="{cy + 2:.1f}" fill="#22d3ee" font-family="monospace" font-size="5.8" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "thermostat":
        return f"""<g class="mep-sym">
          <rect x="{cx - 4.5:.1f}" y="{cy - 4.5:.1f}" width="9" height="9" fill="#0b1120" stroke="#f43f5e" stroke-width="1.1"/>
          <text x="{cx:.1f}" y="{cy + 2.5:.1f}" fill="#f43f5e" font-family="monospace" font-size="5.8" font-weight="700" text-anchor="middle">T</text>
          <text x="{cx + 6.5:.1f}" y="{cy + 2:.1f}" fill="#fb7185" font-family="monospace" font-size="5.5" font-weight="700">{lbl}</text>
        </g>"""
    elif kind == "drain":
        return f"""<g class="mep-sym">
          <circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#0b1120" stroke="#ef4444" stroke-width="1.2"/>
          <circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.8" fill="#ef4444"/>
          <text x="{cx + 6:.1f}" y="{cy + 2:.1f}" fill="#fca5a5" font-family="monospace" font-size="5.5" font-weight="700">{lbl}</text>
        </g>"""
    return ""


def draw_north_rose_and_scale(x, y, scale_px_per_m=40.0, scale_label="1:100"):
    """Dibuja la rosa náutica técnica (con indicación de vientos dominantes SW y Nordés NE) y barra de escala gráfica."""
    m1 = scale_px_per_m
    m2 = scale_px_per_m * 2
    m5 = scale_px_per_m * 5
    return f"""<g transform="translate({x:.1f}, {y:.1f})">
      <!-- Rosa de los vientos técnica -->
      <circle cx="0" cy="0" r="24" fill="#0b1120" stroke="#475569" stroke-width="1.0"/>
      <circle cx="0" cy="0" r="18" fill="none" stroke="#334155" stroke-width="0.6" stroke-dasharray="2,2"/>
      <line x1="-26" y1="0" x2="26" y2="0" stroke="#475569" stroke-width="0.6"/>
      <line x1="0" y1="-26" x2="0" y2="26" stroke="#475569" stroke-width="0.6"/>
      <!-- Aguja Norte -->
      <polygon points="0,-23 5,-4 0,-8 -5,-4" fill="#38bdf8"/>
      <polygon points="0,23 4,4 0,8 -4,4" fill="#475569"/>
      <text x="0" y="-27" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">N (0°)</text>
      <text x="31" y="3" fill="#64748b" font-family="monospace" font-size="6.5" text-anchor="start">E</text>
      <text x="-31" y="3" fill="#64748b" font-family="monospace" font-size="6.5" text-anchor="end">W</text>
      <text x="0" y="34" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">S (SOL)</text>
      <!-- Viento Nordés NE -->
      <line x1="22" y1="-22" x2="10" y2="-10" stroke="#38bdf8" stroke-width="0.8" marker-end="url(#arrow-tech)"/>
      <text x="24" y="-24" fill="#38bdf8" font-family="monospace" font-size="5.5">Nordés NE</text>
      <!-- Escala gráfica -->
      <g transform="translate(-45, 48)">
        <text x="45" y="-5" fill="#cbd5e1" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ESCALA GRÁFICA {scale_label}</text>
        <rect x="0" y="0" width="{m1:.1f}" height="4.5" fill="#38bdf8" stroke="#cbd5e1" stroke-width="0.5"/>
        <rect x="{m1:.1f}" y="0" width="{m1:.1f}" height="4.5" fill="#0b1120" stroke="#cbd5e1" stroke-width="0.5"/>
        <rect x="{m2:.1f}" y="0" width="{m1:.1f}" height="4.5" fill="#38bdf8" stroke="#cbd5e1" stroke-width="0.5"/>
        <text x="0" y="13" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">0</text>
        <text x="{m1:.1f}" y="13" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">1m</text>
        <text x="{m2:.1f}" y="13" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">2m</text>
        <text x="{m1*3:.1f}" y="13" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">3m</text>
      </g>
    </g>"""


def draw_iso_title_block(x, y, w, h, sheet_num, sheet_title, scale_txt, subtitle, summary_rows):
    """
    Dibuja un cajetín técnico normalizado UNE-EN ISO 7200 en la parte inferior del plano.
    """
    c1 = w * 0.34
    c2 = w * 0.68
    c3 = w * 0.85
    out = [
        f'<g class="iso-title-block" transform="translate({x:.1f}, {y:.1f})">',
        f'<rect x="0" y="0" width="{w:.1f}" height="{h:.1f}" fill="#090e1a" stroke="#cbd5e1" stroke-width="1.3"/>',
        # Divisiones verticales del cajetín
        f'<line x1="{c1:.1f}" y1="0" x2="{c1:.1f}" y2="{h:.1f}" stroke="#64748b" stroke-width="0.8"/>',
        f'<line x1="{c2:.1f}" y1="0" x2="{c2:.1f}" y2="{h:.1f}" stroke="#64748b" stroke-width="0.8"/>',
        f'<line x1="{c3:.1f}" y1="0" x2="{c3:.1f}" y2="{h:.1f}" stroke="#64748b" stroke-width="0.8"/>',
        f'<line x1="0" y1="{h*0.48:.1f}" x2="{c1:.1f}" y2="{h*0.48:.1f}" stroke="#334155" stroke-width="0.6"/>',
        f'<line x1="{c2:.1f}" y1="{h*0.50:.1f}" x2="{w:.1f}" y2="{h*0.50:.1f}" stroke="#334155" stroke-width="0.6"/>',
        # Bloque 1: Proyecto y Promotor
        f'<text x="10" y="13" fill="#64748b" font-family="monospace" font-size="6.5" font-weight="700">PROYECTO DE EJECUCIÓN · VIVIENDA UNIFAMILIAR AISLADA PASSIVHAUS</text>',
        f'<text x="10" y="25" fill="#f8fafc" font-family="monospace" font-size="9.5" font-weight="700">PABELLÓN BIOCLIMÁTICO ATLÁNTICO — PROPUESTA D</text>',
        f'<text x="10" y="{h*0.48 + 13:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.8">EMPLAZAMIENTO: Liáns / Santa Cruz · Concello de Oleiros (A Coruña) · Clima C1</text>',
        f'<text x="10" y="{h*0.48 + 25:.1f}" fill="#10b981" font-family="monospace" font-size="6.8" font-weight="700">NORMATIVA: PGOM Oleiros Ord. 2B (Ocup. ≤ 20%) · Decreto 29/2010 NHG · CTE DB-HE/HS6</text>',
        # Bloque 2: Cuadro resumen / notas técnicas
        f'<text x="{c1 + 10:.1f}" y="13" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700">ESPECIFICACIONES Y PARÁMETROS GEOMÉTRICOS DE HOJA</text>',
    ]
    for idx, r_txt in enumerate(summary_rows[:4]):
        out.append(
            f'<text x="{c1 + 10:.1f}" y="{25 + idx*11.5:.1f}" fill="#cbd5e1" font-family="monospace" font-size="6.5">{r_txt}</text>'
        )
    # Bloque 3: Título del plano
    out.extend([
        f'<text x="{c2 + 8:.1f}" y="12" fill="#64748b" font-family="monospace" font-size="6">TÍTULO DEL PLANO:</text>',
        f'<text x="{c2 + 8:.1f}" y="24" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">{sheet_title}</text>',
        f'<text x="{c2 + 8:.1f}" y="{h*0.50 + 12:.1f}" fill="#64748b" font-family="monospace" font-size="6">SUBTÍTULO / CONTENIDO:</text>',
        f'<text x="{c2 + 8:.1f}" y="{h*0.50 + 23:.1f}" fill="#e2e8f0" font-family="monospace" font-size="6.5">{subtitle}</text>',
        # Bloque 4: Número de plano, escala, fecha
        f'<text x="{c3 + 8:.1f}" y="12" fill="#64748b" font-family="monospace" font-size="6">PLANO Nº:</text>',
        f'<text x="{w - 8:.1f}" y="25" fill="#f59e0b" font-family="monospace" font-size="11" font-weight="700" text-anchor="end">{sheet_num}</text>',
        f'<text x="{c3 + 8:.1f}" y="{h*0.50 + 12:.1f}" fill="#64748b" font-family="monospace" font-size="6">ESCALA / FECHA:</text>',
        f'<text x="{w - 8:.1f}" y="{h*0.50 + 23:.1f}" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="end">{scale_txt} · NOV 2026</text>',
        '</g>'
    ])
    return "\n".join(out)


def sanitize_svg_text(svg_str: str) -> str:
    import re
    def repl(m):
        open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
        content = content.replace('&amp;', '&').replace('&', '&amp;').replace('<=', '≤').replace('>=', '≥').replace('<', '&lt;').replace('>', '&gt;')
        return f'{open_tag}{content}{close_tag}'
    return re.sub(r'(<text[^>]*>)(.*?)(</text>)', repl, svg_str, flags=re.DOTALL)



# ==============================================================================
# HIGH-LEVEL WRAPPERS FOR 1:50 & 1:20 EXECUTION PLANS
# ==============================================================================
def svg_defs():
    return cad_defs()

def draw_grid_axes(x_axes, y_axes, x_min_px, x_max_px, y_min_px, y_max_px, px_fn, py_fn):
    out = ['<g class="structural-axes">']
    for code, xm in x_axes:
        x = px_fn(xm)
        out.append(draw_structural_axis(x, y_min_px, x, y_max_px, code, bubble_at="start"))
    for code, ym in y_axes:
        y = py_fn(ym)
        out.append(draw_structural_axis(x_min_px, y, x_max_px, y, code, bubble_at="start"))
    out.append('</g>')
    return "\n".join(out)

def draw_pillars(coords_m, px_fn, py_fn, size_m=0.25, scale=75.0):
    sz = max(size_m * scale, 10.0)
    return "\n".join(draw_pillar(px_fn(xm), py_fn(ym), sz) for xm, ym in coords_m)

def draw_wall(x1, y1, x2, y2, thick_px=16.0, is_ext=True):
    kind = 'ext' if is_ext else 'int'
    if abs(x2 - x1) >= abs(y2 - y1):
        xa, xb = min(x1, x2), max(x1, x2)
        return draw_wall_segment(xa, y1 - thick_px/2.0, xb - xa, thick_px, kind=kind)
    else:
        ya, yb = min(y1, y2), max(y1, y2)
        return draw_wall_segment(x1 - thick_px/2.0, ya, thick_px, yb - ya, kind=kind)

def dim_h(x1, x2, y_ref, offset_dy, text, col='#38bdf8'):
    return draw_dim_h(x1, x2, y_ref, y_ref + offset_dy, text=text, col=col, font_size=6.8)

def dim_v(y1, y2, x_ref, offset_dx, text, col='#38bdf8'):
    return draw_dim_v(y1, y2, x_ref, x_ref + offset_dx, text=text, col=col, font_size=6.8)

def door_swing(x, y, len_px, open_dir='down', wall_dir='right', label=''):
    dir_map = {'up': 'N', 'down': 'S', 'left': 'W', 'right': 'E'}
    return draw_door_swing(x, y, len_px, dir_map.get(wall_dir, 'E'), dir_map.get(open_dir, 'S'), code=label)

def sliding_door(x, y, len_px, thick_px=12.0, orient='h', leaves=2, label=''):
    if orient == 'h':
        return draw_sliding_door(x, y, x + len_px, y, wall_thick=thick_px, leaves=leaves, code=label)
    else:
        return draw_sliding_door(x, y, x, y + len_px, wall_thick=thick_px, leaves=leaves, code=label)

def window_cad(x, y, len_px, thick_px=16.0, orient='h', label=''):
    if orient == 'h':
        return draw_window_cad(x, y, x + len_px, y, wall_thick=thick_px, code=label)
    else:
        return draw_window_cad(x, y, x, y + len_px, wall_thick=thick_px, code=label)

def room_stamp(cx, cy, title, area_m2, subtitle='', code='E-00'):
    return draw_room_stamp(cx, cy, code, title, area_m2, subtitle, '±0,00')

def nhg_circle(cx, cy, scale=75.0, label='Ø1,50m NHG'):
    return draw_nhg_circle(cx, cy, 1.50, scale, label)

def wc_cad(x, y, w, h, orient='left'):
    omap = {'up': 'N', 'down': 'S', 'left': 'E', 'right': 'W'}
    return draw_wc_block(x, y, w, h, orient=omap.get(orient, 'N'))

def sink_cad(x, y, w, h, double=False):
    return draw_sink_block(x, y, w, h, basins=2 if double else 1)

def shower_cad(x, y, w, h):
    return draw_shower_block(x, y, w, h)

def bed_cad(x, y, w, h, orient='N', double=True, label=''):
    return draw_bed_block(x, y, w, h, orient=orient, kind='double' if double else 'single', label=label)

def wardrobe_cad(x, y, w, h, orient='h', label='ARMARIO H=2,60m'):
    return draw_wardrobe_block(x, y, w, h, label=label)

def mep_symbol(cx, cy, kind, label=''):
    return draw_mep_symbol(cx, cy, kind, code=label)

def north_and_scale(x, y, scale_px=75.0, max_m=5):
    return draw_north_rose_and_scale(x, y, scale_px_per_m=scale_px, scale_label='1:50')

def title_block(x, y, w, h, plano_id, title, scale, phase, subtitle, extra_notes):
    return draw_iso_title_block(x, y, w, h, plano_id, title, scale, subtitle, extra_notes)
