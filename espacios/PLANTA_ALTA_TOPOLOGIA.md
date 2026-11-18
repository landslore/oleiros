# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Morfología en "U" Pura ~218 m² constr. (Opción B: Sala Multiusos Atardecer + Patio Libre al Cielo)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)** (Single Source of Truth). Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y ocio sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado de roble natural y porcelánico C3).
* **Altura Libre:** `2,65 m` a falso techo continuo con foso perimetral de iluminación indirecta.
* **Superficie Útil Interior P1:** `93,60 m²` (Aprovechamiento integral con ala oeste expandida sobre planta baja).
* **Superficie Construida P1:** `~110,00 m²` cerrados.
* **Superficie Construida Total Vivienda (PB + P1):** `~200,00 m²` cerrados (`~218,00 m²` computables totales con porches al 50%).
* **Superficie Útil Total Vivienda:** `166,60 m² útiles interiores`.
* **Calidad Constructiva:** **CTE Clase A / nZEB (High Standard)** con presupuesto objetivo llave en mano de ~680.000 € (terreno e impuestos incluidos). Termoarcilla + SATE 12-14 cm, aerotermia y suelo radiante/refrescante.
* **Esquema de Distribución:**
  * **Ala Oeste Expandida (`X = 3.85..7.80 m`):**
    * **Sala Multiusos Atardecer (PA-19B, 16,80 m² útiles):** En la esquina Suroeste (`X = 3.85..7.80, Y = 12.80..17.00`), dimensiones casi cuadradas (3,95 × 4,20 m). Incorpora el gran mirador panorámico `C-18` (2,60 × 2,20 m) a poniente, banco de lectura, sofá en "L" y pantalla multimedia 110"/85".
    * **Baño Compartido Hijos (PA-19, 6,00 m² útiles):** En el tercio norte (`X = 3.85..6.15, Y = 8.50..12.80`), con ventana exterior `C-16` a fachada oeste, mueble doble seno suspendido y plato de ducha enrasado de 140 × 80 cm. Acceso independiente `P-11` desde el desembarco.
    * **Escalera y Doble Altura Cenital (`X = 6.15..8.50, Y = 8.50..12.80`):** Se mantiene abierta sobre el arranque de la escalera, bañando de luz natural el hall de PB.
  * **Patio Claustro Central (`X = 8.50..13.50, Y = 8.50..15.20` · 5,00 × 6,70 m = 33,50 m²):**
    * **100% abierto al cielo.** Abraza el *Acer palmatum* y baña de luz cenital la planta baja y la planta alta.
  * **Galería Distribuidora Claustro (PA-16, 11,50 m² útiles):**
    * Bordea el Patio Claustro por el Sur (`Y = 15.20..17.00`, 1,80 m de ancho libre) con un frente acristalado panorámico continuo `C-15` (4,80 × 2,40 m).
  * **Ala Sur (Dormitorios con Soportal 3m):**
    * Tres dormitorios de gran formato volando 3,00 m sobre el Porche Sur de PB. Ventanales de suelo a techo y **cero balcones abiertos**.
  * **Ala Este (Zona Wellness Suite sobre Cocina):**
    * Gran Vestidor en "U" `PA-21` (8,00 m²) y Baño privado de lujo `PA-22` (6,80 m²) con ventanas exteriores Norte y Este.
* **Cubierta Alta (+6,50 m):** Alberga 14 módulos fotovoltaicos (6,30 kWp), 100% libres de sombras.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 Opción B)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-16** | Galería Distribuidora Claustro | `(7.80, 15.20) -> (17.00, 17.00)` + desembarco `(6.15..8.50, 12.50..15.20)` | 1,80 m ancho continuo | 11,50 m² | Centro / Claustro | Cristalera panorámica C-15 (4,80 m) con vistas 180° al claustro |
| **PA-17** | Dormitorio Infantil Niña | `(6.15, 17.00) -> (9.85, 21.45)` | 3,70 × 4,45 m | 14,50 m² | Sur / Jardín | Ventanal suelo a techo C-12 (2,40 m) volando sobre porche |
| **PA-18** | Dormitorio Infantil Niño | `(9.85, 17.00) -> (13.50, 21.45)`| 3,65 × 4,45 m | 14,50 m² | Sur / Jardín | Ventanal suelo a techo C-13 (2,40 m) volando sobre porche |
| **PA-19** | Baño Compartido Hijos (Ala Oeste N) | `(3.85, 8.50) -> (6.15, 12.80)` | 2,00 × 4,00 m | 6,00 m² | Oeste / Ventana C-16 | Ventana exterior Oeste C-16, doble seno, ducha 140×80 cm y acceso P-11 |
| **PA-19B**| Sala Multiusos Atardecer / Cine | `(3.85, 12.80) -> (7.80, 17.00)` | 3,95 × 4,20 m | 16,80 m² | Oeste / Poniente | Gran Mirador C-18 (2,60 m) al atardecer, sofá L, pantalla 110"/85" y puerta P-19B |
| **PA-20** | Dormitorio Master Suite | `(13.50, 17.00) -> (17.00, 21.45)`| 3,50 × 4,45 m | 15,50 m² | Sur / Sureste | Ventanal suelo a techo C-14 (2,80 m) volando sobre porche |
| **PA-21** | Gran Vestidor Suite (sobre Cocina) | `(13.50, 12.00) -> (17.00, 17.00)`| 3,50 × 5,00 m | 8,00 m² | Este / Claustro | 7,20 m lineales de armarios en U y paso privado a baño |
| **PA-22** | Baño Privado Suite (sobre Cocina) | `(13.50, 8.50) -> (17.00, 12.00)`| 3,50 × 3,50 m | 6,80 m² | Norte y Este | Doble seno, ducha 150×90 cm, ventanas C-11 (N) y C-11B (E) |
| **PA-24** | Campo Solar Fotovoltaico (6,3 kWp)| `Cubierta Superior (+6,50 m)` | Azotea Alta P1 | 42,00 m² | Sur 30° Óptimo | 14 paneles monocristalinos 450W libres de sombras |

---

## 2. Grafo de Circulación 100% Independiente y Limpio

```text
               [Escalera Volada PB-12 desde PB (Ala Oeste)]
                                    │
                  (Doble altura abierta con luz cenital)
                                    ▼ (Llegada en cota +3,15 m)
                     [Desembarco de Escalera P1]
                                    │
        ┌───────────────────────────┼────────────────────────────────────────┐
        │ (P-11: 80cm Norte)        │ (P-19B: 90cm Oeste)                    │ (Galería hacia el Sur)
        ▼                           ▼                                        ▼
   [Baño Hijos PA-19]    [SALA MULTIUSOS ATARDECER PA-19B]   [GRAN GALERÍA DISTRIBUIDORA PA-16]
     (6,00 m² utiles)         (16,80 m² utiles)               (Cristalera C-15 al Patio Claustro)
     Ventana Oeste C-16       ★ GRAN MIRADOR PONIENTE C-18                   │
     Doble seno + Ducha       Sofá L + Pantalla 110"/85"       ┌─────────────┼─────────────┐
                              Banco de lectura atardecer       │ (P-12)      │ (P-13)      │ (P-14)
                                                               ▼             ▼             ▼
                                                          [Dorm. Niña]  [Dorm. Niño]  [MASTER SUITE]
                                                            (PA-17)       (PA-18)     ├──► [Dorm. PA-20 (15,5m²)]
                                                           14,50 m²      14,50 m²     └──► [Ala Este Privada]
                                                               │             │               ├──► [Vestidor PA-21 (8,0m²)]
                                                               ▼             ▼               └──► [Baño Suite PA-22 (6,8m²)]
                                                          [Jardín Sur]  [Jardín Sur]              (Ventanas N y E)
                                                          (Soportal 3m) (Soportal 3m)
```
