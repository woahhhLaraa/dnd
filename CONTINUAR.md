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
> 3. **`PLAN_21_REARQUITECTURA.md`** — **el plan vigente**: los cuatro
>    frentes que hicieron posible que cada guardián se cazara a sí mismo, y las
>    tres fases que los cierran. Nace del encargo del 2026-09-06;
> 4. **`PLAN_20_AUDITORIA.md`** — **la auditoría, ya cerrada**: el inventario
>    medido de autoridad duplicada y las cinco fases que la cerraron. Nace del
>    encargo del 2026-09-03 y de lo que la ronda 2 de estrés destapó;
> 5. **`PLAN_ESTRES.md`** — la rutina de estrés con agentes y sus dos rondas
>    corridas, con los hallazgos de cada una;
> 6. **`FODA.md`** — análisis vigente, si vas a decidir arquitectura;
> 7. **`PLAN_18_REVISION_COMPLETA.md`** — registro de los bloques A-D del
>    Plan 18 (censo, mutaciones, listas cerradas), ya absorbido por el 19
>    pero con el detalle de cada uno;
> 8. **`PLAN_17_SALIR_DEL_ESPIRAL.md`** — solo su §1 (investigación sobre
>    Foundry dnd5e y DiceCloud) y su §2 (el diagnóstico del espiral: qué es
>    un "parche puntual" y por qué el proyecto lo prohíbe). Es la base de la
>    auditoría pendiente, ver más abajo;
> 9. **`FUENTES.md`** — procedencia y correcciones de transcripción, la más
>    reciente arriba (es largo; se lee por sección).

---

## El estado en un vistazo (2026-09-03)

```bash
python3 validar.py            # 0 errores
python3 verificar_srd.py      # 646 valores · 0 discrepancias
python3 verificar_foundry.py  # 3749 valores · 0 discrepancias
python3 cobertura.py          # 0 preguntas sin responder
python3 censo.py              # 957 unidades · 0 sin declarar · 576 pendientes
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done   # 26/26
python3 generar_ficha.py --barrido --exhaustivo   # 240/240
python3 verificar_documentos.py   # ¿CONTINUAR.md y FODA.md dicen la verdad?
python3 verificar_chequeos.py     # ¿algún chequeo abandona un registro en silencio?
```

Las 20 suites de `_verificacion/mutaciones_*.py` están todas en verde;
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
>   **De rebote, `mutaciones_motor` mejoró**: borrar el agregador
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
> - **Nueve fichas nuevas, elegidas por las listas y no por una idea de
>   personaje.** Siete las dirigió la fila 8 y cubren los 18 efectos que no
>   ejercitaba nadie; la octava la dirigió `motor_sin_carga.json` y ejercita el
>   mínimo de 1 PG por nivel (Constitución 8, dado d6 y una tirada de 1: sin
>   esas tres cosas a la vez el mínimo no se activa).
>
> ## ✅ EL PLAN 20 ESTÁ CERRADO (2026-09-06)
>
> Las cinco fases hechas y el criterio de cierre cumplido, remedido:
>
> | Criterio | Prometía | Real |
> |---|---|---|
> | filas del censo | 7 → 9 | **9** |
> | unidades, 0 sin declarar | 867 → ~919 | **937** |
> | fila 9 (constantes) tiende a cero | 34 | **22, y las 22 con motivo real** |
> | fila 8 (efectos con carga) | 25/25 | **25/25** |
> | `mutaciones_motor` | N/N | **12/12 · 9 cazadas, 3 declarados** |
>
> Los tres huecos de motor que quedan **no se cierran con fichas**, y el motivo
> está dentro de `motor_sin_carga.json`: `mul` no lo usa ningún efecto de la
> base, `math.floor` solo actúa sobre una variable no decimal que reciba un
> fraccionario (y lo único fraccionario es `velocidad`, declarada decimal), y
> el orden de agregación necesita dos operaciones sobre la misma variable. Son
> vocabulario del motor por delante del dato. **No busques una ficha
> imposible.**
>
> ### El hallazgo con el que se cerró, y es el mayor de la ronda
>
> Al derivar a ciegas las dos fichas de nivel 20, dos agentes distintos, en dos
> clases distintas, **dieron números mayores que el motor**: 40 puntos de golpe
> en el Bárbaro y 4 de CA en el Monje. Tenían razón los dos.
>
> «Campeón primordial» y «Cuerpo y mente» dicen, sin condición ni duración, que
> dos puntuaciones suben 4 (tope 25, no 20). La regla estaba transcrita y
> citada **pero solo en la prosa**: ni el motor la aplicaba, ni la ficha podía
> expresarla, ni el generador la ponía. **Todo personaje de nivel 20 de Bárbaro
> o Monje salía con dos características y varios números de menos, en verde** —
> incluida `draconido_monje_n20`, que llevaba semanas en la base.
>
> Cerrado con el vocabulario que ya existía (`mejora_caracteristica`, el de las
> dotes), una cuarta fuente de puntuación en `verificar_mejoras` —base +
> trasfondo + mejoras + dotes + **rasgos**— y el mismo cálculo en el generador.
> Y con un matiz que el propio verificador destapó: **el tope de una mejora se
> mide en su momento**, no al final; comparar la del nivel 16 («máx. 20»)
> contra un `final` que el rasgo del 20 dejó en 24 la haría ilegal sin serlo.
>
> **Dos mutaciones cambiaron de vehículo, no de chequeo**, y las dos por la
> misma razón: su premisa dejó de ser cierta. `u_efecto_nuevo_sin_carga`
> colgaba de «Furia» del Bárbaro, y ahora hay un Bárbaro con lectura
> independiente que la sostiene: cuelga de un rasgo de Brujo, una de las cuatro
> clases sin ficha promovida. Y `n_otro_reparto_legal` llevaba dos puntuaciones
> escritas a mano que el rasgo nuevo desfasó: ahora las DERIVA del reparto que
> sustituye.
>
> **Lo siguiente:** el encargo abierto de rearquitecturación, aquí abajo. No
> queda plan escrito por delante.

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
   y `cobertura.py` siguieron sin ese muro hasta la fase 2 del `PLAN_21`
   (2026-09-06), que lo puso en los siete con `informar.muro`.
4. **La identidad de una unidad se inventa en cada sitio.** Huella por conjunto,
   por id, por frase, por línea… y las tres veces que se eligió mal, el
   verificador mintió.

**Lo que NO hay que hacer:** empezar la rearquitecturación arreglando los cinco
casos de la tabla. Eso es exactamente el espiral. Lo que se arregla es el
patrón: una sola abstracción de deuda enumerada, un muro de errores común, una
regla única de identidad, y la promesa de que **todo verificador tiene su
prueba por mutación** convertida en cuenta del censo, no en costumbre.

### El encargo ya tiene plan: `PLAN_21_REARQUITECTURA.md`

Cuatro frentes en tres fases, y **ninguna cifra del plan vale sin remedirla**.

> **Fase 1 CERRADA (2026-09-06) · una sola abstracción de deuda enumerada.**
>
> `deuda.py` en la raíz —entra como unidad del censo, que es lo correcto— con
> las cuatro propiedades que solo tenía el último de los cinco ficheros, y que
> los otros cuatro no tenían porque se escribieron antes:
>
> | fichero | entradas | podaba | nuevo ≠ perdido | guardaba elenco |
> |---|--:|:--:|:--:|:--:|
> | `chequeos_silenciosos.json` | 65 | sí | **no** | **no** |
> | `rasgos_sin_declarar.json` | 480 | **no** | **no** | **no** |
> | `efectos_sin_carga.json` | 0 | sí | **no** | **no** |
> | `motor_sin_carga.json` | 3 | sí | sí | sí |
> | `constantes_de_dominio.json` | 22 | sí | **no** | **no** |
>
> Los cinco llamadores migrados (`verificar_chequeos.main`, las tres filas del
> censo, `mutaciones_motor.main`), y `validar.py` deja de abrir a mano el JSON
> de rasgos: lo lee por `Deuda(...).vigentes`. **Ninguna identidad cambió al
> migrar** — cambiarla invalida la línea base, que es justo la mentira que el
> plan persigue —, pero la identidad pasa a ser una CLAVE CORTA guardada dentro
> del fichero, con la prosa aparte en `_identidad_explicada`. La primera
> versión comparaba la frase entera y **saltó contra su propio autor a los diez
> minutos**, por siete palabras de más.
>
> **La guarda `_verificacion/mutaciones_deuda.py` (10/10)**, y el camino hasta
> ahí es la lección de la fase, repetida por tercera vez en dos días:
>
> - La primera versión corría los cinco llamadores contra la base intacta y
>   sacó **2/7** de las siete de entonces. Con los cinco ficheros en reposo —nada que podar, nada nuevo,
>   nada perdido— romper «¿poda?» no cambia ni un byte: **una mutación que solo
>   cambia el comportamiento en una situación que no ocurre, no cambia nada**.
>   Ahora el arnés FABRICA cada situación con un fichero desechable.
> - Al fabricarlas, el control negativo destapó un defecto REAL de `deuda.py`
>   antes de mutar nada: el elenco no llegaba al disco cuando la deuda no se
>   movía, así que una prueba que empieza a medir más no se distinguía de una
>   regresión a la pasada siguiente.
> - Y la comprobación de identidad salió **6/7** por su propio arnés:
>   preguntaba `"LANZO" in salida` contra las respuestas «LANZO»/«NO_LANZO», y
>   «NO_LANZO» contiene «LANZO». La propiedad daba por buena justo la respuesta
>   que tenía que delatar.
>
> Y la propia migración rompió un guardián, que lo dijo: al pasar
> `verificar_chequeos` a `deuda.py`, «rama nueva» quedó leído como
> `perdidos`, así que **una rama silenciosa en código NUEVO —que nunca estuvo
> en el elenco— salía en verde**. Antes de migrar era roja. `mutaciones_silencios`
> lo cazó en la primera pasada, **3 de 6**, con sus tres mutaciones a la vez.
> El arreglo no fue en el llamador: distinguir lo nuevo de lo perdido es una
> MEDICIÓN y la hacen los cinco, pero **si lo nuevo es aceptable es una
> POLÍTICA del fichero**, y ahora se declara en el `Deuda` junto a la
> identidad. `motor_sin_carga` acepta mediciones nuevas; `chequeos_silenciosos`
> es `cerrada=True` y no acepta ninguna. Vuelve a 6/6, y la política tiene su
> propia mutación.
>
> **Y una mutación cambió de vehículo, no de chequeo.** `m_deuda_muerta`
> metía a mano un rasgo obsoleto en `rasgos_sin_declarar.json` y exigía que el
> censo lo cazara, porque esa fila NO PODABA. Ahora poda: la entrada muerta
> sale sola y el recuento no se mueve (medido: 938 · 0 sin declarar). La
> premisa dejó de ser cierta **porque el defecto se cerró**, así que la
> mutación se movió a la otra dirección, que es peor y no la miraba nadie:
> `m_deuda_rehecha` borra el fichero y exige que el censo pare, porque sin él
> la línea base se rehace con lo medido hoy y los 480 rasgos sin declarar
> quedarían «declarados» de golpe, en verde.
>
> **Y el propio guion que migró los cinco escribió su prosa en blanco.** Como
> `_escribir` prefería siempre lo del disco —para que la prosa se pueda editar
> a mano—, `_como_se_salda` se quedó VACÍO en tres de los cinco: el campo que
> dice cómo se paga una deuda, sin forma de repararlo desde el llamador, que sí
> lo tenía escrito. Y la migración se llevó por delante el `_ultima_poda` de
> `efectos_sin_carga.json`, que nombraba los tres efectos saldados el día
> antes; restaurado de git. Ahora una prosa vacía no le gana a la del código,
> y **la condición de «cuándo hay que escribir» dejó de estar enumerada**: se
> escribe si el texto que saldría es distinto del que hay. Esa lista escrita a
> mano ya se había quedado corta dos veces en un día.
>
> De rebote, `CONTINUAR.md` decía «las 17 suites» con 18 en el disco, **en la
> misma frase que presume de que se descubren por patrón**. Esa cuenta ya la
> ancla `verificar_documentos.py` contra el disco.

> **Fase 2 CERRADA (2026-09-06) · un muro de errores común.**
>
> `informar.py` en la raíz, con `muro(fn, ...) -> (valor, Fallo|None)`. Puesto
> en los siete: `validar._correr` pasa a ser tres líneas encima —sus trece usos
> no cambian—, `verificar_personaje` sustituye su `try` parcial, y `censo`
> (9 filas), `verificar_chequeos` (17 fuentes), `verificar_srd` (12 clases),
> `verificar_foundry` (módulos), `verificar_documentos` (18 suites) y
> `cobertura` (5 bloques) envuelven su bucle. Lo que se perdía no era solo el
> informe: en `verificar_srd` y `verificar_foundry` se perdía **la cifra que
> `verificar_documentos.py` ancla contra estos documentos**, y una cifra que no
> sale no se contrasta con nada.
>
> **El muro no se traga un `sys.exit`.** Un dato que falta en la base tiene que
> seguir parando. Hay UN sitio donde se declara lo contrario, con su motivo:
> `verificar_personaje`, porque allí lo que se examina es la ficha, no la base,
> y la salida es un veredicto sobre la entrada bajo examen. El control negativo
> va en las dos direcciones.
>
> **Y el muro trae un peligro que no estaba en el plan.** Varios de estos
> scripts alimentan una línea base de `deuda.py`, y la poda da por saldado lo
> que hoy no se mide. Un fichero que reventara y cuyo chequeo simplemente
> «siguiera» haría **bajar la deuda sola, en verde**. Lo decide quien mide, no
> el muro: `verificar_chequeos` contrasta con `podar=False` en cuanto una
> fuente falla, y hay un control negativo que lo exige.
>
> ### El hallazgo de la fase, y lo destapó mi propio refactor
>
> Al sacar el cuerpo de un bucle a un ayudante `_ramas_de()` para poder ponerle
> el muro, **cuatro ramas silenciosas desaparecieron de la línea base, en
> verde**, y la poda las dio por saldadas. El motivo: `verificar_chequeos` solo
> miraba funciones llamadas `validar_*`, `verificar_*` o `main`. O sea que
> **bastaba mover una rama de función para dejar de vigilarla**, y una
> convención de nombres es una lista escrita a mano disfrazada — justo lo que
> la regla inviolable 6 prohíbe, dentro del módulo que existe para cazarlo.
>
> Medido: 61 ramas en funciones con prefijo, **59 más en las demás**. Casi la
> mitad de lo que este verificador vigila vivía fuera de su alcance. Ahora se
> miran TODAS las funciones y la línea base pasa de 61 a **120**, con las 59
> como deuda declarada —no permiso: la lista solo puede bajar—. `_auditable` se
> queda para la otra pregunta, la que hace `censo.fila_modulos`: ¿tiene este
> módulo alguna entrada de chequeo, o es una biblioteca? Eran dos preguntas
> compartiendo un predicado.

> **Fase 3 CERRADA (2026-09-06) · la décima fila: guardianes con guardián.**
>
> Convierte «todo verificador tiene su prueba por mutación» de COSTUMBRE en
> CUENTA. `alcanzada` no es «tiene una suite con su nombre»: es **alguna suite
> escribe su fichero `.py`**. La diferencia es toda la fila —
> `mutaciones_materiales`, `mutaciones_prerrequisitos`, `mutaciones_subida` y
> `mutaciones_documentos` existen, están en verde y **no tocan una línea del
> código que dicen guardar**: mutan la base o los documentos, que prueba que el
> chequeo caza datos malos, no que el chequeo no mienta.
>
> **18 unidades · 11 con guardián · 1 declarada · 6 en deuda.** La predicción
> del plan era «~16 y 4 en deuda», y se equivocaba en las dos direcciones:
> `cobertura.py` ya lo cubrió la fase 2, y aparecieron tres que la lista a mano
> no tenía —`buscar.py`, `verificar_documentos.py` y **`informar.py`, el módulo
> que la fase 2 acababa de escribir**—. Por eso la fila se mide y no se lista.
>
> `informar.py` se cerró en el sitio: `mutaciones_muro` mutaba los siete
> scripts y ni una línea del muro, así que **el módulo que existe para que un
> fallo no se pierda podía perder fallos él mismo, en verde**. Ahora se le
> rompen sus tres promesas y va a 13/13.
>
> ### Dos falsos positivos, corregidos afinando
>
> El detector se descubre por AST y las dos veces que mintió lo dijo su propia
> mutación, no yo:
>
> - **Buscaba los nombres `sust`/`_sust` a mano**, y `sust` vive en `_arnes.py`
>   y se importa: decía que `mutaciones_aritmetica` no muta `calculo.py`,
>   cuando sí. Ahora las funciones mutadoras se descubren, y también en qué
>   posición reciben el camino.
> - **Contaba CREAR un fichero como mutarlo.** La mutación que añade un script
>   nuevo a la raíz para exigir que el censo lo cace **se blindaba sola**: la
>   suite que acababa de crearlo aparecía escribiéndolo. Un guardián no fabrica
>   el código que vigila; se lo encuentra y se lo estropea. Ahora una función
>   solo cuenta si LEE el fichero antes de escribirlo.
>
> Y una mutación mía tampoco valía: quitarle a `validar.py` uno de sus DOS
> guardianes no lo deja sin guardián. Ahora quita el único que tiene `deuda.py`.
> `mutaciones_censo` 34/34.

**Lo siguiente:** el `PLAN_21` está cerrado entero. No queda plan escrito por
delante.

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
