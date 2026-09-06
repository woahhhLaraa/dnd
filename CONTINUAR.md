# CONTINUAR — punto exacto de reanudación

> **Empieza aquí.** Todo el estado está en disco: **no depende de ninguna
> conversación previa.**
>
> **Este fichero se reescribió entero el 2026-09-03.** La versión anterior
> tenía 1172 líneas: un registro día a día desde el 2026-08-19 que había
> dejado de leerse — la mayoría ya estaba resuelta y tachada, y el detalle
> vivía duplicado, mejor escrito, en los planes que cierran cada fase. Nada
> se perdió: **el historial completo sigue en `git log -- CONTINUAR.md`**,
> el mismo criterio con que quedó archivado `FODA_2026-08-19_OBSOLETO.md`
> (borrado del disco, vivo en git). Este fichero vuelve a ser lo que su
> nombre dice: el punto exacto de reanudación, no un diario.
>
> Orden de lectura para retomar:
> 1. **este fichero**, entero — es corto a propósito;
> 2. **`PLAN_19_PRODUCTO_COMPLETO.md`** — el plan de trabajo vigente hacia el
>    producto completo: qué falta, qué logra cada fase, resultados medidos
>    de las fases 1-3 en sus §14-16;
> 3. **`PLAN_20_AUDITORIA.md`** — **la auditoría en curso**: el inventario
>    medido de autoridad duplicada y las cinco fases que la cierran. Nace del
>    encargo del 2026-09-03 y de lo que la ronda 2 de estrés destapó;
> 4. **`PLAN_ESTRES.md`** — la rutina de estrés con agentes y sus dos rondas
>    corridas, con los hallazgos de cada una;
> 5. **`FODA.md`** — análisis vigente, si vas a decidir arquitectura;
> 6. **`PLAN_18_REVISION_COMPLETA.md`** — registro de los bloques A-D del
>    Plan 18 (censo, mutaciones, listas cerradas), ya absorbido por el 19
>    pero con el detalle de cada uno;
> 7. **`PLAN_17_SALIR_DEL_ESPIRAL.md`** — solo su §1 (investigación sobre
>    Foundry dnd5e y DiceCloud) y su §2 (el diagnóstico del espiral: qué es
>    un "parche puntual" y por qué el proyecto lo prohíbe). Es la base de la
>    auditoría pendiente, ver más abajo;
> 8. **`FUENTES.md`** — procedencia y correcciones de transcripción, la más
>    reciente arriba (es largo; se lee por sección).

---

## El estado en un vistazo (2026-09-03)

```bash
python3 validar.py            # 0 errores
python3 verificar_srd.py      # 646 valores · 0 discrepancias
python3 verificar_foundry.py  # 3749 valores · 0 discrepancias
python3 cobertura.py          # 0 preguntas sin responder
python3 censo.py              # 937 unidades · 0 sin declarar · 579 pendientes
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done   # 26/26
python3 generar_ficha.py --barrido --exhaustivo   # 240/240
python3 verificar_documentos.py   # ¿CONTINUAR.md y FODA.md dicen la verdad?
python3 verificar_chequeos.py     # ¿algún chequeo abandona un registro en silencio?
```

Las 17 suites de `_verificacion/mutaciones_*.py` están todas en verde;
`verificar_documentos.py` las descubre por patrón y no hace falta acordarse
de sus nombres ni de sus cifras — las contrasta contra lo que este fichero y
`FODA.md` dicen.

### Las cifras que este documento promete

`verificar_documentos.py` las lee **de aquí** y las contrasta contra la salida
real en cada pasada. No son decoración: son las anclas del chequeo, y por eso
van en prosa y no dentro del bloque de comandos de arriba.

> **Repuestas el 2026-09-03.** La reescritura de este fichero de ese mismo día
> las borró sin querer, y `verificar_documentos.py` solo avisaba con `⚠`: once
> cifras dejaron de contrastarse y el script siguió diciendo «los documentos
> de estado cuadran con la base». Ahora borrarlas **hace fallar** el script
> —criterio del `PLAN_19` §12.1: «ningún chequeo se degrada a aviso»—, que es
> justo el modo de fallo que este proyecto persigue.

- `verificar_srd.py` -> 646 valores contrastados · 0 discrepancias
- `verificar_foundry.py` -> 3749 valores contrastados · 0 discrepancias
- INTEGRIDAD: 684 dados · 436 conversiones · 391 conjuros en `tirada` · 677
  pares de vecindad · 782 campos de ortografía · 391 citas de conjuro · 52
  costes sin fuente externa · 25 efectos
- 55 mejoras de dote estructuradas, leídas de `dotes/*.yaml`

**Contenido cerrado, sin manual pendiente de transcribir ni de auditar:** 391
conjuros, 12 clases, 48 subclases, 158 rasgos de clase, 75 dotes, 10
especies, 16 trasfondos, equipo, munición, reglas de generación y multiclase
(transcritas, no ejecutadas — ver más abajo).

---

## 🔬 PRÓXIMA SESIÓN — lo primero, antes de tocar código

**Encargo del 2026-09-03, textual: revisar el código buscando mejor
solución a los "parches puntuales" en vez de seguir apilando verificadores.**

> **Hecha la mitad, el 2026-09-05.** Los diez hallazgos de la ronda 2 están
> cerrados, y siguiendo el encargo: no diez arreglos, sino **cuatro
> mecanismos y tres correcciones de dato** (detalle en `PLAN_ESTRES.md` →
> «Cierre de la ronda 2»). El más ilustrativo es el de las claves
> desconocidas: en vez de rechazar las tres que los agentes inventaron, la
> lista válida se **lee de `personajes/_ESQUEMA.md`**, y así rechaza también
> una cuarta que nadie había probado.
>
> **La otra mitad ya tiene plan y está en marcha: `PLAN_20_AUDITORIA.md`.**
> Ese documento es el estado vivo del encargo — qué se midió, qué se cerró y
> qué falta. Lo hecho hasta hoy (2026-09-05):
>
> - **Fase 0** · el censo ya no se puede inflar en silencio.
> - **Fase 1.1** · `mutaciones_silencios.py` aparte, la primera suite que muta
>   **el motor** (`mutaciones_motor.py`): 4 de 11 mutaciones las caza alguna
>   ficha, y las 7 restantes quedan **enumeradas** en `motor_sin_carga.json`
>   como trozos de aritmética que hoy no protege nada.
> - **Fase 1.2** · el bloque `calculado` lleva `_origen`, y `--calcular` no
>   puede firmar como `agente-manual`: si el escritor puede firmar de oráculo,
>   no hay oráculo.
> - **Fase 1.3** · octava fila del censo, «efectos con carga»: 25 unidades,
>   0 alcanzadas, 25 en deuda. Nace en verde sin perdonar nada.
> - **Fase 1.4** · la CD de conjuros **entra en la base**. Dos calculistas
>   independientes pararon en el mismo sitio: la fórmula vivía cableada en
>   `calculo.py` con su cita en un comentario de Python.
> - **Fase 1.5** · el `KeyError` que ese mismo cierre introdujo — un chequeo
>   que explota en vez de hablar, la familia del hueco nº 10 de la ronda 2,
>   reaparecida el mismo día. Cerrado, y la suite de aritmética volvió a
>   verde (`mutaciones_aritmetica` 40/40 hoy, con la CA base ya dentro).
> - **Fase 1.6** · `verificar_chequeos.py` decía «ninguna rama silenciosa
>   nueva» con 67 silenciosas y una línea base de 64: su huella ignoraba la
>   condición y 67 ramas colapsaban en 41. El guardián del silencio dejaba
>   crecer su propia deuda, y no lo mutaba nadie.
>
> - **Tanda a ciegas del calculista** · **8 de 8**. Dos agentes que recibieron
>   la ficha SIN su bloque `calculado` derivaron a mano los ocho valores de
>   dos fichas y coinciden con el motor. **La fila 8 pasa de 0/25 a 4/25**: el
>   primer contraste externo real de la aritmética. Y de rebote destapó que
>   `calculo.ca()` cableaba el `10` de la CA sin armadura mientras la base la
>   declaraba y `efectos.py` la leía — dos implementaciones sin nadie
>   comparándolas.
> - **Fase 2 CERRADA** · `equipo/` deja de ser invisible. Los DIRECTORIOS de
>   regla también se descubren ahora; `armaduras.yaml` entra como fuente
>   `derivada` (sus 13 registros al censo); el control negativo que exigía que
>   el censo NO se enterara **se invierte, no se borra**; `municion.yaml`
>   —sin validar desde el 2026-08-19 porque `validar_equipo` llevaba sus
>   ficheros a mano— ya se valida, con sus referencias cruzadas; y la cifra
>   del censo queda anclada, que es la que más se mueve y la que nadie
>   contrastaba.
>
> - **Fase 3 · la novena fila del censo: constantes de dominio en Python.**
>   Un literal de Python cuyas cadenas están TODAS en el vocabulario de una
>   colección de la base es autoridad duplicada. Medidas **39** (umbral ≥3
>   cadenas, declarado), y es **la única fila que debe tender a cero**: solo
>   se salda borrando el literal. Ya va por 30. De ahí salió que `buscar.py`
>   no tenía `municion.yaml` en su tupla desde que ese fichero se creó — un
>   objeto suyo no se encontraba y el mensaje decía que no existía. Va por 25.
> - **`reglas/caracteristicas.yaml`** · el emparejamiento «Fuerza» ↔ `fue` no
>   estaba declarado en ninguna parte y Python lo copiaba en CINCO módulos.
>   El fichero no relee el manual: reúne lo que la base ya tenía repartido en
>   tres sitios, y `validar_caracteristicas` lo ata a los tres para que no
>   pueda separarse. De ahí salió un fallo latente: `generar_ficha` repartía
>   el conjunto estándar sobre una lista de seis a mano, así que una séptima
>   característica se habría quedado sin puntuación en silencio.
>
> - **Fase 4 CERRADA · los vocabularios cerrados ya tienen quien los consuma.**
>   El censo comprobaba **base → código**; faltaba la vuelta. Se podía añadir
>   una condición, una operación o una fuente de valor a `reglas/efectos.yaml`
>   y `validar.py` seguía diciendo «0 errores»: el efecto que la usara no se
>   habría aplicado, en silencio. Ahora cada condición dice cómo se decide,
>   `agregar()` ITERA el orden que declara la base —era prosa que citaba y no
>   leía— y cada fuente de valor necesita su lector.
>   **De rebote, `mutaciones_motor` pasa de 4/11 a 7/12**: borrar el agregador
>   `min`, `max` o `set` ya no es invisible, porque el vocabulario tiene
>   consumidor exhaustivo.
>
> - **Fila 9 CERRADA en lo que se podía cerrar: de 39 a 22, y las 22 con
>   motivo real.** Cero deuda «sin mirar». Las que quedan no se derivan a
>   propósito y cada una dice por qué: glosarios de vocabulario externo
>   (ahora con chequeo de cobertura, que no tenían), requisitos de esquema
>   —derivarlos haría el chequeo vacuo—, navegación estructural y listas de
>   excepción auditadas.
> - **Fila 8 de 4/25 a 7/25** con una tercera tanda a ciegas (13 de 13
>   valores). Es el TECHO con las 18 fichas actuales: los 18 efectos que
>   faltan no los aplica ninguna ficha, así que solo se cierran **escribiendo
>   fichas nuevas** que los ejerciten. Eso es trabajo previo al calculista.
>
> - **Ocho fichas nuevas, elegidas por las listas y no por una idea de
>   personaje.** Siete las dirigió la fila 8 y cubren los 18 efectos que no
>   ejercitaba nadie; la octava la dirigió `motor_sin_carga.json` y ejercita el
>   mínimo de 1 PG por nivel (Constitución 8, dado d6 y una tirada de 1: sin
>   esas tres cosas a la vez el mínimo no se activa).
> - **Fila 8 de 4/25 a 16/25** · **`mutaciones_motor` de 4/11 a 9/12 cazadas.**
>
> ## 🔴 LO PRIMERO AL REANUDAR
>
> **Relanzar la tanda a ciegas para cinco fichas.** Los cuatro agentes de la
> última tanda murieron por límite de sesión; dos habían escrito su informe
> antes de morir (paladín y explorador: 10 de 10 valores coinciden, ya
> promovidas) y dos no. Faltan:
>
> ```
> barbaro_berserker_n20   monje_elementos_n20   bardo_danza_n3
> bardo_valor_n3          druida_luna_n3
> ```
>
> El procedimiento está probado: `verificar_personaje.py --datos-crudos <ficha>`
> para el fichero crudo, y el encargo del mandato E de `PLAN_ESTRES.md` con los
> dos avisos que evitan hallazgos ya conocidos (la CA sin armadura y la CD de
> conjuros). Al coincidir, `_origen: agente-manual` con su informe → **la fila 8
> llega a 25/25 y se cierra el criterio del `PLAN_20`**.
>
> **Los tres huecos de motor que quedan NO se cierran con fichas**, y el motivo
> está escrito en `_verificacion/motor_sin_carga.json`: `mul` no lo usa ningún
> efecto de la base, `math.floor` solo actúa sobre una variable no decimal que
> reciba un fraccionario (y lo único fraccionario es `velocidad`, declarada
> decimal), y el orden de agregación necesita dos operaciones sobre la misma
> variable. Son vocabulario del motor por delante del dato. No busques una ficha
> imposible.
>
> Después: el encargo abierto de rearquitecturación, más abajo.
> `subir_nivel.py` y `generar_ficha.py` siguen sin mirarse con esta lupa: el
> punto 2 de aquí abajo sigue vigente para ellos.

### Por qué esto va primero

Es la misma lección que ya cerró el espiral una vez (`PLAN_17`, §2): el
proyecto repitió **cinco veces** una lista escrita a mano que se quedaba
corta, y cada vez la respuesta fue "otro verificador" en vez de "por qué
sigue apareciendo esto". `censo.py` lo cerró **estructuralmente** — la
cobertura se descubre, no se enumera — y desde entonces la regla inviolable
6 lo dice con todas las letras.

La ronda 2 de estrés (2026-09-03, ver `PLAN_ESTRES.md`) encontró **10
hallazgos nuevos** en `verificar_personaje.py`, y al clasificarlos salió
esto: **no son 10 bugs sueltos**.

| Categoría | Cuántos | El patrón |
|---|---|---|
| Autoridad duplicada en Python (el patrón del espiral) | 2 | El tope de 20 en mejoras está cableado con `> 20`, cuando 42 de 43 dotes ya traen `mejora_caracteristica` estructurado. `pg_por_nivel` no se contrasta contra el dado aunque `calculo.valor_establecido_pg()` ya existe y lee la base |
| Falta un validador de forma genérico | 1 | Claves desconocidas del YAML (`raza:`, `decisiones.nota`) no se rechazan una por una — hace falta UN recorrido que valide contra el esquema entero, no parches por clave |
| Falta extender un mecanismo que ya existe | 2 | Idiomas y conjuros de clase no pasan por el mismo contraste "reúne lo permitido, comprueba membresía" que ya usan armas/armaduras/herramientas |
| Bugs puntuales de verdad | 5 | El resto: duplicado truco/preparado, dos falsos positivos, dos de robustez |

**Solo 5 de 10 eran parches puntuales genuinos.** Los otros 5 son la misma
familia de defecto, dos o tres veces, con nombres distintos. Arreglarlos uno
por uno habría sido exactamente el error que `PLAN_17` diagnosticó.

### Lo que hay que hacer, en este orden

1. **No arrancar arreglando los 10 hallazgos de la ronda 2 tal cual.**
   Primero, diseñar los 2-3 mecanismos generales (lectura de
   `mejora_caracteristica`, un validador de forma que recorra el esquema, la
   extensión del contraste "permitidas" a idiomas y conjuros) y ver cuántos
   de los 10 cierran solos.
2. **Extender la pregunta a todo el código, no solo a
   `verificar_personaje.py`.** La ronda de estrés solo estresó la
   verificación de fichas. `calculo.py`, `efectos.py`, `subir_nivel.py`,
   `generar_ficha.py` no se han mirado con esta lupa todavía. Buscar el
   mismo patrón que `_ORIGENES`/`_TABLA_COSTE`/`COMPLETO`-`MEDIO` ya
   enseñaron: un literal en Python (un número, un tope, una tabla) que
   también vive en un `.yaml` de la base, sin que nada los compare.
3. **Si el patrón vuelve a aparecer en otro sitio, no es una regla nueva por
   caso: es la regla inviolable 6 aplicada más ancho**, o el indicio de que
   hace falta una regla inviolable 7 — eso se decide con lo que la auditoría
   encuentre, no antes.
4. Solo entonces, cerrar lo que quede como parche puntual genuino, cada uno
   con su chequeo y su mutación como manda el método.

### Lo que queda después de eso

- **Fase 6 del `PLAN_19` — multiclase.** Reglas ya transcritas y citadas en
  `reglas/generacion_personaje.yaml → multiclase`; falta ejecutarlas.
- **Fase 5 del `PLAN_19` — el residuo de ~11 % en prosa de conjuros.**
  Necesita el manual (no está en este contenedor) y la decisión de cuánto
  importa es de la usuaria: para uso propio, tolerable; no bloquea nada de
  lo anterior.
- El resto de `PLAN_19` §16 (equipo, metamagias, tablas sin contrastar): baja
  prioridad, medido y declarado, no bloquea el producto.

---

## 🏗 ENCARGO ABIERTO — rearquitecturar, no seguir parcheando verificadores

**De la usuaria, el 2026-09-06, textual:**

> *«queda claro que los validadores, debemos dar por hecho que SIEMPRE MIENTEN,
> creo que en futuro se debería hacer una rearquitecturación de código»*

No es una impresión: es lo que midió la auditoría del `PLAN_20` en un solo día.
**Cada guardián de este repositorio se cazó a sí mismo, y ninguno se había
cazado antes:**

| Guardián | Lo que decía | Lo que pasaba |
|---|---|---|
| `verificar_chequeos.py` | «ninguna rama silenciosa nueva» | 67 ramas con línea base de 64: su huella colapsaba las gemelas |
| `censo.py` | «0 sin declarar» | `equipo/` fuera del universo, y una mutación lo blindaba |
| `validar.py` | «0 errores» | `validar_conjuros_cd` reventaba sin imprimir su etiqueta |
| `validar.py` | «0 errores» | tres vocabularios cerrados sin ningún consumidor |
| `mutaciones_motor` | «cobertura perdida» | falso: era una descripción reescrita |

Y el patrón que lo explica: **un verificador que se comprueba a sí mismo no
comprueba nada.** Los cinco se destaparon desde fuera —una mutación, un agente
a ciegas, otro verificador—, nunca solos.

**Lo que la rearquitecturación tendría que atacar, medido, no supuesto:**

1. **Ningún verificador tiene guardián propio por defecto.** `mutaciones_silencios.py`
   nació el 2026-09-05 porque `verificar_chequeos.py` no lo mutaba nadie; el
   mismo hueco sigue abierto para `censo.py` en parte, `cobertura.py`,
   `verificar_documentos.py` y `verificar_srd.py`. Debería ser estructural, no
   una suite por descubrimiento.
2. **Cada deuda enumerada reinventó su fichero.** Hay ya seis JSON con el mismo
   patrón —línea base, solo puede bajar, poda al saldar— y cada uno lo
   implementa a mano, con sus propios bugs: uno guardaba frases en vez de ids,
   otro no podaba, otro no distinguía «nuevo» de «perdido». Es UNA abstracción,
   escrita seis veces.
3. **El error de un chequeo mataba al informe.** Tres veces en dos días. Se
   cerró con `validar._correr()`, pero `verificar_srd.py`, `verificar_foundry.py`
   y `cobertura.py` siguen sin ese muro.
4. **La identidad de una unidad se inventa en cada sitio.** Huella por conjunto,
   por id, por frase, por línea… y las tres veces que se eligió mal, el
   verificador mintió.

**Lo que NO hay que hacer:** empezar la rearquitecturación arreglando los cinco
casos de la tabla. Eso es exactamente el espiral. Lo que se arregla es el
patrón: una sola abstracción de deuda enumerada, un muro de errores común, una
regla única de identidad, y la promesa de que **todo verificador tiene su
prueba por mutación** convertida en cuenta del censo, no en costumbre.

---

## Reglas inviolables

1. **Consultar, no recordar.** Todo dato de reglas sale de la página del
   manual, nunca de lo que el modelo «sepa» de D&D.
2. **Citar siempre.** Sin página citada, un dato no entra en la base.
3. **Decir «no lo tengo».** Si algo no se lee con claridad, se marca y se
   pregunta. Nunca se rellena.
4. **Solo edición 2024.** El manual EDGE de la papelera (2014) está vetado.
5. **Validar antes de dar por cerrada una fase.**
6. **La cobertura se descubre, nunca se escribe a mano.** Ningún módulo
   puede llevar dentro la lista de los ficheros, campos o columnas que mira.
   Se descubre por patrón y se contrasta contra un manifiesto que declara
   también las exclusiones, con motivo. Apareció **cinco veces** en código
   distinto antes de escribirse como regla (detalle en `PLAN_17` §2); hoy la
   comprueba `censo.py` (867 unidades, 0 sin declarar).

   **El corolario que la auditoría pendiente investiga:** la regla 6 es
   sobre listas de cobertura. La ronda 2 de estrés sugiere un patrón hermano
   — *autoridad numérica duplicada en Python en vez de leída de la base* —
   que hoy no tiene ni nombre de regla ni chequeo que lo cace por sí solo.

---

## Cómo se ha trabajado (y conviene seguir haciéndolo)

- **Reparto por modelo:** la lectura visual se delega a agentes Sonnet; el
  diseño, el código y las decisiones, a Opus. Ficheros disjuntos para que
  corran en paralelo sin pisarse.
- **Nada se da por bueno porque un script diga «0 errores».** Los defectos
  más graves de este proyecto sobrevivieron a validaciones en verde. Todo
  trabajo de agente se verifica por muestreo o por estrés independiente.
- **Cada chequeo nuevo se prueba por mutación** antes de confiar en él: se
  corrompe la base a propósito en una copia desechable y se comprueba que
  salta.
- **La ronda de estrés con agentes (`PLAN_ESTRES.md`) se corre después de
  cada fase grande, no una vez.** Es lo único que encuentra lo que ningún
  chequeo escrito por la misma mano encuentra — dos rondas, dos veces
  confirmado.
- **Una ausencia también es un dato, y se documenta como tal.** Cuando el
  manual no dice algo, la respuesta correcta es «el manual no lo dice, y
  aquí está dónde miré», nunca un hueco silencioso.

---

## Mapa de ficheros

| Ruta | Qué hay |
|---|---|
| `clases/<clase>.yaml` | Tabla de progresión 1-20 + `atributos_basicos` |
| `clases/rasgos/<clase>.yaml` | Texto de los 158 rasgos del tronco de clase |
| `clases/subclases/<clase>.yaml` | 48 subclases con el texto de sus rasgos |
| `reglas/generacion_personaje.yaml` | Métodos de características, multiclase, `px_por_nivel` |
| `reglas/habilidades.yaml`, `reglas/idiomas.yaml` | Las 18 habilidades y los idiomas |
| `especies/`, `trasfondos/`, `dotes/`, `equipo/` | Orígenes, dotes y equipo |
| `hechizos.json` | 391 conjuros, filtrables por `clases` y `nivel` |
| `_verificacion/foundry_srd52/` | SRD 5.2 (CC-BY-4.0) estructurado campo a campo, packs de Foundry dnd5e |
| `_verificacion/glosario_especies.yaml`, `glosario_subclases.yaml` | Puentes es↔en de nombres propios, escritos a mano por necesidad y contrastados numéricamente |
| `personajes/` | Fichas de personaje (`_ESQUEMA.md` es el contrato) |
| `calculo.py` | Toda la aritmética de personaje |
| `buscar.py` | Consulta determinista que falla ruidosamente |
| `efectos.py` · `reglas/efectos.yaml` | Motor de efectos: reglas como dato citado, no `if` de Python |
| `materiales.py` | Descomposición del componente material |
| `prerrequisitos.py` · `reglas/prerrequisitos.yaml` | Gramática de prerrequisitos de dote |
| `subir_nivel.py` · `reglas/subida_de_nivel.yaml` | Qué pasa al subir de nivel (monoclase; multiclase transcrita, sin ejecutar) |
| `verificar_personaje.py` | Trazabilidad de una ficha — el objetivo de la auditoría pendiente |
| `verificar_foundry.py` | Contraste contra el SRD 5.2 estructurado, 9 módulos, sin traducir: empareja por claves independientes del idioma |
| `verificar_srd.py` | Contraste contra el SRD 2024 de Open5e |
| `censo.py` · `_verificacion/censo_exenciones.yaml` | La regla inviolable 6, comprobada |
| `validar.py` | Coherencia interna de toda la base, 30 chequeos |
| `generar_ficha.py` | Generador determinista de fichas legales — solo produce lo que se le programó, ver `PLAN_ESTRES.md` |
| `_verificacion/mutaciones_*.py` | Prueba por mutación de cada chequeo, una suite por familia |
| `.claude/skills/personaje/`, `.claude/skills/subir-nivel/` | Los dos flujos de uso |

## Método de lectura visual (si hay que leer más manual)

```bash
pdftoppm -r 170 -f <pag> -l <pag> -png ../Manual_del_Jugador_2024.pdf /tmp/render/p
```

**`pdftotext` NO es fuente válida** (escaneo a 96 DPI, OCR basura) — solo
sirve para localizar página. Offset confirmado: **página_pdf = página_libro
+ 2**. El manual no está en este contenedor; la lectura visual la lleva la
usuaria.
