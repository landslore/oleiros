# Sistema de Coordenadas, Ejes Estructurales y Topología

Este documento fija el sistema de referencia espacial canónico para el proyecto de vivienda unifamiliar en Oleiros (A Coruña) y permite a cualquier agente de IA o software calcular distancias, cotas y adyacencias sin necesidad de parsear código XML vectorial.

---

## 1. Sistema de Referencia y Escala

* **Origen de Coordenadas Global (0, 0):** Vértice Noroeste (NO) exterior de la edificación principal (alineación del muro de cerramiento norte con la linde oeste de servicio).
* **Orientación de Ejes:**
  * **Eje X (Horizontal):** Crece de **Oeste hacia Este** (de 0 a +1.400 unidades CAD).
  * **Eje Y (Vertical):** Crece de **Norte hacia Sur** (de 0 a +1.300 unidades CAD).
  * **Eje Z (Alturas / Niveles):** Crece verticalmente en metros (+0,00 m cota de pavimento terminado PB).
* **Factor de Conversión SVG / CAD a Metros Reales:**
  * En planos generales PB/PA: **50 unidades de dibujo = 1,00 metro real** (Factor `1 px = 0,02 m` / `1 m = 50 px`).
  * En planos de detalle ampliado 1:20 (Ala Norte y Cocina): **100 unidades = 1,00 metro real** (Factor `1 px = 0,01 m`).

---

## 2. Retícula de Ejes Estructurales

La estructura principal se resuelve mediante pórticos mixtos de hormigón armado y acero laminado con crujías estandarizadas:

### 2.1 Ejes Longitudinales (Dirección Oeste - Este)
* **Eje 1 (Norte):** Alineación exterior de fachada norte (Y = 240 px / 4,80 m desde linde de parcela).
* **Eje 2 (Intermedio Norte):** Alineación sur de crujía zaguán - hall - despacho (Y = 440 px / 8,80 m).
* **Eje 3 (Patio / Claustro):** Límite norte del patio central corrala (Y = 460 px).
* **Eje 4 (Sur Claustro):** Límite sur del patio central corrala y distribución salón (Y = 660 px).
* **Eje 5 (Fachada Sur):** Gran frente acristalado de salón y comedor hacia porche sur (Y = 940 px / 18,80 m).
* **Eje 6 (Límite Porche Sur):** Voladizo y límite exterior del porche sur (Y = 1090 px / 21,80 m).

### 2.2 Ejes Transversales (Dirección Norte - Sur)
* **Eje A:** Linde Oeste construida (Sala técnica surf, lavandería y garaje pergolado) (X = 220 px).
* **Eje B:** Límite este de sala técnica / zaguán mudroom (X = 380 px / +2,30 m desde Eje A).
* **Eje C:** Eje central de acceso principal / límite del hall y vestíbulo (X = 560 px / +3,60 m desde Eje B).
* **Eje D:** Límite este de despacho / suite PB y eje divisorio con baño PB (X = 755 px / +3,90 m desde Eje C).
* **Eje E:** Fachada Este (Baño PB y frente de bancada cocina Santos) (X = 922 px / +3,35 m desde Eje D).

---

## 3. Niveles y Cotas Verticales (Cota Z)

| Nivel | Cota Z | Descripción |
| :--- | :--- | :--- |
| **Calle / Rasante** | `±0,00 m` | Cota de referencia de acera exterior en Rúa dos Regos. |
| **Pérgola Aparcamiento** | `-0,10 m` | Pavimento drenante permeable con pendiente 1,5% hacia linde. |
| **Porche Norte Acceso** | `+0,05 m` | Resalte de seguridad contra escorrentías pluviales. |
| **Planta Baja Interior** | `±0,00 m` | Pavimento interior terminado (Roble 14mm / Caliza apomazada / Porcelánico). |
| **Patio Corrala Central** | `±0,00 m` | Tarima técnica Iroko enrasada a cota cero con rejilla oculta. |
| **Porche Sur Techado** | `±0,00 m` | Continuidad sin resaltes mediante carpinterías embutidas. |
| **Planta Primera (+3,15)** | `+3,15 m` | Pavimento terminado dormitorios, sala cine y suite principal. |
| **Altura Libre PB** | `2,70 m` | Desde pavimento terminado a falso techo acústico continuo. |
| **Altura Libre PA** | `2,65 m` | Desde pavimento terminado a falso techo continuo. |
| **Forjado Intermedio** | `0,45 m` | Canto total forjado (vigueta/losa 30cm + recrecido + suelo radiante 10cm + tarima). |
| **Coronación Edificación**| `+6,80 m` | Cumple ampliamente la altura máxima de cornisa PXOM (7,00 m). |

---

## 4. Convención de Denominación de Paramentos y Huecos

Para cada estancia, las cuatro caras se describen rigurosamente por su orientación geográfica:
* **Cara NORTE:** Paramento hacia el límite de entrada/calle (Y mínimo).
* **Cara SUR:** Paramento hacia el jardín y soleamiento principal (Y máximo).
* **Cara ESTE:** Paramento hacia la derecha del plano (X máximo).
* **Cara OESTE:** Paramento hacia la izquierda del plano (X mínimo).

Toda puerta o vano tiene asignadas:
1. **Coordenada de Inicio (X1, Y1)** y **Coordenada de Fin (X2, Y2)** en el sistema global.
2. **Anchura libre de paso (L)** y **Altura libre (H)** en metros.
3. **Tipo de carpintería o hueco** (Corredera enrasada en tabique, batiente 82cm, vano diáfano, cristalera fija).
