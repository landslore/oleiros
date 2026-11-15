#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Independientes de la Cocina (Propuesta D - Hogar Oleiros)
- Plano 01: Planta Arquitectónica Esquemática y de Distribución (Escala 1:20)
- Plano 02: Alzados Interiores y Cotas de Altura Ergonómica (Frente Columnas + Isla Santos)
Normativa: CTE DB-HS / DB-SUA / Normas do Hábitat Galego (NHG) / Antropometría Cocinas Santos Fine
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
      <marker id="arrow-cad" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
        <path d="M 0 1 L 5 3 L 0 5 z" fill="#38bdf8"/>
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
    </defs>
    """

def dim_h(x1, x2, y, offset_y, label, col="#38bdf8", marker="tick-45", font_size=7.5):
    """Línea de cota horizontal acotada"""
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
    """Línea de cota vertical acotada"""
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
    Genera el Plano 01: Planta Esquemática y de Distribución de la Cocina (1:20)
    Espacio: ~4,00 m ancho x 4,60 m largo
    """
    W, H = 1600, 1100
    S = 140.0  # Escala 1m = 140px (gran formato 1:20 de detalle)
    OX = 260.0  # Origen en píxeles (X=0.00 en modelo corresponde al ventanal del patio)
    OY = 200.0  # Origen en píxeles (Y=0.00 en muro Norte)

    def mx(val_m):
        return OX + val_m * S

    def my(val_m):
        return OY + val_m * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        # Cuadro de borde exterior
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1120" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-01 · DISTRIBUCIÓN Y GEOMETRÍA ESQUEMÁTICA DE COCINA (DETALLE 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Propuesta D · Hogar Oleiros · Isla Santos Fine 2,80×1,00m · Frente Columnas 3,60m · Circulaciones reglamentarias NHG</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1120" height="970" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Geometría del espacio de cocina:
    # Ancho libre: 3.80 m (X=0.00 a X=3.80)
    # Longitud: 4.60 m (Y=0.00 a Y=4.60)
    # X=0.00: Ventanal Patio Claustro (Corredera 2H Cortizo Cor Vision Plus)
    # X=3.80: Tabique con Lavandería (con Frente de Columnas empotrado)
    # Y=0.00: Muro Norte (separación con pasillo distribuidor / aseo)
    # Y=4.60: Límite diáfano de conexión visual y física con Comedor Principal

    # 1. Muro Norte (Y = 0.00, grosor 0.15m)
    tw = 0.15 * S
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{4.50*S:.1f}" height="{tw:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # 2. Muro Este divisorio con Lavandería (X = 3.80, grosor 0.15m)
    out.append(f'<rect x="{mx(3.80):.1f}" y="{my(-0.15):.1f}" width="{tw:.1f}" height="{4.90*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')

    # 3. Ventanal Oeste hacia Patio Claustro (X = 0.00, Y = 0.30 a 3.90 -> 3,60 m de hueco acristalado)
    # Muro superior e inferior de jamba
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(-0.15):.1f}" width="{0.35*S:.1f}" height="{0.45*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    out.append(f'<rect x="{mx(-0.35):.1f}" y="{my(3.90):.1f}" width="{0.35*S:.1f}" height="{0.85*S:.1f}" fill="url(#hatch-wall)" stroke="#e2e8f0" stroke-width="1.3"/>')
    # Carpintería corredera 2 hojas embutida en forjado
    out.append(f'<rect x="{mx(-0.06):.1f}" y="{my(0.30):.1f}" width="{0.12*S:.1f}" height="{3.60*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.1"/>')
    # Hoja fija y hoja móvil
    out.append(f'<line x1="{mx(-0.02):.1f}" y1="{my(0.30):.1f}" x2="{mx(-0.02):.1f}" y2="{my(2.10):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<line x1="{mx(0.02):.1f}" y1="{my(2.05):.1f}" x2="{mx(0.02):.1f}" y2="{my(3.90):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<text x="{mx(-0.10):.1f}" y="{my(2.10):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700" transform="rotate(-90 {mx(-0.10):.1f} {my(2.10):.1f})" text-anchor="middle">VENTANAL CORREDERO PATIO CLAUSTRO (3,60×2,65 m)</text>')

    # Pavimento interior técnico
    out.append(f'<rect x="{mx(0.00):.1f}" y="{my(0.00):.1f}" width="{3.80*S:.1f}" height="{4.60*S:.1f}" fill="#0f172a" opacity="0.85"/>')

    # Círculo NHG de habitabilidad y giro de accesibilidad Ø1,50 m
    out.append(f'<circle cx="{mx(2.10):.1f}" cy="{my(2.30):.1f}" r="{0.75*S:.1f}" fill="#38bdf8" fill-opacity="0.04" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{mx(2.10):.1f}" y="{my(2.34):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" text-anchor="middle">CIRCULACIÓN LIBRE Ø1,50 m (NHG)</text>')

    # --------------------------------------------------------------------------
    # FRENTE DE COLUMNAS ESTE (X = 3.15 a 3.80 -> Fondo 0,65 m, Longitud 3,60 m de Y=0.30 a 3.90)
    # --------------------------------------------------------------------------
    fc_x = mx(3.15)
    fc_y = my(0.30)
    fc_w = 0.65 * S
    fc_h = 3.60 * S
    out.append(f'<rect x="{fc_x:.1f}" y="{fc_y:.1f}" width="{fc_w:.1f}" height="{fc_h:.1f}" fill="url(#grad-columnas)" stroke="#e2e8f0" stroke-width="1.4"/>')

    # Módulos del Frente de Columnas (6 columnas de 60cm cada una):
    modulos_col = [
        ("COL 01 (60 cm)", "FRIGORÍFICO XXL", "Integrado 1-puerta", "#38bdf8"),
        ("COL 02 (60 cm)", "CONGELADOR NO-FROST", "Integrado vertical", "#38bdf8"),
        ("COL 03 (60 cm)", "TORRE HORNO + MIC", "Bosch Serie 8", "#f59e0b"),
        ("COL 04 (60 cm)", "DESAYUNADOR (A)", "Puerta escamoteable", "#10b981"),
        ("COL 05 (60 cm)", "DESAYUNADOR (B)", "Encimera café/tost.", "#10b981"),
        ("COL 06 (60 cm)", "DESPENSERO TOTAL", "Gavetas interiores", "#cbd5e1"),
    ]
    for idx, (cod, tit, sub, col) in enumerate(modulos_col):
        m_top = fc_y + idx * 0.60 * S
        out.append(f'<line x1="{fc_x:.1f}" y1="{m_top:.1f}" x2="{fc_x+fc_w:.1f}" y2="{m_top:.1f}" stroke="#475569" stroke-width="0.9"/>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+18:.1f}" fill="{col}" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">{cod}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+36:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{tit}</text>')
        out.append(f'<text x="{fc_x+fc_w/2:.1f}" y="{m_top+52:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{sub}</text>')

    # Puerta corredera empotrada de acceso a Lavandería (al Norte de las columnas: Y = 4.00 a 4.90)
    out.append(f'<rect x="{mx(3.72):.1f}" y="{my(4.00):.1f}" width="{0.08*S:.1f}" height="{0.85*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<text x="{mx(3.92):.1f}" y="{my(4.45):.1f}" fill="#38bdf8" font-family="monospace" font-size="7.0" font-weight="700" transform="rotate(90 {mx(3.92):.1f} {my(4.45):.1f})" text-anchor="middle">PASO A LAVANDERÍA (0,85 m)</text>')

    # --------------------------------------------------------------------------
    # ISLA CENTRAL SANTOS FINE (X = 1.15 a 2.15 -> Ancho 1,00 m, Longitud 2,80 m de Y=0.70 a 3.50)
    # --------------------------------------------------------------------------
    isla_x = mx(1.15)
    isla_y = my(0.70)
    isla_w = 1.00 * S
    isla_h = 2.80 * S

    # Cuerpo principal de la isla (Encimera Dekton)
    out.append(f'<rect x="{isla_x:.1f}" y="{isla_y:.1f}" width="{isla_w:.1f}" height="{isla_h:.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="1.8"/>')
    out.append(f'<rect x="{isla_x+3:.1f}" y="{isla_y+3:.1f}" width="{isla_w-6:.1f}" height="{isla_h-6:.1f}" fill="url(#grad-dekton)" opacity="0.35" stroke="#475569" stroke-width="0.8"/>')

    # Línea que separa zona de trabajo (fondo 65 cm Este) de zona barra volada comensales (fondo 35 cm Oeste)
    barra_split_x = isla_x + 0.35 * S
    out.append(f'<line x1="{barra_split_x:.1f}" y1="{isla_y:.1f}" x2="{barra_split_x:.1f}" y2="{isla_y+isla_h:.1f}" stroke="#38bdf8" stroke-width="0.9" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{isla_x+18:.1f}" y="{isla_y+isla_h/2:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700" transform="rotate(-90 {isla_x+18:.1f} {isla_y+isla_h/2:.1f})" text-anchor="middle">BARRA SNACK VOLADA (0,35 m)</text>')

    # 4 Taburetes altos en la barra (asiento Ø34 cm orientados al Patio Claustro)
    for ty in [1.05, 1.70, 2.35, 3.00]:
        st_cx = isla_x - 0.22 * S
        st_cy = my(ty)
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.18*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
        out.append(f'<circle cx="{st_cx:.1f}" cy="{st_cy:.1f}" r="{0.08*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.6"/>')

    # Módulos interiores en la Isla (Lado Este - zona de trabajo culinario):
    # Fregadero bajo encimera de 70 cm (acero inox / composite negro) + grifo caño alto
    sink_w = 0.50 * S
    sink_h = 0.70 * S
    sink_x = isla_x + 0.42 * S
    sink_y = isla_y + 0.35 * S
    out.append(f'<rect x="{sink_x:.1f}" y="{sink_y:.1f}" width="{sink_w:.1f}" height="{sink_h:.1f}" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.3"/>')
    # Seno interior
    out.append(f'<rect x="{sink_x+4:.1f}" y="{sink_y+4:.1f}" width="{sink_w-8:.1f}" height="{sink_h-8:.1f}" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>')
    # Grifo caño alto monomando con caño giratorio 360°
    out.append(f'<circle cx="{sink_x+sink_w/2:.1f}" cy="{sink_y+sink_h/2:.1f}" r="5.5" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.1"/>')
    out.append(f'<line x1="{sink_x+sink_w/2:.1f}" y1="{sink_y+sink_h/2:.1f}" x2="{sink_x+sink_w/2-10:.1f}" y2="{sink_y+sink_h/2:.1f}" stroke="#f8fafc" stroke-width="1.5"/>')
    out.append(f'<text x="{sink_x+sink_w/2:.1f}" y="{sink_y+sink_h+16:.1f}" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">FREGADERO 70×45 cm</text>')

    # Placa de Inducción con Extracción Integrada Bora Pure (80×52 cm)
    bora_w = 0.52 * S
    bora_h = 0.82 * S
    bora_x = isla_x + 0.40 * S
    bora_y = isla_y + 1.55 * S
    out.append(f'<rect x="{bora_x:.1f}" y="{bora_y:.1f}" width="{bora_w:.1f}" height="{bora_h:.1f}" rx="2" fill="#18181b" stroke="#f59e0b" stroke-width="1.4"/>')
    # Zonas de cocción por inducción
    for zx, zy in [(bora_x+15, bora_y+20), (bora_x+bora_w-15, bora_y+20), (bora_x+15, bora_y+bora_h-20), (bora_x+bora_w-15, bora_y+bora_h-20)]:
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="11" fill="none" stroke="#f59e0b" stroke-width="0.9"/>')
        out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="3" fill="#f59e0b"/>')
    # Tobera central de extracción integrada Bora Pure
    out.append(f'<rect x="{bora_x+bora_w/2-8:.1f}" y="{bora_y+bora_h/2-16:.1f}" width="16" height="32" rx="3" fill="#0f172a" stroke="#06b6d4" stroke-width="1.2"/>')
    out.append(f'<circle cx="{bora_x+bora_w/2:.1f}" cy="{bora_y+bora_h/2:.1f}" r="5" fill="none" stroke="#06b6d4" stroke-width="1.0"/>')
    out.append(f'<text x="{bora_x+bora_w/2:.1f}" y="{bora_y+bora_h+16:.1f}" fill="#f59e0b" font-family="monospace" font-size="6.0" font-weight="700" text-anchor="middle">PLACA BORA PURE 80 cm</text>')

    # Lavavajillas panelado integrado 60 cm (bajo encimera entre fregadero y módulo cocción)
    out.append(f'<text x="{isla_x+0.68*S:.1f}" y="{isla_y+1.28*S:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">[ LAVAVAJILLAS 60 cm ]</text>')

    # --------------------------------------------------------------------------
    # COTAS Y PASOS LIBRES ARQUITECTÓNICOS (MILÍMETRO / METRO)
    # --------------------------------------------------------------------------
    # Paso 1: Entre Cristalera Patio y Taburetes de la Isla (1,15 m)
    out.append(dim_h(mx(0.00), isla_x, my(0.15), 0, "1,15 m (Paso Libre y Taburetes)", "#38bdf8", font_size=7.2))

    # Ancho Isla (1,00 m)
    out.append(dim_h(isla_x, isla_x + isla_w, my(0.15), 0, "1,00 m (Isla)", "#f8fafc", font_size=7.2))

    # Paso 2: Entre Isla y Frente de Columnas (1,00 m - Zona de Trabajo y Apertura Hornos/Frigo)
    out.append(dim_h(isla_x + isla_w, fc_x, my(0.15), 0, "1,00 m (Paso Culinario)", "#10b981", marker="tick-emerald", font_size=7.2))

    # Fondo Frente Columnas (0,65 m)
    out.append(dim_h(fc_x, mx(3.80), my(0.15), 0, "0,65 m", "#94a3b8", font_size=7.0))

    # Cota Total Ancho Cocina (3,80 m)
    out.append(dim_h(mx(0.00), mx(3.80), my(-0.05), -25, "3,80 m (Ancho Total Cocina)", "#38bdf8", font_size=8.5))

    # Cotas Verticales:
    # Retranqueo Norte a Isla (0,70 m)
    out.append(dim_v(my(0.00), isla_y, isla_x, -35, "0,70 m", "#94a3b8", font_size=7.0))
    # Longitud Isla (2,80 m)
    out.append(dim_v(isla_y, isla_y + isla_h, isla_x, -35, "2,80 m (Longitud Isla)", "#f8fafc", font_size=8.0))
    # Paso Sur a Comedor (1,10 m)
    out.append(dim_v(isla_y + isla_h, my(4.60), isla_x, -35, "1,10 m (Paso a Comedor)", "#38bdf8", font_size=7.2))

    # Longitud Total Espacio Cocina (4,60 m)
    out.append(dim_v(my(0.00), my(4.60), mx(0.00), -55, "4,60 m (Longitud Total Cocina)", "#38bdf8", font_size=8.5))

    # Cotas del Frente de Columnas (Este):
    out.append(dim_v(fc_y, fc_y + fc_h, mx(3.80), 30, "3,60 m (6 Módulos Columnas × 60 cm)", "#f59e0b", marker="tick-amber", font_size=7.5))

    # --------------------------------------------------------------------------
    # LEYENDA Y CUADRO DE ESPECIFICACIONES TÉCNICAS (BANDA DERECHA)
    # --------------------------------------------------------------------------
    rx = 1180
    out.append(f'<rect x="{rx}" y="30" width="390" height="1020" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="370" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">MEMORIA ESQUEMÁTICA COCINA</text>')

    specs = [
        ("1. ZONIFICACIÓN Y TRIÁNGULO DE TRABAJO", "#38bdf8", [
            ("Zona Frío / Almacén", "Frente Este (Frigo XXL + Congelador)"),
            ("Zona Cocción", "Isla Central (Bora Pure 80 cm)"),
            ("Zona Aguas / Limpieza", "Isla Central (Fregadero 70 + LVV 60)"),
            ("Zona Desayunador Pocket", "Módulo 120 cm escamoteable"),
            ("Zona Social / Barra", "4 taburetes orientados al patio"),
        ]),
        ("2. DIMENSIONES Y ANTROPOMETRÍA", "#10b981", [
            ("Superficie útil neta", "15,20 m² de estancia cocina"),
            ("Longitud Isla Santos", "2,80 m x 1,00 m (Encimera Dekton)"),
            ("Paso libre patio-isla", "1,15 m (holgura para sentarse y paso)"),
            ("Paso libre culinario", "1,00 m (apertura total de cajones)"),
            ("Accesibilidad", "Giro libre Ø1,50 m cumpliendo NHG"),
        ]),
        ("3. MOBILIARIO SANTOS FINE", "#f59e0b", [
            ("Acabado frentes", "Laca mate seda antihuellas Cashmere"),
            ("Columnas integradas", "Roble humo con tirador gola oculto"),
            ("Herrajes interiores", "Blum Legrabox con amortiguación"),
            ("Mueble Desayunador", "Puertas escamoteables pocket 120cm"),
            ("Zócalo inferior", "Aluminio negro retranqueado (h=6cm)"),
        ]),
        ("4. RELACIÓN CON EL ENTORNO", "#cbd5e1", [
            ("Conexión exterior", "Corredera 3,60 m hacia Patio Claustro"),
            ("Conexión técnica", "Puerta corredera oculta a Lavandería"),
            ("Conexión diáfana", "Fluidez total con Comedor y Salón Sur"),
        ]),
        ("5. PRÓXIMAS FASES DE DEFINICIÓN", "#f43f5e", [
            ("Fase 2", "Tomas de enchufe (C3, C4, C5) y potencias"),
            ("Fase 3", "Iluminación técnica IES (carriles/LEDs)"),
            ("Fase 4", "Detalle carpinterías Cortizo y dintel"),
        ]),
    ]

    sy = 85
    for cat_title, cat_col, rows in specs:
        out.append(f'<text x="{rx+16}" y="{sy}" fill="{cat_col}" font-family="monospace" font-size="7.5" font-weight="700">{cat_title}</text>')
        out.append(f'<line x1="{rx+16}" y1="{sy+4}" x2="{rx+374}" y2="{sy+4}" stroke="{cat_col}" stroke-width="0.7" opacity="0.6"/>')
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
    Genera el Plano 02: Alzados Interiores y Cotas de Altura Ergonómica (1:20)
    - Alzado A: Frente Columnas Este (L=3,60m, H=2,65m)
    - Alzado B: Frente Isla Santos - Lado de Trabajo Este (L=2,80m, H=0,92m)
    - Alzado C: Frente Isla Santos - Lado Barra Oeste / Taburetes (L=2,80m, H=0,92m)
    - Diagrama de Alturas Ergonómicas Normalizadas
    """
    W, H = 1800, 1300
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs_technical(),
        f'<rect x="16" y="16" width="{W-32}" height="{H-32}" fill="none" stroke="#475569" stroke-width="1.6"/>',
        f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#334155" stroke-width="0.8"/>',

        # Cabecera técnica
        '<rect x="32" y="30" width="1280" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.9"/>',
        '<text x="46" y="50" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="700">PLANO K-02 · ALZADOS Y COTAS DE ALTURA ERGONÓMICA DE COCINA (DETALLE 1:20)</text>',
        '<text x="46" y="64" fill="#94a3b8" font-family="monospace" font-size="8.0">Propuesta D · Elevación Frente Columnas Este · Elevación Isla Santos Fine · Alturas sobre Cota ±0,00m de Suelo Terminado</text>',

        # Retícula CAD de fondo
        f'<rect x="32" y="80" width="1280" height="1170" fill="url(#grid-cad-major)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # ==========================================================================
    # SECCIÓN 1: ALZADO A - FRENTE DE COLUMNAS ESTE (L = 3,60 m, H = 2,65 m)
    # ==========================================================================
    # Escala: 1m = 180px
    S1 = 180.0
    A_OX = 180.0
    A_GROUND_Y = 480.0  # Cota ±0,00 m en Y=480

    def ax(val_m):
        return A_OX + val_m * S1

    def ay(val_h_m):
        return A_GROUND_Y - val_h_m * S1

    # Línea de Suelo Terminado (Cota ±0,00 m)
    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{A_GROUND_Y:.1f}" x2="{ax(3.9):.1f}" y2="{A_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{A_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m (SUELO TERMINADO)</text>')

    # Línea de Falso Techo Continuo (Cota +2,65 m)
    ceil_y = ay(2.65)
    out.append(f'<line x1="{ax(-0.3):.1f}" y1="{ceil_y:.1f}" x2="{ax(3.9):.1f}" y2="{ceil_y:.1f}" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="8,4"/>')
    out.append(f'<text x="{ax(-0.35):.1f}" y="{ceil_y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">FALSO TECHO +2,65 m</text>')

    # Título Alzado A
    out.append(f'<rect x="{ax(0.0):.1f}" y="{ceil_y-32:.1f}" width="420" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{ax(0.0)+10:.1f}" y="{ceil_y-17:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO A · FRENTE DE COLUMNAS ESTE (L = 3,60 m · H = 2,65 m)</text>')

    # 1. Zócalo inferior (h = 0,08 m) retranqueado
    zoc_y = ay(0.08)
    out.append(f'<rect x="{ax(0.0):.1f}" y="{zoc_y:.1f}" width="{3.60*S1:.1f}" height="{0.08*S1:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')
    out.append(f'<text x="{ax(1.8):.1f}" y="{A_GROUND_Y-4:.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ZÓCALO RETRANQUEADO h = 8 cm (CON REJILLA VENTILACIÓN FRIGO)</text>')

    # 2. Muebles de Columnas (de h=0.08 a h=2.20 -> 2,12 m de puertas principales)
    # 6 Módulos de 60 cm:
    # Col 1: Frigorífico integrable (puerta 1,78m + altillo)
    # Col 2: Congelador integrable (puerta 1,78m + altillo)
    # Col 3: Torre Horno / Micro (gaveta inferior 0,38m + horno 0,60m + micro 0,45m + altillo)
    # Col 4 y 5: Desayunador Pocket 120 cm (puertas escamoteables de suelo/bancada a 2,20m)
    # Col 6: Columna Despensero con gavetas
    cols = [
        ("COL 01", "FRIGORÍFICO XXL", "1-puerta integrado", 0.60),
        ("COL 02", "CONGELADOR", "No-Frost vertical", 0.60),
        ("COL 03", "TORRE HORNO/MIC", "Bosch Serie 8", 0.60),
        ("COL 04-05", "DESAYUNADOR POCKET (120 cm)", "Puertas escamoteables", 1.20),
        ("COL 06", "DESPENSERO", "Gavetas interiores", 0.60),
    ]

    cur_x = 0.0
    for cid, ctit, csub, cw in cols:
        cx1 = ax(cur_x)
        cw_px = cw * S1
        # Marco general columna
        out.append(f'<rect x="{cx1:.1f}" y="{ay(2.20):.1f}" width="{cw_px:.1f}" height="{2.12*S1:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if "FRIGORÍFICO" in ctit or "CONGELADOR" in ctit:
            # División puerta principal y altillo
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.86):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')
            # Tirador gola vertical
            out.append(f'<line x1="{cx1+cw_px-4:.1f}" y1="{ay(0.15):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(1.80):.1f}" stroke="#38bdf8" stroke-width="1.5"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.00):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">{ctit}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.85):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">{csub}</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(2.03):.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ALTILLO</text>')

        elif "TORRE" in ctit:
            # Gaveta inferior (0.08 a 0.70m)
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(0.70):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(0.70):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="6.0" text-anchor="middle">GAVETA INFERIOR</text>')
            # Horno Bosch Serie 8 (0.70 a 1.30m -> h=60cm)
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.30):.1f}" width="{cw_px-8:.1f}" height="{0.60*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+12:.1f}" y="{ay(1.24):.1f}" width="{cw_px-24:.1f}" height="{0.42*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<circle cx="{cx1+cw_px/2:.1f}" cy="{ay(1.27):.1f}" r="4" fill="none" stroke="#f59e0b" stroke-width="1.0"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.96):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">HORNO PIROLÍTICO</text>')
            # Microondas Bosch Serie 8 (1.30 a 1.75m -> h=45cm)
            out.append(f'<rect x="{cx1+4:.1f}" y="{ay(1.75):.1f}" width="{cw_px-8:.1f}" height="{0.45*S1:.1f}" rx="2" fill="#090d16" stroke="#f59e0b" stroke-width="1.4"/>')
            out.append(f'<rect x="{cx1+12:.1f}" y="{ay(1.71):.1f}" width="{cw_px-24:.1f}" height="{0.30*S1:.1f}" rx="2" fill="#18181b" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.50):.1f}" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MICROONDAS / VAPOR</text>')
            # Altillo superior (1.75 a 2.20m)
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.75):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.75):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.98):.1f}" fill="#64748b" font-family="monospace" font-size="5.5" text-anchor="middle">ALTILLO</text>')

        elif "DESAYUNADOR" in ctit:
            # Línea central que separa las dos puertas pocket de 60 cm
            mid_pocket = cx1 + 0.60 * S1
            out.append(f'<line x1="{mid_pocket:.1f}" y1="{ay(2.20):.1f}" x2="{mid_pocket:.1f}" y2="{ay(0.08):.1f}" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,3"/>')
            # Encimera interior de trabajo a +0,92 m
            out.append(f'<line x1="{cx1+4:.1f}" y1="{ay(0.92):.1f}" x2="{cx1+cw_px-4:.1f}" y2="{ay(0.92):.1f}" stroke="#10b981" stroke-width="1.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.95):.1f}" fill="#10b981" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA INTERIOR DEKTON (+0,92 m)</text>')
            # Estantes superiores a +1,45m y +1,80m con LED
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.45):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.45):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(1.80):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(1.80):.1f}" stroke="#cbd5e1" stroke-width="1.2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.40):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">MUEBLE DESAYUNADOR POCKET (120 cm)</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.25):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Cafetera Espresso · Molinillo · Tostadora · LED integrado</text>')
            # Gavetas inferiores bajo la encimera del desayunador
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(0.50):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(0.50):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.28):.1f}" fill="#64748b" font-family="monospace" font-size="5.8" text-anchor="middle">GAVETAS DESPENSA / MENAJE</text>')

        elif "DESPENSERO" in ctit:
            # Despensero vertical con 5 gavetas interiores extraíbles
            for gy in [0.45, 0.85, 1.25, 1.65]:
                out.append(f'<line x1="{cx1+8:.1f}" y1="{ay(gy):.1f}" x2="{cx1+cw_px-8:.1f}" y2="{ay(gy):.1f}" stroke="#475569" stroke-width="0.6" stroke-dasharray="3,2"/>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(1.05):.1f}" fill="#f8fafc" font-family="monospace" font-size="7.0" font-weight="700" text-anchor="middle">DESPENSERO</text>')
            out.append(f'<text x="{cx1+cw_px/2:.1f}" y="{ay(0.90):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5" text-anchor="middle">Gavetas Blum</text>')
            out.append(f'<line x1="{cx1:.1f}" y1="{ay(1.86):.1f}" x2="{cx1+cw_px:.1f}" y2="{ay(1.86):.1f}" stroke="#475569" stroke-width="0.8"/>')

        cur_x += cw

    # 3. Remate Superior / Faja ciega hasta falso techo (de +2.20m a +2.65m -> h=0.45m)
    faja_y = ay(2.65)
    faja_h = 0.45 * S1
    out.append(f'<rect x="{ax(0.0):.1f}" y="{faja_y:.1f}" width="{3.60*S1:.1f}" height="{faja_h:.1f}" fill="#0f172a" stroke="#475569" stroke-width="1.0"/>')
    out.append(f'<text x="{ax(1.8):.1f}" y="{faja_y+faja_h/2+3:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">REMATADO ENRASADO A FALSO TECHO (+2,20 m a +2,65 m · REGISTROS VMC)</text>')

    # Cotas de Altura del Alzado A (Derecha):
    cx_dim = ax(3.60) + 25
    out.append(dim_v(ay(0.00), ay(0.08), cx_dim, 0, "+0,08 m (Zócalo)", "#94a3b8", font_size=6.8))
    out.append(dim_v(ay(0.08), ay(0.92), cx_dim, 0, "+0,92 m (Bancada Desayunador / Base Horno)", "#10b981", marker="tick-emerald", font_size=6.8))
    out.append(dim_v(ay(0.92), ay(1.30), cx_dim, 0, "+1,30 m (Eje Visual Horno)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.30), ay(1.75), cx_dim, 0, "+1,75 m (Microondas)", "#f59e0b", marker="tick-amber", font_size=6.8))
    out.append(dim_v(ay(1.75), ay(2.20), cx_dim, 0, "+2,20 m (Coronación Puertas)", "#cbd5e1", font_size=6.8))
    out.append(dim_v(ay(2.20), ay(2.65), cx_dim, 0, "+2,65 m (Falso Techo)", "#38bdf8", font_size=7.2))

    # Cota total de altura libre (2,65 m)
    out.append(dim_v(ay(0.00), ay(2.65), cx_dim + 45, 0, "2,65 m ALTURA LIBRE TOTAL", "#38bdf8", font_size=8.5))

    # ==========================================================================
    # SECCIÓN 2: ALZADO B - ELEVACIÓN ISLA SANTOS FINE (L = 2,80 m, H = 0,92 m)
    # Lado de Trabajo (Vista desde el Este hacia el Oeste)
    # ==========================================================================
    S2 = 200.0  # Escala 1m = 200px para la isla
    B_OX = 180.0
    B_GROUND_Y = 820.0  # Cota ±0,00 m en Y=820

    def bx(val_m):
        return B_OX + val_m * S2

    def by(val_h_m):
        return B_GROUND_Y - val_h_m * S2

    # Línea de Suelo Terminado
    out.append(f'<line x1="{bx(-0.3):.1f}" y1="{B_GROUND_Y:.1f}" x2="{bx(3.1):.1f}" y2="{B_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{bx(-0.35):.1f}" y="{B_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    # Título Alzado B
    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(1.20):.1f}" width="460" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{bx(0.0)+10:.1f}" y="{by(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO B · ISLA CENTRAL SANTOS FINE — FRENTE DE TRABAJO (2,80×0,92 m)</text>')

    # 1. Zócalo isla retraído (h = 0,08 m)
    out.append(f'<rect x="{bx(0.05):.1f}" y="{by(0.08):.1f}" width="{2.70*S2:.1f}" height="{0.08*S2:.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.9"/>')

    # 2. Módulos bajos de trabajo (h = 0,08m a 0,90m -> h=0,82m muebles Santos):
    # Mod 1 (80 cm): Fregadero bajo encimera con gaveta reciclaje selectivo
    # Mod 2 (60 cm): Lavavajillas panelado integrado
    # Mod 3 (90 cm): Módulo placa Bora Pure (cajón cubertero interior + 2 caceroleros)
    # Mod 4 (50 cm): Gavetas auxiliares / despensa diaria
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

        # Cuerpo del mueble bajo
        out.append(f'<rect x="{im_x1:.1f}" y="{by(0.90):.1f}" width="{im_w_px:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')

        if "FREGADERO" in im_tit:
            # Gola superior
            out.append(f'<rect x="{im_x1:.1f}" y="{by(0.90):.1f}" width="{im_w_px:.1f}" height="6" fill="#0f172a"/>')
            # 2 Gavetas
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            # Silueta grifo sobre la encimera
            out.append(f'<path d="M {im_x1+im_w_px/2} {by(0.92)} L {im_x1+im_w_px/2} {by(1.30)} Q {im_x1+im_w_px/2} {by(1.40)} {im_x1+im_w_px/2-25} {by(1.38)} L {im_x1+im_w_px/2-25} {by(1.32)}" fill="none" stroke="#38bdf8" stroke-width="3.0"/>')

        elif "LAVAVAJILLAS" in im_tit:
            # Puerta continua panelada
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.52):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.38):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            out.append(f'<circle cx="{im_x1+im_w_px/2:.1f}" cy="{by(0.85):.1f}" r="3" fill="#10b981"/>')

        elif "BORA" in im_tit:
            # Gola y 2 gavetas caceroleras de 38 cm
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.48):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.48):.1f}" stroke="#475569" stroke-width="0.9"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.68):.1f}" fill="{im_col}" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">{im_tit}</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.28):.1f}" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">{im_sub}</text>')
            # Enrasado placa Bora en encimera
            out.append(f'<rect x="{im_x1+15:.1f}" y="{by(0.925):.1f}" width="{im_w_px-30:.1f}" height="6" fill="#18181b" stroke="#f59e0b" stroke-width="1.1"/>')

        elif "GAVETERO" in im_tit:
            # 3 Cajones (cubertero + 2 caceroleros)
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.64):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.64):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<line x1="{im_x1:.1f}" y1="{by(0.36):.1f}" x2="{im_x1+im_w_px:.1f}" y2="{by(0.36):.1f}" stroke="#475569" stroke-width="0.8"/>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.77):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CUBIERTOS</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.50):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CACEROLERO</text>')
            out.append(f'<text x="{im_x1+im_w_px/2:.1f}" y="{by(0.18):.1f}" fill="#cbd5e1" font-family="monospace" font-size="5.8" text-anchor="middle">CACEROLERO</text>')

        ix_cur += im_w

    # 3. Encimera Dekton de 20 mm (+0,90m a +0,92m)
    out.append(f'<rect x="{bx(0.0):.1f}" y="{by(0.92):.1f}" width="{2.80*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')
    out.append(f'<text x="{bx(1.4):.1f}" y="{by(0.92)-6:.1f}" fill="#f8fafc" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">ENCIMERA DEKTON KELYA 20 mm (COTA DE TRABAJO +0,92 m)</text>')

    # Cotas de Altura Isla B (Derecha):
    bx_dim = bx(2.80) + 25
    out.append(dim_v(by(0.00), by(0.08), bx_dim, 0, "+0,08 m", "#94a3b8", font_size=6.8))
    out.append(dim_v(by(0.08), by(0.90), bx_dim, 0, "0,82 m Muebles Santos", "#cbd5e1", font_size=6.8))
    out.append(dim_v(by(0.90), by(0.92), bx_dim, 0, "2 cm", "#f8fafc", font_size=6.5))
    out.append(dim_v(by(0.00), by(0.92), bx_dim + 35, 0, "+0,92 m COTA ENCIMERA", "#38bdf8", font_size=8.0))

    # ==========================================================================
    # SECCIÓN 3: ALZADO C - ELEVACIÓN ISLA LADO BARRA / PATIO CLAUSTRO (OESTE)
    # Vista social con voladizo y 4 taburetes altos
    # ==========================================================================
    C_OX = 180.0
    C_GROUND_Y = 1180.0  # Cota ±0,00 m en Y=1180

    def cx(val_m):
        return C_OX + val_m * S2

    def cy(val_h_m):
        return C_GROUND_Y - val_h_m * S2

    # Línea de Suelo Terminado
    out.append(f'<line x1="{cx(-0.3):.1f}" y1="{C_GROUND_Y:.1f}" x2="{cx(3.1):.1f}" y2="{C_GROUND_Y:.1f}" stroke="#e2e8f0" stroke-width="2.0"/>')
    out.append(f'<text x="{cx(-0.35):.1f}" y="{C_GROUND_Y+4:.1f}" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700" text-anchor="end">COTA ±0,00 m</text>')

    # Título Alzado C
    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(1.20):.1f}" width="460" height="22" fill="#1e293b"/>')
    out.append(f'<text x="{cx(0.0)+10:.1f}" y="{cy(1.20)+15:.1f}" fill="#38bdf8" font-family="monospace" font-size="9.0" font-weight="700">ALZADO C · ISLA SANTOS — FRENTE BARRA SOCIAL Y TABURETES (2,80×0,92 m)</text>')

    # Trasera panelada en laca mate Cashmere / roble
    out.append(f'<rect x="{cx(0.0):.1f}" y="{cy(0.90):.1f}" width="{2.80*S2:.1f}" height="{0.82*S2:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Encimera Dekton con voladizo de 35 cm para piernas
    out.append(f'<rect x="{cx(-0.05):.1f}" y="{cy(0.92):.1f}" width="{2.90*S2:.1f}" height="{0.02*S2:.1f}" fill="url(#grad-dekton)" stroke="#f8fafc" stroke-width="1.4"/>')

    # Dibujo de 4 Taburetes altos ergonómicos (asiento a +0,65 m, respaldo a +0,85 m)
    for st_x_m in [0.35, 1.05, 1.75, 2.45]:
        tx = cx(st_x_m)
        # Patas estilizadas de acero negro
        out.append(f'<line x1="{tx-16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx-10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        out.append(f'<line x1="{tx+16:.1f}" y1="{C_GROUND_Y:.1f}" x2="{tx+10:.1f}" y2="{cy(0.65):.1f}" stroke="#64748b" stroke-width="1.8"/>')
        # Reposapiés a +0,25 m
        out.append(f'<line x1="{tx-14:.1f}" y1="{cy(0.25):.1f}" x2="{tx+14:.1f}" y2="{cy(0.25):.1f}" stroke="#94a3b8" stroke-width="1.5"/>')
        # Asiento tapizado a +0,65 m
        out.append(f'<rect x="{tx-18:.1f}" y="{cy(0.67):.1f}" width="36" height="6" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.0"/>')
        # Respaldo curvado bajo a +0,82 m
        out.append(f'<line x1="{tx-12:.1f}" y1="{cy(0.67):.1f}" x2="{tx-12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<line x1="{tx+12:.1f}" y1="{cy(0.67):.1f}" x2="{tx+12:.1f}" y2="{cy(0.82):.1f}" stroke="#64748b" stroke-width="1.5"/>')
        out.append(f'<rect x="{tx-16:.1f}" y="{cy(0.84):.1f}" width="32" height="6" rx="2" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')

    out.append(f'<text x="{cx(1.4):.1f}" y="{cy(0.50):.1f}" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">VOLADIZO LIBRE 35 cm PARA PIERNAS (HUECO ERGONÓMICO)</text>')

    # Cota asiento taburete
    out.append(dim_v(cy(0.00), cy(0.65), cx(2.85), 15, "+0,65 m (Asiento Taburete)", "#38bdf8", font_size=6.8))
    out.append(dim_v(cy(0.65), cy(0.92), cx(2.85), 15, "0,27 m Holgura Piernas", "#10b981", marker="tick-emerald", font_size=6.5))

    # ==========================================================================
    # BANDA DERECHA: GUÍA TÉCNICA DE ALTURAS ERGONÓMICAS Y MECANISMOS
    # ==========================================================================
    rx = 1340
    out.append(f'<rect x="{rx}" y="30" width="430" height="1220" fill="#0f172a" stroke="#334155" stroke-width="1.0"/>')
    out.append(f'<rect x="{rx+10}" y="42" width="410" height="26" fill="#1e293b"/>')
    out.append(f'<text x="{rx+20}" y="59" fill="#38bdf8" font-family="monospace" font-size="9.5" font-weight="700">GUÍA ERGONÓMICA DE ALTURAS (CTE / UNE)</text>')

    alturas_data = [
        ("1. NIVELES VERTICALES DE EJECUCIÓN", "#38bdf8", [
            ("+2,65 m", "Falso techo continuo (yeso laminado hidrófugo)"),
            ("+2,50 m", "Fosa perimetral cortinero y carril iluminación"),
            ("+2,20 m", "Coronación superior de puertas y columnas"),
            ("+1,75 m", "Límite superior horno microondas / vapor"),
            ("+1,45 m", "Estante superior mueble desayunador pocket"),
            ("+1,30 m", "Eje display y mandos horno Bosch Serie 8"),
            ("+1,10 m", "Interruptores generales y tomas encimera C5"),
            ("+0,92 m", "Cota superior encimera Dekton (isla y desayunador)"),
            ("+0,65 m", "Plano de asiento de 4 taburetes altos de barra"),
            ("+0,30 m", "Bases de enchufe ocultas zócalo y electrodomésticos"),
            ("+0,08 m", "Zócalo retraído Santos (ventilación frigo)"),
            ("±0,00 m", "Pavimento porcelánico suelo radiante terminado"),
        ]),
        ("2. JUSTIFICACIÓN BIOMECÁNICA", "#10b981", [
            ("Encimera a +0,92 m", "Reduce un 35% la flexión lumbar al cortar"),
            ("Hornos a +0,92..1,45 m", "Manipulación de bandejas calientes a 90° de codo"),
            ("Campana Bora integrada", "Cero obstáculos visuales hacia el jardín y patio"),
            ("Voladizo barra 35 cm", "Espacio para rodillas sin golpear frentes"),
        ]),
        ("3. PRÓXIMOS PASOS ACORDADOS", "#f59e0b", [
            ("Paso A", "Validar distribución y alturas esquemáticas"),
            ("Paso B", "Trazado de tomas eléctricas (fuerza + USB-C)"),
            ("Paso C", "Diseño luminotécnico (carril magnético + LED)"),
            ("Paso D", "Detalle encuentro ventanal Cortizo y patio"),
        ]),
    ]

    sy = 85
    for cat_title, cat_col, rows in alturas_data:
        out.append(f'<text x="{rx+16}" y="{sy}" fill="{cat_col}" font-family="monospace" font-size="7.5" font-weight="700">{cat_title}</text>')
        out.append(f'<line x1="{rx+16}" y1="{sy+4}" x2="{rx+414}" y2="{sy+4}" stroke="{cat_col}" stroke-width="0.7" opacity="0.6"/>')
        sy += 16
        for k, v in rows:
            out.append(f'<text x="{rx+20}" y="{sy}" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700">{k}:</text>')
            out.append(f'<text x="{rx+85}" y="{sy}" fill="#e2e8f0" font-family="monospace" font-size="6.0">{v}</text>')
            sy += 17
        sy += 10

    out.append('</svg>')
    return "\n".join(out)


def build_cocina_interactivo_html():
    """Genera visor web interactivo e independiente para la cocina"""
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estudio Técnico de Cocina · Hogar Oleiros (Propuesta D)</title>
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
        <span>RAMA ACTIVA: feature/cocina-diseno-elevaciones</span>
      </div>
      <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
        <span>🍳 Estudio Técnico Independiente: Cocina Isla Santos</span>
      </h1>
      <p class="text-slate-400 text-sm mt-1">Geometría esquemática, alzados interiores, alturas ergonómicas normalizadas y circulaciones NHG</p>
    </div>
    <div class="flex gap-2">
      <a href="plano_cocina_planta_esquematica.svg" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 rounded-lg text-xs font-mono transition">
        Descargar SVG Planta
      </a>
      <a href="plano_cocina_elevaciones_alturas.svg" target="_blank" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 rounded-lg text-xs font-mono transition">
        Descargar SVG Alzados
      </a>
    </div>
  </header>

  <!-- Pestañas de Navegación de Planos -->
  <div class="flex border-b border-slate-800 mb-6 gap-2">
    <button onclick="showTab('planta')" id="tab-planta" class="tab-btn active px-5 py-3 font-mono text-sm border-b-2 font-bold transition flex items-center gap-2">
      <span>📐 Plano K-01: Planta Esquemática (1:20)</span>
    </button>
    <button onclick="showTab('elevaciones')" id="tab-elevaciones" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📏 Plano K-02: Alzados y Alturas (1:20)</span>
    </button>
    <button onclick="showTab('resumen')" id="tab-resumen" class="tab-btn px-5 py-3 font-mono text-sm border-b-2 border-transparent text-slate-400 hover:text-white transition flex items-center gap-2">
      <span>📋 Resumen de Cotas & Módulos</span>
    </button>
  </div>

  <!-- Contenedor Tab 1: Planta Esquemática -->
  <div id="content-planta" class="space-y-4">
    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 overflow-hidden shadow-2xl">
      <div class="flex justify-between items-center mb-3 px-2">
        <span class="text-xs font-mono text-sky-400">ISLA 2,80×1,00m · FRENTE COLUMNAS 3,60m · PASOS LIBRES >1,00m</span>
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
        <span class="text-xs font-mono text-amber-400">ALZADO COLUMNAS (H=2,65m) · ALZADO ISLA SANTOS (H=0,92m)</span>
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
      <h3 class="text-lg font-bold text-sky-400 font-mono mb-4">📐 Geometría & Distribución</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Ancho total:</strong> 3,80 m</li>
        <li>• <strong class="text-white">Longitud total:</strong> 4,60 m</li>
        <li>• <strong class="text-white">Superficie neta:</strong> 15,20 m²</li>
        <li>• <strong class="text-white">Isla Central:</strong> 2,80 × 1,00 m</li>
        <li>• <strong class="text-white">Frente Columnas:</strong> 3,60 × 0,65 m (6 col.)</li>
        <li>• <strong class="text-white">Paso a Patio:</strong> 1,15 m (holgura taburetes)</li>
        <li>• <strong class="text-white">Paso Culinario:</strong> 1,00 m (apertura cajones)</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-amber-400 font-mono mb-4">📏 Alturas Ergonómicas</h3>
      <ul class="space-y-2 text-sm text-slate-300 font-mono">
        <li>• <strong class="text-white">Falso techo:</strong> +2,65 m</li>
        <li>• <strong class="text-white">Coronación muebles:</strong> +2,20 m</li>
        <li>• <strong class="text-white">Microondas:</strong> +1,30 a +1,75 m</li>
        <li>• <strong class="text-white">Horno pirolítico:</strong> +0,70 a +1,30 m</li>
        <li>• <strong class="text-white">Tomas encimera C5:</strong> +1,10 m</li>
        <li>• <strong class="text-white">Encimera Dekton:</strong> +0,92 m</li>
        <li>• <strong class="text-white">Asiento taburetes:</strong> +0,65 m</li>
        <li>• <strong class="text-white">Zócalo técnico:</strong> +0,08 m</li>
      </ul>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
      <h3 class="text-lg font-bold text-emerald-400 font-mono mb-4">⚡ Siguiente Hoja de Ruta</h3>
      <p class="text-xs text-slate-400 mb-3">Con la geometría esquemática y alturas fijadas, podemos detallar:</p>
      <div class="space-y-2 text-sm text-slate-300">
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-sky-300">1. Enchufes y Potencias:</strong> Torres escamoteables en isla, tomas ocultas en desayunador pocket, líneas C3 (25A), C4 (16A) y C5.
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-amber-300">2. Iluminación IES:</strong> Carril magnético de superficie/empotrado sobre la isla, tiras LED cálidas 3000K bajo muebles altos.
        </div>
        <div class="p-2 rounded bg-slate-800/60 border border-slate-700">
          <strong class="text-emerald-300">3. Ventanal y Vano:</strong> Encuentro con carpintería Cortizo Cor Vision Plus y salida directa al banco de iroko del Patio Claustro.
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
    print("Generando Plano 01: Planta Esquemática de Cocina...")
    planta_svg = build_cocina_planta_svg()
    with open("plano_cocina_planta_esquematica.svg", "w", encoding="utf-8") as f:
        f.write(planta_svg)
    print(" -> Guardado en plano_cocina_planta_esquematica.svg")

    print("Generando Plano 02: Alzados Interiores y Alturas Ergonómicas...")
    elev_svg = build_cocina_elevaciones_svg()
    with open("plano_cocina_elevaciones_alturas.svg", "w", encoding="utf-8") as f:
        f.write(elev_svg)
    print(" -> Guardado en plano_cocina_elevaciones_alturas.svg")

    print("Generando Visor Web Interactivo de Cocina...")
    html_content = build_cocina_interactivo_html()
    with open("cocina_estudio_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(" -> Guardado en cocina_estudio_interactivo.html")

    print("Completado con éxito.")

if __name__ == "__main__":
    main()
