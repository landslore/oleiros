# Bitácora de Revisión y Dudas de Diseño — Hogar Oleiros (Propuesta D)

> **Rama de trabajo:** `feature/revision-dudas-diseno`  
> **Estado:** En revisión activa  
> **Base:** Propuesta D Consolidada (`main`)

---

## 1. Objetivo de esta Rama

Esta rama centraliza la resolución de dudas, ajustes arquitectónicos, constructivos, de distribución, instalaciones o presupuesto sobre el diseño actual de **Hogar Oleiros (Propuesta D)**, permitiendo revisar cada cambio de forma trazable a través de su Pull Request en GitHub.

---

## 2. Registro de Dudas y Cambios Acordados

| # | Estancia / Ámbito | Duda o Ajuste Planteado | Solución Aplicada | Archivos Actualizados | Estado |
|---|---|---|---|---|---|
| **01** | **Planta Primera (+3,15 m):** Baño Hijos, Dormitorios Infantiles y Nueva Sala Polivalente | El *Baño Compartido Hijos* (rotulado `6,80 m²`) estaba dibujado con $6,00 \times 2,80\text{ m} = 16,80\text{ m}^2$, pareciendo casi tan grande como las dos habitaciones de los niños juntas (que estaban recortadas por el Sur a $10,4\text{ m}^2$ y $7,7\text{ m}^2$). Se solicita reorganizar la planta superior a escala 100% real e incorporar una **Sala Polivalente**. | 1. **Corrección geométrica a escala 100% real** alineada con los ejes estructurales de Planta Baja (`B=6,15 m .. E=17,00 m` y `1=5,00 m .. 4=18,00 m`).<br>2. **Baño Compartido Hijos (`E-19`)** ajustado a su dimensión exacta: `2,32 × 2,93 m = 6,80 m² útiles`.<br>3. **Nueva Sala Polivalente / Cine, TV & Gaming / 4º Dormitorio (`E-19B`)** de **`4,78 × 2,93 m = 14,00 m² útiles`** en la banda Centro-Norte, cerrada con tabiques acústicos ($R_w \ge 50\text{ dB}$), puerta isofónica `P-11B` ($R_w \ge 38\text{ dB}$), ventana Norte `C-10B` (`1,80 m`) y mirador interior acústico `4+4 Silence` + estor *blackout* hacia la copa del arce del Patio Corrala.<br>4. **Dormitorios Infantiles (`E-17` y `E-18`)** ampliados hasta la línea Sur real (`Y = 17,65 m`), alcanzando **`3,42 × 4,27 m = 14,60 m² útiles reales cada uno`** (más del doble que el baño de hijos). | [`generate_general_plans.py`](file:///home/antigravity/landslore/oleiros/generate_general_plans.py), [`generate_p1_and_sections_plans.py`](file:///home/antigravity/landslore/oleiros/generate_p1_and_sections_plans.py), [`generate_zoom_cad_viewer.py`](file:///home/antigravity/landslore/oleiros/generate_zoom_cad_viewer.py), [`planta_alta_propuesta_d.svg`](file:///home/antigravity/landslore/oleiros/propuestas/planta_alta_propuesta_d.svg), [`plano_constructivo_planta_primera_p1.svg`](file:///home/antigravity/landslore/oleiros/propuestas/plano_constructivo_planta_primera_p1.svg), [`index.html`](file:///home/antigravity/landslore/oleiros/index.html) | ✅ Resuelto |

---

## 3. Detalle Técnico de la Duda #01 — Reorganización de Planta Primera (+3,15 m)

### 3.1 Diagnóstico del Error Gráfico Previo
* **Desfase en Banda Norte:** El rectángulo del *Baño Compartido Hijos (E-19)* abarcaba desde `X = 6,50 m` hasta `X = 12,50 m` ($6,00\text{ m}$ de ancho por $2,80\text{ m}$ de alto = **$16,80\text{ m}^2$ dibujados**), mientras que su etiqueta indicaba `6,80 m²` (sobraban $10,00\text{ m}^2$ sin uso definido).
* **Recorte en Banda Sur:** El cierre Sur de la Planta Primera estaba trazado en `Y = 16,15 m` en lugar de apoyar sobre el pórtico Sur de Planta Baja (`Y = 18,00 m`), reduciendo el dibujo del *Dormitorio Niña* a $3,67 \times 2,84\text{ m}$ ($10,42\text{ m}^2$) y el del *Dormitorio Niño* a $3,11 \times 2,48\text{ m}$ ($7,71\text{ m}^2$).

### 3.2 Cuadro de Superficies y Dimensiones Verificadas a Escala Real (Planta Primera · Cota +3,15 m)

| Código | Estancia | Coordenadas Interiores (`X` ; `Y`) | Dimensiones Libres | Superficie Útil Real | Dotación y Aislamiento Acústico |
|---|---|---|---|---|---|
| **E-16** | **12. Desembarco Escalera y Galería Acústica** | `X: 6,50..8,50` y `6,50..13,48` · `Y: 8,28..13,26` | Pasarelas $1,00\text{ m}$ y $0,86\text{ m}$ | **8,20 m²** | Mampara acústica fija `4+4 Silence` ($R_w = 42\text{ dB}$) sobre el Patio Corrala + pasarela norte sobre alero de $80\text{ cm}$ |
| **E-17** | **13. Dormitorio Infantil 1 (Niña)** | `X: 6,50..9,92 m` · `Y: 13,38..17,65 m` | **`3,42 × 4,27 m`** | **14,60 m²** | Cama $135\times 200\text{ cm}$ + Armario $1,35\text{ m}$ + Escritorio $1,80\text{ m}$ en pared Este (luz Sur a 90°) + Balconera `C-12` ($2,20\text{ m}$) |
| **E-18** | **14. Dormitorio Infantil 2 (Niño)** | `X: 10,06..13,48 m` · `Y: 13,38..17,65 m` | **`3,42 × 4,27 m`** | **14,60 m²** | Gemelo al `E-17` · Separado por medianera ciega $R_w \ge 50\text{ dB}$ + Escritorio $1,80\text{ m}$ en pared Este + Balconera `C-13` ($2,20\text{ m}$) |
| **E-19** | **15. Baño Compartido Hijos** | `X: 6,50..8,82 m` · `Y: 5,35..8,28 m` | **`2,32 × 2,93 m`** | **6,80 m²** | Mueble doble seno $1,40\text{ m}$ en pared Oeste + Bañera/ducha $2,20\times 0,85\text{ m}$ al Norte + Inodoro suspendido + Ventana `C-10` |
| **E-19B** | **15B. Sala Polivalente / Cine, TV & Gaming / 4º Dorm.** | `X: 8,94..13,72 m` · `Y: 5,35..8,28 m` | **`4,78 × 2,93 m`** | **14,00 m²** | **Cerrada con tabique acústico $R_w \ge 50\text{ dB}$ y puerta isofónica `P-11B` ($R_w \ge 38\text{ dB}$)** · Sofá-cama en L + TV OLED 65" + Setup Gaming doble + Ventana Norte `C-10B` ($1,80\text{ m}$) + Mirador `4+4 Silence` con *blackout* al Patio |
| **E-20** | **16. Dormitorio Principal Master Suite** | `X: 13,60..16,65 m` · `Y: 12,24..17,65 m` | **`3,05 × 5,41 m`** | **16,50 m²** | Cama *King Size* $180\times 200\text{ cm}$ + Banco pie de cama + Balconera Sur `C-14` ($2,70\text{ m}$) |
| **E-21** | **17. Vestidor de Paso Doble Suite** | `X: 12,75..16,65 m` · `Y: 7,72..12,12 m` | **`3,90 × 4,40 m`** | **8,40 m²** *(libres)* | Dos frentes de armarios ($3,60\text{ m}$ + $4,15\text{ m}$ = $7,75\text{ m}$ lineales) + Isla joyero central + Ventana Este `C-14B` |
| **E-22** | **18. Baño Privado Master Suite** | `X: 13,84..16,65 m` · `Y: 5,35..7,60 m` | **`2,81 × 2,25 m`** | **6,30 m²** | Ducha doble *Walk-in* ($0,92\times 2,15\text{ m}$) + Encimera doble seno $1,45\text{ m}$ + Inodoro suspendido + Ventana Norte `C-11` |
| **E-23** | **19. Balcón Corrido Sur P1** | `X: 6,15..17,00 m` · `Y: 18,00..19,40 m` | **`10,85 × 1,40 m`** | **14,00 m²** *(ext.)* | Barandilla continua de vidrio laminar estructural `10+10.2 mm` en perfil oculto U · Voladizo de control solar para PB |
| — | **TOTAL PLANTA PRIMERA (+3,15 m)** | **Ejes B (`6,15 m`) a E (`17,00 m`)** | **`10,85 × 13,00 m`** | **89,40 m² int.** *(+14,00 m² balcón)* | **Total Útil Vivienda (PB + P1) = 202,40 m²** |

