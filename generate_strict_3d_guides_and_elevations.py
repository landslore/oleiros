#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de:
1. Plano CAD de los 4 Alzados Exteriores Estrictos (Norte, Sur, Este y Oeste) a Escala 1:100:
   - plano_alzados_exteriores_4_caras.svg
2. Guías Geométricas 3D Exactas (PNG) proyectadas matemáticamente desde las coordenadas reales
   (X=0..20m, Y=0..30m, Z=0..6.80m / +7.80m chimenea) para condicionar los renders fotorrealistas
   de las 4 fachadas y la vista en perspectiva superior.
   Versión Optimizada Passivhaus (~165 m² constr. totales · Desfase Sur · Cero Terrazas Sucias).
"""

import os
import math
from PIL import Image, ImageDraw

from cad_engine import (
    svg_defs, dim_h, dim_v, title_block, sanitize_svg_text
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(BASE_DIR, "propuestas", "renders", "guides_3d")
os.makedirs(GUIDES_DIR, exist_ok=True)


# ==============================================================================
# 1. PLANO CAD DE LOS 4 ALZADOS EXTERIORES ESTRICTOS (ESCALA 1:100)
# ==============================================================================
def build_4_elevations_svg() -> str:
    W, H = 1800, 1320
    S = 34.0  # 1m = 34px

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%" style="background-color:#070b14;">',
        svg_defs(),
        f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#475569" stroke-width="1.5"/>',
        f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#334155" stroke-width="0.6"/>',
        '<rect x="28" y="26" width="1744" height="36" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>',
        '<text x="42" y="43" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700">PLANO A-03 · ALZADOS EXTERIORES ESTRICTOS (NORTE, SUR, ESTE Y OESTE) — VERSIÓN OPTIMIZADA PASSIVHAUS (~165 m²)</text>',
        '<text x="42" y="55" fill="#94a3b8" font-family="monospace" font-size="7.2">Desfase Volumétrico Sur · Efecto Soportal Porche 3,00 m · Cero Terrazas Sucias · Chimenea Exterior Este (+7,80 m) · Solar FV (+6,50 m)</text>',
    ]

    def level_marks(x_left: float, x_right: float, gy: float, levels):
        g = [f'<line x1="{x_left-25:.1f}" y1="{gy:.1f}" x2="{x_right+25:.1f}" y2="{gy:.1f}" stroke="#10b981" stroke-width="2.2"/>']
        for z_m, lbl, col in levels:
            ly = gy - z_m * S
            g.append(f'<line x1="{x_left-15:.1f}" y1="{ly:.1f}" x2="{x_right+15:.1f}" y2="{ly:.1f}" stroke="{col}" stroke-width="0.6" stroke-dasharray="5,3" opacity="0.75"/>')
            g.append(f'<text x="{x_right+18:.1f}" y="{ly+2:.1f}" fill="{col}" font-family="monospace" font-size="5.6" font-weight="700">{lbl}</text>')
        return "\n".join(g)

    # ==========================================================================
    # PANEL 1: ALZADO NORTE (FACHADA PRINCIPAL DE ACCESO · Y = 5,00 m)
    # Vista mirando hacia el Sur -> Izquierda es Este (X=17,00), Derecha es Oeste (X=1,00)
    # ==========================================================================
    out.append('<rect x="28" y="70" width="862" height="515" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="28" y="70" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="40" y="85" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">1. ALZADO NORTE (ACCESO Y VIAL · Y = 5,00 m) — De Este (X=17,00 m) a Oeste (X=1,00 m)</text>')

    gy1 = 465.0
    def nx(xm: float) -> float:
        return 115.0 + (17.00 - xm) * S

    def ny(zm: float) -> float:
        return gy1 - zm * S

    out.append(level_marks(nx(17.50), nx(0.50), gy1, [
        (0.00, "±0,00 m (PB)", "#10b981"),
        (2.90, "+2,90 m (Pérgola)", "#94a3b8"),
        (3.15, "+3,15 m (Cub. PB / Forjado P1)", "#38bdf8"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
        (7.40, "+7,40 m (Campo FV 30°)", "#f59e0b"),
    ]))

    for lbl, xm in [("E", 17.00), ("D", 13.50), ("C", 10.00), ("B", 6.15), ("A", 4.00)]:
        xx = nx(xm)
        out.append(f'<line x1="{xx:.1f}" y1="102" x2="{xx:.1f}" y2="{gy1+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="102" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="105" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.2" font-weight="700">{lbl}</text>')

    # 1.1 SEGUNDO PLANO (AL FONDO): Volumen Planta Primera a Y=14.30m (X=17.00..6.15, Z=3.15..6.80m)
    # SATE Blanco Cálido NCS S 0502-Y
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(6.80):.1f}" width="{10.85*S:.1f}" height="{3.65*S:.1f}" fill="#1e293b" stroke="#94a3b8" stroke-width="1.2"/>')
    out.append(f'<rect x="{nx(17.05):.1f}" y="{ny(6.80):.1f}" width="{10.95*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    # Mirador C-15A Galería (X=6.50..8.30, Z=3.15..5.55) asomando al fondo sobre el patio
    out.append(f'<rect x="{nx(8.30):.1f}" y="{ny(5.55):.1f}" width="{1.80*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.0"/>')
    # Ventana C-10 Baño Hijos (X=8.80..9.80, Z=4.75..5.35)
    out.append(f'<rect x="{nx(9.80):.1f}" y="{ny(5.35):.1f}" width="{1.00*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.0"/>')
    # Campo Solar Fotovoltaico en Azotea Alta (+6,50m): 12 paneles orientados a 30° Sur
    out.append(f'<polygon points="{nx(15.50):.1f},{ny(6.80):.1f} {nx(8.00):.1f},{ny(6.80):.1f} {nx(8.00):.1f},{ny(7.40):.1f} {nx(15.50):.1f},{ny(7.40):.1f}" fill="#0284c7" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{nx(11.75):.1f}" y="{ny(7.05):.1f}" text-anchor="middle" fill="#7dd3fc" font-family="monospace" font-size="5.2" font-weight="700">12 PANELES FV (5,40 kWp · AZOTEA ALTA +6,50 m)</text>')

    # 1.2 PRIMER PLANO: Planta Baja (Y=5.00m, Z=0..3.15m con Cubierta Inclinada Zinc 15%)
    # Volumen Despacho y Baño PB (X=17.00..6.15)
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(3.15):.1f}" width="{10.85*S:.1f}" height="{3.15*S:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>')
    # Zócalo de granito silvestre moreno h=1.10m
    out.append(f'<rect x="{nx(17.00):.1f}" y="{ny(1.10):.1f}" width="{10.85*S:.1f}" height="{1.10*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.9"/>')
    # Cubierta inclinada de zinc 15% sobre Despacho y Hall (Z=3.15..3.60m)
    out.append(f'<polygon points="{nx(17.00):.1f},{ny(3.15):.1f} {nx(6.15):.1f},{ny(3.15):.1f} {nx(6.15):.1f},{ny(3.55):.1f} {nx(17.00):.1f},{ny(3.55):.1f}" fill="#475569" stroke="#94a3b8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(11.50):.1f}" y="{ny(3.35):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="4.8">CUBIERTA ZINC 15% (AUTOLIMPIABLE)</text>')

    # Huecos en Fachada Norte PB:
    # Puerta Pivotante Iroko P-01 (X=7.25..8.35, Z=0..2.40m)
    out.append(f'<rect x="{nx(8.35):.1f}" y="{ny(2.40):.1f}" width="{1.10*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#fbbf24" stroke-width="1.3"/>')
    out.append(f'<circle cx="{nx(7.45):.1f}" cy="{ny(1.20):.1f}" r="2" fill="#fbbf24"/>')
    out.append(f'<text x="{nx(7.80):.1f}" y="{ny(2.55):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="5.2" font-weight="700">P-01 IROKO</text>')
    # Fijo Vidrio Hall (X=6.65..7.25, Z=0..2.40m)
    out.append(f'<rect x="{nx(7.25):.1f}" y="{ny(2.40):.1f}" width="{0.60*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.1"/>')
    # Ventana Despacho C-02 (X=10.80..12.60, Z=1.10..2.30m)
    out.append(f'<rect x="{nx(12.60):.1f}" y="{ny(2.30):.1f}" width="{1.80*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{nx(11.70):.1f}" y="{ny(1.70):.1f}" text-anchor="middle" fill="#e0f2fe" font-family="monospace" font-size="5.2">C-02 DESPACHO</text>')
    # Ventana Baño PB C-03 (X=14.15..15.15, Z=1.80..2.40m)
    out.append(f'<rect x="{nx(15.15):.1f}" y="{ny(2.40):.1f}" width="{1.00*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(14.65):.1f}" y="{ny(2.10):.1f}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="4.6">C-03 BAÑO</text>')

    # 1.3 Volumen Mudroom y Ala Técnica Oeste (X=6.15..3.85, Z=0..3.15m)
    out.append(f'<rect x="{nx(6.15):.1f}" y="{ny(3.15):.1f}" width="{2.30*S:.1f}" height="{3.15*S:.1f}" fill="#334155" stroke="#cbd5e1" stroke-width="1.3"/>')
    out.append(f'<text x="{nx(5.00):.1f}" y="{ny(1.60):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="5.0">MUDROOM PB</text>')

    # 1.4 Pérgola 2 Coches al Oeste (X=3.85..1.00, Z=0..2.90m)
    out.append(f'<rect x="{nx(3.85):.1f}" y="{ny(2.90):.1f}" width="{2.85*S:.1f}" height="{0.22*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<rect x="{nx(1.15):.1f}" y="{ny(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{nx(2.42):.1f}" y="{ny(1.50):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2">PÉRGOLA 2 COCHES</text>')

    # Cotas Horizontales Alzado Norte
    out.append(dim_h(nx(17.00), nx(6.15), gy1, 32, "10,85 m (Cuerpo Principal PB / P1)", "#38bdf8"))
    out.append(dim_h(nx(6.15), nx(3.85), gy1, 32, "2,30 m (Mudroom)", "#cbd5e1"))
    out.append(dim_h(nx(3.85), nx(1.00), gy1, 32, "2,85 m (Pérgola)", "#94a3b8"))
    out.append(dim_h(nx(17.00), nx(1.00), gy1, 56, "16,00 m (FRENTE TOTAL EDIFICACIÓN LÍNEA NORTE)", "#f8fafc"))

    # ==========================================================================
    # PANEL 2: ALZADO SUR (FACHADA PRINCIPAL JARDÍN Y PORCHE TECHADO · Y = 21,45 m)
    # Vista mirando hacia el Norte -> Izquierda es Oeste (X=1,00), Derecha es Este (X=17,00)
    # ==========================================================================
    out.append('<rect x="910" y="70" width="862" height="515" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="910" y="70" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="922" y="85" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">2. ALZADO SUR (FACHADA JARDÍN · EFECTO SOPORTAL) — De Oeste (X=1,00 m) a Este (X=17,80 m)</text>')

    gy2 = 465.0
    def sx(xm: float) -> float:
        return 970.0 + (xm - 1.00) * S

    def sy(zm: float) -> float:
        return gy2 - zm * S

    out.append(level_marks(sx(0.80), sx(18.00), gy2, [
        (0.00, "±0,00 m (Porche/PB)", "#10b981"),
        (3.15, "+3,15 m (Soportal / P1)", "#38bdf8"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
        (7.80, "+7,80 m (Chimenea Este)", "#f59e0b"),
    ]))

    for lbl, xm in [("B", 6.15), ("C", 10.00), ("D", 13.50), ("E", 17.00)]:
        xx = sx(xm)
        out.append(f'<line x1="{xx:.1f}" y1="102" x2="{xx:.1f}" y2="{gy2+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="102" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="105" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.2" font-weight="700">{lbl}</text>')

    # 2.1 PLANTA BAJA: PORCHE SUR TECHADO (Z=0..3,15m) CON EFECTO SOPORTAL CONTINUO
    # Fondo del porche en sombra (Y=18.45m al fondo)
    out.append(f'<rect x="{sx(6.15):.1f}" y="{sy(3.15):.1f}" width="{10.85*S:.1f}" height="{3.15*S:.1f}" fill="#0d1527" stroke="#334155" stroke-width="1.0"/>')
    # Grandes correderas elevables cota cero al fondo del porche:
    # Corredera Salón C-08 (X=6.80..11.60, Z=0..2.60)
    out.append(f'<rect x="{sx(6.80):.1f}" y="{sy(2.60):.1f}" width="{4.80*S:.1f}" height="{2.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<line x1="{sx(9.20):.1f}" y1="{sy(2.60):.1f}" x2="{sx(9.20):.1f}" y2="{sy(0.00):.1f}" stroke="#38bdf8" stroke-width="0.8"/>')
    # Corredera Comedor C-09 (X=12.60..15.80, Z=0..2.60)
    out.append(f'<rect x="{sx(12.60):.1f}" y="{sy(2.60):.1f}" width="{3.20*S:.1f}" height="{2.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.2"/>')
    # Churrasqueira tradicional de granito al fondo Este del porche
    out.append(f'<rect x="{sx(16.00):.1f}" y="{sy(2.80):.1f}" width="{0.95*S:.1f}" height="{2.80*S:.1f}" fill="#334155" stroke="#f59e0b" stroke-width="1.0"/>')
    out.append(f'<text x="{sx(16.48):.1f}" y="{sy(1.40):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.4" transform="rotate(-90 {sx(16.48):.1f} {sy(1.40):.1f})">CHURRASQUEIRA</text>')

    # Pilares estructurales de soporte del soportal en línea de fachada Sur (Y=21.45m)
    for p_x in [6.32, 10.00, 13.50, 16.82]:
        out.append(f'<rect x="{sx(p_x)-4:.1f}" y="{sy(3.15):.1f}" width="8" height="{3.15*S:.1f}" fill="#0f172a" stroke="#cbd5e1" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(11.50):.1f}" y="{sy(0.40):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.5" font-weight="700">PORCHE SUR EXPANDIDO (FONDO 3,00 m · CUBIERTO POR P1)</text>')

    # 2.2 PLANTA PRIMERA SUR (Z=3,15..6,80m · X=6.15..17.00):
    # Desplazada hacia el Sur, vuela a plomo sobre el porche. SATE Blanco Cálido NCS S 0502-Y.
    out.append(f'<rect x="{sx(6.15):.1f}" y="{sy(6.80):.1f}" width="{10.85*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{sx(6.10):.1f}" y="{sy(6.80):.1f}" width="{10.95*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')

    # Ventanales limpios de suelo a techo (sin barandilla de balcón saliente):
    # C-12 Ventanal Dormitorio Niña (X=7.00..9.40, Z=3.15..5.55)
    out.append(f'<rect x="{sx(7.00):.1f}" y="{sy(5.55):.1f}" width="{2.40*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{sx(8.20):.1f}" y1="{sy(5.55):.1f}" x2="{sx(8.20):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(8.20):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#34d399" font-family="monospace" font-size="5.2" font-weight="700">C-12 DORM. NIÑA (2,40m)</text>')

    # Paño Iroko entre D1 y D2 (X=9.40..10.20)
    out.append(f'<rect x="{sx(9.40):.1f}" y="{sy(5.55):.1f}" width="{0.80*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')

    # C-13 Ventanal Dormitorio Niño (X=10.20..12.60, Z=3.15..5.55)
    out.append(f'<rect x="{sx(10.20):.1f}" y="{sy(5.55):.1f}" width="{2.40*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{sx(11.40):.1f}" y1="{sy(5.55):.1f}" x2="{sx(11.40):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(11.40):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#34d399" font-family="monospace" font-size="5.2" font-weight="700">C-13 DORM. NIÑO (2,40m)</text>')

    # Paño Iroko entre D2 y Suite (X=12.60..13.80)
    out.append(f'<rect x="{sx(12.60):.1f}" y="{sy(5.55):.1f}" width="{1.20*S:.1f}" height="{2.40*S:.1f}" fill="#78350f" stroke="#d97706" stroke-width="0.8"/>')

    # C-14 Gran Ventanal Panorámico Master Suite (X=13.80..16.60, Z=3.15..5.55)
    out.append(f'<rect x="{sx(13.80):.1f}" y="{sy(5.55):.1f}" width="{2.80*S:.1f}" height="{2.40*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.4"/>')
    out.append(f'<line x1="{sx(15.20):.1f}" y1="{sy(5.55):.1f}" x2="{sx(15.20):.1f}" y2="{sy(3.15):.1f}" stroke="#38bdf8" stroke-width="0.9"/>')
    out.append(f'<text x="{sx(15.20):.1f}" y="{sy(5.80):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="5.2" font-weight="700">C-14 MASTER SUITE (2,80m)</text>')

    # 2.3 CHIMENEA ESCULTÓRICA EXTERIOR DE GRANITO MORENO EN FACHADA ESTE (OPCIÓN A)
    # X=17.00..17.80, Z=0..7.80m (+1,00m sobre coronación)
    out.append(f'<rect x="{sx(17.00):.1f}" y="{sy(7.80):.1f}" width="{0.80*S:.1f}" height="{7.80*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="1.4"/>')
    out.append(f'<rect x="{sx(16.95):.1f}" y="{sy(7.80):.1f}" width="{0.90*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<circle cx="{sx(17.40):.1f}" cy="{sy(7.95):.1f}" r="4" fill="#0f172a" stroke="#ef4444" stroke-width="1.0"/>')
    out.append(f'<text x="{sx(17.40):.1f}" y="{sy(8.15):.1f}" text-anchor="middle" fill="#ef4444" font-family="monospace" font-size="5.0" font-weight="700">CHIMENEA +7,80m</text>')
    out.append(f'<text x="{sx(17.40):.1f}" y="{sy(4.50):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="4.6" transform="rotate(-90 {sx(17.40):.1f} {sy(4.50):.1f})">GRANITO MORENO (EXTERIOR ESTE)</text>')

    # Cotas Horizontales Alzado Sur
    out.append(dim_h(sx(6.15), sx(10.00), gy2, 32, "3,85 m (Dorm. Niña)", "#34d399"))
    out.append(dim_h(sx(10.00), sx(13.50), gy2, 32, "3,50 m (Dorm. Niño)", "#34d399"))
    out.append(dim_h(sx(13.50), sx(17.00), gy2, 32, "3,50 m (Master Suite)", "#38bdf8"))
    out.append(dim_h(sx(17.00), sx(17.80), gy2, 32, "0,80m", "#f59e0b"))
    out.append(dim_h(sx(6.15), sx(17.80), gy2, 56, "11,65 m (FRENTE SUR TOTAL 2 PLANTAS + CHIMENEA ESTE)", "#f8fafc"))

    # ==========================================================================
    # PANEL 3: ALZADO ESTE (FACHADA LATERAL DERECHA · X = 17,00 m)
    # Vista mirando hacia el Oeste -> Izquierda es Sur (Y=21,45), Derecha es Norte (Y=5,00)
    # ==========================================================================
    out.append('<rect x="28" y="600" width="862" height="535" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="28" y="600" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="40" y="615" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">3. ALZADO ESTE (FACHADA LATERAL · X = 17,00 m) — De Sur (Y=21,45 m) a Norte (Y=5,00 m)</text>')

    gy3 = 1005.0
    def ex(ym: float) -> float:
        return 115.0 + (22.00 - ym) * S

    def ey(zm: float) -> float:
        return gy3 - zm * S

    out.append(level_marks(ex(22.00), ex(4.50), gy3, [
        (0.00, "±0,00 m (PB)", "#10b981"),
        (3.15, "+3,15 m (Forjado P1)", "#38bdf8"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
        (7.80, "+7,80 m (Chimenea)", "#f59e0b"),
    ]))

    for lbl, ym in [("5", 21.45), ("4", 17.50), ("3B", 14.30), ("3", 11.70), ("2", 8.50), ("1", 5.00)]:
        xx = ex(ym)
        out.append(f'<line x1="{xx:.1f}" y1="632" x2="{xx:.1f}" y2="{gy3+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="632" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="635" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.0" font-weight="700">{lbl}</text>')

    # 3.1 PLANTA BAJA ESTE (Y=5.00..21.45m · 16,45 m):
    # Zócalo granito + SATE blanco
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(3.15):.1f}" width="{16.45*S:.1f}" height="{3.15*S:.1f}" fill="#1e293b" stroke="#e2e8f0" stroke-width="1.5"/>')
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(1.10):.1f}" width="{16.45*S:.1f}" height="{1.10*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="0.9"/>')
    # Ventana Cocina Este (Y=9.50..11.00, Z=1.10..2.30m)
    out.append(f'<rect x="{ex(11.00):.1f}" y="{ey(2.30):.1f}" width="{1.50*S:.1f}" height="{1.20*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.1"/>')
    out.append(f'<text x="{ex(10.25):.1f}" y="{ey(1.70):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="4.8">COCINA SANTOS</text>')

    # 3.2 PLANTA PRIMERA ESTE: Solo ocupa Y=14.30..21.45m (7,15 m de fondo · Z=3.15..6.80m)
    # ¡La zona Norte Y=5.00..14.30m es de 1 PLANTA!
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(6.80):.1f}" width="{7.15*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{ex(21.50):.1f}" y="{ey(6.80):.1f}" width="{7.25*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    # Ventana C-11 Baño Suite (Y=15.20..16.20, Z=4.75..5.35m)
    out.append(f'<rect x="{ex(16.20):.1f}" y="{ey(5.35):.1f}" width="{1.00*S:.1f}" height="{0.60*S:.1f}" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.0"/>')
    out.append(f'<text x="{ex(15.70):.1f}" y="{ey(5.55):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.6">C-11 BAÑO SUITE</text>')

    # Cubierta de zinc 15% de Planta Baja visible en Norte (Y=5.00..14.30m, Z=3.15..3.55m)
    out.append(f'<polygon points="{ex(14.30):.1f},{ey(3.15):.1f} {ex(5.00):.1f},{ey(3.15):.1f} {ex(5.00):.1f},{ey(3.55):.1f} {ex(14.30):.1f},{ey(3.15):.1f}" fill="#475569" stroke="#94a3b8" stroke-width="1.0"/>')
    out.append(f'<text x="{ex(9.65):.1f}" y="{ey(3.40):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="4.8">CUBIERTA INCLINADA ZINC 15% (1 PLANTA)</text>')

    # 3.3 CHIMENEA EXTERIOR DE GRANITO MORENO EN FACHADA ESTE (OPCIÓN A)
    # Adosada al extremo Sur (Y=20.65..21.45m), sube hasta +7.80m
    out.append(f'<rect x="{ex(21.45):.1f}" y="{ey(7.80):.1f}" width="{0.80*S:.1f}" height="{7.80*S:.1f}" fill="#334155" stroke="#94a3b8" stroke-width="1.4"/>')
    out.append(f'<rect x="{ex(21.50):.1f}" y="{ey(7.80):.1f}" width="{0.90*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<text x="{ex(21.05):.1f}" y="{ey(8.15):.1f}" text-anchor="middle" fill="#ef4444" font-family="monospace" font-size="5.0" font-weight="700">TIRO BBQ +7,80m</text>')
    out.append(f'<text x="{ex(21.05):.1f}" y="{ey(4.50):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.6" transform="rotate(-90 {ex(21.05):.1f} {ey(4.50):.1f})">CHIMENEA GRANITO ADOSADA EXTERIOR</text>')

    # Cotas Horizontales Alzado Este
    out.append(dim_h(ex(21.45), ex(14.30), gy3, 32, "7,15 m (Cuerpo P1)", "#38bdf8"))
    out.append(dim_h(ex(14.30), ex(5.00), gy3, 32, "9,30 m (1 Planta PB Norte)", "#10b981"))
    out.append(dim_h(ex(21.45), ex(5.00), gy3, 56, "16,45 m (LONGITUD TOTAL ENVOLVENTE ESTE)", "#f8fafc"))

    # ==========================================================================
    # PANEL 4: ALZADO OESTE (FACHADA SERVICIO Y BLINDAJE ATLÁNTICO · X = 1,00 / 3,85 / 6,15 m)
    # Vista mirando hacia el Este -> Izquierda es Norte (Y=5,00), Derecha es Sur (Y=21,45)
    # ==========================================================================
    out.append('<rect x="910" y="600" width="862" height="535" fill="url(#grid-minor)" stroke="#334155" stroke-width="0.8"/>')
    out.append('<rect x="910" y="600" width="862" height="22" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>')
    out.append('<text x="922" y="615" fill="#38bdf8" font-family="monospace" font-size="8.0" font-weight="700">4. ALZADO OESTE (FACHADA SERVICIO Y PROTECCIÓN TEMPORALES) — De Norte a Sur</text>')

    gy4 = 1005.0
    def wx(ym: float) -> float:
        return 970.0 + (ym - 4.50) * S

    def wy(zm: float) -> float:
        return gy4 - zm * S

    out.append(level_marks(wx(4.50), wx(22.00), gy4, [
        (0.00, "±0,00 m (PB)", "#10b981"),
        (2.90, "+2,90 m (Pérgola)", "#94a3b8"),
        (3.15, "+3,15 m (Cub. Oeste / Forjado P1)", "#38bdf8"),
        (6.80, "+6,80 m (Coronación P1)", "#f8fafc"),
    ]))

    for lbl, ym in [("1", 5.00), ("2", 8.50), ("3", 11.70), ("3B", 14.30), ("4", 17.50), ("5", 21.45)]:
        xx = wx(ym)
        out.append(f'<line x1="{xx:.1f}" y1="632" x2="{xx:.1f}" y2="{gy4+15:.1f}" stroke="#f59e0b" stroke-width="0.55" stroke-dasharray="6,3" opacity="0.65"/>')
        out.append(f'<circle cx="{xx:.1f}" cy="632" r="7.5" fill="#0f172a" stroke="#f59e0b" stroke-width="1.0"/>')
        out.append(f'<text x="{xx:.1f}" y="635" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="6.0" font-weight="700">{lbl}</text>')

    # 4.1 SEGUNDO PLANO: Volumen Planta Primera SATE blanco (Y=14.30..21.45, Z=3.15..6.80m · CIEGO)
    out.append(f'<rect x="{wx(14.30):.1f}" y="{wy(6.80):.1f}" width="{7.15*S:.1f}" height="{3.65*S:.1f}" fill="#26334d" stroke="#f8fafc" stroke-width="1.6"/>')
    out.append(f'<rect x="{wx(14.25):.1f}" y="{wy(6.80):.1f}" width="{7.25*S:.1f}" height="{0.15*S:.1f}" fill="#475569" stroke="#f8fafc" stroke-width="1.0"/>')
    out.append(f'<text x="{wx(17.85):.1f}" y="{wy(5.20):.1f}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="5.2" font-weight="700">FACHADA OESTE P1 CIEGA (SATE BLANCO · BLINDAJE TÉRMICO)</text>')

    # 4.2 PRIMER PLANO: Muro de Granito / Servicio Oeste en PB (Y=5.00..21.45m · 16,45 m)
    out.append(f'<rect x="{wx(5.00):.1f}" y="{wy(3.15):.1f}" width="{16.45*S:.1f}" height="{3.15*S:.1f}" fill="#334155" stroke="#e2e8f0" stroke-width="1.5"/>')
    # Puerta Mudroom exterior P-02 (Y=6.40..7.30, Z=0..2.10)
    out.append(f'<rect x="{wx(6.40):.1f}" y="{wy(2.10):.1f}" width="{0.90*S:.1f}" height="{2.10*S:.1f}" fill="#78350f" stroke="#fbbf24" stroke-width="1.2"/>')
    out.append(f'<text x="{wx(6.85):.1f}" y="{wy(2.30):.1f}" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="4.8">P-02 MUDROOM</text>')
    # Puerta Sala Técnica / Surf P-05 (Y=9.80..10.80, Z=0..2.10)
    out.append(f'<rect x="{wx(9.80):.1f}" y="{wy(2.10):.1f}" width="{1.00*S:.1f}" height="{2.10*S:.1f}" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>')
    out.append(f'<text x="{wx(10.30):.1f}" y="{wy(2.30):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.8">P-05 SURF/TÉCNICA</text>')
    # Lucernario Velux SunTunnel en cubierta Oeste (+3,15m)
    out.append(f'<ellipse cx="{wx(9.00):.1f}" cy="{wy(3.25):.1f}" rx="{0.30*S:.1f}" ry="{0.12*S:.1f}" fill="#38bdf8" stroke="#0284c7" stroke-width="1.1"/>')
    out.append(f'<text x="{wx(9.00):.1f}" y="{wy(3.45):.1f}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="4.4">VELUX SUNTUNNEL</text>')

    # Pérgola Coches en primer término (Y=5.00..11.80, Z=0..2.90m)
    out.append(f'<rect x="{wx(5.00):.1f}" y="{wy(2.90):.1f}" width="{6.80*S:.1f}" height="{0.22*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.3"/>')
    for px_c in [5.10, 8.40, 11.70]:
        out.append(f'<rect x="{wx(px_c):.1f}" y="{wy(2.68):.1f}" width="{0.15*S:.1f}" height="{2.68*S:.1f}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.0"/>')

    # Cotas Horizontales Alzado Oeste
    out.append(dim_h(wx(5.00), wx(11.80), gy4, 32, "6,80 m (Pérgola + Mudroom/Surf)", "#38bdf8"))
    out.append(dim_h(wx(11.80), wx(21.45), gy4, 32, "9,65 m (Salón y Cierre Porche)", "#cbd5e1"))
    out.append(dim_h(wx(5.00), wx(21.45), gy4, 56, "16,45 m (LONGITUD TOTAL ENVOLVENTE OESTE)", "#f8fafc"))

    out.append(title_block(
        28, H - 155, W - 56, 128,
        plano_id="A-03",
        title="ALZADOS EXTERIORES DE LAS 4 FACHADAS (NORTE, SUR, ESTE Y OESTE)",
        scale="1:100 (Cotas en m)",
        phase="PROYECTO DE EJECUCIÓN (VERSIÓN OPTIMIZADA PASSIVHAUS ~165 m²)",
        subtitle="Efecto Soportal Atlántico Sur · Desfase Volumétrico · Chimenea Exterior Este (+7,80 m) · Solar FV (+6,50 m)",
        extra_notes=[
            "Alzado Norte: Acceso protegido P-01 (1,10m Iroko), Despacho C-02 (1,80m), Baño PB C-03; Planta Primera al fondo con C-10 y Mirador C-15A",
            "Alzado Sur: Porche de 3,00m de fondo cubierto por P1 (efecto soportal continuo); ventanales de suelo a techo C-12, C-13 y C-14 sin terrazas sucias",
            "Alzado Este: Muro de cocina y churrasqueira; chimenea escultórica de granito moreno gallego (Opción A) adosada al exterior hasta +7,80 m",
            "Alzado Oeste: Muro de granito de 16,45m continuo de alta inercia térmica contra temporales atlánticos; P1 ciega al fondo con SATE blanco",
        ]
    ))

    out.append("</svg>")
    return sanitize_svg_text("\n".join(out))


# ==============================================================================
# 2. GENERADOR DE VISTAS 3D MATEMÁTICAS ESTRICTAS (GUÍAS DE GEOMETRÍA PARA IA)
# ==============================================================================
def get_strict_3d_faces():
    faces = []

    def cy(y_cad):
        return 30.0 - y_cad

    def add_subdivided_quad(p00, p10, p11, p01, color, edgecolor, alpha=1.0, layer=1, bias=0.0, nx=4, ny=4):
        for i in range(nx):
            u0, u1 = i / nx, (i + 1) / nx
            for j in range(ny):
                v0, v1 = j / ny, (j + 1) / ny
                def interp(u, v):
                    return tuple(
                        (1 - u) * (1 - v) * p00[k]
                        + u * (1 - v) * p10[k]
                        + u * v * p11[k]
                        + (1 - u) * v * p01[k]
                        for k in range(3)
                    )
                verts = [interp(u0, v0), interp(u1, v0), interp(u1, v1), interp(u0, v1)]
                faces.append((verts, color, edgecolor, alpha, layer, bias))

    def add_box(x0, x1, y0_cad, y1_cad, z0, z1, color, edgecolor="#334155", alpha=1.0, layer=1, bias=0.0):
        ya, yb = cy(y1_cad), cy(y0_cad)
        nx = max(1, int(round(abs(x1 - x0) / 1.2)))
        ny = max(1, int(round(abs(yb - ya) / 1.2)))
        nz = max(1, int(round(abs(z1 - z0) / 1.2)))

        # 6 caras
        add_subdivided_quad((x0, ya, z0), (x1, ya, z0), (x1, ya, z1), (x0, ya, z1), color, edgecolor, alpha, layer, bias, nx, nz) # y = ya (Sur)
        add_subdivided_quad((x1, yb, z0), (x0, yb, z0), (x0, yb, z1), (x1, yb, z1), color, edgecolor, alpha, layer, bias, nx, nz) # y = yb (Norte)
        add_subdivided_quad((x0, yb, z0), (x0, ya, z0), (x0, ya, z1), (x0, yb, z1), color, edgecolor, alpha, layer, bias, ny, nz) # x = x0 (Oeste)
        add_subdivided_quad((x1, ya, z0), (x1, yb, z0), (x1, yb, z1), (x1, ya, z1), color, edgecolor, alpha, layer, bias, ny, nz) # x = x1 (Este)
        add_subdivided_quad((x0, ya, z1), (x1, ya, z1), (x1, yb, z1), (x0, yb, z1), color, edgecolor, alpha, layer, bias, nx, ny) # z = z1 (Techo)
        add_subdivided_quad((x0, yb, z0), (x1, yb, z0), (x1, ya, z0), (x0, ya, z0), color, edgecolor, alpha, layer, bias, nx, ny) # z = z0 (Suelo)

    def add_rect_on_y(x0, x1, y_cad, z0, z1, color, edgecolor="#0f172a", alpha=1.0, layer=1, bias=-0.35):
        yy = cy(y_cad)
        nx = max(1, int(round(abs(x1 - x0) / 1.0)))
        nz = max(1, int(round(abs(z1 - z0) / 1.0)))
        add_subdivided_quad((x0, yy, z0), (x1, yy, z0), (x1, yy, z1), (x0, yy, z1), color, edgecolor, alpha, layer, bias, nx, nz)

    def add_rect_on_x(x_cad, y0_cad, y1_cad, z0, z1, color, edgecolor="#0f172a", alpha=1.0, layer=1, bias=-0.35):
        ya, yb = cy(y1_cad), cy(y0_cad)
        ny = max(1, int(round(abs(yb - ya) / 1.0)))
        nz = max(1, int(round(abs(z1 - z0) / 1.0)))
        add_subdivided_quad((x_cad, ya, z0), (x_cad, yb, z0), (x_cad, yb, z1), (x_cad, ya, z1), color, edgecolor, alpha, layer, bias, ny, nz)

    def add_rect_on_z(x0, x1, y0_cad, y1_cad, z_val, color, edgecolor="#0f172a", alpha=1.0, layer=0, bias=0.0):
        ya, yb = cy(y1_cad), cy(y0_cad)
        nx = max(1, int(round(abs(x1 - x0) / 1.5)))
        ny = max(1, int(round(abs(yb - ya) / 1.5)))
        add_subdivided_quad((x0, ya, z_val), (x1, ya, z_val), (x1, yb, z_val), (x0, yb, z_val), color, edgecolor, alpha, layer, bias, nx, ny)

    # CAPA 0: Suelo Parcela Césped (20 x 30 m), Porches y Suelo de Patio Claustro
    add_rect_on_z(0, 20, 0, 30, 0.0, "#4d7c0f", "#3f6212", 1.0, layer=0, bias=1.5)
    add_rect_on_z(1.0, 4.0, 0.0, 12.0, 0.02, "#94a3b8", "#64748b", 1.0, layer=0, bias=0.6)
    add_rect_on_z(7.0, 9.3, 0.0, 5.0, 0.02, "#cbd5e1", "#94a3b8", 1.0, layer=0, bias=0.6)
    # Tarima Iroko Porche Sur (X=6.15..17.00, Y=18.45..21.45)
    add_rect_on_z(6.15, 17.00, 18.45, 21.45, 0.04, "#92400e", "#78350f", 1.0, layer=0, bias=-0.3)
    # Suelo Patio Claustro (X=10.00..13.20, Y=8.50..11.70)
    add_rect_on_z(10.00, 13.20, 8.50, 11.70, 0.06, "#92400e", "#78350f", 1.0, layer=0, bias=-0.4)

    # CAPA 1: VOLÚMENES ARQUITECTÓNICOS
    # 1. Pérgola 2 Coches (X=1.00..3.85, Y=5.00..12.00, Z=0..2.90m)
    add_box(1.00, 3.85, 5.00, 12.00, 2.72, 2.90, "#1f2937", "#0f172a", 1.0, layer=1)
    for py_c in [5.15, 8.40, 11.60]:
        add_box(1.05, 1.25, py_c, py_c + 0.20, 0.0, 2.72, "#1f2937", "#0f172a", 1.0, layer=1)

    # 2. Ala Oeste (Mudroom y Sala Técnica X=3.85..6.15, Y=5.00..12.50, Z=0..3.15m) en Granito
    add_box(3.85, 6.15, 5.00, 12.50, 0.0, 3.15, "#9ca3af", "#4b5563", 1.0, layer=1)

    # 3. Planta Baja Norte (Despacho, Hall, Baño PB X=6.15..17.00, Y=5.00..8.50, Z=0..3.15m)
    add_box(6.15, 17.00, 5.00, 8.50, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)

    # 4. Cocina PB Este (X=13.20..17.00, Y=8.50..12.00, Z=0..3.15m)
    add_box(13.20, 17.00, 8.50, 12.00, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)

    # 5. Escalera / Conexión Oeste del Patio (X=6.15..10.00, Y=8.50..14.30, Z=0..3.15m)
    add_box(6.15, 10.00, 8.50, 14.30, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)

    # 6. Salón PB (X=6.15..17.00, Y=14.30..18.45, Z=0..3.15m)
    add_box(6.15, 17.00, 14.30, 18.45, 0.0, 3.15, "#d6d3d1", "#78716c", 1.0, layer=1)

    # 7. Porche Sur Soportal (X=6.15..17.00, Y=18.45..21.45, Z=0..3.15m cubierto por P1)
    # Pilares en borde Sur Y=21.45m
    for px_s in [6.32, 10.00, 13.50, 16.82]:
        add_box(px_s - 0.12, px_s + 0.12, 21.35, 21.45, 0.0, 3.15, "#0f172a", "#cbd5e1", 1.0, layer=1)

    # 8. PLANTA PRIMERA (X=6.15..17.00, Y=14.30..21.45, Z=3.15..6.80m)
    # SATE Blanco Cálido en 4 fachadas
    add_box(6.15, 17.00, 14.30, 21.45, 3.15, 6.80, "#f8fafc", "#cbd5e1", 1.0, layer=1)

    # 9. CHIMENEA EXTERIOR DE GRANITO MORENO EN FACHADA ESTE (OPCIÓN A)
    # X=17.00..17.80, Y=20.65..21.45, Z=0..7.80m (+1,00m sobre cubierta)
    add_box(17.00, 17.80, 20.65, 21.45, 0.0, 7.80, "#334155", "#1f2937", 1.0, layer=1, bias=-0.2)

    # 10. CAMPO SOLAR FOTOVOLTAICO EN CUBIERTA SUPERIOR (+6,50m)
    # 12 Paneles solares sobre P1 (X=8.00..15.50, Y=14.80..20.80, Z=6.85..7.15m)
    for r in range(4):
        ry = 15.20 + r * 1.35
        for c in range(3):
            cx = 8.50 + c * 2.30
            add_box(cx, cx + 2.00, ry, ry + 1.10, 6.85, 7.10, "#1e3a8a", "#38bdf8", 1.0, layer=1, bias=-0.4)

    # 11. Acer Palmatum en Patio Claustro (X=11.60, Y=10.10)
    add_box(11.45, 11.75, 9.95, 10.25, 0.06, 2.30, "#451a03", "#290f02", 1.0, layer=1)
    add_box(10.60, 12.60, 9.10, 11.10, 2.10, 4.80, "#b91c1c", "#7f1d1d", 0.95, layer=1)

    # CARPINTERÍAS FRONTALES:
    # --- FACHADA NORTE PB (Y = 4.92) ---
    add_rect_on_y(7.25, 8.35, 4.92, 0.0, 2.40, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)  # P-01
    add_rect_on_y(6.65, 7.25, 4.92, 0.0, 2.40, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # Fijo Hall
    add_rect_on_y(10.80, 12.60, 4.92, 1.10, 2.30, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-02 Despacho
    add_rect_on_y(14.15, 15.15, 4.92, 1.80, 2.40, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-03 Baño PB

    # --- FACHADA NORTE P1 (Y = 14.22) ---
    add_rect_on_y(6.50, 8.30, 14.22, 3.15, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-15A Galería
    add_rect_on_y(8.80, 9.80, 14.22, 4.75, 5.35, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-10 Baño Hijos

    # --- FACHADA SUR PB (Y = 18.52 al fondo del porche) ---
    add_rect_on_y(6.80, 11.60, 18.52, 0.05, 2.65, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-08 Corredera Salón
    add_rect_on_y(12.60, 15.80, 18.52, 0.05, 2.65, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-09 Corredera Comedor

    # --- FACHADA SUR P1 (Y = 21.48 borde del soportal) ---
    add_rect_on_y(7.00, 9.40, 21.48, 3.15, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # C-12 Dorm. Niña
    add_rect_on_y(9.40, 10.20, 21.48, 3.15, 5.55, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)  # Paño Iroko
    add_rect_on_y(10.20, 12.60, 21.48, 3.15, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-13 Dorm. Niño
    add_rect_on_y(12.60, 13.80, 21.48, 3.15, 5.55, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)# Paño Iroko
    add_rect_on_y(13.80, 16.60, 21.48, 3.15, 5.55, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-14 Master Suite

    # --- FACHADA ESTE (X = 17.08) ---
    add_rect_on_x(17.08, 9.50, 11.00, 1.10, 2.30, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5) # Ventana Cocina
    add_rect_on_x(17.08, 15.20, 16.20, 4.75, 5.35, "#0284c7", "#0f172a", 0.90, layer=1, bias=-0.5)# C-11 Baño Suite

    # --- FACHADA OESTE (X = 3.78) ---
    add_rect_on_x(3.78, 6.40, 7.30, 0.0, 2.10, "#78350f", "#451a03", 1.0, layer=1, bias=-0.5)    # P-02 Mudroom
    add_rect_on_x(3.78, 9.80, 10.80, 0.0, 2.10, "#1e293b", "#0f172a", 0.95, layer=1, bias=-0.5)  # P-05 Surf

    return faces


def render_guide_view(faces, elev_deg: float, azim_deg: float, title: str, out_path: str, cam_dist=42.0, cx=10.0, cy_target=15.0, cz=3.4, W=1536, H=1024):
    img = Image.new("RGBA", (W, H), (7, 11, 20, 255))
    draw = ImageDraw.Draw(img)

    rad_elev = math.radians(elev_deg)
    rad_azim = math.radians(azim_deg)
    cam_x = cx + cam_dist * math.cos(rad_elev) * math.sin(rad_azim)
    cam_y = cy_target - cam_dist * math.cos(rad_elev) * math.cos(rad_azim)
    cam_z = cz + cam_dist * math.sin(rad_elev)

    fx, fy, fz = cx - cam_x, cy_target - cam_y, cz - cam_z
    f_len = math.sqrt(fx * fx + fy * fy + fz * fz)
    fx, fy, fz = fx / f_len, fy / f_len, fz / f_len

    rx = fy * 0.0 - fz * 0.0
    ry = fz * 0.0 - fx * 1.0
    rz = fx * 0.0 - fy * 0.0
    rx, ry, rz = -fy, fx, 0.0
    r_len = math.sqrt(rx * rx + ry * ry)
    if r_len > 1e-6:
        rx, ry, rz = rx / r_len, ry / r_len, 0.0
    else:
        rx, ry, rz = 1.0, 0.0, 0.0

    upx = ry * fz - rz * fy
    upy = rz * fx - rx * fz
    upz = rx * fy - ry * fx
    up_len = math.sqrt(upx * upx + upy * upy + upz * upz)
    upx, upy, upz = upx / up_len, upy / up_len, upz / up_len

    focal = W * 0.95
    projected_polys = []

    for verts, col_hex, edge_hex, alpha, layer, bias in faces:
        pts_2d = []
        dists = []
        valid = True
        for vx, vy, vz in verts:
            dx, dy, dz = vx - cam_x, vy - cam_y, vz - cam_z
            depth = dx * fx + dy * fy + dz * fz
            if depth <= 1.0:
                valid = False
                break
            x_cam = dx * rx + dy * ry + dz * rz
            y_cam = dx * upx + dy * upy + dz * upz
            sx = W / 2.0 + (x_cam / depth) * focal
            sy = H / 2.0 - (y_cam / depth) * focal
            pts_2d.append((sx, sy))
            dists.append(math.sqrt(dx * dx + dy * dy + dz * dz))
        if valid:
            avg_dist = sum(dists) / len(dists) + bias
            projected_polys.append((layer, -avg_dist, pts_2d, hex_to_rgba(col_hex, alpha), hex_to_rgba(edge_hex, min(1.0, alpha + 0.2))))

    projected_polys.sort(key=lambda item: (item[0], item[1]))

    for _, _, pts_2d, fill_rgba, edge_rgba in projected_polys:
        draw.polygon(pts_2d, fill=fill_rgba, outline=edge_rgba, width=1)

    img.convert("RGB").save(out_path, "PNG")
    print(f"Rendered 3D guide: {out_path}")


def hex_to_rgba(hex_code: str, alpha=1.0):
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return (r, g, b, int(alpha * 255))


def main():
    svg_str = build_4_elevations_svg()
    for p in [
        os.path.join(BASE_DIR, "plano_alzados_exteriores_4_caras.svg"),
        os.path.join(BASE_DIR, "propuestas", "plano_alzados_exteriores_4_caras.svg"),
    ]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_str)
        print(f"Written {p} ({len(svg_str)} bytes)")

    faces = get_strict_3d_faces()
    render_guide_view(faces, elev_deg=11, azim_deg=84, title="Fachada Norte", out_path=os.path.join(GUIDES_DIR, "guide_norte.png"))
    render_guide_view(faces, elev_deg=11, azim_deg=-84, title="Fachada Sur", out_path=os.path.join(GUIDES_DIR, "guide_sur.png"))
    render_guide_view(faces, elev_deg=11, azim_deg=-6, title="Fachada Este", out_path=os.path.join(GUIDES_DIR, "guide_este.png"))
    render_guide_view(faces, elev_deg=12, azim_deg=174, title="Fachada Oeste", out_path=os.path.join(GUIDES_DIR, "guide_oeste.png"))
    render_guide_view(faces, elev_deg=41, azim_deg=-122, title="Perspectiva Superior", out_path=os.path.join(GUIDES_DIR, "guide_aerea.png"), cam_dist=35.0, cz=2.2)


if __name__ == "__main__":
    main()
