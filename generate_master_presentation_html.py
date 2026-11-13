#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Visor Master Interactivo Definitivo de la Propuesta D (Oleiros).
Integra: Planos Generales, Galería de Renders Fotorrealistas, Visor 3D Three.js,
Fichas Técnicas Zoom-In 1:20 y Enlace a la Presentación PowerPoint para Mac.
"""

import base64
import os

RENDERS_DIR = "/home/antigravity/landslore/oleiros/propuestas/renders"

def get_base64_image(filename):
    path = os.path.join(RENDERS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
    return ""

img_fachada = get_base64_image("fachada_norte_render.jpg")
img_patio = get_base64_image("patio_corrala_render.jpg")
img_living = get_base64_image("interior_living_render.jpg")
img_despacho = get_base64_image("despacho_render.jpg")
img_suite = get_base64_image("suite_principal_render.jpg")
img_porche = get_base64_image("porche_sur_render.jpg")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hogar Oleiros — Master Dossier Interactivo &amp; Planos Definitivos (Propuesta D)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #0b0f19;
      color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    .nav-tab.active {{
      background-color: #0284c7 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 0.18rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 700;
    }}
    .render-card {{
      transition: all 0.25s ease;
    }}
    .render-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 16px 32px rgba(0, 0, 0, 0.6);
      border-color: #38bdf8;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- CABECERA PRINCIPAL -->
  <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 sticky top-0 z-50 shadow-2xl flex flex-wrap items-center justify-between gap-4">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center font-black text-white text-lg shadow-lg shadow-sky-500/20">
        D
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="badge bg-sky-500/20 text-sky-400 border border-sky-500/30">PROYECTO DE EJECUCIÓN</span>
          <span class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">PROPUESTA D · DEFINITIVA</span>
          <span class="badge bg-amber-500/20 text-amber-400 border border-amber-500/30">OLEIROS (A CORUÑA)</span>
        </div>
        <h1 class="text-lg md:text-xl font-black text-white tracking-tight mt-0.5">
          Hogar Oleiros — Dossier Maestro Interactivo
        </h1>
      </div>
    </div>

    <!-- NAVEGACIÓN PRINCIPAL -->
    <nav class="flex flex-wrap items-center gap-1.5 text-xs">
      <button onclick="switchTab('renders')" id="tab-renders" class="nav-tab active px-3.5 py-2 rounded-xl bg-slate-800 text-slate-200 border border-slate-700 font-semibold transition">
        🖼️ Renders Fotorrealistas (6)
      </button>
      <button onclick="switchTab('planos')" id="tab-planos" class="nav-tab px-3.5 py-2 rounded-xl bg-slate-800 text-slate-200 border border-slate-700 font-medium transition">
        📐 Planos Generales (PB &amp; P1)
      </button>
      <button onclick="switchTab('3d')" id="tab-3d" class="nav-tab px-3.5 py-2 rounded-xl bg-slate-800 text-slate-200 border border-slate-700 font-medium transition">
        🌐 Visor 3D Three.js (Paseo WASD)
      </button>
      <button onclick="switchTab('zoom')" id="tab-zoom" class="nav-tab px-3.5 py-2 rounded-xl bg-slate-800 text-slate-200 border border-slate-700 font-medium transition">
        🔍 Zoom-In 1:20 (17 Estancias)
      </button>
      <button onclick="switchTab('powerpoint')" id="tab-powerpoint" class="nav-tab px-3.5 py-2 rounded-xl bg-amber-950 text-amber-300 border border-amber-800 font-semibold transition flex items-center gap-1.5">
        📊 PowerPoint (.pptx para Mac)
      </button>
    </nav>
  </header>

  <!-- CONTENIDO PRINCIPAL -->
  <main class="flex-1 max-w-[1720px] w-full mx-auto p-4 md:p-6">

    <!-- ═════════════════════════════════════════════════════════════════════════
         SECCIÓN 1: GALERÍA DE RENDERS FOTORREALISTAS
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-renders" class="space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-3xl shadow-xl">
        <div>
          <span class="badge bg-sky-500/20 text-sky-400 border border-sky-500/30">VISUALIZACIÓN ARQUITECTÓNICA</span>
          <h2 class="text-xl md:text-2xl font-black text-white mt-1">Atmósfera, Luz Atlántica &amp; Materiales Reales</h2>
          <p class="text-xs md:text-sm text-slate-400 mt-0.5">Renders fotorrealistas de alta resolución que capturan la espacialidad, texturas y vegetación de la Propuesta D.</p>
        </div>
      </div>

      <!-- GRID DE RENDERS -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

        <!-- 1. PATIO CORRALA -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_patio}" alt="Patio Corrala Habitable" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-amber-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 05 · EL CORAZÓN</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Patio Corrala Habitable y 100% Accesible</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Abierto al cielo con drenaje natural sobre terreno real. Tarima de iroko a cota cero, banco corrido de lectura bajo alero perimetral de 80 cm y arce japonés palmatum Atropurpureum.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ 16,0 m² libres · Cero efecto invernadero · Triple corredera elevable
            </div>
          </div>
        </div>

        <!-- 2. SALÓN, COCINA CON ISLA Y PORCHE -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_living}" alt="Salón y Cocina Abiertos al Patio" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-sky-500 text-slate-950 font-extrabold shadow-md">ESTANCIAS 06-08 · ZONA DE DÍA</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Salón, Comedor, Cocina con Isla &amp; Porche</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Continuidad visual total entre el patio y el jardín sur. Isla Dekton Kelya de 2,80 m con extractor Bora Pure, mesa de roble macizo para 10 pax y chimenea estanca empotrada.
              </p>
            </div>
            <div class="text-[11px] font-mono text-sky-400 bg-sky-950/50 p-2.5 rounded-xl border border-sky-900/60">
              ✓ 59,2 m² integrados · Muro acústico de lamas de roble · Suelo caliza continuo
            </div>
          </div>
        </div>

        <!-- 3. DESPACHO SANCTASANCTÓRUM -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_despacho}" alt="Despacho Sanctasanctórum" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-emerald-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 03 · TELETRABAJO &amp; SUITE</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Despacho Sanctasanctórum &amp; Suite Serena</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Luz difusa a 90° de fachada Norte (cero reflejos en monitor) y cristalera al patio ajardinado. Aislamiento acústico Rw ≥ 38 dB y sofá-cama con acceso privado al Baño PB.
              </p>
            </div>
            <div class="text-[11px] font-mono text-amber-400 bg-amber-950/50 p-2.5 rounded-xl border border-amber-900/60">
              ✓ 11,5 m² útiles · Doble toma RJ45 Cat 6A (10 Gbps) · Cero servidumbre
            </div>
          </div>
        </div>

        <!-- 4. PORCHE SUR CUBIERTO & PISCINA -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_porche}" alt="Porche Sur Expandido" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-amber-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 10 · VIDA EXTERIOR</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Porche Sur Expandido (Fondo 3,00 m)</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                36 m² cubiertos protegidos de la lluvia atlántica. Churrasqueira de granito Zimbabwe, comedor exterior de 10 plazas, salón lounge y vistas abiertas a la piscina y jardín.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ Fondo 3,00 m real · Piscina 3,5 × 7,5 m · Armario robot cortacésped
            </div>
          </div>
        </div>

        <!-- 5. SUITE PRINCIPAL MATRIMONIO P1 -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_suite}" alt="Suite Principal Matrimonio" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-indigo-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 16 · PLANTA PRIMERA</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Suite Principal de Matrimonio</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Ala Este privada de 31,2 m² con cama King Size orientada al Sur, balcón corrido con barandilla de vidrio estructural continuo, vestidor de paso en doble hilera y baño doble.
              </p>
            </div>
            <div class="text-[11px] font-mono text-sky-400 bg-sky-950/50 p-2.5 rounded-xl border border-sky-900/60">
              ✓ 31,2 m² suite · Ducha italiana doble · Frentes de vidrio ahumado
            </div>
          </div>
        </div>

        <!-- 6. FACHADA NORTE Y ACCESO PEATONAL / PÉRGOLA -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_fachada}" alt="Fachada Norte y Acceso" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-purple-500 text-slate-950 font-extrabold shadow-md">EXTERIOR · FACHADA NORTE</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Fachada Norte &amp; Doble Acceso</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Sendero ajardinado con losas de granito hacia el Porche Noble (puerta pivotante de iroko 1,10 m) y pérgola para 2 coches al Oeste con paso a cubierto al Zaguán Mudroom.
              </p>
            </div>
            <div class="text-[11px] font-mono text-purple-400 bg-purple-950/50 p-2.5 rounded-xl border border-purple-900/60">
              ✓ Zócalo de granito gallego · Carpintería Cortizo · Pérgola 2 plazas
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ═════════════════════════════════════════════════════════════════════════
         SECCIÓN 2: PLANOS GENERALES DEFINITIVOS (SVG)
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-planos" class="hidden space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-3xl shadow-xl">
        <div>
          <span class="badge bg-sky-500/20 text-sky-400 border border-sky-500/30">PLANOS ARQUITECTÓNICOS VECTORIALES</span>
          <h2 class="text-xl md:text-2xl font-black text-white mt-1">Planos Definitivos — Planta Baja y Planta Primera</h2>
          <p class="text-xs md:text-sm text-slate-400 mt-0.5">Planos a escala con cotas métricas, circulaciones, carpinterías y amueblamiento normativo.</p>
        </div>
        <div class="flex gap-2">
          <button onclick="showFloorSVG('pb')" id="btn-svg-pb" class="px-4 py-2 rounded-xl text-xs font-bold bg-sky-600 text-white border border-sky-400 shadow-md">
            Planta Baja (±0,00 m)
          </button>
          <button onclick="showFloorSVG('p1')" id="btn-svg-p1" class="px-4 py-2 rounded-xl text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 hover:text-white">
            Planta Primera (+3,15 m)
          </button>
        </div>
      </div>

      <!-- VISOR SVG EMBEBIDO -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-4 md:p-6 shadow-2xl flex justify-center">
        <div id="svg-container-pb" class="w-full flex justify-center overflow-x-auto">
          <object data="planta_baja_propuesta_d.svg" type="image/svg+xml" class="w-full max-w-[1100px] h-auto rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner"></object>
        </div>
        <div id="svg-container-p1" class="w-full flex justify-center overflow-x-auto hidden">
          <object data="planta_alta_propuesta_d.svg" type="image/svg+xml" class="w-full max-w-[1100px] h-auto rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner"></object>
        </div>
      </div>
    </section>

    <!-- ═════════════════════════════════════════════════════════════════════════
         SECCIÓN 3: VISOR 3D THREE.JS (HOMEMAKER)
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-3d" class="hidden space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-3xl shadow-xl">
        <div>
          <span class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">THREE.JS &amp; HOMEMAKER ARCHITECTURE</span>
          <h2 class="text-xl md:text-2xl font-black text-white mt-1">Paseo 3D Interactivo en Primera Persona &amp; Órbita 360°</h2>
          <p class="text-xs md:text-sm text-slate-400 mt-0.5">Explora la casa en 3D: pulsa 'Paseo 1ª Persona' para moverte con WASD o utiliza los botones de teletransporte.</p>
        </div>
      </div>

      <div class="w-full h-[75vh] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl bg-black">
        <iframe src="modelo_3d_propuesta_d_homemaker.html" class="w-full h-full border-0"></iframe>
      </div>
    </section>

    <!-- ═════════════════════════════════════════════════════════════════════════
         SECCIÓN 4: ZOOM-IN 1:20 (17 ESTANCIAS)
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-zoom" class="hidden space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-3xl shadow-xl">
        <div>
          <span class="badge bg-amber-500/20 text-amber-400 border border-amber-500/30">DETALLE DE EJECUCIÓN 1:20</span>
          <h2 class="text-xl md:text-2xl font-black text-white mt-1">Visor de Fichas Técnicas &amp; Planos CAD por Estancia</h2>
          <p class="text-xs md:text-sm text-slate-400 mt-0.5">Ubicación exacta y alturas (h) de enchufes, RJ45, interruptores, suelo radiante y bocas VMC en las 17 zonas.</p>
        </div>
      </div>

      <div class="w-full h-[80vh] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl bg-black">
        <iframe src="fichas_zoom_interactivas_propuesta_d.html" class="w-full h-full border-0"></iframe>
      </div>
    </section>

    <!-- ═════════════════════════════════════════════════════════════════════════
         SECCIÓN 5: PRESENTACIÓN POWERPOINT (MAC / KEYNOTE)
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-powerpoint" class="hidden space-y-6">
      <div class="bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 border border-sky-500/40 p-8 rounded-3xl shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="space-y-3 max-w-3xl">
          <div class="flex items-center gap-2">
            <span class="badge bg-amber-500/20 text-amber-400 border border-amber-500/30">FORMATO WIDESCREEN 16:9</span>
            <span class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">COMPATIBLE AL 100% CON MAC &amp; PC</span>
          </div>
          <h2 class="text-2xl md:text-3xl font-black text-white">Presentación PowerPoint Ejecutiva (.pptx)</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            Hemos preparado la presentación oficial en formato PowerPoint de alta gama (compatible nativamente con <strong>Keynote en Mac</strong> y <strong>Microsoft PowerPoint</strong>). Incluye todas las diapositivas de portada, criterios de diseño, planos, los 6 renders fotorrealistas en alta resolución y el desglose de costes y estándares energéticos.
          </p>
          <div class="flex flex-wrap gap-4 pt-2">
            <a href="Presentacion_Hogar_Oleiros_Propuesta_D.pptx" download class="px-6 py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-extrabold text-sm shadow-xl shadow-sky-500/25 flex items-center gap-2 transition">
              <span>📥 Descargar Archivo PowerPoint (.pptx)</span>
              <span class="text-xs bg-white/20 px-2 py-0.5 rounded-full font-mono">5,3 MB</span>
            </a>
            <a href="https://docs.google.com/presentation/d/1AHYDhaDiH4zxxbKxN8ffe-7R8t2RK37y-VMJbs5lKhw/edit" target="_blank" class="px-6 py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-sm border border-slate-700 flex items-center gap-2 transition">
              <span>☁️ Abrir en Google Slides</span>
            </a>
          </div>
        </div>

        <div class="w-full md:w-80 p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2.5 text-xs">
          <div class="font-bold text-sky-400 uppercase tracking-wider text-[11px]">Contenido del Deck (12 Diapositivas):</div>
          <p>• <strong>01:</strong> Portada &amp; Datos Clave de la Parcela</p>
          <p>• <strong>02:</strong> 4 Criterios Rectores del Rediseño</p>
          <p>• <strong>03:</strong> El Patio Corrala Habitable y Accesible</p>
          <p>• <strong>04:</strong> Zona de Día Integrada (Salón, Cocina, Comedor)</p>
          <p>• <strong>05:</strong> Despacho Sanctasanctórum &amp; Suite Serena</p>
          <p>• <strong>06:</strong> Porche Sur Expandido (Fondo 3m) &amp; Piscina</p>
          <p>• <strong>07:</strong> Suite Principal de Matrimonio (Ala Este P1)</p>
          <p>• <strong>08:</strong> Ingeniería, Radón, VMC Zehnder &amp; Presupuesto</p>
        </div>
      </div>
    </section>

  </main>

  <script>
    function switchTab(tabId) {{
      const tabs = ['renders', 'planos', '3d', 'zoom', 'powerpoint'];
      tabs.forEach(t => {{
        const btn = document.getElementById('tab-' + t);
        const sec = document.getElementById('sec-' + t);
        if (t === tabId) {{
          btn.className = 'nav-tab active px-3.5 py-2 rounded-xl bg-sky-600 text-white border border-sky-400 font-bold transition';
          sec.classList.remove('hidden');
        }} else {{
          btn.className = 'nav-tab px-3.5 py-2 rounded-xl bg-slate-800 text-slate-200 border border-slate-700 font-medium transition';
          sec.classList.add('hidden');
        }}
      }});
    }}

    function showFloorSVG(fl) {{
      const cPb = document.getElementById('svg-container-pb');
      const cP1 = document.getElementById('svg-container-p1');
      const bPb = document.getElementById('btn-svg-pb');
      const bP1 = document.getElementById('btn-svg-p1');

      if (fl === 'pb') {{
        cPb.classList.remove('hidden');
        cP1.classList.add('hidden');
        bPb.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-sky-600 text-white border border-sky-400 shadow-md';
        bP1.className = 'px-4 py-2 rounded-xl text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 hover:text-white';
      }} else {{
        cPb.classList.add('hidden');
        cP1.classList.remove('hidden');
        bPb.className = 'px-4 py-2 rounded-xl text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 hover:text-white';
        bP1.className = 'px-4 py-2 rounded-xl text-xs font-bold bg-sky-600 text-white border border-sky-400 shadow-md';
      }}
    }}
  </script>
</body>
</html>
"""

def main():
    target_path = "/home/antigravity/landslore/oleiros/propuestas/presentacion_propuesta_d_master.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Master HTML: {target_path} ({len(html_content)} bytes)")

    # Artifact directory
    artifact_path = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7/presentacion_propuesta_d_master.html"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Artifact Master HTML: {artifact_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
