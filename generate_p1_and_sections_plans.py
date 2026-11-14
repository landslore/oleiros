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
    S = 58.0  # Escala técnica de alta precisión para crujía X=4.00..17.00m, Y=5.00..19.40m
    OX = 165.0
    OY = 145.0

    def px(xm: float) -> float:
        return OX + (xm - 4.00) * S

    def py(ym: float) -> float:
        return OY + (ym - 5.00) * S

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1180" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.2" font-weight="700">PLANO E-04 · EJECUCIÓN E INSTALACIONES PLANTA PRIMERA (+3,15 m) — ZONA NOCHE + SALA POLIVALENTE (1:50)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.1">Escala 100% Real verificada · Sala Polivalente Cine/Gaming (14,00 m² · Rw≥50dB) · Baño Hijos (6,80 m²) · 2 Dorms (14,60 m²) · Master Suite (31,20 m²)</text>',
        f'<rect x="28" y="68" width="1180" height="995" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>',
    ]

    # Ejes Estructurales 100% alineados con Planta Baja
    x_axes = [("A", 4.00), ("B", 6.15), ("C", 8.50), ("D", 12.50), ("E", 17.00)]
    y_axes = [("1", 5.00), ("2", 8.40), ("3", 12.40), ("4", 18.00), ("4B", 19.40)]
    out.append(draw_grid_axes(x_axes, y_axes, px(3.60), px(17.50), py(4.65), py(20.00), px, py))

    # Cubierta Técnica Oeste No Transitable (X=4.00..6.15, Y=5.00..18.00) con Grava + Campo Solar FV 5,5 kWp
    out.append(f'<rect x="{px(4.00):.1f}" y="{py(5.00):.1f}" width="{2.15*S:.1f}" height="{13.00*S:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="1.1" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{px(5.07):.1f}" y="{py(6.10):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="6.0" font-weight="700">CUBIERTA GRAVA</text>')
    out.append(f'<text x="{px(5.07):.1f}" y="{py(6.35):.1f}" text-anchor="middle" fill="#64748b" font-family="monospace" font-size="5.5">(SOBRE MUDROOM PB)</text>')
    for r in range(6):
        ry_pv = 7.20 + r * 1.65
        out.append(f'<rect x="{px(4.25):.1f}" y="{py(ry_pv):.1f}" width="{1.65*S:.1f}" height="{1.25*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{px(5.07):.1f}" y="{py(17.45):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.8" font-weight="700">12 PANELES FV 5,5kWp</text>')

    # ==========================================================================
    # SUPERFICIES REALES A ESCALA PLANTA PRIMERA (+3,15 m · Interior X=6.50..16.65, Y=5.35..17.65)
    # ==========================================================================
    # Vacío del Patio Central Corrala (X=8.50..12.50, Y=8.40..12.40 -> 4,00 x 4,00 m)
    # Nota: el alero norte de 0,80 m (Y=8.40..9.15) soporta la pasarela de acceso a la Sala Polivalente
    out.append(f'<rect x="{px(8.50):.1f}" y="{py(8.40):.1f}" width="{4.00*S:.1f}" height="{4.00*S:.1f}" fill="#070b14" stroke="#10b981" stroke-width="1.6"/>')
    out.append(f'<line x1="{px(8.50):.1f}" y1="{py(9.15):.1f}" x2="{px(12.50):.1f}" y2="{py(12.40):.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4"/>')
    out.append(f'<line x1="{px(12.50):.1f}" y1="{py(9.15):.1f}" x2="{px(8.50):.1f}" y2="{py(12.40):.1f}" stroke="#10b981" stroke-width="0.8" stroke-dasharray="6,4"/>')
    out.append(f'<circle cx="{px(10.50):.1f}" cy="{py(10.75):.1f}" r="{0.58*S:.1f}" fill="none" stroke="#10b981" stroke-width="1.1" stroke-dasharray="4,3"/>')
    out.append(f'<text x="{px(10.50):.1f}" y="{py(10.60):.1f}" text-anchor="middle" fill="#10b981" font-family="monospace" font-size="6.5" font-weight="700">VACÍO PATIO CORRALA</text>')
    out.append(f'<text x="{px(10.50):.1f}" y="{py(10.90):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="5.5">(4,00×4,00m · COPA ARCE)</text>')

    # 15. Baño Compartido Hijos (Noroeste P1: X=6.50..8.82 [2,32m] × Y=5.35..8.28 [2,93m] = 6,80 m² EXACTOS)
    out.append(f'<rect x="{px(6.50):.1f}" y="{py(5.35):.1f}" width="{2.32*S:.1f}" height="{2.93*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # 15B. Sala Polivalente / Cine, TV & Gaming / 4º Dormitorio (Centro-Norte P1: X=8.94..13.72 [4,78m] × Y=5.35..8.28 [2,93m] = 14,00 m² EXACTOS)
    out.append(f'<rect x="{px(8.94):.1f}" y="{py(5.35):.1f}" width="{4.78*S:.1f}" height="{2.93*S:.1f}" fill="#172036" stroke="none"/>')

    # 18. Baño Privado Master Suite (Noreste P1: X=13.84..16.65 [2,81m] × Y=5.35..7.60 [2,25m] = 6,30 m² EXACTOS)
    out.append(f'<rect x="{px(13.84):.1f}" y="{py(5.35):.1f}" width="{2.81*S:.1f}" height="{2.25*S:.1f}" fill="url(#hatch-tile-60)" stroke="none"/>')

    # 17. Vestidor Doble Pasante Suite (Este P1: X=12.75..16.65 × Y=7.72..12.12 -> 8,40 m² útiles libres)
    out.append(f'<rect x="{px(12.75):.1f}" y="{py(7.72):.1f}" width="{3.90*S:.1f}" height="{4.40*S:.1f}" fill="#131c31" stroke="none"/>')

    # 12. Desembarco Escalera y Galería Acústica (8,20 m² útiles):
    # Tramo Oeste escalera (X=6.50..8.50, Y=8.28..12.40) + Pasarela Norte a Sala Polivalente (X=8.50..10.15, Y=8.28..9.15) + Galería Sur (X=6.50..13.48, Y=12.40..13.26)
    out.append(f'<rect x="{px(6.50):.1f}" y="{py(8.28):.1f}" width="{2.00*S:.1f}" height="{4.12*S:.1f}" fill="#131c31" stroke="none"/>')
    out.append(f'<rect x="{px(8.50):.1f}" y="{py(8.28):.1f}" width="{1.65*S:.1f}" height="{0.87*S:.1f}" fill="#131c31" stroke="none"/>')
    out.append(f'<rect x="{px(6.50):.1f}" y="{py(12.40):.1f}" width="{6.98*S:.1f}" height="{0.86*S:.1f}" fill="#131c31" stroke="none"/>')

    # 13. Dormitorio Infantil Niña (Suroeste P1: X=6.50..9.92 [3,42m] × Y=13.38..17.65 [4,27m] = 14,60 m² EXACTOS)
    out.append(f'<rect x="{px(6.50):.1f}" y="{py(13.38):.1f}" width="{3.42*S:.1f}" height="{4.27*S:.1f}" fill="#131c31" stroke="none"/>')

    # 14. Dormitorio Infantil Niño (Centro-Sur P1: X=10.06..13.48 [3,42m] × Y=13.38..17.65 [4,27m] = 14,60 m² EXACTOS)
    out.append(f'<rect x="{px(10.06):.1f}" y="{py(13.38):.1f}" width="{3.42*S:.1f}" height="{4.27*S:.1f}" fill="#131c31" stroke="none"/>')

    # 16. Dormitorio Principal Master Suite (Sureste P1: X=13.60..16.65 [3,05m] × Y=12.24..17.65 [5,41m] = 16,50 m² EXACTOS)
    out.append(f'<rect x="{px(13.60):.1f}" y="{py(12.24):.1f}" width="{3.05*S:.1f}" height="{5.41*S:.1f}" fill="#131c31" stroke="none"/>')

    # 19. Balcón-Terraza Sur Continuo (X=6.15..17.00 [10,85m] × Y=18.00..19.40 [1,40m] · 14,00 m² útiles)
    out.append(f'<rect x="{px(6.15):.1f}" y="{py(18.00):.1f}" width="{10.85*S:.1f}" height="{1.40*S:.1f}" fill="url(#hatch-tile-60)" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{px(6.15):.1f}" y1="{py(19.36):.1f}" x2="{px(17.00):.1f}" y2="{py(19.36):.1f}" stroke="#e0f2fe" stroke-width="2.0"/>')
    out.append(f'<text x="{px(11.57):.1f}" y="{py(19.58):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="6.0" font-weight="700">BARANDILLA VIDRIO LAMINAR TEMPLADO 10+10.2 mm EN U OCULTA EN FORJADO (h=1,10 m · CTE DB-SUA 1)</text>')

    # ==========================================================================
    # MUROS DE FACHADA Y TABIQUERÍA ACÚSTICA P1 (1:50)
    # ==========================================================================
    tw_ext = 0.35 * S
    tw_int = 0.12 * S
    # Perímetro exterior SATE + Termoarcilla P1 (X=6.15..17.00, Y=5.00..18.00)
    out.append(draw_wall(px(6.15), py(5.18), px(17.00), py(5.18), tw_ext, True))
    out.append(draw_wall(px(6.15), py(17.82), px(17.00), py(17.82), tw_ext, True))
    out.append(draw_wall(px(6.32), py(5.00), px(6.32), py(18.00), tw_ext, True))
    out.append(draw_wall(px(16.82), py(5.00), px(16.82), py(18.00), tw_ext, True))

    # Muro Este del Patio Central (X=12.62, Y=8.28..12.40) y cierre Norte del Patio bajo Sala Polivalente
    out.append(draw_wall(px(12.62), py(8.28), px(12.62), py(12.40), 0.24 * S, True))
    out.append(draw_wall(px(10.15), py(8.34), px(12.62), py(8.34), tw_int * 1.2, False))

    # C-15A y C-15B: Cerramiento Acústico de Vidrio Laminado 4+4 Silence (Rw = 42 dB) en Galería del Patio
    out.append(sliding_door(px(8.50), py(9.15), 3.25*S, tw_ext*0.55, "v", 2, "C-15A GALERÍA ACÚSTICA 4+4 SILENCE"))
    out.append(sliding_door(px(8.50), py(12.40), 4.00*S, tw_ext*0.55, "h", 2, "C-15B GALERÍA ACÚSTICA 4+4 SILENCE"))
    # C-15C: Mirador interior fijo acústico 4+4 Silence + estor blackout en Sala Polivalente hacia copa del arce
    out.append(window_cad(px(10.25), py(8.34), 2.10*S, tw_int*1.3, "h", "C-15C MIRADOR ACÚSTICO 4+4 + BLACKOUT"))

    # Tabiques Banda Norte (Baño Hijos | Sala Polivalente Cine/Gaming | Baño Suite) con aislamiento Rw ≥ 50 dB
    out.append(draw_wall(px(8.88), py(5.35), px(8.88), py(8.28), tw_int * 1.25, False))
    out.append(f'<line x1="{px(8.88):.1f}" y1="{py(5.35):.1f}" x2="{px(8.88):.1f}" y2="{py(8.28):.1f}" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4,2"/>')
    out.append(draw_wall(px(13.78), py(5.35), px(13.78), py(8.28), tw_int * 1.25, False))
    out.append(f'<line x1="{px(13.78):.1f}" y1="{py(5.35):.1f}" x2="{px(13.78):.1f}" y2="{py(8.28):.1f}" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4,2"/>')
    out.append(draw_wall(px(6.50), py(8.28), px(10.15), py(8.28), tw_int * 1.25, False))
    out.append(f'<line x1="{px(8.88):.1f}" y1="{py(8.28):.1f}" x2="{px(10.15):.1f}" y2="{py(8.28):.1f}" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4,2"/>')
    out.append(draw_wall(px(13.78), py(7.66), px(16.65), py(7.66), tw_int, False))

    # Tabiques Banda Sur (Galería | Dormitorio Niña | Dormitorio Niño | Master Suite)
    out.append(draw_wall(px(6.50), py(13.32), px(13.54), py(13.32), tw_int, False))
    # Medianera Acústica Ciega entre Dormitorio 1 y Dormitorio 2 (X=9.99, Y=13.32..17.65 · Doble placa + Lana 70kg/m³ Rw ≥ 50 dB)
    out.append(draw_wall(px(9.99), py(13.32), px(9.99), py(17.65), tw_int*1.25, False))
    out.append(f'<line x1="{px(9.99):.1f}" y1="{py(13.32):.1f}" x2="{px(9.99):.1f}" y2="{py(17.65):.1f}" stroke="#f59e0b" stroke-width="1.3" stroke-dasharray="4,2"/>')
    # Medianera Acústica entre Dormitorio 2 y Master Suite (X=13.54, Y=12.18..17.65)
    out.append(draw_wall(px(13.54), py(12.18), px(13.54), py(17.65), tw_int*1.25, False))
    out.append(f'<line x1="{px(13.54):.1f}" y1="{py(12.18):.1f}" x2="{px(13.54):.1f}" y2="{py(17.65):.1f}" stroke="#f59e0b" stroke-width="1.3" stroke-dasharray="4,2"/>')
    # Separación Vestidor Suite / Dormitorio Suite (Y=12.18, X=12.62..16.65)
    out.append(draw_wall(px(12.62), py(12.18), px(16.65), py(12.18), tw_int, False))

    # ==========================================================================
    # CARPINTERÍAS INTERIORES Y EXTERIORES P1
    # ==========================================================================
    # Puertas interiores acústicas con burlete perimetral y guillotina inferior
    out.append(door_swing(px(7.55), py(8.28), 0.80*S, "up", "left", "P-11 0,80"))             # Baño Hijos
    out.append(door_swing(px(9.12), py(8.28), 0.82*S, "up", "right", "P-11B ACÚST. 38dB"))    # Sala Polivalente Cine/Gaming
    out.append(door_swing(px(12.62), py(12.42), 0.82*S, "right", "down", "P-14 SUITE"))       # Acceso Suite desde Galería
    out.append(sliding_door(px(14.50), py(7.66), 0.80*S, tw_int, "h", 1, "P-16 BAÑO"))        # Vestidor -> Baño Suite
    out.append(sliding_door(px(14.55), py(12.18), 0.90*S, tw_int, "h", 1, "P-15 DORM."))      # Vestidor -> Dormitorio Suite
    out.append(door_swing(px(7.65), py(13.32), 0.82*S, "down", "left", "P-12 NIÑA"))          # Dorm 1 Niña
    out.append(door_swing(px(10.25), py(13.32), 0.82*S, "down", "right", "P-13 NIÑO"))        # Dorm 2 Niño

    # Ventanas Norte y Este + Balconeras Sur
    out.append(window_cad(px(7.15), py(5.18), 1.00*S, tw_ext, "h", "C-10 1,00×0,60"))         # Baño Hijos
    out.append(window_cad(px(10.45), py(5.18), 1.80*S, tw_ext, "h", "C-10B 1,80×1,20"))       # Sala Polivalente
    out.append(window_cad(px(14.65), py(5.18), 1.20*S, tw_ext, "h", "C-11 1,20×0,60"))        # Baño Suite
    out.append(window_cad(px(16.82), py(9.40), 1.00*S, tw_ext, "v", "C-14B 1,00×1,20"))       # Vestidor Este
    out.append(sliding_door(px(7.10), py(17.82), 2.20*S, tw_ext*0.85, "h", 2, "C-12 BALCONERA D1 (2,20×2,40)"))
    out.append(sliding_door(px(10.65), py(17.82), 2.20*S, tw_ext*0.85, "h", 2, "C-13 BALCONERA D2 (2,20×2,40)"))
    out.append(sliding_door(px(13.80), py(17.82), 2.70*S, tw_ext*0.85, "h", 2, "C-14 BALCONERA SUITE (2,70×2,40)"))

    # ==========================================================================
    # MOBILIARIO TÉCNICO Y SANITARIOS P1 A ESCALA REAL (1:50)
    # ==========================================================================
    # Escalera de llegada a P1 (X=6.50..7.50, Y=8.55..12.15)
    st_x, st_y, st_w, st_h = px(6.50), py(8.55), 1.00*S, 3.60*S
    out.append(f'<rect x="{st_x:.1f}" y="{st_y:.1f}" width="{st_w:.1f}" height="{st_h:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    for i in range(1, 17):
        sy = st_y + i * (st_h / 17)
        out.append(f'<line x1="{st_x:.1f}" y1="{sy:.1f}" x2="{st_x+st_w:.1f}" y2="{sy:.1f}" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<text x="{px(8.00):.1f}" y="{py(10.45):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.5" font-weight="700" transform="rotate(-90 {px(8.00):.1f} {py(10.45):.1f})">PASARELA +3,15m</text>')

    # 15. Baño Compartido Hijos (2,32 x 2,93 m = 6,80 m²):
    out.append(shower_cad(px(6.55), py(5.42), 2.20*S, 0.85*S))                                # Bañera/Ducha Norte
    out.append(sink_cad(px(6.55), py(6.42), 0.52*S, 1.40*S, True))                            # Doble seno 1,40 m Oeste
    out.append(wc_cad(px(8.22), py(6.55), 0.55*S, 0.42*S, "left"))                            # Inodoro suspendido Este

    # 15B. Sala Polivalente / Cine, TV & Gaming / 4º Dormitorio (4,78 x 2,93 m = 14,00 m²):
    # Sofá-Cama Chaiselongue en L (2,55 x 1,65 m) en esquina Noroeste mirando al Este
    out.append(f'<rect x="{px(9.10):.1f}" y="{py(5.50):.1f}" width="{2.45*S:.1f}" height="{0.92*S:.1f}" rx="3" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    out.append(f'<rect x="{px(9.10):.1f}" y="{py(6.42):.1f}" width="{0.95*S:.1f}" height="{0.75*S:.1f}" rx="3" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.1"/>')
    out.append(f'<text x="{px(10.32):.1f}" y="{py(6.00):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" font-weight="700">SOFÁ-CAMA CHAISELONGUE (INVITADOS)</text>')
    # Mesa central / puff + Alfombra acústica
    out.append(f'<rect x="{px(10.30):.1f}" y="{py(6.55):.1f}" width="{1.10*S:.1f}" height="{0.60*S:.1f}" rx="2" fill="#0f172a" stroke="#64748b" stroke-width="0.8" stroke-dasharray="3,2"/>')
    # Mueble TV OLED 65" + Barra Dolby Atmos sobre panel fonoabsorbente en pared Este (X=13.42..13.68, Y=5.55..7.45)
    out.append(f'<rect x="{px(13.42):.1f}" y="{py(5.55):.1f}" width="{0.26*S:.1f}" height="{1.90*S:.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="1.1"/>')
    out.append(f'<text x="{px(13.55):.1f}" y="{py(6.50):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="5.0" font-weight="700" transform="rotate(-90 {px(13.55):.1f} {py(6.50):.1f})">TV 65" OLED + ATMOS</text>')
    # Estación Doble Gaming / Estudio con luz Norte (X=11.65..13.30, Y=5.45..6.05 -> 1,65 x 0,60 m)
    out.append(f'<rect x="{px(11.65):.1f}" y="{py(5.45):.1f}" width="{1.65*S:.1f}" height="{0.60*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<circle cx="{px(12.10):.1f}" cy="{py(6.25):.1f}" r="{0.20*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<circle cx="{px(12.85):.1f}" cy="{py(6.25):.1f}" r="{0.20*S:.1f}" fill="#0f172a" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<text x="{px(12.47):.1f}" y="{py(5.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.8" font-weight="700">SETUP GAMING / ESTUDIO</text>')

    # 18. Baño Privado Master Suite (2,81 x 2,25 m = 6,30 m²):
    out.append(shower_cad(px(15.68), py(5.40), 0.92*S, 2.15*S))                               # Ducha Walk-in doble Este
    out.append(sink_cad(px(13.95), py(5.40), 1.45*S, 0.52*S, True))                           # Doble seno 1,45 m Norte
    out.append(wc_cad(px(13.92), py(6.95), 0.55*S, 0.42*S, "right"))                          # Inodoro suspendido

    # 17. Vestidor Doble Pasante Suite (8,40 m² útiles libres):
    out.append(wardrobe_cad(px(12.78), py(7.80), 0.60*S, 3.60*S, "v", "ARMARIOS LADO OESTE (3,60m)"))
    out.append(wardrobe_cad(px(16.02), py(7.80), 0.60*S, 4.15*S, "v", "ARMARIOS LADO ESTE (4,15m)"))
    out.append(f'<rect x="{px(14.35):.1f}" y="{py(9.10):.1f}" width="{0.70*S:.1f}" height="{1.40*S:.1f}" rx="2" fill="#1e293b" stroke="#fbbf24" stroke-width="0.9"/>')
    out.append(f'<text x="{px(14.70):.1f}" y="{py(9.80):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.8" transform="rotate(-90 {px(14.70):.1f} {py(9.80):.1f})">ISLA JOYERO</text>')

    # 13. Dormitorio Infantil Niña (3,42 x 4,27 m = 14,60 m²):
    out.append(wardrobe_cad(px(8.55), py(13.42), 1.30*S, 0.60*S, "h", "ARMARIO 1,30m"))
    out.append(bed_cad(px(6.58), py(14.55), 2.00*S, 1.35*S, "W", False, "CAMA 135×200"))
    out.append(f'<rect x="{px(9.20):.1f}" y="{py(15.20):.1f}" width="{0.65*S:.1f}" height="{1.80*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<circle cx="{px(8.90):.1f}" cy="{py(16.10):.1f}" r="{0.22*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(9.52):.1f}" y="{py(16.10):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" transform="rotate(-90 {px(9.52):.1f} {py(16.10):.1f})">ESTUDIO (LUZ 90°)</text>')

    # 14. Dormitorio Infantil Niño (3,42 x 4,27 m = 14,60 m²):
    out.append(wardrobe_cad(px(11.20), py(13.42), 2.20*S, 0.60*S, "h", "ARMARIO 2,20×0,60m"))
    out.append(bed_cad(px(10.12), py(14.55), 2.00*S, 1.35*S, "W", False, "CAMA 135×200"))
    out.append(f'<rect x="{px(12.76):.1f}" y="{py(15.20):.1f}" width="{0.65*S:.1f}" height="{1.80*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<circle cx="{px(12.46):.1f}" cy="{py(16.10):.1f}" r="{0.22*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{px(13.08):.1f}" y="{py(16.10):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.0" transform="rotate(-90 {px(13.08):.1f} {py(16.10):.1f})">ESTUDIO (LUZ 90°)</text>')

    # 16. Dormitorio Principal Master Suite (3,05 x 5,41 m = 16,50 m²):
    out.append(bed_cad(px(14.60), py(13.85), 2.00*S, 1.80*S, "E", True, "KING SIZE 180×200"))
    out.append(f'<rect x="{px(16.12):.1f}" y="{py(13.30):.1f}" width="{0.45*S:.1f}" height="{0.48*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{px(16.12):.1f}" y="{py(15.72):.1f}" width="{0.45*S:.1f}" height="{0.48*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{px(14.12):.1f}" y="{py(14.10):.1f}" width="{0.42*S:.1f}" height="{1.30*S:.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')

    # Círculos NHG Ø1.50m de Verificación Normativa
    out.append(nhg_circle(px(11.35), py(7.35), S, "Ø1,50m SALA"))
    out.append(nhg_circle(px(7.85), py(16.70), S, "Ø1,50m D1"))
    out.append(nhg_circle(px(11.45), py(16.70), S, "Ø1,50m D2"))
    out.append(nhg_circle(px(15.10), py(16.75), S, "Ø1,50m SUITE"))

    # Pilares Estructurales HEB/HA-30 P1 alineados con PB
    pillars = [(x, y) for x in [6.15, 8.50, 12.50, 17.00] for y in [5.00, 8.40, 12.40, 18.00]]
    out.append(draw_pillars(pillars, px, py, 0.30, S))

    # ==========================================================================
    # MEP INSTALLATIONS OVERLAY P1 (1:50)
    # ==========================================================================
    out.append('<g opacity="0.92">')
    # Impulsión aire limpio VMC (Azul cian Ø90mm) a Sala Polivalente (+35 m³/h), Dorm 1 (+30 m³/h), Dorm 2 (+30 m³/h) y Suite (+45 m³/h)
    out.append(f'<polyline points="{px(7.85):.1f},{py(12.80):.1f} {px(9.50):.1f},{py(8.70):.1f} {px(11.30):.1f},{py(6.80):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="6,3"/>')
    out.append(f'<polyline points="{px(7.85):.1f},{py(12.80):.1f} {px(7.85):.1f},{py(14.10):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="6,3"/>')
    out.append(f'<polyline points="{px(7.85):.1f},{py(12.80):.1f} {px(11.60):.1f},{py(12.80):.1f} {px(15.10):.1f},{py(13.10):.1f}" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="6,3"/>')
    out.append(mep_symbol(px(11.30), py(6.80), "vmc_imp", "+35 m³/h"))
    out.append(mep_symbol(px(7.85), py(14.10), "vmc_imp", "+30 m³/h"))
    out.append(mep_symbol(px(11.60), py(14.10), "vmc_imp", "+30 m³/h"))
    out.append(mep_symbol(px(15.10), py(13.10), "vmc_imp", "+45 m³/h"))

    # Extracción aire viciado VMC en Baño Hijos (-35 m³/h), Baño Suite (-35 m³/h) y Vestidor (-15 m³/h)
    out.append(mep_symbol(px(7.65), py(6.15), "vmc_ext", "-35 m³/h"))
    out.append(mep_symbol(px(15.10), py(6.15), "vmc_ext", "-35 m³/h"))
    out.append(mep_symbol(px(14.70), py(8.30), "vmc_ext", "-15 m³/h"))

    # Bajantes Acústicas PVC Serie B Ø110 mm
    out.append(mep_symbol(px(8.55), py(6.95), "drain", "BAJANTE B-01 Ø110"))
    out.append(mep_symbol(px(14.15), py(7.35), "drain", "BAJANTE B-02 Ø110"))

    # Tomas RJ45 Cat6A 10 Gbps + Schuko en Sala Polivalente (TV + Setup Gaming), Dormitorios y Suite
    out.append(mep_symbol(px(13.30), py(6.50), "rj45", "2×RJ45 TV/Consola"))
    out.append(mep_symbol(px(12.45), py(5.55), "rj45", "2×RJ45 Gaming"))
    out.append(mep_symbol(px(9.35), py(15.80), "rj45", "2×RJ45 D1"))
    out.append(mep_symbol(px(12.90), py(15.80), "rj45", "2×RJ45 D2"))
    out.append(mep_symbol(px(13.75), py(14.75), "rj45", "RJ45 TV Suite"))
    out.append(mep_symbol(px(10.10), py(8.05), "thermostat", "KNX Sala"))
    out.append(mep_symbol(px(8.60), py(13.55), "thermostat", "KNX D1"))
    out.append(mep_symbol(px(11.15), py(13.55), "thermostat", "KNX D2"))
    out.append(mep_symbol(px(13.85), py(12.50), "thermostat", "KNX Suite"))
    out.append('</g>')

    # Sellos de Estancias (Room Stamps)
    out.append(room_stamp(px(7.65), py(7.45), "15. BAÑO HIJOS", 6.80, "2,32×2,93m · Doble Seno", "E-19"))
    out.append(room_stamp(px(11.35), py(7.45), "15B. SALA POLIVALENTE / CINE", 14.00, "4,78×2,93m · Rw≥50dB · 4º Dorm", "E-19B"))
    out.append(room_stamp(px(15.10), py(6.65), "18. BAÑO SUITE", 6.30, "2,81×2,25m · Ducha Doble", "E-22"))
    out.append(room_stamp(px(14.70), py(11.15), "17. VESTIDOR SUITE", 8.40, "7,75 m armarios + Isla", "E-21"))
    out.append(room_stamp(px(10.10), py(12.83), "12. GALERÍA ACÚSTICA", 8.20, "Vidrio 4+4 Silence (Rw=42dB)", "E-16"))
    out.append(room_stamp(px(8.05), py(17.15), "13. DORM. NIÑA", 14.60, "3,42×4,27m · Estudio 90°", "E-17"))
    out.append(room_stamp(px(11.65), py(17.15), "14. DORM. NIÑO", 14.60, "3,42×4,27m · Rw≥50dB", "E-18"))
    out.append(room_stamp(px(15.10), py(17.15), "16. MASTER SUITE", 16.50, "3,05×5,41m · King Size", "E-20"))
    out.append(room_stamp(px(11.55), py(18.70), "19. BALCÓN SUR CONTINUO", 14.00, "10,85×1,40m · Sombra a PB", "E-23"))

    # ==========================================================================
    # ACOTACIÓN ENCADENADA REAL P1 (1:50)
    # ==========================================================================
    # Cotas Superiores (Banda Norte: Baño Hijos + Sala Polivalente + Baño Suite = 10,85 m)
    out.append(dim_h(px(4.00), px(6.15), py(5.00), -22, "2,15 m (Cub. FV)"))
    out.append(dim_h(px(6.15), px(8.88), py(5.00), -22, "2,32 m útil (Baño Hijos 6,80m²)", "#38bdf8"))
    out.append(dim_h(px(8.88), px(13.78), py(5.00), -22, "4,78 m útil (Sala Polivalente 14,00m²)", "#fbbf24"))
    out.append(dim_h(px(13.78), px(17.00), py(5.00), -22, "2,81 m útil (Baño Suite 6,30m²)", "#38bdf8"))
    out.append(dim_h(px(6.15), px(17.00), py(5.00), -44, "10,85 m (ANCHO VOLUMEN CONSTRUIDO PLANTA PRIMERA · EJES B - E)", "#f8fafc"))

    # Cotas Inferiores (Banda Sur: Dormitorio Niña + Dormitorio Niño + Master Suite)
    out.append(dim_h(px(6.15), px(9.99), py(19.40), 22, "3,42 m útil (Dorm. Niña 14,60m²)", "#10b981"))
    out.append(dim_h(px(9.99), px(13.54), py(19.40), 22, "3,42 m útil (Dorm. Niño 14,60m²)", "#10b981"))
    out.append(dim_h(px(13.54), px(17.00), py(19.40), 22, "3,05 m útil (Master Suite 16,50m²)", "#38bdf8"))

    # Cotas Verticales Izquierda y Derecha
    out.append(dim_v(py(5.00), py(8.28), px(6.15), -26, "2,93 m útil (Baño/Sala)"))
    out.append(dim_v(py(8.28), py(13.32), px(6.15), -26, "4,92 m (Esc./Galería)"))
    out.append(dim_v(py(13.32), py(18.00), px(6.15), -26, "4,27 m útil (Dorms Hijos)"))
    out.append(dim_v(py(18.00), py(19.40), px(6.15), -26, "1,40 m (Balcón)"))
    out.append(dim_v(py(5.00), py(7.66), px(17.00), 24, "2,25 m (Baño Suite)"))
    out.append(dim_v(py(7.66), py(12.18), px(17.00), 24, "4,40 m (Vestidor)"))
    out.append(dim_v(py(12.18), py(18.00), px(17.00), 24, "5,41 m (Dorm. Suite)"))
    out.append(dim_v(py(5.00), py(18.00), px(17.00), 54, "13,00 m (FONDO P1 EJES 1 - 4)", "#f8fafc"))

    # Panel Técnico Derecho
    out.append(mep_legend_panel(1224, 26, 548))

    out.append('<g transform="translate(1224, 465)" font-family="monospace">')
    out.append('<rect x="0" y="0" width="548" height="315" fill="#0b1120" stroke="#475569" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="548" height="22" fill="#1e293b" stroke="#475569" stroke-width="1"/>')
    out.append('<text x="12" y="15" fill="#38bdf8" font-size="7.6" font-weight="700">CUADRO DE ESTANCIAS A ESCALA REAL — PLANTA PRIMERA (+3,15 m)</text>')
    rows = [
        ("E-16", "12. Galería Acústica y Escalera", "6,98 × 0,86 m", "8,20 m²", "Vidrio Laminado 4+4 Silence (Rw = 42 dB)"),
        ("E-17", "13. Dormitorio Infantil Niña", "3,42 × 4,27 m", "14,60 m²", "Mesa estudio Este (Luz 90°) · VMC +30 m³/h"),
        ("E-18", "14. Dormitorio Infantil Niño", "3,42 × 4,27 m", "14,60 m²", "Medianera ciega Rw ≥ 50 dB · VMC +30 m³/h"),
        ("E-19", "15. Baño Compartido Hijos", "2,32 × 2,93 m", "6,80 m²", "Doble seno 1,40m + Bañera · VMC -35 m³/h"),
        ("E-19B", "15B. Sala Polivalente / Cine", "4,78 × 2,93 m", "14,00 m²", "TV 65\" + Sofá-cama + Gaming · Rw ≥ 50 dB"),
        ("E-20", "16. Dormitorio Master Suite", "3,05 × 5,41 m", "16,50 m²", "Cama King 180×200 · Balconera Sur 2,70 m"),
        ("E-21", "17. Vestidor Doble Suite", "3,90 × 4,40 m", "8,40 m²", "7,75 m lineales armarios + Isla + Luz Este"),
        ("E-22", "18. Baño Privado Suite", "2,81 × 2,25 m", "6,30 m²", "Doble Ducha Walk-in + Doble Seno 1,45m"),
        ("E-23", "19. Balcón-Terraza Sur", "10,85 × 1,40 m", "14,00 m²", "Barandilla vidrio 10+10.2 mm · Sombra a PB"),
    ]
    ry = 38
    for cod, est, cot, sup, obs in rows:
        out.append(f'<rect x="8" y="{ry-10}" width="532" height="19" fill="none" stroke="#1e293b" stroke-width="0.6"/>')
        out.append(f'<text x="12" y="{ry+3}" fill="#38bdf8" font-size="5.9" font-weight="700">{cod}</text>')
        out.append(f'<text x="58" y="{ry+3}" fill="#e2e8f0" font-size="5.9">{est}</text>')
        out.append(f'<text x="205" y="{ry+3}" fill="#cbd5e1" font-size="5.9">{cot}</text>')
        out.append(f'<text x="278" y="{ry+3}" fill="#10b981" font-size="6.1" font-weight="700">{sup}</text>')
        out.append(f'<text x="335" y="{ry+3}" fill="#94a3b8" font-size="5.5">{obs}</text>')
        ry += 20

    out.append('<rect x="10" y="216" width="528" height="88" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="18" y="231" fill="#10b981" font-size="6.4" font-weight="700">TOTAL ÚTIL PLANTA PRIMERA: 89,40 m² INTERIORES + 14,00 m² BALCÓN (TOTAL VIVIENDA = 202,40 m²)</text>')
    out.append('<text x="18" y="245" fill="#fbbf24" font-size="5.8" font-weight="700">• Sala Polivalente / Cine &amp; Gaming (14,00 m²): Tabiques Rw≥50dB + Puerta Rw≥38dB + Mirador 4+4 Silence.</text>')
    out.append('<text x="18" y="258" fill="#cbd5e1" font-size="5.7">• Escala 100% Real Verificada: Baño Hijos (2,32×2,93m = 6,80 m²) es ahora &lt;50% de cada Dormitorio Infantil (14,60 m²).</text>')
    out.append('<text x="18" y="271" fill="#cbd5e1" font-size="5.7">• Ergonomía Visual Infantil: Mesas de estudio de 1,80 m en paredes Este con luz Sur a 90° sin reflejos.</text>')
    out.append('<text x="18" y="284" fill="#cbd5e1" font-size="5.7">• Versatilidad Futura: La Sala Polivalente (4,78×2,93 m) es convertible en 4º Dormitorio doble sin obra.</text>')
    out.append('</g>')

    out.append(north_and_scale(1290, 845, S, 5))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="E-04",
        title="PLANTA CONSTRUCTIVA E INSTALACIONES — PLANTA PRIMERA (+3,15 m)",
        scale="1:50 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN (REVISIÓN ESCALA REAL + SALA POLIVALENTE)",
        subtitle="Sala Polivalente Cine/Gaming (14 m²), Dorms Hijos (2×14,6 m²), Baño Hijos (6,8 m²), Master Suite (31,2 m²) y Balcón Sur",
        extra_notes=[
            "Superficie Útil Interior P1: 89,40 m² + 14,00 m² Balcón Sur (Total Útil Vivienda PB + P1 = 202,40 m²)",
            "Cota Pavimento Terminado P1: +3,15 m · Altura libre interior bajo falso techo: 2,65 m (Cota coronación +6,80 m)",
            "Aislamiento Acústico Sala Polivalente y Dormitorios: Tabique PYL doble placa + lana mineral (Rw ≥ 50 dB · CTE DB-HR)",
            "Coordenadas alineadas al milímetro con Planta Baja: Ejes A(4,00), B(6,15), C(8,50), D(12,50), E(17,00) / 1(5,00)..4(18,00)",
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
