#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Presentación PowerPoint (.pptx) para Mac (Keynote & PowerPoint).
Presenta la Propuesta D de la Vivienda en Oleiros con planos definitivos, renders fotorrealistas y fichas técnicas.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen (13.333 x 7.5 inches)
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
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Helvetica"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_SKY

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Helvetica"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

        if subtitle:
            p_sub = tf_title.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Helvetica"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 1: PORTADA
    # ═════════════════════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_DARK)

    # Hero Image on right
    img_portada = os.path.join(renders_dir, "fachada_norte_render.jpg")
    if os.path.exists(img_portada):
        s1.shapes.add_picture(img_portada, Inches(6.0), Inches(0.75), width=Inches(6.8), height=Inches(6.0))

    # Left content box
    left_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.0), Inches(4.5))
    tf1 = left_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "PROYECTO DE EJECUCIÓN · VIVIENDA UNIFAMILIAR"
    p0.font.name = "Helvetica"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_SKY

    p1 = tf1.add_paragraph()
    p1.text = "Hogar Oleiros\nPropuesta D"
    p1.font.name = "Helvetica"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Pabellón Bioclimático en Liáns / Santa Cruz\nConcello de Oleiros (A Coruña)"
    p2.font.name = "Helvetica"
    p2.font.size = Pt(14)
    p2.font.color.rgb = ACCENT_GOLD

    p3 = tf1.add_paragraph()
    p3.text = "\n• Parcela: 600 m² (Ordenanza 2B, PGOM Oleiros)\n• Ocupación PB: 116,5 m² (19,4% ≤ 20,0% legal)\n• Patio Corrala Central: 16,0 m² habitable y accesible\n• Presupuesto Llave en Mano: 662.980 €"
    p3.font.name = "Helvetica"
    p3.font.size = Pt(11)
    p3.font.color.rgb = TEXT_MUTED

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 2: CRITERIOS RECTORES DE LA PROPUESTA D
    # ═════════════════════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Criterios Rectores del Rediseño Integral", "ESTRATEGIA ARQUITECTÓNICA & BIOCLIMÁTICA", "Respuesta a la auditoría técnica y necesidades de la familia")

    pillars = [
        ("🍁 1. Patio Corrala Habitable (Opción A)", "El patio central de 16,0 m² está 100% abierto al cielo con drenaje natural sobre terreno real. Se pisa a cota cero con tarima de iroko y alberga un arce japonés palmatum. Tres correderas elevables lo fusionan con la cocina y el salón."),
        ("🚗 2. Doble Acceso Funcional", "Acceso diario protegido bajo techo: de la pérgola de coches directamente al Zaguán Mudroom (secador de lluvia, banco descalzador, acceso a bicis y compras). Acceso noble para visitas por el Porche Norte con puerta pivotante de 1,10 m hacia el Hall."),
        ("💼 3. Despacho Sanctasanctórum", "Puesto de teletrabajo de alta concentración con doble orientación: ventana Norte con luz difusa sin reflejos y gran ventanal al patio. Cero servidumbre de paso hacia la cocina y puerta acústica (Rw ≥ 38 dB)."),
        ("🌿 4. Porche Sur Expandido (Fondo 3 m)", "Superamos los 2,00 m estrechos de iteraciones previas alcanzando 3,00 m libres de fondo. Alberga comedor exterior para 10 plazas, churrasqueira de granito y zona lounge frente a la piscina.")
    ]

    for i, (title, desc) in enumerate(pillars):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(2.0 + row * 2.5)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_SKY

        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Helvetica"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_SKY

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Helvetica"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 3: PATIO CORRALA (EL CORAZÓN)
    # ═════════════════════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "05. Patio Corrala Habitable y 100% Accesible", "EL CORAZÓN DE LA CASA", "16,00 m² útiles · Abierto al cielo · Microclima protegido de los vientos atlánticos")

    img_patio = os.path.join(renders_dir, "patio_corrala_render.jpg")
    if os.path.exists(img_patio):
        s3.shapes.add_picture(img_patio, Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(5.0))

    box_p = s3.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(5.0))
    tf_p = box_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "Evolución de la Iteración:\n"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GOLD

    points = [
        "100% Habitable y pisable: Enrasado al milímetro a cota cero con tarima de madera tecnológica.",
        "Arce Japonés (Acer palmatum): Plantado en alcorque natural profundo con grava volcánica y helechos.",
        "Banco de lectura perimetral: Fabricado en iroko macizo bajo el alero continuo de 80 cm.",
        "Triple corredera elevable Cortizo Cor Vision Plus: Abre 3 m hacia Cocina, 3 m hacia Salón y 2,5 m hacia Galería.",
        "Cero efecto invernadero: Abierto al cielo, evita condensaciones y ahorra ~26.500 € frente a lucernarios motorizados.",
        "Cumplimiento 100% PGOM: No computa como superficie cubierta cerrada (ocupación PB = 116,5 m² ≤ 120 m²)."
    ]
    for pt in points:
        p_pt = tf_p.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 4: ESPACIO DE DÍA INTEGRADO (SALÓN, COCINA, COMEDOR)
    # ═════════════════════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "06-08. Zona de Día Integrada y Porche Sur", "SALÓN CON CHIMENEA · COMEDOR · COCINA CON ISLA", "Continuidad visual y espacial con doble orientación (Patio Norte y Porche Sur)")

    img_living = os.path.join(renders_dir, "interior_living_render.jpg")
    if os.path.exists(img_living):
        s4.shapes.add_picture(img_living, Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(5.0))

    box_l = s4.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(5.0))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Detalles Técnicos y de Interiorismo:\n"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_SKY

    points_l = [
        "Isla Dekton Kelya (2,80 × 1,00 m): Con placa de inducción y extracción hacia abajo Bora Pure (techo despejado).",
        "Mueble desayunador escamoteable: Frente de 120 cm con puertas que se ocultan en los laterales y tomas de fuerza.",
        "Mesa noble de roble para 10 comensales: Pasos libres de circulación de 95 cm hacia la cristalera del porche.",
        "Salón con chimenea estanca: Hogar cerrado con toma de aire exterior dedicada (compatible al 100% con VMC Zehnder).",
        "TV OLED 77\" empotrada a paño: Tubo pasacables oculto Ø 50 mm al mueble suspendido (cero cables visibles).",
        "Suelo continuo de piedra caliza (120 × 120 cm): Pavimento noble con suelo radiante-refrescante zonificado."
    ]
    for pt in points_l:
        p_pt = tf_l.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 5: DESPACHO SANCTASANCTÓRUM
    # ═════════════════════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "03. Despacho Sanctasanctórum & Suite Serena", "TELETRABAJO ERGONÓMICO & SUITE DE INVITADOS", "11,50 m² útiles · Doble orientación Norte-Sur · Cero servidumbre a cocina")

    img_desp = os.path.join(renders_dir, "despacho_render.jpg")
    if os.path.exists(img_desp):
        s5.shapes.add_picture(img_desp, Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(5.0))

    box_d = s5.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(5.0))
    tf_d = box_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "Configuración Acústica y Lumínica:\n"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GREEN

    points_d = [
        "Principio ergonómico a 90°: Luz natural difusa de fachada Norte entrando lateralmente al monitor (cero reflejos).",
        "Vistas relajantes al Patio: Cristalera hacia el arce japonés para pausas visuales durante jornadas intensivas.",
        "Acústica de estudio (Rw ≥ 38 dB): Puerta batiente maciza con guillotina de cierre automático y panel de lamas de roble sobre fieltro fonoabsorbente negro.",
        "Red Cat 6A (10 Gbps): Doble toma blindada en escritorio para videollamadas 4K y streaming profesional sin latencia.",
        "Suite de invitados: Sofá-cama italiano (colchón 140 × 200 cm) con acceso privado al distribuidor y Baño PB.",
        "Climatización y VMC: Impulsión silenciosa de 45 m³/h de aire nuevo filtrado y termostato digital táctil independiente."
    ]
    for pt in points_d:
        p_pt = tf_d.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 6: PORCHE SUR CUBIERTO & JARDÍN
    # ═════════════════════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "10. Porche Sur Cubierto Expandido (Fondo 3,00 m)", "ESPACIO EXTERIOR CUBIERTO PROTEGIDO DE LA LLUVIA", "36,00 m² cubiertos · Churrasqueira de granito · Comedor de verano · Piscina")

    img_porche = os.path.join(renders_dir, "porche_sur_render.jpg")
    if os.path.exists(img_porche):
        s6.shapes.add_picture(img_porche, Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(5.0))

    box_po = s6.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(5.0))
    tf_po = box_po.text_frame
    tf_po.word_wrap = True
    p = tf_po.paragraphs[0]
    p.text = "Equipamiento de Ocio Exterior:\n"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_GOLD

    points_po = [
        "Fondo real de 3,00 m: Permite comer fuera incluso con orballo gallego sin mojar mesas ni sillas.",
        "Churrasqueira en extremo Este: Bancada de granito negro Zimbabwe abujardado con parrilla de inox AISI 316 y leñera ventilada.",
        "Fregadero exterior auxiliar: Con agua fría y caliente sanitaria para limpieza sin entrar a la cocina.",
        "Armario robot cortacésped en extremo Oeste: Con compuerta a ras de suelo para salida autónoma del robot.",
        "Piscina integrada: Lámina de agua de 3,5 × 7,5 m con albardilla perimetral de granito calizo y solárium de madera.",
        "Punto de acceso Wi-Fi 7 exterior IP65: Máxima cobertura en porche, césped y piscina."
    ]
    for pt in points_po:
        p_pt = tf_po.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 7: SUITE PRINCIPAL MATRIMONIO
    # ═════════════════════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "16. Suite Principal de Matrimonio (Ala Este P1)", "DORMITORIO SUR · VESTIDOR EN DOBLE HILERA · BAÑO PRIVADO", "31,20 m² útiles · Privacidad total · Balcón corrido con barandilla de vidrio estructural")

    img_suite = os.path.join(renders_dir, "suite_principal_render.jpg")
    if os.path.exists(img_suite):
        s7.shapes.add_picture(img_suite, Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(5.0))

    box_s = s7.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(5.0))
    tf_s = box_s.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "Distribución y Acabados de Lujo:\n"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_SKY

    points_s = [
        "Cama King Size (1,80 × 2,00 m): Orientada al Sur con vistas panorámicas al jardín desde la almohada.",
        "Barandilla de vidrio estructural 10+10 mm: Embutida en la testa del forjado sin montantes metálicos verticales.",
        "Vestidor de paso (8,4 m²): Doble hilera de armarios con frentes de vidrio ahumado, barras iluminadas por LED y pasillo central libre de 110 cm.",
        "Baño privado de 6,3 m²: Ducha italiana doble (150 × 90 cm) con rociador Raindance Hansgrohe y lavabo de doble seno Dekton.",
        "Cabina de inodoro semi-independiente: Con puerta de vidrio al ácido para privacidad higiénica.",
        "Climatización dual: Suelo radiante independiente en dormitorio y baño + toallero eléctrico de diseño 750W."
    ]
    for pt in points_s:
        p_pt = tf_s.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_LIGHT

    # ═════════════════════════════════════════════════════════════════════════════
    # SLIDE 8: INSTALACIONES, EFICIENCIA & PRESUPUESTO
    # ═════════════════════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Instalaciones, Eficiencia A y Presupuesto Llave en Mano", "INGENIERÍA & PRESUPUESTO DE EJECUCIÓN", "Transparencia económica rigurosa y estándar Passivhaus")

    cards_data = [
        ("🌡️ Climatización & ACS", "• Aerotermia Vaillant aroTHERM plus\n• Suelo radiante-refrescante bajo porcelánico/madera\n• Depósito ACS 250L + recirculación\n• Control digital zonal por estancia"),
        ("🌬️ Ventilación VMC Doble Flujo", "• Unidad Zehnder ComfoAir Q350\n• Recuperador entálpico de calor (92% eficiencia)\n• Filtros F7 polen/partículas y G4 olores\n• Aire filtrado continuo sin abrir ventanas"),
        ("🛡️ Radón & Estanqueidad", "• Membrana anti-radón bajo solera (Zona II CTE DB-HS6)\n• Envolvente térmica continua SATE + lana de roca\n• Hermeticidad BlowerDoor n50 < 1,0 h⁻¹\n• Carpinterías Cortizo Cor Vision Plus"),
        ("⚡ Fotovoltaica & Telecomunicaciones", "• 12 paneles solares monocristalinos 450W (5,4 kWp)\n• Inversor híbrido 5 kW preparado para baterías\n• Red estructurada cableada Cat 6A (10 Gbps)\n• Rack mural 19\" 9U + Wi-Fi 7 PoE")
    ]

    for i, (title, content) in enumerate(cards_data):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(2.0 + row * 2.2)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_GOLD

        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Helvetica"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_GOLD

        p_c = tf.add_paragraph()
        p_c.text = content
        p_c.font.name = "Helvetica"
        p_c.font.size = Pt(10.5)
        p_c.font.color.rgb = TEXT_LIGHT

    # Bottom summary box
    sum_box = s8.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.6))
    tf_sum = sum_box.text_frame
    p_sum = tf_sum.paragraphs[0]
    p_sum.text = "PRESUPUESTO TOTAL LLAVE EN MANO: 662.980 € (PEM: 418.000 € · Gastos Generales y Beneficio: 79.420 € · IVA 10%: 49.742 € · Técnicos y Licencias Concello de Oleiros: 115.818 €)"
    p_sum.font.name = "Helvetica"
    p_sum.font.size = Pt(10.5)
    p_sum.font.bold = True
    p_sum.font.color.rgb = ACCENT_GREEN

    # Save PPTX
    out_path = "/home/antigravity/landslore/oleiros/propuestas/Presentacion_Hogar_Oleiros_Propuesta_D.pptx"
    prs.save(out_path)
    print(f"Presentation saved: {out_path} ({os.path.getsize(out_path)} bytes)")

    # Copy to artifacts directory
    artifact_pptx = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7/Presentacion_Hogar_Oleiros_Propuesta_D.pptx"
    prs.save(artifact_pptx)
    print(f"Artifact presentation saved: {artifact_pptx} ({os.path.getsize(artifact_pptx)} bytes)")

if __name__ == "__main__":
    create_deck()
