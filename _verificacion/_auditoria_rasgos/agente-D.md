# Auditoría de rasgos — Paladín, Pícaro

Agente: agente-D · fecha: 2026-08-21
Páginas leídas: pdf 159, 160, 161, 169, 170, 171
Rasgos revisados: 32 de 32

## Hallazgos

### Paladín · Maestría con armas · pdf 159 (cita errónea)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 159, libro: 157}`
- **Dice la página:** La página pdf 159 (libro 157) contiene únicamente "Nivel 1: Imponer las manos" y "Nivel 1: Lanzamiento de conjuros"; termina con "...pero sí que cuentan como conjuros de paladín para ti." El encabezado "NIVEL 1: MAESTRÍA CON ARMAS" y su texto ("Tu entrenamiento con armas te permite utilizar las propiedades de maestría con dos tipos de armas de tu elección con las que tengas competencia, como espadas largas y jabalinas...") están en la página pdf 160 (libro 158), en la columna izquierda bajo la tabla "Rasgos de paladín".
- **Gravedad:** media (la cita de página es incorrecta, aunque el contenido del rasgo en sí es fiel). Corrección propuesta: `pagina: {pdf: 160, libro: 158}`.

Nota: el mismo rasgo en Pícaro ("Maestría con armas", nivel 1) sí cita correctamente pdf 169/libro 167 — su descripción completa está en esa página.

## Verificación de puntos señalados en el encargo

- **Ataque furtivo (Pícaro), pdf 169:** confirmado literal en la imagen. El texto exige explícitamente **ventaja en la tirada Y arma sutil o a distancia** para el daño adicional; la condición alternativa (sin necesidad de ventaja) es que **al menos un aliado sin el estado de incapacitado esté a 1,5 m o menos del objetivo y tú no tengas desventaja en la tirada**. No aparece ninguna mención a "sin enemigos a 1,5 m de ti" (regla de 2014). El YAML refleja esto condición por condición, sin desviaciones. La progresión de dados de la tabla "Rasgos de pícaro" (1d6 en nivel 1, subiendo un dado cada dos niveles hasta 10d6 en nivel 20) también coincide exactamente con la tabla de la página 170.

- **Imponer las manos (Paladín), pdf 159:** confirmado. La reserva es "igual a cinco veces tu nivel de paladín", se rellena tras un descanso largo, se puede usar como acción adicional para restaurar PG (hasta el máximo que quede en la reserva), y separadamente se pueden gastar 5 PG de la reserva para curar el estado de envenenado (sin restaurar PG). Todo coincide con el YAML.

- **Lanzamiento de conjuros desde nivel 1 (Paladín):** confirmado. La página pdf 159 lleva el encabezado "NIVEL 1: LANZAMIENTO DE CONJUROS" y la tabla "Rasgos de paladín" (pdf 160) muestra 2 espacios de conjuro de nivel 1 ya en la fila de nivel 1. El paladín 2024 sí lanza conjuros desde el nivel 1 (a diferencia de 2014, donde empezaba en nivel 2); la página lo confirma sin ambigüedad.

- **Mejora de característica en nivel 10 del Pícaro (pdf 170):** **CONFIRMADA, no es un error.** La tabla "Rasgos de pícaro" (pdf 170) lista explícitamente "Mejora de característica" en la fila de nivel 10, además de las filas 4, 8, 12 y 16. El texto de apoyo bajo "NIVEL 4: MEJORA DE CARACTERÍSTICA" lo confirma por escrito: *"Vuelves a obtener este rasgo en los niveles 8, 10, 12 y 16 de pícaro."* Es decir, el Pícaro 2024 conserva la mejora de característica extra en nivel 10 que ya tenía el Pícaro (Rogue) de 2014, y que el SRD 5.2 no recoge por tratarse de contenido fuera del SRD. Esto no es un rasgo de `clases/rasgos/picaro.yaml` (ese fichero, igual que `paladin.yaml`, excluye deliberadamente todas las filas "Mejora de característica" del tronco de clase, algo consistente en ambos ficheros de mi lote), así que no genera hallazgo en mi fichero asignado. Dato aparte para quien mantenga `clases/picaro.yaml`: su campo `nota` dice *"Mejoras de característica extra en niveles 6 y 10"*; la página confirma el nivel 10 pero el nivel 6 no aparece en ningún sitio como nivel de Mejora de característica (en nivel 6 el rasgo es "Pericia", tanto en la tabla como en el texto) — esa nota parece tener un error de digitación (6 en vez de, por ejemplo, repetir 4/8/12/16/19), pero al no ser mi fichero asignado no lo reporto como hallazgo formal, solo lo dejo anotado.

## Rasgos revisados sin hallazgo

**Paladín** (pdf 159–161): Imponer las manos, Lanzamiento de conjuros, Castigo de paladín, Estilo de combate, Canalizar divinidad, Ataque adicional, Corcel fiel, Aura de protección, Abjurar de los enemigos, Aura de coraje, Golpes radiantes, Toque reparador, Expansión de aura, Don épico (14 de 15; Maestría con armas tiene el hallazgo de cita arriba, pero su contenido descriptivo también se verificó correcto).

**Pícaro** (pdf 169–171): Ataque furtivo, Jerga de ladrones, Maestría con armas, Pericia (nivel 1 y nivel 6 — ambas entradas citan correctamente pdf 169, donde en efecto aparece el texto de la ampliación de nivel 6 al final de la sección "Nivel 1: Pericia"), Acción astuta, Puntería certera, Esquiva asombrosa, Golpe astuto, Evasión, Talentos fiables, Golpe astuto mejorado, Golpes taimados, Mente escurridiza, Elusivo, Don épico, Golpe de suerte (17 de 17).

Se comprobó además que el recuento de rasgos de tronco de clase (excluyendo Mejora de característica, Subclase y filas "—") coincide exactamente entre cada tabla "Rasgos de paladín"/"Rasgos de pícaro" y el número de entradas de cada YAML: 15 para Paladín, 17 para Pícaro.

## Dudas / ilegible

Ninguna. Las seis páginas (159, 160, 161, 169, 170, 171) se leyeron con claridad a 170 dpi.
