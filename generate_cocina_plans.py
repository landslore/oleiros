#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Independientes de la Cocina y Despensa/Bodega Santos (Propuesta D - Hogar Oleiros v2)
- Plano K-01: Planta Arquitectónica Esquemática y de Distribución (Escala 1:20)
  * Cocina con Isla Santos Fine (15,20 m²)
  * Nueva Despensa Walk-in y Cava/Bodega Santos integrada (5,60 m²) tras traslado de lavandería a ala Oeste
- Plano K-02: Alzados Interiores y Cotas de Altura Ergonómica (Escala 1:20)
  * Alzado A: Frente Columnas Este de Cocina (H = 2,65 m)
  * Alzado B: Frente de Trabajo Isla Santos (H = 0,92 m)
  * Alzado C: Frente Barra Social hacia Patio Claustro con Taburetes (H = 0,92 m)
  * Alzado D: Interior Despensa Walk-in & Cava Bodega Santos (H = 2,65 m)
"""

import os
import math

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

      <!-- Rayado madera roble / muebles -->
      <pattern id="hatch-wood" width="30" height="6" patternUnits="userSpaceOnUse">
        <line x1="0" y1="6" x2="30" y2="6" stroke="#475569" stroke-width="0.4" opacity="0.6"/>
        <line x1="12" y1="0" x2="12" y2="6" stroke="#475569" stroke-width="0.3" opacity="0.5"/>
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
      <marker id="tick-rose" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
        <line x1="1.5" y1="6.5" x2="6.5" y2="1.5" stroke="#f43f5e" stroke-width="1.2"/>
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
      <linearGradient id="grad-bodega" x1="0" y1="0" x2="1" y2="1">
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
    Genera el Plano K-01: Planta Esquemática y de Distribución de Cocina + Despensa/Bodega Santos (1:20)
    Espacio total integrado:
    - Cocina Principal: 3,80 m x 4,60 m (15,20 m²)
    - Despensa Walk-in & Bodega Santos: 2,30 m x 2,45 m (5,60 m²)
    Total Suite Culinaria: 20,80 m²
    """
    W, H = 1950, 1150
    S = 125.0  # Escala 1m = 125px
    OX = 240.0  # X=0.00 en ventanal hacia el Patio Claustro
    OY = 210.0  # Y=0.00 en muro Norte

    def mx(val_m):
        return OX + val_m * S

    def my(val_m):
        return OY + val_m * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        # Bordes generales de plano
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1440" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-01 · PLANTA ESQUEMÁTICA Y DISTRIBUCIÓN: COCINA + DESPENSA/BODEGA SANTOS (1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Propuesta D v2 · Cocina Isla 15,20 m² + Despensa Walk-in Santos 5,60 m² (Total: 20,80 m²) · Circulaciones NHG</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1440" height="1020" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Geometría de los recintos:
    # Recinto 1: Cocina (X=0.00..3.80, Y=0.00..4.60)
    # Recinto 2: Despensa / Bodega Santos (X=3.80..6.10, Y=2.15..4.60)
    # Pared divisoria con Despensa en X=3.80, con puerta corredera pocket
    # Muro Norte Cocina en Y=0.00
    # Muro Norte Despensa en Y=2.15

    tw = 0.15 * S

    # 1. Muro Norte Cocina (X = -0.35..3.95, Y = 0.00)
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{4.30*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # 2. Muro Norte Despensa Santos (X = 3.80..6.25, Y = 2.15)
    out.append(f'<rect x="{mx(3.80):.1f}" y="{my(2.00):.1f}" width="{2.45*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # 3. Muro Este Despensa Santos (X = 6.10, Y = 2.00..4.75)
    out.append(f'<rect x="{mx(6.10):.1f}" y="{my(2.00):.1f}" width="{tw:.1f}" height="{2.75*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # 4. Tabique divisorio Cocina | Despensa Santos (X = 3.80, Y = 0.00..4.60)
    # Tramo norte (Y=0.00..2.15): Muro ciego
    out.append(f'<rect x="{mx(3.80):.1f}" y="{my(0.00):.1f}" width="{tw:.1f}" height="{2.15*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    # Tramo sur (Y=2.15..4.60): Tabique con hueco para puerta corredera escamoteable de 0,85 m
    out.append(f'<rect x="{mx(3.80):.1f}" y="{my(2.15):.1f}" width="{tw:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    # Puerta corredera oculta pocket en tabique (Y=3.55..4.45)
    out.append(f'<rect x="{mx(3.83):.1f}" y="{my(3.55):.1f}" width="{0.09*S:.1f}" height="{0.90*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{mx(3.87):.1f}" y1="{my(3.60):.1f}" x2="{mx(3.87):.1f}" y2="{my(4.40):.1f}" stroke="#38bdf8" stroke-width="2.0"/>')
    out.append(f'<text x="{mx(3.65):.1f}" y="{my(4.00):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" font-weight="700" transform="rotate(-90 {mx(3.65):.1f} {my(4.00):.1f})" text-anchor="middle">PASO POCKET A DESPENSA/BODEGA (0,85 m)</text>')

    # 5. Ventanal Oeste hacia Patio Claustro (X = 0.00, Y = 0.30 a 3.90 -> 3,60 m de hueco acristalado)
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{0.35*S:.1f}" height="{0.45*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(3.90):.1f}" width="{0.35*S:.1f}" height="{0.85*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.60*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<line x1="{mx(-0.02):.1f}" y1="{my(0.30):.1f}" x2="{mx(-0.02):.1f}" y2="{my(2.10):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<line x1="{mx(0.02):.1f}" y1="{my(2.05):.1f}" x2="{mx(0.02):.1f}" y2="{my(3.90):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<text x="{mx(-0.10):.1f}" y="{my(2.10):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" transform="rotate(-90 {mx(-0.10):.1f} {my(2.10):.1f})" text-anchor="middle">VENTANAL CORREDERO PATIO CLAUSTRO (3,60×2,65 m)</text>')

    # Pavimento interior de la Cocina (Porcelánico técnico C2 gran formato)
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{3.80*S:.1f}" height="{4.60*S:.1f}" fill="#0f172a" opacity="0.85"/>')

    # Pavimento interior de la Despensa y Bodega Santos
    out.append(f'<rect x="{mx(3.80):.1f}" y="{my(2.15):.1f}" width="{2.30*S:.1f}" height="{2.45*S:.1f}" fill="#0c1222" opacity="0.95"/>')

    # Círculo NHG de habitabilidad en cocina Ø1,50 m
    out.append(f'<circle cx="{mx(2.10):.1f}" cy="{my(2.30):.1f}" r="{0.75*S:.1f}" fill="#38bdf8" fill-opacity="0.04" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(2.10):.1f}" y="{my(2.34):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" text-anchor="middle">CIRCULACIÓN LIBRE Ø1,50 m (NHG)</text>')

    # --------------------------------------------------------------------------
    # FRENTE DE COLUMNAS ESTE DE COCINA (X = 3.15 a 3.80 -> 3,60 m de longitud)
    # --------------------------------------------------------------------------
    fc_x = mx(3.15)
    fc_y = my(0.30)
    fc_w = 0.65 * S
    fc_h = 3.60 * S
    out.append(f'<rect x="{fc_x:.1f}" y="{fc_y:.1f}" width="{fc_w:.1f}" height="{fc_h:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.4"/>')

    modulos_col = [
        ("COL 01 (60 cm)", "FRIGORÍFICO XXL", "Integrado 1-puerta", "#38bdf8"),
        ("COL 02 (60 cm)", "CONGELADOR", "No-Frost vertical", "#38bdf8"),
        ("COL 03 (60 cm)", "TORRE HORNO + MIC", "Bosch Serie 8", "#f59e0b"),
        ("COL 04 (60 cm)", "DESAYUNADOR (A)", "Puerta escamoteable", "#10b981"),
        ("COL 05 (60 cm)", "DESAYUNADOR (B)", "Encimera café/tost.", "#10b981"),
        ("COL 06 (60 cm)", "DESPENSERO DÍA", "Gavetas interiores", "#cbd5e1"),
    ]
    for idx, (cod, tit, sub, col) in enumerate(modulos_col):
        m_top = fc_y + idx * 0.60 * S
        out.append(f'<line x1="{fc_x:.1f}" y1="{m_top:.1f}" x2="{fc_x+fc_w:.1f}" y2="{m_top:.1f}" stroke="#475569" stroke-width="0.9"/>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+18:.1f}" fill="{col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{cod}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+36:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{tit}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+52:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{sub}</text>')

    # --------------------------------------------------------------------------
    # ISLA CENTRAL SANTOS FINE (X = 1.15 a 2.15 -> 2,80 x 1,00 m)
    # --------------------------------------------------------------------------
    isla_x = mx(1.15)
    isla_y = my(0.70)
    isla_w = 1.00 * S
    isla_h = 2.80 * S

    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="1.8"/>')
    out.append(f'<rect x="{isla_x+3:.1f}" y="{isla_y+3:.1f}" width="{isla_w-6:.1f}" height="{isla_h-6:.1f}" fill="url(#grad-dekton)" opacity="0.35" stroke="#475569" stroke-width="0.8"/>')

    # Línea barra snack volada (35 cm Oeste)
    barra_split_x = isla_x + 0.35 * S
    out.append(f'<line x1="{barra_split_x:.1f}" y1="{isla_y:.1f}" x2="{barra_split_x:.1f}" y2="{isla_y+isla_h:.1f}" stroke="#38bdf8" stroke-width="0.9" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{isla_x+16:.1f}" y="{isla_y+isla_h/2:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700" transform="rotate(-90 {isla_x+16:.1f} {isla_y+isla_h/2:.1f})" text-anchor="middle">BARRA SNACK VOLADA (0,35 m)</text>')

    # 4 Taburetes altos orientados al Patio Claustro
    for ty in [1.05, 1.70, 2.35, 3.00]:
        st_cx = isla_x - 0.22 * S
        st_cy = my(ty)
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.18*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.08*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.6"/>')

    # Fregadero bajo encimera 70 cm
    sink_w = 0.50 * S
    sink_h = 0.70 * S
    sink_x = isla_x + 0.42 * S
    sink_y = isla_y + 0.35 * S
    out.append(f'<rect x="{sink_x:.1f}" y="{sink_y:.1f}" width="{sink_w:.1f}" height="{sink_h:.1f}" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<rect x="{sink_x+4:.1f}" y="{sink_y+4:.1f}" width="{sink_w-8:.1f}" height="{sink_h-8:.1f}" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(f'<circle cx="{sink_x+sink_w/2:.1f}" cy="{sink_y+sink_h/2:.1f}" r="5.5" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.1"/>')
    out.append(f'<line x1="{sink_x+sink_w/2:.1f}" y1="{sink_y+sink_h/2:.1f}" x2="{sink_x+sink_w/2-10:.1f}" y2="{sink_y+sink_h/2:.1f}" stroke="#f8fafc" stroke-width="1.5"/>')
    out.append(f'<text x="{sink_x+sink_w/2:.1f}" y="{sink_y+sink_h+16:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">FREGADERO 70×45 cm</text>')

    # Placa Bora Pure 80 cm
    bora_w = 0.52 * S
    bora_h = 0.82 * S
    bora_x = isla_x + 0.40 * S
    bora_y = isla_y + 1.55 * S
    out.append(f'<rect x="{bora_x:.1f}" y="{bora_y:.1f}" width="{bora_w:.1f}" height="{bora_h:.1f}" rx="2" fill="#18181b" stroke="#f59e0b" stroke-width="1.4"/>')
    for zx, zy in [(bora_x+15, bora_y+20), (bora_x+bora_w-15, bora_y+20), (bora_x+15, bora_y+bora_h-20), (bora_x+bora_w-15, bora_y+bora_h-20)]:
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="11" fill="none" stroke="#f59e0b" stroke-width="0.9"/>')
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="3" fill="#f59e0b"/>')
    out.append(f'<rect x="{bora_x+bora_w/2-8:.1f}" y="{bora_y+bora_h/2-16:.1f}" width="16" height="32" rx="3" fill="#0f172a" stroke="#06b6d4" stroke-width="1.2"/>')
    out.append(f'<circle cx="{bora_x+bora_w/2:.1f}" cy="{bora_y+bora_h/2:.1f}" r="5" fill="none" stroke="#06b6d4" stroke-width="1.0"/>')
    out.append(f'<text x="{bora_x+bora_w/2:.1f}" y="{bora_y+bora_h+16:.1f}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">PLACA BORA PURE 80 cm</text>')

    # Lavavajillas panelado integrado 60 cm
    out.append(f'<text x="{isla_x+0.68*S:.1f}" y="{isla_y+1.28*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">[ LAVAVAJILLAS 60 cm ]</text>')

    # Rótulo identificativo de Cocina
    out.append(f'<rect x="{mx(1.00):.1f}" y="{my(3.85):.1f}" width="160" height="42" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{mx(1.00)+80:.1f}" y="{my(3.85)+17:.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">[E-08] COCINA ISLA SANTOS</text>')
    out.append(f'<text x="{mx(1.00)+80:.1f}" y="{my(3.85)+32:.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" text-anchor="middle">S.Útil: 15,20 m² · Z=±0,00m</text>')

    # --------------------------------------------------------------------------
    # 06B. NUEVA DESPENSA WALK-IN & CAVA/BODEGA SANTOS (5,60 m²)
    # Dimensiones: 2,30 m (X=3.80..6.10) x 2,45 m (Y=2.15..4.60)
    # --------------------------------------------------------------------------
    # 1. Cava de Vinos Climatizada Santos (Módulo 65x65cm con frontal acristalado negro):
    cava_x = mx(3.95)
    cava_y = my(2.30)
    cava_w = 0.65 * S
    cava_h = 0.65 * S
    out.append(f'<rect x="{cava_x:.1f}" y="{cava_y:.1f}" width="{cava_w:.1f}" height="{cava_h:.1f}" fill="url(#grad-bodega)" stroke="#f59e0b" stroke-width="1.3"/>')
    # Rejilla botellero interior
    for by_o in [15, 30, 45, 60]:
        out.append(f'<line x1="{cava_x+8:.1f}" y1="{cava_y+by_o:.1f}" x2="{cava_x+cava_w-8:.1f}" y2="{cava_y+by_o:.1f}" stroke="#f59e0b" stroke-width="0.8" opacity="0.6"/>')
    out.append(f'<text x="{cava_x+cava_w/2:.1f}" y="{cava_y+cava_h/2+3:.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">CAVA VINOS</text>')
    out.append(f'<text x="{cava_x+cava_w/2:.1f}" y="{cava_y+cava_h/2+15:.1f}" fill="#fbbf24" font-family="monospace" font-size="5.5" text-anchor="middle">60 Botellas · Multi-Tª</text>')

    # 2. Bancada Auxiliar "Back Kitchen" / Pequeño Electrodoméstico (fondo 60cm, de X=4.60..5.95 en Y=2.30..2.90)
    bk_x = mx(4.60)
    bk_y = my(2.30)
    bk_w = 1.35 * S
    bk_h = 0.60 * S
    out.append(f'<rect x="{bk_x:.1f}" y="{bk_y:.1f}" width="{bk_w:.1f}" height="{bk_h:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    out.append(f'<text x="{bk_x+bk_w/2:.1f}" y="{bk_y+20:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">BANCADA AUXILIAR "BACK KITCHEN"</text>')
    out.append(f'<text x="{bk_x+bk_w/2:.1f}" y="{bk_y+36:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Robots de Cocina · Thermomix · AirFryer · 4×C5</text>')

    # 3. Estanterías modulares perimetrales Santos en L / U (fondo 40 cm):
    # Frente Este (fondo 40 cm, Y=3.00..4.45)
    est_e_x = mx(5.65)
    est_e_y = my(3.00)
    est_e_w = 0.40 * S
    est_e_h = 1.45 * S
    out.append(f'<rect x="{est_e_x:.1f}" y="{est_e_y:.1f}" width="{est_e_w:.1f}" height="{est_e_h:.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.9"/>')
    for ey in [my(3.35), my(3.70), my(4.05)]:
        out.append(f'<line x1="{est_e_x:.1f}" y1="{ey:.1f}" x2="{est_e_x+est_e_w:.1f}" y2="{ey:.1f}" stroke="#475569" stroke-width="0.8"/>')
    out.append(f'<text x="{est_e_x+est_e_w/2:.1f}" y="{est_e_y+est_e_h/2:.1f}" fill="#cbd5e1" font-family="monospace" font-size="6.0" font-weight="700" transform="rotate(-90 {est_e_x+est_e_w/2:.1f} {est_e_y+est_e_h/2:.1f})" text-anchor="middle">ESTANTES VÍVERES Y VAJILLA (40 cm)</text>')

    # Frente Sur Despensa (fondo 40 cm, X=4.10..5.65, Y=4.15..4.55)
    est_s_x = mx(4.10)
    est_s_y = my(4.15)
    est_s_w = 1.55 * S
    est_s_h = 0.40 * S
    out.append(f'<rect x="{est_s_x:.1f}" y="{est_s_y:.1f}" width="{est_s_w:.1f}" height="{est_s_h:.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.9"/>')
    out.append(f'<text x="{est_s_x+est_s_w/2:.1f}" y="{est_s_y+24:.1f}" fill="#cbd5e1" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">DESPENSA SANTOS (40 cm)</text>')

    # Rótulo de estancia Despensa / Bodega
    out.append(f'<rect x="{mx(4.15):.1f}" y="{my(3.20):.1f}" width="150" height="42" rx="4" fill="#0b1120" stroke="#f59e0b" stroke-width="1.0"/>')
    out.append(f'<text x="{mx(4.15)+75:.1f}" y="{my(3.20)+17:.1f}" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">[E-08B] DESPENSA Y BODEGA</text>')
    out.append(f'<text x="{mx(4.15)+75:.1f}" y="{my(3.20)+32:.1f}" fill="#fde68a" font-family="monospace" font-size="6.8" text-anchor="middle">S.Útil: 5,60 m² · Cava + Víveres</text>')

    # --------------------------------------------------------------------------
    # COTAS GENERALES ISO 129
    # --------------------------------------------------------------------------
    # Cotas Horizontales Cocina:
    out.append(dim_h(mx(0.00), isla_x, my(0.15), 0, "1,15 m (Paso Libre Patio)", "#38bdf8", font_size=7.2))
    out.append(dim_h(isla_x, isla_x + isla_w, my(0.15), 0, "1,00 m (Isla)", "#f8fafc", font_size=7.2))
    out.append(dim_h(isla_x + isla_w, fc_x, my(0.15), 0, "1,00 m (Paso Culinario)", "#10b981", marker="tick-emerald", font_size=7.2))
    out.append(dim_h(fc_x, mx(3.80), my(0.15), 0, "0,65 m", "#94a3b8", font_size=7.0))
    out.append(dim_h(mx(0.00), mx(3.80), my(-0.05), -22, "3,80 m (Ancho Cocina)", "#38bdf8", font_size=8.5))

    # Cotas Horizontales Despensa / Bodega:
    out.append(dim_h(mx(3.80), mx(6.10), my(2.00), -20, "2,30 m (Ancho Despensa / Bodega)", "#f59e0b", marker="tick-amber", font_size=8.0))

    # Cota Horizontal Total Suite Culinaria:
    out.append(dim_h(mx(0.00), mx(6.10), my(-0.05), -48, "6,10 m (ANCHO TOTAL SUITE CULINARIA · 20,80 m²)", "#f8fafc", font_size=9.0))

    # Cotas Verticales Cocina:
    out.append(dim_v(my(0.00), my(4.60), mx(0.00), -55, "4,60 m (Longitud Cocina)", "#38bdf8", font_size=8.5))
    out.append(dim_v(isla_y, isla_y + isla_h, isla_x, -35, "2,80 m (Longitud Isla)", "#f8fafc", font_size=8.0))

    # Cotas Verticales Despensa / Bodega:
    out.append(dim_v(my(2.15), my(4.60), mx(6.10), 30, "2,45 m (Fondo Despensa)", "#f59e0b", marker="tick-amber", font_size=8.0))

    # --------------------------------------------------------------------------
    # BANDA DERECHA: MEMORIA TÉCNICA V2 Y ESPECIFICACIONES
    # --------------------------------------------------------------------------
    rx = 1500
    out.append(f'<rect x="{rx}" y="30" width="420" height="1070" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="400" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">MEMORIA SUITE COCINA & BODEGA V2</text>')

    specs = [
        ("1. ZONIFICACIÓN TRAS TRASLADO LAVANDERÍA", "#38bdf8", [
            ("Lavandería reubicada", "Trasladada a Ala Oeste (11,60 m² + Velux)"),
            ("Espacio liberado Este", "Convertido en Despensa Walk-in Santos"),
            ("Superficie Total Suite", "15,20 m² (Cocina) + 5,60 m² (Bodega) = 20,80 m²"),
            ("Concepto 'Back Kitchen'", "Electrodomésticos ruidosos fuera de la isla"),
        ]),
        ("2. EQUIPAMIENTO DESPENSA / BODEGA", "#f59e0b", [
            ("Cava de vinos climatizada", "Santos integrada, 60 botellas, doble zona"),
            ("Bancada auxiliar", "Robots (Thermomix, AirFryer, batidora)"),
            ("Estanterías modulares", "Fondo 40 cm para víveres secos y vajilla"),
            ("Puerta de acceso", "Corredera pocket 0,85 m oculta en tabique"),
        ]),
        ("3. COCINA ISLA SANTOS FINE", "#10b981", [
            ("Isla de trabajo y social", "2,80 × 1,00 m con encimera Dekton Kelya"),
            ("Placa de cocción", "Bora Pure 80 cm con extractor downdraft"),
            ("Fregadero y lavavajillas", "Seno 70 cm + LVV panelado integrado"),
            ("Barra de desayuno", "4 taburetes orientados al Patio Claustro"),
            ("Frente Columnas Este", "3,60 m (Frigo XXL + Congelador + Horno/Mic)"),
        ]),
        ("4. CIRCULACIONES Y ERGONOMÍA (NHG)", "#cbd5e1", [
            ("Paso Isla - Patio Claustro", "1,15 m (holgura generosa con taburetes)"),
            ("Paso Isla - Frente Columnas", "1,00 m (apertura cajones y hornos)"),
            ("Giro libre reglamentario", "Ø1,50 m cumpliendo estrictamente NHG"),
        ]),
        ("5. FASE 2: DETALLE DE INSTALACIONES", "#f43f5e", [
            ("Enchufes y Fuerza", "Torre Twist isla, 4 tomas C5 en bancada despensa"),
            ("Líneas dedicadas", "C3 Bora (25A), C4 frigo/cava/LVV (16A)"),
            ("Iluminación IES", "Carril magnético isla + LED 3000K en estantes"),
        ]),
    ]

    sy = 85
    for cat_title, cat_col, rows in specs:
        out.append(f'<text x="{rx+16}" y="{sy}" fill="{cat_col}" font-family="monospace" font-size="7.5" font-weight="700">{cat_title}</text>')
        out.append(f'<line x1="{rx+16}" y1="{sy+4}" x2="{rx+404}" y2="{sy+4}" stroke="{cat_col}" stroke-width="0.7" opacity="0.6"/>')
        sy += 16
        for k, v in rows:
            out.append(f'<text x="{rx+20}" y="{sy}" fill="#f1f5f9" font-family="monospace" font-size="6.5" font-weight="700">• {k}:</text>')
            out.append(f'<text x="{rx+28}" y="{sy+11}" fill="#94a3b8" font-family="monospace" font-size="6.0">{v}</text>')
            sy += 21
        sy += 8

    out.append('</svg>')
    return "\n".join(out)


def build_cocina_elevaciones_svg():
    """
    Genera el Plano K-02: Alzados Interiores y Cotas de Altura Ergonómica (1:20)
    - Alzado A: Frente Columnas Este de Cocina (L=3,60m, H=2,65m)
    - Alzado B: Frente Isla Santos - Lado de Trabajo Este (L=2,80m, H=0,92m)
    - Alzado C: Frente Isla Santos - Lado Barra Oeste / Taburetes Patio (L=2,80m, H=0,92m)
    - Alzado D: Interior Despensa Walk-in & Bodega Santos (L=2,30m, H=2,65m) con Cava de Vinos y Estantes
    """
    W, H = 1950, 1420
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1440" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-02 · ALZADOS Y COTAS DE ALTURA: COCINA E INTERIOR DESPENSA/BODEGA (1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Propuesta D v2 · Frente Columnas Este · Isla Santos Fine · Cava y Estantes Bodega · Cotas sobre Suelo Terminado ±0,00m</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1440" height="1310" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # ==========================================================================
    # SECCIÓN 1: ALZADO A - FRENTE DE COLUMNAS ESTE (L = 3,60 m, H = 2,65 m)
    # ==========================================================================
    S1 = 170.0
    A_OX = 160.0
    A_GROUND_Y = 460.0

    def ax(val_m):
        return A_OX + val_m * S1

    def ay(val_h_m):
        return A_GROUND_Y - val_h_m * S1

    # Línea de Suelo Terminado (Cota ±0,00 m)
    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{A_GROUND_Y:.1f}" x2="{ax(3.9):.1f}" y2="{A_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{A_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m (SUELO TERMINADO)</text>')

    # Línea de Falso Techo (+2,65 m)
    ceil_y = ay(2.65)
    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{ceil_y:.1f}" x2="{ax(3.9):.1f}" y2="{ceil_y:.1f}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{ceil_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">FALSO TECHO +2,65 m</text>')

    # Título Alzado A
    out.append(f'<rect x="{ax(0.0):.1f}" y="{ceil_y-32:.1f}" width="420" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{ax(0.0)+10:.1f}" y="{ceil_y-17:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO A · FRENTE DE COLUMNAS ESTE (L = 3,60 m · H = 2,65 m)</text>')

    # Zócalo inferior (h = 0,08 m) retranqueado
    zoc_y = ay(0.08)
    out.append(f'<rect x="{ax(0.0):.1f}" y="{zoc_y:.1f}" width="{3.60*S1:.1f}" height="{0.08*S1:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')
    out.append(f'<text x="{ax(1.8):.1f}" y="{A_GROUND_Y-4:.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ZÓCALO RETRANQUEADO h = 8 cm (CON REJILLA VENTILACIÓN FRIGO)</text>')

    cols = [
        ("COL 01", "FRIGORÍFICO XXL", "1-puerta integrado", 0.60),
        ("COL 02", "CONGELADOR", "No-Frost vertical", 0.60),
        ("COL 03", "TORRE HORNO/MIC", "Bosch Serie 8", 0.60),
        ("COL 04-05", "DESAYUNADOR POCKET (120 cm)", "Puertas escamoteables", 1.20),
        ("COL 06", "DESPENSERO DÍA", "Gavetas interiores", 0.60),
    ]

    cur_x = 0.0
    for cid, ctit, csub, cw in cols:
        cx1 = ax(cur_x)
        cw_px = cw * S1
        out.append(f'<rect x="{cx1:.1f}" y="{ay(2.20):.1f}" width="{cw_px:.1f}" height="{2.12*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if "FRIGORÍFICO" in ctit or "CONGELADOR" in ctit:
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.86):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<line x1="{cx1+cw_px-4:.1f}" y1="{ay(0.15):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(1.80):.1f}" stroke="#38bdf8" stroke-width="1.5"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.00):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">{ctit}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.85):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{csub}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(2.03):.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ALTILLO</text>')

        elif "TORRE" in ctit:
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(0.70):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(0.70):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">GAVETA INFERIOR</text>')
            # Horno Bosch Serie 8 (+0,70 a +1,30m)
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.30):.1f}" width="{cw_px-8:.1f}" height="{0.60*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+12:.1f}" y="{ay(1.24):.1f}" width="{cw_px-24:.1f}" height="{0.42*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<circle cx="{cx1+cw_px/2:.1f}" cy="{ay(1.27):.1f}" r="4" fill="none" stroke="#f59e0b" stroke-width="1.0"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.96):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">HORNO PIROLÍTICO</text>')
            # Microondas (+1,30 a +1,75m)
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.75):.1f}" width="{cw_px-8:.1f}" height="{0.45*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+12:.1f}" y="{ay(1.71):.1f}" width="{cw_px-24:.1f}" height="{0.30*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.50):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MICROONDAS / VAPOR</text>')
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.75):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.75):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.98):.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ALTILLO</text>')

        elif "DESAYUNADOR" in ctit:
            mid_pocket = cx1 + 0.60 * S1
            out.append(f'<line x1="{mid_pocket:.1f}" y1="{ay(2.20):.1f}" x2="{mid_pocket:.1f}" y2="{ay(0.08):.1f}" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,3"/>')
            out.append(f'<line x1="{cx1+4:.1f}" y1="{ay(0.92):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(0.92):.1f}" stroke="#10b981" stroke-width="1.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.95):.1f}" fill="#10b981" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA INTERIOR DEKTON (+0,92 m)</text>')
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.45):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.45):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.80):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.80):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.40):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">MUEBLE DESAYUNADOR POCKET (120 cm)</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.25):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Cafetera Espresso · Molinillo · Tostadora · LED integrado</text>')
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(0.50):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(0.50):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.28):.1f}" fill="#64748b" font-family="monospace" font-size="5.8" text-anchor="middle">GAVETAS DESPENSA / MENAJE</text>')

        elif "DESPENSERO" in ctit:
            for gy in [0.45, 0.85, 1.25, 1.65]:
                out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(gy):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(gy):.1f}" stroke="#475569" stroke-width="0.6" stroke-dasharray="3,2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.05):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">DESPENSERO DÍA</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.90):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Gavetas Blum Legrabox</text>')
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.86):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')

        cur_x += cw

    # Remate Superior ciego a falso techo (+2,20 a +2,65m)
    faja_y = ay(2.65)
    faja_h = 0.45 * S1
    out.append(f'<rect x="{ax(0.0):.1f}" y="{faja_y:.1f}" width="{3.60*S1:.1f}" height="{faja_h:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')
    out.append(f'<text x="{ax(1.8):.1f}" y="{faja_y+faja_h/2+3:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">REMATADO ENRASADO A FALSO TECHO (+2,20 m a +2,65 m)</text>')

    # Cotas de Altura del Alzado A (Derecha):
    cx_dim = ax(3.60) + 25
    out.append(dim_v(ay(0.00), ay(0.08), cx_dim, 0, "+0,08 m (Zócalo)", "#94a3b8", font_size=6.8))
    out.append(dim_v(ay(0.08), ay(0.92), cx_dim, 0, "+0,92 m (Bancada Desayunador / Base Horno)", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_v(ay(0.92), ay(1.30), cx_dim, 0, "+1,30 m (Eje Visual Horno)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.30), ay(1.75), cx_dim, 0, "+1,75 m (Microondas)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.75), ay(2.20), cx_dim, 0, "+2,20 m (Coronación)", "#cbd5e1", font_size=6.8))
    out.append(dim_v(ay(2.20), ay(2.65), cx_dim, 0, "+2,65 m (Techo)", "#38bdf8", font_size=7.2))

    # ==========================================================================
    # SECCIÓN 2: ALZADO B - ELEVACIÓN ISLA SANTOS FINE (L = 2,80 m, H = 0,92 m)
    # Lado de Trabajo (Vista Este)
    # ==========================================================================
    S2 = 180.0
    B_OX = 160.0
    B_GROUND_Y = 760.0

    def bx(val_m):
        return B_OX + val_m * S2

    def by(val_h_m):
        return B_GROUND_Y - val_h_m * S2

    out.append(f'<line x1="{bx(-0.3):.1f}" y1="{B_GROUND_Y:.1f}" x2="{bx(3.1):.1f}" y2="{B_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{bx(-0.35):.1f}" y="{B_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(1.20):.1f}" width="460" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{bx(0.0)+10:.1f}" y="{by(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO B · ISLA CENTRAL SANTOS FINE — FRENTE DE TRABAJO (2,80×0,92 m)</text>')

    # Zócalo isla retraído (h = 0,08 m)
    out.append(f'<rect x="{bx(0.05):.1f}" y="{by(0.08):.1f}" width="{2.70*S2:.1f}" height="{0.08*S2:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')

    isla_mods = [
        ("MÓD. FREGADERO (80 cm)", "Gaveta Cubos Reciclaje", 0.80, "#38bdf8"),
        ("LAVAVAJILLAS (60 cm)", "Totalmente Integrado", 0.60, "#38bdf8"),
        ("MÓD. BORA PURE (90 cm)", "2 Caceroleros + Cubertero", 0.90, "#f59e0b"),
        ("GAVETERO AUX. (50 cm)", "Extracción Total Blum", 0.50, "#cbd5e1"),
    ]

    ix_cur = 0.0
    for im_tit, im_sub, im_w, im_col in isla_mods:
        im_x1 = bx(ix_cur)
        im_w_px = im_w * S2
        out.append(f'<rect x="{im_x1:.1f}" y="{by(0.90):.1f}" width="{im_w_px:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if "FREGADERO" in im_tit:
            out.append(f'<rect x="{im_x1:.1f}" y="{by(0.90):.1f}" width="{im_w_px:.1f}" height="6" fill="#0f172a"/>')
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            out.append(f'<path d="M {im_x1+im_w_px/2} {by(0.92)} L {im_x1+im_w_px/2} {by(1.30)} Q {im_x1+im_w_px/2} {by(1.40)} {im_x1+im_w_px/2-25} {by(1.38)} L {im_x1+im_w_px/2-25} {by(1.32)}" fill="none" stroke="#38bdf8" stroke-width="3.0"/>')

        elif "LAVAVAJILLAS" in im_tit:
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.52):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            out.append(f'<circle cx="{im_x1+im_w_px/2:.1f}" cy="{by(0.85):.1f}" r="3" fill="#10b981"/>')

        elif "BORA" in im_tit:
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            out.append(f'<rect x="{im_x1+15:.1f}" y="{by(0.925):.1f}" width="{im_w_px-30:.1f}" height="6" fill="#18181b" stroke="#f59e0b" stroke-width="1.1"/>')

        elif "GAVETERO" in im_tit:
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.64):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.64):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.36):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.36):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.77):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CUBIERTOS</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.50):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CACEROLERO</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.18):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CACEROLERO</text>')

        ix_cur += im_w

    # Encimera Dekton 20 mm
    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(0.92):.1f}" width="{2.80*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')
    out.append(f'<text x="{bx(1.4):.1f}" y="{by(0.92)-6:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA DEKTON KELYA 20 mm (COTA DE TRABAJO +0,92 m)</text>')

    bx_dim = bx(2.80) + 25
    out.append(dim_v(by(0.00), by(0.08), bx_dim, 0, "+0,08 m", "#94a3b8", font_size=6.8))
    out.append(dim_v(by(0.08), by(0.90), bx_dim, 0, "0,82 m Muebles Santos", "#cbd5e1", font_size=6.8))
    out.append(dim_v(by(0.00), by(0.92), bx_dim + 35, 0, "+0,92 m COTA ENCIMERA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # SECCIÓN 3: ALZADO C - ELEVACIÓN ISLA LADO BARRA SOCIAL HACIA PATIO CLAUSTRO
    # ==========================================================================
    C_OX = 160.0
    C_GROUND_Y = 1060.0

    def cx(val_m):
        return C_OX + val_m * S2

    def cy(val_h_m):
        return C_GROUND_Y - val_h_m * S2

    out.append(f'<line x1="{cx(-0.3):.1f}" y1="{C_GROUND_Y:.1f}" x2="{cx(3.1):.1f}" y2="{C_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{cx(-0.35):.1f}" y="{C_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(1.20):.1f}" width="460" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{cx(0.0)+10:.1f}" y="{cy(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO C · ISLA SANTOS — FRENTE BARRA SOCIAL Y TABURETES (2,80×0,92 m)</text>')

    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(0.90):.1f}" width="{2.80*S2:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    out.append(f'<rect x="{cx(-0.05):.1f}" y="{cy(0.92):.1f}" width="{2.90*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')

    for st_x_m in [0.35, 1.05, 1.75, 2.45]:
        tx = cx(st_x_m)
        out.append(f'<line x1="{tx-16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx-10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        out.append(f'<line x1="{tx+16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx+10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        out.append(f'<line x1="{tx-14:.1f}" y1="{cy(0.25):.1f}" x2="{tx+14:.1f}" y2="{cy(0.25):.1f}" stroke="#94a3b8" stroke-width="1.5"/>')
        out.append(f'<rect x="{tx-18:.1f}" y="{cy(0.67):.1f}" width="36" height="6" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.0"/>')
        out.append(f'<line x1="{tx-12:.1f}" y1="{cy(0.67):.1f}" x2="{tx-12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<line x1="{tx+12:.1f}" y1="{cy(0.67):.1f}" x2="{tx+12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<rect x="{tx-16:.1f}" y="{cy(0.84):.1f}" width="32" height="6" rx="2" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')

    out.append(f'<text x="{cx(1.4):.1f}" y="{cy(0.50):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">VOLADIZO LIBRE 35 cm PARA PIERNAS (HUECO ERGONÓMICO)</text>')

    out.append(dim_v(cy(0.00), cy(0.65), cx(2.85), 15, "+0,65 m (Asiento Taburete)", "#38bdf8", font_size=6.8))
    out.append(dim_v(cy(0.65), cy(0.92), cx(2.85), 15, "0,27 m Holgura Piernas", "#10b981", marker="tick-emerald", font_size=6.5))

    # ==========================================================================
    # SECCIÓN 4: ALZADO D - NUEVO! INTERIOR DESPENSA WALK-IN & BODEGA SANTOS
    # L = 2,30 m, H = 2,65 m (Cava de Vinos + Bancada Back Kitchen + Estantes)
    # ==========================================================================
    D_OX = 160.0
    D_GROUND_Y = 1360.0

    def dx(val_m):
        return D_OX + val_m * S2

    def dy(val_h_m):
        return D_GROUND_Y - val_h_m * S2

    out.append(f'<line x1="{dx(-0.3):.1f}" y1="{D_GROUND_Y:.1f}" x2="{dx(2.6):.1f}" y2="{D_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{dx(-0.35):.1f}" y="{D_GROUND_Y+4:.1f}" fill="#f59e0b" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    d_ceil_y = dy(2.65)
    out.append(f'<line x1="{dx(-0.3):.1f}" y1="{d_ceil_y:.1f}" x2="{dx(2.6):.1f}" y2="{d_ceil_y:.1f}" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{dx(-0.35):.1f}" y="{d_ceil_y+4:.1f}" fill="#f59e0b" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">FALSO TECHO +2,65 m</text>')

    out.append(f'<rect x="{dx(0.0):.1f}" y="{d_ceil_y-32:.1f}" width="480" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{dx(0.0)+10:.1f}" y="{d_ceil_y-17:.1f}" fill="#f59e0b" font-family="monospace" font-size="9.0" font-weight="700">ALZADO D · INTERIOR DESPENSA WALK-IN & CAVA BODEGA SANTOS (2,30×2,65 m)</text>')

    # 1. Módulo Cava de Vinos Climatizada (X=0.00..0.70m, H=2,20m)
    cava_w_px = 0.70 * S2
    out.append(f'<rect x="{dx(0.0):.1f}" y="{dy(2.20):.1f}" width="{cava_w_px:.1f}" height="{2.12*S2:.1f}" fill="url(#grad-bodega)" stroke="#f59e0b" stroke-width="1.4"/>')
    # Vidrio oscurecido con estantes de madera para vino
    for vy in [0.35, 0.65, 0.95, 1.25, 1.55, 1.85]:
        out.append(f'<line x1="{dx(0.0)+6:.1f}" y1="{dy(vy):.1f}" x2="{dx(0.0)+cava_w_px-6:.1f}" y2="{dy(vy):.1f}" stroke="#f59e0b" stroke-width="1.1" opacity="0.7"/>')
        out.append(f'<circle cx="{dx(0.0)+20:.1f}" cy="{dy(vy)-6:.1f}" r="4" fill="#fbbf24" opacity="0.8"/>')
        out.append(f'<circle cx="{dx(0.0)+40:.1f}" cy="{dy(vy)-6:.1f}" r="4" fill="#fbbf24" opacity="0.8"/>')
        out.append(f'<circle cx="{dx(0.0)+60:.1f}" cy="{dy(vy)-6:.1f}" r="4" fill="#fbbf24" opacity="0.8"/>')
    out.append(f'<text x="{dx(0.0)+cava_w_px/2:.1f}" y="{dy(2.05):.1f}" fill="#fde68a" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">CAVA SANTOS CLIMATIZADA</text>')
    out.append(f'<text x="{dx(0.0)+cava_w_px/2:.1f}" y="{dy(0.18):.1f}" fill="#fde68a" font-family="monospace" font-size="6.0" text-anchor="middle">Capacidad: 60 Botellas</text>')

    # 2. Bancada Auxiliar "Back Kitchen" (X=0.70..1.70m -> 1,00m):
    # Muebles bajos con gavetas hasta +0,90m, encimera a +0,92m
    bk_w_px = 1.00 * S2
    out.append(f'<rect x="{dx(0.70):.1f}" y="{dy(0.90):.1f}" width="{bk_w_px:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    out.append(f'<line x1="{dx(0.70):.1f}" y1="{dy(0.48):.1f}" x2="{dx(0.70)+bk_w_px:.1f}" y2="{dy(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
    out.append(f'<rect x="{dx(0.70):.1f}" y="{dy(0.92):.1f}" width="{bk_w_px:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<text x="{dx(0.70)+bk_w_px/2:.1f}" y="{dy(0.68):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">BANCADA "BACK KITCHEN"</text>')
    out.append(f'<text x="{dx(0.70)+bk_w_px/2:.1f}" y="{dy(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Gavetas menaje / vajilla de fiesta</text>')
    # Robots de cocina en bancada (Thermomix + Airfryer + 4 enchufes C5 a +1,10m)
    out.append(f'<rect x="{dx(0.85):.1f}" y="{dy(1.22):.1f}" width="28" height="32" rx="3" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.0"/>')
    out.append(f'<text x="{dx(0.85)+14:.1f}" y="{dy(1.05):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.2" text-anchor="middle">ROBOT</text>')
    # Tomas de corriente C5 a +1,10m
    out.append(f'<circle cx="{dx(1.30):.1f}" cy="{dy(1.10):.1f}" r="4.5" fill="#f59e0b" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<text x="{dx(1.30)+18:.1f}" y="{dy(1.10)+3:.1f}" fill="#f59e0b" font-family="monospace" font-size="5.5" font-weight="700">4×C5 (16A)</text>')
    # Estantes superiores con iluminación LED a +1,45m y +1,85m
    out.append(f'<line x1="{dx(0.70)+6:.1f}" y1="{dy(1.45):.1f}" x2="{dx(0.70)+bk_w_px-6:.1f}" y2="{dy(1.45):.1f}" stroke="#cbd5e1" stroke-width="1.5"/>')
    out.append(f'<line x1="{dx(0.70)+6:.1f}" y1="{dy(1.85):.1f}" x2="{dx(0.70)+bk_w_px-6:.1f}" y2="{dy(1.85):.1f}" stroke="#cbd5e1" stroke-width="1.5"/>')
    out.append(f'<text x="{dx(0.70)+bk_w_px/2:.1f}" y="{dy(1.65):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Balda Cristalería LED 3000K</text>')

    # 3. Estantería Vertical Víveres y Despensa Santos (X=1.70..2.30m -> 0,60m)
    est_w_px = 0.60 * S2
    out.append(f'<rect x="{dx(1.70):.1f}" y="{dy(2.20):.1f}" width="{est_w_px:.1f}" height="{2.12*S2:.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="1.1"/>')
    for ey in [0.45, 0.85, 1.25, 1.65]:
        out.append(f'<line x1="{dx(1.70):.1f}" y1="{dy(ey):.1f}" x2="{dx(1.70)+est_w_px:.1f}" y2="{dy(ey):.1f}" stroke="#475569" stroke-width="0.8"/>')
    out.append(f'<text x="{dx(1.70)+est_w_px/2:.1f}" y="{dy(1.05):.1f}" fill="#f8fafc" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ESTANTES VÍVERES</text>')
    out.append(f'<text x="{dx(1.70)+est_w_px/2:.1f}" y="{dy(0.90):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Conservas y Cajas</text>')

    # Remate superior a falso techo de despensa
    out.append(f'<rect x="{dx(0.0):.1f}" y="{dy(2.65):.1f}" width="{2.30*S2:.1f}" height="{0.45*S2:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')
    out.append(f'<text x="{dx(1.15):.1f}" y="{dy(2.65)+0.22*S2+3:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">CIERRE ENRASADO A FALSO TECHO (+2,20 a +2,65 m)</text>')

    # Cotas Alzado D
    dx_dim = dx(2.30) + 20
    out.append(dim_v(dy(0.00), dy(0.92), dx_dim, 0, "+0,92 m (Bancada Auxiliar)", "#38bdf8", font_size=6.8))
    out.append(dim_v(dy(0.92), dy(1.10), dx_dim, 0, "+1,10 m (Tomas C5)", "#f59e0b", marker="tick-amber", font_size=6.5))
    out.append(dim_v(dy(1.10), dy(2.20), dx_dim, 0, "+2,20 m (Coronación)", "#cbd5e1", font_size=6.8))
    out.append(dim_v(dy(2.20), dy(2.65), dx_dim, 0, "+2,65 m (Techo)", "#f59e0b", marker="tick-amber", font_size=7.0))

    # ==========================================================================
    # BANDA DERECHA: GUÍA TÉCNICA DE ALTURAS ERGONÓMICAS Y MECANISMOS
    # ==========================================================================
    rx = 1480
    out.append(f'<rect x="{rx}" y="30" width="440" height="1360" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="420" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">GUÍA ERGONÓMICA DE ALTURAS Y BODEGA</text>')

    alturas_data = [
        ("1. NIVELES VERTICALES NORMALIZADOS", "#38bdf8", [
            ("+2,65 m", "Falso techo continuo (yeso laminado hidrófugo)"),
            ("+2,50 m", "Fosa perimetral cortinero hacia patio claustro"),
            ("+2,20 m", "Coronación muebles columnas cocina y bodega"),
            ("+1,75 m", "Límite superior horno microondas / vapor"),
            ("+1,45 m", "Estante desayunador pocket y balda bodega LED"),
            ("+1,30 m", "Eje visual y táctil horno Bosch Serie 8"),
            ("+1,10 m", "Tomas encimera C5 y bancada back kitchen"),
            ("+0,92 m", "Cota encimera Dekton (isla, desayunador y bodega)"),
            ("+0,65 m", "Plano de asiento 4 taburetes altos de barra"),
            ("+0,30 m", "Enchufes ocultos zócalo y fuerza electrodomésticos"),
            ("+0,08 m", "Zócalo retraído Santos (rejilla ventilación)"),
            ("±0,00 m", "Suelo radiante porcelánico continuo"),
        ]),
        ("2. VENTAJAS DE LA NUEVA DESPENSA / BODEGA", "#f59e0b", [
            ("Cava de vinos integrada", "Santos 60 botellas con control higrotérmico"),
            ("Isla 100% limpia", "Robots de cocina en la bancada auxiliar"),
            ("Mayor capacidad seca", "Estantes en U de 40 cm para conservas y menaje"),
            ("Puerta corredera pocket", "Aísla el ruido de pequeños electrodomésticos"),
        ]),
        ("3. JUSTIFICACIÓN BIOMECÁNICA", "#10b981", [
            ("Encimera a +0,92 m", "Reduce un 35% la flexión lumbar al cortar"),
            ("Hornos a +0,92..1,45 m", "Manipulación de bandejas a 90° de codo"),
            ("Campana Bora integrada", "Cero obstáculos visuales hacia el patio"),
            ("Voladizo barra 35 cm", "Espacio para rodillas sin rozar frentes"),
        ]),
        ("4. PRÓXIMOS PASOS DE LA RAMA", "#f43f5e", [
            ("Mecanismos y fuerza", "Cuadro de tomas C3, C4, C5 y torres escamoteables"),
            ("Iluminación IES", "Carril magnético techo + tiras LED 3000K"),
            ("Carpintería Cortizo", "Detalle encuentro corredera embutida con patio"),
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
    """Genera visor web interactivo de cocina + despensa/bodega Santos"""
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estudio Técnico: Cocina + Despensa/Bodega Santos · Hogar Oleiros (Propuesta D v2)</title>
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
        <span>RAMA: feature/cocina-diseno-elevaciones (Rebased s/ v2 definitiva)</span>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
        <span>🍳 Suite Culinaria: Cocina Isla Santos + Despensa & Cava Bodega</span>
      </h1>
      <p class="text-slate-400 text-sm mt-1">Superficie ampliada a 20,80 m² (15,20 m² cocina + 5,60 m² despensa/bodega) tras reubicación de lavandería a ala Oeste</p>
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
      <span>📐 Plano K-01: Planta Suite Cocina + Bodega (1:20)</span>
    </button>
    <button onclick="showTab('elevaciones')" id="tab-elevaciones" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📏 Plano K-02: Alzados Cocina & Interior Bodega (1:20)</span>
    </button>
    <button onclick="showTab('resumen')" id="tab-resumen" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📋 Análisis Espacial & Ventajas v2</span>
    </button>
  </div>

  <!-- Contenedor Tab 1: Planta Esquemática -->
  <div id="content-planta" class="space-y-4">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 overflow-hidden shadow-2xl">
      <div class="flex justify-between items-center mb-3 px-2">
        <span class="text-xs font-mono text-sky-400">ISLA SANTOS 2,80×1,00m · FRENTE COLUMNAS 3,60m · NUEVA DESPENSA/BODEGA 5,60m²</span>
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
        <span class="text-xs font-mono text-amber-400">ALZADO COLUMNAS (H=2,65m) · ALZADO ISLA (H=0,92m) · ALZADO D BODEGA & CAVA (H=2,65m)</span>
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
      <h3 class="text-lg font-bold text-sky-400 font-mono mb-4">📐 Suite Culinaria Ampliada (20,80 m²)</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Cocina Isla Santos:</strong> 15,20 m² ($3,80 \times 4,60$ m)</li>
        <li>• <strong class="text-white">Despensa Walk-in Santos:</strong> 5,60 m² ($2,30 \times 2,45$ m)</li>
        <li>• <strong class="text-white">Isla Central:</strong> 2,80 × 1,00 m (encimera Dekton Kelya)</li>
        <li>• <strong class="text-white">Frente Columnas:</strong> 3,60 × 0,65 m (6 columnas × 60 cm)</li>
        <li>• <strong class="text-white">Paso a Patio:</strong> 1,15 m (holgura taburetes)</li>
        <li>• <strong class="text-white">Paso Culinario:</strong> 1,00 m (apertura cajones)</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-amber-400 font-mono mb-4">🍷 Equipamiento Bodega & Cava</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Cava Santos climatizada:</strong> 60 botellas, doble zona Tª</li>
        <li>• <strong class="text-white">Bancada "Back Kitchen":</strong> Para robots (Thermomix, etc.)</li>
        <li>• <strong class="text-white">Estantes en U (40 cm):</strong> Conservas, víveres y menaje</li>
        <li>• <strong class="text-white">Puerta pocket (0,85 m):</strong> Oculta en tabique</li>
        <li>• <strong class="text-white">Encimera auxiliar:</strong> A cota +0,92 m con tomas C5</li>
        <li>• <strong class="text-white">Iluminación LED:</strong> Tiras cálidas 3000K en baldas</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-emerald-400 font-mono mb-4">⚡ Siguiente Hoja de Ruta</h3>
      <p class="text-xs text-slate-400 mb-3">Con el espacio de cocina y bodega consolidado, podemos detallar:</p>
      <div class="space-y-2 text-sm text-slate-300">
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-sky-300">1. Enchufes y Potencias:</strong> Torres escamoteables en isla, tomas de bancada en bodega (C5) y líneas dedicadas C3 (25A) y C4 (16A).
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-amber-300">2. Iluminación IES:</strong> Carril magnético empotrado en falso techo de cocina + luz cálida ambiental en cava de vinos.
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-emerald-300">3. Ventanal y Vano:</strong> Encuentro con corredera Cortizo Cor Vision Plus y salida directa al banco de iroko del Patio Claustro.
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
    print("Generando Plano K-01: Planta Esquemática Cocina + Despensa/Bodega Santos v2...")
    planta_svg = build_cocina_planta_svg()
    with open("plano_cocina_planta_esquematica.svg", "w", encoding="utf-8") as f:
        f.write(planta_svg)
    print(" -> Guardado en plano_cocina_planta_esquematica.svg")

    print("Generando Plano K-02: Alzados Interiores y Alturas Ergonómicas v2...")
    elev_svg = build_cocina_elevaciones_svg()
    with open("plano_cocina_elevaciones_alturas.svg", "w", encoding="utf-8") as f:
        f.write(elev_svg)
    print(" -> Guardado en plano_cocina_elevaciones_alturas.svg")

    print("Generando Visor Web Interactivo de Cocina v2...")
    html_content = build_cocina_interactivo_html()
    with open("cocina_estudio_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(" -> Guardado en cocina_estudio_interactivo.html")

    print("Completado con éxito.")

if __name__ == "__main__":
    main()
