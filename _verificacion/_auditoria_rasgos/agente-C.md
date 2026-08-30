# Auditoría de rasgos — Guerrero, Mago, Monje

Agente: agente-C · fecha: 2026-08-21
Páginas leídas: pdf 115, 116, 139, 140, 141, 151, 152, 153
Rasgos revisados: 44 de 44

## Hallazgos

### Guerrero · Acción súbita (dos usos) · pdf 116
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 116, libro: 114}`
- **Dice la página:** La frase que describe este beneficio («A partir del nivel 17, podrás usarlo dos veces antes de descansar, pero solo una vez por turno») está impresa en la **página pdf 115** (libro 113), dentro del párrafo de «Nivel 2: Acción súbita». La página pdf 116 solo contiene la fila de la tabla «Rasgos de guerrero» que nombra «Acción súbita (dos usos)» en el nivel 17, no una descripción propia.
- **Gravedad:** baja (no cambia ninguna mecánica; el texto condensado es correcto, solo la cita de página no señala dónde está la prosa). Nota: contraste con «Indómito (dos usos)»/«Indómito (tres usos)», cuya prosa de ampliación sí está en pdf 116 junto con el resto de "Nivel 9: Indómito", así que esos dos sí citan bien.

### Mago · Adepto en rituales · pdf 139
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 139, libro: 137}`
- **Dice la página:** El encabezado «Nivel 1: Adepto en rituales» y su párrafo («Puedes lanzar de forma ritual cualquier conjuro de mago que figure en tu libro de conjuros y esté marcado como "ritual"...») están impresos en la **página pdf 140** (libro 138), no en la 139. La página 139 solo llega hasta el final de «Lanzamiento de conjuros» (Conjuros preparados de nivel 1 y superiores).
- **Gravedad:** media (mismo tipo de error que ya se detectó en Clérigo; puede llevar a alguien que quiera verificar la fuente a la página equivocada).

### Mago · Recuperación arcana · pdf 139
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 139, libro: 137}`
- **Dice la página:** Igual que el caso anterior: el encabezado «Nivel 1: Recuperación arcana» está en la **página pdf 140** (libro 138), inmediatamente debajo de «Adepto en rituales» y antes de «Nivel 2: Académico». El texto condensado del YAML («la suma de niveles... debe ser igual o inferior a la mitad de tu nivel de mago, redondeando hacia arriba, y ninguno puede ser de nivel 6 o más») es fiel a la página, solo la cita está desplazada una página.
- **Gravedad:** media (mismo motivo que el hallazgo anterior).

## Notas sin llegar a hallazgo formal

- **Mago · Lanzamiento de conjuros (pdf 139):** confirmado con exactitud: el libro de conjuros es «un objeto Diminuto que pesa 1,5 kg, contiene 100 páginas y solo podéis leerlo tú o alguien que lance identificar», empiezas con 6 conjuros de nivel 1 recomendando exactamente armadura de mago, caída de pluma, detectar magia, dormir, ola atronadora y proyectil mágico. Estas cifras que cita la base son correctas letra por letra.
  El apartado «Ampliar/sustituir el libro» que el YAML incluye dentro de este mismo rasgo (2 horas y 50 po/nivel para copiar un conjuro encontrado; 1 hora y 10 po/nivel para copiar tu propio libro; mismo procedimiento si lo pierdes) es también fiel en cifras, pero ese recuadro «Ampliar y sustituir un libro de conjuros» está físicamente impreso en la **página pdf 141** (libro 139), dos páginas después de la citada. No lo elevo a hallazgo de "cita falsa" porque el encabezado del rasgo (Nivel 1: Lanzamiento de conjuros) sí está en pdf 139 y el rasgo se extiende varias páginas — pero quien revise conviene que sepa que ese dato concreto se confirma en pdf 141, no en pdf 139.

- **Monje · Defensa sin armadura (pdf 151):** fórmula verificada literalmente contra la página: «Mientras no lleves armadura ni portes un escudo, tu clase de armadura base será igual a 10 más tus modificadores por Destreza y Sabiduría.» Coincide exactamente con el YAML (10 + modificador de Destreza + modificador de Sabiduría). Sin discrepancias.

## Rasgos revisados sin hallazgo

**Guerrero:** Estilo de combate, Maestría con armas, Tomar aliento, Acción súbita (un uso), Mente táctica, Ataque adicional, Desplazamiento táctico, Indómito (un uso), Maestro táctico, Dos ataques adicionales, Ataques estudiados, Indómito (dos usos), Indómito (tres usos), Don épico, Tres ataques adicionales.
(16 rasgos totales; el único con hallazgo es Acción súbita (dos usos), listado arriba)

**Mago:** Lanzamiento de conjuros (ver nota), Académico, Memorizar conjuro, Maestría sobre conjuros, Don épico, Conjuros característicos.
(8 rasgos totales; Adepto en rituales y Recuperación arcana tienen hallazgo arriba)

**Monje:** Artes marciales, Defensa sin armadura, Concentración de monje, Metabolismo asombroso, Movimiento sin armadura, Desviar ataques, Caída lenta, Ataque adicional, Golpe aturdidor, Golpes potenciados, Evasión, Movimiento acrobático, Autorrestablecimiento, Concentración agudizada, Desviar energía, Superviviente disciplinado, Concentración perfecta, Defensa superior, Don épico, Cuerpo y mente.
(20 rasgos totales, sin hallazgos)

## Dudas / ilegible

Ninguna. Las 8 páginas (115, 116, 139, 140, 141, 151, 152, 153) se leyeron con claridad a 170 dpi; no hubo texto ilegible ni ambiguo.
