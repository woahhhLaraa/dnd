---
name: subir-nivel
description: Sube de nivel un personaje de D&D 2024 (5.5e) ya existente en este proyecto, paso a paso y sin usar nada del conocimiento del modelo sobre las reglas. Usar cuando el usuario pida subir de nivel, avanzar o mejorar una ficha de personaje existente.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python3 *)
  - Bash(ls *)
---

# /subir-nivel — subida de nivel sobre la base canónica

Argumentos: `$ARGUMENTS` (opcional: ruta de la ficha y nivel destino).

## Regla que gobierna todo lo demás

**Consultar, no recordar.** No sabes reglas de D&D 2024 de memoria a efectos de
esta skill. **Qué pasa en cada nivel te lo dice `subir_nivel.py`**, que lo lee
de la tabla de la clase. Si te parece que falta algo, no lo añadas: dilo.

**Nunca hagas la aritmética a mente.** PG, CA, CD y bonificadores salen de los
scripts. Si un script no tiene lo que necesitas, dilo en vez de improvisarlo.

## Paso 0 — Precondición (obligatoria, no se salta)

```bash
python3 validar.py && python3 verificar_srd.py && python3 cobertura.py
```

Si alguno falla, **detente** y muestra el error. Y verifica la ficha de partida
antes de tocarla:

```bash
python3 verificar_personaje.py personajes/<nombre>.yaml
```

Si la ficha ya está mal, arréglala **antes** de subirla de nivel.

## Paso 1 — Qué pasa al subir

```bash
python3 subir_nivel.py --ficha personajes/<nombre>.yaml --a <nivel destino>
```

Devuelve, por cada nivel del salto, dos listas separadas:

- **`concede`** — lo que la base da sin preguntar: rasgos de clase con su
  página, rasgos de subclase, subida del bonificador por competencia, espacios
  de conjuro y columnas de la tabla (`ataque_furtivo`, `puntos_concentracion`…).
  **Enséñaselo al usuario, no le preguntes por ello.**
- **`elige`** — lo que el jugador decide y ningún script puede decidir por él.

Lee el texto de cada rasgo nuevo con la `ref` que trae el JSON y muéstraselo:
un rasgo concedido y no explicado es un rasgo que el jugador no va a usar.

## Paso 2 — Las elecciones, una por una

### Puntos de golpe (en cada nivel del salto)

Dos métodos, y elige el jugador:

```bash
python3 -c "import calculo; print(calculo.valor_establecido_pg('<Clase>'))"
```

- **valor establecido** — ese número, sin tirar;
- **tirada** — el jugador tira su dado de golpe y te da el resultado.

En ambos se suma el modificador por Constitución, **con un mínimo de 1 en el
total**. Anota en `pg_por_nivel` una entrada por nivel con `metodo` y el
**valor crudo** (nunca con el modificador ya sumado): el total se recalcula
solo, y por eso la subida de Constitución sale retroactiva sin tocar nada.

### Subclase (nivel 3)

Ofrece las opciones que trae `elige` y escribe la elegida en
`clases[].subclase` como `"clases/subclases/<clase>.yaml#<Subclase>"`.

### Mejora de característica **o dote**

Si el jugador sube características, **anótalo en `mejoras`** con su nivel y su
reparto (`{des: 2}` o `{des: 1, con: 1}`), y actualiza `caracteristicas.final`.
El verificador exige que `final` sea exactamente `base + ajuste_trasfondo +
mejoras`: una puntuación sin justificar es una puntuación inventada. Si en vez
de subir características toma una dote, va en `dotes:` con
`origen: {clase: X, nivel: N}` — cada nivel de mejora tiene que estar gastado de
una de las dos formas.


**No listes todas las dotes.** Pide las que el personaje puede tomar:

```bash
python3 buscar.py dotes-disponibles personajes/<nombre>.yaml
```

Devuelve `disponibles` y `bloqueadas`, **cada una con el porqué**. Ofrece solo
las disponibles y, si el usuario pregunta por una bloqueada, enséñale su motivo
en vez de discutirlo. `Mejora de característica` es ella misma una dote de la
base: si el jugador prefiere subir características, es esa.

### Conjuros (si la clase es lanzadora)

Las columnas `trucos` y `prep` aparecen en `elige` con su valor de antes y de
después. **El verificador cuenta**: los conjuros sin `origen` (o con un `origen`
que solo nombra la clase) tienen que ser exactamente los que dice la tabla, y
todo extra —dote, especie, opción de orden— tiene que declarar de dónde sale.

Ofrece con:

```bash
python3 buscar.py conjuros-de <Clase> --nivel <N>
```

## Paso 3 — Escribir la ficha

Edita la ficha **existente**, no crees otra. Actualiza `nivel_total`,
`clases[].nivel`, `pg_por_nivel`, y lo que corresponda de `conjuros`, `dotes`,
`competencias`. Cada elección va también a `decisiones[]` con su `en: "nivel N"`
y su cita.

**No escribas `calculado` a mano.** Pídelo:

```bash
python3 verificar_personaje.py --calcular personajes/<nombre>.yaml
```

y pega su salida tal cual.

## Paso 4 — Verificar

```bash
python3 verificar_personaje.py personajes/<nombre>.yaml
```

Muestra el resultado. Si falla, corrige **la ficha**, nunca el script, y repite
hasta que pase. No entregues una ficha que no verifica.

## Lo que esta skill NO hace todavía, y conviene decirlo

- **Multiclase.** `subir_nivel.py` se detiene si la ficha tiene más de una
  clase. Las reglas están en `reglas/generacion_personaje.yaml → multiclase`,
  pero nadie las ha automatizado.
- **El «mínimo de 1» de los PG con Constitución negativa.** Si algún nivel lo
  toca, `verificar_personaje.py` **avisa**: la base no resuelve cómo interactúa
  eso con la regla retroactiva. No lo decidas tú.
