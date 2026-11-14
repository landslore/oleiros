#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Planos Técnicos Generales de Ejecución (A-01 Planta Baja y A-02 Planta Primera).
Escala geométrica rigurosa (1 m = 42 px), ejes estructurales, cotas encadenadas triples,
bloques CAD de mobiliario/sanitarios, círculos NHG y cajetín ISO 7200.
"""

import os
import shutil
from cad_engine import (
    sanitize_svg_text,
    cad_defs, fmt_m, draw_structural_axis, draw_pillar, draw_wall_segment,
    draw_dim_h, draw_dim_v, draw_door_swing, draw_sliding_door, draw_window_cad,
    draw_room_stamp, draw_nhg_circle, draw_wc_block, draw_sink_block,
    draw_shower_block, draw_bed_block, draw_wardrobe_block, draw_mep_symbol,
    draw_north_rose_and_scale, draw_iso_title_block
)

S = 40.0  # 1 metro = 40.0 px (Escala 1:100 exacta según skill distribucion-planos-svg)
OX = 110.0  # Origen X de la parcela (0,0) en lienzo SVG
OY = 85.0   # Origen Y de la parcela (0,0) en lienzo SVG


def X(m):
    return OX + m * S


def Y(m):
    return OY + m * S


def L(m):
    return m * S


def build_planta_baja_svg():
    """
    Construye el Plano Técnico A-01: Planta Baja General (±0,00 m) e Implantación en Parcela (20x30 m).
    """
    W_SVG, H_SVG = 1500, 1460
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_SVG} {H_SVG}" width="100%" height="100%" '
        f'style="background-color: #070b14; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;">',
        cad_defs(),
        # Marco exterior de lámina técnica ISO A1
        f'<rect x="12" y="12" width="{W_SVG - 24}" height="{H_SVG - 24}" fill="#0b1120" stroke="#94a3b8" stroke-width="1.8"/>',
        f'<rect x="20" y="20" width="{W_SVG - 40}" height="{H_SVG - 40}" fill="url(#cad-grid-major)" stroke="#cbd5e1" stroke-width="0.9"/>',
    ]

    # Marcas de coordenadas de borde de lámina (A..H / 1..8)
    for idx, ch in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
        xm = 120 + idx * 175
        out.append(f'<text x="{xm}" y="18" fill="#64748b" font-size="7" text-anchor="middle">{ch}</text>')
        out.append(f'<text x="{xm}" y="{H_SVG - 14}" fill="#64748b" font-size="7" text-anchor="middle">{ch}</text>')

    # =========================================================================
    # CAPA 1: PARCELA Y RETRANQUEOS (id="parcela-y-retranqueos")
    # =========================================================================
    out.append('<g id="parcela-y-retranqueos">')
    # Vial público al Norte (Y = -1.2m a 0.0m)
    out.append(f'<rect x="{X(0):.1f}" y="{Y(-1.2):.1f}" width="{L(20):.1f}" height="{L(1.2):.1f}" fill="#0f172a" stroke="#475569" stroke-width="0.8"/>')
    out.append(f'<line x1="{X(0):.1f}" y1="{Y(-0.6):.1f}" x2="{X(20):.1f}" y2="{Y(-0.6):.1f}" stroke="#64748b" stroke-width="0.8" stroke-dasharray="12,8"/>')
    out.append(f'<text x="{X(10):.1f}" y="{Y(-0.75):.1f}" fill="#94a3b8" font-size="8.5" font-weight="700" text-anchor="middle" letter-spacing="2">VIAL PÚBLICO MUNICIPAL (ACCESO RODADO Y PEATONAL NORTE · COTA -0,15 m)</text>')

    # Límite oficial de Parcela 20,00 x 30,00 m = 600,00 m²
    out.append(f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{L(20):.1f}" height="{L(30):.1f}" fill="none" stroke="#e2e8f0" stroke-width="1.6" stroke-dasharray="16,5,3,5"/>')
    # Hitos topográficos en las 4 esquinas de la parcela
    for px_m, py_m, lbl in [
        (0, 0, "P-NW (0,00 ; 0,00) Z=-0,15"),
        (20, 0, "P-NE (20,00 ; 0,00) Z=-0,15"),
        (0, 30, "P-SW (0,00 ; 30,00) Z=-0,20"),
        (20, 30, "P-SE (20,00 ; 30,00) Z=-0,20"),
    ]:
        out.append(f'<circle cx="{X(px_m):.1f}" cy="{Y(py_m):.1f}" r="4" fill="#0b1120" stroke="#f59e0b" stroke-width="1.2"/>')
        out.append(f'<circle cx="{X(px_m):.1f}" cy="{Y(py_m):.1f}" r="1" fill="#f59e0b"/>')
        anchor = "start" if px_m == 0 else "end"
        dx_t = 7 if px_m == 0 else -7
        dy_t = 11 if py_m == 0 else -6
        out.append(f'<text x="{X(px_m)+dx_t:.1f}" y="{Y(py_m)+dy_t:.1f}" fill="#f59e0b" font-size="6.5" font-weight="700" text-anchor="{anchor}">{lbl}</text>')

    # Línea discontinua de Retranqueos PGOM Oleiros Ordenanza 2B (Norte 5,00m, Este/Oeste 3,00m, Sur 3,00m mín / >10m real)
    out.append(f'<rect x="{X(3.0):.1f}" y="{Y(5.0):.1f}" width="{L(14.0):.1f}" height="{L(22.0):.1f}" fill="none" stroke="#ef4444" stroke-width="0.9" stroke-dasharray="6,4" opacity="0.8"/>')
    out.append(f'<text x="{X(16.8):.1f}" y="{Y(4.85):.1f}" fill="#ef4444" font-size="6.5" font-weight="700" text-anchor="end">LÍNEA LÍMITE DE EDIFICACIÓN (RETRANQUEO FRONTAL 5,00 m · LATERALES 3,00 m — PGOM 2B)</text>')

    # Ejes Estructurales de Replanteo (Verticales A..E, Horizontales 1..5)
    v_axes = [(4.00, "A"), (6.15, "B"), (8.50, "C"), (12.50, "D"), (17.00, "E")]
    for xm, lbl in v_axes:
        out.append(draw_structural_axis(X(xm), Y(3.8), X(xm), Y(22.2), lbl, bubble_at="start"))
    h_axes = [(5.00, "1"), (8.40, "2"), (12.40, "3"), (18.45, "4"), (21.45, "5")]
    for ym, lbl in h_axes:
        out.append(draw_structural_axis(X(0.4), Y(ym), X(18.2), Y(ym), lbl, bubble_at="start"))
    out.append('</g>')

    # =========================================================================
    # CAPA 2: URBANIZACIÓN EXTERIOR, PÉRGOLA, PORCHES Y PISCINA
    # =========================================================================
    out.append('<g id="urbanizacion-exteriores">')
    # Acceso rodado y Pérgola 2 Vehículos: X=[1.00..3.85], Y=[5.00..12.00] (28,00 m²)
    out.append(f'<rect x="{X(1.00):.1f}" y="{Y(0.00):.1f}" width="{L(2.85):.1f}" height="{L(5.00):.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="0.7"/>')
    out.append(f'<text x="{X(2.42):.1f}" y="{Y(2.50):.1f}" fill="#94a3b8" font-size="6.5" text-anchor="middle">RAMPA ACCESO RODADO (p=2%)</text>')
    out.append(f'<rect x="{X(1.00):.1f}" y="{Y(5.00):.1f}" width="{L(2.85):.1f}" height="{L(7.00):.1f}" fill="url(#hatch-tile-60)" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="8,3"/>')
    # Vigas de pérgola
    for ym_beam in [5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]:
        out.append(f'<line x1="{X(1.00):.1f}" y1="{Y(ym_beam):.1f}" x2="{X(3.85):.1f}" y2="{Y(ym_beam):.1f}" stroke="#475569" stroke-width="0.6" stroke-dasharray="4,2"/>')
    # Dos plazas de vehículo técnicas (con ejes y contorno mecánico CAD)
    for idx_car, cy_m in enumerate([(5.35, "PLAZA V-01 (VE)"), (8.65, "PLAZA V-02")]):
        ym_c, lbl_c = cy_m
        out.append(f'<rect x="{X(1.30):.1f}" y="{Y(ym_c):.1f}" width="{L(2.10):.1f}" height="{L(2.85):.1f}" rx="4" fill="none" stroke="#64748b" stroke-width="0.85"/>')
        out.append(f'<rect x="{X(1.48):.1f}" y="{Y(ym_c+0.35):.1f}" width="{L(1.74):.1f}" height="{L(2.15):.1f}" fill="none" stroke="#475569" stroke-width="0.5"/>')
        out.append(f'<line x1="{X(1.30):.1f}" y1="{Y(ym_c):.1f}" x2="{X(3.40):.1f}" y2="{Y(ym_c+2.85):.1f}" stroke="#334155" stroke-width="0.4" stroke-dasharray="3,2"/>')
        out.append(f'<text x="{X(2.35):.1f}" y="{Y(ym_c+1.45):.1f}" fill="#94a3b8" font-size="6" text-anchor="middle">{lbl_c}</text>')
    # Wallbox 7.4kW
    out.append(f'<rect x="{X(3.70):.1f}" y="{Y(6.20):.1f}" width="6" height="12" fill="#0b1120" stroke="#f59e0b" stroke-width="1"/>')
    out.append(f'<text x="{X(3.60):.1f}" y="{Y(6.35):.1f}" fill="#f59e0b" font-size="5.8" font-weight="700" text-anchor="end">WALLBOX 7,4kW (32A)</text>')

    # Senda peatonal Norte y Porche Entrada Noble: X=[7.00..9.30], Y=[3.50..5.00] (3,50 m²)
    out.append(f'<rect x="{X(7.30):.1f}" y="{Y(0.00):.1f}" width="{L(1.60):.1f}" height="{L(3.50):.1f}" fill="url(#hatch-tile-60)" stroke="#475569" stroke-width="0.6"/>')
    out.append(f'<rect x="{X(7.00):.1f}" y="{Y(3.50):.1f}" width="{L(2.30):.1f}" height="{L(1.50):.1f}" fill="url(#hatch-tile-60)" stroke="#38bdf8" stroke-width="1.1" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{X(8.15):.1f}" y="{Y(4.15):.1f}" fill="#38bdf8" font-size="6.5" font-weight="700" text-anchor="middle">[E-02] PORCHE NORTE</text>')
    out.append(f'<text x="{X(8.15):.1f}" y="{Y(4.40):.1f}" fill="#cbd5e1" font-size="5.8" text-anchor="middle">3,50 m² · Granito C3 · Z=+0,05m</text>')

    # Porche Sur Expandido Techado: X=[6.15..17.00], Y=[18.45..21.45] (Fondo 3,00 m · 36,00 m²)
    out.append(f'<rect x="{X(6.15):.1f}" y="{Y(18.45):.1f}" width="{L(10.85):.1f}" height="{L(3.00):.1f}" fill="url(#hatch-wood-deck)" stroke="#f59e0b" stroke-width="1.2"/>')
    # Canaleta perimetral oculta AISI 316 en borde sur del porche
    out.append(f'<line x1="{X(6.15):.1f}" y1="{Y(21.40):.1f}" x2="{X(17.00):.1f}" y2="{Y(21.40):.1f}" stroke="#38bdf8" stroke-width="0.9" stroke-dasharray="6,2"/>')
    # Churrasqueira tradicional de obra en testero Este del Porche Sur: X=[16.10..16.95], Y=[18.60..21.20]
    out.append(f'<rect x="{X(16.10):.1f}" y="{Y(18.65):.1f}" width="{L(0.82):.1f}" height="{L(2.40):.1f}" fill="#1e293b" stroke="#f8fafc" stroke-width="1.0"/>')
    # Parrilla inox 100x60cm y fregadero auxiliar
    out.append(f'<rect x="{X(16.20):.1f}" y="{Y(18.85):.1f}" width="{L(0.62):.1f}" height="{L(1.00):.1f}" fill="#0f172a" stroke="#ef4444" stroke-width="0.8"/>')
    for yg in [19.0, 19.15, 19.3, 19.45, 19.6, 19.7]:
        out.append(f'<line x1="{X(16.22):.1f}" y1="{Y(yg):.1f}" x2="{X(16.80):.1f}" y2="{Y(yg):.1f}" stroke="#ef4444" stroke-width="0.4"/>')
    out.append(draw_sink_block(X(16.20), Y(20.10), L(0.62), L(0.75), basins=1, orient="E"))
    out.append(f'<g transform="translate({X(15.95):.1f}, {Y(19.85):.1f}) rotate(-90)"><text x="0" y="0" fill="#f59e0b" font-size="6" font-weight="700" text-anchor="middle">CHURRASQUEIRA GRANITO 2,40x0,80m</text></g>')

    # Mesa Comedor Exterior 10 Pax en Porche Sur: X=[12.60..15.40], Y=[19.40..20.40]
    out.append(f'<rect x="{X(12.60):.1f}" y="{Y(19.40):.1f}" width="{L(2.80):.1f}" height="{L(1.00):.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.85"/>')
    for idx_s in range(4):
        sx = X(12.80 + idx_s * 0.62)
        out.append(f'<rect x="{sx:.1f}" y="{Y(19.18):.1f}" width="{L(0.42):.1f}" height="{L(0.18):.1f}" fill="none" stroke="#94a3b8" stroke-width="0.6"/>')
        out.append(f'<rect x="{sx:.1f}" y="{Y(20.44):.1f}" width="{L(0.42):.1f}" height="{L(0.18):.1f}" fill="none" stroke="#94a3b8" stroke-width="0.6"/>')
    out.append(f'<text x="{X(14.00):.1f}" y="{Y(19.95):.1f}" fill="#cbd5e1" font-size="6" font-weight="700" text-anchor="middle">MESA EXT. IROKO 2,80x1,00m (10 PAX)</text>')

    # Lounge Exterior en Porche Sur frente al Salón: X=[7.20..10.20], Y=[19.20..20.80]
    out.append(f'<path d="M {X(7.20):.1f} {Y(19.20):.1f} L {X(9.80):.1f} {Y(19.20):.1f} L {X(9.80):.1f} {Y(19.95):.1f} L {X(7.95):.1f} {Y(19.95):.1f} L {X(7.95):.1f} {Y(20.85):.1f} L {X(7.20):.1f} {Y(20.85):.1f} Z" fill="#0f172a" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{X(8.25):.1f}" y="{Y(20.15):.1f}" width="{L(1.20):.1f}" height="{L(0.65):.1f}" fill="#0f172a" stroke="#64748b" stroke-width="0.7"/>')
    out.append(draw_room_stamp(X(11.30), Y(20.80), "E-14", "PORCHE SUR EXPANDIDO", 36.00, "Tarima Iroko (Fondo 3,00m)", "±0,00"))

    # Piscina Privada Soleada (7,50 x 3,50 m = 26,25 m²): X=[8.50..16.00], Y=[23.00..26.50]
    # Albardilla perimetral de piedra caliza C3 de 50 cm
    out.append(f'<rect x="{X(8.00):.1f}" y="{Y(22.50):.1f}" width="{L(8.50):.1f}" height="{L(4.50):.1f}" fill="url(#hatch-tile-60)" stroke="#94a3b8" stroke-width="0.8"/>')
    out.append(f'<rect x="{X(8.50):.1f}" y="{Y(23.00):.1f}" width="{L(7.50):.1f}" height="{L(3.50):.1f}" fill="#082f49" stroke="#38bdf8" stroke-width="1.5"/>')
    out.append(f'<rect x="{X(8.50):.1f}" y="{Y(23.00):.1f}" width="{L(7.50):.1f}" height="{L(3.50):.1f}" fill="url(#hatch-water)"/>')
    # Playa sumergida Oeste (1.20m ancho, h=-0.40m) y peldaños de bajada
    out.append(f'<line x1="{X(9.70):.1f}" y1="{Y(23.00):.1f}" x2="{X(9.70):.1f}" y2="{Y(26.50):.1f}" stroke="#38bdf8" stroke-width="0.9" stroke-dasharray="4,2"/>')
    for xp_s in [9.95, 10.20, 10.45]:
        out.append(f'<line x1="{X(xp_s):.1f}" y1="{Y(23.00):.1f}" x2="{X(xp_s):.1f}" y2="{Y(24.10):.1f}" stroke="#38bdf8" stroke-width="0.6"/>')
    out.append(f'<text x="{X(9.10):.1f}" y="{Y(24.80):.1f}" fill="#7dd3fc" font-size="5.8" text-anchor="middle">PLAYA -0,40m</text>')
    out.append(draw_room_stamp(X(12.60), Y(24.75), "E-15", "PISCINA PRIVADA", 26.25, "Gunitado Porcelánico", "-1,20/-1,50"))
    # Caseta técnica enterrada depuración salina: X=[16.80..18.80], Y=[24.50..26.00]
    out.append(f'<rect x="{X(16.80):.1f}" y="{Y(24.50):.1f}" width="{L(2.00):.1f}" height="{L(1.50):.1f}" fill="#0f172a" stroke="#64748b" stroke-width="0.8" stroke-dasharray="4,2"/>')
    out.append(f'<text x="{X(17.80):.1f}" y="{Y(25.20):.1f}" fill="#94a3b8" font-size="6" font-weight="700" text-anchor="middle">ARQUETA TÉCNICA PISCINA</text>')
    out.append(f'<text x="{X(17.80):.1f}" y="{Y(25.45):.1f}" fill="#64748b" font-size="5.5" text-anchor="middle">2,00x1,50m · Clorador Salino</text>')
    out.append('</g>')

    # =========================================================================
    # CAPA 3: PAVIMENTOS INTERIORES Y PATIO CORRALA
    # =========================================================================
    out.append('<g id="pavimentos-interiores">')
    # Cuerpo interior principal PB: X=[6.15..17.00], Y=[5.00..18.45] + Ala Oeste Mudroom/Trastero X=[3.85..6.15], Y=[5.00..12.40]
    out.append(f'<rect x="{X(3.85):.1f}" y="{Y(5.00):.1f}" width="{L(2.30):.1f}" height="{L(7.40):.1f}" fill="url(#hatch-tile-60)"/>')
    out.append(f'<rect x="{X(6.15):.1f}" y="{Y(5.00):.1f}" width="{L(10.85):.1f}" height="{L(13.45):.1f}" fill="url(#hatch-tile-60)"/>')
    # Serpentín de suelo radiante-refrescante (sombreado técnico sutil en zonas interiores)
    out.append(f'<rect x="{X(6.30):.1f}" y="{Y(5.35):.1f}" width="{L(10.35):.1f}" height="{L(12.75):.1f}" fill="url(#hatch-radiant)" opacity="0.5"/>')

    # PATIO CORRALA CENTRAL HABITABLE: X=[8.50..12.50], Y=[8.40..12.40] (4,00 x 4,00 m = 16,00 m²)
    out.append(f'<rect x="{X(8.50):.1f}" y="{Y(8.40):.1f}" width="{L(4.00):.1f}" height="{L(4.00):.1f}" fill="#071510" stroke="#10b981" stroke-width="1.4"/>')
    out.append(f'<rect x="{X(8.50):.1f}" y="{Y(8.40):.1f}" width="{L(4.00):.1f}" height="{L(4.00):.1f}" fill="url(#hatch-wood-deck)"/>')
    # Canaleta perimetral oculta inox AISI 316 en los 4 bordes del patio
    out.append(f'<rect x="{X(8.62):.1f}" y="{Y(8.52):.1f}" width="{L(3.76):.1f}" height="{L(3.76):.1f}" fill="none" stroke="#38bdf8" stroke-width="0.7" stroke-dasharray="4,2"/>')
    # Alcorque circular drenante con Acer palmatum en cuadrante NW del patio
    out.append(f'<circle cx="{X(9.55):.1f}" cy="{Y(9.55):.1f}" r="{L(0.72):.1f}" fill="url(#hatch-gravel)" stroke="#10b981" stroke-width="1.0"/>')
    out.append(f'<circle cx="{X(9.55):.1f}" cy="{Y(9.55):.1f}" r="{L(0.52):.1f}" fill="none" stroke="#34d399" stroke-width="0.7" stroke-dasharray="3,2"/>')
    out.append(f'<line x1="{X(9.05):.1f}" y1="{Y(9.55):.1f}" x2="{X(10.05):.1f}" y2="{Y(9.55):.1f}" stroke="#10b981" stroke-width="0.5"/>')
    out.append(f'<line x1="{X(9.55):.1f}" y1="{Y(9.05):.1f}" x2="{X(9.55):.1f}" y2="{Y(10.05):.1f}" stroke="#10b981" stroke-width="0.5"/>')
    out.append(f'<text x="{X(9.55):.1f}" y="{Y(9.50):.1f}" fill="#a7f3d0" font-size="5.5" font-weight="700" text-anchor="middle">ACER PALMATUM</text>')
    out.append(f'<text x="{X(9.55):.1f}" y="{Y(9.68):.1f}" fill="#6ee7b7" font-size="5.0" text-anchor="middle">Alcorque Ø1,44m</text>')
    # Banco corrido de lectura de Iroko en pared Norte del patio (2,40 x 0,50 m) bajo alero de 80 cm
    out.append(f'<rect x="{X(10.00):.1f}" y="{Y(8.55):.1f}" width="{L(2.35):.1f}" height="{L(0.50):.1f}" fill="#0f172a" stroke="#f59e0b" stroke-width="0.8"/>')
    out.append(f'<text x="{X(11.17):.1f}" y="{Y(8.85):.1f}" fill="#fde68a" font-size="5.5" text-anchor="middle">BANCO IROKO 2,35x0,50m</text>')
    # Sumideros sifónicos pluviales Ø110mm en patio
    out.append(draw_mep_symbol(X(8.80), Y(12.10), "drain", "SUM-P1 Ø110"))
    out.append(draw_mep_symbol(X(12.10), Y(12.10), "drain", "SUM-P2 Ø110"))
    out.append(draw_room_stamp(X(10.50), Y(11.15), "E-07", "PATIO CORRALA CENTRAL", 16.00, "Iroko Cota 0 · Abierto", "±0,00"))
    out.append('</g>')

    # =========================================================================
    # CAPA 4: MUROS EXTERIORES DE CARGA Y ENVOLVENTE SATE (id="muros-exteriores")
    # Espesor = 0,35 m (14 px) con hoja portante + aislamiento SATE + rayado ANSI31
    # =========================================================================
    out.append('<g id="muros-exteriores">')
    wt = L(0.35)  # 14 px
    # Muro Norte Ala Oeste (Zaguán): X=3.85..6.15, Y=5.00..5.35
    out.append(draw_wall_segment(X(3.85), Y(5.00), L(2.30), wt, "ext"))
    # Muro Norte Cuerpo Principal: X=6.15..17.00, Y=5.00..5.35 (con huecos C-01, C-03, C-04)
    out.append(draw_wall_segment(X(6.15), Y(5.00), L(1.55), wt, "ext"))   # Tramo hasta puerta C-01 (X=7.70..8.70)
    out.append(draw_wall_segment(X(8.70), Y(5.00), L(1.90), wt, "ext"))   # Tramo hasta ventana Despacho C-03 (X=10.60..12.40)
    out.append(draw_wall_segment(X(12.40), Y(5.00), L(2.10), wt, "ext"))  # Tramo hasta ventana Baño C-04 (X=14.50..15.30)
    out.append(draw_wall_segment(X(15.30), Y(5.00), L(1.70), wt, "ext"))  # Esquina NE hasta X=17.00

    # Muro Oeste Ala Mudroom + Trastero: X=3.85..4.20, Y=5.00..12.40 (con huecos C-02 y C-09)
    out.append(draw_wall_segment(X(3.85), Y(5.00), wt, L(1.40), "ext"))   # Hasta puerta C-02 (Y=6.40..7.30)
    out.append(draw_wall_segment(X(3.85), Y(7.30), wt, L(2.50), "ext"))   # Hasta puerta Trastero C-09 (Y=9.80..10.70)
    out.append(draw_wall_segment(X(3.85), Y(10.70), wt, L(1.70), "ext"))  # Hasta esquina SW trastero Y=12.40
    # Cierre Sur Trastero: X=3.85..6.15, Y=12.05..12.40
    out.append(draw_wall_segment(X(3.85), Y(12.05), L(2.30), wt, "ext"))

    # Muro Oeste Salón y Escalera: X=6.15..6.50, Y=12.05..18.45
    out.append(draw_wall_segment(X(6.15), Y(12.05), wt, L(6.40), "ext"))

    # Muro Este Completo: X=16.65..17.00, Y=5.00..18.45
    out.append(draw_wall_segment(X(16.65), Y(5.00), wt, L(13.45), "ext"))

    # Muro Sur Fachada Salón y Comedor: Y=18.10..18.45, X=6.15..17.00 (con grandes correderas C-07 y C-08)
    out.append(draw_wall_segment(X(6.15), Y(18.10), L(0.95), wt, "ext"))   # Machón SW hasta C-07 (X=7.10..12.10)
    out.append(draw_wall_segment(X(12.10), Y(18.10), L(0.75), wt, "ext"))  # Pilar central Sur entre C-07 y C-08 (X=12.85..16.35)
    out.append(draw_wall_segment(X(16.35), Y(18.10), L(0.65), wt, "ext"))  # Machón SE

    # Pilares estructurales (25x25 cm) en intersecciones de ejes
    pillars = [
        (4.00, 5.17, "P-01"), (6.32, 5.17, "P-02"), (8.50, 5.17, "P-03"), (12.50, 5.17, "P-04"), (16.82, 5.17, "P-05"),
        (4.00, 8.40, "P-06"), (6.32, 8.40, "P-07"), (8.50, 8.40, "P-08"), (12.50, 8.40, "P-09"), (16.82, 8.40, "P-10"),
        (4.00, 12.22, "P-11"), (6.32, 12.40, "P-12"), (8.50, 12.40, "P-13"), (12.50, 12.40, "P-14"), (16.82, 12.40, "P-15"),
        (6.32, 18.28, "P-16"), (12.45, 18.28, "P-17"), (16.82, 18.28, "P-18"),
        # Pilares metálicos HEB 160 de Porche Sur y Pérgola
        (1.15, 5.15, "PM-1"), (1.15, 8.50, "PM-2"), (1.15, 11.85, "PM-3"),
        (6.32, 21.30, "PS-1"), (12.45, 21.30, "PS-2"), (16.82, 21.30, "PS-3"),
    ]
    for px_m, py_m, plbl in pillars:
        out.append(draw_pillar(X(px_m), Y(py_m), size_px=9, label=plbl))
    out.append('</g>')

    # =========================================================================
    # CAPA 5: TABIQUERÍA INTERIOR ACÚSTICA PYL (id="tabiqueria-interior")
    # Espesor = 0,10 m (4 px) / Muros técnicos = 0,15 m (6 px)
    # =========================================================================
    out.append('<g id="tabiqueria-interior">')
    pt = L(0.12)  # 4.8 px
    # Separación Zaguán Mudroom / Trastero (Y=8.40, X=4.20..6.15) con puerta corredera
    out.append(draw_wall_segment(X(4.20), Y(8.35), L(1.95), pt, "int"))
    # Separación Zaguán-Trastero / Hall-Escalera (X=6.15, Y=5.35..12.05)
    out.append(draw_wall_segment(X(6.15), Y(5.35), pt, L(1.15), "int"))   # Tramo Norte hasta corredera vidrio (Y=6.50..7.35)
    out.append(draw_wall_segment(X(6.15), Y(7.35), pt, L(4.70), "acoustic"))  # Muro acústico Trastero/Sala Técnica - Escalera

    # Separación Hall / Despacho (X=9.75, Y=5.35..8.40) con puerta acústica C-int
    out.append(draw_wall_segment(X(9.75), Y(5.35), pt, L(1.65), "acoustic"))
    out.append(draw_wall_segment(X(9.75), Y(7.82), pt, L(0.58), "acoustic"))

    # Separación Despacho / Baño PB y Distribuidor Neutro (X=13.65, Y=5.35..8.40)
    out.append(draw_wall_segment(X(13.65), Y(5.35), pt, L(2.15), "acoustic"))
    out.append(draw_wall_segment(X(13.65), Y(8.22), pt, L(0.18), "acoustic"))

    # Tabique horizontal interior entre Baño PB (Y=5.35..7.50) y Distribuidor Neutro (Y=7.50..8.40)
    out.append(draw_wall_segment(X(13.65), Y(7.45), L(3.00), pt, "int"))
    # Tabique Sur del Distribuidor Neutro separándolo de la Cocina (Y=8.40, X=13.65..16.65)
    out.append(draw_wall_segment(X(12.50), Y(8.35), L(4.15), pt, "int"))

    # Lavandería Técnica y Despensa: X=[14.25..16.65], Y=[12.10..14.40]
    out.append(draw_wall_segment(X(14.25), Y(12.10), L(2.40), pt, "int"))
    out.append(draw_wall_segment(X(14.25), Y(12.10), pt, L(2.30), "int"))
    out.append(draw_wall_segment(X(14.25), Y(14.40), L(2.40), pt, "int"))
    out.append('</g>')

    # =========================================================================
    # CAPA 6: CARPINTERÍAS EXTERIORES E INTERIORES (id="carpinterias")
    # Códigos oficiales C-01 a C-09 según Tabla Maestra SSOT
    # =========================================================================
    out.append('<g id="carpinterias">')
    # C-01: Puerta Pivotante Entrada Noble Norte (1,00 x 2,40 m) en X=7.70..8.70, Y=5.00
    out.append(f'<rect x="{X(7.70):.1f}" y="{Y(5.00):.1f}" width="{L(1.00):.1f}" height="{wt:.1f}" fill="#0b1120"/>')
    out.append(draw_door_swing(X(7.70), Y(5.35), L(1.00), WallDir="E", SwingDir="S", code="C-01", dim_txt="1,00x2,40"))

    # C-02: Puerta Batiente Mudroom desde Pérgola (0,90 x 2,10 m) en X=3.85, Y=6.40..7.30
    out.append(f'<rect x="{X(3.85):.1f}" y="{Y(6.40):.1f}" width="{wt:.1f}" height="{L(0.90):.1f}" fill="#0b1120"/>')
    out.append(draw_door_swing(X(4.20), Y(6.40), L(0.90), WallDir="S", SwingDir="E", code="C-02", dim_txt="0,90x2,10"))

    # C-03: Ventana Norte Despacho (1,80 x 1,20 m, h=95cm) en X=10.60..12.40, Y=5.17
    out.append(draw_window_cad(X(10.60), Y(5.17), X(12.40), Y(5.17), wall_thick=wt, code="C-03", dim_txt="1,80x1,20 (h=95)"))

    # C-04: Ventana Norte Baño PB (0,80 x 0,60 m, h=160cm) en X=14.50..15.30, Y=5.17
    out.append(draw_window_cad(X(14.50), Y(5.17), X(15.30), Y(5.17), wall_thick=wt, code="C-04", dim_txt="0,80x0,60 (h=160)"))

    # C-05: Cristalera Fija Suelo-Techo Hall y Despacho hacia Patio Corrala (Y=8.40, X=8.50..12.50)
    out.append(draw_window_cad(X(8.50), Y(8.40), X(12.50), Y(8.40), wall_thick=8, code="C-05", dim_txt="Fijo Cor Vision 4,00x2,60"))

    # C-06: Corredera Elevable 2H Cocina a Patio Corrala (3,00 x 2,60 m) en X=12.50, Y=8.70..11.70
    out.append(draw_sliding_door(X(12.50), Y(8.70), X(12.50), Y(11.70), wall_thick=8, leaves=2, code="C-06", dim_txt="3,00x2,60"))

    # Corredera Elevable 2H Galería/Escalera a Patio Corrala (2,50 x 2,60 m) en X=8.50, Y=9.00..11.50
    out.append(draw_sliding_door(X(8.50), Y(9.00), X(8.50), Y(11.50), wall_thick=8, leaves=2, code="C-06B", dim_txt="2,50x2,60"))

    # Corredera Elevable 2H Salón a Patio Corrala (3,00 x 2,60 m) en Y=12.40, X=9.00..12.00
    out.append(draw_sliding_door(X(9.00), Y(12.40), X(12.00), Y(12.40), wall_thick=8, leaves=2, code="C-06C", dim_txt="3,00x2,60"))

    # C-07: Gran Corredera Elevable 3H Salón a Porche Sur (5,00 x 2,60 m) en Y=18.28, X=7.10..12.10
    out.append(draw_sliding_door(X(7.10), Y(18.28), X(12.10), Y(18.28), wall_thick=wt, leaves=3, code="C-07", dim_txt="5,00x2,60 Cor Vision Plus"))

    # C-08: Gran Corredera Elevable 2H Comedor a Porche Sur (3,50 x 2,60 m) en Y=18.28, X=12.85..16.35
    out.append(draw_sliding_door(X(12.85), Y(18.28), X(16.35), Y(18.28), wall_thick=wt, leaves=2, code="C-08", dim_txt="3,50x2,60 Cor Vision Plus"))

    # C-09: Puerta Batiente Exterior Trastero/Sala Técnica (0,90 x 2,05 m) en X=3.85, Y=9.80..10.70
    out.append(f'<rect x="{X(3.85):.1f}" y="{Y(9.80):.1f}" width="{wt:.1f}" height="{L(0.90):.1f}" fill="#0b1120"/>')
    out.append(draw_door_swing(X(3.85), Y(9.80), L(0.90), WallDir="S", SwingDir="W", code="C-09", dim_txt="0,90x2,05"))

    # Puertas interiores de paso:
    # P-Int 1: Corredera vidrio estriado Zaguán → Hall (0,85m) en X=6.15, Y=6.50..7.35
    out.append(draw_sliding_door(X(6.15), Y(6.50), X(6.15), Y(7.35), wall_thick=pt, leaves=1, code="P-01", dim_txt="0,85"))
    # P-Int 2: Corredera Zaguán → Trastero (0,80m) en Y=8.37, X=4.75..5.55
    out.append(draw_sliding_door(X(4.75), Y(8.37), X(5.55), Y(8.37), wall_thick=pt, leaves=1, code="P-02", dim_txt="0,80"))
    # P-Int 3: Puerta Acústica Rw≥38dB Hall → Despacho (0,82m) en X=9.75, Y=7.00..7.82
    out.append(draw_door_swing(X(9.80), Y(7.00), L(0.82), WallDir="S", SwingDir="E", code="P-03", dim_txt="0,82 Rw38dB"))
    # P-Int 4: Puerta corredera Despacho → Distribuidor Neutro Baño (0,80m) en X=13.65, Y=7.50..8.30
    out.append(draw_sliding_door(X(13.65), Y(7.50), X(13.65), Y(8.30), wall_thick=pt, leaves=1, code="P-04", dim_txt="0,80"))
    # P-Int 5: Puerta corredera oculta Krona Distribuidor Neutro → Baño PB (0,75m) en Y=7.47, X=14.50..15.25
    out.append(draw_sliding_door(X(14.50), Y(7.47), X(15.25), Y(7.47), wall_thick=pt, leaves=1, code="P-05", dim_txt="0,75 NHG"))
    # P-Int 6: Puerta corredera Distribuidor Neutro → Pasillo Cocina (0,80m) en Y=8.37, X=13.80..14.60
    out.append(draw_sliding_door(X(13.80), Y(8.37), X(14.60), Y(8.37), wall_thick=pt, leaves=1, code="P-06", dim_txt="0,80 NHG"))
    # P-Int 7: Puerta corredera Lavandería (0,80m) en X=14.25, Y=12.85..13.65
    out.append(draw_sliding_door(X(14.25), Y(12.85), X(14.25), Y(13.65), wall_thick=pt, leaves=1, code="P-07", dim_txt="0,80"))
    out.append('</g>')

    # =========================================================================
    # CAPA 7: MOBILIARIO REGLAMENTARIO NHG Y EQUIPAMIENTO TÉCNICO (id="mobiliario-nhg")
    # =========================================================================
    out.append('<g id="mobiliario-nhg">')
    # 01. ZAGUÁN MUDROOM (X=4.20..6.15, Y=5.35..8.35 → 1.95 x 3.00 m = 5.85 m²)
    out.append(f'<rect x="{X(4.30):.1f}" y="{Y(5.42):.1f}" width="{L(1.60):.1f}" height="{L(0.45):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.75"/>')
    out.append(f'<text x="{X(5.10):.1f}" y="{Y(5.70):.1f}" fill="#cbd5e1" font-size="5.2" text-anchor="middle">BANCO ZAPATERO 1,60x0,45</text>')
    out.append(draw_wardrobe_block(X(4.25), Y(7.40), L(0.60), L(0.90), "SECADOR"))
    out.append(draw_room_stamp(X(5.25), Y(6.55), "E-03", "ZAGUÁN MUDROOM", 5.80, "Porcelánico C3", "±0,00"))

    # 02. HALL / RECIBIDOR PRINCIPAL (X=6.25..9.75, Y=5.35..8.35 → 3.50 x 3.00 m = 10.40 m²)
    out.append(draw_wardrobe_block(X(6.30), Y(5.42), L(1.25), L(0.60), "GABANERO 1,25x0,60"))
    # Cuadros CGMP y RITI empotrados
    out.append(f'<rect x="{X(6.27):.1f}" y="{Y(7.45):.1f}" width="{L(0.22):.1f}" height="{L(0.80):.1f}" fill="#0b1120" stroke="#ef4444" stroke-width="0.9"/>')
    out.append(f'<text x="{X(6.58):.1f}" y="{Y(7.90):.1f}" fill="#fca5a5" font-size="5.2">CGMP+RITI</text>')
    out.append(draw_nhg_circle(X(8.20), Y(6.80), 1.50, S, "Ø1,50m NHG"))
    out.append(draw_room_stamp(X(8.20), Y(7.75), "E-04", "HALL PRINCIPAL", 10.40, "Roble 14mm", "±0,00"))

    # 03. DESPACHO SANCTASANCTÓRUM (X=9.85..13.65, Y=5.35..8.35 → 3.80 x 3.00 m = 11.50 m²)
    # Mesa de trabajo 1,80 x 0,80 m perpendicular a fachada norte (luz a 90° por la izquierda)
    out.append(f'<rect x="{X(9.95):.1f}" y="{Y(5.50):.1f}" width="{L(0.80):.1f}" height="{L(1.40):.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<rect x="{X(10.02):.1f}" y="{Y(5.90):.1f}" width="{L(0.18):.1f}" height="{L(0.60):.1f}" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.6"/>')
    out.append(f'<circle cx="{X(11.00):.1f}" cy="{Y(6.20):.1f}" r="{L(0.26):.1f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>')
    out.append(f'<text x="{X(10.35):.1f}" y="{Y(5.78):.1f}" fill="#38bdf8" font-size="5.0" text-anchor="middle">MESA 90°</text>')
    # Sofá-cama invitados 1,40 x 2,00 m en pared Este
    out.append(draw_bed_block(X(12.70), Y(5.45), L(0.90), L(1.90), orient="N", kind="single", label="SOFÁ-CAMA 140"))
    out.append(draw_nhg_circle(X(11.80), Y(6.95), 1.50, S, "Ø1,50m NHG"))
    out.append(draw_room_stamp(X(11.75), Y(7.80), "E-05", "DESPACHO / SUITE", 11.50, "Roble 14mm · Rw38dB", "±0,00"))

    # 04. BAÑO COMPLETO PB y DISTRIBUIDOR NEUTRO (X=13.75..16.65, Y=5.35..8.35 → 5.20 m²)
    out.append(draw_sink_block(X(13.82), Y(5.40), L(0.90), L(0.48), basins=1, orient="N"))
    out.append(draw_wc_block(X(14.90), Y(5.40), L(0.42), L(0.56), orient="N"))
    out.append(draw_shower_block(X(15.45), Y(5.40), L(1.15), L(0.90), drain_side="E", label="DUCHA 1,15x0,90"))
    out.append(draw_room_stamp(X(15.20), Y(6.85), "E-06", "BAÑO COMPLETO PB", 5.20, "Porcelánico C3", "±0,00"))
    out.append(f'<text x="{X(15.20):.1f}" y="{Y(8.05):.1f}" fill="#10b981" font-size="5.5" font-weight="700" text-anchor="middle">DISTRIBUIDOR NEUTRO NHG (DOBLE PUERTA)</text>')

    # 11. TRASTERO EXTERIOR SURF/BICIS y SALA TÉCNICA PASSIVHAUS (X=4.20..6.15, Y=8.50..12.05 → 8,20 m²)
    # Equipos técnicos a escala
    out.append(f'<rect x="{X(5.40):.1f}" y="{Y(8.60):.1f}" width="{L(0.68):.1f}" height="{L(0.65):.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.85"/>')
    out.append(f'<text x="{X(5.74):.1f}" y="{Y(8.95):.1f}" fill="#38bdf8" font-size="4.8" font-weight="700" text-anchor="middle">AEROTERMIA</text>')
    out.append(f'<circle cx="{X(5.74):.1f}" cy="{Y(9.65):.1f}" r="{L(0.30):.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="0.85"/>')
    out.append(f'<text x="{X(5.74):.1f}" y="{Y(9.70):.1f}" fill="#f8fafc" font-size="4.8" font-weight="700" text-anchor="middle">ACS 250L</text>')
    out.append(f'<rect x="{X(5.40):.1f}" y="{Y(10.15):.1f}" width="{L(0.68):.1f}" height="{L(0.75):.1f}" fill="#0f172a" stroke="#10b981" stroke-width="0.85"/>')
    out.append(f'<text x="{X(5.74):.1f}" y="{Y(10.55):.1f}" fill="#10b981" font-size="4.8" font-weight="700" text-anchor="middle">VMC Q350</text>')
    out.append(f'<rect x="{X(5.45):.1f}" y="{Y(11.05):.1f}" width="{L(0.60):.1f}" height="{L(0.55):.1f}" fill="#0f172a" stroke="#a855f7" stroke-width="0.85"/>')
    out.append(f'<text x="{X(5.75):.1f}" y="{Y(11.35):.1f}" fill="#c084fc" font-size="4.8" font-weight="700" text-anchor="middle">RACK 19"+FV</text>')
    # Racks tablas surf y bicis en pared oeste
    out.append(f'<rect x="{X(4.25):.1f}" y="{Y(8.60):.1f}" width="{L(0.45):.1f}" height="{L(1.10):.1f}" fill="none" stroke="#f59e0b" stroke-width="0.7" stroke-dasharray="3,2"/>')
    out.append(f'<text x="{X(4.47):.1f}" y="{Y(9.20):.1f}" fill="#f59e0b" font-size="4.8" text-anchor="middle">RACK SURF</text>')
    out.append(draw_room_stamp(X(4.85), Y(11.55), "E-13", "SALA TÉCNICA / SURF", 8.20, "Epoxi C3", "-0,05"))

    # 10. ESCALERA PRINCIPAL VOLADA (X=6.55..7.65, Y=8.40..13.33 → 17 peldaños H=29cm, CH=17,6cm)
    st_x, st_y, st_w = X(6.55), Y(8.40), L(1.05)
    tread_h = L(0.29)
    out.append(f'<rect x="{st_x:.1f}" y="{st_y:.1f}" width="{st_w:.1f}" height="{17 * tread_h:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    for i in range(1, 17):
        ty = st_y + i * tread_h
        dash = 'stroke-dasharray="3,2"' if i > 10 else ''
        out.append(f'<line x1="{st_x:.1f}" y1="{ty:.1f}" x2="{st_x + st_w:.1f}" y2="{ty:.1f}" stroke="#94a3b8" stroke-width="0.65" {dash}/>')
        if i in (1, 5, 9, 13, 17):
            out.append(f'<text x="{st_x + 7:.1f}" y="{ty - 2.5:.1f}" fill="#64748b" font-size="4.8">{i:02d}</text>')
    # Línea de corte de escalera en peldaño 10 y flecha de subida en eje central
    cut_y = st_y + 10 * tread_h
    out.append(f'<line x1="{st_x - 3:.1f}" y1="{cut_y - 4:.1f}" x2="{st_x + st_w + 3:.1f}" y2="{cut_y + 4:.1f}" stroke="#f59e0b" stroke-width="1.0"/>')
    out.append(f'<line x1="{st_x + st_w/2:.1f}" y1="{st_y + 6:.1f}" x2="{st_x + st_w/2:.1f}" y2="{st_y + 16*tread_h:.1f}" stroke="#38bdf8" stroke-width="0.9" marker-end="url(#arrow-tech)"/>')
    # Barandilla de vidrio estructural 10+10mm
    out.append(f'<line x1="{st_x + st_w:.1f}" y1="{st_y:.1f}" x2="{st_x + st_w:.1f}" y2="{st_y + 17*tread_h:.1f}" stroke="#38bdf8" stroke-width="1.5"/>')
    out.append(f'<g transform="translate({st_x + st_w + 9:.1f}, {st_y + 8.5*tread_h:.1f}) rotate(-90)"><text x="0" y="0" fill="#cbd5e1" font-size="5.5" font-weight="700" text-anchor="middle">[E-12] ESCALERA VOLADA 17P (H=0,29 / CH=0,176)</text></g>')

    # 06. COCINA CON ISLA SANTOS (X=12.50..16.65, Y=8.40..12.10 → 15,20 m²)
    # Frente de columnas Este (fondo 0.65m): Frigo, Hornos, Desayunador Pocket Doors
    col_x = X(16.00)
    for idx_m, (ym_m, hm_m, lbl_m) in enumerate([
        (8.45, 0.75, "FRIGO XXL"),
        (9.20, 0.70, "HORNO/MICRO"),
        (9.90, 1.25, "DESAYUNADOR"),
        (11.15, 0.85, "COL. DESP."),
    ]):
        out.append(f'<rect x="{col_x:.1f}" y="{Y(ym_m):.1f}" width="{L(0.65):.1f}" height="{L(hm_m):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.75"/>')
        out.append(f'<line x1="{col_x:.1f}" y1="{Y(ym_m):.1f}" x2="{col_x+L(0.65):.1f}" y2="{Y(ym_m+hm_m):.1f}" stroke="#475569" stroke-width="0.4"/>')
        out.append(f'<g transform="translate({col_x + L(0.32):.1f}, {Y(ym_m + hm_m/2):.1f}) rotate(-90)"><text x="0" y="2" fill="#cbd5e1" font-size="4.8" text-anchor="middle">{lbl_m}</text></g>')

    # Isla Central Santos Fine (2,80 x 1,00 m) en X=13.75..14.75, Y=8.85..11.65
    # Paso libre al Patio (Oeste): 13.75 - 12.50 = 1.25 m (≥1.05m) | Paso libre a columnas (Este): 16.00 - 14.75 = 1.25 m (≥1.10m)
    ix, iy, iw, ih = X(13.75), Y(8.85), L(1.00), L(2.80)
    out.append(f'<rect x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{ih:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.1"/>')
    # Placa inducción Bora Pure (0,80 x 0,50 m) con extractor central descendente
    out.append(f'<rect x="{ix + L(0.15):.1f}" y="{iy + L(0.35):.1f}" width="{L(0.52):.1f}" height="{L(0.82):.1f}" fill="#1e293b" stroke="#ef4444" stroke-width="0.8"/>')
    out.append(f'<circle cx="{ix + L(0.30):.1f}" cy="{iy + L(0.55):.1f}" r="4.5" fill="none" stroke="#ef4444" stroke-width="0.6"/>')
    out.append(f'<circle cx="{ix + L(0.30):.1f}" cy="{iy + L(0.95):.1f}" r="4.5" fill="none" stroke="#ef4444" stroke-width="0.6"/>')
    out.append(f'<rect x="{ix + L(0.36):.1f}" y="{iy + L(0.68):.1f}" width="5" height="10" fill="#ef4444"/>')
    # Seno fregadero 70x45cm inox antracita
    out.append(f'<rect x="{ix + L(0.15):.1f}" y="{iy + L(1.55):.1f}" width="{L(0.48):.1f}" height="{L(0.75):.1f}" rx="1.5" fill="#0b1120" stroke="#38bdf8" stroke-width="0.75"/>')
    out.append(f'<circle cx="{ix + L(0.39):.1f}" cy="{iy + L(1.92):.1f}" r="2" fill="#38bdf8"/>')
    # 3 Taburetes barra desayuno en cara Oeste de la isla
    for ys_b in [9.25, 10.05, 10.85]:
        out.append(f'<circle cx="{X(13.52):.1f}" cy="{Y(ys_b):.1f}" r="5.5" fill="#0f172a" stroke="#94a3b8" stroke-width="0.65"/>')
    out.append(draw_room_stamp(X(14.35), Y(11.82), "E-08", "COCINA ISLA SANTOS", 15.20, "Porcelánico C2 · Dekton", "±0,00"))

    # 07. LAVANDERÍA TÉCNICA y DESPENSA (X=14.35..16.65, Y=12.15..14.40 → 5,60 m²)
    # Columna Lavadora + Secadora (0,65 x 0,65m) y Pila de lavar (0,60 x 0,55m)
    out.append(f'<rect x="{X(15.95):.1f}" y="{Y(12.22):.1f}" width="{L(0.65):.1f}" height="{L(0.65):.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.8"/>')
    out.append(f'<circle cx="{X(16.27):.1f}" cy="{Y(12.54):.1f}" r="7" fill="none" stroke="#38bdf8" stroke-width="0.6"/>')
    out.append(f'<text x="{X(16.27):.1f}" y="{Y(12.56):.1f}" fill="#cbd5e1" font-size="4.5" text-anchor="middle">LAV+SEC</text>')
    out.append(draw_sink_block(X(15.95), Y(12.92), L(0.65), L(0.65), basins=1, orient="E"))
    # Estanterías despensa 40cm fondo
    out.append(draw_wardrobe_block(X(14.40), Y(13.92), L(2.15), L(0.42), "DESPENSA 40cm"))
    out.append(draw_room_stamp(X(15.30), Y(13.25), "E-09", "LAVANDERÍA / DESP.", 5.60, "Porcelánico C2", "±0,00"))

    # 08. SALÓN PRINCIPAL CON CHIMENEA (X=6.50..12.20, Y=13.35..18.10 → 26,50 m²)
    # Muro Oeste de Granito Moreno + Chimenea Estanca Stûv 21 + TV OLED 77" enrasada
    out.append(f'<rect x="{X(6.50):.1f}" y="{Y(13.50):.1f}" width="{L(0.45):.1f}" height="{L(4.30):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.85"/>')
    # Hogar Chimenea estanca (1,00 x 0,45 m) con toma aire exterior Ø150
    out.append(f'<rect x="{X(6.52):.1f}" y="{Y(13.75):.1f}" width="{L(0.42):.1f}" height="{L(1.05):.1f}" fill="#1e293b" stroke="#ef4444" stroke-width="1.1"/>')
    out.append(f'<circle cx="{X(6.73):.1f}" cy="{Y(14.27):.1f}" r="5" fill="none" stroke="#f59e0b" stroke-width="0.9"/>')
    out.append(f'<text x="{X(7.08):.1f}" y="{Y(14.30):.1f}" fill="#fca5a5" font-size="5.2" font-weight="700">CHIMENEA ESTANCA Ø200/Ø150</text>')
    # Pantalla OLED 77" en hornacina (ancho 1,72 m)
    out.append(f'<rect x="{X(6.52):.1f}" y="{Y(15.30):.1f}" width="{L(0.12):.1f}" height="{L(1.72):.1f}" fill="#38bdf8"/>')
    out.append(f'<text x="{X(7.08):.1f}" y="{Y(16.15):.1f}" fill="#38bdf8" font-size="5.2" font-weight="700">TV OLED 77" (h=110cm)</text>')
    # Sofá modular en L (3,40 x 2,40 m) orientado a TV/Chimenea (Oeste) y Porche/Piscina (Sur)
    out.append(f'<path d="M {X(9.40):.1f} {Y(14.10):.1f} L {X(11.80):.1f} {Y(14.10):.1f} L {X(11.80):.1f} {Y(17.10):.1f} L {X(10.85):.1f} {Y(17.10):.1f} L {X(10.85):.1f} {Y(15.05):.1f} L {X(9.40):.1f} {Y(15.05):.1f} Z" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.95"/>')
    # Respaldo sofá
    out.append(f'<line x1="{X(9.40):.1f}" y1="{Y(14.32):.1f}" x2="{X(11.58):.1f}" y2="{Y(14.32):.1f}" stroke="#64748b" stroke-width="0.6"/>')
    out.append(f'<line x1="{X(11.58):.1f}" y1="{Y(14.32):.1f}" x2="{X(11.58):.1f}" y2="{Y(17.10):.1f}" stroke="#64748b" stroke-width="0.6"/>')
    # Mesa de centro de roble (1,40 x 0,80 m) y alfombra
    out.append(f'<rect x="{X(7.90):.1f}" y="{Y(14.40):.1f}" width="{L(2.75):.1f}" height="{L(2.60):.1f}" fill="none" stroke="#334155" stroke-width="0.5" stroke-dasharray="4,2"/>')
    out.append(f'<rect x="{X(8.90):.1f}" y="{Y(15.45):.1f}" width="{L(0.85):.1f}" height="{L(1.40):.1f}" fill="#131c31" stroke="#f59e0b" stroke-width="0.8"/>')
    out.append(f'<text x="{X(9.32):.1f}" y="{Y(16.18):.1f}" fill="#fde68a" font-size="5.2" text-anchor="middle">MESA 1,40x0,85</text>')
    # Cota visual de distancia ergonómica TV → Sofá (3,80 m)
    out.append(f'<line x1="{X(6.65):.1f}" y1="{Y(16.55):.1f}" x2="{X(10.85):.1f}" y2="{Y(16.55):.1f}" stroke="#38bdf8" stroke-width="0.55" stroke-dasharray="3,3" marker-end="url(#arrow-tech)"/>')
    out.append(f'<text x="{X(8.15):.1f}" y="{Y(16.48):.1f}" fill="#38bdf8" font-size="5.2">Dist. Visual TV = 3,80 m</text>')
    out.append(draw_nhg_circle(X(8.05), Y(17.35), 1.50, S, "Ø1,50m NHG"))
    out.append(draw_room_stamp(X(9.65), Y(17.45), "E-10", "SALÓN PRINCIPAL", 26.50, "Caliza Apomazada · H=2,80m", "±0,00"))

    # 09. COMEDOR PRINCIPAL 10 PAX (X=12.20..16.65, Y=14.40..18.10 → 17,50 m²)
    # Mesa de roble macizo 2,80 x 1,00 m con 10 sillas
    mx_c, my_c = X(12.80), Y(15.40)
    out.append(f'<rect x="{mx_c:.1f}" y="{my_c:.1f}" width="{L(2.80):.1f}" height="{L(1.00):.1f}" fill="#0f172a" stroke="#f8fafc" stroke-width="0.95"/>')
    for idx_s in range(4):
        sx = X(13.00 + idx_s * 0.62)
        out.append(f'<rect x="{sx:.1f}" y="{Y(15.16):.1f}" width="{L(0.42):.1f}" height="{L(0.20):.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.65"/>')
        out.append(f'<rect x="{sx:.1f}" y="{Y(16.44):.1f}" width="{L(0.42):.1f}" height="{L(0.20):.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.65"/>')
    out.append(f'<rect x="{X(12.56):.1f}" y="{Y(15.68):.1f}" width="{L(0.20):.1f}" height="{L(0.44):.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.65"/>')
    out.append(f'<rect x="{X(15.64):.1f}" y="{Y(15.68):.1f}" width="{L(0.20):.1f}" height="{L(0.44):.1f}" fill="#131c31" stroke="#94a3b8" stroke-width="0.65"/>')
    out.append(f'<text x="{X(14.20):.1f}" y="{Y(15.93):.1f}" fill="#f8fafc" font-size="5.8" font-weight="700" text-anchor="middle">MESA ROBLE 2,80x1,00m (10 PAX)</text>')
    # Aparador suspendido en pared Este (2,00 x 0,45 m)
    out.append(f'<rect x="{X(16.18):.1f}" y="{Y(14.90):.1f}" width="{L(0.45):.1f}" height="{L(2.00):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.75"/>')
    out.append(draw_room_stamp(X(14.35), Y(17.45), "E-11", "COMEDOR PRINCIPAL", 17.50, "Caliza Apomazada · 10 Pax", "±0,00"))
    out.append('</g>')

    # =========================================================================
    # CAPA 8: INSTALACIONES MEP EN PLANTA BAJA (VMC, SANEAMIENTO, ELECTRICIDAD)
    # =========================================================================
    out.append('<g id="instalaciones-mep-pb">')
    # Trazado de conductos principales VMC Zehnder Ø90mm desde Sala Técnica (X=5.74, Y=10.55)
    out.append(f'<polyline points="{X(5.74):.1f},{Y(10.55):.1f} {X(5.74):.1f},{Y(6.10):.1f} {X(15.80):.1f},{Y(6.10):.1f}" fill="none" stroke="#06b6d4" stroke-width="0.85" stroke-dasharray="6,3" opacity="0.8"/>')
    out.append(f'<polyline points="{X(5.74):.1f},{Y(10.55):.1f} {X(7.95):.1f},{Y(10.55):.1f} {X(7.95):.1f},{Y(14.00):.1f} {X(14.80):.1f},{Y(14.00):.1f}" fill="none" stroke="#10b981" stroke-width="0.85" stroke-dasharray="6,3" opacity="0.8"/>')
    # Bocas de Impulsión y Extracción VMC con caudales CTE DB-HS3
    out.append(draw_mep_symbol(X(5.65), Y(6.10), "vmc_ext", "VMC-E 30m³/h"))
    out.append(draw_mep_symbol(X(11.80), Y(6.10), "vmc_imp", "VMC-I 35m³/h"))
    out.append(draw_mep_symbol(X(15.80), Y(6.10), "vmc_ext", "VMC-E 50m³/h"))
    out.append(draw_mep_symbol(X(15.50), Y(9.20), "vmc_ext", "VMC-E 50m³/h"))
    out.append(draw_mep_symbol(X(15.50), Y(12.50), "vmc_ext", "VMC-E 30m³/h"))
    out.append(draw_mep_symbol(X(8.20), Y(14.00), "vmc_imp", "VMC-I 60m³/h"))
    out.append(draw_mep_symbol(X(13.50), Y(14.60), "vmc_imp", "VMC-I 40m³/h"))
    # Bajantes insonorizadas Geberit Silent-PP Ø110mm y termostatos
    out.append(draw_mep_symbol(X(16.45), Y(5.55), "drain", "BAJANTE B-01 Ø110"))
    out.append(draw_mep_symbol(X(7.00), Y(6.50), "drain", "BAJANTE B-02 Ø110 (de P1)"))
    out.append(draw_mep_symbol(X(9.60), Y(7.20), "thermostat", "T-PB1", 145))
    out.append(draw_mep_symbol(X(9.90), Y(7.20), "thermostat", "T-PB2", 145))
    out.append(draw_mep_symbol(X(12.60), Y(11.90), "thermostat", "T-PB3", 145))
    out.append(draw_mep_symbol(X(7.50), Y(13.55), "thermostat", "T-PB4", 145))
    out.append('</g>')

    # =========================================================================
    # CAPA 9: TEXTOS, COTAS ENCADENADAS, SECCIONES Y NORTE (id="textos-cotas-norte")
    # =========================================================================
    out.append('<g id="textos-cotas-norte">')
    # Líneas de Corte de Sección Longitudinal A-A' (X=10.50m) y Transversal B-B' (Y=10.40m)
    out.append(f'<line x1="{X(10.50):.1f}" y1="{Y(3.10):.1f}" x2="{X(10.50):.1f}" y2="{Y(27.20):.1f}" stroke="#f43f5e" stroke-width="0.8" stroke-dasharray="12,4,2,4" marker-start="url(#arrow-sec)" marker-end="url(#arrow-sec)"/>')
    out.append(f'<rect x="{X(10.50)-14:.1f}" y="{Y(2.75):.1f}" width="28" height="13" fill="#f43f5e"/><text x="{X(10.50):.1f}" y="{Y(2.75)+9.5:.1f}" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">A</text>')
    out.append(f'<rect x="{X(10.50)-14:.1f}" y="{Y(27.25):.1f}" width="28" height="13" fill="#f43f5e"/><text x="{X(10.50):.1f}" y="{Y(27.25)+9.5:.1f}" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">A\'</text>')

    out.append(f'<line x1="{X(0.60):.1f}" y1="{Y(10.40):.1f}" x2="{X(18.50):.1f}" y2="{Y(10.40):.1f}" stroke="#f43f5e" stroke-width="0.8" stroke-dasharray="12,4,2,4" marker-start="url(#arrow-sec)" marker-end="url(#arrow-sec)"/>')
    out.append(f'<rect x="{X(0.20):.1f}" y="{Y(10.40)-6.5:.1f}" width="22" height="13" fill="#f43f5e"/><text x="{X(0.20)+11:.1f}" y="{Y(10.40)+3:.1f}" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">B</text>')
    out.append(f'<rect x="{X(18.55):.1f}" y="{Y(10.40)-6.5:.1f}" width="22" height="13" fill="#f43f5e"/><text x="{X(18.55)+11:.1f}" y="{Y(10.40)+3:.1f}" fill="#ffffff" font-size="7.5" font-weight="700" text-anchor="middle">B\'</text>')

    # TRIPLE CADENA DE ACOTACIÓN SUPERIOR (NORTE)
    # Línea 1: Cotas parciales de estancias y huecos (Y = 3.15 m)
    out.append(draw_dim_h(X(0.00), X(3.85), Y(5.00), Y(3.15), "3,85 (Pérgola)", S, "#38bdf8"))
    out.append(draw_dim_h(X(3.85), X(6.15), Y(5.00), Y(3.15), "2,30 (Zaguán)", S, "#38bdf8"))
    out.append(draw_dim_h(X(6.15), X(9.75), Y(5.00), Y(3.15), "3,60 (Hall)", S, "#38bdf8"))
    out.append(draw_dim_h(X(9.75), X(13.65), Y(5.00), Y(3.15), "3,90 (Despacho)", S, "#38bdf8"))
    out.append(draw_dim_h(X(13.65), X(17.00), Y(5.00), Y(3.15), "3,35 (Baño PB)", S, "#38bdf8"))
    out.append(draw_dim_h(X(17.00), X(20.00), Y(5.00), Y(3.15), "3,00 (Retr. E)", S, "#f59e0b", "tick-45-amber"))

    # Línea 2: Cotas de volumen edificado (Y = 2.25 m)
    out.append(draw_dim_h(X(0.00), X(3.85), Y(3.15), Y(2.25), "3,85 m Lindero W", S, "#cbd5e1", "tick-45-white"))
    out.append(draw_dim_h(X(3.85), X(17.00), Y(3.15), Y(2.25), "13,15 m (Ancho Total Edificación PB)", S, "#cbd5e1", "tick-45-white"))
    out.append(draw_dim_h(X(17.00), X(20.00), Y(3.15), Y(2.25), "3,00 m Lindero E", S, "#cbd5e1", "tick-45-white"))

    # Línea 3: Cota Total de Parcela Norte (Y = 1.40 m)
    out.append(draw_dim_h(X(0.00), X(20.00), Y(2.25), Y(1.40), "20,00 m (FRENTE PARCELA AL VIAL NORTE)", S, "#f59e0b", "tick-45-amber", font_size=8.5))

    # TRIPLE CADENA DE ACOTACIÓN IZQUIERDA (OESTE)
    # Línea 1: Cotas parciales eje Y (X = -0.65 m)
    out.append(draw_dim_v(Y(0.00), Y(5.00), X(0.00), X(-0.65), "5,00 (Retr. N)", S, "#f59e0b", "tick-45-amber"))
    out.append(draw_dim_v(Y(5.00), Y(8.40), X(3.85), X(-0.65), "3,40 (Banda N)", S, "#38bdf8"))
    out.append(draw_dim_v(Y(8.40), Y(12.40), X(3.85), X(-0.65), "4,00 (Claustro)", S, "#38bdf8"))
    out.append(draw_dim_v(Y(12.40), Y(18.45), X(6.15), X(-0.65), "6,05 (Salón/Com)", S, "#38bdf8"))
    out.append(draw_dim_v(Y(18.45), Y(21.45), X(6.15), X(-0.65), "3,00 (Porche Sur)", S, "#38bdf8"))
    out.append(draw_dim_v(Y(21.45), Y(30.00), X(0.00), X(-0.65), "8,55 (Jardín/Pisc)", S, "#10b981"))

    # Línea 2: Cota Total Fondo Parcela (X = -1.55 m)
    out.append(draw_dim_v(Y(0.00), Y(30.00), X(-0.65), X(-1.55), "30,00 m (FONDO TOTAL PARCELA NORTE-SUR · 600,00 m²)", S, "#f59e0b", "tick-45-amber", font_size=8.5))

    # Cotas interiores del Patio Corrala y Piscina
    out.append(draw_dim_h(X(8.50), X(12.50), Y(12.40), Y(12.85), "4,00 m (Patio Corrala)", S, "#10b981"))
    out.append(draw_dim_h(X(8.50), X(16.00), Y(26.50), Y(27.05), "7,50 m (Lámina Agua Piscina)", S, "#38bdf8"))
    out.append(draw_dim_v(Y(23.00), Y(26.50), X(16.00), X(16.50), "3,50 m", S, "#38bdf8"))

    # Rosa de los vientos y escala gráfica (arriba a la derecha del plano)
    out.append(draw_north_rose_and_scale(X(18.50), Y(2.20), scale_px_per_m=S, scale_label="1:100"))
    out.append('</g>')

    # =========================================================================
    # PANEL TÉCNICO LATERAL DERECHO: CUADRO DE SUPERFICIES, LEYENDA Y PARÁMETROS
    # =========================================================================
    px_panel = 955.0
    pw_panel = 515.0
    out.append(f'<g id="panel-tecnico-derecho" transform="translate({px_panel}, 35)">')
    out.append(f'<rect x="0" y="0" width="{pw_panel}" height="1235" fill="#090e1a" stroke="#64748b" stroke-width="1.2"/>')

    # Encabezado de panel
    out.append('<rect x="0" y="0" width="515" height="34" fill="#131c31" stroke="#64748b" stroke-width="0.8"/>')
    out.append('<text x="257" y="15" fill="#38bdf8" font-size="9.5" font-weight="700" text-anchor="middle">CUADRO DE SUPERFICIES Y PARÁMETROS URBANÍSTICOS (PLANTA BAJA)</text>')
    out.append('<text x="257" y="27" fill="#94a3b8" font-size="6.8" text-anchor="middle">Concello de Oleiros (Liáns / Santa Cruz) · PGOM Ordenanza 2B · Decreto 29/2010 NHG</text>')

    # Tabla 1: Verificación Urbanística PGOM 2B
    out.append('<text x="14" y="52" fill="#f59e0b" font-size="8" font-weight="700">1. VERIFICACIÓN DE CUMPLIMIENTO URBANÍSTICO (PGOM OLEIROS ORD. 2B)</text>')
    urb_rows = [
        ("Superficie Neta de Parcela (20,00 × 30,00 m)", "600,00 m²", "Mín. 500 m²", "CUMPLE"),
        ("Ocupación Máxima Permitida en PB (20,00 %)", "120,00 m²", "Máx. 20,0 %", "LÍMITE"),
        ("Huella Cerrada Real en Planta Baja (Propuesta D)", "116,50 m²", "19,42 % ≤ 20%", "CUMPLE"),
        ("Retranqueo Frontal al Vial Norte", "5,00 m", "Mín. 5,00 m", "CUMPLE"),
        ("Retranqueos a Linderos Laterales (Este / Oeste)", "3,00 / 3,85 m", "Mín. 3,00 m", "CUMPLE"),
        ("Retranqueo Posterior Sur (Jardín y Piscina)", "11,55 m", "Mín. 3,00 m", "CUMPLE"),
        ("Altura de Cierre Opaco / Vegetal", "2,00 m", "Máx. 2,00 m", "CUMPLE"),
    ]
    y_t = 62
    out.append(f'<rect x="14" y="{y_t}" width="487" height="16" fill="#1e293b" stroke="#475569" stroke-width="0.6"/>')
    out.append(f'<text x="20" y="{y_t+11}" fill="#cbd5e1" font-size="6.5" font-weight="700">PARÁMETRO URBANÍSTICO</text>')
    out.append(f'<text x="290" y="{y_t+11}" fill="#cbd5e1" font-size="6.5" font-weight="700">PROYECTO</text>')
    out.append(f'<text x="375" y="{y_t+11}" fill="#cbd5e1" font-size="6.5" font-weight="700">NORMATIVA</text>')
    out.append(f'<text x="455" y="{y_t+11}" fill="#cbd5e1" font-size="6.5" font-weight="700">ESTADO</text>')
    for idx, (p_nam, p_val, p_norm, p_st) in enumerate(urb_rows):
        yr = y_t + 16 + idx * 16
        out.append(f'<rect x="14" y="{yr}" width="487" height="16" fill="none" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="20" y="{yr+11}" fill="#e2e8f0" font-size="6.3">{p_nam}</text>')
        out.append(f'<text x="290" y="{yr+11}" fill="#38bdf8" font-size="6.5" font-weight="700">{p_val}</text>')
        out.append(f'<text x="375" y="{yr+11}" fill="#94a3b8" font-size="6.3">{p_norm}</text>')
        out.append(f'<text x="455" y="{yr+11}" fill="#10b981" font-size="6.3" font-weight="700">{p_st}</text>')

    # Tabla 2: Desglose de Superficies de Planta Baja
    y_t2 = 205
    out.append(f'<text x="14" y="{y_t2}" fill="#38bdf8" font-size="8" font-weight="700">2. CUADRO DE SUPERFICIES ÚTILES Y ACABADOS — PLANTA BAJA (COTA ±0,00 m)</text>')
    pb_rooms = [
        ("E-03", "01. Zaguán Atlántico / Mudroom Térmico", "5,80 m²", "Porcelánico C3 Pizarra", "±0,00 m"),
        ("E-04", "02. Hall / Recibidor Principal", "10,40 m²", "Roble Multicapa 14 mm", "±0,00 m"),
        ("E-05", "03. Despacho Sanctasanctórum / Suite Visitas", "11,50 m²", "Roble 14 mm + Lamas Acúst.", "±0,00 m"),
        ("E-06", "04. Baño Completo PB + Distribuidor Neutro", "5,20 m²", "Porcelánico C3 + Kerdi", "±0,00 m"),
        ("E-08", "06. Cocina con Isla Santos Fine + Desayunador", "15,20 m²", "Porcelánico C2 120×60", "±0,00 m"),
        ("E-09", "07. Lavandería Técnica y Despensa", "5,60 m²", "Porcelánico C2 Técnico", "±0,00 m"),
        ("E-10", "08. Salón Principal con Chimenea Estanca", "26,50 m²", "Caliza Natural Apomazada", "±0,00 m"),
        ("E-11", "09. Comedor Principal Interior (10 Pax)", "17,50 m²", "Caliza Natural Apomazada", "±0,00 m"),
        ("E-12", "10. Escalera Volada Roble 80mm (17 Peldaños)", "5,20 m²", "Roble Macizo 80 mm", "±0,00/+3,15"),
        ("E-13", "11. Trastero Surf/Bicis y Sala Técnica Passivhaus", "8,20 m²", "Hormigón Pulido Epoxi", "-0,05 m"),
        ("SUB-1", "TOTAL SUPERFICIE ÚTIL INTERIOR PLANTA BAJA", "98,90 m²", "(Construida cerrada: 116,50 m²)", ""),
        ("E-01", "Pérgola Cubierta Aparcamiento (2 Vehículos)", "28,00 m²", "Adoquín Drenante Granito", "-0,10 m"),
        ("E-02", "Porche Entrada Peatonal Noble Norte", "3,50 m²", "Granito Abujardado C3", "+0,05 m"),
        ("E-07", "05. Patio Corrala Central Habitable (Abierto)", "16,00 m²", "Tarima Iroko s/ Plots", "±0,00 m"),
        ("E-14", "10. Porche Sur Expandido Techado (Fondo 3,00 m)", "36,00 m²", "Tarima Iroko Cota Cero", "±0,00 m"),
        ("E-15", "11. Piscina Privada Soleada (7,50 × 3,50 m)", "26,25 m²", "Gresite Porcelánico Arena", "-1,20/-1,50"),
    ]
    yr0 = y_t2 + 10
    out.append(f'<rect x="14" y="{yr0}" width="487" height="16" fill="#1e293b" stroke="#475569" stroke-width="0.6"/>')
    out.append(f'<text x="20" y="{yr0+11}" fill="#cbd5e1" font-size="6.3" font-weight="700">ID</text>')
    out.append(f'<text x="62" y="{yr0+11}" fill="#cbd5e1" font-size="6.3" font-weight="700">ESTANCIA / ZONA FUNCIONAL</text>')
    out.append(f'<text x="275" y="{yr0+11}" fill="#cbd5e1" font-size="6.3" font-weight="700">SUP. ÚTIL</text>')
    out.append(f'<text x="335" y="{yr0+11}" fill="#cbd5e1" font-size="6.3" font-weight="700">PAVIMENTO / ACABADO</text>')
    out.append(f'<text x="455" y="{yr0+11}" fill="#cbd5e1" font-size="6.3" font-weight="700">COTA Z</text>')
    for idx, (cid, cnam, csup, cpav, cz) in enumerate(pb_rooms):
        yr = yr0 + 16 + idx * 16.5
        is_sub = cid == "SUB-1"
        bg = "#131c31" if is_sub else "none"
        col_txt = "#f59e0b" if is_sub else "#e2e8f0"
        out.append(f'<rect x="14" y="{yr:.1f}" width="487" height="16.5" fill="{bg}" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="20" y="{yr+11.5:.1f}" fill="#38bdf8" font-size="6.2" font-weight="700">{cid}</text>')
        out.append(f'<text x="62" y="{yr+11.5:.1f}" fill="{col_txt}" font-size="6.2" font-weight="{"700" if is_sub else "400"}">{cnam}</text>')
        out.append(f'<text x="275" y="{yr+11.5:.1f}" fill="{col_txt}" font-size="6.5" font-weight="700">{csup}</text>')
        out.append(f'<text x="335" y="{yr+11.5:.1f}" fill="#94a3b8" font-size="6.0">{cpav}</text>')
        out.append(f'<text x="455" y="{yr+11.5:.1f}" fill="#cbd5e1" font-size="6.0">{cz}</text>')

    # Tabla 3: Cuadro de Carpinterías de Planta Baja (C-01 a C-09)
    y_t3 = 515
    out.append(f'<text x="14" y="{y_t3}" fill="#10b981" font-size="8" font-weight="700">3. CUADRO DE CARPINTERÍAS EXTERIORES E INTERIORES (PLANTA BAJA)</text>')
    carp_rows = [
        ("C-01", "Porche Norte → Hall", "Pivotante Eje Despl.", "1,00 × 2,40 m", "h=0 cm", "Iroko Macizo 70mm (Ud=1,1)"),
        ("C-02", "Pérgola → Mudroom", "Batiente 1H Hermética", "0,90 × 2,10 m", "h=0 cm", "Cortizo COR 80 RPT + Guillotina"),
        ("C-03", "Despacho Norte", "Oscilobatiente 2H", "1,80 × 1,20 m", "h=95 cm", "COR 80 RPT · 4+4Sil/16Ar/4/16Ar/4"),
        ("C-04", "Baño PB Norte", "Oscilobatiente 1H", "0,80 × 0,60 m", "h=160 cm", "COR 80 RPT · Vidrio Mate"),
        ("C-05", "Hall/Desp. → Patio", "Fijo Suelo a Techo", "4,00 × 2,60 m", "h=0 cm", "Cortizo Cor Vision Plus Oculto"),
        ("C-06", "Cocina/Salón → Patio", "Corredera Elevable 2H", "3,00 × 2,60 m", "h=0 cm", "Cor Vision Plus · Enrasado Purenit"),
        ("C-07", "Salón → Porche Sur", "Corredera Elevable 3H", "5,00 × 2,60 m", "h=0 cm", "Cor Vision Plus · Triple Vidrio"),
        ("C-08", "Comedor → Porche Sur", "Corredera Elevable 2H", "3,50 × 2,60 m", "h=0 cm", "Cor Vision Plus · Triple Vidrio"),
        ("C-09", "Trastero / Técnica", "Batiente Reforzada", "0,90 × 2,05 m", "h=0 cm", "Acero Galv. Termolacado RPT"),
        ("P-03", "Hall → Despacho", "Batiente Isofónica", "0,82 × 2,10 m", "h=0 cm", "Madera Maciza Acústica Rw≥38dB"),
    ]
    yr3 = y_t3 + 10
    out.append(f'<rect x="14" y="{yr3}" width="487" height="16" fill="#1e293b" stroke="#475569" stroke-width="0.6"/>')
    out.append(f'<text x="18" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">CÓD.</text>')
    out.append(f'<text x="55" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">UBICACIÓN</text>')
    out.append(f'<text x="148" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">APERTURA</text>')
    out.append(f'<text x="238" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">DIMENSIÓN</text>')
    out.append(f'<text x="302" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">ANTEP.</text>')
    out.append(f'<text x="348" y="{yr3+11}" fill="#cbd5e1" font-size="6.2" font-weight="700">SERIE Y VIDRIO</text>')
    for idx, (cc, cub, cap, cdim, cant, cser) in enumerate(carp_rows):
        yr = yr3 + 16 + idx * 16
        out.append(f'<rect x="14" y="{yr}" width="487" height="16" fill="none" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="18" y="{yr+11}" fill="#f59e0b" font-size="6.2" font-weight="700">{cc}</text>')
        out.append(f'<text x="55" y="{yr+11}" fill="#e2e8f0" font-size="6.0">{cub}</text>')
        out.append(f'<text x="148" y="{yr+11}" fill="#94a3b8" font-size="6.0">{cap}</text>')
        out.append(f'<text x="238" y="{yr+11}" fill="#38bdf8" font-size="6.2" font-weight="700">{cdim}</text>')
        out.append(f'<text x="302" y="{yr+11}" fill="#cbd5e1" font-size="6.0">{cant}</text>')
        out.append(f'<text x="348" y="{yr+11}" fill="#94a3b8" font-size="5.8">{cser}</text>')

    # Bloque 4: Leyenda gráfica de simbología CAD y muros
    y_t4 = 720
    out.append(f'<text x="14" y="{y_t4}" fill="#38bdf8" font-size="8" font-weight="700">4. LEYENDA DE SIMBOLOGÍA TÉCNICA CAD E INSTALACIONES</text>')
    out.append(f'<rect x="14" y="{y_t4+10}" width="487" height="175" fill="#0b1120" stroke="#475569" stroke-width="0.7"/>')
    # Muestras de muro en leyenda
    out.append(draw_wall_segment(26, y_t4 + 24, 55, 14, "ext"))
    out.append(f'<text x="92" y="{y_t4+34}" fill="#e2e8f0" font-size="6.2">Muro Cerramiento Fachada (35 cm): Termoarcilla 19cm + SATE Lana Roca 12cm (U=0,21 W/m²K)</text>')
    out.append(draw_wall_segment(26, y_t4 + 48, 55, 6, "acoustic"))
    out.append(f'<text x="92" y="{y_t4+54}" fill="#e2e8f0" font-size="6.2">Tabique Acústico Interior (12 cm): Doble placa Pladur Fonic + Lana mineral 50mm (Rw≥45 dB)</text>')
    out.append(draw_pillar(52, y_t4 + 74, 10, "P-XX"))
    out.append(f'<text x="92" y="{y_t4+77}" fill="#e2e8f0" font-size="6.2">Pilar Estructural HA-25 / HEB-160 (25×25 cm) en intersección de ejes de replanteo</text>')
    # Símbolos MEP en leyenda
    out.append(draw_mep_symbol(38, y_t4 + 100, "vmc_imp", "Boca Impulsión VMC Zehnder Ø125 (Aire Nuevo Filtrado F7)"))
    out.append(draw_mep_symbol(275, y_t4 + 100, "vmc_ext", "Boca Extracción VMC Ø125 (Aire Viciado)"))
    out.append(draw_mep_symbol(38, y_t4 + 122, "thermostat", "Termostato Táctil Suelo Radiante (h=145 cm)"))
    out.append(draw_mep_symbol(275, y_t4 + 122, "drain", "Bajante / Sumidero Sifónico Geberit Silent-PP Ø110"))
    out.append(draw_nhg_circle(38, y_t4 + 155, 0.55, S, ""))
    out.append(f'<text x="65" y="{y_t4+158}" fill="#10b981" font-size="6.2" font-weight="700">Círculo Libre de Inscripción Ø1,50 m (Cumplimiento Decreto 29/2010 Normas do Hábitat Galego)</text>')

    # Bloque 5: Notas Constructivas de Obligado Cumplimiento en Obra
    y_t5 = 925
    out.append(f'<text x="14" y="{y_t5}" fill="#f43f5e" font-size="8" font-weight="700">5. PRESCRIPCIONES TÉCNICAS OBLIGATORIAS DE EJECUCIÓN EN OBRA</text>')
    out.append(f'<rect x="14" y="{y_t5+10}" width="487" height="285" fill="#0b1120" stroke="#475569" stroke-width="0.7"/>')
    notas = [
        "1. BARRERA ANTI-RADÓN (CTE DB-HS6 ZONA II OLEIROS): Lámina elastomérica continua de e ≥ 2,0 mm",
        "   (D ≤ 10^-11 m²/s) bajo solera con solapes de 15 cm termosoldados y pasamuros sellados con manguito.",
        "2. ENRASADO COTA CERO SIN PUENTE TÉRMICO: Todos los carriles inferiores de correderas Cortizo Cor Vision",
        "   Plus descansan sobre premarco térmico de Purenit de 50 mm y canaleta lineal oculta inox AISI 316.",
        "3. PATIO CORRALA ABIERTO AL CIELO: Prohibido cerrar el patio con lucernarios (elimina sobrecalentamiento).",
        "   Pendiente del 1,5% bajo tarima de Iroko sobre plots hacia 2 sumideros sifónicos pluviales Ø110 mm.",
        "4. CHIMENEA ESTANCA PASSIVHAUS: Hogar cerrado Stûv 21 con conducto de admisión de aire exterior Ø150 mm",
        "   bajo solera. Garantiza estanqueidad BlowerDoor (n50 ≤ 1,0 h^-1) sin interferir con la VMC Zehnder.",
        "5. EXTRACCIÓN DE COCINA BORA PURE: Conducto plano insonorizado Bora Ecotube embutido por cámara",
        "   sanitaria hacia compuerta mural motorizada estanca en fachada. Circuito eléctrico dedicado C3 (6 mm²).",
        "6. INDEPENDENCIA DEL BAÑO PB (NHG GALICIA): El Baño E-06 cuenta con distribuidor neutro previo y doble",
        "   puerta (P-05 y P-06) respecto a la cocina y comedor, cumpliendo estrictamente el Decreto 29/2010.",
    ]
    for idx_n, n_line in enumerate(notas):
        col_n = "#f8fafc" if n_line[0].isdigit() else "#94a3b8"
        fw_n = "700" if n_line[0].isdigit() else "400"
        out.append(f'<text x="22" y="{y_t5 + 28 + idx_n*21}" fill="{col_n}" font-size="6.1" font-weight="{fw_n}">{n_line}</text>')
    out.append('</g>')

    # =========================================================================
    # CAJETÍN TÉCNICO NORMALIZADO ISO 7200 (PIE DE PLANO)
    # =========================================================================
    out.append(
        draw_iso_title_block(
            x=30, y=1365, w=1440, h=65,
            sheet_num="A-01",
            sheet_title="PLANTA BAJA GENERAL (COTA ±0,00 m) E IMPLANTACIÓN",
            scale_txt="ESCALA 1:100 (1m=40px)",
            subtitle="Replanteo Estructural, Albañilería, Carpinterías, Mobiliario NHG y Red VMC",
            summary_rows=[
                "• Parcela Neta: 600,00 m² (20,00 × 30,00 m) · Huella Cerrada PB: 116,50 m² (19,42% ≤ 20% PGOM)",
                "• Superficie Útil Interior PB: 98,90 m² · Patio Corrala Central: 16,00 m² · Porche Sur: 36,00 m²",
                "• Cota Interior y Porches: ±0,00 m (enrasado continuo) · Altura libre interior: 2,65 m / 2,80 m (Salón)",
                "• Sistema coordenadas: Origen (0,0) esquina NW parcela · Ejes estructurales A-E / 1-5",
            ],
        )
    )

    out.append("</svg>")
    return "\n".join(out)


def build_planta_alta_svg():
    """
    Construye el Plano Técnico A-02: Planta Primera General (+3,15 m) y Cubiertas Técnicas Inferiores.
    """
    W_SVG, H_SVG = 1500, 1220
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_SVG} {H_SVG}" width="100%" height="100%" '
        f'style="background-color: #070b14; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;">',
        cad_defs(),
        f'<rect x="12" y="12" width="{W_SVG - 24}" height="{H_SVG - 24}" fill="#0b1120" stroke="#94a3b8" stroke-width="1.8"/>',
        f'<rect x="20" y="20" width="{W_SVG - 40}" height="{H_SVG - 40}" fill="url(#cad-grid-major)" stroke="#cbd5e1" stroke-width="0.9"/>',
    ]

    # Usando factor de escala 1m = 52px para Planta Primera para máximo nivel de detalle en la lámina
    S1 = 52.0
    OX1 = 75.0
    OY1 = -130.0

    def X1(m):
        return OX1 + m * S1

    def Y1(m):
        return OY1 + m * S1

    def L1(m):
        return m * S1

    # =========================================================================
    # CAPA 1: EJES ESTRUCTURALES Y CUBIERTAS TÉCNICAS INFERIORES (id="parcela-y-retranqueos")
    # =========================================================================
    out.append('<g id="parcela-y-retranqueos">')
    v_axes = [(4.00, "A"), (6.15, "B"), (8.50, "C"), (12.50, "D"), (17.00, "E")]
    for xm, lbl in v_axes:
        out.append(draw_structural_axis(X1(xm), Y1(3.8), X1(xm), Y1(20.2), lbl, bubble_at="start"))
    h_axes = [(5.00, "1"), (8.40, "2"), (12.40, "3"), (16.50, "3B"), (18.45, "4")]
    for ym, lbl in h_axes:
        out.append(draw_structural_axis(X1(0.6), Y1(ym), X1(17.8), Y1(ym), lbl, bubble_at="start"))

    # Cubierta plana técnica sobre Pérgola y Trastero (X=1.00..6.15, Y=5.00..12.40) con 12 paneles solares FV
    out.append(f'<rect x="{X1(1.00):.1f}" y="{Y1(5.00):.1f}" width="{L1(5.15):.1f}" height="{L1(7.40):.1f}" fill="url(#hatch-gravel)" stroke="#64748b" stroke-width="1.0" stroke-dasharray="6,3"/>')
    out.append(f'<text x="{X1(3.55):.1f}" y="{Y1(5.45):.1f}" fill="#94a3b8" font-size="6.8" font-weight="700" text-anchor="middle">CUBIERTA PLANA TÉCNICA NO TRANSITABLE (GRAVA DRENANTE · COTA +3,05 m)</text>')
    # 12 Paneles Fotovoltaicos Monocristalinos (1,75 x 1,10 m cada uno → 5,40 kWp)
    for row_i in range(4):
        for col_j in range(3):
            px_pv = X1(1.35 + col_j * 1.48)
            py_pv = Y1(5.80 + row_i * 1.35)
            out.append(f'<rect x="{px_pv:.1f}" y="{py_pv:.1f}" width="{L1(1.32):.1f}" height="{L1(1.05):.1f}" fill="#0c192c" stroke="#38bdf8" stroke-width="0.75"/>')
            out.append(f'<line x1="{px_pv:.1f}" y1="{py_pv + L1(0.52):.1f}" x2="{px_pv + L1(1.32):.1f}" y2="{py_pv + L1(0.52):.1f}" stroke="#1e3a8a" stroke-width="0.4"/>')
            out.append(f'<text x="{px_pv + L1(0.66):.1f}" y="{py_pv + L1(0.58):.1f}" fill="#7dd3fc" font-size="4.8" text-anchor="middle">FV-{row_i*3+col_j+1:02d} 450W</text>')
    # Cazoletas pluviales y líneas de pendiente de cubierta
    out.append(draw_mep_symbol(X1(1.30), Y1(12.00), "drain", "CAZ-01 Ø90 (p=2%)"))
    out.append(draw_mep_symbol(X1(5.80), Y1(12.00), "drain", "CAZ-02 Ø90 (p=2%)"))
    out.append('</g>')

    # =========================================================================
    # CAPA 2: PAVIMENTOS DE PLANTA PRIMERA Y VACÍO CENTRAL DEL PATIO CORRALA
    # =========================================================================
    out.append('<g id="pavimentos-p1">')
    # Huella interior Planta Primera: X=[6.15..17.00], Y=[5.00..16.50]
    out.append(f'<rect x="{X1(6.15):.1f}" y="{Y1(5.00):.1f}" width="{L1(10.85):.1f}" height="{L1(11.50):.1f}" fill="url(#hatch-wood-deck)"/>')
    out.append(f'<rect x="{X1(6.35):.1f}" y="{Y1(5.35):.1f}" width="{L1(10.35):.1f}" height="{L1(10.85):.1f}" fill="url(#hatch-radiant)" opacity="0.45"/>')

    # Vacío Cenital del Patio Corrala Central: X=[8.50..12.50], Y=[8.40..12.40] (4,00 x 4,00 m)
    out.append(f'<rect x="{X1(8.50):.1f}" y="{Y1(8.40):.1f}" width="{L1(4.00):.1f}" height="{L1(4.00):.1f}" fill="#070b14" stroke="#10b981" stroke-width="1.4"/>')
    # Líneas diagonales técnicas de vacío / doble altura
    out.append(f'<line x1="{X1(8.50):.1f}" y1="{Y1(8.40):.1f}" x2="{X1(12.50):.1f}" y2="{Y1(12.40):.1f}" stroke="#10b981" stroke-width="0.6" stroke-dasharray="6,4" opacity="0.6"/>')
    out.append(f'<line x1="{X1(12.50):.1f}" y1="{Y1(8.40):.1f}" x2="{X1(8.50):.1f}" y2="{Y1(12.40):.1f}" stroke="#10b981" stroke-width="0.6" stroke-dasharray="6,4" opacity="0.6"/>')
    # Proyección de alero perimetral de 80 cm y copa del Arce Japonés inferior
    out.append(f'<rect x="{X1(9.30):.1f}" y="{Y1(9.20):.1f}" width="{L1(2.40):.1f}" height="{L1(2.40):.1f}" fill="none" stroke="#34d399" stroke-width="0.7" stroke-dasharray="3,3"/>')
    out.append(f'<circle cx="{X1(9.55):.1f}" cy="{Y1(9.55):.1f}" r="{L1(0.65):.1f}" fill="none" stroke="#10b981" stroke-width="0.8" stroke-dasharray="2,2"/>')
    out.append(f'<text x="{X1(10.50):.1f}" y="{Y1(10.30):.1f}" fill="#10b981" font-size="7.5" font-weight="700" text-anchor="middle">VACÍO PATIO CORRALA (4,00 × 4,00 m)</text>')
    out.append(f'<text x="{X1(10.50):.1f}" y="{Y1(10.60):.1f}" fill="#6ee7b7" font-size="6.0" text-anchor="middle">Abierto al cielo · Proyección copa Acer palmatum</text>')

    # 19. BALCÓN CORRIDO SUR P1: X=[6.15..17.00], Y=[16.50..17.90] (Fondo 1,40 m · 14,00 m² útiles)
    out.append(f'<rect x="{X1(6.15):.1f}" y="{Y1(16.50):.1f}" width="{L1(10.85):.1f}" height="{L1(1.40):.1f}" fill="url(#hatch-wood-deck)" stroke="#38bdf8" stroke-width="1.1"/>')
    # Barandilla continua de vidrio estructural laminar 10+10.2 mm en borde Sur (Y=17.90)
    out.append(f'<line x1="{X1(6.15):.1f}" y1="{Y1(17.86):.1f}" x2="{X1(17.00):.1f}" y2="{Y1(17.86):.1f}" stroke="#38bdf8" stroke-width="2.2"/>')
    out.append(f'<line x1="{X1(6.15):.1f}" y1="{Y1(17.92):.1f}" x2="{X1(17.00):.1f}" y2="{Y1(17.92):.1f}" stroke="#e2e8f0" stroke-width="0.6"/>')
    # Proyección del vuelo inferior del Porche Sur de PB (Y=17.90..21.45)
    out.append(f'<rect x="{X1(6.15):.1f}" y="{Y1(17.90):.1f}" width="{L1(10.85):.1f}" height="{L1(2.10):.1f}" fill="none" stroke="#475569" stroke-width="0.8" stroke-dasharray="6,4"/>')
    out.append(f'<text x="{X1(11.57):.1f}" y="{Y1(19.10):.1f}" fill="#64748b" font-size="6.5" text-anchor="middle">PROYECCIÓN CUBIERTA PORCHE SUR INFERIOR (COTA +3,00 m · PENDIENTE 1,5%)</text>')
    out.append(draw_room_stamp(X1(11.57), Y1(17.20), "E-23", "BALCÓN CORRIDO SUR P1", 14.00, "Iroko · Vidrio 10+10mm", "+3,15"))
    out.append('</g>')

    # =========================================================================
    # CAPA 3: MUROS EXTERIORES DE PLANTA PRIMERA (id="muros-exteriores")
    # =========================================================================
    out.append('<g id="muros-exteriores">')
    wt = L1(0.35)
    # Fachada Norte P1 (Y=5.00, X=6.15..17.00) con huecos C-10 (Baño Hijos) y C-11 (Baño Suite)
    out.append(draw_wall_segment(X1(6.15), Y1(5.00), L1(1.85), wt, "ext"))   # Hasta C-10 (X=8.00..9.20)
    out.append(draw_wall_segment(X1(9.20), Y1(5.00), L1(5.00), wt, "ext"))   # Tramo central hasta C-11 (X=14.20..15.60)
    out.append(draw_wall_segment(X1(15.60), Y1(5.00), L1(1.40), wt, "ext"))  # Esquina NE

    # Fachada Oeste P1 (X=6.15, Y=5.00..16.50) — Ciega para aislamiento térmico/acústico
    out.append(draw_wall_segment(X1(6.15), Y1(5.00), wt, L1(11.50), "ext"))

    # Fachada Este P1 (X=16.65, Y=5.00..16.50) — Ciega de alta inercia
    out.append(draw_wall_segment(X1(16.65), Y1(5.00), wt, L1(11.50), "ext"))

    # Fachada Sur P1 hacia Balcón Corrido (Y=16.15..16.50, X=6.15..17.00) con huecos C-12, C-13, C-14
    out.append(draw_wall_segment(X1(6.15), Y1(16.15), L1(0.85), wt, "ext"))   # Machón SW hasta C-12 (X=7.00..9.20)
    out.append(draw_wall_segment(X1(9.20), Y1(16.15), L1(1.15), wt, "ext"))   # Machón entre C-12 y C-13 (X=10.35..12.55)
    out.append(draw_wall_segment(X1(12.55), Y1(16.15), L1(0.85), wt, "ext"))  # Machón entre C-13 y C-14 (X=13.40..16.40)
    out.append(draw_wall_segment(X1(16.40), Y1(16.15), L1(0.60), wt, "ext"))  # Machón SE

    # Muros perimetrales del Claustro en Norte y Este (X=8.50..12.50, Y=8.40..12.40)
    out.append(draw_wall_segment(X1(8.50), Y1(8.15), L1(4.00), L1(0.25), "ext"))
    out.append(draw_wall_segment(X1(12.50), Y1(8.15), L1(0.25), L1(4.25), "ext"))

    # Pilares estructurales P1
    for px_m, py_m, plbl in [
        (6.32, 5.17, "P-02"), (8.50, 5.17, "P-03"), (12.50, 5.17, "P-04"), (16.82, 5.17, "P-05"),
        (6.32, 8.40, "P-07"), (8.50, 8.40, "P-08"), (12.50, 8.40, "P-09"), (16.82, 8.40, "P-10"),
        (6.32, 12.40, "P-12"), (8.50, 12.40, "P-13"), (12.50, 12.40, "P-14"), (16.82, 12.40, "P-15"),
        (6.32, 16.32, "P-16"), (9.80, 16.32, "P-17A"), (13.00, 16.32, "P-17B"), (16.82, 16.32, "P-18"),
    ]:
        out.append(draw_pillar(X1(px_m), Y1(py_m), size_px=10, label=plbl))
    out.append('</g>')

    # =========================================================================
    # CAPA 4: TABIQUERÍA INTERIOR P1 E INDEPENDENCIA ACÚSTICA (id="tabiqueria-interior")
    # =========================================================================
    out.append('<g id="tabiqueria-interior">')
    pt = L1(0.12)
    # 15. Baño Compartido Hijos (X=6.50..12.50, Y=5.35..8.15): cierre sur y este
    out.append(draw_wall_segment(X1(6.50), Y1(8.15), L1(2.00), pt, "int"))
    out.append(draw_wall_segment(X1(12.50), Y1(5.35), pt, L1(2.80), "acoustic"))

    # 18. Baño Privado Suite (X=12.65..16.65, Y=5.35..7.55)
    out.append(draw_wall_segment(X1(12.65), Y1(7.55), L1(4.00), pt, "int"))

    # 17. Vestidor de Paso Doble Suite (X=12.65..16.65, Y=7.65..10.80)
    out.append(draw_wall_segment(X1(12.65), Y1(10.80), L1(4.00), pt, "int"))

    # Separación Galería Acústica (Y=12.40..13.55) / Dormitorios Infantiles (Y=12.50..16.15)
    # Dormitorio Niña: X=6.50..9.75, Y=12.50..16.15 (3,25 x 4,50 m = 14,60 m²)
    # Dormitorio Niño: X=9.87..13.00, Y=12.50..16.15 (3,13 x 4,66 m = 14,60 m²)
    # Master Suite Dormitorio: X=13.12..16.65, Y=10.92..16.15 (16,50 m²)
    out.append(draw_wall_segment(X1(6.50), Y1(12.40), L1(2.00), pt, "acoustic"))
    out.append(draw_wall_segment(X1(8.50), Y1(13.55), L1(4.50), pt, "acoustic"))

    # TABIQUE MEDIANERO CIEGO DE ALTA MASA ACÚSTICA (Rw ≥ 50 dB) entre Dormitorio Niña y Niño (X=9.75)
    out.append(draw_wall_segment(X1(9.75), Y1(13.55), L1(0.14), L1(2.60), "acoustic"))
    out.append(f'<g transform="translate({X1(9.66):.1f}, {Y1(14.85):.1f}) rotate(-90)"><text x="0" y="0" fill="#f59e0b" font-size="5.5" font-weight="700" text-anchor="middle">MEDIANERA CIEGA Rw≥50dB (CERO HUECOS)</text></g>')

    # Tabique acústico entre Dormitorio Niño y Master Suite (X=13.00, Y=12.40..16.15)
    out.append(draw_wall_segment(X1(13.00), Y1(12.40), L1(0.14), L1(3.75), "acoustic"))
    out.append('</g>')

    # =========================================================================
    # CAPA 5: CARPINTERÍAS DE PLANTA PRIMERA (C-10 a C-15) (id="carpinterias")
    # =========================================================================
    out.append('<g id="carpinterias">')
    # C-10: Ventana Norte Baño Hijos (1,20 x 0,60 m, h=160cm) en X=8.00..9.20, Y=5.17
    out.append(draw_window_cad(X1(8.00), Y1(5.17), X1(9.20), Y1(5.17), wall_thick=wt, code="C-10", dim_txt="1,20x0,60 (h=160)"))

    # C-11: Ventana Norte Baño Suite (1,40 x 0,60 m, h=160cm) en X=14.20..15.60, Y=5.17
    out.append(draw_window_cad(X1(14.20), Y1(5.17), X1(15.60), Y1(5.17), wall_thick=wt, code="C-11", dim_txt="1,40x0,60 (h=160)"))

    # C-12: Balconera Corredera Dormitorio Niña a Balcón Sur (2,20 x 2,40 m) en X=7.00..9.20, Y=16.32
    out.append(draw_sliding_door(X1(7.00), Y1(16.32), X1(9.20), Y1(16.32), wall_thick=wt, leaves=2, code="C-12", dim_txt="2,20x2,40 COR 80"))

    # C-13: Balconera Corredera Dormitorio Niño a Balcón Sur (2,20 x 2,40 m) en X=10.35..12.55, Y=16.32
    out.append(draw_sliding_door(X1(10.35), Y1(16.32), X1(12.55), Y1(16.32), wall_thick=wt, leaves=2, code="C-13", dim_txt="2,20x2,40 COR 80"))

    # C-14: Gran Balconera Corredera Suite Matrimonio a Balcón Sur (3,00 x 2,40 m) en X=13.40..16.40, Y=16.32
    out.append(draw_sliding_door(X1(13.40), Y1(16.32), X1(16.40), Y1(16.32), wall_thick=wt, leaves=2, code="C-14", dim_txt="3,00x2,40 Cor Vision"))

    # C-15: Mampara Acústica Fija Continua 4+4 Silence sobre el Claustro (4,00 x 2,60 m, Rw=42dB)
    # En borde Oeste (X=8.50, Y=8.40..12.40) y borde Sur del Claustro (Y=12.40, X=8.50..12.50)
    out.append(draw_window_cad(X1(8.50), Y1(8.40), X1(8.50), Y1(12.40), wall_thick=7, code="C-15A", dim_txt="Mampara 4+4 Silence 42dB"))
    out.append(draw_window_cad(X1(8.50), Y1(12.40), X1(12.50), Y1(12.40), wall_thick=7, code="C-15B", dim_txt="Mampara Acústica 4+4 Silence (4,00x2,60m · Aísla 42 dB)"))

    # Puertas interiores P1:
    # P-11: Entrada Baño Hijos (0,82m) en Y=8.15, X=7.40..8.22
    out.append(draw_door_swing(X1(7.40), Y1(8.15), L1(0.82), WallDir="E", SwingDir="N", code="P-11", dim_txt="0,82"))
    # P-12: Entrada Dormitorio Niña (0,82m) en Y=12.40, X=7.45..8.27
    out.append(draw_door_swing(X1(7.45), Y1(12.52), L1(0.82), WallDir="E", SwingDir="S", code="P-12", dim_txt="0,82"))
    # P-13: Entrada Dormitorio Niño (0,82m) en Y=13.55, X=10.05..10.87
    out.append(draw_door_swing(X1(10.05), Y1(13.67), L1(0.82), WallDir="E", SwingDir="S", code="P-13", dim_txt="0,82"))
    # P-14: Entrada Suite Principal desde Galería (0,85m) en X=13.00, Y=12.60..13.45
    out.append(draw_door_swing(X1(13.14), Y1(12.60), L1(0.85), WallDir="S", SwingDir="E", code="P-14", dim_txt="0,85"))
    # P-15: Corredera Vestidor → Dormitorio Suite (0,90m) en Y=10.80, X=14.20..15.10
    out.append(draw_sliding_door(X1(14.20), Y1(10.85), X1(15.10), Y1(10.85), wall_thick=pt, leaves=1, code="P-15", dim_txt="0,90"))
    # P-16: Corredera Vestidor → Baño Privado Suite (0,85m) en Y=7.55, X=14.20..15.05
    out.append(draw_sliding_door(X1(14.20), Y1(7.60), X1(15.05), Y1(7.60), wall_thick=pt, leaves=1, code="P-16", dim_txt="0,85"))
    out.append('</g>')

    # =========================================================================
    # CAPA 6: MOBILIARIO REGLAMENTARIO NHG PLANTA PRIMERA (id="mobiliario-nhg")
    # =========================================================================
    out.append('<g id="mobiliario-nhg">')
    # 12. DESEMBARCO ESCALERA Y GALERÍA ACÚSTICA P1 (8,20 m² útiles)
    st_x, st_y, st_w = X1(6.55), Y1(8.40), L1(1.05)
    tread_h = L1(0.23)
    out.append(f'<rect x="{st_x:.1f}" y="{st_y:.1f}" width="{st_w:.1f}" height="{17 * tread_h:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    for i in range(1, 18):
        ty = st_y + i * tread_h
        out.append(f'<line x1="{st_x:.1f}" y1="{ty:.1f}" x2="{st_x + st_w:.1f}" y2="{ty:.1f}" stroke="#94a3b8" stroke-width="0.65"/>')
    out.append(f'<line x1="{st_x + st_w/2:.1f}" y1="{st_y + 10:.1f}" x2="{st_x + st_w/2:.1f}" y2="{st_y + 16*tread_h:.1f}" stroke="#10b981" stroke-width="0.9" marker-end="url(#arrow-tech)"/>')
    out.append(f'<text x="{st_x + st_w/2:.1f}" y="{st_y + 16.5*tread_h:.1f}" fill="#10b981" font-size="5.5" font-weight="700" text-anchor="middle">LLEGADA +3,15m</text>')
    out.append(draw_room_stamp(X1(10.65), Y1(13.00), "E-16", "GALERÍA ACÚSTICA P1", 8.20, "Roble 14mm · Balizas 25cm", "+3,15"))

    # 15. BAÑO COMPARTIDO HIJOS (X=6.50..12.50, Y=5.35..8.15 → 6,80 m²)
    # Bañera/Ducha amplia encastrada 1,70 x 0,75 m
    out.append(draw_shower_block(X1(6.60), Y1(5.45), L1(1.70), L1(0.80), drain_side="E", label="BAÑERA/DUCHA 1,70x0,75"))
    # Mueble suspendido doble seno (1,40 x 0,50 m)
    out.append(draw_sink_block(X1(9.35), Y1(5.42), L1(1.40), L1(0.50), basins=2, orient="N"))
    # Inodoro suspendido Geberit iCon Rimless
    out.append(draw_wc_block(X1(11.15), Y1(5.42), L1(0.42), L1(0.56), orient="N"))
    out.append(draw_nhg_circle(X1(9.60), Y1(7.10), 1.20, S1, "Ø1,20m NHG"))
    out.append(draw_room_stamp(X1(11.15), Y1(7.25), "E-19", "BAÑO COMPARTIDO HIJOS", 6.80, "Porcelánico C3 · Doble Seno", "+3,15"))

    # 13. DORMITORIO INFANTIL NIÑA (X=6.50..9.75, Y=12.55..16.15 → 14,60 m²)
    # Armario empotrado en pared Norte (1,50 x 0,60 m)
    out.append(draw_wardrobe_block(X1(8.20), Y1(12.58), L1(1.50), L1(0.58), "ARMARIO 1,50m"))
    # Cama 1,20 x 2,00 m apoyada en pared Oeste
    out.append(draw_bed_block(X1(6.58), Y1(13.65), L1(1.95), L1(1.20), orient="W", kind="single", label="CAMA 1,20x2,00"))
    # Mesa de estudio suspendida (1,80 x 0,65 m) en PARED LATERAL ESTE (Luz de balconera Sur a 90°)
    out.append(f'<rect x="{X1(9.05):.1f}" y="{Y1(13.85):.1f}" width="{L1(0.65):.1f}" height="{L1(1.80):.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<circle cx="{X1(8.75):.1f}" cy="{Y1(14.75):.1f}" r="{L1(0.24):.1f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>')
    out.append(f'<g transform="translate({X1(9.40):.1f}, {Y1(14.75):.1f}) rotate(-90)"><text x="0" y="0" fill="#38bdf8" font-size="5.3" font-weight="700" text-anchor="middle">ESTUDIO 1,80m (LUZ 90°)</text></g>')
    out.append(draw_nhg_circle(X1(7.80), Y1(15.45), 1.50, S1, "Ø1,50m NHG"))
    out.append(draw_room_stamp(X1(7.80), Y1(13.15), "E-17", "DORMITORIO NIÑA", 14.60, "Roble 14mm · Luz 90°", "+3,15"))

    # 14. DORMITORIO INFANTIL NIÑO (X=9.90..13.00, Y=13.65..16.15 → 14,60 m²)
    out.append(draw_wardrobe_block(X1(11.15), Y1(13.70), L1(1.75), L1(0.58), "ARMARIO 1,75m"))
    out.append(draw_bed_block(X1(9.95), Y1(14.35), L1(1.90), L1(1.20), orient="W", kind="single", label="CAMA 1,20x2,00"))
    # Mesa de estudio suspendida (1,80 x 0,65 m) en PARED LATERAL ESTE (Luz de balconera Sur a 90°)
    out.append(f'<rect x="{X1(12.30):.1f}" y="{Y1(14.30):.1f}" width="{L1(0.65):.1f}" height="{L1(1.75):.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<circle cx="{X1(12.02):.1f}" cy="{Y1(15.15):.1f}" r="{L1(0.24):.1f}" fill="none" stroke="#94a3b8" stroke-width="0.7"/>')
    out.append(f'<g transform="translate({X1(12.65):.1f}, {Y1(15.15):.1f}) rotate(-90)"><text x="0" y="0" fill="#38bdf8" font-size="5.3" font-weight="700" text-anchor="middle">ESTUDIO 1,80m (LUZ 90°)</text></g>')
    out.append(draw_Room_Or_Stamp := draw_room_stamp(X1(11.15), Y1(15.72), "E-18", "DORMITORIO NIÑO", 14.60, "Roble 14mm · Luz 90°", "+3,15"))

    # 18. BAÑO PRIVADO SUITE (X=12.65..16.65, Y=5.35..7.55 → 6,30 m²)
    out.append(draw_sink_block(X1(12.80), Y1(5.42), L1(1.60), L1(0.50), basins=2, orient="N"))
    out.append(draw_wc_block(X1(14.55), Y1(5.42), L1(0.42), L1(0.56), orient="N"))
    out.append(draw_shower_block(X1(15.10), Y1(5.42), L1(1.50), L1(0.95), drain_side="E", label="DUCHA DOBLE 1,50x0,95"))
    out.append(draw_room_stamp(X1(14.65), Y1(6.95), "E-22", "BAÑO PRIVADO SUITE", 6.30, "Dekton Kelya · Ducha Doble", "+3,15"))

    # 17. VESTIDOR DE PASO DOBLE SUITE (X=12.65..16.65, Y=7.68..10.80 → 8,40 m²)
    # Dos hileras enfrentadas de suelo a techo (fondo 60 cm) con pasillo central libre
    out.append(draw_wardrobe_block(X1(12.75), Y1(7.80), L1(0.60), L1(2.85), "VESTIDOR W (0,60m)"))
    out.append(draw_wardrobe_block(X1(16.00), Y1(7.80), L1(0.60), L1(2.85), "VESTIDOR E (0,60m)"))
    out.append(draw_room_stamp(X1(14.65), Y1(9.25), "E-21", "VESTIDOR DE PASO SUITE", 8.40, "Vidrio Ahumado · LED", "+3,15"))

    # 16. MASTER SUITE MATRIMONIO (X=13.15..16.65, Y=10.95..16.15 → 16,50 m²)
    # Cama King Size 1,80 x 2,00 m centrada con mesillas flotantes
    out.append(draw_bed_block(X1(14.00), Y1(11.10), L1(1.80), L1(2.00), orient="N", kind="double", label="KING SIZE 1,80 × 2,00 m"))
    out.append(f'<rect x="{X1(13.50):.1f}" y="{Y1(11.10):.1f}" width="{L1(0.45):.1f}" height="{L1(0.42):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.7"/>')
    out.append(f'<rect x="{X1(15.85):.1f}" y="{Y1(11.10):.1f}" width="{L1(0.45):.1f}" height="{L1(0.42):.1f}" fill="#131c31" stroke="#cbd5e1" stroke-width="0.7"/>')
    out.append(draw_nhg_circle(X1(14.90), Y1(14.15), 1.50, S1, "Ø1,50m NHG"))
    out.append(draw_room_stamp(X1(14.90), Y1(15.35), "E-20", "MASTER SUITE MATRIMONIO", 16.50, "Roble 14mm · Balcón Sur", "+3,15"))
    out.append('</g>')

    # =========================================================================
    # CAPA 7: INSTALACIONES MEP PLANTA PRIMERA (VMC, BAJANTES, ELECTRICIDAD)
    # =========================================================================
    out.append('<g id="instalaciones-mep-p1">')
    out.append(draw_mep_symbol(X1(11.20), Y1(6.20), "vmc_ext", "VMC-E 40m³/h"))
    out.append(draw_mep_symbol(X1(15.80), Y1(6.60), "vmc_ext", "VMC-E 40m³/h"))
    out.append(draw_mep_symbol(X1(7.20), Y1(15.60), "vmc_imp", "VMC-I 30m³/h"))
    out.append(draw_mep_symbol(X1(10.30), Y1(15.60), "vmc_imp", "VMC-I 30m³/h"))
    out.append(draw_mep_symbol(X1(16.00), Y1(13.80), "vmc_imp", "VMC-I 40m³/h"))
    # Tomas RJ45 Cat 6A en los pupitres de estudio (desplazadas >30 cm en tabique medianero)
    out.append(draw_mep_symbol(X1(9.55), Y1(14.30), "rj45", "2×RJ45+3×16A (h=80)"))
    out.append(draw_mep_symbol(X1(12.80), Y1(14.80), "rj45", "2×RJ45+3×16A (h=80)"))
    # Bajantes insonorizadas Geberit Silent-PP Ø110
    out.append(draw_mep_symbol(X1(11.65), Y1(5.55), "drain", "BAJANTE B-02 Ø110"))
    out.append(draw_mep_symbol(X1(16.45), Y1(5.55), "drain", "BAJANTE B-01 Ø110"))
    out.append('</g>')

    # =========================================================================
    # CAPA 8: COTAS ENCADENADAS Y NORTE PLANTA PRIMERA (id="textos-cotas-norte")
    # =========================================================================
    out.append('<g id="textos-cotas-norte">')
    # Cotas Horizontales Superiores (Norte)
    out.append(draw_dim_h(X1(1.00), X1(6.15), Y1(5.00), Y1(4.15), "5,15 m (Cubierta Técnica FV)", S1, "#94a3b8", "tick-45-white"))
    out.append(draw_dim_h(X1(6.15), X1(12.50), Y1(5.00), Y1(4.15), "6,35 m (Baño Hijos + Escalera)", S1, "#38bdf8"))
    out.append(draw_dim_h(X1(12.50), X1(17.00), Y1(5.00), Y1(4.15), "4,50 m (Ala Master Suite Este)", S1, "#38bdf8"))
    out.append(draw_dim_h(X1(6.15), X1(17.00), Y1(4.15), Y1(3.45), "10,85 m (ANCHO TOTAL VOLUMEN PLANTA PRIMERA)", S1, "#f59e0b", "tick-45-amber", font_size=8.5))

    # Cotas Horizontales Inferiores (Sur - Dormitorios)
    out.append(draw_dim_h(X1(6.15), X1(9.75), Y1(17.90), Y1(18.45), "3,60 m (Dorm. Niña)", S1, "#38bdf8"))
    out.append(draw_dim_h(X1(9.75), X1(13.00), Y1(17.90), Y1(18.45), "3,25 m (Dorm. Niño)", S1, "#38bdf8"))
    out.append(draw_dim_h(X1(13.00), X1(17.00), Y1(17.90), Y1(18.45), "4,00 m (Master Suite)", S1, "#38bdf8"))

    # Cotas Verticales Izquierda (Oeste)
    out.append(draw_dim_v(Y1(5.00), Y1(8.40), X1(1.00), X1(0.30), "3,40 m (Núcleo Baños N)", S1, "#38bdf8"))
    out.append(draw_dim_v(Y1(8.40), Y1(12.40), X1(1.00), X1(0.30), "4,00 m (Vacío Claustro)", S1, "#10b981"))
    out.append(draw_dim_v(Y1(12.40), Y1(16.50), X1(6.15), X1(0.30), "4,10 m (Dormitorios Sur)", S1, "#38bdf8"))
    out.append(draw_dim_v(Y1(16.50), Y1(17.90), X1(6.15), X1(0.30), "1,40 m (Balcón Sur)", S1, "#f59e0b", "tick-45-amber"))

    out.append(draw_north_rose_and_scale(X1(3.50), Y1(15.50), scale_px_per_m=S1, scale_label="1:75"))
    out.append('</g>')

    # =========================================================================
    # PANEL TÉCNICO LATERAL DERECHO PLANTA PRIMERA
    # =========================================================================
    out.append('<g id="panel-tecnico-p1" transform="translate(990, 35)">')
    out.append('<rect x="0" y="0" width="480" height="1040" fill="#090e1a" stroke="#64748b" stroke-width="1.2"/>')
    out.append('<rect x="0" y="0" width="480" height="34" fill="#131c31" stroke="#64748b" stroke-width="0.8"/>')
    out.append('<text x="240" y="15" fill="#38bdf8" font-size="9.0" font-weight="700" text-anchor="middle">CUADRO DE SUPERFICIES Y DETALLE TÉCNICO — PLANTA PRIMERA</text>')
    out.append('<text x="240" y="27" fill="#94a3b8" font-size="6.5" text-anchor="middle">Cota de Pavimento Terminado: +3,15 m · Altura Libre: 2,65 m · Coronación: +6,80 m</text>')

    p1_rooms = [
        ("E-16", "12. Desembarco Escalera y Galería Acústica", "8,20 m²", "Roble 14mm + Vidrio 4+4 Silence"),
        ("E-17", "13. Dormitorio Infantil Niña (Estudio 90°)", "14,60 m²", "Roble 14mm + Balconera 2,20m"),
        ("E-18", "14. Dormitorio Infantil Niño (Estudio 90°)", "14,60 m²", "Roble 14mm + Balconera 2,20m"),
        ("E-19", "15. Baño Compartido Hijos (Doble Seno)", "6,80 m²", "Porcelánico C3 + Bañera 1,70m"),
        ("E-20", "16. Dormitorio Master Suite Matrimonio", "16,50 m²", "Roble 14mm + Balconera 3,00m"),
        ("E-21", "17. Vestidor de Paso Doble Hilera Suite", "8,40 m²", "Roble 14mm + Vidrio Ahumado"),
        ("E-22", "18. Baño Privado Suite (Ducha Doble 1,50m)", "6,30 m²", "Porcelánico C3 + Dekton Kelya"),
        ("SUB-P1", "TOTAL SUPERFICIE ÚTIL INTERIOR P1", "75,40 m²", "(Construida cerrada P1: 98,50 m²)"),
        ("E-23", "19. Balcón Corrido Sur en Voladizo (Fondo 1,4m)", "14,00 m²", "Tarima Iroko s/ Plots + Vidrio"),
        ("CUB-FV", "Cubierta Plana Técnica Inferior (12 Módulos)", "38,10 m²", "Grava + 5,40 kWp Solar FV"),
        ("TOT-VIV", "SUPERFICIE ÚTIL TOTAL VIVIENDA (PB + P1)", "188,40 m²", "(Construida Total: 215,00 m²)"),
    ]
    out.append('<text x="14" y="52" fill="#38bdf8" font-size="7.8" font-weight="700">1. DESGLOSE DE SUPERFICIES ÚTILES Y ACABADOS (PLANTA PRIMERA +3,15 m)</text>')
    y0 = 60
    for idx, (cid, cnam, csup, cpav) in enumerate(p1_rooms):
        yr = y0 + idx * 18
        is_hl = cid in ("SUB-P1", "TOT-VIV")
        bg = "#131c31" if is_hl else "none"
        col_c = "#f59e0b" if is_hl else "#e2e8f0"
        out.append(f'<rect x="14" y="{yr}" width="452" height="18" fill="{bg}" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="18" y="{yr+12}" fill="#38bdf8" font-size="6.0" font-weight="700">{cid}</text>')
        out.append(f'<text x="65" y="{yr+12}" fill="{col_c}" font-size="6.0" font-weight="{"700" if is_hl else "400"}">{cnam}</text>')
        out.append(f'<text x="275" y="{yr+12}" fill="{col_c}" font-size="6.3" font-weight="700">{csup}</text>')
        out.append(f'<text x="330" y="{yr+12}" fill="#94a3b8" font-size="5.6">{cpav}</text>')

    # Tabla Carpinterías P1
    y_c1 = 280
    out.append(f'<text x="14" y="{y_c1}" fill="#10b981" font-size="7.8" font-weight="700">2. CUADRO DE CARPINTERÍAS DE PLANTA PRIMERA (C-10 A C-15)</text>')
    c_p1 = [
        ("C-10", "Baño Hijos Norte", "Oscilobatiente Alta", "1,20 × 0,60 m", "h=160 cm", "Cortizo COR 80 RPT Mate"),
        ("C-11", "Baño Suite Norte", "Oscilobatiente Alta", "1,40 × 0,60 m", "h=160 cm", "Cortizo COR 80 RPT Mate"),
        ("C-12", "Dorm. Niña → Balcón", "Balconera Corredera", "2,20 × 2,40 m", "h=0 cm", "COR 80 RPT + Persiana Motor."),
        ("C-13", "Dorm. Niño → Balcón", "Balconera Corredera", "2,20 × 2,40 m", "h=0 cm", "COR 80 RPT + Persiana Motor."),
        ("C-14", "Suite → Balcón Sur", "Balconera Corredera", "3,00 × 2,40 m", "h=0 cm", "Cortizo Cor Vision + Persiana"),
        ("C-15", "Galería → Claustro", "Fijo Acústico Suelo-Techo", "4,00 × 2,60 m", "h=0 cm", "Laminado Acústico 4+4 Silence"),
    ]
    for idx, (cc, cub, cap, cdim, cant, cser) in enumerate(c_p1):
        yr = y_c1 + 10 + idx * 17
        out.append(f'<rect x="14" y="{yr}" width="452" height="17" fill="none" stroke="#334155" stroke-width="0.5"/>')
        out.append(f'<text x="18" y="{yr+11.5}" fill="#f59e0b" font-size="6.0" font-weight="700">{cc}</text>')
        out.append(f'<text x="55" y="{yr+11.5}" fill="#e2e8f0" font-size="5.8">{cub}</text>')
        out.append(f'<text x="145" y="{yr+11.5}" fill="#94a3b8" font-size="5.8">{cap}</text>')
        out.append(f'<text x="235" y="{yr+11.5}" fill="#38bdf8" font-size="6.0" font-weight="700">{cdim}</text>')
        out.append(f'<text x="300" y="{yr+11.5}" fill="#cbd5e1" font-size="5.8">{cant}</text>')
        out.append(f'<text x="345" y="{yr+11.5}" fill="#94a3b8" font-size="5.6">{cser}</text>')

    # Criterios Técnicos de Ejecución P1
    y_n1 = 415
    out.append(f'<text x="14" y="{y_n1}" fill="#f59e0b" font-size="7.8" font-weight="700">3. ESPECIFICACIONES DE EJECUCIÓN Y ACÚSTICA EN PLANTA PRIMERA</text>')
    out.append(f'<rect x="14" y="{y_n1+10}" width="452" height="260" fill="#0b1120" stroke="#475569" stroke-width="0.7"/>')
    notas_p1 = [
        "1. MAMPARA ACÚSTICA 4+4 SILENCE (C-15): Cerramiento fijo de vidrio laminado acústico con",
        "   butiral PVB Silence que cierra la galería sobre el vacío del Patio Corrala. Atenuación Rw = 42 dB.",
        "2. ERGONOMÍA DE ESTUDIO A 90° (CERO REFLEJOS): En ambos dormitorios infantiles (E-17 y E-18),",
        "   las mesas de estudio de 1,80 × 0,65 m se anclan en la pared lateral Este. La luz del Sur entra",
        "   perpendicularmente por la izquierda, evitando deslumbramiento y contraluz en pantallas.",
        "3. TABIQUE MEDIANERO DE ALTA MASA ACÚSTICA (Rw ≥ 50 dB): La divisoria entre ambos dormitorios",
        "   infantiles se ejecuta con doble placa Pladur Fonic 13mm por cara y lana mineral 70 kg/m³.",
        "   Prohibido enfrentar cajas de mecanismos eléctricos (desfase mínimo horizontal de 30 cm).",
        "4. UNIFICACIÓN VERTICAL DE BAJANTES: El Baño de Hijos (E-19) y el Baño Suite (E-22) descargan",
        "   verticalmente por las bajantes B-02 y B-01 (Geberit Silent-PP Ø110 mm) sin colectores colgados",
        "   sobre el techo del Salón ni del Comedor.",
        "5. BARANDILLA ESTRUCTURAL DEL BALCÓN SUR: Perfil en U de aluminio anodizado embutido en el canto",
        "   del forjado de hormigón para alojar vidrio laminar templado 10+10.2 mm sin montantes verticales.",
    ]
    for idx_n, nl in enumerate(notas_p1):
        col_n = "#f8fafc" if nl[0].isdigit() else "#94a3b8"
        fw_n = "700" if nl[0].isdigit() else "400"
        out.append(f'<text x="20" y="{y_n1 + 26 + idx_n*18.5:.1f}" fill="{col_n}" font-size="5.8" font-weight="{fw_n}">{nl}</text>')

    # Esquema de Sección de Forjado P1 + Suelo Radiante
    y_det = 705
    out.append(f'<text x="14" y="{y_det}" fill="#38bdf8" font-size="7.8" font-weight="700">4. DETALLE SECCIÓN CONSTRUCTIVA DE FORJADO P1 Y BALCÓN SUR (E 1:20)</text>')
    out.append(f'<rect x="14" y="{y_det+10}" width="452" height="310" fill="#0b1120" stroke="#475569" stroke-width="0.7"/>')
    # Dibujo CAD de sección del forjado P1 y encuentro con balcón sur enrasado cota +3,15m
    dx0, dy0 = 40, y_det + 145
    # Losa de hormigón armado 25cm
    out.append(f'<rect x="{dx0}" y="{dy0}" width="380" height="45" fill="url(#hatch-ansi31)" stroke="#e2e8f0" stroke-width="1.2"/>')
    out.append(f'<text x="{dx0+190}" y="{dy0+26}" fill="#f8fafc" font-size="6.5" font-weight="700" text-anchor="middle">LOSA / FORJADO HORMIGÓN ARMADO HA-25 (e = 25,0 cm)</text>')
    # Interior (izquierda): Lámina anti-impacto + XPS 30mm + Autonivelante anhidrita 50mm con tubos PEX + Roble 14mm
    out.append(f'<rect x="{dx0}" y="{dy0-14}" width="210" height="14" fill="url(#hatch-insulation)" stroke="#38bdf8" stroke-width="0.7"/>')
    out.append(f'<rect x="{dx0}" y="{dy0-32}" width="210" height="18" fill="#1e293b" stroke="#cbd5e1" stroke-width="0.8"/>')
    for x_p in range(dx0 + 20, dx0 + 200, 28):
        out.append(f'<circle cx="{x_p}" cy="{dy0-22}" r="3.5" fill="#0b1120" stroke="#f43f5e" stroke-width="1.1"/>')
    out.append(f'<rect x="{dx0}" y="{dy0-38}" width="210" height="6" fill="#78350f" stroke="#f59e0b" stroke-width="0.7"/>')
    # Taco Purenit 50mm bajo marco balconera C-14 (en X = dx0+210..235)
    out.append(f'<rect x="{dx0+210}" y="{dy0-38}" width="24" height="38" fill="#334155" stroke="#f59e0b" stroke-width="1.1"/>')
    out.append(f'<rect x="{dx0+214}" y="{dy0-95}" width="16" height="57" fill="#0b1120" stroke="#38bdf8" stroke-width="1.2"/>')
    # Exterior Balcón Sur (derecha): Impermeabilización + Plots regulables + Tarima Iroko 21mm a cota +3,15m + Barandilla vidrio 10+10
    out.append(f'<rect x="{dx0+234}" y="{dy0-38}" width="130" height="6" fill="#78350f" stroke="#f59e0b" stroke-width="0.8"/>')
    for x_pl in [dx0 + 250, dx0 + 295, dx0 + 340]:
        out.append(f'<rect x="{x_pl}" y="{dy0-32}" width="10" height="30" fill="#475569" stroke="#cbd5e1" stroke-width="0.6"/>')
    # Perfil U oculto y barandilla de vidrio estructural 10+10mm en extremo derecho
    out.append(f'<rect x="{dx0+366}" y="{dy0-38}" width="12" height="32" fill="#334155" stroke="#e2e8f0" stroke-width="1.0"/>')
    out.append(f'<rect x="{dx0+369}" y="{dy0-125}" width="6" height="95" fill="#38bdf8" fill-opacity="0.35" stroke="#38bdf8" stroke-width="1.1"/>')
    # Etiquetas del detalle constructivo
    out.append(f'<text x="{dx0+100}" y="{dy0-46}" fill="#f8fafc" font-size="6.2" font-weight="700" text-anchor="middle">INTERIOR DORMITORIO (+3,15 m)</text>')
    out.append(f'<text x="{dx0+100}" y="{dy0-57}" fill="#94a3b8" font-size="5.6" text-anchor="middle">Roble 14mm + Anhidrita 50mm (PEX Ø16) + XPS 30mm</text>')
    out.append(f'<text x="{dx0+295}" y="{dy0-46}" fill="#38bdf8" font-size="6.2" font-weight="700" text-anchor="middle">BALCÓN SUR ENRASADO (+3,15 m)</text>')
    out.append(f'<text x="{dx0+295}" y="{dy0-57}" fill="#94a3b8" font-size="5.6" text-anchor="middle">Tarima Iroko 21mm s/ Plots + EPDM p=1,5%</text>')
    out.append(f'<text x="{dx0+222}" y="{dy0+62}" fill="#f59e0b" font-size="5.8" font-weight="700" text-anchor="middle">RPT Purenit 50mm (Cero Puente Térmico)</text>')
    out.append(f'<text x="{dx0+355}" y="{dy0-110}" fill="#38bdf8" font-size="5.8" font-weight="700" text-anchor="end">Vidrio Estructural 10+10.2 mm (h=1,10 m)</text>')
    out.append('</g>')

    # =========================================================================
    # CAJETÍN TÉCNICO ISO 7200 PLANTA PRIMERA
    # =========================================================================
    out.append(
        draw_iso_title_block(
            x=30, y=1125, w=1440, h=65,
            sheet_num="A-02",
            sheet_title="PLANTA PRIMERA GENERAL (COTA +3,15 m) Y CUBIERTAS",
            scale_txt="ESCALA 1:75 / 1:20",
            subtitle="Zonificación Nocturna, Mampara Acústica 4+4 Silence, Estudio a 90° y Campo FV 5,4 kWp",
            summary_rows=[
                "• Superficie Útil Interior P1: 75,40 m² + Balcón Corrido Sur: 14,00 m² · Total Útil Vivienda: 188,40 m²",
                "• Aislamiento Acústico: Mampara 4+4 Silence (42 dB) sobre Claustro + Medianera Dormitorios Rw ≥ 50 dB",
                "• Ergonomía Visual: Pupitres de 1,80 m en pared Este con luz natural lateral a 90° (cero reflejos)",
                "• Cubierta Técnica Inferior: 12 Módulos Fotovoltaicos Monocristalinos 450W (5,40 kWp) con Inversor 5kW",
            ],
        )
    )

    out.append("</svg>")
    return "\n".join(out)


def main():
    pb_svg = build_planta_baja_svg()
    p1_svg = build_planta_alta_svg()

    paths_pb = [
        "/home/antigravity/landslore/oleiros/planta_baja_propuesta_d.svg",
        "/home/antigravity/landslore/oleiros/propuestas/planta_baja_propuesta_d.svg",
    ]
    for p in paths_pb:
        with open(p, "w", encoding="utf-8") as f:
            f.write(pb_svg)
        print(f"Written {p} ({len(pb_svg)} bytes)")

    paths_p1 = [
        "/home/antigravity/landslore/oleiros/planta_alta_propuesta_d.svg",
        "/home/antigravity/landslore/oleiros/propuestas/planta_alta_propuesta_d.svg",
    ]
    for p in paths_p1:
        with open(p, "w", encoding="utf-8") as f:
            f.write(p1_svg)
        print(f"Written {p} ({len(p1_svg)} bytes)")


if __name__ == "__main__":
    main()
