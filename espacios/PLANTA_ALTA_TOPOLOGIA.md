# Planta Alta: Topología Espacial, Bounding Boxes y Grafo de Adyacencia
## Opción A: 4 Dormitorios Completos + Sala Multiusos Atardecer (16 m²) + Galería Claustro

Este documento actúa como el **Master Plan Semántico de Planta Primera (+3,15 m)** (Single Source of Truth). Permite a cualquier agente de IA o software CAD consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de las estancias de noche y ocio sin parsear archivos vectoriales.

* **Cota de Nivel General:** `+3,15 m` (Pavimento terminado de roble natural y porcelánico C3).
* **Altura Libre:** `2,65 m` a falso techo continuo con foso perimetral de iluminación indirecta.
* **Superficie Útil Interior P1:** `155,00 m²` útiles interiores.
* **Superficie Construida P1:** `175,00 m²` cerrados.
* **Programa Arquitectónico Optimizado (Opción A):**
  * **4 Dormitorios Completos:**
    1. **Master Suite Matrimonio (`PA-20`):** $13,35\text{ m²}$ zona dormitorio + Gran Vestidor en U `PA-21` ($17,10\text{ m²}$) + Baño privado de lujo `PA-22` ($15,20\text{ m²}$) con bañera exenta y ducha. Total suite: $45,65\text{ m²}$.
    2. **Dormitorio Infantil Niña (`PA-17`):** $14,68\text{ m²}$ ($3,30 \times 4,45\text{ m}$), ventanal de suelo a techo al Sur sobre porche.
    3. **Dormitorio Infantil Niño (`PA-18`):** $14,24\text{ m²}$ ($3,20 \times 4,45\text{ m}$), ventanal de suelo a techo al Sur sobre porche.
    4. **Dormitorio 4 / Invitados / Despacho P1 (`PA-25`):** $16,24\text{ m²}$ ($3,65 \times 4,45\text{ m}$), en esquina Suroeste con ventanal Sur y ventana Oeste al atardecer.
  * **Sala Multiusos Atardecer / Cine / Estar Familiar (`PA-19B`):**
    * $16,43\text{ m²}$ libres ($3,65 \times 4,50\text{ m}$), de formato cuadrangular óptimo en el Ala Oeste.
    * Incorpora el **Gran Mirador Panorámico C-18** ($3,00 \times 2,20\text{ m}$) orientado a poniente para contemplar el atardecer, sofá en L y pantalla multimedia 85".
    * Puerta independiente `P-19B` con acceso directo desde el distribuidor central general.
  * **Baño Compartido Hijos / Invitados (`PA-19`):**
    * $9,20\text{ m²}$ ($2,30 \times 4,00\text{ m}$), con mueble doble lavabo suspendido, ducha enrasada $150 \times 90\text{ cm}$, inodoro suspendido Geberit y ventana exterior Oeste `C-16`.
    * **Puerta `P-11` con acceso 100% directo e independiente** frente al desembarco de escalera en `Y = 12.50`. Cero intromisión en la sala multiusos.
  * **Galería Mirador y Rincón de Estudio Claustro (`PA-09` & `PA-16`):**
    * `PA-09` Galería Oeste ($10,00\text{ m²}$): Discurre entre la escalera y el patio, con gran frente acristalado continuo mirando al arce japonés.
    * `PA-16` Galería Sur y Zona Estudio ($25,65\text{ m²}$): Conecta el distribuidor con la suite este e integra un pupitre/estudio infantil frente a la luz cenital del claustro.
  * **Patio Claustro Abierto (`PA-07`):**
    * Hueco cenital libre al cielo de $3,20 \times 3,20\text{ m}$ ($10,24\text{ m²}$), exactamente coincidente 1:1 con Planta Baja.

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (P1 Opción A)

*Escala de coordenadas canónica: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar | Vistas / Ventilación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PA-07** | Patio Claustro Abierto (Hueco Cenital) | `(10.00, 8.50) -> (13.20, 11.70)` | 3,20 × 3,20 m | 10,24 m² | Núcleo Bioclimático | Hueco libre al cielo vertical 1:1 coincidente con PB-07 |
| **PA-07B**| Galería Paso Sur Claustro | `(10.00, 11.70) -> (13.20, 12.50)`| 3,20 × 0,80 m | 2,56 m² | Claustro / Distribuidor | Paso vidriado sur entre galería oeste y zona este |
| **PA-12** | Hueco y Desembarco Escalera Volada | `(6.15, 8.50) -> (7.50, 12.50)` | 1,35 × 4,00 m | 5,40 m² | Oeste / Cenital | Doble altura sobre escalera roble. Desembarco en cota +3,15 m a Y = 12.50 m |
| **PA-09** | Galería Mirador Oeste Claustro | `(7.50, 8.50) -> (10.00, 12.50)`| 2,50 × 4,00 m | 10,00 m² | Este / Claustro | Cristalera continua mirando al arce japonés del patio central |
| **PA-19** | Baño Compartido Hijos / Invitados | `(3.85, 8.50) -> (6.15, 12.50)` | 2,30 × 4,00 m | 9,20 m² | Oeste / Fachada | Ventana exterior Oeste C-16, doble seno, ducha 150×90 cm y puerta P-11 al desembarco |
| **PA-19B**| Sala Multiusos Atardecer / Cine | `(3.85, 12.50) -> (7.50, 17.00)` | 3,65 × 4,50 m | 16,43 m² | Oeste / Poniente | **16 m² formato óptimo.** Gran Mirador C-18 al atardecer, sofá L, pantalla 85", puerta P-19B |
| **PA-16** | Galería Distribuidora y Rincón Estudio | `(7.50, 12.50) -> (13.20, 17.00)`| 5,70 × 4,50 m | 25,65 m² | Centro / Claustro | Cristalera panorámica C-15 (3,20 m) con vistas directas al claustro y rincón de estudio |
| **PA-25** | Dormitorio 4 / Invitados / Despacho P1 | `(3.85, 17.00) -> (7.50, 21.45)` | 3,65 × 4,45 m | 16,24 m² | Sur y Oeste | Doble orientación: ventanal Sur sobre porche y ventana Oeste al atardecer |
| **PA-17** | Dormitorio Infantil Niña | `(7.50, 17.00) -> (10.80, 21.45)`| 3,30 × 4,45 m | 14,68 m² | Sur / Jardín | Ventanal suelo a techo C-12 (2,40 m) volando sobre porche sur |
| **PA-18** | Dormitorio Infantil Niño | `(10.80, 17.00) -> (14.00, 21.45)`| 3,20 × 4,45 m | 14,24 m² | Sur / Jardín | Ventanal suelo a techo C-13 (2,40 m) volando sobre porche sur |
| **PA-20** | Master Suite Matrimonio (Dormitorio) | `(14.00, 17.00) -> (17.00, 21.45)`| 3,00 × 4,45 m | 13,35 m² | Sur / Sureste | Ventanal suelo a techo C-14 (2,80 m) volando sobre porche sur |
| **PA-21** | Gran Vestidor Suite (sobre Cocina) | `(13.20, 12.50) -> (17.00, 17.00)`| 3,80 × 4,50 m | 17,10 m² | Este / Claustro | Armarios continuos en U, tocador, luz natural y paso privado a baño suite |
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
         ┌──────────────────────────┼──────────────────────────┬──────────────────────────┐
         │ (P-11: Puerta Norte)     │ (P-19B: Puerta Oeste)    │ (Pasillo hacia el Sur)   │ (Galerías Claustro PA-09/16)
         ▼                          ▼                          ▼                          ▼
   [BAÑO HIJOS / INVITADOS]     [SALA MULTIUSOS ATARDECER]  [DISTRIBUIDOR DE NOCHE]    [Vistas al Arce Japonés]
        (PA-19, 9,20 m²)            (PA-19B, 16,43 m²)                 │               Zona de estudio integrada
     ★ VENTANA EXTERIOR C-16      ★ GRAN MIRADOR PONIENTE C-18         ├──────────┬──────────┬──────────┐
     Doble seno + Ducha 150×90    Sofá L + Pantalla 85"                │ (P-25)   │ (P-12)   │ (P-13)   │ (P-14)
     Acceso 100% independiente    Estar familiar y cine                ▼          ▼          ▼          ▼
                                                                  [DORM. 4]  [DORM. NIÑA][DORM. NIÑO][MASTER SUITE]
                                                                   (PA-25)    (PA-17)    (PA-18)     ├──► [Dorm. PA-20 (13,4m²)]
                                                                  16,24 m²   14,68 m²   14,24 m²     └──► [Ala Este Privada]
                                                                 (Sur+Oeste)(Jardín Sur)(Jardín Sur)        ├──► [Vestidor PA-21 (17,1m²)]
                                                                                                            └──► [Baño Suite PA-22 (15,2m²)]
```
