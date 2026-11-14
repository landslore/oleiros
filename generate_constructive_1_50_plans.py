#!/usr/bin/env python3
"""
Generador de Planos Constructivos de Ejecución e Instalaciones a Escala 1:50 (Planta Baja)
Propuesta D — Pabellón Bioclimático con Patio Central (Corrala Contemporánea)
Produce:
  - plano_constructivo_zona_norte_pb.svg (Plano E-01: Zona Norte PB 1:50)
  - plano_constructivo_centro_patio_cocina_pb.svg (Plano E-02: Banda Central PB 1:50)
  - plano_constructivo_sur_salon_porche_pb.svg (Plano E-03: Zona Sur y Piscina PB 1:50)
"""
import os
from cad_engine import (
    fmt_m, svg_defs, draw_grid_axes, draw_pillars, draw_wall,
    dim_h, dim_v, door_swing, sliding_door, window_cad,
    room_stamp, nhg_circle, wc_cad, sink_cad, shower_cad,
    bed_cad, wardrobe_cad, mep_symbol, north_and_scale, title_block,
    sanitize_svg_text
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def mep_legend_panel(x: float, y: float, w: float) -> str:
    """Draws normalized MEP & Constructive CAD Legend Panel for 1:50 execution sheets."""
    out = [f'<g transform="translate({x},{y})" font-family="monospace">']
    out.append(f'<rect x="0" y="0" width="{w}" height="430" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append(f'<rect x="0" y="0" width="{w}" height="24" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15.5" fill="#38bdf8" font-size="8.0" font-weight="700">LEYENDA TÉCNICA DE INSTALACIONES Y SECCIÓN CONSTRUCTIVA (ESCALA 1:50)</text>')

    items = [
        ("ELÉCTRICA BT (REBT ITC-BT-25)", "#f59e0b", [
            ("C1 · Alumbrado interior/exterior (1,5 mm² · PIA 10A)", "Puntos de luz conmutados / DALI / LED 2700K"),
            ("C2 · Tomas uso general Schuko 16A (2,5 mm² · PIA 16A)", "Mecanismos empotrados h=30 cm / h=110 cm"),
            ("C3 · Cocina: Inducción Bora Pure + Horno (6 mm² · PIA 25A)", "Toma trifásica/monofásica dedicada en isla"),
            ("C4 · Lavadora / Secadora / Lavavajillas / Termo (2,5 mm² · 16A)", "Tomas húmedas independientes con dif. 30mA"),
            ("C5 · Tomas baños y encimera cocina (2,5 mm² · PIA 16A)", "Distancia seguridad > 0,60 m volumen ducha"),
            ("C10/C11 · Aerotermia Vaillant + Wallbox VE 7,4kW (6 mm² · 32A)", "Protección diferencial Tipo A / Rearme auto"),
        ]),
        ("TELECOMUNICACIONES Y DOMÓTICA (ICT / KNX)", "#6366f1", [
            ("Red Datos RJ45 Cat 6A F/UTP Libre Halógenos", "Doble toma en Despacho, Salón TV y Dormitorios"),
            ("Rack Mural 19\" 9U en Sala Técnica (Switch PoE 16p)", "Puntos de Acceso WiFi 6E en techo PB y P1"),
            ("Termostatos KNX / Sondas CO2 + HR por zona", "Control de cabezales electroválvulas colector SR"),
        ]),
        ("FONTANERÍA Y SANEAMIENTO (CTE DB-HS4 / HS5)", "#3b82f6", [
            ("Tubería Multicapa PEX-Al-PEX Ø20/Ø16 mm AF (Azul) / ACS (Rojo)", "Colectores con llaves de corte en cada cuarto húmedo"),
            ("Retorno ACS Ø16 mm con bomba recirculación inteligente", "Agua caliente instantánea en griferías ≤ 3 seg"),
            ("Saneamiento PVC Serie B Insonorizado Ø110 mm / Ø50 mm", "Pendiente mín. 2% a arquetas registrables exteriores"),
        ]),
        ("VENTILACIÓN MECÁNICA VMC DOBLE FLUJO (CTE DB-HS3)", "#06b6d4", [
            ("Recuperador Zehnder ComfoAir Q350 (η = 92% · Passivhaus)", "Ubicado en Sala Técnica con silenciadores"),
            ("Impulsión aire limpio filtrado F7 (Conducto PEAD Ø90 mm)", "Bocas en Salón, Comedor, Despacho y Dormitorios"),
            ("Extracción aire viciado húmedo (Conducto PEAD Ø90/Ø125 mm)", "Bocas en Cocina, Baños, Lavandería y Zaguán"),
        ]),
        ("SECCIÓN DE MUROS Y CARPINTERÍA (CTE DB-HE1)", "#94a3b8", [
            ("Muro F1 SATE (e=41,5 cm · U = 0,18 W/m²K)", "1,5cm SATE + 16cm EPS-G + 20cm Termoarcilla + 4cm trasdosado"),
            ("Muro F2 Granito (e=45,5 cm · U = 0,18 W/m²K)", "10cm Granito Silvestre + 3cm cámara + 14cm XPS + 15cm HA"),
            ("Tabiquería Acústica PYL (e=10 / 12 cm · Rw ≥ 50 dB)", "Doble placa 12,5+12,5 mm por cara + Lana mineral 70 kg/m³"),
        ]),
    ]
    cy = 40
    for cat_title, color, rows in items:
        out.append(f'<rect x="12" y="{cy-9}" width="6" height="6" fill="{color}"/>')
        out.append(f'<text x="24" y="{cy-3}" fill="{color}" font-size="6.8" font-weight="700">{cat_title}</text>')
        cy += 11
        for k, v in rows:
            out.append(f'<text x="20" y="{cy}" fill="#e2e8f0" font-size="6.0" font-weight="700">• {k}</text>')
            out.append(f'<text x="28" y="{cy+9}" fill="#94a3b8" font-size="5.6">{v}</text>')
            cy += 21
        cy += 5

    out.append('</g>')
    return "\n".join(out)


# ==============================================================================
# PLANO E-01: ZONA NORTE PB (ESCALA 1:50)
# ==============================================================================
def build_zona_norte_pb_svg() -> str:
    W, H = 1800, 1240
    S = 75.0  # 1m = 75px (gran formato 1:50 de alta precisión)
    OX = 85.0  # X=2.5m plot starts near OX
    OY = 85.0  # Y=3.0m plot starts near OY

    def px(xm: float) -> float:
        return OX + (xm - 2.50) * S

    def py(ym: float) -> float:
        return OY + (ym - 3.00) * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1180" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO E-01 · EJECUCIÓN E INSTALACIONES ZONA NORTE PLANTA BAJA (ESCALA 1:50)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Cotas de Albañilería al milímetro · Red Eléctrica C1-C11 · Datos Cat 6A · Fontanería PEX AF/ACS · Saneamiento PVC · Conductos VMC PEAD</text>',
    ]

    # Grid background in drawing viewport
    out.append(f'<rect x="28" y="68" width="1180" height="995" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')

    # Structural Axes inside North Zone
    x_axes = [("A", 3.00), ("B", 8.00), ("C", 12.00), ("D", 14.00), ("E", 17.00)]
    y_axes = [("1", 5.00), ("2", 9.00), ("3", 13.00)]
    out.append(draw_grid_axes(x_axes, y_axes, px(2.60), px(17.40), py(3.20), py(13.60), px, py))

    # Retranqueo 5.00m line
    out.append(f'<line x1="{px(2.70):.1f}" y1="{py(5.00):.1f}" x2="{px(17.30):.1f}" y2="{py(5.00):.1f}" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="10,5"/>')
    out.append(f'<text x="{px(14.25):.1f}" y="{py(4.85):.1f}" fill="#ef4444" font-family="monospace" font-size="7.0" font-weight="700">LÍNEA RETRANQUEO FRONTAL 5,00 m (PGOM)</text>')

    # Floor Fills & Textures
    # 01. Pérgola Garaje (X=3.00..8.00, Y=3.60..9.20 -> 5.00 x 5.60 = 28.00 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(3.60):.1f}" width="{5.00*S:.1f}" height="{5.60*S:.1f}" fill="#0f172a" stroke="#64748b" stroke-width="1.5" stroke-dasharray="10,5"/>')
    for gx in [3.50, 4.00, 4.50, 5.00, 5.50, 6.00, 6.50, 7.00, 7.50]:
        out.append(f'<line x1="{px(gx):.1f}" y1="{py(3.60):.1f}" x2="{px(gx):.1f}" y2="{py(9.20):.1f}" stroke="#334155" stroke-width="0.9" stroke-dasharray="6,4"/>')

    # Technical CAD vehicles (2 plazas 2.50 x 5.00m)
    for vx, vlabel in [(3.25, "PLAZA APARCAMIENTO 01 (VE)"), (5.65, "PLAZA APARCAMIENTO 02")]:
        out.append(f'<g opacity="0.65">')
        out.append(f'<rect x="{px(vx):.1f}" y="{py(4.00):.1f}" width="{2.05*S:.1f}" height="{4.60*S:.1f}" rx="8" fill="none" stroke="#64748b" stroke-width="1.1" stroke-dasharray="8,4"/>')
        out.append(f'<rect x="{px(vx+0.18):.1f}" y="{py(4.75):.1f}" width="{1.69*S:.1f}" height="{2.30*S:.1f}" rx="4" fill="none" stroke="#475569" stroke-width="0.8"/>')
        out.append(f'<line x1="{px(vx):.1f}" y1="{py(4.00):.1f}" x2="{px(vx+2.05):.1f}" y2="{py(8.60):.1f}" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="{px(vx+1.02):.1f}" y="{py(6.00):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="6.0">{vlabel}</text>')
        out.append('</g>')

    # 02. Porche Norte Cubierto (X=8.00..10.35, Y=3.50..5.00 -> 2.35 x 1.50 = 3.50 m²)
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(3.50):.1f}" width="{2.35*S:.1f}" height="{1.50*S:.1f}" fill="url(#hatch-tile-60)" stroke="#94a3b8" stroke-width="1.3" stroke-dasharray="6,3"/>')
    # Peldaño +0.05m y felpudo técnico empotrado
    out.append(f'<rect x="{px(8.35):.1f}" y="{py(4.45):.1f}" width="{1.50*S:.1f}" height="{0.45*S:.1f}" fill="url(#hatch-gravel)" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(9.10):.1f}" y="{py(4.71):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="5.5">FELPUDO DRENANTE EMPOTRADO</text>')

    # Interior North Band Rooms (X=8.00..17.00, Y=5.00..9.00)
    # 03. Zaguán / Mudroom: X=8.00..9.45, Y=5.00..9.00 (1.45 x 4.00 = 5.80 m²)
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(5.00):.1f}" width="{1.45*S:.1f}" height="{4.00*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')
    # 04. Hall / Distribuidor: X=9.45..12.05, Y=5.00..9.00 (2.60 x 4.00 = 10.40 m²)
    out.append(f'<rect x="{px(9.45):.1f}" y="{py(5.00):.1f}" width="{2.60*S:.1f}" height="{4.00*S:.1f}" fill="#131c31" stroke="none"/>')
    # 05. Despacho: X=12.05..14.925, Y=5.00..9.00 (2.875 x 4.00 = 11.50 m²)
    out.append(f'<rect x="{px(12.05):.1f}" y="{py(5.00):.1f}" width="{2.875*S:.1f}" height="{4.00*S:.1f}" fill="#131c31" stroke="none"/>')
    # Distribuidor previo a Baño PB: X=14.925..15.70, Y=5.00..9.00 (0.775 x 4.00)
    out.append(f'<rect x="{px(14.925):.1f}" y="{py(5.00):.1f}" width="{0.775*S:.1f}" height="{4.00*S:.1f}" fill="#131c31" stroke="none"/>')
    # 06. Baño PB: X=15.70..17.00, Y=5.00..9.00 (1.30 x 4.00 = 5.20 m²)
    out.append(f'<rect x="{px(15.70):.1f}" y="{py(5.00):.1f}" width="{1.30*S:.1f}" height="{4.00*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # Reference preview of Central Band below Y=9.00 (Y=9.00..12.80)
    # 10. Sala Técnica / Surf (X=3.00..5.05, Y=9.20..13.20)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(9.20):.1f}" width="{2.05*S:.1f}" height="{3.60*S:.1f}" fill="url(#hatch-tile-60)" opacity="0.55"/>')
    # 09. Escalera (X=5.05..8.00, Y=9.00..12.80)
    out.append(f'<rect x="{px(5.05):.1f}" y="{py(9.00):.1f}" width="{2.95*S:.1f}" height="{3.80*S:.1f}" fill="#0f172a" opacity="0.65"/>')
    # 00. Patio Central Corrala (X=8.00..12.00, Y=9.00..12.80)
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(9.00):.1f}" width="{4.00*S:.1f}" height="{3.80*S:.1f}" fill="url(#hatch-wood-deck)" opacity="0.75"/>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(11.00):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="8.0" font-weight="700">00. PATIO CENTRAL DESCUBIERTO (4,00 × 4,00 m)</text>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(11.25):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="6.5">Ver despiece constructivo completo en PLANO E-02</text>')

    # Exterior Multi-layer Walls (e = 0.40m = 30px at 1:50)
    tw_ext = 0.40 * S
    tw_int = 0.12 * S

    # North wall Y=5.00 from X=8.00 to 17.00
    out.append(draw_wall(px(8.00), py(5.00), px(17.00), py(5.00), tw_ext, True))
    # East wall X=17.00 from Y=5.00 to 12.80
    out.append(draw_wall(px(17.00), py(5.00), px(17.00), py(12.80), tw_ext, True))
    # West wall of Zaguán X=8.00 from Y=5.00 to 9.00
    out.append(draw_wall(px(8.00), py(5.00), px(8.00), py(9.00), tw_ext, True))
    # North wall of Stair/Tech X=3.00..8.00 at Y=9.00
    out.append(draw_wall(px(3.00), py(9.00), px(8.00), py(9.00), tw_ext, True))
    # West wall X=3.00 from Y=9.00 to 12.80
    out.append(draw_wall(px(3.00), py(9.00), px(3.00), py(12.80), tw_ext, True))

    # Interior Partitions (e=12cm acoustic PYL with double plate + mineral wool)
    out.append(draw_wall(px(9.45), py(5.00), px(9.45), py(9.00), tw_int, False))   # Zaguán | Hall
    out.append(draw_wall(px(12.05), py(5.00), px(12.05), py(9.00), tw_int, False)) # Hall | Despacho
    out.append(draw_wall(px(14.925), py(5.00), px(14.925), py(9.00), tw_int, False)) # Despacho | Dist Baño
    out.append(draw_wall(px(15.70), py(5.00), px(15.70), py(9.00), tw_int, False)) # Dist | Baño PB
    out.append(draw_wall(px(12.00), py(9.00), px(15.05), py(9.00), tw_int, False)) # Despacho | Cocina South
    out.append(draw_wall(px(5.05), py(9.00), px(5.05), py(12.80), tw_int, False))  # Sala Técnica | Escalera

    # Openings & Carpinterías CAD
    # C-01: Puerta Pivotante Acorazada Norte en Hall (X=9.60..10.80, Y=5.00)
    out.append(door_swing(px(9.60), py(5.00), 1.20*S, "down", "right", "C-01 PIVOT. 1,20×2,40"))
    # C-02: Puerta Técnica Peatonal Zaguán desde Garaje (X=8.00, Y=6.20..7.10)
    out.append(door_swing(px(8.00), py(6.20), 0.90*S, "right", "down", "C-02 0,90"))
    # Puerta interior estanca Zaguán -> Hall (X=9.45, Y=6.30..7.20)
    out.append(door_swing(px(9.45), py(6.30), 0.90*S, "right", "down", "P-01 0,90"))
    # C-05: Fijo + Corredera Vidrio Hall -> Patio Central (X=8.00..12.00, Y=9.00)
    out.append(sliding_door(px(8.00), py(9.00), 4.00*S, tw_ext*0.75, "h", 2, "C-05 VIDRIO PATIO 3,60×2,60 (Uw=0,85)"))
    # C-03: Ventana Norte Despacho (X=12.60..14.40, Y=5.00)
    out.append(window_cad(px(12.60), py(5.00), 1.80*S, tw_ext, "h", "C-03 1,80×1,20 (LUZ NORTE 90°)"))
    # Puerta Acústica Despacho (X=12.90..13.80, Y=9.00)
    out.append(door_swing(px(12.90), py(9.00), 0.90*S, "up", "right", "P-02 ACÚST. Rw≥38dB"))
    # Doble puerta corredera distribuidor previo Baño PB (cumplimiento NHG sin abrir a cocina/comedor)
    out.append(sliding_door(px(14.98), py(9.00), 0.70*S, tw_int, "h", 1, "P-03 CORR. 0,80"))
    out.append(sliding_door(px(15.70), py(6.80), 0.85*S, tw_int, "v", 1, "P-04 CORR. 0,82"))
    # C-04: Ventana Baño PB Fachada Este (X=17.00, Y=5.60..6.20)
    out.append(window_cad(px(17.00), py(5.60), 0.60*S, tw_ext, "v", "C-04 0,60×0,60"))

    # Detailed Technical Furniture & Built-in Carpentry
    # 03. Zaguán / Mudroom:
    # Armario ropero técnico Este (X=8.85..9.40, Y=5.15..6.20) + Sur (X=8.85..9.40, Y=7.30..8.85)
    out.append(wardrobe_cad(px(8.85), py(5.15), 0.55*S, 1.05*S, "v"))
    out.append(wardrobe_cad(px(8.85), py(7.30), 0.55*S, 1.55*S, "v"))
    # Banco descalzador con rejilla ventilada inferior (X=8.12..8.55, Y=7.30..8.80)
    out.append(f'<rect x="{px(8.12):.1f}" y="{py(7.30):.1f}" width="{0.43*S:.1f}" height="{1.50*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(8.33):.1f}" y="{py(8.05):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.5" transform="rotate(-90 {px(8.33):.1f} {py(8.05):.1f})">BANCO DESCALZADOR + CALEF.</text>')

    # 04. Hall:
    # Armario Gabanero empotrado (X=11.35..11.95, Y=5.15..6.95)
    out.append(wardrobe_cad(px(11.35), py(5.15), 0.60*S, 1.80*S, "v"))
    # Consola suspendida de roble (X=9.55..9.90, Y=7.40..8.60)
    out.append(f'<rect x="{px(9.55):.1f}" y="{py(7.40):.1f}" width="{0.35*S:.1f}" height="{1.20*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')

    # 05. Despacho / Estudio (Sanctasanctórum):
    # Mesa de trabajo perpendicular a ventana Norte (X=12.15..12.95, Y=5.40..7.20 -> luz Norte a 90° izquierda/derecha sin reflejos)
    out.append(f'<rect x="{px(12.15):.1f}" y="{py(5.40):.1f}" width="{0.80*S:.1f}" height="{1.80*S:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.1"/>')
    # Doble monitor CAD sobre soporte articulado
    out.append(f'<rect x="{px(12.28):.1f}" y="{py(5.65):.1f}" width="{0.14*S:.1f}" height="{0.55*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<rect x="{px(12.28):.1f}" y="{py(6.30):.1f}" width="{0.14*S:.1f}" height="{0.55*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.9"/>')
    # Silla ergonómica giratoria CAD
    out.append(f'<circle cx="{px(13.25):.1f}" cy="{py(6.30):.1f}" r="{0.28*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<path d="M {px(13.35):.1f},{py(6.05):.1f} A {0.28*S:.1f},{0.28*S:.1f} 0 0 1 {px(13.35):.1f},{py(6.55):.1f}" fill="none" stroke="#38bdf8" stroke-width="1.4"/>')
    # Librería acústica de suelo a techo en tabique Este (X=14.42..14.85, Y=5.20..8.80)
    out.append(wardrobe_cad(px(14.42), py(5.20), 0.43*S, 3.60*S, "v"))
    # Sillón lectura / sofá cama visitas (X=12.15..12.95, Y=7.55..8.45)
    out.append(f'<rect x="{px(12.15):.1f}" y="{py(7.55):.1f}" width="{0.80*S:.1f}" height="{0.90*S:.1f}" rx="3" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')

    # 06. Baño Cortesía PB:
    # Plato de ducha enrasado Walk-in (X=15.78..16.92, Y=5.12..6.02 -> 1.14 x 0.90 m)
    out.append(shower_cad(px(15.78), py(5.12), 1.14*S, 0.90*S))
    # Lavabo suspendido (X=16.38..16.88, Y=6.35..7.15)
    out.append(sink_cad(px(16.38), py(6.35), 0.50*S, 0.80*S, False))
    # Inodoro suspendido Geberit con cisterna oculta (X=16.22..16.88, Y=7.75..8.25)
    out.append(wc_cad(px(16.35), py(7.75), 0.42*S, 0.55*S, "left"))

    # NHG Ø1.50m Accessibility Circles
    out.append(nhg_circle(px(10.60), py(7.15), S, "Ø1,50m NHG"))
    out.append(nhg_circle(px(13.65), py(7.15), S, "Ø1,50m NHG"))
    out.append(nhg_circle(px(16.25), py(6.95), S, "Ø1,50m PB"))

    # Structural Pillars (25x25 cm)
    pillars = [(x, y) for x in [3.00, 8.00, 12.00, 14.00, 17.00] for y in [5.00, 9.00]] + [(3.00, 3.60), (8.00, 3.60)]
    out.append(draw_pillars(pillars, px, py, 0.25, S))

    # ==========================================================================
    # MEP INSTALLATIONS OVERLAY (1:50 HIGH PRECISION)
    # ==========================================================================
    # 1. Red de Fontanería PEX-Al-PEX AF (Azul) / ACS (Rojo) desde Sala Técnica (X=4.20, Y=9.50) hasta Baño PB (X=16.85)
    out.append('<g opacity="0.9">')
    # Tubería AF Ø20 mm
    out.append(f'<polyline points="{px(4.20):.1f},{py(9.50):.1f} {px(4.20):.1f},{py(8.85):.1f} {px(16.85):.1f},{py(8.85):.1f} {px(16.85):.1f},{py(5.40):.1f}" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="8,3"/>')
    # Tubería ACS Ø20 mm
    out.append(f'<polyline points="{px(4.35):.1f},{py(9.50):.1f} {px(4.35):.1f},{py(8.77):.1f} {px(16.77):.1f},{py(8.77):.1f} {px(16.77):.1f},{py(5.40):.1f}" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="8,3"/>')
    out.append(f'<text x="{px(11.00):.1f}" y="{py(8.70):.1f}" fill="#60a5fa" font-family="monospace" font-size="5.8" font-weight="700">MONTANTE FALSO TECHO PEX-Al-PEX Ø20 mm (AF + ACS + RETORNO)</text>')

    # Saneamiento PVC Ø110 mm Baño PB -> Arqueta Este (X=17.35, Y=8.10)
    out.append(f'<polyline points="{px(16.35):.1f},{py(8.00):.1f} {px(17.35):.1f},{py(8.00):.1f}" fill="none" stroke="#eab308" stroke-width="2.0" stroke-dasharray="5,3"/>')
    out.append(f'<rect x="{px(17.25):.1f}" y="{py(7.85):.1f}" width="16" height="16" fill="#0f172a" stroke="#eab308" stroke-width="1.4"/>')
    out.append(f'<text x="{px(17.25):.1f}" y="{py(8.35):.1f}" text-anchor="middle" fill="#eab308" font-family="monospace" font-size="5.5" font-weight="700">ARQ. SANEAM. Ø110</text>')

    # 2. Red VMC Doble Flujo (Zehnder ComfoAir Q350 en X=3.80, Y=10.20)
    # Impulsión aire limpio (Azul cian Ø90mm) -> Hall y Despacho
    out.append(f'<polyline points="{px(3.80):.1f},{py(9.60):.1f} {px(10.80):.1f},{py(5.60):.1f} {px(13.60):.1f},{py(5.60):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.6" stroke-dasharray="6,3"/>')
    out.append(mep_symbol(px(13.60), py(5.60), "vmc_imp", "+25 m³/h"))
    # Extracción aire viciado (Morado Ø90mm) -> Zaguán y Baño PB
    out.append(f'<polyline points="{px(3.95):.1f},{py(9.60):.1f} {px(8.60):.1f},{py(5.60):.1f} {px(16.15):.1f},{py(5.60):.1f}" fill="none" stroke="#f43f5e" stroke-width="1.6" stroke-dasharray="6,3"/>')
    out.append(mep_symbol(px(8.60), py(5.60), "vmc_ext", "-15 m³/h"))
    out.append(mep_symbol(px(16.15), py(5.60), "vmc_ext", "-30 m³/h"))

    # 3. Puntos Eléctricos, RJ45, Termostatos, Wallbox y Cuadro General CGMP
    # Wallbox 7.4kW en Pérgola (X=7.85, Y=6.80)
    out.append(f'<rect x="{px(7.72):.1f}" y="{py(6.70):.1f}" width="18" height="24" rx="2" fill="#064e3b" stroke="#10b981" stroke-width="1.5"/>')
    out.append(f'<text x="{px(7.55):.1f}" y="{py(6.88):.1f}" text-anchor="end" fill="#10b981" font-family="monospace" font-size="6.0" font-weight="700">WALLBOX VE 7,4kW (C11 · 32A)</text>')
    # CGMP en Zaguán (X=9.35, Y=6.05)
    out.append(f'<rect x="{px(9.20):.1f}" y="{py(5.95):.1f}" width="16" height="12" fill="#451a03" stroke="#f59e0b" stroke-width="1.3"/>')
    out.append(f'<text x="{px(9.12):.1f}" y="{py(6.05):.1f}" text-anchor="end" fill="#f59e0b" font-family="monospace" font-size="5.8" font-weight="700">CGMP + ICP</text>')

    # Tomas Schuko, RJ45 y Termostatos
    out.append(mep_symbol(px(8.25), py(8.65), "schuko", "C2 Secacalzado"))
    out.append(mep_symbol(px(9.75), py(8.00), "schuko", "C2"))
    out.append(mep_symbol(px(9.75), py(5.35), "thermostat", "KNX Hall"))
    out.append(mep_symbol(px(12.22), py(5.85), "rj45", "2×RJ45 Cat6A"))
    out.append(mep_symbol(px(12.22), py(6.65), "schuko", "4×C2 SAI/PC"))
    out.append(mep_symbol(px(14.30), py(8.75), "thermostat", "KNX Desp."))
    out.append(mep_symbol(px(16.75), py(6.85), "schuko", "C5 Espejo"))
    out.append(mep_symbol(px(16.10), py(5.55), "drain", "Bote Sifónico Ø110"))
    out.append('</g>')

    # Room Stamps
    out.append(room_stamp(px(5.50), py(5.20), "01. PÉRGOLA GARAJE (2 VE)", 28.00, "Cota ±0,00 m · Hormigón drenante", "E-01"))
    out.append(room_stamp(px(9.15), py(4.05), "02. PORCHE NORTE", 3.50, "Cota +0,05 m · Granito flameado", "E-02"))
    out.append(room_stamp(px(8.72), py(6.75), "03. ZAGUÁN", 5.80, "Esclusa térmica · Gres 60×60", "E-03"))
    out.append(room_stamp(px(10.65), py(6.15), "04. HALL ACCESO", 10.40, "Roble 14mm · Visión Patio", "E-04"))
    out.append(room_stamp(px(13.65), py(6.05), "05. DESPACHO", 11.50, "Roble 14mm · Rw ≥ 38 dB", "E-05"))
    out.append(room_stamp(px(16.35), py(8.55), "06. BAÑO PB", 5.20, "Gres · Ducha Walk-in", "E-06"))

    # ==========================================================================
    # CHAINED ARCHITECTURAL DIMENSIONS (1:50 PRECISION)
    # ==========================================================================
    # Top Chained Dimensions (North Facade Breakdown)
    out.append(dim_h(px(3.00), px(8.00), py(3.50), -26, "5,00 m (Pérgola 2 Plazas)"))
    out.append(dim_h(px(8.00), px(9.45), py(5.00), -26, "1,45 m (Zaguán)"))
    out.append(dim_h(px(9.45), px(12.05), py(5.00), -26, "2,60 m (Hall)"))
    out.append(dim_h(px(12.05), px(14.925), py(5.00), -26, "2,88 m (Despacho)"))
    out.append(dim_h(px(14.925), px(15.70), py(5.00), -26, "0,78 m"))
    out.append(dim_h(px(15.70), px(17.00), py(5.00), -26, "1,30 m (Baño)"))
    # Overall Top Width
    out.append(dim_h(px(3.00), px(17.00), py(3.50), -52, "14,00 m (ANCHO TOTAL EDIFICACIÓN EJE A - EJE E)", "#f8fafc"))

    # Interior & Openings Dimensions
    out.append(dim_h(px(9.60), px(10.80), py(5.00), 22, "1,20 m (C-01)", "#fbbf24"))
    out.append(dim_h(px(12.60), px(14.40), py(5.00), 22, "1,80 m (C-03)", "#fbbf24"))
    out.append(dim_h(px(8.00), px(12.00), py(9.00), 24, "4,00 m (Frente Acristalado Patio Corrala C-05)", "#10b981"))

    # Vertical Dimensions (Left & Right)
    out.append(dim_v(py(3.60), py(9.20), px(3.00), -28, "5,60 m (Fondo Pérgola)"))
    out.append(dim_v(py(5.00), py(9.00), px(17.00), 28, "4,00 m (Crujía Norte Eje 1-2)"))
    out.append(dim_v(py(3.50), py(5.00), px(8.00), -22, "1,50 m (Porche N)"))

    # Right Side Technical MEP & Constructive Legend
    out.append(mep_legend_panel(1224, 26, 548))

    # Cuadro de Circuitos y Cargas Zona Norte (Right Side Bottom)
    out.append('<g transform="translate(1224, 470)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="548" height="295" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="548" height="22" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15" fill="#38bdf8" font-size="7.8" font-weight="700">CUADRO DE REPLANTEO DE ESTANCIAS E INSTALACIONES — ZONA NORTE PB</text>')
    headers = [("CÓD.", 12), ("ESTANCIA", 55), ("COTAS INT.", 185), ("SUP. ÚTIL", 265), ("DOTACIÓN MEP / OBSERVACIONES", 330)]
    for h_txt, hx in headers:
        out.append(f'<text x="{hx}" y="38" fill="#94a3b8" font-size="6.2" font-weight="700">{h_txt}</text>')
    out.append('<line x1="8" y1="43" x2="540" y2="43" stroke="#334155" stroke-width="0.8"/>')

    rows = [
        ("E-01", "01. Pérgola Garaje 2 Plazas", "5,00 × 5,60 m", "28,00 m²", "Wallbox 7,4kW (C11) · Toma C2 · Sumidero ACO"),
        ("E-02", "02. Porche Cubierto Norte", "2,35 × 1,50 m", "3,50 m²", "Cota +0,05m · Videoportero IP PoE · LED presencia"),
        ("E-03", "03. Zaguán / Mudroom", "1,45 × 4,00 m", "5,80 m²", "CGMP · Extracción VMC -15 m³/h · Suelo radiante"),
        ("E-04", "04. Hall Acceso Principal", "2,60 × 4,00 m", "10,40 m²", "Puerta C-01 1,20m · Fijo C-05 Patio · Termostato KNX"),
        ("E-05", "05. Despacho / Estudio", "2,88 × 4,00 m", "11,50 m²", "2×RJ45 Cat6A · 6×Schuko · Impulsión VMC +25 m³/h"),
        ("E-06", "06. Baño Cortesía PB", "1,30 × 4,00 m", "5,20 m²", "Ducha enrasada · Extracción VMC -30 m³/h · Colector PEX"),
    ]
    ry = 58
    for cod, est, cot, sup, obs in rows:
        out.append(f'<rect x="8" y="{ry-11}" width="532" height="22" fill="none" stroke="#1e293b" stroke-width="0.6"/>')
        out.append(f'<text x="12" y="{ry+3}" fill="#38bdf8" font-size="6.2" font-weight="700">{cod}</text>')
        out.append(f'<text x="55" y="{ry+3}" fill="#e2e8f0" font-size="6.2">{est}</text>')
        out.append(f'<text x="185" y="{ry+3}" fill="#cbd5e1" font-size="6.2">{cot}</text>')
        out.append(f'<text x="265" y="{ry+3}" fill="#10b981" font-size="6.4" font-weight="700">{sup}</text>')
        out.append(f'<text x="330" y="{ry+3}" fill="#94a3b8" font-size="5.7">{obs}</text>')
        ry += 24

    # Detalle Constructivo Esclusa Térmica Zaguán
    out.append('<rect x="10" y="205" width="528" height="78" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="20" y="221" fill="#fbbf24" font-size="6.8" font-weight="700">PRESCRIPCIÓN DE EJECUCIÓN — ESCLUSA TÉRMICA Y ACÚSTICA NORTE:</text>')
    out.append('<text x="20" y="235" fill="#cbd5e1" font-size="6.0">1. El Zaguán (E-03) actúa como cámara estanca para acceso cotidiano desde aparcamiento bajo lluvia SW.</text>')
    out.append('<text x="20" y="248" fill="#cbd5e1" font-size="6.0">2. El Despacho (E-05) se independiza con tabiquería doble placa + lana mineral (Rw ≥ 50 dB) y puerta Rw ≥ 38 dB.</text>')
    out.append('<text x="20" y="261" fill="#cbd5e1" font-size="6.0">3. El Baño PB (E-06) dispone de ante-distribuidor neutro con doble puerta corredera (cumplimiento íntegro NHG).</text>')
    out.append('<text x="20" y="274" fill="#10b981" font-size="6.0" font-weight="700">4. Cota de pavimento interior ±0,00 m continua con Patio Central Corrala (umbral Cortizo sobre Purenit 50 mm).</text>')
    out.append('</g>')

    # North rose & Graphic scale (1:50)
    out.append(north_and_scale(1290, 845, S, 5))

    # ISO 7200 Title Block
    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-01",
        title="PLANTA CONSTRUCTIVA E INSTALACIONES — ZONA NORTE PB",
        scale="1:50 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN",
        subtitle="Replanteo de Albañilería, Carpinterías C-01..C-05, Electricidad, Telecomunicaciones, Agua y VMC",
        extra_notes=[
            "Estancias incluidas: 01 Pérgola Garaje, 02 Porche Norte, 03 Zaguán, 04 Hall, 05 Despacho, 06 Baño PB",
            "Superficie Útil Interior Zona Norte: 32,90 m² + 31,50 m² Exteriores Cubiertos (Pérgola + Porche)",
            "Cota Pavimento Interior: ±0,00 m · Altura libre falso techo: 2,50 m (Zaguán/Baño) / 2,65 m (Hall/Despacho)",
            "Coordenadas referidas a Esquina Noroeste de Parcela (0,00 ; 0,00) · Ejes Estructurales A-E / 1-2",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


# ==============================================================================
# PLANO E-02: BANDA CENTRAL PB — PATIO, COCINA ISLA, ESCALERA Y SALA TÉCNICA (1:50)
# ==============================================================================
def build_centro_patio_cocina_pb_svg() -> str:
    W, H = 1800, 1240
    S = 75.0  # 1m = 75px (escala 1:50)
    OX = 85.0
    OY = 85.0

    def px(xm: float) -> float:
        return OX + (xm - 2.50) * S

    def py(ym: float) -> float:
        return OY + (ym - 7.80) * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1180" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO E-02 · EJECUCIÓN E INSTALACIONES BANDA CENTRAL PB: PATIO, COCINA Y SALA TÉCNICA (1:50)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Patio Corrala 4,00×4,00m Cota ±0,00m · Cocina Isla Santos 2,80×1,00m · Lavandería · Escalera Volada 17 Peldaños · Central Passivhaus</text>',
        f'<rect x="28" y="68" width="1180" height="995" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Structural Axes
    x_axes = [("A", 3.00), ("B", 8.00), ("C", 12.00), ("D", 14.00), ("E", 17.00)]
    y_axes = [("2", 9.00), ("3", 13.00), ("4", 18.00)]
    out.append(draw_grid_axes(x_axes, y_axes, px(2.60), px(17.40), py(8.10), py(18.60), px, py))

    # Floor Surfaces in Central Band (Y=9.00..13.50) + Transition to South Band
    # 10. Sala Técnica Passivhaus & Surf: X=3.00..5.05, Y=9.00..13.00 (2.05 x 4.00 = 8.20 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(9.00):.1f}" width="{2.05*S:.1f}" height="{4.00*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')
    # 09. Escalera Volada y Distribuidor Oeste: X=5.05..8.00, Y=9.00..13.00
    out.append(f'<rect x="{px(5.05):.1f}" y="{py(9.00):.1f}" width="{2.95*S:.1f}" height="{4.00*S:.1f}" fill="#131c31" stroke="none"/>')

    # 00. PATIO CENTRAL DESCUBIERTO (CORRALA): X=8.00..12.00, Y=9.00..13.00 (4.00 x 4.00 = 16.00 m²)
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(9.00):.1f}" width="{4.00*S:.1f}" height="{4.00*S:.1f}" fill="url(#hatch-wood-deck)" stroke="#10b981" stroke-width="1.6"/>')
    # Canaleta perimetral oculta AISI 316 con rejilla ranurada (cota ±0.00m)
    out.append(f'<rect x="{px(8.16):.1f}" y="{py(9.16):.1f}" width="{3.68*S:.1f}" height="{3.68*S:.1f}" fill="none" stroke="#38bdf8" stroke-width="1.3" stroke-dasharray="5,3"/>')
    # Alero perimetral de 80 cm con banco corrido de Iroko
    out.append(f'<rect x="{px(8.80):.1f}" y="{py(9.80):.1f}" width="{2.40*S:.1f}" height="{2.40*S:.1f}" fill="none" stroke="#fbbf24" stroke-width="1.0" stroke-dasharray="8,4"/>')
    # Alcorque drenante central (1,60 x 1,60 m) con grava de cuarzo y Arce Japonés (Acer palmatum)
    out.append(f'<rect x="{px(9.20):.1f}" y="{py(10.20):.1f}" width="{1.60*S:.1f}" height="{1.60*S:.1f}" fill="url(#hatch-gravel)" stroke="#10b981" stroke-width="1.2"/>')
    out.append(f'<circle cx="{px(10.00):.1f}" cy="{py(11.00):.1f}" r="{0.62*S:.1f}" fill="#064e3b" fill-opacity="0.45" stroke="#10b981" stroke-width="1.4"/>')
    out.append(f'<circle cx="{px(10.00):.1f}" cy="{py(11.00):.1f}" r="{0.09*S:.1f}" fill="#10b981"/>')
    for ang in range(0, 360, 45):
        import math
        rad = math.radians(ang)
        out.append(f'<line x1="{px(10.00):.1f}" y1="{py(11.00):.1f}" x2="{px(10.00)+math.cos(rad)*0.55*S:.1f}" y2="{py(11.00)+math.sin(rad)*0.55*S:.1f}" stroke="#34d399" stroke-width="0.8"/>')

    # 08. Cocina Conecta con Isla Central: X=12.00..15.40, Y=9.00..13.50 (3.40 x 4.50 = 15.20 m²)
    out.append(f'<rect x="{px(12.00):.1f}" y="{py(9.00):.1f}" width="{3.40*S:.1f}" height="{4.50*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')
    # 07. Lavandería y Despensa Técnica: X=15.40..17.00, Y=9.00..12.50 (1.60 x 3.50 = 5.60 m²)
    out.append(f'<rect x="{px(15.40):.1f}" y="{py(9.00):.1f}" width="{1.60*S:.1f}" height="{3.50*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # Reference preview of South Zone (Salón & Comedor Y=13.00..17.50)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(13.00):.1f}" width="{14.00*S:.1f}" height="{4.50*S:.1f}" fill="#131c31" opacity="0.55"/>')
    out.append(f'<text x="{px(8.00):.1f}" y="{py(15.40):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="8.0" font-weight="700">11. SALÓN - COMEDOR DIÁFANO (44,00 m²) — Ver PLANO E-03</text>')

    # Walls (e=0.40m exterior, e=0.12m interior)
    tw_ext = 0.40 * S
    tw_int = 0.12 * S
    out.append(draw_wall(px(3.00), py(9.00), px(8.00), py(9.00), tw_ext, True))
    out.append(draw_wall(px(3.00), py(9.00), px(3.00), py(17.50), tw_ext, True))
    out.append(draw_wall(px(17.00), py(8.50), px(17.00), py(17.50), tw_ext, True))
    out.append(draw_wall(px(5.05), py(9.00), px(5.05), py(13.00), tw_int, False)) # Sala Técnica | Escalera
    out.append(draw_wall(px(3.00), py(13.00), px(5.05), py(13.00), tw_int, False)) # Sala Técnica South wall
    out.append(draw_wall(px(12.00), py(9.00), px(15.05), py(9.00), tw_int, False)) # Cocina North wall
    out.append(draw_wall(px(15.40), py(9.00), px(15.40), py(12.50), tw_int, False)) # Cocina | Lavandería
    out.append(draw_wall(px(15.40), py(12.50), px(17.00), py(12.50), tw_int, False)) # Lavandería South wall

    # 3 Caras Acristaladas del Patio Central Corrala (Cota Cero sobre Purenit)
    out.append(sliding_door(px(8.00), py(9.00), 4.00*S, tw_ext*0.75, "h", 2, "C-05 NORTE PATIO 3,60×2,60"))
    out.append(sliding_door(px(8.00), py(9.00), 4.00*S, tw_ext*0.75, "v", 2, "C-05B OESTE ESCALERA 3,60×2,60"))
    out.append(sliding_door(px(12.00), py(9.00), 4.00*S, tw_ext*0.75, "v", 2, "C-06 ESTE COCINA 3,60×2,60"))
    out.append(sliding_door(px(8.00), py(13.00), 4.00*S, tw_ext*0.75, "h", 2, "C-05C SUR SALÓN 3,60×2,60"))

    # Otras Puertas y Ventanas Banda Central
    # C-10: Puerta Exterior Sala Técnica (X=3.60..4.50, Y=9.00)
    out.append(door_swing(px(3.60), py(9.00), 0.90*S, "down", "right", "C-10 EXT. 0,90"))
    # Puerta Corredera Oculta Cocina -> Lavandería (X=15.40, Y=10.30..11.15)
    out.append(sliding_door(px(15.40), py(10.30), 0.85*S, tw_int, "v", 1, "P-05 CORR. 0,80"))
    # C-09: Ventana Fachada Este Lavandería (X=17.00, Y=10.20..11.20)
    out.append(window_cad(px(17.00), py(10.20), 1.00*S, tw_ext, "v", "C-09 1,00×1,00"))

    # ==========================================================================
    # EQUIPAMIENTO TÉCNICO DETALLADO (ESCALA 1:50)
    # ==========================================================================
    # 10. Sala Técnica Passivhaus & Surf (X=3.00..5.05, Y=9.00..13.00):
    # Unidad Interior Aerotermia Vaillant aroTHERM plus + Depósito Inercia/ACS 250L (X=3.15..3.85, Y=9.80..10.50)
    out.append(f'<rect x="{px(3.15):.1f}" y="{py(9.80):.1f}" width="{0.65*S:.1f}" height="{0.65*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<circle cx="{px(3.48):.1f}" cy="{py(10.12):.1f}" r="{0.24*S:.1f}" fill="#0f172a" stroke="#ef4444" stroke-width="1.2"/>')
    out.append(f'<text x="{px(3.48):.1f}" y="{py(10.15):.1f}" text-anchor="middle" fill="#f8fafc" font-family="monospace" font-size="5.5" font-weight="700">ACS 250L</text>')
    # Recuperador VMC Zehnder ComfoAir Q350 en pared/techo + Silenciadores (X=3.15..3.85, Y=10.65..11.35)
    out.append(f'<rect x="{px(3.15):.1f}" y="{py(10.65):.1f}" width="{0.68*S:.1f}" height="{0.70*S:.1f}" fill="#083344" stroke="#06b6d4" stroke-width="1.3"/>')
    out.append(f'<line x1="{px(3.15):.1f}" y1="{py(10.65):.1f}" x2="{px(3.83):.1f}" y2="{py(11.35):.1f}" stroke="#06b6d4" stroke-width="0.8"/>')
    out.append(f'<line x1="{px(3.83):.1f}" y1="{py(10.65):.1f}" x2="{px(3.15):.1f}" y2="{py(11.35):.1f}" stroke="#06b6d4" stroke-width="0.8"/>')
    out.append(f'<text x="{px(3.49):.1f}" y="{py(11.02):.1f}" text-anchor="middle" fill="#cffafe" font-family="monospace" font-size="5.5" font-weight="700">VMC Q350</text>')
    # Inversor Híbrido Solar Huawei SUN2000 5kW + Batería LUNA2000 (X=3.15..3.65, Y=11.50..12.15)
    out.append(f'<rect x="{px(3.15):.1f}" y="{py(11.50):.1f}" width="{0.45*S:.1f}" height="{0.65*S:.1f}" fill="#451a03" stroke="#f59e0b" stroke-width="1.2"/>')
    out.append(f'<text x="{px(3.38):.1f}" y="{py(11.85):.1f}" text-anchor="middle" fill="#fde68a" font-family="monospace" font-size="5.2" font-weight="700">INV. 5kW</text>')
    # Rack 19" 9U Comunicaciones (X=3.15..3.65, Y=12.25..12.80)
    out.append(f'<rect x="{px(3.15):.1f}" y="{py(12.25):.1f}" width="{0.50*S:.1f}" height="{0.55*S:.1f}" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.2"/>')
    out.append(f'<text x="{px(3.40):.1f}" y="{py(12.55):.1f}" text-anchor="middle" fill="#c7d2fe" font-family="monospace" font-size="5.2" font-weight="700">RACK 9U</text>')
    # Racks Verticales Tablas Surf + Ducha neoprenos (X=4.35..4.95, Y=9.80..12.75)
    out.append(f'<rect x="{px(4.35):.1f}" y="{py(9.80):.1f}" width="{0.58*S:.1f}" height="{1.90*S:.1f}" fill="#0f172a" stroke="#64748b" stroke-width="1.0"/>')
    for sy in [10.05, 10.35, 10.65, 10.95, 11.25, 11.50]:
        out.append(f'<ellipse cx="{px(4.64):.1f}" cy="{py(sy):.1f}" rx="{0.22*S:.1f}" ry="{0.06*S:.1f}" fill="none" stroke="#38bdf8" stroke-width="0.8"/>')
    out.append(shower_cad(px(4.35), py(11.85), 0.58*S, 0.90*S))

    # 09. Escalera Volada de Roble (17 peldaños · H=29 cm · CH=17,6 cm · Ancho 1,10 m):
    st_x = px(5.30)
    st_y = py(9.25)
    st_w = 1.15 * S
    st_h = 3.55 * S
    out.append(f'<rect x="{st_x:.1f}" y="{st_y:.1f}" width="{st_w:.1f}" height="{st_h:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    n_steps = 17
    for i in range(1, n_steps):
        sy = st_y + i * (st_h / n_steps)
        out.append(f'<line x1="{st_x:.1f}" y1="{sy:.1f}" x2="{st_x+st_w:.1f}" y2="{sy:.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
        out.append(f'<text x="{st_x+10:.1f}" y="{sy-2:.1f}" fill="#64748b" font-family="monospace" font-size="4.8">{i:02d}</text>')
    # Línea de huella y flecha de subida reglamentaria
    out.append(f'<line x1="{st_x+st_w/2:.1f}" y1="{st_y+st_h-12:.1f}" x2="{st_x+st_w/2:.1f}" y2="{st_y+12:.1f}" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<polyline points="{st_x+st_w/2-6:.1f},{st_y+22:.1f} {st_x+st_w/2:.1f},{st_y+12:.1f} {st_x+st_w/2+6:.1f},{st_y+22:.1f}" fill="none" stroke="#38bdf8" stroke-width="1.3"/>')
    out.append(f'<text x="{st_x+st_w/2:.1f}" y="{st_y-6:.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700">SUBE A P1 (+3,15 m) · 17C × 17,6 cm / 16H × 29,0 cm</text>')

    # 08. Cocina Santos Fine con Isla Central (2,80 x 1,00 m) y Frente Columnas (3,60 m):
    # Frente de columnas integradas Este (X=14.68..15.32, Y=9.15..12.75): Frigo Combi + Congelador + Torre Horno/Micro + Desayunador Escamoteable Pocket
    out.append(f'<rect x="{px(14.68):.1f}" y="{py(9.15):.1f}" width="{0.64*S:.1f}" height="{3.60*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    for cy, clbl in [(9.45, "FRIGO 70"), (10.15, "CONGEL."), (10.85, "HORNO/MIC"), (11.65, "DESAYUN. POCKET"), (12.40, "COL. DESP.")]:
        out.append(f'<line x1="{px(14.68):.1f}" y1="{py(cy+0.32):.1f}" x2="{px(15.32):.1f}" y2="{py(cy+0.32):.1f}" stroke="#475569" stroke-width="0.8"/>')
        out.append(f'<text x="{px(15.00):.1f}" y="{py(cy):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.0">{clbl}</text>')

    # Isla Central Santos Fine (X=12.90..13.90, Y=9.55..12.35 -> 1,00 x 2,80 m):
    ix, iy, iw, ih = px(12.90), py(9.55), 1.00*S, 2.80*S
    out.append(f'<rect x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{ih:.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="1.4"/>')
    # Fregadero submontado 70x40cm + Lavavajillas integrado 60cm
    out.append(f'<rect x="{ix+10:.1f}" y="{iy+24:.1f}" width="{0.45*S:.1f}" height="{0.70*S:.1f}" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<circle cx="{ix+24:.1f}" cy="{iy+50:.1f}" r="4" fill="none" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{ix+28:.1f}" y="{iy+75:.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0">FREG. 70</text>')
    # Placa Inducción Bora Pure con extractor downdraft integrado (80x52cm) + Conducto Ecotube en solera
    out.append(f'<rect x="{ix+10:.1f}" y="{iy+1.45*S:.1f}" width="{0.52*S:.1f}" height="{0.85*S:.1f}" fill="#18181b" stroke="#f59e0b" stroke-width="1.1"/>')
    for bx, by in [(ix+20, iy+1.62*S), (ix+36, iy+1.62*S), (ix+20, iy+2.08*S), (ix+36, iy+2.08*S)]:
        out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="7.5" fill="none" stroke="#f59e0b" stroke-width="0.9"/>')
    # Tobera central Bora Pure
    out.append(f'<rect x="{ix+23:.1f}" y="{iy+1.80*S:.1f}" width="10" height="16" rx="2" fill="#0f172a" stroke="#06b6d4" stroke-width="1.0"/>')
    # 4 Taburetes en vuelo barra Oeste de la isla (orientados hacia el Patio Corrala)
    for sy in [9.85, 10.50, 11.15, 11.80]:
        out.append(f'<circle cx="{px(12.72):.1f}" cy="{py(sy):.1f}" r="{0.17*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.9"/>')

    # 07. Lavandería y Despensa Técnica (X=15.40..17.00, Y=9.00..12.50):
    # Encimera Este con Torre Lavadora/Secadora Míele + Pilón (X=16.25..16.88, Y=9.15..11.85)
    out.append(f'<rect x="{px(16.25):.1f}" y="{py(9.15):.1f}" width="{0.63*S:.1f}" height="{2.70*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.0"/>')
    out.append(f'<rect x="{px(16.28):.1f}" y="{py(9.22):.1f}" width="{0.56*S:.1f}" height="{0.58*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<circle cx="{px(16.56):.1f}" cy="{py(9.51):.1f}" r="{0.20*S:.1f}" fill="none" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{px(16.56):.1f}" y="{py(9.54):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" font-weight="700">LAV+SEC</text>')
    # Pilón lavadero
    out.append(sink_cad(px(16.32), py(10.05), 0.50*S, 0.65*S, False))
    # Estanterías Despensa Seca (X=15.50..15.95, Y=11.35..12.40)
    out.append(wardrobe_cad(px(15.50), py(11.35), 0.45*S, 1.05*S, "v"))

    # NHG Ø1.50m Circles in Cocina & Lavandería
    out.append(nhg_circle(px(14.30), py(10.95), S, "Ø1,50m COCINA"))
    out.append(nhg_circle(px(12.45), py(10.95), S, "PASO 0,90m"))

    # Structural Pillars
    pillars = [(x, y) for x in [3.00, 8.00, 12.00, 14.00, 17.00] for y in [9.00, 13.00]]
    out.append(draw_pillars(pillars, px, py, 0.25, S))

    # ==========================================================================
    # MEP INSTALLATIONS OVERLAY (BANDA CENTRAL 1:50)
    # ==========================================================================
    out.append('<g opacity="0.92">')
    # Unidad Exterior Aerotermia Vaillant aroTHERM plus en bancada antivibratoria Oeste (X=2.35, Y=10.00)
    out.append(f'<rect x="{px(2.30):.1f}" y="{py(9.80):.1f}" width="{0.52*S:.1f}" height="{0.95*S:.1f}" fill="#0f172a" stroke="#10b981" stroke-width="1.4"/>')
    out.append(f'<circle cx="{px(2.56):.1f}" cy="{py(10.28):.1f}" r="{0.20*S:.1f}" fill="none" stroke="#10b981" stroke-width="1.1"/>')
    out.append(f'<text x="{px(2.18):.1f}" y="{py(10.28):.1f}" text-anchor="end" fill="#10b981" font-family="monospace" font-size="5.8" font-weight="700">U. EXT. AEROTERMIA R290</text>')

    # Sumidero Sifónico Patio Central -> Red Pluviales PVC Ø110 mm hacia Oeste
    out.append(mep_symbol(px(8.35), py(12.65), "drain", "SUMIDERO SIFÓNICO PATIO"))
    out.append(f'<polyline points="{px(8.35):.1f},{py(12.65):.1f} {px(2.50):.1f},{py(12.65):.1f}" fill="none" stroke="#38bdf8" stroke-width="2.0" stroke-dasharray="7,3"/>')
    out.append(f'<text x="{px(6.50):.1f}" y="{py(12.52):.1f}" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">COLECTOR PLUVIALES PATIO PVC Ø110 mm (Pendiente 2% + Válvula Antirretorno)</text>')

    # Conducto Bora Ecotube embutido en recrecido de solera (Isla -> Fachada Este X=17.00)
    out.append(f'<polyline points="{px(13.20):.1f},{py(11.40):.1f} {px(17.15):.1f},{py(11.40):.1f}" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{px(15.20):.1f}" y="{py(11.28):.1f}" text-anchor="middle" fill="#f59e0b" font-family="monospace" font-size="5.6" font-weight="700">CONDUCTO PLANO BORA ECOTUBE 245×89 mm EN SOLERA</text>')

    # VMC Extracción Cocina (-45 m³/h) y Lavandería (-20 m³/h)
    out.append(mep_symbol(px(14.35), py(9.45), "vmc_ext", "-45 m³/h"))
    out.append(mep_symbol(px(15.95), py(9.45), "vmc_ext", "-20 m³/h"))
    out.append(f'<polyline points="{px(3.50):.1f},{py(11.00):.1f} {px(3.50):.1f},{py(9.35):.1f} {px(15.95):.1f},{py(9.35):.1f}" fill="none" stroke="#f43f5e" stroke-width="1.6" stroke-dasharray="6,3"/>')

    # Puntos eléctricos C3 (Isla), C4 (Lavavajillas/Lavadora) y C5 (Encimera/Desayunador)
    out.append(mep_symbol(px(13.40), py(11.55), "schuko", "C3 25A Bora"))
    out.append(mep_symbol(px(13.40), py(10.10), "schuko", "C4 LVV"))
    out.append(mep_symbol(px(14.65), py(11.65), "schuko", "4×C5 Pocket"))
    out.append(mep_symbol(px(16.20), py(9.50), "schuko", "2×C4 Lav/Sec"))
    out.append('</g>')

    # Room Stamps
    out.append(room_stamp(px(10.00), py(9.55), "00. PATIO CENTRAL CORRALA", 16.00, "Cota ±0,00m · Iroko + Arce Japonés", "E-00"))
    out.append(room_stamp(px(4.02), py(9.45), "10. SALA TÉCNICA / SURF", 8.20, "Aerotermia + VMC Q350 + FV + Rack", "E-10"))
    out.append(room_stamp(px(7.20), py(10.90), "09. ESCALERA", 6.50, "17 Peldaños Roble Volados", "E-09"))
    out.append(room_stamp(px(13.40), py(13.15), "08. COCINA ISLA SANTOS", 15.20, "Isla 2,80×1,00 m · Dekton Kelya", "E-08"))
    out.append(room_stamp(px(16.15), py(12.10), "07. LAVANDERÍA / DESP.", 5.60, "Torre Míele + Pilón + Despensa", "E-07"))

    # ==========================================================================
    # CHAINED ARCHITECTURAL DIMENSIONS (BANDA CENTRAL 1:50)
    # ==========================================================================
    out.append(dim_h(px(3.00), px(5.05), py(9.00), -25, "2,05 m (Sala Técnica)"))
    out.append(dim_h(px(5.05), px(8.00), py(9.00), -25, "2,95 m (Escalera / Paso)"))
    out.append(dim_h(px(8.00), px(12.00), py(9.00), -25, "4,00 m (Patio Central Corrala)"))
    out.append(dim_h(px(12.00), px(15.40), py(9.00), -25, "3,40 m (Cocina Isla Santos)"))
    out.append(dim_h(px(15.40), px(17.00), py(9.00), -25, "1,60 m (Lavand.)"))
    out.append(dim_h(px(3.00), px(17.00), py(9.00), -50, "14,00 m (ANCHO TOTAL BANDA CENTRAL EJE A - EJE E)", "#f8fafc"))

    # Detailed Kitchen Island Clearances (pasos libres 0.90m / 1.00m / 0.60m)
    out.append(dim_h(px(12.00), px(12.90), py(12.55), 18, "0,90 m (Paso Oeste)", "#fbbf24"))
    out.append(dim_h(px(12.90), px(13.90), py(12.55), 18, "1,00 m (Isla)", "#38bdf8"))
    out.append(dim_h(px(13.90), px(14.68), py(12.55), 18, "0,78 m (Paso Trabajo)", "#fbbf24"))
    out.append(dim_h(px(14.68), px(15.32), py(12.55), 18, "0,64 m (Col.)", "#94a3b8"))

    # Vertical Dimensions
    out.append(dim_v(py(9.00), py(13.00), px(3.00), -28, "4,00 m (Crujía Central Eje 2-3)"))
    out.append(dim_v(py(9.55), py(12.35), px(12.90), -18, "2,80 m (Isla Santos)", "#38bdf8"))
    out.append(dim_v(py(9.00), py(12.50), px(17.00), 28, "3,50 m (Lavandería)"))

    # Right Panel: MEP Legend + Patio & Kitchen Constructive Specs
    out.append(mep_legend_panel(1224, 26, 548))

    out.append('<g transform="translate(1224, 470)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="548" height="295" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="548" height="22" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15" fill="#38bdf8" font-size="7.8" font-weight="700">ESPECIFICACIONES CONSTRUCTIVAS — PATIO CORRALA, COCINA Y SALA TÉCNICA</text>')
    specs = [
        ("00. PATIO CENTRAL DESCUBIERTO (4,00 × 4,00 m = 16,00 m² · NO COMPUTA OCUPACIÓN PGOM):", "#10b981", [
            "• Drenaje cota cero: Tarima de Iroko macizo sobre plots regulables (h=12 cm) con junta abierta de 6 mm.",
            "• Canaleta oculta perimetral en acero inox AISI 316L junto a las 3 carpinterías Cortizo Cor Vision Plus.",
            "• Forjado rebajado -15 cm con pendiente 2% a sumidero sifónico central Ø110 mm + válvula antirretorno.",
            "• Alcorque central drenante (1,60 × 1,60 m) conectado a terreno natural para ejemplar de Arce Japonés.",
        ]),
        ("08. COCINA ISLA SANTOS FINE + DESAYUNADOR ESCAMOTEABLE (15,20 m²):", "#38bdf8", [
            "• Isla central de 2,80 × 1,00 m en porcelánico Dekton Kelya 20 mm con unión a inglete y vuelo para 4 taburetes.",
            "• Sistema de inducción con extracción integrada Bora Pure + conducto plano Ecotube embutido en solera.",
            "• Mueble desayunador con puertas escamoteables (Pocket Doors) de 120 cm con 4 tomas Schuko C5 internas.",
        ]),
        ("10. SALA TÉCNICA PASSIVHAUS Y GUARDATABLAS SURF CON ACCESO EXTERIOR (8,20 m²):", "#f59e0b", [
            "• Central térmica e hidráulica registrable desde el exterior (C-10) sin invadir la vivienda con trajes húmedos.",
            "• Aerotermia Vaillant aroTHERM plus + Depósito ACS 250L + VMC Zehnder ComfoAir Q350 + Inversor FV 5kW + Rack 9U.",
        ]),
    ]
    sy = 38
    for stitle, scol, bullets in specs:
        out.append(f'<text x="12" y="{sy}" fill="{scol}" font-size="6.5" font-weight="700">{stitle}</text>')
        sy += 13
        for b in bullets:
            out.append(f'<text x="18" y="{sy}" fill="#cbd5e1" font-size="5.8">{b}</text>')
            sy += 13
        sy += 6
    out.append('</g>')

    out.append(north_and_scale(1290, 845, S, 5))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-02",
        title="PLANTA CONSTRUCTIVA E INSTALACIONES — BANDA CENTRAL PB (PATIO Y COCINA)",
        scale="1:50 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN",
        subtitle="Detalle de Patio Central Corrala 4×4m, Cocina Isla Santos, Lavandería, Escalera Volada y Sala Técnica",
        extra_notes=[
            "Estancias incluidas: 00 Patio Central (16,00 m²), 07 Lavandería (5,60 m²), 08 Cocina (15,20 m²), 09 Escalera, 10 Sala Técnica (8,20 m²)",
            "Cota Pavimento Interior y Tarima Flotante de Patio: ±0,00 m enrasado continuo sin escalón (Purenit 50 mm)",
            "Evacuación Pluviales Patio: Sumidero Sifónico Ø110 mm + Rebosadero de seguridad Ø90 mm a pozo filtrante",
            "Coordenadas referidas a Esquina Noroeste de Parcela (0,00 ; 0,00) · Ejes Estructurales A-E / 2-3",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


# ==============================================================================
# PLANO E-03: ZONA SUR PB — SALÓN, COMEDOR, PORCHE SUR, CHURRASQUEIRA Y PISCINA (1:50)
# ==============================================================================
def build_sur_salon_porche_pb_svg() -> str:
    W, H = 1800, 1240
    S = 68.0  # 1m = 68px (cubre desde Y=12.50 hasta Y=25.50 con piscina completa)
    OX = 85.0
    OY = 85.0

    def px(xm: float) -> float:
        return OX + (xm - 2.50) * S

    def py(ym: float) -> float:
        return OY + (ym - 12.20) * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1180" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO E-03 · EJECUCIÓN E INSTALACIONES ZONA SUR PB: SALÓN, PORCHE, CHURRASQUEIRA Y PISCINA (1:50)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Salón-Comedor 44,00 m² · Muro Inercial Granito + Chimenea Stûv 21 · Porche Sur 36,00 m² · Churrasqueira · Piscina 7,50×3,50 m</text>',
        f'<rect x="28" y="68" width="1180" height="995" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Structural Axes
    x_axes = [("A", 3.00), ("B", 8.00), ("C", 12.00), ("D", 14.00), ("E", 17.00)]
    y_axes = [("3", 13.00), ("4", 18.00), ("5", 21.00)]
    out.append(draw_grid_axes(x_axes, y_axes, px(2.60), px(17.40), py(12.50), py(25.60), px, py))

    # 11A + 11B: Salón Estar (26,50 m²) + Comedor Principal (17,50 m²) = 44,00 m² (X=3.00..17.00, Y=13.00..18.00)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(13.00):.1f}" width="{14.00*S:.1f}" height="{5.00*S:.1f}" fill="#131c31" stroke="none"/>')
    # Subtle serpentine radiant floor circuit hatch in Salón & Comedor
    out.append(f'<rect x="{px(3.40):.1f}" y="{py(13.40):.1f}" width="{5.80*S:.1f}" height="{4.20*S:.1f}" fill="url(#hatch-radiant)" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,4"/>')
    out.append(f'<rect x="{px(10.20):.1f}" y="{py(13.60):.1f}" width="{6.20*S:.1f}" height="{4.00*S:.1f}" fill="url(#hatch-radiant)" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,4"/>')

    # 12. Porche Sur Cubierto + Cocina Exterior / Churrasqueira (X=3.00..15.00, Y=18.00..21.00 -> 12,00 x 3,00 m = 36,00 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(18.00):.1f}" width="{12.00*S:.1f}" height="{3.00*S:.1f}" fill="url(#hatch-tile-60)" stroke="#fbbf24" stroke-width="1.3" stroke-dasharray="8,4"/>')
    # Canaleta lineal ACO oculta en transición Salón - Porche (Y=18.08)
    out.append(f'<line x1="{px(3.00):.1f}" y1="{py(18.08):.1f}" x2="{px(17.00):.1f}" y2="{py(18.08):.1f}" stroke="#38bdf8" stroke-width="1.4" stroke-dasharray="6,3"/>')

    # 13. Solárium y Piscina Desbordante (X=6.00..13.50, Y=21.80..25.30 -> 7,50 x 3,50 m = 26,25 m²)
    out.append(f'<rect x="{px(5.40):.1f}" y="{py(21.30):.1f}" width="{8.70*S:.1f}" height="{4.40*S:.1f}" fill="url(#hatch-tile-60)" stroke="#64748b" stroke-width="0.9"/>')
    out.append(f'<rect x="{px(6.00):.1f}" y="{py(21.80):.1f}" width="{7.50*S:.1f}" height="{3.50*S:.1f}" fill="#082f49" stroke="#38bdf8" stroke-width="2.0"/>')
    out.append(f'<rect x="{px(6.00):.1f}" y="{py(21.80):.1f}" width="{7.50*S:.1f}" height="{3.50*S:.1f}" fill="url(#hatch-water)"/>')
    # Peldaños playa húmeda sumergida Oeste
    for i in range(1, 5):
        sx = px(6.00 + i * 0.35)
        out.append(f'<line x1="{sx:.1f}" y1="{py(21.80):.1f}" x2="{sx:.1f}" y2="{py(25.30):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    # Arqueta Técnica Depuración Salina enterrada (X=14.00..15.10, Y=22.20..23.30)
    out.append(f'<rect x="{px(14.00):.1f}" y="{py(22.20):.1f}" width="{1.10*S:.1f}" height="{1.10*S:.1f}" fill="#0f172a" stroke="#06b6d4" stroke-width="1.3" stroke-dasharray="5,2"/>')
    out.append(f'<text x="{px(14.55):.1f}" y="{py(22.70):.1f}" text-anchor="middle" fill="#06b6d4" font-family="monospace" font-size="5.5" font-weight="700">ARQUETA SALINA</text>')
    out.append(f'<text x="{px(14.55):.1f}" y="{py(22.90):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.0">+ BOMBA CALOR</text>')

    # Exterior Multi-Layer Walls (e=0.40m, Muro Oeste F2 Granito e=0.45m)
    tw_ext = 0.40 * S
    tw_granito = 0.45 * S
    # West Inertia Granite Wall (X=3.00, Y=13.00..18.00)
    out.append(draw_wall(px(3.00), py(13.00), px(3.00), py(18.00), tw_granito, True))
    # East Wall (X=17.00, Y=13.00..18.00) + Prolongación Muro Churrasqueira Este del Porche (Y=18.00..21.00)
    out.append(draw_wall(px(17.00), py(13.00), px(17.00), py(18.00), tw_ext, True))
    out.append(draw_wall(px(15.00), py(18.00), px(15.00), py(21.00), tw_ext, True))
    # South Facade Wall segments at Y=18.00 (X=3.00..17.00)
    out.append(draw_wall(px(3.00), py(18.00), px(17.00), py(18.00), tw_ext, True))

    # Grandes Ventanales Correderos Cortizo Cor Vision Plus (Enrasados Cota ±0,00 m)
    # C-07: Corredera 3 Hojas Salón -> Porche Sur (5,00 x 2,60 m en X=3.80..8.80, Y=18.00)
    out.append(sliding_door(px(3.80), py(18.00), 5.00*S, tw_ext*0.8, "h", 3, "C-07 CORREDERA SALÓN 5,00×2,60 m (3 HOJAS · RPT · Uw=0,90)"))
    # C-08: Corredera 2 Hojas Comedor -> Porche Sur (3,50 x 2,60 m en X=10.80..14.30, Y=18.00)
    out.append(sliding_door(px(10.80), py(18.00), 3.50*S, tw_ext*0.8, "h", 2, "C-08 CORREDERA COMEDOR 3,50×2,60 m (2 HOJAS · RPT)"))
    # C-05C: Corredera Salón -> Patio Central Corrala en Y=13.00 (X=8.00..12.00)
    out.append(sliding_door(px(8.00), py(13.00), 4.00*S, tw_ext*0.75, "h", 2, "C-05C VIDRIO PATIO CORRALA 3,60×2,60 m"))

    # ==========================================================================
    # MOBILIARIO TÉCNICO Y CHIMENEA / CHURRASQUEIRA (1:50)
    # ==========================================================================
    # 11A. Salón Estar:
    # Muro Técnico Oeste: Chimenea Estanca de Leña Stûv 21 con toma exterior Ø150 mm + Bancada Granito + TV OLED 77" (X=3.20..3.85, Y=14.00..17.10)
    out.append(f'<rect x="{px(3.22):.1f}" y="{py(13.90):.1f}" width="{0.60*S:.1f}" height="{3.20*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    # Hogar estanco Stûv 21 (X=3.25..3.80, Y=14.20..15.10) + Conducto toma aire comburente exterior Ø150mm
    out.append(f'<rect x="{px(3.25):.1f}" y="{py(14.20):.1f}" width="{0.52*S:.1f}" height="{0.90*S:.1f}" fill="#451a03" stroke="#f97316" stroke-width="1.4"/>')
    out.append(f'<circle cx="{px(3.51):.1f}" cy="{py(14.65):.1f}" r="{0.15*S:.1f}" fill="none" stroke="#f97316" stroke-width="1.1"/>')
    out.append(f'<line x1="{px(2.65):.1f}" y1="{py(14.65):.1f}" x2="{px(3.25):.1f}" y2="{py(14.65):.1f}" stroke="#06b6d4" stroke-width="1.8" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{px(2.60):.1f}" y="{py(14.55):.1f}" text-anchor="end" fill="#06b6d4" font-family="monospace" font-size="5.5" font-weight="700">TOMA AIRE EXT. Ø150mm</text>')
    # TV OLED 77" en soporte mural (Y=15.45..16.85)
    out.append(f'<rect x="{px(3.32):.1f}" y="{py(15.45):.1f}" width="{0.12*S:.1f}" height="{1.40*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{px(3.62):.1f}" y="{py(16.15):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.5" transform="rotate(-90 {px(3.62):.1f} {py(16.15):.1f})">TV OLED 77"</text>')

    # Gran Sofá Modular en L (3,40 x 2,40 m) orientado a Chimenea/TV y a Piscina Sur (sin dar la espalda al jardín)
    out.append(f'<path d="M {px(5.10):.1f},{py(14.20):.1f} H {px(7.90):.1f} V {py(16.80):.1f} H {px(6.90):.1f} V {py(15.15):.1f} H {px(5.10):.1f} Z" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>')
    # Respaldo y cojines técnicos CAD
    out.append(f'<line x1="{px(5.10):.1f}" y1="{py(14.42):.1f}" x2="{px(7.90):.1f}" y2="{py(14.42):.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<line x1="{px(7.68):.1f}" y1="{py(14.20):.1f}" x2="{px(7.68):.1f}" y2="{py(16.80):.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
    # Mesa de centro (1,40 x 0,90 m) + Butaca lectura
    out.append(f'<rect x="{px(5.30):.1f}" y="{py(15.55):.1f}" width="{1.30*S:.1f}" height="{0.85*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="0.9"/>')
    out.append(f'<rect x="{px(4.35):.1f}" y="{py(16.55):.1f}" width="{0.75*S:.1f}" height="{0.75*S:.1f}" rx="4" fill="#1e293b" stroke="#94a3b8" stroke-width="0.9"/>')

    # 11B. Comedor Principal (Mesa Roble Macizo 2,60 x 1,10 m para 10 comensales + Aparador):
    mx, my, mw, mh = px(11.35), py(14.95), 2.60*S, 1.10*S
    out.append(f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.2"/>')
    for i in range(4):
        cx = mx + 22 + i * ((mw - 44) / 3)
        out.append(f'<rect x="{cx-10:.1f}" y="{my-12:.1f}" width="20" height="9" rx="2" fill="none" stroke="#94a3b8" stroke-width="0.8"/>')
        out.append(f'<rect x="{cx-10:.1f}" y="{my+mh+3:.1f}" width="20" height="9" rx="2" fill="none" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{mx-12:.1f}" y="{my+mh/2-10:.1f}" width="9" height="20" rx="2" fill="none" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{mx+mw+3:.1f}" y="{my+mh/2-10:.1f}" width="9" height="20" rx="2" fill="none" stroke="#94a3b8" stroke-width="0.8"/>')
    # Aparador vajillero en tabique Este (X=16.32..16.82, Y=14.40..16.80)
    out.append(f'<rect x="{px(16.32):.1f}" y="{py(14.40):.1f}" width="{0.50*S:.1f}" height="{2.40*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.9"/>')

    # 12. Porche Sur Cubierto + Churrasqueira Galaica:
    # Bloque Churrasqueira de Granito en cierre Este del Porche (X=14.15..14.90, Y=18.25..20.85 -> Parrilla 90cm + Fregadero aux + Leñero)
    out.append(f'<rect x="{px(14.15):.1f}" y="{py(18.25):.1f}" width="{0.75*S:.1f}" height="{2.60*S:.1f}" fill="#1e293b" stroke="#f97316" stroke-width="1.3"/>')
    out.append(f'<rect x="{px(14.22):.1f}" y="{py(18.40):.1f}" width="{0.58*S:.1f}" height="{0.95*S:.1f}" fill="#451a03" stroke="#f59e0b" stroke-width="1.1"/>')
    for gy in [18.55, 18.70, 18.85, 19.00, 19.15]:
        out.append(f'<line x1="{px(14.26):.1f}" y1="{py(gy):.1f}" x2="{px(14.76):.1f}" y2="{py(gy):.1f}" stroke="#f97316" stroke-width="0.8"/>')
    out.append(sink_cad(px(14.25), py(19.65), 0.50*S, 0.65*S, False))
    out.append(f'<text x="{px(14.52):.1f}" y="{py(20.60):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="5.5" font-weight="700">CHURRASQUEIRA</text>')

    # Mesa Comedor Exterior (2,80 x 1,10 m en X=10.30..13.10, Y=18.95..20.05) + Zona Chill-out Oeste (X=4.20..7.80, Y=18.70..20.40)
    out.append(f'<rect x="{px(10.30):.1f}" y="{py(18.95):.1f}" width="{2.80*S:.1f}" height="{1.10*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="1.0"/>')
    out.append(f'<rect x="{px(4.30):.1f}" y="{py(18.75):.1f}" width="{2.60*S:.1f}" height="{0.85*S:.1f}" rx="3" fill="#0f172a" stroke="#94a3b8" stroke-width="0.9"/>')
    out.append(f'<rect x="{px(4.80):.1f}" y="{py(19.75):.1f}" width="{1.50*S:.1f}" height="{0.65*S:.1f}" fill="#0f172a" stroke="#64748b" stroke-width="0.8"/>')

    # NHG Ø1.50m Circles
    out.append(nhg_circle(px(9.35), py(16.20), S, "Ø1,50m SALÓN"))
    out.append(nhg_circle(px(9.10), py(19.50), S, "Ø1,50m PORCHE"))

    # Structural Pillars
    pillars = [(x, y) for x in [3.00, 8.00, 12.00, 14.00, 17.00] for y in [13.00, 18.00]] + [(3.00, 21.00), (8.00, 21.00), (12.00, 21.00), (15.00, 21.00)]
    out.append(draw_pillars(pillars, px, py, 0.25, S))

    # ==========================================================================
    # MEP INSTALLATIONS OVERLAY (ZONA SUR 1:50)
    # ==========================================================================
    out.append('<g opacity="0.92">')
    # Impulsión VMC Doble Flujo a Salón (+40 m³/h) y Comedor (+35 m³/h)
    out.append(mep_symbol(px(4.20), py(13.55), "vmc_imp", "+40 m³/h"))
    out.append(mep_symbol(px(15.80), py(13.85), "vmc_imp", "+35 m³/h"))
    out.append(f'<polyline points="{px(4.20):.1f},{py(13.55):.1f} {px(15.80):.1f},{py(13.55):.1f} {px(15.80):.1f},{py(13.85):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="6,3"/>')

    # Puntos de Datos RJ45 Cat6A + Schuko C2 en Muro TV y Mesa Comedor + Exterior IP65 en Porche
    out.append(mep_symbol(px(3.30), py(16.10), "rj45", "2×RJ45 TV/Audio"))
    out.append(mep_symbol(px(3.30), py(16.55), "schuko", "5×C2 AV"))
    out.append(mep_symbol(px(6.00), py(15.95), "schuko", "Caja Suelo IP66"))
    out.append(mep_symbol(px(9.50), py(17.75), "thermostat", "KNX Salón/Com."))
    out.append(mep_symbol(px(14.10), py(19.65), "schuko", "2×C2 IP65 BBQ"))

    # Tuberías impulsión/retorno/fondo Piscina Ø63 mm PEAD hacia Arqueta Salina
    out.append(f'<polyline points="{px(13.50):.1f},{py(22.75):.1f} {px(14.00):.1f},{py(22.75):.1f}" fill="none" stroke="#38bdf8" stroke-width="2.0"/>')
    out.append(f'<polyline points="{px(6.20):.1f},{py(23.55):.1f} {px(14.00):.1f},{py(23.10):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.3" stroke-dasharray="5,3"/>')
    out.append('</g>')

    # Room Stamps
    out.append(room_stamp(px(6.40), py(13.50), "11A. SALÓN ESTAR", 26.50, "Altura 2,80m · Muro Granito + Stûv 21", "E-11A"))
    out.append(room_stamp(px(12.65), py(13.95), "11B. COMEDOR PRINCIPAL", 17.50, "Mesa 10 pax · Cota ±0,00 m", "E-11B"))
    out.append(room_stamp(px(8.80), py(18.55), "12. PORCHE SUR + CHURRASQUEIRA", 36.00, "Fondo 3,00 m · Cota ±0,00 m · Porcelánico C3", "E-12"))
    out.append(room_stamp(px(9.75), py(23.45), "13. PISCINA SALINA CLIMATIZADA", 26.25, "Lámina 7,50 × 3,50 m · Prof. 1,20 - 1,65 m", "E-13"))

    # ==========================================================================
    # CHAINED ARCHITECTURAL DIMENSIONS (ZONA SUR 1:50)
    # ==========================================================================
    out.append(dim_h(px(3.00), px(9.50), py(13.00), -22, "6,50 m (Zona Salón Estar)"))
    out.append(dim_h(px(9.50), px(17.00), py(13.00), -22, "7,50 m (Zona Comedor Principal)"))
    out.append(dim_h(px(3.80), px(8.80), py(18.00), -20, "5,00 m (Corredera C-07)", "#fbbf24"))
    out.append(dim_h(px(10.80), px(14.30), py(18.00), -20, "3,50 m (Corredera C-08)", "#fbbf24"))
    out.append(dim_h(px(3.00), px(15.00), py(21.00), 22, "12,00 m (Frente Porche Cubierto Sur + Churrasqueira)"))
    out.append(dim_h(px(6.00), px(13.50), py(25.30), 22, "7,50 m (Vaso Piscina Desbordante)", "#38bdf8"))

    # Vertical Dimensions
    out.append(dim_v(py(13.00), py(18.00), px(3.00), -28, "5,00 m (Crujía Salón-Comedor Eje 3-4)"))
    out.append(dim_v(py(18.00), py(21.00), px(3.00), -28, "3,00 m (Fondo Porche Sur)"))
    out.append(dim_v(py(21.80), py(25.30), px(6.00), -24, "3,50 m (Ancho Piscina)", "#38bdf8"))
    out.append(dim_v(py(13.00), py(21.00), px(17.00), 28, "8,00 m (Salón + Porche Sur)"))

    # Right Side Technical Panel
    out.append(mep_legend_panel(1224, 26, 548))

    out.append('<g transform="translate(1224, 470)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="548" height="295" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="548" height="22" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15" fill="#38bdf8" font-size="7.8" font-weight="700">ESPECIFICACIONES CONSTRUCTIVAS — SALÓN, PORCHE SUR Y PISCINA</text>')
    specs = [
        ("11. SALÓN-COMEDOR DIÁFANO CON DOBLE ORIENTACIÓN PATIO / SUR (44,00 m²):", "#38bdf8", [
            "• Doble transparencia Norte-Sur: recibe sol directo por el Sur y mira al Arce Japonés del Patio al Norte.",
            "• Muro inercial de granito silvestre al Oeste (e=45,5 cm) con chimenea estanca Stûv 21 (toma ext. Ø150 mm).",
            "• Cajas de suelo empotradas IP66 bajo zona de sofá para evitar cables vistos en pavimento de roble.",
        ]),
        ("12. PORCHE SUR DE 3,00 m DE FONDO + CHURRASQUEIRA GALAICA (36,00 m²):", "#fbbf24", [
            "• Alero estructural de 3,00 m calculado para latitud 43°20' N (Oleiros): sombra total en junio/julio y sol en invierno.",
            "• Churrasqueira de granito con parrilla inox 90 cm, campana con tiro sobre cubierta y fregadero auxiliar AF/ACS.",
            "• Enrasado interior-exterior ±0,00 m con guía embutida sobre Purenit 50 mm y canaleta lineal ACO Inox.",
        ]),
        ("13. PISCINA DE CLORACIÓN SALINA Y SOLÁRIUM C3 (7,50 × 3,50 m = 26,25 m²):", "#10b981", [
            "• Vaso de hormigón gunitado con revestimiento porcelánico 60×60 cm e iluminación subacuática LED RGBW 12V DC.",
            "• Preinstalación hidráulica y eléctrica para bomba de calor reversible e impulsor contracorriente.",
        ]),
    ]
    sy = 38
    for stitle, scol, bullets in specs:
        out.append(f'<text x="12" y="{sy}" fill="{scol}" font-size="6.5" font-weight="700">{stitle}</text>')
        sy += 13
        for b in bullets:
            out.append(f'<text x="18" y="{sy}" fill="#cbd5e1" font-size="5.8">{b}</text>')
            sy += 13
        sy += 6
    out.append('</g>')

    out.append(north_and_scale(1290, 845, S, 5))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-03",
        title="PLANTA CONSTRUCTIVA E INSTALACIONES — ZONA SUR PB Y PISCINA",
        scale="1:50 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN",
        subtitle="Salón-Comedor 44 m², Muro Inercial con Chimenea Stûv 21, Porche Sur 36 m², Churrasqueira y Piscina",
        extra_notes=[
            "Estancias incluidas: 11A Salón Estar (26,50 m²), 11B Comedor (17,50 m²), 12 Porche Sur (36,00 m²), 13 Piscina (26,25 m²)",
            "Cota Pavimento Salón, Comedor, Porche Sur y Solárium: ±0,00 m (accesibilidad universal sin resaltes)",
            "Carpinterías Gran Formato: C-07 (5,00×2,60 m, 3 hojas) y C-08 (3,50×2,60 m, 2 hojas) con vidrio triple control solar",
            "Coordenadas referidas a Esquina Noroeste de Parcela (0,00 ; 0,00) · Ejes Estructurales A-E / 3-5",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


def main():
    files = [
        ("plano_constructivo_zona_norte_pb.svg", build_zona_norte_pb_svg()),
        ("plano_constructivo_centro_patio_cocina_pb.svg", build_centro_patio_cocina_pb_svg()),
        ("plano_constructivo_sur_salon_porche_pb.svg", build_sur_salon_porche_pb_svg()),
    ]
    for fname, content in files:
        for folder in [BASE_DIR, os.path.join(BASE_DIR, "propuestas")]:
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Written {path} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
