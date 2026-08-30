# Informe V8 — verificación visual pdf 269 (pág. impresa 267)

Fuente: render `pdftoppm -r 170 -f 269 -l 269 -png Manual_del_Jugador_2024.pdf /tmp/render/v8` (lectura visual del PNG, con recortes adicionales a 300 dpi para confirmar cada línea). No se ha usado `pdftotext` en ningún momento. Ambos conjuros están completos dentro de la pdf 269 (columna izquierda y columna derecha de la misma página); no ha hecho falta la pdf 270.

En esta página aparecen 4 conjuros de curación: Curar (Heal), Curar en masa (Mass Heal), Curar heridas (Cure Wounds) y Curar heridas en masa (Mass Cure Wounds). Los dos pedidos son el segundo y el cuarto.

---

## 1. Transcripción completa — «Curar heridas en masa» (columna derecha)

> **CURAR HERIDAS EN MASA**
> *Abjuración de nivel 5 (bardo, clérigo, druida)*
>
> **Tiempo de lanzamiento:** Acción
> **Alcance:** 18 m
> **Componentes:** V, S
> **Duración:** Instantáneo
>
> Una ola de energía curativa brota de un punto que puedas ver dentro del alcance. Elige a hasta seis criaturas en una esfera de 9 m de radio centrada en ese punto. Cada objetivo recupera una cantidad de puntos de golpe igual a 5d8 más tu modificador por aptitud mágica.
>
> *Con un espacio de conjuro de nivel superior.* La curación aumenta en 1d8 por cada nivel por encima de 5 que tenga el espacio.

---

## 2. Transcripción completa — «Curar en masa» (columna izquierda)

> **CURAR EN MASA**
> *Abjuración de nivel 9 (clérigo)*
>
> **Tiempo de lanzamiento:** Acción
> **Alcance:** 18 m
> **Componentes:** V, S
> **Duración:** Instantáneo
>
> De ti brota una oleada de energía curativa que envuelve a las criaturas que te rodean. Haces recuperar hasta 700 puntos de golpe, repartidos como tú escojas entre cualquier cantidad de criaturas que puedas ver dentro del alcance. Las criaturas sanadas con este conjuro también se libran de los estados de cegadas, ensordecidas y envenenadas.

Nota importante: a diferencia de los demás conjuros de curación de esta página, **«Curar en masa» NO lleva párrafo de "Con un espacio de conjuro de nivel superior"**. Tras la frase "...se libran de los estados de cegadas, ensordecidas y envenenadas." viene directamente la línea divisoria y el siguiente conjuro ("Curar heridas"). Se ha comprobado dos veces con zoom a 300 dpi que no hay texto adicional entre medias.

---

## 3. Diferencias mecánicas (una línea cada una)

- **A cuántas criaturas alcanza:** «Curar heridas en masa» cura a **hasta seis criaturas** dentro de una esfera; «Curar en masa» cura a **cualquier cantidad de criaturas** que el lanzador pueda ver dentro del alcance (sin tope numérico impreso).
- **Cuánto cura cada uno:** «Curar heridas en masa» → **5d8 + modificador por aptitud mágica** por objetivo (y escala con espacios de nivel superior, +1d8 por nivel por encima de 5); «Curar en masa» → un total fijo de **hasta 700 puntos de golpe** repartidos a elección del lanzador entre los objetivos, y no escala con espacios de nivel superior (no tiene ese párrafo).
- **Radio/alcance:** ambos tienen **Alcance: 18 m**, pero «Curar heridas en masa» además exige que los objetivos estén dentro de una **esfera de 9 m de radio** centrada en un punto visible dentro del alcance; «Curar en masa» no menciona esfera/radio, solo que las criaturas deben estar "dentro del alcance" (18 m) y ser visibles.
- Extra no pedido pero visible en el texto: «Curar en masa» también libra a las criaturas curadas de cegadas/ensordecidas/envenenadas; «Curar heridas en masa» no menciona esa cura de estados.

---

## 4. Cabeceras exactas tal como están impresas

| Conjuro | Nombre impreso (cabecera) | Nivel/escuela | Clases listadas |
|---|---|---|---|
| Mass Cure Wounds | **CURAR HERIDAS EN MASA** | Abjuración de nivel 5 | bardo, clérigo, druida |
| Mass Heal | **CURAR EN MASA** | Abjuración de nivel 9 | clérigo |

---

## Evidencia (capturas usadas)

- `/tmp/render/v8-269.png` — página completa (pdf 269 = impresa 267), r170.
- `/tmp/render/zoom_curarmasa.png` — recorte columna izquierda, "Curar en masa" completo, r300.
- `/tmp/render/zoom_curarheridasmasa.png` — recorte columna derecha, cierre de "Curar en masa" + "Curar heridas" completo + cabecera "Curar heridas en masa", r300.
- `/tmp/render/zoom_curarheridasmasa2.png` — recorte columna derecha, cuerpo completo de "Curar heridas en masa" incl. párrafo de mejora, r300.

No se ha tocado ni leído ningún fichero de la base (hechizos.json, *.yaml, *.py) ni informes de otros agentes.
