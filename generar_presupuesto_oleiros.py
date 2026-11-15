import csv
import json

def build_budget():
    # Parámetros físicos de la vivienda Propuesta D
    sup_cerrada = 215.00 # m2 construidos cerrados (PB: 116.50 m2 + P1: 98.50 m2)
    sup_porches_balcon = 53.50 # m2 (Porche Sur 36 m2 + Porche Norte 3.5 m2 + Balcón P1 14 m2)
    sup_equiv_construida = sup_cerrada + (sup_porches_balcon * 0.5) # 241.75 m2
    sup_parcela = 600.00 # m2 (20x30m en Liáns / Santa Cruz)
    sup_patio_corrala = 16.00 # m2
    sup_piscina = 26.25 # m2 (7.5 x 3.5 m)
    
    # Escenarios:
    # 1. Estándar / Funcional
    # 2. Calidad Media-Alta
    # 3. Propuesta D Premium Passivhaus (Especificación real del proyecto)

    scenarios = {
        "Estandar": {
            "nombre": "1. Estándar / Funcional",
            "terreno": 140000.0,
            "coste_m2_contrata": 1500.0, # Incluye PEM + GG (13%) + BI (6%)
            "cierres_parcela": 12000.0,
            "cocina_electro": 14000.0,
            "piscina": 0.0, # No incluida
            "honorarios_pct": 0.10,
            "imprevistos_pct": 0.05
        },
        "Media_Alta": {
            "nombre": "2. Calidad Media-Alta",
            "terreno": 160000.0,
            "coste_m2_contrata": 1800.0, # Incluye PEM + GG (13%) + BI (6%)
            "cierres_parcela": 16500.0,
            "cocina_electro": 20000.0,
            "piscina": 22000.0,
            "honorarios_pct": 0.11,
            "imprevistos_pct": 0.07
        },
        "Propuesta_D_Premium": {
            "nombre": "3. Propuesta D Consolidada (Premium Passivhaus)",
            "terreno": 175000.0,
            "coste_m2_contrata": 2100.0, # Cortizo minimalista, SATE 12cm+Granito gallego, Zehnder Q350, Vaillant aroTHERM, etc.
            "cierres_parcela": 21000.0, # Muro zócalo granito + cerrajería lamas + portón auto + riego Hunter
            "cocina_electro": 28000.0, # Santos Fine + Dekton + Bora Pure + Siemens/Bosch Serie 8
            "piscina": 26500.0, # 7.5x3.5m gunitada, porcelánico C3, clorador salino, LED
            "honorarios_pct": 0.115,
            "imprevistos_pct": 0.08
        }
    }

    results = {}

    for s_key, s in scenarios.items():
        # A. TERRENO Y ADQUISICIÓN
        p_suelo = s["terreno"]
        itp_suelo = p_suelo * 0.10 # ITP Galicia 10%
        notaria_registro_suelo = 2200.0
        tasacion_suelo = 450.0
        total_suelo = p_suelo + itp_suelo + notaria_registro_suelo + tasacion_suelo

        # B. ESTUDIOS PREVIOS
        topografico = 750.0
        geotecnico = 1600.0 if s_key == "Propuesta_D_Premium" else 1300.0 # Sondeo roca granítica Oleiros
        iva_estudios = (topografico + geotecnico) * 0.21
        total_estudios = topografico + geotecnico + iva_estudios

        # C. EJECUCIÓN MATERIAL Y CONTRATA DE VIVIENDA
        # Base de contrata (Edificación cerrada + porches + patio + instalaciones integradas)
        contrata_edificacion = sup_equiv_construida * s["coste_m2_contrata"]
        pem_estimado = contrata_edificacion / 1.19 # Descontando 13% GG y 6% BI
        gg_bi = contrata_edificacion - pem_estimado

        # Partidas exteriores y complementarias
        cierres = s["cierres_parcela"]
        cocina = s["cocina_electro"]
        piscina = s["piscina"]
        total_partidas_complementarias = cierres + cocina + piscina

        # Total base imponible constructora / contratas
        base_imponible_obras = contrata_edificacion + total_partidas_complementarias
        iva_obras = base_imponible_obras * 0.10 # IVA reducido 10% autopromoción vivienda habitual

        # D. HONORARIOS TÉCNICOS Y DIRECCIÓN FACULTATIVA
        # Calculados sobre PEM
        honorarios_tecnicos = pem_estimado * s["honorarios_pct"]
        coordinacion_seguridad_ensayos = 3200.0
        total_tecnicos_neto = honorarios_tecnicos + coordinacion_seguridad_ensayos
        iva_tecnicos = total_tecnicos_neto * 0.21

        # E. TASAS E IMPUESTOS MUNICIPALES (CONCELLO DE OLEIROS)
        # ICIO en Oleiros: 4% sobre PEM oficial
        # Tasa urbanística de obras: ~1.3% sobre PEM
        # Fianza de gestión de residuos y aceras (reembolsable al finalizar): ~4.000 €
        icio_oleiros = pem_estimado * 0.04
        tasa_obras_oleiros = pem_estimado * 0.013
        total_impuestos_oleiros = icio_oleiros + tasa_obras_oleiros
        fianza_residuos_reembolsable = 4000.0

        # F. ACOMETIDAS DE SERVICIOS
        acometidas_neto = 4500.0 # Luz (UFD), Agua (Concello Oleiros), Fibra óptica
        iva_acometidas = acometidas_neto * 0.21
        total_acometidas = acometidas_neto + iva_acometidas

        # G. GASTOS NOTARIALES, REGISTRALES Y JURÍDICOS DE OBRA NUEVA
        notaria_registro_obra = 3000.0
        ajd_obra_nueva = base_imponible_obras * 0.015 # AJD Galicia 1.5%
        fin_de_obra_registro = 1800.0
        total_juridico_obra = notaria_registro_obra + ajd_obra_nueva + fin_de_obra_registro

        # H. COLCHÓN DE IMPREVISTOS / CONTINGENCIAS
        imprevistos = base_imponible_obras * s["imprevistos_pct"]

        # TOTAL LLAVE EN MANO
        total_inversion = (
            total_suelo +
            total_estudios +
            base_imponible_obras +
            iva_obras +
            total_tecnicos_neto +
            iva_tecnicos +
            total_impuestos_oleiros +
            total_acometidas +
            total_juridico_obra +
            imprevistos
        )

        results[s_key] = {
            "nombre": s["nombre"],
            "suelo_compra": p_suelo,
            "itp_gastos_suelo": itp_suelo + notaria_registro_suelo + tasacion_suelo,
            "total_suelo": total_suelo,
            "estudios_previos": total_estudios,
            "pem_estimado": pem_estimado,
            "gg_bi": gg_bi,
            "contrata_edificacion": contrata_edificacion,
            "cierres_jardin": cierres,
            "cocina_equipada": cocina,
            "piscina": piscina,
            "total_obras_neto": base_imponible_obras,
            "iva_obras_10": iva_obras,
            "honorarios_tecnicos_neto": total_tecnicos_neto,
            "iva_honorarios_21": iva_tecnicos,
            "tasas_concello_oleiros": total_impuestos_oleiros,
            "fianza_reembolsable": fianza_residuos_reembolsable,
            "acometidas_definitivas": total_acometidas,
            "notaria_registro_ajd": total_juridico_obra,
            "colchon_imprevistos": imprevistos,
            "TOTAL_INVERSION": total_inversion
        }

    # Desglose del PEM por Capítulos Constructivos (Estándar COAG / Aparejadores) para Propuesta D
    # Base PEM Propuesta D = results["Propuesta_D_Premium"]["pem_estimado"]
    pem_d = results["Propuesta_D_Premium"]["pem_estimado"]
    capitulos_pem_d = [
        ("Cap. 01 Actuaciones Previas y Movimiento de Tierras (con contingencia roca granítica)", 0.052, "Desbroce, excavación caciada, vaciado, picado de bolos graníticos y retirada a vertedero RCD"),
        ("Cap. 02 Cimentación y Solera Sanitaria Cáviti Anti-Radón (CTE DB-HS6)", 0.088, "Zapatas, zunchos, solera ventilada Cáviti 50cm, lámina antirradón continua PEAD 1,5mm y arquetas"),
        ("Cap. 03 Estructura Portante (Hormigón Armado + Acero)", 0.145, "Pilares HA-25, vigas planas/descuelgue, forjados unidireccionales bovedilla hormigón y losas"),
        ("Cap. 04 Fachadas y Envolvente Térmica (SATE 12cm + Mampostería Granito Moreno)", 0.138, "SATE EPS grafito 12cm blanco + chapado granito moreno gallego de 12cm con anclajes inox"),
        ("Cap. 05 Cubiertas Planas Invertidas y Balcón Sur", 0.062, "Impermeabilización bicapa SBS soldada, aislamiento XPS 14cm, geotextil, grava y tarima balcón"),
        ("Cap. 06 Carpintería Exterior de Alta Eficiencia (Cortizo COR 80 + Cor Vision Plus)", 0.135, "Grandes correderas elevables enrasadas cota cero, triple vidrio con gas argón y lamas motorizadas"),
        ("Cap. 07 Particiones Interiores y Aislamiento Acústico (Pladur Silence)", 0.058, "Pladur doble placa 15+15 con lana de roca 60mm, tabiques acústicos Rw>=50dB y puertas isofónicas"),
        ("Cap. 08 Revestimientos y Acabados Interiores (Roble Macizo + Porcelánicos)", 0.075, "Falsos techos continuos con foseados LED, tarima multicapa de roble 14mm y porcelánico rectificado"),
        ("Cap. 09 Fontanería, Red de Saneamiento y Sanitarios de Gama Alta", 0.048, "Red PEX multicapa, bajantes Geberit Silent-PP insonorizadas, inodoros Geberit Rimless suspendidos"),
        ("Cap. 10 Climatización (Vaillant aroTHERM + Uponor) y VMC (Zehnder Q350)", 0.085, "Aerotermia bomba de calor, suelo radiante/refrescante zonal y ventilación doble flujo con recuperación"),
        ("Cap. 11 Electricidad, Iluminación LED Regulable y Telecomunicaciones Cat 6A", 0.054, "CGMP zonificado, mecanismos Schneider Elegance, red datos Cat 6A 10Gbps a cada puesto y LED 2700K"),
        ("Cap. 12 Energía Solar Fotovoltaica (12 paneles 5,4 kWp + Inversor Híbrido)", 0.018, "Paneles monocristalinos en cubierta baja Oeste, inversor híbrido monofásico y protecciones"),
        ("Cap. 13 Patio Corrala Central y Porche Sur (Iroko cota cero + Churrasqueira)", 0.027, "Tarima de Iroko con clips inox ocultos, canaletas inox AISI 316 y barbacoa de granito de obra"),
        ("Cap. 14 Pinturas Ecológicas y Tratamientos Especiales de Madera", 0.015, "Pintura al silicato transpirable lavable y lasur hidrófugo en maderas exteriores"),
        ("Cap. 15 Seguridad y Salud + Gestión Ambiental de Residuos", 0.010, "Protecciones colectivas, líneas de vida provisionales y contenedor RCD autorizado")
    ]

    return results, capitulos_pem_d, pem_d

if __name__ == "__main__":
    results, capitulos_pem_d, pem_d = build_budget()
    
    # Exportar CSV completo
    with open("presupuesto_autopromocion_oleiros.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["CAPÍTULO / PARTIDA", "1. ESTÁNDAR (€)", "2. MEDIA-ALTA (€)", "3. PROPUESTA D PREMIUM (€)", "OBSERVACIONES / TIPO IMPOSITIVO"])
        
        items = [
            ("A. TERRENO Y COMPRAVENTA (OLEIROS)", "", "", "", "Parcela residencial ~600 m² (PXOM 2B Liáns/Santa Cruz)"),
            ("1. Precio del suelo / Parcela neta", "suelo_compra", "suelo_compra", "suelo_compra", "Solar urbano consolidado"),
            ("2. Impuestos compra suelo (ITP Galicia 10%) + Notaría y Registro", "itp_gastos_suelo", "itp_gastos_suelo", "itp_gastos_suelo", "ITP 10% + Escritura Notarial + Registro de la Propiedad"),
            ("SUBTOTAL TERRENO ADQUIRIDO Y ESCRITURADO", "total_suelo", "total_suelo", "total_suelo", "Suelo en propiedad a nombre del autopromotor"),
            ("B. ESTUDIOS PREVIOS Y GEOTÉCNICO", "estudios_previos", "estudios_previos", "estudios_previos", "Topográfico + Geotécnico con sondeo roca granítica e IVA 21%"),
            ("C. EJECUCIÓN MATERIAL Y CONTRATA VIVIENDA", "", "", "", "215 m² cerrados + 53,5 m² exteriores cubiertos"),
            ("1. Presupuesto de Ejecución Material (PEM base)", "pem_estimado", "pem_estimado", "pem_estimado", "Coste directo de materiales y mano de obra"),
            ("2. Gastos Generales (13%) y Beneficio Industrial (6%)", "gg_bi", "gg_bi", "gg_bi", "Margen empresarial legal constructora (19%)"),
            ("3. Contrata Edificación completa (Clima, VMC, etc.)", "contrata_edificacion", "contrata_edificacion", "contrata_edificacion", "Edificación cerrada e instalaciones terminadas"),
            ("4. Cierres de parcela y Urbanización exterior", "cierres_jardin", "cierres_jardin", "cierres_jardin", "Muro zócalo granito + cancelas + césped y riego"),
            ("5. Cocina amueblada y equipada", "cocina_equipada", "cocina_equipada", "cocina_equipada", "Santos Fine + Dekton + Bora + gama alta Siemens/Bosch"),
            ("6. Piscina privada y solárium", "piscina", "piscina", "piscina", "Vaso gunitado 7,5x3,5m, porcelánico, cloración salina"),
            ("TOTAL CONTRATA DE OBRAS NETA (Base Imponible)", "total_obras_neto", "total_obras_neto", "total_obras_neto", "Facturación total de contratas"),
            ("7. IVA Reducido de Autopromoción (10%)", "iva_obras_10", "iva_obras_10", "iva_obras_10", "Ley del IVA (vivienda habitual autopromotor)"),
            ("D. HONORARIOS TÉCNICOS Y DIRECCIÓN FACULTATIVA", "honorarios_tecnicos_neto", "honorarios_tecnicos_neto", "honorarios_tecnicos_neto", "Arquitecto (PBE + DO) + Aparejador (DEO + CSS)"),
            ("1. IVA Honorarios Facultativos (21%)", "iva_honorarios_21", "iva_honorarios_21", "iva_honorarios_21", "IVA general servicios profesionales"),
            ("E. LICENCIAS Y TASAS CONCELLO DE OLEIROS", "tasas_concello_oleiros", "tasas_concello_oleiros", "tasas_concello_oleiros", "ICIO 4% + Tasa municipal de obras ~1,3%"),
            ("Fianza de residuos RCD y aceras (Reembolsable)", "fianza_reembolsable", "fianza_reembolsable", "fianza_reembolsable", "Depósito municipal devuelto al fin de obra"),
            ("F. ACOMETIDAS DE SERVICIOS (Luz, Agua, Datos)", "acometidas_definitivas", "acometidas_definitivas", "acometidas_definitivas", "Acometidas UFD, Concello Oleiros e IVA 21%"),
            ("G. NOTARÍA, REGISTRO Y AJD OBRA NUEVA", "notaria_registro_ajd", "notaria_registro_ajd", "notaria_registro_ajd", "Declaración Obra Nueva, AJD Galicia 1,5%, Fin de Obra"),
            ("H. COLCHÓN DE IMPREVISTOS / CONTINGENCIAS", "colchon_imprevistos", "colchon_imprevistos", "colchon_imprevistos", "5% a 8% sobre base imponible de obras"),
            ("TOTAL INVERSIÓN LLAVE EN MANO (€)", "TOTAL_INVERSION", "TOTAL_INVERSION", "TOTAL_INVERSION", "Coste real completo de inicio a fin")
        ]

        def fmt(val):
            return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

        for row in items:
            label = row[0]
            if row[1] == "":
                writer.writerow([label, "", "", "", row[4]])
            else:
                c1 = fmt(results["Estandar"][row[1]])
                c2 = fmt(results["Media_Alta"][row[2]])
                c3 = fmt(results["Propuesta_D_Premium"][row[3]])
                writer.writerow([label, c1, c2, c3, row[4]])

    print("Archivo presupuesto_autopromocion_oleiros.csv generado con éxito.")
    for k, v in results.items():
        print(f"-> {v['nombre']}: {v['TOTAL_INVERSION']:,.2f} €")
