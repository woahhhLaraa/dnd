# Esquema de los efectos (Fase 14)

Un **efecto** es una regla mecánica escrita como dato citado, en vez de como
una rama de código. Vive **pegado al registro que la concede** — el rasgo, el
rasgo de subclase, el rasgo de especie — y lleva la página de ese registro.

```yaml
- nombre: "Defensa sin armadura"
  nivel: 1
  pagina: {pdf: 151, libro: 149}
  desc: "Mientras no lleves armadura ni portes un escudo, tu clase de armadura base es 10 + modificador de Destreza + modificador de Sabiduría."
  efectos:
    - {objetivo: ca, op: base, formula: "10 + mod_des + mod_sab", requiere: [sin_armadura, sin_escudo], pagina: {pdf: 151, libro: 149}}
```

| Campo | Qué es |
|---|---|
| `objetivo` | La variable que toca. Vocabulario cerrado en `reglas/efectos.yaml`. |
| `op` | `base` · `add` · `mul` · `min` · `max` · `set`. Vocabulario cerrado. |
| `formula` | Aritmética entera sobre variables declaradas: `+ - *`, paréntesis y `min(a,b)` / `max(a,b)`. Nada más. |
| `requiere` | Condiciones que deben cumplirse **todas**. Vocabulario cerrado. Ausente = siempre aplica. |
| `pagina` | Obligatoria y numérica. Regla 2 del proyecto: sin página, un dato no entra. |

## Por qué existe

`calculo.py` traía las fórmulas de "Defensa sin armadura" como `lambda`
indexadas por nombre de clase:

```python
_CA_SIN_ARMADURA = {"Bárbaro": lambda …, "Monje": lambda …}
```

con el comentario *«son las dos únicas excepciones en el tronco de clase,
confirmado por grep sobre las 12 clases»*. Era cierto, y por eso mismo era el
problema: **la base tiene cuatro fórmulas de CA base**, y las otras dos están
en subclases — *Juego de pies deslumbrante* (Bardo, pdf 66) y *Resistencia
dracónica* (Hechicero, pdf 135). El grep miró donde el `lambda` sabía mirar.

Lo mismo con los PG: `personajes/_ESQUEMA.md` tenía un campo `bonus_pg_especie`
que el propio esquema admitía como parche. Cubría **1 de los 2** efectos sobre
PG máximos de la base, guardaba un `1` fijo cuando el rasgo dice *«y en 1 más
cada vez que subes de nivel»*, y nadie obligaba a rellenarlo: la única ficha de
Enano de la base lo tenía vacío y **verificaba en verde con los PG mal**.

Una regla cableada no se puede citar, no se puede validar y no se entera de que
existe una quinta.

## Reglas

1. **El efecto no repite el texto: lo acompaña.** `desc` sigue siendo la
   autoridad legible; el efecto es su forma calculable. Si los dos discrepan,
   manda la página.
2. **Un efecto nunca se copia a la ficha del personaje.** La ficha referencia el
   rasgo; los efectos se recogen al calcular. Es la regla central de
   `personajes/_ESQUEMA.md` aplicada a la aritmética: si la base se corrige, el
   personaje se entera solo.
3. **Lo que ya está estructurado no se duplica como efecto.** El `+2` del escudo
   y las fórmulas de armadura se **derivan** en código del campo `ca` que ya
   tiene `equipo/armaduras.yaml`. Escribir el `+2` otra vez al lado del `+2`
   sería el modo de fallo nº 10 de este proyecto («dato agregado»): dos copias
   que nadie vuelve a comparar y que divergen en silencio.
4. **Si el texto promete una mecánica, tiene que haber un efecto.**
   `validar_efectos()` lee las `desc` buscando promesas («CA base», «PG máximos
   aumentan») y falla si no hay efecto detrás. Es la mitad del chequeo que
   cubre el defecto que de verdad ocurrió: no un dato malo, un dato que falta.

## El orden de agregación, y la divergencia deliberada

El orden viene de DiceCloud v2 (`getAggregatorResult.js`), leído como concepto y
reimplementado — DiceCloud es GPL-3.0 y no se copia código (ver
`ANALISIS_REPOS.md` §1):

```
base → + Σadd → × Πmul → acotar entre min y max → set gana sobre todo → floor
```

**Con una divergencia, y es a propósito.** DiceCloud resuelve varios `base` a la
vez con `max()`. El manual castellano 2024 dice otra cosa:

> Si el personaje tiene varias formas de calcular su CA (p. ej. Defensa sin
> armadura de monje y Resistencia dracónica de hechicero), solo puede
> beneficiarse de una, **a elegir**.
> — `reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`

Elegir no es maximizar. El motor **exige** que la ficha declare cuál en
`elecciones.ca_base` y **falla ruidosamente** si hay más de una aplicable sin
elección. Coger la mayor acertaría casi siempre, y eso es indistinguible de
acertar por casualidad — amenaza nº 5 del `FODA.md`.

## Lo que este esquema todavía NO representa

Se declara, en vez de fingir que está cubierto:

- **Escalado por nivel.** «Movimiento sin armadura» del Monje da +3 m en nivel 2,
  +4,5 en el 6, +6 en el 10… Es una **tabla dispersa con decimales**, que es el
  `ScaleValue` de Foundry (`ANALISIS_REPOS.md` §2) y pide su propia decisión de
  modelo. **Esa decisión se tomó el 2026-08-30 y `velocidad` SÍ está en el
  vocabulario desde entonces**, resuelta sin inventar escalado: el efecto
  LEE la columna `mov_sin_armadura_m` de la progresión del Monje con
  `columna:` en vez de copiarla. (Este párrafo decía lo contrario hasta el
  2026-09-06; lo destapó un calculista a ciegas, no ningún chequeo: la
  prosa de los `_ESQUEMA` no la contrasta nadie.)
- **La CA base de quien no lleva nada** (`10 + mod_des`) **ya tiene página
  citada**: pdf 43 = libro 41, desde el 2026-08-30, tras dos lecturas
  independientes que coincidieron palabra por palabra. Venía como literal sin
  cita en `calculo.py`. Se declara
  con `_falta_cita: true` en `reglas/efectos.yaml` y `validar_efectos()` avisa
  mientras siga abierta. Cerrarla es **una** lectura de página.
- **Ventaja/desventaja, resistencias y competencias** no son variables
  numéricas y no entran aquí. DiceCloud las trata con operaciones aparte
  (`advantage`, `fail`, `conditional`); cuando hagan falta, se añaden al
  vocabulario con el mismo método, no se improvisan.
