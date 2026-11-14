#!/usr/bin/env python3
"""
Script para generar el Plano Constructivo y de Instalaciones de Planta Primera (+3,15 m)
Escala gráfica 1:50, cotas milimétricas, amueblamiento normativo, y MEP completa:
- Electricidad (Schuko, conmutados, USB-C, balizas zócalo h=25cm, cuadros P1, toalleros)
- Fontanería y Saneamiento (PEX-a, bajantes insonorizadas Ø110, Geberit, sumideros lineales)
- Climatización y Ventilación VMC (Zehnder impulsión/extracción, suelo radiante zonal)
- Carpinterías C-10 a C-15 con especificación de vidrios y estanqueidad
"""

import os
import shutil

SVG_CONTENT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 980" width="100%" height="100%" style="background-color: #0b1120; font-family: 'SF Pro Text', -apple-system, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <pattern id="cad-grid-p1" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.6" opacity="0.6"/>
    </pattern>
    <pattern id="hatch-wall-p1" width="8" height="8" patternUnits="userSpaceOnUse">
      <path d="M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4" stroke="#475569" stroke-width="0.8"/>
    </pattern>
    <pattern id="hatch-acoustic-p1" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#1e1b4b"/>
      <path d="M 0 3 L 6 3" stroke="#6366f1" stroke-width="0.8"/>
    </pattern>
    <pattern id="deck-iroko-p1" width="24" height="24" patternUnits="userSpaceOnUse">
      <rect width="24" height="24" fill="#3d2008" opacity="0.4"/>
      <line x1="0" y1="6" x2="24" y2="6" stroke="#b45309" stroke-width="0.8" opacity="0.6"/>
      <line x1="0" y1="18" x2="24" y2="18" stroke="#b45309" stroke-width="0.8" opacity="0.6"/>
    </pattern>
    <pattern id="oak-floor-p1" width="40" height="16" patternUnits="userSpaceOnUse">
      <rect width="40" height="16" fill="#1c1917" opacity="0.4"/>
      <line x1="0" y1="0" x2="40" y2="0" stroke="#78350f" stroke-width="0.5" opacity="0.5"/>
      <line x1="20" y1="0" x2="20" y2="16" stroke="#78350f" stroke-width="0.4" opacity="0.3"/>
    </pattern>
    <pattern id="tile-bath-p1" width="25" height="25" patternUnits="userSpaceOnUse">
      <rect width="25" height="25" fill="#0f172a" stroke="#334155" stroke-width="0.5"/>
    </pattern>
    <marker id="dim-arr-p1" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M 1 1 L 7 4 L 1 7 z" fill="#38bdf8"/>
    </marker>
  </defs>

  <!-- BACKGROUND GRID -->
  <rect width="100%" height="100%" fill="url(#cad-grid-p1)"/>

  <!-- ========================================== -->
  <!-- HEADER CAD -->
  <!-- ========================================== -->
  <rect x="30" y="20" width="1140" height="65" rx="6" fill="#131c31" stroke="#38bdf8" stroke-width="1"/>
  <text x="50" y="45" fill="#38bdf8" font-size="14" font-weight="800" letter-spacing="1">PROYECTO DE EJECUCIÓN · DETALLE CONSTRUCTIVO 1:50 · PLANTA PRIMERA (+3,15 m)</text>
  <text x="50" y="65" fill="#94a3b8" font-size="11">Master Suite (31,2 m²), Dormitorios Hijos (14,6 m² c/u), Baños P1, Galería Acústica Silence y Balcón Corrido Sur</text>
  <rect x="920" y="32" width="230" height="42" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <text x="935" y="49" fill="#f8fafc" font-size="10" font-weight="700">PLANO Nº: E-04 (PLANTA PRIMERA)</text>
  <text x="935" y="63" fill="#10b981" font-size="9" font-weight="600">FECHA: NOV 2026 · REV. DEFINITIVA</text>

  <!-- ========================================== -->
  <!-- MUROS PERIMETRALES EXTERIORES (FACHADAS NORTE, ESTE Y OESTE) -->
  <!-- ========================================== -->
  <!-- Muro Exterior Norte (hatch 35cm = 35px) -->
  <rect x="250" y="95" width="750" height="30" fill="url(#hatch-wall-p1)" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Muro Exterior Oeste (35px) -->
  <rect x="250" y="95" width="35" height="520" fill="url(#hatch-wall-p1)" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Muro Exterior Este (35px) -->
  <rect x="965" y="95" width="35" height="520" fill="url(#hatch-wall-p1)" stroke="#38bdf8" stroke-width="1.5"/>

  <!-- ========================================== -->
  <!-- ZONA NORTE P1: BAÑOS Y FACHADA TÉCNICA -->
  <!-- ========================================== -->

  <!-- 1. BAÑO COMPARTIDO HIJOS (x=285..580, y=125..245 · 6,80 m²) -->
  <g id="bano-hijos">
    <rect x="285" y="125" width="295" height="120" fill="url(#tile-bath-p1)"/>
    <text x="430" y="148" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">15. BAÑO COMPARTIDO HIJOS</text>
    <text x="430" y="160" fill="#94a3b8" font-size="8.5" text-anchor="middle">6,80 m² útiles · Pavimento Porcelánico C3</text>

    <!-- Ventana C-10 Oscilobatiente Alta (Norte x=380..460, y=95..125) -->
    <rect x="380" y="95" width="80" height="30" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="420" y="114" fill="#ffffff" font-size="8" font-weight="700" text-anchor="middle">C-10 · 1,20×0,60 m (h=160)</text>

    <!-- Doble Seno Cerámico en Mueble Roble Suspendido 1,40m (x=300..400, y=180..235) -->
    <rect x="300" y="180" width="100" height="55" rx="3" fill="#1e293b" stroke="#0284c7" stroke-width="1.2"/>
    <ellipse cx="325" cy="207" rx="16" ry="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <ellipse cx="375" cy="207" rx="16" ry="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <circle cx="325" cy="207" r="2.5" fill="#38bdf8"/>
    <circle cx="375" cy="207" r="2.5" fill="#38bdf8"/>
    <text x="350" y="243" fill="#94a3b8" font-size="7.5" text-anchor="middle">Doble Seno Dekton 1,40m</text>
    <!-- Tomas eléctricas baño hijos: 2 Schuko IP44 + luz espejo -->
    <circle cx="310" cy="175" r="3.5" fill="#ef4444"/>
    <circle cx="390" cy="175" r="3.5" fill="#ef4444"/>
    <text x="350" y="174" fill="#ef4444" font-size="7" font-weight="700" text-anchor="middle">2x Schuko IP44 (C5)</text>

    <!-- Bañera / Ducha amplia 1,70 x 0,75m (x=460..575, y=135..190) -->
    <rect x="460" y="135" width="115" height="60" rx="4" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>
    <rect x="465" y="140" width="105" height="50" rx="3" fill="#082f49"/>
    <circle cx="560" cy="165" r="5" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <text x="515" y="168" fill="#bae6fd" font-size="8" font-weight="700" text-anchor="middle">Bañera/Ducha 1,70×0,75m</text>

    <!-- Inodoro suspendido Geberit iCon Rimless (x=480..525, y=205..240) -->
    <rect x="480" y="210" width="35" height="12" fill="#334155" stroke="#475569" stroke-width="1"/>
    <path d="M 483 222 C 483 240, 512 240, 512 222 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <circle cx="497" cy="227" r="2" fill="#38bdf8"/>
    <text x="497" y="206" fill="#94a3b8" font-size="7" text-anchor="middle">Geberit Rimless</text>
    <!-- Bajante insonorizada Ø110 -->
    <circle cx="535" cy="225" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="1"/>
    <text x="555" y="228" fill="#f59e0b" font-size="7" font-weight="700">Bajante Ø110</text>

    <!-- Radiador Toallero Hidráulico 750W y Extracción VMC -->
    <rect x="290" y="135" width="8" height="35" fill="#ef4444" stroke="#ffffff" stroke-width="0.8"/>
    <text x="303" y="145" fill="#fca5a5" font-size="7">Toallero 750W</text>
    <circle cx="430" cy="175" r="5" fill="#047857" stroke="#10b981" stroke-width="1"/>
    <text x="430" y="188" fill="#10b981" font-size="7" font-weight="700" text-anchor="middle">VMC Extr. 40 m³/h</text>

    <!-- Puerta batiente hacia distribuidor (x=550..580, y=245) -->
    <line x1="550" y1="245" x2="550" y2="280" stroke="#f59e0b" stroke-width="2"/>
    <path d="M 580 245 A 30 30 0 0 1 550 275" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="3 3"/>
  </g>

  <!-- TABIQUE SEPARADOR ENTRE BAÑOS (x=580..600, y=125..245) -->
  <rect x="580" y="125" width="20" height="120" fill="url(#hatch-wall-p1)" stroke="#475569" stroke-width="1"/>

  <!-- 2. BAÑO PRIVADO MASTER SUITE (x=600..965, y=125..245 · 6,30 m²) -->
  <g id="bano-suite">
    <rect x="600" y="125" width="365" height="120" fill="url(#tile-bath-p1)"/>
    <text x="780" y="148" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">18. BAÑO PRIVADO MASTER SUITE</text>
    <text x="780" y="160" fill="#94a3b8" font-size="8.5" text-anchor="middle">6,30 m² útiles · Ducha Italiana Doble · Cota cero</text>

    <!-- Ventana C-11 Oscilobatiente Alta (Norte x=730..820, y=95..125) -->
    <rect x="730" y="95" width="90" height="30" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="775" y="114" fill="#ffffff" font-size="8" font-weight="700" text-anchor="middle">C-11 · 1,40×0,60 m (h=160)</text>

    <!-- Ducha Italiana Doble 1,50 x 0,90m (x=835..955, y=135..235) -->
    <rect x="835" y="135" width="120" height="100" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.5"/>
    <!-- Sumidero lineal oculto AISI 316 -->
    <rect x="940" y="145" width="6" height="80" fill="#94a3b8" stroke="#ffffff" stroke-width="0.8"/>
    <!-- 2 Rociadores de techo efecto lluvia -->
    <circle cx="875" cy="165" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="1.2"/>
    <circle cx="875" cy="205" r="8" fill="#0284c7" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="875" y="168" fill="#ffffff" font-size="6" font-weight="800" text-anchor="middle">🚿</text>
    <text x="875" y="208" fill="#ffffff" font-size="6" font-weight="800" text-anchor="middle">🚿</text>
    <text x="890" y="188" fill="#bae6fd" font-size="7.5" font-weight="700" text-anchor="middle">Ducha Doble</text>
    <text x="890" y="198" fill="#7dd3fc" font-size="6.5" text-anchor="middle">Termostatos dobles</text>

    <!-- Mueble Suspendido Doble Seno Dekton Kelya 1,60m (x=615..725, y=175..235) -->
    <rect x="615" y="175" width="110" height="60" rx="3" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <rect x="625" y="185" width="40" height="30" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <rect x="675" y="185" width="40" height="30" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
    <circle cx="645" cy="200" r="2.5" fill="#38bdf8"/>
    <circle cx="695" cy="200" r="2.5" fill="#38bdf8"/>
    <text x="670" y="244" fill="#fde68a" font-size="7.5" font-weight="700" text-anchor="middle">Dekton Kelya 1,60m</text>
    <!-- Tomas 2 Schuko IP44 + sensor antivaho espejo -->
    <circle cx="620" cy="170" r="3.5" fill="#ef4444"/>
    <circle cx="710" cy="170" r="3.5" fill="#ef4444"/>
    <text x="665" y="168" fill="#ef4444" font-size="7" font-weight="700" text-anchor="middle">2x Schuko IP44</text>

    <!-- Inodoro Suspendido Geberit con DuoFresh (x=750..795, y=200..235) -->
    <rect x="755" y="200" width="35" height="10" fill="#334155" stroke="#475569" stroke-width="1"/>
    <path d="M 758 210 C 758 230, 787 230, 787 210 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <text x="772" y="196" fill="#94a3b8" font-size="7" text-anchor="middle">Geberit DuoFresh</text>
    <!-- Bajante insonorizada Ø110 -->
    <circle cx="805" cy="215" r="6" fill="#f59e0b" stroke="#ffffff" stroke-width="1"/>
    <text x="805" y="235" fill="#f59e0b" font-size="6.5" font-weight="700" text-anchor="middle">Ø110</text>

    <!-- Toallero Eléctrico 750W y VMC Extracción -->
    <rect x="955" y="185" width="8" height="35" fill="#ef4444" stroke="#ffffff" stroke-width="0.8"/>
    <circle cx="770" cy="175" r="5" fill="#047857" stroke="#10b981" stroke-width="1"/>
    <text x="770" y="187" fill="#10b981" font-size="7" font-weight="700" text-anchor="middle">VMC 40 m³/h</text>

    <!-- Puerta corredera oculta hacia Vestidor Suite (x=670..730, y=245) -->
    <line x1="660" y1="245" x2="720" y2="245" stroke="#38bdf8" stroke-width="3" stroke-dasharray="4 2"/>
    <text x="690" y="258" fill="#38bdf8" font-size="7" font-weight="700" text-anchor="middle">P. Corredera 0,80m</text>
  </g>

  <!-- ========================================== -->
  <!-- ZONA INTERMEDIA: ESCALERA, GALERÍA SILENCE Y VESTIDOR -->
  <!-- ========================================== -->

  <!-- 3. DESEMBARCO DE ESCALERA VOLADA (x=285..365, y=245..365) -->
  <g id="desembarco-escalera">
    <rect x="285" y="245" width="80" height="120" fill="#1e293b" stroke="#475569" stroke-width="1"/>
    <!-- Peldaños P11 a P17 de roble macizo 80mm -->
    <g stroke="#64748b" stroke-width="1">
      <line x1="285" y1="260" x2="365" y2="260"/>
      <line x1="285" y1="275" x2="365" y2="275"/>
      <line x1="285" y1="290" x2="365" y2="290"/>
      <line x1="285" y1="305" x2="365" y2="305"/>
      <line x1="285" y1="320" x2="365" y2="320"/>
      <line x1="285" y1="335" x2="365" y2="335"/>
      <line x1="285" y1="350" x2="365" y2="350"/>
    </g>
    <!-- Flecha de llegada P1 -->
    <line x1="325" y1="350" x2="325" y2="255" stroke="#10b981" stroke-width="2" marker-end="url(#dim-arr-p1)"/>
    <text x="325" y="300" fill="#10b981" font-size="8" font-weight="800" text-anchor="middle">DESEMBARCO</text>
    <text x="325" y="312" fill="#a7f3d0" font-size="7" text-anchor="middle">Cota +3,15 m</text>
    <!-- Barandilla de Vidrio Laminado Templado 10+10.2mm -->
    <line x1="365" y1="245" x2="365" y2="365" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="357" y="310" fill="#38bdf8" font-size="6.5" font-weight="700" transform="rotate(-90 357 310)" text-anchor="middle">Barandilla Vidrio 10+10</text>
  </g>

  <!-- 4. GALERÍA ACÚSTICA P1 Y PASILLO (x=365..600, y=245..365 · 8,20 m²) -->
  <g id="galeria-acustica">
    <rect x="365" y="245" width="235" height="120" fill="url(#oak-floor-p1)"/>
    <text x="480" y="275" fill="#c084fc" font-size="11" font-weight="800" text-anchor="middle">12. GALERÍA ACÚSTICA &amp; DISTRIBUIDOR</text>
    <text x="480" y="288" fill="#94a3b8" font-size="8.5" text-anchor="middle">8,20 m² útiles · Roble multicapa 14mm · Aislamiento 42 dB</text>

    <!-- MAMPARA ACÚSTICA C-15 (VIDRIO 4+4 SILENCE DE SUELO A TECHO, 4,00 x 2,60m) -->
    <!-- Separa acústicamente la galería del hueco central del patio corrala inferior -->
    <rect x="375" y="355" width="220" height="8" rx="2" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="485" y="350" fill="#38bdf8" font-size="8" font-weight="800" text-anchor="middle">C-15 · MAMPARA ACÚSTICA 4+4 SILENCE (4,00 × 2,60 m)</text>
    <text x="485" y="375" fill="#64748b" font-size="7.5" text-anchor="middle">↓ Vacío sobre Patio Corrala (Vista cenital copa Acer palmatum) ↓</text>

    <!-- Balizas de cortesía LED empotradas en zócalo (h=25cm) para trayectos nocturnos -->
    <g fill="#fef08a" stroke="#ca8a04" stroke-width="0.8">
      <circle cx="390" cy="250" r="3"/>
      <circle cx="450" cy="250" r="3"/>
      <circle cx="510" cy="250" r="3"/>
      <circle cx="570" cy="250" r="3"/>
    </g>
    <text x="480" y="260" fill="#fef08a" font-size="7" font-weight="700" text-anchor="middle">Balizas Nocturnas LED h=25cm (circuito crepuscular)</text>

    <!-- Cuadro Secundario Planta Primera (empotrado) -->
    <rect x="370" y="248" width="12" height="20" fill="#ef4444" stroke="#ffffff" stroke-width="0.8"/>
    <text x="390" y="258" fill="#ef4444" font-size="6.5" font-weight="700">Subcuadro P1</text>
  </g>

  <!-- 5. VESTIDOR DE PASO DOBLE SUITE (x=600..965, y=245..365 · 8,40 m²) -->
  <g id="vestidor-suite">
    <rect x="600" y="245" width="365" height="120" fill="url(#oak-floor-p1)"/>
    <text x="780" y="270" fill="#f59e0b" font-size="11" font-weight="800" text-anchor="middle">17. VESTIDOR DE PASO DOBLE SUITE</text>
    <text x="780" y="282" fill="#94a3b8" font-size="8.5" text-anchor="middle">8,40 m² útiles · Doble hilera continua 4,20 m · Frentes vidrio ahumado</text>

    <!-- Hilera Armarios Norte (Fondo 60cm, L=3,60m · x=605..960, y=248..278) -->
    <rect x="605" y="248" width="355" height="28" rx="2" fill="#1e293b" stroke="#b45309" stroke-width="1.2"/>
    <text x="780" y="265" fill="#fef3c7" font-size="7.5" font-weight="700" text-anchor="middle">Armarios Empotrados Norte (L=4,20 m · fondo 60 cm)</text>

    <!-- Pasillo Central Libre de 1,10 m (y=278..332) -->
    <line x1="610" y1="305" x2="955" y2="305" stroke="#f59e0b" stroke-width="0.8" stroke-dasharray="4 2"/>
    <text x="780" y="303" fill="#fde68a" font-size="7.5" text-anchor="middle">Pasillo libre 1,10 m · Iluminación LED vertical integrada</text>

    <!-- Hilera Armarios Sur (Fondo 60cm · x=605..960, y=332..362) -->
    <rect x="605" y="332" width="355" height="28" rx="2" fill="#1e293b" stroke="#b45309" stroke-width="1.2"/>
    <text x="780" y="348" fill="#fef3c7" font-size="7.5" font-weight="700" text-anchor="middle">Armarios Empotrados Sur (L=4,20 m · fondo 60 cm)</text>

    <!-- Puerta corredera de vidrio ahumado hacia Master Suite -->
    <line x1="750" y1="365" x2="810" y2="365" stroke="#f59e0b" stroke-width="3"/>
    <text x="780" y="377" fill="#f59e0b" font-size="7" font-weight="700" text-anchor="middle">Paso libre hacia Suite</text>
  </g>

  <!-- ========================================== -->
  <!-- ZONA SUR P1: DORMITORIOS PRIVADOS Y BALCÓN -->
  <!-- ========================================== -->

  <!-- 6. DORMITORIO INFANTIL NIÑA (x=285..495, y=380..590 · 14,60 m²) -->
  <g id="dormitorio-nina">
    <rect x="285" y="380" width="210" height="210" fill="url(#oak-floor-p1)"/>
    <text x="390" y="405" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">13. DORMITORIO NIÑA</text>
    <text x="390" y="418" fill="#94a3b8" font-size="8.5" text-anchor="middle">14,60 m² útiles · Roble multicapa 14mm</text>

    <!-- Cama 1,20 x 2,00m con Cabecero Tapizado en Pared Norte (x=300..365, y=430..530) -->
    <rect x="295" y="430" width="70" height="100" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <!-- Cabecero -->
    <rect x="295" y="430" width="70" height="15" rx="2" fill="#0369a1"/>
    <!-- Almohada -->
    <rect x="305" y="450" width="50" height="20" rx="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>
    <text x="330" y="490" fill="#bae6fd" font-size="8" font-weight="700" text-anchor="middle">Cama 1,20×2,00</text>
    <!-- Mesilla suspendida con Schuko + USB-C a h=65cm -->
    <rect x="368" y="430" width="22" height="22" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1"/>
    <circle cx="379" cy="441" r="3" fill="#ef4444"/>
    <text x="379" y="460" fill="#ef4444" font-size="6.5" font-weight="700" text-anchor="middle">2x Schuko + USB-C</text>

    <!-- MESA DE ESTUDIO SUSPENDIDA 1,80m EN PARED ESTE (x=455..490, y=420..540) -->
    <!-- Recibe luz lateral a 90° de la balconera sur sin reflejos -->
    <rect x="455" y="420" width="35" height="110" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1.5"/>
    <text x="472" y="475" fill="#fef3c7" font-size="8" font-weight="800" transform="rotate(-90 472 475)" text-anchor="middle">MESA ESTUDIO 1,80 m</text>
    <!-- Silla ergonómica orientada al Este -->
    <circle cx="435" cy="475" r="10" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <path d="M 425 465 C 420 475, 420 475, 425 485" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
    <!-- Canaleta mecanismos: 3 Schuko + 2 RJ45 Cat 6A + USB-C PD a h=80cm -->
    <circle cx="485" cy="445" r="3" fill="#ef4444"/>
    <circle cx="485" cy="460" r="3" fill="#38bdf8"/>
    <circle cx="485" cy="475" r="3" fill="#10b981"/>
    <text x="430" y="430" fill="#10b981" font-size="6.5" font-weight="700">Luz lateral 90° · Cero reflejos</text>

    <!-- Armario Empotrado de Suelo a Techo (Pared Norte x=300..420, y=382..412) -->
    <rect x="300" y="382" width="120" height="25" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
    <text x="360" y="398" fill="#e2e8f0" font-size="7.5" text-anchor="middle">Armario Empotrado 2,00 m</text>

    <!-- VMC Zehnder Impulsión y Termostato Zonal -->
    <circle cx="390" cy="520" r="5" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <text x="390" y="535" fill="#38bdf8" font-size="7" font-weight="700" text-anchor="middle">VMC Imp. 30 m³/h</text>
    <rect x="290" y="560" width="6" height="10" fill="#10b981"/>
    <text x="300" y="568" fill="#10b981" font-size="6.5">Termostato</text>

    <!-- Balconera Corredera Sur C-12 (x=330..450, y=585..600) -->
    <rect x="330" y="585" width="120" height="15" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="390" y="596" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">C-12 · Cortizo 2,20×2,40m</text>
  </g>

  <!-- ========================================== -->
  <!-- TABIQUE MEDIANERO ACÚSTICO ENTRE DORMITORIOS HIJOS (x=495..515, y=380..590) -->
  <!-- ========================================== -->
  <rect x="495" y="380" width="20" height="210" fill="url(#hatch-acoustic-p1)" stroke="#6366f1" stroke-width="1.5"/>
  <text x="505" y="485" fill="#a5b4fc" font-size="7.5" font-weight="800" transform="rotate(-90 505 485)" text-anchor="middle">TABIQUE ACÚSTICO Rw ≥ 50 dB (CERO HUECOS)</text>

  <!-- 7. DORMITORIO INFANTIL NIÑO (x=515..720, y=380..590 · 14,60 m²) -->
  <g id="dormitorio-nino">
    <rect x="515" y="380" width="205" height="210" fill="url(#oak-floor-p1)"/>
    <text x="617" y="405" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">14. DORMITORIO NIÑO</text>
    <text x="617" y="418" fill="#94a3b8" font-size="8.5" text-anchor="middle">14,60 m² útiles · Distribución simétrica ergonómica</text>

    <!-- Cama 1,20 x 2,00m en Pared Oeste (x=525..595, y=430..530) -->
    <rect x="525" y="430" width="70" height="100" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <rect x="525" y="430" width="70" height="15" rx="2" fill="#0369a1"/>
    <rect x="535" y="450" width="50" height="20" rx="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>
    <text x="560" y="490" fill="#bae6fd" font-size="8" font-weight="700" text-anchor="middle">Cama 1,20×2,00</text>
    <!-- Mesilla suspendida -->
    <rect x="598" y="430" width="22" height="22" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1"/>
    <circle cx="609" cy="441" r="3" fill="#ef4444"/>
    <text x="609" y="460" fill="#ef4444" font-size="6.5" font-weight="700" text-anchor="middle">2x Schuko + USB-C</text>

    <!-- MESA DE ESTUDIO SUSPENDIDA 1,80m EN PARED ESTE (x=680..715, y=420..540) -->
    <rect x="680" y="420" width="35" height="110" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1.5"/>
    <text x="697" y="475" fill="#fef3c7" font-size="8" font-weight="800" transform="rotate(-90 697 475)" text-anchor="middle">MESA ESTUDIO 1,80 m</text>
    <!-- Silla ergonómica -->
    <circle cx="660" cy="475" r="10" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <!-- Canaleta mecanismos: 3 Schuko + 2 RJ45 Cat 6A + USB-C PD -->
    <circle cx="710" cy="445" r="3" fill="#ef4444"/>
    <circle cx="710" cy="460" r="3" fill="#38bdf8"/>
    <circle cx="710" cy="475" r="3" fill="#10b981"/>
    <text x="655" y="430" fill="#10b981" font-size="6.5" font-weight="700">Luz lateral 90° · Cero reflejos</text>

    <!-- Armario Empotrado (Pared Norte x=525..645, y=382..412) -->
    <rect x="525" y="382" width="120" height="25" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
    <text x="585" y="398" fill="#e2e8f0" font-size="7.5" text-anchor="middle">Armario Empotrado 2,00 m</text>

    <!-- VMC Impulsión -->
    <circle cx="617" cy="520" r="5" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <text x="617" y="535" fill="#38bdf8" font-size="7" font-weight="700" text-anchor="middle">VMC Imp. 30 m³/h</text>

    <!-- Balconera Corredera Sur C-13 (x=560..680, y=585..600) -->
    <rect x="560" y="585" width="120" height="15" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="620" y="596" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">C-13 · Cortizo 2,20×2,40m</text>
  </g>

  <!-- TABIQUE DIVISORIO ACÚSTICO ENTRE DORMITORIOS Y MASTER SUITE (x=720..740, y=380..590) -->
  <rect x="720" y="380" width="20" height="210" fill="url(#hatch-wall-p1)" stroke="#475569" stroke-width="1.5"/>

  <!-- 8. MASTER SUITE PRINCIPAL MATRIMONIO (x=740..965, y=380..590 · 16,50 m²) -->
  <g id="master-suite">
    <rect x="740" y="380" width="225" height="210" fill="url(#oak-floor-p1)"/>
    <text x="852" y="405" fill="#38bdf8" font-size="11" font-weight="800" text-anchor="middle">16. MASTER SUITE MATRIMONIO</text>
    <text x="852" y="418" fill="#94a3b8" font-size="8.5" text-anchor="middle">16,50 m² útiles · Cama King Size · Vistas Sur</text>

    <!-- Cama King Size 1,80 x 2,00m en Pared Norte (x=790..915, y=430..535) -->
    <rect x="790" y="430" width="125" height="105" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <!-- Cabecero acústico tapizado -->
    <rect x="785" y="425" width="135" height="15" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="1"/>
    <!-- 2 Almohadas -->
    <rect x="800" y="445" width="45" height="25" rx="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>
    <rect x="860" y="445" width="45" height="25" rx="4" fill="#334155" stroke="#64748b" stroke-width="0.8"/>
    <text x="852" y="495" fill="#bae6fd" font-size="9" font-weight="800" text-anchor="middle">King Size 1,80×2,00m</text>

    <!-- Mesillas flotantes integradas a ambos lados -->
    <rect x="755" y="435" width="25" height="25" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1"/>
    <circle cx="767" cy="447" r="3.5" fill="#ef4444"/>
    <text x="767" y="470" fill="#ef4444" font-size="6.5" font-weight="700" text-anchor="middle">2x Schuko + USB-C</text>

    <rect x="925" y="435" width="25" height="25" rx="2" fill="#451a03" stroke="#b45309" stroke-width="1"/>
    <circle cx="937" cy="447" r="3.5" fill="#ef4444"/>
    <text x="937" y="470" fill="#ef4444" font-size="6.5" font-weight="700" text-anchor="middle">2x Schuko + USB-C</text>

    <!-- Termostato digital independiente y control estor -->
    <rect x="745" y="550" width="8" height="12" fill="#10b981"/>
    <text x="758" y="560" fill="#10b981" font-size="7" font-weight="700">Termostato Zonal P1</text>

    <!-- VMC Impulsión -->
    <circle cx="852" cy="540" r="6" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
    <text x="852" y="555" fill="#38bdf8" font-size="7" font-weight="700" text-anchor="middle">VMC Impulsión 40 m³/h</text>

    <!-- Balconera Corredera Sur C-14 (Cortizo Cor Vision 3,00 x 2,40m · x=775..930, y=585..600) -->
    <rect x="775" y="585" width="155" height="15" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="852" y="596" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">C-14 · Cortizo Cor Vision 3,00×2,40m</text>
  </g>

  <!-- ========================================== -->
  <!-- 9. BALCÓN CORRIDO SUR P1 (Cota +3,15 m · x=285..965, y=600..675) -->
  <!-- ========================================== -->
  <g id="balcon-sur-p1">
    <rect x="285" y="600" width="680" height="75" fill="url(#deck-iroko-p1)" stroke="#b45309" stroke-width="1"/>
    <text x="625" y="630" fill="#f59e0b" font-size="12" font-weight="800" text-anchor="middle">19. BALCÓN CORRIDO SUR P1 (14,00 m² útiles · Fondo 1,40 m · Cota +3,15 m)</text>
    <text x="625" y="645" fill="#fef3c7" font-size="8.5" text-anchor="middle">Tarima maciza de Iroko sobre plots regulables · Enrasada a cota cero con dormitorios · Pendiente 1,5%</text>

    <!-- BARANDILLA CONTINUA DE VIDRIO ESTRUCTURAL 10+10.2 MM (y=675) -->
    <line x1="285" y1="675" x2="965" y2="675" stroke="#38bdf8" stroke-width="3"/>
    <text x="625" y="668" fill="#38bdf8" font-size="8" font-weight="800" text-anchor="middle">BARANDILLA CONTINUA DE VIDRIO ESTRUCTURAL TEMPLADO-LAMINADO 10+10.2 mm (h=1,10 m)</text>

    <!-- Gárgolas de desagüe ocultas en ambos extremos -->
    <circle cx="295" cy="670" r="4" fill="#0284c7"/>
    <circle cx="955" cy="670" r="4" fill="#0284c7"/>
    <text x="315" y="665" fill="#7dd3fc" font-size="7">Sumidero</text>
    <text x="935" y="665" fill="#7dd3fc" font-size="7" text-anchor="end">Sumidero</text>
  </g>

  <!-- ========================================== -->
  <!-- LÍNEAS DE COTA CAD Y DIMENSIONES (ESC. 1:50) -->
  <!-- ========================================== -->
  <g id="cotas-cad" stroke="#38bdf8" stroke-width="1">
    <!-- Cota Total Ancho Fachada Sur (L=14,00 m) -->
    <line x1="285" y1="700" x2="965" y2="700" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="625" y="695" fill="#38bdf8" font-size="10" font-weight="800" text-anchor="middle">14,00 m (Ancho Total Planta Primera P1)</text>

    <!-- Cotas Parciales Dormitorios Sur -->
    <line x1="285" y1="720" x2="495" y2="720" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="390" y="716" fill="#38bdf8" font-size="8.5" font-weight="700" text-anchor="middle">3,80 m (Dorm. Niña)</text>

    <line x1="515" y1="720" x2="720" y2="720" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="617" y="716" fill="#38bdf8" font-size="8.5" font-weight="700" text-anchor="middle">3,80 m (Dorm. Niño)</text>

    <line x1="740" y1="720" x2="965" y2="720" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="852" y="716" fill="#38bdf8" font-size="8.5" font-weight="700" text-anchor="middle">4,30 m (Master Suite)</text>

    <!-- Cota Fondo Norte-Sur (Y=125..600 = 9,50 m) -->
    <line x1="230" y1="125" x2="230" y2="590" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="220" y="360" fill="#38bdf8" font-size="9" font-weight="800" transform="rotate(-90 220 360)" text-anchor="middle">9,50 m (Fondo Interior P1)</text>

    <!-- Cota Fondo Balcón Sur (1,40 m) -->
    <line x1="230" y1="600" x2="230" y2="675" marker-start="url(#dim-arr-p1)" marker-end="url(#dim-arr-p1)"/>
    <text x="220" y="640" fill="#38bdf8" font-size="8" font-weight="700" transform="rotate(-90 220 640)" text-anchor="middle">1,40 m</text>
  </g>

  <!-- ========================================== -->
  <!-- LEYENDA TÉCNICA Y CUADRO DE INSTALACIONES MEP -->
  <!-- ========================================== -->
  <g id="leyenda-tecnica">
    <rect x="50" y="750" width="1100" height="205" rx="8" fill="#131c31" stroke="#334155" stroke-width="1.2"/>
    <text x="70" y="775" fill="#38bdf8" font-size="12" font-weight="800">LEYENDA TÉCNICA · INSTALACIONES &amp; CONSTRUCTIBILIDAD PLANTA PRIMERA (+3,15 m)</text>

    <!-- Columna 1: Electricidad & Telecomunicaciones -->
    <text x="70" y="800" fill="#f8fafc" font-size="10" font-weight="700">⚡ ELECTRICIDAD &amp; DATOS (REBT / ICT)</text>
    <circle cx="80" cy="815" r="4" fill="#ef4444"/>
    <text x="92" y="818" fill="#cbd5e1" font-size="8.5">Tomas Schuko 16A (h=30cm en dormitorios, h=80cm en mesas de estudio)</text>
    <circle cx="80" cy="832" r="4" fill="#38bdf8"/>
    <text x="92" y="835" fill="#cbd5e1" font-size="8.5">Tomas dobles RJ45 Cat 6A blindadas 10 Gbps en cada pupitre de estudio</text>
    <circle cx="80" cy="849" r="4" fill="#10b981"/>
    <text x="92" y="852" fill="#cbd5e1" font-size="8.5">Carga rápida USB-C Power Delivery 65W empotrada en cabeceros y mesas</text>
    <circle cx="80" cy="866" r="4" fill="#fef08a" stroke="#ca8a04"/>
    <text x="92" y="869" fill="#cbd5e1" font-size="8.5">Balizas LED de cortesía en zócalo (h=25cm) para guiado nocturno a baños</text>
    <rect x="76" y="880" width="8" height="8" fill="#ef4444"/>
    <text x="92" y="887" fill="#cbd5e1" font-size="8.5">Subcuadro eléctrico secundario P1 con diferenciales superinmunizados</text>

    <!-- Columna 2: Climatización y Ventilación Passivhaus -->
    <text x="440" y="800" fill="#f8fafc" font-size="10" font-weight="700">🌬️ CLIMATIZACIÓN &amp; VMC (PASSIVHAUS)</text>
    <circle cx="450" cy="815" r="5" fill="#0284c7" stroke="#38bdf8"/>
    <text x="465" y="818" fill="#cbd5e1" font-size="8.5">Impulsión VMC Zehnder ComfoAir (30 m³/h dormitorios, 40 m³/h suite)</text>
    <circle cx="450" cy="832" r="5" fill="#047857" stroke="#10b981"/>
    <text x="465" y="835" fill="#cbd5e1" font-size="8.5">Extracción forzada VMC en baños (40 m³/h Baño Hijos y Baño Suite)</text>
    <rect x="446" y="845" width="8" height="8" fill="#10b981"/>
    <text x="465" y="852" fill="#cbd5e1" font-size="8.5">Suelo radiante/refrescante zonal con termostatos digitales independientes</text>
    <rect x="446" y="862" width="8" height="14" fill="#ef4444"/>
    <text x="465" y="871" fill="#cbd5e1" font-size="8.5">Radiadores toalleros hidráulicos 750W conectados a circuito aerotermia</text>
    <circle cx="450" cy="890" r="5" fill="#f59e0b" stroke="#ffffff"/>
    <text x="465" y="893" fill="#cbd5e1" font-size="8.5">Bajantes fecales insonorizadas Ø110 con ventilación primaria a cubierta</text>

    <!-- Columna 3: Carpinterías & Aislamiento Acústico -->
    <text x="810" y="800" fill="#f8fafc" font-size="10" font-weight="700">🪟 CARPINTERÍAS &amp; ACÚSTICA</text>
    <rect x="816" y="810" width="12" height="6" fill="#0284c7" stroke="#38bdf8"/>
    <text x="835" y="816" fill="#cbd5e1" font-size="8.5">C-15: Mampara 4+4 Silence (42 dB) con vista cenital al Patio Corrala</text>
    <rect x="816" y="827" width="12" height="6" fill="#0369a1" stroke="#38bdf8"/>
    <text x="835" y="833" fill="#cbd5e1" font-size="8.5">C-12, C-13: Cortizo COR 80 RPT con triple vidrio acústico Guardian Sun</text>
    <rect x="816" y="844" width="12" height="6" fill="#0369a1" stroke="#38bdf8"/>
    <text x="835" y="850" fill="#cbd5e1" font-size="8.5">C-14: Corredera Cortizo Cor Vision 3,00×2,40m en Master Suite</text>
    <line x1="816" y1="867" x2="828" y2="867" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="835" y="870" fill="#cbd5e1" font-size="8.5">Barandilla continua vidrio templado-laminado 10+10.2mm (h=1,10m)</text>
    <rect x="816" y="881" width="12" height="6" fill="url(#hatch-acoustic-p1)" stroke="#6366f1"/>
    <text x="835" y="887" fill="#cbd5e1" font-size="8.5">Tabiques medianeros Pladur Fonic Rw ≥ 50 dB sin puentes fónicos</text>

    <!-- Cuadro resumen de superficies útiles P1 -->
    <rect x="70" y="910" width="1050" height="32" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
    <text x="85" y="930" fill="#38bdf8" font-size="9" font-weight="800">SUPERFICIES ÚTILES P1 (+3,15 m):</text>
    <text x="290" y="930" fill="#f8fafc" font-size="9">Master Suite: 16,5 m²</text>
    <text x="430" y="930" fill="#f8fafc" font-size="9">Vestidor: 8,4 m²</text>
    <text x="540" y="930" fill="#f8fafc" font-size="9">Baño Suite: 6,3 m²</text>
    <text x="650" y="930" fill="#f8fafc" font-size="9">Dorm. Niña: 14,6 m²</text>
    <text x="770" y="930" fill="#f8fafc" font-size="9">Dorm. Niño: 14,6 m²</text>
    <text x="890" y="930" fill="#f8fafc" font-size="9">Baño Hijos: 6,8 m²</text>
    <text x="1000" y="930" fill="#10b981" font-size="9" font-weight="700">Total P1: 89,5 m² (+14m² balcón)</text>
  </g>

</svg>'''

def main():
    repo_dir = "/home/antigravity/landslore/oleiros"
    dest_prop = os.path.join(repo_dir, "propuestas", "plano_constructivo_planta_alta_p1.svg")
    dest_root = os.path.join(repo_dir, "plano_constructivo_planta_alta_p1.svg")
    
    with open(dest_prop, "w", encoding="utf-8") as f:
        f.write(SVG_CONTENT)
    print(f"Generated {dest_prop}")
    
    with open(dest_root, "w", encoding="utf-8") as f:
        f.write(SVG_CONTENT)
    print(f"Generated {dest_root}")

if __name__ == "__main__":
    main()
