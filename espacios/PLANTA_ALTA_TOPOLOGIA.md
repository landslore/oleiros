# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)**. Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y descanso sin parsear el plano `planta_alta_definitiva.svg`.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado).
* **Altura Libre:** `2,65 m` a falso techo continuo.
* **Superficie Útil Interior P1:** `89,40 m²` (Aprovechamiento 100% útil sin pasillos ciegos).
* **Superficie Exterior Vinculada:** Balcón Corrido Sur (13,20 m²) + Cubierta Técnica Solar FV (38,10 m²).
* **Total Vivienda Útil Acumulada (PB + P1):** `198,65 m²` (ó `202,40 m²` con elementos auxiliares).

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1)

*Escala de coordenadas: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Coords SVG (X1, Y1) a (X2, Y2) | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-16** | Desembarco Escalera y Galería | `(380, 460) -> (450, 680)` | `(7.60, 9.20) -> (9.00, 13.60)`| 1,40 × 4,40 m | 8,20 m² | Oeste / Cenital |
| **PA-17** | Dormitorio Infantil Niña | `(450, 660) -> (620, 875)` | `(9.00, 13.20) -> (12.40, 17.50)`| 3,42 × 4,27 m | 14,60 m² | Sur / Jardín |
| **PA-18** | Dormitorio Infantil Niño | `(620, 660) -> (790, 875)` | `(12.40, 13.20) -> (15.80, 17.50)`| 3,42 × 4,27 m | 14,60 m² | Sur / Jardín |
| **PA-19** | Baño Compartido Hijos | `(450, 460) -> (565, 605)` | `(9.00, 9.20) -> (11.30, 12.10)`| 2,32 × 2,93 m | 6,80 m² | Norte / Claustro |
| **PA-19B**| Sala Polivalente Cine / Gaming | `(565, 460) -> (805, 605)` | `(11.30, 9.20) -> (16.10, 12.10)`| 4,78 × 2,93 m | 14,00 m² | Norte / Este |
| **PA-20** | Dormitorio Master Suite | `(790, 660) -> (922, 930)` | `(15.80, 13.20) -> (18.44, 18.60)`| 3,05 × 5,41 m | 16,50 m² | Sur / Sureste |
| **PA-21** | Vestidor de Paso Doble Suite | `(805, 460) -> (922, 605)` | `(16.10, 9.20) -> (18.44, 12.10)`| 2,34 × 3,59 m | 8,40 m² | Este |
| **PA-22** | Baño Privado Master Suite | `(790, 345) -> (922, 460)` | `(15.80, 6.90) -> (18.44, 9.20)`| 2,81 × 2,25 m | 6,30 m² | Este / Noreste |
| **PA-23** | Balcón Corrido Sur Techado | `(420, 875) -> (922, 945)` | `(8.40, 17.50) -> (18.44, 18.90)`| 10,15 × 1,40 m | 13,20 m² | Sur |
| **PA-24** | Cubierta Plana Técnica Solar FV | `(235, 275) -> (450, 660)` | `(4.70, 5.50) -> (9.00, 13.20)`| Ala Oeste PB | 38,10 m² | Cubierta Baja |

---

## 2. Grafo de Adyacencias y Red de Circulación en Planta Primera

```text
               [Escalera Volada PB-12]
                         │
                         ▼ (Llegada peldaño 17 en cota +3,15m)
        [Desembarco Escalera y Galería Acústica PA-16]
          │
          ├──► (Puerta batiente P-07: 82cm) ──► [Baño Hijos PA-19]
          │
          ├──► (Puerta corredera acústica P-08: 90cm) ──► [Sala Cine / Gaming PA-19B]
          │
          ├──► (Puerta batiente P-09: 82cm) ──► [Dormitorio Infantil Niña PA-17]
          │                                              │
          │                                              ▼ (Balconera corredera C-11)
          │                                      [Balcón Corrido Sur PA-23]
          │                                              ▲
          ├──► (Puerta batiente P-10: 82cm) ──► [Dormitorio Infantil Niño PA-18]
          │                                              │
          │                                              ▼ (Balconera corredera C-12)
          │                                      [Balcón Corrido Sur PA-23]
          │
          └──► (Puerta corredera embutida P-11: 90cm)
                    │
                    ▼
          [Master Suite: Distribuidor Privado]
            ├──► (Paso libre) ──► [Vestidor de Paso PA-21]
            │                           │
            │                           ▼ (Puerta enrasada P-12: 80cm)
            │                     [Baño Privado Suite PA-22]
            │
            └──► (Paso fluido continuo) ──► [Dormitorio Principal PA-20]
                                                  │
                                                  ▼ (Balconera elevable C-13)
                                          [Balcón Corrido Sur PA-23]
```

### Tabla de Vanos y Puntos de Enganche en P1

| Desde | Hacia | Coordenadas Globales del Vano | Tipo de Vano / Carpintería | Ancho Libre |
| :--- | :--- | :--- | :--- | :--- |
| `PB-12 (Escalera)` | `PA-16 (Desembarco)`| `X: 380..450, Y: 460` | Llegada de tramo con barandilla de vidrio | 1,40 m paso |
| `PA-16 (Galería)` | `PA-19 (Baño Hijos)`| `X: 470..510, Y: 605` | Puerta batiente enrasada P-07 | 0,82 m |
| `PA-16 (Galería)` | `PA-19B (Sala Cine)`| `X: 580..625, Y: 605` | Puerta acústica corredera P-08 ($R_w \ge 45\text{ dB}$)| 0,90 m |
| `PA-16 (Galería)` | `PA-17 (Dorm. Niña)`| `X: 480..525, Y: 660` | Puerta batiente enrasada P-09 | 0,82 m |
| `PA-16 (Galería)` | `PA-18 (Dorm. Niño)`| `X: 640..685, Y: 660` | Puerta batiente enrasada P-10 | 0,82 m |
| `PA-16 (Galería)` | `Master Suite PA-20`| `X: 790, Y: [620..665]` | Puerta enrasada suelo-techo P-11 | 0,90 m |
| `PA-21 (Vestidor)`| `PA-22 (Baño Suite)`| `Y: 460, X: [830..870]` | Puerta corredera embutida P-12 | 0,80 m |
| `PA-17 (Dorm. Niña)`| `PA-23 (Balcón Sur)`| `Y: 875, X: [490..600]` | Balconera osciloparalela C-11 | 2,20 m |
| `PA-18 (Dorm. Niño)`| `PA-23 (Balcón Sur)`| `Y: 875, X: [660..770]` | Balconera osciloparalela C-12 | 2,20 m |
| `PA-20 (Master Suite)`| `PA-23 (Balcón Sur)`| `Y: 875, X: [810..910]` | Balconera corredera elevable C-13 | 2,70 m |
| `PA-16 (Galería)` | `PA-24 (Cubierta FV)`| `X: 380, Y: [520..565]` | Puerta técnica estanca hacia cubierta baja | 0,82 m |

---

## 3. Coordinación Estructural y de Cargas con Planta Baja

1. **Alineación de Muros Portantes y Fachadas:**
   * La fachada sur de los 3 dormitorios de P1 (`Y = 875`) se retranquea 1,30 m respecto a la fachada baja (`Y = 940`), creando el voladizo natural que sombrea bioclimáticamente el salón inferior en verano.
   * La fachada norte de P1 (`Y = 460`) vierte luz cenital sobre el patio claustro central de planta baja.
2. **Aislamiento Acústico entre Forjados:**
   * Lámina anti-impacto de polietileno reticulado (10 mm, $\Delta L_w \ge 28\text{ dB}$) bajo el recrecido del suelo radiante en toda la superficie de P1 para eliminar ruidos de pisadas hacia el salón y cocina.
