# Planta Baja: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Versión Optimizada Passivhaus (~165 m² construidos totales · Con Patio Claustro y Porche 3 m)

Este documento actúa como el **Master Plan Semántico de Planta Baja**. Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de cada estancia sin parsear archivos vectoriales.

* **Cota de Nivel General:** `±0,00 m` (Pavimento terminado interior y enrasado exterior cota cero).
* **Superficie Útil Interior PB:** `73,00 m²`.
* **Superficie Construida PB Cerrada:** `88,00 m²` (Ocupación: **14,6 %** sobre parcela de 600 m², ampliamente legal s/ límite del 20 % = 120 m² PXOM Oleiros Ord. 2B).
* **Superficies Exteriores Vinculadas:** Pérgola aparcamiento (24,00 m²), Porche Norte (3,00 m²), Patio Claustro Abierto (10,24 m²), Porche Sur Techado (21,60 m² · Fondo 3,00 m), Pradera Césped Sur (180,00 m²).
* **Cubiertas Autolimpiables:** La zona de entrada Norte (coches/mudroom) y el Ala Oeste (técnica/surf) cuentan con cubiertas inclinadas hacia los lindes exteriores para evacuación natural de aguas y hojas.
* **Churrasqueira y Chimenea:** En el extremo Este del Porche Sur (`X = 18.44 m`), con chimenea escultórica de granito moreno que sube por el exterior de la fachada Este.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (PB Optimizada)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Observaciones Funcionales |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PB-01** | Pérgola Cubierta Coches | `(1.60, 1.60) -> (5.60, 5.50)` | 4,00 × 5,00 m | 24,00 m² | Noroeste / Calle | Toma Wallbox 7,4 kW, paso cubierto al mudroom |
| **PB-02** | Porche Peatonal Norte | `(7.60, 4.00) -> (9.80, 5.50)` | 2,20 × 1,50 m | 3,00 m² | Norte | Granito abujardado cota +0,05 m |
| **PB-03** | Zaguán Mudroom Cortavientos | `(4.70, 5.50) -> (7.60, 7.60)` | 2,10 × 2,00 m | 4,20 m² | Noroeste | Banco zapatero 12 pares, secador y esclusa térmica |
| **PB-04** | Hall / Recibidor Principal | `(7.60, 5.50) -> (10.00, 8.00)` | 2,40 × 2,50 m | 6,00 m² | Norte / Central | Puerta noble pivotante y vista directa al patio claustro |
| **PB-05** | Despacho / Suite Invitados | `(10.00, 5.50) -> (13.20, 8.50)`| 3,20 × 3,00 m | 9,60 m² | Norte | Ventana Norte sin reflejos, sofá-cama y puerta acústica |
| **PB-06** | Baño Completo PB + Distribuidor | `(13.20, 5.50) -> (15.40, 7.25)`| 2,20 × 1,75 m | 3,80 m² | Noreste | Ducha cota cero 120×80 cm, inodoro Geberit y distribuidor neutro |
| **PB-07** | Patio Claustro Abierto | `(10.00, 8.50) -> (13.20, 11.70)`| 3,20 × 3,20 m | 10,24 m² | Núcleo Bioclimático | **Abierto al cielo.** Arce japonés, tarima Iroko y canaleta AISI 316 |
| **PB-08** | Cocina con Isla Santos / Dica | `(13.20, 8.50) -> (17.05, 12.00)`| 3,85 × 3,50 m | 13,50 m² | Este / Patio | Isla 2,20×1,00 m, frente columnas 3,50 m y salida a corrala |
| **PB-10** | Salón - Comedor Principal | `(7.60, 14.30) -> (15.50, 18.80)`| 7,90 × 4,50 m | 31,50 m² | Sur / Claustro | Muro TV 77\", conexión fluida a jardín y porche sur |
| **PB-12** | Escalera Volada Roble | `(7.60, 8.50) -> (9.20, 12.50)` | 1,40 × 4,00 m | 4,50 m² | Oeste / Patio | 17 peldaños, zanca oculta y luz cenital de claustro |
| **PB-13** | Sala Técnica / Surf & Lavandería| `(4.70, 7.60) -> (7.60, 11.80)` | 2,90 × 4,20 m | 10,50 m² | Oeste / Servicio | Aerotermia Vaillant, VMC Zehnder, lavadora/secadora y racks surf |
| **PB-14** | Porche Sur Techado Expandido | `(7.60, 18.80) -> (14.80, 21.80)`| 7,20 × 3,00 m | 21,60 m² | Sur / Pradera | **Fondo libre 3,00 m.** Cubierto 100% por P1. Churrasqueira al Este |
| **PB-15** | Pradera Césped Natural Sur | `(1.60, 21.80) -> (20.00, 30.00)`| 18,40 × 8,20 m | 180,00 m² | Sur | Pradera llana, sol de mediodía y preinstalación piscina Fase 2 |

---

## 2. Grafo de Adyacencias y Conexiones Físicas en Planta Baja

```text
[Calle / Pérgola PB-01]
       │
       ▼ (Paso exterior peatonal resguardado)
[Porche Norte PB-02] ──(Puerta Pivotante 1,00m)──► [Hall Principal PB-04]
                                                          │  ▲
       ┌──────────────────────────────────────────────────┘  │
       ▼ (Puerta batiente 82 cm)                             │
[Zaguán Mudroom PB-03] ──(Puerta estanca)──► [Sala Técnica PB-13]
       │
       ▼ (Distribuidor libre)
[Hall y Galería de Entrada]
  ├──► (Puerta acústica) ──► [Despacho / Suite Invitados PB-05]
  ├──► (Puerta batiente) ──► [Baño Completo PB-06]
  ├──► (Vista directa 360°) ──► [PATIO CLAUSTRO ABIERTO PB-07 (Arce japonés)]
  ├──► (Paso a Cocina) ──► [Cocina con Isla PB-08]
  └──► (Arranque escalera) ──► [Escalera Volada PB-12 hacia P1]
                                     │
                                     ▼
                      [Salón - Comedor Principal PB-10]
                                     │
                                     ▼ (Gran corredera elevable cota cero)
                      [PORCHE SUR TECHADO PB-14 (Fondo 3,00 m)]
                        ├── [Mesa 10 Comensales al Sur]
                        └── [Churrasqueira Granito al Este ──► Chimenea Exterior]
```

---

## 3. Condiciones Constructivas y Passivhaus Clave

1. **Forjado Sanitario Ventilado Cáviti:** Discurre continuo bajo toda la vivienda a cota $\pm 0,00\text{ m}$ con lámina elastomérica anti-radón termosoldada (CTE DB-HS6). El alcorque del arce japonés en el Patio Claustro es un cajón estanco de hormigón impermeabilizado apoyado sobre el forjado Cáviti, sin perforar la solera ni tener contacto directo con el sustrato granítico.
2. **Cubiertas Inclinadas Norte y Oeste:** Chapa de zinc / panel sándwich de alta densidad con pendiente del 15 % vertiendo hacia canalón exterior. Cero acumulación de hojas.
3. **Soportal Sur:** La Planta Primera cubre exactamente los 7,20 m × 3,00 m del Porche Sur, sirviendo de alero pasivo para el ventanal del salón en verano.
