# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Morfología en "U" Pura (Opción B: Sala Multiusos Atardecer + Galería Claustro Integral + Suite Sur Expandida)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)** (Single Source of Truth). Permite a cualquier agente de IA o software CAD consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y ocio sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado de roble natural y porcelánico C3).
* **Altura Libre:** `2,65 m` a falso techo continuo con foso perimetral de iluminación indirecta.
* **Superficie Útil Interior P1:** `152,47 m²` útiles interiores.
* **Superficie Construida P1:** `175,00 m²` cerrados.
* **Morfología Estructural:** Edificación continua sin ningún rincón ni hueco perdido:
  * **Galería Oeste del Claustro (`PA-09`, 10,00 m²):** Espacio recuperado entre la escalera y el patio (`X = 7.50..10.00, Y = 8.50..12.50`), con cristalera corrida hacia el patio del arce japonés.
  * **Esquina Suroeste Recuperada (`X = 3.85..6.15, Y = 16.50..21.45` · 11,38 m²):** Integrada plenamente en el Ala Sur (`PA-17`), eliminando el corte exterior sobre el porche y dando lugar a una suite infantil esquinera con doble orientación Sur y Oeste.
  * **Baño Compartido Hijos (`PA-19`, 9,20 m²):** Acceso 100% directo e independiente por puerta `P-11` desde el distribuidor general (`X = 6.15`), sin cruzar jamás la sala multiusos. Ventana exterior oeste `C-16`.
  * **Sala Multiusos Atardecer (`PA-19B`, 9,20 m²):** Mirador panorámico `C-18` a poniente, sofá en L y pantalla 85", con puerta independiente `P-19B` al desembarco de escalera en `Y = 12.50`.
  * **Patio Claustro Abierto (`PA-07`, 10,24 m²):** Hueco cenital continuo de $3,20 \times 3,20\text{ m}$ idéntico a Planta Baja.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 Optimizada Integral)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-07** | Patio Claustro Abierto (Hueco Cenital) | `(10.00, 8.50) -> (13.20, 11.70)` | 3,20 × 3,20 m | 10,24 m² | Núcleo Bioclimático | Hueco libre al cielo vertical 1:1 coincidente con PB-07 |
| **PA-12** | Hueco y Desembarco Escalera Volada | `(6.15, 8.50) -> (7.50, 12.50)` | 1,35 × 4,00 m | 5,40 m² | Oeste / Cenital | Doble altura sobre escalera roble. Desembarco en cota +3,15 m a Y = 12.50 m |
| **PA-09** | Galería Mirador Oeste Claustro | `(7.50, 8.50) -> (10.00, 12.50)`| 2,50 × 4,00 m | 10,00 m² | Este / Claustro | **Hueco recuperado junto al claustro.** Cristalera continua mirando al arce |
| **PA-19B**| Sala Multiusos Atardecer / Cine | `(3.85, 8.50) -> (6.15, 12.50)` | 2,30 × 4,00 m | 9,20 m² | Oeste / Poniente | Gran Mirador C-18 (2,60 m) al atardecer, sofá L, pantalla 85", puerta P-19B |
| **PA-19** | Baño Compartido Hijos | `(3.85, 12.50) -> (6.15, 16.50)`| 2,30 × 4,00 m | 9,20 m² | Oeste / Fachada | Ventana exterior Oeste C-16, doble seno, ducha 150×90 cm y puerta P-11 directa a pasillo |
| **PA-16** | Galería Distribuidora y Rincón Estudio | `(6.15, 12.50) -> (13.20, 16.50)`| 7,05 × 4,00 m | 28,20 m² | Centro / Claustro | Cristalera panorámica C-15 (3,20 m) con vistas directas al claustro y rincón de estudio |
| **PA-17** | Dormitorio Niña (Suite Esquinera) | `(3.85, 16.50) -> (8.50, 21.45)` | 4,65 × 4,95 m | 23,00 m² | Sur y Oeste | **Hueco recuperado Suroeste.** Doble orientación: ventanal C-12 (Sur) y C-12B (Oeste) |
| **PA-18** | Dormitorio Infantil Niño | `(8.50, 16.50) -> (13.20, 21.45)`| 4,70 × 4,95 m | 23,26 m² | Sur / Jardín | Ventanal suelo a techo C-13 (2,80 m) volando sobre porche sur |
| **PA-20** | Dormitorio Master Suite Matrimonio | `(13.20, 16.50) -> (17.00, 21.45)`| 3,80 × 4,95 m | 18,81 m² | Sur / Sureste | Ventanal suelo a techo C-14 (2,80 m) volando sobre porche sur |
| **PA-21** | Gran Vestidor Suite (sobre Cocina) | `(13.20, 12.50) -> (17.00, 16.50)`| 3,80 × 4,00 m | 15,20 m² | Este / Claustro | Armarios continuos en U, luz natural y paso privado a baño suite |
| **PA-22** | Baño Privado Suite (sobre Cocina) | `(13.20, 8.50) -> (17.00, 12.50)`| 3,80 × 4,00 m | 15,20 m² | Norte y Este | Doble seno, bañera exenta y ducha 160×90 cm, ventanas C-11 (N) y C-11B (E) |
| **PA-24** | Campo Solar Fotovoltaico (6,3 kWp)| `Cubierta Superior (+6,50 m)` | Azotea Alta P1 | 42,00 m² | Sur 30° Óptimo | 14 paneles monocristalinos 450W libres de sombras |

---

## 2. Grafo de Circulación 100% Independiente y Limpio

```text
               [Escalera Volada PB-12 desde PB (Ala Oeste)]
                                    │
                   (Doble altura abierta con luz cenital)
                                    ▼ (Llegada en cota +3,15 m a Y = 12.50 m)
                      [Desembarco de Escalera P1]
                                    │
         ┌──────────────────────────┼────────────────────────────────────────┐
         │ (P-19B: Batiente Norte)  │ (P-11: Batiente Oeste)                 │ (Galerías hacia el Claustro y Sur)
         ▼                          ▼                                        ▼
   [SALA MULTIUSOS ATARDECER]   [BAÑO COMPARTIDO HIJOS]      [GALERÍAS CLAUSTRO PA-09 & PA-16]
        (PA-19B, 9,20 m²)            (PA-19, 9,20 m²)         (Vistas 360° al Patio Claustro y Arce)
     ★ GRAN MIRADOR PONIENTE C-18   ★ VENTANA EXTERIOR C-16     Estudio infantil + Galería Oeste
     Sofá L + Pantalla 85"          Doble seno + Ducha 150×90                │
     Atardecer y lectura            ACCESO DIRECTO INDEPENDIENTE ┌───────────┼───────────┐
                                                                 │ (P-12)    │ (P-13)    │ (P-14)
                                                                 ▼           ▼           ▼
                                                           [SUITE NIÑA] [DORM. NIÑO] [MASTER SUITE]
                                                             (PA-17)      (PA-18)    ├──► [Dorm. PA-20 (18,8m²)]
                                                            23,00 m²     23,26 m²    └──► [Ala Este Privada]
                                                          (Sur + Oeste) (Jardín Sur)        ├──► [Vestidor PA-21 (15,2m²)]
                                                                                            └──► [Baño Suite PA-22 (15,2m²)]
```
