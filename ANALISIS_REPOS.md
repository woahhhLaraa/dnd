# Qué sacamos de DiceCloud, Foundry dnd5e, PCGen y Open5e

> Fecha: **2026-08-21**. Investigación sobre el código real de los cuatro
> proyectos (clonados y leídos, no sus README).
> Complementa a `FODA.md`; lo que aquí se propone alimenta la **Fase 8b**.

## Conclusión en una línea

**Ninguno aporta contenido que sustituya a la base** (todos son inglés y/o
subconjunto SRD). Lo que aportan es **arquitectura** para `calculo.py` y
**vocabulario** para `/subir-nivel`, más una **segunda fuente de contraste ya
estructurada** que amplía `verificar_srd.py` mucho más allá de las tablas de clase.

| Proyecto | Licencia | Qué tomamos | Qué NO |
|---|---|---|---|
| DiceCloud v2 | GPL-3.0 | Modelo de efectos + orden de agregación + grafo de dependencias | Su código (GPL contagia); es Meteor/MongoDB |
| Foundry dnd5e | MIT (código) / CC-BY-4.0 (contenido) | Taxonomía de *advancement* + datos SRD 5.2 estructurados | La plataforma; el contenido en inglés no entra en la base |
| PCGen | LGPL | Solo la **idea** de prerrequisitos componibles | Todo lo demás: es 3.5e, Java, formato LST arcaico |
| Open5e | CC-BY-4.0 | Ampliar la verificación externa (ya conectado) | Que sea autoridad; y ojo con el filtro (ver trampa abajo) |

Material descargado y colocado:

- `_verificacion/foundry_srd52/` — datos SRD 5.2 estructurados (fuente de contraste)
- `../_referencias/dicecloud-motor/` — motor de cómputo (referencia de diseño)
- `../_referencias/foundry-advancement/` — sistema de subida de nivel (referencia de diseño)

Los dos últimos van **fuera de `base-canonica/`** a propósito: son código para
leer, jamás autoridad sobre una regla. Nada de esto puede entrar en `clases/`,
`hechizos.json`, `especies/` ni `trasfondos/` — la regla 4 (solo edición 2024,
castellano, del manual) sigue intacta.

---

## 1. DiceCloud — el motor de efectos

**El problema que resuelve.** Hoy `calculo.py` son funciones puras
independientes con los casos especiales cableados en Python:

```python
_CA_SIN_ARMADURA = {
    "Bárbaro": lambda des, con, sab: 10 + des + con,
    "Monje":   lambda des, con, sab: 10 + des + sab,
}
```

Cada regla nueva es otra rama de código. Y ya hay una fuga documentada: el
campo `bonus_pg_especie` de `personajes/_ESQUEMA.md` existe porque «Aguante
enano» (+1 PG) **no era representable** — el esquema mismo admite que es un
parche porque el rasgo es prosa, no dato.

**Cómo lo resuelve DiceCloud.** Un efecto es un registro con tres campos:
una **operación**, una **cantidad** y los **nombres de variable** a los que
apunta (`app/imports/api/properties/Effects.ts`):

```
operation ∈ { base, add, mul, min, max, set,
              advantage, disadvantage, passiveAdd, fail, conditional }
amount    : fórmula (puede referirse a otras variables)
stats     : [nombres de variable objetivo]
```

**El orden de agregación**, que es la joya, está en
`computeVariable/getAggregatorResult.js` y es fijo y determinista:

```
base   = max(efectos.base, valorBaseDelStat)
result = (base + Σ add) * Π mul
result = clamp(result, Σ min, Σ max)
si hay set: result = set          ← set gana sobre todo
result = floor(result)            ← salvo stats decimales
```

Traducido a nuestro caso: «Defensa sin armadura» del Monje deja de ser un
`lambda` y pasa a ser un efecto en `clases/rasgos/monje.yaml` — con su página
citada, como todo lo demás. «Aguante enano» deja de necesitar campo especial.
El escudo (+2) deja de ser un `if`.

**Lo segundo que vale.** El grafo de dependencias
(`buildCreatureComputation.ts` + `computeCreatureComputation.ts`) hace
recorrido en profundidad y, cuando detecta un ciclo, **lo registra como error
explícito** (`type: 'dependencyLoop'`) en vez de colgarse o devolver un número
plausible. Es exactamente la doctrina «fallar ruidosamente» de `buscar.py`,
aplicada a la aritmética.

**Aviso legal.** DiceCloud es **GPL-3.0**. Se leen los conceptos y se
reimplementa en Python; **no se copia código**. Los ficheros en
`../_referencias/dicecloud-motor/` son para leer.

## 2. Foundry dnd5e — el vocabulario de subida de nivel

Esto es **directamente la Fase 8b**. Foundry no trata «subir de nivel» como un
procedimiento, sino como una **lista de objetos `advancement`** colgados de la
clase, cada uno con su nivel. Del `barbarian.yml` real:

```
ScaleValue              (sin nivel) 'Rage Damage'   {"1":2, "9":3, "16":4}
ItemGrant               L1,2,3,5,7,9,11,13,15,17,18,20  'Class Features'
AbilityScoreImprovement L4, L8, L12, L16, L19
Trait                   L1  'Skill Proficiencies' / 'Weapon Mastery' / …
Trait                   L3  'Primal Knowledge'
Subclass                L3
HitPoints               (sin nivel)
```

Los **nueve tipos** (`../_referencias/foundry-advancement/`) son la taxonomía
completa de «qué puede pasar al subir de nivel»: `ItemGrant`, `ItemChoice`,
`AbilityScoreImprovement`, `Trait`, `ScaleValue`, `Subclass`, `HitPoints`,
`Size`, `ModifyItem`. Con eso, `/subir-nivel` no improvisa qué preguntar: lee
la lista para el nivel destino y pregunta exactamente lo que haya.

Tres detalles que valen por sí solos:

- **`apply(level, data)` / `reverse(level)`** — cada advancement sabe
  deshacerse. Una subida de nivel reversible. Encaja con el bloque
  `decisiones` de nuestra ficha, que ya es un log auditable.
- **`ScaleValue` como tabla dispersa** (`{"1":2,"9":3,"16":4}`) — forma
  normalizada de las columnas numéricas de `clases/*.yaml`.
- **`Trait` separa `grants` de `choices`** — `grants` es lo automático,
  `choices: [{count: 1, pool: [...]}]` es «elige N de esta lista», y un pool
  abierto es «cualquiera». **Esto es exactamente el problema del Bardo** que
  `CONTINUAR.md` documenta: nuestro `cualesquiera: true` + `de:` es el mismo
  concepto expresado con dos campos que se contradicen si alguien lee solo
  uno. El modelo de Foundry lo dice sin ambigüedad.

## 3. `_verificacion/foundry_srd52/` — la segunda fuente de contraste

Hoy `verificar_srd.py` contrasta **646 valores, solo de las 12 tablas de
clase**, contra Markdown que hay que parsear a mano. Los paquetes de Foundry
traen el mismo SRD 5.2 (`source.rules: "2024"`, `license: "CC-BY-4.0"`) ya
estructurado en YAML campo a campo:

| Carpeta | Registros | Sirve para contrastar |
|---|---|---|
| `spells24/` | 352 | nivel, escuela, componentes, concentración, ritual, alcance de `hechizos.json` |
| `equipment24/` | 679 | precios, peso, propiedades, CA de `equipo/*.yaml` |
| `origins24/species/` | 61 | rasgos de `especies/especies.yaml` |
| `origins24/backgrounds/` | 4 | `trasfondos/trasfondos.yaml` |
| `feats24/` | 21 | `dotes/*.yaml` |
| `classes24/` | 12 + subclases | ya cubierto, pero con más campos |

Los 352 conjuros **cuadran exactamente** con la cifra que `_verificacion/LEEME.md`
ya atribuye al SRD — buena señal de que las dos copias del SRD 5.2 coinciden.

Ojo: sigue siendo **subconjunto y en inglés**. Confirma, no completa, igual que
`srd52/`. Un desajuste manda a leer la página del manual, no a copiar.

## 4. Open5e — ya estábamos conectados, y hay una trampa

`_verificacion/srd2024_open5e_clases.json` ya salió de esta API. Cobertura real
medida hoy con `document__key=srd-2024`:

```
spells 339 · items 440 · classes 24 (12 + 12 subclases) · feats 17 · backgrounds 4
```

**La trampa, y es seria:** `api.open5e.com/v2/<endpoint>/` **sin filtrar
devuelve por defecto contenido de Advanced 5th Edition (A5E)**, un sistema de
terceros que no es D&D. Lo comprobé: la primera página de `/v2/classes/` viene
del documento `a5e-ag` («Adventurer's Guide»). Cualquier consulta a esta API
**debe** llevar `document__key=srd-2024`, o estaremos metiendo reglas de otro
juego creyendo que son SRD. Esto es del mismo género que el bug `Clerigo`: no
falla, devuelve algo plausible y equivocado.

Dos notas menores: `/v2/races/` no existe (404) — las especies hay que sacarlas
de `origins24/` de Foundry; y `feats` (17) y `backgrounds` (4) confirman lo que
`LEEME.md` ya decía, que el SRD cubre ~23-25% de nuestras dotes y trasfondos.

## 5. PCGen — una idea, y solo una

No merece la pena descargarlo: es Java, orientado a 3.5e/Pathfinder, y su
formato LST es de los años del CD-ROM. Pero su sistema de prerrequisitos es
**prerrequisitos como dato componible**, no como prosa:

```
PRESTAT:1,INT=19,WIS=19,CHA=19
PREABILITY:1,CATEGORY=Feat,Power Attack
PREMULT:2,[PREAGESET:1,Middle Age],[!PREAGESET:1,Old]
```

Un `!` delante invierte; `PREMULT:N,[...],[...]` exige que se cumplan N de los
bloques. La `FUENTES.md` ya registra que **toda dote tiene prerrequisito** y que
por eso el capítulo 5 fue lectura visual obligatoria. Hoy ese prerrequisito vive
como texto. Convertirlo en algo evaluable es lo que permitiría que
`/subir-nivel` **ofrezca solo las dotes que el personaje puede tomar** en vez de
listarlas todas y confiar en que el LLM lea bien.

---

## Riesgo principal de todo esto

Estos cuatro proyectos son **2014/SRD/inglés**. La amenaza nº 1 de `FODA.md` —
que el modelo rellene huecos con la edición vetada — se agrava si tenemos
`_verificacion/foundry_srd52/` a mano y alguien lo trata como fuente en vez de
como contraste. Reglas que no cambian:

1. Un dato solo entra en la base **leído del manual castellano 2024, con página**.
2. Estas fuentes solo pueden **contradecir** un dato (y disparar una relectura),
   nunca **aportarlo**.
3. Ante discrepancia, manda el manual. Ya pasó: el SRD **omite** la mejora de
   característica de nivel 10 del Pícaro que el manual sí trae.
