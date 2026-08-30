# Hallazgos — Humano Explorador (Vagabundo), nivel 1

Personaje construido: `personajes/humano_explorador.yaml` — "Rowan Aldeacampo".

## 1. Qué funcionó bien

- `validar.py`, `verificar_srd.py` y `cobertura.py` pasaron limpios antes de
  empezar (precondición del paso 0 de la skill), 0 errores.
- `clases/explorador.yaml → progresion` confirma con datos propios (no de
  memoria) que el Explorador 2024 es lanzador `medio` con espacios de
  conjuro **desde nivel 1**: `progresion[n=1].slots: [2,0,0,0,0]`, y
  `python3 calculo.py espacios --clase Explorador --nivel 1` devuelve
  exactamente `[2, 0, 0, 0, 0]`. No hay trucos en nivel 1 (los trucos de
  Explorador solo llegan opcionalmente en nivel 2 vía "Guerrero druídico");
  el rasgo "Lanzamiento de conjuros" confirma "empiezas con 2 conjuros de
  nivel 1... se recomiendan curar heridas y golpe apresador".
- **`cd-conjuros` y `ataque-conjuros` funcionan igual de bien para un
  lanzador "medio" que para uno "completo"**: la fórmula solo usa el
  modificador de aptitud mágica + bonificador de competencia, sin
  distinguir el tipo de progresión. `calculo.py cd-conjuros --aptitud 16
  --nivel 1` → `13`; `ataque-conjuros --aptitud 16 --nivel 1` → `5`. Ambos
  coinciden con el cálculo manual (mod Sab 16 = +3, PB nivel 1 = +2). No se
  encontró ningún tratamiento especial ni bug para "medio" vs. "completo"
  en esta parte — el caso ya está cubierto correctamente.
- `buscar.py conjuros-de Explorador --nivel 1` devolvió 14 conjuros
  correctos, incluidos "Curar heridas" y "Golpe apresador".
- Todas las refs de equipo (armadura, armas, munición, paquete, canalizador
  druídico, ítems del trasfondo) resolvieron a la primera contra
  `equipo/armaduras.yaml`, `equipo/armas.yaml`, `equipo/municion.yaml` y
  `equipo/aventureros.yaml`.
- `equipo/municion.yaml` (nuevo desde la ronda anterior, a juzgar por su
  comentario de PROCEDENCIA) resuelve bien "Flechas" — antes "20 flechas"
  del equipo de Explorador no tenía dónde resolver.
- `verificar_personaje.py` terminó en 0 problemas tras el ajuste descrito
  en el punto 2.

## 2. Bugs o comportamientos raros

**Bug real: `verificar_categorias()` no contrasta `competencias.herramientas`
contra el trasfondo, solo contra las clases.**

Comando y salida exacta (con `herramientas: [{categoria: "herramientas de
ladrón", origen: {trasfondo: Vagabundo}}]` en la ficha):

```
$ python3 verificar_personaje.py personajes/humano_explorador.yaml
23 referencias comprobadas.
❌ 1 problemas:
  ✗ competencias.herramientas: 'herramientas de ladrón' no está en lo que conceden las clases del personaje ([])
```

Causa: en `verificar_personaje.py → verificar_categorias()`, `permitidas`
se construye solo recorriendo `ficha["clases"]` y leyendo
`atributos_basicos.armas/armaduras/herramientas` de cada clase — nunca lee
`trasfondo.herramienta`. El Explorador no concede ninguna categoría de
herramienta (`atributos_basicos.herramientas: []`), así que cualquier
herramienta legítima que venga solo del trasfondo (aquí, "herramientas de
ladrón" de Vagabundo) es rechazada aunque sea 100% correcta según la base.
El mismo problema existe en teoría para `armas`/`armaduras` si algún
trasfondo llegara a conceder una categoría de arma/armadura (no ocurre con
Vagabundo, pero el código no lo contempla en absoluto).

No se tocó `verificar_personaje.py`. Workaround aplicado en la ficha: se
dejó `competencias.herramientas: []` y la competencia real con herramientas
de ladrón se documentó solo en `decisiones[]`, con un comentario largo en
el YAML explicando por qué no aparece en `competencias.herramientas`.

**Comportamiento no verificado pero sospechoso (no confirmado como bug):**
`verificar_habilidades()` no comprueba que el número de habilidades con
`origen: {clase: X}` coincida con `atributos_basicos.habilidades.elige` de
esa clase — solo que cada habilidad elegida esté dentro de la unión de
"permitidas" de todas las fuentes (clase + trasfondo, más las 18 si
`cualesquiera`). En esta ficha no se necesitó explotarlo porque Naturaleza,
Investigación y "Trato con animales" (origen especie/dote) ya estaban
dentro de la lista `de` del Explorador por coincidencia, así que no generó
error — pero en teoría una ficha podría declarar 6 habilidades con
`origen: {clase: Explorador}` (el doble de las 3 permitidas) y
`verificar_personaje.py` no lo detectaría. Se reporta como posible hueco,
no como bug confirmado (no se forzó el caso para no desviarse de construir
una ficha honesta).

## 3. Documentación confusa

- El comentario de `_ESQUEMA.md` sobre `competencias.armas/armaduras/herramientas`
  dice "se comprueban contra la lista real de `atributos_basicos` de la
  clase (o del trasfondo cuando aplique)" — pero el código de
  `verificar_categorias()` **nunca** mira el trasfondo pese a que el
  comentario del esquema lo da a entender como ya soportado ("cuando
  aplique"). Esto llevó a construir la ficha con la expectativa equivocada
  y perder un ciclo de verificación descubriendo el gap. Sugerencia (sin
  tocar código): corregir la frase del esquema para que diga explícitamente
  que hoy solo se contrasta contra clases, y que el trasfondo se documenta
  aparte en `decisiones[]`.
- `SKILL.md` (Paso 8) dice "Herramienta que el trasfondo permita elegir" —
  pero en Vagabundo la herramienta no es una elección, es fija
  (`herramienta: "herramientas de ladrón"`, sin lista de opciones). El
  texto de la skill da a entender que siempre hay elección; no siempre la
  hay.

## 4. Huecos de datos

- Ninguno relevante para este personaje. Todos los conjuros, equipo,
  idiomas y dotes necesarios existieron y resolvieron correctamente.

## 5. Salida final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/humano_explorador.yaml
23 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

`validar.py` también se volvió a correr al final para confirmar que la
base seguía en 0 errores (no se tocó ningún fichero fuera de
`personajes/`).
