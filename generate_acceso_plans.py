#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos del Ala Norte de Acceso, Hall, Despacho y Baño PB
Oleiros (A Coruña) - Propuesta Definitiva v2
- Ejes Estructurales A - B - C - D - E (Longitud total de ala: 13,15 m):
  * Eje A a B (2,30 m): [E-03] Zaguán Mudroom (5,80 m² útiles, Banco zapatero 1,60x0,45, Gabanero 1,25x0,60, Secador surf, VMC-E 30m³/h)
  * Eje B a C (3,60 m): [E-02] Porche Norte (3,50 m², Granito C3) + [E-04] Hall Principal (10,40 m², Roble 14mm, Puerta C-01 pivotante 1,00x2,40m, Bajante B-02, CGMP+RITI)
  * Eje C a D (3,90 m): [E-05] Despacho / Suite PB (11,50 m², Roble 14mm, Rw38dB, Mesa 90°, Sofá-cama 140, Ventana C-03 1,80x1,20 h=95, VMC-I 35m³/h)
  * Eje D a E (3,35 m): [E-06] Baño Completo PB (5,20 m², Ducha enrasada 1,15x0,90 cota cero, Inodoro suspendido, Lavabo 90x50, Ventana C-04 0,80x0,60 h=160)
  * Distribuidor Neutro NHG: Esclusa reglamentaria Decreto 29/2010 con triple puerta (P-04 desde despacho, P-05 hacia baño, P-06 hacia cocina unificada).
"""

import os
import xml.etree.ElementTree as ET

def svg_defs_technical():
    return """
    <defs>
      <!-- Retícula CAD milimétrica -->
      <pattern id="grid-cad-fine" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.35" opacity="0.6"/>
      </pattern>
      <pattern id="grid-cad-major" width="100" height="100" patternUnits="userSpaceOnUse">
        <rect width="100" height="100" fill="url(#grid-cad-fine)"/>
        <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#334155" stroke-width="0.8" opacity="0.75"/>
      </pattern>

      <!-- Rayado técnico muros ANSI31 -->
      <pattern id="hatch-wall" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="6" stroke="#94a3b8" stroke-width="0.8"/>
      </pattern>

      <!-- Rayado pilares estructurales -->
      <pattern id="hatch-pillar" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="5" stroke="#e2e8f0" stroke-width="1.1"/>
        <line x1="0" y1="0" x2="5" y2="0" stroke="#e2e8f0" stroke-width="1.1"/>
      </pattern>

      <!-- Marcadores de cota a 45 grados (UNE-EN ISO 129) -->
      <marker id="tick-45" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#38bdf8" stroke-width="1.2"/>
      </marker>
      <marker id="tick-amber" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#f59e0b" stroke-width="1.2"/>
      </marker>
      <marker id="tick-emerald" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#10b981" stroke-width="1.2"/>
      </marker>
      <marker id="arrow-tech" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
        <polygon points="0 0, 7 3.5, 0 7" fill="#38bdf8"/>
      </marker>

      <!-- Gradientes -->
      <linearGradient id="grad-wood" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#2a221b"/>
        <stop offset="100%" stop-color="#1c1611"/>
      </linearGradient>
      <linearGradient id="grad-granite" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#262e3d"/>
        <stop offset="100%" stop-color="#141a24"/>
      </linearGradient>
    </defs>
    """

def dim_h(x1, x2, y, offset_y, label, col="#38bdf8", marker="tick-45", font_size=7.5):
    """Línea de cota horizontal acotada ISO 129"""
    if x2 < x1:
        x1, x2 = x2, x1
    yd = y + offset_y
    y_start = y + (2 if offset_y > 0 else -2)
    y_end = yd + (4 if offset_y > 0 else -4)
    mx = (x1 + x2) / 2.0
    tw = max(len(label) * (font_size * 0.60) + 6, 20)
    return f"""<g class="cad-dim">
      <line x1="{x1:.1f}" y1="{y_start:.1f}" x2="{x1:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{x2:.1f}" y1="{y_start:.1f}" x2="{x2:.1f}" y2="{y_end:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{x1:.1f}" y1="{yd:.1f}" x2="{x2:.1f}" y2="{yd:.1f}" stroke="{col}" stroke-width="0.8" marker-start="url(#{marker})" marker-end="url(#{marker})"/>
      <rect x="{mx - tw/2:.1f}" y="{yd - font_size/2 - 2:.1f}" width="{tw:.1f}" height="{font_size + 4:.1f}" fill="#0b1120" opacity="0.9"/>
      <text x="{mx:.1f}" y="{yd + font_size/2 - 1:.1f}" fill="{col}" font-family="monospace" font-size="{font_size}" font-weight="700" text-anchor="middle">{label}</text>
    </g>"""

def dim_v(y1, y2, x, offset_x, label, col="#38bdf8", marker="tick-45", font_size=7.5):
    """Línea de cota vertical acotada ISO 129"""
    if y2 < y1:
        y1, y2 = y2, y1
    xd = x + offset_x
    x_start = x + (2 if offset_x > 0 else -2)
    x_end = xd + (4 if offset_x > 0 else -4)
    my = (y1 + y2) / 2.0
    th = font_size + 4
    tw = max(len(label) * (font_size * 0.60) + 6, 20)
    return f"""<g class="cad-dim">
      <line x1="{x_start:.1f}" y1="{y1:.1f}" x2="{x_end:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{x_start:.1f}" y1="{y2:.1f}" x2="{x_end:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{xd:.1f}" y1="{y1:.1f}" x2="{xd:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.8" marker-start="url(#{marker})" marker-end="url(#{marker})"/>
      <g transform="translate({xd:.1f}, {my:.1f}) rotate(-90)">
        <rect x="{-tw/2:.1f}" y="{-th/2:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="#0b1120" opacity="0.9"/>
        <text x="0" y="{font_size/2 - 1:.1f}" fill="{col}" font-family="monospace" font-size="{font_size}" font-weight="700" text-anchor="middle">{label}</text>
      </g>
    </g>"""

def generate_plano_acceso_planta():
    """Genera plano A-01: Planta Esquemática y Distribución 1:20 del Ala Norte"""
    # Escala y origen:
    # 1 metro = 95 píxeles CAD
    # Eje A: x = 180 (Zaguán)
    # Eje B: x = 180 + 2.30*95 = 180 + 218.5 = 398.5
    # Eje C: x = 398.5 + 3.60*95 = 398.5 + 342 = 740.5
    # Eje D: x = 740.5 + 3.90*95 = 740.5 + 370.5 = 1111.0
    # Eje E: x = 1111.0 + 3.35*95 = 1111.0 + 318.25 = 1429.25
    
    # Y de fachada norte interior = 420.0
    # Y de fachada norte exterior = 385.0 (espesor muro 35 cm = 33.25 px)
    # Y de porche norte = 260.0 (fondo porche 1.30 m)
    # Y de pared sur zaguán = 670.0 (fondo zaguán 2.63 m = 250 px)
    # Y de pared sur hall/despacho = 750.0 (fondo hall 3.47 m = 330 px)
    # Y de pasillo distribuidor neutro = 670.0 a 750.0

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco técnico normalizado
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    """)

    # Encabezado técnico
    svg.append("""
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">ALA NORTE: ACCESO, ZAGUÁN, HALL, DESPACHO Y BAÑO COMPLETO PB</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">VIVIENDA UNIFAMILIAR AISLADA · LIÁNS, OLEIROS (A CORUÑA) · ESCALA 1:20 (CAD DETALLE) · PLANO A-01</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Retranqueo Frontal PGOM (Línea límite de edificación 5,00 m)
    svg.append("""
    <g class="cad-setback">
      <line x1="120" y1="350" x2="1500" y2="350" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="10,5,2,5"/>
      <rect x="420" y="338" width="580" height="18" fill="#0b1120" stroke="#ef4444" stroke-width="0.8"/>
      <text x="710" y="351" fill="#fca5a5" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">LÍNEA LÍMITE DE EDIFICACIÓN (RETRANQUEO FRONTAL 5,00 m · PGOM OLEIROS ORDENANZA 2B)</text>
    </g>
    """)

    # EJES ESTRUCTURALES
    axes = [
        ("A", 180.0, "2,30 m (Zaguán)"),
        ("B", 398.5, "3,60 m (Hall)"),
        ("C", 740.5, "3,90 m (Despacho)"),
        ("D", 1111.0, "3,35 m (Baño PB)"),
        ("E", 1429.25, "")
    ]
    for tag, xpos, span_lbl in axes:
        svg.append(f"""
        <g class="cad-axis">
          <line x1="{xpos:.1f}" y1="160" x2="{xpos:.1f}" y2="820" stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="14,4,3,4" opacity="0.65"/>
          <circle cx="{xpos:.1f}" cy="180" r="14" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="{xpos:.1f}" y="185" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="900" text-anchor="middle">{tag}</text>
        </g>
        """)

    # Acotaciones entre ejes (Top)
    svg.append(dim_h(180.0, 398.5, 210, 0, "2,30 m (ZAGUÁN)", "#38bdf8", font_size=8.5))
    svg.append(dim_h(398.5, 740.5, 210, 0, "3,60 m (HALL / PORCHE)", "#38bdf8", font_size=8.5))
    svg.append(dim_h(740.5, 1111.0, 210, 0, "3,90 m (DESPACHO)", "#38bdf8", font_size=8.5))
    svg.append(dim_h(1111.0, 1429.25, 210, 0, "3,35 m (BAÑO + DISTR.)", "#38bdf8", font_size=8.5))
    svg.append(dim_h(180.0, 1429.25, 145, 0, "LONGITUD TOTAL ALA NORTE = 13,15 m", "#f59e0b", marker="tick-amber", font_size=9.5))

    # [E-02] PORCHE NORTE EXTERIOR
    # Entre B y C: x=398.5 a 740.5 (342 px), y=270 a 420 (fondo 1.50 m)
    svg.append("""
    <!-- [E-02] PORCHE NORTE -->
    <rect x="398.5" y="270" width="342" height="150" fill="url(#grad-granite)" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="6,4"/>
    <g class="porche-stamp">
      <rect x="470" y="290" width="200" height="46" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="0.8"/>
      <text x="570" y="308" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">[E-02] PORCHE NORTE</text>
      <text x="570" y="324" fill="#cbd5e1" font-family="monospace" font-size="7.5" text-anchor="middle">3,50 m² · Granito Silvestre C3 · Z=+0,05m</text>
    </g>
    <!-- Focos empotrados en porche exterior -->
    <circle cx="480" cy="360" r="4.5" fill="#f59e0b" opacity="0.75"/>
    <circle cx="660" cy="360" r="4.5" fill="#f59e0b" opacity="0.75"/>
    """)

    # SOLERAS INTERIORES (Relleno base según material de suelo)
    # Zaguán: Porcelánico C3 (Gris basalto)
    svg.append('<rect x="180.0" y="420" width="218.5" height="260" fill="#111827"/>')
    # Hall: Roble Natural 14mm
    svg.append('<rect x="398.5" y="420" width="342.0" height="330" fill="url(#grad-wood)" opacity="0.85"/>')
    # Despacho: Roble Natural 14mm
    svg.append('<rect x="740.5" y="420" width="370.5" height="330" fill="url(#grad-wood)" opacity="0.85"/>')
    # Baño PB: Porcelánico C3 antideslizante
    svg.append('<rect x="1111.0" y="420" width="318.25" height="250" fill="#0f172a"/>')
    # Distribuidor neutro: Roble / Continuo
    svg.append('<rect x="1111.0" y="670" width="318.25" height="80" fill="#1e293b"/>')

    # MUROS ESTRUCTURALES Y CERRAMIENTOS TERMICOS (Termoarcilla 24cm + SATE 12cm = 36cm = 34px)
    # Muro Norte Zaguán: x=180 a 398.5, y=386 a 420
    # Muro Norte Hall con hueco puerta C-01: C-01 de 1.00m = 95px (x=590 a 685)
    # Muro Norte Despacho con ventana C-03: C-03 de 1.80m = 171px (x=840 a 1011)
    # Muro Norte Baño con ventana C-04: C-04 de 0.80m = 76px (x=1150 a 1226)

    svg.append("""
    <!-- MUROS PERIMETRALES EXTERIORES -->
    <!-- Fachada Norte Zaguán -->
    <rect x="146" y="386" width="252.5" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    <!-- Fachada Oeste Zaguán -->
    <rect x="146" y="386" width="34" height="294" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    
    <!-- Fachada Norte Hall (Entre B y C) con hueco C-01 -->
    <rect x="398.5" y="386" width="191.5" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    <!-- Hueco Puerta Principal C-01: x=590 a 685 -->
    <!-- Continuación muro norte tras puerta C-01 -->
    <rect x="685.0" y="386" width="55.5" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>

    <!-- Fachada Norte Despacho con ventana C-03 (x=840 a 1011) -->
    <rect x="740.5" y="386" width="99.5" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    <!-- Hueco ventana C-03 (1,80m): x=840 a 1011 -->
    <rect x="1011.0" y="386" width="100.0" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>

    <!-- Fachada Norte Baño con ventana C-04 (x=1150 a 1226) -->
    <rect x="1111.0" y="386" width="39.0" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    <!-- Hueco ventana C-04 (0,80m): x=1150 a 1226 -->
    <rect x="1226.0" y="386" width="237.25" height="34" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    <!-- Muro Este Baño PB -->
    <rect x="1429.25" y="386" width="34" height="398" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    """)

    # TABIQUES INTERIORES Y ACÚSTICOS
    svg.append("""
    <!-- TABIQUERÍA INTERIOR -->
    <!-- Separación Zaguán / Hall (Eje B, x=398.5): hueco puerta P-02 (0,80m = 76px) en y=580 a 656 -->
    <rect x="388.5" y="420" width="10" height="160" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <rect x="388.5" y="656" width="10" height="24" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>

    <!-- Separación Sur Zaguán con Sala Técnica: y=680 -->
    <rect x="146" y="680" width="242.5" height="15" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>

    <!-- Separación Hall / Despacho (Eje C, tabique acústico Rw38dB, x=740.5): hueco puerta P-03 acústica en y=620 a 702 -->
    <rect x="734.5" y="420" width="12" height="200" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>
    <rect x="734.5" y="702" width="12" height="48" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>

    <!-- Separación Despacho / Baño y Distribuidor (Eje D, x=1111.0): hueco puerta P-04 en y=675 a 745 -->
    <rect x="1105.0" y="420" width="12" height="255" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <rect x="1105.0" y="745" width="12" height="5" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>

    <!-- Tabique Baño / Distribuidor Neutro (y=670): hueco puerta P-05 (0,75m = 71px) en x=1180 a 1251 -->
    <rect x="1117.0" y="665" width="63.0" height="10" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <rect x="1251.0" y="665" width="178.25" height="10" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>

    <!-- Pared Sur Distribuidor Neutro hacia Cocina (y=750): con puerta corredera P-06 (0,80m = 76px) en x=1220 a 1296 -->
    <rect x="1111.0" y="750" width="109.0" height="15" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <rect x="1296.0" y="750" width="167.25" height="15" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    """)

    # PILARES ESTRUCTURALES (P-01 a P-05)
    pillars = [
        (180.0, 398.5, "P-01"),
        (398.5, 398.5, "P-02"),
        (740.5, 398.5, "P-03"),
        (1111.0, 398.5, "P-04"),
        (1429.25, 398.5, "P-05"),
        (398.5, 750.0, "P-07")
    ]
    for px, py, plabel in pillars:
        svg.append(f"""
        <g class="cad-pillar">
          <rect x="{px-12:.1f}" y="{py-12:.1f}" width="24" height="24" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.4"/>
          <text x="{px+16:.1f}" y="{py-4:.1f}" fill="#94a3b8" font-family="monospace" font-size="7" font-weight="700">{plabel}</text>
        </g>
        """)

    # CARPINTERÍAS: PUERTAS Y VENTANAS
    # Puerta Principal C-01: Pivotante 1,00 x 2,40 m (x=590 a 685, y=420)
    svg.append("""
    <!-- PUERTA PRINCIPAL C-01 PIVOTANTE -->
    <g class="cad-door" id="door-C01">
      <line x1="590.0" y1="420" x2="685.0" y2="420" stroke="#f59e0b" stroke-width="2.5"/>
      <!-- Hoja abatida en 90° hacia interior del hall con eje pivotante a 15cm -->
      <circle cx="605.0" cy="420" r="3.5" fill="#f59e0b"/>
      <line x1="605.0" y1="420" x2="605.0" y2="515" stroke="#f59e0b" stroke-width="2.0"/>
      <!-- Arco de barrido -->
      <path d="M 685.0 420 A 80 80 0 0 1 605.0 500" fill="none" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="3,3"/>
      <rect x="620" y="445" width="120" height="18" fill="#0b1120" stroke="#f59e0b" stroke-width="0.6"/>
      <text x="680" y="457" fill="#fde68a" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">C-01 · 1,00x2,40m PIVOTANTE</text>
    </g>
    """)

    # Ventana Despacho C-03: 1,80 x 1,20 m (h=95 cm) (x=840 a 1011)
    svg.append("""
    <!-- VENTANA C-03 DESPACHO -->
    <g class="cad-window" id="win-C03">
      <rect x="840.0" y="394" width="171.0" height="18" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="840.0" y1="403" x2="1011.0" y2="403" stroke="#38bdf8" stroke-width="1.8"/>
      <line x1="925.5" y1="394" x2="925.5" y2="412" stroke="#38bdf8" stroke-width="1.0"/>
      <rect x="860" y="370" width="130" height="16" fill="#0b1120" stroke="#38bdf8" stroke-width="0.6"/>
      <text x="925" y="381" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">C-03 · 1,80x1,20 (h=95)</text>
    </g>
    """)

    # Ventana Baño C-04: 0,80 x 0,60 m (h=160 cm) (x=1150 a 1226)
    svg.append("""
    <!-- VENTANA C-04 BAÑO PB (ALTA INTIMIDAD) -->
    <g class="cad-window" id="win-C04">
      <rect x="1150.0" y="394" width="76.0" height="18" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="1150.0" y1="403" x2="1226.0" y2="403" stroke="#38bdf8" stroke-width="1.8"/>
      <rect x="1135" y="370" width="110" height="16" fill="#0b1120" stroke="#38bdf8" stroke-width="0.6"/>
      <text x="1190" y="381" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">C-04 · 0,80x0,60 (h=160)</text>
    </g>
    """)

    # Puertas Interiores P-02, P-03, P-04, P-05, P-06
    svg.append("""
    <!-- PUERTA P-02 (ZAGUÁN <-> HALL, 0,80m) -->
    <g class="cad-door" id="door-P02">
      <line x1="398.5" y1="580" x2="398.5" y2="656" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,2"/>
      <line x1="398.5" y1="580" x2="330.0" y2="580" stroke="#cbd5e1" stroke-width="1.8"/>
      <path d="M 398.5 656 A 76 76 0 0 1 330.0 580" fill="none" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3,3"/>
      <text x="360" y="625" fill="#cbd5e1" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">P-02 0,80</text>
    </g>

    <!-- PUERTA P-03 ACÚSTICA (HALL <-> DESPACHO, 0,82m Rw38dB) -->
    <g class="cad-door" id="door-P03">
      <line x1="740.5" y1="620" x2="740.5" y2="702" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,2"/>
      <line x1="740.5" y1="620" x2="815.0" y2="620" stroke="#38bdf8" stroke-width="2.0"/>
      <path d="M 740.5 702 A 82 82 0 0 0 815.0 620" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="3,3"/>
      <rect x="710" y="640" width="85" height="24" fill="#0b1120" stroke="#ef4444" stroke-width="0.8"/>
      <text x="752" y="652" fill="#fca5a5" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">P-03 · 0,82m</text>
      <text x="752" y="661" fill="#ef4444" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">Rw ≥ 38 dB</text>
    </g>

    <!-- PUERTA P-04 (DESPACHO <-> DISTRIBUIDOR NEUTRO, 0,80m) -->
    <g class="cad-door" id="door-P04">
      <line x1="1111.0" y1="675" x2="1111.0" y2="745" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,2"/>
      <line x1="1111.0" y1="675" x2="1045.0" y2="675" stroke="#cbd5e1" stroke-width="1.8"/>
      <path d="M 1111.0 745 A 70 70 0 0 1 1045.0 675" fill="none" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3,3"/>
      <text x="1080" y="715" fill="#cbd5e1" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">P-04 0,80</text>
    </g>

    <!-- PUERTA P-05 (DISTRIBUIDOR <-> BAÑO PB, 0,75m) -->
    <g class="cad-door" id="door-P05">
      <line x1="1180.0" y1="670" x2="1251.0" y2="670" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,2"/>
      <line x1="1180.0" y1="670" x2="1180.0" y2="600" stroke="#cbd5e1" stroke-width="1.8"/>
      <path d="M 1251.0 670 A 71 71 0 0 0 1180.0 600" fill="none" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3,3"/>
      <text x="1225" y="640" fill="#cbd5e1" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">P-05 0,75 NHG</text>
    </g>

    <!-- PUERTA CORREDERA P-06 EMPOTRADA (DISTRIBUIDOR <-> COCINA UNIFICADA, 0,80m) -->
    <g class="cad-door" id="door-P06">
      <rect x="1220.0" y="747" width="76.0" height="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
      <!-- Guía corredera -->
      <line x1="1144.0" y1="750" x2="1296.0" y2="750" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="3,2"/>
      <circle cx="1225" cy="750" r="2.5" fill="#38bdf8"/>
      <text x="1258" y="768" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">P-06 0,80 CORREDERA (A COCINA)</text>
    </g>
    """)

    # MOBILIARIO Y EQUIPAMIENTO DETALLADO
    # 1. ZAGUÁN MUDROOM:
    # Banco zapatero 1,60 x 0,45 m (x=190 a 342, y=430 a 472)
    # Gabanero 1,25 x 0,60 m (x=270 a 388, y=500 a 557)
    # Secador térmico para surf/neoprenos (x=190 a 240, y=590 a 670)
    svg.append("""
    <!-- MOBILIARIO ZAGUÁN MUDROOM [E-03] -->
    <!-- Banco zapatero 1,60 x 0,45 m -->
    <rect x="190.0" y="430" width="152.0" height="42.7" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0" rx="2"/>
    <text x="266.0" y="455" fill="#f8fafc" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">BANCO ZAPATERO 1,60×0,45 m</text>
    <line x1="228" y1="430" x2="228" y2="472.7" stroke="#475569" stroke-width="0.5"/>
    <line x1="266" y1="430" x2="266" y2="472.7" stroke="#475569" stroke-width="0.5"/>
    <line x1="304" y1="430" x2="304" y2="472.7" stroke="#475569" stroke-width="0.5"/>

    <!-- Gabanero empotrado 1,25 x 0,60 m -->
    <rect x="270.0" y="500" width="118.7" height="57.0" fill="#131c31" stroke="#cbd5e1" stroke-width="1.0"/>
    <line x1="270" y1="500" x2="388.7" y2="557" stroke="#475569" stroke-width="0.5"/>
    <line x1="388.7" y1="500" x2="270" y2="557" stroke="#475569" stroke-width="0.5"/>
    <line x1="329.3" y1="500" x2="329.3" y2="557" stroke="#38bdf8" stroke-width="0.7"/>
    <text x="329.3" y="533" fill="#cbd5e1" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">GABANERO 1,25×0,60</text>

    <!-- Secador térmico surf/abrigos -->
    <rect x="190.0" y="590" width="55.0" height="80.0" fill="#131c31" stroke="#f59e0b" stroke-width="1.0"/>
    <line x1="190" y1="590" x2="245" y2="670" stroke="#78350f" stroke-width="0.5"/>
    <line x1="245" y1="590" x2="190" y2="670" stroke="#78350f" stroke-width="0.5"/>
    <g transform="translate(217.5, 630) rotate(-90)">
      <text x="0" y="3" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">SECADOR SURF</text>
    </g>

    <!-- Rejilla VMC Extracción Zaguán -->
    <rect x="350" y="440" width="22" height="22" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
    <line x1="350" y1="440" x2="372" y2="462" stroke="#38bdf8" stroke-width="0.6"/>
    <line x1="372" y1="440" x2="350" y2="462" stroke="#38bdf8" stroke-width="0.6"/>
    <text x="361" y="475" fill="#38bdf8" font-family="monospace" font-size="6" text-anchor="middle">VMC-E 30m³/h</text>
    """)

    # 2. HALL PRINCIPAL [E-04]
    # Bajante B-02 Ø110, CGMP + RITI, Círculo Ø1,50 m NHG
    svg.append("""
    <!-- HALL PRINCIPAL [E-04] -->
    <!-- Bajante B-02 insonorizada (de P1) -->
    <circle cx="430.0" cy="460" r="10.5" fill="#0b1120" stroke="#ef4444" stroke-width="1.5"/>
    <circle cx="430.0" cy="460" r="5.2" fill="#ef4444"/>
    <text x="430.0" y="482" fill="#fca5a5" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">BAJANTE B-02 Ø110</text>

    <!-- Armario empotrado CGMP + RITI en tabique oeste -->
    <rect x="393.5" y="670" width="12" height="60" fill="#0b1120" stroke="#ef4444" stroke-width="1.2"/>
    <g transform="translate(415, 700) rotate(-90)">
      <text x="0" y="0" fill="#ef4444" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">CGMP + RITI</text>
    </g>

    <!-- Círculo de maniobra accesible Ø1,50 m NHG (radio = 71.25 px) -->
    <g class="nhg-accessible-circle" opacity="0.6">
      <circle cx="560.0" cy="580" r="71.25" fill="none" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,4"/>
      <line x1="550" y1="580" x2="570" y2="580" stroke="#10b981" stroke-width="0.8"/>
      <line x1="560" y1="570" x2="560" y2="590" stroke="#10b981" stroke-width="0.8"/>
      <text x="560" y="605" fill="#10b981" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">Ø 1,50 m NHG ACCESIBLE</text>
    </g>

    <!-- Flecha de circulación hacia Corredor y Patio Sur -->
    <line x1="560" y1="670" x2="560" y2="740" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arrow-tech)"/>
    <text x="560" y="730" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">HACIA GALERÍA / PATIO SUR</text>
    """)

    # 3. DESPACHO / SUITE PB [E-05]
    # Mesa ergonómica 90° con silla, Sofá-cama 140, VMC-I 35m³/h, Círculo Ø1,50 m
    # Mesa: x=755 a 850, y=430 a 530
    svg.append("""
    <!-- DESPACHO / SUITE PB [E-05] -->
    <!-- Mesa de trabajo ergonómica a 90° -->
    <path d="M 755 430 L 870 430 L 870 490 L 815 490 L 815 540 L 755 540 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <rect x="765" y="445" width="45" height="28" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.6"/>
    <text x="800" y="440" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">MESA 90° (TELETRABAJO)</text>
    <!-- Silla de oficina giratoria -->
    <circle cx="820" cy="515" r="14" fill="#0f172a" stroke="#94a3b8" stroke-width="0.8"/>
    <circle cx="820" cy="515" r="5" fill="#38bdf8"/>

    <!-- Sofá-Cama 140 cm (1,40 x 0,90 m plegado / 1,40 x 2,00 m abierto) -->
    <!-- Posición: pared este (x=1010 a 1105, y=430 a 530) -->
    <rect x="1010.0" y="430" width="95.0" height="133.0" rx="3" fill="#1e293b" stroke="#94a3b8" stroke-width="1.0"/>
    <rect x="1010.0" y="430" width="95.0" height="18.0" fill="#334155"/>
    <rect x="1020.0" y="455" width="75.0" height="25.0" rx="2" fill="#0f172a" stroke="#64748b" stroke-width="0.6"/>
    <line x1="1010.0" y1="495" x2="1105.0" y2="495" stroke="#475569" stroke-width="0.8" stroke-dasharray="3,2"/>
    <text x="1057.5" y="525" fill="#e2e8f0" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">SOFÁ-CAMA 140</text>
    <text x="1057.5" y="537" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">(SUITE INVITADOS / PB)</text>

    <!-- Impulsión VMC Despacho -->
    <circle cx="940" cy="510" r="10" fill="#0b1120" stroke="#10b981" stroke-width="1.2"/>
    <line x1="933" y1="510" x2="947" y2="510" stroke="#10b981" stroke-width="1.0"/>
    <line x1="940" y1="503" x2="940" y2="517" stroke="#10b981" stroke-width="1.0"/>
    <text x="940" y="532" fill="#10b981" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">VMC-I 35m³/h</text>

    <!-- Círculo accesible Ø1,50 m Despacho -->
    <g class="nhg-accessible-circle" opacity="0.6">
      <circle cx="920.0" cy="620" r="71.25" fill="none" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,4"/>
      <text x="920" y="623" fill="#10b981" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">Ø 1,50 m NHG</text>
    </g>

    <!-- Ventanal sur hacia patio: Fijo Cor Vision 4,00 x 2,60 m (y=750) -->
    <rect x="740.5" y="746" width="370.5" height="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="925" y="768" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">FIJO COR VISION PLUS (AL PATIO CENTRAL)</text>
    """)

    # 4. BAÑO COMPLETO PB [E-06]
    # Lavabo 90x50 cm, inodoro suspendido con cisterna Geberit, ducha 1,15x0,90m cota cero con sumidero lineal
    # Mueble lavabo: x=1125 a 1210, y=425 a 468
    # Inodoro suspendido: x=1240 a 1285, y=425 a 480
    # Ducha: x=1310 a 1420 (1.15m), y=425 a 510 (0.90m)
    svg.append("""
    <!-- BAÑO COMPLETO PB [E-06] -->
    <!-- Mueble Lavabo Suspendido 90x50 cm -->
    <g class="cad-sanitary">
      <rect x="1125.0" y="425" width="85.5" height="47.5" rx="2" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0"/>
      <ellipse cx="1167.7" cy="448.7" rx="28.5" ry="14.2" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
      <circle cx="1167.7" cy="448.7" r="2.5" fill="#38bdf8"/>
      <text x="1167.7" y="484" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">LAVABO 90×50</text>
    </g>

    <!-- Inodoro Suspendido con Cisterna Oculta Geberit -->
    <g class="cad-sanitary">
      <rect x="1235.0" y="420" width="47.5" height="15.0" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
      <path d="M 1240.0 435 L 1277.5 435 Q 1280.0 480 1258.7 480 Q 1237.5 480 1240.0 435 Z" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.0"/>
      <ellipse cx="1258.7" cy="455" rx="10.5" ry="13.0" fill="none" stroke="#64748b" stroke-width="0.6"/>
      <text x="1258.7" y="495" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">INODORO GEBERIT</text>
    </g>

    <!-- Gran Ducha Enrasada a Cota Cero 1,15 x 0,90 m -->
    <g class="cad-shower">
      <rect x="1310.0" y="425" width="115.0" height="90.0" fill="#131c31" stroke="#38bdf8" stroke-width="1.2"/>
      <!-- Mampara de vidrio templado fijo de 10mm (x=1310, y=425 a 500) -->
      <line x1="1310.0" y1="425" x2="1310.0" y2="505" stroke="#38bdf8" stroke-width="2.8"/>
      <circle cx="1310.0" cy="505" r="3.0" fill="#38bdf8"/>
      <!-- Líneas de caída de pendiente 2% hacia sumidero lineal este -->
      <line x1="1315" y1="430" x2="1415" y2="445" stroke="#475569" stroke-width="0.5" stroke-dasharray="3,2"/>
      <line x1="1315" y1="510" x2="1415" y2="495" stroke="#475569" stroke-width="0.5" stroke-dasharray="3,2"/>
      <line x1="1330" y1="470" x2="1410" y2="470" stroke="#38bdf8" stroke-width="0.6" marker-end="url(#arrow-tech)"/>
      <!-- Sumidero lineal oculto AISI 316 -->
      <rect x="1417.0" y="435" width="6" height="70" fill="#38bdf8"/>
      <!-- Rociador cenital XXL Ø25cm -->
      <circle cx="1370" cy="470" r="12" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2,2"/>
      <text x="1365" y="527" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">DUCHA 1,15×0,90 COTA CERO</text>
    </g>

    <!-- Bajante esquina noreste y extracción VMC -->
    <circle cx="1418" cy="405" r="8" fill="#0b1120" stroke="#ef4444" stroke-width="1.2"/>
    <text x="1395" y="408" fill="#ef4444" font-family="monospace" font-size="6" text-anchor="end">BAJANTE</text>
    <rect x="1275" y="515" width="20" height="20" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
    <line x1="1275" y1="515" x2="1295" y2="535" stroke="#38bdf8" stroke-width="0.6"/>
    <line x1="1295" y1="515" x2="1275" y2="535" stroke="#38bdf8" stroke-width="0.6"/>
    <text x="1285" y="546" fill="#38bdf8" font-family="monospace" font-size="6" text-anchor="middle">VMC-E 50m³/h</text>
    """)

    # 5. DISTRIBUIDOR NEUTRO NHG (ESCLUSA DE AISLAMIENTO)
    svg.append("""
    <!-- DISTRIBUIDOR NEUTRO NHG -->
    <g class="distribuidor-nhg">
      <rect x="1135" y="695" width="270" height="32" rx="2" fill="#0b1120" stroke="#10b981" stroke-width="1.0"/>
      <text x="1270" y="709" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="900" text-anchor="middle">DISTRIBUIDOR NEUTRO NHG (DOBLE PUERTA)</text>
      <text x="1270" y="721" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">Cumplimiento Decreto 29/2010 Galicia · Independencia Baño PB</text>
    </g>
    """)

    # RÓTULOS DE ESTANCIAS OFICIALES (ROOM STAMPS)
    stamps = [
        (260.0, 520.0, "[E-03] ZAGUÁN MUDROOM", "S.Útil: 5,80 m²", "Porcelánico C3 · Z=±0,00m"),
        (560.0, 500.0, "[E-04] HALL PRINCIPAL", "S.Útil: 10,40 m²", "Roble 14mm · Z=±0,00m"),
        (925.0, 560.0, "[E-05] DESPACHO / SUITE", "S.Útil: 11,50 m²", "Roble 14mm · Rw38dB · Z=±0,00m"),
        (1210.0, 580.0, "[E-06] BAÑO COMPLETO PB", "S.Útil: 5,20 m²", "Porcelánico C3 · Z=±0,00m")
    ]
    for rx, ry, rcode, rsurf, rmat in stamps:
        svg.append(f"""
        <g class="room-stamp">
          <rect x="{rx-65:.1f}" y="{ry-22:.1f}" width="130" height="44" rx="2" fill="#0b1120" fill-opacity="0.92" stroke="#38bdf8" stroke-width="0.9"/>
          <line x1="{rx-65:.1f}" y1="{ry-7:.1f}" x2="{rx+65:.1f}" y2="{ry-7:.1f}" stroke="#334155" stroke-width="0.6"/>
          <text x="{rx:.1f}" y="{ry-11:.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="900" text-anchor="middle">{rcode}</text>
          <text x="{rx:.1f}" y="{ry+6:.1f}" fill="#f8fafc" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">{rsurf}</text>
          <text x="{rx:.1f}" y="{ry+16:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.2" text-anchor="middle">{rmat}</text>
        </g>
        """)

    # CUADRO DE SUPERFICIES Y CARPINTERÍAS DEL ALA NORTE (Inferior)
    svg.append("""
    <g transform="translate(60, 850)">
      <!-- Panel 1: Cuadro de Superficies -->
      <rect x="0" y="0" width="580" height="280" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="580" height="28" fill="#1e293b"/>
      <text x="15" y="19" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="900">CUADRO DE SUPERFICIES ÚTILES · ALA NORTE PB</text>
      
      <text x="20" y="55" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">[E-02] Porche Entrada Noble Norte (Exterior)</text>
      <text x="440" y="55" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">3,50 m²</text>
      <text x="20" y="70" fill="#94a3b8" font-family="monospace" font-size="6.5">Losas de granito silvestre abujardado C3 cota +0,05m</text>
      <line x1="20" y1="80" x2="560" y2="80" stroke="#1e293b" stroke-width="0.8"/>

      <text x="20" y="100" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">[E-03] Zaguán Mudroom (Filtro Atlántico)</text>
      <text x="440" y="100" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">5,80 m²</text>
      <text x="20" y="115" fill="#94a3b8" font-family="monospace" font-size="6.5">Banco zapatero 1,60×0,45m, gabanero 1,25×0,60m, secador neoprenos</text>
      <line x1="20" y1="125" x2="560" y2="125" stroke="#1e293b" stroke-width="0.8"/>

      <text x="20" y="145" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">[E-04] Hall Principal de Entrada</text>
      <text x="440" y="145" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">10,40 m²</text>
      <text x="20" y="160" fill="#94a3b8" font-family="monospace" font-size="6.5">Roble 14mm, CGMP+RITI integrado, conexión directa con patio</text>
      <line x1="20" y1="170" x2="560" y2="170" stroke="#1e293b" stroke-width="0.8"/>

      <text x="20" y="190" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">[E-05] Despacho / Dormitorio Suite PB Adaptable</text>
      <text x="440" y="190" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">11,50 m²</text>
      <text x="20" y="205" fill="#94a3b8" font-family="monospace" font-size="6.5">Mesa 90°, sofá-cama 140, tabique acústico Rw38dB, VMC-I 35m³/h</text>
      <line x1="20" y1="215" x2="560" y2="215" stroke="#1e293b" stroke-width="0.8"/>

      <text x="20" y="235" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">[E-06] Baño Completo PB + Distribuidor Neutro</text>
      <text x="440" y="235" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">5,20 m²</text>
      <text x="20" y="250" fill="#94a3b8" font-family="monospace" font-size="6.5">Ducha cota cero 1,15×0,90m sumidero lineal, Geberit, lavabo 90×50</text>
      <rect x="20" y="258" width="540" height="16" fill="#131c31"/>
      <text x="25" y="269" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">TOTAL S.ÚTIL INTERIOR ALA NORTE PB: 32,90 m²</text>

      <!-- Panel 2: Cuadro de Carpinterías -->
      <g transform="translate(610, 0)">
        <rect x="0" y="0" width="600" height="280" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
        <rect x="0" y="0" width="600" height="28" fill="#1e293b"/>
        <text x="15" y="19" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="900">CUADRO DE CARPINTERÍAS Y PUERTAS (ALA NORTE)</text>
        
        <text x="20" y="55" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700">C-01 · PUERTA PRINCIPAL PIVOTANTE ACORAZADA</text>
        <text x="450" y="55" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700">1,00 × 2,40 m</text>
        <text x="20" y="68" fill="#94a3b8" font-family="monospace" font-size="6.5">Hoja pivotante con eje oculto descentrado, cerradura biométrica motorizada Grado 4</text>
        <line x1="20" y1="76" x2="580" y2="76" stroke="#1e293b" stroke-width="0.8"/>

        <text x="20" y="94" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700">C-03 · VENTANAL DESPACHO NORTE (ANTEPECHO h=95cm)</text>
        <text x="450" y="94" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700">1,80 × 1,20 m</text>
        <text x="20" y="107" fill="#94a3b8" font-family="monospace" font-size="6.5">Cortizo COR-70 Hoja Oculta RPT, triple vidrio 4+4/16Ar/6 acústico bajo emisivo</text>
        <line x1="20" y1="115" x2="580" y2="115" stroke="#1e293b" stroke-width="0.8"/>

        <text x="20" y="133" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700">C-04 · VENTANA BAÑO PB ALTA INTIMIDAD (ANTEPECHO h=160cm)</text>
        <text x="450" y="133" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700">0,80 × 0,60 m</text>
        <text x="20" y="146" fill="#94a3b8" font-family="monospace" font-size="6.5">Oscilobatiente Cortizo COR-70 con vidrio mateado traslúcido y rotura térmica</text>
        <line x1="20" y1="154" x2="580" y2="154" stroke="#1e293b" stroke-width="0.8"/>

        <text x="20" y="172" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">P-02 · PUERTA PASO ZAGUÁN - HALL</text>
        <text x="450" y="172" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">0,80 × 2,10 m</text>
        <text x="20" y="185" fill="#94a3b8" font-family="monospace" font-size="6.5">Puerta enrasada de paso térmico para corte de brisa atlántica</text>
        <line x1="20" y1="193" x2="580" y2="193" stroke="#1e293b" stroke-width="0.8"/>

        <text x="20" y="211" fill="#ef4444" font-family="monospace" font-size="7.5" font-weight="700">P-03 · PUERTA ACÚSTICA DESPACHO / DORMITORIO SUITE</text>
        <text x="450" y="211" fill="#ef4444" font-family="monospace" font-size="7.5" font-weight="700">0,82 × 2,10 m</text>
        <text x="20" y="224" fill="#94a3b8" font-family="monospace" font-size="6.5">Puerta maciza fonoabsorbente con guillotina inferior y junta perimetral Rw ≥ 38 dB</text>
        <line x1="20" y1="232" x2="580" y2="232" stroke="#1e293b" stroke-width="0.8"/>

        <text x="20" y="250" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">P-04 / P-05 / P-06 · ESCLUSA DISTRIBUIDOR NEUTRO NHG</text>
        <text x="450" y="250" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">0,80 / 0,75 / 0,80 m</text>
        <text x="20" y="263" fill="#94a3b8" font-family="monospace" font-size="6.5">P-04 paso despacho, P-05 paso baño completo, P-06 corredera empotrada a cocina</text>
      </g>

      <!-- Panel 3: Cumplimiento Normativo NHG / CTE -->
      <g transform="translate(1240, 0)">
        <rect x="0" y="0" width="560" height="280" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
        <rect x="0" y="0" width="560" height="28" fill="#1e293b"/>
        <text x="15" y="19" fill="#10b981" font-family="monospace" font-size="9" font-weight="900">DICTAMEN NORMATIVO HABITABILIDAD (NHG / CTE)</text>
        
        <text x="15" y="55" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">1. INDEPENDENCIA DEL BAÑO PB (DECRETO 29/2010 NHG):</text>
        <text x="15" y="70" fill="#94a3b8" font-family="monospace" font-size="6.8">El baño completo E-06 NO comunica directamente con la cocina ni con el</text>
        <text x="15" y="82" fill="#94a3b8" font-family="monospace" font-size="6.8">comedor. Cuenta con distribuidor neutro previo con doble puerta (P-05 y P-06).</text>

        <text x="15" y="105" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">2. ACCESIBILIDAD Y MOVILIDAD REDUCIDA (CTE DB-SUA / NHG):</text>
        <text x="15" y="120" fill="#94a3b8" font-family="monospace" font-size="6.8">Círculos de giro Ø 1,50 m libres de obstáculos garantizados en Hall (E-04)</text>
        <text x="15" y="132" fill="#94a3b8" font-family="monospace" font-size="6.8">y Despacho (E-05). Itinerario accesible cota cero entre porche, hall y suite.</text>

        <text x="15" y="155" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">3. CONFORT ACÚSTICO TELETRABAJO (CTE DB-HR):</text>
        <text x="15" y="170" fill="#94a3b8" font-family="monospace" font-size="6.8">Tabique divisorio Hall-Despacho compuesto por doble placa de yeso laminado</text>
        <text x="15" y="182" fill="#94a3b8" font-family="monospace" font-size="6.8">con alma de lana de roca 50mm e interposición elástica (Rw ≥ 38 dBA).</text>

        <text x="15" y="205" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">4. SALUBRIDAD Y CALIDAD DEL AIRE INTERIOR (CTE DB-HS3):</text>
        <text x="15" y="220" fill="#94a3b8" font-family="monospace" font-size="6.8">Extracción mecánica continúa: Zaguán (30 m³/h) y Baño PB (50 m³/h).</text>
        <text x="15" y="232" fill="#94a3b8" font-family="monospace" font-size="6.8">Impulsión higiénica en Despacho / Suite (35 m³/h) mediante VMC Zehnder.</text>

        <rect x="15" y="246" width="530" height="22" fill="#131c31" stroke="#10b981" stroke-width="0.8"/>
        <text x="280" y="260" fill="#10b981" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">ESTADO: CONFORME 100% NHG GALICIA Y PXOM OLEIROS</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def generate_plano_acceso_elevaciones():
    """Genera plano A-02: Alzados y Secciones Técnicas 1:20 del Ala Norte"""
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">ALA NORTE: ALZADOS ARQUITECTÓNICOS Y SECCIONES TÉCNICAS (1:20)</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">ALZADO NORTE EXTERIOR · SECCIÓN LONGITUDINAL INTERIOR · COTAS VERTICALES CTE DB-SUA / DB-HE · PLANO A-02</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # 1. ALZADO 1: FACHADA NORTE EXTERIOR (Y = 140 a 540)
    # Altura de planta baja = 3,00 m (escala vertical 1m = 100px)
    # Suelo Z=±0,00m en y=440
    # Techo Z=+3,00m en y=140
    # X de 180 a 1450 (1270 px)
    svg.append("""
    <!-- ========================================== -->
    <!-- ALZADO 1: FACHADA NORTE EXTERIOR           -->
    <!-- ========================================== -->
    <g transform="translate(0, 0)">
      <text x="180" y="130" fill="#f59e0b" font-family="monospace" font-size="12" font-weight="900">ALZADO 01: FACHADA NORTE EXTERIOR (ACCESO PRINCIPAL, PORCHE Y HUECOS DE VENTANA)</text>
      
      <!-- Línea de cota terreno natural y acera exterior -->
      <line x1="120" y1="440" x2="1520" y2="440" stroke="#64748b" stroke-width="1.5"/>
      <text x="140" y="455" fill="#94a3b8" font-family="monospace" font-size="7.5">ACERA EXTERIOR Z=±0,00m</text>

      <!-- Cuerpo Edificado Fachada Norte (Zaguán, Porche, Despacho, Baño) -->
      <!-- Zaguán: x=180 a 398.5 -->
      <rect x="180.0" y="140" width="218.5" height="300" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>
      <g transform="translate(289, 290)">
        <text x="0" y="0" fill="#64748b" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">FACHADA CIEGA ZAGUÁN</text>
        <text x="0" y="15" fill="#475569" font-family="monospace" font-size="7.5" text-anchor="middle">(AISLAMIENTO SATE 12cm SILICONA GRIS)</text>
      </g>

      <!-- Porche Retranqueado y Puerta Principal C-01: x=398.5 a 740.5 -->
      <!-- Voladizo superior de porche -->
      <rect x="398.5" y="140" width="342.0" height="30" fill="#0b1120" stroke="#f59e0b" stroke-width="1.2"/>
      <text x="569.5" y="160" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">VOLADIZO HORMIGÓN VISTO ENTRADA NOBLE</text>
      <!-- Fondo del porche -->
      <rect x="398.5" y="170" width="342.0" height="265" fill="#131c31" stroke="#334155" stroke-width="0.8"/>
      <!-- Peldaño granito z=+0,05m -->
      <rect x="398.5" y="435" width="342.0" height="5" fill="#64748b"/>
      <!-- Puerta Pivotante C-01 (1,00 x 2,40 m): x=570 a 670, y=195 a 435 -->
      <rect x="570.0" y="195" width="100.0" height="240" fill="#0f172a" stroke="#f59e0b" stroke-width="1.8"/>
      <rect x="575.0" y="200" width="90.0" height="230" fill="#18181b" stroke="#78350f" stroke-width="0.8"/>
      <!-- Fijo de vidrio lateral de seguridad -->
      <rect x="500.0" y="195" width="60.0" height="240" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
      <line x1="500" y1="195" x2="560" y2="435" stroke="#38bdf8" stroke-width="0.4" opacity="0.5"/>
      <text x="530" y="320" fill="#38bdf8" font-family="monospace" font-size="7" text-anchor="middle">FIJO VIDRIO</text>
      <!-- Tirador vertical integrado negro -->
      <rect x="655" y="270" width="4" height="90" rx="1" fill="#f59e0b"/>
      <text x="620" y="310" fill="#fde68a" font-family="monospace" font-size="8" font-weight="900" text-anchor="middle">C-01 · PIVOTANTE</text>
      <text x="620" y="325" fill="#cbd5e1" font-family="monospace" font-size="7" text-anchor="middle">1,00 × 2,40 m</text>

      <!-- Fachada Despacho con ventana C-03: x=740.5 a 1111.0 -->
      <rect x="740.5" y="140" width="370.5" height="300" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>
      <!-- Ventana C-03: Ancho 1,80m (180px), Alto 1,20m (120px), Antepecho h=95cm (y=345 a 225) -->
      <!-- x=840 a 1020 -->
      <rect x="840.0" y="225" width="180.0" height="120" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
      <line x1="930.0" y1="225" x2="930.0" y2="345" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="930.0" y="285" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">C-03 · 1,80×1,20 m</text>
      <text x="930.0" y="298" fill="#94a3b8" font-family="monospace" font-size="6.5" text-anchor="middle">ANTEPECHO h = 0,95 m</text>

      <!-- Fachada Baño PB con ventana C-04: x=1111.0 a 1429.25 -->
      <rect x="1111.0" y="140" width="318.25" height="300" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>
      <!-- Ventana C-04: Ancho 0,80m (80px), Alto 0,60m (60px), Antepecho h=160cm (y=280 a 220) -->
      <!-- x=1150 a 1230 -->
      <rect x="1150.0" y="220" width="80.0" height="60" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="1190.0" y="250" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">C-04 · 0,80×0,60</text>
      <text x="1190.0" y="262" fill="#94a3b8" font-family="monospace" font-size="6" text-anchor="middle">h = 1,60 m</text>

      <!-- Cotas de altura Fachada Norte -->
      <!-- Altura libre 3,00m -->
      <g transform="translate(1450, 0)">
        <line x1="20" y1="140" x2="20" y2="440" stroke="#38bdf8" stroke-width="0.8" marker-start="url(#tick-45)" marker-end="url(#tick-45)"/>
        <text x="35" y="290" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">H. CORNISA = +3,00 m</text>
        <!-- Cota antepecho C-03 -->
        <line x1="0" y1="345" x2="15" y2="345" stroke="#94a3b8" stroke-width="0.5"/>
        <text x="35" y="348" fill="#94a3b8" font-family="monospace" font-size="7">Antepecho C-03 = +0,95 m</text>
        <!-- Cota dintel C-01 -->
        <line x1="0" y1="195" x2="15" y2="195" stroke="#f59e0b" stroke-width="0.5"/>
        <text x="35" y="198" fill="#f59e0b" font-family="monospace" font-size="7">Dintel C-01 = +2,45 m</text>
      </g>
    </g>
    """)

    # 2. SECCIÓN 2: SECCIÓN LONGITUDINAL INTERIOR ZAGUÁN - HALL - DESPACHO - BAÑO (Y = 600 a 1050)
    # Suelo Z=±0,00m en y=920
    # Falso techo Z=+2,60m en y=660
    # Forjado superior Z=+3,00m en y=620
    svg.append("""
    <!-- ========================================== -->
    <!-- ALZADO 2: SECCIÓN LONGITUDINAL INTERIOR    -->
    <!-- ========================================== -->
    <g transform="translate(0, 520)">
      <text x="180" y="110" fill="#10b981" font-family="monospace" font-size="12" font-weight="900">ALZADO 02: SECCIÓN INTERIOR DETALLADA (ZAGUÁN MUDROOM, HALL, DESPACHO Y BAÑO COMPLETO)</text>
      
      <!-- Forjado de Suelo PB (Solera ventilada sobre Caviti + Aislamiento XPS 100mm + Suelo Radiante) -->
      <rect x="146" y="400" width="1317.25" height="40" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.0"/>
      <line x1="120" y1="400" x2="1480" y2="400" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="140" y="425" fill="#38bdf8" font-family="monospace" font-size="7.5">COTA INTERIOR ACABADA Z = ±0,00 m</text>

      <!-- Falso techo continuo Pladur hidrófugo con foso perimetral LED (h=2,60m en y=140) -->
      <rect x="180" y="140" width="1249.25" height="15" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="180" y="130" fill="#f59e0b" font-family="monospace" font-size="7.5">FALSO TECHO CONTINUO (ALTURA LIBRE = 2,60 m)</text>

      <!-- 1. INTERIOR ZAGUÁN (x=180 a 398.5): Banco zapatero y armario gabanero -->
      <!-- Pared de fondo zaguán -->
      <rect x="180" y="155" width="208.5" height="245" fill="#111827"/>
      <!-- Banco zapatero en sección (y=355 a 400, altura 45cm = 45px) -->
      <rect x="190" y="355" width="130" height="45" rx="2" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0"/>
      <text x="255" y="380" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">BANCO ZAPATERO (h=45cm)</text>
      <!-- Perchero de pared y estante superior -->
      <line x1="190" y1="240" x2="320" y2="240" stroke="#f59e0b" stroke-width="2.0"/>
      <circle cx="210" cy="248" r="3" fill="#f59e0b"/>
      <circle cx="240" cy="248" r="3" fill="#f59e0b"/>
      <circle cx="270" cy="248" r="3" fill="#f59e0b"/>
      <circle cx="300" cy="248" r="3" fill="#f59e0b"/>
      <text x="255" y="232" fill="#fde68a" font-family="monospace" font-size="6.5" text-anchor="middle">PERCHERO GABANERO</text>

      <!-- Tabique divisorio Eje B (x=388.5 a 398.5) con Puerta P-02 abierta -->
      <rect x="388.5" y="155" width="10" height="245" fill="#334155"/>
      <rect x="388.5" y="190" width="10" height="210" fill="#0b1120" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="393.5" y="270" fill="#cbd5e1" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle" transform="rotate(-90 393.5 270)">PASO P-02 (0,80m)</text>

      <!-- 2. INTERIOR HALL PRINCIPAL (x=398.5 a 740.5) -->
      <rect x="398.5" y="155" width="336" height="245" fill="#131c31"/>
      <!-- Puerta principal pivotante C-01 vista desde dentro -->
      <rect x="440" y="160" width="100" height="240" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
      <text x="490" y="260" fill="#fde68a" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">C-01 PIVOTANTE INTERIOR</text>
      <!-- Armario CGMP + RITI empotrado -->
      <rect x="580" y="240" width="70" height="110" fill="#0b1120" stroke="#ef4444" stroke-width="1.0"/>
      <text x="615" y="295" fill="#ef4444" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">CGMP + RITI</text>

      <!-- Tabique Acústico Rw38dB Eje C (x=734.5 a 746.5) con Puerta P-03 -->
      <rect x="734.5" y="155" width="12" height="245" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>
      <rect x="734.5" y="190" width="12" height="210" fill="#0b1120" stroke="#ef4444" stroke-width="1.2"/>
      <text x="740.5" y="280" fill="#fca5a5" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle" transform="rotate(-90 740.5 280)">P-03 ACÚSTICA Rw38dB</text>

      <!-- 3. INTERIOR DESPACHO / SUITE (x=746.5 a 1105.0) -->
      <rect x="746.5" y="155" width="358.5" height="245" fill="#1e293b"/>
      <!-- Mesa de trabajo en sección con silla ergonómica -->
      <rect x="770" y="325" width="120" height="15" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>
      <line x1="780" y1="340" x2="780" y2="400" stroke="#cbd5e1" stroke-width="1.5"/>
      <line x1="880" y1="340" x2="880" y2="400" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="830" y="318" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">MESA TELETRABAJO (h=75cm)</text>
      <!-- Sofá-Cama 140 cm en sección -->
      <rect x="980" y="330" width="110" height="70" rx="3" fill="#0f172a" stroke="#94a3b8" stroke-width="1.0"/>
      <rect x="990" y="300" width="100" height="30" rx="2" fill="#1e293b"/>
      <text x="1035" y="365" fill="#e2e8f0" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">SOFÁ-CAMA 140</text>

      <!-- Tabique Eje D (x=1105.0 a 1117.0) con Puerta P-04 -->
      <rect x="1105.0" y="155" width="12" height="245" fill="#334155"/>

      <!-- 4. INTERIOR BAÑO COMPLETO PB (x=1117.0 a 1429.25) -->
      <rect x="1117.0" y="155" width="312.25" height="245" fill="#0f172a"/>
      <!-- Mueble Lavabo Suspendido (h=85cm en y=315) con espejo iluminado -->
      <rect x="1140" y="315" width="80" height="45" rx="1.5" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0"/>
      <rect x="1140" y="210" width="80" height="90" fill="#0b1120" stroke="#38bdf8" stroke-width="0.8"/>
      <text x="1180" y="255" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">ESPEJO LED</text>
      <text x="1180" y="342" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">LAVABO h=85cm</text>

      <!-- Inodoro Suspendido (h=42cm en y=358) -->
      <rect x="1245" y="358" width="40" height="42" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.0"/>
      <rect x="1240" y="290" width="50" height="110" fill="none" stroke="#64748b" stroke-width="0.6" stroke-dasharray="2,2"/>
      <rect x="1255" y="310" width="20" height="12" fill="#cbd5e1"/>
      <text x="1265" y="382" fill="#cbd5e1" font-family="monospace" font-size="6" text-anchor="middle">GEBERIT</text>

      <!-- Ducha cota cero 1,15m con mampara de vidrio (x=1310 a 1420) -->
      <line x1="1310" y1="160" x2="1310" y2="400" stroke="#38bdf8" stroke-width="2.5"/>
      <text x="1318" y="240" fill="#38bdf8" font-family="monospace" font-size="6" transform="rotate(-90 1318 240)">MAMPARA VIDRIO 10mm</text>
      <!-- Rociador de techo empotrado -->
      <rect x="1355" y="155" width="25" height="4" fill="#38bdf8"/>
      <line x1="1367" y1="159" x2="1367" y2="180" stroke="#38bdf8" stroke-width="1.5"/>
      <circle cx="1367" cy="183" r="10" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
      <text x="1367" y="350" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">DUCHA COTA CERO</text>
      <!-- Sumidero lineal este -->
      <rect x="1415" y="396" width="6" height="4" fill="#38bdf8"/>
      
      <!-- Muro Este Exterior -->
      <rect x="1429.25" y="140" width="34" height="300" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.0"/>

      <!-- Acotaciones de altura interior -->
      <g transform="translate(1480, 0)">
        <line x1="20" y1="155" x2="20" y2="400" stroke="#10b981" stroke-width="0.8" marker-start="url(#tick-emerald)" marker-end="url(#tick-emerald)"/>
        <text x="35" y="275" fill="#10b981" font-family="monospace" font-size="8" font-weight="700">ALTURA LIBRE = 2,60 m</text>
        <line x1="0" y1="315" x2="15" y2="315" stroke="#94a3b8" stroke-width="0.5"/>
        <text x="35" y="318" fill="#94a3b8" font-family="monospace" font-size="7">Plano Lavabo = +0,85 m</text>
        <line x1="0" y1="358" x2="15" y2="358" stroke="#94a3b8" stroke-width="0.5"/>
        <text x="35" y="361" fill="#94a3b8" font-family="monospace" font-size="7">Taza Inodoro = +0,42 m</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def generate_plano_acceso_electricidad():
    """Genera plano A-03: Electricidad, Cuadros REBT y Telecomunicaciones ICT-2 (1:20)"""
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">ALA NORTE: INSTALACIÓN ELÉCTRICA, CUADROS Y DATOS REBT / ICT-2</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">CUADRO GENERAL CGMP · RITI TELECOMUNICACIONES · TOMAS ESPECÍFICAS TELETRABAJO Y VOLÚMENES BAÑO · PLANO A-03</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Base esquemática atenuada
    svg.append("""
    <g opacity="0.35">
      <!-- Muros exteriores e interiores -->
      <rect x="180.0" y="380" width="1249.25" height="370" fill="none" stroke="#94a3b8" stroke-width="1.5"/>
      <line x1="398.5" y1="380" x2="398.5" y2="680" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="740.5" y1="380" x2="740.5" y2="750" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="1111.0" y1="380" x2="1111.0" y2="750" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="1111.0" y1="670" x2="1429.25" y2="670" stroke="#94a3b8" stroke-width="1.0"/>
      <!-- Nombres de estancias -->
      <text x="289" y="420" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">ZAGUÁN MUDROOM</text>
      <text x="569" y="420" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">HALL PRINCIPAL</text>
      <text x="925" y="420" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">DESPACHO / SUITE</text>
      <text x="1270" y="420" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">BAÑO COMPLETO PB</text>
    </g>
    """)

    # CUADRO GENERAL CGMP + RITI (Punto neurálgico en x=393.5, y=670 a 730)
    svg.append("""
    <!-- CUADRO GENERAL CGMP + RITI -->
    <g id="cgmp-panel">
      <rect x="375" y="660" width="35" height="85" fill="#0b1120" stroke="#ef4444" stroke-width="2.0"/>
      <text x="392" y="705" fill="#fca5a5" font-family="monospace" font-size="8" font-weight="900" text-anchor="middle" transform="rotate(-90 392 705)">CGMP + RITI</text>
      <!-- Canalizaciones de distribución que parten del cuadro -->
      <!-- Hacia Zaguán -->
      <path d="M 375 680 L 250 680 L 250 540" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
      <!-- Hacia Hall -->
      <path d="M 410 680 L 520 680 L 520 540" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
      <!-- Hacia Despacho -->
      <path d="M 410 710 L 750 710 L 800 520" fill="none" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,2"/>
      <!-- Hacia Baño PB -->
      <path d="M 410 730 L 1150 730 L 1150 520" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,2"/>
    </g>
    """)

    # TOMAS ELÉCTRICAS Y DATOS
    # 1. Zaguán Mudroom:
    # Toma schuko C2 para aspirador/banco (+30cm)
    # Toma schuko C4 dedicada secador de neoprenos/surf (+110cm)
    svg.append("""
    <!-- TOMAS ZAGUÁN -->
    <circle cx="210" cy="450" r="6" fill="#0b1120" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="225" y="453" fill="#fde68a" font-family="monospace" font-size="7">TOMA SECADOR C4 (16A, +1,10m)</text>
    
    <circle cx="340" cy="520" r="5" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="340" y="540" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">Schuko C2 (+0,30m)</text>
    """)

    # 2. Hall Principal:
    # Videointerfono IP conectado a domótica (+150cm)
    # Pulsador cerradura puerta C-01 y alimentación pivotante motorizada (+110cm)
    # Toma de servicio Schuko C2 (+30cm)
    svg.append("""
    <!-- DISPOSITIVOS HALL -->
    <!-- Videointerfono IP -->
    <rect x="560" y="440" width="16" height="24" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="585" y="455" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700">VIDEOINTERFONO IP (+1,50m)</text>
    <!-- Mando pivotante C-01 -->
    <circle cx="675" cy="440" r="5" fill="#f59e0b"/>
    <text x="690" y="443" fill="#f59e0b" font-family="monospace" font-size="6.5">ALIMENTACIÓN PIVOTANTE C-01</text>
    <!-- Toma Hall -->
    <circle cx="480" cy="580" r="5" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="480" y="600" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="middle">Schuko C2 (+0,30m)</text>
    """)

    # 3. Despacho / Teletrabajo:
    # Bloque de tomas en mesa 90°: 4 Schuko C2 + 2 RJ45 Cat 6A + USB-C PD 65W (+75cm)
    # Tomas sofá-cama: 2 Schuko + USB (+30cm)
    svg.append("""
    <!-- TOMAS DESPACHO TELETRABAJO -->
    <rect x="760" y="460" width="60" height="25" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="790" y="475" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">BLOQUE MESA 90°</text>
    <text x="790" y="500" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">4×Schuko + 2×RJ45 Cat6A + USB-C</text>
    
    <circle cx="1090" cy="460" r="5" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="1070" y="480" fill="#cbd5e1" font-family="monospace" font-size="6.5" text-anchor="end">2×Schuko Sofá (+0,30m)</text>

    <!-- Termostato independiente Despacho -->
    <rect x="755" y="600" width="14" height="18" rx="1" fill="#0b1120" stroke="#10b981" stroke-width="1.2"/>
    <text x="778" y="612" fill="#10b981" font-family="monospace" font-size="6.5">CRONO-TERMOSTATO SUELO (+1,50m)</text>
    """)

    # 4. Baño Completo PB:
    # Volúmenes de prohibición ITC-BT-27
    # Toma de afeitadora/secador en lavabo (Volumen 3, +110cm con diferencial dedicado 30mA)
    # Alimentación espejo antivaho LED
    svg.append("""
    <!-- SEGURIDAD ELÉCTRICA BAÑO PB (ITC-BT-27) -->
    <!-- Volumen 0 (Ducha): Prohibido tomas/interruptores -->
    <rect x="1310" y="425" width="115" height="90" fill="#ef4444" fill-opacity="0.15" stroke="#ef4444" stroke-width="1.0" stroke-dasharray="3,2"/>
    <text x="1367" y="465" fill="#fca5a5" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">VOLUMEN 0</text>
    <text x="1367" y="477" fill="#fca5a5" font-family="monospace" font-size="6" text-anchor="middle">IPX7 OBLIGATORIO</text>

    <!-- Volumen 1 (Sobre plato hasta 2,25m) -->
    <!-- Volumen 2 (0,60m alrededor ducha) -->
    <rect x="1270" y="425" width="40" height="90" fill="#f59e0b" fill-opacity="0.1" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="3,2"/>
    <text x="1290" y="470" fill="#fde68a" font-family="monospace" font-size="6" text-anchor="middle">VOL 2</text>

    <!-- Volumen 3 (Zona lavabo): Toma autorizada -->
    <circle cx="1135" cy="445" r="5" fill="#0b1120" stroke="#10b981" stroke-width="1.5"/>
    <text x="1135" y="468" fill="#10b981" font-family="monospace" font-size="6.5" text-anchor="middle">TOMA LAVABO C5</text>
    <text x="1135" y="478" fill="#cbd5e1" font-family="monospace" font-size="6" text-anchor="middle">(+1,10m IP44 Estanca)</text>
    """)

    # Memoria técnica eléctrica REBT
    svg.append("""
    <g transform="translate(60, 850)">
      <rect x="0" y="0" width="1800" height="280" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="1800" height="28" fill="#1e293b"/>
      <text x="15" y="19" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="900">ESQUEMA TÉCNICO DE CIRCUITOS Y ASIGNACIÓN REBT (ALA NORTE)</text>
      
      <g transform="translate(20, 45)">
        <text x="0" y="15" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">CIRCUITO C1 · ILUMINACIÓN Y CONTROL DOMÓTICO KNX / CASAMBI</text>
        <text x="0" y="30" fill="#94a3b8" font-family="monospace" font-size="7">Magnetotérmico 10A · Conductor H07Z1-K 1,5 mm² libre de halógenos · Downlights estancos baño + foso LED regulable</text>

        <text x="0" y="60" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">CIRCUITO C2 · TOMAS DE CORRIENTE DE USO GENERAL Y TELETRABAJO</text>
        <text x="0" y="75" fill="#94a3b8" font-family="monospace" font-size="7">Magnetotérmico 16A · Conductor H07Z1-K 2,5 mm² · Tomas despacho (ordenador, pantallas, impresoras), hall y zaguán</text>

        <text x="0" y="105" fill="#ef4444" font-family="monospace" font-size="8" font-weight="700">CIRCUITO C4.7 · CIRCUITO DEDICADO SECADOR SURF Y DESHUMIDIFICADOR</text>
        <text x="0" y="120" fill="#94a3b8" font-family="monospace" font-size="7">Magnetotérmico 16A individual en CGMP · Conductor H07Z1-K 2,5 mm² · Secador térmico zaguán para neoprenos húmedos</text>

        <text x="0" y="150" fill="#10b981" font-family="monospace" font-size="8" font-weight="700">CIRCUITO C5 · TOMAS DE CUARTO DE BAÑO (ZONA VOLUMEN 3)</text>
        <text x="0" y="165" fill="#94a3b8" font-family="monospace" font-size="7">Magnetotérmico 16A + Diferencial hiperinmunizado clase A 30mA · Conductor H07Z1-K 2,5 mm² · Toma estanca IP44</text>
      </g>

      <g transform="translate(900, 45)">
        <text x="0" y="15" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">RED DE TELECOMUNICACIONES ICT-2 (RITI PB)</text>
        <text x="0" y="30" fill="#94a3b8" font-family="monospace" font-size="7">Punto de Acceso a Usuario (PAU) de fibra óptica y cableado UTP Cat 6A libre de halógenos hasta rosetas de despacho</text>

        <text x="0" y="60" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">SEGURIDAD Y CONTROL DE ACCESOS</text>
        <text x="0" y="75" fill="#94a3b8" font-family="monospace" font-size="7">Cerradura inteligente motorizada puerta C-01 alimentada con SAI respaldo en CGMP · Apertura por huella / app</text>

        <text x="0" y="105" fill="#10b981" font-family="monospace" font-size="8" font-weight="700">CLIMATIZACIÓN Y VMC CONTROL ZONAL</text>
        <text x="0" y="120" fill="#94a3b8" font-family="monospace" font-size="7">Termostatos táctiles Modbus conectados a suelo radiante Uponor y control de caudal VMC Zehnder ComfoAir Q350</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def generate_plano_acceso_iluminacion():
    """Genera plano A-04: Iluminación Técnica, Escenas y Climatización/VMC (1:20)"""
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">ALA NORTE: ILUMINACIÓN TÉCNICA, ESCENAS Y VENTILACIÓN VMC (1:20)</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">FOSOS LED PERIMETRALES · RED VMC ZEHNDER DB-HS3 · CIRCUITOS DALI/CASAMBI · PLANO A-04</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Base atenuada
    svg.append("""
    <g opacity="0.30">
      <rect x="180.0" y="380" width="1249.25" height="370" fill="none" stroke="#94a3b8" stroke-width="1.5"/>
      <line x1="398.5" y1="380" x2="398.5" y2="680" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="740.5" y1="380" x2="740.5" y2="750" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="1111.0" y1="380" x2="1111.0" y2="750" stroke="#94a3b8" stroke-width="1.0"/>
      <line x1="1111.0" y1="670" x2="1429.25" y2="670" stroke="#94a3b8" stroke-width="1.0"/>
    </g>
    """)

    # ILUMINACIÓN Y ESCENAS
    # 1. Zaguán: Fosa perimetral cálida 2700K + Downlight de presencia
    # 2. Porche exterior: 2 Downlights IP65 en voladizo
    # 3. Hall: Fosa lineal rasante en pared oeste + Downlights antideslumbrantes UGR<19
    # 4. Despacho: Carril magnético 48V con focos orientables sobre mesa + foso indirecto
    # 5. Baño PB: Fosa indirecta sobre ducha + Downlight estanco IP65 + Espejo retroiluminado
    svg.append("""
    <!-- RED DE ILUMINACIÓN Y LUMINARIAS -->
    <!-- Porche Exterior: 2 Downlights IP65 3000K -->
    <circle cx="480" cy="350" r="9" fill="#0b1120" stroke="#f59e0b" stroke-width="1.5"/>
    <circle cx="480" cy="350" r="3" fill="#f59e0b"/>
    <circle cx="660" cy="350" r="9" fill="#0b1120" stroke="#f59e0b" stroke-width="1.5"/>
    <circle cx="660" cy="350" r="3" fill="#f59e0b"/>
    <text x="570" y="375" fill="#fde68a" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">2× DOWNLIGHT IP65 PORCHE (ENCENDIDO CREPUSCULAR / SENSOR)</text>

    <!-- Zaguán: Fosa LED Perimetral cálida 2700K (Línea ámbar brillante) -->
    <path d="M 190 430 L 380 430 L 380 660 L 190 660 Z" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="8,4"/>
    <text x="285" y="490" fill="#fde68a" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">FOSA INDIRECTA PERIMETRAL LED 2700K</text>
    <circle cx="285" cy="540" r="8" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="285" y="565" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">DOWNLIGHT COB 7W</text>

    <!-- Hall Principal: Fosa Rasante en Pared de Entrada + Downlights UGR<19 -->
    <line x1="410" y1="430" x2="410" y2="720" stroke="#f59e0b" stroke-width="3.0"/>
    <text x="425" y="540" fill="#fde68a" font-family="monospace" font-size="7" font-weight="700" transform="rotate(-90 425 540)">FOSA RASANTE PARED OESTE</text>
    <circle cx="560" cy="500" r="8" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
    <circle cx="560" cy="620" r="8" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="560" y="525" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">SPOT UGR&lt;19 (L-01)</text>
    <text x="560" y="645" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">SPOT UGR&lt;19 (L-02)</text>

    <!-- Despacho / Teletrabajo: Carril Magnético 48V sobre mesa + Foco lectura -->
    <rect x="760" y="440" width="140" height="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
    <circle cx="780" cy="443" r="4" fill="#38bdf8"/>
    <circle cx="830" cy="443" r="4" fill="#38bdf8"/>
    <circle cx="880" cy="443" r="4" fill="#38bdf8"/>
    <text x="830" y="430" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">CARRIL MAGNÉTICO 48V (3× SPOTS 3000K ANTIDESLUMBRANTES 500 LUX)</text>

    <!-- Baño PB: Fosa estanca sobre Ducha + Downlight IP65 + Espejo retroiluminado -->
    <line x1="1310" y1="430" x2="1425" y2="430" stroke="#38bdf8" stroke-width="3.0"/>
    <text x="1367" y="445" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">FOSA ESTANCA DUCHA IP65</text>
    <circle cx="1230" cy="540" r="8" fill="#0b1120" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="1230" y="565" fill="#38bdf8" font-family="monospace" font-size="6.5" text-anchor="middle">SPOT IP65 BAÑO</text>
    """)

    # RED DE VENTILACIÓN MECÁNICA VMC (CTE DB-HS3)
    svg.append("""
    <!-- RED DE VENTILACIÓN VMC ZEHNDER -->
    <!-- Conductos de ventilación aislados Ø90mm -->
    <path d="M 360 450 L 360 410 L 1285 410 L 1285 525" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="6,3"/>
    <path d="M 940 510 L 940 410" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="6,3"/>
    
    <text x="800" y="400" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="900">RED CONDUCTOS VMC EN FALSO TECHO (EXTRACCIÓN E IMPULSIÓN CRUZADA)</text>
    """)

    # Resumen de confort ambiental
    svg.append("""
    <g transform="translate(60, 850)">
      <rect x="0" y="0" width="1800" height="280" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="1800" height="28" fill="#1e293b"/>
      <text x="15" y="19" fill="#10b981" font-family="monospace" font-size="9" font-weight="900">ESCENAS LUMÍNICAS CASAMBI Y CONFORT AMBIENTAL PASSIVHAUS</text>
      
      <g transform="translate(20, 45)">
        <text x="0" y="15" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">ESCENA 1 · "BIENVENIDA / LLEGADA NOCHE":</text>
        <text x="0" y="30" fill="#94a3b8" font-family="monospace" font-size="7">Activación por apertura C-01: Porche exterior suave 20%, fosa rasante hall al 40% y fosa zaguán al 50% (luz cálida indirecta 2700K).</text>

        <text x="0" y="60" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">ESCENA 2 · "FOCUS TELETRABAJO (DESPACHO)":</text>
        <text x="0" y="75" fill="#94a3b8" font-family="monospace" font-size="7">Carril magnético a 500 lux (3000K CRI&gt;95) enfocado en superficie de trabajo para cero fatiga visual según norma UNE-EN 12464-1.</text>

        <text x="0" y="105" fill="#cbd5e1" font-family="monospace" font-size="8" font-weight="700">ESCENA 3 · "SUITE INVITADOS / NOCHE":</text>
        <text x="0" y="120" fill="#94a3b8" font-family="monospace" font-size="7">Luz indirecta tenue 10% en foso perimetral y balizamiento nocturno de cortesía hacia el baño completo a través del distribuidor neutro.</text>
      </g>

      <g transform="translate(900, 45)">
        <text x="0" y="15" fill="#10b981" font-family="monospace" font-size="8" font-weight="700">BALANCE DE VENTILACIÓN CTE DB-HS3:</text>
        <text x="0" y="30" fill="#94a3b8" font-family="monospace" font-size="7">Caudal total de extracción = 30 (Zaguán) + 50 (Baño PB) = 80 m³/h · Impulsión equilibrada en locales secos con recuperador &gt;90% rendimiento.</text>

        <text x="0" y="60" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">CONFORT TÉRMICO Y PROTECCIÓN FRENTE A RADÓN (DB-HS6):</text>
        <text x="0" y="75" fill="#94a3b8" font-family="monospace" font-size="7">Suelo radiante Uponor con aislamiento inferior XPS 100mm y lámina anti-radón continua con sellado hermético perimetral.</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def generate_interactive_html():
    """Genera visor interactivo multi-pestaña acceso_estudio_interactivo.html"""
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ala Norte: Acceso, Zaguán, Hall, Despacho y Baño PB · Oleiros</title>
  <style>
    :root {
      --bg: #070b14;
      --card-bg: #0b1120;
      --border: #1e293b;
      --primary: #38bdf8;
      --accent: #f59e0b;
      --emerald: #10b981;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow-x: hidden;
      line-height: 1.5;
    }
    header {
      background: #0b1120 border-bottom 1px solid var(--border);
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .tabs-nav {
      display: flex;
      background: #0f172a;
      padding: 0.5rem 2rem;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
    }
    .tab-btn {
      background: transparent;
      color: var(--text-muted);
      border: 1px solid transparent;
      padding: 0.6rem 1.2rem;
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tab-btn:hover {
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
    }
    .tab-btn.active {
      background: var(--card-bg);
      color: var(--primary);
      border-color: var(--primary);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }
    .main-container {
      padding: 1.5rem 2rem;
      max-width: 1800px;
      margin: 0 auto;
    }
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
      animation: fadeIn 0.25s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .viewer-frame {
      width: 100%;
      height: 780px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #050811;
      overflow: hidden;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    }
    .viewer-frame iframe, .viewer-frame embed, .viewer-frame object {
      width: 100%;
      height: 100%;
      border: none;
    }
    .grid-info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
      margin-top: 1.5rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
    }
    .card h3 {
      color: var(--primary);
      font-size: 1rem;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card ul {
      list-style-type: none;
      padding-left: 0;
    }
    .card li {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 0.45rem;
      display: flex;
      justify-content: space-between;
    }
    .card li strong {
      color: var(--text);
    }
  </style>
</head>
<body>
  <header>
    <div>
      <span class="badge">V2 DEFINITIVA · ZOOM-IN CAD 1:20</span>
      <h1 style="font-size: 1.4rem; margin-top: 0.35rem;">Ala Norte: Acceso, Zaguán Mudroom, Hall, Despacho y Baño PB</h1>
      <p style="font-size: 0.85rem; color: var(--text-muted);">Liáns, Concello de Oleiros · Parcela 2B · Cumplimiento Integral NHG Galicia y PXOM</p>
    </div>
    <div style="text-align: right;">
      <span style="font-size: 0.8rem; color: var(--accent); font-weight: 700;">Superficie Útil Ala Norte: 32,90 m²</span><br>
      <span style="font-size: 0.75rem; color: var(--text-muted);">Longitud de Fachada Norte: 13,15 m (Ejes A a E)</span>
    </div>
  </header>

  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="showTab('tab-a01')">📐 A-01: Planta Esquemática 1:20</button>
    <button class="tab-btn" onclick="showTab('tab-a02')">🏛️ A-02: Alzados y Secciones 1:20</button>
    <button class="tab-btn" onclick="showTab('tab-a03')">⚡ A-03: Electricidad y CGMP+RITI</button>
    <button class="tab-btn" onclick="showTab('tab-a04')">💡 A-04: Iluminación y VMC</button>
    <button class="tab-btn" onclick="showTab('tab-memoria')">📋 Memoria Técnica y NHG</button>
  </nav>

  <div class="main-container">
    <!-- Pestaña 1: Planta Esquemática -->
    <div id="tab-a01" class="tab-pane active">
      <div class="viewer-frame">
        <object data="plano_acceso_planta_esquematica.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>[E-03] Zaguán Mudroom (5,80 m²)</h3>
          <ul>
            <li>Banco zapatero: <strong>1,60 × 0,45 m con almacenaje</strong></li>
            <li>Gabanero empotrado: <strong>1,25 × 0,60 m integrado</strong></li>
            <li>Secador técnico: <strong>Armario térmico neoprenos/surf</strong></li>
            <li>Ventilación: <strong>VMC-E 30 m³/h extracción</strong></li>
            <li>Suelo: <strong>Porcelánico C3 gris basalto</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[E-04] Hall Principal (10,40 m²)</h3>
          <ul>
            <li>Puerta principal C-01: <strong>1,00 × 2,40 m Pivotante</strong></li>
            <li>Accesibilidad: <strong>Círculo Ø 1,50 m libre NHG</strong></li>
            <li>Cuadro técnico: <strong>CGMP + RITI empotrado</strong></li>
            <li>Bajante: <strong>B-02 Ø110 insonorizada de P1</strong></li>
            <li>Conexión: <strong>Abierto a galería y patio sur</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[E-05] Despacho / Suite PB (11,50 m²)</h3>
          <ul>
            <li>Mesa de trabajo: <strong>En L a 90° ergonómica</strong></li>
            <li>Sofá-cama 140: <strong>Dormitorio PB / invitados</strong></li>
            <li>Acústica: <strong>Tabique reforzado Rw ≥ 38 dB</strong></li>
            <li>Ventana C-03: <strong>1,80 × 1,20 m (h=95cm) norte</strong></li>
            <li>Orientación sur: <strong>Fijo Cor Vision al patio</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[E-06] Baño Completo PB (5,20 m²)</h3>
          <ul>
            <li>Ducha cota cero: <strong>1,15 × 0,90 m sumidero lineal</strong></li>
            <li>Inodoro: <strong>Suspendido Geberit empotrado</strong></li>
            <li>Mueble lavabo: <strong>90 × 50 cm suspendido</strong></li>
            <li>Ventana C-04: <strong>0,80 × 0,60 m (h=160cm) alta</strong></li>
            <li>Distribuidor: <strong>Esclusa neutra doble puerta NHG</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Pestaña 2: Alzados y Secciones -->
    <div id="tab-a02" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_acceso_elevaciones_alturas.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
    </div>

    <!-- Pestaña 3: Electricidad y CGMP+RITI -->
    <div id="tab-a03" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_acceso_electricidad_fuerza.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
    </div>

    <!-- Pestaña 4: Iluminación y VMC -->
    <div id="tab-a04" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_acceso_iluminacion_clima.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
    </div>

    <!-- Pestaña 5: Memoria Técnica y NHG -->
    <div id="tab-memoria" class="tab-pane">
      <div class="card" style="margin-bottom: 1.5rem;">
        <h2 style="color: var(--primary); margin-bottom: 1rem;">Memoria Arquitectónica Descriptiva · Ala Norte PB</h2>
        <p style="margin-bottom: 1rem; color: var(--text-muted);">
          El diseño del ala norte de la planta baja responde con máxima precisión a los condicionantes climáticos costeros de Oleiros (Zona C1) y a la estricta normativa de habitabilidad autonómica (Normas do Hábitat Galego - Decreto 29/2010). Se configura como una secuencia funcional de entrada noble y filtro atlántico, combinada con un espacio de teletrabajo de altas prestaciones acústicas y un baño completo totalmente accesible.
        </p>
        <h3 style="color: var(--accent); margin: 1rem 0 0.5rem 0;">1. Secuencia de Acceso y Zaguán Mudroom (Filtro Atlántico)</h3>
        <p style="color: var(--text-muted); margin-bottom: 0.75rem;">
          Se accede desde el norte bajo el porche cubierto E-02 (3,50 m², pavimento de losas abujardadas de granito silvestre Clase 3). La entrada cuenta con una puerta acorazada pivotante C-01 (1,00 x 2,40 m) que da acceso al Hall Principal E-04 (10,40 m²). A la derecha (oeste) se sitúa el Zaguán Mudroom E-03 (5,80 m²), concebido específicamente para la vida en la costa coruñesa: permite descalzarse en un banco corrido de 1,60x0,45 m, colgar abrigos mojados en el gabanero empotrado de 1,25x0,60 m y secar trajes de surf y neoprenos en un armario técnico con calefacción y extracción mecánica VMC-E (30 m³/h). La puerta intermedia P-02 actúa como esclusa térmica frente al viento atlántico.
        </p>
        <h3 style="color: var(--accent); margin: 1rem 0 0.5rem 0;">2. Despacho / Suite de Planta Baja (Flexibilidad y Acústica Rw38dB)</h3>
        <p style="color: var(--text-muted); margin-bottom: 0.75rem;">
          El Despacho E-05 (11,50 m²) está diseñado con una mesa ergonómica en L a 90° para teletrabajo intensivo, con canalizaciones de datos Cat 6A y tomas múltiples. Se equipa con un sofá-cama de 140 cm que permite su uso inmediato como dormitorio de invitados o suite de planta baja accesible para personas con movilidad reducida (PMR). El tabique que lo separa del Hall cuenta con aislamiento reforzado de lana mineral de alta densidad y doble placa fonoabsorbente (Rw ≥ 38 dBA) con puerta acústica P-03 provista de guillotina automática de estanqueidad.
        </p>
        <h3 style="color: var(--accent); margin: 1rem 0 0.5rem 0;">3. Independencia y Normativa NHG del Baño Completo PB</h3>
        <p style="color: var(--text-muted); margin-bottom: 0.75rem;">
          De conformidad con el Decreto 29/2010 de Galicia, el baño completo E-06 (5,20 m²) no abre directamente a ninguna estancia de estancia/comedor/cocina. Se accede exclusivamente a través de un Distribuidor Neutro intermedio mediante una esclusa de tres puertas: P-04 (desde el Despacho), P-05 (hacia el Baño) y P-06 (corredera empotrada hacia la Cocina unificada). El baño está dotado de ducha enrasada a cota cero de 1,15 x 0,90 m con sumidero lineal oculto de acero inoxidable AISI 316, inodoro suspendido Geberit con cisterna empotrada y lavabo suspendido de 90x50 cm, garantizando un itinerario 100% practicable.
        </p>
      </div>
    </div>
  </div>

  <script>
    function showTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
    }
  </script>
</body>
</html>
"""
    return html

def main():
    print("=== Generando Planos Técnicos del Ala Norte PB ===")
    
    # 1. Planta Esquemática
    svg_p = generate_plano_acceso_planta()
    with open("plano_acceso_planta_esquematica.svg", "w", encoding="utf-8") as f:
        f.write(svg_p)
    print("✓ plano_acceso_planta_esquematica.svg generado")
    
    # 2. Alzados y Secciones
    svg_a = generate_plano_acceso_elevaciones()
    with open("plano_acceso_elevaciones_alturas.svg", "w", encoding="utf-8") as f:
        f.write(svg_a)
    print("✓ plano_acceso_elevaciones_alturas.svg generado")

    # 3. Electricidad y CGMP+RITI
    svg_e = generate_plano_acceso_electricidad()
    with open("plano_acceso_electricidad_fuerza.svg", "w", encoding="utf-8") as f:
        f.write(svg_e)
    print("✓ plano_acceso_electricidad_fuerza.svg generado")

    # 4. Iluminación y VMC
    svg_i = generate_plano_acceso_iluminacion()
    with open("plano_acceso_iluminacion_clima.svg", "w", encoding="utf-8") as f:
        f.write(svg_i)
    print("✓ plano_acceso_iluminacion_clima.svg generado")

    # 5. Visor interactivo
    html = generate_interactive_html()
    with open("acceso_estudio_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ acceso_estudio_interactivo.html generado")

    # Validar XML de todos los SVGs
    for fname in ["plano_acceso_planta_esquematica.svg", "plano_acceso_elevaciones_alturas.svg", 
                  "plano_acceso_electricidad_fuerza.svg", "plano_acceso_iluminacion_clima.svg"]:
        ET.parse(fname)
        print(f"✓ XML VÁLIDO: {fname}")

if __name__ == "__main__":
    main()
