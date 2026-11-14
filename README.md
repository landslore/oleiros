# Hogar Oleiros — Pabellón Bioclimático Atlántico (Propuesta D)

Proyecto integral de arquitectura, bioclimática y ejecución de vivienda unifamiliar en **Liáns / Santa Cruz, Concello de Oleiros (A Coruña)**.

---

## 📌 Resumen Ejecutivo del Proyecto (Propuesta D)

* **Tipología arquitectónica:** Pabellón articulado alrededor de un **Patio Corrala Central Habitable (16,00 m² libres · 4,00 × 4,00 m)** a cota cero ($\pm 0,00\text{ m}$) abierto al cielo, con *Acer palmatum*, banco de iroko corrido bajo alero de 80 cm y drenaje lineal perimetral oculto.
* **Superficie:** **`215,0 m² construidos cerrados`** (PB: 116,50 m² + P1: 98,50 m²) + Porche Sur cubierto de fondo 3,00 m (`36,0 m²`) + Pérgola exterior para 2 vehículos (`28,0 m²`).
* **Familia:** Pareja + 2 hijos (niña de 9 años y niño de 7 años) + despacho sanctasanctórum de teletrabajo diario / suite privada para invitados familiares.
* **Parcela objetivo:** `600,00 m²` (`20,00 × 30,00 m`) en Oleiros (PGOM Ordenanza 2B: Ocupación máxima 20% = 120,00 m²; Proyecto ocupa 116,50 m² cerrados en PB).
* **Presupuesto llave en mano cerrado:** **`662.980 €`** (Terreno `180.000 €` + Obra PEM `381.600 €` + Técnicos, Licencias, Aerotermia Vaillant, VMC Zehnder Q350, Solar FV 5,4 kWp, Cocina Santos/Dekton, Porche con Churrasqueira de granito y Piscina 7,5×3,5m).
* **Estado actual:** **Propuesta D consolidada al nivel de Proyecto de Ejecución (1:50 y 1:20)** con documentación agéntica completa en Markdown (SSOT).

---

## 🧭 Estructura del Repositorio y Documentación Agéntica (SSOT)

> **REGLA AGÉNTICA PRIMORDIAL:** Cualquier agente de IA que trabaje en este proyecto **NO necesita leer ni parsear archivos HTML**. Todo el proyecto está completamente documentado y acotado al milímetro en archivos Markdown (`.md`) para que dos agentes distintos plasmen con exactitud paramétrica el mismo plano técnico.

```
├── README.md                                                        # Este documento (visión general e índice)
│
├── docs/                                                            # Documentación de Ejecución Oficial
│   ├── PROYECTO_EJECUCION_DEFINITIVO_COTAS_E_INSTALACIONES.md       # ⭐ SINGLE SOURCE OF TRUTH (Cotas, coordenadas, REBT, fontanería, VMC)
│   ├── FICHAS_TECNICAS_ESTANCIAS_ZOOM_PROPUESTA_D.md                # Fichas técnicas 1:20 de las 17 zonas
│   └── PROPUESTA_D_PABELLON_BIOCLIMATICO_OLEIROS.md                 # Memoria conceptual y bioclimática de Propuesta D
│
├── context/                                                         # Contexto vivo sincronizado
│   ├── 00_ESTADO_DEL_PROYECTO_Y_HOJA_DE_RUTA.md                    # Estado vigente, mandamientos y fases
│   ├── 01_PROGRAMA_NECESIDADES_Y_MODELO_FINANCIERO.md               # Programa, finanzas y costes desglosados
│   ├── 02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md                    # Zonificación, cotas X/Y/Z y superficies
│   ├── 03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md              # Climatización Passivhaus, Bora, churrasqueira y piscina
│   └── 04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md        # Historial de decisiones y alternativas rechazadas
│
├── propuestas/                                                      # Planos vectoriales SVG a escala y Renders
│   ├── plano_constructivo_zona_norte_pb.svg                         # Detalle 1:50 Zona Norte PB
│   ├── plano_constructivo_centro_patio_cocina_pb.svg                # Detalle 1:50 Centro PB (Patio, Cocina, Escalera)
│   ├── plano_constructivo_sur_salon_porche_pb.svg                   # Detalle 1:50 Zona Sur PB (Salón, Porche, Piscina)
│   ├── planta_baja_propuesta_d.svg                                  # Planta Baja General 1:100
│   ├── planta_alta_propuesta_d.svg                                  # Planta Primera General 1:100
│   ├── Presentacion_Hogar_Oleiros_Propuesta_D.pptx                  # PowerPoint 16:9 compatible con Mac (Keynote)
│   └── renders/                                                     # Galería de 12 renders fotorrealistas
│
└── .agents/                                                         # Skills de arquitectura, bioclimática y cálculo
```

---

## 🤖 Protocolo Obligatorio para Agentes de IA

Si eres un agente de IA que retoma o continúa este proyecto:

1. **Lectura Obligatoria #1 (SSOT):** Lee [`docs/PROYECTO_EJECUCION_DEFINITIVO_COTAS_E_INSTALACIONES.md`](file:///home/antigravity/landslore/oleiros/docs/PROYECTO_EJECUCION_DEFINITIVO_COTAS_E_INSTALACIONES.md). Contiene las coordenadas exactas $(X, Y, Z)$, las dimensiones de muros, carpinterías, muebles, tomas de corriente Schuko/RJ45, caudales de ventilación VMC y trazado de fontanería.
2. **Consultas de Contexto Rápido:**
   * Para cotas y superficies: [`context/02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md`](file:///home/antigravity/landslore/oleiros/context/02_DISTRIBUCION_ARQUITECTONICA_Y_COTAS.md).
   * Para instalaciones Passivhaus y calidades: [`context/03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md`](file:///home/antigravity/landslore/oleiros/context/03_MEMORIA_TECNICA_INSTALACIONES_Y_CALIDADES.md).
   * Para no reintroducir ideas descartadas: [`context/04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md`](file:///home/antigravity/landslore/oleiros/context/04_BITACORA_DECISIONES_Y_ALTERNATIVAS_DESCARTADAS.md).
3. **Reglas de Oro Innegociables:**
   * 🚫 **El Patio Corrala (16 m²) es a cielo abierto:** Jamás colocar cubiertas de cristal cerradas ni lucernarios motorizados. Es una corrala habitable a cota cero.
   * 🚫 **Un solo patio en toda la casa:** El salón no tiene 2 patios. Al Norte linda con el Patio Corrala y al Sur se abre al Porche techado y la piscina.
   * 🚫 **Escritorios infantiles siempre a 90°:** Apoyan en la pared Este para recibir luz lateral de la balconera Sur sin reflejos en las pantallas. Cero ventanas en tabiques medianeros.
   * 🚫 **Baño PB legal NHG:** Requiere siempre distribuidor neutro con puerta corredera que evite comunicación directa con la cocina.
   * 🚫 **Chimenea estanca:** Siempre con toma de aire exterior directa $\varnothing 150\text{ mm}$ (compatible con VMC Zehnder).

---

## 📱 Visualizadores y Entregables en Vivo

* 🌐 **Web Móvil en Vivo (GitHub Pages):** [https://landslore.github.io/oleiros/](https://landslore.github.io/oleiros/) *(Planos SVG 1:50 interactivos, galería de renders y visor 3D Three.js)*.
* 📊 **Presentación PowerPoint (.pptx):** [Presentacion_Hogar_Oleiros_Propuesta_D.pptx](file:///home/antigravity/landslore/oleiros/propuestas/Presentacion_Hogar_Oleiros_Propuesta_D.pptx) *(14 diapositivas maquetadas para Mac / Keynote)*.
* ☁️ **Versión Cloud:** [Google Slides](https://docs.google.com/presentation/d/1AHYDhaDiH4zxxbKxN8ffe-7R8t2RK37y-VMJbs5lKhw/edit)
