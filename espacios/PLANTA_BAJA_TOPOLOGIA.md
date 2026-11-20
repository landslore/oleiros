# Planta Baja: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Optimizada Passivhaus (~165 m² construidos totales · Coches en Tándem Lateral + Patio Claustro y Porche 3 m)

Este documento actúa como el **Master Plan Semántico de Planta Baja** (Single Source of Truth). Permite a cualquier agente de IA o software CAD consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de cada estancia sin parsear archivos vectoriales.

* **Cota de Nivel General:** `±0,00 m` (Pavimento terminado interior y enrasado exterior cota cero).
* **Superficie Útil Interior PB:** `75,00 m²`.
* **Superficie Construida PB Cerrada:** `88,00 m²` (Ocupación: **14,6 %** sobre parcela de 600 m², ampliamente legal s/ límite del 20 % = 120 m² PXOM Oleiros Ord. 2B).
* **Superficies Exteriores Vinculadas:** Pérgola aparcamiento lateral 2 coches en línea (28,50 m²), Porche Peatonal Norte (7,40 m²), Patio Claustro Abierto (10,24 m²), Porche Sur Techado (32,55 m² · Fondo 3,00 m), Pradera Césped Sur (162,00 m²).
* **Aparcamiento en Tándem Lateral Oeste:** Los dos vehículos aparcan en línea (uno detrás de otro) a lo largo de la linde Oeste (`X = 1.00..3.85, Y = 2.50..12.50`). Esto libera el 100% de la fachada Norte para un acceso peatonal noble, jardín de entrada y vistas despejadas desde la calle.
* **Churrasqueira y Chimenea:** En el extremo Este del Porche Sur (`X = 17.00 m`), con chimenea de granito moreno exterior.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (PB Optimizada)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Observaciones Funcionales |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PB-01** | Pérgola Lateral 2 Coches en Línea | `(1.00, 2.50) -> (3.85, 12.50)` | 2,85 × 10,00 m | 28,50 m² | Oeste / Lateral | Coches en tándem, Wallbox 7,4 kW, paso resguardado a Mudroom y Sala Técnica |
| **PB-02** | Porche Peatonal Norte | `(6.15, 3.00) -> (9.85, 5.00)` | 3,70 × 2,00 m | 7,40 m² | Norte / Calle | Entrada noble ajardinada, granito abujardado cota +0,05 m ante puerta pivotante C-01 |
| **PB-03** | Zaguán Mudroom Cortavientos | `(3.85, 5.00) -> (6.15, 8.50)` | 2,30 × 3,50 m | 8,05 m² | Noroeste | Banco zapatero 16 pares, secador y esclusa térmica con puerta a pérgola |
| **PB-04** | Hall / Recibidor Principal | `(6.15, 5.00) -> (9.85, 8.50)` | 3,70 × 3,50 m | 12,95 m² | Norte / Central | Puerta noble pivotante y vista directa al patio claustro |
| **PB-05** | Despacho / Suite Invitados | `(9.85, 5.00) -> (13.65, 8.50)`| 3,80 × 3,50 m | 13,30 m² | Norte | Ventana Norte sin reflejos, sofá-cama y puerta acústica |
| **PB-06** | Baño Completo PB + Distribuidor | `(13.65, 5.00) -> (17.00, 8.50)`| 3,35 × 3,50 m | 11,72 m² | Noreste | Ducha cota cero 120×80 cm, inodoro Geberit y distribuidor neutro |
| **PB-13** | Sala Técnica / Surf Passivhaus | `(3.85, 8.50) -> (6.15, 12.50)` | 2,30 × 4,00 m | 9,20 m² | Oeste / Servicio | Aerotermia Vaillant, VMC Zehnder y racks surf con salida a pérgola |
| **PB-12** | Escalera Volada Roble | `(6.15, 8.50) -> (7.50, 12.50)` | 1,35 × 4,00 m | 5,40 m² | Oeste / Patio | 17 peldaños, zanca oculta y luz cenital de claustro |
| **PB-09** | Galería Pasillo Oeste Claustro | `(7.50, 8.50) -> (10.00, 12.50)`| 2,50 × 4,00 m | 10,00 m² | Oeste / Patio | Conecta hall y salón bordeando el patio por el oeste con vistas al arce |
| **PB-07** | Patio Claustro Abierto | `(10.00, 8.50) -> (13.20, 11.70)`| 3,20 × 3,20 m | 10,24 m² | Núcleo Bioclimático | **100% abierto al cielo.** Arce japonés, tarima Iroko y canaleta AISI 316 |
| **PB-07B**| Galería Paso Sur Claustro | `(10.00, 11.70) -> (13.20, 12.50)`| 3,20 × 0,80 m | 2,56 m² | Claustro / Salón | Conexión acristalada de paso sur entre cocina, salón y galería oeste |
| **PB-08** | Cocina con Isla Santos / Dica | `(13.20, 8.50) -> (17.00, 12.50)`| 3,80 × 4,00 m | 15,20 m² | Este / Patio | Isla 2,80×1,00 m, frente columnas 3,80 m y salida a corrala |
| **PB-13B**| Lavandería y Plancha Oeste | `(3.85, 12.50) -> (6.15, 18.45)`| 2,30 × 5,95 m | 13,68 m² | Oeste / Servicio | Lavadora, secadora, lencería y claraboyas cenitales |
| **PB-10** | Salón - Comedor Principal | `(6.15, 12.50) -> (17.00, 18.45)`| 10,85 × 5,95 m | 64,55 m² | Sur / Claustro | Muro TV 77", chimenea estanca, conexión fluida a jardín y porche sur |
| **PB-13C**| Caseta Jardinería y Aperos | `(3.85, 18.45) -> (6.15, 21.45)`| 2,30 × 3,00 m | 6,90 m² | Oeste / Jardín | Robot cortacésped, herramientas y cierre oeste del porche |
| **PB-14** | Porche Sur Techado Expandido | `(6.15, 18.45) -> (17.00, 21.45)`| 10,85 × 3,00 m | 32,55 m² | Sur / Pradera | **Fondo libre 3,00 m.** Cubierto 100% por P1. Churrasqueira al Este |
| **PB-15** | Pradera Césped Natural Sur | `(1.00, 21.45) -> (20.00, 30.00)`| 19,00 × 8,55 m | 162,00 m² | Sur | Pradera llana, sol de mediodía y preinstalación piscina Fase 2 |

---

## 2. Grafo de Adyacencias y Conexiones Físicas en Planta Baja

```text
[Calle Rúa dos Regos]
       │
       ├─────────────────────────────────────────┐
       ▼ (Entrada de vehículos al lateral Oeste)  ▼ (Acceso peatonal ajardinado al Norte)
[Pérgola Tándem PB-01 (10m x 2,85m)]        [Porche Peatonal Norte PB-02]
       │ (Paso lateral resguardado)               │ (Puerta Pivotante C-01)
       ├───────────────────┐                      ▼
       ▼                   ▼               [Hall Principal PB-04]
[Zaguán Mudroom PB-03] [Sala Técnica PB-13]       │
       │                                          ▼
       └─────────────────────────────► [Galería y Distribuidor]
                                         ├──► [Despacho / Suite PB-05]
                                         ├──► [Baño Completo PB-06]
                                         ├──► [Patio Claustro Abierto PB-07]
                                         ├──► [Cocina con Isla PB-08]
                                         └──► [Escalera Volada PB-12] ──► [P1]
                                                    │
                                                    ▼
                                     [Salón - Comedor Principal PB-10]
                                                    │
                                                    ▼
                                     [Porche Sur Techado PB-14 (3,00 m)]
```
