#!/usr/bin/env python3
"""
Generador de Planos Constructivos de Ejecución e Instalaciones:
  - plano_constructivo_planta_primera_p1.svg (Plano E-04: Planta Primera Completa +3,15 m a Escala 1:50)
  - plano_secciones_y_detalle_constructivo.svg (Plano E-05: Secciones A-A' y B-B' 1:50 + Detalles 1:20)
Propuesta D — Pabellón Bioclimático con Patio Central (Oleiros, A Coruña)
"""
import os
from cad_engine import (
    fmt_m, svg_defs, draw_grid_axes, draw_pillars, draw_wall,
    dim_h, dim_v, door_swing, sliding_door, window_cad,
    room_stamp, nhg_circle, wc_cad, sink_cad, shower_cad,
    bed_cad, wardrobe_cad, mep_symbol, north_and_scale, title_block,
    sanitize_svg_text
)
from generate_constructive_1_50_plans import mep_legend_panel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==============================================================================
# PLANO E-04: PLANTA PRIMERA COMPLETA (+3,15 m) E INSTALACIONES (ESCALA 1:50)
# ==============================================================================
def build_planta_primera_1_50_svg() -> str:
    W, H = 1800, 1240
    S = 72.0  # 1m = 72px (Escala 1:50 de alta precisión para crujía X=3..17m, Y=8..20.5m)
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
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO E-04 · EJECUCIÓN E INSTALACIONES PLANTA PRIMERA (+3,15 m) — ZONA DE NOCHE (ESCALA 1:50)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Galería Acústica 4+4 Silence · Dormitorios Hijos con mediana Rw≥50dB · Master Suite con Vestidor y Baño · Balcón Sur Continuo</text>',
        f'<rect x="28" y="68" width="1180" height="995" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Structural Axes
    x_axes = [("A", 3.00), ("B", 8.00), ("C", 12.00), ("D", 14.00), ("E", 17.00)]
    y_axes = [("2", 9.00), ("3", 13.00), ("4", 18.00), ("4B", 19.40)]
    out.append(draw_grid_axes(x_axes, y_axes, px(2.60), px(17.40), py(8.10), py(20.40), px, py))

    # Cubierta Técnica No Transitable al Norte (Y=8.10..9.00) con Grava + 12 Paneles FV 5,4 kWp
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(8.15):.1f}" width="{14.00*S:.1f}" height="{0.85*S:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="1.0" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(8.62):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="6.5" font-weight="700">CUBIERTA PLANA INVERTIDA DE GRAVA (BANDA NORTE PB · COTA +3,35 m) + CAMPO SOLAR FV 5,4 kWp</text>')

    # ==========================================================================
    # FLOOR SURFACES PLANTA PRIMERA (+3,15 m)
    # ==========================================================================
    # Vacío del Patio Central Corrala (X=8.00..12.00, Y=9.00..13.00 -> 4,00 x 4,00 m)
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(9.00):.1f}" width="{4.00*S:.1f}" height="{4.00*S:.1f}" fill="#070b14" stroke="#10b981" stroke-width="1.6"/>')
    out.append(f'<line x1="{px(8.00):.1f}" y1="{py(9.00):.1f}" x2="{px(12.00):.1f}" y2="{py(13.00):.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4"/>')
    out.append(f'<line x1="{px(12.00):.1f}" y1="{py(9.00):.1f}" x2="{px(8.00):.1f}" y2="{py(13.00):.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4"/>')
    out.append(f'<circle cx="{px(10.00):.1f}" cy="{py(11.00):.1f}" r="{0.55*S:.1f}" fill="none" stroke="#10b981" stroke-width="1.1" stroke-dasharray="4,3"/>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(10.85):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="6.8" font-weight="700">VACÍO PATIO CENTRAL</text>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(11.15):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.8">(PROYECCIÓN COPA ARCE)</text>')

    # 12. Desembarco Escalera y Galería Acústica:
    # Tramo Oeste escalera (X=5.20..8.00, Y=9.00..13.00) + Pasarela Acústica Sur del Patio (X=8.00..13.00, Y=13.00..14.15)
    out.append(f'<rect x="{px(5.20):.1f}" y="{py(9.00):.1f}" width="{2.80*S:.1f}" height="{4.00*S:.1f}" fill="#131c31" stroke="none"/>')
    out.append(f'<rect x="{px(8.00):.1f}" y="{py(13.00):.1f}" width="{5.00*S:.1f}" height="{1.15*S:.1f}" fill="#131c31" stroke="none"/>')

    # 13. Baño Compartido Hijos (Noroeste P1: X=3.00..5.20, Y=9.00..12.10 -> 2,20 x 3,10 = 6,80 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(9.00):.1f}" width="{2.20*S:.1f}" height="{3.10*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # 14. Dormitorio Hijo 1 (Niña) (Suroeste P1: X=3.00..7.60, Y=14.15..18.00 + recodo entrada -> 14,60 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(12.10):.1f}" width="{2.20*S:.1f}" height="{2.05*S:.1f}" fill="#131c31" stroke="none"/>')
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(14.15):.1f}" width="{4.60*S:.1f}" height="{3.85*S:.1f}" fill="#131c31" stroke="none"/>')

    # 15. Dormitorio Hijo 2 (Niño) (Centro-Sur P1: X=7.60..11.40, Y=14.15..18.00 -> 3,80 x 3,85 = 14,60 m²)
    out.append(f'<rect x="{px(7.60):.1f}" y="{py(14.15):.1f}" width="{3.80*S:.1f}" height="{3.85*S:.1f}" fill="#131c31" stroke="none"/>')

    # 16C. Baño Privado Master Suite (Noreste P1: X=12.00..14.60, Y=9.00..11.45 -> 2,60 x 2,45 = 6,30 m²)
    out.append(f'<rect x="{px(12.00):.1f}" y="{py(9.00):.1f}" width="{2.60*S:.1f}" height="{2.45*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # 16B. Vestidor Doble Pasante Suite (Este P1: X=14.60..17.00, Y=9.00..12.50 -> 2,40 x 3,50 = 8,40 m²)
    out.append(f'<rect x="{px(14.60):.1f}" y="{py(9.00):.1f}" width="{2.40*S:.1f}" height="{3.50*S:.1f}" fill="#131c31" stroke="none"/>')

    # 16A. Dormitorio Principal Master Suite (Sureste P1: X=11.40..17.00, Y=12.50..18.00 -> 16,50 m² netos dormitorio)
    out.append(f'<rect x="{px(11.40):.1f}" y="{py(12.50):.1f}" width="{5.60*S:.1f}" height="{5.50*S:.1f}" fill="#131c31" stroke="none"/>')

    # 17. Balcón-Terraza Sur Continuo (X=3.00..17.00, Y=18.00..19.40 -> 14,00 x 1,40 m · S.Útil computable 14,00 m²)
    out.append(f'<rect x="{px(3.00):.1f}" y="{py(18.00):.1f}" width="{14.00*S:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-tile-60)" stroke="#38bdf8" stroke-width="1.4"/>')
    # Barandilla de vidrio laminar estructural 10+10.2 mm en perfil oculto U de aluminio
    out.append(f'<line x1="{px(3.00):.1f}" y1="{py(19.36):.1f}" x2="{px(17.00):.1f}" y2="{py(19.36):.1f}" stroke="#e0f2fe" stroke-width="2.0"/>')
    out.append(f'<text x="{px(10.00):.1f}" y="{py(19.60):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="6.2" font-weight="700">BARANDILLA VIDRIO LAMINAR TEMPLADO 10+10.2 mm EN U OCULTA EN FORJADO (h=1,10 m · CTE DB-SUA 1)</text>')

    # ==========================================================================
    # WALLS & ACOUSTIC PARTITIONS (1:50)
    # ==========================================================================
    tw_ext = 0.40 * S
    tw_int = 0.12 * S
    # Perímetro exterior P1
    out.append(draw_wall(px(3.00), py(9.00), px(8.00), py(9.00), tw_ext, True))
    out.append(draw_wall(px(12.00), py(9.00), px(17.00), py(9.00), tw_ext, True))
    out.append(draw_wall(px(3.00), py(9.00), px(3.00), py(18.00), tw_ext, True))
    out.append(draw_wall(px(17.00), py(9.00), px(17.00), py(18.00), tw_ext, True))
    out.append(draw_wall(px(3.00), py(18.00), px(17.00), py(18.00), tw_ext, True))
    # Muro Este del Patio Central (X=12.00, Y=9.00..13.00)
    out.append(draw_wall(px(12.00), py(9.00), px(12.00), py(13.00), tw_ext, True))

    # C-15: Cerramiento Acústico de Vidrio Laminado 4+4 Silence (Rw = 42 dB) en Galería del Patio (Oeste X=8.00 y Sur Y=13.00)
    out.append(sliding_door(px(8.00), py(9.00), 4.00*S, tw_ext*0.65, "v", 2, "C-15A GALERÍA ACÚSTICA 4+4 SILENCE (Rw=42 dB)"))
    out.append(sliding_door(px(8.00), py(13.00), 4.00*S, tw_ext*0.65, "h", 2, "C-15B GALERÍA ACÚSTICA 4+4 SILENCE (Rw=42 dB)"))

    # Tabiquería interior y medianeras acústicas Rw ≥ 50 dB entre dormitorios
    out.append(draw_wall(px(5.20), py(9.00), px(5.20), py(12.10), tw_int, False))  # Baño Hijos | Escalera
    out.append(draw_wall(px(3.00), py(12.10), px(5.20), py(12.10), tw_int, False)) # Baño Hijos | Acceso Dorm 1
    out.append(draw_wall(px(5.20), py(14.15), px(11.40), py(14.15), tw_int, False)) # Pasarela Galería | Dorms 1 y 2
    # Medianera Acústica Ciega entre Dormitorio 1 y Dormitorio 2 (X=7.60, Y=14.15..18.00 · Doble placa 12,5+12,5 + Lana 70kg/m³ Rw ≥ 50 dB)
    out.append(draw_wall(px(7.60), py(14.15), px(7.60), py(18.00), tw_int*1.25, False))
    out.append(f'<line x1="{px(7.60):.1f}" y1="{py(14.15):.1f}" x2="{px(7.60):.1f}" y2="{py(18.00):.1f}" stroke="#f59e0b" stroke-width="1.3" stroke-dasharray="4,2"/>')
    # Medianera Acústica entre Dormitorio 2 y Master Suite (X=11.40, Y=14.15..18.00)
    out.append(draw_wall(px(11.40), py(13.00), px(11.40), py(18.00), tw_int*1.25, False))
    out.append(f'<line x1="{px(11.40):.1f}" y1="{py(13.00):.1f}" x2="{px(11.40):.1f}" y2="{py(18.00):.1f}" stroke="#f59e0b" stroke-width="1.3" stroke-dasharray="4,2"/>')
    # Tabiques Suite (Baño Suite | Vestidor | Dormitorio)
    out.append(draw_wall(px(14.60), py(9.00), px(14.60), py(12.50), tw_int, False))
    out.append(draw_wall(px(12.00), py(11.45), px(14.60), py(11.45), tw_int, False))
    out.append(draw_wall(px(12.00), py(12.50), px(15.20), py(12.50), tw_int, False))

    # ==========================================================================
    # CARPINTERÍAS INTERIORES Y EXTERIORES P1 (C-11..C-15)
    # ==========================================================================
    # Puertas interiores acústicas Rw ≥ 35 dB con burlete perimetral y guillotina inferior
    out.append(door_swing(px(5.20), py(10.80), 0.82*S, "left", "down", "P-11 0,82"))      # Baño Hijos
    out.append(door_swing(px(5.45), py(14.15), 0.82*S, "down", "right", "P-12 0,82"))     # Dorm 1 Niña
    out.append(door_swing(px(8.25), py(14.15), 0.82*S, "down", "right", "P-13 0,82"))     # Dorm 2 Niño
    out.append(door_swing(px(11.40), py(13.15), 0.85*S, "right", "down", "P-14 SUITE"))   # Acceso Suite
    out.append(sliding_door(px(15.40), py(12.50), 0.90*S, tw_int, "h", 1, "P-15 VEST."))  # Vestidor -> Dorm
    out.append(sliding_door(px(14.60), py(10.05), 0.82*S, tw_int, "v", 1, "P-16 BAÑO"))   # Vestidor -> Baño Suite

    # Ventanas y Balconeras Fachadas Sur, Norte y Este
    # C-11A y C-11B: Balconeras Sur Dormitorios Infantiles (2,20 x 2,25 m)
    out.append(sliding_door(px(4.10), py(18.00), 2.20*S, tw_ext*0.8, "h", 2, "C-11A BALCONERA D1 (2,20×2,25)"))
    out.append(sliding_door(px(8.40), py(18.00), 2.20*S, tw_ext*0.8, "h", 2, "C-11B BALCONERA D2 (2,20×2,25)"))
    # C-12: Gran Balconera Sur Master Suite (3,20 x 2,25 m)
    out.append(sliding_door(px(12.60), py(18.00), 3.20*S, tw_ext*0.8, "h", 2, "C-12 BALCONERA SUITE (3,20×2,25)"))
    # C-13: Ventana Baño Hijos Norte (X=3.65..4.65, Y=9.00)
    out.append(window_cad(px(3.65), py(9.00), 1.00*S, tw_ext, "h", "C-13 1,00×0,80"))
    # C-14: Ventana Baño Suite Norte (X=12.80..13.80, Y=9.00)
    out.append(window_cad(px(12.80), py(9.00), 1.00*S, tw_ext, "h", "C-14 1,00×0,80"))
    # C-14B: Ventana Luz Natural Este en Vestidor Suite (X=17.00, Y=10.25..11.25)
    out.append(window_cad(px(17.00), py(10.25), 1.00*S, tw_ext, "v", "C-14B 1,00×1,20"))

    # ==========================================================================
    # MOBILIARIO TÉCNICO Y SANITARIOS P1 (ESCALA 1:50)
    # ==========================================================================
    # Escalera de llegada a P1 (X=5.35..6.50, Y=9.25..12.80)
    st_x, st_y, st_w, st_h = px(5.35), py(9.25), 1.15*S, 3.55*S
    out.append(f'<rect x="{st_x:.1f}" y="{st_y:.1f}" width="{st_w:.1f}" height="{st_h:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    for i in range(1, 17):
        sy = st_y + i * (st_h / 17)
        out.append(f'<line x1="{st_x:.1f}" y1="{sy:.1f}" x2="{st_x+st_w:.1f}" y2="{sy:.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<text x="{st_x+st_w/2:.1f}" y="{st_y+st_h+11:.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">DESEMBARCO +3,15 m</text>')

    # 13. Baño Compartido Hijos (6,80 m²):
    # Ducha / Bañera en Norte (X=3.12..5.08, Y=9.12..9.95)
    out.append(shower_cad(px(3.12), py(9.12), 1.96*S, 0.83*S))
    # Mueble Doble Lavabo en Oeste (X=3.12..3.65, Y=10.15..11.45)
    out.append(sink_cad(px(3.12), py(10.15), 0.52*S, 1.30*S, True))
    # Inodoro suspendido (X=3.12..3.68, Y=11.52..11.98)
    out.append(wc_cad(px(3.12), py(11.52), 0.55*S, 0.42*S, "right"))

    # 14. Dormitorio Hijo 1 (Niña · 14,60 m²):
    # Armario empotrado en tabique Norte/Acceso (X=3.12..4.95, Y=12.22..12.82)
    out.append(wardrobe_cad(px(3.12), py(12.22), 1.83*S, 0.60*S, "h", "ARMARIO EMPOTRADO 1,85×0,60m"))
    # Cama 1,35 x 2,00 m apoyada en muro Oeste con cabecero tapizado (X=3.15..5.15, Y=15.05..16.40)
    out.append(bed_cad(px(3.15), py(15.05), 2.00*S, 1.35*S, "W", False, "CAMA 135×200"))
    # Mesa de Estudio ergonómica (1,60 x 0,65 m) en pared Este mirando al Este -> recibe luz Sur a 90° lateral derecha
    out.append(f'<rect x="{px(6.82):.1f}" y="{py(15.55):.1f}" width="{0.65*S:.1f}" height="{1.60*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<circle cx="{px(6.52):.1f}" cy="{py(16.35):.1f}" r="{0.24*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(7.14):.1f}" y="{py(16.35):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" transform="rotate(-90 {px(7.14):.1f} {py(16.35):.1f})">ESTUDIO (LUZ 90°)</text>')

    # 15. Dormitorio Hijo 2 (Niño · 14,60 m²):
    # Armario empotrado en Norte (X=9.25..11.25, Y=14.25..14.85)
    out.append(wardrobe_cad(px(9.25), py(14.25), 2.00*S, 0.60*S, "h", "ARMARIO EMPOTRADO 2,00×0,60m"))
    # Cama 1,35 x 2,00 m apoyada en tabique acústico Oeste (pero separada de la mesa del Dorm 1 por cámara acústica Rw≥50dB)
    out.append(bed_cad(px(7.72), py(15.20), 2.00*S, 1.35*S, "W", False, "CAMA 135×200"))
    # Mesa de Estudio (1,60 x 0,65 m) en pared Este -> recibe luz Sur a 90° lateral derecha
    out.append(f'<rect x="{px(10.62):.1f}" y="{py(15.55):.1f}" width="{0.65*S:.1f}" height="{1.60*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<circle cx="{px(10.32):.1f}" cy="{py(16.35):.1f}" r="{0.24*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(10.94):.1f}" y="{py(16.35):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" transform="rotate(-90 {px(10.94):.1f} {py(16.35):.1f})">ESTUDIO (LUZ 90°)</text>')

    # 16C. Baño Privado Master Suite (6,30 m²):
    # Ducha Doble Walk-in Raindance (X=12.12..13.05, Y=9.12..11.32 -> 0,93 x 2,20 m)
    out.append(shower_cad(px(12.12), py(9.12), 0.93*S, 2.20*S))
    # Encimera Doble Seno Suspendida (X=13.20..14.48, Y=9.12..9.68 -> 1,28 x 0,56 m)
    out.append(sink_cad(px(13.20), py(9.12), 1.28*S, 0.56*S, True))
    # Inodoro Geberit suspendido en cabina (X=13.85..14.48, Y=10.75..11.25)
    out.append(wc_cad(px(13.90), py(10.75), 0.55*S, 0.42*S, "left"))

    # 16B. Vestidor Doble Pasante en Paralelo (8,40 m²):
    # Dos frentes de armarios de 2,80 m lineales cada uno (Oeste X=14.70..15.30 y Este X=16.28..16.88) dejando pasillo central de 1,00 m con ventana Este
    out.append(wardrobe_cad(px(14.70), py(9.15), 0.60*S, 2.95*S, "v", "VESTIDOR LADO A (2,95m)"))
    out.append(wardrobe_cad(px(16.28), py(9.15), 0.60*S, 2.95*S, "v", "VESTIDOR LADO B (2,95m)"))

    # 16A. Dormitorio Principal Master Suite (16,50 m²):
    # Cama King Size 1,80 x 2,00 m con cabecero al Norte + 2 mesillas integradas (X=13.25..15.05, Y=12.65..14.65)
    out.append(bed_cad(px(13.25), py(12.65), 1.80*S, 2.00*S, "N", True, "KING SIZE 180×200"))
    out.append(f'<rect x="{px(12.68):.1f}" y="{py(12.68):.1f}" width="{0.50*S:.1f}" height="{0.45*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{px(15.12):.1f}" y="{py(12.68):.1f}" width="{0.50*S:.1f}" height="{0.45*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')
    # Banco descalzador a pie de cama (1,50 x 0,45 m) + Butaca de lectura junto al Balcón Sur
    out.append(f'<rect x="{px(13.40):.1f}" y="{py(14.72):.1f}" width="{1.50*S:.1f}" height="{0.42*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')
    out.append(f'<rect x="{px(15.95):.1f}" y="{py(15.80):.1f}" width="{0.75*S:.1f}" height="{0.75*S:.1f}" rx="4" fill="#1e293b" stroke="#94a3b8" stroke-width="0.9"/>')

    # NHG Ø1.50m Accessibility & Space Verification Circles
    out.append(nhg_circle(px(5.85), py(16.95), S, "Ø1,50m D1"))
    out.append(nhg_circle(px(9.45), py(16.95), S, "Ø1,50m D2"))
    out.append(nhg_circle(px(14.15), py(16.35), S, "Ø1,50m SUITE"))
    out.append(nhg_circle(px(13.65), py(10.25), S, "Ø1,50m BAÑO"))

    # Structural Pillars P1
    pillars = [(x, y) for x in [3.00, 8.00, 12.00, 14.00, 17.00] for y in [9.00, 13.00, 18.00]]
    out.append(draw_pillars(pillars, px, py, 0.25, S))

    # ==========================================================================
    # MEP INSTALLATIONS OVERLAY P1 (1:50)
    # ==========================================================================
    out.append('<g opacity="0.92">')
    # Montantes y red VMC Doble Flujo en Planta Primera:
    # Impulsión aire limpio (Azul cian Ø90mm) a Dormitorio 1 (+30 m³/h), Dormitorio 2 (+30 m³/h) y Master Suite (+45 m³/h)
    out.append(f'<polyline points="{px(6.80):.1f},{py(13.55):.1f} {px(4.50):.1f},{py(14.55):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.6" stroke-dasharray="6,3"/>')
    out.append(f'<polyline points="{px(6.80):.1f},{py(13.55):.1f} {px(10.00):.1f},{py(13.55):.1f} {px(15.80):.1f},{py(13.55):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.6" stroke-dasharray="6,3"/>')
    out.append(mep_symbol(px(4.50), py(14.55), "vmc_imp", "+30 m³/h"))
    out.append(mep_symbol(px(9.60), py(15.20), "vmc_imp", "+30 m³/h"))
    out.append(mep_symbol(px(15.80), py(13.55), "vmc_imp", "+45 m³/h"))

    # Extracción aire viciado (Rojo/Cian Ø90mm) en Baño Hijos (-35 m³/h), Baño Suite (-35 m³/h) y Vestidor (-15 m³/h)
    out.append(mep_symbol(px(4.35), py(10.20), "vmc_ext", "-35 m³/h"))
    out.append(mep_symbol(px(13.30), py(10.80), "vmc_ext", "-35 m³/h"))
    out.append(mep_symbol(px(15.75), py(9.65), "vmc_ext", "-15 m³/h"))

    # Bajantes Acústicas PVC Serie B Ø110 mm en patinillos registrables
    out.append(mep_symbol(px(3.25), py(11.85), "drain", "BAJANTE ACÚST. B-01 Ø110"))
    out.append(mep_symbol(px(14.35), py(11.20), "drain", "BAJANTE ACÚST. B-02 Ø110"))

    # Tomas RJ45 Cat6A + Schuko C2 en mesas de estudio y cabeceros + Termostatos KNX por dormitorio
    out.append(mep_symbol(px(6.95), py(16.10), "rj45", "2×RJ45 D1"))
    out.append(mep_symbol(px(6.95), py(16.65), "schuko", "3×C2 Mesa"))
    out.append(mep_symbol(px(10.75), py(16.10), "rj45", "2×RJ45 D2"))
    out.append(mep_symbol(px(10.75), py(16.65), "schuko", "3×C2 Mesa"))
    out.append(mep_symbol(px(16.70), py(14.20), "rj45", "RJ45 TV Suite"))
    out.append(mep_symbol(px(6.35), py(14.35), "thermostat", "KNX D1"))
    out.append(mep_symbol(px(8.95), py(14.35), "thermostat", "KNX D2"))
    out.append(mep_symbol(px(11.95), py(12.75), "thermostat", "KNX Suite"))
    out.append('</g>')

    # Room Stamps
    out.append(room_stamp(px(10.30), py(13.55), "12. GALERÍA ACÚSTICA", 8.20, "Roble 14mm · Vidrio 4+4 Silence", "E-14"))
    out.append(room_stamp(px(4.25), py(11.00), "13. BAÑO HIJOS", 6.80, "Porcelánico · Doble Lavabo", "E-15"))
    out.append(room_stamp(px(4.95), py(17.25), "14. DORM. HIJO 1 (NIÑA)", 14.60, "Roble 14mm · Estudio Luz 90°", "E-16"))
    out.append(room_stamp(px(9.15), py(17.25), "15. DORM. HIJO 2 (NIÑO)", 14.60, "Roble 14mm · Mediana Rw≥50dB", "E-17"))
    out.append(room_stamp(px(14.15), py(15.65), "16A. MASTER SUITE", 16.50, "Cama 180×200 · Vistas Sur", "E-18A"))
    out.append(room_stamp(px(15.75), py(11.65), "16B. VESTIDOR SUITE", 8.40, "5,90 m lineales armarios", "E-18B"))
    out.append(room_stamp(px(13.45), py(10.05), "16C. BAÑO SUITE", 6.30, "Doble Ducha + Doble Seno", "E-18C"))
    out.append(room_stamp(px(9.80), py(18.70), "17. BALCÓN SUR CONTINUO", 14.00, "Fondo 1,40 m · Sombra a PB", "E-19"))

    # ==========================================================================
    # CHAINED ARCHITECTURAL DIMENSIONS P1 (1:50)
    # ==========================================================================
    # Top Chained Dimensions
    out.append(dim_h(px(3.00), px(5.20), py(9.00), -22, "2,20 m (Baño Hijos)"))
    out.append(dim_h(px(5.20), px(8.00), py(9.00), -22, "2,80 m (Escalera / Desemb.)"))
    out.append(dim_h(px(8.00), px(12.00), py(9.00), -22, "4,00 m (Vacío Patio Central)", "#10b981"))
    out.append(dim_h(px(12.00), px(14.60), py(9.00), -22, "2,60 m (Baño Suite)"))
    out.append(dim_h(px(14.60), px(17.00), py(9.00), -22, "2,40 m (Vestidor)"))
    out.append(dim_h(px(3.00), px(17.00), py(8.15), -28, "14,00 m (ANCHO TOTAL PLANTA PRIMERA EJE A - EJE E)", "#f8fafc"))

    # South Bedrooms Breakdown
    out.append(dim_h(px(3.00), px(7.60), py(18.00), -20, "4,60 m (Dormitorio 1 Niña)", "#fbbf24"))
    out.append(dim_h(px(7.60), px(11.40), py(18.00), -20, "3,80 m (Dormitorio 2 Niño)", "#fbbf24"))
    out.append(dim_h(px(11.40), px(17.00), py(18.00), -20, "5,60 m (Master Suite Principal)", "#38bdf8"))

    # Vertical Dimensions
    out.append(dim_v(py(9.00), py(12.10), px(3.00), -26, "3,10 m (Baño Hijos)"))
    out.append(dim_v(py(12.10), py(18.00), px(3.00), -26, "5,90 m (Dormitorio 1)"))
    out.append(dim_v(py(18.00), py(19.40), px(3.00), -26, "1,40 m (Balcón)"))
    out.append(dim_v(py(9.00), py(12.50), px(17.00), 26, "3,50 m (Vestidor Suite)"))
    out.append(dim_v(py(12.50), py(18.00), px(17.00), 26, "5,50 m (Dorm. Suite)"))

    # Right Side Technical Panel
    out.append(mep_legend_panel(1224, 26, 548))

    out.append('<g transform="translate(1224, 470)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="548" height="295" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="548" height="22" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15" fill="#38bdf8" font-size="7.8" font-weight="700">CUADRO DE ESTANCIAS Y AISLAMIENTO ACÚSTICO — PLANTA PRIMERA (+3,15 m)</text>')
    rows = [
        ("E-14", "12. Galería Acústica Patio", "5,00 × 1,15 m", "8,20 m²", "Vidrio Laminado 4+4 Silence (Rw = 42 dB)"),
        ("E-15", "13. Baño Compartido Hijos", "2,20 × 3,10 m", "6,80 m²", "Doble seno + Ducha 1,96m · VMC -35 m³/h"),
        ("E-16", "14. Dormitorio Hijo 1 (Niña)", "4,60 × 3,85 m", "14,60 m²", "Mesa estudio Este (Luz 90°) · VMC +30 m³/h"),
        ("E-17", "15. Dormitorio Hijo 2 (Niño)", "3,80 × 3,85 m", "14,60 m²", "Medianera ciega Rw ≥ 50 dB · VMC +30 m³/h"),
        ("E-18A", "16A. Dormitorio Master Suite", "5,60 × 3,15 m", "16,50 m²", "Cama 180×200 · Balconera C-12 · VMC +45 m³/h"),
        ("E-18B", "16B. Vestidor Doble Suite", "2,40 × 3,50 m", "8,40 m²", "5,90 m lineales armarios + Luz natural Este"),
        ("E-18C", "16C. Baño Privado Suite", "2,60 × 2,45 m", "6,30 m²", "Doble Ducha + Doble Seno · VMC -35 m³/h"),
        ("E-19", "17. Balcón-Terraza Sur", "14,00 × 1,40 m", "14,00 m²", "Barandilla vidrio 10+10.2 mm · Sombra verano"),
    ]
    ry = 40
    for cod, est, cot, sup, obs in rows:
        out.append(f'<rect x="8" y="{ry-10}" width="532" height="20" fill="none" stroke="#1e293b" stroke-width="0.6"/>')
        out.append(f'<text x="12" y="{ry+3}" fill="#38bdf8" font-size="6.0" font-weight="700">{cod}</text>')
        out.append(f'<text x="58" y="{ry+3}" fill="#e2e8f0" font-size="6.0">{est}</text>')
        out.append(f'<text x="200" y="{ry+3}" fill="#cbd5e1" font-size="6.0">{cot}</text>')
        out.append(f'<text x="275" y="{ry+3}" fill="#10b981" font-size="6.2" font-weight="700">{sup}</text>')
        out.append(f'<text x="335" y="{ry+3}" fill="#94a3b8" font-size="5.6">{obs}</text>')
        ry += 21

    out.append('<rect x="10" y="210" width="528" height="72" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="18" y="225" fill="#10b981" font-size="6.5" font-weight="700">TOTAL SUPERFICIE ÚTIL PLANTA PRIMERA: 89,50 m² (TOTAL VIVIENDA PB + P1 = 188,40 m² ÚTILES)</text>')
    out.append('<text x="18" y="239" fill="#cbd5e1" font-size="5.8">• Privacidad Acústica Noche/Día: Galería superior cerrada con vidrio acústico 4+4 Silence (corta el ruido de Salón PB).</text>')
    out.append('<text x="18" y="252" fill="#cbd5e1" font-size="5.8">• Ergonomía Visual Infantil: Mesas de estudio ubicadas en paredes Este con entrada de luz Sur a 90° sin deslumbramiento.</text>')
    out.append('<text x="18" y="265" fill="#cbd5e1" font-size="5.8">• Separación entre Hijos: Tabique ciego multicapa (doble placa + lana mineral 70 kg/m³, Rw ≥ 50 dB) sin armarios pasantes.</text>')
    out.append('</g>')

    out.append(north_and_scale(1290, 845, S, 5))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-04",
        title="PLANTA CONSTRUCTIVA E INSTALACIONES — PLANTA PRIMERA (+3,15 m)",
        scale="1:50 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN",
        subtitle="Galería Acústica, Dormitorios Hijos, Baño Compartido, Master Suite con Vestidor/Baño y Balcón Sur",
        extra_notes=[
            "Superficie Útil Planta Primera: 89,50 m² (75,40 m² interiores cerrados + 14,00 m² Balcón Sur cubierto)",
            "Cota Pavimento Terminado P1: +3,15 m · Altura libre interior bajo falso techo: 2,60 m (Cota cubierta +6,80 m)",
            "Aislamiento Acústico entre Dormitorios: Tabique PYL 125 mm doble placa + lana mineral (Rw ≥ 50 dB · CTE DB-HR)",
            "Coordenadas referidas a Esquina Noroeste de Parcela (0,00 ; 0,00) · Ejes Estructurales A-E / 2-4",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


# ==============================================================================
# PLANO E-05: SECCIONES CONSTRUCTIVAS A-A' Y B-B' (1:50) + DETALLES 1:20
# ==============================================================================
def build_secciones_y_detalles_svg() -> str:
    W, H = 1800, 1240
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1744" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO E-05 · SECCIONES CONSTRUCTIVAS A-A\' Y B-B\' (1:50) Y DETALLES DE EJECUCIÓN A ESCALA 1:20</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Cotas Altimétricas Z · Soleamiento Estacional 43°20\'N · Detalle D-01 Barrera Anti-Radón DB-HS6 · Detalle D-02 Umbral Cota Cero Purenit · Detalle D-03 Cubierta</text>',
    ]

    # ==========================================================================
    # 1. SECCIÓN LONGITUDINAL A-A' (NORTE - SUR POR EL PATIO CENTRAL Y PISCINA)
    # ==========================================================================
    # Viewport: x=28..1160, y=68..555
    out.append('<g font-family="monospace">')
    out.append('<rect x="28" y="68" width="1132" height="485" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="28" y="68" width="1132" height="24" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="42" y="84" fill="#38bdf8" font-size="8.5" font-weight="700">SECCIÓN CONSTRUCTIVA LONGITUDINAL A-A\' (CORTE NORTE - SUR POR HALL, PATIO CORRALA, SALÓN, PORCHE Y PISCINA · ESCALA 1:50)</text>')

    # Scale for Section A-A': 1m horizontal = 42px, 1m vertical = 42px
    S_sec = 42.0
    OX_s = 70.0   # Y_plot = 3.00m starts at OX_s
    Z0_y = 435.0  # Cota Z = ±0,00 m at y = 435.0 px

    def sx(ym_plot: float) -> float:
        return OX_s + (ym_plot - 3.00) * S_sec

    def sz(zm: float) -> float:
        return Z0_y - zm * S_sec

    # Structural Axes 1, 2, 3, 4, 5 in Section A-A'
    for code, ym in [("1", 5.00), ("2", 9.00), ("3", 13.00), ("4", 18.00), ("5", 21.00)]:
        ax = sx(ym)
        out.append(f'<line x1="{ax:.1f}" y1="105" x2="{ax:.1f}" y2="515" stroke="#64748b" stroke-width="0.65" stroke-dasharray="12,4,2,4"/>')
        out.append(f'<circle cx="{ax:.1f}" cy="105" r="8.5" fill="#0b1120" stroke="#64748b" stroke-width="1.0"/>')
        out.append(f'<text x="{ax:.1f}" y="108" text-anchor="middle" fill="#e2e8f0" font-size="7.5" font-weight="700">{code}</text>')

    # Horizontal Altimetric Level Lines (Z levels)
    z_levels = [
        (+6.80, "Z = +6,80 m (Coronación Peto Cubierta P1 ≤ 7,00 m PGOM)", "#f59e0b"),
        (+5.75, "Z = +5,75 m (Falso Techo P1 · H.libre = 2,60 m)", "#64748b"),
        (+3.15, "Z = +3,15 m (Pavimento Terminado Planta Primera)", "#38bdf8"),
        (+2.80, "Z = +2,80 m (Techo Salón-Comedor PB)", "#64748b"),
        (0.00,  "Z = ±0,00 m (Cota Cero Continua Interior / Patio / Porche / Solárium)", "#10b981"),
        (-0.45, "Z = -0,45 m (Cámara Sanitaria Ventilada Cáviti + Barrera Radón)", "#64748b"),
        (-1.50, "Z = -1,50 m (Fondo Vaso Piscina Salina)", "#38bdf8"),
    ]
    for zm, zlbl, zcol in z_levels:
        zy = sz(zm)
        out.append(f'<line x1="40" y1="{zy:.1f}" x2="1145" y2="{zy:.1f}" stroke="{zcol}" stroke-width="0.6" stroke-dasharray="5,4" opacity="0.75"/>')
        out.append(f'<text x="1148" y="{zy-2:.1f}" text-anchor="end" fill="{zcol}" font-size="5.6" font-weight="700">{zlbl}</text>')

    # Terreno natural y Estrato Granítico + Cimentación / Cáviti (Y=3.50..25.50)
    out.append(f'<rect x="{sx(3.20):.1f}" y="{sz(0.00):.1f}" width="{(25.50-3.20)*S_sec:.1f}" height="{1.85*S_sec:.1f}" fill="url(#hatch-gravel)" opacity="0.45"/>')
    # Forjado sanitario Cáviti + Solera bajo edificio (Y=5.00..21.00, Z=-0.45..0.00)
    out.append(f'<rect x="{sx(5.00):.1f}" y="{sz(0.00):.1f}" width="{(21.00-5.00)*S_sec:.1f}" height="{0.45*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#e2e8f0" stroke-width="1.2"/>')
    # Lámina Anti-Radón continua (línea roja gruesa continua bajo solera)
    out.append(f'<line x1="{sx(4.80):.1f}" y1="{sz(-0.22):.1f}" x2="{sx(21.20):.1f}" y2="{sz(-0.22):.1f}" stroke="#ef4444" stroke-width="2.0" stroke-dasharray="8,3"/>')

    # Rebaje de Forjado en Patio Central Corrala (Y=9.00..13.00, Z=-0.15..0.00) + Alcorque Arce Japonés
    out.append(f'<rect x="{sx(8.00):.1f}" y="{sz(0.00):.1f}" width="{4.00*S_sec:.1f}" height="{0.18*S_sec:.1f}" fill="#070b14" stroke="#10b981" stroke-width="1.1"/>')
    # Tarima de Iroko enrasada a Z=0.00 sobre plots
    out.append(f'<line x1="{sx(8.00):.1f}" y1="{sz(0.00):.1f}" x2="{sx(12.00):.1f}" y2="{sz(0.00):.1f}" stroke="#fbbf24" stroke-width="2.2" stroke-dasharray="6,2"/>')
    # Alcorque y Árbol Arce Japonés en Sección (Y=10.20..11.80)
    out.append(f'<rect x="{sx(9.30):.1f}" y="{sz(0.00):.1f}" width="{1.40*S_sec:.1f}" height="{0.90*S_sec:.1f}" fill="#064e3b" stroke="#10b981" stroke-width="1.0"/>')
    out.append(f'<line x1="{sx(10.00):.1f}" y1="{sz(0.00):.1f}" x2="{sx(10.00):.1f}" y2="{sz(3.60):.1f}" stroke="#10b981" stroke-width="2.2"/>')
    out.append(f'<ellipse cx="{sx(10.00):.1f}" cy="{sz(3.60):.1f}" rx="{0.95*S_sec:.1f}" ry="{0.85*S_sec:.1f}" fill="#064e3b" fill-opacity="0.45" stroke="#10b981" stroke-width="1.2" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{sx(10.00):.1f}" y="{sz(3.60):.1f}" text-anchor="middle" fill="#34d399" font-size="5.8" font-weight="700">ARCE JAPONÉS</text>')

    # Muros y Forjados Seccionados en Planta Baja:
    # Muro Fachada Norte (Y=5.00, Z=0.00..3.35) + Cubierta Plana Invertida Banda Norte (Y=3.50..8.00, Z=2.85..3.35)
    out.append(f'<rect x="{sx(4.80):.1f}" y="{sz(3.35):.1f}" width="{0.40*S_sec:.1f}" height="{3.35*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{sx(3.50):.1f}" y="{sz(3.25):.1f}" width="{4.50*S_sec:.1f}" height="{0.45*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')
    # Paneles Fotovoltaicos inclinados 15° en Cubierta Norte
    for p_ym in [5.40, 6.40]:
        out.append(f'<line x1="{sx(p_ym):.1f}" y1="{sz(3.40):.1f}" x2="{sx(p_ym+0.75):.1f}" y2="{sz(3.62):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')

    # Carpinterías Patio Central: C-05 Norte (Y=8.00) y C-05C Sur (Y=12.00)
    out.append(f'<line x1="{sx(8.00):.1f}" y1="{sz(0.00):.1f}" x2="{sx(8.00):.1f}" y2="{sz(2.80):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<line x1="{sx(12.00):.1f}" y1="{sz(0.00):.1f}" x2="{sx(12.00):.1f}" y2="{sz(2.80):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    # C-15B: Vidrio Acústico 4+4 Silence en Galería P1 (Y=12.00, Z=3.15..5.95)
    out.append(f'<line x1="{sx(12.00):.1f}" y1="{sz(3.15):.1f}" x2="{sx(12.00):.1f}" y2="{sz(5.95):.1f}" stroke="#a855f7" stroke-width="2.4"/>')
    # Tabique interior Galería | Dormitorio P1 (Y=13.15, Z=3.15..5.95)
    out.append(f'<rect x="{sx(13.15):.1f}" y="{sz(5.95):.1f}" width="{0.12*S_sec:.1f}" height="{2.80*S_sec:.1f}" fill="#334155" stroke="#cbd5e1" stroke-width="1.0"/>')

    # Forjado Entrepiso P1 sobre Salón-Comedor + Balcón Sur (Y=12.00..19.40, Z=2.80..3.15)
    out.append(f'<rect x="{sx(11.20):.1f}" y="{sz(3.15):.1f}" width="{(19.40-11.20)*S_sec:.1f}" height="{0.35*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')
    # Prolongación Alero Porche Sur Cubierto hasta Y=21.00 (Fondo libre 3,00 m desde fachada Y=18.00)
    out.append(f'<rect x="{sx(19.40):.1f}" y="{sz(3.05):.1f}" width="{1.60*S_sec:.1f}" height="{0.25*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#fbbf24" stroke-width="1.2"/>')
    # Barandilla de vidrio laminar 10+10.2 mm en Balcón Sur P1 (Y=19.40, Z=3.15..4.25)
    out.append(f'<line x1="{sx(19.35):.1f}" y1="{sz(3.15):.1f}" x2="{sx(19.35):.1f}" y2="{sz(4.25):.1f}" stroke="#e0f2fe" stroke-width="2.2"/>')

    # Carpinterías Fachada Sur: C-07 Corredera Salón PB (Y=18.00, Z=0.00..2.80) y C-11 Balconera P1 (Y=18.00, Z=3.15..5.75)
    out.append(f'<line x1="{sx(18.00):.1f}" y1="{sz(0.00):.1f}" x2="{sx(18.00):.1f}" y2="{sz(2.80):.1f}" stroke="#38bdf8" stroke-width="2.6"/>')
    out.append(f'<line x1="{sx(18.00):.1f}" y1="{sz(3.15):.1f}" x2="{sx(18.00):.1f}" y2="{sz(5.75):.1f}" stroke="#38bdf8" stroke-width="2.6"/>')

    # Forjado de Cubierta Superior P1 (Y=11.60..19.40, Z=5.95..6.45) + Peto Perimetral hasta Z=+6.80m
    out.append(f'<rect x="{sx(11.60):.1f}" y="{sz(6.45):.1f}" width="{(19.40-11.60)*S_sec:.1f}" height="{0.50*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{sx(11.60):.1f}" y="{sz(6.80):.1f}" width="{0.35*S_sec:.1f}" height="{0.35*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<rect x="{sx(19.05):.1f}" y="{sz(6.80):.1f}" width="{0.35*S_sec:.1f}" height="{0.35*S_sec:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')

    # Vaso de Piscina Seccionado al Sur (Y=21.80..25.30, Z=-1.50..0.00)
    out.append(f'<path d="M {sx(21.80):.1f},{sz(0.00):.1f} V {sz(-1.50):.1f} H {sx(25.30):.1f} V {sz(0.00):.1f}" fill="#082f49" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<rect x="{sx(21.80):.1f}" y="{sz(-0.08):.1f}" width="{3.50*S_sec:.1f}" height="{1.42*S_sec:.1f}" fill="url(#hatch-water)"/>')

    # ==========================================================================
    # DIAGRAMAS SOLARES BIOCLIMÁTICOS (LATITUD 43°20' N — OLEIROS)
    # ==========================================================================
    # Sol de Verano (21 Junio · Altura solar 70°): bloqueado por alero de 3,00 m (Porche Sur) y Balcón P1 (1,40 m)
    out.append(f'<line x1="{sx(22.20):.1f}" y1="{sz(6.60):.1f}" x2="{sx(21.00):.1f}" y2="{sz(3.05):.1f}" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow-tech)"/>')
    out.append(f'<line x1="{sx(21.00):.1f}" y1="{sz(3.05):.1f}" x2="{sx(19.85):.1f}" y2="{sz(0.00):.1f}" stroke="#f59e0b" stroke-width="1.1" stroke-dasharray="3,3" opacity="0.6"/>')
    out.append(f'<text x="{sx(22.35):.1f}" y="{sz(6.40):.1f}" fill="#f59e0b" font-size="6.0" font-weight="700">SOL VERANO 70° (SOMBRA TOTAL EN VIDRIO C-07)</text>')
    # Sol de Invierno (21 Diciembre · Altura solar 23°): penetra hasta el fondo del Salón e ilumina muro inercial
    out.append(f'<line x1="{sx(24.50):.1f}" y1="{sz(4.20):.1f}" x2="{sx(13.20):.1f}" y2="{sz(0.00):.1f}" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="8,3" marker-end="url(#arrow-sec)"/>')
    out.append(f'<text x="{sx(22.60):.1f}" y="{sz(3.65):.1f}" fill="#ef4444" font-size="6.0" font-weight="700">SOL INVIERNO 23° (CAPTACIÓN SOLAR PASIVA)</text>')

    # Labels inside Section A-A' spaces
    sec_labels = [
        (4.20, 1.20, "PORCHE N"),
        (6.50, 1.35, "04. HALL ACCESO\n(H=2,65 m)"),
        (10.00, 1.35, "00. PATIO CENTRAL\n(4,00 m · Cota ±0,00)"),
        (15.00, 1.35, "11. SALÓN - COMEDOR\n(H=2,80 m · Suelo Radiante)"),
        (19.50, 1.35, "12. PORCHE SUR\n(Fondo 3,00 m)"),
        (23.55, -0.75, "13. PISCINA\n(-1,50 m)"),
        (12.55, 4.40, "GALERÍA\n4+4 SILENCE"),
        (15.60, 4.40, "14/15/16. DORMITORIOS P1\n(Cota +3,15 m · H=2,60 m)"),
    ]
    for ym, zm, txt in sec_labels:
        lines = txt.split("\n")
        for idx, l in enumerate(lines):
            out.append(f'<text x="{sx(ym):.1f}" y="{sz(zm)+idx*9:.1f}" text-anchor="middle" fill="#e2e8f0" font-size="6.0" font-weight="700">{l}</text>')

    # Chained Horizontal Dimensions along bottom of Section A-A'
    out.append(dim_h(sx(3.50), sx(5.00), sz(-0.55), 24, "1,50m"))
    out.append(dim_h(sx(5.00), sx(8.00), sz(-0.55), 24, "3,00 m (Hall)"))
    out.append(dim_h(sx(8.00), sx(12.00), sz(-0.55), 24, "4,00 m (Patio Corrala)", "#10b981"))
    out.append(dim_h(sx(12.00), sx(18.00), sz(-0.55), 24, "6,00 m (Salón-Comedor)"))
    out.append(dim_h(sx(18.00), sx(21.00), sz(-0.55), 24, "3,00 m (Porche Sur)", "#fbbf24"))
    out.append(dim_h(sx(21.80), sx(25.30), sz(-1.50), 22, "3,50 m (Ancho Piscina)", "#38bdf8"))
    out.append('</g>')

    # ==========================================================================
    # 2. SECCIÓN TRANSVERSAL B-B' (OESTE - ESTE POR PATIO CENTRAL, ESCALERA Y COCINA)
    # ==========================================================================
    # Viewport: x=1172..1772, y=68..555
    out.append('<g font-family="monospace">')
    out.append('<rect x="1172" y="68" width="600" height="485" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="1172" y="68" width="600" height="24" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="1184" y="84" fill="#38bdf8" font-size="8.0" font-weight="700">SECCIÓN TRANSVERSAL B-B\' (OESTE-ESTE POR PATIO Y COCINA · 1:50)</text>')

    S_b = 34.0
    OX_b = 1210.0  # X=2.50m starts at OX_b

    def bx(xm_plot: float) -> float:
        return OX_b + (xm_plot - 2.50) * S_b

    def bz(zm: float) -> float:
        return Z0_y - zm * S_b

    # Structural Axes A, B, C, D, E
    for code, xm in [("A", 3.00), ("B", 8.00), ("C", 12.00), ("D", 14.00), ("E", 17.00)]:
        ax = bx(xm)
        out.append(f'<line x1="{ax:.1f}" y1="105" x2="{ax:.1f}" y2="515" stroke="#64748b" stroke-width="0.65" stroke-dasharray="12,4,2,4"/>')
        out.append(f'<circle cx="{ax:.1f}" cy="105" r="8.0" fill="#0b1120" stroke="#64748b" stroke-width="1.0"/>')
        out.append(f'<text x="{ax:.1f}" y="108" text-anchor="middle" fill="#e2e8f0" font-size="7.2" font-weight="700">{code}</text>')

    # Forjado Sanitario + Lámina Anti-Radón (X=3.00..17.00)
    out.append(f'<rect x="{bx(3.00):.1f}" y="{bz(0.00):.1f}" width="{14.00*S_b:.1f}" height="{0.45*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#e2e8f0" stroke-width="1.2"/>')
    out.append(f'<line x1="{bx(2.85):.1f}" y1="{bz(-0.22):.1f}" x2="{bx(17.15):.1f}" y2="{bz(-0.22):.1f}" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="7,3"/>')

    # Muros Exteriores Oeste (X=3.00) y Este (X=17.00) de 2 plantas (Z=0.00..6.80m)
    out.append(f'<rect x="{bx(2.60):.1f}" y="{bz(6.80):.1f}" width="{0.40*S_b:.1f}" height="{6.80*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')
    out.append(f'<rect x="{bx(17.00):.1f}" y="{bz(6.80):.1f}" width="{0.40*S_b:.1f}" height="{6.80*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.3"/>')

    # Forjado Entrepiso Ala Oeste (X=3.00..8.00) y Ala Este (X=12.00..17.00) dejando vacío el Patio Central (X=8.00..12.00)
    out.append(f'<rect x="{bx(3.00):.1f}" y="{bz(3.15):.1f}" width="{5.00*S_b:.1f}" height="{0.35*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<rect x="{bx(12.00):.1f}" y="{bz(3.15):.1f}" width="{5.00*S_b:.1f}" height="{0.35*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')
    # Forjado Cubierta Superior P1 (Ala Oeste y Ala Este)
    out.append(f'<rect x="{bx(3.00):.1f}" y="{bz(6.45):.1f}" width="{5.00*S_b:.1f}" height="{0.45*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')
    out.append(f'<rect x="{bx(12.00):.1f}" y="{bz(6.45):.1f}" width="{5.00*S_b:.1f}" height="{0.45*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')

    # Cierres de vidrio hacia el Patio Central (X=8.00 y X=12.00 en PB y P1)
    out.append(f'<line x1="{bx(8.00):.1f}" y1="{bz(0.00):.1f}" x2="{bx(8.00):.1f}" y2="{bz(2.80):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<line x1="{bx(12.00):.1f}" y1="{bz(0.00):.1f}" x2="{bx(12.00):.1f}" y2="{bz(2.80):.1f}" stroke="#38bdf8" stroke-width="2.4"/>')
    out.append(f'<line x1="{bx(8.00):.1f}" y1="{bz(3.15):.1f}" x2="{bx(8.00):.1f}" y2="{bz(6.00):.1f}" stroke="#a855f7" stroke-width="2.4"/>')
    out.append(f'<rect x="{bx(12.00):.1f}" y="{bz(6.45):.1f}" width="{0.35*S_b:.1f}" height="{3.30*S_b:.1f}" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.2"/>')

    # Isla de Cocina Santos seccionada en X=12.90..13.90 (PB) + Escalera Volada en X=5.30..6.45
    out.append(f'<rect x="{bx(12.90):.1f}" y="{bz(0.92):.1f}" width="{1.00*S_b:.1f}" height="{0.92*S_b:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    for st_i in range(8):
        out.append(f'<rect x="{bx(5.30+st_i*0.28):.1f}" y="{bz(0.40+st_i*0.35):.1f}" width="{0.32*S_b:.1f}" height="4" fill="#fbbf24"/>')

    # Arce Japonés en el Patio Central (X=10.00)
    out.append(f'<line x1="{bx(10.00):.1f}" y1="{bz(0.00):.1f}" x2="{bx(10.00):.1f}" y2="{bz(3.50):.1f}" stroke="#10b981" stroke-width="2.0"/>')
    out.append(f'<circle cx="{bx(10.00):.1f}" cy="{bz(3.50):.1f}" r="{0.85*S_b:.1f}" fill="#064e3b" fill-opacity="0.45" stroke="#10b981" stroke-width="1.2"/>')

    b_labels = [
        (4.10, 1.35, "10. SALA TÉCNICA"),
        (6.60, 1.35, "09. ESCALERA"),
        (10.00, 1.35, "00. PATIO 4×4m"),
        (13.65, 1.35, "08. COCINA ISLA"),
        (16.10, 1.35, "07. LAVAND."),
        (5.50, 4.40, "13. BAÑO / GALERÍA P1"),
        (14.50, 4.40, "16. BAÑO Y VESTIDOR SUITE"),
    ]
    for xm, zm, txt in b_labels:
        out.append(f'<text x="{bx(xm):.1f}" y="{bz(zm):.1f}" text-anchor="middle" fill="#e2e8f0" font-size="5.6" font-weight="700">{txt}</text>')

    out.append(dim_h(bx(3.00), bx(8.00), bz(-0.55), 24, "5,00 m (Ala Oeste)"))
    out.append(dim_h(bx(8.00), bx(12.00), bz(-0.55), 24, "4,00 m (Patio)", "#10b981"))
    out.append(dim_h(bx(12.00), bx(17.00), bz(-0.55), 24, "5,00 m (Ala Este)"))
    out.append(dim_h(bx(3.00), bx(17.00), bz(-0.55), 46, "14,00 m (ANCHO TOTAL EJE A - EJE E)", "#f8fafc"))
    out.append('</g>')

    # ==========================================================================
    # 3. TRES DETALLES CONSTRUCTIVOS DE EJECUCIÓN A ESCALA 1:20 (ROW Y=568..1062)
    # ==========================================================================
    # DETALLE D-01 (x=28..598): BARRERA ANTI-RADÓN CTE DB-HS6, CÁVITI Y SUELO RADIANTE (1:20)
    out.append('<g transform="translate(28, 568)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="568" height="492" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="568" height="24" fill="#1e293b" stroke="#475569" stroke-width="1.0"/>')
    out.append('<text x="12" y="15.5" fill="#38bdf8" font-size="8.0" font-weight="700">DETALLE D-01 (ESCALA 1:20) · SOLERA VENTILADA CÁVITI Y PROTECCIÓN ANTI-RADÓN (CTE DB-HS6)</text>')

    # Graphic multilayer stratigraphic section D-01
    layers_d1 = [
        (45, 22, "url(#hatch-wood-deck)", "#fbbf24", "1. Pavimento terminado: Tarima Roble 14mm multicapa / Porcelánico 10mm (Z = ±0,00 m)"),
        (67, 36, "url(#hatch-radiant)", "#f43f5e", "2. Mortero autonivelante anhidrita 55 mm con tubería PEX-a Ø16 mm Suelo Radiante"),
        (103, 44, "url(#hatch-insulation)", "#38bdf8", "3. Placa aislamiento termoacústico EPS-T de tetones 60 mm (λ = 0,034 W/mK)"),
        (147, 10, "#ef4444", "#f8fafc", "4. BARRERA ANTI-RADÓN: Lámina continua Polietileno Reticulado 2,0 mm termosoldada"),
        (157, 45, "url(#hatch-ansi31)", "#cbd5e1", "5. Losa superior de hormigón armado HA-25/B/20/IIa (e = 100 mm) con mallazo Ø8 a 15 cm"),
        (202, 85, "#0f172a", "#64748b", "6. Cámara de aire ventilada con encofrado perdido tipo Cáviti C-25 (h = 250 mm)"),
        (287, 35, "url(#hatch-ansi31)", "#94a3b8", "7. Solera de limpieza y regularización HM-20 (e = 80 mm) sobre geotextil 200 g/m²"),
        (322, 65, "url(#hatch-gravel)", "#64748b", "8. Encachado de grava silícea lavada Ø20/40 mm (e = 150 mm) + Tubo drenaje perforado Ø110 mm"),
    ]
    for ly, lh, lfill, lcol, llbl in layers_d1:
        out.append(f'<rect x="20" y="{ly}" width="175" height="{lh}" fill="{lfill}" stroke="{lcol}" stroke-width="1.1"/>')
        out.append(f'<line x1="195" y1="{ly+lh/2:.1f}" x2="215" y2="{ly+lh/2:.1f}" stroke="{lcol}" stroke-width="0.9"/>')
        out.append(f'<circle cx="195" cy="{ly+lh/2:.1f}" r="2.2" fill="{lcol}"/>')
        out.append(f'<text x="222" y="{ly+lh/2+2.5:.1f}" fill="#e2e8f0" font-size="6.0">{llbl}</text>')

    # Cáviti arches graphic inside layer 6
    for cx_arch in [45, 95, 145]:
        out.append(f'<path d="M {cx_arch-18},287 Q {cx_arch},210 {cx_arch+18},287" fill="#070b14" stroke="#38bdf8" stroke-width="1.2"/>')
    # Radon extraction perforated pipe inside layer 6/8
    out.append('<circle cx="108" cy="355" r="14" fill="#090e1a" stroke="#ef4444" stroke-width="1.6" stroke-dasharray="4,2"/>')
    out.append('<text x="108" y="358" text-anchor="middle" fill="#ef4444" font-size="5.5" font-weight="700">Ø110</text>')

    out.append('<rect x="16" y="402" width="536" height="76" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="26" y="418" fill="#ef4444" font-size="6.5" font-weight="700">PRESCRIPCIÓN OBLIGATORIA CTE DB-HS6 (MUNICIPIO ZONA II RADÓN — OLEIROS):</text>')
    out.append('<text x="26" y="432" fill="#cbd5e1" font-size="5.8">• Sellado estanco de todos los pasatubos y acometidas en Sala Técnica con manguitos elásticos EPDM y masilla de poliuretano.</text>')
    out.append('<text x="26" y="445" fill="#cbd5e1" font-size="5.8">• Despresurización del espacio de contención (cámara Cáviti) mediante conducto colector PVC Ø110 mm hasta cubierta con extractor.</text>')
    out.append('<text x="26" y="458" fill="#10b981" font-size="5.8" font-weight="700">• Transmitancia térmica global de suelo en contacto con cámara ventilada: U = 0,21 W/m²K (Cumple holgadamente CTE DB-HE1).</text>')
    out.append('</g>')

    # DETALLE D-02 (x=610..1186): ENRASADO COTA CERO (±0,00 m) CARPINTERÍA CORTIZO SOBRE PURENIT + PATIO/PORCHE (1:20)
    out.append('<g transform="translate(610, 568)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="576" height="492" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="576" height="24" fill="#1e293b" stroke="#475569" stroke-width="1.0"/>')
    out.append('<text x="12" y="15.5" fill="#38bdf8" font-size="8.0" font-weight="700">DETALLE D-02 (ESCALA 1:20) · UMBRAL ENRASADO COTA ±0,00 m SOBRE PURENIT Y CANALETA AISI 316</text>')

    # Graphic CAD cross-section of zero-threshold sliding door (Interior Left -> Cortizo Track -> Slot Drain -> Exterior Deck Right)
    # Z=0.00 line at y=160
    out.append('<line x1="20" y1="160" x2="550" y2="160" stroke="#10b981" stroke-width="1.0" stroke-dasharray="6,3"/>')
    out.append('<text x="548" y="153" text-anchor="end" fill="#10b981" font-size="6.2" font-weight="700">NIVEL ENRASADO CONTINUO Z = ±0,00 m (SIN RESALTE)</text>')

    # Left: Interior Floor (Roble 14mm + Mortero SR 55mm + EPS 60mm)
    out.append('<rect x="25" y="160" width="165" height="16" fill="url(#hatch-wood-deck)" stroke="#fbbf24" stroke-width="1.1"/>')
    out.append('<rect x="25" y="176" width="165" height="44" fill="url(#hatch-radiant)" stroke="#f43f5e" stroke-width="1.0"/>')
    out.append('<rect x="25" y="220" width="165" height="50" fill="url(#hatch-insulation)" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append('<text x="105" y="150" text-anchor="middle" fill="#f8fafc" font-size="6.2" font-weight="700">INTERIOR VIVIENDA (±0,00 m)</text>')

    # Center: Triple Glass Leaf + Bottom Embedded Frame + Purenit 50mm Structural Thermal Break Block
    out.append('<rect x="198" y="55" width="26" height="105" fill="#082f49" stroke="#38bdf8" stroke-width="1.6"/>')
    out.append('<line x1="206" y1="55" x2="206" y2="160" stroke="#e0f2fe" stroke-width="1.2"/>')
    out.append('<line x1="216" y1="55" x2="216" y2="160" stroke="#e0f2fe" stroke-width="1.2"/>')
    # Bottom recessed aluminum rail (h=50mm) flush at y=160
    out.append('<rect x="190" y="160" width="44" height="35" fill="#1e293b" stroke="#f8fafc" stroke-width="1.4"/>')
    # Purenit 50mm high-density polyurethane thermal block under the rail (y=195..270)
    out.append('<rect x="190" y="195" width="44" height="75" fill="url(#hatch-insulation)" stroke="#f59e0b" stroke-width="1.5"/>')
    out.append('<text x="212" y="235" text-anchor="middle" fill="#fbbf24" font-size="5.8" font-weight="700">PURENIT</text>')

    # Right of Frame: AISI 316 Stainless Steel Slot Drain Channel (x=236..276, y=160..235) connected to Ø50/Ø110 drain
    out.append('<rect x="236" y="160" width="40" height="65" fill="#090e1a" stroke="#38bdf8" stroke-width="1.5"/>')
    out.append('<line x1="236" y1="162" x2="276" y2="162" stroke="#e0f2fe" stroke-width="2.2" stroke-dasharray="4,3"/>')
    out.append('<path d="M 252,225 V 310 H 380" fill="none" stroke="#38bdf8" stroke-width="3.0"/>')

    # Exterior Right: Floating Iroko Deck / C3 Porcelain on Adjustable Plots (x=280..535, y=160..178) over Dropped Slab (-15 cm)
    out.append('<rect x="280" y="160" width="255" height="18" fill="url(#hatch-wood-deck)" stroke="#10b981" stroke-width="1.3"/>')
    for plot_x in [310, 405, 500]:
        out.append(f'<rect x="{plot_x-10}" y="178" width="20" height="82" fill="#334155" stroke="#cbd5e1" stroke-width="1.0"/>')
        out.append(f'<rect x="{plot_x-18}" y="252" width="36" height="8" fill="#64748b"/>')
    # EPDM Waterproofing Membrane + Sloped Mortar (2%) on Dropped Slab (y=260..325)
    out.append('<polyline points="190,270 190,195 234,195 234,262 535,268" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-dasharray="5,2"/>')
    out.append('<rect x="25" y="270" width="510" height="55" fill="url(#hatch-ansi31)" stroke="#cbd5e1" stroke-width="1.2"/>')
    out.append('<text x="410" y="150" text-anchor="middle" fill="#10b981" font-size="6.2" font-weight="700">PATIO CORRALA / PORCHE SUR (±0,00 m)</text>')

    # Callout Annotations D-02
    d2_notes = [
        "1. Hoja corredera Cortizo Cor Vision Plus RPT con triple vidrio bajo emisivo + Argón (Uw = 0,85 W/m²K).",
        "2. Guía inferior de aluminio embutida a ras de pavimento interior y exterior (accesibilidad total silla de ruedas).",
        "3. Submarco térmico de poliuretano de alta densidad PURENIT (50 mm · λ=0,08 W/mK · imputrescible) eliminando puente térmico.",
        "4. Canaleta lineal oculta de acero inoxidable marino AISI 316L adosada al marco exterior con evacuación directa a red pluvial.",
        "5. Pavimento exterior de Iroko / Porcelánico C3 sobre plots regulables (cámara drenante h=10-12 cm sobre lámina EPDM).",
    ]
    for idx, note in enumerate(d2_notes):
        out.append(f'<text x="20" y="{352+idx*16}" fill="#cbd5e1" font-size="5.8">{note}</text>')

    out.append('<rect x="16" y="432" width="544" height="46" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="26" y="449" fill="#38bdf8" font-size="6.3" font-weight="700">GARANTÍA DE ESTANQUEIDAD FRENTE A TEMPORALES ATLÁNTICOS SW (CTE DB-HS1 GRADO 5):</text>')
    out.append('<text x="26" y="464" fill="#cbd5e1" font-size="5.8">Doble barrera de drenaje (canaleta superficial AISI 316 + cámara bajo plots con pendiente 2% y sumidero sifónico Ø110 mm).</text>')
    out.append('</g>')

    # DETALLE D-03 (x=1198..1772): FACHADA SATE / GRANITO Y ENCUENTRO CUBIERTA PLANA INVERTIDA (1:20)
    out.append('<g transform="translate(1198, 568)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="574" height="492" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="574" height="24" fill="#1e293b" stroke="#475569" stroke-width="1.0"/>')
    out.append('<text x="12" y="15.5" fill="#38bdf8" font-size="8.0" font-weight="700">DETALLE D-03 (ESCALA 1:20) · ENCUENTRO FACHADA SATE CON CUBIERTA PLANA INVERTIDA PASSIVHAUS</text>')

    # Graphic CAD section of Parapet + SATE Facade + Inverted Flat Roof with Gravel
    # Exterior SATE Insulation (x=45..90, y=55..320) wrapping over the parapet (zero thermal bridge)
    out.append('<rect x="45" y="55" width="45" height="265" fill="url(#hatch-insulation)" stroke="#38bdf8" stroke-width="1.3"/>')
    # Ceramic/Concrete structural wall + parapet (x=90..150, y=75..320) + Roof Slab (x=90..380, y=215..275)
    out.append('<path d="M 90,75 H 145 V 215 H 380 V 275 H 145 V 320 H 90 Z" fill="url(#hatch-ansi31)" stroke="#f8fafc" stroke-width="1.4"/>')
    # Interior parapet insulation + XPS Roof Insulation 200mm (x=145..380, y=145..205)
    out.append('<rect x="145" y="75" width="25" height="140" fill="url(#hatch-insulation)" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append('<rect x="170" y="145" width="210" height="58" fill="url(#hatch-insulation)" stroke="#38bdf8" stroke-width="1.3"/>')
    # Washed gravel ballast 50mm (x=170..380, y=118..145)
    out.append('<rect x="170" y="118" width="210" height="27" fill="url(#hatch-gravel)" stroke="#94a3b8" stroke-width="1.0"/>')
    # EPDM Continuity Line (Red dashed)
    out.append('<polyline points="90,72 170,72 170,208 380,213" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-dasharray="6,2"/>')
    # Lacquered Aluminum Coping Cap with Drip Edge (Albahaquero con goterón)
    out.append('<path d="M 38,65 V 50 H 180 V 65" fill="none" stroke="#fbbf24" stroke-width="2.5"/>')

    d3_callouts = [
        (60,  "1. Albardilla de aluminio lacado e=2 mm con doble goterón y pendiente hacia el interior de cubierta"),
        (100, "2. Envolvente continua SATE EPS Grafito 160 mm (λ=0,031 W/mK) envolviendo el peto (sin puente térmico)"),
        (132, "3. Lastre de canto rodado lavado Ø16/32 mm (e = 60 mm) sobre geotextil antipunzonamiento 300 g/m²"),
        (175, "4. Doble capa de aislamiento Poliestireno Extruido XPS 100+100 mm = 200 mm (U cubierta = 0,14 W/m²K)"),
        (210, "5. Impermeabilización bicapa EPDM 1,5 mm sobre hormigón celular de formación de pendientes (min. 2%)"),
        (248, "6. Forjado reticular / losa maciza HA-25 (h = 250+50 mm) + barrera de vapor bituminosa"),
        (295, "7. Trasdosado interior autoportante PYL 12,5+12,5 mm con lana mineral 48 mm y cámara de instalaciones"),
    ]
    for cy_c, c_txt in d3_callouts:
        out.append(f'<text x="20" y="{cy_c+255 if cy_c>200 else 330 + d3_callouts.index((cy_c, c_txt))*17}" fill="#cbd5e1" font-size="5.8">{c_txt}</text>')

    out.append('<rect x="16" y="452" width="542" height="28" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="26" y="469" fill="#10b981" font-size="6.2" font-weight="700">CONTINUIDAD DE LA ENVOLVENTE TÉRMICA (Ψ ≤ 0,01 W/mK · ESTÁNDAR PASSIVHAUS EN CLIMA ATLÁNTICO C1)</text>')
    out.append('</g>')

    # ISO 7200 Title Block
    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-05",
        title="SECCIONES CONSTRUCTIVAS A-A' Y B-B' (1:50) Y DETALLES DE EJECUCIÓN (1:20)",
        scale="1:50 / 1:20 (Cotas m/mm)",
        phase="PROYECTO DE EJECUCIÓN",
        subtitle="Altimetría Z, Soleamiento Estacional, Detalle Anti-Radón DB-HS6, Umbral Cota Cero Purenit y Cubierta",
        extra_notes=[
            "Sección Longitudinal A-A' (Norte-Sur): Porche Norte -> Hall -> Patio Central -> Salón-Comedor -> Porche Sur -> Piscina",
            "Sección Transversal B-B' (Oeste-Este): Sala Técnica -> Escalera -> Patio Central -> Cocina Isla Santos -> Lavandería",
            "Altura Máxima de Coronación: Z = +6,80 m ≤ 7,00 m (Cumple PGOM Oleiros Ordenanza 2B · Bajo Rasante 0,00 m²)",
            "Detalles Constructivos 1:20: D-01 Cáviti + Radón DB-HS6 · D-02 Umbral Cota Cero Purenit · D-03 Cubierta Invertida",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


def main():
    files = [
        ("plano_constructivo_planta_primera_p1.svg", build_planta_primera_1_50_svg()),
        ("plano_secciones_y_detalle_constructivo.svg", build_secciones_y_detalles_svg()),
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
