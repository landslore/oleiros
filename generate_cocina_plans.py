#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos de la Cocina Unificada Santos (Opción A: Frente Mixto con Ventanal Panorámico Este)
- Superficie total unificada: 20,80 m² útiles (4,15 m ancho x 6,00 m longitud)
- Frente Este Mixto de 6,00 m:
  * 3 Columnas altas Norte (1,80 m): Frigo XXL, Congelador No-Frost, Torre Horno/Micro Bosch Serie 8
  * Bancada central Desayunador/Coffee Station (3,00 m) con VENTANAL PANORÁMICO ESTE (3,00 x 0,80 m)
  * 2 Columnas altas Sur (1,20 m): Cava de Vinos Santos climatizada (60 botellas) + Gran Despensa / Vitrina Comedor
- Gran Isla Central Santos Fine de 3,60 x 1,10 m con placa Bora Pure, fregadero 70 cm y 5 taburetes al patio
- Apertura total al Oeste (Patio Corrala Claustro con corredera Cortizo 3,00x2,60m)
- Apertura total al Sur (Comedor Principal con 4,20 m de fondo libres para mesa 10 Pax)
- Triple orientación lumínica: Sol de mañana (Este) + Sol de tarde (Oeste) + Luz meridional (Sur)
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
      <linearGradient id="grad-sol-este" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.35"/>
        <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.05"/>
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
    Plano K-01: Planta de la Cocina Unificada Santos (Opción A: Frente Mixto con Ventanal Panorámico Este)
    Dimensiones: 4,15 m (ancho) x 6,00 m (longitud) = 20,80 m² útiles
    """
    W, H = 1920, 1220
    S = 135.0  # 1m = 135px
    OX = 260.0
    OY = 210.0

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
        '<rect x="32" y="30" width="1400" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-01 · PLANTA COCINA UNIFICADA: FRENTE MIXTO CON VENTANAL PANORÁMICO ESTE (20,80 m² · 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Propuesta A · Ventana Faja Este (Luz de Mañana) · Gran Isla Santos 3,60 m · Abierta a Patio Oeste y Comedor Sur (4,20 m libres)</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1400" height="1100" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
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

    # 2. Muro Este Exterior Perimetral (X = 4.15, de Y = -0.15 a Y = 6.20):
    # Tramo Norte ciego tras columnas altas (Y = -0.15..1.80)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(-0.15):.1f}" width="{tw_ext:.1f}" height="{1.95*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')
    # Tramo Central con VENTANAL PANORÁMICO ESTE C-07 (Y = 1.80..4.80 -> 3,00 m de hueco acristalado sobre bancada):
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(1.80):.1f}" width="{tw_ext:.1f}" height="{3.00*S:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.4"/>')
    # Vidrio continuo con luz de mañana
    out.append(f'<line x1="{mx(4.30):.1f}" y1="{my(1.80):.1f}" x2="{mx(4.30):.1f}" y2="{my(4.80):.1f}" stroke="#38bdf8" stroke-width="2.5"/>')
    out.append(f'<line x1="{mx(4.35):.1f}" y1="{my(1.80):.1f}" x2="{mx(4.35):.1f}" y2="{my(4.80):.1f}" stroke="#f59e0b" stroke-width="1.0" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{mx(4.65):.1f}" y="{my(3.30):.1f}" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700" transform="rotate(90 {mx(4.65):.1f} {my(3.30):.1f})" text-anchor="middle">VENTANAL PANORÁMICO ESTE C-07 (3,00×0,80 m · SOL MAÑANA)</text>')
    # Tramo Sur ciego tras columnas altas (Y = 4.80..6.20)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(4.80):.1f}" width="{tw_ext:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.4"/>')

    # Pilares en muro este (P-15 intermedio en Y=4.00 embebido en jamba, P-20 en Y=6.00)
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(3.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(4.45):.1f}" y="{my(4.00):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-15</text>')
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(5.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(4.45):.1f}" y="{my(6.00):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-20</text>')

    # 3. Límite Oeste:
    # Tramo 1 (Y=0.00..4.00): Ventanal corredero al Patio Corrala Central (C-06 3,00x2,60 m)
    out.append(f'<rect x="{mx(-0.12):.1f}" y="{my(3.88):.1f}" width="{0.25*S:.1f}" height="{0.25*S:.1f}" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{mx(-0.25):.1f}" y="{my(4.02):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">P-13</text>')
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.40*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{mx(-0.02):.1f}" y1="{my(0.30):.1f}" x2="{mx(-0.02):.1f}" y2="{my(2.05):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<line x1="{mx(0.02):.1f}" y1="{my(1.95):.1f}" x2="{mx(0.02):.1f}" y2="{my(3.70):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<text x="{mx(-0.12):.1f}" y="{my(2.00):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" transform="rotate(-90 {mx(-0.12):.1f} {my(2.00):.1f})" text-anchor="middle">CORREDERA PATIO CORRALA C-06 (3,00×2,60 m)</text>')

    # Tramo 2 Oeste (Y=4.00..6.00): Abierto / Conexión fluida con corredor hacia Salón
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(4.00):.1f}" x2="{mx(0.00):.1f}" y2="{my(6.00):.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(-0.10):.1f}" y="{my(5.00):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" transform="rotate(-90 {mx(-0.10):.1f} {my(5.00):.1f})" text-anchor="middle">PASO LIBRE AL SALÓN (2,00 m)</text>')

    # 4. Límite Sur (Y = 6.00): Abierto diáfano al Comedor Principal
    out.append(f'<line x1="{mx(0.00):.1f}" y1="{my(6.00):.1f}" x2="{mx(4.15):.1f}" y2="{my(6.00):.1f}" stroke="#10b981" stroke-width="1.2" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{mx(2.07):.1f}" y="{my(6.15):.1f}" fill="#10b981" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="middle">LÍNEA DE CONEXIÓN DIÁFANA CON COMEDOR (4,20 m DE FONDO LIBRES AL SUR)</text>')

    # Pavimento interior técnico
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{4.15*S:.1f}" height="{6.00*S:.1f}" fill="#0f172a" opacity="0.88"/>')

    # Rayo sutil de sol matinal entrando por la ventana este
    out.append(f'<polygon points="{mx(4.15):.1f},{my(1.80):.1f} {mx(4.15):.1f},{my(4.80):.1f} {mx(2.50):.1f},{my(4.20):.1f} {mx(2.50):.1f},{my(2.40):.1f}" fill="url(#grad-sol-este)"/>')

    # Círculo NHG Ø1,50 m
    out.append(f'<circle cx="{mx(2.15):.1f}" cy="{my(2.60):.1f}" r="{0.75*S:.1f}" fill="#38bdf8" fill-opacity="0.04" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(2.15):.1f}" y="{my(2.64):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" text-anchor="middle">GIRO REGLAMENTARIO Ø1,50 m (NHG)</text>')

    # --------------------------------------------------------------------------
    # FRENTE MIXTO ESTE DE 6,00 m (OPCIÓN A: COLUMNAS + BANCADA PANORÁMICA + COLUMNAS)
    # --------------------------------------------------------------------------
    fc_x = mx(3.50)
    fc_w = 0.65 * S

    # BLOQUE 1 NORTE: 3 Columnas altas (Y=0.00..1.80 -> 1,80 m)
    out.append(f'<rect x="{fc_x:.1f}" y="{my(0.00):.1f}" width="{fc_w:.1f}" height="{1.80*S:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.4"/>')
    cols_norte = [
        (0.00, "COL 01", "FRIGORÍFICO XXL", "Integrado 1-puerta", "#38bdf8"),
        (0.60, "COL 02", "CONGELADOR", "No-Frost vertical", "#38bdf8"),
        (1.20, "COL 03", "TORRE HORNO/MIC", "Bosch Serie 8", "#f59e0b"),
    ]
    for yo, cod, tit, sub, col in cols_norte:
        m_top = my(yo)
        out.append(f'<line x1="{fc_x:.1f}" y1="{m_top:.1f}" x2="{fc_x+fc_w:.1f}" y2="{m_top:.1f}" stroke="#475569" stroke-width="0.9"/>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+17:.1f}" fill="{col}" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">{cod}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+33:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{tit}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+48:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{sub}</text>')

    # BLOQUE 2 CENTRAL: Bancada Desayunador / Coffee Station bajo Ventanal Panorámico (Y=1.80..4.80 -> 3,00 m)
    # Encimera Dekton de fondo 65 cm
    bk_y = my(1.80)
    bk_h = 3.00 * S
    out.append(f'<rect x="{fc_x:.1f}" y="{bk_y:.1f}" width="{fc_w:.1f}" height="{bk_h:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>')
    out.append(f'<rect x="{fc_x+2:.1f}" y="{bk_y+2:.1f}" width="{fc_w-4:.1f}" height="{bk_h-4:.1f}" fill="url(#grad-dekton)" opacity="0.35"/>')
    # 3 módulos bajos de 100 cm (o 5 de 60 cm)
    for idx_mb, my_mb in enumerate([2.80, 3.80]):
        out.append(f'<line x1="{fc_x:.1f}" y1="{my(my_mb):.1f}" x2="{fc_x+fc_w:.1f}" y2="{my(my_mb):.1f}" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(2.30):.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">COFFEE STATION</text>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(2.45):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Cafetera Espresso · Molinillo</text>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(3.30):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">BANCADA BAJO VENTANAL (H=+0,92m)</text>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(3.45):.1f}" fill="#f8fafc" font-family="monospace" font-size="5.8" text-anchor="middle">3,00 m Encimera Dekton · Sol de Mañana</text>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(4.30):.1f}" fill="#10b981" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ZONA ROBOTS / AIRFRYER</text>')
    out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{my(4.45):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">4×Tomas C5 a +1,10m</text>')

    # BLOQUE 3 SUR: 2 Columnas altas (Y=4.80..6.00 -> 1,20 m)
    out.append(f'<rect x="{fc_x:.1f}" y="{my(4.80):.1f}" width="{fc_w:.1f}" height="{1.20*S:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.4"/>')
    cols_sur = [
        (4.80, "COL 04", "CAVA SANTOS", "60 botellas doble-Tª", "#f59e0b"),
        (5.40, "COL 05", "DESPENSA / VITRINA", "Gavetas + Cristalería", "#10b981"),
    ]
    for yo, cod, tit, sub, col in cols_sur:
        m_top = my(yo)
        out.append(f'<line x1="{fc_x:.1f}" y1="{m_top:.1f}" x2="{fc_x+fc_w:.1f}" y2="{m_top:.1f}" stroke="#475569" stroke-width="0.9"/>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+17:.1f}" fill="{col}" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">{cod}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+33:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{tit}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+48:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{sub}</text>')

    # --------------------------------------------------------------------------
    # GRAN ISLA CENTRAL SANTOS FINE DE 3,60 x 1,10 m
    # --------------------------------------------------------------------------
    isla_x = mx(1.25)
    isla_y = my(1.00)
    isla_w = 1.10 * S
    isla_h = 3.60 * S

    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="2.0"/>')
    out.append(f'<rect x="{isla_x+3:.1f}" y="{isla_y+3:.1f}" width="{isla_w-6:.1f}" height="{isla_h-6:.1f}" fill="url(#grad-dekton)" opacity="0.4" stroke="#475569" stroke-width="0.8"/>')

    # Línea barra snack volada (35 cm Oeste mirando al patio)
    barra_split_x = isla_x + 0.35 * S
    out.append(f'<line x1="{barra_split_x:.1f}" y1="{isla_y:.1f}" x2="{barra_split_x:.1f}" y2="{isla_y+isla_h:.1f}" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="5,2"/>')
    out.append(f'<text x="{isla_x+16:.1f}" y="{isla_y+isla_h/2:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 {isla_x+16:.1f} {isla_y+isla_h/2:.1f})" text-anchor="middle">BARRA SNACK VOLADA 35 cm (VISTAS AL PATIO)</text>')

    # 5 Taburetes altos
    for ty in [1.35, 2.00, 2.65, 3.30, 3.95]:
        st_cx = isla_x - 0.22 * S
        st_cy = my(ty)
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.18*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.08*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.6"/>')

    # Fregadero bajo encimera 70 cm
    sink_w = 0.52 * S
    sink_h = 0.75 * S
    sink_x = isla_x + 0.45 * S
    sink_y = isla_y + 0.40 * S
    out.append(f'<rect x="{sink_x:.1f}" y="{sink_y:.1f}" width="{sink_w:.1f}" height="{sink_h:.1f}" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<rect x="{sink_x+4:.1f}" y="{sink_y+4:.1f}" width="{sink_w-8:.1f}" height="{sink_h-8:.1f}" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<circle cx="{sink_x+sink_w/2:.1f}" cy="{sink_y+sink_h/2:.1f}" r="6" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<line x1="{sink_x+sink_w/2:.1f}" y1="{sink_y+sink_h/2:.1f}" x2="{sink_x+sink_w/2-10:.1f}" y2="{sink_y+sink_h/2:.1f}" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<text x="{sink_x+sink_w/2:.1f}" y="{sink_y+sink_h+16:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">FREGADERO 70×45 cm</text>')

    # Lavavajillas panelado 60 cm
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+1.50*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">[ LAVAVAJILLAS PANELADO 60 cm ]</text>')

    # Placa Bora Pure 80 cm
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

    # Zona Preparación y Emplatado Sur
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+3.20*S:.1f}" fill="#10b981" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">ZONA PREPARACIÓN Y SERVICIO</text>')
    out.append(f'<text x="{isla_x+0.72*S:.1f}" y="{isla_y+3.35*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Caceroleros 90 cm + Enchufes Twist</text>')

    # Rótulo de estancia unificada
    out.append(f'<rect x="{mx(1.05):.1f}" y="{my(5.05):.1f}" width="240" height="46" rx="4" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{mx(1.05)+120:.1f}" y="{my(5.05)+19:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">[E-08] COCINA UNIFICADA SANTOS</text>')
    out.append(f'<text x="{mx(1.05)+120:.1f}" y="{my(5.05)+35:.1f}" fill="#f8fafc" font-family="monospace" font-size="7.5" text-anchor="middle">S.Útil: 20,80 m² · Ventanal Este 3,00 m · Z=±0,00m</text>')

    # --------------------------------------------------------------------------
    # COTAS GENERALES ISO 129
    # --------------------------------------------------------------------------
    out.append(dim_h(mx(0.00), isla_x, my(0.15), 0, "1,25 m (Paso Libre Patio)", "#38bdf8", font_size=7.2))
    out.append(dim_h(isla_x, isla_x + isla_w, my(0.15), 0, "1,10 m (Ancho Isla)", "#f8fafc", font_size=7.2))
    out.append(dim_h(isla_x + isla_w, fc_x, my(0.15), 0, "1,15 m (Paso Libre Trabajo)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_h(fc_x, mx(4.15), my(0.15), 0, "0,65 m", "#94a3b8", font_size=7.0))
    out.append(dim_h(mx(0.00), mx(4.15), my(-0.05), -25, "4,15 m (ANCHO TOTAL ESPACIO COCINA)", "#38bdf8", font_size=8.5))

    out.append(dim_v(my(0.00), isla_y, isla_x, -35, "1,00 m", "#94a3b8", font_size=7.0))
    out.append(dim_v(isla_y, isla_y + isla_h, isla_x, -35, "3,60 m (LONGITUD GRAN ISLA)", "#f8fafc", font_size=8.0))
    out.append(dim_v(isla_y + isla_h, my(6.00), isla_x, -35, "1,40 m (Paso Abierto a Comedor)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_v(my(0.00), my(6.00), mx(0.00), -60, "6,00 m (LONGITUD TOTAL ESPACIO COCINA)", "#38bdf8", font_size=9.0))

    # Cotas del Frente Mixto Este:
    out.append(dim_v(my(0.00), my(1.80), mx(4.15), 30, "1,80 m (3 Columnas Norte)", "#38bdf8", font_size=7.2))
    out.append(dim_v(my(1.80), my(4.80), mx(4.15), 30, "3,00 m (Bancada y Ventanal Este)", "#f59e0b", marker="tick-amber", font_size=7.5))
    out.append(dim_v(my(4.80), my(6.00), mx(4.15), 30, "1,20 m (2 Columnas Sur)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_v(my(0.00), my(6.00), mx(4.15), 65, "6,00 m (Frente Mixto Este)", "#38bdf8", font_size=8.5))

    # --------------------------------------------------------------------------
    # BANDA DERECHA: MEMORIA TÉCNICA
    # --------------------------------------------------------------------------
    rx = 1460
    out.append(f'<rect x="{rx}" y="30" width="430" height="1150" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="410" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">MEMORIA FRENTE MIXTO Y LUZ ESTE</text>')

    specs = [
        ("1. ESTRATEGIA DE LUZ DE MAÑANA (ESTE)", "#f59e0b", [
            ("Ventanal Panorámico C-07", "3,00 × 0,80 m enrasado a encimera"),
            ("Sol matinal en Galicia", "Luz suave y energizante en el desayuno"),
            ("Vistas al jardín lateral", "Conexión visual con vegetación este"),
            ("Triple orientación", "Este (mañana) + Oeste (patio) + Sur (comedor)"),
        ]),
        ("2. FRENTE MIXTO SANTOS (6,00 m)", "#38bdf8", [
            ("3 Columnas altas Norte", "Frigo XXL + Congelador + Horno/Mic"),
            ("Bancada baja central (3m)", "Coffee station + robots + gavetas bajas"),
            ("2 Columnas altas Sur", "Cava Santos 60 botellas + Despensa/Vitrina"),
            ("Capacidad de almacenaje", "5 columnas de 60cm + 3m gavetas + isla"),
        ]),
        ("3. GRAN ISLA CENTRAL SANTOS (3,60×1,10 m)", "#10b981", [
            ("Superficie de trabajo", "Encimera Dekton Kelya 20 mm"),
            ("Cocción Bora Pure", "Extracción integrada sin campana colgante"),
            ("Fregadero y lavavajillas", "Seno 70 cm + LVV panelado integrado"),
            ("Barra snack al patio", "5 taburetes mirando al Acer palmatum"),
        ]),
        ("4. RELACIÓN CON EL COMEDOR SUR", "#cbd5e1", [
            ("Fondo libre comedor", "4,20 m libres hasta cristalera sur"),
            ("Mesa 10 Pax (2,80×1,00m)", "Ocupa 2,20 m con sillas a ambos lados"),
            ("Pasos libres holgados", "1,00 m libre al norte y 1,00 m al sur"),
            ("Transición fluida", "Cero tabiques; espacio diáfano continuo"),
        ]),
        ("5. DETALLE DE INSTALACIONES (FASE 2)", "#f43f5e", [
            ("Tomas bancada este", "4 tomas C5 a +1,10m para cafeteras/robots"),
            ("Tomas isla central", "Torre Twist escamoteable + tomas laterales"),
            ("Líneas dedicadas", "C3 Bora (25A), C4 frigo/cava/LVV (16A)"),
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
    Plano K-02: Alzados y Sección de la Cocina con Ventanal Panorámico Este (Opción A)
    - Alzado A: Frente Mixto Este con Ventanal Panorámico (L = 6,00 m, H = 2,65 m)
    - Alzado B: Gran Isla Santos - Frente Trabajo Este (L = 3,60 m, H = 0,92 m)
    - Alzado C: Gran Isla Santos - Frente Barra Social Oeste hacia Patio (L = 3,60 m, H = 0,92 m)
    - Alzado D: Sección Transversal Este-Oeste completa mostrando el corte de luz
    """
    W, H = 1950, 1420
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1440" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-02 · ALZADOS Y SECCIÓN: FRENTE MIXTO CON VENTANAL PANORÁMICO ESTE (1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Ventanal Este 3,00×0,80 m sobre Bancada Dekton · Gran Isla 3,60 m · Sección Transversal con Patio Claustro · Cotas s/ Suelo ±0,00m</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1440" height="1310" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # ==========================================================================
    # SECCIÓN 1: ALZADO A - FRENTE MIXTO ESTE CON VENTANAL PANORÁMICO (6,00 m)
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

    out.append(f'<rect x="{ax(0.0):.1f}" y="{ceil_y-32:.1f}" width="560" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{ax(0.0)+10:.1f}" y="{ceil_y-17:.1f}" fill="#f59e0b" font-family="monospace" font-size="9.0" font-weight="700">ALZADO A · FRENTE MIXTO ESTE CON VENTANAL PANORÁMICO C-07 (L = 6,00 m · H = 2,65 m)</text>')

    # Zócalo general
    out.append(f'<rect x="{ax(0.0):.1f}" y="{ay(0.08):.1f}" width="{6.00*S1:.1f}" height="{0.08*S1:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')
    out.append(f'<text x="{ax(3.0):.1f}" y="{A_GROUND_Y-4:.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ZÓCALO RETRANQUEADO h = 8 cm</text>')

    # 1. BLOQUE NORTE: 3 Columnas altas (X=0.00..1.80m, H=2,20m)
    cols_a_norte = [
        (0.00, "FRIGORÍFICO XXL", "1-puerta integrado", 0.60),
        (0.60, "CONGELADOR", "No-Frost vertical", 0.60),
        (1.20, "TORRE HORNO/MIC", "Bosch Serie 8", 0.60),
    ]
    for cx_m, tit, sub, cw in cols_a_norte:
        x1 = ax(cx_m)
        w_px = cw * S1
        out.append(f'<rect x="{x1:.1f}" y="{ay(2.20):.1f}" width="{w_px:.1f}" height="{2.12*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
        if "HORNO" in tit:
            out.append(f'<line x1="{x1:.1f}" y1="{ay(0.70):.1f}" x2="{x1+w_px:.1f}" y2="{ay(0.70):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<rect x="{x1+4:.1f}" y="{ay(1.30):.1f}" width="{w_px-8:.1f}" height="{0.60*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{x1+10:.1f}" y="{ay(1.24):.1f}" width="{w_px-20:.1f}" height="{0.42*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<circle cx="{x1+w_px/2:.1f}" cy="{ay(1.27):.1f}" r="4" fill="none" stroke="#f59e0b" stroke-width="1.0"/>')
            out.append(f'<text x="{x1+w_px/2:.1f}" y="{ay(0.96):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">HORNO PIROLÍTICO</text>')
            out.append(f'<rect x="{x1+4:.1f}" y="{ay(1.75):.1f}" width="{w_px-8:.1f}" height="{0.45*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{x1+10:.1f}" y="{ay(1.71):.1f}" width="{w_px-20:.1f}" height="{0.30*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{x1+w_px/2:.1f}" y="{ay(1.50):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.2" font-weight="700" text-anchor="middle">MICROONDAS / VAPOR</text>')
            out.append(f'<line x1="{x1:.1f}" y1="{ay(1.75):.1f}" x2="{x1+w_px:.1f}" y2="{ay(1.75):.1f}" stroke="#475569" stroke-width="0.8"/>')
        else:
            out.append(f'<line x1="{x1:.1f}" y1="{ay(1.86):.1f}" x2="{x1+w_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{x1+w_px/2:.1f}" y="{ay(1.00):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{tit}</text>')
            out.append(f'<text x="{x1+w_px/2:.1f}" y="{ay(0.85):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">{sub}</text>')

    # 2. BLOQUE CENTRAL: Bancada Baja + Ventanal Panorámico Este (X=1.80..4.80m -> 3,00 m ancho)
    mid_x1 = ax(1.80)
    mid_w_px = 3.00 * S1

    # Muebles bajos (H = 0,08m a 0,90m) con 3 grandes módulos de 100 cm con 2 gavetas caceroleras cada uno
    out.append(f'<rect x="{mid_x1:.1f}" y="{ay(0.90):.1f}" width="{mid_w_px:.1f}" height="{0.82*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    for mb_x in [1.00, 2.00]:
        out.append(f'<line x1="{mid_x1+mb_x*S1:.1f}" y1="{ay(0.90):.1f}" x2="{mid_x1+mb_x*S1:.1f}" y2="{ay(0.08):.1f}" stroke="#475569" stroke-width="0.8"/>')
    out.append(f'<line x1="{mid_x1:.1f}" y1="{ay(0.48):.1f}" x2="{mid_x1+mid_w_px:.1f}" y2="{ay(0.48):.1f}" stroke="#475569" stroke-width="0.8"/>')
    out.append(f'<text x="{mid_x1+mid_w_px/2:.1f}" y="{ay(0.68):.1f}" fill="#cbd5e1" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MUEBLES BAJOS SANTOS (3 GAVETEROS DE 100 cm · LEGRABOX)</text>')
    out.append(f'<text x="{mid_x1+mid_w_px/2:.1f}" y="{ay(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Almacenaje de vajilla, ollas y pequeño menaje</text>')

    # Encimera Dekton Kelya 20 mm (H = 0,90 a 0,92 m)
    out.append(f'<rect x="{mid_x1:.1f}" y="{ay(0.92):.1f}" width="{mid_w_px:.1f}" height="{0.02*S1:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.3"/>')

    # VENTANAL PANORÁMICO ESTE C-07 (de +0,95 m a +1,75 m -> H = 0,80 m, L = 3,00 m):
    win_y1 = ay(1.75)
    win_h_px = 0.80 * S1
    out.append(f'<rect x="{mid_x1:.1f}" y="{win_y1:.1f}" width="{mid_w_px:.1f}" height="{win_h_px:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="2.0"/>')
    # Resplandor de sol de mañana
    out.append(f'<rect x="{mid_x1+3:.1f}" y="{win_y1+3:.1f}" width="{mid_w_px-6:.1f}" height="{win_h_px-6:.1f}" fill="#f59e0b" fill-opacity="0.12"/>')
    out.append(f'<text x="{mid_x1+mid_w_px/2:.1f}" y="{ay(1.40):.1f}" fill="#fde68a" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">☀️ VENTANAL PANORÁMICO ESTE C-07 (3,00 × 0,80 m)</text>')
    out.append(f'<text x="{mid_x1+mid_w_px/2:.1f}" y="{ay(1.22):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" text-anchor="middle">Luz Solar de Mañana · Vistas al Jardín Lateral · Vidrio Bajo Emisivo con Control Solar</text>')
    # 4 Bases de enchufe integradas en esquina de bancada a +1,10m
    out.append(f'<circle cx="{mid_x1+25:.1f}" cy="{ay(1.10):.1f}" r="4.5" fill="#f59e0b" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<circle cx="{mid_x1+40:.1f}" cy="{ay(1.10):.1f}" r="4.5" fill="#f59e0b" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<text x="{mid_x1+55:.1f}" y="{ay(1.10)+3:.1f}" fill="#f59e0b" font-family="monospace" font-size="5.8" font-weight="700">4×C5 Cafetera/Robots</text>')

    # Módulos altos suspendidos sobre la ventana (de +1,78 m a +2,20 m -> H = 0,42 m):
    out.append(f'<rect x="{mid_x1:.1f}" y="{ay(2.20):.1f}" width="{mid_w_px:.1f}" height="{0.42*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Tira LED inferior continua
    out.append(f'<line x1="{mid_x1:.1f}" y1="{ay(1.78):.1f}" x2="{mid_x1+mid_w_px:.1f}" y2="{ay(1.78):.1f}" stroke="#f59e0b" stroke-width="2.0"/>')
    out.append(f'<text x="{mid_x1+mid_w_px/2:.1f}" y="{ay(2.00):.1f}" fill="#cbd5e1" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MUEBLES ALTOS SUSPENDIDOS SANTOS CON ILUMINACIÓN LED INTEGRADA</text>')

    # 3. BLOQUE SUR: 2 Columnas altas (X=4.80..6.00m -> 1,20 m)
    col_sur_x1 = ax(4.80)
    col_sur_w = 1.20 * S1
    out.append(f'<rect x="{col_sur_x1:.1f}" y="{ay(2.20):.1f}" width="{col_sur_w:.1f}" height="{2.12*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Cava de Vinos Santos (4.80 a 5.40m)
    cava_w = 0.60 * S1
    out.append(f'<rect x="{col_sur_x1+4:.1f}" y="{ay(2.15):.1f}" width="{cava_w-8:.1f}" height="{2.02*S1:.1f}" fill="url(#grad-cava)" stroke="#f59e0b" stroke-width="1.2"/>')
    for vy in [0.40, 0.70, 1.00, 1.30, 1.60, 1.90]:
        out.append(f'<line x1="{col_sur_x1+8:.1f}" y1="{ay(vy):.1f}" x2="{col_sur_x1+cava_w-8:.1f}" y2="{ay(vy):.1f}" stroke="#f59e0b" stroke-width="1.0" opacity="0.6"/>')
        out.append(f'<circle cx="{col_sur_x1+20:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
        out.append(f'<circle cx="{col_sur_x1+45:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
        out.append(f'<circle cx="{col_sur_x1+70:.1f}" cy="{ay(vy)-5:.1f}" r="3.5" fill="#fbbf24" opacity="0.8"/>')
    out.append(f'<text x="{col_sur_x1+cava_w/2:.1f}" y="{ay(1.10):.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">CAVA SANTOS</text>')
    out.append(f'<text x="{col_sur_x1+cava_w/2:.1f}" y="{ay(0.95):.1f}" fill="#fbbf24" font-family="monospace" font-size="5.2" text-anchor="middle">60 Botellas Multi-Tª</text>')

    # Despensa / Vitrina Comedor (5.40 a 6.00m)
    vit_x1 = col_sur_x1 + cava_w
    vit_w = 0.60 * S1
    out.append(f'<rect x="{vit_x1+4:.1f}" y="{ay(2.15):.1f}" width="{vit_w-8:.1f}" height="{2.02*S1:.1f}" fill="#0f172a" stroke="#10b981" stroke-width="1.2"/>')
    for vy in [0.55, 1.05, 1.55]:
        out.append(f'<line x1="{vit_x1+8:.1f}" y1="{ay(vy):.1f}" x2="{vit_x1+vit_w-8:.1f}" y2="{ay(vy):.1f}" stroke="#10b981" stroke-width="1.0" opacity="0.7"/>')
    out.append(f'<text x="{vit_x1+vit_w/2:.1f}" y="{ay(1.25):.1f}" fill="#a7f3d0" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">DESPENSA / VITRINA</text>')
    out.append(f'<text x="{vit_x1+vit_w/2:.1f}" y="{ay(1.10):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.2" text-anchor="middle">Gavetas + Vajillero</text>')

    # Remate superior ciego enrasado hasta falso techo (+2,20 a +2,65m)
    out.append(f'<rect x="{ax(0.0):.1f}" y="{ay(2.65):.1f}" width="{6.00*S1:.1f}" height="{0.45*S1:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')
    out.append(f'<text x="{ax(3.0):.1f}" y="{ay(2.65)+0.22*S1+3:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">REMATADO ENRASADO A FALSO TECHO (+2,20 m a +2,65 m · BOCAS VMC)</text>')

    # Cotas de Altura Alzado A
    cx_dim = ax(6.00) + 25
    out.append(dim_v(ay(0.00), ay(0.08), cx_dim, 0, "+0,08 m (Zócalo)", "#94a3b8", font_size=6.8))
    out.append(dim_v(ay(0.08), ay(0.92), cx_dim, 0, "+0,92 m (Bancada Dekton)", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_v(ay(0.92), ay(1.75), cx_dim, 0, "+1,75 m (Ventanal Este 0,80m)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.75), ay(2.20), cx_dim, 0, "+2,20 m (Coronación)", "#cbd5e1", font_size=6.8))
    out.append(dim_v(ay(2.20), ay(2.65), cx_dim, 0, "+2,65 m (Falso Techo)", "#38bdf8", font_size=7.2))

    # ==========================================================================
    # SECCIÓN 2: ALZADO B - GRAN ISLA SANTOS FINE (L = 3,60 m, H = 0,92 m)
    # Frente de Trabajo Este
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

    out.append(f'<rect x="{bx(0.05):.1f}" y="{by(0.08):.1f}" width="{3.50*S2:.1f}" height="{0.08*S2:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')

    isla_mods_360 = [
        ("MÓD. FREGADERO (80 cm)", "Seno 70 cm + Cubos Reciclaje", 0.80, "#38bdf8"),
        ("LAVAVAJILLAS (60 cm)", "Totalmente Integrado Panelado", 0.60, "#38bdf8"),
        ("MÓD. BORA PURE (90 cm)", "2 Caceroleros + Cubertero Nogal", 0.90, "#f59e0b"),
        ("GAVETERO MENAJE (70 cm)", "Extracción Total Blum Legrabox", 0.70, "#cbd5e1"),
        ("MÓD. EMPLATADO (60 cm)", "Salida fluida a Comedor", 0.60, "#10b981"),
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

    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(0.92):.1f}" width="{3.60*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')
    out.append(f'<text x="{bx(1.8):.1f}" y="{by(0.92)-6:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA DEKTON KELYA 20 mm (LONGITUD 3,60 m · COTA DE TRABAJO +0,92 m)</text>')

    bx_dim = bx(3.60) + 25
    out.append(dim_v(by(0.00), by(0.08), bx_dim, 0, "+0,08 m", "#94a3b8", font_size=6.8))
    out.append(dim_v(by(0.08), by(0.90), bx_dim, 0, "0,82 m Muebles Santos", "#cbd5e1", font_size=6.8))
    out.append(dim_v(by(0.00), by(0.92), bx_dim + 35, 0, "+0,92 m COTA ENCIMERA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # SECCIÓN 3: ALZADO C - GRAN ISLA SANTOS (FRENTE BARRA SOCIAL HACIA PATIO CLAUSTRO)
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
    # SECCIÓN 4: ALZADO D - SECCIÓN TRANSVERSAL Y ENTRADA DE LUZ (ESTE <-> OESTE)
    # ==========================================================================
    D_OX = 150.0
    D_GROUND_Y = 1360.0
    S4 = 110.0

    def dx(val_m):
        return D_OX + val_m * S4

    def dy(val_h_m):
        return D_GROUND_Y - val_h_m * S4

    out.append(f'<line x1="{dx(-0.3):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(9.5):.1f}" y2="{D_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{dx(-0.35):.1f}" y="{D_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    d_ceil_y = dy(2.65)
    out.append(f'<line x1="{dx(4.0):.1f}" y1="{d_ceil_y:.1f}" x2="{dx(8.3):.1f}" y2="{d_ceil_y:.1f}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{dx(8.4):.1f}" y="{d_ceil_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">FALSO TECHO +2,65 m</text>')

    out.append(f'<rect x="{dx(0.0):.1f}" y="{d_ceil_y-32:.1f}" width="600" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{dx(0.0)+10:.1f}" y="{d_ceil_y-17:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO D · SECCIÓN TRANSVERSAL: PATIO CORRALA (OESTE) → ISLA → VENTANAL PANORÁMICO ESTE → JARDÍN</text>')

    # 1. Patio Corrala Claustro (X=0.00..4.00m):
    out.append(f'<rect x="{dx(0.0):.1f}" y="{D_GROUND_Y-2:.1f}" width="{4.00*S4:.1f}" height="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>')
    out.append(f'<line x1="{dx(1.50):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(1.50):.1f}" y2="{dy(2.20):.1f}" stroke="#10b981" stroke-width="2.5"/>')
    out.append(f'<circle cx="{dx(1.50):.1f}" cy="{dy(2.00):.1f}" r="{0.65*S4:.1f}" fill="#10b981" fill-opacity="0.25" stroke="#10b981" stroke-width="1.2"/>')
    out.append(f'<text x="{dx(1.50):.1f}" y="{dy(2.00):.1f}" fill="#a7f3d0" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ACER PALMATUM</text>')
    out.append(f'<text x="{dx(2.00):.1f}" y="{dy(0.40):.1f}" fill="#10b981" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">PATIO CORRALA (4,00 m · LUZ DE TARDE)</text>')

    # 2. Corredera Cortizo en X=4.00m
    out.append(f'<line x1="{dx(4.00):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(4.00):.1f}" y2="{d_ceil_y:.1f}" stroke="#38bdf8" stroke-width="3.5"/>')
    out.append(f'<text x="{dx(4.00):.1f}" y="{dy(1.35):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 {dx(4.00):.1f} {dy(1.35):.1f})" text-anchor="middle">CORREDERA CORTIZO (SUELO-TECHO)</text>')

    # 3. Sección Isla Santos (X=5.25..6.35m -> 1,10m ancho)
    out.append(f'<rect x="{dx(5.25):.1f}" y="{dy(0.92):.1f}" width="{1.10*S4:.1f}" height="{0.92*S4:.1f}" fill="#1e293b" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{dx(5.25):.1f}" y="{dy(0.92):.1f}" width="{0.35*S4:.1f}" height="{0.02*S4:.1f}" fill="url(#grad-dekton)"/>')
    out.append(f'<rect x="{dx(5.00):.1f}" y="{dy(0.65):.1f}" width="22" height="6" rx="2" fill="#38bdf8"/>')
    out.append(f'<line x1="{dx(5.10):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(5.10):.1f}" y2="{dy(0.65):.1f}" stroke="#64748b" stroke-width="1.5"/>')
    out.append(f'<text x="{dx(5.80):.1f}" y="{dy(0.50):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ISLA 1,10m</text>')

    # 4. Sección Bancada Este con Ventanal Panorámico (X=7.50..8.15m -> 0,65m fondo)
    # Mueble bajo hasta +0,90m
    out.append(f'<rect x="{dx(7.50):.1f}" y="{dy(0.90):.1f}" width="{0.65*S4:.1f}" height="{0.82*S4:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Encimera Dekton a +0,92m
    out.append(f'<rect x="{dx(7.50):.1f}" y="{dy(0.92):.1f}" width="{0.65*S4:.1f}" height="{0.02*S4:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.2"/>')
    # Ventanal Panorámico Este en muro (de +0,95m a +1,75m)
    out.append(f'<line x1="{dx(8.15):.1f}" y1="{dy(0.95):.1f}" x2="{dx(8.15):.1f}" y2="{dy(1.75):.1f}" stroke="#f59e0b" stroke-width="3.5"/>')
    # Flechas de sol de mañana entrando desde la derecha (Este)
    out.append(f'<line x1="{dx(9.10):.1f}" y1="{dy(1.40):.1f}" x2="{dx(7.70):.1f}" y2="{dy(1.05):.1f}" stroke="#f59e0b" stroke-width="2.0" stroke-dasharray="6,3"/>')
    out.append(f'<polygon points="{dx(7.65)},{dy(1.04)} {dx(7.85)},{dy(1.06)} {dx(7.78)},{dy(1.18)}" fill="#f59e0b"/>')
    out.append(f'<text x="{dx(8.85):.1f}" y="{dy(1.60):.1f}" fill="#f59e0b" font-family="monospace" font-size="7.0" font-weight="700">SOL DE MAÑANA (ESTE)</text>')
    # Mueble alto suspendido (de +1,78m a +2,20m)
    out.append(f'<rect x="{dx(7.75):.1f}" y="{dy(2.20):.1f}" width="{0.40*S4:.1f}" height="{0.42*S4:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0"/>')
    # Cierre superior a techo (+2,20 a +2,65m)
    out.append(f'<rect x="{dx(7.50):.1f}" y="{d_ceil_y:.1f}" width="{0.65*S4:.1f}" height="{0.45*S4:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')

    # Cotas Sección
    out.append(dim_h(dx(0.00), dx(4.00), D_GROUND_Y, 20, "4,00 m Patio Claustro", "#10b981", marker="tick-emerald", font_size=7.0))
    out.append(dim_h(dx(4.00), dx(5.25), D_GROUND_Y, 20, "1,25 m Paso", "#38bdf8", font_size=6.8))
    out.append(dim_h(dx(5.25), dx(6.35), D_GROUND_Y, 20, "1,10 m Isla", "#f8fafc", font_size=6.8))
    out.append(dim_h(dx(6.35), dx(7.50), D_GROUND_Y, 20, "1,15 m Paso", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_h(dx(7.50), dx(8.15), D_GROUND_Y, 20, "0,65 m Bancada", "#f59e0b", marker="tick-amber", font_size=6.5))
    out.append(dim_h(dx(4.00), dx(8.15), D_GROUND_Y, 40, "4,15 m ANCHO TOTAL COCINA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # BANDA DERECHA: GUÍA TÉCNICA Y NIVELES NORMALIZADOS
    # ==========================================================================
    rx = 1480
    out.append(f'<rect x="{rx}" y="30" width="440" height="1360" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="420" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">GUÍA ERGONÓMICA Y COTAS DE ALTURA</text>')

    alturas_data = [
        ("1. NIVELES VERTICALES NORMALIZADOS", "#38bdf8", [
            ("+2,65 m", "Falso techo continuo (yeso hidrófugo y VMC)"),
            ("+2,50 m", "Fosa perimetral cortinero hacia patio claustro"),
            ("+2,20 m", "Coronación superior de muebles altos y columnas"),
            ("+1,75 m", "Dintel superior Ventanal Panorámico Este"),
            ("+1,75 m", "Límite superior horno microondas / vapor"),
            ("+1,45 m", "Estante desayunador y balda suspendida LED"),
            ("+1,30 m", "Eje visual y táctil horno Bosch Serie 8"),
            ("+1,10 m", "Tomas de encimera C5 y tomas coffee station"),
            ("+0,95 m", "Antepecho inferior Ventanal Este (sobre encimera)"),
            ("+0,92 m", "Cota superior encimeras Dekton (isla y bancada)"),
            ("+0,65 m", "Plano de asiento de 5 taburetes altos de barra"),
            ("+0,30 m", "Enchufes ocultos zócalo y fuerza electrodomésticos"),
            ("+0,08 m", "Zócalo retraído Santos (rejillas ventilación)"),
            ("±0,00 m", "Suelo radiante porcelánico continuo"),
        ]),
        ("2. VENTAJAS DE LA OPCIÓN A", "#f59e0b", [
            ("Luz solar de mañana", "Sol este energizante directo en la bancada"),
            ("Luz cruzada Este-Oeste", "Sensación de pabellón acristalado y amplio"),
            ("Almacenaje masivo", "5 columnas altas + 3m cajones bajos + isla"),
            ("Coffee station integrada", "Espacio dedicado para cafetera y tostadora"),
            ("Vistas al jardín", "Trabajar y desayunar mirando a la naturaleza"),
        ]),
        ("3. RELACIÓN ESPACIAL CON EL COMEDOR", "#10b981", [
            ("Fondo libre 4,20 m", "Comedor holgado de 17,50 m² al sur"),
            ("Mesa 10 Pax (2,80×1,00m)", "Pasos de 1,00 m libres al norte y sur"),
            ("Cava y Vitrina sur", "Servicio directo e inmediato a la mesa"),
            ("Isla de 3,60 m", "Zona de emplatado orientada al comedor"),
        ]),
        ("4. PRÓXIMOS PASOS DE LA RAMA", "#f43f5e", [
            ("Mecanismos y fuerza", "Plano de tomas C3 (25A), C4 (16A) y C5 (+1,10m)"),
            ("Iluminación IES", "Carril magnético isla + LED cálido bajo ventana"),
            ("Detalle carpinterías", "Encuentro Cortizo Cor Vision Plus a cota cero"),
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
    """Genera visor web interactivo de la cocina unificada Opción A"""
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cocina Unificada Santos · Frente Mixto con Ventanal Panorámico Este</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background-color: #070b14; color: #f8fafc; font-family: ui-sans-serif, system-ui, sans-serif; }
    .tab-btn.active { border-color: #f59e0b; color: #f59e0b; background: rgba(245, 158, 11, 0.12); }
  </style>
</head>
<body class="p-4 md:p-8 max-w-7xl mx-auto">
  <!-- Cabecera -->
  <header class="border-b border-slate-800 pb-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800 text-amber-400 text-xs font-mono mb-2">
        <span>OPCIÓN A SELECCIONADA: FRENTE MIXTO CON VENTANAL ESTE (20,80 m²)</span>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
        <span>☀️ Cocina Unificada: Ventanal Panorámico Este & Gran Isla Santos</span>
      </h1>
      <p class="text-slate-400 text-sm mt-1">Luz solar de mañana (Este) + Luz de tarde (Patio Claustro Oeste) + Comedor diáfano Sur (4,20 m libres)</p>
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
      <span>📐 Plano K-01: Planta Frente Mixto & Ventanal Este (1:20)</span>
    </button>
    <button onclick="showTab('elevaciones')" id="tab-elevaciones" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📏 Plano K-02: Alzado Ventana 3m & Sección Patio (1:20)</span>
    </button>
    <button onclick="showTab('resumen')" id="tab-resumen" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📋 Memoria de Luz & Almacenaje</span>
    </button>
  </div>

  <!-- Contenedor Tab 1: Planta Esquemática -->
  <div id="content-planta" class="space-y-4">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 overflow-hidden shadow-2xl">
      <div class="flex justify-between items-center mb-3 px-2">
        <span class="text-xs font-mono text-amber-400">VENTANAL ESTE C-07 (3,00×0,80m) · BANCADA DEKTON · GRAN ISLA 3,60×1,10m · PATIO OESTE</span>
        <span class="text-xs font-mono text-slate-500">Vector SVG ISO 129 (1:20)</span>
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
        <span class="text-xs font-mono text-amber-400">ALZADO FRENTE MIXTO CON VENTANAL (+0,95m a +1,75m) · ISLA 3,60m · CORTE LUZ ESTE-OESTE</span>
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
      <h3 class="text-lg font-bold text-amber-400 font-mono mb-4">☀️ Luz Solar & Ventanal Este</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Ventana Panorámica:</strong> 3,00 × 0,80 m (+0,95 a +1,75 m)</li>
        <li>• <strong class="text-white">Sol matinal:</strong> Luz suave de desayuno sobre la bancada</li>
        <li>• <strong class="text-white">Luz cruzada:</strong> Sol Este + Luz Oeste del Patio Claustro</li>
        <li>• <strong class="text-white">Coffee Station:</strong> Encimera Dekton con vistas al jardín</li>
        <li>• <strong class="text-white">Muebles altos:</strong> Suspendidos con iluminación LED</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-sky-400 font-mono mb-4">🏛️ Almacenaje Masivo Equilibrado</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Col 01:</strong> Frigorífico XXL integrable (todo frío)</li>
        <li>• <strong class="text-white">Col 02:</strong> Congelador vertical No-Frost</li>
        <li>• <strong class="text-white">Col 03:</strong> Torre Horno + Micro Bosch Serie 8</li>
        <li>• <strong class="text-white">Bancada Este:</strong> 3 gaveteros de 100 cm (caceroleros)</li>
        <li>• <strong class="text-white">Col 04:</strong> Cava vinos Santos 60 botellas vitrina</li>
        <li>• <strong class="text-white">Col 05:</strong> Despensa gavetas Legrabox + Vajillero</li>
        <li>• <strong class="text-white">Gran Isla:</strong> 3,60 × 1,10 m con caceroleros 90 cm</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-emerald-400 font-mono mb-4">🍽️ Comedor Principal (4,20 m)</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Superficie Comedor:</strong> 17,50 m² ($4,15 \times 4,20$ m)</li>
        <li>• <strong class="text-white">Mesa 10 Pax:</strong> 2,80 × 1,00 m roble macizo</li>
        <li>• <strong class="text-white">Paso Norte:</strong> 1,00 m libre hacia la isla de cocina</li>
        <li>• <strong class="text-white">Paso Sur:</strong> 1,00 m libre hacia el porche y jardín</li>
        <li>• <strong class="text-white">Transición:</strong> Cero tabiques, espacio continuo y abierto</li>
      </ul>
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
        document.getElementById('tab-planta').classList.add('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-elevaciones').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-resumen').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
      } else if (tab === 'elevaciones') {
        document.getElementById('tab-elevaciones').classList.add('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-planta').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-resumen').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
      } else {
        document.getElementById('tab-resumen').classList.add('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-planta').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
        document.getElementById('tab-elevaciones').classList.remove('border-amber-400', 'text-amber-400', 'bg-amber-950/20');
      }
    }
  </script>
</body>
</html>
"""

def main():
    print("Generando Plano K-01: Planta Cocina con Frente Mixto y Ventanal Panorámico Este (Opción A)...")
    planta_svg = build_cocina_planta_svg()
    with open("plano_cocina_planta_esquematica.svg", "w", encoding="utf-8") as f:
        f.write(planta_svg)
    print(" -> Guardado en plano_cocina_planta_esquematica.svg")

    print("Generando Plano K-02: Alzados con Ventanal Este y Sección Transversal...")
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
