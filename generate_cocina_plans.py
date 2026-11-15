#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos de la Cocina Unificada de Gran Almacenaje (Propuesta D v2 - Hogar Oleiros)
- Espacio unificado total: 20,80 m² útiles (15,20 m² cocina + 5,60 m² despensa previa unificada)
- Geometría: Ancho 4,15 m (X=12.50..16.65) x Longitud 6,00 m (Y=8.40..14.40)
- Abierta al Patio Corrala Central en el Oeste (4,00 m de cristalera corredera Cortizo)
- Abierta al Comedor Principal en el Sur (4,15 m diáfanos)
- Frente de Columnas Este Monumental de 6,00 m de longitud (10 módulos de 60 cm)
- Gran Isla Central Santos Fine de 3,60 x 1,10 m con barra snack y taburetes al patio
"""

import os
import math
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

      <!-- Gradientes decorativos -->
      <linearGradient id="grad-columnas" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#1e293b"/>
        <stop offset="100%" stop-color="#0f172a"/>
      </linearGradient>
      <linearGradient id="grad-dekton" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#27272a"/>
        <stop offset="50%" stop-color="#3f3f46"/>
        <stop offset="100%" stop-color="#27272a"/>
      </linearGradient>
      <linearGradient id="grad-cava" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#18181b"/>
        <stop offset="50%" stop-color="#271b12"/>
        <stop offset="100%" stop-color="#09090b"/>
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

def build_cocina_planta_svg():
    """
    Plano K-01: Planta Esquemática de la Cocina Unificada (20,80 m² útiles)
    Espacio: 4,15 m (ancho Oeste-Este) x 6,00 m (longitud Norte-Sur)
    - Abierta al Patio Corrala Central en el Oeste (X=0.00, Y=0.00..4.00)
    - Abierta al Comedor Principal en el Sur (Y=6.00)
    - Muro Este perimetral con 6,00 m de Frente de Columnas Santos (10 columnas x 60 cm)
    - Isla Santos Fine central de 3,60 x 1,10 m
    """
    W, H = 1900, 1200
    S = 135.0  # Escala 1m = 135px (gran formato 1:20 de detalle)
    OX = 260.0  # X=0.00 en ventanal hacia el Patio Claustro
    OY = 210.0  # Y=0.00 en muro Norte

    def mx(val_m):
        return OX + val_m * S

    def my(val_m):
        return OY + val_m * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1380" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-01 · PLANTA COCINA UNIFICADA DE GRAN ALMACENAJE (20,80 m² · ESCALA 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Unificación Cocina (15,20 m²) + Despensa Sur (5,60 m²) · Frente Columnas 6,00 m · Abierta a Patio Oeste y Comedor Sur</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1380" height="1080" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    tw = 0.15 * S
    tw_ext = 0.35 * S

    # 1. Muro Norte (Y = 0.00, de X = -0.35 a X = 4.30)
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{4.65*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # Pilares estructurales en muro norte (P-09 en X=0.00, P-10 en X=4.15)
    out.append(f'<rect x="{mx(-0.12):.1f}" y="{my(-0.15):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(-0.16):.1f}" y="{my(-0.18):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-09</text>')
    out.append(f'<rect x="{mx(4.03):.1f}" y="{my(-0.15):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(4.03):.1f}" y="{my(-0.18):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-10</text>')

    # 2. Muro Este Exterior Perimetral (X = 4.15, de Y = -0.15 a Y = 6.20)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(-0.15):.1f}" width="{tw_ext:.1f}" height="{6.35*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')
    # Pilares en muro este (P-15 intermedio en Y=4.00, P-20 en Y=6.00)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(3.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(4.45):.1f}" y="{my(4.00):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-15</text>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(5.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(4.45):.1f}" y="{my(6.00):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-20</text>')

    # 3. Límite Oeste:
    # Tramo 1 (Y=0.00..4.00): Ventanal corredero al Patio Corrala Central (C-06 3,00x2,60 m)
    # Pilar P-13 en esquina sur del patio (X=0.00, Y=4.00)
    out.append(f'<rect x="{mx(-0.12):.1f}" y="{my(3.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(-0.25):.1f}" y="{my(4.02):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-13</text>')

    # Carpintería corredera Cortizo Cor Vision Plus (X=0.00, Y=0.30..3.70 -> 3,40 m de cristal)
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.40*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{mx(-0.02):.1f}" y1="{my(0.30):.1f}" x2="{mx(-0.02):.1f}" y2="{my(2.05):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<line x1="{mx(0.02):.1f}" y1="{my(1.95):.1f}" x2="{mx(0.02):.1f}" y2="{my(3.70):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<text x="{mx(-0.12):.1f}" y="{my(2.00):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" transform="rotate(-90 {mx(-0.12):.1f} {my(2.00):.1f})" text-anchor="middle">CORREDERA PATIO CORRALA C-06 (3,00×2,60 m)</text>')

    # Tramo 2 Oeste (Y=4.00..6.00): Abierto / Conexión fluida con corredor hacia Salón Principal
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(4.00):.1f}" x2="{mx(0.00):.1f}" y2="{my(6.00):.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(-0.10):.1f}" y="{my(5.00):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" transform="rotate(-90 {mx(-0.10):.1f} {my(5.00):.1f})" text-anchor="middle">PASO LIBRE AL SALÓN (2,00 m)</text>')

    # 4. Límite Sur (Y = 6.00): Abierto diáfano al Comedor Principal
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(6.00):.1f}" x2="{mx(4.15):.1f}" y2="{my(6.00):.1f}" stroke="#10b981" stroke-width="1.2" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{mx(2.07):.1f}" y="{my(6.15):.1f}" fill="#10b981" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="middle">LÍNEA DE CONEXIÓN DIÁFANA CON COMEDOR PRINCIPAL SUR (4,15 m LIBRES)</text>')

    # Pavimento interior técnico porcelánico C2
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{4.15*S:.1f}" height="{6.00*S:.1f}" fill="#0f172a" opacity="0.88"/>')

    # Círculo NHG de habitabilidad y accesibilidad Ø1,50 m
    out.append(f'<circle cx="{mx(2.15):.1f}" cy="{my(2.60):.1f}" r="{0.75*S:.1f}" fill="#38bdf8" fill-opacity="0.04" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(2.15):.1f}" y="{my(2.64):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" text-anchor="middle">GIRO REGLAMENTARIO Ø1,50 m (NHG)</text>')

    # --------------------------------------------------------------------------
    # FRENTE DE COLUMNAS ESTE MONUMENTAL DE 6,00 m (10 MÓDULOS DE 60 cm)
    # Fondo 0,65 m (X = 3.50..4.15), Longitud 6,00 m (Y = 0.00..6.00)
    # --------------------------------------------------------------------------
    fc_x = mx(3.50)
    fc_y = my(0.00)
    fc_w = 0.65 * S
    fc_h = 6.00 * S
    out.append(f'<rect x="{fc_x:.1f}" y="{fc_y:.1f}" width="{fc_w:.1f}" height="{fc_h:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.5"/>')

    modulos_col = [
        ("COL 01 (60 cm)", "FRIGORÍFICO XXL", "Integrado 1-puerta", "#38bdf8"),
        ("COL 02 (60 cm)", "CONGELADOR", "No-Frost vertical", "#38bdf8"),
        ("COL 03 (60 cm)", "CAVA DE VINOS", "Santos 60 botellas", "#f59e0b"),
        ("COL 04 (60 cm)", "TORRE HORNO/MIC", "Bosch Serie 8", "#f59e0b"),
        ("COL 05 (60 cm)", "DESAYUNADOR (A)", "Puertas pocket 120cm", "#10b981"),
        ("COL 06 (60 cm)", "DESAYUNADOR (B)", "Café / Tostadora / LED", "#10b981"),
        ("COL 07 (60 cm)", "DESPENSERO DÍA", "Gavetas Legrabox", "#cbd5e1"),
        ("COL 08 (60 cm)", "DESPENSA SECA", "Víveres y menaje", "#cbd5e1"),
        ("COL 09 (60 cm)", "BACK KITCHEN AUX", "Robots ocultables", "#38bdf8"),
        ("COL 10 (60 cm)", "VAJILLERO COMEDOR", "Vitrina cristal ahumado", "#f59e0b"),
    ]

    for idx, (cod, tit, sub, col) in enumerate(modulos_col):
        m_top = fc_y + idx * 0.60 * S
        out.append(f'<line x1="{fc_x:.1f}" y1="{m_top:.1f}" x2="{fc_x+fc_w:.1f}" y2="{m_top:.1f}" stroke="#475569" stroke-width="0.9"/>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+17:.1f}" fill="{col}" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">{cod}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+33:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{tit}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+48:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{sub}</text>')

    # --------------------------------------------------------------------------
    # GRAN ISLA CENTRAL SANTOS FINE DE 3,60 x 1,10 m
    # Ubicación: X = 1.25..2.35 (ancho 1,10 m), Y = 1.00..4.60 (longitud 3,60 m)
    # --------------------------------------------------------------------------
    isla_x = mx(1.25)
    isla_y = my(1.00)
    isla_w = 1.10 * S
    isla_h = 3.60 * S

    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="2.0"/>')
    out.append(f'<rect x="{isla_x+3:.1f}" y="{isla_y+3:.1f}" width="{isla_w-6:.1f}" height="{isla_h-6:.1f}" fill="url(#grad-dekton)" opacity="0.4" stroke="#475569" stroke-width="0.8"/>')

    # Línea barra snack volada (35 cm en cara Oeste mirando al patio)
    barra_split_x = isla_x + 0.35 * S
    out.append(f'<line x1="{barra_split_x:.1f}" y1="{isla_y:.1f}" x2="{barra_split_x:.1f}" y2="{isla_y+isla_h:.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="5,2"/>')
    out.append(f'<text x="{isla_x+16:.1f}" y="{isla_y+isla_h/2:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 {isla_x+16:.1f} {isla_y+isla_h/2:.1f})" text-anchor="middle">BARRA SNACK VOLADA 35 cm (VISTAS AL PATIO)</text>')

    # 5 Taburetes altos ergonómicos orientados al Patio Claustro
    for ty in [1.35, 2.00, 2.65, 3.30, 3.95]:
        st_cx = isla_x - 0.22 * S
        st_cy = my(ty)
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.18*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.08*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.6"/>')

    # Equipamiento en la Isla (Lado de Trabajo Este, fondo 75 cm):
    # 1. Fregadero bajo encimera 70 cm (acero inox antracita)
    sink_w = 0.52 * S
    sink_h = 0.75 * S
    sink_x = isla_x + 0.45 * S
    sink_y = isla_y + 0.40 * S
    out.append(f'<rect x="{sink_x:.1f}" y="{sink_y:.1f}" width="{sink_w:.1f}" height="{sink_h:.1f}" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<rect x="{sink_x+4:.1f}" y="{sink_y+4:.1f}" width="{sink_w-8:.1f}" height="{sink_h-8:.1f}" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<circle cx="{sink_x+sink_w/2:.1f}" cy="{sink_y+sink_h/2:.1f}" r="6" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<line x1="{sink_x+sink_w/2:.1f}" y1="{sink_y+sink_h/2:.1f}" x2="{sink_x+sink_w/2-10:.1f}" y2="{sink_y+sink_h/2:.1f}" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<text x="{sink_x+sink_w/2:.1f}" y="{sink_y+sink_h+16:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">FREGADERO 70×45 cm</text>')

    # 2. Lavavajillas integrable panelado 60 cm
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+1.50*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">[ LAVAVAJILLAS PANELADO 60 cm ]</text>')

    # 3. Placa de Inducción con Extracción Integrada Bora Pure (80×52 cm)
    bora_w = 0.52 * S
    bora_h = 0.85 * S
    bora_x = isla_x + 0.45 * S
    bora_y = isla_y + 1.95 * S
    out.append(f'<rect x="{bora_x:.1f}" y="{bora_y:.1f}" width="{bora_w:.1f}" height="{bora_h:.1f}" rx="3" fill="#18181b" stroke="#f59e0b" stroke-width="1.4"/>')
    for zx, zy in [(bora_x+16, bora_y+22), (bora_x+bora_w-16, bora_y+22), (bora_x+16, bora_y+bora_h-22), (bora_x+bora_w-16, bora_y+bora_h-22)]:
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="11" fill="none" stroke="#f59e0b" stroke-width="0.9"/>')
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="3" fill="#f59e0b"/>')
    out.append(f'<rect x="{bora_x+bora_w/2-8:.1f}" y="{bora_y+bora_h/2-16:.1f}" width="16" height="32" rx="3" fill="#0f172a" stroke="#06b6d4" stroke-width="1.2"/>')
    out.append(f'<circle cx="{bora_x+bora_w/2:.1f}" cy="{bora_y+bora_h/2:.1f}" r="5" fill="none" stroke="#06b6d4" stroke-width="1.0"/>')
    out.append(f'<text x="{bora_x+bora_w/2:.1f}" y="{bora_y+bora_h+16:.1f}" fill="#f59e0b" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">PLACA BORA PURE 80 cm</text>')

    # 4. Zona de Preparación y Servicio hacia Comedor (Sur de la Isla, Y=3.00..3.60m)
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+3.20*S:.1f}" fill="#10b981" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">ZONA PREPARACIÓN Y SERVICIO</text>')
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+3.35*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Caceroleros 90 cm + Enchufes Twist</text>')

    # Rótulo de la estancia unificada
    out.append(f'<rect x="{mx(1.05):.1f}" y="{my(5.05):.1f}" width="240" height="46" rx="4" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{mx(1.05)+120:.1f}" y="{my(5.05)+19:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">[E-08] COCINA UNIFICADA SANTOS</text>')
    out.append(f'<text x="{mx(1.05)+120:.1f}" y="{my(5.05)+35:.1f}" fill="#f8fafc" font-family="monospace" font-size="7.5" text-anchor="middle">S.Útil: 20,80 m² (15,20 + 5,60) · Dekton Kelya · Z=±0,00m</text>')

    # --------------------------------------------------------------------------
    # COTAS GENERALES ISO 129
    # --------------------------------------------------------------------------
    # Cotas Horizontales:
    out.append(dim_h(mx(0.00), isla_x, my(0.15), 0, "1,25 m (Paso Libre Patio y Taburetes)", "#38bdf8", font_size=7.2))
    out.append(dim_h(isla_x, isla_x + isla_w, my(0.15), 0, "1,10 m (Ancho Isla)", "#f8fafc", font_size=7.2))
    out.append(dim_h(isla_x + isla_w, fc_x, my(0.15), 0, "1,15 m (Paso Libre de Trabajo)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_h(fc_x, mx(4.15), my(0.15), 0, "0,65 m", "#94a3b8", font_size=7.0))
    out.append(dim_h(mx(0.00), mx(4.15), my(-0.05), -25, "4,15 m (ANCHO TOTAL ESPACIO COCINA)", "#38bdf8", font_size=8.5))

    # Cotas Verticales:
    out.append(dim_v(my(0.00), isla_y, isla_x, -35, "1,00 m", "#94a3b8", font_size=7.0))
    out.append(dim_v(isla_y, isla_y + isla_h, isla_x, -35, "3,60 m (LONGITUD GRAN ISLA SANTOS)", "#f8fafc", font_size=8.0))
    out.append(dim_v(isla_y + isla_h, my(6.00), isla_x, -35, "1,40 m (Paso Abierto a Comedor)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_v(my(0.00), my(6.00), mx(0.00), -60, "6,00 m (LONGITUD TOTAL ESPACIO COCINA)", "#38bdf8", font_size=9.0))
    out.append(dim_v(fc_y, fc_y + fc_h, mx(4.15), 30, "6,00 m (Frente Monumental 10 Columnas × 60 cm)", "#f59e0b", marker="tick-amber", font_size=8.0))

    # --------------------------------------------------------------------------
    # BANDA DERECHA: MEMORIA TÉCNICA DE LA UNIFICACIÓN
    # --------------------------------------------------------------------------
    rx = 1440
    out.append(f'<rect x="{rx}" y="30" width="430" height="1130" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="410" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">MEMORIA COCINA UNIFICADA (20,80 m²)</text>')

    specs = [
        ("1. CONCEPTO ARQUITECTÓNICO UNIFICADO", "#38bdf8", [
            ("Unificación total", "15,20 m² (Cocina) + 5,60 m² (Despensa previa)"),
            ("Superficie resultante", "20,80 m² útiles continuos y luminosos"),
            ("Apertura Oeste", "Corredera Cortizo 3,00 m hacia Patio Claustro"),
            ("Apertura Sur", "Conexión 100% diáfana con Comedor Principal"),
            ("Fluidez visual", "Cero tabiques interiores divisorios"),
        ]),
        ("2. FRENTE MONUMENTAL ESTE (6,00 m)", "#f59e0b", [
            ("10 Columnas integradas", "Modulación 60 cm de suelo a techo (+2,65m)"),
            ("Frío independiente", "Frigo XXL 1-puerta + Congelador vertical"),
            ("Cava de vinos climatizada", "Santos 60 botellas con vitrina cristal negro"),
            ("Torre técnica", "Horno pirolítico + Microondas Bosch Serie 8"),
            ("Desayunador Pocket 120cm", "Puertas escamoteables, encimera café/tost."),
            ("Despensa de gran capacidad", "2 columnas con gavetas Legrabox"),
            ("Vajillero de cortesía", "Vitrina iluminada orientada al comedor"),
        ]),
        ("3. GRAN ISLA CENTRAL SANTOS (3,60×1,10 m)", "#10b981", [
            ("Encimera continua", "Dekton Kelya 20 mm resistente a 300°C"),
            ("Cocción Bora Pure", "Extractor de superficie (cero campanas techo)"),
            ("Aguas y limpieza", "Fregadero 70 cm + lavavajillas panelado"),
            ("Barra social al patio", "Voladizo 35 cm para 5 taburetes de diseño"),
            ("Zona emplatado sur", "Conexión directa con la mesa del comedor"),
        ]),
        ("4. ERGONOMÍA Y CIRCULACIÓN (NHG)", "#cbd5e1", [
            ("Paso Oeste (Isla-Patio)", "1,25 m (amplitud para taburetes y paso)"),
            ("Paso Este (Isla-Columnas)", "1,15 m (apertura simultánea cajones y horno)"),
            ("Paso Sur (Isla-Comedor)", "1,40 m libre (tránsito culinario perfecto)"),
            ("Giro reglamentario", "Ø1,50 m holgado en múltiples puntos"),
        ]),
        ("5. INSTALACIONES PREVISTAS (FASE 2)", "#f43f5e", [
            ("Electricidad y Datos", "Torres Twist retráctiles en isla + Cat 6A"),
            ("Cuadro de cargas", "Línea C3 Bora (25A), 5 líneas C4 (16A)"),
            ("Iluminación IES", "Carril magnético techo + tiras LED 3000K"),
        ]),
    ]

    sy = 85
    for cat_title, cat_col, rows in specs:
        out.append(f'<text x="{rx+16}" y="{sy}" fill="{cat_col}" font-family="monospace" font-size="7.5" font-weight="700">{cat_title}</text>')
        out.append(f'<line x1="{rx+16}" y1="{sy+4}" x2="{rx+414}" y2="{sy+4}" stroke="{cat_col}" stroke-width="0.7" opacity="0.6"/>')
        sy += 16
        for k, v in rows:
            out.append(f'<text x="{rx+20}" y="{sy}" fill="#f1f5f9" font-family="monospace" font-size="6.5" font-weight="700">• {k}:</text>')
            out.append(f'<text x="{rx+28}" y="{sy+11}" fill="#94a3b8" font-family="monospace" font-size="5.8">{v}</text>')
            sy += 21
        sy += 8

    out.append('</svg>')
    return "\n".join(out)


def build_cocina_elevaciones_svg():
    """
    Plano K-02: Alzados Interiores y Alturas Ergonómicas de la Cocina Unificada (Escala 1:20)
    - Alzado A: Frente Monumental de Columnas Este (L = 6,00 m, H = 2,65 m, 10 Módulos)
    - Alzado B: Gran Isla Santos Fine - Frente de Trabajo Este (L = 3,60 m, H = 0,92 m)
    - Alzado C: Gran Isla Santos Fine - Frente Barra Social hacia Patio (L = 3,60 m, H = 0,92 m, 5 Taburetes)
    - Alzado D: Sección Transversal y Relación Espacial Este-Oeste (Patio Corrala -> Ventanal -> Isla -> Columnas)
    """
    W, H = 1950, 1420
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1440" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-02 · ALZADOS Y COTAS DE ALTURA: COCINA UNIFICADA (ESCALA 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Frente Monumental 6,00 m (10 Columnas) · Gran Isla Santos 3,60 m · Sección Transversal con Patio · Cotas s/ Suelo Terminado ±0,00m</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1440" height="1310" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # ==========================================================================
    # SECCIÓN 1: ALZADO A - FRENTE MONUMENTAL DE COLUMNAS ESTE (L = 6,00 m, H = 2,65 m)
    # ==========================================================================
    S1 = 150.0  # 1m = 150px
    A_OX = 150.0
    A_GROUND_Y = 460.0

    def ax(val_m):
        return A_OX + val_m * S1

    def ay(val_h_m):
        return A_GROUND_Y - val_h_m * S1

    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{A_GROUND_Y:.1f}" x2="{ax(6.3):.1f}" y2="{A_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{A_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m (SUELO TERMINADO)</text>')

    ceil_y = ay(2.65)
    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{ceil_y:.1f}" x2="{ax(6.3):.1f}" y2="{ceil_y:.1f}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{ceil_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">FALSO TECHO +2,65 m</text>')

    out.append(f'<rect x="{ax(0.0):.1f}" y="{ceil_y-32:.1f}" width="460" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{ax(0.0)+10:.1f}" y="{ceil_y-17:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO A · FRENTE MONUMENTAL DE COLUMNAS ESTE (L = 6,00 m · H = 2,65 m)</text>')

    # Zócalo inferior h = 0,08 m
    out.append(f'<rect x="{ax(0.0):.1f}" y="{ay(0.08):.1f}" width="{6.00*S1:.1f}" height="{0.08*S1:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')
    out.append(f'<text x="{ax(3.0):.1f}" y="{A_GROUND_Y-4:.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ZÓCALO RETRANQUEADO h = 8 cm (CON REJILLA VENTILACIÓN FRIGO Y CAVA)</text>')

    cols_alzado = [
        ("COL 01", "FRIGORÍFICO XXL", "1-puerta integrado", 0.60, "frigo"),
        ("COL 02", "CONGELADOR", "No-Frost vertical", 0.60, "frigo"),
        ("COL 03", "CAVA SANTOS", "60 botellas doble-Tª", 0.60, "cava"),
        ("COL 04", "TORRE HORNO/MIC", "Bosch Serie 8", 0.60, "horno"),
        ("COL 05-06", "DESAYUNADOR POCKET (120 cm)", "Puertas escamoteables", 1.20, "pocket"),
        ("COL 07", "DESPENSA DÍA", "Gavetas Legrabox", 0.60, "despensa"),
        ("COL 08", "DESPENSA SECA", "Víveres y menaje", 0.60, "despensa"),
        ("COL 09", "BACK KITCHEN", "Robots ocultables", 0.60, "despensa"),
        ("COL 10", "VITRINA COMEDOR", "Cristal ahumado LED", 0.60, "vitrina"),
    ]

    cur_x = 0.0
    for cid, ctit, csub, cw, ctipo in cols_alzado:
        cx1 = ax(cur_x)
        cw_px = cw * S1
        out.append(f'<rect x="{cx1:.1f}" y="{ay(2.20):.1f}" width="{cw_px:.1f}" height="{2.12*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if ctipo == "frigo":
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.86):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<line x1="{cx1+cw_px-4:.1f}" y1="{ay(0.15):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(1.80):.1f}" stroke="#38bdf8" stroke-width="1.5"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.00):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{ctit}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.85):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{csub}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(2.03):.1f}" fill="#64748b" font-family="monospace" font-size="5.2" text-anchor="middle">ALTILLO</text>')

        elif ctipo == "cava":
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(2.15):.1f}" width="{cw_px-8:.1f}" height="{2.02*S1:.1f}" fill="url(#grad-cava)" stroke="#f59e0b" stroke-width="1.2"/>')
            for vy in [0.40, 0.70, 1.00, 1.30, 1.60, 1.90]:
                out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(vy):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(vy):.1f}" stroke="#f59e0b" stroke-width="1.0" opacity="0.6"/>')
                out.append(f'<circle cx="{cx1+20:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
                out.append(f'<circle cx="{cx1+45:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
                out.append(f'<circle cx="{cx1+70:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.10):.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">CAVA SANTOS</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.95):.1f}" fill="#fbbf24" font-family="monospace" font-size="5.2" text-anchor="middle">60 Botellas Multi-Tª</text>')

        elif ctipo == "horno":
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(0.70):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(0.70):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">GAVETA INFERIOR</text>')
            # Horno Bosch Serie 8
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.30):.1f}" width="{cw_px-8:.1f}" height="{0.60*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+10:.1f}" y="{ay(1.24):.1f}" width="{cw_px-20:.1f}" height="{0.42*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<circle cx="{cx1+cw_px/2:.1f}" cy="{ay(1.27):.1f}" r="4" fill="none" stroke="#f59e0b" stroke-width="1.0"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.96):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">HORNO PIROLÍTICO</text>')
            # Microondas
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.75):.1f}" width="{cw_px-8:.1f}" height="{0.45*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+10:.1f}" y="{ay(1.71):.1f}" width="{cw_px-20:.1f}" height="{0.30*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.50):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">MICROONDAS / VAPOR</text>')
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.75):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.75):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.98):.1f}" fill="#64748b" font-family="monospace" font-size="5.2" text-anchor="middle">ALTILLO</text>')

        elif ctipo == "pocket":
            mid_pocket = cx1 + 0.60 * S1
            out.append(f'<line x1="{mid_pocket:.1f}" y1="{ay(2.20):.1f}" x2="{mid_pocket:.1f}" y2="{ay(0.08):.1f}" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,3"/>')
            out.append(f'<line x1="{cx1+4:.1f}" y1="{ay(0.92):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(0.92):.1f}" stroke="#10b981" stroke-width="1.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.95):.1f}" fill="#10b981" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ENCIMERA INTERIOR DEKTON (+0,92 m)</text>')
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.45):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.45):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.80):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.80):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.40):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">DESAYUNADOR POCKET (120 cm)</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.25):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Cafetera Espresso · Molinillo · Tostadora · LED integrado</text>')

        elif ctipo == "despensa":
            for gy in [0.45, 0.85, 1.25, 1.65]:
                out.append(f'<line x1="{cx1+6:.1f}" y1="{ay(gy):.1f}" x2="{cx1+cw_px-6:.1f}" y2="{ay(gy):.1f}" stroke="#475569" stroke-width="0.6" stroke-dasharray="3,2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.05):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{ctit}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.90):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">Gavetas Blum</text>')

        elif ctipo == "vitrina":
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(2.15):.1f}" width="{cw_px-8:.1f}" height="{2.02*S1:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>')
            for vy in [0.55, 1.05, 1.55]:
                out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(vy):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(vy):.1f}" stroke="#f59e0b" stroke-width="1.0" opacity="0.7"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.25):.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">VITRINA / VAJILLERO</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.10):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">Orientado al Comedor</text>')

        cur_x += cw

    # Remate superior a falso techo (+2,20 a +2,65m)
    faja_y = ay(2.65)
    faja_h = 0.45 * S1
    out.append(f'<rect x="{ax(0.0):.1f}" y="{faja_y:.1f}" width="{6.00*S1:.1f}" height="{faja_h:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')
    out.append(f'<text x="{ax(3.0):.1f}" y="{faja_y+faja_h/2+3:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">REMATADO ENRASADO A FALSO TECHO (+2,20 m a +2,65 m · BOCAS VMC)</text>')

    # Cotas de Altura Alzado A
    cx_dim = ax(6.00) + 25
    out.append(dim_v(ay(0.00), ay(0.08), cx_dim, 0, "+0,08 m (Zócalo)", "#94a3b8", font_size=6.8))
    out.append(dim_v(ay(0.08), ay(0.92), cx_dim, 0, "+0,92 m (Bancada Desayunador / Horno)", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_v(ay(0.92), ay(1.30), cx_dim, 0, "+1,30 m (Eje Horno)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.30), ay(1.75), cx_dim, 0, "+1,75 m (Microondas)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.75), ay(2.20), cx_dim, 0, "+2,20 m (Coronación)", "#cbd5e1", font_size=6.8))
    out.append(dim_v(ay(2.20), ay(2.65), cx_dim, 0, "+2,65 m (Falso Techo)", "#38bdf8", font_size=7.2))

    # ==========================================================================
    # SECCIÓN 2: ALZADO B - GRAN ISLA SANTOS FINE (L = 3,60 m, H = 0,92 m)
    # Lado de Trabajo Este
    # ==========================================================================
    S2 = 170.0
    B_OX = 150.0
    B_GROUND_Y = 760.0

    def bx(val_m):
        return B_OX + val_m * S2

    def by(val_h_m):
        return B_GROUND_Y - val_h_m * S2

    out.append(f'<line x1="{bx(-0.3):.1f}" y1="{B_GROUND_Y:.1f}" x2="{bx(3.9):.1f}" y2="{B_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{bx(-0.35):.1f}" y="{B_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(1.20):.1f}" width="480" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{bx(0.0)+10:.1f}" y="{by(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO B · GRAN ISLA SANTOS FINE — FRENTE DE TRABAJO (3,60×0,92 m)</text>')

    # Zócalo isla
    out.append(f'<rect x="{bx(0.05):.1f}" y="{by(0.08):.1f}" width="{3.50*S2:.1f}" height="{0.08*S2:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')

    isla_mods_360 = [
        ("MÓD. FREGADERO (80 cm)", "Seno 70 cm + Cubos Reciclaje", 0.80, "#38bdf8"),
        ("LAVAVAJILLAS (60 cm)", "Totalmente Integrado Panelado", 0.60, "#38bdf8"),
        ("MÓD. BORA PURE (90 cm)", "2 Caceroleros + Cubertero Nogal", 0.90, "#f59e0b"),
        ("GAVETERO MENAJE (70 cm)", "Extracción Total Blum Legrabox", 0.70, "#cbd5e1"),
        ("MÓD. EMPLATADO (60 cm)", "Salida a Comedor Sur", 0.60, "#10b981"),
    ]

    ix_cur = 0.0
    for im_tit, im_sub, im_w, im_col in isla_mods_360:
        im_x1 = bx(ix_cur)
        im_w_px = im_w * S2
        out.append(f'<rect x="{im_x1:.1f}" y="{by(0.90):.1f}" width="{im_w_px:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if "FREGADERO" in im_tit:
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{im_sub}</text>')
            out.append(f'<path d="M {im_x1+im_w_px/2} {by(0.92)} L {im_x1+im_w_px/2} {by(1.30)} Q {im_x1+im_w_px/2} {by(1.40)} {im_x1+im_w_px/2-25} {by(1.38)} L {im_x1+im_w_px/2-25} {by(1.32)}" fill="none" stroke="#38bdf8" stroke-width="3.0"/>')

        elif "LAVAVAJILLAS" in im_tit:
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.52):.1f}" fill="{im_col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{im_sub}</text>')
            out.append(f'<circle cx="{im_x1+im_w_px/2:.1f}" cy="{by(0.85):.1f}" r="3" fill="#10b981"/>')

        elif "BORA" in im_tit:
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{im_sub}</text>')
            out.append(f'<rect x="{im_x1+15:.1f}" y="{by(0.925):.1f}" width="{im_w_px-30:.1f}" height="6" fill="#18181b" stroke="#f59e0b" stroke-width="1.1"/>')

        else:
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{im_sub}</text>')

        ix_cur += im_w

    # Encimera Dekton Kelya 20 mm
    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(0.92):.1f}" width="{3.60*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')
    out.append(f'<text x="{bx(1.8):.1f}" y="{by(0.92)-6:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA DEKTON KELYA 20 mm (LONGITUD 3,60 m · COTA DE TRABAJO +0,92 m)</text>')

    bx_dim = bx(3.60) + 25
    out.append(dim_v(by(0.00), by(0.08), bx_dim, 0, "+0,08 m", "#94a3b8", font_size=6.8))
    out.append(dim_v(by(0.08), by(0.90), bx_dim, 0, "0,82 m Muebles Santos", "#cbd5e1", font_size=6.8))
    out.append(dim_v(by(0.00), by(0.92), bx_dim + 35, 0, "+0,92 m COTA ENCIMERA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # SECCIÓN 3: ALZADO C - GRAN ISLA SANTOS (FRENTE BARRA SOCIAL HACIA PATIO CLAUSTRO)
    # Vista Oeste con 5 Taburetes y Vuelo de 35 cm
    # ==========================================================================
    C_OX = 150.0
    C_GROUND_Y = 1060.0

    def cx(val_m):
        return C_OX + val_m * S2

    def cy(val_h_m):
        return C_GROUND_Y - val_h_m * S2

    out.append(f'<line x1="{cx(-0.3):.1f}" y1="{C_GROUND_Y:.1f}" x2="{cx(3.9):.1f}" y2="{C_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{cx(-0.35):.1f}" y="{C_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(1.20):.1f}" width="480" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{cx(0.0)+10:.1f}" y="{cy(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO C · GRAN ISLA SANTOS — FRENTE BARRA SOCIAL Y 5 TABURETES (3,60×0,92 m)</text>')

    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(0.90):.1f}" width="{3.60*S2:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    out.append(f'<rect x="{cx(-0.05):.1f}" y="{cy(0.92):.1f}" width="{3.70*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')

    # 5 Taburetes de diseño
    for st_x_m in [0.40, 1.10, 1.80, 2.50, 3.20]:
        tx = cx(st_x_m)
        out.append(f'<line x1="{tx-16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx-10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        out.append(f'<line x1="{tx+16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx+10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        out.append(f'<line x1="{tx-14:.1f}" y1="{cy(0.25):.1f}" x2="{tx+14:.1f}" y2="{cy(0.25):.1f}" stroke="#94a3b8" stroke-width="1.5"/>')
        out.append(f'<rect x="{tx-18:.1f}" y="{cy(0.67):.1f}" width="36" height="6" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.0"/>')
        out.append(f'<line x1="{tx-12:.1f}" y1="{cy(0.67):.1f}" x2="{tx-12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<line x1="{tx+12:.1f}" y1="{cy(0.67):.1f}" x2="{tx+12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<rect x="{tx-16:.1f}" y="{cy(0.84):.1f}" width="32" height="6" rx="2" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')

    out.append(f'<text x="{cx(1.8):.1f}" y="{cy(0.50):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">VOLADIZO LIBRE 35 cm PARA PIERNAS (HUECO ERGONÓMICO 5 PLAZAS)</text>')

    out.append(dim_v(cy(0.00), cy(0.65), cx(3.65), 15, "+0,65 m (Asiento Taburete)", "#38bdf8", font_size=6.8))
    out.append(dim_v(cy(0.65), cy(0.92), cx(3.65), 15, "0,27 m Holgura Piernas", "#10b981", marker="tick-emerald", font_size=6.5))

    # ==========================================================================
    # SECCIÓN 4: ALZADO D - SECCIÓN TRANSVERSAL Y RELACIÓN CON PATIO CLAUSTRO (OESTE -> ESTE)
    # L = 4,15 m Cocina + 4,00 m Patio = 8,15 m total
    # ==========================================================================
    D_OX = 150.0
    D_GROUND_Y = 1360.0
    S4 = 110.0  # 1m = 110px

    def dx(val_m):
        return D_OX + val_m * S4

    def dy(val_h_m):
        return D_GROUND_Y - val_h_m * S4

    out.append(f'<line x1="{dx(-0.3):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(8.5):.1f}" y2="{D_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{dx(-0.35):.1f}" y="{D_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    d_ceil_y = dy(2.65)
    out.append(f'<line x1="{dx(4.0):.1f}" y1="{d_ceil_y:.1f}" x2="{dx(8.3):.1f}" y2="{d_ceil_y:.1f}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{dx(8.4):.1f}" y="{d_ceil_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">FALSO TECHO +2,65 m</text>')

    out.append(f'<rect x="{dx(0.0):.1f}" y="{d_ceil_y-32:.1f}" width="540" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{dx(0.0)+10:.1f}" y="{d_ceil_y-17:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO D · SECCIÓN TRANSVERSAL: PATIO CORRALA CLAUSTRO → VENTANAL CORTIZO → ISLA → COLUMNAS ESTE</text>')

    # 1. Patio Corrala Claustro (X=0.00..4.00m):
    # Tarima Iroko sobre plots
    out.append(f'<rect x="{dx(0.0):.1f}" y="{D_GROUND_Y-2:.1f}" width="{4.00*S4:.1f}" height="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>')
    # Arce Japonés en alcorque
    out.append(f'<line x1="{dx(1.50):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(1.50):.1f}" y2="{dy(2.20):.1f}" stroke="#10b981" stroke-width="2.5"/>')
    out.append(f'<circle cx="{dx(1.50):.1f}" cy="{dy(2.00):.1f}" r="{0.65*S4:.1f}" fill="#10b981" fill-opacity="0.25" stroke="#10b981" stroke-width="1.2"/>')
    out.append(f'<text x="{dx(1.50):.1f}" y="{dy(2.00):.1f}" fill="#a7f3d0" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ACER PALMATUM</text>')
    out.append(f'<text x="{dx(2.00):.1f}" y="{dy(0.40):.1f}" fill="#10b981" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">PATIO CORRALA (4,00 m · AIRE LIBRE)</text>')

    # 2. Carpintería Corredera Cortizo Cor Vision Plus en ras de forjado (X=4.00m, H=2,65m)
    out.append(f'<line x1="{dx(4.00):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(4.00):.1f}" y2="{d_ceil_y:.1f}" stroke="#38bdf8" stroke-width="3.5"/>')
    out.append(f'<text x="{dx(4.00):.1f}" y="{dy(1.35):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 {dx(4.00):.1f} {dy(1.35):.1f})" text-anchor="middle">VIDRIO SUELO-TECHO CORTIZO</text>')

    # 3. Interior Cocina:
    # Paso libre exterior (1,25 m de X=4.00 a X=5.25)
    out.append(f'<text x="{dx(4.62):.1f}" y="{dy(0.35):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.0" text-anchor="middle">PASO 1,25 m</text>')

    # Sección Isla Santos (X=5.25..6.35 -> 1,10 m ancho, H=0,92 m)
    out.append(f'<rect x="{dx(5.25):.1f}" y="{dy(0.92):.1f}" width="{1.10*S4:.1f}" height="{0.92*S4:.1f}" fill="#1e293b" stroke="#f8fafc" stroke-width="1.3"/>')
    # Vuelo barra oeste
    out.append(f'<rect x="{dx(5.25):.1f}" y="{dy(0.92):.1f}" width="{0.35*S4:.1f}" height="{0.02*S4:.1f}" fill="url(#grad-dekton)"/>')
    # Taburete en sección
    out.append(f'<rect x="{dx(5.00):.1f}" y="{dy(0.65):.1f}" width="22" height="6" rx="2" fill="#38bdf8"/>')
    out.append(f'<line x1="{dx(5.10):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(5.10):.1f}" y2="{dy(0.65):.1f}" stroke="#64748b" stroke-width="1.5"/>')
    out.append(f'<text x="{dx(5.80):.1f}" y="{dy(0.50):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ISLA 1,10m</text>')

    # Paso de trabajo culinario (1,15 m de X=6.35 a X=7.50)
    out.append(f'<text x="{dx(6.92):.1f}" y="{dy(0.35):.1f}" fill="#10b981" font-family="monospace" font-size="6.0" text-anchor="middle">PASO 1,15 m</text>')

    # Sección Frente Columnas Este (X=7.50..8.15 -> fondo 0,65 m, H=2,65 m hasta techo)
    out.append(f'<rect x="{dx(7.50):.1f}" y="{d_ceil_y:.1f}" width="{0.65*S4:.1f}" height="{2.65*S4:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.4"/>')
    out.append(f'<text x="{dx(7.82):.1f}" y="{dy(1.30):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 {dx(7.82):.1f} {dy(1.30):.1f})" text-anchor="middle">COLUMNAS ESTE (0,65 m)</text>')

    # Cotas Sección Transversal
    out.append(dim_h(dx(0.00), dx(4.00), D_GROUND_Y, 20, "4,00 m Patio Corrala", "#10b981", marker="tick-emerald", font_size=7.0))
    out.append(dim_h(dx(4.00), dx(5.25), D_GROUND_Y, 20, "1,25 m Paso", "#38bdf8", font_size=6.8))
    out.append(dim_h(dx(5.25), dx(6.35), D_GROUND_Y, 20, "1,10 m Isla", "#f8fafc", font_size=6.8))
    out.append(dim_h(dx(6.35), dx(7.50), D_GROUND_Y, 20, "1,15 m Paso", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_h(dx(7.50), dx(8.15), D_GROUND_Y, 20, "0,65 m", "#94a3b8", font_size=6.5))
    out.append(dim_h(dx(4.00), dx(8.15), D_GROUND_Y, 40, "4,15 m ANCHO TOTAL COCINA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # BANDA DERECHA: GUÍA TÉCNICA DE ALTURAS ERGONÓMICAS Y MECANISMOS
    # ==========================================================================
    rx = 1480
    out.append(f'<rect x="{rx}" y="30" width="440" height="1360" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="420" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">GUÍA ERGONÓMICA Y DE ALTURAS (UNE)</text>')

    alturas_data = [
        ("1. NIVELES VERTICALES NORMALIZADOS", "#38bdf8", [
            ("+2,65 m", "Falso techo continuo (yeso laminado hidrófugo)"),
            ("+2,50 m", "Fosa perimetral cortinero hacia patio claustro"),
            ("+2,20 m", "Coronación superior de las 10 columnas Santos"),
            ("+1,75 m", "Límite superior horno microondas / vapor"),
            ("+1,45 m", "Estante superior mueble desayunador pocket LED"),
            ("+1,30 m", "Eje visual y táctil horno Bosch Serie 8"),
            ("+1,10 m", "Tomas de encimera C5 y tomas desayunador"),
            ("+0,92 m", "Cota superior encimera Dekton (isla y desayunador)"),
            ("+0,65 m", "Plano de asiento de 5 taburetes altos de barra"),
            ("+0,30 m", "Bases de enchufe ocultas zócalo y fuerza"),
            ("+0,08 m", "Zócalo retraído Santos (rejillas ventilación)"),
            ("±0,00 m", "Suelo radiante porcelánico continuo"),
        ]),
        ("2. VENTAJAS DE LA UNIFICACIÓN (20,80 m²)", "#f59e0b", [
            ("Gran almacenamiento", "10 columnas continuas (6,00 m lineales)"),
            ("Cava de vinos integrada", "Santos 60 botellas climatizada con vitrina"),
            ("Isla expandida 3,60 m", "Superficie de preparación culinaria XXL"),
            ("Apertura total Sur", "Conexión directa y fluida con Comedor 10 Pax"),
            ("Luz natural Este-Oeste", "Ventanal continuo Cortizo hacia el patio"),
        ]),
        ("3. JUSTIFICACIÓN BIOMECÁNICA", "#10b981", [
            ("Encimera a +0,92 m", "Reduce un 35% la flexión lumbar al cortar"),
            ("Hornos a +0,92..1,45 m", "Manipulación de bandejas a 90° de codo"),
            ("Campana Bora integrada", "Cero obstáculos visuales hacia el patio"),
            ("Voladizo barra 35 cm", "Espacio para rodillas sin rozar frentes"),
        ]),
        ("4. PRÓXIMOS PASOS ACORDADOS", "#f43f5e", [
            ("Paso A", "Validar plano de planta y sección transversal"),
            ("Paso B", "Replanteo de tomas eléctricas (fuerza, C3, C4, C5)"),
            ("Paso C", "Diseño luminotécnico (carril magnético + LEDs)"),
            ("Paso D", "Detalle encuentro ventanal Cortizo a cota cero"),
        ]),
    ]

    sy = 85
    for cat_title, cat_col, rows in alturas_data:
        out.append(f'<text x="{rx+16}" y="{sy}" fill="{cat_col}" font-family="monospace" font-size="7.5" font-weight="700">{cat_title}</text>')
        out.append(f'<line x1="{rx+16}" y1="{sy+4}" x2="{rx+424}" y2="{sy+4}" stroke="{cat_col}" stroke-width="0.7" opacity="0.6"/>')
        sy += 16
        for k, v in rows:
            out.append(f'<text x="{rx+20}" y="{sy}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700">{k}:</text>')
            out.append(f'<text x="{rx+85}" y="{sy}" fill="#e2e8f0" font-family="monospace" font-size="6.0">{v}</text>')
            sy += 17
        sy += 10

    out.append('</svg>')
    return "\n".join(out)


def build_cocina_interactivo_html():
    """Genera visor web interactivo de la cocina unificada de 20,80 m²"""
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cocina Unificada de Gran Almacenaje (20,80 m²) · Hogar Oleiros</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background-color: #070b14; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; }
    .tab-btn.active { border-color: #38bdf8; color: #38bdf8; background: rgba(56, 189, 248, 0.1); }
  </style>
</head>
<body class="p-4 md:p-8 max-w-7xl mx-auto">
  <!-- Cabecera -->
  <header class="border-b border-slate-800 pb-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950/60 border border-sky-800 text-sky-400 text-xs font-mono mb-2">
        <span>RAMA: feature/cocina-diseno-elevaciones (Propuesta Unificada 20,80 m²)</span>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
        <span>🍳 Cocina Unificada de Gran Almacenaje (20,80 m²)</span>
      </h1>
      <p class="text-slate-400 text-sm mt-1">Integración total Cocina (15,20 m²) + Despensa Sur (5,60 m²) · Frente Monumental Este 6,00 m · Abierta al Comedor Sur y Patio Oeste</p>
    </div>
    <div class="flex gap-2">
      <a href="plano_cocina_planta_esquematica.svg" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 rounded-lg text-xs font-mono transition">
        Descargar SVG Planta K-01
      </a>
      <a href="plano_cocina_elevaciones_alturas.svg" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 rounded-lg text-xs font-mono transition">
        Descargar SVG Alzados K-02
      </a>
    </div>
  </header>

  <!-- Pestañas de Navegación de Planos -->
  <div class="flex border-b border-slate-800 mb-6 gap-2">
    <button onclick="showTab('planta')" id="tab-planta" class="tab-btn active px-5 py-3 font-mono text-sm border-b-2 font-bold transition flex items-center gap-2">
      <span>📐 Plano K-01: Planta Cocina Unificada (1:20)</span>
    </button>
    <button onclick="showTab('elevaciones')" id="tab-elevaciones" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📏 Plano K-02: Alzados 6m & Sección Patio (1:20)</span>
    </button>
    <button onclick="showTab('resumen')" id="tab-resumen" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📋 Análisis Espacial & Memoria</span>
    </button>
  </div>

  <!-- Contenedor Tab 1: Planta Esquemática -->
  <div id="content-planta" class="space-y-4">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 overflow-hidden shadow-2xl">
      <div class="flex justify-between items-center mb-3 px-2">
        <span class="text-xs font-mono text-sky-400">ESPACIO UNIFICADO 4,15 × 6,00 m = 20,80 m² · ISLA SANTOS 3,60 × 1,10 m · FRENTE COLUMNAS 6,00 m</span>
        <span class="text-xs font-mono text-slate-500">Vector SVG ISO 128 (Zoom Nativo)</span>
      </div>
      <div class="w-full overflow-x-auto border border-slate-800 rounded-xl bg-slate-950">
        <img src="plano_cocina_planta_esquematica.svg" alt="Plano Planta Cocina" class="w-full min-w-[900px] h-auto block"/>
      </div>
    </div>
  </div>

  <!-- Contenedor Tab 2: Alzados y Alturas -->
  <div id="content-elevaciones" class="space-y-4 hidden">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 overflow-hidden shadow-2xl">
      <div class="flex justify-between items-center mb-3 px-2">
        <span class="text-xs font-mono text-amber-400">FRENTE MONUMENTAL 10 COLUMNAS (6,00m) · GRAN ISLA (3,60m) · SECCIÓN TRANSVERSAL CON PATIO</span>
        <span class="text-xs font-mono text-slate-500">Vector SVG ISO 128</span>
      </div>
      <div class="w-full overflow-x-auto border border-slate-800 rounded-xl bg-slate-950">
        <img src="plano_cocina_elevaciones_alturas.svg" alt="Plano Alzados Cocina" class="w-full min-w-[900px] h-auto block"/>
      </div>
    </div>
  </div>

  <!-- Contenedor Tab 3: Resumen & Siguientes Pasos -->
  <div id="content-resumen" class="grid grid-cols-1 md:grid-cols-3 gap-6 hidden">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-sky-400 font-mono mb-4">📐 Geometría Unificada (20,80 m²)</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Dimensiones:</strong> 4,15 m (ancho) × 6,00 m (largo)</li>
        <li>• <strong class="text-white">Superficie útil:</strong> 20,80 m² continuos</li>
        <li>• <strong class="text-white">Gran Isla Santos:</strong> 3,60 × 1,10 m (Dekton Kelya)</li>
        <li>• <strong class="text-white">Frente Columnas:</strong> 6,00 × 0,65 m (10 módulos × 60cm)</li>
        <li>• <strong class="text-white">Paso a Patio Oeste:</strong> 1,25 m (amplitud taburetes)</li>
        <li>• <strong class="text-white">Paso Culinario Este:</strong> 1,15 m (apertura cajones/horno)</li>
        <li>• <strong class="text-white">Apertura Sur:</strong> 4,15 m diáfana hacia Comedor</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-amber-400 font-mono mb-4">🏛️ Frente Monumental (10 Módulos)</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Col 01:</strong> Frigorífico integrable XXL (todo frío)</li>
        <li>• <strong class="text-white">Col 02:</strong> Congelador vertical No-Frost</li>
        <li>• <strong class="text-white">Col 03:</strong> Cava vinos Santos 60 botellas</li>
        <li>• <strong class="text-white">Col 04:</strong> Torre Horno + Micro Bosch Serie 8</li>
        <li>• <strong class="text-white">Col 05-06:</strong> Desayunador Pocket 120cm</li>
        <li>• <strong class="text-white">Col 07-08:</strong> Despensa doble con gavetas Legrabox</li>
        <li>• <strong class="text-white">Col 09:</strong> Back kitchen auxiliar (robots)</li>
        <li>• <strong class="text-white">Col 10:</strong> Vitrina vajillero orientada al comedor</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-emerald-400 font-mono mb-4">⚡ Siguiente Hoja de Ruta</h3>
      <p class="text-xs text-slate-400 mb-3">Con la unificación espacial consolidada, abordamos:</p>
      <div class="space-y-2 text-sm text-slate-300">
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-sky-300">1. Enchufes y Potencias:</strong> Torres escamoteables en isla (Twist), tomas en desayunador (4×C5 a +1,10m) y líneas dedicadas C3 (25A) y C4 (16A).
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-amber-300">2. Iluminación IES:</strong> Carril magnético empotrado en techo alineado con la isla de 3,60 m + LEDs cálidos 3000K en vitrina y desayunador.
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-emerald-300">3. Ventanal y Vano:</strong> Encuentro corredera Cortizo Cor Vision Plus a cota cero hacia el patio.
        </div>
      </div>
    </div>
  </div>

  <script>
    function showTab(tab) {
      document.getElementById('content-planta').classList.toggle('hidden', tab !== 'planta');
      document.getElementById('content-elevaciones').classList.toggle('hidden', tab !== 'elevaciones');
      document.getElementById('content-resumen').classList.toggle('hidden', tab !== 'resumen');
      
      document.getElementById('tab-planta').classList.toggle('active', tab === 'planta');
      document.getElementById('tab-elevaciones').classList.toggle('active', tab === 'elevaciones');
      document.getElementById('tab-resumen').classList.toggle('active', tab === 'resumen');
      
      if(tab === 'planta') {
        document.getElementById('tab-planta').classList.add('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-elevaciones').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-resumen').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
      } else if (tab === 'elevaciones') {
        document.getElementById('tab-elevaciones').classList.add('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-planta').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-resumen').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
      } else {
        document.getElementById('tab-resumen').classList.add('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-planta').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
        document.getElementById('tab-elevaciones').classList.remove('border-sky-400', 'text-sky-400', 'bg-sky-950/20');
      }
    }
  </script>
</body>
</html>
"""

def main():
    print("Generando Plano K-01: Planta Cocina Unificada de Gran Almacenaje (20,80 m²)...")
    planta_svg = build_cocina_planta_svg()
    with open("plano_cocina_planta_esquematica.svg", "w", encoding="utf-8") as f:
        f.write(planta_svg)
    print(" -> Guardado en plano_cocina_planta_esquematica.svg")

    print("Generando Plano K-02: Alzados 6m y Sección Transversal con Patio...")
    elev_svg = build_cocina_elevaciones_svg()
    with open("plano_cocina_elevaciones_alturas.svg", "w", encoding="utf-8") as f:
        f.write(elev_svg)
    print(" -> Guardado en plano_cocina_elevaciones_alturas.svg")

    print("Generando Visor Web Interactivo...")
    html_content = build_cocina_interactivo_html()
    with open("cocina_estudio_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(" -> Guardado en cocina_estudio_interactivo.html")

    # Validación XML estricta
    for fname in ["plano_cocina_planta_esquematica.svg", "plano_cocina_elevaciones_alturas.svg"]:
        ET.parse(fname)
        print(f" -> {fname}: 100% VALID XML (0 errores)")

    print("Completado con éxito.")

if __name__ == "__main__":
    main()
