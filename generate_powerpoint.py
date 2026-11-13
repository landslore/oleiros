#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Presentación PowerPoint (.pptx) Definitiva para Mac (Keynote & PowerPoint).
Presenta la Propuesta D de la Vivienda en Oleiros estancia por estancia con sus renders fotorrealistas corregidos.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Brand Colors
    BG_DARK = RGBColor(11, 15, 25)       # #0b0f19
    CARD_BG = RGBColor(22, 30, 46)       # #161e2e
    ACCENT_SKY = RGBColor(56, 189, 248)  # #38bdf8
    ACCENT_GOLD = RGBColor(245, 158, 11) # #f59e0b
    ACCENT_GREEN = RGBColor(16, 185, 129)# #10b981
    TEXT_LIGHT = RGBColor(248, 250, 252) # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184) # #94a3b8

    renders_dir = "/home/antigravity/landslore/oleiros/propuestas/renders"

    def set_slide_background(slide, color=BG_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category="PROYECTO OLEIROS · PROPUESTA D", subtitle=None):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Helvetica"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_SKY

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Helvetica"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

        if subtitle:
            p_sub = tf_title.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Helvetica"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_room_slide(title, category, subtitle, img_name, points, badge_color=ACCENT_SKY):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide)
        add_header(slide, title, category, subtitle)

        img_path = os.path.join(renders_dir, img_name)
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(0.8), Inches(1.7), width=Inches(7.2), height=Inches(5.2))

        box = slide.shapes.add_textbox(Inches(8.3), Inches(1.7), Inches(4.2), Inches(5.2))
        tf = box.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = "Claves de Diseño & Aparejador:\n"
        p_h.font.bold = True
        p_h.font.size = Pt(13)
        p_h.font.color.rgb = badge_color

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(10.5)
            p_pt.font.color.rgb = TEXT_LIGHT

    # 1. PORTADA
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)
    img_portada = os.path.join(renders_dir, "fachada_norte_render.jpg")
    if os.path.exists(img_portada):
        s1.shapes.add_picture(img_portada, Inches(6.0), Inches(0.75), width=Inches(6.8), height=Inches(6.0))

    left_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.0), Inches(4.5))
    tf1 = left_box.text_frame
    tf1.word_wrap = True
    p0 = tf1.paragraphs[0]
    p0.text = "PROYECTO DE EJECUCIÓN · VIVIENDA UNIFAMILIAR"
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = ACCENT_SKY
    p1 = tf1.add_paragraph()
    p1.text = "Hogar Oleiros\nPropuesta D"
    p1.font.bold = True
    p1.font.size = Pt(36)
    p1.font.color.rgb = TEXT_LIGHT
    p2 = tf1.add_paragraph()
    p2.text = "Pabellón Bioclimático en Liáns / Santa Cruz\nConcello de Oleiros (A Coruña)"
    p2.font.size = Pt(13)
    p2.font.color.rgb = ACCENT_GOLD
    p3 = tf1.add_paragraph()
    p3.text = "\n• Parcela: 600 m² (Ordenanza 2B, PGOM Oleiros)\n• Ocupación PB: 116,5 m² (19,4% ≤ 20,0% legal)\n• Patio Corrala Central: 16,0 m² habitable y accesible\n• Presupuesto Llave en Mano: 662.980 €"
    p3.font.size = Pt(11)
    p3.font.color.rgb = TEXT_MUTED

    # 2. FACHADA NORTE Y ACCESO
    add_room_slide(
        "Acceso Principal & Fachada Norte",
        "PLANTA BAJA · EXTERIORES",
        "Doble acceso peatonal cubierto y aparcamiento bajo pérgola",
        "fachada_norte_render.jpg",
        [
            "Porche cubierto de entrada noble con puerta pivotante de iroko macizo (1,10 m).",
            "Pérgola de aparcamiento para 2 coches al Oeste con paso a cubierto.",
            "Conexión directa desde el aparcamiento al Zaguán Mudroom.",
            "Zócalo de granito gallego del país y carpintería minimalista Cortizo negro forja."
        ],
        ACCENT_SKY
    )

    # 3. ZAGUÁN MUDROOM
    add_room_slide(
        "01. Zaguán Atlántico / Mudroom Térmico",
        "PLANTA BAJA · ENTRADA DIARIA",
        "5,80 m² útiles · Esclusa térmica de doble barrera contra lluvia y viento",
        "zaguan_mudroom_render.jpg",
        [
            "Banco descalzador de roble macizo con zapatero ventilado para 16 pares.",
            "Armario secador de ropa de lluvia con bandeja de inox para goteo.",
            "Puerta corredera de vidrio estriado hacia el Hall noble.",
            "Puerta de servicio directa hacia el Trastero de Surf y Bicis.",
            "Pavimento porcelánico C3 antideslizante gris pizarra (NCS S 4502-Y)."
        ],
        ACCENT_GOLD
    )

    # 4. HALL RECIBIDOR
    add_room_slide(
        "02. Hall / Recibidor Principal",
        "PLANTA BAJA · RECEPCIÓN",
        "10,40 m² útiles · Conexión visual directa con el claustro ajardinado",
        "hall_recibidor_render.jpg",
        [
            "En cuanto se cruza la puerta, la mirada se fuga al arce japonés del Patio.",
            "Cristalera fija de suelo a techo Cortizo Cor Vision Plus hacia el patio.",
            "Consola suspendida de roble tostado con espejo circular retroiluminado LED.",
            "Armario gabanero empotrado para abrigos de visitas.",
            "Pantalla táctil domótica central para control de clima, persianas y portero."
        ],
        ACCENT_SKY
    )

    # 5. PATIO CORRALA CENTRAL (EL CORAZÓN)
    add_room_slide(
        "05. Patio Corrala Habitable y Accesible",
        "PLANTA BAJA · EL CORAZÓN DE LA CASA",
        "16,00 m² libres · Abierto al cielo · Microclima resguardado del Nordés",
        "patio_corrala_render.jpg",
        [
            "100% Habitable y pisable: Enrasado a cota cero con tarima de iroko.",
            "Arce japonés (Acer palmatum) plantado en alcorque natural con grava volcánica.",
            "Banco corrido de lectura bajo alero perimetral cubierto de 80 cm.",
            "Triple corredera elevable abriendo a Cocina (3m), Salón (3m) y Galería (2,5m).",
            "Cero efecto invernadero: Abierto al cielo, evita condensaciones y ahorra ~26.500 €."
        ],
        ACCENT_GREEN
    )

    # 6. COCINA CON ISLA
    add_room_slide(
        "06. Cocina con Isla y Desayunador",
        "PLANTA BAJA · ZONA DE DÍA",
        "15,20 m² útiles · Isla Dekton Kelya con campana integrada Bora Pure",
        "cocina_isla_render.jpg",
        [
            "Isla central de 2,80 × 1,00 m con pasos libres de 105 cm a ambos lados.",
            "Placa Bora Pure con extracción hacia abajo: techo 100% limpio sin campanas.",
            "Mueble desayunador con puertas escamoteables y enchufes ocultos.",
            "Columnas Santos Fine en cashmere mate y roble humo.",
            "Conexión directa mediante corredera de 3 m al Patio Corrala para desayunos al sol."
        ],
        ACCENT_GOLD
    )

    # 7. SALÓN PRINCIPAL Y JARDÍN SUR
    add_room_slide(
        "08. Salón Principal con Chimenea",
        "PLANTA BAJA · ZONA DE DÍA",
        "26,50 m² útiles · Abierto al Porche Sur, piscina y jardín",
        "salon_jardin_render.jpg",
        [
            "Sofá modular en L tapizado en arena a 3,60 m de la pantalla.",
            "Chimenea panorámica estanca de leña con toma de aire exterior (compatible VMC).",
            "Gran corredera Cortizo Cor Vision de 5 m abierta de par en par al Porche Sur.",
            "Vistas continuas al césped atlántico, hortensias y piscina sin barreras.",
            "Suelo continuo de piedra caliza con suelo radiante-refrescante zonificado."
        ],
        ACCENT_SKY
    )

    # 8. DESPACHO SANCTASANCTÓRUM
    add_room_slide(
        "03. Despacho Sanctasanctórum & Suite Serena",
        "PLANTA BAJA · TELETRABAJO & INVITADOS",
        "11,50 m² útiles · Doble orientación Norte-Sur · Cero servidumbre",
        "despacho_render.jpg",
        [
            "Mesa orientada con luz lateral a 90° de ventana Norte (cero reflejos en monitor).",
            "Cristalera con vistas relajantes al arce del Patio Claustro.",
            "Aislamiento acústico Rw ≥ 38 dB con puerta maciza y panel de lamas de roble.",
            "Doble toma RJ45 Cat 6A blindada en escritorio para videollamadas 4K.",
            "Sofá-cama de matrimonio (140 × 200 cm) con acceso privado al Baño PB."
        ],
        ACCENT_GREEN
    )

    # 9. BAÑO COMPLETO PB
    add_room_slide(
        "04. Baño Completo PB & Distribuidor Neutro",
        "PLANTA BAJA · ZONA NOBLE",
        "5,20 m² útiles · Ducha walk-in cota cero y sanitarios Geberit",
        "bano_pb_render.jpg",
        [
            "Acceso desde distribuidor neutro: sin paso directo a cocina (100% legal NHG).",
            "Ducha walk-in enrasada cota cero (120 × 80 cm) con mampara fija de 8 mm antical.",
            "Mueble suspendido de roble de 90 cm con grifería empotrada negra mate.",
            "Inodoro suspendido Geberit iCon Rimless con pulsador antiolores DuoFresh.",
            "Ventana practicable a fachada Norte para iluminación y ventilación natural."
        ],
        ACCENT_SKY
    )

    # 10. PORCHE SUR CUBIERTO & PISCINA
    add_room_slide(
        "10. Porche Sur Expandido (Fondo 3,00 m)",
        "PLANTA BAJA · EXTERIORES",
        "36,00 m² cubiertos · Churrasqueira de granito y comedor de verano",
        "porche_sur_render.jpg",
        [
            "Fondo libre real de 3,00 m: protegido de la lluvia gallega para comer fuera.",
            "Churrasqueira en extremo Este con bancada de granito Zimbabwe y leñera.",
            "Comedor exterior para 10 personas + zona lounge frente al jardín.",
            "Piscina de 3,5 × 7,5 m con albardilla de granito calizo y solárium.",
            "Armario lateral integrado con salida directa para robot cortacésped."
        ],
        ACCENT_GOLD
    )

    # 11. GALERÍA ACÚSTICA Y ESCALERA P1
    add_room_slide(
        "12. Galería Acústica & Escalera P1",
        "PLANTA PRIMERA · DISTRIBUIDOR",
        "8,20 m² útiles · Mampara acústica continua de vidrio 4+4 Silence",
        "galeria_escalera_render.jpg",
        [
            "Mampara de vidrio laminar 4+4 Silence: aísla 42 dB de ruido entre plantas.",
            "Peldaños volados de roble macizo con zanca de acero oculta e iluminación LED.",
            "Vistas cenitales espectaculares sobre el patio claustral y el arce.",
            "Balizas LED de cortesía en zócalo (h = 25 cm) para trayectos nocturnos infantiles."
        ],
        ACCENT_SKY
    )

    # 12. SUITE PRINCIPAL MATRIMONIO
    add_room_slide(
        "16. Suite Principal de Matrimonio",
        "PLANTA PRIMERA · ALA ESTE PRIVADA",
        "31,20 m² útiles · Dormitorio Sur, vestidor doble y baño privado",
        "suite_principal_render.jpg",
        [
            "Cama King Size (1,80 × 2,00 m) orientada al Sur con vistas panorámicas al jardín.",
            "Balcón corrido con barandilla continua de vidrio estructural 10+10 mm sin montantes.",
            "Vestidor de paso en doble hilera con frentes de vidrio ahumado y barras LED.",
            "Baño privado de 6,3 m² con ducha italiana doble (150 × 90 cm) y doble seno Dekton.",
            "Climatización dual independiente con suelo radiante zonal y toallero de 750W."
        ],
        ACCENT_GREEN
    )

    # 13. DORMITORIOS INFANTILES
    add_room_slide(
        "13-14. Dormitorios Infantiles (Luz a 90°)",
        "PLANTA PRIMERA · ALA OESTE",
        "14,60 m² útiles cada uno · Estudio ergonómico sin reflejos y balcón sur",
        "dormitorio_infantil_render.jpg",
        [
            "Mesa de estudio suspendida de 1,80 m apoyada en pared lateral con luz a 90°.",
            "Cero reflejos en pantalla de portátil y cero contraluz.",
            "Cama de 120 × 200 cm con cabecero tapizado y armario empotrado de suelo a techo.",
            "Salida directa a Balcón Corrido Sur con carpintería Cortizo COR 80 RPT.",
            "Aislamiento acústico medianero reforzado Rw ≥ 50 dB entre dormitorios."
        ],
        ACCENT_SKY
    )

    # 14. RESUMEN TÉCNICO Y PRESUPUESTO
    s_end = prs.slides.add_slide(blank_layout)
    set_slide_background(s_end)
    add_header(s_end, "Instalaciones, Eficiencia A y Presupuesto Llave en Mano", "INGENIERÍA & PRESUPUESTO", "Transparencia económica rigurosa y estándar Passivhaus")

    cards_data = [
        ("🌡️ Climatización & ACS", "• Aerotermia Vaillant aroTHERM plus\n• Suelo radiante-refrescante bajo porcelánico/madera\n• Depósito ACS 250L + recirculación\n• Control digital zonal por estancia"),
        ("🌬️ Ventilación VMC Doble Flujo", "• Unidad Zehnder ComfoAir Q350\n• Recuperador entálpico de calor (92% eficiencia)\n• Filtros F7 polen/partículas y G4 olores\n• Aire filtrado continuo sin abrir ventanas"),
        ("🛡️ Radón & Estanqueidad", "• Membrana anti-radón bajo solera (Zona II CTE DB-HS6)\n• Envolvente térmica continua SATE + lana de roca\n• Hermeticidad BlowerDoor n50 < 1,0 h⁻¹\n• Carpinterías Cortizo Cor Vision Plus"),
        ("⚡ Fotovoltaica & Telecomunicaciones", "• 12 paneles solares monocristalinos 450W (5,4 kWp)\n• Inversor híbrido 5 kW preparado para baterías\n• Red estructurada cableada Cat 6A (10 Gbps)\n• Rack mural 19\" 9U + Wi-Fi 7 PoE")
    ]

    for i, (t, c) in enumerate(cards_data):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.3)

        card = s_end.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_GOLD

        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = t
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = ACCENT_GOLD

        p_c = tf.add_paragraph()
        p_c.text = c
        p_c.font.size = Pt(10.5)
        p_c.font.color.rgb = TEXT_LIGHT

    sum_box = s_end.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5))
    tf_sum = sum_box.text_frame
    p_sum = tf_sum.paragraphs[0]
    p_sum.text = "PRESUPUESTO TOTAL LLAVE EN MANO: 662.980 € (PEM: 418.000 € · Gastos y Beneficio: 79.420 € · IVA 10%: 49.742 € · Técnicos y Tasas: 115.818 €)"
    p_sum.font.bold = True
    p_sum.font.size = Pt(10)
    p_sum.font.color.rgb = ACCENT_GREEN

    # Save
    out_path = "/home/antigravity/landslore/oleiros/propuestas/Presentacion_Hogar_Oleiros_Propuesta_D.pptx"
    prs.save(out_path)
    print(f"Deck saved: {out_path} ({os.path.getsize(out_path)} bytes)")

    artifact_pptx = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7/Presentacion_Hogar_Oleiros_Propuesta_D.pptx"
    prs.save(artifact_pptx)
    print(f"Artifact saved: {artifact_pptx} ({os.path.getsize(artifact_pptx)} bytes)")

if __name__ == "__main__":
    create_deck()
