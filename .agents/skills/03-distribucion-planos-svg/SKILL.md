---
name: distribucion-planos-svg
description: Genera planos vectoriales SVG a escala con cotas, mobiliario reglamentario (NHG) y orientación adaptada al soleamiento y vientos de Oleiros.
---

# Generador de Esquemas de Distribución (SVG - Oleiros)

## Instrucciones
1. Confirma antes de dibujar: orientación Norte exacta, cota de acceso desde el vial, pendiente del terreno y superficie máxima de ocupación en planta.
2. Guarda cada propuesta en `/propuestas/` (ej. `planta-baja-v1.svg`, `planta-alta-v1.svg`, `implantacion-parcela.svg`).
3. Usa escala precisa (`1 metro = 40 píxeles`) y estructura el código SVG en capas (`<g id="...">`):
   - `parcela-y-retranqueos` (límites de finca y línea discontinua de ocupación máxima).
   - `muros-exteriores` (espesor 35-40 cm contemplando aislamiento SATE o fachada ventilada).
   - `tabiqueria-interior` (10-12 cm).
   - `carpinterias` (puertas con ancho mínimo libre de 0,80 m y ventanas con barrido de apertura).
   - `mobiliario-nhg` (mobiliario mínimo reglamentario en Galicia: cama doble 1,50x2,00 m con pasos libres, mesa comedor, sofás, sanitarios con espacio de uso).
   - `textos-cotas-norte` (superficie útil de cada pieza, cotas generales, rosa de los vientos indicando Norte y vientos dominantes SW/NE).
4. Si el navegador integrado de Antigravity está disponible, renderiza el archivo SVG para revisarlo visualmente con el usuario.

## Reglas de diseño
- **Orientación:** Abre las piezas principales de día (salón, comedor, porche) hacia el **Sur / Suroeste** para captar el sol de tarde y resguarda la fachada **Norte** ubicando allí accesos, escaleras, baños, lavadero y garaje.
- **Protección de lluvia:** Diseña el acceso peatonal principal bajo cubierta o retranqueado para evitar entrada directa de agua y viento.
