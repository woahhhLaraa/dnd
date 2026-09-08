# PLAN 22 — la lectura independiente, dirigida por una cuenta y no por el ojo

> Estado: **fases 1 y 2.0 cerradas el 2026-09-08**; la tanda (2.1) en marcha.

## Contexto

El `PLAN_21` cerró el 2026-09-06 y dejó escrito su propio límite, en
`ARQUITECTURA.md` §5:

> **Un guardián no puede cazar aquello en lo que el motor y el verificador se
> equivocan de acuerdo.** Si la regla nunca entró en la base, el motor no la
> aplica, el verificador no la exige y las dos partes coinciden — en verde.

Eso no es teórico. Es el hallazgo mayor de toda la auditoría: dos agentes a
ciegas, en dos clases distintas, dieron números **mayores** que el motor y
tenían razón. «Campeón primordial» y «Cuerpo y mente» subían dos
características, la regla estaba transcrita y citada **pero solo en la prosa**,
y todo personaje de nivel 20 de Bárbaro o Monje salía con números de menos, en
verde, durante semanas.

La única pieza que mira desde fuera del sistema es el mandato **E · el
calculista** de `PLAN_ESTRES.md`. Hoy cubre **12 de 26 fichas**. Este plan
cierra las otras 14.

---

## Lo medido, el 2026-09-07, antes de escribir nada

### El criterio que dirigía esta tanda ha expirado, y nadie lo notó

`PLAN_ESTRES.md` es explícito: **«No se elige a ojo qué fichas calcular.»** El
encargo de cada tanda sale de dos listas que el repo mantiene, y el criterio de
cierre es «fila 8 a 25/25 y `motor_sin_carga.json` vacío». Hoy:

| lista | estado | qué significa |
|---|---|---|
| `efectos_sin_carga.json` | **0 entradas** | fila 8 cerrada, 25/25 |
| `motor_sin_carga.json` | 3 entradas | las tres **declaradas imposibles con los datos de hoy** (`mul` sin efecto que lo use, `math.floor` sin variable fraccionaria no decimal, orden de agregación sin dos operaciones sobre la misma variable). El propio `PLAN_20` cerró diciendo: «No busques una ficha imposible.» |

O sea: **el criterio ya no elige nada**, y correr la tanda «tal cual» sería
elegir a ojo — lo que el mandato prohíbe. Que una lista se quede sin poder
dirigir y siga en su sitio como si dirigiera es exactamente la forma del error
que este repositorio persigue (`ARQUITECTURA.md` §1).

### La cobertura real, por clase y por nivel

| | |
|---|---|
| fichas con `_origen: agente-manual` | **12** de 26 |
| **clases sin ninguna lectura independiente, a ningún nivel** | **4 de 12: Brujo, Guerrero, Mago, Pícaro** |
| de las 14 sin cubrir | **10 son de nivel 1**; 4 de nivel alto |

Cubiertas hoy: Bárbaro (1, 20), Bardo (3 ×2), Hechicero (3), Monje (2, 20),
Druida (1, 3), Clérigo (5), Explorador (6), Paladín (15).

Las 14 sin cubrir, con lo que compra cada una:

| # | ficha | qué es | qué compra |
|---|---|---|---|
| 1 | `gnomo_mago_n20` | Mago 20 · Evocador | **Mago no tiene lectura a ningún nivel**, y es nivel 20 — donde salió el hallazgo mayor |
| 2 | `_ejemplo_aerin` | Brujo 1 | el **pacto**: espacios de conjuro con reglas propias que nadie ha derivado a mano |
| 3 | `enano_guerrero` | Guerrero 1 | clase sin cubrir |
| 4 | `mediano_picaro` | Pícaro 1 | clase sin cubrir |
| 5 | `mago_quebradizo_n3` | Mago 3 · Abjurador | segunda de Mago, otra subclase |
| 6 | `draconido_hechicero_n4` | Hechicero 4 | **nivel 4: la primera mejora de característica**, que ninguna derivación ciega ha tocado salvo n15/n20 |
| 7 | `draconido_monje_n20` | Monje 20 · Mano Abierta | otra subclase de Monje a nivel 20 |
| 8-14 | `aasimar_clerigo`, `draconido_hechicero`, `draconido_monje`, `elfo_paladin`, `gnomo_mago`, `humano_explorador`, `tiefling_bardo` | todas nivel 1 | valor marginal: sus clases ya tienen lectura a nivel alto |

### Lo que ya existe y se reutiliza

- `verificar_personaje.py:1342` · `--datos-crudos <ficha>` imprime la ficha
  **sin su bloque `calculado`**. Existe porque la primera tanda lo pidió y no
  se pudo cumplir: los datos crudos y los números viven en el mismo fichero.
  *«La ceguera no se pide, se REPARTE.»*
- `censo.py:fila_efectos_con_carga` · el patrón de leer `personajes/*.yaml` y
  mirar `calculado._origen.metodo == "agente-manual"`. La fila nueva lo copia.
- `deuda.Deuda` · la contabilidad de la línea base (podar, nuevo ≠ perdido,
  elenco, identidad).
- `_verificacion/_aritmetica/<ficha>-calculista-ciego.md` · el formato de las
  14 derivaciones que ya existen.

---

## Fase 1 · La fila 11: fichas con lectura independiente

**Logra:** que el criterio de dirección sea una **cuenta** y no una costumbre,
para que no pueda volver a expirar en silencio. Es lo mismo que la fila 10 hizo
con «todo verificador tiene su prueba por mutación», y por la misma razón.

Va primero porque **es lo que hace legítima la fase 2**: sin ella, elegir ficha
es elegir a ojo.

`censo.fila_lectura_independiente()`, hermana de `fila_efectos_con_carga`:

- **Universo:** los `.yaml` de `personajes/`.
- **Alcanzada:** `calculado._origen.metodo == "agente-manual"` **y su
  `informe` existe en disco**. Las dos cosas, no la primera sola: un `_origen`
  que apunte a un informe borrado es una declaración muerta, y este repositorio
  ya se llenó una vez de ocho de esas.
- **Deuda enumerada** vía `deuda.Deuda`, `cerrada=False` — como `fila_rasgos` y
  `fila_efectos_con_carga`: una ficha nueva cae en `medidos_nuevos`, no entra en
  `deuda`, y `Fila` la saca como SIN DECLARAR, que ya es rojo. La política
  `cerrada` sobra aquí y añadirla sería una segunda puerta para el mismo rojo.
- **Identidad:** el nombre del fichero de la ficha.
- **`_ejemplo_aerin.yaml`:** **decidir mirándolo, no ahora.** Es un Brujo 1 real
  que el barrido verifica y que `personajes/_ESQUEMA.md` y la skill `personaje`
  citan como ejemplo del formato. Si su papel es documentar, se declara con
  motivo en `censo_exenciones.yaml`; si es una ficha como las demás, entra en la
  tanda — y en el orden de arriba está la nº 2 justamente porque es el único
  Brujo.

**Se comprueba:** dos mutaciones en `mutaciones_censo.py` —una ficha nueva sin
lectura independiente, y un `_origen` que apunta a un informe que no existe—
más un control negativo: una ficha con `agente-manual` y su informe en disco no
cuenta como deuda.

**Y `PLAN_ESTRES.md` se corrige**, porque hoy manda algo que no se puede
cumplir: su sección «Cómo se dirige» pasa a apuntar a esta fila, y el criterio
de cierre deja de ser «fila 8 a 25/25» —ya cumplido— para ser «fila 11 a cero».

**Cifra prevista:** 26 unidades · 12 alcanzadas · 14 en deuda (menos 1 si
`_ejemplo_aerin` se declara). **A remedir.**

### ✅ FASE 1 CERRADA (2026-09-07) — remedido

**26 unidades · 12 alcanzadas · 14 en deuda.** La cifra prevista era exacta, y
`_ejemplo_aerin` **NO se declara exento**: es un Brujo 1 real que el barrido
verifica como los demás, y es el ÚNICO Brujo del repositorio. Declararlo habría
escondido que una clase entera no tiene ninguna lectura independiente — el
motivo mismo por el que la fila existe. Entra como unidad, y en la tanda va la
segunda.

Censo **957 → 983** unidades · 0 sin declarar · **576 → 590** pendientes.

**Y un falso positivo, corregido afinando.** La primera versión puso en el
universo todo `.yaml` de `personajes/`, y un control negativo que ya existía lo
cazó a la primera: `n_yaml_en_directorio_no_de_regla` deja un
`personajes/prueba.yaml` de una sola clave para exigir que **no todo `.yaml` es
una regla**, y la fila le pedía una derivación a mano a ese fichero de prueba.
El criterio dice ahora qué es una ficha —tener `clases:`, porque un personaje
sin clases no es un personaje—, la rama va declarada con `# TOLERADO:`, y el
control se queda donde estaba.

**`PLAN_ESTRES.md` corregido**, que era la mitad del encargo: su sección «Cómo
se dirige» apuntaba a dos listas que ya no dirigen, y ahora apunta a la fila 11.
El criterio de cierre pasa de «fila 8 a 25/25» —cumplido hace un día— a **fila
11 a cero**.

**Y una mutación mía se quedó vieja al nacer la fila, dentro de la suite que
vigila justo eso.** `d_fila_nueva_sin_documentar` anclaba en
`"         fila_guardianes)"` —el nombre de la última fila de `FILAS`—, y en
cuanto la fila 11 pasó a ser la última el anclaje dejó de encajar y
`mutaciones_documentos` reventó entera. Lo cazó `verificar_documentos.py` con
«no termina en verde». El anclaje va ahora en el cierre del paréntesis, que es
lo que no se mueve. La otra cosa que cazó en la misma pasada: `CONTINUAR.md`
prometía 34/34 para `mutaciones_censo` cuando ya eran 37/37 — mía también.


---

## Fase 2.0 · El `veredicto`, para que la lectura independiente no caduque

**El hueco, encontrado al mirar cómo se contrasta.** La fila 11 comprueba que
el informe **existe en disco**. No comprueba que **siga diciendo lo mismo que
el motor**. O sea: una vez que una ficha gana su `_origen: agente-manual`,
nada vuelve a mirar esa derivación nunca más. Si el motor cambia mañana —y ha
cambiado mucho: `PLAN_20` y `PLAN_21` en tres días—, la ficha sigue diciendo
«un agente verificó esto a ciegas» sin que nadie lo compruebe. Es media
comprobación, y del tipo exacto que este repositorio persigue: una declaración
que se queda vieja sin que nadie se entere.

Además, **el contraste no tiene hoy ninguna herramienta ni ningún registro**:
se hace a ojo, leyendo la tabla final del informe y comparándola con
`--calcular`. Un paso hecho a ojo, por quien además quiere que coincida.

**El arreglo, y es barato:** cada derivación termina en un bloque
legible por máquina, y `verificar_personaje.py` lo contrasta.

````markdown
```veredicto
pg_max: 14
ca: 13
velocidad: 9
cd_conjuros: no_procede
bonif_ataque_conjuros: no_procede
```
````

- **Dónde vive el contraste:** en `verificar_personaje.py`. Es su sitio natural
  —el verificador de la ficha comprueba lo que la ficha declara— y sale
  **gratis**, porque ya calcula ese bloque para la propia ficha. NO va en
  `censo.py`: la fila tendría que calcular las 26 fichas en cada pasada, y
  `mutaciones_censo` corre el censo 37 veces (≈ +40 min por suite).
- **Retrofit de las 12 que ya existen.** Sus tablas finales son prosa y varían
  de formato —cabeceras distintas, negrita en sitios distintos, y las dos de
  nivel 20 traen **dos lecturas alternativas**, que es justo donde estuvo el
  hallazgo—. Así que no se parsea la prosa: **se transcribe a mano el bloque, y
  luego se contrasta**. Cualquier desacuerdo se INVESTIGA, no se corrige: puede
  ser mi transcripción o puede ser que la derivación ya no case con el motor de
  hoy, y lo segundo es un hallazgo.
- **Las dos de nivel 20** (`barbaro_berserker_n20`, `monje_elementos_n20`)
  llevan la lectura que se resolvió —fue el hallazgo de «Campeón primordial» y
  «Cuerpo y mente»— con una nota diciendo cuál era la otra y por qué se cerró.

**Se comprueba:** una mutación que altere un valor del `veredicto` y exija que
`verificar_personaje` lo cace, más un control negativo —reescribir la prosa de
la derivación no cambia nada—. Va en la suite que ya construye fichas y las
pasa por `verificar_personaje` (`mutaciones_nivel20.py`, 4 usos, o
`mutaciones_pg.py`, 2; **a decidir mirando cuál encaja**).

### ✅ FASE 2.0 CERRADA (2026-09-08)

`verificar_personaje.verificar_veredicto` contrasta el bloque de cada
derivación contra lo que el motor calcula, para toda ficha con
`_origen: agente-manual`. Sale gratis: el bloque ya se calculaba. La mutación
va en `mutaciones_nivel20.py`, que ya construye fichas y las pasa por el
verificador.

**Las 12 derivaciones retrofiteadas, y las 12 siguen cuadrando.** Los bloques se
transcribieron de la tabla final de cada informe **sin mirar el motor**, y solo
después se contrastaron: **0 desacuerdos**. No era obvio — esas derivaciones son
del 2026-09-06 y el motor cambió mucho entre medias (`PLAN_20` y `PLAN_21`), así
que el resultado es información, no rutina. Las dos de nivel 20 llevan su nota:
la lectura elegida fue la del hallazgo («Campeón primordial», «Cuerpo y mente»),
y se dice cuál era la otra y por qué se cerró.

`mutaciones_nivel20` pasa de 52/52 a **55/55**: dos mutaciones —el `veredicto`
deja de cuadrar con el motor; el `veredicto` desaparece— y un control negativo
—reescribir la prosa del informe no cambia nada—.

**Y un control negativo que hubo que afinar, no relajar.**
`n_pg_tirada_al_minimo` cambia una tirada de PG a 1 —legal, por deprimente que
sea— y actualizaba `calculado.pg_max` para que cuadrase. Con el chequeo nuevo
saltaba, y **tenía razón**: la derivación a ciegas de esa ficha se hizo sobre
otras tiradas, así que ya no dice nada sobre esta. Lo que se corrigió es el
control, que ahora también baja el `_origen` a `motor`. La regla que eso
encodifica, y que no estaba escrita en ninguna parte: **cambiar las entradas de
una ficha invalida su lectura independiente hasta que alguien la rehaga.**

---

## Fase 2.1 · La tanda, en el orden que la fila dicta

Las **14**, por orden de valor —el de la tabla de arriba—, hasta llevar la fila
11 a cero.

### Las reglas del método, intactas

1. **No lee el código.** Prohibidos `calculo.py`, `efectos.py`,
   `reglas/efectos.yaml`, cualquier verificador, todo `_verificacion/` y todo
   `personajes/`. Sí lee la base —`reglas/`, `especies/`, `clases/`, `equipo/`,
   `dotes/`—, que es de donde tiene que salir cada paso.
2. **No ejecuta el verificador.** Los datos crudos, por
   `python3 verificar_personaje.py --datos-crudos personajes/<ficha>.yaml`.
3. **La derivación se escribe antes de ver ningún número nuestro**, en
   `_verificacion/_aritmetica/<ficha>-calculista-ciego.md`.
4. **Nada entra en `personajes/`** hasta que el contraste lo apruebe.

### Lo que deriva

`pg_max`, `ca`, `velocidad`, `cd_conjuros` y `bonif_ataque_conjuros`, con cada
paso escrito, **citando de dónde sale cada regla**, y terminando en el bloque
` ```veredicto ` de la fase 2.0.

**El listón está puesto y hay 12 ejemplos.** `orco_barbaro-calculista-ciego.md`
son 472 líneas con esta estructura, que el encargo pide mantener: cabecera con
la ficha y los ficheros consultados · **«Desviaciones cometidas — declaración
honesta»**, donde el agente declara lo que ha rozado y por qué no le contamina
· modificadores primero · **inventario cerrado de fuentes de efectos** —leído
de `reglas/fuentes_de_efectos.yaml`, para poder afirmar que no se deja
ninguna— · un apartado por valor · tabla final · «lo que NO se ha podido
derivar de la base».

Un detalle del método que ese informe fija y hay que conservar: varios ficheros
permitidos traen, junto al texto en prosa, un bloque `efectos:` con la fórmula
ya formalizada. **Se deriva desde el `desc` en prosa y solo después se mira el
`efectos:` como confirmación**, diciéndolo. Si no, la derivación deja de ser
una segunda transcripción y pasa a ser una lectura del motor con otra letra.

### Cómo se lanzan

De **uno o dos a la vez**, nunca los catorce: los límites de tasa mataron
agentes en dos tandas anteriores. Antes de lanzar cada uno, los datos crudos se
escriben fuera del repositorio con
`verificar_personaje.py --datos-crudos` — así el agente nunca necesita abrir
`personajes/`.

**Con una adaptación que hay que decir:** el mandato original dice «citando la
página del manual», y **el PDF no está en este contenedor**. Así que la cita es
el fichero de la base y la `pagina:` que ese registro declara. No es un
descuento: la base lleva su procedencia dentro, y es lo que el agente puede
verificar. Lo que **no** se puede correr aquí es el mandato D —el abogado del
manual—, que sí necesita leer la página.

### Qué se hace con cada resultado

| | |
|---|---|
| **Coincide** | la ficha gana `calculado._origen: {metodo: agente-manual, informe: …, fecha: …}` y sale de la deuda de la fila 11 |
| **Discrepa** | **hallazgo.** La derivación escrita dice de quién es el error: del informe o del motor. Se investiga antes de tocar nada |
| **La cita no dice lo que el agente creía** | se descarta **registrado como descartado**, con su motivo. No se borra |

---

## Riesgos, medidos

- **Los límites de tasa mataron agentes dos veces** en las tandas anteriores.
  Mitigación: de uno en uno o de dos en dos, nunca los catorce a la vez, y cada
  agente escribe su `.md` **antes** de cualquier otra cosa — así un agente que
  muere pierde solo lo suyo y la tanda se retoma por donde iba.
- **La ceguera se rompe sola si el agente abre la ficha.** Por eso
  `--datos-crudos` y la prohibición de `personajes/` son parte del encargo, no
  una recomendación.
- **Una derivación que coincide no prueba que el motor esté bien**, solo que
  dos lecturas independientes dan lo mismo. Sigue siendo lo más fuerte que hay.

---

## Lo que NO hay que hacer

1. **No elegir fichas a ojo.** El mandato lo prohíbe y por eso la fase 1 va
   primero.
2. **No dejar que el agente vea el bloque `calculado`**, ni de reojo. Una
   derivación anclada a un número ya visto no es independiente, por honesta que
   sea.
3. **No borrar una derivación que discrepe.** Si la cita no dice lo que el
   agente creía, se registra como descartada con su motivo.
4. **No hacer `cerrada=True` en la deuda de la fila 11.** El rojo ya lo pone
   `Fila` vía SIN DECLARAR; dos puertas para el mismo rojo es ruido.
5. **No fabricar el motivo de `_ejemplo_aerin`** sin mirar qué papel tiene.
6. **No parsear la prosa de las derivaciones para sacar sus números.** Los
   formatos varían y dos traen lecturas alternativas; una huella mal elegida
   sobre prosa es un error que este repositorio ya ha cometido tres veces. El
   bloque `veredicto` se escribe explícito.
7. **No "arreglar" un desacuerdo del retrofit.** Si el `veredicto` transcrito
   no casa con el motor, se investiga: o la transcripción está mal, o la
   derivación ya no vale contra el motor de hoy — y lo segundo es un hallazgo.
8. **No poner el contraste en `censo.py`.** Calcularía las 26 fichas en cada
   pasada y `mutaciones_censo` corre el censo 37 veces.
9. **No dar por buena ninguna cifra de este documento sin remedirla.**

---

## Verificación

```bash
python3 validar.py && python3 censo.py && python3 verificar_chequeos.py
python3 verificar_srd.py && python3 verificar_foundry.py && python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 generar_ficha.py --barrido --exhaustivo
python3 _verificacion/mutaciones_censo.py     # las tres de la fila 11
python3 _verificacion/mutaciones_nivel20.py   # la del `veredicto` (fase 2.0)
python3 _verificacion/mutaciones_deuda.py
python3 verificar_documentos.py               # corre las suites (~5 min)
```

**Y el contraste, que es lo que esta fase compra:** cada
`verificar_personaje.py personajes/<ficha>.yaml` de una ficha con
`_origen: agente-manual` tiene que decir que su `veredicto` sigue coincidiendo
con el motor. Las 12 viejas incluidas — ahí está el primer sitio donde puede
saltar algo.

Estado al empezar la fase 2, remedido tras cerrar la fase 1: censo **983**
unidades · 0 sin declarar · **590** pendientes · fila 11 **26 · 12 · 14** ·
26 fichas · barrido 240/240 · 646 contra el SRD y 3749 contra Foundry · ramas
silenciosas 120/120 · censo **37/37** · muro 13/13 · documentos 16/16 · deuda
10/10 · silencios 7/7 · efectos 42/42 · motor 12/12 · nivel20 52/52.

Y las reglas que no cambian: **todo hueco que se cierre lleva su chequeo y su
prueba por mutación**; todo falso positivo se corrige **afinando, no
relajando**, y se queda como control negativo; y **`ARQUITECTURA.md` nombra
todo módulo y toda fila** — la fila 11 tendrá que entrar ahí, o el ancla falla.

### Ficheros críticos

- `verificar_personaje.py` — el contraste del `veredicto` (fase 2.0), junto a
  `calcular_bloque`; y `--datos-crudos` (línea 1342), la ceguera repartida
- `_verificacion/_aritmetica/` — las 12 derivaciones a retrofitear y las 14
  nuevas. `orco_barbaro-calculista-ciego.md` es el modelo
- `_verificacion/mutaciones_nivel20.py` — la mutación del `veredicto`
- `personajes/*.yaml` — el `_origen` de cada ficha que apruebe

Ya cerrados en la fase 1, aquí solo se tocan sus cifras: `censo.py`
(`fila_lectura_independiente`), `_verificacion/mutaciones_censo.py`,
`_verificacion/lectura_independiente.json`, `PLAN_ESTRES.md`,
`ARQUITECTURA.md`, `CONTINUAR.md` y `FODA.md`.
