# Índice de Especificación Espacial y Topología (Digital Twin Markdown)

> **Instrucción para Agentes de IA:**
> **NO necesitas parsear los planos SVG de 1.400 líneas para comprender la distribución de la casa ni sus cotas.**
> Consulta este directorio `espacios/` para obtener en segundos las dimensiones exactas, coordenadas de enganche, carpinterías, instalaciones y criterios de materiales sin saturar tu ventana de contexto.

---

## 1. Documentos Maestros Globales

1. [SISTEMA_COORDENADAS_Y_EJES.md](./SISTEMA_COORDENADAS_Y_EJES.md):
   * Origen `(0,0)`, escala (`50 px = 1,00 m`), ejes estructurales (A–E y 1–6) y cotas Z en altura.
2. [CRITERIOS_MATERIALES_Y_ARMONIA.md](./CRITERIOS_MATERIALES_Y_ARMONIA.md):
   * **Pliego Canónico de Acabados:** Paleta cromática (NCS S 0502-Y, NCS S 2005-Y20R, RAL 9005 ST), maderas nobles (Roble natural interior, Iroko exterior), piedra caliza, porcelánicos C2/C3 e iluminación cálida (2.700 K CRI>90). Reglas de oro anti-ruptura de armonía.
3. [PLANTA_BAJA_TOPOLOGIA.md](./PLANTA_BAJA_TOPOLOGIA.md):
   * Bounding boxes de todas las estancias de PB (`109,25 m²` útiles interiores), grafo de adyacencias, red de puertas (C-01 a C-07, P-01 a P-06) y conexiones con exteriores.
4. [PLANTA_ALTA_TOPOLOGIA.md](./PLANTA_ALTA_TOPOLOGIA.md):
   * Bounding boxes de todas las estancias de P1 (`89,40 m²` útiles interiores), red de circulación, carpinterías (C-10 a C-15, P-07 a P-12) y coordinación de cargas con PB.

---

## 2. Fichas Particulares por Estancia (`estancias/`)

Cada ficha detalla:
* Bounding Box y cotas exactas en metros y px de dibujo.
* Paramentos Norte, Sur, Este y Oeste con especificación de muros y huecos de enganche.
* Cuadro de instalaciones (fontanería, saneamiento, tomas REBT, VMC y clima).
* Ergonomía y cumplimiento normativo (círculos libres de paso NHG).
* **Anexo particular de materiales y acabados** vinculado al pliego maestro de armonía.

### Planta Baja (`±0,00 m`):
* [PB-02: Porche Entrada Peatonal Norte (3,50 m²)](./estancias/pb_02_porche_norte.md)
* [PB-03: Zaguán Mudroom Térmico (5,80 m²)](./estancias/pb_03_zaguan_mudroom.md) *(Zoom técnico 1:20)*
* [PB-04: Hall / Recibidor Principal (10,40 m²)](./estancias/pb_04_hall_recibidor.md) *(Zoom técnico 1:20)*
* [PB-05: Despacho Sanctasanctórum / Suite PB (11,50 m²)](./estancias/pb_05_despacho_suite.md) *(Zoom técnico 1:20)*
* [PB-06: Baño Completo PB y Distribuidor Neutro (5,20 m²)](./estancias/pb_06_bano_pb.md) *(Zoom técnico 1:20)*
* [PB-07: Patio Corrala Central / Claustro Bioclimático (16,00 m²)](./estancias/pb_07_patio_corrala_central.md)
* [PB-08: Cocina Unificada Santos Fine con Isla de 3,60m (20,80 m²)](./estancias/pb_08_cocina_santos.md)
* [PB-10: Salón Principal con Chimenea (26,50 m²)](./estancias/pb_10_salon_chimenea.md)
* [PB-11: Comedor Principal Interior (17,50 m²)](./estancias/pb_11_comedor_principal.md)
* [PB-12: Escalera Volada de Roble (5,20 m²)](./estancias/pb_12_escalera_volada.md)
* [PB-13: Sala Técnica / Surf & Bicis Passivhaus (7,60 m²)](./estancias/pb_13_sala_tecnica_surf.md)
* [PB-13B: Lavandería y Plancha Oeste (11,60 m²)](./estancias/pb_13b_lavanderia_plancha.md)
* [PB-14: Porche Sur Techado Expandido (32,55 m²)](./estancias/pb_14_porche_sur.md)

### Planta Primera (`+3,15 m`):
* [PA-16: Desembarco Escalera y Galería Acústica (8,20 m²)](./estancias/pa_16_desembarco_galeria.md)
* [PA-17: Dormitorio Infantil Niña (14,60 m²)](./estancias/pa_17_dormitorio_infantil_nina.md)
* [PA-18: Dormitorio Infantil Niño (14,60 m²)](./estancias/pa_18_dormitorio_infantil_nino.md)
* [PA-19: Baño Compartido Hijos (6,80 m²)](./estancias/pa_19_bano_compartido_hijos.md)
* [PA-19B: Sala Polivalente Cine / Gaming / 4º Dormitorio (14,00 m²)](./estancias/pa_19b_sala_cine_gaming.md)
* [PA-20: Dormitorio Principal Master Suite (16,50 m²)](./estancias/pa_20_master_suite.md)
* [PA-21: Vestidor de Paso Doble Suite (8,40 m²)](./estancias/pa_21_vestidor_suite.md)
* [PA-22: Baño Privado Master Suite (6,30 m²)](./estancias/pa_22_bano_privado_suite.md)
* [PA-23: Balcón Corrido Sur Techado (13,20 m²)](./estancias/pa_23_balcon_corrido_sur.md)
