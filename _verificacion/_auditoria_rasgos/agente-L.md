# Auditoría de conjuros — lote 4

Agente: agente-L · fecha: 2026-08-21
Páginas leídas: pdf 318, 319, 320, 321, 323, 324, 326, 327, 331, 333, 334, 336, 337, 339, 340, 341, 342, 343, 344
Conjuros revisados: 20 de 20

## Hallazgos

(ninguno hasta ahora)

## Revisados sin hallazgo
- Palabra de poder: fortalecer · pdf 318 (libro 316) — todos los campos coinciden.
- Palabra de resplandor · pdf 319 (libro 317) — todos los campos coinciden, incluida mejora de truco.
- Pasar sin rastro · pdf 320 (libro 318) — coincide con el dato de control (V,S,M cenizas de muérdago quemado; Concentración, hasta 1 hora).
- Pequeña choza de Leomund · pdf 321 (libro 319) — Tiempo de lanzamiento «1 minuto o un ritual» confirma `ritual: true` del JSON; Duración «8 horas» sin mención de Concentración confirma `concentracion: false`.
- Presencia regia de Yolande · pdf 323 (libro 321) — todos los campos coinciden.
- Puerta arcana · pdf 326 (libro 324) — todos los campos coinciden.
- Rayo de hechicería · pdf 327 (libro 325) — todos los campos coinciden.
- Risa horrible de Tasha · pdf 331 (libro 329) — todos los campos coinciden.
- Salto · pdf 333 (libro 331) — todos los campos coinciden; sin mención de Concentración en Duración, confirma `concentracion: false`.
- Sanctasanctórum privado de Mordenkainen · pdf 333 (libro 331) — **escuela verificada directamente en la cabecera: «Abjuración de nivel 4 (mago)»**, coincide con el JSON (`escuela: "Abjuración"`). El resto de campos también coincide (tiempo 10 min, alcance 36 m, componentes V,S,M lámina fina de plomo, duración 24 horas sin concentración). La nota `_nota_verificacion` del JSON puede darse por resuelta: la escuela es correcta.
- Sentidos de la bestia · pdf 334 (libro 332) — Tiempo de lanzamiento «Acción o ritual» confirma `ritual: true`; Componentes «S» (solo somático) coincide exactamente con el JSON; Duración «Concentración, hasta 1 hora» confirma `concentracion: true`.
- Tañido por los muertos · pdf 336 (libro 334) — todos los campos coinciden.
- Telepatía · pdf 337 (libro 335) — todos los campos coinciden; Duración «24 horas» sin mención de Concentración confirma `concentracion: false`.
- Tentáculos negros de Evard · pdf 339 (libro 337) — todos los campos coinciden.
- Texto ilusorio · pdf 340 (libro 338) — Tiempo de lanzamiento «1 minuto o un ritual» confirma `ritual: true`; Componentes «S, M (tinta que valga al menos 10 po, que se consume...)» coincide exactamente con el JSON (`verbal: false`, coste «10 po*», `consume_material: true`).
- Tormenta de espinas · pdf 341 (libro 339) — todos los campos coinciden (Componentes: V solamente; Duración: Instantáneo, sin concentración).
- Tormenta de meteoritos · pdf 342 (libro 340) — todos los campos coinciden.
- Tormenta resplandeciente de Jallarzi · pdf 342 (libro 340) — todos los campos coinciden (Componentes: V, S, M una pizca de fósforo; Duración: Concentración, hasta 1 minuto).
- Tronar · pdf 343 (libro 341) — Componentes «S» (solo somático, sin verbal) coincide exactamente con el JSON.
- Ver invisibilidad · pdf 344 (libro 342) — todos los campos coinciden; Duración «1 hora» sin mención de Concentración confirma `concentracion: false`.

## Dudas / ilegible

Ninguna. Todas las páginas se leyeron con claridad a 170 dpi.

Nota menor sin relevancia mecánica: en la descripción impresa de «Tormenta resplandeciente de Jallarzi» (pdf 342) aparece la secuencia «cilindro de 3 m de radio diámetro y 12 m de alto», que parece un artefacto tipográfico del propio manual (posible resto de una edición previa). No afecta ninguna cifra del JSON, que registra correctamente «3 m de radio y 12 m de alto», así que no se reporta como hallazgo.
