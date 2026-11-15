# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Optimizada Passivhaus (~165 m² construidos totales · Distribución en "U" con Alas Este y Oeste)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)**. Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y descanso sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado).
* **Altura Libre:** `2,65 m` a falso techo continuo.
* **Superficie Útil Interior P1:** `69,50 m²` (Aprovechamiento 100% útil con galería bioclimática perimetral).
* **Superficie Construida P1:** `82,00 m²` cerrados.
* **Morfología en "U" envolviendo el Patio Claustro:**
  * **Ala Oeste (sobre Escalera):** Desembarco y galería acristalada con vistas directas al patio.
  * **Ala Sur (sobre Salón y Porche Sur):** Galería distribuidora luminosa, dormitorios infantiles y dormitorio suite volando 3,00 m sobre el Porche Sur (soportal continuo).
  * **Ala Este (sobre Cocina):** Zona privada de la Suite (Vestidor y Baño privado de lujo con ventana exterior al Este).
  * **Zona Norte (sobre Despacho y Entrada):** Se mantiene en **1 sola planta** con cubierta inclinada (15%) de zinc autolimpiable.
* **Cero Terrazas Planas Sucias:** Ventanales limpios de suelo a techo en fachada Sur directos al jardín, sin salientes donde se acumulen hojas.
* **Cubierta Alta (+6,50 m):** Alberga los 12 módulos fotovoltaicos (5,4 kWp), 100 % libres de sombras e invisibles desde el jardín.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 en "U")

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-16** | Desembarco y Gran Galería Claustro | `(8.50, 14.30) -> (13.50, 17.00)` + desembarco | 5,00 × 2,70 m + 2,35 × 1,10 m | 13,50 m² | Norte / Patio | Mirador panorámico de 5,00 m sobre Patio Claustro y doble altura |
| **PA-17** | Dormitorio Infantil Niña | `(6.15, 17.00) -> (9.85, 21.45)` | 3,70 × 4,45 m | 14,20 m² | Sur / Jardín | Ventanal de suelo a techo C-12 (2,40m) al jardín Sur |
| **PA-18** | Dormitorio Infantil Niño | `(9.85, 17.00) -> (13.50, 21.45)`| 3,65 × 4,45 m | 14,00 m² | Sur / Jardín | Ventanal de suelo a techo C-13 (2,40m) al jardín Sur |
| **PA-19** | Baño Compartido Hijos (Ala Oeste) | `(6.15, 14.30) -> (8.50, 17.00)` | 2,35 × 2,70 m | 5,10 m² | Oeste / Ventana C-16 | Ventana exterior Oeste, inodoro, doble seno, ducha 120×80 y acceso directo P-11 |
| **PA-20** | Dormitorio Master Suite | `(13.50, 17.00) -> (17.00, 21.45)`| 3,50 × 4,45 m | 15,50 m² | Sur / Sureste | Ventanal panorámico C-14 (2,80m) al jardín Sur |
| **PA-21** | Vestidor Suite (Ala Este sobre Cocina) | `(13.50, 12.00) -> (17.00, 17.00)`| 3,50 × 4,00 m | 6,80 m² | Este / Claustro | 6,40 m de armarios dobles, paso a baño y conexión privada |
| **PA-22** | Baño Privado Suite (Ala Este sobre Cocina)| `(13.50, 8.50) -> (17.00, 12.00)`| 3,50 × 3,50 m | 6,20 m² | Norte y Este | Ducha 150×90, doble lavabo, ventanas exteriores C-11 y C-11B |
| **PA-24** | Campo Solar Fotovoltaico (5,4 kWp)| `Cubierta Superior (+6,50 m)` | Azotea Alta P1 | 38,00 m² | Sur 30° Óptimo | 100 % libre de sombras todo el día |

---

## 2. Grafo de Circulación 100 % Independiente y Limpio

```text
               [Escalera Volada PB-12 desde PB (Ala Oeste)]
                                    │
                  (Doble altura abierta con luz cenital)
                                    ▼ (Llegada en cota +3,15 m)
               [Gran Galería Claustro PA-16 (5,00 m de Mirador)]
                 (Luz natural cenital, suelo de roble y vistas al arce)
                                    │
         ┌──────────────────────────┼──────────────────────────┬──────────────────────────┐
         │ (Puerta P-11: 80 cm)     │ (Puerta P-12: 82 cm)     │ (Puerta P-13: 82 cm)     │ (Puerta P-14: 90 cm)
         ▼                          ▼                          ▼                          ▼
   [Baño Hijos PA-19]        [Dorm. Niña PA-17]         [Dorm. Niño PA-18]        [MASTER SUITE PRIVADA]
    (5,10 m² Ala Oeste)       (14,20 m² útiles)          (14,00 m² útiles)        ├──► [Dormitorio PA-20 (15,50 m²)]
    Ventana exterior Oeste            │                          │                │      (Ventanal C-14 al Jardín Sur)
                                      ▼                          ▼                └──► [Ala Este sobre Cocina]
                                [Jardín Sur]               [Jardín Sur]                  ├──► [Vestidor PA-21 (6,80 m²)]
                                                                                         └──► [Baño Suite PA-22 (6,20 m²)]
                                                                                                (Ventanas C-11 y C-11B)
```

---

## 3. Coordinación Estructural con Planta Baja

1. **Estructura en "U" apoyada sobre muros de carga de PB:**
   * **Ala Oeste:** Apoya sobre el muro estructural de la escalera y lavandería (`X = 6.15..8.50 m`).
   * **Ala Este:** Apoya sobre los muros de la cocina (`X = 13.50..17.00 m`).
   * **Ala Sur:** Apoya sobre el muro norte del salón (`Y = 14.30 m`) y vuela 3,00 m hacia el Sur cubriendo el Porche Sur (`Y = 18.45..21.45 m`).
2. **Patio Claustro Abierto al Cielo:**
   * El patio de PB (`10.00..13.20 m`, `8.50..11.70 m`) queda abrazado por las tres alas, recibiendo el sol cenital del mediodía y la luz del Norte libre de obstáculos.
3. **Chimenea Exterior Este:**
   * Adosada por el exterior de la fachada Este (`X = 17.00..17.80 m`, `Y = 20.65..21.45 m`), asciende como columna de granito hasta `+7,80 m`, sin tocar el interior del dormitorio de matrimonio.
