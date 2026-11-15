# Directrices Obligatorias para Agentes de IA (Hogar Oleiros)

Bienvenido a la base de código de **Hogar Oleiros (Pabellón Bioclimático Atlántico)**.
Para optimizar el uso de tokens, evitar respuestas lentas y garantizar la coherencia arquitectónica y constructiva, **debes seguir estrictamente estas reglas**.

---

## ⛔ Regla Negativa de Oro (Anti-Parsing de SVG)

> **PROHIBIDO LEER O PARSEAR ARCHIVOS `.svg` PARA CONSULTAR DISTRIBUCIONES, COTAS O ADYACENCIAS.**
> Los archivos SVG de este repositorio son densos (entre 500 y 1.400 líneas de código XML vectorial milimétrico). No intentes descifrar geometrías, polígonos, ni relaciones espaciales inspeccionando ficheros `.svg`. Los planos vectoriales son únicamente **artefactos gráficos de salida y visualización**.

---

## ⚡ Regla Positiva de Oro (Single Source of Truth: `espacios/`)

Toda la distribución arquitectónica, cotas de inicio/fin, bounding boxes, adyacencias, carpinterías e instalaciones está **aplanada y documentada en Markdown estructurado** dentro de la carpeta:

👉 [**`espacios/`**](file:///home/antigravity/landslore/oleiros/espacios/README.md)

### Protocolo de Consulta Rápida:

1. **Visión General y Bounding Boxes de Plantas:**
   * Planta Baja: Consulta [**`espacios/PLANTA_BAJA_TOPOLOGIA.md`**](file:///home/antigravity/landslore/oleiros/espacios/PLANTA_BAJA_TOPOLOGIA.md).
   * Planta Primera: Consulta [**`espacios/PLANTA_ALTA_TOPOLOGIA.md`**](file:///home/antigravity/landslore/oleiros/espacios/PLANTA_ALTA_TOPOLOGIA.md).
   * Sistema de Coordenadas y Escala: [**`espacios/SISTEMA_COORDENADAS_Y_EJES.md`**](file:///home/antigravity/landslore/oleiros/espacios/SISTEMA_COORDENADAS_Y_EJES.md) (`50 px = 1,00 m`).

2. **Detalle Particular de una Estancia:**
   * Si el usuario te pide trabajar en un habitáculo concreto (ej. cocina, mudroom, baño, despacho, dormitorio, etc.), **lee ÚNICAMENTE su ficha particular** en [**`espacios/estancias/`**](file:///home/antigravity/landslore/oleiros/espacios/estancias/):
     - `pb_02_porche_norte.md`, `pb_03_zaguan_mudroom.md`, `pb_04_hall_recibidor.md`, `pb_05_despacho_suite.md`, `pb_06_bano_pb.md`, `pb_07_patio_corrala_central.md`, `pb_08_cocina_santos.md`, `pb_10_salon_chimenea.md`, `pb_11_comedor_principal.md`, `pb_12_escalera_volada.md`, `pb_13_sala_tecnica_surf.md`, `pb_13b_lavanderia_plancha.md`, `pb_14_porche_sur.md`.
     - `pa_16_desembarco_galeria.md`, `pa_17_dormitorio_infantil_nina.md`, `pa_18_dormitorio_infantil_nino.md`, `pa_19_bano_compartido_hijos.md`, `pa_19b_sala_cine_gaming.md`, `pa_20_master_suite.md`, `pa_21_vestidor_suite.md`, `pa_22_bano_privado_suite.md`, `pa_23_balcon_corrido_sur.md`.
   * En cada ficha tienes: límites N-S-E-O, puntos de enganche de puertas/ventanas, tomas eléctricas REBT, VMC, saneamiento y acabados.

3. **Criterios de Materiales y Armonía (Obligatorio antes de proponer acabados):**
   * Antes de proponer o modificar cualquier material, revisa [**`espacios/CRITERIOS_MATERIALES_Y_ARMONIA.md`**](file:///home/antigravity/landslore/oleiros/espacios/CRITERIOS_MATERIALES_Y_ARMONIA.md).
   * Paleta canónica: NCS S 0502-Y (Blanco roto lino), NCS S 2005-Y20R (Greige suave), RAL 9005 ST (Negro texturado).
   * Maderas: Roble europeo natural en interior e Iroko FSC en exteriores. Prohibido mezclar más tipos de maderas o usar rodapiés sobrepuestos estándar (solo rodapié enrasado con foso de sombra de 15 mm).

---

## 🛠️ Si tienes que Generar o Actualizar un Plano SVG

1. Lee las cotas y coordenadas desde los archivos `.md` de `espacios/`.
2. Modifica o crea el script generador de Python correspondiente (`generate_*.py`) o genera el código SVG directamente respetando las capas y la escala canónica fijada.
3. Actualiza la ficha `.md` de la estancia si tus cambios alteran alguna cota, vano o instalación.
