#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Visor Interactivo Completo de Planta Baja para Presentación Familiar
Hogar Oleiros (Pabellón Bioclimático Atlántico)
"""

def build_presentation_html():
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hogar Oleiros · Estudio Detallado de Planta Baja (1:20)</title>
  <style>
    :root {
      --bg: #070b14;
      --card-bg: #0b1120;
      --border: #1e293b;
      --primary: #38bdf8;
      --accent: #f59e0b;
      --emerald: #10b981;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.5;
    }
    header {
      background: var(--card-bg);
      padding: 1.25rem 2rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .tabs-nav {
      display: flex;
      background: #0f172a;
      padding: 0.5rem 2rem;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
    }
    .tab-btn {
      background: transparent;
      color: var(--text-muted);
      border: 1px solid transparent;
      padding: 0.65rem 1.25rem;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tab-btn:hover {
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
    }
    .tab-btn.active {
      background: var(--card-bg);
      color: var(--primary);
      border-color: var(--primary);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }
    .main-container {
      padding: 1.5rem 2rem;
      max-width: 1900px;
      margin: 0 auto;
    }
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
      animation: fadeIn 0.25s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .viewer-frame {
      width: 100%;
      height: 760px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #050811;
      overflow: hidden;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    }
    .viewer-frame object, .viewer-frame embed, .viewer-frame iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
    .grid-info {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1.5rem;
      margin-top: 1.5rem;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
    }
    .card h3 {
      color: var(--primary);
      font-size: 1rem;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card ul {
      list-style-type: none;
      padding-left: 0;
    }
    .card li {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 0.45rem;
      display: flex;
      justify-content: space-between;
      gap: 1rem;
    }
    .card li strong {
      color: var(--text);
    }
    .btn-action {
      background: #1e293b;
      color: #38bdf8;
      border: 1px solid #334155;
      padding: 0.4rem 0.8rem;
      border-radius: 4px;
      font-size: 0.75rem;
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .btn-action:hover {
      background: #38bdf8;
      color: #0b1120;
    }
  </style>
</head>
<body>
  <header>
    <div>
      <span class="badge">PROYECTO HOGAR OLEIROS · PLANTA BAJA DEFINITIVA</span>
      <h1 style="font-size: 1.35rem; margin-top: 0.35rem;">Visor Arquitectónico de Planta Baja: Zoom-in Detallado (1:20)</h1>
      <p style="font-size: 0.85rem; color: var(--text-muted);">Liáns, Concello de Oleiros (A Coruña) · Superficie Útil Interior: 109,25 m² · Huella computable: 119,50 m²</p>
    </div>
    <div style="display: flex; gap: 1rem; align-items: center;">
      <div style="text-align: right;">
        <span style="font-size: 0.85rem; color: var(--accent); font-weight: 700;">Crujía Sur Vividera: 76,55 m²</span><br>
        <span style="font-size: 0.75rem; color: var(--emerald); font-weight: 600;">Cocina Unificada Santos: 20,80 m²</span>
      </div>
    </div>
  </header>

  <nav class="tabs-nav">
    <button class="tab-btn active" onclick="showTab('tab-sur')">🛋️ Salón, Comedor y Porche Sur [S-01]</button>
    <button class="tab-btn" onclick="showTab('tab-patio')">🌳 Patio Claustro y Escalera Volada [N-01]</button>
    <button class="tab-btn" onclick="showTab('tab-oeste')">🏄 Ala Oeste: Surf, Lavandería y Caseta [W-01]</button>
    <button class="tab-btn" onclick="showTab('tab-acceso')">🚪 Ala Norte: Acceso, Mudroom y Despacho [A-01]</button>
    <button class="tab-btn" onclick="showTab('tab-cocina')">🍳 Cocina Santos con Cava e Isla [K-01]</button>
    <button class="tab-btn" onclick="showTab('tab-general')">🌟 Master Plan PB Completo [Definitivo]</button>
  </nav>

  <div class="main-container">

    <!-- PESTAÑA 1: SALÓN, COMEDOR Y PORCHE SUR -->
    <div id="tab-sur" class="tab-pane active">
      <div class="viewer-frame">
        <object data="plano_salon_comedor_porche_planta.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>[PB-10] Salón Principal con Chimenea (26,50 m²)</h3>
          <ul>
            <li>Chimenea Passivhaus: <strong>Hogar estanco con cristal 3 caras</strong></li>
            <li>Bancada suspendida: <strong>Roble tostado macizo en pared oeste</strong></li>
            <li>Zona estar: <strong>Sofá en L (3,60×2,60m) + mesa centro 1,40m</strong></li>
            <li>Audiovisual: <strong>Mueble TV 85" con altavoces empotrados</strong></li>
            <li>Luz y vistas: <strong>Cristalera norte al patio y gran corredera sur</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-11] Comedor Principal Interior (17,50 m²)</h3>
          <ul>
            <li>Mesa de banquetes: <strong>Roble macizo 3,00 × 1,10 m (10-12 Pax)</strong></li>
            <li>Iluminación: <strong>Lámpara escultórica suspendida DALI (2700K)</strong></li>
            <li>Conexión Cocina: <strong>Emboquillado diáfano fluido de 2,40 m</strong></li>
            <li>Paso libre NHG: <strong>Circulación perimetral holgada de 1,20 m</strong></li>
            <li>Pavimento continuo: <strong>Caliza natural apomazada 120×120 cm</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-14] Porche Sur Techado Expandido (32,55 m²)</h3>
          <ul>
            <li>Dimensiones: <strong>10,84 m de longitud × 3,00 m de fondo</strong></li>
            <li>Gran corredera C-07: <strong>Cortizo Cor Vision Plus 7,50m cota cero</strong></li>
            <li>Zona Chill-out: <strong>Salón exterior de teca y tapicería náutica</strong></li>
            <li>Comedor exterior: <strong>Mesa 8 comensales + módulo barbacoa grill</strong></li>
            <li>Protección solar: <strong>Voladizo P1 que bloquea el sol de verano</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- PESTAÑA 2: PATIO CLAUSTRO, ESCALERA Y HUECOS MUERTOS -->
    <div id="tab-patio" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_patio_escalera_huecos_planta.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>[PB-07] Patio Central Corrala / Claustro (16,00 m²)</h3>
          <ul>
            <li>Dimensiones: <strong>4,00 × 4,00 m entre cristaleras de suelo a techo</strong></li>
            <li>Pulmón bioclimático: <strong>Ventilación cruzada noche/día y luz cenital</strong></li>
            <li>Jardinería: <strong>Parterre central con arce japonés iluminado IP68</strong></li>
            <li>Pavimento: <strong>Tarima de Iroko FSC sobre plots a cota cero</strong></li>
            <li>Pluviales: <strong>Arqueta sifónica a depósito enterrado de 5.000 L</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-12] Escalera Volada de Roble Macizo (5,20 m²)</h3>
          <ul>
            <li>Peldaños volados: <strong>17 peldaños de roble macizo 80 mm volados</strong></li>
            <li>Geometría DB-SUA: <strong>Huella 28,0 cm · Contrahuella 17,65 cm (Blondel 63,3)</strong></li>
            <li>Barandilla de seguridad: <strong>Vidrio laminar Silence 10+10 mm embutido</strong></li>
            <li>Iluminación nocturna: <strong>LED cálido 2700K fresado bajo cada peldaño</strong></li>
            <li>Anchura de paso: <strong>1,10 m libre y diáfana hacia el patio</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>Aprovechamiento Quirúrgico de Huecos Muertos (3,80 m³)</h3>
          <ul>
            <li>Zona baja (Peldaños 1-6): <strong>4 gavetas push zapatero profundo (1,20m)</strong></li>
            <li>Zona media (Peldaños 7-11): <strong>Armario robot aspirador y maletas</strong></li>
            <li>Zona alta (Peldaños 12-17): <strong>Paso libre cómodo y registro de shunts</strong></li>
            <li>Estética enrasada: <strong>Frentes ciegos sin tirador a paño de pared</strong></li>
            <li>Eficiencia total: <strong>Cero metros cúbicos desperdiciados</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- PESTAÑA 3: ALA OESTE DE SERVICIO -->
    <div id="tab-oeste" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_ala_oeste_servicio_planta.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>[PB-13] Sala Técnica Passivhaus / Surf & Bicis (7,60 m²)</h3>
          <ul>
            <li>Aerotermia: <strong>Vaillant aroTHERM + interacumulador ACS 300L inox</strong></li>
            <li>Ventilación VMC: <strong>Zehnder ComfoAir Q350 con recuperador >90%</strong></li>
            <li>Fotovoltaica: <strong>Inversor solar 6 kW + espacio batería 10 kWh</strong></li>
            <li>Zona Surf: <strong>Rack 4 tablas + pila endulzado inox con manguera</strong></li>
            <li>Suelo técnico: <strong>Epoxi continuo C3 con sumidero sifónico (-0,05m)</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-13B] Lavandería y Plancha Oeste (11,60 m²)</h3>
          <ul>
            <li>Ergonomía: <strong>Torre lavadora y secadora elevada a +30 cm</strong></li>
            <li>Bancada corrida: <strong>2,40 m de encimera con fregadero auxiliar hondo</strong></li>
            <li>Secado rápido: <strong>Extracción VMC-E 45 m³/h para ropa en invierno</strong></li>
            <li>Salida exterior: <strong>Puerta vidriera hacia tendedero cubierto oeste</strong></li>
            <li>Iluminación natural: <strong>Ventana cenital de tejado tipo Velux</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-13C] Caseta de Jardín / Cortacésped (5,20 m²)</h3>
          <ul>
            <li>Acceso directo: <strong>Puerta enrasada de madera desde el Porche Sur</strong></li>
            <li>Equipamiento: <strong>Base robot cortacésped, herramientas y mangueras</strong></li>
            <li>Almacenaje invierno: <strong>Guarda de cojines y mobiliario lounge exterior</strong></li>
            <li>Función pasiva: <strong>Escudo cortavientos contra temporales del suroeste</strong></li>
            <li>Pavimento: <strong>Hormigón fratasado continuo de alta resistencia</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- PESTAÑA 4: ALA NORTE (ACCESO, MUDROOM, DESPACHO Y BAÑO) -->
    <div id="tab-acceso" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_acceso_planta_esquematica.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>[PB-03] Zaguán Mudroom Térmico (5,80 m²)</h3>
          <ul>
            <li>Banco zapatero: <strong>1,60 × 0,45 m en roble con cajones inferiores</strong></li>
            <li>Gabanero empotrado: <strong>1,25 × 0,60 m integrado para abrigos mojados</strong></li>
            <li>Armario secador: <strong>Módulo térmico deshumidificado trajes surf</strong></li>
            <li>Esclusa térmica: <strong>Puerta P-02 cortavientos hacia el hall</strong></li>
            <li>Suelo: <strong>Porcelánico C3 gris pizarra antideslizante</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-05] Despacho / Suite Invitados PB (11,50 m²)</h3>
          <ul>
            <li>Teletrabajo: <strong>Mesa ergonómica a 90° con electrificación y datos</strong></li>
            <li>Flexibilidad suite: <strong>Sofá-cama de 140 cm para dormitorio PB</strong></li>
            <li>Aislamiento acústico: <strong>Tabique reforzado Habito con lana roca (Rw≥45dB)</strong></li>
            <li>Ventanas: <strong>Ventana norte C-03 (h=95) y ventanal fijo al patio sur</strong></li>
            <li>Calidad aire: <strong>Impulsión VMC-I 35 m³/h Zehnder</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>[PB-06] Baño Completo PB + Distribuidor Neutro (5,20 m²)</h3>
          <ul>
            <li>Normativa Galicia: <strong>Distribuidor neutro con doble puerta s/ Decreto 29/2010</strong></li>
            <li>Ducha cota cero: <strong>1,15 × 0,90 m con sumidero lineal oculto AISI 316</strong></li>
            <li>Sanitarios: <strong>Inodoro suspendido Geberit y lavabo suspendido 90cm</strong></li>
            <li>Ventilación natural: <strong>Ventana alta C-04 (h=160cm) que preserva intimidad</strong></li>
            <li>Extracción mecánica: <strong>VMC-E 50 m³/h</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- PESTAÑA 5: COCINA UNIFICADA SANTOS -->
    <div id="tab-cocina" class="tab-pane">
      <div class="viewer-frame">
        <object data="plano_cocina_planta_esquematica.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
      <div class="grid-info">
        <div class="card">
          <h3>Espacio Unificado Santos Fine (20,80 m²)</h3>
          <ul>
            <li>Frente Este continuo: <strong>6,00 m con bancada Dekton de 3,00 m</strong></li>
            <li>Ventanal panorámico C-07: <strong>3,00 × 0,80 m con sol matinal de levante</strong></li>
            <li>Cava de vinos Santos: <strong>Columna climatizada de 60 botellas iluminada</strong></li>
            <li>Gran despensa Sur: <strong>Módulos suelo-techo integrados cara al comedor</strong></li>
            <li>Columnas Norte: <strong>Frigorífico XXL, congelador y torre hornos Bosch</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>Gran Isla Central Santos Fine (3,60 × 1,10 m)</h3>
          <ul>
            <li>Cocción integrada: <strong>Placa Bora Pure con extracción filtrante enrasada</strong></li>
            <li>Zona de aguas: <strong>Fregadero bajo encimera 70 cm con grifo extraíble</strong></li>
            <li>Barra de desayunos: <strong>Voladizo ergonómico de 35 cm con 5 taburetes altos</strong></li>
            <li>Orientación: <strong>Taburetes orientados a la cocina con vistas al patio</strong></li>
            <li>Conexión patio: <strong>Cristalera corredera Cortizo C-06 de 2,40 m</strong></li>
          </ul>
        </div>
        <div class="card">
          <h3>Instalaciones y Normativa (K-03 / K-04)</h3>
          <ul>
            <li>Electricidad REBT: <strong>Circuito C3 (25A Bora Pure), C4.1 a C4.6 individuales</strong></li>
            <li>Tomas de bancada: <strong>4 bases Schuko a +1,05m sobre encimera Dekton</strong></li>
            <li>Iluminación técnica: <strong>Carril magnético 48V de 3,00m + tira LED continua</strong></li>
            <li>Escenas lumínicas: <strong>4 ambientes preprogramados (Cocina, Desayuno, Noche, Fiesta)</strong></li>
            <li>Comunicación: <strong>Puerta corredera P-06 hacia distribuidor neutro y baño</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- PESTAÑA 6: MASTER PLAN PLANTA BAJA COMPLETO -->
    <div id="tab-general" class="tab-pane">
      <div class="viewer-frame">
        <object data="v2/planos/planta_baja_definitiva.svg" type="image/svg+xml" width="100%" height="100%"></object>
      </div>
    </div>

  </div>

  <script>
    function showTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
    }
  </script>
</body>
</html>
"""

def main():
    print("=== Generando Visor Interactivo Maestro de Planta Baja ===")
    html = build_presentation_html()
    with open("planta_baja_estudio_familiar_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✓ planta_baja_estudio_familiar_interactivo.html generado")

if __name__ == "__main__":
    main()
