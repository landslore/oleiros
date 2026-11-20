# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Morfología en "U" Pura (Opción B: Sala Multiusos Atardecer + Patio Libre al Cielo)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)** (Single Source of Truth). Permite a cualquier agente de IA o software CAD consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y ocio sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado de roble natural y porcelánico C3).
* **Altura Libre:** `2,65 m` a falso techo continuo con foso perimetral de iluminación indirecta.
* **Superficie Útil Interior P1:** `110,80 m²` útiles interiores.
* **Superficie Construida P1:** `135,00 m²` cerrados.
* **Superficie Construida Total Vivienda (PB + P1):** `223,00 m²` cerrados (`239,00 m²` computables totales con porches al 50%).
* **Calidad Constructiva:** **CTE Clase A / nZEB (High Standard)** con presupuesto objetivo llave en mano de ~680.000 € (terreno e impuestos incluidos). Termoarcilla + SATE 12-14 cm, aerotermia y suelo radiante/refrescante.
* **Esquema de Distribución y Circulación Limpia:**
  * **Ala Oeste (`X = 3.85..6.15 m`):**
    * **Sala Multiusos Atardecer / Cine (PA-19B, 9,20 m² útiles):** En el tercio norte (`X = 3.85..6.15, Y = 8.50..12.50`), con mirador panorámico `C-18` (2,60 × 2,20 m) a poniente, sofá en "L" y pantalla multimedia 85". Acceso independiente con puerta `P-19B` desde el desembarco de escalera en `Y = 12.50`.
    * **Baño Compartido Hijos (PA-19, 9,20 m² útiles):** En el tramo central (`X = 3.85..6.15, Y = 12.50..16.50`), con ventana exterior `C-16` a fachada oeste, mueble doble seno suspendido y plato de ducha enrasado de 150 × 90 cm. **Acceso 100% directo e independiente con puerta `P-11` desde el distribuidor general (`X = 6.15`). NO requiere jamás atravesar la sala multiusos ni ningún dormitorio.**
  * **Patio Claustro Central (`X = 10.00..13.20, Y = 8.50..11.70` · 3,20 × 3,20 m = 10,24 m²):**
    * **100% abierto al cielo.** Hueco vertical continuo idéntico a Planta Baja. Abraza el *Acer palmatum* y baña de luz cenital la planta baja y la planta alta.
  * **Galería Distribuidora y Zona de Estudio Claustro (PA-16, 28,20 m² útiles):**
    * Abraza el Patio Claustro por el Oeste y el Sur (`Y = 11.70..16.50`, `X = 6.15..13.20`) con un frente acristalado panorámico continuo `C-15` (3,20 × 2,40 m). Incluye rincón de lectura y pupitre infantil integrado frente al jardín cenital.
  * **Ala Sur (Dormitorios con Soportal 3m · `Y = 16.50..21.45 m`):**
    * Tres dormitorios de gran formato volando 3,00 m sobre el Porche Sur de PB. Ventanales de suelo a techo y **cero balcones abiertos**.
  * **Ala Este (Zona Wellness Suite sobre Cocina · `X = 13.20..17.00 m`):**
    * Gran Vestidor en "U" `PA-21` (15,20 m²) y Baño privado de lujo `PA-22` (15,20 m²) con ventanas exteriores Norte y Este, sobre la crujía de cocina y despensa de PB.
* **Cubierta Alta (+6,50 m):** Alberga 14 módulos fotovoltaicos (6,30 kWp), 100% libres de sombras.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 Opción B)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-07** | Patio Claustro Abierto (Hueco Cenital) | `(10.00, 8.50) -> (13.20, 11.70)` | 3,20 × 3,20 m | 10,24 m² | Núcleo Bioclimático | Hueco libre al cielo vertical 1:1 coincidente con PB-07 |
| **PA-12** | Hueco y Desembarco Escalera Volada | `(6.15, 8.50) -> (7.50, 12.50)` | 1,35 × 4,00 m | 5,40 m² | Oeste / Cenital | Doble altura sobre escalera roble. Desembarco en cota +3,15 m a Y = 12.50 m |
| **PA-19B**| Sala Multiusos Atardecer / Cine | `(3.85, 8.50) -> (6.15, 12.50)` | 2,30 × 4,00 m | 9,20 m² | Oeste / Poniente | Gran Mirador C-18 (2,60 m) al atardecer, sofá L, pantalla 85", puerta P-19B |
| **PA-19** | Baño Compartido Hijos | `(3.85, 12.50) -> (6.15, 16.50)`| 2,30 × 4,00 m | 9,20 m² | Oeste / Fachada | Ventana exterior Oeste C-16, doble seno, ducha 150×90 cm y puerta P-11 a pasillo |
| **PA-16** | Galería Distribuidora y Rincón Estudio | `(6.15, 12.50) -> (13.20, 16.50)`| 7,05 × 4,00 m | 28,20 m² | Centro / Claustro | Cristalera panorámica C-15 (3,20 m) con vistas directas al claustro y arce |
| **PA-17** | Dormitorio Infantil Niña | `(6.15, 16.50) -> (9.70, 21.45)` | 3,55 × 4,95 m | 17,57 m² | Sur / Jardín | Ventanal suelo a techo C-12 (2,40 m) volando sobre porche |
| **PA-18** | Dormitorio Infantil Niño | `(9.70, 16.50) -> (13.20, 21.45)`| 3,50 × 4,95 m | 17,32 m² | Sur / Jardín | Ventanal suelo a techo C-13 (2,40 m) volando sobre porche |
| **PA-20** | Dormitorio Master Suite | `(13.20, 16.50) -> (17.00, 21.45)`| 3,80 × 4,95 m | 18,81 m² | Sur / Sureste | Ventanal suelo a techo C-14 (2,80 m) volando sobre porche |
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
         │ (P-19B: Batiente Norte)  │ (P-11: Batiente Oeste)                 │ (Galería hacia el Sur/Este)
         ▼                          ▼                                        ▼
   [SALA MULTIUSOS ATARDECER]   [BAÑO COMPARTIDO HIJOS]      [GRAN GALERÍA DISTRIBUIDORA PA-16]
        (PA-19B, 9,20 m²)            (PA-19, 9,20 m²)         (Cristalera C-15 al Patio Claustro)
     ★ GRAN MIRADOR PONIENTE C-18   ★ VENTANA EXTERIOR C-16     Estudio infantil + vista al arce
     Sofá L + Pantalla 85"          Doble seno + Ducha 150×90                │
     Atardecer y lectura            ACCESO DIRECTO INDEPENDIENTE ┌───────────┼───────────┐
                                                                 │ (P-12)    │ (P-13)    │ (P-14)
                                                                 ▼           ▼           ▼
                                                            [Dorm. Niña] [Dorm. Niño] [MASTER SUITE]
                                                               (PA-17)     (PA-18)    ├──► [Dorm. PA-20 (18,8m²)]
                                                              17,57 m²    17,32 m²    └──► [Ala Este Privada]
                                                                 │           │               ├──► [Vestidor PA-21 (15,2m²)]
                                                                 ▼           ▼               └──► [Baño Suite PA-22 (15,2m²)]
                                                            [Jardín Sur] [Jardín Sur]              (Ventanas N y E)
                                                            (Soportal 3m)(Soportal 3m)
```
