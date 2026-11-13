#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Visor Interactivo Zoom-In 1:20 con Planos CAD SVG para todas las estancias de Propuesta D.
"""

import json
import os

ROOMS = [
    {
        "id": "r01", "fl": "PB", "num": "01", "short": "01. Zaguán Mudroom",
        "title": "01. Zaguán Atlántico / Mudroom Térmico",
        "w": 1.50, "h": 3.85, "area": "5,80 m² útiles", "dims": "1,50 × 3,85 m · h = 2,65 m",
        "desc": "Conexión directa bajo alero desde la pérgola de coches. Esclusa térmica de doble barrera con banco descalzador, zapatero ventilado y armario secador de ropa de lluvia.",
        "wN": "Muro exterior Norte (35 cm) con armario empotrado y zapatero.",
        "wS": "Puerta corredera hacia el Trastero de Surf / Sala Técnica (descarga de compras/neoprenos).",
        "wE": "Tabique interior con puerta corredera de vidrio estriado hacia el Hall noble.",
        "wW": "Muro exterior Oeste con la puerta de acceso directo desde la Pérgola de aparcamiento.",
        "openings": [
            {"wall": "W", "pos": 2.20, "len": 0.90, "type": "door", "label": "Puerta Pérgola"},
            {"wall": "E", "pos": 2.00, "len": 0.90, "type": "sliding", "label": "Puerta Vidrio a Hall"},
            {"wall": "S", "pos": 0.30, "len": 0.85, "type": "sliding", "label": "A Trastero"}
        ],
        "furn": [
            {"code": "M1", "name": "Banco descalzador de roble (1,20 × 0,45 m)", "x": 0.15, "y": 0.20, "w": 1.20, "h": 0.45, "col": "#78350f", "str": "#d97706", "desc": "Asiento a h = 45 cm en roble macizo con tratamiento hidrófugo."},
            {"code": "M2", "name": "Zapatero inferior ventilado (16 pares)", "x": 0.15, "y": 0.70, "w": 1.20, "h": 0.40, "col": "#1e293b", "str": "#475569", "desc": "Bandejas extraíbles con rejilla de ventilación conectada a la extracción VMC."},
            {"code": "M3", "name": "Armario ropa lluvia y paraguas", "x": 0.15, "y": 1.20, "w": 1.20, "h": 0.60, "col": "#334155", "str": "#64748b", "desc": "Armario con barra a h = 170 cm y bandeja de inox para goteo de paraguas/botas."}
        ],
        "elec": [
            {"code": "E1", "name": "Enchufe 16A secador de calzado", "x": 0.10, "y": 0.60, "h_cm": 30, "cir": "C2", "desc": "Para conectar calentadores/secadores de botas de agua o calzado deportivo."},
            {"code": "E2", "name": "Enchufe servicio general", "x": 0.10, "y": 3.40, "h_cm": 30, "cir": "C2", "desc": "Para aspirador o lámpara auxiliar."},
            {"code": "E3", "name": "Enchufe interior armario", "x": 0.20, "y": 1.50, "h_cm": 110, "cir": "C2", "desc": "Toma interna en armario de abrigo para deshumidificador o recarga."}
        ],
        "sw": [
            {"code": "I1", "name": "Sensor de presencia microondas", "x": 0.75, "y": 1.90, "h_cm": 265, "cir": "C1", "desc": "Encendido automático de luz cálida indirecta al entrar desde la pérgola."},
            {"code": "I2", "name": "Conmutador noble Zaguán-Hall", "x": 1.40, "y": 2.00, "h_cm": 110, "cir": "C1", "desc": "Junto a la puerta de vidrio hacia el Hall."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante-Refrescante", "x": 0.75, "y": 2.50, "cir": "SR-PB-1", "isFloor": True, "desc": "Tubería multicapa paso 10 cm bajo porcelánico C3 antideslizante."},
            {"code": "VMC", "name": "Boca de Extracción Zehnder Ø 125 mm", "x": 0.75, "y": 1.20, "cir": "VMC-EXT", "isVMC": True, "desc": "Caudal continuo de 30 m³/h para evacuar humedad de ropa mojada y calzado."}
        ],
        "planning": [
            "Banco descalzador de 120 × 45 cm, altura de asiento ergonómica 45 cm.",
            "Zapatero ventilado con capacidad para 16 pares de uso diario.",
            "Armario secador de abrigos de 140 × 60 cm con bandeja inox inferior para botas mojadas.",
            "Pasillo central libre de 105 cm para paso holgado con niños o compras."
        ],
        "materials": "Suelo porcelánico C3 antideslizante gris pizarra (NCS S 4502-Y) · Paredes pintura blanco roto lavable (NCS S 0502-Y) · Roble macizo hidrófugo",
        "lighting": "150 lux general · Tira LED 2700K cálida bajo banco + foco empotrado cenital antideslumbramiento UGR < 16"
    },
    {
        "id": "r02", "fl": "PB", "num": "02", "short": "02. Hall Principal",
        "title": "02. Hall / Recibidor Principal",
        "w": 2.60, "h": 4.00, "area": "10,40 m² útiles", "dims": "2,60 × 4,00 m · h = 2,65 m",
        "desc": "Acceso noble para visitas desde el Porche Norte. En cuanto se cruza la puerta pivotante, la mirada se fuga hacia el arce del Patio Claustro a través de una gran cristalera de suelo a techo.",
        "wN": "Fachada Norte con la Puerta Principal pivotante de 1,10 m hacia el Porche Cubierto.",
        "wS": "Gran cristalera Cortizo Cor Vision Plus fija de suelo a techo hacia el Patio Claustro.",
        "wE": "Pared con armario gabanero y paso hacia el Despacho y la zona de día.",
        "wW": "Tabique interior con puerta corredera de vidrio estriado hacia el Zaguán Mudroom.",
        "openings": [
            {"wall": "N", "pos": 0.80, "len": 1.10, "type": "door", "label": "Puerta Principal (Visitas)"},
            {"wall": "S", "pos": 0.10, "len": 2.40, "type": "glass_fixed", "label": "Cristalera a Claustro"},
            {"wall": "W", "pos": 1.50, "len": 0.90, "type": "sliding", "label": "De Zaguán"}
        ],
        "furn": [
            {"code": "M1", "name": "Puerta pivotante iroko macizo (1,10 × 2,40 m)", "x": 0.80, "y": 0.05, "w": 1.10, "h": 0.15, "col": "#78350f", "str": "#b45309", "desc": "Puerta de seguridad pivotante con cerradura biométrica inteligente y tirador vertical inox negro."},
            {"code": "M2", "name": "Armario gabanero empotrado (1,20 × 0,60 m)", "x": 0.05, "y": 0.20, "w": 0.60, "h": 1.20, "col": "#334155", "str": "#64748b", "desc": "Armario enrasado en tabique con frentes lacados blanco mate y apertura push-pull."},
            {"code": "M3", "name": "Consola suspendida roble + Espejo Ø 80 cm", "x": 1.95, "y": 1.20, "w": 0.35, "h": 1.00, "col": "#d97706", "str": "#92400e", "desc": "Consola flotante a h = 85 cm con vaciabolsillos y espejo circular retroiluminado LED."}
        ],
        "elec": [
            {"code": "E1", "name": "Enchufe general junto a consola", "x": 2.50, "y": 1.10, "h_cm": 30, "cir": "C1", "desc": "Para lámpara decorativa de mesa o cargador."},
            {"code": "E2", "name": "Enchufe interior armario gabanero", "x": 0.10, "y": 0.80, "h_cm": 110, "cir": "C1", "desc": "Para estación de carga de llaves o domótica."},
            {"code": "RJ1", "name": "Toma doble RJ45 Cat 6A consola", "x": 2.50, "y": 2.30, "h_cm": 30, "cir": "RACK-PB", "isRJ": True, "desc": "Punto de red cableado para teléfono IP o repetidor domótico."},
            {"code": "DOM", "name": "Pantalla táctil domótica central", "x": 2.50, "y": 2.60, "h_cm": 150, "cir": "DOM", "desc": "Pantalla de 10\" para control de aerotermia, persianas, videoportero y fotovoltaica."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptor general Master apagado", "x": 0.70, "y": 0.20, "h_cm": 110, "cir": "C1", "desc": "Apagado general de toda la vivienda al salir de casa."},
            {"code": "I2", "name": "Conmutador foseado techo y consola", "x": 2.50, "y": 1.70, "h_cm": 110, "cir": "C1", "desc": "Regulación de luz cálida de bienvenida."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Hall", "x": 1.30, "y": 2.50, "cir": "SR-PB-2", "isFloor": True, "desc": "Pavimento porcelánico 120 × 120 cm acabado arena caliza (NCS S 1505-Y20R)."}
        ],
        "planning": [
            "Acceso noble con puerta pivotante de 110 cm en madera maciza de iroko.",
            "Fuga visual inmediata hacia el arce japonés del Patio Claustro.",
            "Armario gabanero integrado enrasado para visitas con apertura push-pull.",
            "Pantalla táctil domótica central a h = 150 cm junto al paso a zona de día."
        ],
        "materials": "Porcelánico rectificado 120 × 120 cm piedra caliza (NCS S 1505-Y20R) · Cortizo Cor Vision Plus negro forja · Roble tostado",
        "lighting": "100 lux ambiental + 250 lux acento consola · Foseado perimetral 2700K regulable + 2 focos antideslumbramiento 24°"
    },
    {
        "id": "r03", "fl": "PB", "num": "03", "short": "03. Despacho Sanctasanctórum",
        "title": "03. Despacho Sanctasanctórum & Suite Serena",
        "w": 3.50, "h": 3.30, "area": "11,50 m² útiles", "dims": "3,50 × 3,30 m · h = 2,65 m",
        "desc": "Espacio de teletrabajo intensivo de máxima concentración y suite privada de invitados. Doble orientación (ventana exterior Norte + cristalera a Patio Claustro Sur). Fin a la servidumbre de paso hacia la cocina.",
        "wN": "Fachada Norte con ventana practicable de 2,00 m (luz difusa sin reflejos y ventilación legal NHG).",
        "wS": "Cristalera panorámica de 2,60 m hacia el Patio Claustro ajardinado.",
        "wE": "Tabique interior con puerta corredera acústica hacia el distribuidor del Baño PB.",
        "wW": "Tabique interior con puerta batiente acústica maciza (Rw >= 38 dB) hacia el Hall.",
        "openings": [
            {"wall": "N", "pos": 0.75, "len": 2.00, "type": "window", "label": "Ventana Norte 2,00m (NHG)"},
            {"wall": "S", "pos": 0.45, "len": 2.60, "type": "glass_fixed", "label": "Ventanal a Patio Claustro"},
            {"wall": "W", "pos": 1.20, "len": 0.85, "type": "door", "label": "Puerta Acústica (Rw 38dB)"},
            {"wall": "E", "pos": 1.10, "len": 0.85, "type": "sliding", "label": "A Baño PB"}
        ],
        "furn": [
            {"code": "M1", "name": "Mesa teletrabajo ergonómica (1,80 × 0,80 m)", "x": 0.50, "y": 0.50, "w": 1.80, "h": 0.80, "col": "#1e293b", "str": "#38bdf8", "desc": "Mesa en roble natural a h = 74 cm con luz natural lateral indirecta a 90° (cero reflejos)."},
            {"code": "M2", "name": "Monitor Ultrawide 34\" + Docking USB-C", "x": 1.00, "y": 0.55, "w": 0.85, "h": 0.22, "col": "#0f172a", "str": "#38bdf8", "desc": "Brazo articulado con paso oculto de cables."},
            {"code": "M3", "name": "Silla ergonómica Herman Miller", "x": 1.15, "y": 1.45, "w": 0.55, "h": 0.55, "col": "#475569", "str": "#94a3b8", "desc": "Espacio de retroceso libre de 120 × 120 cm."},
            {"code": "M4", "name": "Sofá-cama matrimonio visitas (1,40 × 2,00 m)", "x": 2.60, "y": 0.80, "w": 0.80, "h": 1.80, "col": "#334155", "str": "#cbd5e1", "desc": "Apertura italiana con colchón de 140 × 200 cm grosor 16 cm para visitas familiares."},
            {"code": "TV", "name": "TV 43\" Smart TV empotrada", "x": 0.05, "y": 2.00, "w": 0.10, "h": 0.85, "col": "#0f172a", "str": "#ef4444", "desc": "En tabique Oeste a h = 115 cm para ver desde el sofá o cama de invitados."}
        ],
        "elec": [
            {"code": "E1", "name": "3× Enchufes 16A + 2× USB-C PD mesa", "x": 1.40, "y": 0.45, "h_cm": 80, "cir": "C2", "desc": "Sobre la mesa de teletrabajo para portátil, monitor y periféricos."},
            {"code": "RJ1", "name": "Doble Toma RJ45 Cat 6A (10 Gbps) mesa", "x": 1.80, "y": 0.45, "h_cm": 80, "cir": "RACK-PB", "isRJ": True, "desc": "Cableado blindado Cat 6A directo al Rack para videollamadas 4K sin retardo."},
            {"code": "E2", "name": "2× Enchufes + RJ45 tras TV 43\"", "x": 0.10, "y": 2.40, "h_cm": 115, "cir": "C2 + RACK", "isRJ": True, "desc": "Alimentación y toma de red oculta tras pantalla de TV."},
            {"code": "E3", "name": "Enchufe + USB-C mesilla sofá-cama", "x": 3.40, "y": 0.70, "h_cm": 65, "cir": "C2", "desc": "Para que los invitados carguen el teléfono desde la cama."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutador general + luz foseado", "x": 0.10, "y": 1.10, "h_cm": 110, "cir": "C1", "desc": "Junto a la puerta acústica del Hall."},
            {"code": "I2", "name": "Pulsador estor motorizado patio", "x": 0.30, "y": 3.20, "h_cm": 110, "cir": "C1", "desc": "Baja el estor screen para privacidad nocturna al dormir invitados."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Despacho", "x": 1.75, "y": 2.00, "cir": "SR-PB-3", "isFloor": True, "desc": "Climatización invisible sin radiadores en paredes."},
            {"code": "T", "name": "Termostato digital táctil independiente", "x": 0.10, "y": 1.30, "h_cm": 150, "cir": "CLIMA", "desc": "Control de temperatura independiente del resto de la casa."},
            {"code": "VMC", "name": "Boca Impulsión Zehnder Ø 125 mm", "x": 2.20, "y": 2.70, "cir": "VMC-IMP", "isVMC": True, "desc": "Aporte de 45 m³/h de aire puro filtrado F7 sin ruido."}
        ],
        "planning": [
            "Mesa orientada con luz lateral a 90°: elimina reflejos en monitor y deslumbramiento.",
            "Puerta acústica maciza Rw >= 38 dB con guillotina para aislamiento total.",
            "Sofá-cama de matrimonio apertura italiana con colchón de 140 × 200 cm.",
            "Acceso directo y exclusivo al distribuidor del Baño PB para visitas."
        ],
        "materials": "Panel acústico de lamas de roble sobre fieltro fonoabsorbente negro (αw = 0,85) en pared Oeste · Pintura mineral lino natural (NCS S 1005-Y20R)",
        "lighting": "500 lux en mesa + 300 lux vertical facial videollamadas · Perfil suspendido UGR < 19 Tunable White (4000K día / 2700K noche)"
    },
    {
        "id": "r04", "fl": "PB", "num": "04", "short": "04. Baño Completo PB",
        "title": "04. Baño Completo PB & Distribuidor Neutro",
        "w": 2.60, "h": 2.00, "area": "5,20 m² útiles", "dims": "2,60 × 2,00 m · h = 2,65 m",
        "desc": "Baño noble y completo con ducha walk-in, inodoro suspendido y lavabo en roble. Acceso desde distribuidor neutro: máxima intimidad, sin comunicación directa con la cocina (100% legal NHG).",
        "wN": "Fachada Norte con ventana practicable de ventilación e iluminación natural.",
        "wS": "Tabique interior con puerta batiente noble hacia el distribuidor de paso.",
        "wE": "Pared con patinillo de bajantes insonorizadas unificadas con la cocina y suite P1.",
        "wW": "Tabique interior acústico separador con el Despacho.",
        "openings": [
            {"wall": "N", "pos": 0.80, "len": 1.00, "type": "window", "label": "Ventana Norte"},
            {"wall": "S", "pos": 0.85, "len": 0.80, "type": "door", "label": "Puerta Baño"}
        ],
        "furn": [
            {"code": "M1", "name": "Ducha Walk-in enrasada cota cero (1,20 × 0,80 m)", "x": 1.30, "y": 0.10, "w": 1.20, "h": 0.80, "col": "#0284c7", "str": "#38bdf8", "desc": "Plato enrasado antideslizante con desagüe lineal inox y rociador termostático."},
            {"code": "M2", "name": "Mampara fija vidrio templado 8 mm antical", "x": 1.30, "y": 0.90, "w": 0.80, "h": 0.05, "col": "#bae6fd", "str": "#0284c7", "desc": "Mampara fija sin perfilería inferior para limpieza inmediata."},
            {"code": "M3", "name": "Mueble suspendido roble 90 cm + Lavabo", "x": 0.10, "y": 0.50, "w": 0.50, "h": 0.90, "col": "#f8fafc", "str": "#cbd5e1", "desc": "Dos cajones Blum de extracción total con grifería empotrada negra mate a h = 115 cm."},
            {"code": "M4", "name": "Inodoro suspendido Geberit iCon Rimless", "x": 0.80, "y": 0.10, "w": 0.40, "h": 0.55, "col": "#f8fafc", "str": "#94a3b8", "desc": "Cisterna empotrada Geberit Sigma 8 cm con pulsador DuoFresh antiolores."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes estancos IP44 lavabo", "x": 0.10, "y": 1.45, "h_cm": 115, "cir": "C5", "desc": "Junto al lavabo para afeitadora, cepillo de dientes o secador."},
            {"code": "TR", "name": "Radiador Toallero Eléctrico Negro 500W", "x": 0.10, "y": 1.70, "h_cm": 120, "cir": "C-TOALLERO", "desc": "Toallero programable de diseño de 120 × 50 cm para calentar y secar toallas."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptor general + Luz espejo LED", "x": 0.70, "y": 1.90, "h_cm": 110, "cir": "C1", "desc": "Junto a la puerta de entrada al baño."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Baño", "x": 1.30, "y": 1.40, "cir": "SR-PB-4", "isFloor": True, "desc": "Pavimento cálido al salir de la ducha."},
            {"code": "VMC", "name": "Boca Extracción Zehnder Ø 125 mm", "x": 2.20, "y": 0.50, "cir": "VMC-EXT", "isVMC": True, "desc": "Extracción continua de 45 m³/h para eliminar el vapor de la ducha al instante."}
        ],
        "planning": [
            "Ducha walk-in cota cero de 120 × 80 cm con mampara fija de 8 mm.",
            "Inodoro suspendido Geberit iCon Rimless con pulsador antiolores DuoFresh.",
            "Acceso desde distribuidor neutro con armario ropero para toallas.",
            "Ventana practicable en fachada Norte para luz y ventilación natural directa."
        ],
        "materials": "Porcelánico rectificado gran formato 120 × 260 cm piedra caliza gris sin juntas · Mueble roble natural · Grifería negro mate",
        "lighting": "300 lux general + 450 lux vertical en rostro sin sombras ante espejo retroiluminado antivaho"
    },
    {
        "id": "r05", "fl": "PB", "num": "05", "short": "05. Patio Corrala Habitable",
        "title": "05. Patio Corrala Habitable y Accesible",
        "w": 4.00, "h": 4.00, "area": "16,00 m² libres", "dims": "4,00 × 4,00 m · Cielo abierto",
        "desc": "El corazón habitable de la casa. Abierto al cielo con drenaje natural sobre terreno real. Tarima de madera tecnológica enrasada a cota cero, banco bajo alero, mesa de café y 3 correderas elevables que lo fusionan con la cocina y el salón.",
        "wN": "Ventanal acristalado fijo del Despacho Sanctasanctórum.",
        "wS": "Gran corredera elevable de 3,00 m que abre hacia el Salón-Comedor.",
        "wE": "Gran corredera elevable de 3,00 m que abre hacia la Cocina con Isla.",
        "wW": "Corredera elevable de 2,50 m que abre hacia la Galería y Escalera.",
        "openings": [
            {"wall": "W", "pos": 0.75, "len": 2.50, "type": "sliding", "label": "Corredera Galería 2,50m"},
            {"wall": "E", "pos": 0.50, "len": 3.00, "type": "sliding", "label": "Corredera Cocina 3,00m"},
            {"wall": "S", "pos": 0.50, "len": 3.00, "type": "sliding", "label": "Corredera Salón 3,00m"},
            {"wall": "N", "pos": 0.70, "len": 2.60, "type": "glass_fixed", "label": "Ventanal Despacho"}
        ],
        "furn": [
            {"code": "M1", "name": "Alcorque drenante + Arce Japonés", "x": 0.50, "y": 0.50, "w": 1.40, "h": 1.40, "col": "#065f46", "str": "#10b981", "desc": "Arce palmatum Atropurpureum plantado en tierra vegetal profunda con grava volcánica y helechos."},
            {"code": "M2", "name": "Banco corrido de lectura de Iroko", "x": 2.30, "y": 0.15, "w": 1.50, "h": 0.45, "col": "#b45309", "str": "#d97706", "desc": "Banco bajo alero perimetral cubierto de 80 cm para leer protegido de lloviznas."},
            {"code": "M3", "name": "Mesa de café exterior + 2 Sillones", "x": 2.30, "y": 2.20, "w": 1.20, "h": 1.20, "col": "#78350f", "str": "#b45309", "desc": "Mobiliario lounge de cuerda trenzada técnica resistente a salitre e intemperie."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes estancos IP66 bajo banco", "x": 2.50, "y": 0.10, "h_cm": 30, "cir": "C1", "desc": "Para iluminación decorativa exterior o portátil."}
        ],
        "sw": [
            {"code": "I1", "name": "Reloj astronómico crepuscular", "x": 3.80, "y": 2.00, "h_cm": 110, "cir": "DOM", "desc": "Encendido automático al caer la noche bañado el arce."}
        ],
        "hvac": [
            {"code": "RIEGO", "name": "Goteo inteligente Hunter Hydrawise", "x": 0.80, "y": 0.80, "cir": "RIEGO-1", "desc": "Tubería enterrada autocompensante conectada a previsión meteorológica."}
        ],
        "planning": [
            "100% habitable, accesible y pisable a cota cero con tarima tecnológica de exterior.",
            "3 puertas correderas elevables que lo abren a Salón, Cocina y Galería.",
            "Alero perimetral de 80 cm con banco corrido de iroko macizo.",
            "Alcorque drenante natural con arce japonés palmatum y helechos atlánticos."
        ],
        "materials": "Tarima tecnológica de madera enrasada a cota cero · Vidrio laminar bajo emisivo Cortizo Cor Vision Plus · Iroko macizo",
        "lighting": "3 proyectores de suelo empotrados IP67 cálidos 2700K bañando el árbol + tira LED perimetral oculta bajo banco"
    },
    {
        "id": "r06", "fl": "PB", "num": "06", "short": "06. Cocina con Isla",
        "title": "06. Cocina con Isla y Mueble Desayunador",
        "w": 3.80, "h": 4.00, "area": "15,20 m² útiles", "dims": "3,80 × 4,00 m · h = 2,65 m",
        "desc": "Espacio culinario de alta gama con isla Dekton de 2,80 m, placa Bora de extracción hacia abajo y mueble desayunador con puertas escamoteables. Conexión directa al patio corrala para desayunos al aire libre.",
        "wN": "Pared de separación con núcleo de baño y distribuidor.",
        "wS": "Paso abierto sin puertas hacia el Comedor Principal.",
        "wE": "Frente continuo de columnas Santos Fine (frigorífico XXL, congelador y horno vapor) + Desayunador.",
        "wW": "Gran cristalera corredera elevable de 3,00 m abierta al Patio Corrala.",
        "openings": [
            {"wall": "W", "pos": 0.50, "len": 3.00, "type": "sliding", "label": "Corredera al Patio 3,00m"},
            {"wall": "S", "pos": 0.50, "len": 2.80, "type": "open", "label": "Paso libre a Comedor"}
        ],
        "furn": [
            {"code": "ISLA", "name": "Isla central Dekton (2,80 × 1,00 m)", "x": 0.80, "y": 1.30, "w": 2.00, "h": 1.40, "col": "#334155", "str": "#38bdf8", "desc": "Bancada en Dekton 20 mm con pasos libres de 105 cm a ambos lados."},
            {"code": "BORA", "name": "Placa de inducción con extractor Bora Pure", "x": 1.00, "y": 1.50, "w": 0.80, "h": 0.50, "col": "#0f172a", "str": "#ef4444", "desc": "Absorción de humos en la propia encimera, dejando el techo 100% limpio."},
            {"code": "DESAY", "name": "Mueble desayunador escamoteable 120 cm", "x": 3.20, "y": 0.40, "w": 0.55, "h": 1.20, "col": "#fef3c7", "str": "#d97706", "desc": "Puertas escamoteables con cafetera, molinillo, tostadora y tomas ocultas."},
            {"code": "COLUM", "name": "Frente columnas Santos Fine (Roble humo)", "x": 3.20, "y": 1.70, "w": 0.55, "h": 2.10, "col": "#475569", "str": "#1e293b", "desc": "Frigo XXL integrable, congelador vertical independiente y hornos Bosch Serie 8."}
        ],
        "elec": [
            {"code": "E1", "name": "Torre retráctil Bachmann Twist en isla", "x": 2.60, "y": 1.50, "h_cm": 92, "cir": "C2", "desc": "2 tomas de corriente 16A + cargador USB-C integrados en la superficie Dekton."},
            {"code": "E2", "name": "4× Enchufes en Mueble Desayunador", "x": 3.25, "y": 0.90, "h_cm": 110, "cir": "C2", "desc": "Para cafetera espresso, molinillo de muelas, tostadora y hervidor."},
            {"code": "E3", "name": "Toma dedicada Vitrocerámica / Inducción 25A", "x": 1.40, "y": 1.50, "h_cm": 30, "cir": "C3", "desc": "Línea exclusiva de 6 mm² para la placa Bora."},
            {"code": "RJ1", "name": "Doble RJ45 Cat 6A lateral de isla", "x": 0.80, "y": 2.50, "h_cm": 75, "cir": "RACK-PB", "isRJ": True, "desc": "Para tablet de cocina o portátil mientras se trabaja en la isla."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutador cocina / carril isla", "x": 3.10, "y": 3.70, "h_cm": 110, "cir": "C1", "desc": "Junto al paso al comedor para encendido del carril de techo."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Cocina", "x": 1.80, "y": 2.00, "cir": "SR-PB-5", "isFloor": True, "desc": "Clima invisible con termostato digital zonal."},
            {"code": "VMC", "name": "Boca Extracción Zehnder Ø 125 mm", "x": 3.00, "y": 1.00, "cir": "VMC-EXT", "isVMC": True, "desc": "Extracción continua de 60 m³/h para renovar el aire sin abrir ventanas."}
        ],
        "planning": [
            "Isla central de 280 × 100 cm con pasos libres de 105 cm a ambos lados.",
            "Inducción con campana integrada Bora Pure: techo despejado y libre de humos.",
            "Mueble desayunador con puertas escamoteables de 120 cm.",
            "Conexión directa al patio corrala para desayunos al aire libre."
        ],
        "materials": "Dekton Kelya Cosentino 20 mm · Mobiliario Santos Fine Cashmere mate seda + roble humo · Perfiles empotrados Cortizo",
        "lighting": "600 lux de trabajo en encimera e isla · Carril magnético empotrado con 3 focos UGR < 16 + tira LED continua bajo muebles altos"
    },
    {
        "id": "r07", "fl": "PB", "num": "07", "short": "07. Lavandería y Cuarto Técnico",
        "title": "07. Lavandería y Cuarto Técnico Auxiliar",
        "w": 2.25, "h": 2.50, "area": "5,60 m² útiles", "dims": "2,25 × 2,50 m · h = 2,65 m",
        "desc": "Espacio de lavado, secado y plancha independiente, contiguo a la cocina y patinillo de aguas. Columna de lavado ergonómica, pila profunda de ropa y zona para aspirador vertical Dyson.",
        "wN": "Fachada exterior con ventana oscilobatiente.",
        "wS": "Tabique interior con puerta corredera acústica hacia la cocina.",
        "wE": "Pared con bancada de plegado y fregadero profundo de lencería.",
        "wW": "Pared con columna de lavadora y secadora sobre bancada fonoabsorbente.",
        "openings": [
            {"wall": "N", "pos": 0.60, "len": 0.90, "type": "window", "label": "Ventana Ventilación"},
            {"wall": "S", "pos": 0.70, "len": 0.85, "type": "door", "label": "Puerta a Cocina"}
        ],
        "furn": [
            {"code": "LAV", "name": "Lavadora Bosch Serie 6 (9 kg)", "x": 0.15, "y": 0.20, "w": 0.60, "h": 0.65, "col": "#f8fafc", "str": "#cbd5e1", "desc": "Lavadora con dosificación automática i-DOS montada en bancada a h = 40 cm."},
            {"code": "SEC", "name": "Secadora bomba de calor A+++ (9 kg)", "x": 0.15, "y": 0.90, "w": 0.60, "h": 0.65, "col": "#f8fafc", "str": "#cbd5e1", "desc": "Secadora en columna con bandeja extraíble intermedia para apoyar cestos de ropa."},
            {"code": "PILA", "name": "Pila de lavar ropa inox + Bancada plegado", "x": 1.50, "y": 0.20, "w": 0.60, "h": 1.40, "col": "#bae6fd", "str": "#0284c7", "desc": "Encimera sintética antibacteriana con fregadero profundo y grifo monomando extensible."},
            {"code": "ARM", "name": "Armario plancha + soporte Dyson con carga", "x": 1.50, "y": 1.70, "w": 0.60, "h": 0.70, "col": "#334155", "str": "#64748b", "desc": "Alojamiento vertical para tabla de planchar abatible y base de carga de aspirador."}
        ],
        "elec": [
            {"code": "E1", "name": "Toma dedicada Lavadora 16A", "x": 0.10, "y": 0.50, "h_cm": 110, "cir": "C4", "desc": "Línea independiente de 16A con toma de tierra reforzada."},
            {"code": "E2", "name": "Toma dedicada Secadora 16A", "x": 0.10, "y": 1.20, "h_cm": 110, "cir": "C4", "desc": "Línea independiente de 16A para bomba de calor."},
            {"code": "E3", "name": "2× Enchufes centro de planchado", "x": 1.45, "y": 0.80, "h_cm": 110, "cir": "C2", "desc": "Sobre la bancada para centro de planchado de vapor continuo."},
            {"code": "E4", "name": "Enchufe base de carga Dyson V15", "x": 2.10, "y": 1.90, "h_cm": 120, "cir": "C2", "desc": "Dentro del armario de limpieza."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptor entrada lavandería", "x": 0.60, "y": 2.40, "h_cm": 110, "cir": "C1", "desc": "Junto a la puerta corredera."}
        ],
        "hvac": [
            {"code": "VMC", "name": "Boca de Extracción VMC Ø 125 mm", "x": 1.10, "y": 1.25, "cir": "VMC-EXT", "isVMC": True, "desc": "Extracción reforzada de 45 m³/h para evitar humedad y condensación de ropa."}
        ],
        "planning": [
            "Columna de lavado y secado en bancada ergonómica con bandeja extraíble para cestos.",
            "Bancada de plegado de 140 cm con pila profunda de acero inoxidable.",
            "Armario vertical con enchufe para aspirador sin cable y tabla de planchar.",
            "Extracción VMC continua de 45 m³/h para secado sin olores."
        ],
        "materials": "Porcelánico técnico C3 gris cemento · Bancada fenólica antibacteriana · Muebles blanco mate",
        "lighting": "300 lux general con plafón LED estanco IP44 de encendido instantáneo"
    },
    {
        "id": "r08", "fl": "PB", "num": "08", "short": "08. Salón con Chimenea",
        "title": "08. Salón Principal con Chimenea",
        "w": 5.30, "h": 5.00, "area": "26,50 m² útiles", "dims": "5,30 × 5,00 m · h = 2,70 m",
        "desc": "Espacio de descanso y reunión familiar. Ventanal en esquina Suroeste con vistas panorámicas al atardecer, TV OLED 77\" empotrada a paño y chimenea panorámica de leña estanca.",
        "wN": "Corredera elevable de 3,00 m hacia el Patio Corrala ajardinado.",
        "wS": "Gran corredera elevable de 3,50 m abierta de par en par al Porche Sur cubierto.",
        "wE": "Paso diáfano y continuo hacia el Comedor Principal.",
        "wW": "Muro multimedia multimedia con chimenea de leña, TV 77\" empotrada y ventanal en esquina SW.",
        "openings": [
            {"wall": "S", "pos": 0.80, "len": 3.50, "type": "sliding", "label": "Corredera a Porche Sur 3,50m"},
            {"wall": "N", "pos": 0.80, "len": 3.00, "type": "sliding", "label": "Corredera a Patio Corrala"},
            {"wall": "W", "pos": 3.80, "len": 1.20, "type": "window", "label": "Ventanal Esquina SW"}
        ],
        "furn": [
            {"code": "TV", "name": "TV OLED 77\" empotrada a paño", "x": 0.05, "y": 1.30, "w": 0.12, "h": 1.70, "col": "#0f172a", "str": "#ef4444", "desc": "Pantalla 4K a h = 105 cm con canaleta oculta Ø 50 mm al mueble inferior."},
            {"code": "CHIM", "name": "Chimenea panorámica de leña estanca 100 cm", "x": 0.05, "y": 3.20, "w": 0.45, "h": 1.00, "col": "#b91c1c", "str": "#f87171", "desc": "Hogar estanco con toma de aire exterior dedicada (compatible con VMC)."},
            {"code": "SOFA", "name": "Sofá modular en L (3,20 × 2,40 m)", "x": 2.20, "y": 1.10, "w": 2.40, "h": 2.80, "col": "#334155", "str": "#64748b", "desc": "Tapizado texturizado hidrófugo tono arena a 3,60 m de la pantalla."},
            {"code": "MESA", "name": "Mesa de centro roble (1,20 × 0,70 m)", "x": 1.30, "y": 1.70, "w": 0.70, "h": 1.20, "col": "#d97706", "str": "#78350f", "desc": "Mesa baja a 45 cm del sofá."}
        ],
        "elec": [
            {"code": "E1", "name": "4× Enchufes 16A tras TV 77\"", "x": 0.10, "y": 2.10, "h_cm": 115, "cir": "C2", "desc": "Alimentación oculta para televisor, consola, deco y barra de sonido."},
            {"code": "RJ1", "name": "2× Doble Toma RJ45 Cat 6A (4 puertos tras TV)", "x": 0.10, "y": 2.40, "h_cm": 115, "cir": "RACK-PB", "isRJ": True, "desc": "Conexión por cable de 10 Gbps para streaming 4K y gaming sin latencia."},
            {"code": "WIFI", "name": "Punto de Acceso PoE Wi-Fi 7 de techo", "x": 2.65, "y": 2.50, "h_cm": 270, "cir": "RACK-POE", "isRJ": True, "desc": "Cobertura inalámbrica de máxima velocidad en toda la planta baja."},
            {"code": "E2", "name": "Enchufes esquinas sofá para lámparas/móvil", "x": 4.80, "y": 1.00, "h_cm": 30, "cir": "C1", "desc": "Con cargador rápido USB-C integrado."}
        ],
        "sw": [
            {"code": "I1", "name": "Botonera de escenas de iluminación", "x": 5.10, "y": 3.80, "h_cm": 110, "cir": "DOM", "desc": "Escena Relax, Cine, Noche y Lectura."}
        ],
        "hvac": [
            {"code": "SR", "name": "2 Circuitos Suelo Radiante Salón", "x": 2.65, "y": 3.50, "cir": "SR-PB-6/7", "isFloor": True, "desc": "Zonificación térmica con mortero autonivelante de alta transmisión."},
            {"code": "VMC", "name": "Boca Impulsión Zehnder Ø 125 mm", "x": 4.50, "y": 4.20, "cir": "VMC-IMP", "isVMC": True, "desc": "Impulsión de 60 m³/h de aire nuevo filtrado."}
        ],
        "planning": [
            "TV OLED 77\" empotrada a paño con centro a h = 105 cm y tubo pasacables Ø 50 mm.",
            "Sofá modular en L a distancia perfecta de 3,60 m de la pantalla.",
            "Chimenea de leña estanca con toma de aire exterior que convive al 100% con la VMC.",
            "Ventanal en esquina Suroeste para disfrutar de las puestas de sol atlánticas."
        ],
        "materials": "Porcelánico rectificado 120 × 120 cm piedra caliza · Muro Oeste porcelánico imitación piedra abujardada · Roble natural",
        "lighting": "150 lux general / 50 lux modo cine · Foseado indirecto cálido 2400K–2700K regulable + 4 balizas empotradas de suelo en ventanal"
    },
    {
        "id": "r09", "fl": "PB", "num": "09", "short": "09. Comedor Principal",
        "title": "09. Comedor Principal (10 Pax)",
        "w": 4.40, "h": 4.00, "area": "17,50 m² útiles", "dims": "4,40 × 4,00 m · h = 2,70 m",
        "desc": "Espacio de celebración familiar conectado directamente con la cocina y el porche exterior sur. Mesa noble de roble de 2,80 m para 10 comensales con paso holgado hacia el jardín.",
        "wN": "Paso libre diáfano hacia la cocina con isla.",
        "wS": "Gran corredera Cortizo Cor Vision Plus de 3,60 m hacia el Porche Sur.",
        "wE": "Fachada exterior Este con ventanal rasante de mañana.",
        "wW": "Conexión abierta y continua con el Salón Principal.",
        "openings": [
            {"wall": "S", "pos": 0.40, "len": 3.60, "type": "sliding", "label": "Corredera Porche Sur 3,60m"},
            {"wall": "N", "pos": 0.40, "len": 3.00, "type": "open", "label": "Abierto a Cocina"}
        ],
        "furn": [
            {"code": "MESA", "name": "Mesa noble de roble macizo (2,80 × 1,00 m)", "x": 0.80, "y": 1.40, "w": 2.80, "h": 1.00, "col": "#78350f", "str": "#d97706", "desc": "Mesa para 10 personas con cantos achaflanados y acabado al aceite natural."},
            {"code": "SILLAS", "name": "10× Sillas tapizadas con brazos", "x": 0.60, "y": 0.80, "w": 3.20, "h": 2.20, "col": "none", "str": "#94a3b8", "dashed": True, "desc": "Área de retroceso de sillas de 95 cm a cada lado."},
            {"code": "APARAD", "name": "Aparador suspendido roble (1,80 × 0,45 m)", "x": 0.20, "y": 0.15, "w": 1.80, "h": 0.45, "col": "#334155", "str": "#64748b", "desc": "Para vajilla, cristalería de fiesta y mantelería."}
        ],
        "elec": [
            {"code": "E1", "name": "Enchufes auxiliares sobre aparador", "x": 1.10, "y": 0.10, "h_cm": 110, "cir": "C1", "desc": "Para calientaplatos o lámpara auxiliar."},
            {"code": "E2", "name": "Enchufes en zócalo bajo mesa", "x": 2.20, "y": 3.80, "h_cm": 30, "cir": "C1", "desc": "Para fondue, raclette o cargadores."}
        ],
        "sw": [
            {"code": "I1", "name": "Regulador de luz colgante mesa", "x": 3.90, "y": 0.30, "h_cm": 110, "cir": "C1", "desc": "Regulación precisa de calidez e intensidad sobre la mesa."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Comedor", "x": 2.20, "y": 2.00, "cir": "SR-PB-8", "isFloor": True, "desc": "Mismo pavimento continuo sin juntas desde el salón y cocina."}
        ],
        "planning": [
            "Mesa noble de 280 × 100 cm para 10 personas.",
            "Espacio de retroceso de sillas de 95 cm libres en ambos lados.",
            "Aparador de apoyo suspendido para vajilla de gala a h = 85 cm.",
            "Conexión diáfana al porche sur y a la cocina."
        ],
        "materials": "Roble macizo salvaje acabado al aceite · Porcelánico arena continuo · Cortizo negro forja",
        "lighting": "2 lámparas suspendidas acústicas a 75 cm sobre la mesa con emisión cálida 2700K regulable"
    },
    {
        "id": "r10", "fl": "PB", "num": "10", "short": "10. Porche Sur Expandido",
        "title": "10. Porche Sur Cubierto Expandido (Fondo 3,00 m)",
        "w": 12.00, "h": 3.00, "area": "36,00 m² cubiertos", "dims": "12,00 × 3,00 m · h = 2,80 m",
        "desc": "Espacio exterior cubierto protegido de la lluvia gallega con 3 metros de fondo real. Alberga el comedor de verano para 10 personas, barbacoa/churrasqueira de granito y zona lounge exterior frente al jardín y piscina.",
        "wN": "Fachada Sur de la casa con las grandes cristaleras correderas de Cocina, Comedor y Salón.",
        "wS": "Alineación de pilares metálicos esbeltos y salida a ras de suelo hacia el césped y piscina.",
        "wE": "Muro testero Este con la Churrasqueira de granito y leñera integrada.",
        "wW": "Muro testero Oeste con armario de jardín y salida para robot cortacésped.",
        "openings": [
            {"wall": "N", "pos": 1.00, "len": 10.00, "type": "sliding", "label": "Correderas Salón, Comedor y Cocina"}
        ],
        "furn": [
            {"code": "BBQ", "name": "Churrasqueira de carbón y leña en granito", "x": 10.50, "y": 0.30, "w": 1.20, "h": 2.40, "col": "#1e293b", "str": "#ef4444", "desc": "Bancada de 240 × 65 cm en granito Zimbabwe con parrilla de inox y leñera."},
            {"code": "MESA", "name": "Comedor de verano en teka (10 Pax)", "x": 6.80, "y": 0.60, "w": 2.60, "h": 1.00, "col": "#78350f", "str": "#b45309", "desc": "Mesa exterior de 260 × 100 cm frente a la salida de cocina."},
            {"code": "SOFA", "name": "Salón Lounge exterior (Sofás de cuerda)", "x": 1.50, "y": 0.60, "w": 3.20, "h": 1.80, "col": "#334155", "str": "#64748b", "desc": "Mobiliario exterior de relajación protegido del viento."},
            {"code": "ROBOT", "name": "Armario robot cortacésped Husqvarna", "x": 0.20, "y": 0.30, "w": 0.80, "h": 0.80, "col": "#065f46", "str": "#10b981", "desc": "Salida a nivel de hierba para segado autónomo."}
        ],
        "elec": [
            {"code": "E1", "name": "4× Enchufes estancos IP66 en BBQ", "x": 10.80, "y": 0.15, "h_cm": 110, "cir": "C1-EXT", "desc": "Para parrilla eléctrica, batidora o música exterior."},
            {"code": "WIFI", "name": "Punto de Acceso Wi-Fi Exterior IP65", "x": 6.00, "y": 1.50, "h_cm": 280, "cir": "RACK-POE", "isRJ": True, "desc": "Cobertura total en el porche, jardín y piscina."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptores estancos iluminación porche", "x": 10.20, "y": 0.20, "h_cm": 110, "cir": "C1", "desc": "Zonificación luz comedor, lounge y balizas de césped."}
        ],
        "hvac": [
            {"code": "AGUA", "name": "Fregadero exterior inox (agua fría/caliente)", "x": 11.20, "y": 1.80, "cir": "ACS-EXT", "desc": "Para lavar utensilios de barbacoa sin entrar a la casa."}
        ],
        "planning": [
            "Fondo libre real de 3,00 m (supera holgadamente los 2,00 m estrechos de iteraciones previas).",
            "Comedor de verano de 10 personas + Churrasqueira de granito en extremo Este.",
            "Zona lounge frente a la salida del salón.",
            "Armario integrado para robot cortacésped con salida directa a jardín."
        ],
        "materials": "Tarima exterior de madera tecnológica gris cálida · Granito negro abujardado · Falso techo de iroko",
        "lighting": "Líneas LED cálidas 2400K embutidas en lamas de madera de falso techo + focos estancos en BBQ"
    },
    {
        "id": "r11", "fl": "PB", "num": "11", "short": "11. Trastero Bicis y Sala Técnica",
        "title": "11. Trastero Bicis/Surf & Sala Técnica",
        "w": 4.00, "h": 2.05, "area": "8,20 m² útiles", "dims": "4,00 × 2,05 m · h = 2,65 m",
        "desc": "El corazón energético y deportivo. Conexión directa desde la pérgola de coches para bicis y tablas de surf. Aloja la unidad interior de aerotermia, el recuperador VMC Zehnder y el Rack de telecomunicaciones de la casa.",
        "wN": "Tabique interior con puerta corredera hacia el Zaguán Mudroom.",
        "wS": "Pared con bancada de instalaciones (Aerotermia y VMC).",
        "wE": "Pared con armario Rack mural de telecomunicaciones e inversor solar fotovoltaico.",
        "wW": "Muro exterior Oeste con puerta estanca de acceso directo desde la Pérgola.",
        "openings": [
            {"wall": "W", "pos": 0.40, "len": 0.90, "type": "door", "label": "Puerta a Pérgola"},
            {"wall": "N", "pos": 1.50, "len": 0.85, "type": "sliding", "label": "A Zaguán Mudroom"}
        ],
        "furn": [
            {"code": "AERO", "name": "Aerotermia Vaillant aroTHERM + Depósito 250L", "x": 2.20, "y": 1.30, "w": 0.70, "h": 0.65, "col": "#0284c7", "str": "#38bdf8", "desc": "Interacumulador de ACS y bomba de calor para suelo radiante."},
            {"code": "VMC", "name": "Unidad Central VMC Zehnder ComfoAir Q350", "x": 3.10, "y": 1.30, "w": 0.75, "h": 0.60, "col": "#0d9488", "str": "#14b8a6", "desc": "Recuperador de calor de alta eficiencia (92%) con filtros F7."},
            {"code": "RACK", "name": "Armario Rack 19\" 9U + Switch PoE + Router", "x": 3.40, "y": 0.20, "w": 0.55, "h": 0.60, "col": "#7c3aed", "str": "#a855f7", "desc": "Punto neurálgico de red cableada Cat 6A y domótica."},
            {"code": "SURF", "name": "Racks para 3 tablas de surf + 4 trajes", "x": 0.15, "y": 0.20, "w": 0.45, "h": 1.60, "col": "#f59e0b", "str": "#d97706", "desc": "Barra de secado de neoprenos con desagüe lineal en suelo."},
            {"code": "BICIS", "name": "Soportes verticales para 4 bicicletas", "x": 1.00, "y": 0.15, "w": 1.20, "h": 0.35, "col": "#475569", "str": "#94a3b8", "desc": "Colgadas en pared para liberar el suelo."}
        ],
        "elec": [
            {"code": "E1", "name": "Toma trifásica / monofásica Aerotermia", "x": 2.50, "y": 1.80, "h_cm": 150, "cir": "C-CLIMA", "desc": "Protección diferencial superinmunizada."},
            {"code": "E2", "name": "4× Tomas SAI en Rack 19\"", "x": 3.60, "y": 0.50, "h_cm": 180, "cir": "SAI-RACK", "desc": "Alimentación ininterrumpida para router, switch y cámaras."},
            {"code": "E3", "name": "2× Enchufes carga bicis eléctricas", "x": 1.10, "y": 0.10, "h_cm": 110, "cir": "C2", "desc": "Para cargar las baterías de las bicicletas en su soporte."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptor estanco conmutado puertas", "x": 0.30, "y": 0.80, "h_cm": 110, "cir": "C1", "desc": "Encendido desde entrada exterior o desde el zaguán."}
        ],
        "hvac": [
            {"code": "DESAG", "name": "Sumidero sifónico de suelo neoprenos", "x": 0.40, "y": 1.00, "cir": "PLUV", "desc": "Recoge el agua de goteo de los trajes de surf y bicis mojadas."}
        ],
        "planning": [
            "Doble acceso: exterior desde pérgola de coches e interior desde mudroom.",
            "Racks para 4 bicicletas colgadas y 3 tablas de surf.",
            "Barra de secado de trajes de neopreno con sumidero de desagüe en suelo.",
            "Concentración de todos los equipos ruidosos (aerotermia, VMC, Rack) fuera del volumen habitable."
        ],
        "materials": "Suelo porcelánico técnico C3 gris cemento · Paredes lavables · Bancadas antivibratorias",
        "lighting": "200 lux de servicio con regleta LED estanca IP65 de 4000K neutra"
    },
    {
        "id": "r12", "fl": "P1", "num": "12", "short": "12. Galería Acústica y Escalera",
        "title": "12. Galería Acústica & Escalera P1",
        "w": 4.80, "h": 2.20, "area": "8,20 m² útiles", "dims": "4,80 × 2,20 m · h = 2,65 m",
        "desc": "Espacio distribuidor superior con vistas cenitales sobre el Patio Claustro. Mampara acústica continua de vidrio 4+4 Silence que aísla 42 dB de ruido entre plantas y escalera de roble con iluminación rasante.",
        "wN": "Fachada Norte con escalera de roble y cristalera cenital.",
        "wS": "Mampara acristalada fija acústica 4+4 Silence hacia el vacío del Patio Claustro.",
        "wE": "Paso hacia la Suite Principal de Matrimonio.",
        "wW": "Paso hacia los dormitorios infantiles y baño de hijos.",
        "openings": [
            {"wall": "S", "pos": 0.50, "len": 3.80, "type": "glass_fixed", "label": "Mampara Acústica 4+4 Silence (42dB)"}
        ],
        "furn": [
            {"code": "ESC", "name": "Escalera de peldaños flotantes de roble (17 peld.)", "x": 0.20, "y": 0.20, "w": 2.20, "h": 0.90, "col": "#78350f", "str": "#d97706", "desc": "Huella 28 cm, contrahuella 17,6 cm con zanca de acero oculta."},
            {"code": "LIBR", "name": "Librería empotrada de pasillo (1,60 × 0,30 m)", "x": 2.80, "y": 0.15, "w": 1.60, "h": 0.30, "col": "#334155", "str": "#64748b", "desc": "Estantería para libros de lectura infantil y familiar."}
        ],
        "elec": [
            {"code": "E1", "name": "Enchufe de servicio en pasillo", "x": 3.00, "y": 0.10, "h_cm": 30, "cir": "C1", "desc": "Para aspirador o lámpara auxiliar."},
            {"code": "BALIZ", "name": "4× Balizas LED de cortesía nocturna en zócalo", "x": 1.20, "y": 0.10, "h_cm": 25, "cir": "C1-NOCHE", "desc": "Luz tenue ámbar para trayecto nocturno de los niños al baño sin encender luces principales."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutadores cuádruples escalera arriba/abajo", "x": 2.50, "y": 0.20, "h_cm": 110, "cir": "C1", "desc": "Encendido de escalera y galería desde ambos extremos."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Galería", "x": 2.40, "y": 1.50, "cir": "SR-P1-GAL", "isFloor": True, "desc": "Madera noble sobre forjado acústico."}
        ],
        "planning": [
            "Mampara de vidrio laminar 4+4 Silence: aísla 42 dB de ruido entre plantas.",
            "Escalera de 17 peldaños flotantes con zanca oculta.",
            "Balizas LED de cortesía a 25 cm para trayectos nocturnos de los niños.",
            "Librería empotrada integrada en tabique ciego."
        ],
        "materials": "Vidrio acústico laminar 4+4 Silence · Peldaños roble macizo · Pared blanco lino",
        "lighting": "Luz indirecta foseada en techo + 4 balizas empotradas rasantes de suelo a 2400K"
    },
    {
        "id": "r13", "fl": "P1", "num": "13", "short": "13. Dormitorio Niña",
        "title": "13. Dormitorio Infantil Niña",
        "w": 3.65, "h": 4.00, "area": "14,60 m² útiles", "dims": "3,65 × 4,00 m · h = 2,65 m",
        "desc": "Espacio de descanso y estudio juvenil. Mesa de 1,80 m apoyada en pared lateral Este con luz natural a 90° (cero reflejos en pantalla de portátil y cero contraluz) y salida directa al Balcón Corrido Sur.",
        "wN": "Pared con armario empotrado de suelo a techo y tabique con pasillo superior.",
        "wS": "Fachada Sur con balconera corredera elevable y persiana autoblocante motorizada.",
        "wE": "Pared lateral con mesa de estudio suspendida y luz natural lateral.",
        "wW": "Tabique acústico medianero con el dormitorio del hermano (aislamiento Rw >= 50 dB).",
        "openings": [
            {"wall": "S", "pos": 0.50, "len": 2.20, "type": "sliding", "label": "Balconera a Balcón Sur"},
            {"wall": "N", "pos": 0.30, "len": 0.85, "type": "door", "label": "Puerta Dormitorio"}
        ],
        "furn": [
            {"code": "MESA", "name": "Mesa de estudio suspendida (1,80 × 0,65 m)", "x": 2.80, "y": 0.80, "w": 0.65, "h": 1.80, "col": "#1e293b", "str": "#38bdf8", "desc": "Mesa en abedul a h = 74 cm apoyada en pared lateral Este: luz a 90° sin reflejos."},
            {"code": "CAMA", "name": "Cama juvenil (1,20 × 2,00 m)", "x": 0.30, "y": 1.50, "w": 1.20, "h": 2.00, "col": "#334155", "str": "#cbd5e1", "desc": "Cama con cabecero tapizado y mesilla suspendida."},
            {"code": "ARM", "name": "Armario empotrado suelo a techo (2,00 × 0,60 m)", "x": 1.40, "y": 0.10, "w": 2.00, "h": 0.60, "col": "#475569", "str": "#94a3b8", "desc": "Puertas lisas lacadas con baldas regulables y cajonera interior."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes 16A + 2× USB-C mesa estudio", "x": 3.45, "y": 1.70, "h_cm": 80, "cir": "C2", "desc": "Sobre el escritorio para ordenador portátil, flexo y tablet de estudio."},
            {"code": "RJ1", "name": "Doble Toma RJ45 Cat 6A (10 Gbps) escritorio", "x": 3.45, "y": 1.20, "h_cm": 80, "cir": "RACK-P1", "isRJ": True, "desc": "Cableado de alta velocidad para clases online y descargas pesadas."},
            {"code": "E2", "name": "2× Enchufes + RJ45 pared frontal cama", "x": 0.10, "y": 2.20, "h_cm": 115, "cir": "C2 + RACK", "isRJ": True, "desc": "Previsión para TV/pantalla frente a la cama."},
            {"code": "E3", "name": "Enchufe + conmutador en mesilla de noche", "x": 0.10, "y": 1.20, "h_cm": 65, "cir": "C1", "desc": "Apagado de luz general desde la cama."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutador triple puerta/cabecero", "x": 1.20, "y": 0.20, "h_cm": 110, "cir": "C1", "desc": "Control conmutado de luz general y foseado LED."},
            {"code": "I2", "name": "Pulsador persiana autoblocante motorizada", "x": 2.80, "y": 3.80, "h_cm": 110, "cir": "PERSIANAS", "desc": "Subida y bajada de persiana Somfy."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Dormitorio Niña", "x": 1.80, "y": 2.50, "cir": "SR-P1-1", "isFloor": True, "desc": "Tarima de roble nórdico apta para suelo radiante."},
            {"code": "T", "name": "Termostato digital táctil independiente", "x": 1.20, "y": 0.40, "h_cm": 150, "cir": "CLIMA", "desc": "Termostato zonal programable."},
            {"code": "VMC", "name": "Boca Impulsión Zehnder Ø 125 mm", "x": 1.80, "y": 3.40, "cir": "VMC-IMP", "isVMC": True, "desc": "Impulsión silenciosa de 30 m³/h de aire fresco."}
        ],
        "planning": [
            "Mesa de estudio suspendida de 180 × 65 cm con luz lateral a 90°.",
            "Cama juvenil de 120 × 200 cm con cabecero tapizado y mesilla suspendida.",
            "Armario empotrado de suelo a techo de 200 × 60 cm.",
            "Salida directa al Balcón Corrido Sur protegido."
        ],
        "materials": "Paredes tono salvia suave empolvada (NCS S 1510-G40Y) · Tarima roble blanqueado · Textiles lino natural",
        "lighting": "500 lux en mesa de estudio con lámpara orientable + foseado LED cálido 2700K en cabecero"
    },
    {
        "id": "r14", "fl": "P1", "num": "14", "short": "14. Dormitorio Niño",
        "title": "14. Dormitorio Infantil Niño",
        "w": 3.65, "h": 4.00, "area": "14,60 m² útiles", "dims": "3,65 × 4,00 m · h = 2,65 m",
        "desc": "Espacio de descanso y estudio juvenil gemelo. Mesa de 1,80 m apoyada en pared lateral con luz a 90° sin reflejos en monitor, armario empotrado y salida directa al balcón sur.",
        "wN": "Pared con armario empotrado de suelo a techo y tabique con pasillo superior.",
        "wS": "Fachada Sur con balconera corredera elevable y persiana autoblocante motorizada.",
        "wE": "Tabique acústico medianero con el dormitorio de la hermana (Rw >= 50 dB).",
        "wW": "Pared lateral con mesa de estudio suspendida y luz natural lateral.",
        "openings": [
            {"wall": "S", "pos": 0.50, "len": 2.20, "type": "sliding", "label": "Balconera a Balcón Sur"},
            {"wall": "N", "pos": 2.50, "len": 0.85, "type": "door", "label": "Puerta Dormitorio"}
        ],
        "furn": [
            {"code": "MESA", "name": "Mesa de estudio suspendida (1,80 × 0,65 m)", "x": 0.20, "y": 0.80, "w": 0.65, "h": 1.80, "col": "#1e293b", "str": "#38bdf8", "desc": "Mesa en abedul a h = 74 cm con luz lateral a 90° sin reflejos."},
            {"code": "CAMA", "name": "Cama juvenil (1,20 × 2,00 m)", "x": 2.10, "y": 1.50, "w": 1.20, "h": 2.00, "col": "#334155", "str": "#cbd5e1", "desc": "Cama con cabecero tapizado y mesilla suspendida."},
            {"code": "ARM", "name": "Armario empotrado suelo a techo (2,00 × 0,60 m)", "x": 0.30, "y": 0.10, "w": 2.00, "h": 0.60, "col": "#475569", "str": "#94a3b8", "desc": "Puertas lacadas con distribución interior personalizada."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes 16A + 2× USB-C mesa estudio", "x": 0.15, "y": 1.70, "h_cm": 80, "cir": "C2", "desc": "Para portátil y flexo de estudio."},
            {"code": "RJ1", "name": "Doble Toma RJ45 Cat 6A (10 Gbps) escritorio", "x": 0.15, "y": 1.20, "h_cm": 80, "cir": "RACK-P1", "isRJ": True, "desc": "Toma de red Gigabit directo al Rack."},
            {"code": "E2", "name": "2× Enchufes + RJ45 pared frontal cama", "x": 3.45, "y": 2.20, "h_cm": 115, "cir": "C2 + RACK", "isRJ": True, "desc": "Previsión para pantalla frente a cama."},
            {"code": "E3", "name": "Enchufe + conmutador en mesilla de noche", "x": 3.45, "y": 1.20, "h_cm": 65, "cir": "C1", "desc": "Apagado desde la cama."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutador triple puerta/cabecero", "x": 2.40, "y": 0.20, "h_cm": 110, "cir": "C1", "desc": "Control conmutado de iluminación."},
            {"code": "I2", "name": "Pulsador persiana motorizada", "x": 0.80, "y": 3.80, "h_cm": 110, "cir": "PERSIANAS", "desc": "Motor Somfy silencioso."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Dormitorio Niño", "x": 1.80, "y": 2.50, "cir": "SR-P1-2", "isFloor": True, "desc": "Tarima de roble nórdico blanqueado."},
            {"code": "T", "name": "Termostato digital táctil independiente", "x": 2.40, "y": 0.40, "h_cm": 150, "cir": "CLIMA", "desc": "Termostato zonal programable."},
            {"code": "VMC", "name": "Boca Impulsión Zehnder Ø 125 mm", "x": 1.80, "y": 3.40, "cir": "VMC-IMP", "isVMC": True, "desc": "Impulsión de 30 m³/h de aire fresco."}
        ],
        "planning": [
            "Distribución gemela ergonómica con luz a 90° en pupitre.",
            "Aislamiento acústico medianero Rw >= 50 dB entre dormitorios.",
            "Armario empotrado de 200 × 60 cm y cama de 120 × 200 cm.",
            "Acceso directo a Balcón Corrido Sur."
        ],
        "materials": "Paredes tono neutro cálido arena y azul grisáceo suave (NCS S 2005-B20G) · Tarima roble blanqueado",
        "lighting": "500 lux de estudio + foseado indirecto cálido en cabecero de cama"
    },
    {
        "id": "r15", "fl": "P1", "num": "15", "short": "15. Baño Compartido Hijos",
        "title": "15. Baño Compartido Hijos",
        "w": 2.70, "h": 2.50, "area": "6,80 m² útiles", "dims": "2,70 × 2,50 m · h = 2,65 m",
        "desc": "Baño amplio para uso diario simultáneo de los dos hermanos. Encimera de doble lavabo de 140 cm, bañera ergonómica con ducha combinada, inodoro suspendido y ventana oscilobatiente a fachada Norte.",
        "wN": "Fachada Norte con ventana practicable oscilobatiente.",
        "wS": "Tabique interior con puerta batiente hacia el pasillo superior.",
        "wE": "Pared con mueble de doble lavabo y toallero calefactable.",
        "wW": "Pared con bañera y zona de inodoro suspendido.",
        "openings": [
            {"wall": "N", "pos": 0.80, "len": 1.10, "type": "window", "label": "Ventana Norte"},
            {"wall": "S", "pos": 0.90, "len": 0.80, "type": "door", "label": "Puerta Baño"}
        ],
        "furn": [
            {"code": "LAV2", "name": "Mueble suspendido 140 cm con Doble Seno", "x": 2.10, "y": 0.30, "w": 0.50, "h": 1.40, "col": "#f8fafc", "str": "#38bdf8", "desc": "Dos senos bajo encimera con dos grifos monomando empotrados negros."},
            {"code": "BAN", "name": "Bañera exenta acrílica ergonómica (1,60 × 0,75 m)", "x": 0.15, "y": 0.15, "w": 0.75, "h": 1.60, "col": "#0284c7", "str": "#38bdf8", "desc": "Bañera profunda con rociador efecto lluvia superior y grifería termostática."},
            {"code": "WC", "name": "Inodoro suspendido Geberit Rimless", "x": 0.20, "y": 1.90, "w": 0.40, "h": 0.50, "col": "#f8fafc", "str": "#94a3b8", "desc": "Cisterna empotrada insonorizada Geberit."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes estancos IP44 lavabo", "x": 2.10, "y": 1.80, "h_cm": 115, "cir": "C5", "desc": "Para secador y cepillos de dientes eléctricos."},
            {"code": "TR", "name": "Radiador Toallero Eléctrico Negro 600W", "x": 2.10, "y": 2.10, "h_cm": 120, "cir": "C-TOALLERO", "desc": "Toallero de gran formato 140 × 50 cm para secar las toallas de ambos niños."}
        ],
        "sw": [
            {"code": "I1", "name": "Interruptor general + Luz espejo LED", "x": 0.80, "y": 2.40, "h_cm": 110, "cir": "C1", "desc": "Junto a la puerta de entrada."}
        ],
        "hvac": [
            {"code": "SR", "name": "Circuito Suelo Radiante Baño Hijos", "x": 1.35, "y": 1.40, "cir": "SR-P1-BH", "isFloor": True, "desc": "Suelo cálido al salir de la bañera."},
            {"code": "VMC", "name": "Boca Extracción Zehnder Ø 125 mm", "x": 1.35, "y": 0.50, "cir": "VMC-EXT", "isVMC": True, "desc": "Extracción continua de 45 m³/h de vapor de baño."}
        ],
        "planning": [
            "Encimera de 140 cm con doble seno: uso matinal simultáneo de los dos niños.",
            "Bañera acrílica de 160 × 75 cm con rociador efecto lluvia superior.",
            "Inodoro suspendido Geberit con cisterna insonorizada.",
            "Ventana oscilobatiente en fachada Norte para iluminación y ventilación natural."
        ],
        "materials": "Porcelánico rectificado imitación caliza gris clara · Mueble suspendido roble claro · Grifería negra",
        "lighting": "300 lux general + espejo con tira LED perimetral frontal de 400 lux sin sombras"
    },
    {
        "id": "r16", "fl": "P1", "num": "16", "short": "16. Suite Matrimonio",
        "title": "16. Suite Principal de Matrimonio",
        "w": 7.00, "h": 4.50, "area": "31,20 m² totales", "dims": "7,00 × 4,50 m · h = 2,65 m",
        "desc": "Ala Este privada en Planta Primera: Dormitorio Sur de 16,5 m² con vistas abiertas al jardín, vestidor de paso de 8,4 m² en doble hilera con iluminación LED y baño privado doble de 6,3 m² con ducha italiana doble.",
        "wN": "Fachada Norte con ventana del baño privado y vestidor.",
        "wS": "Fachada Sur con balconera corredera elevable hacia el Balcón Corrido.",
        "wE": "Muro exterior Este con orientación al naciente.",
        "wW": "Tabique interior con puerta de acceso desde la Galería Acústica.",
        "openings": [
            {"wall": "S", "pos": 0.80, "len": 2.80, "type": "sliding", "label": "Balconera a Balcón Sur"},
            {"wall": "N", "pos": 5.20, "len": 1.20, "type": "window", "label": "Ventana Baño Suite"},
            {"wall": "W", "pos": 1.80, "len": 0.85, "type": "door", "label": "Entrada Suite"}
        ],
        "furn": [
            {"code": "KING", "name": "Cama King Size (1,80 × 2,00 m)", "x": 0.80, "y": 1.60, "w": 1.80, "h": 2.00, "col": "#334155", "str": "#cbd5e1", "desc": "Cama orientada al Sur con vistas abiertas al jardín y cabecero de roble tostado."},
            {"code": "VEST1", "name": "Vestidor Hilera 1 (Armarios con LED)", "x": 3.40, "y": 0.20, "w": 0.60, "h": 2.40, "col": "#475569", "str": "#1e293b", "desc": "Frentes de vidrio ahumado con barras iluminadas y cajones pantaloneros."},
            {"code": "VEST2", "name": "Vestidor Hilera 2 (Armarios con LED)", "x": 4.70, "y": 0.20, "w": 0.60, "h": 2.40, "col": "#475569", "str": "#1e293b", "desc": "Pasillo central libre de 110 cm entre ambas hileras de armario."},
            {"code": "LAV2", "name": "Encimera Dekton 150 cm con Doble Seno", "x": 5.80, "y": 0.20, "w": 0.50, "h": 1.50, "col": "#f8fafc", "str": "#38bdf8", "desc": "Dos senos bajo encimera con grifería monomando empotrada negra mate."},
            {"code": "DUCHA", "name": "Ducha italiana doble (1,50 × 0,90 m)", "x": 5.80, "y": 2.40, "w": 0.90, "h": 1.50, "col": "#0284c7", "str": "#38bdf8", "desc": "Rociador de techo empotrado 40 × 40 cm Hansgrohe Raindance con termostato electrónico."},
            {"code": "WC", "name": "Cabina de Inodoro semi-independiente", "x": 5.80, "y": 4.00, "w": 0.40, "h": 0.45, "col": "#f8fafc", "str": "#94a3b8", "desc": "Inodoro suspendido Geberit con puerta translúcida."}
        ],
        "elec": [
            {"code": "E1", "name": "2× Enchufes + USB-C cada mesilla de noche", "x": 0.40, "y": 1.80, "h_cm": 65, "cir": "C1", "desc": "Carga rápida en ambos lados de la cama King Size."},
            {"code": "RJ1", "name": "Doble Toma RJ45 Cat 6A cabecero", "x": 0.40, "y": 2.20, "h_cm": 65, "cir": "RACK-P1", "isRJ": True, "desc": "Toma de red Gigabit en mesilla."},
            {"code": "E2", "name": "2× Enchufes + RJ45 tras TV 55\" frontal", "x": 2.80, "y": 1.60, "h_cm": 115, "cir": "C2 + RACK", "isRJ": True, "desc": "Previsión empotrada en tabique frente a la cama."},
            {"code": "E3", "name": "2× Enchufes estancos IP44 lavabo suite", "x": 5.75, "y": 1.00, "h_cm": 115, "cir": "C5", "desc": "Para afeitadora o secador."}
        ],
        "sw": [
            {"code": "I1", "name": "Botonera cuádruple en cabecero", "x": 0.40, "y": 1.50, "h_cm": 65, "cir": "DOM", "desc": "Apagado total, luz foseada, aplique de lectura y persiana sin levantarse de la cama."}
        ],
        "hvac": [
            {"code": "SR", "name": "2 Circuitos Suelo Radiante Suite (Dormitorio + Baño)", "x": 2.00, "y": 2.80, "cir": "SR-P1-3/4", "isFloor": True, "desc": "Zonificación independiente."},
            {"code": "TR", "name": "Radiador Toallero Eléctrico Diseño Negro 750W", "x": 5.75, "y": 2.00, "h_cm": 120, "cir": "C-TOALLERO", "desc": "Toallero de gran formato en baño suite."},
            {"code": "VMC", "name": "Impulsión en dormitorio (45 m³/h) + Extracción en baño (45 m³/h)", "x": 2.00, "y": 3.80, "cir": "VMC", "isVMC": True, "desc": "Circulación de aire óptima."}
        ],
        "planning": [
            "Suite completa de 31,2 m² en ala Este privada.",
            "Cama King Size orientada al Sur con vistas panorámicas al jardín.",
            "Vestidor de paso en doble hilera con pasillo central libre de 110 cm.",
            "Baño privado de 6,3 m² con ducha doble walk-in (150 × 90 cm) y doble seno."
        ],
        "materials": "Dekton Kelya Cosentino en lavabo y ducha · Roble tostado en cabecero y panelados · Vidrio ahumado en vestidor",
        "lighting": "150 lux dormitorio / 300 lux vestidor / 400 lux baño · Foseado perimetral regulable + apliques lectura Marset Ledtube"
    },
    {
        "id": "r17", "fl": "P1", "num": "17", "short": "17. Balcón Corrido Sur",
        "title": "17. Balcón Corrido Sur P1",
        "w": 11.50, "h": 1.20, "area": "14,00 m² útiles", "dims": "11,50 × 1,20 m · h = 1,10 m peto",
        "desc": "Balcón volado corrido con orientación 100% Sur sobre el porche de PB. Barandilla continua de vidrio estructural 10+10 mm sin montantes metálicos verticales: vistas despejadas al jardín y piscina desde el interior de la cama.",
        "wN": "Fachada Sur de la planta primera con salidas desde los tres dormitorios (suite y dos infantiles).",
        "wS": "Barandilla continua de vidrio estructural laminar de seguridad 10+10 mm embutida en forjado.",
        "wE": "Testero Este con celosía de lamas de madera para privacidad de la suite.",
        "wW": "Testero Oeste con peto de hormigón blanco.",
        "openings": [
            {"wall": "N", "pos": 0.80, "len": 9.50, "type": "sliding", "label": "Balconeras Suite y Dormitorios"}
        ],
        "furn": [
            {"code": "VIDRIO", "name": "Barandilla vidrio estructural 10+10 mm (11,5 m)", "x": 0.10, "y": 1.10, "w": 11.30, "h": 0.08, "col": "#bae6fd", "str": "#0284c7", "desc": "Vidrio laminar de seguridad embutido en perfil U oculto en forjado (cero montantes)."},
            {"code": "SILLAS", "name": "2× Sillones lounge de exterior en balcón suite", "x": 8.50, "y": 0.20, "w": 1.80, "h": 0.70, "col": "#334155", "str": "#64748b", "desc": "Para tomar el sol o café matinal al despertar."}
        ],
        "elec": [
            {"code": "E1", "name": "3× Enchufes estancos IP66 en balcón", "x": 2.00, "y": 0.10, "h_cm": 30, "cir": "C1-EXT", "desc": "Uno en cada zona de dormitorio para recarga de portátil o móvil al aire libre."}
        ],
        "sw": [
            {"code": "I1", "name": "Conmutador luz balcón", "x": 9.00, "y": 0.10, "h_cm": 110, "cir": "C1", "desc": "Encendido desde el dormitorio principal."}
        ],
        "hvac": [
            {"code": "SUMID", "name": "3× Sumideros lineales ocultos de pluviales", "x": 5.50, "y": 1.10, "cir": "PLUV", "desc": "Evacuación inmediata del agua de lluvia hacia bajantes ocultas."}
        ],
        "planning": [
            "Longitud continua de 11,50 m con 1,20 m de vuelo libre.",
            "Barandilla de vidrio estructural 10+10 mm: visual 100% limpia sin barrotes desde la cama.",
            "Tarima tecnológica de exterior idéntica a la del Porche y Patio Corrala.",
            "Actúa como voladizo de sombra estival para los grandes ventanales de la Planta Baja."
        ],
        "materials": "Vidrio estructural laminar 10+10 mm · Tarima exterior teka tecnológica · Falso techo de iroko",
        "lighting": "Línea rasante LED 2400K embutida en zócalo inferior bañando el suelo de madera"
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fichas Técnicas Zoom-In 1:20 con Planos CAD — Propuesta D (Oleiros)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #0b0f19;
      color: #f8fafc;
      margin: 0;
      padding: 0;
    }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
    .marker-node {
      cursor: pointer;
      transition: transform 0.15s ease, filter 0.15s ease;
      transform-origin: center;
      transform-box: fill-box;
    }
    .marker-node:hover {
      transform: scale(1.15);
      filter: drop-shadow(0 3px 6px rgba(15,23,42,0.4));
    }
    .marker-selected {
      stroke: #38bdf8 !important;
      stroke-width: 3px !important;
      filter: drop-shadow(0 0 10px rgba(56,189,248,0.9));
    }
    .room-btn.active {
      background-color: #0284c7 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
      font-weight: 700;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      padding: 0.15rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 700;
    }
  </style>
</head>
<body class="p-3 md:p-6 max-w-[1780px] mx-auto space-y-4">

  <!-- CABECERA PRINCIPAL -->
  <header class="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-5 shadow-2xl flex flex-col lg:flex-row lg:items-center justify-between gap-4">
    <div class="space-y-1">
      <div class="flex flex-wrap items-center gap-2">
        <span class="badge bg-sky-500/20 text-sky-400 border border-sky-500/30">PROYECTO DE EJECUCIÓN · ESCALA 1:20</span>
        <span class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">INTERIORISTA &amp; APAREJADOR</span>
        <span class="badge bg-amber-500/20 text-amber-400 border border-amber-500/30">17 PLANOS CAD SVG + FICHAS TÉCNICAS</span>
      </div>
      <h1 class="text-xl md:text-2xl font-black text-white tracking-tight">Hogar Oleiros — Visor Técnico de Estancias al Centímetro (Propuesta D)</h1>
      <p class="text-xs md:text-sm text-slate-400 max-w-5xl">
        Cada una de las <strong>17 estancias</strong> cuenta con su <strong>plano técnico CAD interactivo</strong>: cotas reales, distribución de mobiliario a escala, ubicación exacta y altura ($h$) de <strong>enchufes 16A/25A, tomas dobles RJ45 Cat 6A, interruptores, serpentín de suelo radiante y bocas VMC Zehnder</strong>.
      </p>
    </div>

    <!-- FILTRO DE PLANTA -->
    <div class="flex flex-wrap items-center gap-2 shrink-0">
      <button id="filter-ALL" onclick="setFloorFilter('ALL')" class="px-3.5 py-2 rounded-xl text-xs font-bold border border-sky-500 bg-sky-600 text-white shadow-lg transition">
        Todas (17)
      </button>
      <button id="filter-PB" onclick="setFloorFilter('PB')" class="px-3.5 py-2 rounded-xl text-xs font-semibold border border-slate-800 bg-slate-800 text-slate-300 hover:text-white transition">
        Planta Baja (11)
      </button>
      <button id="filter-P1" onclick="setFloorFilter('P1')" class="px-3.5 py-2 rounded-xl text-xs font-semibold border border-slate-800 bg-slate-800 text-slate-300 hover:text-white transition">
        Planta Primera (6)
      </button>
    </div>
  </header>

  <!-- SELECTOR RÁPIDO DE TODAS LAS ESTANCIAS (PILLS) -->
  <nav id="room-pills" class="flex flex-wrap gap-1.5 bg-slate-900 border border-slate-800 rounded-2xl p-3 shadow-lg"></nav>

  <!-- GRID PRINCIPAL: PLANO CAD SVG (IZQUIERDA) + FICHA DETALLADA (DERECHA) -->
  <div class="grid grid-cols-1 xl:grid-cols-12 gap-5 items-start">

    <!-- COLUMNA IZQUIERDA (7 COLS): PLANO CAD 1:20 SVG -->
    <div class="xl:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-2xl space-y-4">
      
      <!-- HEADER DE LA ESTANCIA SELECCIONADA -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
        <div>
          <span id="room-badge" class="badge bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">PLANTA BAJA (±0,00 m)</span>
          <h2 id="room-title" class="text-xl font-black text-white mt-1">01. Zaguán Mudroom Térmico</h2>
        </div>
        <div class="text-right">
          <div id="room-dims" class="text-xs font-bold mono text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-3 py-1 rounded-xl">1,50 × 3,85 m · 5,80 m² útiles</div>
        </div>
      </div>

      <!-- BOTONES DE CAPAS (LAYERS) -->
      <div class="flex flex-wrap items-center justify-between gap-2 bg-slate-950 p-2.5 rounded-2xl border border-slate-800/80">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider pl-1">Capas CAD:</span>
        <div class="flex flex-wrap gap-1.5">
          <button onclick="toggleLayer('furn')" id="btn-layer-furn" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-slate-700 text-white border border-slate-600 transition">🛋️ Muebles: ON</button>
          <button onclick="toggleLayer('elec')" id="btn-layer-elec" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-600 text-white border border-amber-500 transition">🔌 Enchufes / RJ45: ON</button>
          <button onclick="toggleLayer('sw')" id="btn-layer-sw" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white border border-blue-500 transition">💡 Interruptores / Luz: ON</button>
          <button onclick="toggleLayer('hvac')" id="btn-layer-hvac" class="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-600 text-white border border-emerald-500 transition">🌡️ Clima / Suelo: ON</button>
        </div>
      </div>

      <!-- LEYENDA TÉCNICA -->
      <div class="flex flex-wrap items-center gap-3 text-[11px] bg-slate-950/80 border border-slate-800 rounded-xl px-3 py-2 text-slate-300">
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500 inline-block border border-amber-800"></span> <strong>E#</strong> Enchufe 16A/25A</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-purple-600 inline-block"></span> <strong>RJ#</strong> Red Cat 6A / WiFi</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-600 inline-block"></span> <strong>I#</strong> Interruptor / Conmutado</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-rose-600 inline-block"></span> <strong>T / TR</strong> Termostato / Toallero</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-teal-500 inline-block"></span> <strong>VMC</strong> Impulsión / Extracción</span>
        <span class="ml-auto text-[10px] font-bold text-sky-400">💡 Haz clic en cualquier símbolo del plano para inspeccionarlo</span>
      </div>

      <!-- CANVAS SVG 1:20 -->
      <div class="w-full overflow-x-auto bg-[#0a0f1d] border border-slate-800 rounded-2xl p-3 flex justify-center shadow-inner">
        <svg id="room-svg" viewBox="0 0 840 680" class="w-full max-w-[840px] h-auto select-none"></svg>
      </div>

      <!-- 4 PAREDES (COLINDANCIAS) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <div class="font-bold text-sky-400">⬆️ Pared Norte (Arriba):</div>
          <p id="wall-N" class="text-slate-300 mt-1"></p>
        </div>
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <div class="font-bold text-amber-400">⬇️ Pared Sur (Abajo · Soleamiento):</div>
          <p id="wall-S" class="text-slate-300 mt-1"></p>
        </div>
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <div class="font-bold text-emerald-400">➡️ Pared Este (Derecha):</div>
          <p id="wall-E" class="text-slate-300 mt-1"></p>
        </div>
        <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
          <div class="font-bold text-purple-400">⬅️ Pared Oeste (Izquierda):</div>
          <p id="wall-W" class="text-slate-300 mt-1"></p>
        </div>
      </div>

    </div>

    <!-- COLUMNA DERECHA (5 COLS): INSPECTOR & DESGLOSE TÉCNICO -->
    <div class="xl:col-span-5 space-y-4">

      <!-- DETALLE DEL ELEMENTO SELECCIONADO AL HACER CLIC -->
      <div id="clicked-item-box" class="bg-gradient-to-r from-sky-950/80 to-indigo-950/80 border-2 border-sky-500/60 rounded-2xl p-4 shadow-xl">
        <div class="text-[11px] font-bold uppercase tracking-wider text-sky-400">🎯 Elemento Seleccionado en el Plano CAD</div>
        <div id="clicked-item-title" class="text-base font-extrabold text-white mt-0.5">Haz clic en cualquier aparato, enchufe o interruptor</div>
        <div id="clicked-item-desc" class="text-xs text-slate-300 mt-1">Verás aquí su altura exacta de montaje ($h$ in cm), circuito eléctrico y especificación completa.</div>
      </div>

      <!-- 1. SPACE PLANNING & MOBILIARIO -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg space-y-2">
        <h3 class="text-xs font-black uppercase tracking-wider text-sky-400 flex items-center justify-between">
          <span>🛋️ 1. Mobiliario, Antropometría &amp; Ergonomía</span>
          <span id="count-furn" class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 mono text-[11px]"></span>
        </h3>
        <div id="list-furn" class="space-y-1.5 max-h-[220px] overflow-y-auto pr-1 text-xs"></div>
      </div>

      <!-- 2. ENCHUFES Y RJ45 -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg space-y-2">
        <h3 class="text-xs font-black uppercase tracking-wider text-amber-400 flex items-center justify-between">
          <span>🔌 2. Enchufes, Alturas ($h$) y Red RJ45 Cat 6A</span>
          <span id="count-elec" class="px-2 py-0.5 rounded bg-amber-950 text-amber-300 mono text-[11px]"></span>
        </h3>
        <div id="list-elec" class="space-y-1.5 max-h-[220px] overflow-y-auto pr-1 text-xs"></div>
      </div>

      <!-- 3. INTERRUPTORES Y LUZ -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg space-y-2">
        <h3 class="text-xs font-black uppercase tracking-wider text-blue-400 flex items-center justify-between">
          <span>💡 3. Interruptores, Conmutadores &amp; Iluminación IES</span>
          <span id="count-sw" class="px-2 py-0.5 rounded bg-blue-950 text-blue-300 mono text-[11px]"></span>
        </h3>
        <div id="list-sw" class="space-y-1.5 max-h-[190px] overflow-y-auto pr-1 text-xs"></div>
      </div>

      <!-- 4. CLIMA INVISIBLE -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg space-y-2">
        <h3 class="text-xs font-black uppercase tracking-wider text-emerald-400 flex items-center justify-between">
          <span>🌡️ 4. Suelo Radiante-Refrescante &amp; VMC Zehnder</span>
          <span id="count-hvac" class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 mono text-[11px]"></span>
        </h3>
        <div id="list-hvac" class="space-y-1.5 text-xs"></div>
      </div>

      <!-- 5. MATERIALES & MUNSELL/NCS -->
      <div class="bg-slate-950 border border-slate-800/80 rounded-2xl p-4 space-y-2 text-xs">
        <div class="text-[11px] font-bold uppercase tracking-wider text-purple-400">🎨 Materiales &amp; Paleta Munsell / NCS</div>
        <p id="room-materials" class="text-slate-300"></p>
        <div class="text-[11px] font-bold uppercase tracking-wider text-yellow-400 pt-1">💡 Especificación Lumínica IES</div>
        <p id="room-lighting" class="text-slate-300"></p>
      </div>

    </div>
  </div>

  <script>
    const ROOMS_DATA = __ROOMS_DATA_JSON__;

    let currentFilter = 'ALL';
    let currentRoomId = 'r01';
    let selectedMarkerCode = null;
    const layers = { furn: true, elec: true, sw: true, hvac: true };

    function setFloorFilter(fl) {
      currentFilter = fl;
      ['ALL', 'PB', 'P1'].forEach(k => {
        const btn = document.getElementById('filter-' + k);
        if (k === fl) {
          btn.className = 'px-3.5 py-2 rounded-xl text-xs font-bold border border-sky-500 bg-sky-600 text-white shadow-lg transition';
        } else {
          btn.className = 'px-3.5 py-2 rounded-xl text-xs font-semibold border border-slate-800 bg-slate-800 text-slate-300 hover:text-white transition';
        }
      });
      renderPills();
      const visible = ROOMS_DATA.filter(r => currentFilter === 'ALL' || r.fl === currentFilter);
      if (!visible.some(r => r.id === currentRoomId)) {
        selectRoom(visible[0].id);
      }
    }

    function toggleLayer(k) {
      layers[k] = !layers[k];
      const colors = { furn: 'bg-slate-700', elec: 'bg-amber-600', sw: 'bg-blue-600', hvac: 'bg-emerald-600' };
      const labels = { furn: '🛋️ Muebles', elec: '🔌 Enchufes / RJ45', sw: '💡 Interruptores / Luz', hvac: '🌡️ Clima / Suelo' };
      const btn = document.getElementById('btn-layer-' + k);
      if (layers[k]) {
        btn.className = `px-2.5 py-1 rounded-lg text-xs font-bold text-white border transition ${colors[k]}`;
        btn.textContent = `${labels[k]}: ON`;
      } else {
        btn.className = 'px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-800 text-slate-500 border border-slate-700 transition';
        btn.textContent = `${labels[k]}: OFF`;
      }
      renderCurrentRoom();
    }

    function renderPills() {
      const nav = document.getElementById('room-pills');
      const visible = ROOMS_DATA.filter(r => currentFilter === 'ALL' || r.fl === currentFilter);
      nav.innerHTML = visible.map(r => {
        const active = r.id === currentRoomId;
        const badgeCol = r.fl === 'PB' ? 'bg-sky-500/20 text-sky-400' : 'bg-indigo-500/20 text-indigo-400';
        return `<button onclick="selectRoom('${r.id}')" class="room-btn px-3 py-1.5 rounded-xl text-xs font-medium border transition flex items-center gap-1.5 ${
          active ? 'active' : 'bg-slate-900 text-slate-300 border-slate-800 hover:border-slate-700'
        }">
          <span class="badge ${active ? 'bg-white text-slate-900 font-extrabold' : badgeCol}">${r.fl}</span>
          <span>${r.short}</span>
        </button>`;
      }).join('');
    }

    function selectRoom(id) {
      currentRoomId = id;
      selectedMarkerCode = null;
      renderPills();
      renderCurrentRoom();
    }

    function selectMarker(code) {
      selectedMarkerCode = code;
      renderCurrentRoom();
      highlightClickedItem(code);
    }

    function highlightClickedItem(code) {
      const room = ROOMS_DATA.find(r => r.id === currentRoomId);
      if (!room) return;
      let item = (room.furn || []).find(x => x.code === code) ||
                 (room.elec || []).find(x => x.code === code) ||
                 (room.sw || []).find(x => x.code === code) ||
                 (room.hvac || []).find(x => x.code === code);
      if (item) {
        document.getElementById('clicked-item-title').textContent = `${item.code} · ${item.name}`;
        const hText = item.h_cm ? ` | Altura: ${item.h_cm} cm` : '';
        const cirText = item.cir ? ` | Circuito: ${item.cir}` : '';
        document.getElementById('clicked-item-desc').textContent = `${item.desc || ''}${hText}${cirText}`;
      }
    }

    function renderCurrentRoom() {
      const room = ROOMS_DATA.find(r => r.id === currentRoomId) || ROOMS_DATA[0];

      document.getElementById('room-badge').textContent = room.fl === 'PB' ? 'PLANTA BAJA (±0,00 m)' : 'PLANTA PRIMERA (+3,15 m)';
      document.getElementById('room-badge').className = room.fl === 'PB'
        ? 'badge bg-sky-500/20 text-sky-400 border border-sky-500/30'
        : 'badge bg-indigo-500/20 text-indigo-400 border border-indigo-500/30';

      document.getElementById('room-title').textContent = room.title;
      document.getElementById('room-dims').textContent = room.dims;

      document.getElementById('wall-N').textContent = room.wN || 'Colindancia Norte';
      document.getElementById('wall-S').textContent = room.wS || 'Colindancia Sur';
      document.getElementById('wall-E').textContent = room.wE || 'Colindancia Este';
      document.getElementById('wall-W').textContent = room.wW || 'Colindancia Oeste';

      document.getElementById('room-materials').textContent = room.materials || 'Materiales según memoria técnica.';
      document.getElementById('room-lighting').textContent = room.lighting || 'Iluminación según estándar IES.';

      renderRoomSVG(room);
      renderLists(room);
    }

    function renderRoomSVG(room) {
      const svg = document.getElementById('room-svg');
      const W = 840, H = 680;
      const padX = 100, padY = 90;
      const availW = W - padX * 2;
      const availH = H - padY * 2;
      const scale = Math.min(availW / room.w, availH / room.h);
      const rw = room.w * scale;
      const rh = room.h * scale;
      const ox = (W - rw) / 2;
      const oy = (H - rh) / 2;

      const px = x => ox + x * scale;
      const py = y => oy + y * scale;

      let out = `
        <defs>
          <pattern id="cadGrid" width="${scale * 0.5}" height="${scale * 0.5}" patternUnits="userSpaceOnUse" x="${ox}" y="${oy}">
            <path d="M ${scale * 0.5} 0 L 0 0 0 ${scale * 0.5}" fill="none" stroke="#1e293b" stroke-width="0.8"/>
          </pattern>
          <pattern id="radiantLoops" width="28" height="28" patternUnits="userSpaceOnUse" x="${ox}" y="${oy}">
            <path d="M 4 0 L 4 24 Q 4 28 8 28 L 14 28 Q 18 28 18 24 L 18 4 Q 18 0 22 0 L 28 0" fill="none" stroke="#f43f5e" stroke-width="1.3" stroke-dasharray="4,3" opacity="0.32"/>
          </pattern>
        </defs>
      `;

      // Cardinal Labels
      out += `
        <text x="${W / 2}" y="26" text-anchor="middle" font-size="11" font-weight="800" fill="#94a3b8">⬆️ NORTE (Arriba en plano)</text>
        <text x="${W / 2}" y="${H - 14}" text-anchor="middle" font-size="11" font-weight="800" fill="#94a3b8">⬇️ SUR (Abajo · Soleamiento y Jardín)</text>
        <text x="18" y="${H / 2}" text-anchor="middle" font-size="11" font-weight="800" fill="#94a3b8" transform="rotate(-90 18 ${H / 2})">⬅️ OESTE</text>
        <text x="${W - 18}" y="${H / 2}" text-anchor="middle" font-size="11" font-weight="800" fill="#94a3b8" transform="rotate(90 ${W - 18} ${H / 2})">➡️ ESTE</text>
      `;

      // Room Floor & Grid
      out += `
        <rect x="${ox}" y="${oy}" width="${rw}" height="${rh}" fill="#0f172a" />
        <rect x="${ox}" y="${oy}" width="${rw}" height="${rh}" fill="url(#cadGrid)" />
      `;

      // Radiant Floor Loops
      if (layers.hvac && room.id !== 'r05' && room.id !== 'r10' && room.id !== 'r17') {
        out += `
          <rect x="${ox + 12}" y="${oy + 12}" width="${rw - 24}" height="${rh - 24}" rx="8" fill="url(#radiantLoops)" stroke="#fb7185" stroke-width="1" stroke-dasharray="5,4" opacity="0.55"/>
        `;
      }

      // Outer Structural Walls (thick stroke)
      out += `
        <rect x="${ox - 6}" y="${oy - 6}" width="${rw + 12}" height="${rh + 12}" fill="none" stroke="#334155" stroke-width="12" rx="4"/>
      `;

      // Cotas de Dimensiones
      out += `
        <line x1="${ox}" y1="${oy - 30}" x2="${ox + rw}" y2="${oy - 30}" stroke="#64748b" stroke-width="1.5"/>
        <line x1="${ox}" y1="${oy - 38}" x2="${ox}" y2="${oy - 22}" stroke="#64748b" stroke-width="1.5"/>
        <line x1="${ox + rw}" y1="${oy - 38}" x2="${ox + rw}" y2="${oy - 22}" stroke="#64748b" stroke-width="1.5"/>
        <rect x="${ox + rw / 2 - 45}" y="${oy - 42}" width="90" height="22" rx="6" fill="#0284c7"/>
        <text x="${ox + rw / 2}" y="${oy - 27}" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff" class="mono">${room.w.toFixed(2).replace('.', ',')} m</text>

        <line x1="${ox - 30}" y1="${oy}" x2="${ox - 30}" y2="${oy + rh}" stroke="#64748b" stroke-width="1.5"/>
        <line x1="${ox - 38}" y1="${oy}" x2="${ox - 22}" y2="${oy}" stroke="#64748b" stroke-width="1.5"/>
        <line x1="${ox - 38}" y1="${oy + rh}" x2="${ox - 22}" y2="${oy + rh}" stroke="#64748b" stroke-width="1.5"/>
        <g transform="translate(${ox - 30}, ${oy + rh / 2}) rotate(-90)">
          <rect x="-45" y="-11" width="90" height="22" rx="6" fill="#0284c7"/>
          <text x="0" y="4" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff" class="mono">${room.h.toFixed(2).replace('.', ',')} m</text>
        </g>
      `;

      // Openings (Doors, Windows, Sliding Doors)
      (room.openings || []).forEach(op => {
        const isHoriz = op.wall === 'N' || op.wall === 'S';
        const x1 = isHoriz ? px(op.pos) : (op.wall === 'W' ? ox - 6 : ox + rw + 6);
        const y1 = isHoriz ? (op.wall === 'N' ? oy - 6 : oy + rh + 6) : py(op.pos);
        const lenPx = op.len * scale;

        let fillCol = '#1e293b';
        let strokeCol = '#38bdf8';
        if (op.type === 'sliding') { fillCol = '#fef3c7'; strokeCol = '#f59e0b'; }
        else if (op.type === 'door') { fillCol = '#f8fafc'; strokeCol = '#10b981'; }
        else if (op.type === 'open') { fillCol = '#0f172a'; strokeCol = '#64748b'; }

        if (isHoriz) {
          out += `<rect x="${x1}" y="${y1 - 7}" width="${lenPx}" height="14" fill="${fillCol}" stroke="${strokeCol}" stroke-width="2" rx="2"/>`;
          if (op.type === 'sliding') {
            out += `<line x1="${x1 + 6}" y1="${y1}" x2="${x1 + lenPx - 6}" y2="${y1}" stroke="${strokeCol}" stroke-width="2.5" stroke-dasharray="6,3"/>`;
          }
          const ly = op.wall === 'N' ? y1 - 12 : y1 + 22;
          out += `<text x="${x1 + lenPx / 2}" y="${ly}" text-anchor="middle" font-size="10" font-weight="700" fill="${strokeCol}">${op.label}</text>`;
        } else {
          out += `<rect x="${x1 - 7}" y="${y1}" width="14" height="${lenPx}" fill="${fillCol}" stroke="${strokeCol}" stroke-width="2" rx="2"/>`;
          if (op.type === 'sliding') {
            out += `<line x1="${x1}" y1="${y1 + 6}" x2="${x1}" y2="${y1 + lenPx - 6}" stroke="${strokeCol}" stroke-width="2.5" stroke-dasharray="6,3"/>`;
          }
          const lx = op.wall === 'W' ? x1 - 14 : x1 + 14;
          out += `<text x="${lx}" y="${y1 + lenPx / 2}" text-anchor="middle" font-size="10" font-weight="700" fill="${strokeCol}" transform="rotate(-90 ${lx} ${y1 + lenPx / 2})">${op.label}</text>`;
        }
      });

      // 1. Furniture
      if (layers.furn) {
        (room.furn || []).forEach(f => {
          const fx = px(f.x), fy = py(f.y), fw = f.w * scale, fh = f.h * scale;
          const isSel = selectedMarkerCode === f.code;
          const dashAttr = f.dashed ? 'stroke-dasharray="6,4"' : '';
          const selClass = isSel ? 'marker-selected' : '';
          out += `
            <g class="marker-node ${selClass}" onclick="selectMarker('${f.code}')">
              <rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" rx="5" fill="${f.col}" stroke="${f.str}" stroke-width="${isSel ? 3 : 1.8}" ${dashAttr} fill-opacity="${f.col === 'none' ? 0 : 0.85}"/>
              <rect x="${fx + 3}" y="${fy + 3}" width="${Math.min(fw - 6, 44)}" height="16" rx="3" fill="${f.str}"/>
              <text x="${fx + 3 + Math.min(fw - 6, 44) / 2}" y="${fy + 14}" text-anchor="middle" font-size="9" font-weight="800" fill="#ffffff" class="mono">${f.code}</text>
              ${fw > 60 && fh > 32 ? `<text x="${fx + fw / 2}" y="${fy + fh / 2 + 5}" text-anchor="middle" font-size="10" font-weight="700" fill="#f8fafc">${f.name.split('(')[0].substring(0, 24)}</text>` : ''}
            </g>
          `;
        });
      }

      // 2. Switches & Lighting
      if (layers.sw) {
        (room.sw || []).forEach(s => {
          const sx = px(s.x), sy = py(s.y);
          const isSel = selectedMarkerCode === s.code;
          out += `
            <g class="marker-node ${isSel ? 'marker-selected' : ''}" onclick="selectMarker('${s.code}')">
              <circle cx="${sx}" cy="${sy}" r="12" fill="#2563eb" stroke="#ffffff" stroke-width="2"/>
              <text x="${sx}" y="${sy + 3.5}" text-anchor="middle" font-size="9" font-weight="800" fill="#ffffff" class="mono">${s.code}</text>
            </g>
          `;
        });
      }

      // 3. HVAC
      if (layers.hvac) {
        (room.hvac || []).forEach(h => {
          if (h.isFloor) return;
          const hx = px(h.x), hy = py(h.y);
          const isSel = selectedMarkerCode === h.code;
          const bg = h.isVMC ? '#0d9488' : '#e11d48';
          out += `
            <g class="marker-node ${isSel ? 'marker-selected' : ''}" onclick="selectMarker('${h.code}')">
              <rect x="${hx - 15}" y="${hy - 11}" width="30" height="22" rx="6" fill="${bg}" stroke="#ffffff" stroke-width="2"/>
              <text x="${hx}" y="${hy + 3.5}" text-anchor="middle" font-size="8.5" font-weight="800" fill="#ffffff" class="mono">${h.code}</text>
            </g>
          `;
        });
      }

      // 4. Electrical & RJ45
      if (layers.elec) {
        (room.elec || []).forEach(e => {
          const ex = px(e.x), ey = py(e.y);
          const isSel = selectedMarkerCode === e.code;
          const bg = e.isRJ ? '#7c3aed' : '#d97706';
          out += `
            <g class="marker-node ${isSel ? 'marker-selected' : ''}" onclick="selectMarker('${e.code}')">
              <circle cx="${ex}" cy="${ey}" r="12" fill="${bg}" stroke="#ffffff" stroke-width="2"/>
              <text x="${ex}" y="${ey + 3.5}" text-anchor="middle" font-size="8.5" font-weight="800" fill="#ffffff" class="mono">${e.code}</text>
            </g>
          `;
        });
      }

      svg.innerHTML = out;
    }

    function renderLists(room) {
      // 1. Furniture list
      const listFurn = document.getElementById('list-furn');
      const furnItems = room.furn || [];
      document.getElementById('count-furn').textContent = `${furnItems.length} elementos`;
      listFurn.innerHTML = furnItems.map(f => `
        <div onclick="selectMarker('${f.code}')" class="p-2 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition cursor-pointer flex items-start gap-2 ${selectedMarkerCode === f.code ? 'border-sky-500 bg-sky-950/40' : ''}">
          <span class="px-1.5 py-0.5 rounded bg-slate-800 text-sky-400 font-bold mono text-[10px] shrink-0">${f.code}</span>
          <div>
            <div class="font-bold text-slate-200 text-xs">${f.name}</div>
            <div class="text-[11px] text-slate-400 mt-0.5">${f.desc || ''}</div>
          </div>
        </div>
      `).join('');

      // 2. Elec list
      const listElec = document.getElementById('list-elec');
      const elecItems = room.elec || [];
      document.getElementById('count-elec').textContent = `${elecItems.length} tomas`;
      listElec.innerHTML = elecItems.map(e => `
        <div onclick="selectMarker('${e.code}')" class="p-2 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition cursor-pointer flex items-start gap-2 ${selectedMarkerCode === e.code ? 'border-amber-500 bg-amber-950/40' : ''}">
          <span class="px-1.5 py-0.5 rounded ${e.isRJ ? 'bg-purple-900/60 text-purple-300' : 'bg-amber-900/60 text-amber-300'} font-bold mono text-[10px] shrink-0">${e.code}</span>
          <div>
            <div class="font-bold text-slate-200 text-xs">${e.name} <span class="text-amber-400 font-mono text-[11px]">(h = ${e.h_cm} cm)</span></div>
            <div class="text-[11px] text-slate-400 mt-0.5">${e.desc || ''} <span class="text-slate-500">· Circuito: ${e.cir}</span></div>
          </div>
        </div>
      `).join('');

      // 3. Switch list
      const listSw = document.getElementById('list-sw');
      const swItems = room.sw || [];
      document.getElementById('count-sw').textContent = `${swItems.length} mecanismos`;
      listSw.innerHTML = swItems.map(s => `
        <div onclick="selectMarker('${s.code}')" class="p-2 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition cursor-pointer flex items-start gap-2 ${selectedMarkerCode === s.code ? 'border-blue-500 bg-blue-950/40' : ''}">
          <span class="px-1.5 py-0.5 rounded bg-blue-900/60 text-blue-300 font-bold mono text-[10px] shrink-0">${s.code}</span>
          <div>
            <div class="font-bold text-slate-200 text-xs">${s.name} <span class="text-blue-400 font-mono text-[11px]">(h = ${s.h_cm} cm)</span></div>
            <div class="text-[11px] text-slate-400 mt-0.5">${s.desc || ''}</div>
          </div>
        </div>
      `).join('');

      // 4. HVAC list
      const listHvac = document.getElementById('list-hvac');
      const hvacItems = room.hvac || [];
      document.getElementById('count-hvac').textContent = `${hvacItems.length} circuitos`;
      listHvac.innerHTML = hvacItems.map(h => `
        <div onclick="selectMarker('${h.code}')" class="p-2 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition cursor-pointer flex items-start gap-2 ${selectedMarkerCode === h.code ? 'border-emerald-500 bg-emerald-950/40' : ''}">
          <span class="px-1.5 py-0.5 rounded ${h.isVMC ? 'bg-teal-900/60 text-teal-300' : 'bg-rose-900/60 text-rose-300'} font-bold mono text-[10px] shrink-0">${h.code}</span>
          <div>
            <div class="font-bold text-slate-200 text-xs">${h.name}</div>
            <div class="text-[11px] text-slate-400 mt-0.5">${h.desc || ''}</div>
          </div>
        </div>
      `).join('');
    }

    // Inicialización
    renderPills();
    renderCurrentRoom();
  </script>
</body>
</html>
"""

def main():
    json_rooms = json.dumps(ROOMS, ensure_ascii=False)
    html_content = HTML_TEMPLATE.replace("__ROOMS_DATA_JSON__", json_rooms)
    
    # Save to propuestas/
    target_path = "/home/antigravity/landslore/oleiros/propuestas/fichas_zoom_interactivas_propuesta_d.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {target_path} ({len(html_content)} bytes)")
    
    # Save to artifacts directory
    artifact_path = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/e8f6a578-76cf-4abb-986f-afb074438ab7/fichas_zoom_propuesta_d.html"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Artifact updated: {artifact_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
