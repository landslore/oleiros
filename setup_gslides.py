#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configura la presentación en Google Slides con diapositivas elegantes y sube las imágenes renderizadas.
"""

import json
import subprocess
import os

PRES_ID = "1AHYDhaDiH4zxxbKxN8ffe-7R8t2RK37y-VMJbs5lKhw"
RENDERS_DIR = "/home/antigravity/landslore/oleiros/propuestas/renders"

batch_ops = [
    # Slide 1: Portada (p is default slide)
    {"op": "delete-element", "element": "i0"},
    {"op": "delete-element", "element": "i1"},
    {"op": "set-background", "slide": "p", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "p", "text": "PROYECTO DE EJECUCIÓN · VIVIENDA UNIFAMILIAR", "x": 40, "y": 60, "width": 640, "height": 30, "font_size": 11, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "p", "text": "Hogar Oleiros — Propuesta D", "x": 40, "y": 95, "width": 640, "height": 55, "font_size": 34, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "p", "text": "Pabellón Bioclimático en Liáns / Santa Cruz (Oleiros)\nPatio Corrala Habitable · Doble Acceso · Aislamiento Acústico · Estándar Passivhaus", "x": 40, "y": 155, "width": 640, "height": 45, "font_size": 13, "color": "#F59E0B", "font_family": "Roboto"},
    {"op": "set-notes", "slide": "p", "text": "Presentación ejecutiva de la Propuesta D. Vivienda unifamiliar aislada en parcela de 600 m² en Oleiros."},

    # Slide 2: Patio Corrala
    {"op": "add-slide", "layout": "BLANK", "id": "SLIDE_PATIO"},
    {"op": "set-background", "slide": "SLIDE_PATIO", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "SLIDE_PATIO", "text": "EL CORAZÓN DE LA VIVIENDA", "x": 40, "y": 20, "width": 640, "height": 20, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "SLIDE_PATIO", "text": "05. Patio Corrala Habitable y 100% Accesible", "x": 40, "y": 40, "width": 640, "height": 35, "font_size": 22, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "SLIDE_PATIO", "text": "• 16,0 m² abiertos al cielo con drenaje natural sobre terreno real.\n• Arce japonés palmatum + helechos atlánticos.\n• Tarima de iroko a cota cero y banco corrido bajo alero de 80 cm.\n• 3 correderas Cortizo Cor Vision Plus abriendo a Cocina, Salón y Galería.", "x": 410, "y": 100, "width": 280, "height": 240, "font_size": 11, "color": "#CBD5E1", "font_family": "Roboto", "line_spacing": 140},

    # Slide 3: Zona de Día
    {"op": "add-slide", "layout": "BLANK", "id": "SLIDE_LIVING"},
    {"op": "set-background", "slide": "SLIDE_LIVING", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "SLIDE_LIVING", "text": "ESPACIO DIÁFANO INTEGRADO", "x": 40, "y": 20, "width": 640, "height": 20, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "SLIDE_LIVING", "text": "06-08. Salón, Comedor, Cocina con Isla y Porche", "x": 40, "y": 40, "width": 640, "height": 35, "font_size": 22, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "SLIDE_LIVING", "text": "• Isla central Dekton Kelya con campana integrada Bora Pure.\n• Mesa de roble macizo para 10 comensales.\n• Chimenea estanca de leña empotrada con toma exterior dedicada.\n• Continuidad espacial directa hacia el Porche Sur y hacia el Patio Corrala.", "x": 410, "y": 100, "width": 280, "height": 240, "font_size": 11, "color": "#CBD5E1", "font_family": "Roboto", "line_spacing": 140},

    # Slide 4: Despacho
    {"op": "add-slide", "layout": "BLANK", "id": "SLIDE_DESPACHO"},
    {"op": "set-background", "slide": "SLIDE_DESPACHO", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "SLIDE_DESPACHO", "text": "TELETRABAJO INTENSIVO & SUITE DE INVITADOS", "x": 40, "y": 20, "width": 640, "height": 20, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "SLIDE_DESPACHO", "text": "03. Despacho Sanctasanctórum & Suite Serena", "x": 40, "y": 40, "width": 640, "height": 35, "font_size": 22, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "SLIDE_DESPACHO", "text": "• Mesa orientada con luz lateral a 90° de ventana Norte (cero reflejos).\n• Vistas al Patio Claustro para relax visual.\n• Puerta acústica Rw ≥ 38 dB y panel fonoabsorbente de lamas de roble.\n• Sofá-cama matrimonio con acceso privado al Baño PB.", "x": 410, "y": 100, "width": 280, "height": 240, "font_size": 11, "color": "#CBD5E1", "font_family": "Roboto", "line_spacing": 140},

    # Slide 5: Suite P1
    {"op": "add-slide", "layout": "BLANK", "id": "SLIDE_SUITE"},
    {"op": "set-background", "slide": "SLIDE_SUITE", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "SLIDE_SUITE", "text": "ALA ESTE PRIVADA EN PLANTA PRIMERA", "x": 40, "y": 20, "width": 640, "height": 20, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "SLIDE_SUITE", "text": "16. Suite Principal de Matrimonio (31,2 m²)", "x": 40, "y": 40, "width": 640, "height": 35, "font_size": 22, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "SLIDE_SUITE", "text": "• Cama King Size mirando al Sur hacia el jardín y piscina.\n• Balcón corrido con barandilla de vidrio estructural 10+10 mm sin montantes.\n• Vestidor de paso en doble hilera con frentes de vidrio ahumado y LED.\n• Baño privado con ducha doble walk-in y doble seno Dekton.", "x": 410, "y": 100, "width": 280, "height": 240, "font_size": 11, "color": "#CBD5E1", "font_family": "Roboto", "line_spacing": 140},

    # Slide 6: Porche Sur
    {"op": "add-slide", "layout": "BLANK", "id": "SLIDE_PORCHE"},
    {"op": "set-background", "slide": "SLIDE_PORCHE", "color": "#0B0F19"},
    {"op": "add-textbox", "slide": "SLIDE_PORCHE", "text": "VIDA EXTERIOR PROTEGIDA DE LA LLUVIA", "x": 40, "y": 20, "width": 640, "height": 20, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto"},
    {"op": "add-textbox", "slide": "SLIDE_PORCHE", "text": "10. Porche Sur Expandido (Fondo 3,00 m)", "x": 40, "y": 40, "width": 640, "height": 35, "font_size": 22, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
    {"op": "add-textbox", "slide": "SLIDE_PORCHE", "text": "• 36 m² cubiertos con fondo real de 3 metros.\n• Churrasqueira de granito negro Zimbabwe con campana y leñera.\n• Comedor exterior para 10 personas + zona lounge.\n• Conexión visual y directa con la piscina y césped.", "x": 410, "y": 100, "width": 280, "height": 240, "font_size": 11, "color": "#CBD5E1", "font_family": "Roboto", "line_spacing": 140}
]

# Write batch JSON
batch_file = "/tmp/gslides_batch.json"
with open(batch_file, "w", encoding="utf-8") as f:
    json.dump(batch_ops, f, indent=2)

print("Executing batch update on Google Slides...")
res = subprocess.run(["gslides", "mutate", "batch", PRES_ID, "-f", batch_file, "--json"], capture_output=True, text=True)
print("Batch output:", res.stdout)
if res.returncode != 0:
    print("Batch error:", res.stderr)

try:
    data = json.loads(res.stdout)
    resolved = data.get("resolved_ids", {})
    print("Resolved slide IDs:", resolved)

    # Insert images into resolved slides
    slide_images = {
        "p": ("fachada_norte_render.jpg", 40, 215, 340, 190),
        resolved.get("SLIDE_PATIO"): ("patio_corrala_render.jpg", 40, 90, 350, 240),
        resolved.get("SLIDE_LIVING"): ("interior_living_render.jpg", 40, 90, 350, 240),
        resolved.get("SLIDE_DESPACHO"): ("despacho_render.jpg", 40, 90, 350, 240),
        resolved.get("SLIDE_SUITE"): ("suite_principal_render.jpg", 40, 90, 350, 240),
        resolved.get("SLIDE_PORCHE"): ("porche_sur_render.jpg", 40, 90, 350, 240),
    }

    for slide_id, (img_name, x, y, w, h) in slide_images.items():
        if not slide_id:
            continue
        img_path = os.path.join(RENDERS_DIR, img_name)
        if os.path.exists(img_path):
            print(f"Uploading {img_name} to slide {slide_id}...")
            img_res = subprocess.run([
                "gslides", "mutate", "insert-image-from-file", PRES_ID,
                "--slide", slide_id,
                "--file", img_path,
                "--x", str(x), "--y", str(y),
                "--width", str(w), "--height", str(h)
            ], capture_output=True, text=True)
            print(f"Result for {img_name}:", img_res.stdout)
            if img_res.returncode != 0:
                print(f"Error uploading {img_name}:", img_res.stderr)

except Exception as e:
    print("Error parsing batch response:", e)

print(f"Google Slides deck ready: https://docs.google.com/presentation/d/{PRES_ID}/edit")
