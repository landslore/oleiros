# PROYECTO DE EJECUCIÓN DEFINITIVO · COTAS, GEOMETRÍA E INSTALACIONES
## Pabellón Bioclimático Atlántico en Liáns / Santa Cruz (Concello de Oleiros, A Coruña)
### Documento Maestro de Persistencia Agéntica — Single Source of Truth (SSOT)

> **PROPÓSITO AGÉNTICO:** Este documento contiene la totalidad de las especificaciones paramétricas, cotas milimétricas, coordenadas geométricas, carpinterías, instalaciones (eléctricas, datos, fontanería, saneamiento y ventilación VMC) y acabados de la **Propuesta D**. Cualquier agente de IA que lea este archivo debe ser capaz de reconstruir o generar de forma idéntica los planos vectoriales (SVG/CAD) y el modelo 3D sin necesidad de consultar archivos HTML auxiliares.

---

## 1. SISTEMA DE COORDENADAS GLOBAL Y PARCELA

* **Ubicación:** Liáns / Santa Cruz, Concello de Oleiros (A Coruña). Clima C1 Atlántico costero.
* **Normativa de Aplicación:** PGOM de Oleiros (Ordenanza 2B: Residencial Unifamiliar Aislada) y Normas do Hábitat Galego (Decreto 29/2010).
* **Dimensiones de la Parcela:** $20,00\text{ m}$ (Fachada Norte al vial) $\times 30,00\text{ m}$ (Fondo Norte-Sur) = **$600,00\text{ m}^2$**.
* **Retranqueos Obligatorios (PGOM Oleiros 2B):**
  * Retranqueo Frontal (Norte): **$5,00\text{ m}$** a cierre de vial público.
  * Retranqueos Laterales (Este y Oeste): **$3,00\text{ m}$** a linderos de parcelas colindantes.
  * Retranqueo Posterior (Sur / Testero): **$> 10,00\text{ m}$** (ocupa el jardín privado soleado y piscina).
* **Límites de Ocupación y Edificabilidad:**
  * Ocupación máxima en PB: $20,00\% \times 600\text{ m}^2 = \mathbf{120,00\text{ m}^2}$.
  * Ocupación cerrada real PB Propuesta D: **$116,50\text{ m}^2$ ($19,42\% \le 20,00\%$)** $\rightarrow$ **Cumple estrictamente**.
  * Porche Sur cubierto ($36,00\text{ m}^2$) computa al 50% según PGOM ($18,00\text{ m}^2$).
* **Sistema de Referencia Paramétrico (Escala 1:100 CAD: 1 metro = 40 px | Escala 1:50 Detalle: 1 metro = 100 px):**
  * Origen $(0, 0)$: Esquina Noroeste de la parcela.
  * Eje $+X$: Dirección Este (ancho de parcela, 0 a 20 m).
  * Eje $+Y$: Dirección Sur (fondo de parcela, 0 a 30 m).
  * Eje $+Z$: Cota de elevación vertical:
    * Cota terreno natural / vial: $-0,15\text{ m}$.
    * Cota Pérgola aparcamiento: $-0,10\text{ m}$.
    * Cota Porche Norte: $+0,05\text{ m}$.
    * Cota Planta Baja interior y Patio Corrala: $\mathbf{\pm 0,00\text{ m}}$ (enrasado a cota cero).
    * Cota Balcón Corrido Sur P1 y Planta Primera: $\mathbf{+3,15\text{ m}}$.
    * Cota Coronación de cubierta: $+6,80\text{ m}$.

---

## 2. MEMORIA DE SUPERFICIES Y CUADRO DE ESTANCIAS

| ID | Estancia | Planta | Sup. Útil ($m^2$) | Pavimento | Cota Z | Orientación |
|---|---|---|---|---|---|---|
| **E-01** | Pérgola 2 Vehículos | PB Ext. | 28,00 m² | Adoquín drenante | -0,10 m | Norte-Oeste |
| **E-02** | Porche Entrada Noble | PB Ext. | 3,50 m² | Granito abujardado C3 | +0,05 m | Norte |
| **E-03** | Zaguán Atlántico / Mudroom | PB | 5,80 m² | Porcelánico pizarra C3 | ±0,00 m | Norte-Oeste |
| **E-04** | Hall / Recibidor Principal | PB | 10,40 m² | Roble multicapa 14mm | ±0,00 m | Norte-Centro |
| **E-05** | Despacho Sanctasanctórum | PB | 11,50 m² | Roble multicapa 14mm | ±0,00 m | Norte-Centro |
| **E-06** | Baño Completo PB & Distribuidor | PB | 5,20 m² | Porcelánico C3 | ±0,00 m | Norte-Este |
| **E-07** | Patio Corrala Habitable | PB Int/Ext | 16,00 m² | Tarima Iroko cota cero | ±0,00 m | Centro (Cielo abierto) |
| **E-08** | Cocina con Isla Santos | PB | 15,20 m² | Porcelánico C2 120x60 | ±0,00 m | Este-Centro |
| **E-09** | Lavandería Técnica & Despensa | PB | 5,60 m² | Porcelánico C2 | ±0,00 m | Este-Sur |
| **E-10** | Salón Principal con Chimenea | PB | 26,50 m² | Caliza natural apomazada | ±0,00 m | Sur-Oeste |
| **E-11** | Comedor Principal 10 Pax | PB | 17,50 m² | Caliza natural apomazada | ±0,00 m | Sur-Este |
| **E-12** | Escalera Volada | PB-P1 | 5,20 m² | Roble macizo 80mm | ±0,00 a +3,15 m | Oeste-Centro |
| **E-13** | Trastero Surf/Bicis & Técnica | PB Ext. | 8,20 m² | Hormigón pulido epoxi | -0,05 m | Oeste |
| **E-14** | Porche Sur Expandido (Fondo 3m)| PB Ext. | 36,00 m² | Tarima Iroko cota cero | ±0,00 m | Sur (Techado) |
| **E-15** | Piscina Privada (7,5 × 3,5 m) | PB Ext. | 26,25 m² | Porcelánico arena vaso | -1,50 a -0,40 m| Sur (Soleado) |
| **E-16** | Galería Acústica & Distribuidor | P1 | 8,20 m² | Roble multicapa 14mm | +3,15 m | Centro-Oeste |
| **E-17** | Dormitorio Infantil Niña | P1 | 14,60 m² | Roble multicapa 14mm | +3,15 m | Sur-Oeste |
| **E-18** | Dormitorio Infantil Niño | P1 | 14,60 m² | Roble multicapa 14mm | +3,15 m | Sur-Centro |
| **E-19** | Baño Compartido Hijos | P1 | 6,80 m² | Porcelánico C3 | +3,15 m | Norte-Oeste |
| **E-20** | Suite Matrimonio Principal | P1 | 16,50 m² | Roble multicapa 14mm | +3,15 m | Sur-Este |
| **E-21** | Vestidor de Paso Doble Suite | P1 | 8,40 m² | Roble multicapa 14mm | +3,15 m | Centro-Este |
| **E-22** | Baño Privado Suite (Ducha doble)| P1 | 6,30 m² | Porcelánico C3 | +3,15 m | Norte-Este |
| **E-23** | Balcón Corrido Sur P1 | P1 Ext. | 14,00 m² | Tarima Iroko cota cero | +3,15 m | Sur (Voladizo) |
| **TOTAL**| **SUPERFICIE ÚTIL TOTAL INTERIOR** | | **188,40 m²** | *(PB: 98,90 m² + P1: 89,50 m²)* | | |
| **TOTAL**| **SUPERFICIE CUBIERTA EXTERIOR** | | **81,50 m²** | *(Pérgola 28m² + Porches 39,5m² + Balcón 14m²)* | | |

---

## 3. DEFINICIÓN GEOMÉTRICA PLANTA A PLANTA (COTAS Y COORDENADAS)

### 3.1. PLANTA BAJA (Cota ±0,00 m)

#### A. ZONA NORTE (Acceso, Aislamiento y Trabajo)
1. **PÉRGOLA DE APARCAMIENTO (28,00 m² · $7,00 \times 4,00\text{ m}$):**
   * Coordenadas: $X \in [1,10; 3,90\text{ m}]$, $Y \in [5,00; 12,00\text{ m}]$.
   * Capacidad: 2 vehículos en batería ($2,50 \times 5,00\text{ m}$ cada plaza).
   * Paso cubierto: 2 metros de pasillo lateral directo hacia la puerta del Zaguán Mudroom.
   * Instalación VE: Caja mural Wallbox 7,4 kW (32A) a $h=140\text{ cm}$ en pilar metálico oeste, alimentada con cable $3 \times 10\text{ mm}^2$ directo desde el CGMP.
2. **PORCHE NORTE PEATONAL (3,50 m² · $2,30 \times 1,50\text{ m}$):**
   * Coordenadas: $X \in [7,00; 9,30\text{ m}]$, $Y \in [3,50; 5,00\text{ m}]$.
   * Pavimento: Granito moreno abujardado antideslizante C3 a cota $+0,05\text{ m}$ con pendiente 1,5% hacia fuera.
   * Videoportero: Placa IP PoE con cámara gran angular 180° a $h=150\text{ cm}$ en jamba derecha.
3. **01. ZAGUÁN ATLÁNTICO / MUDROOM (5,80 m² · $1,90 \times 3,05\text{ m}$):**
   * Coordenadas interiores: $X \in [4,25; 6,15\text{ m}]$, $Y \in [5,35; 8,40\text{ m}]$.
   * Puerta Acceso Pérgola (Muro Oeste): Carpintería de aluminio *Cortizo COR 80 RPT* ($0,90 \times 2,10\text{ m}$), apertura batiente hacia el interior a izquierdas, con junta perimétrica de estanqueidad y burlete de guillotina automático al suelo.
   * Puerta hacia Hall (Muro Este): Corredera empotrada de vidrio estriado (*Fluted glass*) de 8 mm ($0,85 \times 2,40\text{ m}$).
   * Puerta hacia Trastero (Muro Sur): Corredera acústica ciega ($0,80 \times 2,10\text{ m}$).
   * Mobiliario: Banco de roble macizo ($1,60 \times 0,45\text{ m}$, $h=45\text{ cm}$) con zapatero ventilado inferior (16 pares). Armario secador de ropa de lluvia ($0,70 \times 0,60\text{ m}$) con bandeja de acero inox para goteo y extracción VMC directa.
   * Tomas e Instalaciones: 2 Schukos 16A a $h=30\text{ cm}$, detector de presencia PIR en techo, boca de extracción VMC $\varnothing 125\text{ mm}$ a $30\text{ m}^3/\text{h}$.
4. **02. HALL / RECIBIDOR PRINCIPAL (10,40 m² · $3,50 \times 2,97\text{ m}$):**
   * Coordenadas interiores: $X \in [6,25; 9,75\text{ m}]$, $Y \in [5,35; 8,32\text{ m}]$.
   * Puerta Noble Norte: Pivotante de iroko macizo con eje descentrado a 15 cm ($1,00 \times 2,40\text{ m}$ paso libre; hueco $1,15 \times 2,45\text{ m}$). Cerradura electrónica motorizada con lector dactilar.
   * Armario Gabanero (Pared Oeste): Empotrado de suelo a techo ($1,80 \times 0,65\text{ m}$, altura $2,60\text{ m}$), 3 puertas batientes lisas lacadas blanco roto mate.
   * Cristalera Sur (Vistas a Patio): Paño fijo de suelo a techo *Cortizo Cor Vision Plus* ($2,80 \times 2,60\text{ m}$) con carpintería oculta.
   * Cuadros Técnicos: CGMP y RITI empotrados tras panelado de roble alistonado registrable. Pantalla domótica táctil 7" a $h=145\text{ cm}$.
5. **03. DESPACHO SANCTASANCTÓRUM / SUITE INVITADOS (11,50 m² · $3,80 \times 3,03\text{ m}$):**
   * Coordenadas interiores: $X \in [9,85; 13,65\text{ m}]$, $Y \in [5,35; 8,38\text{ m}]$.
   * Ventana Norte (Calle): Oscilobatiente *Cortizo COR 80 RPT* ($1,80 \times 1,20\text{ m}$, antepecho $h=95\text{ cm}$). Vidrio triple Guardian Sun 4+4Silence/16Ar/4/16Ar/4. Persiana motorizada de lamas orientables.
   * Cristalera Sur (Patio Corrala): Cristalera fija ($2,40 \times 2,60\text{ m}$) con cortina acústica de lino grueso motorizada.
   * Puerta Acceso (Pared Oeste): Puerta acústica maciza isofónica ($0,82 \times 2,10\text{ m}$, $R_w \ge 38\text{ dB}$) con guillotina retráctil inferior, batiente a derechas hacia interior.
   * Mesa de Trabajo: Roble macizo ($1,80 \times 0,80\text{ m}$) apoyada en pared oeste, con la luz de la ventana norte entrando a 90° por la izquierda (cero reflejos). Torre de mecanismos integrada en mesa con 4 Schuko 16A + 2 RJ45 Cat 6A blindados (10 Gbps) + USB-C PD 65W.
   * Sofá-cama invitados: $1,40 \times 2,00\text{ m}$ en pared este.
   * Climatización: Impulsión VMC $\varnothing 125\text{ mm}$ a $35\text{ m}^3/\text{h}$ + suelo radiante zonal con termostato táctil a $h=145\text{ cm}$.
6. **04. BAÑO COMPLETO PB & DISTRIBUIDOR NEUTRO (5,20 m² · $2,30 \times 2,26\text{ m}$):**
   * Coordenadas interiores: $X \in [13,75; 16,05\text{ m}]$, $Y \in [5,35; 7,61\text{ m}]$.
   * Distribuidor Neutro previo: Independizado con puerta corredera oculta Krona de $0,72\text{ m}$ (estricto cumplimiento NHG Galicia: doble puerta respecto a cocina).
   * Ventana Norte: Oscilobatiente alta ($0,80 \times 0,60\text{ m}$, antepecho $h=160\text{ cm}$, vidrio translúcido).
   * Ducha Walk-in cota cero ($1,20 \times 0,80\text{ m}$): Pendiente 2% hacia sumidero lineal oculto inox AISI 316 con lámina impermeable *Schlüter-KERDI* termosoldada. Mampara fija de vidrio templado 8 mm antical. Grifería termostática empotrada negra mate con rociador de techo $\varnothing 25\text{ cm}$.
   * Inodoro Suspendido: *Geberit iCon Rimless* sobre bastidor *Duofix* con cisterna *Sigma 8 cm* y pulsador *DuoFresh* con extracción de olores. Bajante insonorizada *Geberit Silent-PP $\varnothing 110\text{ mm}$*.
   * Lavabo: Suspendido de roble ($0,90 \times 0,48\text{ m}$, $h=85\text{ cm}$), grifo empotrado en pared a $h=105\text{ cm}$, 2 Schukos IP44 con diferencial dedicado de 10 mA.
   * Ventilación: Boca de extracción VMC $\varnothing 125\text{ mm}$ a $50\text{ m}^3/\text{h}$.

---

#### B. BANDA CENTRAL (Patio Corrala, Cocina y Servicios)
7. **05. PATIO CORRALA HABITABLE (16,00 m² · $4,00 \times 4,00\text{ m}$):**
   * Coordenadas libres: $X \in [8,50; 12,50\text{ m}]$, $Y \in [8,40; 12,40\text{ m}]$.
   * Naturaleza: Patio claustral central 100% habitable, enrasado a cota cero ($\pm 0,00\text{ m}$), abierto al cielo (sin cubiertas ni lucernarios cerrados).
   * Pavimento: Tarima de Iroko macizo ($120 \times 21\text{ mm}$) fijada con clips ocultos inox A4 sobre rastreles de aluminio y plots autonivelantes.
   * Drenaje Pluvial: Canaleta perimetral de ranura oculta inox AISI 316 bajo los 4 umbrales de vidrio + 2 sumideros sifónicos pluviales $\varnothing 110\text{ mm}$ con cesta antihojas conectada a red separativa.
   * Alcorque Vegetal: Esquina Noroeste ($r=42\text{ cm}$), relleno de grava volcánica drenante con ejemplar de *Acer palmatum* (arce japonés), riego por goteo integrado y foco sumergible IP68 LED cálido 2700K rasante al tronco.
   * Banco de Lectura: En pared Norte bajo alero perimetral de 80 cm de hormigón. Madera maciza de iroko ($2,40 \times 0,50\text{ m}$, $h=45\text{ cm}$) con colchoneta náutica Sunbrella.
   * Carpinterías Correderas Elevables Cortizo Cor Vision:
     * Hacia Cocina (Este): 2 hojas ($3,00 \times 2,60\text{ m}$, paso libre $1,40\text{ m}$).
     * Hacia Salón-Comedor (Sur): 2 hojas ($3,00 \times 2,60\text{ m}$).
     * Hacia Galería/Escalera (Oeste): 2 hojas ($2,50 \times 2,60\text{ m}$).
     * Hacia Despacho/Hall (Norte): Cristaleras fijas embutidas.
8. **06. COCINA CON ISLA SANTOS (15,20 m² · $4,20 \times 3,62\text{ m}$):**
   * Coordenadas interiores: $X \in [12,60; 16,80\text{ m}]$, $Y \in [8,40; 12,02\text{ m}]$.
   * Isla Central Santos Modelo Fine ($2,80 \times 1,00\text{ m}$):
     * Encimera Dekton Kelya de 20 mm con canto ingleteado.
     * Pasos libres ergonómicos: **$105\text{ cm}$ hacia el patio (Oeste)** y **$110\text{ cm}$ hacia las columnas (Este)**.
     * Cocción: Placa de inducción *Bora Pure* de 7,6 kW con extractor central descendente integrado y conducto plano *Bora Ecotube* por cámara sanitaria hacia fachada norte (Circuito C3, cable $6\text{ mm}^2$, PIA 25A). Cero campana colgada.
     * Fregadero: Seno bajo encimera de $70\text{ cm}$ inox antracita con grifería monomando extraíble.
     * Torre de enchufes: *EVOline BackFlip* enrasada en Dekton (2 Schukos + USB-C PD 30W).
   * Pared de Columnas (Pared Este):
     * Mueble Desayunador con *Pocket Doors* escamoteables, encimera de roble, 4 Schukos dedicados (C4) e iluminación LED 2700K al abrir.
     * Columna Horno Pirolítico + Microondas $60\text{ cm}$ a media altura.
     * Frigorífico Combi integrable No-Frost de $70\text{ cm}$ con toma de agua.
   * Climatización: Suelo radiante con termostato táctil + extracción forzada VMC $\varnothing 125\text{ mm}$ a $50\text{ m}^3/\text{h}$.
9. **07. LAVANDERÍA TÉCNICA & DESPENSA (5,60 m² · $2,40 \times 2,33\text{ m}$):**
   * Coordenadas interiores: $X \in [14,40; 16,80\text{ m}]$, $Y \in [12,12; 14,45\text{ m}]$.
   * Puerta: Corredera empotrada de $0,80\text{ m}$ lacada blanco mate.
   * Bancada de Lavado: Hormigón aligerado con apoyos de neopreno antivibratorio para lavadora y secadora en columna. 2 tomas Schuko 16A a $h=120\text{ cm}$ (Circuito C10).
   * Pila de Lavar: Resina sintética blanca ($50 \times 40\text{ cm}$) con monomando y llaves de corte PEX-a.
   * Despensa: Módulos de estanterías metálicas de $40\text{ cm}$ de fondo.
   * Ventilación: Extracción VMC $\varnothing 125\text{ mm}$ a $30\text{ m}^3/\text{h}$.
10. **ESCALERA PRINCIPAL VOLADA (Ala Oeste · 17 Peldaños):**
    * Coordenadas: $X \in [6,85; 7,90\text{ m}]$, $Y \in [8,40; 13,33\text{ m}]$. Sentido de subida: Norte $\rightarrow$ Sur.
    * Estructura: Zanca de acero HEA 160 oculta en muro perimetral oeste con cartelas en voladizo de chapa de 15 mm.
    * Peldaños: Madera maciza de roble natural de **$80\text{ mm}$ de espesor** enfundados sobre estructura con elastómero acústico.
    * Dimensiones: Ancho útil = **$1,05\text{ m}$**, Huella = **$29,0\text{ cm}$**, Contrahuella = **$17,6\text{ cm}$** ($2CH + H = 64,2\text{ cm}$, Ley de Blondel estricta).
    * Barandilla: Vidrio estructural templado-laminado $10+10.2\text{ mm}$ anclado con perfil en $U$ empotrado en canto de forjado.
    * Iluminación: Tiras LED 24V ocultas bajo el vuelo de cada peldaño con encendido secuencial mediante sensores de presencia.
11. **TRASTERO EXTERIOR DE SURF & SALA TÉCNICA (8,20 m² · $2,40 \times 3,42\text{ m}$):**
    * Coordenadas: $X \in [3,75; 6,15\text{ m}]$, $Y \in [8,50; 11,92\text{ m}]$. Acceso exclusivamente exterior.
    * Equipos Passivhaus:
      * Bomba de calor Aerotermia *Vaillant aroTHERM plus* bibloc (gas R290).
      * Interacumulador de ACS de 250 litros con bomba de recirculación de alta eficiencia.
      * Unidad VMC *Zehnder ComfoAir Q350* con recuperador entálpico (92% de rendimiento) y silenciadores acústicos.
      * Inversor solar híbrido fotovoltaico de 5 kW con protecciones DC/AC y conexión ethernet.
      * Desagüe de condensados $\varnothing 40\text{ mm}$ con sifón seco esférico de seguridad antiolores.
    * Equipamiento Deportivo: Racks de pared para 3 tablas de surf + barra con bandeja inox perforada para secado de 3 neoprenos + ganchos de pared para 3 bicicletas.

---

#### C. ZONA SUR (Convivencia Noble y Exteriores)
12. **08. SALÓN PRINCIPAL CON CHIMENEA (26,50 m² · $5,30 \times 5,00\text{ m}$):**
    * Coordenadas interiores: $X \in [7,90; 13,20\text{ m}]$, $Y \in [13,45; 18,45\text{ m}]$. Altura libre: **$2,80\text{ m}$**.
    * Pared Oeste (Granito Moreno Gallego, Fuego y TV):
      * Muro de carga revestido en granito moreno del país en junta seca.
      * **Chimenea Estanca de Leña:** Hogar con puerta guillotina panorámica de 3 caras (*Stûv 21* o similar). Toma de aire exterior directa de $\varnothing 150\text{ mm}$ canalizada bajo solera. Conducto concéntrico de humos en acero inox AISI 316 doble pared aislada $\varnothing 200\text{ mm}$ hasta sobrepasar 1 m la cumbrera. Leñero vertical encastrado con luz LED.
      * **Muro Multimedia / Pantalla OLED 77":** Hornacina enrasada a $h=110\text{ cm}$. Conducto pasacables embutido $\varnothing 50\text{ mm}$ hasta el mueble bajo suspendido de roble ($2,40 \times 0,45\text{ m}$, $h=45\text{ cm}$). 6 tomas Schuko 16A + 2 tomas RJ45 Cat 6A blindadas a $h=35\text{ cm}$ + tomas TV/SAT.
    * Mobiliario: Sofá modular en L ($3,40 \times 2,40\text{ m}$) a $3,80\text{ m}$ de distancia de la pantalla, orientado hacia el fuego/TV (Oeste) y hacia el jardín/piscina (Sur). Mesa de centro de roble ($1,40 \times 0,80\text{ m}$).
    * Pared Sur: Gran corredera elevable *Cortizo Cor Vision Plus* de 3 hojas embutidas en solera a cota cero ($\pm 0,00\text{ m}$): **hueco de $5,00 \times 2,60\text{ m}$**. Vidrio triple Guardian Sun ($U_g = 0,6\text{ W/m}^2\text{K}$, $g=0,38$).
    * Protección Solar: Estor motorizado enrollable oculto en fosa de falso techo con tejido *Screen 1%*.
13. **09. COMEDOR PRINCIPAL INTERIOR 10 PLAZAS (17,50 m² · $4,20 \times 4,17\text{ m}$):**
    * Coordenadas interiores: $X \in [13,20; 17,40\text{ m}]$, $Y \in [13,45; 17,62\text{ m}]$.
    * Mesa de Comedor: Roble macizo natural ($2,80 \times 1,00\text{ m}$) para 10 personas con lámpara lineal suspendida DALI-2 a $h=160\text{ cm}$.
    * Pared Este: Aparador suspendido de $2,00\text{ m}$ con 2 Schukos a $h=90\text{ cm}$.
    * Pared Sur: Corredera elevable *Cortizo Cor Vision* de 2 hojas ($3,50 \times 2,60\text{ m}$).
14. **10. PORCHE SUR EXPANDIDO TECHADO (36,00 m² cubiertos · Fondo real de 3,00 m):**
    * Coordenadas cubiertas: $X \in [7,50; 19,50\text{ m}]$, $Y \in [18,45; 21,45\text{ m}]$. Cota: $\mathbf{\pm 0,00\text{ m}}$ enrasado con interior.
    * Techo: Forjado superior de hormigón en voladizo con falso techo de madera de iroko y downlights LED IP65 2700K empotrados.
    * Pavimento: Tarima maciza de Iroko ($120 \times 21\text{ mm}$) con canaleta perimetral de drenaje oculta en acero inoxidable AISI 316.
    * **Churrasqueira Tradicional de Granito de Obra (Pared Este del Porche):**
      * Módulo de granito moreno gallego de $2,20 \times 0,80\text{ m}$.
      * Parrilla de carbón/leña en acero inoxidable de $100 \times 60\text{ cm}$ con manivela de elevación y cajón de cenizas.
      * Campana exterior de chapa de acero de 3 mm lacada en negro forja anticalórico.
      * Bancada de granito negro *Zimbabwe* de $1,20\text{ m}$ con pila auxiliar inox exterior con grifo monomando de agua fría y caliente.
      * Leñero inferior ventilado con capacidad para $1\text{ m}^3$ de leña.
      * 2 tomas Schuko estancas IP66 con tapa abatible.
    * Comedor de Verano: Mesa de iroko/teca ($2,80 \times 1,00\text{ m}$) para 10 plazas frente a la cristalera del comedor interior.
    * Zona Lounge Exterior: Sofá en L de cuerda náutica Sunbrella y mesa baja frente a la cristalera del salón.
15. **11. PISCINA PRIVADA SOLEADA (26,25 m² · $7,50 \times 3,50\text{ m}$) & JARDÍN SUR:**
    * Coordenadas: $X \in [9,50; 17,00\text{ m}]$, $Y \in [22,50; 26,00\text{ m}]$.
    * Vaso: Hormigón gunitado proyectado de 25 cm de espesor con gresite porcelánico continuo color arena (agua turquesa caribeño).
    * Profundidad: Playa sumergida de acceso con banco de hidromasaje en extremo oeste ($h=40\text{ cm}$); vaso con pendiente suave de $1,20\text{ m}$ a $1,50\text{ m}$.
    * Albardilla: Piedra caliza natural abujardada antideslizante C3 de 50 cm de ancho enrasada con el césped atlántico.
    * Caseta Técnica Enterrada ($2,00 \times 1,50\text{ m}$ en esquina sureste): Clorador salino automático con sonda inteligente de pH y bomba de velocidad variable (< 45 dB) + 2 focos subacuáticos LED blancos cálidos 3000K + preinstalación hidráulica para climatización por aerotermia.
    * Jardín y Robot: Riego automático por aspersión emergente en 4 sectores con programador wifi. Caseta de carga estanca para robot cortacésped en lateral oeste.

---

### 3.2. PLANTA PRIMERA (Cota +3,15 m)

```
                            FACHADA NORTE (Técnica & Baños)
+---------------------------------------+---------------------------------------+
| OESTE                                 | ESTE                                  |
| 15. BAÑO COMPARTIDO HIJOS (6,80 m²)   | 18. BAÑO PRIVADO SUITE (6,30 m²)      |
| • Doble lavabo en encimera Dekton     | • Doble seno Dekton Kelya + espejo LED|
| • Bañera / Ducha amplia 1,70 × 0,75 m | • Ducha italiana doble 1,50 × 0,90 m  |
| • Inodoro suspendido Geberit          | • Inodoro suspendido Geberit Rimless  |
| • Radiador toallero hidráulico 750W   | • Toallero radiador independiente     |
| • Ventana norte alta oscilobatiente   | • Ventana norte alta oscilobatiente   |
+---------------------------------------+---------------------------------------+
| 12. DESEMBARCO ESCALERA & GALERÍA     | 17. VESTIDOR DE PASO SUITE (8,40 m²)  |
| ACÚSTICA P1 (8,20 m²)                 | • Módulos enfrentados de suelo a techo|
| [Pared Norte: MAMPARA 4+4 SILENCE]    | • Frentes de vidrio ahumado translúc. |
| • Vistas cenitales al Patio Corrala   | • Iluminación LED vertical integrada  |
| • Aislamiento acústico entre plantas  | • Paso directo entre baño y dormitorio|
| • Balizas nocturnas LED a h=25 cm     +---------------------------------------+
|---------------------------------------| 16. SUITE PRINCIPAL MATRIMONIO        |
| 13. DORMITORIO NIÑA (14,60 m²)        | (16,50 m² útiles)                     |
| • Cama 1,20 × 2,00 m cabecero tapizado| • Cama King Size 1,80 × 2,00 m Sur    |
| • Mesa estudio suspendida 1,80 m Este | • Mesillas flotantes integradas       |
| • Luz a 90° de balconera (cero reflej)| • Termostato digital independiente    |
| • Salida directa a Balcón Corrido Sur | • Balconera corredera 3,00 m a Balcón |
| • Armario empotrado suelo a techo     |                                       |
|---------------------------------------|                                       |
| 14. DORMITORIO NIÑO (14,60 m²)        |                                       |
| • Distribución gemela simétrica       |                                       |
| • Mesa estudio suspendida 1,80 m Este |                                       |
| • Salida directa a Balcón Corrido Sur |                                       |
+---------------------------------------+---------------------------------------+
| 19. BALCÓN CORRIDO SUR P1 (14,00 m² útiles · Fondo 1,40 m · Cota +3,15 m)     |
| • Tarima de Iroko sobre plots · Barandilla continua de vidrio 10+10 mm        |
+-------------------------------------------------------------------------------+
```

16. **12. DESEMBARCO DE ESCALERA Y GALERÍA ACÚSTICA (8,20 m² útiles):**
    * Coordenadas: $X \in [6,85; 12,50\text{ m}]$, $Y \in [8,40; 9,80\text{ m}]$.
    * **Mampara Acústica Continua de Vidrio Laminado `4+4 Silence`:** Cerramiento acristalado de suelo a techo ($4,00 \times 2,60\text{ m}$) que asoma sobre el vacío cenital del Patio Corrala inferior. Corta **$42\text{ dB}$ de ruido** entre la zona social de planta baja y la zona de descanso de planta primera, permitiendo una visión panorámica continua de la copa del *Acer palmatum*.
    * Iluminación: Balizas de cortesía empotradas en zócalo a $h=25\text{ cm}$ del suelo cada 1,5 metros con encendido crepuscular suave para trayectos nocturnos infantiles hacia los baños.
17. **13 y 14. DORMITORIOS INFANTILES (14,60 m² útiles cada uno · $3,80 \times 3,84\text{ m}$):**
    * Coordenadas Niña: $X \in [6,85; 10,65\text{ m}]$, $Y \in [9,90; 13,74\text{ m}]$.
    * Coordenadas Niño: $X \in [10,75; 14,55\text{ m}]$, $Y \in [9,90; 13,74\text{ m}]$.
    * **Pared Medianera Central (Divisoria entre ambos dormitorios):** Tabique ciego de alta masa acústica con doble placa Pladur Fonic a cada cara y lana mineral de 50 mm ($R_w \ge 50\text{ dB}$). **Cero huecos ni ventanas.**
    * **Pared Lateral Este:** Pared ciega donde apoya la **mesa de estudio suspendida de roble de $1,80 \times 0,65\text{ m}$**. Recibe la luz natural de la balconera sur lateralmente a 90° (ergonomía visual pura, sin contraluz ni reflejos en pantallas). Incluye canaleta con 3 tomas Schuko + 2 RJ45 Cat 6A + USB-C PD a $h=80\text{ cm}$.
    * **Fachada Sur (Única Pared Exterior):** Balconera corredera *Cortizo COR 80 RPT* ($2,20 \times 2,40\text{ m}$) con persiana motorizada de lamas orientables. Salida directa a cota cero al Balcón Corrido Sur.
    * Mobiliario: Cama de $1,20 \times 2,00\text{ m}$ con cabecero tapizado y armario empotrado de suelo a techo de $2,00\text{ m}$ de longitud en pared norte.
18. **15. BAÑO COMPARTIDO HIJOS (6,80 m² útiles · $3,80 \times 1,79\text{ m}$):**
    * Coordenadas interiores: $X \in [6,85; 10,65\text{ m}]$, $Y \in [6,50; 8,29\text{ m}]$.
    * Ventana Norte alta oscilobatiente traslúcida ($1,20 \times 0,60\text{ m}$, antepecho $h=160\text{ cm}$).
    * Doble seno cerámico integrado en mueble suspendido de roble de $1,40\text{ m}$ ($h=85\text{ cm}$) con grifería empotrada bimando y 2 tomas Schuko IP44.
    * Bañera/Ducha amplia encastrada de $1,70 \times 0,75\text{ m}$ con mampara de cristal de 8 mm antical.
    * Inodoro suspendido Geberit iCon Rimless con bajante insonorizada $\varnothing 110\text{ mm}$.
    * Radiador toallero hidráulico de 750W conectado al circuito de baja temperatura de la aerotermia. Extracción VMC $\varnothing 125\text{ mm}$ a $40\text{ m}^3/\text{h}$.
19. **16. MASTER SUITE PRINCIPAL DE MATRIMONIO (16,50 m² útiles · $4,30 \times 3,84\text{ m}$):**
    * Coordenadas interiores: $X \in [14,65; 18,95\text{ m}]$, $Y \in [9,90; 13,74\text{ m}]$.
    * Cama King Size ($1,80 \times 2,00\text{ m}$) centrada en pared norte con cabecero tapizado acústico y mesillas suspendidas integradas con interruptores conmutados, tomas USB-C y tomas Schuko a ambos lados ($h=65\text{ cm}$).
    * Fachada Sur: Gran balconera corredera *Cortizo Cor Vision* de 2 hojas ($3,00 \times 2,40\text{ m}$) abierta al Balcón Sur sobre el jardín privado y la piscina.
    * Climatización: Circuito de suelo radiante zonal con termostato táctil independiente a $h=145\text{ cm}$ e impulsión VMC $\varnothing 125\text{ mm}$ a $40\text{ m}^3/\text{h}$.
20. **17. VESTIDOR DE PASO DOBLE SUITE (8,40 m² útiles · $4,30 \times 1,95\text{ m}$):**
    * Coordenadas: $X \in [14,65; 18,95\text{ m}]$, $Y \in [7,85; 9,80\text{ m}]$.
    * Distribución: Dos hileras continuas de armarios de suelo a techo ($4,20\text{ m}$ de longitud cada una, fondo $60\text{ cm}$) con pasillo central libre de $1,10\text{ m}$.
    * Acabado: Frentes de vidrio ahumado translúcido con perfiles de aluminio negro mate, barras de colgar iluminadas con perfiles LED verticales continuos integrados en cremalleras de regulación.
21. **18. BAÑO PRIVADO SUITE (6,30 m² útiles · $4,30 \times 1,46\text{ m}$):**
    * Coordenadas interiores: $X \in [14,65; 18,95\text{ m}]$, $Y \in [6,30; 7,76\text{ m}]$.
    * Ventana Norte alta oscilobatiente traslúcida ($1,40 \times 0,60\text{ m}$).
    * Mueble suspendido doble seno en Dekton Kelya ($1,60 \times 0,50\text{ m}$) con dos lavabos integrados y grifería empotrada mural en negro mate. Espejo retroiluminado antivaho con sensor táctil.
    * Ducha Italiana Doble ($1,50 \times 0,90\text{ m}$): Enrasada a cota cero con sumidero lineal oculto inox AISI 316 y dos rociadores de techo independientes con griferías termostáticas dobles.
    * Inodoro suspendido Geberit con pulsador DuoFresh.
    * Toallero eléctrico programable de 750W en pared este. Extracción VMC forzada $\varnothing 125\text{ mm}$ a $40\text{ m}^3/\text{h}$.
22. **19. BALCÓN CORRIDO SUR P1 (14,00 m² útiles · $10,00 \times 1,40\text{ m}$):**
    * Coordenadas: $X \in [8,50; 18,50\text{ m}]$, $Y \in [13,85; 15,25\text{ m}]$. Cota: $+3,15\text{ m}$.
    * Estructura: Vuelo del forjado de hormigón armado de planta primera sobre el porche de PB.
    * Pavimento: Tarima de Iroko macizo a cota cero con las habitaciones, apoyada sobre plots regulables y lámina impermeabilizante bicapa con pendiente del 1,5% hacia gárgolas de desagüe ocultas.
    * Barandilla: Barandilla continua de **vidrio estructural laminar templado $10+10.2\text{ mm}$** sin montantes verticales, embutida en perfil de aluminio empotrado en el canto del forjado (altura reglamentaria $1,10\text{ m}$).

---

## 4. TABLA MAESTRA DE CARPINTERÍAS Y HUECOS DE FACHADA

| Código | Ubicación | Tipo Apertura | Ancho × Alto (m) | Antepecho ($h$) | Serie Carpintería | Vidrio (Composición) | Protección Solar |
|---|---|---|---|---|---|---|---|
| **C-01** | Porche Norte | Pivotante Eje Despl. | 1,00 × 2,40 | 0 cm (Cota +0,05) | Iroko Macizo Aislado | Puerta opaca Ud=1,1 | Alero Porche |
| **C-02** | Mudroom / Pérgola | Batiente 1 Hoja | 0,90 × 2,10 | 0 cm (Cota -0,10) | Cortizo COR 80 RPT | 4+4 / 16Ar / 4 Guardian | Guillotina suelo |
| **C-03** | Despacho Norte | Oscilobatiente | 1,80 × 1,20 | 95 cm | Cortizo COR 80 RPT | 4+4Sil / 16Ar / 4 / 16Ar / 4 | Persiana motorizada |
| **C-04** | Baño PB Norte | Oscilobatiente Alta | 0,80 × 0,60 | 160 cm | Cortizo COR 80 RPT | 4+4 / 16Ar / 4 Carglass | Vidrio traslúcido |
| **C-05** | Hall / Patio Claustro | Fijo Suelo-Techo | 2,80 × 2,60 | 0 cm (Cota ±0,00) | Cortizo Cor Vision Plus | 6T / 16Ar / 4 / 16Ar / 4+4.2 | Patio resguardado |
| **C-06** | Cocina / Patio | Corredera Elevable 2H| 3,00 × 2,60 | 0 cm (Cota ±0,00) | Cortizo Cor Vision Plus | 6T / 16Ar / 4 / 16Ar / 4+4.2 | Alero patio 80cm |
| **C-07** | Salón / Porche Sur | Corredera Elevable 3H| 5,00 × 2,60 | 0 cm (Cota ±0,00) | Cortizo Cor Vision Plus | 6T / 16Ar / 4 / 16Ar / 4+4.2 | Porche 3m + Screen 1% |
| **C-08** | Comedor / Porche Sur | Corredera Elevable 2H| 3,50 × 2,60 | 0 cm (Cota ±0,00) | Cortizo Cor Vision Plus | 6T / 16Ar / 4 / 16Ar / 4+4.2 | Porche 3m + Screen 1% |
| **C-09** | Trastero Exterior | Batiente Chapa Acero | 0,90 × 2,05 | 0 cm | Chapa Galvanizada Lacada | Opaca reforzada | Alero pérgola |
| **C-10** | Baño Hijos P1 | Oscilobatiente Alta | 1,20 × 0,60 | 160 cm | Cortizo COR 80 RPT | 4+4 / 16Ar / 4 Carglass | Vidrio traslúcido |
| **C-11** | Baño Suite P1 | Oscilobatiente Alta | 1,40 × 0,60 | 160 cm | Cortizo COR 80 RPT | 4+4 / 16Ar / 4 Carglass | Vidrio traslúcido |
| **C-12** | Dorm. Niña / Balcón | Balconera Corredera | 2,20 × 2,40 | 0 cm (Cota +3,15) | Cortizo COR 80 RPT | 4+4Sil / 16Ar / 4 Guardian | Persiana motorizada |
| **C-13** | Dorm. Niño / Balcón | Balconera Corredera | 2,20 × 2,40 | 0 cm (Cota +3,15) | Cortizo COR 80 RPT | 4+4Sil / 16Ar / 4 Guardian | Persiana motorizada |
| **C-14** | Suite / Balcón Sur | Balconera Corredera | 3,00 × 2,40 | 0 cm (Cota +3,15) | Cortizo Cor Vision | 6T / 16Ar / 4 / 16Ar / 4+4.2 | Persiana motorizada |
| **C-15** | Galería P1 / Patio | Fijo Acústico Silence | 4,00 × 2,60 | 0 cm (Cota +3,15) | Perfilería Oculta | Laminado acústico 4+4 Silence| Interior |

---

## 5. INGENIERÍA DE INSTALACIONES (PUNTO A PUNTO)

### 5.1. Electricidad y Telecomunicaciones (REBT / ICT)
* **Acometida y Cuadros:**
  * CGMP en Hall PB: IGA 40A + Protector sobretensiones permanentes y transitorias tipo 1+2.
  * Línea individual dedicada para Wallbox VE ($3 \times 10\text{ mm}^2$, PIA 32A).
  * Cuadro secundario P1 con diferenciales clase A superinmunizados.
* **Mecanismos por Estancia:**
  * **Zaguán:** 2 Schuko 16A ($h=30\text{ cm}$) + detector PIR techo.
  * **Hall:** 2 Schuko 16A ($h=30\text{ cm}$) + pulsadores conmutados ($h=105\text{ cm}$) + Pantalla domótica 7" ($h=145\text{ cm}$).
  * **Despacho:** 4 Schuko + 2 RJ45 Cat 6A + USB-C PD en mesa ($h=75\text{ cm}$) + 2 Schuko perimetrales ($h=30\text{ cm}$) + termostato ($h=145\text{ cm}$).
  * **Baños:** 2 Schuko IP44 junto a lavabo ($h=110\text{ cm}$) con diferencial dedicado de 10 mA.
  * **Cocina:**
    * Circuito C3: Toma 25A placa Bora Pure ($h=30\text{ cm}$).
    * Circuito C4: 4 Schukos desayunador ($h=110\text{ cm}$) + Schuko horno ($h=80\text{ cm}$) + Schuko microondas ($h=130\text{ cm}$) + Schuko lavavajillas ($h=40\text{ cm}$) + Schuko frigo ($h=40\text{ cm}$).
    * Isla: Torre retráctil con 2 Schuko + USB-C.
  * **Salón:** 6 Schuko 16A + 2 RJ45 Cat 6A blindados tras TV ($h=35\text{ cm}$) + 4 Schuko perimetrales para lámparas.
  * **Comedor:** 2 Schuko en aparador ($h=90\text{ cm}$) + línea suspendida DALI regulable.
  * **Dormitorios Infantiles:** 3 Schuko + 2 RJ45 Cat 6A en mesa de estudio ($h=80\text{ cm}$) + 2 Schuko junto a cama ($h=65\text{ cm}$) + termostatos.
  * **Suite:** 2 Schuko + USB-C a cada lado de cama ($h=65\text{ cm}$) + 2 Schuko en vestidor + termostato.
  * **Porche Exterior:** 2 Schuko estancos IP66 en churrasqueira + 2 Schuko IP66 en zona lounge.

### 5.2. Fontanería y Saneamiento (CTE DB-HS4 / DB-HS5)
* **Red de Fontanería:** Colectores de distribución en polietileno reticulado (PEX-a) con aislamiento térmico elastomérico de $13\text{ mm}$ en tuberías de ACS para evitar pérdidas térmicas. Llaves de corte independientes por cuarto húmedo.
* **Red de Saneamiento:**
  * Bajantes insonorizadas minerales *Geberit Silent-PP* de $\varnothing 110\text{ mm}$ fijadas con abrazaderas isofónicas de goma desolarizadas de la estructura.
  * Colectores horizontales colgados bajo forjado sanitario con pendiente mínima constante del 2,0%.
  * Evacuación separativa: Aguas pluviales (cubiertas, patio y porches) canalizadas independientemente hacia arqueta de infiltración / red municipal; aguas residuales conducidas a red de saneamiento.
  * Sifones secos de membrana en desagües de condensados (aerotermia, VMC y caseta de piscina) para bloqueo permanente de olores.

### 5.3. Climatización y Ventilación Passivhaus (CTE DB-HS3 / DB-HE)
* **Unidad VMC Zehnder ComfoAir Q350:**
  * Conductos circulares de PE-HD *ComfoTube $\varnothing 90\text{ mm}$* aislados acústicamente con silenciadores de impulsión y retorno.
  * Caudales nominales de impulsión (aire nuevo filtrado): Despacho ($35\text{ m}^3/\text{h}$), Salón ($60\text{ m}^3/\text{h}$), Comedor ($40\text{ m}^3/\text{h}$), Dormitorios infantiles ($30\text{ m}^3/\text{h}$ cada uno), Suite ($40\text{ m}^3/\text{h}$).
  * Caudales nominales de extracción (aire viciado húmedo): Cocina ($50\text{ m}^3/\text{h}$), Lavandería ($30\text{ m}^3/\text{h}$), Baño PB ($50\text{ m}^3/\text{h}$), Baño hijos P1 ($40\text{ m}^3/\text{h}$), Baño suite P1 ($40\text{ m}^3/\text{h}$), Mudroom ($30\text{ m}^3/\text{h}$).
* **Suelo Radiante-Refrescante:**
  * Placa de nódulos de poliestireno extruido (XPS) de $30\text{ mm}$ de alta densidad ($35\text{ kg/m}^3$) con lámina de barrera de vapor termosoldada.
  * Tubería PEX-a de $\varnothing 16\text{ mm}$ con barrera antidifusión de oxígeno (EVOH). Paso de tubo de $10\text{ cm}$ en baños y perímetros de ventanales; paso de $15\text{ cm}$ en estancias generales.
  * Regulación mediante cabezales electrotérmicos a 24V gobernados por termostatos táctiles digitales zonales independientes.

---

## 6. COMPATIBILIDAD CONSTRUCTIVA Y CRITERIOS PARA EL CONSTRUCTOR

1. **Estanqueidad al Gas Radón (CTE DB-HS6 - Zona II Oleiros):**
   * Es preceptiva la instalación de una lámina elastomérica anti-radón continua certificada (espesor $\ge 2,0\text{ mm}$, coeficiente de difusión $\le 10^{-11}\text{ m}^2/\text{s}$) colocada directamente bajo la solera de hormigón, con solapes de $15\text{ cm}$ termosoldados con soplete y sellado estanco hermético en todos los pasos de tuberías y pasamuros.
2. **Eliminación de Puentes Térmicos en Enrasados Cota Cero:**
   * En todas las carpinterías correderas a cota cero (Patio Corrala y Porche Sur), el perfil de aluminio se asienta sobre taco de rotura de puente térmico de poliestireno de alta densidad (*Purenit* de $50\text{ mm}$), garantizando la continuidad del aislamiento entre la solera interior y el exterior sin condensaciones bajo el marco.
3. **Chimenea y Ventilación Mecánica:**
   * Queda estrictamente prohibida la instalación de hogares abiertos o chimeneas atmosféricas. El hogar debe ser estanco certificado clase BlowerDoor ($n_{50} < 1,0\text{ h}^{-1}$) con su propia toma de aire exterior canalizada.
4. **Independencia Acústica de Dormitorios Infantiles:**
   * El tabique medianero entre los dos dormitorios no admite cajas de mecanismos eléctricos enfrentadas; las tomas de corriente y datos de ambas habitaciones se desplazarán un mínimo de $30\text{ cm}$ en horizontal para preservar el aislamiento acústico de $50\text{ dB}$.

---
*Fin del documento maestro de persistencia agéntica de la Propuesta D.*
