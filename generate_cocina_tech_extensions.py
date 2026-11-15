#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Especializados:
- K-03: Electricidad, Fuerza y Mecanismos (REBT ITC-BT-25)
- K-04: Iluminación Técnica, Niveles de Lux y Escenas Lumínicas (CTE DB-HE3 / IESNA)
"""

import xml.etree.ElementTree as ET

def get_tech_svg_defs():
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
      <pattern id="hatch-pillar" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="5" stroke="#e2e8f0" stroke-width="1.1"/>
        <line x1="0" y1="0" x2="5" y2="0" stroke="#e2e8f0" stroke-width="1.1"/>
      </pattern>

      <!-- Marcadores de cota -->
      <marker id="tick-45" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#38bdf8" stroke-width="1.2"/>
      </marker>
      <marker id="tick-amber" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#f59e0b" stroke-width="1.2"/>
      </marker>
      <marker id="tick-emerald" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#10b981" stroke-width="1.2"/>
      </marker>
      <marker id="arrow-elec" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
        <path d="M 0 0 L 6 3 L 0 6 Z" fill="#38bdf8"/>
      </marker>

      <!-- Gradientes fotométricos isolux -->
      <radialGradient id="lux-isla" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25"/>
        <stop offset="60%" stop-color="#38bdf8" stop-opacity="0.10"/>
        <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0"/>
      </radialGradient>
      <radialGradient id="lux-bancada" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.30"/>
        <stop offset="70%" stop-color="#f59e0b" stop-opacity="0.10"/>
        <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.0"/>
      </radialGradient>
      <radialGradient id="lux-cava" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#eab308" stop-opacity="0.35"/>
        <stop offset="100%" stop-color="#eab308" stop-opacity="0.0"/>
      </radialGradient>
      <linearGradient id="lux-foso" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.0"/>
      </linearGradient>
    </defs>
    """

def dim_h(x1, x2, y, offset_y, label, col="#38bdf8", marker="tick-45", font_size=7.5):
    if x2 < x1: x1, x2 = x2, x1
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
    if y2 < y1: y1, y2 = y2, y1
    xd = x + offset_x
    x_start = x + (2 if offset_x > 0 else -2)
    x_end = xd + (4 if offset_x > 0 else -4)
    my = (y1 + y2) / 2.0
    tw = max(len(label) * (font_size * 0.60) + 6, 20)
    return f"""<g class="cad-dim">
      <line x1="{x_start:.1f}" y1="{y1:.1f}" x2="{x_end:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{x_start:.1f}" y1="{y2:.1f}" x2="{x_end:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.5" opacity="0.6"/>
      <line x1="{xd:.1f}" y1="{y1:.1f}" x2="{xd:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.8" marker-start="url(#{marker})" marker-end="url(#{marker})"/>
      <g transform="translate({xd:.1f}, {my:.1f}) rotate(-90)">
        <rect x="{-tw/2:.1f}" y="{-font_size/2 - 2:.1f}" width="{tw:.1f}" height="{font_size + 4:.1f}" fill="#0b1120" opacity="0.9"/>
        <text x="0" y="{font_size/2 - 1:.1f}" fill="{col}" font-family="monospace" font-size="{font_size}" font-weight="700" text-anchor="middle">{label}</text>
      </g>
    </g>"""

# --------------------------------------------------------------------------
# SÍMBOLOS ELÉCTRICOS NORMALIZADOS UNE-EN 60617
# --------------------------------------------------------------------------
def sym_schuko(x, y, circ, h_cota, label, col="#38bdf8", rot=0):
    """Símbolo de toma de corriente Schuko 16A + TT con etiqueta técnica"""
    return f"""<g class="sym-elec" transform="translate({x:.1f},{y:.1f}) rotate({rot})">
      <circle cx="0" cy="0" r="7" fill="#0f172a" stroke="{col}" stroke-width="1.3"/>
      <line x1="-4" y1="0" x2="4" y2="0" stroke="{col}" stroke-width="1.1"/>
      <line x1="0" y1="-7" x2="0" y2="7" stroke="{col}" stroke-width="0.8"/>
      <rect x="9" y="-9" width="60" height="18" rx="2" fill="#0b1120" stroke="{col}" stroke-width="0.6" opacity="0.92"/>
      <text x="12" y="-1" fill="{col}" font-family="monospace" font-size="6.0" font-weight="700">{circ} · 16A</text>
      <text x="12" y="6" fill="#cbd5e1" font-family="monospace" font-size="5.2">h={h_cota}</text>
      <text x="9" y="15" fill="#94a3b8" font-family="monospace" font-size="4.8">{label}</text>
    </g>"""

def sym_fuerza_25A(x, y, circ, h_cota, label, col="#ef4444", rot=0):
    """Símbolo de toma de fuerza especial 25A (Placa inducción + extracción)"""
    return f"""<g class="sym-elec-power" transform="translate({x:.1f},{y:.1f}) rotate({rot})">
      <circle cx="0" cy="0" r="9" fill="#0f172a" stroke="{col}" stroke-width="1.6"/>
      <circle cx="0" cy="0" r="5" fill="#ef4444" fill-opacity="0.3" stroke="{col}" stroke-width="1.0"/>
      <line x1="-7" y1="-7" x2="7" y2="7" stroke="{col}" stroke-width="1.4"/>
      <line x1="-7" y1="7" x2="7" y2="-7" stroke="{col}" stroke-width="1.4"/>
      <rect x="11" y="-10" width="70" height="20" rx="2" fill="#0b1120" stroke="{col}" stroke-width="0.8" opacity="0.95"/>
      <text x="14" y="-2" fill="{col}" font-family="monospace" font-size="6.5" font-weight="700">{circ} · 25A (7,6 kW)</text>
      <text x="14" y="6" fill="#f8fafc" font-family="monospace" font-size="5.4">h={h_cota} · Tubo M32</text>
      <text x="11" y="17" fill="#fca5a5" font-family="monospace" font-size="5.0">{label}</text>
    </g>"""

def sym_pop_island(x, y, circ, label, col="#10b981"):
    """Módulo escamoteable o lateral de isla: 2 tomas 16A + 2 USB-C PD 65W"""
    return f"""<g class="sym-twist" transform="translate({x:.1f},{y:.1f})">
      <rect x="-14" y="-7" width="28" height="14" rx="2" fill="#0f172a" stroke="{col}" stroke-width="1.3"/>
      <circle cx="-6" cy="0" r="3.5" fill="none" stroke="{col}" stroke-width="0.8"/>
      <circle cx="6" cy="0" r="3.5" fill="none" stroke="{col}" stroke-width="0.8"/>
      <rect x="-18" y="9" width="85" height="18" rx="2" fill="#0b1120" stroke="{col}" stroke-width="0.6" opacity="0.95"/>
      <text x="-15" y="17" fill="{col}" font-family="monospace" font-size="5.8" font-weight="700">{circ} · 2×16A + 2×USB-C</text>
      <text x="-15" y="24" fill="#cbd5e1" font-family="monospace" font-size="5.0">h=+0,88 m · {label}</text>
    </g>"""

# --------------------------------------------------------------------------
# BUILD PLANO K-03: ELECTRICIDAD Y FUERZA
# --------------------------------------------------------------------------
def build_cocina_electricidad_svg():
    W, H = 1920, 1220
    S = 135.0  # 1m = 135px
    OX = 260.0
    OY = 210.0

    def mx(val_m): return OX + val_m * S
    def my(val_m): return OY + val_m * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        get_tech_svg_defs(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1400" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-03 · INSTALACIÓN ELÉCTRICA, FUERZA Y MECANISMOS (REBT ITC-BT-25 · 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Circuito C3 (25A Placa/Extracción Bora) · Circuitos C4.1 a C4.6 (16A Electrodomésticos) · Circuitos C5 (Tomas Bancada Dekton e Isla)</text>',

        # Retícula CAD
        f'<rect x="32" y="80" width="1400" height="1100" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    tw = 0.15 * S
    tw_ext = 0.35 * S

    # Arquitectura base (Muros, Ventana, Patio, Puerta Norte)
    # 1. Muro Norte con Puerta Corredera P-06 en X=0.80..1.60
    # Tramo izquierdo del muro norte (X = -0.35 .. 0.80)
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{1.15*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    # Hueco de paso Puerta Corredera P-06 (0,80 m)
    out.append(f'<rect x="{mx(0.80):.1f}" y="{my(-0.15):.1f}" width="{0.80*S:.1f}" height="{tw:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<line x1="{mx(0.85):.1f}" y1="{my(-0.075):.1f}" x2="{mx(1.55):.1f}" y2="{my(-0.075):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<text x="{mx(1.20):.1f}" y="{my(-0.20):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">PUERTA CORREDERA P-06 (0,80 m)</text>')
    # Tramo derecho del muro norte (X = 1.60 .. 4.30)
    out.append(f'<rect x="{mx(1.60):.1f}" y="{my(-0.15):.1f}" width="{2.70*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # Pilares estructurales norte
    out.append(f'<rect x="{mx(-0.12):.1f}" y="{my(-0.15):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{mx(4.03):.1f}" y="{my(-0.15):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')

    # 2. Muro Este con Ventanal C-07 (Y=1.80..4.80)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(-0.15):.1f}" width="{tw_ext:.1f}" height="{1.95*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(1.80):.1f}" width="{tw_ext:.1f}" height="{3.00*S:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.4"/>')
    out.append(f'<line x1="{mx(4.30):.1f}" y1="{my(1.80):.1f}" x2="{mx(4.30):.1f}" y2="{my(4.80):.1f}" stroke="#38bdf8" stroke-width="2.5"/>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(4.80):.1f}" width="{tw_ext:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')

    # 3. Límite Oeste con Patio Claustro y Corredera Cortizo C-06 (Y=0.00..4.00)
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.40*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(4.00):.1f}" x2="{mx(0.00):.1f}" y2="{my(6.00):.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')

    # 4. Límite Sur Comedor
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(6.00):.1f}" x2="{mx(4.15):.1f}" y2="{my(6.00):.1f}" stroke="#10b981" stroke-width="1.2" stroke-dasharray="8,4"/>')

    # Pavimento base
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{4.15*S:.1f}" height="{6.00*S:.1f}" fill="#0f172a" opacity="0.88"/>')

    # Mobiliario de fondo (Líneas finas CAD)
    fc_x = mx(3.50)
    fc_w = 0.65 * S
    # Frente Este (Columnas norte, bancada, columnas sur)
    out.append(f'<rect x="{fc_x:.1f}" y="{my(0.00):.1f}" width="{fc_w:.1f}" height="{6.00*S:.1f}" fill="none" stroke="#475569" stroke-width="0.9"/>')
    for y_div in [0.60, 1.20, 1.80, 2.80, 3.80, 4.80, 5.40]:
        out.append(f'<line x1="{fc_x:.1f}" y1="{my(y_div):.1f}" x2="{fc_x+fc_w:.1f}" y2="{my(y_div):.1f}" stroke="#334155" stroke-width="0.6"/>')

    # Gran Isla Central (3,60 x 1,10 m)
    isla_x = mx(1.25)
    isla_y = my(1.00)
    isla_w = 1.10 * S
    isla_h = 3.60 * S
    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#131c31" stroke="#475569" stroke-width="1.1"/>')
    # Fregadero e inducción esquemáticos
    out.append(f'<rect x="{isla_x+0.45*S:.1f}" y="{isla_y+0.40*S:.1f}" width="{0.52*S:.1f}" height="{0.75*S:.1f}" fill="#0b1120" stroke="#334155" stroke-width="0.8"/>')
    out.append(f'<rect x="{isla_x+0.45*S:.1f}" y="{isla_y+1.95*S:.1f}" width="{0.52*S:.1f}" height="{0.85*S:.1f}" fill="#0b1120" stroke="#334155" stroke-width="0.8"/>')

    # --------------------------------------------------------------------------
    # RED DE DISTRIBUCIÓN Y CANALIZACIONES ELÉCTRICAS
    # --------------------------------------------------------------------------
    # Caja general de paso / Registro secundario en pared norte
    reg_x = mx(2.20)
    reg_y = my(0.00)
    out.append(f'<rect x="{reg_x-12:.1f}" y="{reg_y-8:.1f}" width="24" height="16" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<text x="{reg_x:.1f}" y="{reg_y-14:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">REGISTRO DERIVACIÓN COCINA (RS-01)</text>')

    # Trazado de canalización bajo solera hacia la isla (Tubo M32 + 2xM25)
    out.append(f'<path d="M {reg_x:.1f} {reg_y:.1f} L {reg_x:.1f} {isla_y+1.80*S:.1f} L {isla_x+0.60*S:.1f} {isla_y+1.80*S:.1f}" fill="none" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{reg_x-8:.1f}" y="{my(0.55):.1f}" fill="#ef4444" font-family="monospace" font-size="5.8" font-weight="700" transform="rotate(-90 {reg_x-8:.1f} {my(0.55):.1f})" text-anchor="middle">TUBO M32 (C3 6mm²) + TUBOS M25 (C4.1 / C5.3)</text>')

    # Trazado de canalización en pared este (C4.2 a C4.6 y C5.1/C5.2)
    out.append(f'<path d="M {reg_x:.1f} {reg_y:.1f} L {mx(3.80):.1f} {reg_y:.1f} L {mx(3.80):.1f} {my(5.80):.1f}" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="6,3"/>')

    # --------------------------------------------------------------------------
    # PUNTOS DE FUERZA Y TOMAS EN LA GRAN ISLA SANTOS
    # --------------------------------------------------------------------------
    # 1. Toma C3 (25A) para Placa de Inducción Bora Pure (7,6 kW)
    bora_cen_x = isla_x + 0.70 * S
    bora_cen_y = isla_y + 2.37 * S
    out.append(sym_fuerza_25A(bora_cen_x, bora_cen_y, "C3", "+0,30m", "Placa Bora Pure 80cm (7,6 kW)", "#ef4444", 0))

    # Conexión motorizada de compuerta mural exterior Bora
    out.append(f'<line x1="{bora_cen_x:.1f}" y1="{bora_cen_y+15:.1f}" x2="{mx(0.00):.1f}" y2="{my(3.30):.1f}" stroke="#06b6d4" stroke-width="1.4" stroke-dasharray="4,2"/>')
    out.append(f'<rect x="{mx(0.00)-8:.1f}" y="{my(3.30)-8:.1f}" width="16" height="16" fill="#0f172a" stroke="#06b6d4" stroke-width="1.4"/>')
    out.append(f'<text x="{mx(0.00)-14:.1f}" y="{my(3.30)+4:.1f}" fill="#06b6d4" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="end">COMPUERTA ESTANCA BORA MOTORIZADA</text>')

    # 2. Toma C4.1 (16A) para Lavavajillas panelado 60 cm
    # Ubicado en el módulo contiguo al fregadero para permitir enrasado total
    lvv_x = isla_x + 0.70 * S
    lvv_y = isla_y + 1.45 * S
    out.append(sym_schuko(lvv_x, lvv_y, "C4.1", "+0,30m", "Lavavajillas panelado 60cm", "#38bdf8", 0))

    # 3. Toma C5.3 (16A) Módulo escamoteable / lateral isla
    twist_x = isla_x + 0.55 * S
    twist_y = isla_y + 3.40 * S
    out.append(sym_pop_island(twist_x, twist_y, "C5.3", "Testero Sur Isla / Barra", "#10b981"))

    # --------------------------------------------------------------------------
    # PUNTOS DE FUERZA Y TOMAS EN FRENTE ESTE (6,00 m)
    # --------------------------------------------------------------------------
    # Bloque 1 Norte: Columnas altas
    # Col 01: Frigorífico XXL (C4.4)
    out.append(sym_schuko(mx(3.85), my(0.30), "C4.4", "+0,30m", "Frigorífico XXL Integrable", "#38bdf8", -90))
    # Col 02: Congelador No-Frost (C4.5)
    out.append(sym_schuko(mx(3.85), my(0.90), "C4.5", "+0,30m", "Congelador No-Frost Vertical", "#38bdf8", -90))
    # Col 03: Horno Pirolítico Bosch Serie 8 (C4.2)
    out.append(sym_schuko(mx(3.85), my(1.35), "C4.2", "+0,90m", "Horno Pirolítico 3,6 kW", "#f59e0b", -90))
    # Col 03: Microondas Integrable Bosch Serie 8 (C4.3)
    out.append(sym_schuko(mx(3.85), my(1.65), "C4.3", "+1,30m", "Microondas Integrable 1,2 kW", "#38bdf8", -90))

    # Bloque 2 Central: Bancada Este con Ventanal C-07 (Tomas sobre encimera a +1,05 m)
    # Bloque Doble Norte C5.1 (2 Schukos) para cafetera espresso y molinillo
    out.append(f'<g transform="translate({mx(3.95):.1f},{my(2.05):.1f})">')
    out.append('<circle cx="0" cy="0" r="7" fill="#0f172a" stroke="#f59e0b" stroke-width="1.3"/>')
    out.append('<circle cx="0" cy="16" r="7" fill="#0f172a" stroke="#f59e0b" stroke-width="1.3"/>')
    out.append('<rect x="-85" y="-6" width="75" height="30" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="0.8" opacity="0.95"/>')
    out.append('<text x="-15" y="4" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="end">C5.1 · 2×16A SCHUKO</text>')
    out.append('<text x="-15" y="12" fill="#cbd5e1" font-family="monospace" font-size="5.2" text-anchor="end">h=+1,05 m (Coffee Station)</text>')
    out.append('<text x="-15" y="20" fill="#94a3b8" font-family="monospace" font-size="4.8" text-anchor="end">Cafetera Espresso + Molinillo</text>')
    out.append('</g>')

    # Bloque Doble Sur C5.2 (2 Schukos) para robots de cocina y tostador
    out.append(f'<g transform="translate({mx(3.95):.1f},{my(4.55):.1f})">')
    out.append('<circle cx="0" cy="0" r="7" fill="#0f172a" stroke="#f59e0b" stroke-width="1.3"/>')
    out.append('<circle cx="0" cy="16" r="7" fill="#0f172a" stroke="#f59e0b" stroke-width="1.3"/>')
    out.append('<rect x="-85" y="-6" width="75" height="30" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="0.8" opacity="0.95"/>')
    out.append('<text x="-15" y="4" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="end">C5.2 · 2×16A SCHUKO</text>')
    out.append('<text x="-15" y="12" fill="#cbd5e1" font-family="monospace" font-size="5.2" text-anchor="end">h=+1,05 m (Robots / Prep)</text>')
    out.append('<text x="-15" y="20" fill="#94a3b8" font-family="monospace" font-size="4.8" text-anchor="end">Thermomix + Tostadora</text>')
    out.append('</g>')

    # Bloque 3 Sur: Columnas altas
    # Col 04: Cava de Vinos Santos climatizada (C4.6)
    out.append(sym_schuko(mx(3.85), my(5.10), "C4.6", "+0,30m", "Cava Santos 60 Botellas", "#eab308", -90))
    # Col 05: Despensa / Iluminación interior Legrabox
    out.append(sym_schuko(mx(3.85), my(5.70), "C1", "+2,20m", "Transformador LED Despensa", "#94a3b8", -90))

    # Motorización estor solar ventanal Este C-07 (C1 a h=+2,25m)
    out.append(f'<circle cx="{mx(4.15):.1f}" cy="{my(1.90):.1f}" r="5" fill="#f59e0b"/>')
    out.append(f'<text x="{mx(4.05):.1f}" y="{my(1.90)+3:.1f}" fill="#f59e0b" font-family="monospace" font-size="5.0" font-weight="700" text-anchor="end">MOTOR ESTOR C-07 (h=+2,25m)</text>')

    # --------------------------------------------------------------------------
    # TOMAS DE USO GENERAL (CIRCUITO C2 - LIMPIEZA / AUXILIAR)
    # --------------------------------------------------------------------------
    # En pared norte junto a puerta P-06
    out.append(sym_schuko(mx(0.65), my(0.12), "C2", "+0,30m", "Toma Auxiliar / Aspirador", "#94a3b8", 0))
    # En paso al comedor
    out.append(sym_schuko(mx(0.15), my(5.85), "C2", "+0,30m", "Toma Auxiliar Comedor", "#94a3b8", 0))

    # --------------------------------------------------------------------------
    # BANDA DERECHA: CUADRO DE CARGAS REBT Y SIMBOLOGÍA
    # --------------------------------------------------------------------------
    rx = 1460
    out.append(f'<rect x="{rx}" y="80" width="430" height="1100" fill="#090e1a" stroke="#334155" stroke-width="0.8"/>')
    out.append(f'<text x="{rx+16}" y="105" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">CUADRO DE CARGAS Y CIRCUITOS (REBT)</text>')
    out.append(f'<line x1="{rx+16}" y1="112" x2="{rx+414}" y2="112" stroke="#38bdf8" stroke-width="0.8"/>')

    circ_table = [
        ("C3", "Placa Bora Pure 80cm Inducción", "25 A", "3×6 mm²", "Ø32 mm", "7.600 W", "Isla (+0,30m)"),
        ("C4.1", "Lavavajillas Integrable 60cm", "16 A", "3×2,5 mm²", "Ø25 mm", "2.200 W", "Isla (+0,30m)"),
        ("C4.2", "Horno Pirolítico Bosch Serie 8", "16 A", "3×2,5 mm²", "Ø25 mm", "3.600 W", "Torre (+0,90m)"),
        ("C4.3", "Microondas Bosch Serie 8", "16 A", "3×2,5 mm²", "Ø25 mm", "1.200 W", "Torre (+1,30m)"),
        ("C4.4", "Frigorífico XXL Integrable", "16 A", "3×2,5 mm²", "Ø25 mm", "350 W", "Col 01 (+0,30m)"),
        ("C4.5", "Congelador Vertical No-Frost", "16 A", "3×2,5 mm²", "Ø25 mm", "400 W", "Col 02 (+0,30m)"),
        ("C4.6", "Cava Vinos Santos 60 Botellas", "16 A", "3×2,5 mm²", "Ø25 mm", "250 W", "Col 04 (+0,30m)"),
        ("C5.1", "2 Tomas Coffee Station Este", "16 A", "3×2,5 mm²", "Ø25 mm", "3.680 W", "Bancada (+1,05m)"),
        ("C5.2", "2 Tomas Robots / Prep Este", "16 A", "3×2,5 mm²", "Ø25 mm", "3.680 W", "Bancada (+1,05m)"),
        ("C5.3", "Módulo Isla 2×16A + 2×USB-C", "16 A", "3×2,5 mm²", "Ø25 mm", "3.680 W", "Isla (+0,88m)"),
        ("C2", "Tomas Uso General / Limpieza", "16 A", "3×2,5 mm²", "Ø20 mm", "3.680 W", "Pared (+0,30m)"),
        ("C1", "Alimentación Iluminación / LED", "10 A", "3×1,5 mm²", "Ø20 mm", "600 W", "Techo (+2,65m)"),
    ]

    ty = 130
    out.append(f'<rect x="{rx+16}" y="{ty}" width="398" height="20" fill="#1e293b"/>')
    out.append(f'<text x="{rx+22}" y="{ty+13}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700">CIRCUITO</text>')
    out.append(f'<text x="{rx+75}" y="{ty+13}" fill="#e2e8f0" font-family="monospace" font-size="6.0" font-weight="700">DESTINO / RECEPTOR</text>')
    out.append(f'<text x="{rx+235}" y="{ty+13}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700">PIA</text>')
    out.append(f'<text x="{rx+265}" y="{ty+13}" fill="#10b981" font-family="monospace" font-size="6.0" font-weight="700">SECC.</text>')
    out.append(f'<text x="{rx+325}" y="{ty+13}" fill="#e2e8f0" font-family="monospace" font-size="6.0" font-weight="700">POTENCIA</text>')
    ty += 24

    for c, dest, pia, sec, tubo, pot, ubi in circ_table:
        out.append(f'<rect x="{rx+16}" y="{ty-3}" width="398" height="18" fill="{"#0f172a" if ty%36==0 else "none"}"/>')
        out.append(f'<text x="{rx+22}" y="{ty+9}" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">{c}</text>')
        out.append(f'<text x="{rx+75}" y="{ty+9}" fill="#cbd5e1" font-family="monospace" font-size="5.4">{dest}</text>')
        out.append(f'<text x="{rx+235}" y="{ty+9}" fill="#f59e0b" font-family="monospace" font-size="5.8" font-weight="700">{pia}</text>')
        out.append(f'<text x="{rx+265}" y="{ty+9}" fill="#10b981" font-family="monospace" font-size="5.4">{sec}</text>')
        out.append(f'<text x="{rx+325}" y="{ty+9}" fill="#f8fafc" font-family="monospace" font-size="5.6" font-weight="700">{pot}</text>')
        ty += 20

    # Potencia total instalada y simultánea
    ty += 10
    out.append(f'<rect x="{rx+16}" y="{ty}" width="398" height="38" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<text x="{rx+26}" y="{ty+15}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700">POTENCIA TOTAL INSTALADA COCINA: 28.140 W</text>')
    out.append(f'<text x="{rx+26}" y="{ty+28}" fill="#10b981" font-family="monospace" font-size="6.2">Potencia simultánea de cálculo (Fs=0,45): 12.660 W · Derivación 10 mm²</text>')

    # SIMBOLOGÍA NORMALIZADA
    ty += 55
    out.append(f'<text x="{rx+16}" y="{ty}" fill="#f59e0b" font-family="monospace" font-size="9.0" font-weight="700">SIMBOLOGÍA NORMALIZADA (UNE-EN 60617)</text>')
    out.append(f'<line x1="{rx+16}" y1="{ty+6}" x2="{rx+414}" y2="{ty+6}" stroke="#f59e0b" stroke-width="0.7"/>')
    ty += 18

    simbs = [
        ("#ef4444", "Toma de fuerza 25A + TT (Placa Bora Pure enrasada)", "h = +0,30 m en interior de mueble isla"),
        ("#38bdf8", "Toma de corriente Schuko 16A + TT (Electrodomésticos C4)", "h = +0,30 m / +0,90 m / +1,30 m según aparato"),
        ("#f59e0b", "Bloque doble Schuko 16A estanco (Tomas de bancada C5)", "h = +1,05 m sobre encimera Dekton"),
        ("#10b981", "Módulo escamoteable / lateral isla (2xSchuko + 2xUSB-C)", "h = +0,88 m en testero isla para servicio y barra"),
        ("#06b6d4", "Compuerta mural estanca motorizada para Bora Pure", "Canalización bajo forjado sanitario a fachada"),
        ("#a855f7", "Caja general de derivación y registro secundario", "Pared norte registrable para mantenimiento"),
    ]
    for col, tit, sub in simbs:
        out.append(f'<circle cx="{rx+30}" cy="{ty+8}" r="6" fill="{col}"/>')
        out.append(f'<text x="{rx+45}" y="{ty+7}" fill="#f8fafc" font-family="monospace" font-size="5.8" font-weight="700">{tit}</text>')
        out.append(f'<text x="{rx+45}" y="{ty+15}" fill="#94a3b8" font-family="monospace" font-size="5.0">{sub}</text>')
        ty += 24

    # CRITERIOS DE SEGURIDAD Y EJECUCIÓN
    ty += 15
    out.append(f'<text x="{rx+16}" y="{ty}" fill="#10b981" font-family="monospace" font-size="9.0" font-weight="700">CRITERIOS DE SEGURIDAD Y EJECUCIÓN</text>')
    out.append(f'<line x1="{rx+16}" y1="{ty+6}" x2="{rx+414}" y2="{ty+6}" stroke="#10b981" stroke-width="0.7"/>')
    ty += 18

    criterios = [
        "1. PROHIBICIÓN SOBRE FREGADERO: Ninguna toma C5 a menos de 50 cm del seno de aguas.",
        "2. VENTANAL ESTE C-07: Las tomas C5.1 y C5.2 se instalan en las jambas laterales de los",
        "   extremos de la bancada a +1,05m, respetando el vidrio del ventanal de +0,95m a +1,75m.",
        "3. DESACOPLO DE LAVAVAJILLAS: La toma del LVV se aloja en el módulo fregadero contiguo,",
        "   evitando fondos ciegos y permitiendo desenchufar sin extraer el electrodoméstico.",
        "4. EXTRACCIÓN BORA PURE: Conducto plano aislado acústicamente con compuerta estanca",
        "   motorizada comandada por la propia electrónica de la campana extractora.",
        "5. CABLEADO LIBRE DE HALÓGENOS: Conductores Afumex H07Z1-K ignífugos de baja emisión.",
    ]
    for crit in criterios:
        out.append(f'<text x="{rx+20}" y="{ty}" fill="#cbd5e1" font-family="monospace" font-size="5.4">{crit}</text>')
        ty += 13

    out.append('</svg>')
    return '\n'.join(out)

# --------------------------------------------------------------------------
# BUILD PLANO K-04: ILUMINACIÓN TÉCNICA Y ESCENAS
# --------------------------------------------------------------------------
def build_cocina_iluminacion_svg():
    W, H = 1920, 1220
    S = 135.0  # 1m = 135px
    OX = 260.0
    OY = 210.0

    def mx(val_m): return OX + val_m * S
    def my(val_m): return OY + val_m * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        get_tech_svg_defs(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1400" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#f59e0b" font-family="monospace" font-size="12" font-weight="700">PLANO K-04 · ILUMINACIÓN TÉCNICA, NIVELES DE LUX Y ESCENAS LUMÍNICAS (CTE DB-HE3 / IESNA · 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Carril Magnético 48V Trimless (3,00 m) · Tira LED COB 2700K Bancada Este · Foso Perimetral Patio Claustro · Sistema DALI/Casambi</text>',

        # Retícula CAD
        f'<rect x="32" y="80" width="1400" height="1100" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    tw = 0.15 * S
    tw_ext = 0.35 * S

    # Arquitectura base
    # Muro Norte con Puerta P-06
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{1.15*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    out.append(f'<rect x="{mx(0.80):.1f}" y="{my(-0.15):.1f}" width="{0.80*S:.1f}" height="{tw:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<line x1="{mx(0.85):.1f}" y1="{my(-0.075):.1f}" x2="{mx(1.55):.1f}" y2="{my(-0.075):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<text x="{mx(1.20):.1f}" y="{my(-0.20):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">PUERTA CORREDERA P-06</text>')
    out.append(f'<rect x="{mx(1.60):.1f}" y="{my(-0.15):.1f}" width="{2.70*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # Muro Este con Ventanal C-07
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(-0.15):.1f}" width="{tw_ext:.1f}" height="{1.95*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(1.80):.1f}" width="{tw_ext:.1f}" height="{3.00*S:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.4"/>')
    out.append(f'<line x1="{mx(4.30):.1f}" y1="{my(1.80):.1f}" x2="{mx(4.30):.1f}" y2="{my(4.80):.1f}" stroke="#38bdf8" stroke-width="2.5"/>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(4.80):.1f}" width="{tw_ext:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')

    # Límite Oeste Patio Claustro
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.40*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(4.00):.1f}" x2="{mx(0.00):.1f}" y2="{my(6.00):.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')

    # Límite Sur Comedor
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(6.00):.1f}" x2="{mx(4.15):.1f}" y2="{my(6.00):.1f}" stroke="#10b981" stroke-width="1.2" stroke-dasharray="8,4"/>')

    # Pavimento base
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{4.15*S:.1f}" height="{6.00*S:.1f}" fill="#0f172a" opacity="0.88"/>')

    # Mobiliario de fondo (Líneas finas CAD)
    fc_x = mx(3.50)
    fc_w = 0.65 * S
    out.append(f'<rect x="{fc_x:.1f}" y="{my(0.00):.1f}" width="{fc_w:.1f}" height="{6.00*S:.1f}" fill="none" stroke="#475569" stroke-width="0.9"/>')
    isla_x = mx(1.25)
    isla_y = my(1.00)
    isla_w = 1.10 * S
    isla_h = 3.60 * S
    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#131c31" stroke="#475569" stroke-width="1.1"/>')

    # --------------------------------------------------------------------------
    # MAPA DE NIVELES FOTOMÉTRICOS ISOLUX
    # --------------------------------------------------------------------------
    # Zona de alta iluminancia (>500 lux) sobre la Isla
    out.append(f'<ellipse cx="{isla_x+isla_w/2:.1f}" cy="{isla_y+isla_h/2:.1f}" rx="{1.1*S:.1f}" ry="{2.1*S:.1f}" fill="url(#lux-isla)"/>')
    out.append(f'<ellipse cx="{isla_x+isla_w/2:.1f}" cy="{isla_y+isla_h/2:.1f}" rx="{0.7*S:.1f}" ry="{1.7*S:.1f}" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="5,3" opacity="0.6"/>')
    out.append(f'<text x="{isla_x+isla_w/2:.1f}" y="{isla_y+0.25*S:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">ZONA TRABAJO ISLA: 550 LUX (CRI ≥ 95 · UGR &lt; 16)</text>')

    # Zona de alta iluminancia (>500 lux) sobre Bancada Este
    out.append(f'<ellipse cx="{mx(3.82):.1f}" cy="{my(3.30):.1f}" rx="{0.7*S:.1f}" ry="{1.7*S:.1f}" fill="url(#lux-bancada)"/>')
    out.append(f'<ellipse cx="{mx(3.82):.1f}" cy="{my(3.30):.1f}" rx="{0.4*S:.1f}" ry="{1.4*S:.1f}" fill="none" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="5,3" opacity="0.6"/>')
    out.append(f'<text x="{mx(3.30):.1f}" y="{my(3.30):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" transform="rotate(90 {mx(3.30):.1f} {my(3.30):.1f})" text-anchor="middle">ZONA BANCADA ESTE: 500 LUX CONTINUOS</text>')

    # Zona Cava Santos (Luz ámbar cálida de acento)
    out.append(f'<rect x="{fc_x:.1f}" y="{my(4.80):.1f}" width="{fc_w:.1f}" height="{0.60*S:.1f}" fill="url(#lux-cava)"/>')

    # Foso perimetral Cortizo (Luz indirecta bañando transición patio)
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.30):.1f}" width="{0.40*S:.1f}" height="{3.40*S:.1f}" fill="url(#lux-foso)"/>')

    # --------------------------------------------------------------------------
    # SISTEMAS Y LUMINARIAS EN FALSO TECHO (h=+2,65 m)
    # --------------------------------------------------------------------------
    # 1. L-01: CARRIL MAGNÉTICO 48V TRIMLESS EMPOTRADO EN FALSO TECHO (3,00 m)
    track_x = isla_x + 0.55 * S
    track_y1 = isla_y + 0.30 * S
    track_y2 = isla_y + 3.30 * S
    # Perfil de carril
    out.append(f'<rect x="{track_x-5:.1f}" y="{track_y1:.1f}" width="10" height="{track_y2-track_y1:.1f}" rx="2" fill="#090e1a" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{track_x:.1f}" y1="{track_y1:.1f}" x2="{track_x:.1f}" y2="{track_y2:.1f}" stroke="#06b6d4" stroke-width="1.8"/>')

    # Módulos lineales difusos opalinos (2 unidades de 1,00 m cada una)
    out.append(f'<rect x="{track_x-4:.1f}" y="{track_y1+0.20*S:.1f}" width="8" height="{0.90*S:.1f}" fill="#f8fafc" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<rect x="{track_x-4:.1f}" y="{track_y1+1.80*S:.1f}" width="8" height="{0.90*S:.1f}" fill="#f8fafc" stroke="#38bdf8" stroke-width="0.8"/>')

    # Proyectores orientables cilíndricos Ø40mm (3 unidades antideslumbrantes)
    for py, plab in [(track_y1+0.05*S, "FOCO 01 FREGADERO"), (track_y1+1.35*S, "FOCO 02 BORA PURE"), (track_y1+2.90*S, "FOCO 03 EMPLATADO")]:
        out.append(f'<circle cx="{track_x:.1f}" cy="{py:.1f}" r="7" fill="#f59e0b" stroke="#f8fafc" stroke-width="1.2"/>')
        out.append(f'<line x1="{track_x:.1f}" y1="{py:.1f}" x2="{track_x+18:.1f}" y2="{py-6:.1f}" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{track_x+22:.1f}" y="{py-3:.1f}" fill="#f59e0b" font-family="monospace" font-size="5.2" font-weight="700">{plab} (24° · 2700K)</text>')

    out.append(f'<text x="{track_x-14:.1f}" y="{isla_y+1.80*S:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" transform="rotate(-90 {track_x-14:.1f} {isla_y+1.80*S:.1f})" text-anchor="middle">L-01 · CARRIL MAGNÉTICO 48V TRIMLESS (3,00 m · DALI / CASAMBI)</text>')

    # 2. L-02: TIRA LED COB CONTINUA BAJO MUEBLES ALTOS BANCADA ESTE (3,00 m)
    led_x = mx(3.75)
    led_y1 = my(1.80)
    led_y2 = my(4.80)
    out.append(f'<line x1="{led_x:.1f}" y1="{led_y1:.1f}" x2="{led_x:.1f}" y2="{led_y2:.1f}" stroke="#f59e0b" stroke-width="2.6" stroke-linecap="round"/>')
    out.append(f'<line x1="{led_x:.1f}" y1="{led_y1:.1f}" x2="{led_x:.1f}" y2="{led_y2:.1f}" stroke="#fef08a" stroke-width="1.0" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{led_x+10:.1f}" y="{my(3.30):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(90 {led_x+10:.1f} {my(3.30):.1f})" text-anchor="middle">L-02 · TIRA LED COB CONTINUA ENRASADA (14,4 W/m · 2700K · CRI &gt; 95 · 1200 lm/m)</text>')

    # 3. L-03: RETROILUMINACIÓN VERTICAL CAVA SANTOS
    cava_x = mx(3.60)
    cava_y = my(4.90)
    out.append(f'<rect x="{cava_x:.1f}" y="{cava_y:.1f}" width="4" height="{0.40*S:.1f}" fill="#eab308"/>')
    out.append(f'<text x="{cava_x-8:.1f}" y="{cava_y+0.20*S:.1f}" fill="#eab308" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="end">L-03 · LED ÁMBAR CAVA (2400K)</text>')

    # 4. L-04: FOSO DE LUZ INDIRECTA PERIMETRAL PATIO CLAUSTRO (4,00 m)
    foso_x = mx(0.08)
    foso_y1 = my(0.20)
    foso_y2 = my(3.80)
    out.append(f'<line x1="{foso_x:.1f}" y1="{foso_y1:.1f}" x2="{foso_x:.1f}" y2="{foso_y2:.1f}" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{foso_x+10:.1f}" y="{my(2.00):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" transform="rotate(90 {foso_x+10:.1f} {my(2.00):.1f})" text-anchor="middle">L-04 · FOSO CORNER INDIRECTO PATIO CLAUSTRO (2700K)</text>')

    # 5. L-05: DOWNLIGHTS EMPOTRADOS DE CIRCULACIÓN (4 Unidades trimless Ø50mm IP44)
    downlights = [
        (mx(0.60), my(0.80), "DL-01 (150 lux)"),
        (mx(0.60), my(3.20), "DL-02 (150 lux)"),
        (mx(2.95), my(0.80), "DL-03 (200 lux)"),
        (mx(2.95), my(5.20), "DL-04 (200 lux)"),
    ]
    for dx, dy, dlab in downlights:
        out.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.3"/>')
        out.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="3" fill="#38bdf8"/>')
        out.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="16" fill="none" stroke="#38bdf8" stroke-width="0.5" stroke-dasharray="3,2"/>')
        out.append(f'<text x="{dx:.1f}" y="{dy+18:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{dlab}</text>')

    # --------------------------------------------------------------------------
    # PULSADORES Y TECLADOS DE CONTROL DE ESCENAS (DALI / CASAMBI)
    # --------------------------------------------------------------------------
    # Teclado M-01 en acceso Norte (junto a puerta corredera P-06)
    k1_x = mx(0.70)
    k1_y = my(-0.05)
    out.append(f'<rect x="{k1_x-10:.1f}" y="{k1_y-10:.1f}" width="20" height="20" rx="3" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<text x="{k1_x:.1f}" y="{k1_y+3:.1f}" fill="#070b14" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">M-01</text>')
    out.append(f'<text x="{k1_x-14:.1f}" y="{k1_y-14:.1f}" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700" text-anchor="end">TECLADO 4 ESCENAS NORTE</text>')

    # Teclado M-02 en paso Sur hacia el Comedor
    k2_x = mx(0.20)
    k2_y = my(5.90)
    out.append(f'<rect x="{k2_x-10:.1f}" y="{k2_y-10:.1f}" width="20" height="20" rx="3" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<text x="{k2_x:.1f}" y="{k2_y+3:.1f}" fill="#070b14" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">M-02</text>')
    out.append(f'<text x="{k2_x+16:.1f}" y="{k2_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">TECLADO 4 ESCENAS COMEDOR</text>')

    # --------------------------------------------------------------------------
    # BANDA DERECHA: TABLA DE LUMINARIAS Y MATRIZ DE ESCENAS LUMÍNICAS
    # --------------------------------------------------------------------------
    rx = 1460
    out.append(f'<rect x="{rx}" y="80" width="430" height="1100" fill="#090e1a" stroke="#334155" stroke-width="0.8"/>')
    out.append(f'<text x="{rx+16}" y="105" fill="#f59e0b" font-family="monospace" font-size="9.5" font-weight="700">TABLA DE LUMINARIAS Y FOTOMETRÍA</text>')
    out.append(f'<line x1="{rx+16}" y1="112" x2="{rx+414}" y2="112" stroke="#f59e0b" stroke-width="0.8"/>')

    lum_table = [
        ("L-01A", "Módulo Lineal Difuso Carril 48V (2x)", "32 W", "2.800 lm", "2700 K", "CRI ≥ 95", "DALI 0-100%"),
        ("L-01B", "Proyector Orientable 24° Carril (3x)", "27 W", "2.400 lm", "2700 K", "CRI ≥ 95", "UGR &lt; 16 DALI"),
        ("L-02",  "Tira LED COB Enrasada Bancada (3m)",  "43 W", "3.600 lm", "2700 K", "CRI &gt; 95", "Regulable PWM"),
        ("L-03",  "Microperfil LED Ámbar Cava Santos",  "15 W", "950 lm",   "2400 K", "CRI &gt; 90", "Regulación 10%"),
        ("L-04",  "Foso Cortinero Patio Claustro (4m)",  "48 W", "4.000 lm", "2700 K", "CRI &gt; 90", "Casambi"),
        ("L-05",  "Downlights Trimless Ø50mm IP44 (4x)", "28 W", "2.200 lm", "3000 K", "CRI ≥ 90", "DALI"),
    ]

    ty = 130
    out.append(f'<rect x="{rx+16}" y="{ty}" width="398" height="20" fill="#1e293b"/>')
    out.append(f'<text x="{rx+22}" y="{ty+13}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700">CÓDIGO</text>')
    out.append(f'<text x="{rx+70}" y="{ty+13}" fill="#e2e8f0" font-family="monospace" font-size="6.0" font-weight="700">TIPO / MODELO</text>')
    out.append(f'<text x="{rx+235}" y="{ty+13}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700">POT.</text>')
    out.append(f'<text x="{rx+270}" y="{ty+13}" fill="#10b981" font-family="monospace" font-size="6.0" font-weight="700">CCT</text>')
    out.append(f'<text x="{rx+325}" y="{ty+13}" fill="#e2e8f0" font-family="monospace" font-size="6.0" font-weight="700">CONTROL</text>')
    ty += 24

    for c, mod, pot, lm, cct, cri, reg in lum_table:
        out.append(f'<rect x="{rx+16}" y="{ty-3}" width="398" height="18" fill="{"#0f172a" if ty%36==0 else "none"}"/>')
        out.append(f'<text x="{rx+22}" y="{ty+9}" fill="#f59e0b" font-family="monospace" font-size="5.8" font-weight="700">{c}</text>')
        out.append(f'<text x="{rx+70}" y="{ty+9}" fill="#cbd5e1" font-family="monospace" font-size="5.4">{mod}</text>')
        out.append(f'<text x="{rx+235}" y="{ty+9}" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">{pot}</text>')
        out.append(f'<text x="{rx+270}" y="{ty+9}" fill="#10b981" font-family="monospace" font-size="5.4">{cct}</text>')
        out.append(f'<text x="{rx+325}" y="{ty+9}" fill="#f8fafc" font-family="monospace" font-size="5.4">{reg}</text>')
        ty += 20

    # MATRIZ DE ESCENAS LUMÍNICAS
    ty += 25
    out.append(f'<text x="{rx+16}" y="{ty}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">MATRIZ DE PROGRAMACIÓN DE ESCENAS</text>')
    out.append(f'<line x1="{rx+16}" y1="{ty+6}" x2="{rx+414}" y2="{ty+6}" stroke="#38bdf8" stroke-width="0.7"/>')
    ty += 20

    scenes = [
        ("ESCENA 1 · CHEF / TRABAJO", "#38bdf8", [
            ("L-01 Carril Isla", "100% (550 lux)"),
            ("L-02 LED Bancada", "100% (500 lux)"),
            ("L-03 Cava Santos", "50% cálido"),
            ("L-04 Foso Patio", "Apagado"),
            ("L-05 Downlights", "60% paso"),
        ]),
        ("ESCENA 2 · DESAYUNO SOLEADO", "#f59e0b", [
            ("L-01 Carril Isla", "30% difuso"),
            ("L-02 LED Bancada", "40% soporte"),
            ("L-03 Cava Santos", "Apagado"),
            ("L-04 Foso Patio", "20% suave"),
            ("L-05 Downlights", "Apagado"),
        ]),
        ("ESCENA 3 · CENA &amp; COPAS SOCIAL", "#eab308", [
            ("L-01 Carril Isla", "15% foco barra"),
            ("L-02 LED Bancada", "10% foso"),
            ("L-03 Cava Santos", "100% ámbar"),
            ("L-04 Foso Patio", "50% escénico"),
            ("L-05 Downlights", "Apagado"),
        ]),
        ("ESCENA 4 · CORTESÍA NOCHE", "#10b981", [
            ("L-01 Carril Isla", "Apagado"),
            ("L-02 LED Bancada", "5% zócalo"),
            ("L-03 Cava Santos", "5% balizado"),
            ("L-04 Foso Patio", "Apagado"),
            ("L-05 Downlights", "10% nocturno"),
        ]),
    ]

    for sc_name, sc_col, items in scenes:
        out.append(f'<rect x="{rx+16}" y="{ty}" width="398" height="60" rx="3" fill="#131c31" stroke="{sc_col}" stroke-width="0.8"/>')
        out.append(f'<text x="{rx+24}" y="{ty+13}" fill="{sc_col}" font-family="monospace" font-size="6.5" font-weight="700">{sc_name}</text>')
        iy = ty + 24
        for it_nam, it_val in items[:3]:
            out.append(f'<text x="{rx+24}" y="{iy}" fill="#94a3b8" font-family="monospace" font-size="5.2">• {it_nam}: <tspan fill="#f8fafc" font-weight="700">{it_val}</tspan></text>')
            iy += 10
        iy = ty + 24
        for it_nam, it_val in items[3:]:
            out.append(f'<text x="{rx+220}" y="{iy}" fill="#94a3b8" font-family="monospace" font-size="5.2">• {it_nam}: <tspan fill="#f8fafc" font-weight="700">{it_val}</tspan></text>')
            iy += 10
        ty += 68

    # CUMPLIMIENTO NORMATIVO CTE DB-HE3
    ty += 15
    out.append(f'<text x="{rx+16}" y="{ty}" fill="#10b981" font-family="monospace" font-size="9.0" font-weight="700">CUMPLIMIENTO CTE DB-HE3 / CONFORT IESNA</text>')
    out.append(f'<line x1="{rx+16}" y1="{ty+6}" x2="{rx+414}" y2="{ty+6}" stroke="#10b981" stroke-width="0.7"/>')
    ty += 16
    confort_notes = [
        "• EFICIENCIA ENERGÉTICA (VEEI): 2,8 W/m²/100 lux (Límite CTE: 3,5).",
        "• ÍNDICE DE REPRODUCCIÓN CROMÁTICA: CRI ≥ 95 en toda el área de corte y",
        "  preparación de alimentos para máxima fidelidad visual y seguridad.",
        "• CONFORT VISUAL: Ópticas oscuras antideslumbrantes UGR &lt; 16 en carril.",
        "• RIESGO FOTOBIOLÓGICO: Grupo RG0 (Exento de riesgo fotobiológico).",
    ]
    for c_note in confort_notes:
        out.append(f'<text x="{rx+20}" y="{ty}" fill="#cbd5e1" font-family="monospace" font-size="5.4">{c_note}</text>')
        ty += 13

    out.append('</svg>')
    return '\n'.join(out)

# --------------------------------------------------------------------------
# MAIN EXECUTION & VALIDATION
# --------------------------------------------------------------------------
def main():
    print("Generando Plano K-03: Electricidad, Fuerza y Mecanismos...")
    k03 = build_cocina_electricidad_svg()
    with open("plano_cocina_electricidad_fuerza.svg", "w", encoding="utf-8") as f:
        f.write(k03)
    ET.parse("plano_cocina_electricidad_fuerza.svg")
    print(" -> plano_cocina_electricidad_fuerza.svg: 100% VALID XML (0 errores)")

    print("Generando Plano K-04: Iluminación Técnica, Fotometría y Escenas...")
    k04 = build_cocina_iluminacion_svg()
    with open("plano_cocina_iluminacion_escenas.svg", "w", encoding="utf-8") as f:
        f.write(k04)
    ET.parse("plano_cocina_iluminacion_escenas.svg")
    print(" -> plano_cocina_iluminacion_escenas.svg: 100% VALID XML (0 errores)")

if __name__ == "__main__":
    main()
