# Superficies Propuesta D
sup_cerrada = 215.0 # m2 (PB 116.5 + P1 98.5)
sup_exterior_cubierta = 53.5 # m2 (Porche Sur 36, Porche Norte 3.5, Balcón P1 14)
# En metros cuadrados construidos equivalentes (estándar tasación y contrata):
# Exterior cubierto computa al 50%: 215 + (53.5 * 0.5) = 241.75 m2 equivalentes
sup_eq = sup_cerrada + (sup_exterior_cubierta * 0.5)

print(f"Superficie construida equivalente: {sup_eq:.2f} m²")

# Escenario 1: Estándar (1.500 €/m² contrata completa de edificación)
# Escenario 2: Media-Alta (1.850 €/m² contrata completa de edificación)
# Escenario 3: Premium Propuesta D (2.150 €/m² contrata completa de edificación)

for nombre, ratio in [("Estándar", 1550), ("Media-Alta", 1850), ("Premium Propuesta D", 2150)]:
    coste_obra_edif = sup_eq * ratio
    print(f"\n--- {nombre} ({ratio} €/m² eq) ---")
    print(f"Edificación completa (incluye clima, VMC, etc): {coste_obra_edif:,.2f} €")
