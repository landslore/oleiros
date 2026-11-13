#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import os
import shutil

RENDERS_DIR = "/home/antigravity/landslore/oleiros/propuestas/renders"
PROPUESTAS_DIR = "/home/antigravity/landslore/oleiros/propuestas"
ARTIFACT_DIR = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7"

def get_base64_image(filename):
    path = os.path.join(RENDERS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
    return ""

img_fachada = get_base64_image("fachada_norte_render.jpg")
img_zaguan = get_base64_image("zaguan_mudroom_render.jpg")
img_hall = get_base64_image("hall_recibidor_render.jpg")
img_patio = get_base64_image("patio_corrala_render.jpg")
img_cocina = get_base64_image("cocina_isla_render.jpg")
img_salon = get_base64_image("salon_jardin_render.jpg")
img_despacho = get_base64_image("despacho_render.jpg")
img_bano_pb = get_base64_image("bano_pb_render.jpg")
img_porche = get_base64_image("porche_sur_render.jpg")
img_galeria = get_base64_image("galeria_escalera_render.jpg")
img_suite = get_base64_image("suite_principal_render.jpg")
img_ninos = get_base64_image("dormitorio_infantil_render.jpg")

with open(os.path.join(PROPUESTAS_DIR, 'planta_baja_propuesta_d.svg'), 'r') as f:
    raw_svg_pb = f.read()

with open(os.path.join(PROPUESTAS_DIR, 'planta_alta_propuesta_d.svg'), 'r') as f:
    raw_svg_p1 = f.read()
with open(os.path.join(PROPUESTAS_DIR, 'plano_constructivo_zona_norte_pb.svg'), 'r') as f:
    raw_svg_norte = f.read()
with open(os.path.join(PROPUESTAS_DIR, 'plano_constructivo_centro_patio_cocina_pb.svg'), 'r') as f:
    raw_svg_centro = f.read()
with open(os.path.join(PROPUESTAS_DIR, 'plano_constructivo_sur_salon_porche_pb.svg'), 'r') as f:
    raw_svg_sur = f.read()


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
        🖼️ Renders de Cada Estancia (12)
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
         SECCIÓN 1: GALERÍA COMPLETA DE RENDERS ESTANCIA POR ESTANCIA
         ═════════════════════════════════════════════════════════════════════════ -->
    <section id="sec-renders" class="space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-3xl shadow-xl">
        <div>
          <span class="badge bg-sky-500/20 text-sky-400 border border-sky-500/30">VISUALIZACIÓN ARQUITECTÓNICA COMPLETA</span>
          <h2 class="text-xl md:text-2xl font-black text-white mt-1">Todas las Estancias al Detalle: Atmósfera, Luz &amp; Acabados</h2>
          <p class="text-xs md:text-sm text-slate-400 mt-0.5">Renders fotorrealistas corregidos estancia por estancia: el patio corrala central, la cocina con isla, el salón abierto al sur y las suites.</p>
        </div>
      </div>

      <!-- GRID DE RENDERS (12 ESTANCIAS) -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

        <!-- 1. PATIO CORRALA (EL CORAZÓN) -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_patio}" alt="Patio Corrala Habitable" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-emerald-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 05 · EL CORAZÓN DE LA CASA</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Patio Corrala Habitable y 100% Accesible</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                El único patio interior de la casa: 16,0 m² abiertos al cielo con drenaje natural sobre terreno real. Tarima de iroko a cota cero, banco de lectura bajo alero de 80 cm y arce japonés.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ 16,0 m² · Cero efecto invernadero · Triple corredera elevable Cortizo
            </div>
          </div>
        </div>

        <!-- 2. COCINA CON ISLA Y PATIO -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_cocina}" alt="Cocina con Isla y Desayunador" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-amber-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 06 · COCINA CON ISLA</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Cocina con Isla Dekton Kelya &amp; Desayunador</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Isla de 2,80 × 1,00 m con placa Bora Pure de extracción hacia abajo. Mueble desayunador con puertas escamoteables y corredera de 3 m abierta al Patio Corrala.
              </p>
            </div>
            <div class="text-[11px] font-mono text-amber-400 bg-amber-950/50 p-2.5 rounded-xl border border-amber-900/60">
              ✓ 15,2 m² útiles · Techo 100% limpio sin campanas · Santos Fine Cashmere
            </div>
          </div>
        </div>

        <!-- 3. SALÓN PRINCIPAL Y JARDÍN SUR -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_salon}" alt="Salón Principal con Chimenea" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-sky-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 08 · SALÓN CON CHIMENEA</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Salón Principal Abierto al Porche Sur y Jardín</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Sofá en L en lino arena frente a la chimenea estanca de granito. Gran corredera de 5 metros abierta de par en par al Porche Sur cubierto, césped con hortensias y piscina.
              </p>
            </div>
            <div class="text-[11px] font-mono text-sky-400 bg-sky-950/50 p-2.5 rounded-xl border border-sky-900/60">
              ✓ 26,5 m² útiles · Chimenea estanca con aire exterior · Cero segundo patio
            </div>
          </div>
        </div>

        <!-- 4. DESPACHO SANCTASANCTÓRUM -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_despacho}" alt="Despacho Sanctasanctórum" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-emerald-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 03 · TELETRABAJO &amp; INVITADOS</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Despacho Sanctasanctórum &amp; Suite Serena</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Mesa ergonómica con luz difusa a 90° de ventana Norte (cero reflejos en monitor) y cristalera al patio ajardinado. Aislamiento acústico Rw ≥ 38 dB y sofá-cama con acceso privado al Baño PB.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ 11,5 m² útiles · Doble toma RJ45 Cat 6A (10 Gbps) · Cero servidumbre
            </div>
          </div>
        </div>

        <!-- 5. HALL Y RECIBIDOR NOBLE -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_hall}" alt="Hall Principal" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-purple-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 02 · RECEPCIÓN NOBLE</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Hall / Recibidor Principal (Vistas al Claustro)</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Entrada por puerta pivotante de iroko macizo (1,10 m). Al cruzar el umbral, la mirada se fuga directamente al arce japonés a través de una gran cristalera de suelo a techo.
              </p>
            </div>
            <div class="text-[11px] font-mono text-purple-400 bg-purple-950/50 p-2.5 rounded-xl border border-purple-900/60">
              ✓ 10,4 m² · Consola flotante y espejo LED · Armario gabanero empotrado
            </div>
          </div>
        </div>

        <!-- 6. ZAGUÁN MUDROOM TÉRMICO -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_zaguan}" alt="Zaguán Mudroom" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-amber-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 01 · ACCESO DIARIO</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Zaguán Mudroom Térmico (Acceso Pérgola)</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Esclusa térmica con banco descalzador de roble, zapatero ventilado para 16 pares, armario secador de lluvia y puerta corredera de vidrio estriado hacia el Hall.
              </p>
            </div>
            <div class="text-[11px] font-mono text-amber-400 bg-amber-950/50 p-2.5 rounded-xl border border-amber-900/60">
              ✓ 5,8 m² · Paso directo desde aparcamiento cubierto · Porcelánico C3
            </div>
          </div>
        </div>

        <!-- 7. BAÑO COMPLETO PB -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_bano_pb}" alt="Baño Completo PB" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-sky-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 04 · BAÑO NOBLE PB</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Baño Completo PB &amp; Distribuidor Neutro</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Acceso desde distribuidor neutro (sin servidumbre a cocina, 100% legal NHG). Ducha walk-in cota cero de 120 × 80 cm, mueble suspendido roble 90 cm e inodoro Geberit Rimless.
              </p>
            </div>
            <div class="text-[11px] font-mono text-sky-400 bg-sky-950/50 p-2.5 rounded-xl border border-sky-900/60">
              ✓ 5,2 m² · Porcelánico gran formato caliza · Ventana exterior practicable
            </div>
          </div>
        </div>

        <!-- 8. PORCHE SUR CUBIERTO (FONDO 3M) -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_porche}" alt="Porche Sur Expandido" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-emerald-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 10 · VIDA EXTERIOR SUR</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Porche Sur Cubierto Expandido (Fondo 3,00 m)</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                36 m² cubiertos protegidos de la lluvia atlántica. Churrasqueira de granito Zimbabwe, comedor exterior de 10 plazas, salón lounge y vistas abiertas a la piscina y jardín.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ Fondo 3,00 m real · Piscina 3,5 × 7,5 m · Armario robot cortacésped
            </div>
          </div>
        </div>

        <!-- 9. GALERÍA ACÚSTICA Y ESCALERA P1 -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_galeria}" alt="Galería Acústica y Escalera" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-purple-500 text-slate-950 font-extrabold shadow-md">ESTANCIA 12 · DISTRIBUIDOR P1</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Galería Acústica &amp; Escalera de Roble</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Mampara acristalada fija 4+4 Silence (aísla 42 dB entre plantas) con vistas cenitales sobre el patio claustral. Escalera con peldaños volados de roble y balizas LED de cortesía.
              </p>
            </div>
            <div class="text-[11px] font-mono text-purple-400 bg-purple-950/50 p-2.5 rounded-xl border border-purple-900/60">
              ✓ 8,2 m² · Vidrio 4+4 Silence · Balizas de zócalo para trayectos nocturnos
            </div>
          </div>
        </div>

        <!-- 10. SUITE PRINCIPAL MATRIMONIO P1 -->
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
                Ala Este privada de 31,2 m² con cama King Size orientada al Sur, balcón corrido con barandilla continua de vidrio estructural, vestidor de paso en doble hilera y baño doble.
              </p>
            </div>
            <div class="text-[11px] font-mono text-sky-400 bg-sky-950/50 p-2.5 rounded-xl border border-sky-900/60">
              ✓ 31,2 m² suite · Ducha italiana doble · Frentes de vidrio ahumado
            </div>
          </div>
        </div>

        <!-- 11. DORMITORIOS INFANTILES -->
        <div class="render-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
          <div class="relative overflow-hidden aspect-video bg-slate-950">
            <img src="{img_ninos}" alt="Dormitorio Infantil Niña/Niño" class="w-full h-full object-cover">
            <div class="absolute top-3 left-3">
              <span class="badge bg-emerald-500 text-slate-950 font-extrabold shadow-md">ESTANCIAS 13-14 · DORMITORIOS HIJOS</span>
            </div>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Dormitorios Infantiles (Estudio a 90°)</h3>
              <p class="text-xs text-slate-400 mt-1 leading-relaxed">
                Pupitre suspendido de 1,80 m con luz natural lateral a 90° de balconera sur (cero contraluz ni reflejos en portátil), cama tapizada, armario empotrado y salida a balcón sur.
              </p>
            </div>
            <div class="text-[11px] font-mono text-emerald-400 bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-900/60">
              ✓ 14,6 m² cada uno · Aislamiento acústico medianero Rw ≥ 50 dB
            </div>
          </div>
        </div>

        <!-- 12. FACHADA NORTE Y ACCESO -->
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
        <div class="flex flex-wrap gap-2.5 w-full sm:w-auto">
          <button type="button" onclick="showFloorSVG('pb')" id="btn-svg-pb" class="py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-sky-600 text-white border border-sky-400 shadow-lg shadow-sky-600/30 min-h-[44px] flex items-center justify-center cursor-pointer transition">
            Planta Baja (±0,00 m)
          </button>
          <button type="button" onclick="showFloorSVG('p1')" id="btn-svg-p1" class="py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition">
            Planta Primera (+3,15 m)
          </button>
          <button type="button" onclick="showFloorSVG('norte')" id="btn-svg-norte" class="py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition">
            🛠️ 1:50 Zona Norte PB
          </button>
          <button type="button" onclick="showFloorSVG('centro')" id="btn-svg-centro" class="py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition">
            🍳 1:50 Centro PB
          </button>
          <button type="button" onclick="showFloorSVG('sur')" id="btn-svg-sur" class="py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-orange-500 text-slate-950 border border-orange-300 shadow-lg shadow-orange-500/30 min-h-[44px] flex items-center justify-center cursor-pointer transition">
            🔥 1:50 Sur PB (Salón, Porche &amp; Piscina)
          </button>
        </div>
      </div>

      <!-- VISOR SVG EMBEBIDO -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-4 md:p-6 shadow-2xl flex justify-center">
        <div id="svg-container-pb" class="w-full flex justify-center overflow-x-auto rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner p-2">
          {raw_svg_pb}
        </div>
        <div id="svg-container-p1" class="w-full flex justify-center overflow-x-auto hidden rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner p-2">
          {raw_svg_p1}
        </div>
        <div id="svg-container-norte" class="w-full flex justify-center overflow-x-auto hidden rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner p-2">
          {raw_svg_norte}
        </div>
        <div id="svg-container-centro" class="w-full flex justify-center overflow-x-auto hidden rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner p-2">
          {raw_svg_centro}
        </div>
        <div id="svg-container-sur" class="w-full flex justify-center overflow-x-auto hidden rounded-2xl border border-slate-800 bg-[#0f172a] shadow-inner p-2">
          {raw_svg_sur}
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
            <span class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">COMPATIBLE AL 100% CON MAC (KEYNOTE) &amp; PC</span>
          </div>
          <h2 class="text-2xl md:text-3xl font-black text-white">Presentación PowerPoint Ejecutiva (.pptx)</h2>
          <p class="text-sm text-slate-300 leading-relaxed">
            Hemos preparado la presentación oficial en formato PowerPoint de alta gama (compatible nativamente con <strong>Keynote en Mac</strong> y <strong>Microsoft PowerPoint</strong>). Incluye 14 diapositivas completas con la portada, criterios de diseño, planos y cada estancia con su render fotorrealista y desglose técnico.
          </p>
          <div class="flex flex-wrap gap-4 pt-2">
            <a href="Presentacion_Hogar_Oleiros_Propuesta_D.pptx" download class="px-6 py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-extrabold text-sm shadow-xl shadow-sky-500/25 flex items-center gap-2 transition">
              <span>📥 Descargar Archivo PowerPoint (.pptx)</span>
              <span class="text-xs bg-white/20 px-2 py-0.5 rounded-full font-mono">10,1 MB</span>
            </a>
            <a href="https://docs.google.com/presentation/d/1AHYDhaDiH4zxxbKxN8ffe-7R8t2RK37y-VMJbs5lKhw/edit" target="_blank" class="px-6 py-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-sm border border-slate-700 flex items-center gap-2 transition">
              <span>☁️ Abrir en Google Slides</span>
            </a>
          </div>
        </div>

        <div class="w-full md:w-80 p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2 text-xs">
          <div class="font-bold text-sky-400 uppercase tracking-wider text-[11px]">14 Diapositivas Estancia por Estancia:</div>
          <p>• <strong>01:</strong> Portada &amp; Datos Clave</p>
          <p>• <strong>02:</strong> Fachada Norte y Acceso</p>
          <p>• <strong>03:</strong> Zaguán Mudroom Térmico</p>
          <p>• <strong>04:</strong> Hall / Recibidor Principal</p>
          <p>• <strong>05:</strong> Patio Corrala Habitable</p>
          <p>• <strong>06:</strong> Cocina con Isla y Desayunador</p>
          <p>• <strong>07:</strong> Salón Principal &amp; Jardín Sur</p>
          <p>• <strong>08:</strong> Despacho Sanctasanctórum</p>
          <p>• <strong>09:</strong> Baño Completo PB</p>
          <p>• <strong>10:</strong> Porche Sur Expandido (Fondo 3m)</p>
          <p>• <strong>11:</strong> Galería Acústica &amp; Escalera</p>
          <p>• <strong>12:</strong> Suite Principal Matrimonio</p>
          <p>• <strong>13:</strong> Dormitorios Infantiles (Luz 90°)</p>
          <p>• <strong>14:</strong> Instalaciones &amp; Presupuesto</p>
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
      const cNorte = document.getElementById('svg-container-norte');
      const cCentro = document.getElementById('svg-container-centro');
      const cSur = document.getElementById('svg-container-sur');
      const bPb = document.getElementById('btn-svg-pb');
      const bP1 = document.getElementById('btn-svg-p1');
      const bNorte = document.getElementById('btn-svg-norte');
      const bCentro = document.getElementById('btn-svg-centro');
      const bSur = document.getElementById('btn-svg-sur');

      cPb.classList.add('hidden');
      cP1.classList.add('hidden');
      cNorte.classList.add('hidden');
      cCentro.classList.add('hidden');
      cSur.classList.add('hidden');

      bPb.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition';
      bP1.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition';
      bNorte.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition';
      bCentro.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition';
      bSur.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 border border-slate-700 hover:text-white min-h-[44px] flex items-center justify-center cursor-pointer transition';

      if (fl === 'pb') {{
        cPb.classList.remove('hidden');
        bPb.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-sky-600 text-white border border-sky-400 shadow-lg shadow-sky-600/30 min-h-[44px] flex items-center justify-center cursor-pointer transition';
      }} else if (fl === 'p1') {{
        cP1.classList.remove('hidden');
        bP1.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-sky-600 text-white border border-sky-400 shadow-lg shadow-sky-600/30 min-h-[44px] flex items-center justify-center cursor-pointer transition';
      }} else if (fl === 'norte') {{
        cNorte.classList.remove('hidden');
        bNorte.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-amber-500 text-slate-950 border border-amber-300 shadow-lg shadow-amber-500/30 min-h-[44px] flex items-center justify-center cursor-pointer transition';
      }} else if (fl === 'centro') {{
        cCentro.classList.remove('hidden');
        bCentro.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-emerald-500 text-slate-950 border border-emerald-300 shadow-lg shadow-emerald-500/30 min-h-[44px] flex items-center justify-center cursor-pointer transition';
      }} else if (fl === 'sur') {{
        cSur.classList.remove('hidden');
        bSur.className = 'py-2.5 px-4 rounded-xl text-xs sm:text-sm font-bold bg-orange-500 text-slate-950 border border-orange-300 shadow-lg shadow-orange-500/30 min-h-[44px] flex items-center justify-center cursor-pointer transition';
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

    artifact_path = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7/presentacion_propuesta_d_master.html"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Artifact Master HTML: {artifact_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
    target_path = "/home/antigravity/landslore/oleiros/propuestas/presentacion_propuesta_d_master.html"
    files_to_sync = [
        'fichas_zoom_interactivas_propuesta_d.html',
        'modelo_3d_propuesta_d_homemaker.html',
        'planta_baja_propuesta_d.svg',
        'planta_alta_propuesta_d.svg',
        'Presentacion_Hogar_Oleiros_Propuesta_D.pptx',
        'plano_constructivo_zona_norte_pb.svg',
        'plano_constructivo_centro_patio_cocina_pb.svg',
        'plano_constructivo_sur_salon_porche_pb.svg'
    ]
    for fn in files_to_sync:
        src = os.path.join(PROPUESTAS_DIR, fn)
        if os.path.exists(src):
            shutil.copyfile(src, fn)
            shutil.copyfile(src, os.path.join(ARTIFACT_DIR, fn))
            print(f'Synced {fn} to root and artifact')

    shutil.copyfile(target_path, 'index.html')
    shutil.copyfile(target_path, os.path.join(ARTIFACT_DIR, 'index.html'))
    print('Updated index.html at root and artifact')
