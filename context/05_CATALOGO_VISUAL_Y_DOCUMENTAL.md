# Catálogo Visual y Documental del Proyecto — Hogar Oleiros

Este documento cataloga y enlaza todos los planos interactivos, visores web HTML, dossiers técnicos y renders en alta resolución generados a lo largo del proyecto, disponibles en el directorio [`history/`](file:///home/antigravity/landslore/oleiros/history).

---

## 1. Colección de Planos Técnicos de Ejecución CAD (ISO 128 / UNE 1032 — Propuesta D)

Todos los planos vectoriales de ejecución se generan paramétricamente mediante el motor [`cad_engine.py`](file:///home/antigravity/landslore/oleiros/cad_engine.py), [`generate_general_plans.py`](file:///home/antigravity/landslore/oleiros/generate_general_plans.py), [`generate_constructive_1_50_plans.py`](file:///home/antigravity/landslore/oleiros/generate_constructive_1_50_plans.py) y [`generate_p1_and_sections_plans.py`](file:///home/antigravity/landslore/oleiros/generate_p1_and_sections_plans.py):

| Código | Archivo SVG | Escala | Contenido Técnico de Ejecución |
| :--- | :--- | :--- | :--- |
| **A-01** | [`planta_baja_propuesta_d.svg`](file:///home/antigravity/landslore/oleiros/propuestas/planta_baja_propuesta_d.svg) | **1:100** | **Planta Baja General (Cota $\pm 0,00\text{ m}$) e Implantación en Parcela:** Ejes estructurales `A-E / 1-5`, pilares $25\times 25\text{ cm}$, muros multicapa con rayado `ANSI31`, triples líneas de cota encadenadas con trazos a $45^\circ$, círculos NHG $\varnothing 1,50\text{ m}$, cuadro de superficies y carpinterías `C-01..C-10`, cajetín ISO 7200. |
| **A-02** | [`planta_alta_propuesta_d.svg`](file:///home/antigravity/landslore/oleiros/propuestas/planta_alta_propuesta_d.svg) | **1:75** | **Planta Primera General (Cota $+3,15\text{ m}$) y Cubiertas Técnicas:** Galería acústica `4+4 Silence`, dormitorios infantiles con medianera ciega $R_w \ge 50\text{ dB}$ y estudio con luz Sur a $90^\circ$, Master Suite con vestidor y baño doble, balcón continuo Sur y campo solar FV $5,4\text{ kWp}$. |
| **E-01** | [`plano_constructivo_zona_norte_pb.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_constructivo_zona_norte_pb.svg) | **1:50** | **Ejecución e Instalaciones Zona Norte PB:** Pérgola 2 VE (Wallbox $7,4\text{ kW}$), Porche Norte ($+0,05\text{ m}$), Zaguán Mudroom (esclusa térmica + CGMP), Hall, Despacho Sanctasanctórum y Baño Cortesía PB con ante-distribuidor NHG. Trazados eléctricos, RJ45 Cat 6A, PEX AF/ACS y VMC. |
| **E-02** | [`plano_constructivo_centro_patio_cocina_pb.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_constructivo_centro_patio_cocina_pb.svg) | **1:50** | **Ejecución e Instalaciones Banda Central PB:** Patio Central Descubierto Corrala ($4,00\times 4,00\text{ m}$, drenaje cota cero y alcorque de Arce Japonés), Cocina Isla Santos ($2,80\times 1,00\text{ m}$, Bora Pure + conducto Ecotube en solera), Lavandería, Escalera Volada (17 peldaños) y Sala Técnica Passivhaus. |
| **E-03** | [`plano_constructivo_sur_salon_porche_pb.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_constructivo_sur_salon_porche_pb.svg) | **1:50** | **Ejecución e Instalaciones Zona Sur PB y Piscina:** Salón-Comedor ($44,00\text{ m}^2$), muro inercial de granito con chimenea estanca Stûv 21 ($\varnothing 150\text{ mm}$), Porche Sur ($36,00\text{ m}^2$, fondo $3,00\text{ m}$), Churrasqueira de granito y Piscina Salina ($7,50\times 3,50\text{ m}$). |
| **E-04** | [`plano_constructivo_planta_primera_p1.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_constructivo_planta_primera_p1.svg) | **1:50** | **Ejecución e Instalaciones Planta Primera Completa ($+3,15\text{ m}$):** Replanteo de tabiquería acústica, red VMC doble flujo por estancia, bajantes insonorizadas $\varnothing 110\text{ mm}$, datos Cat 6A y circuitos eléctricos de zona de noche. |
| **E-05** | [`plano_secciones_y_detalle_constructivo.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_secciones_y_detalle_constructivo.svg) | **1:50 / 1:20** | **Secciones Constructivas Longitudinal A-A' y Transversal B-B' (1:50) + 3 Detalles Constructivos (1:20):** Altimetría $Z$, ángulos solares de Oleiros ($70^\circ$ verano / $23^\circ$ invierno), Detalle `D-01` Cáviti + Barrera Anti-Radón CTE DB-HS6, Detalle `D-02` Umbral Cota Cero sobre Purenit + Canaleta AISI 316, y Detalle `D-03` Cubierta Plana Invertida Passivhaus. |

---

## 2. Visores Web Interactivos y Dossiers Técnicos

Los siguientes archivos HTML son interactivos, autónomos (no requieren servidor) y pueden abrirse en cualquier navegador web moderno:

| Documento | Ubicación | Descripción técnica y contenido |
| :--- | :--- | :--- |
| **Dossier Maestro Interactivo (Propuesta D)** | [`presentacion_propuesta_d_master.html`](file:///home/antigravity/landslore/oleiros/propuestas/presentacion_propuesta_d_master.html) | **Aplicación principal unificada (`index.html`).** Integra las 7 láminas técnicas CAD (`A-01`, `A-02`, `E-01..E-05`), el visor de fichas técnicas 1:20, el visor 3D Three.js y los 12 renders fotorrealistas. |
| **Visor CAD 1:20 de las 17 Estancias** | [`fichas_zoom_interactivas_propuesta_d.html`](file:///home/antigravity/landslore/oleiros/propuestas/fichas_zoom_interactivas_propuesta_d.html) | **17 Planos técnicos CAD interactivos a escala 1:20:** Muros multicapa con rayado `ANSI31`, acotación ISO 129 con trazos a $45^\circ$, círculos NHG $\varnothing 1,50\text{ m}$, mobiliario técnico y capas conmutables de enchufes, RJ45, interruptores, suelo radiante y VMC. |
| **Plano General Amueblado (Iteración 3)** | [`planos_amueblamiento_detallado_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/planos_amueblamiento_detallado_iter3.html) | **Plano maestro histórico (Iteración 3).** Incorpora las 25 zonas de PB y P1 clicables. |
| **Zoom-In al Centímetro (Iteración 3)** | [`planos_zoom_estancias_detalle_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/planos_zoom_estancias_detalle_iter3.html) | **Fichas técnicas estancia a estancia (histórico Iteración 3).** |
| **Visor 3D con Radar de Cámaras** | [`galeria_interactiva_casa_completa_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/galeria_interactiva_casa_completa_iter3.html) | Visor interactivo con plano 2D que muestra los puntos y conos de visión de cada render y despliega las perspectivas en alta resolución incrustadas. |
| **Dossier de Renders en Markdown** | [`galeria_completa_multiangulo_iter3.md`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/galeria_completa_multiangulo_iter3.md) | Dossier visual con carruseles de las 18 perspectivas organizadas por sectores de la casa. |
| **Presentación Web Completa para la Familia** | [`presentacion_hogar_oleiros.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/presentacion_hogar_oleiros.html) | Web interactiva para presentar el proyecto a familiares, con navegación por estancias, renders y resúmenes. |
| **Esquema de Ejecución de Instalaciones** | [`proyecto_ejecucion_instalaciones_oleiros.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/proyecto_ejecucion_instalaciones_oleiros.html) | Planos y diagramas de fontanería, electricidad, red RJ45, solar FV, aerotermia y riego. |
| **Memoria Técnica Original** | [`memoria_tecnica_ejecucion_oleiros.md`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/memoria_tecnica_ejecucion_oleiros.md) | Pliego de calidades y especificaciones para licitación constructora a precio cerrado. |
| **Comparador de Alternativas (Iteración 2)** | [`explorador_alternativas_iteracion2.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/explorador_alternativas_iteracion2.html) | Comparador visual entre la Opción 1 (patio pecera) y la Opción 2 (patio corrala con techo motorizado). |

---

## 2. Catálogo de Renders en Alta Resolución

Todos los archivos gráficos originales se encuentran en [`history/context/2_renders_alta_resolucion/`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion).

### Iteración 3 (Colección Principal y Validada):
1. **Render de Referencia Geométrica Estricta:**
   * [`iter3_estancia03_despacho_vista_sur_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_estancia03_despacho_vista_sur_1794546084600.jpg): **Despacho mirando de Norte a Sur.** Render verificado 100 % fiel al plano: a la derecha el Patio Corrala techado; a la izquierda la corredera abierta a la Cocina viendo la isla; en pared Este el sofá-cama y puerta al baño; en pared Oeste el escritorio, puerta al hall y TV. **(Esta imagen es el ancla visual obligatoria para generar el Ángulo 2 del despacho)**.
2. **Exteriores y Conexiones:**
   * [`iter3_03_fachada_norte_pergola_hall_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_03_fachada_norte_pergola_hall_1794544418385.jpg): Fachada Norte, pérgola para 2 coches y único acceso peatonal cubierto hacia el Hall.
   * [`iter3_08_comedor_porche_barbacoa_carbon_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_08_comedor_porche_barbacoa_carbon_1794544399344.jpg): Comedor principal abierto al porche Sur y a la barbacoa de carbón.
3. **Zonas Comunes y Patio Corrala:**
   * [`iter3_01_hall_galeria_patio_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_01_hall_galeria_patio_1794544380062.jpg): Vestíbulo principal (Hall) mirando al Sur por la galería con vista al patio corrala.
   * [`iter3_04_cocina_isla_desayunador_patio_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_04_cocina_isla_desayunador_patio_1794544380846.jpg): Cocina con isla Dekton de 3 m, placa Bora, desayunador y salida a corrala.
   * [`iter3_05_despacho_vistas_patio_corrala_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_05_despacho_vistas_patio_corrala_1794544397502.jpg): Puesto de trabajo del despacho con vistas a la vegetación del patio.
   * [`iter3_06_bano_pb_doble_acceso_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_06_bano_pb_doble_acceso_1794544414529.jpg): Baño PB con antebaño de doble acceso (hacia despacho y hacia cocina).
   * [`iter3_07_salon_chimenea_tv77_porche_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_07_salon_chimenea_tv77_porche_1794544380443.jpg): Salón principal con chimenea de leña, TV OLED 77" empotrada y salida a jardín Sur.
   * [`iter3_09_lavanderia_plancha_tecnico_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_09_lavanderia_plancha_tecnico_1794544415498.jpg): Lavandería con lavadora y secadora en columna, encimera y pila.
4. **Planta Primera (+3,15 m):**
   * [`iter3_02_corrala_pasillo_p1_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_02_corrala_pasillo_p1_1794544396971.jpg): Pasillo superior acristalado sobre el patio corrala con balizas LED nocturnas.
   * [`iter3_10_dormitorios_ninos_angulo_estudio_balcon_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_10_dormitorios_ninos_angulo_estudio_balcon_1794544384001.jpg): Dormitorios infantiles con escritorio en pared lateral Este y salida al balcón Sur.
   * [`iter3_11_bano_hijos_doble_seno_p1_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_11_bano_hijos_doble_seno_p1_1794544400985.jpg): Baño compartido de los niños con doble lavabo y toallero.
   * [`iter3_12_suite_vestidor_bano_matrimonio_p1_...jpg`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_3/iter3_12_suite_vestidor_bano_matrimonio_p1_1794544424017.jpg): Suite principal con vestidor de paso y baño privado.

### Colecciones Previas (Históricas):
* **Iteración 2 (5 imágenes):** Ubicadas en [`history/context/2_renders_alta_resolucion/iteracion_2/`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_2), exploraron la primera versión del patio corrala techado y las variantes de cama abatible para el despacho.
* **Iteración 1 (8 imágenes):** Ubicadas en [`history/iteracion1/`](file:///home/antigravity/landslore/oleiros/history/iteracion1) y [`history/context/2_renders_alta_resolucion/iteracion_1/`](file:///home/antigravity/landslore/oleiros/history/context/2_renders_alta_resolucion/iteracion_1), representaron el anteproyecto conceptual de la vivienda.

---

## 3. Historial de Conversación y Logs Técnicos

Los registros completos del diálogo con el arquitecto y los parámetros del agente previo se conservan en:
* **Transcripción legible paso a paso:** [`CONVERSACION_COMPLETA_LEGIBLE.md`](file:///home/antigravity/landslore/oleiros/history/context/3_conversacion_y_contexto/CONVERSACION_COMPLETA_LEGIBLE.md).
* **Logs originales estructurados (JSONL):**
  * [`transcript_full.jsonl`](file:///home/antigravity/landslore/oleiros/history/context/3_conversacion_y_contexto/raw_logs/transcript_full.jsonl)
  * [`transcript.jsonl`](file:///home/antigravity/landslore/oleiros/history/context/3_conversacion_y_contexto/raw_logs/transcript.jsonl)
