#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Detallados (1:20):
1. Patio Claustro Central (PB-07) + Escalera Volada (PB-12) + Aprovechamiento de Huecos Muertos
2. Ala Oeste de Servicio: Sala Técnica Passivhaus / Surf & Bicis (PB-13) + Lavandería (PB-13B) + Caseta Jardín (PB-13C)
Vivienda Unifamiliar en Liáns, Concello de Oleiros (A Coruña)
"""

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
      <marker id="arrow-tech" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
        <polygon points="0 0, 7 3.5, 0 7" fill="#38bdf8"/>
      </marker>

      <!-- Gradientes -->
      <linearGradient id="grad-iroko-patio" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#3b2514"/>
        <stop offset="100%" stop-color="#24170d"/>
      </linearGradient>
      <linearGradient id="grad-roble-pelda" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#2d2217"/>
        <stop offset="100%" stop-color="#1d150e"/>
      </linearGradient>
      <linearGradient id="grad-tecnico" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#182232"/>
        <stop offset="100%" stop-color="#0f1622"/>
      </linearGradient>
    </defs>
    """

def dim_h(x1, x2, y, offset_y, label, col="#38bdf8", marker="tick-45", font_size=7.5):
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

def generate_plano_patio_escalera_huecos():
    """Genera plano CAD 1:20 del Patio Claustro + Escalera Volada + Aprovechamiento de Huecos Muertos"""
    # Escala: 1 metro = 100 píxeles
    # Patio Claustro: 4,00 x 4,00 m = 400 x 400 px (X: 550 a 950, Y: 260 a 660)
    # Escalera Volada PB-12: 1,40 x 4,00 m = 140 x 400 px (X: 380 a 520, Y: 260 a 660)
    # Muro de anclaje oeste: X: 350 a 380
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">NÚCLEO CENTRAL: PATIO CLAUSTRO, ESCALERA VOLADA Y HUECOS DE ALMACENAJE (1:20)</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">PULMÓN BIOCLIMÁTICO [PB-07] · ESCALERA VOLADA ROBLE 80mm [PB-12] · APROVECHAMIENTO BAJO ESCALERA · PLANO N-01</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Acotaciones
    svg.append(dim_h(380.0, 520.0, 200, 0, "1,40 m · [PB-12] ESCALERA", "#38bdf8", font_size=8))
    svg.append(dim_h(550.0, 950.0, 200, 0, "4,00 m · [PB-07] PATIO CLAUSTRO BIOCLIMÁTICO", "#10b981", marker="tick-emerald", font_size=8.5))
    svg.append(dim_h(380.0, 950.0, 150, 0, "ANCHURA TOTAL NÚCLEO = 5,70 m", "#f59e0b", marker="tick-amber", font_size=9))
    svg.append(dim_v(260.0, 660.0, 310, 0, "LONGITUD = 4,00 m (17 PELDAÑOS)", "#38bdf8", font_size=8.5))

    # 1. PATIO CENTRAL CORRALA / CLAUSTRO BIOCLIMÁTICO [PB-07] (X: 550 a 950, Y: 260 a 660)
    svg.append("""
    <!-- PATIO CLAUSTRO [PB-07] -->
    <!-- Solera exterior: Tarima maciza Iroko sobre plots -->
    <rect x="550" y="260" width="400" height="400" fill="url(#grad-iroko-patio)" stroke="#10b981" stroke-width="1.5"/>
    """)
    # Lamas de Iroko
    for ly in range(260, 660, 12):
        svg.append(f'<line x1="550" y1="{ly}" x2="950" y2="{ly}" stroke="#451a03" stroke-width="0.5" opacity="0.6"/>')

    # Parterre ajardinado central estanco de 1,50 x 1,50 m = 150 x 150 px (X: 675 a 825, Y: 385 a 535)
    svg.append("""
    <!-- Parterre Vegetal Central y Árbol Singular (Arce Japonés) -->
    <rect x="675" y="385" width="150" height="150" rx="3" fill="#0f1f17" stroke="#10b981" stroke-width="1.8"/>
    <!-- Copa de árbol (Arce Japonés / Liquidambar) -->
    <circle cx="750" cy="460" r="60" fill="#064e3b" fill-opacity="0.45" stroke="#10b981" stroke-width="1.2" stroke-dasharray="4,2"/>
    <circle cx="750" cy="460" r="10" fill="#10b981"/>
    <!-- 4 Focos rasantes sumergibles IP68 (2700K cálido) -->
    <circle cx="700" cy="410" r="5" fill="#f59e0b"/>
    <circle cx="800" cy="410" r="5" fill="#f59e0b"/>
    <circle cx="700" cy="510" r="5" fill="#f59e0b"/>
    <circle cx="800" cy="510" r="5" fill="#f59e0b"/>
    <text x="750" y="464" fill="#f8fafc" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">ARCE JAPONÉS</text>
    <text x="750" y="476" fill="#a7f3d0" font-family="monospace" font-size="6" text-anchor="middle">(CORTEZA ROJA EN OTOÑO)</text>

    <!-- Arqueta de recogida de pluviales (Conexión a depósito 5.000 L) -->
    <rect x="570" y="280" width="24" height="24" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
    <text x="582" y="295" fill="#38bdf8" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="middle">PLUV</text>

    <!-- Carpinterías perimetrales de vidrio -->
    <!-- Norte: Cristalera fija C-05 hacia Hall/Despacho -->
    <rect x="550" y="254" width="400" height="6" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="750" y="248" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">C-05 FIJO VIDRIO AL HALL Y DESPACHO (4,00 m)</text>
    <!-- Sur: Cristalera hacia Salón -->
    <rect x="550" y="660" width="400" height="6" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="750" y="678" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">FRENTE VIDRIO VENTILACIÓN CRUZADA SALÓN</text>
    <!-- Este: Gran Corredera C-06 (2,40 m) hacia Cocina Santos -->
    <rect x="947" y="340" width="6" height="240" fill="#0b1120" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="965" y="460" fill="#f59e0b" font-family="monospace" font-size="6.8" font-weight="700" transform="rotate(90 965 460)">C-06 CORREDERA COCINA SANTOS (2,40 m)</text>
    <!-- Oeste: Barandilla vidrio Silence 10+10mm frente a escalera -->
    <line x1="520" y1="260" x2="520" y2="660" stroke="#38bdf8" stroke-width="2.8"/>
    <text x="532" y="460" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 532 460)">BARANDILLA VIDRIO SILENCE 10+10mm</text>
    """)

    # 2. ESCALERA VOLADA DE ROBLE [PB-12] (X: 380 a 520, Y: 260 a 660)
    # 17 peldaños volados de 80 mm.
    # Longitud = 4,00 m = 400 px. Cada peldaño tiene 400 / 17 = 23.53 px.
    # Huella real = 28 cm. Contrahuella = 17,65 cm.
    # Arranque en Y = 260 (PB cota ±0,00m). Ascenso hacia el Sur (Y = 660, cota +3,15m desembarco P1).
    svg.append("""
    <!-- ESCALERA VOLADA [PB-12] -->
    <!-- Muro portante oeste de anclaje estructural (X: 340 a 380) -->
    <rect x="340" y="260" width="40" height="400" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>
    """)

    step_h = 400.0 / 17.0
    for i in range(17):
        sy = 260.0 + i * step_h
        step_num = i + 1
        level = (i + 1) * 0.1765
        # Peldaño volado macizo
        svg.append(f"""
        <g class="cad-step">
          <rect x="380" y="{sy:.1f}" width="140" height="{step_h:.1f}" fill="url(#grad-roble-pelda)" stroke="#cbd5e1" stroke-width="0.7"/>
          <line x1="380" y1="{sy + step_h - 2:.1f}" x2="520" y2="{sy + step_h - 2:.1f}" stroke="#f59e0b" stroke-width="1.2" opacity="0.8"/>
          <text x="395" y="{sy + step_h/2 + 2:.1f}" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700">{step_num:02d}</text>
          <text x="490" y="{sy + step_h/2 + 2:.1f}" fill="#94a3b8" font-family="monospace" font-size="5.5">+{level:.2f}m</text>
        </g>
        """)

    # Flecha de subida
    svg.append("""
    <g class="cad-stair-arrow">
      <line x1="450" y1="280" x2="450" y2="630" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arrow-tech)"/>
      <circle cx="450" cy="280" r="3.5" fill="#38bdf8"/>
      <text x="450" y="272" fill="#38bdf8" font-family="monospace" font-size="6.8" font-weight="700" text-anchor="middle">SUBE (17 PELDAÑOS A P1)</text>
    </g>
    """)

    # 3. DETALLE DE APROVECHAMIENTO DE HUECOS MUERTOS BAJO LA ESCALERA
    # Representado como alzado/sección paralela a la izquierda (X: 60 a 300, Y: 260 a 660)
    svg.append("""
    <!-- ======================================================== -->
    <!-- ALZADO SECCIÓN: APROVECHAMIENTO DE HUECOS BAJO ESCALERA  -->
    <!-- ======================================================== -->
    <g id="huecos-muertos-seccion" transform="translate(0, 0)">
      <rect x="60" y="260" width="240" height="400" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="2"/>
      <rect x="60" y="260" width="240" height="24" fill="#1e293b"/>
      <text x="180" y="276" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="900" text-anchor="middle">SECCIÓN BAJO ESCALERA: ZONIFICACIÓN</text>

      <!-- Perfil de altura ascendente de peldaños (de 0m a 3,00m en escala vertical) -->
      <!-- Zona 1: Peldaños 1-6 (h = 0,00 a 1,06 m) -> BATERÍA DE GAVETAS PUSH -->
      <path d="M 70 300 L 290 300 L 290 370 L 70 370 Z" fill="#131c31" stroke="#38bdf8" stroke-width="1.0"/>
      <!-- 4 Gavetas extraíbles -->
      <rect x="75" y="310" width="48" height="50" rx="1" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="128" y="310" width="48" height="50" rx="1" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="181" y="310" width="48" height="50" rx="1" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="234" y="310" width="48" height="50" rx="1" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.7"/>
      <text x="180" y="385" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ZONA 1 (h &lt; 1,05m): 4 GAVETAS EXTRAÍBLES PUSH</text>
      <text x="180" y="396" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Zapatero profundo (fondo 1,20m) y calzado de invierno</text>

      <!-- Zona 2: Peldaños 7-11 (h = 1,06 a 1,94 m) -> ARMARIO ROBOT + MALETERO -->
      <rect x="70" y="415" width="220" height="95" fill="#131c31" stroke="#f59e0b" stroke-width="1.0" rx="2"/>
      <rect x="80" y="430" width="60" height="70" fill="#0f172a" stroke="#f59e0b" stroke-width="0.8"/>
      <!-- Robot aspirador en base -->
      <circle cx="110" cy="485" r="14" fill="#0b1120" stroke="#f59e0b" stroke-width="1.2"/>
      <text x="110" y="488" fill="#fde68a" font-family="monospace" font-size="5" text-anchor="middle">ROBOT</text>
      <rect x="150" y="430" width="130" height="70" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <text x="215" y="465" fill="#cbd5e1" font-family="monospace" font-size="6" text-anchor="middle">ALMACENAJE MALETAS</text>
      <text x="180" y="525" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ZONA 2 (h = 1,06-1,94m): ARMARIO TÉCNICO Y ROBÓTICA</text>
      <text x="180" y="536" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Base de carga oculta robot aspirador y maletero</text>

      <!-- Zona 3: Peldaños 12-17 (h = 1,94 a 3,00 m) -> PASO Y REGISTRO INSTALACIONES -->
      <rect x="70" y="550" width="220" height="95" fill="#131c31" stroke="#10b981" stroke-width="1.0" rx="2"/>
      <rect x="80" y="565" width="40" height="65" fill="#0f172a" stroke="#ef4444" stroke-width="0.8"/>
      <text x="100" y="600" fill="#fca5a5" font-family="monospace" font-size="5" text-anchor="middle">SHUNT</text>
      <text x="180" y="585" fill="#10b981" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ZONA 3 (h &gt; 1,94m): PASO LIBRE Y SHUNT</text>
      <text x="180" y="598" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Paso cómodo altura de hombre y registro VMC/P1</text>
    </g>
    """)

    # Paneles técnicos laterales derecha (X: 1020 a 1840)
    svg.append("""
    <g transform="translate(1020, 260)">
      <rect x="0" y="0" width="820" height="550" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="820" height="28" fill="#1e293b"/>
      <text x="15" y="19" fill="#10b981" font-family="monospace" font-size="9" font-weight="900">MEMORIA TÉCNICA · NÚCLEO BIOCLIMÁTICO Y CONEXIÓN VERTICAL</text>
      
      <g transform="translate(20, 45)">
        <text x="0" y="15" fill="#10b981" font-family="monospace" font-size="8.5" font-weight="700">1. PATIO CENTRAL CLAUSTRO [PB-07] · EL PULMÓN VERDE:</text>
        <text x="0" y="32" fill="#94a3b8" font-family="monospace" font-size="7">· Superficie: 16,00 m² (4,00 × 4,00 m libres entre paramentos de vidrio de suelo a techo).</text>
        <text x="0" y="46" fill="#94a3b8" font-family="monospace" font-size="7">· Función bioclimática: Genera un microclima húmedo y fresco en verano mediante sombraje natural</text>
        <text x="0" y="58" fill="#94a3b8" font-family="monospace" font-size="7">  y efecto chimenea térmica con ventilación cruzada noche/día hacia el salón y cocina.</text>
        <text x="0" y="72" fill="#94a3b8" font-family="monospace" font-size="7">· Tarima de Iroko FSC sobre plots regulables de polipropileno con cota cero absoluta enrasada.</text>
        <text x="0" y="86" fill="#94a3b8" font-family="monospace" font-size="7">· Parterre vegetal central de 1,50×1,50 m con arce japonés (Acer palmatum) e iluminación rasante IP68.</text>

        <text x="0" y="115" fill="#38bdf8" font-family="monospace" font-size="8.5" font-weight="700">2. ESCALERA VOLADA DE ROBLE MACIZO [PB-12]:</text>
        <text x="0" y="132" fill="#94a3b8" font-family="monospace" font-size="7">· 17 peldaños volados de 80 mm de roble macizo europeo empotrados en placa oculta en muro oeste.</text>
        <text x="0" y="146" fill="#94a3b8" font-family="monospace" font-size="7">· Geometría CTE DB-SUA: Huella H = 28,0 cm | Contrahuella CH = 17,65 cm | Ley Blondel = 63,30 cm.</text>
        <text x="0" y="160" fill="#94a3b8" font-family="monospace" font-size="7">· Anchura libre de paso = 1,10 m. Barandilla continua de vidrio Silence 10+10mm sin postes verticales.</text>
        <text x="0" y="174" fill="#94a3b8" font-family="monospace" font-size="7">· Tiras LED 2700K cálidas fresadas en la base de cada peldaño con encendido progresivo crepuscular.</text>

        <text x="0" y="205" fill="#f59e0b" font-family="monospace" font-size="8.5" font-weight="700">3. APROVECHAMIENTO QUIRÚRGICO DE HUECOS MUERTOS (3,80 m³):</text>
        <text x="0" y="222" fill="#94a3b8" font-family="monospace" font-size="7">· Zona inferior (Peldaños 1-6): 4 gavetas extraíbles push-to-open de 1,20 m de fondo para calzado.</text>
        <text x="0" y="236" fill="#94a3b8" font-family="monospace" font-size="7">· Zona media (Peldaños 7-11): Armario para robot aspirador con toma eléctrica y gaveta para maletas.</text>
        <text x="0" y="250" fill="#94a3b8" font-family="monospace" font-size="7">· Zona alta (Peldaños 12-17): Registro técnico insonorizado para el paso vertical de shunts y VMC.</text>

        <rect x="0" y="280" width="780" height="180" fill="#131c31" stroke="#334155" stroke-width="0.8"/>
        <text x="15" y="305" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700">EXPERIENCIA SENSORIAL FAMILIAR:</text>
        <text x="15" y="325" fill="#cbd5e1" font-family="monospace" font-size="7.2">Al subir o bajar de la planta primera, la barandilla de vidrio transparente permite</text>
        <text x="15" y="340" fill="#cbd5e1" font-family="monospace" font-size="7.2">mantener contacto visual permanente con el árbol del patio claustro y la luz natural.</text>
        <text x="15" y="355" fill="#cbd5e1" font-family="monospace" font-size="7.2">Al mismo tiempo, la pared bajo la escalera queda completamente limpia y enrasada,</text>
        <text x="15" y="370" fill="#cbd5e1" font-family="monospace" font-size="7.2">transformando un espacio habitualmente residual en almacenaje de alta capacidad.</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def generate_plano_ala_oeste_servicio():
    """Genera plano CAD 1:20 del Ala Oeste de Servicio: Sala Técnica Passivhaus + Lavandería + Caseta"""
    # Coordenadas según espacios/PLANTA_BAJA_TOPOLOGIA.md:
    # PB-13: Sala Técnica / Surf & Bicis (2,90 x 2,60 m = 7,60 m² útiles)
    # PB-13B: Lavandería y Plancha (2,90 x 4,00 m = 11,60 m² útiles)
    # PB-13C: Caseta Jardín / Cortacésped (2,90 x 3,20 m = 5,20 m² útiles)
    # Longitud total crujía oeste = 2,60 + 4,00 + 3,20 = 9,80 m
    # Escala: 1 metro = 90 píxeles
    # Ancho 2,90 m = 261 px (X: 200 a 461)
    # Longitud 9,80 m = 882 px (Y: 200 a 1082)
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">ALA OESTE DE SERVICIO: SALA TÉCNICA SURF, LAVANDERÍA Y CASETA (1:20)</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">CORAZÓN TÉCNICO PASSIVHAUS [PB-13] · LAVANDERÍA ELEVADA [PB-13B] · CASETA JARDÍN [PB-13C] · PLANO W-01</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Acotaciones
    svg.append(dim_h(200.0, 461.0, 160, 0, "ANCHURA LIBRE CRUJÍA OESTE = 2,90 m", "#38bdf8", font_size=8.5))
    svg.append(dim_v(200.0, 434.0, 150, 0, "2,60 m · [PB-13] SALA TÉCNICA SURF", "#38bdf8", font_size=7.5))
    svg.append(dim_v(434.0, 794.0, 150, 0, "4,00 m · [PB-13B] LAVANDERÍA Y PLANCHA", "#38bdf8", font_size=7.5))
    svg.append(dim_v(794.0, 1082.0, 150, 0, "3,20 m · [PB-13C] CASETA JARDÍN", "#f59e0b", marker="tick-amber", font_size=7.5))
    svg.append(dim_v(200.0, 1082.0, 100, 0, "LONGITUD TOTAL CRUJÍA OESTE = 9,80 m", "#f59e0b", marker="tick-amber", font_size=9))

    # SOLERAS
    # PB-13: Hormigón pulido continuo con sellador epoxi C3 cota -0,05m
    svg.append('<rect x="200" y="200" width="261" height="234" fill="#131c31"/>')
    # PB-13B: Porcelánico C2 gris neutro rectificado cota ±0,00m
    svg.append('<rect x="200" y="434" width="261" height="360" fill="#182232"/>')
    # PB-13C: Hormigón fratasado exterior caseta
    svg.append('<rect x="200" y="794" width="261" height="288" fill="#101827"/>')

    # Muros perimetrales
    svg.append('<rect x="170" y="200" width="30" height="882" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    svg.append('<rect x="461" y="200" width="30" height="882" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    svg.append('<rect x="200" y="170" width="261" height="30" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    svg.append('<rect x="200" y="1082" width="261" height="30" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')

    # Tabiques divisorios interiores
    # Entre Sala Técnica y Lavandería (Y = 434) con puerta batiente P-03 (0,82m)
    svg.append("""
    <rect x="200" y="430" width="70" height="8" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <rect x="345" y="430" width="116" height="8" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>
    <!-- Puerta P-03 (0,82m = 74px) -->
    <line x1="270" y1="434" x2="344" y2="434" stroke="#475569" stroke-width="1.0" stroke-dasharray="2,2"/>
    <line x1="270" y1="434" x2="270" y2="500" stroke="#cbd5e1" stroke-width="1.8"/>
    <path d="M 344 434 A 74 74 0 0 1 270 500" fill="none" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3,3"/>
    <text x="310" y="450" fill="#cbd5e1" font-family="monospace" font-size="6.5">P-03 0,82m</text>
    """)

    # Entre Lavandería y Caseta (Y = 794) con tabique estanco acústico
    svg.append('<rect x="200" y="790" width="261" height="8" fill="#334155" stroke="#cbd5e1" stroke-width="0.8"/>')

    # 1. EQUIPAMIENTO DETALLADO SALA TÉCNICA PASSIVHAUS / SURF & BICIS [PB-13]
    svg.append("""
    <!-- SALA TÉCNICA [PB-13] -->
    <!-- Aerotermia Vaillant aroTHERM + ACS 300L Inox (X: 370 a 455, Y: 210 a 280) -->
    <rect x="370" y="210" width="85" height="70" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>
    <circle cx="412" cy="245" r="22" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>
    <text x="412" y="242" fill="#38bdf8" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">AEROTERMIA</text>
    <text x="412" y="253" fill="#f8fafc" font-family="monospace" font-size="6" font-weight="900" text-anchor="middle">ACS 300L</text>

    <!-- Central VMC Zehnder ComfoAir Q350 (X: 370 a 455, Y: 295 a 355) -->
    <rect x="370" y="295" width="85" height="60" rx="2" fill="#0b1120" stroke="#10b981" stroke-width="1.2"/>
    <circle cx="395" cy="325" r="8" fill="#1e293b" stroke="#10b981" stroke-width="0.8"/>
    <circle cx="430" cy="325" r="8" fill="#1e293b" stroke="#10b981" stroke-width="0.8"/>
    <text x="412" y="348" fill="#10b981" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">VMC ZEHNDER Q350</text>

    <!-- Inversor Solar 6kW + Batería Litio 10kWh (X: 370 a 455, Y: 370 a 420) -->
    <rect x="380" y="370" width="75" height="50" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="1.0"/>
    <text x="417" y="392" fill="#f59e0b" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">INVERSOR FV 6kW</text>
    <text x="417" y="404" fill="#fde68a" font-family="monospace" font-size="5.5" text-anchor="middle">+ BATERÍA 10kWh</text>

    <!-- ZONA SURF: Rack vertical acolchado para 4 tablas de surf (Pared Oeste, X: 210 a 240, Y: 210 a 330) -->
    <rect x="210" y="210" width="30" height="120" fill="none" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4,2"/>
    <line x1="210" y1="240" x2="240" y2="240" stroke="#f59e0b" stroke-width="1.0"/>
    <line x1="210" y1="270" x2="240" y2="270" stroke="#f59e0b" stroke-width="1.0"/>
    <line x1="210" y1="300" x2="240" y2="300" stroke="#f59e0b" stroke-width="1.0"/>
    <text x="225" y="345" fill="#f59e0b" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">RACK SURF (4 TABLAS)</text>

    <!-- Pila de lavado profundo en acero inox + manguera termostática (X: 210 a 260, Y: 360 a 420) -->
    <rect x="210" y="360" width="50" height="60" rx="1" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>
    <circle cx="235" cy="390" r="14" fill="#0b1120" stroke="#38bdf8" stroke-width="0.8"/>
    <text x="235" y="415" fill="#38bdf8" font-family="monospace" font-size="5.5" text-anchor="middle">PILA ENDULZADO</text>

    <!-- Sumidero sifónico central en suelo cota -0,05m -->
    <rect x="300" y="310" width="16" height="16" fill="#0b1120" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="308" y="338" fill="#cbd5e1" font-family="monospace" font-size="5.5" text-anchor="middle">SUMIDERO</text>
    """)

    # 2. EQUIPAMIENTO DETALLADO LAVANDERÍA Y PLANCHA OESTE [PB-13B]
    svg.append("""
    <!-- LAVANDERÍA Y PLANCHA [PB-13B] -->
    <!-- Torre Lavadora + Secadora elevadas +30cm (X: 210 a 270, Y: 460 a 530) -->
    <rect x="210" y="460" width="60" height="70" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="1.4"/>
    <circle cx="240" cy="495" r="18" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>
    <text x="240" y="492" fill="#38bdf8" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="middle">TORRE LAV</text>
    <text x="240" y="502" fill="#f8fafc" font-family="monospace" font-size="5.5" font-weight="900" text-anchor="middle">+ SECADORA</text>
    <text x="240" y="542" fill="#38bdf8" font-family="monospace" font-size="5.8" text-anchor="middle">ELEVADA +30cm</text>

    <!-- Bancada corrida de planchado y doblado 2,40m con fregadero auxiliar (X: 210 a 270, Y: 560 a 760) -->
    <rect x="210" y="560" width="60" height="200" rx="2" fill="#131c31" stroke="#cbd5e1" stroke-width="1.0"/>
    <rect x="215" y="580" width="40" height="40" rx="1" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
    <circle cx="235" cy="600" r="3" fill="#38bdf8"/>
    <text x="240" y="660" fill="#cbd5e1" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(-90 240 660)">BANCADA PLANCHA 2,40m</text>

    <!-- Puerta vidriera de salida al tendedero exterior cubierto oeste (X = 200, Y: 600 a 680) -->
    <rect x="196" y="600" width="8" height="80" fill="#0b1120" stroke="#f59e0b" stroke-width="1.4"/>
    <text x="180" y="640" fill="#f59e0b" font-family="monospace" font-size="6" font-weight="700" transform="rotate(-90 180 640)">SALIDA TENDEDERO</text>

    <!-- Ventilación VMC Extracción 45 m³/h -->
    <rect x="360" y="470" width="20" height="20" fill="#0b1120" stroke="#10b981" stroke-width="1.0"/>
    <text x="370" y="502" fill="#10b981" font-family="monospace" font-size="5.5" text-anchor="middle">VMC-E 45m³/h</text>
    """)

    # 3. EQUIPAMIENTO CASETA DE JARDÍN / CORTACÉSPED [PB-13C]
    svg.append("""
    <!-- CASETA JARDÍN [PB-13C] -->
    <!-- Espacio libre cortacésped y herramientas (X: 220 a 440, Y: 820 a 1050) -->
    <rect x="220" y="820" width="120" height="80" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="1.0"/>
    <text x="280" y="865" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">ROBOT CORTACÉSPED</text>

    <!-- Estanterías perimetrales de jardín -->
    <rect x="400" y="820" width="50" height="230" fill="#131c31" stroke="#cbd5e1" stroke-width="0.8"/>
    <text x="425" y="940" fill="#cbd5e1" font-family="monospace" font-size="6.5" transform="rotate(90 425 940)">ESTANTES HERRAMIENTAS</text>

    <!-- Puerta de acceso desde Porche Sur (Y = 1082, X: 300 a 380) -->
    <rect x="300" y="1078" width="80" height="8" fill="#0b1120" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="340" y="1068" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">PUERTA CASETA (DESDE PORCHE)</text>
    """)

    # Rótulos de estancias
    svg.append("""
    <g class="room-stamp" transform="translate(290, 250)">
      <rect x="0" y="0" width="160" height="42" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="0.9"/>
      <text x="80" y="16" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">[PB-13] SALA TÉCNICA SURF</text>
      <text x="80" y="28" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">S.Útil: 7,60 m²</text>
      <text x="80" y="38" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Epoxi C3 · Z=-0,05m</text>
    </g>

    <g class="room-stamp" transform="translate(290, 700)">
      <rect x="0" y="0" width="160" height="42" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="0.9"/>
      <text x="80" y="16" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">[PB-13B] LAVANDERÍA Y PLANCHA</text>
      <text x="80" y="28" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">S.Útil: 11,60 m²</text>
      <text x="80" y="38" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Porcelánico C2 · Z=±0,00m</text>
    </g>

    <g class="room-stamp" transform="translate(250, 940)">
      <rect x="0" y="0" width="150" height="42" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="0.9"/>
      <text x="75" y="16" fill="#f59e0b" font-family="monospace" font-size="7" font-weight="900" text-anchor="middle">[PB-13C] CASETA JARDÍN</text>
      <text x="75" y="28" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">S.Útil: 5,20 m²</text>
      <text x="75" y="38" fill="#94a3b8" font-family="monospace" font-size="5.8" text-anchor="middle">Hormigón Fratasado</text>
    </g>
    """)

    # Paneles de memoria técnica ala oeste (X: 550 a 1840)
    svg.append("""
    <g transform="translate(560, 200)">
      <rect x="0" y="0" width="1280" height="880" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="1280" height="32" fill="#1e293b"/>
      <text x="20" y="22" fill="#38bdf8" font-family="monospace" font-size="10" font-weight="900">MEMORIA TÉCNICA · ALA OESTE DE SERVICIO Y CORAZÓN PASSIVHAUS</text>
      
      <g transform="translate(30, 60)">
        <text x="0" y="20" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="700">1. SALA TÉCNICA / SURF &amp; BICIS [PB-13] (7,60 m² útiles · Cota -0,05 m):</text>
        <text x="0" y="40" fill="#94a3b8" font-family="monospace" font-size="7.5">· Climatización y ACS: Bomba de calor aerotérmica Vaillant aroTHERM plus con depósito interacumulador de 300 litros inox.</text>
        <text x="0" y="55" fill="#94a3b8" font-family="monospace" font-size="7.5">· Ventilación Mecánica Controlada: Unidad central Zehnder ComfoAir Q350 de doble flujo con recuperación entálpica &gt;90%.</text>
        <text x="0" y="70" fill="#94a3b8" font-family="monospace" font-size="7.5">· Fotovoltaica y Acumulación: Inversor solar híbrido de 6 kW + cuadro de protecciones CC y espacio para batería de 10 kWh.</text>
        <text x="0" y="85" fill="#94a3b8" font-family="monospace" font-size="7.5">· Deporte Atlántico: Racks acolchados para 4 tablas de surf, pila de lavado hondo en acero inox con manguera termostática,</text>
        <text x="0" y="100" fill="#94a3b8" font-family="monospace" font-size="7.5">  suelo continuo de hormigón epoxi con desnivel de 5 cm y sumidero sifónico para desagüe de agua salada y arena.</text>

        <text x="0" y="140" fill="#10b981" font-family="monospace" font-size="9" font-weight="700">2. LAVANDERÍA Y PLANCHA OESTE [PB-13B] (11,60 m² útiles · Cota ±0,00 m):</text>
        <text x="0" y="160" fill="#94a3b8" font-family="monospace" font-size="7.5">· Ergonomía de lavado: Torre de lavadora y secadora elevada a +30 cm para carga y descarga frontal sin agacharse.</text>
        <text x="0" y="175" fill="#94a3b8" font-family="monospace" font-size="7.5">· Bancada continua de planchado y doblado de 2,40 m en estratificado antibacteriano con fregadero de servicio y grifo caño alto.</text>
        <text x="0" y="190" fill="#94a3b8" font-family="monospace" font-size="7.5">· Secado pasivo invernal: Extracción forzada VMC-E de 45 m³/h que seca la ropa tendida en el interior en días de temporal.</text>
        <text x="0" y="205" fill="#94a3b8" font-family="monospace" font-size="7.5">· Salida directa a tendedero exterior cubierto en fachada oeste y ventana de tejado Velux para iluminación cenital natural.</text>

        <text x="0" y="245" fill="#f59e0b" font-family="monospace" font-size="9" font-weight="700">3. CASETA DE JARDÍN / CORTACÉSPED [PB-13C] (5,20 m² útiles):</text>
        <text x="0" y="265" fill="#94a3b8" font-family="monospace" font-size="7.5">· Acceso directo exterior desde el Porche Sur techado mediante puerta enrasada de lamas de madera de Iroko.</text>
        <text x="0" y="280" fill="#94a3b8" font-family="monospace" font-size="7.5">· Almacenamiento limpio para robot cortacésped, herramientas de jardinería, mangueras y cojines del salón exterior en invierno.</text>
        <text x="0" y="295" fill="#94a3b8" font-family="monospace" font-size="7.5">· Actúa como escudo cortavientos frente a las borrascas del suroeste protegiendo el porche sur y el salón.</text>

        <rect x="0" y="340" width="1220" height="460" fill="#131c31" stroke="#38bdf8" stroke-width="0.8"/>
        <text x="25" y="375" fill="#f8fafc" font-family="monospace" font-size="8.5" font-weight="700">INTEGRACIÓN EN EL MASTER PLAN DE PLANTA BAJA (AJUSTE COMO UN GUANTE):</text>
        
        <text x="25" y="410" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="700">· COHERENCIA DIMENSIONAL:</text>
        <text x="25" y="425" fill="#cbd5e1" font-family="monospace" font-size="7">La crujía oeste mantiene el ancho estricto de 2,90 m libres desde la fachada norte hasta el porche sur, alineada con los ejes A y B.</text>

        <text x="25" y="455" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">· SECUENCIA HIGRÓTÉRICA INTELIGENTE:</text>
        <text x="25" y="470" fill="#cbd5e1" font-family="monospace" font-size="7">Llegada de la playa -&gt; Entrada a Zaguán Mudroom (P-01) -&gt; Paso con traje mojado a Sala Surf (P-02) -&gt; Endulzado en pila</text>
        <text x="25" y="485" fill="#cbd5e1" font-family="monospace" font-size="7">-&gt; Colocación en rack secador -&gt; Paso a Lavandería (P-03) -&gt; Entrada limpia y seca a la zona noble de la vivienda.</text>

        <text x="25" y="515" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700">· CONFORT ACÚSTICO SALÓN (PB-10):</text>
        <text x="25" y="530" fill="#cbd5e1" font-family="monospace" font-size="7">La pared compartida entre la lavandería y el salón cuenta con doble placa Habito con lana de roca (Rw &gt;= 50 dB),</text>
        <text x="25" y="545" fill="#cbd5e1" font-family="monospace" font-size="7">garantizando silencio absoluto en el salón junto a la chimenea incluso durante el centrifugado a 1.400 rpm.</text>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def main():
    print("=== Generando Planos CAD 1:20 de Patio, Escalera y Ala Oeste ===")
    
    # 1. Patio Claustro + Escalera Volada + Huecos Muertos
    svg_p = generate_plano_patio_escalera_huecos()
    with open("plano_patio_escalera_huecos_planta.svg", "w", encoding="utf-8") as f:
        f.write(svg_p)
    print("✓ plano_patio_escalera_huecos_planta.svg generado")
    ET.parse("plano_patio_escalera_huecos_planta.svg")
    print("✓ XML VÁLIDO: plano_patio_escalera_huecos_planta.svg")

    # 2. Ala Oeste de Servicio
    svg_w = generate_plano_ala_oeste_servicio()
    with open("plano_ala_oeste_servicio_planta.svg", "w", encoding="utf-8") as f:
        f.write(svg_w)
    print("✓ plano_ala_oeste_servicio_planta.svg generado")
    ET.parse("plano_ala_oeste_servicio_planta.svg")
    print("✓ XML VÁLIDO: plano_ala_oeste_servicio_planta.svg")

if __name__ == "__main__":
    main()
