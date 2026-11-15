---
name: distribucion-planos-svg
description: Genera planos vectoriales SVG a escala con cotas, mobiliario reglamentario (NHG) y orientación adaptada al soleamiento y vientos de Oleiros.
---

# Generador de Esquemas de Distribución (SVG - Oleiros)

## ⛔ Regla Primordial de Consulta Espacial
> **NUNCA leas ni parsees archivos `.svg` previos para calcular cotas, superficies o adyacencias.**
> Toda la información geométrica, cotas exactas, bounding boxes y puntos de enganche de puertas/ventanas está unificada en Markdown dentro de:
> - [`espacios/PLANTA_BAJA_TOPOLOGIA.md`](espacios/PLANTA_BAJA_TOPOLOGIA.md)
> - [`espacios/PLANTA_ALTA_TOPOLOGIA.md`](espacios/PLANTA_ALTA_TOPOLOGIA.md)
> - Fichas particulares en [`espacios/estancias/`](espacios/estancias/)
> - Criterios de materiales en [`espacios/CRITERIOS_MATERIALES_Y_ARMONIA.md`](espacios/CRITERIOS_MATERIALES_Y_ARMONIA.md)

## Instrucciones
1. **Extracción Paramétrica:** Obtén las coordenadas $(X, Y)$ y dimensiones directamente desde las tablas de `espacios/` antes de trazar cualquier línea.
2. **Escala y Ejes:** Usa escala precisa (`1 metro = 50 píxeles` en plantas generales; `1 metro = 100 píxeles` en detalles 1:20) con origen `(0,0)` en el vértice Noroeste exterior.
3. **Estructura de Capas SVG (`<g id="...">`):**
   - `ejes-estructurales` (Líneas finas de trazo y punto con rotulación de ejes A-E y 1-6).
   - `muros-exteriores` (Espesor 35-40 cm con rayado técnico ANSI31 o aislamiento SATE).
   - `tabiqueria-interior` (Espesor 10-15 cm según aislamiento acústico).
   - `carpinterias` (Puertas con barrido de apertura y cotas de paso libre reglamentarias NHG $\ge 0,80\text{ m}$).
   - `mobiliario-fijo-y-nhg` (Círculos libres $\varnothing 1,20\text{ m}$ / $\varnothing 1,50\text{ m}$, bancada cocina Santos, sanitarios y armarios).
   - `cotas-y-rotulacion` (Superficie útil de cada pieza, identificador `PB-XX` / `PA-XX` y cota de nivel Z).
4. Guarda las propuestas y versiones vectoriales en `propuestas/` o `v2/planos/`.
5. Si actualizas alguna cota o puerta en el dibujo, refleja inmediatamente el cambio en la ficha `.md` correspondiente de `espacios/estancias/`.
