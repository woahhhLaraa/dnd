# Hallazgos — Dracónido / Monje / Ermitaño (nivel 1)

## 1. Qué funcionó bien

- Los tres guardarraíles previos (`validar.py`, `verificar_srd.py`,
  `cobertura.py`) pasaron limpios antes de tocar nada.
- `_ESQUEMA.md` y `_ejemplo_aerin.yaml` (versión corregida) son coherentes
  entre sí y con el código de `verificar_personaje.py`; no encontré
  contradicciones nuevas de ese tipo.
- La fórmula especial de CA del Monje (10 + mod Des + mod Sab, sin
  armadura) está codificada explícitamente en `calculo.py` (`_CA_SIN_ARMADURA`)
  y se confirmó con `python3 calculo.py ca --des 15 --con 14 --sab 16
  --clase Monje` → `15` (10+2+3), distinta de la genérica 10+Des=12. No pasé
  `--armadura`, como pedía la tarea.
- `python3 buscar.py equipo "Bastón"` sin `--archivo` devuelve en silencio
  la primera coincidencia (la de `equipo/armas.yaml`, el arma) en vez de
  fallar o avisar de la ambigüedad con `equipo/aventureros.yaml#Bastón`
  (canalizador arcano). No es un bug bloqueante para esta ficha —usé
  `--archivo` explícito igualmente, como exige el esquema— pero el
  comportamiento por defecto de `buscar.equipo()` sin `archivo` es
  "silenciosamente ambiguo", lo cual invita a error si alguien construye una
  ref a mano sin pasar por la herramienta.
- La ficha final pasa `verificar_personaje.py` con 0 problemas (ver
  sección 5).

## 2. Bugs o comportamientos raros

### Bug real: `verificar_categorias()` no considera el trasfondo para
`competencias.armas/armaduras/herramientas`, aunque el propio `_ESQUEMA.md`
dice que sí debería.

`_ESQUEMA.md`, regla 6: "se comprueban contra la lista real de
`atributos_basicos` de la clase (**o del trasfondo cuando aplique**)".

Pero en `verificar_personaje.py`, `verificar_categorias()` solo recorre
`ficha["clases"]` para construir `permitidas`:

```python
for c in ficha.get("clases", []):
    clase_d = buscar.clase(c["clase"])
    permitidas |= set(clase_d.get("atributos_basicos", {}).get(campo, []))
```

Nunca añade `ficha["trasfondo"]`. El trasfondo Ermitaño concede
`herramienta: "útiles de herborista"` de forma fija (igual que concede
habilidades fijas), pero **no hay ningún campo `atributos_basicos.herramientas`
de trasfondo que lo respalde** en esa función. Si se añade una entrada:

```yaml
herramientas:
  - {categoria: "útiles de herborista", origen: {trasfondo: Ermitaño}}
```

`verificar_personaje.py` falla con:

```
✗ competencias.herramientas: 'útiles de herborista' no está en lo que
  conceden las clases del personaje (['Un tipo de herramientas de artesano
  o instrumento musical a elección'])
```

Contraste: `verificar_habilidades()` sí mezcla trasfondo + clase
correctamente (`permitidas |= set(tf.get("habilidades", []))`). El mismo
patrón falta en `verificar_categorias()` para armas/armaduras/herramientas.
Reporto sin arreglar, como se pidió — dejé la ficha final **sin** listar la
competencia de herramienta del trasfondo en `competencias.herramientas` para
poder pasar la verificación, y documenté la omisión en un comentario dentro
del propio YAML.

### Comportamiento confirmado (no bug): duplicado de nombre "Bastón"

Igual que la ronda anterior detectó, "Bastón" existe en dos ficheros con
significados distintos:
- `equipo/armas.yaml#Bastón` → arma sencilla cuerpo a cuerpo (1d6
  contundente, "2 pp").
- `equipo/aventureros.yaml#Bastón` (bajo `canalizadores_arcanos`) → foco de
  lanzamiento arcano ("5 po").

El equipo de opción A del trasfondo Ermitaño ("bastón, útiles de
herborista...") es el bastón como objeto mundano/arma, no un canalizador
arcano (el Monje no lanza conjuros). Usé
`{ref: "equipo/armas.yaml#Bastón", ...}` explícitamente. Sin el `archivo:`
en la ref, `buscar.equipo("Bastón")` habría devuelto la misma entrada por
casualidad (es la primera que encuentra), pero no hay garantía de que el
orden de búsqueda coincida siempre con la intención — ver punto anterior
sobre el comportamiento silencioso.

## 3. Documentación confusa

- `_ESQUEMA.md` no aclara en qué fichero de `equipo/` vive cada categoría
  (armas, armaduras, aventureros, herramientas). Tuve que grepear
  `equipo/*.yaml` a mano para descubrir que "Útiles de herborista" vive en
  `equipo/herramientas.yaml`, no en `equipo/aventureros.yaml` donde están
  "Útiles de escalada" y "Útiles de sanador" (ambos con nombre similar,
  ¡pero en otro fichero!). Mi primer intento de ref
  (`equipo/aventureros.yaml#Útiles de herborista`) falló con "no existe un
  objeto llamado...". El mensaje de error de `verificar_personaje.py` es
  claro y útil, así que el coste fue solo un intento extra — pero un
  índice de "qué categoría vive en qué fichero de equipo/" en `_ESQUEMA.md`
  ahorraría ese tanteo.
- SKILL.md (paso 7) no menciona que el `archivo:` de la ref de equipo es
  obligatorio para desambiguar; eso solo está documentado en `_ESQUEMA.md`
  regla 1. Alguien que siga solo SKILL.md podría escribir una ref sin
  fichero y que "funcione" por casualidad (ver punto 2).

## 4. Huecos de datos

- **No existe ningún catálogo de instrumentos musicales ni de tipos
  concretos de "herramientas de artesano" en `equipo/`.** La opción A del
  equipo inicial del Monje es literalmente "lanza, 5 dagas, herramientas de
  artesano o instrumento musical elegido para la competencia con
  herramientas, paquete de explorador y 11 po" (`clases/monje.yaml`), pero
  no hay ningún registro tipo "Flauta", "Herramientas de herrero", etc. con
  precio/peso para referenciar como objeto concreto (confirmé con `grep -in
  "Herramientas de\|Instrumento"` sobre `equipo/*.yaml`: sin resultados,
  salvo la mención de pasada dentro de la descripción de la dote
  `Fabricante` en `dotes/origen.yaml`, que no es un registro de equipo). No
  incluí ese objeto en la ficha final; lo dejé documentado como comentario
  en el YAML. Esto también afectaría a cualquier ficha de Bardo que quiera
  concretar su instrumento.
- Tampoco hay una `útiles de sanador` en la lista de equipo inicial del
  Ermitaño ni del Monje, aunque la dote `Sanador` (que el trasfondo Ermitaño
  concede automáticamente) depende de tener ese objeto encima ("si tienes
  útiles de sanador, puedes gastar un uso..."). No es un error de la base
  —así está el trasfondo oficialmente, sin ese objeto— pero es un hueco
  jugable real: con la ficha tal cual, la dote Sanador es actualmente
  inutilizable hasta que el personaje compre "Útiles de sanador" (5 po,
  `equipo/aventureros.yaml#Útiles de sanador`) con oro propio.

## 5. Salida final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/draconido_monje.yaml
14 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Ficha: `personajes/draconido_monje.yaml`.
Cálculos usados (todos vía `calculo.py`, ninguno a mano):
- `python3 calculo.py mod 15` → 2 (Des)
- `python3 calculo.py mod 14` → 2 (Con)
- `python3 calculo.py mod 16` → 3 (Sab)
- `python3 calculo.py pg --dado d8 --con 14` → 10
- `python3 calculo.py pb --nivel 1` → 2
- `python3 calculo.py ca --des 15 --con 14 --sab 16 --clase Monje` → 15
  (sin `--armadura`, confirma que aplica 10+Des+Sab del Monje y no la
  fórmula genérica 10+Des)
