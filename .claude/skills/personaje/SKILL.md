---
name: personaje
description: Crea un personaje de D&D 2024 (5.5e) de nivel 1 a partir de la base canónica, paso a paso, sin usar nada del conocimiento del modelo sobre las reglas. Usar cuando el usuario pida crear/generar un personaje nuevo de D&D en este proyecto.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash(python3 *)
  - Bash(ls *)
---

# /personaje — creación de personaje nivel 1

Argumentos: `$ARGUMENTS` (opcional: nombre del personaje).

## Regla que gobierna todo lo demás

**Consultar, no recordar.** No sabes reglas de D&D 2024 de memoria a efectos
de esta skill: todo lo que ofrezcas, calcules o escribas sale de esta base o
de las herramientas que la consultan. Si algo que necesitas no está en la
base, dilo y detente — no lo rellenes con lo que "sabes" de D&D (probablemente
sea la edición 2014, vetada, ver `FUENTES.md`).

**Nunca hagas la aritmética a mente.** Todos los números — PG, CA, CD de
conjuros, bonificador de competencia, coste en puntos — se obtienen
ejecutando `calculo.py`, nunca sumando tú. Si `calculo.py` no tiene la
función que necesitas, dilo al usuario en vez de improvisar el cálculo.

## Paso 0 — Precondición (obligatoria, no se salta)

Antes de preguntar nada, ejecuta en la raíz de la base:

```bash
python3 validar.py && python3 verificar_srd.py && python3 cobertura.py
```

Si cualquiera de los tres falla, **detente** y muestra el error al usuario:
la base no está en un estado fiable para construir un personaje sobre ella.
No continúes "con cuidado" — la garantía de esta skill depende de que los
tres pasen.

## Paso 1 — Nombre del personaje

Pregunta el nombre. El fichero de destino será
`personajes/<nombre-en-minusculas-con-guiones>.yaml`. Si ya existe, avisa y
pregunta si se sobreescribe antes de tocar nada.

## Paso 2 — Especie

Lista las especies reales:

```bash
python3 -c "import yaml; d=yaml.safe_load(open('especies/especies.yaml')); print([e['nombre'] for e in d['especies']])"
```

Muestra las opciones, pregunta cuál, y si esa especie tiene una elección
interna (ver el campo `tamano` u otros en su `rasgos` — algunas especies
ofrecen variantes), pregúntala también. Guarda `especie.ref` como
`"especies/especies.yaml#<Nombre>"`.

## Paso 3 — Trasfondo

Mismo patrón con `trasfondos/trasfondos.yaml`. El trasfondo fija:
`caracteristicas` (las tres sobre las que se reparte el ajuste),
`habilidades` (fijas, no son elección), `dote` (se añade directamente a
`dotes:` en la ficha, con `origen: {trasfondo: <nombre>}`), `herramienta` y
`equipo_a`/`equipo_b`.

## Paso 4 — Clase

Lista las 12 clases (`clases/*.yaml`, campo `clase`). Al elegir una, léela
completa con `python3 buscar.py clase <Nombre>` — de ahí salen
`atributos_basicos` (dado de golpe, salvaciones, habilidades a elegir,
armas, armaduras, herramientas, característica principal, equipo inicial
A/B) y si es lanzadora (`lanzador`, `aptitud_magica`).

## Paso 5 — Características

Pregunta el método: conjunto estándar (`15/14/13/12/10/8`, repartido
libremente o siguiendo `reglas/generacion_personaje.yaml →
conjunto_estandar_por_clase` como sugerencia), compra por puntos (usa
`python3 calculo.py coste-compra --fue N --des N ... ` para validar que
suma 27) o aleatorio. Anota `caracteristicas.base`.

Aplica el ajuste del trasfondo (+2/+1 o +1/+1/+1 sobre las características
que listó el trasfondo) y guarda `caracteristicas.ajuste_trasfondo` y
`caracteristicas.final`.

## Paso 6 — Habilidades

La clase ofrece `atributos_basicos.habilidades.elige` opciones de
`atributos_basicos.habilidades.de`. **Si el bloque trae
`cualesquiera: true`** (algunas clases, ver
`clases/_ESQUEMA_atributos_basicos.md`), el jugador puede elegir *cualquiera*
de las 18 habilidades, no solo las listadas en `de` — muéstraselo así, con
el `literal` de la clase citado. Añade también, sin preguntar, las
habilidades fijas del trasfondo.

## Paso 7 — Equipo

Ofrece la opción A (objetos) o B (oro) del `equipo_inicial` de la clase, y
lo mismo para el trasfondo. Si la opción A incluye un objeto que un rasgo
concede sin venderse (como el libro de conjuros del Mago, en
`equipo/aventureros.yaml → objetos_de_rasgo_de_clase`), inclúyelo igual —
no depende de si el jugador eligió A o B, nace del rasgo.

## Paso 8 — Idiomas y herramientas

Idiomas de la especie/trasfondo más los que el trasfondo permita elegir
(`reglas/idiomas.yaml`). Herramienta que el trasfondo permita elegir.

## Paso 9 — Conjuros (solo si la clase es lanzadora)

Usa `python3 buscar.py conjuros-de <Clase> --nivel 0` para los trucos y
`--nivel 1` para los de nivel 1. Ofrece el número que indique
`atributos_basicos`/`progresion` de la clase para trucos conocidos y
conjuros preparados/conocidos de nivel 1.

## Paso 10 — Calcular y escribir la ficha

Con todo elegido, calcula (nunca a mano). Para lo que no depende de rasgos:

```bash
python3 calculo.py pb --nivel 1
python3 calculo.py cd-conjuros --aptitud <FINAL de la aptitud mágica> --nivel 1     # solo si lanzadora
python3 calculo.py ataque-conjuros --aptitud <FINAL de la aptitud mágica> --nivel 1  # solo si lanzadora
```

**Los PG y la CA NO se piden a `calculo.py`.** Desde la Fase 14 dependen de
efectos citados en los rasgos (la CA de Bárbaro, Monje, Bardo/Danza y
Hechicero/Dracónica; los PG del Enano y del Hechicero dracónico), y
`calculo.py ca --clase` **se niega a responder** cuando la respuesta depende de
un rasgo — correctamente, porque no puede saber el nivel, la subclase ni el
escudo. El camino bueno es escribir la ficha **sin** el bloque `calculado` y
pedirlo entero:

```bash
python3 verificar_personaje.py --calcular personajes/<nombre>.yaml
```

Eso imprime el bloque `calculado` ya listo para pegar, agregando los efectos que
el personaje de verdad tiene. Pega su salida tal cual.

Escribe `personajes/<nombre>.yaml` siguiendo **exactamente** el contrato de
`personajes/_ESQUEMA.md` (hay un ejemplo completo y verificado en
`personajes/_ejemplo_aerin.yaml`). Cada elección va también a `decisiones[]`
con su cita.

## Paso 11 — Verificar

```bash
python3 verificar_personaje.py personajes/<nombre>.yaml
```

Muestra el resultado al usuario. Si falla, corrige la ficha (nunca el
script) y vuelve a correrlo hasta que pase. No entregues una ficha que no
pasa `verificar_personaje.py`.
