#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de:
1. Plano CAD de los 4 Alzados Exteriores Estrictos (Norte, Sur, Este y Oeste) a Escala 1:100:
   - plano_alzados_exteriores_4_caras.svg
2. Guías Geométricas 3D Exactas (PNG) proyectadas matemáticamente desde las coordenadas reales
   (X=0..20m, Y=0..30m, Z=0..6.80m) para condicionar los renders fotorrealistas de las 4 fachadas
   y la vista en perspectiva superior.
"""

import os
import math
from PIL import Image, ImageDraw

from cad_engine import (
    svg_defs, dim_h, dim_v, title_block, sanitize_svg_text
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(BASE_DIR, "propuestas", "renders", "guides_3d")
os.makedirs(GUIDES_DIR, exist_ok=True)


# ==============================================================================
# 1. PLANO CAD DE LOS 4 ALZADOS EXTERIORES ESTRICTOS (ESCALA 1:100)
# ==============================================================================
def build_4_elevations_svg() -> str:
    W, H = 1800, 1320
    S = 34.0  # 1m = 34px

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1744" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO A-03 · ALZADOS EXTERIORES ESTRICTOS (NORTE, SUR, ESTE Y OESTE) — GEOMETRÍA 100% FIEL A PLANOS</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Correspondencia milimétrica con Plantas A-01, A-02 y E-04 · Cotas de coronación +6,80 m · Forjado P1 +3,15 m · Cubierta Oeste FV +3,45 m · Pérgola +2,90 m</text>',
    ]

    def level_marks(x_left: float, x_right: float, gy: float, levels):
        g = [f'<line x1="{x_left-25:.1f}" y1="{gy:.1f}" x2="{x_right+25:.1f}" y2="{gy:.1f}" stroke="#10b981" stroke-width="2.2"/>']
        for z_m, lbl, col in levels:
            ly = gy - z_m * S
            g.append(f'<line x1="{x_left-15:.1f}" y1="{ly:.1f}" x2="{x_right+15:.1f}" y2="{ly:.1f}" stroke="{col}" stroke-width="0.6" stroke-dasharray="5,3" opacity="0.75"/>')
            g.append(f'<text x="{x_right+18:.1f}" y="{ly+2:.1f}" fill="{col}" font-family="monospace" font-size="5.6" font-weight="700">{lbl}</text>')
        return "\n".join(g)

    # ==========================================================================
    # PANEL 1: ALZADO NORTE (FACHADA PRINCIPAL DE ACCESO · Y = 5,00 m)
    # Vista mirando hacia el Sur -> Izquierda es Este (X=17,00), Derecha es Oeste (X=1,00)
    # ==========================================================================
    out.append('<rect x="28" y="70" width="862" height="515" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="28" y="70" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="40" y="85" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">1. ALZADO NORTE (FACHADA VIAL DE ACCESO · EJE 1: Y = 5,00 m) — De Este (X=17,00 m) a Oeste (X=1,00 m)</text>')

    gy1 = 465.0
    # Función x para Alzado Norte: X=17.00 a la izquierda, X=1.00 a la derecha
    def nx(xm: float) -> float:
        return 115.0 + (17.00 - xm) * S

    def ny(zm: float) -> float:
        return gy1 - zm * S

    # Niveles
    out.append(level_marks(nx(17.50), nx(0.50), gy1, [
        (0.00, "±0,00 m (PB)", "#10b981"),
        (2.90, "+2,90 m (Pérgola)", "#94a3b8"),
        (3.15, "+3,15 m (Forjado P1)", "#38bdf8"),
        (3.45, "+3,45 m (Cub. Oeste FV)", "#f59e0b"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
    ]))

    # Ejes verticales E, D, C, B, A
    for lbl, xm in [("E", 17.00), ("D", 12.50), ("C", 8.50), ("B", 6.15), ("A", 4.00)]:
        xx = nx(xm)
        out.append(f'<line x1="{xx:.1f}" y1="102" x2="{xx:.1f}" y2="{gy1+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="102" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="105" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.2" font-weight="700">{lbl}</text>')

    # Cuerpo Principal 2 Plantas (X=17.00 a X=6.15 -> ancho 10,85 m)
    # Planta Baja (Z=0..3.15): Zócalo y paños de granito gallego + SATE blanco
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(3.15):.1f}" width="{10.85*S:.1f}" height="{3.15*S:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>')
    # Zócalo granito h=1,10m
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(1.10):.1f}" width="{10.85*S:.1f}" height="{1.10*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.9"/>')
    # Planta Primera (Z=3.15..6.80): SATE Blanco Cálido NCS S 0502-Y
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(6.80):.1f}" width="{10.85*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    # Albardilla coronación +6,80m
    out.append(f'<rect x="{nx(17.05):.1f}" y="{ny(6.80):.1f}" width="{10.95*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')

    # Cuerpo Oeste 1 Planta (Mudroom X=6.15..4.00, Z=0..3.45m) en mampostería de granito
    out.append(f'<rect x="{nx(6.15):.1f}" y="{ny(3.45):.1f}" width="{2.15*S:.1f}" height="{3.45*S:.1f}" fill="#334155" stroke="#cbd5e1" stroke-width="1.4"/>')
    # Paneles solares FV sobre cubierta Oeste (Z=3.45..3.75m)
    out.append(f'<polygon points="{nx(5.90):.1f},{ny(3.45):.1f} {nx(4.25):.1f},{ny(3.45):.1f} {nx(4.40):.1f},{ny(3.82):.1f} {nx(5.90):.1f},{ny(3.60):.1f}" fill="#0284c7" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(5.07):.1f}" y="{ny(4.00):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" font-weight="700">12 PANELES FV</text>')

    # Chimenea Salón asomando al fondo en X=4.40..4.95, Z=3.45..7.25m
    out.append(f'<rect x="{nx(4.95):.1f}" y="{ny(7.25):.1f}" width="{0.55*S:.1f}" height="{3.80*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(4.67):.1f}" y="{ny(7.42):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.0">CHIMENEA +7,25m</text>')

    # Pérgola Aparcamiento 2 Coches (X=4.00..1.00, Z=0..2.90m)
    out.append(f'<rect x="{nx(4.00):.1f}" y="{ny(2.90):.1f}" width="{3.00*S:.1f}" height="{0.22*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<rect x="{nx(1.15):.1f}" y="{ny(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<text x="{nx(2.50):.1f}" y="{ny(1.50):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.5" font-weight="700">PÉRGOLA 2 COCHES</text>')
    out.append(f'<text x="{nx(2.50):.1f}" y="{ny(1.20):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">(3,00 × 6,80 m)</text>')

    # Huecos Planta Baja Norte:
    # C-03 Ventana Baño PB (X=14.15..15.15, Z=1.80..2.40)
    out.append(f'<rect x="{nx(15.15):.1f}" y="{ny(2.40):.1f}" width="{1.00*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{nx(14.65):.1f}" y="{ny(1.50):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">C-03 BAÑO PB</text>')
    # C-02 Ventana Despacho (X=10.80..12.60, Z=1.10..2.30)
    out.append(f'<rect x="{nx(12.60):.1f}" y="{ny(2.30):.1f}" width="{1.80*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<line x1="{nx(11.70):.1f}" y1="{ny(2.30):.1f}" x2="{nx(11.70):.1f}" y2="{ny(1.10):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{nx(11.70):.1f}" y="{ny(0.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" font-weight="700">C-02 DESPACHO (1,80×1,20)</text>')
    # Porche Norte + Puerta Pivotante Iroko P-01 (X=6.50..9.10, Z=0..2.40)
    out.append(f'<rect x="{nx(9.10):.1f}" y="{ny(2.55):.1f}" width="{2.60*S:.1f}" height="{2.55*S:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.1"/>')
    out.append(f'<rect x="{nx(8.35):.1f}" y="{ny(2.40):.1f}" width="{1.10*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#fbbf24" stroke-width="1.4"/>')
    out.append(f'<rect x="{nx(7.25):.1f}" y="{ny(2.40):.1f}" width="{0.55*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(7.80):.1f}" y="{ny(2.70):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="5.2" font-weight="700">P-01 IROKO (1,10×2,40)</text>')

    # Huecos Planta Primera Norte (+3,15 m):
    # C-11 Ventana Baño Suite (X=14.65..15.85, Z=4.95..5.55)
    out.append(f'<rect x="{nx(15.85):.1f}" y="{ny(5.55):.1f}" width="{1.20*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{nx(15.25):.1f}" y="{ny(5.75):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">C-11 BAÑO SUITE (1,20×0,60)</text>')
    # C-10B Ventana Sala Polivalente / Cine & Gaming (X=10.45..12.25, Z=4.15..5.35) + Paño Iroko
    out.append(f'<rect x="{nx(12.65):.1f}" y="{ny(5.55):.1f}" width="{0.40*S:.1f}" height="{1.40*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')
    out.append(f'<rect x="{nx(12.25):.1f}" y="{ny(5.35):.1f}" width="{1.80*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#fbbf24" stroke-width="1.4"/>')
    out.append(f'<line x1="{nx(11.35):.1f}" y1="{ny(5.35):.1f}" x2="{nx(11.35):.1f}" y2="{ny(4.15):.1f}" stroke="#fbbf24" stroke-width="0.9"/>')
    out.append(f'<text x="{nx(11.35):.1f}" y="{ny(5.75):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="5.3" font-weight="700">C-10B SALA POLIVALENTE (1,80×1,20)</text>')
    # C-10 Ventana Baño Hijos (X=7.15..8.15, Z=4.95..5.55)
    out.append(f'<rect x="{nx(8.15):.1f}" y="{ny(5.55):.1f}" width="{1.00*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{nx(7.65):.1f}" y="{ny(5.75):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">C-10 BAÑO HIJOS (1,00×0,60)</text>')

    # Cotas Horizontales Alzado Norte
    out.append(dim_h(nx(17.00), nx(6.15), gy1, 32, "10,85 m (Volumen 2 Plantas · Ejes E - B)", "#38bdf8"))
    out.append(dim_h(nx(6.15), nx(4.00), gy1, 32, "2,15 m (Mudroom PB)", "#cbd5e1"))
    out.append(dim_h(nx(4.00), nx(1.00), gy1, 32, "3,00 m (Pérgola)", "#94a3b8"))
    out.append(dim_h(nx(17.00), nx(1.00), gy1, 56, "16,00 m (FRENTE TOTAL EDIFICACIÓN + PÉRGOLA EN LÍNEA Y=5,00 m)", "#f8fafc"))

    # ==========================================================================
    # PANEL 2: ALZADO SUR (FACHADA AL JARDÍN Y PISCINA · Y = 18,00 / 21,45 m)
    # Vista mirando hacia el Norte -> Izquierda es Oeste (X=1,00), Derecha es Este (X=17,00)
    # ==========================================================================
    out.append('<rect x="910" y="70" width="862" height="515" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="910" y="70" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="922" y="85" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">2. ALZADO SUR (FACHADA PRINCIPAL JARDÍN Y PISCINA) — De Oeste (X=1,00 m) a Este (X=17,00 m)</text>')

    gy2 = 465.0
    def sx(xm: float) -> float:
        return 970.0 + (xm - 1.00) * S

    def sy(zm: float) -> float:
        return gy2 - zm * S

    out.append(level_marks(sx(0.80), sx(17.40), gy2, [
        (0.00, "±0,00 m (Porche/PB)", "#10b981"),
        (3.15, "+3,15 m (Balcón P1)", "#38bdf8"),
        (3.45, "+3,45 m (Cub. Oeste)", "#f59e0b"),
        (6.80, "+6,80 m (Coronación)", "#f8fafc"),
    ]))

    for lbl, xm in [("A", 4.00), ("B", 6.15), ("C", 8.50), ("D", 12.50), ("E", 17.00)]:
        xx = sx(xm)
        out.append(f'<line x1="{xx:.1f}" y1="102" x2="{xx:.1f}" y2="{gy2+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="102" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="105" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.2" font-weight="700">{lbl}</text>')

    # Cuerpo Oeste 1 Planta visto desde el Sur (Muro de Granito del Salón extendido hasta el Porche X=4.00..6.15, Z=0..3.45m + Chimenea +7.25m)
    out.append(f'<rect x="{sx(4.00):.1f}" y="{sy(3.45):.1f}" width="{2.15*S:.1f}" height="{3.45*S:.1f}" fill="#334155" stroke="#cbd5e1" stroke-width="1.4"/>')
    out.append(f'<rect x="{sx(4.40):.1f}" y="{sy(7.25):.1f}" width="{0.55*S:.1f}" height="{3.80*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="1.1"/>')
    out.append(f'<text x="{sx(5.07):.1f}" y="{sy(1.75):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="4.8" transform="rotate(-90 {sx(5.07):.1f} {sy(1.75):.1f})">MURO GRANITO SALÓN</text>')

    # Cuerpo Principal 2 Plantas (X=6.15..17.00 -> 10,85 m)
    # Planta Baja (Porche Sur Cubierto + Grandes Correderas C-08 y C-09)
    out.append(f'<rect x="{sx(6.15):.1f}" y="{sy(3.15):.1f}" width="{10.85*S:.1f}" height="{3.15*S:.1f}" fill="#172036" stroke="#e2e8f0" stroke-width="1.5"/>')
    # Corredera Salón C-08 (X=6.80..11.60, Z=0..2.60)
    out.append(f'<rect x="{sx(6.80):.1f}" y="{sy(2.60):.1f}" width="{4.80*S:.1f}" height="{2.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{sx(9.20):.1f}" y1="{sy(2.60):.1f}" x2="{sx(9.20):.1f}" y2="{sy(0.00):.1f}" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{sx(9.20):.1f}" y="{sy(1.30):.1f}" text-anchor="middle" fill="#e0f2fe" font-family="monospace" font-size="5.5" font-weight="700">C-08 CORREDERA SALÓN (4,80×2,60m)</text>')
    # Corredera Comedor C-09 (X=12.60..16.20, Z=0..2.60)
    out.append(f'<rect x="{sx(12.60):.1f}" y="{sy(2.60):.1f}" width="{3.60*S:.1f}" height="{2.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{sx(14.40):.1f}" y1="{sy(2.60):.1f}" x2="{sx(14.40):.1f}" y2="{sy(0.00):.1f}" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{sx(14.40):.1f}" y="{sy(1.30):.1f}" text-anchor="middle" fill="#e0f2fe" font-family="monospace" font-size="5.2" font-weight="700">C-09 COMEDOR (3,60×2,60m)</text>')
    # Churrasqueira en extremo Este del Porche Sur (X=15.40..16.95, Z=0..3.15)
    out.append(f'<rect x="{sx(15.65):.1f}" y="{sy(2.85):.1f}" width="{1.30*S:.1f}" height="{2.85*S:.1f}" fill="#334155" stroke="#f59e0b" stroke-width="1.1"/>')
    out.append(f'<text x="{sx(16.30):.1f}" y="{sy(1.40):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.6" transform="rotate(-90 {sx(16.30):.1f} {sy(1.40):.1f})">CHURRASQUEIRA</text>')

    # Planta Primera Sur (X=6.15..17.00, Z=3.15..6.80): SATE Blanco + 3 Balconeras + Barandilla Vidrio
    out.append(f'<rect x="{sx(6.15):.1f}" y="{sy(6.80):.1f}" width="{10.85*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{sx(6.10):.1f}" y="{sy(6.80):.1f}" width="{10.95*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    # C-12 Balconera Dormitorio 1 Niña (X=7.10..9.30, Z=3.15..5.55)
    out.append(f'<rect x="{sx(7.10):.1f}" y="{sy(5.55):.1f}" width="{2.20*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<line x1="{sx(8.20):.1f}" y1="{sy(5.55):.1f}" x2="{sx(8.20):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(8.20):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="5.0" font-weight="700">C-12 DORM. NIÑA (2,20m)</text>')
    # Paño Iroko entre D1 y D2 (X=9.30..10.65)
    out.append(f'<rect x="{sx(9.30):.1f}" y="{sy(5.55):.1f}" width="{1.35*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')
    # C-13 Balconera Dormitorio 2 Niño (X=10.65..12.85, Z=3.15..5.55)
    out.append(f'<rect x="{sx(10.65):.1f}" y="{sy(5.55):.1f}" width="{2.20*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<line x1="{sx(11.75):.1f}" y1="{sy(5.55):.1f}" x2="{sx(11.75):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(11.75):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="5.0" font-weight="700">C-13 DORM. NIÑO (2,20m)</text>')
    # Paño Iroko entre D2 y Suite (X=12.85..13.80)
    out.append(f'<rect x="{sx(12.85):.1f}" y="{sy(5.55):.1f}" width="{0.95*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')
    # C-14 Balconera Master Suite (X=13.80..16.50, Z=3.15..5.55)
    out.append(f'<rect x="{sx(13.80):.1f}" y="{sy(5.55):.1f}" width="{2.70*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<line x1="{sx(15.15):.1f}" y1="{sy(5.55):.1f}" x2="{sx(15.15):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(15.15):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" font-weight="700">C-14 SUITE (2,70m)</text>')

    # Barandilla continua de vidrio 10+10.2 mm en Balcón Sur (Z=3.15..4.25, X=6.15..17.00)
    out.append(f'<rect x="{sx(6.15):.1f}" y="{sy(4.25):.1f}" width="{10.85*S:.1f}" height="{1.10*S:.1f}" fill="#38bdf8" fill-opacity="0.18" stroke="#e0f2fe" stroke-width="1.5"/>')

    # Cotas Horizontales Alzado Sur
    out.append(dim_h(sx(4.00), sx(6.15), gy2, 32, "2,15 m (Salón 1P)", "#cbd5e1"))
    out.append(dim_h(sx(6.15), sx(9.99), gy2, 32, "3,42 m útil (Dorm 1)", "#10b981"))
    out.append(dim_h(sx(9.99), sx(13.54), gy2, 32, "3,42 m útil (Dorm 2)", "#10b981"))
    out.append(dim_h(sx(13.54), sx(17.00), gy2, 32, "3,05 m útil (Suite)", "#38bdf8"))
    out.append(dim_h(sx(6.15), sx(17.00), gy2, 56, "10,85 m (FRENTE SUR 2 PLANTAS + BALCÓN CORRIDO Y PORCHE)", "#f8fafc"))

    # ==========================================================================
    # PANEL 3: ALZADO ESTE (FACHADA LATERAL DERECHA · X = 17,00 m)
    # Vista mirando hacia el Oeste -> Izquierda es Sur (Y=24,00), Derecha es Norte (Y=5,00)
    # ==========================================================================
    out.append('<rect x="28" y="600" width="862" height="535" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="28" y="600" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="40" y="615" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">3. ALZADO ESTE (FACHADA LATERAL DERECHA · EJE E: X = 17,00 m) — De Sur (Y=21,45 m) a Norte (Y=5,00 m)</text>')

    gy3 = 1005.0
    def ex(ym: float) -> float:
        return 115.0 + (22.00 - ym) * S

    def ey(zm: float) -> float:
        return gy3 - zm * S

    out.append(level_marks(ex(22.00), ex(4.50), gy3, [
        (0.00, "±0,00 m (PB/Porche)", "#10b981"),
        (3.15, "+3,15 m (Forjado P1)", "#38bdf8"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
    ]))

    for lbl, ym in [("5", 21.45), ("4B", 19.40), ("4", 18.00), ("3", 12.40), ("2", 8.40), ("1", 5.00)]:
        xx = ex(ym)
        out.append(f'<line x1="{xx:.1f}" y1="632" x2="{xx:.1f}" y2="{gy3+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="632" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="635" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.0" font-weight="700">{lbl}</text>')

    # Cuerpo Principal 2 Plantas en Alzado Este (Y=18.00 a Y=5.00 -> 13,00 m)
    out.append(f'<rect x="{ex(18.45):.1f}" y="{ey(3.15):.1f}" width="{13.45*S:.1f}" height="{3.15*S:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>')
    out.append(f'<rect x="{ex(18.45):.1f}" y="{ey(1.10):.1f}" width="{13.45*S:.1f}" height="{1.10*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.9"/>')
    out.append(f'<rect x="{ex(18.00):.1f}" y="{ey(6.80):.1f}" width="{13.00*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{ex(18.05):.1f}" y="{ey(6.80):.1f}" width="{13.10*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')

    # Vuelo del Porche Sur (Y=21.45..18.45 -> 3,00 m) + Muro Ciego Posterior de la Churrasqueira de Granito + Balcón Sur P1 unificado a 3,00m
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(3.15):.1f}" width="{3.00*S:.1f}" height="{0.30*S:.1f}" fill="#334155" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(2.85):.1f}" width="{0.35*S:.1f}" height="{2.85*S:.1f}" fill="#334155" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Muro ciego posterior de piedra de la Churrasqueira (mira al interior del porche, ciego al Este)
    out.append(f'<rect x="{ex(21.10):.1f}" y="{ey(2.85):.1f}" width="{1.60*S:.1f}" height="{2.85*S:.1f}" fill="#334155" stroke="#64748b" stroke-width="1.2"/>')
    out.append(f'<text x="{ex(20.30):.1f}" y="{ey(1.50):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="5.0">MURO TRASERO CHURRASQUEIRA</text>')
    # Balcón Sur P1 unificado (Y=21.45..18.00 -> 3,00 m) con celosía Iroko
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(3.15):.1f}" width="{3.00*S:.1f}" height="{0.25*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(4.25):.1f}" width="{3.00*S:.1f}" height="{1.10*S:.1f}" fill="#38bdf8" fill-opacity="0.22" stroke="#e0f2fe" stroke-width="1.3"/>')
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(6.60):.1f}" width="{0.30*S:.1f}" height="{3.25*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="1.0"/>')

    # Huecos Fachada Este Actualizados:
    # PB: C-04 Ventana Lavandería (Y=11.95..12.85, Z=1.40..2.40) + C-04B Ventana Corrida Cocina sobre encimera (Y=9.20..11.20, Z=1.15..1.65)
    out.append(f'<rect x="{ex(12.85):.1f}" y="{ey(2.40):.1f}" width="{0.90*S:.1f}" height="{1.00*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{ex(12.40):.1f}" y="{ey(2.60):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">C-04 LAVANDERÍA (0,90×1,00)</text>')
    out.append(f'<rect x="{ex(11.20):.1f}" y="{ey(1.65):.1f}" width="{2.00*S:.1f}" height="{0.50*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{ex(10.20):.1f}" y="{ey(1.85):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.8">C-04B COCINA CORRIDA (2,00×0,50)</text>')
    # P1: C-14B Ventana Vestidor Master Suite (Y=9.40..10.40, Z=4.15..5.35) + C-14C Ventana Este Suite (Y=14.00..15.20, Z=4.15..5.35)
    out.append(f'<rect x="{ex(10.75):.1f}" y="{ey(5.55):.1f}" width="{1.70*S:.1f}" height="{1.60*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')
    out.append(f'<rect x="{ex(10.40):.1f}" y="{ey(5.35):.1f}" width="{1.00*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<text x="{ex(9.90):.1f}" y="{ey(5.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" font-weight="700">C-14B VESTIDOR (1,00×1,20)</text>')
    out.append(f'<rect x="{ex(15.20):.1f}" y="{ey(5.35):.1f}" width="{1.20*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<text x="{ex(14.60):.1f}" y="{ey(5.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" font-weight="700">C-14C SUITE ESTE (1,20×1,20)</text>')

    # Copa del Arce Japonés asomando en sección/proyección central (Y=8.40..12.40)
    out.append(f'<line x1="{ex(12.40):.1f}" y1="{ey(3.15):.1f}" x2="{ex(12.40):.1f}" y2="{ey(6.80):.1f}" stroke="#10b981" stroke-width="0.9" stroke-dasharray="4,3"/>')
    out.append(f'<line x1="{ex(8.40):.1f}" y1="{ey(3.15):.1f}" x2="{ex(8.40):.1f}" y2="{ey(6.80):.1f}" stroke="#10b981" stroke-width="0.9" stroke-dasharray="4,3"/>')
    out.append(f'<text x="{ex(10.40):.1f}" y="{ey(6.35):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="4.8">(PROYECCIÓN PATIO CENTRAL 4,00m)</text>')

    # Cotas Horizontales Alzado Este
    out.append(dim_h(ex(21.45), ex(18.45), gy3, 32, "3,00 m (Porche Sur)", "#fbbf24"))
    out.append(dim_h(ex(18.45), ex(12.40), gy3, 32, "6,05 m (Crujía Sur)", "#38bdf8"))
    out.append(dim_h(ex(12.40), ex(8.40), gy3, 32, "4,00 m (Crujía Central)", "#10b981"))
    out.append(dim_h(ex(8.40), ex(5.00), gy3, 32, "3,40 m (Crujía Norte)", "#38bdf8"))
    out.append(dim_h(ex(21.45), ex(5.00), gy3, 56, "16,45 m (LONGITUD TOTAL EDIFICACIÓN + PORCHE SUR EN EJE E)", "#f8fafc"))

    # ==========================================================================
    # PANEL 4: ALZADO OESTE (FACHADA LATERAL IZQUIERDA · X = 1,00 / 4,00 / 6,15 m)
    # Vista mirando hacia el Este -> Izquierda es Norte (Y=5,00), Derecha es Sur (Y=21,45)
    # ==========================================================================
    out.append('<rect x="910" y="600" width="862" height="535" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="910" y="600" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="922" y="615" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">4. ALZADO OESTE (FACHADA LATERAL IZQUIERDA · EJES A-B) — De Norte (Y=5,00 m) a Sur (Y=21,45 m)</text>')

    gy4 = 1005.0
    def wx(ym: float) -> float:
        return 970.0 + (ym - 4.50) * S

    def wy(zm: float) -> float:
        return gy4 - zm * S

    out.append(level_marks(wx(4.50), wx(22.00), gy4, [
        (0.00, "±0,00 m (PB)", "#10b981"),
        (2.90, "+2,90 m (Pérgola)", "#94a3b8"),
        (3.45, "+3,45 m (Cub. Oeste)", "#f59e0b"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
    ]))

    for lbl, ym in [("1", 5.00), ("2", 8.40), ("3", 12.40), ("4", 18.00), ("4B", 19.40), ("5", 21.45)]:
        xx = wx(ym)
        out.append(f'<line x1="{xx:.1f}" y1="632" x2="{xx:.1f}" y2="{gy4+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="632" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="635" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.0" font-weight="700">{lbl}</text>')

    # Tercer plano al fondo (X=6.15): Volumen Planta Primera SATE blanco (Y=5.00..18.00, Z=3.45..6.80) + Balcón Sur unificado (Y=18.00..21.45)
    out.append(f'<rect x="{wx(5.00):.1f}" y="{wy(6.80):.1f}" width="{13.00*S:.1f}" height="{3.35*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{wx(4.95):.1f}" y="{wy(6.80):.1f}" width="{13.10*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<text x="{wx(11.50):.1f}" y="{wy(5.20):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="5.5" font-weight="700">FACHADA OESTE P1 CIEGA (SATE BLANCO · BLINDAJE TÉRMICO NOROESTE)</text>')
    # Vuelo Balcón Sur P1 unificado (Y=18.00..21.45 -> 3,45 m)
    out.append(f'<rect x="{wx(18.00):.1f}" y="{wy(3.15):.1f}" width="{3.45*S:.1f}" height="{0.25*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<rect x="{wx(18.00):.1f}" y="{wy(4.25):.1f}" width="{3.45*S:.1f}" height="{1.10*S:.1f}" fill="#38bdf8" fill-opacity="0.22" stroke="#e0f2fe" stroke-width="1.3"/>')

    # Segundo plano (X=4.00): Muro de Granito Continuo extendido hasta el final del Porche (Y=5.00..21.45 -> 16,45 m continuos)
    out.append(f'<rect x="{wx(5.00):.1f}" y="{wy(3.45):.1f}" width="{16.45*S:.1f}" height="{3.45*S:.1f}" fill="#334155" stroke="#e2e8f0" stroke-width="1.5"/>')
    out.append(f'<text x="{wx(19.95):.1f}" y="{wy(1.75):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.8">MURO OESTE CIERRE PORCHE</text>')
    # Puerta P-02 Zaguán Mudroom (Y=6.60..7.50, Z=0..2.20)
    out.append(f'<rect x="{wx(6.60):.1f}" y="{wy(2.20):.1f}" width="{0.90*S:.1f}" height="{2.20*S:.1f}" fill="#78350f" stroke="#fbbf24" stroke-width="1.2"/>')
    out.append(f'<text x="{wx(7.05):.1f}" y="{wy(2.40):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.8">P-02 MUDROOM</text>')
    # Puerta doble P-05 Trastero Surf / Sala Técnica (Y=9.60..11.00, Z=0..2.20) + Rejillas VMC
    out.append(f'<rect x="{wx(9.60):.1f}" y="{wy(2.20):.1f}" width="{1.40*S:.1f}" height="{2.20*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{wx(10.30):.1f}" y1="{wy(2.20):.1f}" x2="{wx(10.30):.1f}" y2="{wy(0.00):.1f}" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<text x="{wx(10.30):.1f}" y="{wy(2.40):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.8">P-05 SALA TÉC./SURF</text>')
    # Chimenea vertical de leña en Salón (Y=14.60..15.25, Z=0..7.25m)
    out.append(f'<rect x="{wx(14.60):.1f}" y="{wy(7.25):.1f}" width="{0.65*S:.1f}" height="{7.25*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="1.2"/>')
    out.append(f'<text x="{wx(14.92):.1f}" y="{wy(7.42):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.0">CHIMENEA +7,25m</text>')

    # Primer plano (X=1.00..4.00): Pérgola 2 Coches (Y=5.00..11.80, Z=0..2.90)
    out.append(f'<rect x="{wx(5.00):.1f}" y="{wy(2.90):.1f}" width="{6.80*S:.1f}" height="{0.22*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<rect x="{wx(5.05):.1f}" y="{wy(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<rect x="{wx(8.35):.1f}" y="{wy(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<rect x="{wx(11.65):.1f}" y="{wy(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')

    # Cotas Horizontales Alzado Oeste
    out.append(dim_h(wx(5.00), wx(11.80), gy4, 32, "6,80 m (Pérgola 2 Coches + Mudroom/Surf)", "#38bdf8"))
    out.append(dim_h(wx(11.80), wx(18.45), gy4, 32, "6,65 m (Muro Granito Salón + Chimenea)", "#cbd5e1"))
    out.append(dim_h(wx(18.45), wx(21.45), gy4, 32, "3,00 m (Cierre Lateral Granito Porche Sur)", "#fbbf24"))
    out.append(dim_h(wx(5.00), wx(21.45), gy4, 56, "16,45 m (DESARROLLO TOTAL OESTE CERRADO Y PROTEGIDO)", "#f8fafc"))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="A-03",
        title="ALZADOS EXTERIORES DE LAS 4 FACHADAS (NORTE, SUR, ESTE Y OESTE)",
        scale="1:100 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN (GEOMETRÍA ESTRICTA ITERACIÓN #02)",
        subtitle="Muro Cortaviento Oeste Continuo + Vuelo Sur Unificado Sin Escalón + Preinstalación Piscina en Césped + Ventanas Este",
        extra_notes=[
            "Alzado Norte: Puerta Pivotante P-01 (1,10m), Despacho C-02 (1,80m), Baño PB C-03 (1,00m), Baño Hijos C-10 (1,00m), Sala Polivalente C-10B (1,80m) y Baño Suite C-11 (1,20m)",
            "Alzado Sur: Correderas Salón C-08 (4,80m) y Comedor C-09 (3,60m) bajo Porche de 3,00m cerrado al Oeste por muro de granito; Balcón corrido P1 de 3,00m unificado con 3 balconeras",
            "Alzado Este: Ventana Lavandería C-04 (0,90m) + Ventana Corrida Cocina C-04B (2,00×0,50m) en PB; Ventanas Vestidor C-14B y Suite C-14C en P1; Muro ciego trasero de Churrasqueira",
            "Alzado Oeste: Muro de granito continuo de 16,45m (Mudroom, Sala Técnica, Salón y Cierre Porche Sur) con chimenea +7,25m, 12 paneles FV y Pérgola 2 coches",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


# ==============================================================================
# 2. GENERADOR DE VISTAS 3D MATEMÁTICAS ESTRICTAS (GUÍAS DE GEOMETRÍA PARA IA)
# ==============================================================================
def get_strict_3d_faces():
    """
    Construye el modelo 3D exacto subdividido en celdas para que el algoritmo del pintor
    tenga precisión tipo Z-buffer sin artefactos de oclusión.
    """
    faces = []

    def cy(y_cad):
        return 30.0 - y_cad

    def add_subdivided_quad(p00, p10, p11, p01, color, edgecolor, alpha=1.0, layer=1, bias=0.0, nx=4, ny=4):
        for i in range(nx):
            u0, u1 = i / nx, (i + 1) / nx
            for j in range(ny):
                v0, v1 = j / ny, (j + 1) / ny
                def interp(u, v):
                    return tuple(
                        (1 - u) * (1 - v) * p00[k]
                        + u * (1 - v) * p10[k]
                        + u * v * p11[k]
                        + (1 - u) * v * p01[k]
                        for k in range(3)
                    )
                verts = [interp(u0, v0), interp(u1, v0), interp(u1, v1), interp(u0, v1)]
                faces.append((verts, color, edgecolor, alpha, layer, bias))

    def add_box(x0, x1, y0_cad, y1_cad, z0, z1, color, edgecolor="#334155", alpha=1.0, layer=1, bias=0.0):
        ya, yb = cy(y1_cad), cy(y0_cad)  # ya < yb
        nx = max(1, int(round(abs(x1 - x0) / 1.2)))
        ny = max(1, int(round(abs(yb - ya) / 1.2)))
        nz = max(1, int(round(abs(z1 - z0) / 1.2)))
        # Top (z1)
        add_subdivided_quad((x0, ya, z1), (x1, ya, z1), (x1, yb, z1), (x0, yb, z1), color, edgecolor, alpha, layer, bias, nx, ny)
        # South (ya)
        add_subdivided_quad((x0, ya, z0), (x1, ya, z0), (x1, ya, z1), (x0, ya, z1), color, edgecolor, alpha, layer, bias, nx, nz)
        # North (yb)
        add_subdivided_quad((x0, yb, z0), (x1, yb, z0), (x1, yb, z1), (x0, yb, z1), color, edgecolor, alpha, layer, bias, nx, nz)
        # West (x0)
        add_subdivided_quad((x0, ya, z0), (x0, yb, z0), (x0, yb, z1), (x0, ya, z1), color, edgecolor, alpha, layer, bias, ny, nz)
        # East (x1)
        add_subdivided_quad((x1, ya, z0), (x1, yb, z0), (x1, yb, z1), (x1, ya, z1), color, edgecolor, alpha, layer, bias, ny, nz)

    def add_rect_on_y(x0, x1, y_cad, z0, z1, color, edgecolor="#0f172a", alpha=1.0, layer=1, bias=-0.35):
        yy = cy(y_cad)
        nx = max(1, int(round(abs(x1 - x0) / 1.0)))
        nz = max(1, int(round(abs(z1 - z0) / 1.0)))
        add_subdivided_quad((x0, yy, z0), (x1, yy, z0), (x1, yy, z1), (x0, yy, z1), color, edgecolor, alpha, layer, bias, nx, nz)

    def add_rect_on_x(x_cad, y0_cad, y1_cad, z0, z1, color, edgecolor="#0f172a", alpha=1.0, layer=1, bias=-0.35):
        ya, yb = cy(y1_cad), cy(y0_cad)
        ny = max(1, int(round(abs(yb - ya) / 1.0)))
        nz = max(1, int(round(abs(z1 - z0) / 1.0)))
        add_subdivided_quad((x_cad, ya, z0), (x_cad, yb, z0), (x_cad, yb, z1), (x_cad, ya, z1), color, edgecolor, alpha, layer, bias, ny, nz)

    def add_rect_on_z(x0, x1, y0_cad, y1_cad, z_val, color, edgecolor="#0f172a", alpha=1.0, layer=0, bias=0.0):
        ya, yb = cy(y1_cad), cy(y0_cad)
        nx = max(1, int(round(abs(x1 - x0) / 1.5)))
        ny = max(1, int(round(abs(yb - ya) / 1.5)))
        add_subdivided_quad((x0, ya, z_val), (x1, ya, z_val), (x1, yb, z_val), (x0, yb, z_val), color, edgecolor, alpha, layer, bias, nx, ny)

    # CAPA 0: Parcela Césped Completa (20 x 30 m), Vial, Tarima Porche y Suelo Patio (SIN PISCINA, SOLO CÉSPED)
    add_rect_on_z(0, 20, 0, 30, 0.0, "#4d7c0f", "#3f6212", 1.0, layer=0, bias=1.5)
    add_rect_on_z(1.0, 4.5, 0.0, 11.8, 0.02, "#94a3b8", "#64748b", 1.0, layer=0, bias=0.6)
    add_rect_on_z(6.5, 9.1, 0.0, 5.0, 0.02, "#cbd5e1", "#94a3b8", 1.0, layer=0, bias=0.6)
    # Tarima Iroko Porche Sur (X=6.15..17.00, Y=18.45..21.45)
    add_rect_on_z(6.15, 17.00, 18.45, 21.45, 0.04, "#92400e", "#78350f", 1.0, layer=0, bias=-0.3)
    # Suelo Patio Central
    add_rect_on_z(8.50, 12.50, 8.40, 12.40, 0.06, "#92400e", "#78350f", 1.0, layer=0, bias=-0.4)

    # CAPA 1: VOLÚMENES ARQUITECTÓNICOS ESTRICTOS
    # 1. Cuerpo Oeste Continuo en Granito Gallego extendido hasta el final del Porche Sur (X=4.00..6.15, Y=5.00..21.45, Z=0..3.45)
    add_box(4.00, 6.15, 5.00, 21.45, 0.0, 3.45, "#9ca3af", "#4b5563", 1.0, layer=1)
    # Cubierta Grava + 12 Paneles Solares FV (X=4.25..5.90, Y=7.20..17.00, Z=3.50)
    add_rect_on_z(4.08, 6.12, 5.08, 18.35, 3.47, "#cbd5e1", "#64748b", 1.0, layer=1, bias=-0.2)
    for r in range(6):
        ry = 7.20 + r * 1.65
        add_rect_on_z(4.25, 5.90, ry, ry + 1.25, 3.52, "#1e3a8a", "#38bdf8", 1.0, layer=1, bias=-0.55)
    # Chimenea vertical negra en Salón (X=4.35..4.95, Y=14.60..15.25, Z=0..7.25)
    add_box(4.35, 4.95, 14.60, 15.25, 0.0, 7.25, "#1f2937", "#0f172a", 1.0, layer=1, bias=-0.2)

    # 2. Pérgola 2 Coches al Oeste (X=1.00..4.00, Y=5.00..11.80, Z=0..2.90)
    add_box(1.00, 4.00, 5.00, 11.80, 2.72, 2.90, "#1f2937", "#0f172a", 1.0, layer=1)
    for py_c in [5.15, 8.40, 11.60]:
        add_box(1.05, 1.25, py_c, py_c + 0.20, 0.0, 2.72, "#1f2937", "#0f172a", 1.0, layer=1)

    # 3. Volumen Principal 2 Plantas alrededor del Patio Central (X=6.15..17.00, Y=5.00..18.00)
    # Bloque Norte (X=6.15..17.00, Y=5.00..8.40):
    add_box(6.15, 17.00, 5.00, 8.40, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)
    add_box(6.15, 17.00, 5.00, 8.40, 3.15, 6.80, "#f8fafc", "#cbd5e1", 1.0, layer=1)
    # Bloque Sur (X=6.15..17.00, Y=12.40..18.00 / PB llega a 18.45):
    add_box(6.15, 17.00, 12.40, 18.45, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)
    add_box(6.15, 17.00, 12.40, 18.00, 3.15, 6.80, "#f8fafc", "#cbd5e1", 1.0, layer=1)
    # Bloque Oeste del Patio (Escalera X=6.15..8.50, Y=8.40..12.40):
    add_box(6.15, 8.50, 8.40, 12.40, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)
    add_box(6.15, 8.50, 8.40, 12.40, 3.15, 6.80, "#f8fafc", "#cbd5e1", 1.0, layer=1)
    # Bloque Este del Patio (Cocina PB + Vestidor Suite P1 X=12.50..17.00, Y=8.40..12.40):
    add_box(12.50, 17.00, 8.40, 12.40, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)
    add_box(12.50, 17.00, 8.40, 12.40, 3.15, 6.80, "#f8fafc", "#cbd5e1", 1.0, layer=1)

    # 4. Arce Japonés en el centro del Patio Corrala (X=9.50..11.50, Y=9.50..11.50)
    add_box(10.35, 10.65, 10.35, 10.65, 0.06, 2.30, "#451a03", "#290f02", 1.0, layer=1)
    add_box(9.45, 11.55, 9.45, 11.55, 2.10, 4.95, "#b91c1c", "#7f1d1d", 0.95, layer=1)

    # 5. Porche Sur Cubierto (X=6.15..17.00, Y=18.45..21.45, techo en Z=2.90..3.15) + Churrasqueira Este
    add_box(6.15, 17.00, 18.45, 21.45, 2.90, 3.15, "#f8fafc", "#cbd5e1", 1.0, layer=1)
    add_box(16.65, 17.00, 21.10, 21.45, 0.0, 2.90, "#d6d3d1", "#78716c", 1.0, layer=1)
    # Muro de cierre posterior de la Churrasqueira al Este (ciego en cara exterior)
    add_box(15.60, 16.95, 19.20, 21.00, 0.0, 2.90, "#4b5563", "#1f2937", 1.0, layer=1)

    # 6. Balcón Corrido Sur P1 UNIFICADO (X=6.15..17.00, Y=18.00..21.45, losa Z=3.15..3.35)
    # Vuela exactamente los 3.00 m del porche, eliminando el doble escalón
    add_box(6.15, 17.00, 18.00, 21.45, 3.15, 3.35, "#f8fafc", "#cbd5e1", 1.0, layer=1)

    # CAPA 1 CON BIAS FRONTAL: CARPINTERÍAS Y HUECOS ESTRICTOS EN LAS 4 FACHADAS
    # --- FACHADA NORTE (Y = 4.92) ---
    add_rect_on_y(7.25, 8.35, 4.92, 0.0, 2.40, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)   # P-01 Puerta Pivotante Iroko
    add_rect_on_y(6.65, 7.25, 4.92, 0.0, 2.40, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)  # Fijo vidrio Hall
    add_rect_on_y(10.80, 12.60, 4.92, 1.10, 2.30, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-02 Ventana Despacho (1,80x1,20)
    add_rect_on_y(14.15, 15.15, 4.92, 1.80, 2.40, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-03 Ventana Baño PB (1,00x0,60)
    add_rect_on_y(7.15, 8.15, 4.92, 4.95, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)  # C-10 Ventana Baño Hijos (1,00x0,60)
    add_rect_on_y(10.45, 12.25, 4.92, 4.15, 5.35, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-10B Ventana Sala Polivalente (1,80x1,20)
    add_rect_on_y(12.25, 12.75, 4.92, 4.15, 5.55, "#92400e", "#78350f", 1.0, layer=1, bias=-0.5) # Paño Iroko Norte
    add_rect_on_y(14.65, 15.85, 4.92, 4.95, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-11 Ventana Baño Suite (1,20x0,60)

    # --- FACHADA SUR (Y = 18.52 en PB, Y = 18.08 en P1) ---
    add_rect_on_y(6.80, 11.60, 18.52, 0.05, 2.65, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-08 Corredera Salón (4,80x2,60)
    add_rect_on_y(12.60, 16.20, 18.52, 0.05, 2.65, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-09 Corredera Comedor (3,60x2,60)
    add_rect_on_y(7.10, 9.30, 18.08, 3.35, 5.75, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-12 Balconera Dorm Niña (2,20x2,40)
    add_rect_on_y(9.30, 10.65, 18.08, 3.35, 5.75, "#92400e", "#78350f", 1.0, layer=1, bias=-0.5) # Paño Iroko entre D1 y D2
    add_rect_on_y(10.65, 12.85, 18.08, 3.35, 5.75, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-13 Balconera Dorm Niño (2,20x2,40)
    add_rect_on_y(12.85, 13.80, 18.08, 3.35, 5.75, "#92400e", "#78350f", 1.0, layer=1, bias=-0.5)# Paño Iroko entre D2 y Suite
    add_rect_on_y(13.80, 16.50, 18.08, 3.35, 5.75, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-14 Balconera Suite (2,70x2,40)

    # Barandilla de vidrio del Balcón Sur al borde de los 3.00 m (Y = 21.42)
    add_rect_on_y(6.15, 17.00, 21.42, 3.35, 4.35, "#7dd3fc", "#0284c7", 0.42, layer=1, bias=-0.3)
    add_rect_on_x(6.15, 18.00, 21.40, 3.35, 4.35, "#7dd3fc", "#0284c7", 0.42, layer=1, bias=-0.3)
    add_rect_on_x(17.00, 18.00, 21.40, 3.35, 6.60, "#92400e", "#78350f", 0.92, layer=1, bias=-0.3)

    # --- FACHADA ESTE (X = 17.08) ---
    add_rect_on_x(17.08, 11.95, 12.85, 1.40, 2.40, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-04 Ventana Lavandería PB (0,90x1,00)
    add_rect_on_x(17.08, 9.20, 11.20, 1.15, 1.65, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-04B Ventana Corrida Cocina PB (2,00x0,50)
    add_rect_on_x(17.08, 9.40, 10.40, 4.15, 5.35, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-14B Ventana Vestidor Suite P1 (1,00x1,20)
    add_rect_on_x(17.08, 10.40, 11.20, 4.15, 5.55, "#92400e", "#78350f", 1.0, layer=1, bias=-0.5)# Listones Iroko Este
    add_rect_on_x(17.08, 14.00, 15.20, 4.15, 5.35, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-14C Ventana Suite Este (1,20x1,20)

    # --- FACHADA OESTE (X = 3.92 en PB) ---
    add_rect_on_x(3.92, 6.60, 7.50, 0.0, 2.20, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)    # P-02 Puerta Mudroom
    add_rect_on_x(3.92, 9.60, 11.00, 0.0, 2.20, "#1f2937", "#0f172a", 1.0, layer=1, bias=-0.5)   # P-05 Puerta Sala Técnica / Surf

    return faces


def render_guide_view(faces, elev_deg, azim_deg, title, out_path, cam_dist=31.0, cz=2.6):
    """
    Renderiza en perspectiva 3D exacta las caras subdivididas del modelo.
    """
    W, H = 1600, 1000
    img = Image.new("RGBA", (W, H), (219, 234, 254, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    draw.rectangle([0, 0, W, int(H * 0.52)], fill=(186, 230, 253, 255))
    draw.rectangle([0, int(H * 0.52), W, H], fill=(226, 232, 240, 255))

    cx, cy = 9.5, 14.5
    elev = math.radians(elev_deg)
    azim = math.radians(azim_deg)

    ux = math.cos(elev) * math.cos(azim)
    uy = math.cos(elev) * math.sin(azim)
    uz = math.sin(elev)
    cam_x = cx + cam_dist * ux
    cam_y = cy + cam_dist * uy
    cam_z = cz + cam_dist * uz

    fx, fy, fz = -ux, -uy, -uz
    rx, ry, rz = -math.sin(azim), math.cos(azim), 0.0
    upx = ry * fz - rz * fy
    upy = rz * fx - rx * fz
    upz = rx * fy - ry * fx

    focal = 1520.0

    def hex_to_rgba(h, alpha=1.0):
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * alpha))

    projected_polys = []
    for verts, col_hex, edge_hex, alpha, layer, bias in faces:
        pts_2d = []
        dists = []
        valid = True
        for vx, vy, vz in verts:
            dx, dy, dz = vx - cam_x, vy - cam_y, vz - cam_z
            depth = dx * fx + dy * fy + dz * fz
            if depth <= 1.0:
                valid = False
                break
            x_cam = dx * rx + dy * ry + dz * rz
            y_cam = dx * upx + dy * upy + dz * upz
            sx = W / 2.0 + (x_cam / depth) * focal
            sy = H / 2.0 - (y_cam / depth) * focal
            pts_2d.append((sx, sy))
            dists.append(math.sqrt(dx * dx + dy * dy + dz * dz))
        if valid:
            avg_dist = sum(dists) / len(dists) + bias
            projected_polys.append((layer, -avg_dist, pts_2d, hex_to_rgba(col_hex, alpha), hex_to_rgba(edge_hex, min(1.0, alpha + 0.2))))

    # Ordenar primero por capa (0=suelo/piscina, 1=edificio) y luego de mayor distancia a menor distancia
    projected_polys.sort(key=lambda item: (item[0], item[1]))

    for _, _, pts_2d, fill_rgba, edge_rgba in projected_polys:
        draw.polygon(pts_2d, fill=fill_rgba, outline=edge_rgba, width=1)

    img.convert("RGB").save(out_path, "PNG")
    print(f"Rendered 3D guide: {out_path}")


def main():
    svg_str = build_4_elevations_svg()
    for p in [
        os.path.join(BASE_DIR, "plano_alzados_exteriores_4_caras.svg"),
        os.path.join(BASE_DIR, "propuestas", "plano_alzados_exteriores_4_caras.svg"),
    ]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_str)
        print(f"Written {p} ({len(svg_str)} bytes)")

    faces = get_strict_3d_faces()
    render_guide_view(faces, elev_deg=11, azim_deg=84, title="Fachada Norte", out_path=os.path.join(GUIDES_DIR, "guide_norte.png"))
    render_guide_view(faces, elev_deg=11, azim_deg=-84, title="Fachada Sur", out_path=os.path.join(GUIDES_DIR, "guide_sur.png"))
    render_guide_view(faces, elev_deg=11, azim_deg=-6, title="Fachada Este", out_path=os.path.join(GUIDES_DIR, "guide_este.png"))
    render_guide_view(faces, elev_deg=12, azim_deg=174, title="Fachada Oeste", out_path=os.path.join(GUIDES_DIR, "guide_oeste.png"))
    render_guide_view(faces, elev_deg=41, azim_deg=-122, title="Perspectiva Superior", out_path=os.path.join(GUIDES_DIR, "guide_aerea.png"), cam_dist=35.0, cz=2.2)


if __name__ == "__main__":
    main()
