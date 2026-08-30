# Auditoría dotes — lote M

Agente: agente-M · fecha: 2026-08-22
Páginas leídas: pdf 202, 203, 204, 211, 212, 213
Registros revisados: 32 de 32

## Hallazgos

### Afortunado · pdf 203 (dice la base) / pdf real 202
- **Campo:** `pagina.pdf` y `pagina.libro`
- **Dice la base:** `pagina: {pdf: 203, libro: 201}`
- **Dice la página:** la dote «Afortunado» está impresa en la página cuyo pie dice «200», que corresponde a pdf 202 (offset confirmado: 202 = 200 + 2). La página pdf 203 (pie «201») empieza directamente con «Atacante salvaje»; ni «Afortunado» ni «Alerta» aparecen en ella.
- **Gravedad:** media (la mecánica descrita es correcta y coincide con el texto de la página 202; solo falla la cita, que es justo el dato que sostiene la auditabilidad de la base).

### Alerta · pdf 203 (dice la base) / pdf real 202
- **Campo:** `pagina.pdf` y `pagina.libro`
- **Dice la base:** `pagina: {pdf: 203, libro: 201}`
- **Dice la página:** igual que «Afortunado», «Alerta» está en la misma página pdf 202 (pie «200»), no en pdf 203 (pie «201»).
- **Gravedad:** media (mismo caso: contenido correcto, cita de página equivocada; debería ser `pdf: 202, libro: 200`).

El resto de dotes de `origen.yaml` (Atacante salvaje, Duro, Fabricante, Habilidoso, Iniciado en la magia, Matón de taberna, Músico, Sanador) sí están correctamente citadas en pdf 203/libro 201 y pdf 204/libro 202, y su contenido coincide con la página, incluida la tabla completa de «Fabricación rápida» (8 filas de herramienta → objeto, todas verificadas letra por letra).

## Revisados sin hallazgo

**Dotes de origen** (`origen.yaml`):
- Atacante salvaje (pdf 203/libro 201) — descripción y ausencia de prerrequisito confirmadas.
- Duro (pdf 203/libro 201) — confirmada.
- Fabricante (pdf 203/libro 201) — confirmada, incluida la tabla de fabricación rápida completa.
- Habilidoso (pdf 203/libro 201) — confirmada, «Repetible» está en la página.
- Iniciado en la magia (pdf 203/libro 201) — confirmada, «Repetible... lista de conjuros distinta cada vez» está en la página.
- Matón de taberna (pdf 204/libro 202) — confirmada.
- Músico (pdf 204/libro 202) — confirmada.
- Sanador (pdf 204/libro 202) — confirmada.

**Dotes de estilo de combate** (`estilo_de_combate.yaml`), todas con prerrequisito «rasgo Estilo de combate» confirmado en la página:
- Combate con armas a dos manos (pdf 211/libro 209)
- Combate con armas arrojadizas (pdf 211/libro 209)
- Combate con dos armas (pdf 211/libro 209)
- Combate sin armas (pdf 211/libro 209)
- Defensa (pdf 211/libro 209)
- Duelo (pdf 211/libro 209)
- Intercepción (pdf 211/libro 209)
- Lucha a ciegas (pdf 212/libro 210)
- Protección (pdf 212/libro 210)
- Tiro con arco (pdf 212/libro 210)

**Dotes de don épico** (`don_epico.yaml`), todas con prerrequisito «nivel 19 o más» verificado línea a línea en la página (ninguna dice solo «nivel 19», todas llevan «o más»; ninguna incluye una característica mínima adicional en la línea de prerrequisito salvo la señalada):
- Don de la fortaleza (pdf 212/libro 210)
- Don de la habilidad (pdf 212/libro 210)
- Don de la pericia en combate (pdf 212/libro 210)
- Don de la recuperación (pdf 212/libro 210)
- Don de la resistencia a energías (pdf 212/libro 210)
- Don de la velocidad (pdf 213/libro 211)
- Don de la visión verdadera (pdf 213/libro 211)
- Don del ataque imparable (pdf 213/libro 211) — prerrequisito en la página es solo «nivel 19 o más»; la exigencia de Fuerza o Destreza aparece dentro del beneficio «Mejora de característica», no en la línea de prerrequisito. La base lo tiene correctamente separado (`prerrequisito: "nivel 19 o más"`, y la elección Fuerza/Destreza dentro de `descripcion`).
- Don del destino (pdf 213/libro 211)
- Don del espíritu de la noche (pdf 213/libro 211)
- Don del recuerdo de conjuros (pdf 213/libro 211) — único de los 12 con prerrequisito compuesto: «nivel 19 o más, rasgo Lanzamiento de conjuros», confirmado tal cual en la página y correctamente transcrito en la base.
- Don del viaje dimensional (pdf 213/libro 211)

## Dudas / ilegible

Ninguna. Todas las páginas (202-204, 211-213) se leyeron con claridad a 170 dpi.
