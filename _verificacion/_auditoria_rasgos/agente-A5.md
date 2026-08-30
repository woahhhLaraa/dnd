# Auditoría de descripciones (Fase 13p) — lote A5

Agente: A5 · fecha: 2026-08-27
Páginas leídas: pdf 270, 271, 272, 273 (libro 268-271)
Conjuros revisados: 14 de 14

## Hallazgos

### De la carne a la piedra · pdf 270
- **Campo:** descripcion
- **Modo de fallo:** 2 (terminología que no es la del manual — nombres de condición/tipo de criatura incorrectos)
- **Dice la base:** «El objetivo hace una tirada de salvación de Constitución; si falla, queda **restringido**, si tiene éxito, su velocidad es 0 hasta su próximo turno. Un objetivo **restringido** repite la salvación al final de cada turno [...] Las **construcciones** resisten automáticamente.»
- **Dice la página:** «Si la falla, tendrá el estado de **apresado** hasta que el conjuro termine [...] Los **autómatas** superan automáticamente la tirada de salvación [...] Un objetivo **apresado** realiza otra tirada de salvación de Constitución al final de cada uno de sus turnos.»
- **Gravedad:** media (el nombre de condición «restringido» no es el que usa el manual — es «apresado» —, y «construcciones» tampoco coincide con «autómatas»; quien busque la condición o el tipo de criatura en el apéndice no la encontrará con esos nombres).

### Detectar magia · pdf 272
- **Campo:** descripcion
- **Modo de fallo:** 6 (conversión de unidad falsa/inventada)
- **Dice la base:** «El conjuro no puede atravesar 30 cm / **11 pulgadas** de piedra, tierra o madera, 2,5 cm / **0,9 pulgada** de metal o una lámina fina de plomo.»
- **Dice la página:** «El conjuro no puede atravesar 30 cm de piedra, tierra o madera, 2,5 cm de metal o una lámina fina de plomo.» (sin ninguna conversión a pulgadas)
- **Gravedad:** baja-media. La página no trae conversión a pulgadas en absoluto, y la que añade la base es aritméticamente incorrecta (30 cm ≈ 11,8 pulgadas → se redondearía a 12, no 11; 2,5 cm ≈ 0,98 pulgada → se redondearía a 1, no 0,9). Además es inconsistente con las otras tres «Detectar…» de este mismo lote (*Detectar el bien y el mal* y *Detectar venenos y enfermedades*), que para el mismo par 30 cm/2,5 cm usan «1 pie / 1 pulgada», correcto y consistente con el resto de la base.

### Detectar pensamientos · pdf 271 (= pdf 273 en el render, libro 271)
- **Campo:** descripcion
- **Modo de fallo:** 2 (regla/terminología de otra fuente — nombre de prueba de característica que no es el que usa el manual)
- **Dice la base:** «[...] puede usar su acción para intentar finalizar el conjuro con prueba de **Inteligencia (Arcana)** contra tu CD de salvación.»
- **Dice la página:** «[...] podrá usar una acción en su turno para hacer una prueba de **Inteligencia (Conocimiento arcano)** contra tu CD de salvación de conjuros; si la supera, el conjuro terminará.»
- **Gravedad:** media (el nombre de la competencia no es el que usa el manual de 2024; «Arcana» es el nombre de la edición de 2014, «Conocimiento arcano» es el término de esta página).

## Revisados sin hallazgo
- Dañar (pdf 270)
- Dedo de la muerte (pdf 270) — nota: el campo `descripcion` ya trae una corrección previa registrada en `_nota_verificacion` («7d8 + 30»); se ha releído la página y el texto actual coincide exactamente con ella. Sin hallazgo nuevo.
- Descarga de fuego (pdf 270)
- Descarga sobrenatural (pdf 270)
- Deseo (pdf 270-271) — nota: el campo `descripcion` ya trae una corrección previa registrada en `_nota_verificacion` (los 7 efectos completos + el párrafo de la tensión). Se ha releído toda la página 271 y el texto coincide palabra por palabra con la corrección ya aplicada. Sin hallazgo nuevo.
- Despertar (pdf 271)
- Desplazamiento entre planos (pdf 272)
- Destierro (pdf 272)
- Detectar el bien y el mal (pdf 272)
- Detectar trampas (pdf 273)
- Detectar venenos y enfermedades (pdf 273)

(Nota: "Detectar magia" y "Detectar pensamientos" aparecen arriba, en Hallazgos, y no se repiten aquí.)

## Dudas / ilegible

- **Detectar pensamientos** — campo `tirada`: la base dice `"Directo"`, pero la opción «Leer pensamientos» de la descripción exige explícitamente una «tirada de salvación de Sabiduría» al objetivo cuando se sondea en profundidad. Como el propio briefing indica que este patrón («Directo» + descripción que pide salvación) ya está contabilizado aparte por la decisión de diseño pendiente, lo dejo en dudas y no en hallazgos.
- Ninguna página resultó ilegible; todas se leyeron a 170 ppp sin necesidad de recortes adicionales salvo el recorte de verificación hecho sobre "De la carne a la piedra" (pdf 270) para confirmar el texto exacto de "apresado"/"autómatas".
