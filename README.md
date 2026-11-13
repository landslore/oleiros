# Hogar Oleiros — Pabellón con Patio Corrala Habitable

Proyecto integral de diseño, arquitectura y ejecución de vivienda unifamiliar en **Liáns / Santa Cruz, Concello de Oleiros (A Coruña)**.

---

## 📌 Resumen Ejecutivo del Proyecto

* **Tipología arquitectónica:** Pabellón en U articulado alrededor de un **Patio Corrala Central Habitable (19,0 m² útiles)** con lucernario motorizado de cristal.
* **Superficie:** **`212,0 m² construidos cerrados`** + Pérgola exterior cubierta para 2 vehículos (`28,0 m²`) exenta de cómputo.
* **Familia:** Pareja + 2 hijos (niña de 9 años y niño de 7 años) + espacio polivalente de teletrabajo diario / suite privada para visitas familiares.
* **Parcela objetivo:** `500 – 700 m²` (`~600 m²`, `20 × 30 m`) en Oleiros (PGOM Ordenanza 2B).
* **Presupuesto llave en mano cerrado:** **`662.980 €`** (Terreno `180.000 €` + Obra `381.600 €` + Técnicos, Licencias, Aerotermia, Solar FV 4,5 kWp, Cocina completa Santos/Dekton y Riego Hunter).
* **Estado actual:** **Iteración 3 validada.** Distribución definitiva aprobada, zoom técnico 1:20 de estancias completado y metodología de renderizado estancia a estancia con control geométrico estricto en marcha.

---

## 🧭 Estructura del Repositorio y Módulos de Contexto

Para garantizar que **cualquier agente de IA o sesión de trabajo mantenga el contexto íntegro sin perder detalles ni alucinar decisiones ya cerradas**, el proyecto se estructura en módulos documentales independientes dentro de [`context/`](file:///home/antigravity/landslore/oleiros/context):

```
├── README.md                                             # Este documento (visión general e índice)
├── context/                                              # Contexto vivo, estructurado y modular
│   ├── 00_ESTADO_DEL_PROYECTO_Y_HOJA_DE_RUTA.md         # Estado vigente, próximas tareas y Reglas de Oro
│   ├── 01_PROGRAMA_NECESIDADES_Y_MODELO_FINANCIERO.md    # Perfil familiar, cuadro de áreas y finanzas completas
│   ├── 02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md         # Zonificación exhaustiva PB y P1, flujos y cotas
│   ├── 03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md   # Clima invisible, VMC, solar FV, domótica, materiales
│   ├── 04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md # Qué se decidió, qué se descartó y por qué
│   └── 05_CATALOGO_VISUAL_Y_DOCUMENTAL.md                # Mapa de planos HTML interactivos y 19 renders
│
├── history/                                              # Histórico íntegro de las conversaciones previas
│   ├── context/                                          # Entregables de la Iteración 2 y 3
│   │   ├── 1_planos_y_visores_html/                      # Visores web navegables y zoom 1:20
│   │   ├── 2_renders_alta_resolucion/                    # Renders HD por iteración (1, 2 y 3)
│   │   └── 3_conversacion_y_contexto/                    # Transcripción del chat y logs crudos (JSONL)
│   └── iteracion1/                                       # Archivo original de la Iteración 1
│
└── .agents/                                              # Skills de arquitectura y diseño avanzado
```

---

## 🤖 Protocolo para Agentes de IA en Nuevas Conversaciones

Cuando inicies una nueva conversación o sesión de trabajo en este repositorio, **sigue este orden de lectura obligatorio**:

1. **Lectura de arranque:** Consulta [`context/00_ESTADO_DEL_PROYECTO_Y_HOJA_DE_RUTA.md`](file:///home/antigravity/landslore/oleiros/context/00_ESTADO_DEL_PROYECTO_Y_HOJA_DE_RUTA.md) para situarte en el punto exacto de avance y revisar los mandamientos innegociables.
2. **Consultas temáticas:**
   * Si vas a tocar **distribución o geometría:** consulta [`context/02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md`](file:///home/antigravity/landslore/oleiros/context/02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md).
   * Si vas a revisar **materiales, enchufes o instalaciones:** consulta [`context/03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md`](file:///home/antigravity/landslore/oleiros/context/03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md).
   * Antes de proponer cualquier cambio espacial: **revisa [`context/04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md`](file:///home/antigravity/landslore/oleiros/context/04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md)** para no volver a plantear soluciones ya rechazadas por el usuario.
3. **Plano de referencia:** El plano oficial vigente es [`planos_amueblamiento_detallado_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/planos_amueblamiento_detallado_iter3.html). Toda visual o render debe ser 100 % coherente con su orientación geográfica y distribución.

---

## 🛠️ Entregables Interactivos Destacados

* 📐 **Plano General Clicable:** [`history/context/1_planos_y_visores_html/planos_amueblamiento_detallado_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/planos_amueblamiento_detallado_iter3.html)
* 🔍 **Fichas Técnicas Zoom-In 1:20:** [`history/context/1_planos_y_visores_html/planos_zoom_estancias_detalle_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/planos_zoom_estancias_detalle_iter3.html)
* 📸 **Radar de Cámaras 3D:** [`history/context/1_planos_y_visores_html/galeria_interactiva_casa_completa_iter3.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/galeria_interactiva_casa_completa_iter3.html)
* 🏡 **Web Presentación Hogar:** [`history/context/1_planos_y_visores_html/presentacion_hogar_oleiros.html`](file:///home/antigravity/landslore/oleiros/history/context/1_planos_y_visores_html/presentacion_hogar_oleiros.html)
