# Handoff — Tarea A: «Hablar con animales» sin clases

Página consultada: **pdf 291 = libro 289** (`Manual_del_Jugador_2024.pdf`),
lectura visual directa (imagen a 170 dpi), columna derecha superior.

## Lo que dice el manual

> **HABLAR CON LOS ANIMALES**
> *Adivinación de nivel 1 (bardo, brujo, druida, explorador)*
> Tiempo de lanzamiento: Acción o ritual
> Alcance: Lanzador
> Componentes: V, S
> Duración: 10 minutos

Texto: "Hasta que termine el conjuro, puedes comprender y comunicarte
verbalmente con bestias y usar con ellas cualquiera de las opciones de la
acción de influir. La mayoría de bestias tienen poco que decir en cuestiones
que no tengan que ver con la supervivencia o la compañía, pero como mínimo
podrán proporcionarte información sobre los lugares y monstruos cercanos,
incluyendo lo que hayan percibido en el último día."

Contraste con lo guardado (nivel 1, ritual: sí) → **coincide** en nivel y en
ritual. Confirmado también: escuela Adivinación, tiempo "Acción o ritual",
alcance "Lanzador", duración "10 minutos", componentes V, S (sin material).

## Hallazgo importante: NO es un campo vacío que rellenar — es una entrada duplicada

`hechizos.json` contiene **dos objetos distintos** para el mismo conjuro:

1. `"nombre": "Hablar con animales"` (sin "los") — `clases: []`, alcance
   "Toque", duración "8 h.", tiempo "Acción" (sin ritual explícito en el
   campo tiempo_lanzamiento aunque `ritual: true`). Estos datos **no
   coinciden con la página del manual** (el manual dice alcance Lanzador,
   duración 10 minutos, tiempo "Acción o ritual"). Esta entrada parece mal
   transcrita o corresponde a otra fuente/versión.
2. `"nombre": "Hablar con los animales"` (con "los", que es el título real
   tal y como aparece impreso en la página 289) — `clases: ["Bardo",
   "Brujo", "Druida", "Explorador"]`, alcance "Lanzador", duración "10 min",
   tiempo "Acción o ritual". **Esta entrada ya coincide exactamente con la
   página del manual** y ya tiene las clases correctas.

Es decir: el conjuro con el nombre bien escrito ("Hablar con los animales")
ya está completo y correcto. El que tiene `clases: []` es un **duplicado con
nombre truncado** ("Hablar con animales", sin "los") y con varios campos
desalineados del manual (alcance, duración).

## Recomendación para quien edite `hechizos.json`

No basta con copiar la lista de clases al duplicado — probablemente lo
correcto es **eliminar la entrada duplicada** `"Hablar con animales"` (sin
"los") y dejar solo `"Hablar con los animales"`, que ya es fiel a la página
289 del manual. Si se decide conservar ambas entradas por algún motivo (p. ej.
alias de búsqueda), como mínimo hay que corregir en el duplicado: nombre,
clases, alcance (Lanzador, no Toque), duración (10 minutos, no 8 h.) y tiempo
de lanzamiento (Acción o ritual).

No he tocado `hechizos.json` (fuera de mis límites en esta tarea).
