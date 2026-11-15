# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Optimizada Passivhaus (~165 m² construidos totales · Desfase Sur)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)**. Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y descanso sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado).
* **Altura Libre:** `2,65 m` a falso techo continuo.
* **Superficie Útil Interior P1:** `69,50 m²` (Aprovechamiento 100% útil sin pasillos residuales).
* **Superficie Construida P1:** `82,00 m²` cerrados.
* **Desfase Volumétrico Sur:** Toda la Planta Primera se desplaza hacia el Sur, cubriendo directamente los 3,00 m de fondo del Porche Sur de Planta Baja (efecto soportal continuo).
* **Cero Terrazas Planas Sucias:** Ventanales limpios de suelo a techo en fachada Sur; el agua y el viento limpian la fachada directamente.
* **Cubierta Alta (+6,50 m):** Alberga los 12 módulos fotovoltaicos (5,4 kWp), 100 % libres de sombras e invisibles desde el jardín.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 Optimizada)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-16** | Desembarco Escalera y Distribuidor | `(7.60, 14.30) -> (9.20, 17.50)` | 1,60 × 2,60 m | 4,20 m² | Norte / Cenital | Asoma directamente sobre el Patio Claustro |
| **PA-17** | Dormitorio Infantil Niña | `(7.60, 17.50) -> (11.00, 21.80)` | 3,40 × 4,20 m | 14,20 m² | Sur / Jardín | Ventanal limpio al jardín sobre el porche |
| **PA-18** | Dormitorio Infantil Niño | `(11.00, 17.50) -> (14.40, 21.80)`| 3,40 × 4,20 m | 14,20 m² | Sur / Jardín | Ventanal limpio al jardín sobre el porche |
| **PA-19** | Baño Compartido Hijos | `(9.20, 14.30) -> (11.70, 16.80)` | 2,50 × 1,80 m | 4,50 m² | Norte / Claustro | Luz y ventilación norte sobre el patio |
| **PA-20** | Dormitorio Master Suite | `(14.40, 17.50) -> (18.44, 21.80)`| 3,80 × 4,10 m | 15,50 m² | Sur / Sureste | Ventanal panorámico al jardín Sur |
| **PA-21** | Vestidor Suite Principal | `(14.40, 14.30) -> (16.50, 16.80)`| 2,10 × 1,80 m | 3,80 m² | Este | Conexión fluida dormitorio-baño |
| **PA-22** | Baño Privado Master Suite | `(16.50, 14.30) -> (18.44, 16.80)`| 2,40 × 1,75 m | 4,20 m² | Este / Noreste | Luz natural y doble lavabo |
| **PA-24** | Campo Solar Fotovoltaico (5,4 kWp)| `Cubierta Superior (+6,50 m)` | Azotea Alta P1 | 38,00 m² | Sur 30° Óptimo | 100 % libre de sombras todo el día |

> [!NOTE]
> **Modificaciones respecto al anteproyecto de 215 m²:**
> * `PA-19B` (Sala Cine / Gaming de 14 m²): Suprimida para encajar en el presupuesto objetivo de ~670k €.
> * `PA-23` (Balcón Corrido Exterior de 14 m²): Suprimido; el suelo de los dormitorios vuela directamente sobre el porche cubriéndolo sin salientes planos que acumulen hojas.
> * Chimenea de la churrasqueira: Discurre por el exterior de la fachada Este (`X = 18.44 m`) como columna escultórica de granito moreno gallego (Opción A), sin tocar el interior del dormitorio de matrimonio.

---

## 2. Grafo de Adyacencias y Circulación en Planta Primera

```text
               [Escalera Volada PB-12 desde PB]
                             │
                             ▼ (Llegada en cota +3,15 m)
            [Distribuidor Central de Noche PA-16 (4,20 m²)]
              │  (Vistas cenitales hacia el Patio Claustro Norte)
              │
              ├──► (Puerta batiente 82 cm) ──► [Baño Hijos PA-19 (4,50 m²)]
              │
              ├──► (Puerta batiente 82 cm) ──► [Dormitorio Niña PA-17 (14,20 m²)]
              │                                      │ (Ventanal Sur)
              │                                      ▼ [Jardín Sur]
              │
              ├──► (Puerta batiente 82 cm) ──► [Dormitorio Niño PA-18 (14,20 m²)]
              │                                      │ (Ventanal Sur)
              │                                      ▼ [Jardín Sur]
              │
              └──► (Paso libre / puerta 90 cm)
                        │
                        ▼
              [Master Suite Matrimonio]
                ├──► [Vestidor PA-21 (3,80 m²)] ──► [Baño Privado PA-22 (4,20 m²)]
                │
                └──► [Dormitorio Principal PA-20 (15,50 m²)]
                           │ (Ventanal Sur panorámico)
                           ▼ [Jardín Sur]
```

---

## 3. Coordinación Estructural con Planta Baja

1. **Alineación con el Porche Sur (Efecto Soportal):**
   * La fachada Sur de P1 (`Y = 21.80 m`) se alinea milimétricamente con el límite del Porche Sur de PB.
   * El techo del porche es directamente el suelo de los dormitorios. Cero terrazas, cero puentes térmicos en voladizo expuesto y sombra pasiva automática en verano sobre la planta baja.
2. **Fachada Norte de P1 sobre el Patio Claustro:**
   * La fachada Norte de P1 (`Y = 14.30 m`) apoya sobre la crujía estructural que separa el Salón del Patio Claustro.
   * El Patio Claustro (`Y: 10.00..13.20 m`) queda **100 % al aire libre**, recibiendo sol y luz cenital limpia desde el Norte sin ningún obstáculo de dos plantas.
3. **Chimenea Exterior Este:**
   * Adosada por el exterior de la fachada Este (`X = 18.44 m`), sube desde la churrasqueira en planta baja hasta sobrepasar 1,00 m la cubierta alta de P1, forrada en granito gallego.
