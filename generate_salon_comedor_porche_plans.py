#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Detallados (1:20) del Salón, Comedor Principal y Porche Sur Techado
Vivienda Unifamiliar en Liáns, Concello de Oleiros (A Coruña)
Crujía Sur Vividera:
- PB-10: Salón Principal con Chimenea Estanca Passivhaus (26,50 m² útiles, 4,40 x 6,00 m)
- PB-11: Comedor Principal Interior (17,50 m² útiles, 5,00 x 3,50 m, mesa 10-12 Pax)
- PB-14: Porche Sur Techado Expandido (32,55 m² útiles, 10,84 x 3,00 m, enrasado cota cero)
- Cerramiento Singular C-07: Gran Corredera Elevable CORTIZO Cor Vision Plus (7,50 m) con guía oculta embutida
- Chimenea Passivhaus estanca de leña en pared oeste con bancada corrida suspendida de roble y aplacado de caliza
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

      <!-- Gradientes materiales -->
      <linearGradient id="grad-caliza" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#2a2e38"/>
        <stop offset="50%" stop-color="#1f242d"/>
        <stop offset="100%" stop-color="#171b22"/>
      </linearGradient>
      <linearGradient id="grad-iroko" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#3d2817"/>
        <stop offset="50%" stop-color="#2c1d11"/>
        <stop offset="100%" stop-color="#1f140b"/>
      </linearGradient>
      <linearGradient id="grad-fuego" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#ef4444" stop-opacity="0.8"/>
        <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="#eab308" stop-opacity="0.7"/>
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

def generate_plano_salon_comedor_porche():
    """Genera plano CAD 1:20 de Planta: Salón + Comedor + Porche Sur Techado"""
    # Escala: 1 metro = 90 píxeles
    # Origen X = 200 (Pared Oeste del Salón)
    # Salón: 4,40 m ancho = 396 px -> X: 200 a 596
    # Comedor: 5,00 m ancho = 450 px -> X: 596 a 1046
    # Prolongación Este hacia jardín: X: 1046 a 1180
    # Longitud total porche = 10,84 m = 975.6 px (X: 200 a 1175.6)
    
    # Eje Y:
    # Límite Norte (Encuentro con Patio Claustro en Salón y Cocina en Comedor): Y = 260
    # Fondo Salón y Comedor: 6,00 m = 540 px -> Y: 260 a 800
    # Línea Gran Corredera C-07: Y = 800 (Longitud 7,50 m = 675 px, X: 300 a 975)
    # Fondo Porche Sur Techado: 3,00 m = 270 px -> Y: 800 a 1070
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1220" width="100%" height="100%" style="background-color:#070b14;">')
    svg.append(svg_defs_technical())
    svg.append('<rect width="1920" height="1220" fill="url(#grid-cad-major)"/>')

    # Marco
    svg.append("""
    <rect x="30" y="30" width="1860" height="1160" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="36" y="36" width="1848" height="1148" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    <g transform="translate(60, 70)">
      <text x="0" y="0" fill="#38bdf8" font-family="monospace" font-size="20" font-weight="900" letter-spacing="2">CRUJÍA SUR: SALÓN PRINCIPAL, COMEDOR Y PORCHE TECHADO (1:20)</text>
      <text x="0" y="24" fill="#94a3b8" font-family="monospace" font-size="11">FUSIÓN INTERIOR-EXTERIOR COTA CERO · GRAN CORREDERA C-07 (7,50m) · CHIMENEA PASSIVHAUS · PLANO S-01</text>
      <line x1="0" y1="36" x2="1800" y2="36" stroke="#334155" stroke-width="1.2"/>
    </g>
    """)

    # Acotaciones superiores e intermedias
    svg.append(dim_h(200.0, 596.0, 180, 0, "4,40 m · [PB-10] SALÓN PRINCIPAL", "#38bdf8", font_size=8.5))
    svg.append(dim_h(596.0, 1046.0, 180, 0, "5,00 m · [PB-11] COMEDOR INTERIOR", "#38bdf8", font_size=8.5))
    svg.append(dim_h(200.0, 1175.6, 130, 0, "FACHADA SUR TOTAL = 10,84 m · [PB-14] PORCHE TECHADO SUR", "#f59e0b", marker="tick-amber", font_size=9.5))

    # Acotaciones laterales
    svg.append(dim_v(260.0, 800.0, 140, 0, "FONDO SALÓN/COMEDOR = 6,00 m", "#38bdf8", font_size=8.5))
    svg.append(dim_v(800.0, 1070.0, 140, 0, "FONDO PORCHE = 3,00 m", "#f59e0b", marker="tick-amber", font_size=8.5))

    # SOLERAS (Relleno base)
    # Interior Salón y Comedor: Caliza Natural Apomazada 120x120cm
    svg.append('<rect x="200" y="260" width="846" height="540" fill="url(#grad-caliza)"/>')
    # Modulación de juntas de Caliza 120x120cm (108 px en escala 90px=1m)
    for jx in range(200, 1046, 108):
        svg.append(f'<line x1="{jx}" y1="260" x2="{jx}" y2="800" stroke="#334155" stroke-width="0.4" opacity="0.6"/>')
    for jy in range(260, 800, 108):
        svg.append(f'<line x1="200" y1="{jy}" x2="1046" y2="{jy}" stroke="#334155" stroke-width="0.4" opacity="0.6"/>')

    # Exterior Porche Sur: Tarima maciza de Iroko FSC (Lamas de 120mm sobre plots)
    svg.append('<rect x="200" y="800" width="975.6" height="270" fill="url(#grad-iroko)"/>')
    # Trazado de lamas de Iroko paralelas a fachada
    for ly in range(800, 1070, 11):
        svg.append(f'<line x1="200" y1="{ly}" x2="1175.6" y2="{ly}" stroke="#451a03" stroke-width="0.5" opacity="0.7"/>')

    # MUROS ESTRUCTURALES Y ENCUENTROS
    # Muro Oeste (X = 170 a 200): Separa salón de Caseta de jardín y Lavandería
    svg.append('<rect x="170" y="260" width="30" height="810" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Muro Norte Comedor / Cocina (Y = 230 a 260) con emboquillado diáfano 2,40m (X: 740 a 956)
    svg.append('<rect x="596" y="230" width="144" height="30" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    svg.append('<rect x="956" y="230" width="90" height="30" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Paso diáfano a Cocina Santos: X: 740 a 956 (2,40 m)
    svg.append("""
    <g class="cad-opening">
      <line x1="740" y1="260" x2="956" y2="260" stroke="#38bdf8" stroke-width="1.0" stroke-dasharray="4,3"/>
      <rect x="780" y="248" width="140" height="18" fill="#0b1120" stroke="#38bdf8" stroke-width="0.6"/>
      <text x="850" y="260" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">PASO DIÁFANO A COCINA SANTOS (2,40 m)</text>
    </g>
    """)

    # Muro Norte Salón / Patio Claustro (Y = 260, X: 200 a 596): Cristalera C-05 hacia el patio ajardinado
    svg.append("""
    <!-- Cristalera Norte Salón al Patio Claustro -->
    <rect x="240" y="254" width="356" height="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
    <line x1="240" y1="260" x2="596" y2="260" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="418" y="246" fill="#38bdf8" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">CRISTALERA PANORÁMICA AL PATIO CENTRAL CLAUSTRO (4,00 m)</text>
    """)

    # Muro Este Comedor (X = 1046 a 1076, Y: 260 a 800) con ventanal y salida lateral
    svg.append('<rect x="1046" y="260" width="30" height="540" fill="url(#hatch-wall)" stroke="#cbd5e1" stroke-width="1.2"/>')
    svg.append("""
    <!-- Ventanal Este Comedor con puerta balconera -->
    <rect x="1042" y="440" width="12" height="200" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
    <line x1="1046" y1="440" x2="1046" y2="640" stroke="#38bdf8" stroke-width="1.8"/>
    <text x="1065" y="540" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" transform="rotate(90 1065 540)">VENTANAL ESTE COMEDOR</text>
    """)

    # Pilares Estructurales
    pillars = [
        (200.0, 260.0, "P-08"),
        (596.0, 260.0, "P-09"),
        (200.0, 800.0, "P-10"),
        (1046.0, 800.0, "P-11"),
        (200.0, 1070.0, "P-12 (Porche)"),
        (1175.6, 1070.0, "P-13 (Porche)")
    ]
    for px, py, plabel in pillars:
        svg.append(f"""
        <g class="cad-pillar">
          <rect x="{px-12:.1f}" y="{py-12:.1f}" width="24" height="24" fill="url(#hatch-pillar)" stroke="#f8fafc" stroke-width="1.4"/>
          <text x="{px+16:.1f}" y="{py+14:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.8" font-weight="700">{plabel}</text>
        </g>
        """)

    # CERRAMIENTO SINGULAR C-07: GRAN CORREDERA ELEVABLE SUR (7,50 m)
    # Longitud: 7,50 m = 675 px (X: 300 a 975, Y = 800)
    # 3 Hojas correderas embutidas con guía oculta a cota cero
    svg.append("""
    <!-- ======================================================== -->
    <!-- CERRAMIENTO C-07: CORREDERA ELEVABLE CORTIZO COR VISION PLUS -->
    <!-- ======================================================== -->
    <g id="carpinteria-C07">
      <!-- Guía embutida oculta en pavimento -->
      <rect x="290" y="794" width="695" height="12" fill="#0b1120" stroke="#f59e0b" stroke-width="1.4"/>
      <!-- Hoja 1 (Fija/Corredera Oeste): X: 300 a 525 -->
      <rect x="300" y="796" width="225" height="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="412" cy="798" r="2.5" fill="#f59e0b"/>
      <!-- Hoja 2 (Corredera Central): X: 525 a 750 -->
      <rect x="525" y="800" width="225" height="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="637" cy="802" r="2.5" fill="#f59e0b"/>
      <!-- Hoja 3 (Corredera Este): X: 750 a 975 -->
      <rect x="750" y="796" width="225" height="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="862" cy="798" r="2.5" fill="#f59e0b"/>

      <!-- Rótulo y especificación técnica de la corredera C-07 -->
      <rect x="420" y="776" width="460" height="20" fill="#0b1120" stroke="#f59e0b" stroke-width="0.8" rx="2"/>
      <text x="650" y="790" fill="#fde68a" font-family="monospace" font-size="7.5" font-weight="900" text-anchor="middle">
        C-07 · CORREDERA CORTIZO COR VISION PLUS (7,50 × 2,70 m) · GUÍA EMBUTIDA COTA CERO
      </text>

      <!-- Flechas indicadoras de apertura telescópica -->
      <line x1="600" y1="816" x2="400" y2="816" stroke="#f59e0b" stroke-width="1.2" marker-end="url(#arrow-tech)"/>
      <line x1="700" y1="816" x2="900" y2="816" stroke="#f59e0b" stroke-width="1.2" marker-end="url(#arrow-tech)"/>
      <text x="650" y="828" fill="#f59e0b" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">APERTURA BIDIRECCIONAL CONTINUA (APERTURA LIBRE HASTA 5,00 m)</text>
    </g>
    """)

    # 1. AMUEBLAMIENTO DETALLADO DEL SALÓN PRINCIPAL [PB-10]
    # - Chimenea estanca Passivhaus en X: 200 a 240, Y: 460 a 540 con bancada corrida suspendida
    # - Conjunto sofá chaise longue / sofá en L de 3,60 x 2,80 m
    # - Mesa de centro en roble y metal negro 1,40 x 0,80 m
    # - Butacas de diseño contemporáneo
    # - Mueble bajo audiovisual de roble con TV 85" empotrada
    svg.append("""
    <!-- ============================================== -->
    <!-- AMUEBLAMIENTO CANÓNICO SALÓN PRINCIPAL [PB-10] -->
    <!-- ============================================== -->
    <!-- Chimenea Passivhaus Estanca de Leña (Pared Oeste) -->
    <g id="chimenea-salon">
      <!-- Aplacado de caliza/mortero mineral pared chimenea (X: 200 a 250, Y: 440 a 620) -->
      <rect x="200" y="440" width="50" height="180" fill="#131c31" stroke="#cbd5e1" stroke-width="1.0"/>
      <!-- Hogar estanco de hierro fundido con cristal a 3 caras -->
      <rect x="205" y="500" width="40" height="60" fill="#0b1120" stroke="#f59e0b" stroke-width="1.6"/>
      <rect x="215" y="515" width="20" height="30" fill="url(#grad-fuego)" rx="2"/>
      <circle cx="225" cy="530" r="12" fill="none" stroke="#ef4444" stroke-width="1.0" stroke-dasharray="2,2"/>
      <!-- Conducto humos inoxidable aislado Ø200mm -->
      <circle cx="225" cy="505" r="8" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.2"/>
      <text x="225" y="490" fill="#fca5a5" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">CHIMENEA ESTANCA</text>
      <!-- Bancada corrida suspendida en roble tostado (X: 200 a 235, Y: 380 a 680) -->
      <rect x="200" y="380" width="35" height="300" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8"/>
      <text x="212" y="650" fill="#38bdf8" font-family="monospace" font-size="6" transform="rotate(-90 212 650)">BANCADA SUSPENDIDA ROBLE</text>
    </g>

    <!-- Sofá principal en L (3,60 × 2,60 m): X: 300 a 540, Y: 420 a 640 -->
    <g id="sofa-salon">
      <path d="M 300 420 L 540 420 L 540 500 L 380 500 L 380 660 L 300 660 Z" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>
      <path d="M 310 430 L 530 430 L 530 490 L 370 490 L 370 650 L 310 650 Z" fill="#0f172a" stroke="#475569" stroke-width="0.8"/>
      <!-- Almohadones modulares -->
      <line x1="380" y1="430" x2="380" y2="490" stroke="#334155" stroke-width="0.8"/>
      <line x1="450" y1="430" x2="450" y2="490" stroke="#334155" stroke-width="0.8"/>
      <line x1="310" y1="550" x2="370" y2="550" stroke="#334155" stroke-width="0.8"/>
      <!-- Mesa de centro (1,40 × 0,80 m = 126 × 72 px) -->
      <rect x="400" y="520" width="126" height="72" rx="2" fill="#131c31" stroke="#38bdf8" stroke-width="1.0"/>
      <text x="463" y="560" fill="#f8fafc" font-family="monospace" font-size="7" font-weight="700" text-anchor="middle">MESA CENTRO 1,40×0,80</text>
      <!-- Butaca auxiliar tapizada en lino -->
      <circle cx="560" cy="560" r="28" fill="#1e293b" stroke="#94a3b8" stroke-width="1.0"/>
      <text x="560" y="563" fill="#cbd5e1" font-family="monospace" font-size="6" text-anchor="middle">BUTACA</text>
    </g>

    <!-- Mueble Audiovisual y TV 85" (Pared Norte junto a cristalera patio) -->
    <rect x="340" y="275" width="220" height="32" rx="2" fill="#0b1120" stroke="#38bdf8" stroke-width="1.0"/>
    <rect x="360" y="280" width="180" height="8" rx="1" fill="#38bdf8"/>
    <text x="450" y="300" fill="#38bdf8" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MUEBLE TV 85" INTEGRADO</text>
    """)

    # 2. AMUEBLAMIENTO DETALLADO DEL COMEDOR PRINCIPAL [PB-11]
    # - Gran Mesa de Comedor de Roble Macizo de 3,00 × 1,10 m (270 × 99 px)
    # - 10-12 Sillas ergonómicas de diseño nórdico con reposabrazos
    # - Lámpara suspendida escultural central con regulación DALI
    # - Perímetro de circulación libre > 1,20 m conforme a NHG
    svg.append("""
    <!-- ============================================== -->
    <!-- AMUEBLAMIENTO CANÓNICO COMEDOR INTERIOR [PB-11]-->
    <!-- ============================================== -->
    <!-- Gran Mesa de Comedor 3,00 x 1,10 m (X: 680 a 950, Y: 450 a 549) -->
    <g id="mesa-comedor">
      <rect x="680" y="450" width="270" height="99" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <!-- Textura de tablones de roble macizo -->
      <line x1="680" y1="483" x2="950" y2="483" stroke="#334155" stroke-width="0.6"/>
      <line x1="680" y1="516" x2="950" y2="516" stroke="#334155" stroke-width="0.6"/>
      <!-- Lámpara lineal suspendida DALI en centro de mesa -->
      <line x1="720" y1="499.5" x2="910" y2="499.5" stroke="#f59e0b" stroke-width="3.0"/>
      <circle cx="720" cy="499.5" r="4" fill="#f59e0b"/>
      <circle cx="815" cy="499.5" r="5" fill="#f59e0b"/>
      <circle cx="910" cy="499.5" r="4" fill="#f59e0b"/>
      <text x="815" y="493" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">LÁMPARA SUSPENDIDA DALI (2700K)</text>
      <text x="815" y="525" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="900" text-anchor="middle">MESA COMEDOR ROBLE (10-12 PAX) 3,00×1,10 m</text>

      <!-- 10 Sillas de comedor (5 arriba, 5 abajo, 2 cabeceras) -->
      <!-- Cabecera Oeste -->
      <rect x="650" y="475" width="22" height="48" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <!-- Cabecera Este -->
      <rect x="958" y="475" width="22" height="48" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <!-- Fila Norte (5 sillas) -->
      <rect x="700" y="420" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="755" y="420" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="810" y="420" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="865" y="420" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="920" y="420" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <!-- Fila Sur (5 sillas) -->
      <rect x="700" y="557" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="755" y="557" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="810" y="557" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="865" y="557" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <rect x="920" y="557" width="45" height="22" rx="2" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
    </g>

    <!-- Aparador bajo de comedor adosado a pared este -->
    <rect x="1010" y="320" width="30" height="180" rx="1.5" fill="#131c31" stroke="#cbd5e1" stroke-width="0.9"/>
    <text x="1025" y="410" fill="#cbd5e1" font-family="monospace" font-size="6" text-anchor="middle" transform="rotate(90 1025 410)">APARADOR VAJILLA</text>
    """)

    # 3. AMUEBLAMIENTO DETALLADO DEL PORCHE SUR TECHADO [PB-14]
    # - Zona Salón Exterior / Chill-out (Oeste): Conjunto sofás de exterior en Iroko y tapicería Sunbrella
    # - Zona Comedor Exterior (Este): Mesa exterior 2,40 x 1,00 m con 8 sillas y barbacoa integrada
    # - Cota cero absoluta enrasada con el interior
    svg.append("""
    <!-- ============================================== -->
    <!-- AMUEBLAMIENTO PORCHE SUR TECHADO [PB-14]       -->
    <!-- ============================================== -->
    <!-- Zona 1: Salón Exterior Lounge (Oeste) -->
    <g id="lounge-porche">
      <rect x="250" y="860" width="240" height="150" fill="#1e293b" fill-opacity="0.7" stroke="#f59e0b" stroke-width="1.0" rx="3"/>
      <!-- Sofá en L exterior -->
      <path d="M 260 870 L 460 870 L 460 920 L 320 920 L 320 990 L 260 990 Z" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>
      <!-- Mesita baja de teca/iroko -->
      <circle cx="390" cy="955" r="28" fill="#131c31" stroke="#f59e0b" stroke-width="1.0"/>
      <text x="390" y="958" fill="#fde68a" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">MESA TECA</text>
      <text x="360" y="850" fill="#f59e0b" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">ZONA SALÓN EXTERIOR CHILL-OUT</text>
    </g>

    <!-- Zona 2: Comedor Exterior y Barbacoa (Este) -->
    <g id="comedor-porche">
      <!-- Mesa exterior 2,40 x 1,00 m (216 x 90 px) -->
      <rect x="680" y="880" width="216" height="90" rx="2" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <text x="788" y="930" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700" text-anchor="middle">COMEDOR EXTERIOR (8 PAX)</text>
      <!-- Sillas de exterior -->
      <rect x="700" y="850" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="750" y="850" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="800" y="850" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="850" y="850" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="700" y="980" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="750" y="980" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="800" y="980" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>
      <rect x="850" y="980" width="38" height="20" rx="1.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.7"/>

      <!-- Módulo Barbacoa de exterior / Bancada de apoyo (X: 980 a 1080, Y: 870 a 930) -->
      <rect x="980" y="870" width="100" height="50" rx="2" fill="#0b1120" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="1005" cy="895" r="14" fill="#1e293b" stroke="#ef4444" stroke-width="1.0"/>
      <text x="1005" y="898" fill="#fca5a5" font-family="monospace" font-size="5.5" font-weight="700" text-anchor="middle">GRILL</text>
      <text x="1050" y="898" fill="#fde68a" font-family="monospace" font-size="6" text-anchor="middle">BANCADA</text>
    </g>
    """)

    # Rótulos de Estancias
    stamps = [
        (400.0, 710.0, "[PB-10] SALÓN CHIMENEA", "S.Útil: 26,50 m²", "Caliza Apomazada 120×120 · Z=±0,00m"),
        (815.0, 710.0, "[PB-11] COMEDOR INTERIOR", "S.Útil: 17,50 m²", "Caliza Apomazada 120×120 · Z=±0,00m"),
        (580.0, 1030.0, "[PB-14] PORCHE SUR TECHADO", "S.Útil: 32,55 m²", "Tarima Iroko s/ plots · Cota Cero")
    ]
    for rx, ry, rcode, rsurf, rmat in stamps:
        svg.append(f"""
        <g class="room-stamp">
          <rect x="{rx-70:.1f}" y="{ry-22:.1f}" width="140" height="44" rx="2" fill="#0b1120" fill-opacity="0.94" stroke="#38bdf8" stroke-width="0.9"/>
          <line x1="{rx-70:.1f}" y1="{ry-7:.1f}" x2="{rx+70:.1f}" y2="{ry-7:.1f}" stroke="#334155" stroke-width="0.6"/>
          <text x="{rx:.1f}" y="{ry-11:.1f}" fill="#38bdf8" font-family="monospace" font-size="7.5" font-weight="900" text-anchor="middle">{rcode}</text>
          <text x="{rx:.1f}" y="{ry+6:.1f}" fill="#f8fafc" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">{rsurf}</text>
          <text x="{rx:.1f}" y="{ry+16:.1f}" fill="#94a3b8" font-family="monospace" font-size="6.2" text-anchor="middle">{rmat}</text>
        </g>
        """)

    # Paneles de memoria constructiva y especificación técnica
    svg.append("""
    <g transform="translate(1220, 260)">
      <!-- Panel 1: Memoria Bioclimática y Espacial -->
      <rect x="0" y="0" width="640" height="400" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
      <rect x="0" y="0" width="640" height="28" fill="#1e293b"/>
      <text x="15" y="19" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="900">MEMORIA ARQUITECTÓNICA · CRUJÍA SUR (DÍA Y CONVITES)</text>
      
      <g transform="translate(20, 45)">
        <text x="0" y="15" fill="#f59e0b" font-family="monospace" font-size="8" font-weight="700">1. FLUIDEZ ESPACIAL Y FUSIÓN TOTAL DE 76,55 m²:</text>
        <text x="0" y="30" fill="#94a3b8" font-family="monospace" font-size="6.8">Salón (26,50 m²) y Comedor (17,50 m²) forman un espacio diáfano continuo sin</text>
        <text x="0" y="42" fill="#94a3b8" font-family="monospace" font-size="6.8">pilares intermedios, que se amplía en verano hacia el Porche Sur (32,55 m²)</text>
        <text x="0" y="54" fill="#94a3b8" font-family="monospace" font-size="6.8">mediante la corredera C-07 embutida a cota cero sin resaltes ni tropiezos.</text>

        <text x="0" y="80" fill="#38bdf8" font-family="monospace" font-size="8" font-weight="700">2. COMPORTAMIENTO PASIVO Y PROTECCIÓN SOLAR (ZONA C1):</text>
        <text x="0" y="95" fill="#94a3b8" font-family="monospace" font-size="6.8">El voladizo techado de 3,00 m de fondo bloquea el 100% del sol cenital de</text>
        <text x="0" y="107" fill="#94a3b8" font-family="monospace" font-size="6.8">verano (ángulo > 68°), evitando el sobrecalentamiento. En invierno (ángulo 23°),</text>
        <text x="0" y="119" fill="#94a3b8" font-family="monospace" font-size="6.8">la radiación penetra profundamente en la caliza actuando como masa térmica.</text>

        <text x="0" y="145" fill="#ef4444" font-family="monospace" font-size="8" font-weight="700">3. CHIMENEA PASSIVHAUS INDEPENDIENTE:</text>
        <text x="0" y="160" fill="#94a3b8" font-family="monospace" font-size="6.8">Hogar 100% estanco con conducto comburente inferior exterior para no alterar</text>
        <text x="0" y="172" fill="#94a3b8" font-family="monospace" font-size="6.8">la depresión del sistema de ventilación mecánica controlada (VMC Zehnder).</text>

        <text x="0" y="198" fill="#10b981" font-family="monospace" font-size="8" font-weight="700">4. MATERIALES NOBLES ARMONIZADOS:</text>
        <text x="0" y="213" fill="#94a3b8" font-family="monospace" font-size="6.8">Interior en losas de caliza 120×120 cm apomazada; exterior en lamas de Iroko</text>
        <text x="0" y="225" fill="#94a3b8" font-family="monospace" font-size="6.8">FSC sobre plots nivelables con drenaje perimetral continuo oculto.</text>

        <rect x="0" y="250" width="600" height="75" fill="#131c31" stroke="#334155" stroke-width="0.8"/>
        <text x="15" y="270" fill="#f8fafc" font-family="monospace" font-size="7.5" font-weight="700">RESUMEN DE SUPERFICIES COMPONENTES:</text>
        <text x="15" y="288" fill="#38bdf8" font-family="monospace" font-size="7">· Salón Principal con Chimenea [PB-10]: 26,50 m² útiles</text>
        <text x="15" y="302" fill="#38bdf8" font-family="monospace" font-size="7">· Comedor Principal Interior [PB-11]: 17,50 m² útiles</text>
        <text x="15" y="316" fill="#f59e0b" font-family="monospace" font-size="7">· Porche Sur Techado Exterior [PB-14]: 32,55 m² útiles (Fondo 3,00 m)</text>
      </g>

      <!-- Panel 2: Especificación Carpintería C-07 -->
      <g transform="translate(0, 420)">
        <rect x="0" y="0" width="640" height="390" fill="#0b1120" stroke="#334155" stroke-width="1.0" rx="3"/>
        <rect x="0" y="0" width="640" height="28" fill="#1e293b"/>
        <text x="15" y="19" fill="#f59e0b" font-family="monospace" font-size="9" font-weight="900">FICHA TÉCNICA · CORREDERA CORTIZO COR VISION PLUS (C-07)</text>
        
        <g transform="translate(20, 45)">
          <text x="0" y="15" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">DIMENSIÓN TOTAL:</text>
          <text x="200" y="15" fill="#f8fafc" font-family="monospace" font-size="8" font-weight="700">7,50 m (Longitud) × 2,70 m (Altura libre)</text>

          <text x="0" y="38" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">CONFIGURACIÓN:</text>
          <text x="200" y="38" fill="#f8fafc" font-family="monospace" font-size="7.5">3 hojas correderas de 2,50 m sobre 3 carriles embutidos</text>

          <text x="0" y="61" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">SECCIÓN VISTA NUDO:</text>
          <text x="200" y="61" fill="#f8fafc" font-family="monospace" font-size="7.5">Encuentro central minimalista de solo 25 mm de aluminio visto</text>

          <text x="0" y="84" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">GUÍA INFERIOR:</text>
          <text x="200" y="84" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">100% Embutida a cota cero en pavimento (sin resalte)</text>

          <text x="0" y="107" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">VIDRIO TÉCNICO:</text>
          <text x="200" y="107" fill="#f8fafc" font-family="monospace" font-size="7.5">Triple acristalamiento 6+6 Silence / 18 Ar / 6 Guardian Sun</text>

          <text x="0" y="130" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">TRANSMITANCIA TÉRMICA:</text>
          <text x="200" y="130" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">Uw = 0,85 W/m²K (Apta Passivhaus)</text>

          <text x="0" y="153" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">ATENUACIÓN ACÚSTICA:</text>
          <text x="200" y="153" fill="#10b981" font-family="monospace" font-size="7.5" font-weight="700">Rw = 42 dB (Confort total frente a vendaval atlántico)</text>

          <text x="0" y="176" fill="#cbd5e1" font-family="monospace" font-size="7.5" font-weight="700">ACABADO SUPERFICIAL:</text>
          <text x="200" y="176" fill="#f8fafc" font-family="monospace" font-size="7.5">Lacado polvo poliéster negro texturado RAL 9005 ST</text>

          <rect x="0" y="210" width="600" height="90" fill="#131c31" stroke="#f59e0b" stroke-width="0.8"/>
          <text x="15" y="235" fill="#fde68a" font-family="monospace" font-size="7.5" font-weight="700">VENTAJA FAMILIAR:</text>
          <text x="15" y="253" fill="#94a3b8" font-family="monospace" font-size="6.8">En días soleados de primavera/otoño y verano, las tres hojas se desplazan</text>
          <text x="15" y="267" fill="#94a3b8" font-family="monospace" font-size="6.8">dejando un hueco abierto de 5 metros que permite a los niños y comensales circular</text>
          <text x="15" y="281" fill="#94a3b8" font-family="monospace" font-size="6.8">sin barreras entre la mesa de comedor, la chimenea, el porche y el césped.</text>
        </g>
      </g>
    </g>
    """)

    svg.append("</svg>")
    return "\n".join(svg)

def main():
    print("=== Generando Plano CAD 1:20 del Salón, Comedor y Porche Sur ===")
    svg = generate_plano_salon_comedor_porche()
    with open("plano_salon_comedor_porche_planta.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ plano_salon_comedor_porche_planta.svg generado")
    ET.parse("plano_salon_comedor_porche_planta.svg")
    print("✓ XML VÁLIDO: plano_salon_comedor_porche_planta.svg")

if __name__ == "__main__":
    main()
