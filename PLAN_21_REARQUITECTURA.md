# PLAN 21 — rearquitecturar los guardianes, no seguir parcheándolos

> Aprobado el 2026-09-06. Sale del cierre del `PLAN_20`, y del encargo que la
> usuaria dejó anotado en `CONTINUAR.md`: *«los validadores, debemos dar por
> hecho que SIEMPRE MIENTEN»*.

## Contexto

El `PLAN_20` cerró el 2026-09-06, y su resultado más incómodo no fue ninguna de
las cinco fases: fue que **en un solo día cada guardián del repositorio se cazó
a sí mismo, y ninguno se había cazado antes**.

| Guardián | Decía | Pasaba |
|---|---|---|
| `verificar_chequeos` | «ninguna rama silenciosa nueva» | 67 ramas con línea base 64: su huella colapsaba las gemelas |
| `censo` | «0 sin declarar» | `equipo/` fuera del universo, **y una mutación lo blindaba** |
| `validar` | «0 errores» | tres vocabularios cerrados sin ningún consumidor |
| `validar` | «0 errores» | dos chequeos que reventaban sin imprimir su etiqueta |
| `mutaciones_motor` | «cobertura perdida» | falso: era una descripción reescrita |
| `calculo.ca()` | — | cableaba el `10` que la base declaraba y `efectos.py` leía |

La usuaria lo nombró: *«queda claro que los validadores, debemos dar por hecho
que SIEMPRE MIENTEN, creo que en futuro se debería hacer una
rearquitecturación de código»*.

El patrón que lo explica: **un verificador que se comprueba a sí mismo no
comprueba nada**. Los seis se destaparon desde fuera —una mutación, un agente a
ciegas, otro verificador—, nunca solos.

**Este plan NO arregla esos seis casos** (ya están arreglados) ni busca más
instancias. Arregla las cuatro formas que los hicieron posibles.

---

## Lo medido, el 2026-09-06, antes de escribir nada

**Frente 2 — cinco ficheros de deuda, cinco implementaciones, ninguna completa:**

| fichero | poda | nuevo ≠ perdido | guarda elenco | identidad |
|---|:--:|:--:|:--:|---|
| `chequeos_silenciosos.json` (65) | sí | no | no | texto + condición + ordinal |
| `rasgos_sin_declarar.json` (480) | **no** | no | no | `archivo#nombre` |
| `efectos_sin_carga.json` (0) | sí | no | no | `efecto:archivo#rasgo·obj·op` |
| `motor_sin_carga.json` (3) | sí | **sí** | **sí** | nombre de función |
| `constantes_de_dominio.json` (23) | sí | no | no | huella de conjunto |

`motor_sin_carga` es el único que aprendió las tres lecciones —y las aprendió
el último día, a golpes—. Las otras cuatro no las tienen porque se escribieron
antes. **Es una abstracción, escrita cinco veces, con cuatro copias viejas.**

**Frente 1 — seis scripts de la raíz sin ninguna suite que mute su código:**
`_convertir_hechizos.py`, `cobertura.py`, `generar_ficha.py`, `materiales.py`,
`prerrequisitos.py`, `subir_nivel.py`.

**Frente 3 — el muro de errores existe en un sitio y medio:** `validar._correr()`
(13 usos, captura `Exception`), `verificar_personaje` con un `try/except`
parcial (solo `KeyError` y `SystemExit`, líneas 1404-1411), y **sin muro**:
`censo`, `verificar_chequeos`, `verificar_srd`, `verificar_foundry`,
`verificar_documentos`, `cobertura`.

**Frente 4 — seis convenciones de identidad** para la misma pregunta «¿es esta
la misma unidad que ayer?»: las cinco de la tabla más la del censo (`tipo:algo`).
Las tres veces que se eligió mal, el verificador mintió.

---

## Fase 1 · Una sola abstracción de deuda enumerada

**Logra:** que las cuatro implementaciones viejas hereden lo que solo tiene la
quinta, y que la sexta no se escriba nunca. Va primero porque arrastra el
frente 4: la regla de identidad se declara aquí, una vez.

**Nuevo `deuda.py`** en la raíz (entra como unidad del censo, que es lo
correcto), con una clase `Deuda` cuyo contrato sale de lo medido, no inventado:

```python
Deuda(fichero, nota, como_se_salda, identidad)
    .contrastar(medido_hoy: dict[id, str], elenco_hoy: set[id] | None) -> Informe
```

- `medido_hoy` — lo que hoy sigue siendo deuda, `{id: descripción}`.
- `elenco_hoy` — TODO lo que se midió, no solo lo que falló. Sin esto no se
  puede distinguir «una prueba nueva mide algo que nunca estuvo cubierto» de
  «algo que se cubría ha dejado de cubrirse», y `mutaciones_motor` llamó
  regresión a lo primero.
- `identidad` — una cadena que DESCRIBE la regla («el nombre de la función»,
  «la huella del conjunto de cadenas»). No se puede verificar sola, y por eso
  se guarda dentro del fichero: un lector futuro ve con qué se comparó.

El `Informe` distingue cuatro cosas, que hoy solo `motor_sin_carga` separa:
`saldados` (se podan, y la poda se imprime), `medidos_nuevos` (id que no estaba
en el elenco previo → medición nueva, **no** regresión, se anota), `perdidos`
(id que estaba en el elenco previo y NO era deuda, y hoy sí → **rojo**), y
`vigentes`.

**Se migran las cinco**, cada una conservando su identidad actual —cambiarla
invalidaría su fichero, y eso es el error que este plan persigue—:

| llamador | fichero | qué gana |
|---|---|---|
| `verificar_chequeos.main()` | `chequeos_silenciosos.json` | elenco, distinguir nuevo de perdido |
| `censo.fila_rasgos` | `rasgos_sin_declarar.json` | **poda**, elenco, nuevo ≠ perdido |
| `censo.fila_efectos_con_carga` | `efectos_sin_carga.json` | elenco, nuevo ≠ perdido |
| `censo.fila_constantes_de_dominio` | `constantes_de_dominio.json` | elenco, nuevo ≠ perdido |
| `mutaciones_motor.main()` | `motor_sin_carga.json` | nada: es el modelo |

`validar.py:2289-2340` lee `rasgos_sin_declarar.json` para su propio chequeo:
pasa a leerlo por `deuda.Deuda(...).vigentes` en vez de abrir el JSON a mano.

**Se comprueba:** `_verificacion/mutaciones_deuda.py` (nueva), que muta la
ABSTRACCIÓN y exige que las cinco lo noten —una por cada propiedad: se quita la
poda, se confunde nuevo con perdido, se borra el elenco, se cambia la
identidad—, más un control negativo: reescribir la `nota` de un fichero no
puede hacer saltar nada.

**Cifras:** se remiden. Es previsible que `rasgos_sin_declarar` no cambie hoy
(0 entradas muertas medidas), pero podrá podar cuando toque.

### ✅ FASE 1 CERRADA (2026-09-06) — lo que salió, remedido

`deuda.py` en la raíz, las cinco migradas sin tocar ninguna identidad, los
cinco llamadores movidos y `validar.py` leyendo por `Deuda(...).vigentes` en
vez de abrir el JSON a mano. La guarda `_verificacion/mutaciones_deuda.py`
**10/10** (8 que deben notarse, 2 controles negativos).

**Cuatro cosas se aprendieron por el camino, y las cuatro son la misma:**

1. **La suite sacó 2/7 en su primera versión.** Corría los cinco llamadores
   contra la base intacta, y con los cinco ficheros en reposo —nada que podar,
   nada nuevo, nada perdido— quitar la poda no cambia ni un byte. Es el tercer
   caso en dos días de **una mutación que solo cambia el comportamiento en una
   situación que no ocurre**. El arnés pasó a FABRICAR cada situación con un
   fichero de deuda desechable.
2. **Fabricarlas destapó un defecto real de `deuda.py`, contra el control,
   antes de mutar nada:** el elenco no llegaba al disco cuando la deuda no se
   movía. Una prueba que empieza a medir más no se distinguía, a la pasada
   siguiente, de una regresión — exactamente el fallo que la abstracción
   existe para no repetir.
3. **La comprobación de identidad salió 6/7 por el arnés, no por `deuda.py`:**
   preguntaba `"LANZO" in salida` contra las respuestas «LANZO» y «NO_LANZO»,
   y «NO_LANZO» contiene «LANZO». La propiedad daba por buena justo la
   respuesta que tenía que delatar. Comparación exacta, y salta.
4. **La migración rompió `verificar_chequeos`, y el guardián lo dijo.** Al
   pasarlo a `deuda.py`, «rama nueva» quedó leído como `perdidos`, así que una
   rama silenciosa en código NUEVO —que nunca estuvo en el elenco— salía en
   verde; antes de migrar, cualquier huella fuera de la línea base era roja.
   `mutaciones_silencios` lo cazó a la primera: **3 de 6**, sus tres mutaciones a
   la vez. El arreglo NO fue en el llamador: distinguir lo nuevo de lo perdido
   es una MEDICIÓN y la hacen los cinco, pero **si lo nuevo es aceptable es
   una POLÍTICA del fichero**, y ahora se declara en el `Deuda` junto a la
   identidad (`cerrada=True`). `motor_sin_carga` acepta mediciones nuevas;
   `chequeos_silenciosos` no acepta ninguna. Vuelve a 6/6, y la política tiene
   su propia mutación.

**Y una mutación cambió de vehículo, no de chequeo** —la regla de esta casa
cuando una premisa deja de ser cierta—. `m_deuda_muerta` metía a mano un rasgo
obsoleto en `rasgos_sin_declarar.json` y exigía que el censo lo cazara, porque
esa fila NO PODABA. Ahora poda: la entrada muerta sale sola, se anuncia como
saldada y el recuento no se mueve (remedido: 938 · 0 sin declarar). La premisa
se cayó **porque el defecto se cerró**. Así que la mutación se movió a la otra
dirección, peor y sin vigilancia: `m_deuda_rehecha` borra el fichero y exige
que el censo pare, porque sin él la línea base se rehace con lo medido hoy y
los 480 rasgos sin declarar quedarían «declarados» de golpe, en verde.

**El guion que migró los cinco escribió su prosa en blanco**, y como
`_escribir` prefería siempre lo del disco —para que la prosa se pueda editar a
mano—, `_como_se_salda` quedó VACÍO en tres de los cinco: el campo que dice
cómo se paga una deuda, sin forma de repararlo desde el llamador, que sí lo
tenía escrito. La migración también se llevó el `_ultima_poda` de
`efectos_sin_carga.json`, que nombraba los tres efectos saldados el día antes;
restaurado de git. Hoy una prosa vacía no le gana a la del código, y
**la condición de «cuándo hay que escribir» dejó de estar enumerada**: se
escribe si el texto que saldría es distinto del que hay —lo que además
normaliza el orden de claves, que había divergido—. Aquella lista escrita a
mano se quedó corta dos veces en el mismo día.

**Dos lectores se habían quedado con la forma vieja**, y solo se vieron
corriendo las suites: `mutaciones_censo.m_deuda_muerta` y
`mutaciones_efectos.d_rasgo_sacado_de_la_lista` abrían el JSON esperando
`rasgos`, una lista de ids, donde ahora hay `entradas`, un diccionario. Es el
argumento del módulo por escrito: la forma la fija `deuda.py` para los cinco,
en vez de una por fichero.

**Y la identidad cambió de forma, no de valor.** La primera `Deuda` guardaba
como identidad la FRASE que describe la regla, y saltó contra su propio autor a
los diez minutos porque un fichero la tenía escrita con siete palabras de más.
Ahora la identidad es una clave corta y estable (`nombre-de-mutacion`,
`fichero-almohadilla-nombre`) y la prosa vive aparte en
`_identidad_explicada`, que se puede reescribir sin invalidar nada — y hay un
control negativo que lo exige.

**De rebote, una cuenta más anclada:** `CONTINUAR.md` decía «las 17 suites de
`_verificacion/mutaciones_*.py`» con 18 en el disco, **en la misma frase que
presume de que se descubren por patrón**. `verificar_documentos.py` la
contrasta ahora contra el disco, con sus dos mutaciones en
`mutaciones_documentos.py` (borrarla y falsearla).

**Cifras remedidas al cerrar:** censo **938** unidades · 0 sin declarar · 570
pendientes · `mutaciones_deuda` 10/10 · `mutaciones_documentos` 12/12 · las
demás sin cambio.

---

## Fase 2 · Un muro de errores común

**Logra:** que la familia «un chequeo explota en vez de hablar» —tres veces en
dos días— no pueda repetirse en los seis scripts que hoy no tienen muro.

- `deuda.py` no es su sitio. Va a un `informar.py` nuevo, o a `deuda.py`
  renombrado a algo más ancho: **decidir al empezar la fase, no ahora**.
- `muro(fn, *args, etiqueta=None)` generaliza `validar._correr()`: captura
  `Exception`, deja pasar `SystemExit`, y devuelve el fallo COMO dato del
  chequeo que lo provocó, con su tipo y su mensaje.
- `validar._correr` pasa a ser un alias de tres líneas sobre `muro`, para no
  tocar sus 13 usos.
- `verificar_personaje` cambia su `except KeyError/SystemExit` parcial por el
  muro: hoy cualquier otra excepción se lleva el proceso.
- `censo`, `verificar_chequeos`, `verificar_srd`, `verificar_foundry`,
  `verificar_documentos` y `cobertura` envuelven sus bucles de chequeo.

**Se comprueba:** `_verificacion/mutaciones_muro.py`, que inyecta un `raise` en
un chequeo de cada script y exige que el informe SIGA saliendo, con ese chequeo
en rojo y los demás intactos. Control negativo: un `sys.exit` legítimo —un dato
que falta en la base— tiene que seguir parando, no convertirse en una línea de
error entre otras.

### ✅ FASE 2 CERRADA (2026-09-06) — lo que salió, remedido

`informar.py` en la raíz, con `muro(fn, ...) -> (valor, Fallo|None)` y `Fallo`
llevando la etiqueta separada del motivo (`validar.py` ya imprime el nombre en
su columna; `verificar_personaje` lo necesita dentro de la frase). Puesto en los
siete, con la unidad de chequeo que cada uno tiene:

| script | unidad | qué se perdía |
|---|---|---|
| `validar.py` | un `validar_*` | nada: tenía muro desde el día antes |
| `verificar_personaje.py` | un `verificar_*` | todo salvo `KeyError` y `SystemExit` |
| `censo.py` | una fila (9) | las NUEVE y el recuento que anclan los documentos |
| `verificar_chequeos.py` | una fuente (17) | todo, **y podía podar en falso** |
| `verificar_srd.py` | una clase (12) | las doce y la cifra de 646 |
| `verificar_foundry.py` | un módulo | todos y la cifra de 3749 |
| `verificar_documentos.py` | una suite (18) | todo, por un `IndexError` de lista vacía |
| `cobertura.py` | un bloque (5) | los cinco |

**`validar._correr` son ahora tres líneas encima del muro** y sus trece usos no
cambian; lo que se queda ahí es la adaptación a la terna `(nombre, errores,
avisos)`, no el mecanismo.

**El `sys.exit` sigue parando**, con una excepción declarada y una sola:
`verificar_personaje`, porque allí lo examinado es la FICHA y la salida de
`calculo` es un veredicto sobre la entrada bajo examen, no un dato que falte en
la base. El parámetro se llama `salida_es_veredicto` y no `capturar_salidas`
a propósito: el nombre tiene que decir por qué, no qué. El control negativo va
en las dos direcciones.

**El peligro que el muro trae consigo, y no estaba en el plan.** Lo destapó
medir `verificar_chequeos` antes de tocarlo: varios de estos scripts alimentan
una línea base de `deuda.py`, y `Deuda.contrastar` PODA lo que hoy no se mide.
Un fichero que reventara y cuyo chequeo simplemente «siguiera» dejaría de
aportar sus ramas, la poda las daría por saldadas y **la deuda bajaría sola, en
verde** — la mentira contra la que existe la línea base, entrando por la puerta
que se abrió para no perder informes. El muro no puede decidirlo (no sabe qué
alimenta cada chequeo): lo decide quien mide, con `podar=False`, y hay un
control negativo que lo exige.

### El hallazgo de la fase: lo destapó el refactor de la propia fase

Al sacar el cuerpo de un bucle a un ayudante `_ramas_de()` para poder ponerle el
muro, **cuatro ramas silenciosas desaparecieron de la línea base, en verde**, y
la poda las dio por saldadas. `verificar_chequeos` solo miraba funciones
llamadas `validar_*`, `verificar_*` o `main`: **bastaba mover una rama de
función para dejar de vigilarla**. Una convención de nombres es una lista
escrita a mano disfrazada, que es lo que la regla inviolable 6 prohíbe — dentro
del módulo que existe para cazarlo.

Medido: **61 ramas en funciones con prefijo, 59 más en las demás**. Casi la
mitad de lo que este verificador vigila vivía fuera de su alcance. Ahora se
miran TODAS las funciones y la línea base pasa de 61 a **120**, con las 59 como
deuda declarada —no permiso: sigue pudiendo solo bajar— y su `_migracion` dentro
del fichero. `_auditable` se queda para la otra pregunta, la que hace
`censo.fila_modulos`: ¿tiene este módulo alguna entrada de chequeo, o es una
biblioteca? Eran dos preguntas compartiendo un predicado, y por eso una podía
mentirle a la otra. Su mutación nueva está en `mutaciones_silencios.py` (7/7):
una rama silenciosa metida en un ayudante `_con_guion_bajo`.

**Cifras remedidas al cerrar:** censo **939** unidades · 0 sin declarar · 570
pendientes · ramas silenciosas **120**, línea base 120 · `mutaciones_muro` 10/10
(nueva) · `mutaciones_silencios` 7/7 · el resto sin cambio.

---

## Fase 3 · La fila del censo que cuenta los guardianes sin guardián

**Logra:** convertir «todo verificador tiene su prueba por mutación» de
costumbre en cuenta. Va la última porque las fases 1 y 2 crean módulos nuevos
que esta fila tendrá que contar.

Fila 10 del censo, hermana de `fila_modulos` (`censo.py:439`, que ya enumera
los scripts de la raíz con `verificar_chequeos.fuentes()`):

- **Universo:** los scripts de la raíz.
- **Alcanzada:** alguna suite de `_verificacion/mutaciones_*.py` **escribe su
  fichero** —muta su código, no solo la base—. Se descubre por AST: una llamada
  a `sust`/`_sust`/`write_text` cuyo destino es ese `.py`. Nunca a mano: la
  lista escrita a mano es el defecto que este censo persigue.
- **Declarable con motivo** para lo que legítimamente no lo necesita
  (`_convertir_hechizos.py` es un conversor de un solo uso; `materiales.py` es
  una biblioteca sin funciones auditables, ya declarada así en `fila_modulos`).
- **Deuda enumerada** —vía `deuda.py` de la fase 1— para los que sí lo
  necesitan y hoy no lo tienen: `cobertura.py`, `generar_ficha.py`,
  `prerrequisitos.py`, `subir_nivel.py`.

**Se comprueba:** dos mutaciones en `mutaciones_censo.py` —un script nuevo en la
raíz sin suite que lo mute, y una suite que deja de mutar el script que decía
cubrir— más un control negativo: una suite que muta solo la base no cuenta como
guardián de código.

**Cifra prevista:** la fila nace con ~16 unidades y 4 en deuda. **A remedir.**

### ✅ FASE 3 CERRADA (2026-09-06) — y la cifra prevista estaba mal

**18 unidades · 11 con guardián · 1 declarada · 6 en deuda.** La predicción
—«~16 y 4»— se equivocaba en las dos direcciones, que es exactamente para lo
que la regla «no dar por buena ninguna cifra de este documento sin remedirla»
existe:

- `cobertura.py`, que el plan daba por deuda, lo cubrió la fase 2 al ponerle el
  muro (y `mutaciones_muro` le muta el código);
- aparecieron tres que la lista escrita a mano no tenía: `buscar.py`,
  `verificar_documentos.py` y **`informar.py`, el módulo que la fase 2 acababa
  de escribir**;
- `materiales.py` NO es declarable, contra lo que el plan suponía: esa
  suposición venía de `fila_modulos` («biblioteca sin funciones auditables»),
  que responde a otra pregunta. `mutaciones_materiales` muta la base, así que
  un fallo en la descomposición de costes pasaría. Queda en deuda.

El único declarable es `_convertir_hechizos.py`, y con un motivo que no es «no
hace falta» sino **«mutarlo no probaría nada»**: es un conversor de un solo uso
cuyo resultado ya está en la base y lo validan `validar_hechizos` y las 391
citas de conjuro. Corromperlo hoy no cambiaría ningún dato, así que no habría
nada que exigir que se notara.

**`informar.py` se cerró en el sitio.** `mutaciones_muro` mutaba los siete
scripts y ni una línea del muro: el módulo que existe para que un fallo no se
pierda podía perder fallos él mismo, en verde — el guardián sin guardián que
esta fila cuenta, dentro de la fase que la escribió. Se le rompen ahora sus
tres promesas (deja de capturar, se traga el `sys.exit`, `Fallo` pierde la
etiqueta) y la suite va a **13/13**.

### El detector mintió dos veces, y las dos lo dijo su propia mutación

- **Buscaba los nombres `sust`/`_sust`/`write_text` a mano.** `sust` vive en
  `_arnes.py` y se IMPORTA, así que mirar solo el fichero de la suite decía que
  `mutaciones_aritmetica` no muta `calculo.py`, y sí lo hace. Además, tomar
  cualquier cadena de la llamada por destino contaba el TEXTO sustituido como
  si fuera un fichero. Ahora las funciones mutadoras se descubren —y también en
  qué posición reciben el camino: es el operando derecho del `/`—.
- **Contaba CREAR un fichero como mutarlo.** La mutación que añade un script
  nuevo a la raíz para exigir que el censo lo cace **se blindaba sola**: la
  suite que acababa de crearlo aparecía escribiéndolo, así que el censo lo daba
  por guardado. Un guardián no fabrica el código que vigila: se lo encuentra y
  se lo estropea. Ahora una función solo cuenta si LEE el fichero antes de
  escribirlo.

Y una tercera, esta en la suite y no en el detector: quitarle a `validar.py`
uno de sus DOS guardianes no lo deja sin guardián, así que la mutación no se
detectaba. Ahora le quita a `deuda.py` el único que tiene. `mutaciones_censo`
**34/34**, con las dos que deben salir y el control negativo —una suite que
muta solo la base no convierte en guardado ningún script—.

**Cifras remedidas al cerrar:** censo **957** unidades · 0 sin declarar · 576
pendientes · `mutaciones_muro` 13/13 · `mutaciones_censo` 34/34 · el resto sin
cambio.

---

## Lo que NO hay que hacer

1. **No empezar por los seis casos de la tabla del contexto.** Están
   arreglados; volver a ellos es el espiral.
2. **No cambiar la identidad de ningún fichero de deuda al migrarlo.** Invalida
   su línea base, y esa es exactamente la mentira que el plan persigue.
3. **No unificar los cinco ficheros en uno solo.** Cada uno tiene su dueño y su
   momento de escritura; juntarlos crearía un fichero que nadie sabe quién
   escribe.
4. **No hacer que el muro se trague un `sys.exit`.** Un dato que falta en la
   base tiene que seguir parando el proceso: convertirlo en una línea de error
   entre otras es cómo se pierde un fallo grave.
5. **No declarar a mano qué script cubre cada suite** en la fase 3. Se descubre
   por AST o no se hace.
6. **Ningún chequeo nuevo como aviso `⚠`** (criterio `PLAN_19` §12.1).
7. **No dar por buena ninguna cifra de este documento sin remedirla.**

---

## Verificación de cada fase

```bash
python3 validar.py && python3 censo.py && python3 verificar_chequeos.py
python3 verificar_srd.py && python3 verificar_foundry.py && python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 generar_ficha.py --barrido --exhaustivo
python3 _verificacion/mutaciones_deuda.py     # nueva, fase 1
python3 _verificacion/mutaciones_muro.py      # nueva, fase 2
python3 verificar_documentos.py               # corre las suites (~5 min)
```

Estado al empezar, para contrastar: censo **937** unidades · 0 sin declarar ·
26 fichas · barrido 240/240 · 646 valores contra el SRD y 3749 contra Foundry ·
censo 31/31 · contenido 61/61 · efectos 42/42 · motor 12/12 · aritmética 40/40 ·
silencios 6/6 · documentos 10/10 · nivel20 52/52.

## ✅ EL PLAN 21 ESTÁ CERRADO (2026-09-06)

Las tres fases hechas, y el criterio de cierre remedido:

| Frente | Prometía | Real |
|---|---|---|
| 1 · una sola abstracción de deuda | 5 ficheros migrados | **5, sin cambiar ninguna identidad** |
| 2 · un muro de errores común | 6 scripts sin muro | **7 con muro, `validar` incluido** |
| 3 · la fila de los guardianes | ~16 unidades, 4 en deuda | **18 · 11 · 1 declarada · 6 en deuda** |
| 4 · una regla única de identidad | declarada en `deuda.py` | **declarada, y comprobada: cambiarla lanza** |

**Lo que más dice de este plan no es ninguna de las tres fases: es que las tres
rompieron algo y las tres lo dijo un guardián, no yo.** La fase 1 rompió
`verificar_chequeos` (3 de 6) y dejó la prosa de tres ficheros en blanco; la
fase 2 escondió cuatro ramas silenciosas moviéndolas a un ayudante, y destapó
que casi la mitad de las ramas vivían fuera del alcance del verificador; la
fase 3 nació con un detector que se blindaba solo. Ninguno de esos seis
hallazgos salió de leer el código.

Y la regla que no cambia: **todo hueco que se cierre lleva su chequeo y su
prueba por mutación**; todo falso positivo se corrige afinando, no relajando, y
se queda como control negativo.

### Ficheros críticos

- `deuda.py` — nuevo, la abstracción y la regla de identidad
- `verificar_chequeos.py:160-215` · `censo.py:485-510, 555-610, 750-822` ·
  `validar.py:2289-2340` · `_verificacion/mutaciones_motor.py:260-345` — los
  cinco llamadores a migrar
- `validar.py:3177` — `_correr()`, el muro que se generaliza
- `verificar_personaje.py:1396-1411` — el muro parcial que se sustituye
- `censo.py:439` — `fila_modulos`, hermana de la fila nueva
