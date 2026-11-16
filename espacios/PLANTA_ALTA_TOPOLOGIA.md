# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Amplia Familiar ~215 m² - 224 m² cerrados (CTE Clase A / nZEB · Sala Cine 15 m² + 3 Dormitorios)

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)** (Single Source of Truth). Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y ocio sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado de roble natural y porcelánico C3).
* **Altura Libre:** `2,65 m` a falso techo continuo con foso perimetral de iluminación indirecta.
* **Superficie Útil Interior P1:** `90,10 m²` (Distribución espaciosa y sin pasillos estrangulados).
* **Superficie Construida P1:** `~105,00 m²` cerrados.
* **Superficie Construida Total Vivienda (PB + P1):** `~215 - 224 m²` cerrados (`163,10 m² útiles interiores`).
* **Calidad Constructiva:** **CTE Clase A / nZEB (High Standard)** con presupuesto objetivo llave en mano de ~680.000 € (terreno e impuestos incluidos). Termoarcilla + SATE 12-14 cm, aerotermia y suelo radiante/refrescante.
* **Esquema de Distribución:**
  * **Núcleo Central Ocio (PA-19B):** Sala de Cine / Gaming / 4º Dormitorio polivalente (15,20 m² útiles) con tabiquería acústica box-in-a-box (Rw ≥ 50 dB), mirador panorámico C-17 sobre el Patio Claustro y pantalla de 110".
  * **Galería Distribuidora (PA-16):** Pasillo recto y luminoso de **1,80 m de ancho continuo** (`Y=15.20..17.00`), con accesos 100% independientes a todas las estancias. Cero pasos por baños ni zonas ajenas.
  * **Ala Sur (Dormitorios con Efecto Soportal):** 3 dormitorios de gran formato volando 3,00 m sobre el Porche Sur de PB. Ventanales limpios de suelo a techo (COR 70 RPT) protegidos del sol cenital y **cero balcones abiertos** para evitar mantenimiento, suciedad y filtraciones.
  * **Ala Este (Wellness Suite sobre Cocina):** Gran vestidor en "U" (8,00 m²) y Baño privado de lujo (6,80 m²) con doble ventana exterior (Norte y Este).
  * **Ala Oeste (Hueco de Escalera y Baño Hijos):** Doble altura cenital diáfana sobre el arranque de la escalera (`Y=8.50..13.20`), desembarco limpio y Baño de hijos (5,10 m²) con ventana exterior propia.
  * **Zona Norte de PB:** En 1 sola planta con cubierta inclinada (15%) de zinc autolimpiable.
* **Cubierta Alta (+6,50 m):** Alberga 14 módulos fotovoltaicos (6,30 kWp), 100% libres de sombras.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 ~215 m²)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-16** | Galería Distribuidora Recta | `(8.50, 15.20) -> (17.00, 17.00)` + desembarco `(6.15..8.50, 13.20..14.50)` | 1,80 m ancho continuo | 10,50 m² | Centro / Sur | Conecta directamente todos los accesos independientes |
| **PA-17** | Dormitorio Infantil Niña | `(6.15, 17.00) -> (9.85, 21.45)` | 3,70 × 4,45 m | 14,50 m² | Sur / Jardín | Ventanal de suelo a techo C-12 (2,40m) volando sobre porche |
| **PA-18** | Dormitorio Infantil Niño | `(9.85, 17.00) -> (13.50, 21.45)`| 3,65 × 4,45 m | 14,50 m² | Sur / Jardín | Ventanal de suelo a techo C-13 (2,40m) volando sobre porche |
| **PA-19** | Baño Compartido Hijos (Ala Oeste) | `(6.15, 14.50) -> (8.50, 17.00)` | 2,35 × 2,50 m | 5,10 m² | Oeste / Ventana C-16 | Ventana exterior Oeste, inodoro, mueble suspendido, ducha 120×80 y puerta P-11 |
| **PA-19B**| Sala Cine / Gaming / 4º Dormitorio | `(8.50, 11.70) -> (13.50, 15.20)` | 5,00 × 3,50 m | 15,20 m² | Norte / Claustro | Mirador C-17 (3,40m) al claustro, pantalla 110\", sofá L y puerta acústica P-19B |
| **PA-20** | Dormitorio Master Suite | `(13.50, 17.00) -> (17.00, 21.45)`| 3,50 × 4,45 m | 15,50 m² | Sur / Sureste | Ventanal suelo a techo C-14 (2,80m) volando sobre porche |
| **PA-21** | Gran Vestidor Suite (sobre Cocina) | `(13.50, 12.00) -> (17.00, 17.00)`| 3,50 × 5,00 m | 8,00 m² | Este / Claustro | 7,20 m lineales de armarios en U y paso privado a baño |
| **PA-22** | Baño Privado Suite (sobre Cocina) | `(13.50, 8.50) -> (17.00, 12.00)`| 3,50 × 3,50 m | 6,80 m² | Norte y Este | Doble seno, ducha 140×90, ventanas C-11 (N) y C-11B (E) |
| **PA-24** | Campo Solar Fotovoltaico (6,3 kWp)| `Cubierta Superior (+6,50 m)` | Azotea Alta P1 | 42,00 m² | Sur 30° Óptimo | 14 paneles solares monocristalinos libres de sombras |

---

## 2. Grafo de Circulación 100% Independiente y Limpio

```text
               [Escalera Volada PB-12 desde PB (Ala Oeste)]
                                    │
                  (Doble altura abierta con luz cenital)
                                    ▼ (Llegada en cota +3,15 m)
                     [Desembarco de Escalera P1]
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────────┐
       │     GALERÍA DISTRIBUIDORA RECTA PA-16 (1,80 m DE ANCHO)    │
       └────┬──────────────┬──────────────┬──────────────┬──────────┘
            │              │              │              │
      (P-11: 80cm)   (P-19B: 90cm)  (P-12: 82cm)   (P-13: 82cm)   (P-14: 90cm)
            ▼              ▼              ▼              ▼              ▼
       [Baño Hijos]  [SALA CINE /   [Dorm. Niña]   [Dorm. Niño]   [MASTER SUITE]
         (PA-19)       GAMING]        (PA-17)        (PA-18)      ├──► [Dormitorio PA-20]
         5,10 m²      (PA-19B)       14,50 m²       14,50 m²      │      (15,50 m² Sur)
        Ventana C-16  15,20 m²            │              │        └──► [Ala Este Privada]
                      Pantalla 110"       ▼              ▼               ├──► [Vestidor PA-21 (8,00 m²)]
                      Mirador C-17   [Jardín Sur]   [Jardín Sur]         └──► [Baño Suite PA-22 (6,80 m²)]
                                     (Soportal 3m)  (Soportal 3m)              (Ventanas C-11 y C-11B)
```

---

## 3. Coordinación Constructiva y Estructural

1. **Estructura Portante:**
   * **Ala Oeste:** Muros portantes sobre escalera y cuarto técnico/mudroom de PB. Doble altura abierta a cielo (`Y=8.50..13.20`) para inundar de luz el hall.
   * **Ala Este:** Apoya sobre los muros de la cocina (`X = 13.50..17.00 m`).
   * **Ala Sur:** Apoya sobre el pórtico norte del salón (`Y = 17.00 m`) y vuela 3,00 m en voladizo continuo cubriendo el Porche Sur (`Y = 18.45..21.45 m`).
2. **Patio Claustro Central:**
   * La Sala de Cine (PA-19B) se sitúa al sur del claustro (`Y=11.70..15.20`), permitiendo un mirador acristalado bajo hacia el jardín zen interior.
3. **Chimenea de Leña Exterior (Fachada Este):**
   * Chimenea cassette en salón adosada por el exterior de la fachada Este (`X = 17.00..17.80 m`, `Y = 20.65..21.45 m`) con conducto de doble pared inox Ø250 revestido en granito silvestre hasta `+7,80 m`, sin interferir en el espacio interior de la suite.
