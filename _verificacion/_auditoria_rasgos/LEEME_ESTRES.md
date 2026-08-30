# Briefing común: construir personajes para estresar el verificador

Vas a construir fichas de personaje de D&D 2024 (5.5e) **leyendo la base
canónica** que hay en `~/Documents/DnD/base-canonica/`. No estás jugando: estás
poniendo a prueba el **verificador** de este proyecto.

## Las cuatro reglas del método. Rómpelas y el experimento no vale nada

1. ⛔ **NO leas el código del verificador.** Prohibidos `verificar_personaje.py`,
   `validar.py`, `efectos.py`, `calculo.py`, `subir_nivel.py`,
   `generar_ficha.py`, `prerrequisitos.py`, `materiales.py`, `cobertura.py`,
   `buscar.py`, `verificar_*.py` y todo `_verificacion/`. Si vieras los
   chequeos, fabricarías violaciones que ya se cazan y evitarías las que no —
   justo al revés de lo que hace falta.
2. ⛔ **NO ejecutes ningún verificador ni script del proyecto.** Nada de
   `python3 ...`. Si pudieras, iterarías hasta ponerlo verde y destruirías la
   señal. Entregas la ficha y te vas.
3. ✅ **Escribe el sobre cerrado ANTES de terminar**, en su fichero aparte.
4. ⛔ **No toques nada dentro de `personajes/`** ni ningún fichero de la base.
   Solo escribes en `/tmp/estres/`.

## Lo que SÍ puedes leer (y debes)

- `personajes/_ESQUEMA.md` — **el contrato de una ficha**. Es tu referencia
  principal.
- `personajes/*.yaml` — ejemplos ya construidos, para ver el formato.
- `clases/*.yaml`, `clases/rasgos/`, `clases/subclases/`, `especies/`,
  `trasfondos/`, `dotes/`, `equipo/`, `reglas/`, `hechizos.json` — **la base es
  la autoridad**. Toda regla sale de ahí.

⛔ **Prohibido el conocimiento previo de D&D.** Si crees recordar una regla y no
está en la base, no existe. Varias reglas cambiaron en 2024 y lo que «suena
bien» es exactamente el modo de fallo que este proyecto combate.

## Qué entregas

**Entre 3 y 5 fichas**, cada una en `/tmp/estres/<tu-letra>-<n>.yaml`, siguiendo
el formato de `personajes/_ESQUEMA.md`.

Y **un sobre cerrado** en `/tmp/estres/<tu-letra>-sobre.md` con, **por cada
ficha**, una tabla de sus decisiones deliberadas:

```
## a-1.yaml — Guerrero 8

| # | Decisión | ¿Legal? | La regla de la base | Por qué |
|---|---|---|---|---|
| 1 | `final.fue` es 18 con base 15 y una sola mejora | ILEGAL | `dotes/generales.yaml#Mejora de característica`: «+2 a una, o +1 a dos» | 15+2 = 17, no 18 |
| 2 | Habilidad «Arcanos» elegida | ILEGAL | `clases/guerrero.yaml → atributos_basicos.habilidades.de` no la incluye | … |
| 3 | Todo lo demás | LEGAL | | |
```

**Cada decisión ILEGAL tiene que citar la regla concreta de la base que rompe**,
con fichero y campo. Si no puedes citarla, **no la declares ilegal**: será
descartada, y con razón.

Di también, para cada ficha, **cuántas decisiones ilegales lleva** — el que
puntúa necesita saber si encontró todas.

## Cómo se te puntúa

| | El verificador salta | El verificador calla |
|---|---|---|
| Decisión **ILEGAL** | ✅ el sistema funciona | 🔴 **hueco encontrado** |
| Decisión **LEGAL** | 🔴 **falso positivo** | ✅ el sistema funciona |

**Las dos casillas rojas valen igual.** Una ficha legal que el verificador
rechaza es tan buen hallazgo como una tramposa que deja pasar.
