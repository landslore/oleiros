---
name: presupuesto-mediciones
description: Estima el Presupuesto de Ejecución Material (PEM), gastos de autopromoción, tasas del Concello de Oleiros y cronograma de obra en el área de A Coruña.
---

# Presupuesto de Autopromoción y Hoja de Ruta (Oleiros / A Coruña)

## Instrucciones
1. Calcula la superficie construida computable diferenciando:
   - Vivienda climatizada (100 %).
   - Porches y terrazas cubiertas (50 %).
   - Sótano / Garaje (aprox. 60 % - 70 % del coste/m² de vivienda según excavación y presencia de roca granítica).
2. Aplica **ratios de construcción reales en el área de A Coruña / Oleiros**:
   - **Calidad Estándar / Funcional:** `1.450 € - 1.650 €/m²` construido (PEM + gastos generales y beneficio industrial de contrata).
   - **Calidad Media-Alta (SATE/fachada ventilada, aerotermia, VMC, carpintería alta gama):** `1.700 € - 2.000 €/m²` construido.
   - **Calidad Premium / Estándar Passivhaus:** `2.100 € - 2.500+ €/m²` construido.
3. Desglosa todos los costes adicionales de la autopromoción en Oleiros:
   - **Estudios previos:** Levantamiento topográfico (~600 € - 900 €) y Estudio Geotécnico (~1.100 € - 1.600 €, clave para detectar roca granítica o nivel freático antes de excavar).
   - **Honorarios técnicos (Proyecto + Dirección de Obra + Dirección de Ejecución + Coord. Seguridad):** aprox. `10 % - 13 %` del PEM.
   - **Impuestos y tasas municipales (Concello de Oleiros):** ICIO + Tasa de licencia urbanística (aprox. `4 % - 4,5 %` sobre el PEM declarado) + fianza de gestión de residuos (RCD).
   - **IVA:** `10 %` en ejecución de obra de vivienda habitual para autopromotor; `21 %` en honorarios técnicos, estudios y acometidas.
   - **Otros gastos:** Acometidas (agua, saneamiento, luz), cierre de parcela, ajardinamiento, notaría, registro de obra nueva y colchón de imprevistos (`10 % - 15 %`).
4. Si el usuario lo solicita, exporta el desglose completo a un archivo `.csv` en la raíz del proyecto.

## Formato de salida
- **Tabla comparativa de inversión total llave en mano** (Construcción + Técnicos + Impuestos + Parcela/Cierres) en los 3 escenarios.
- **Cronograma estimado en Oleiros** (desde estudio previo y solicitud de licencia municipal hasta ejecución de obra y comunicación previa de primera ocupación).
