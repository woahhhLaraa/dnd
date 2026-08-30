# Semántica de `tirada` — lote T2

Agente: T2 · fecha: 2026-08-29
Páginas leídas: pdf 306, 309, 314, 315 (libro 304, 307, 312, 313)

## Levitar · pdf 306 (libro 304)
- **Cita:** «El conjuro puede hacer levitar un objeto que pese hasta 250 kg y no
  afecta a una criatura no voluntaria que supere una tirada de salvación de
  Constitución.»
- **Veredicto:** DISPARADOR
- **Por qué:** es la única tirada del conjuro. Si la criatura no voluntaria la
  supera, el conjuro **no le afecta en absoluto** (no levita). Decide si el
  conjuro tiene efecto sobre el objetivo, no modula nada después.
- **Otras salvaciones del conjuro:** ninguna otra.

## Mal de ojo · pdf 309 (libro 307)
- **Cita:** «Una criatura de tu elección que puedas ver a 18 m o menos de ti
  deberá superar una tirada de salvación de Sabiduría o se verá afectada por
  uno de los efectos descritos debajo, a tu elección, hasta que termine el
  conjuro.»
- **Veredicto:** DISPARADOR
- **Por qué:** patrón «deberá superar ... o [efecto]». Si la supera, no le pasa
  nada; si la falla, sufre uno de los tres efectos (Náuseas/envenenado,
  Pánico/asustado, Sueño/inconsciente) a elección del lanzador.
- **Otras salvaciones del conjuro:** ninguna otra tirada de salvación descrita
  para escapar de los efectos (Pánico termina solo si el objetivo llega a 18 m
  sin ser visto; Sueño termina con daño o con una acción de otra criatura; no
  hay tiradas adicionales).

## Muro de piedra · pdf 314 (libro 312)
- **Cita:** «Si una criatura fuera a quedar rodeada por todas partes por el
  muro (o por el muro y otra superficie sólida), puede hacer una tirada de
  salvación de Destreza. Si la supera, podrá usar su reacción para moverse
  hasta su velocidad y no quedar encerrada por el muro.»
- **Veredicto:** MODULA
- **Por qué:** el muro se manifiesta igual, y si atraviesa el espacio de una
  criatura esta es empujada a un lado **sin necesidad de ninguna tirada**. La
  única tirada de salvación del conjuro es un caso especial (quedaría
  totalmente rodeada) y solo sirve para evitar el estado añadido de "quedar
  encerrada"; no evita que el muro se cree ni que empuje.
- **Otras salvaciones del conjuro:** ninguna otra; es la única tirada descrita
  en el texto de este conjuro.

## Muro prismático · pdf 315 (libro 313)
- **Cita (primera tirada del conjuro, en el cuerpo del texto, antes de la
  tabla):** «Si otra criatura que pueda ver el muro se acerca a 6 m o menos de
  él, deberá superar una tirada de salvación de Constitución o tendrá el
  estado de cegada durante 1 minuto.»
- **Veredicto:** DISPARADOR (para este efecto concreto)
- **Por qué:** patrón «deberá superar ... o tendrá el estado de X»: si la
  supera no queda cegada; si la falla, sí. Ojo: esto **no** es la tirada que
  protege el muro en sí — el muro se forma igualmente, siempre; esta tirada
  solo regula si una criatura que se acerca queda cegada.

**Aviso pedido — capas prismáticas, varias salvaciones:**
La *primera* tirada "estructural" del conjuro (la que protege el muro contra
quien intenta atravesarlo) es la de Destreza descrita justo después:
«Cuando una criatura meta la mano en el muro o lo atraviese, lo debe hacer
capa por capa hasta superarlas todas [...] deberá realizar una tirada de
salvación de Destreza o quedará afectada por las propiedades de esa capa,
como se describe en la tabla "Capas prismáticas".»
Es una única tirada de Destreza por capa (no dos), pero el papel de "superarla"
cambia según el color:

| Capa (orden) | Papel de la tirada de Destreza |
|---|---|
| 1 Roja, 2 Naranja, 3 Amarilla, 4 Verde, 5 Azul | **MODULA** — el daño (12d6 del tipo correspondiente) se sufre igual; si se supera la tirada es solo la mitad. El efecto (daño) ocurre siempre. |
| 6 Añil | **DISPARADOR** — «si falla la tirada» aparece apresado y encadena tiradas de salvación de Constitución al final de cada turno (3 éxitos = libre, 3 fallos = petrificado); no se menciona efecto si se supera la Destreza inicial, luego superarla evita el estado por completo. |
| 7 Violeta | **DISPARADOR** — «si falla la tirada» aparece cegado y hace una tirada de salvación de Sabiduría al inicio del siguiente turno del lanzador (si la supera, cegado termina; si la falla, cegado termina pero es teletransportado a otro plano); superar la Destreza inicial evita el estado por completo. |

Es decir, el conjuro mezcla ambos patrones: capas 1-5 son MODULA (daño con
mitad si se supera) y capas 6-7 son DISPARADOR (estado evitado por completo si
se supera), cada una además con tiradas de seguimiento propias (Constitución
repetida en la capa 6, Sabiduría en la capa 7) que deciden si el objetivo se
libera del estado ya aplicado — esas de seguimiento sí son del tipo "librarse
de un estado ya aplicado" (no disparan el conjuro).

## Dudas / ilegible
- Ninguna imagen ilegible. Las cuatro páginas se leyeron con claridad.
- Muro prismático es el único caso ambiguo para un único veredicto de campo
  `tirada`: la salvación de Constitución por acercarse (cegar) es DISPARADOR,
  pero el muro en sí aparece siempre sin salvación, y las capas mezclan
  MODULA (1-5) y DISPARADOR (6-7). No hay una sola etiqueta que resuma todo el
  conjuro con fidelidad; si el campo debe ser único, márquese como DUDOSO o
  decídase a nivel de qué tirada representa el campo (la de acercarse, o la
  de atravesar la primera capa).
