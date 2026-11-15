# Planta Baja: Topología Espacial, Bounding Boxes y Grafo de Adyacencia

Este documento actúa como el **Master Plan Semántico de Planta Baja**. Permite a cualquier agente de IA consultar instantáneamente las dimensiones, coordenadas envolventes y puntos de enganche de cada estancia sin parsear el plano `planta_baja_definitiva.svg`.

* **Cota de Nivel General:** `±0,00 m` (Pavimento terminado).
* **Superficie Útil Interior PB:** `109,25 m²`.
* **Superficie Construida PB:** `119,50 m²` (Computable ≤ 120,00 m² s/ PXOM Oleiros).
* **Superficies Exteriores Vinculadas:** Pérgola aparcamiento (28,00 m²), Porche Norte (3,50 m²), Patio Central Corrala (16,00 m²), Porche Sur Techado (32,55 m²), Jardín/Pradera Sur (171,00 m²).

---

## 1. Matriz Canónica de Estancias y Bounding Boxes (PB)

*Escala de coordenadas: 50 unidades de plano = 1,00 metro real.*

| ID | Estancia / Espacio | Coords SVG (X1, Y1) a (X2, Y2) | Cota Real en Metros (X1, Y1) a (X2, Y2) | Dimensión Libre (Ancho × Fondo) | Sup. Útil | Orientación Solar |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PB-01** | Pérgola Cubierta Aparcamiento | `(080, 080) -> (280, 260)` | `(1.60, 1.60) -> (5.60, 5.20)` | 4,00 × 5,00 m | 28,00 m² | Noroeste / Calle |
| **PB-02** | Porche Entrada Peatonal Norte | `(380, 200) -> (500, 275)` | `(7.60, 4.00) -> (10.00, 5.50)`| 2,40 × 1,50 m | 3,50 m² | Norte |
| **PB-03** | Zaguán Atlántico / Mudroom Térmico | `(235, 275) -> (380, 425)` | `(4.70, 5.50) -> (7.60, 8.50)` | 2,90 × 2,00 m | 5,80 m² | Noroeste |
| **PB-04** | Hall / Recibidor Principal | `(380, 275) -> (560, 460)` | `(7.60, 5.50) -> (11.20, 9.20)`| 3,60 × 2,90 m | 10,40 m² | Norte / Central |
| **PB-05** | Despacho Sanctasanctórum / Suite PB | `(560, 275) -> (755, 460)` | `(11.20, 5.50) -> (15.10, 9.20)`| 3,90 × 2,95 m | 11,50 m² | Norte |
| **PB-06** | Baño Completo PB + Distribuidor NHG | `(755, 275) -> (922, 440)` | `(15.10, 5.50) -> (18.44, 8.80)`| 3,35 × 1,55 m | 5,20 m² | Noreste |
| **PB-07** | Patio Corrala Central (Abierto) | `(450, 460) -> (650, 660)` | `(9.00, 9.20) -> (13.00, 13.20)`| 4,00 × 4,00 m | 16,00 m² | Núcleo Bioclimático |
| **PB-08** | Cocina Unificada Santos Fine | `(650, 440) -> (922, 705)` | `(13.00, 8.80) -> (18.44, 14.10)`| 5,44 × 3,82 m | 20,80 m² | Este / Jardín |
| **PB-10** | Salón Principal con Chimenea | `(380, 660) -> (600, 940)` | `(7.60, 13.20) -> (12.00, 18.80)`| 4,40 × 6,00 m | 26,50 m² | Sur / Claustro |
| **PB-11** | Comedor Principal Interior | `(600, 660) -> (850, 940)` | `(12.00, 13.20) -> (17.00, 18.80)`| 5,00 × 3,50 m | 17,50 m² | Sur / Este |
| **PB-12** | Escalera Volada Roble (17 Peldaños) | `(380, 460) -> (450, 660)` | `(7.60, 9.20) -> (9.00, 13.20)` | 1,40 × 4,00 m | 5,20 m² | Núcleo Oeste |
| **PB-13** | Sala Técnica / Surf & Bicis | `(235, 425) -> (380, 580)` | `(4.70, 8.50) -> (7.60, 11.60)`| 2,90 × 2,60 m | 7,60 m² | Oeste / Servicio |
| **PB-13B**| Lavandería y Plancha Oeste | `(235, 580) -> (380, 780)` | `(4.70, 11.60) -> (7.60, 15.60)`| 2,90 × 4,00 m | 11,60 m² | Oeste / Jardín |
| **PB-13C**| Caseta Jardín / Cortacésped | `(235, 780) -> (380, 940)` | `(4.70, 15.60) -> (7.60, 18.80)`| 2,90 × 3,20 m | 5,20 m² | Oeste / Porche Sur |
| **PB-14** | Porche Sur Techado Expandido | `(380, 940) -> (922, 1090)`| `(7.60, 18.80) -> (18.44, 21.80)`| 10,84 × 3,00 m | 32,55 m² | Sur / Pradera |
| **PB-15** | Pradera Césped Natural Sur | `(080, 1090) -> (1000, 1400)`| `(1.60, 21.80) -> (20.00, 28.00)`| 18,40 × 9,30 m | 171,00 m² | Sur |

---

## 2. Grafo de Adyacencias y Conexiones Físicas (Red de Accesos)

Cada arista del grafo define cómo se conectan dos estancias contiguas y la carpintería o vano asociado:

```text
[Calle / Pérgola PB-01]
       │
       ▼ (Paso exterior peatonal)
[Porche Norte PB-02] ──(Puerta Pivotante C-01: 1,00×2,40m)──► [Hall Principal PB-04]
                                                                  │  ▲  ▲
                      ┌───────────────────────────────────────────┘  │  │
                      ▼                                              │  │
           (Puerta Batiente P-01: 82cm)                              │  │
                      ▼                                              │  │
           [Zaguán Mudroom PB-03] ──(Puerta P-02)──► [Sala Surf PB-13] │
                                                                     │
                      ┌──────────────────────────────────────────────┘
                      ▼ (Acceso directo libre / vano 1,20m)
           [Distribuidor Eje Central]
            ├──► (Puerta Acústica P-04: 82cm) ──► [Despacho / Suite PB-05]
            ├──► (Puerta Batiente P-05: 82cm) ──► [Baño Completo PB-06]
            └──► (Puerta Corredera P-06: 1,00m) ──► [Cocina Santos PB-08]
                                                           │
                      ┌────────────────────────────────────┘
                      ▼ (Emboquillado diáfano 2,40m)
           [Comedor Principal PB-11] ◄──(Diáfano continuo)──► [Salón Chimenea PB-10]
                      │                                               │
                      └─────────────┬─────────────────────────────────┘
                                    ▼ (Corredera C-07: 7,50m en 3 hojas embutidas)
                         [Porche Sur Techado PB-14]
                                    │
                                    ▼ (Continuidad a ras de suelo)
                         [Pradera Jardín Sur PB-15]
```

### Tabla Resumen de Vanos y Conexiones de Enganche

| Desde | Hacia | Coordenadas Globales del Vano | Tipo de Vano / Carpintería | Ancho Libre |
| :--- | :--- | :--- | :--- | :--- |
| `PB-02 (Porche Norte)` | `PB-04 (Hall)` | `X: [430..480], Y: 275` | Puerta Pivotante C-01 acorazada Roble/Alum | 1,00 m (Hoja 1,20m) |
| `PB-04 (Hall)` | `PB-03 (Mudroom)` | `X: 380, Y: [340..385]` | Puerta enrasada P-01 batiente a mudroom | 0,82 m |
| `PB-03 (Mudroom)` | `PB-13 (Sala Surf)` | `Y: 425, X: [270..315]` | Puerta cortafuegos estanca P-02 | 0,82 m |
| `PB-04 (Hall)` | `PB-05 (Despacho)` | `X: 560, Y: [320..365]` | Puerta acústica P-04 ($R_w \ge 38\text{ dB}$) | 0,82 m |
| `PB-04 (Hall)` | `PB-06 (Baño PB)` | `X: 755, Y: [320..365]` | Puerta batiente P-05 (distribuidor neutro NHG)| 0,82 m |
| `PB-04 (Hall)` | `PB-08 (Cocina)` | `X: 680..730, Y: 440` | Puerta corredera embutida P-06 en tabique | 1,00 m |
| `PB-04 (Hall)` | `PB-12 (Escalera)` | `X: 380..450, Y: 460` | Arranque de escalera (Peldaño 1 volado) | 1,40 m libre |
| `PB-04 (Hall)` | `PB-07 (Patio Claustro)` | `Y: 460, X: [450..560]` | Fijo de vidrio triple de seguridad C-05 | 2,20 m vista |
| `PB-08 (Cocina)` | `PB-07 (Patio Claustro)` | `X: 650, Y: [460..580]` | Cristalera corredera C-06 salida al patio | 2,40 m |
| `PB-08 (Cocina)` | `PB-11 (Comedor)` | `Y: 705, X: [720..840]` | Vano abierto o corredera de vidrio oculta | 2,40 m diáfano |
| `PB-10 (Salón)` | `PB-11 (Comedor)` | `X: 600, Y: [660..940]` | Espacio unificado continuo diáfano | 5,60 m abierto |
| `PB-10/11 (Salón/Com)`| `PB-14 (Porche Sur)`| `Y: 940, X: [420..880]` | Gran Corredera Elevable C-07 (3 hojas) | 7,50 m |
| `PB-13 (Sala Surf)` | `PB-13B (Lavandería)`| `Y: 580, X: [270..315]` | Puerta de paso P-03 batiente | 0,82 m |
| `PB-13B (Lavandería)`| `Exterior Oeste` | `X: 235, Y: [640..685]` | Puerta vidriera salida a tendedero exterior | 0,90 m |
| `PB-14 (Porche Sur)`| `PB-13C (Caseta)` | `X: 380, Y: [820..865]` | Puerta batiente enrasada lamas de madera | 0,82 m |

---

## 3. Patés y Shunts Técnicos Verticales Compartidos con Planta Alta

1. **Bajante B-01 (Núcleo Baño Suite P1 a Baño PB):**
   * Coordenadas: `X: 765, Y: 285` (Esquina N-O del Baño PB-06). Shunt insonorizado 40×30 cm.
2. **Bajante B-02 (Baño Hijos P1 a Falso Techo Hall/Cocina):**
   * Coordenadas: `X: 545, Y: 285` (Muro divisorio Hall - Despacho). Shunt 30×30 cm con registro.
3. **Shunt Instalaciones Clima / VMC (Recuperador a Cubierta FV):**
   * Coordenadas: `X: 370, Y: 435` (Encuentro Sala Técnica PB-13 con zaguán y arranque de escalera). Patinillo 50×40 cm directo a cubierta plana técnica.
4. **Conducto Humos Chimenea Salón:**
   * Coordenadas: `X: 410, Y: 780` (Muro oeste del Salón PB-10, sube exento por galería P1 con doble pared inox aislada).
