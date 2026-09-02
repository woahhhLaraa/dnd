# PLAN 18 — Revisión completa del código y plan de acción

> Escrito el **2026-08-31**, después de aplicar el Plan 17 (C1, C3, C4). Todas
> las cifras están **medidas hoy** con los comandos que se citan al lado.
>
> **Actualizado el 2026-09-02: los bloques A, B y A2 están HECHOS.** El
> resultado, con lo que el censo destapó y no estaba en este plan, en el §11
> (A y B) y el §12 (A2) al final.
>
> Este documento **absorbe los puntos abiertos del `PLAN_17`** y pasa a ser el
> único documento de trabajo hacia delante. El 17 se queda como registro de la
> investigación sobre Foundry y DiceCloud y del diagnóstico del espiral.

---

## 1. Qué funciona (verificado hoy, no de memoria)

```
validar.py                    0 errores · 3,9 s
verificar_srd.py              646 valores · 0 discrepancias
verificar_foundry.py         3020 valores · 0 discrepancias
cobertura.py                  262 preguntas · 0 sin responder
17/17 fichas · barrido 240/240 (136 s)
mutaciones: efectos 26/26 · pg 13/13 · prerrequisitos 10/10
verificar_chequeos            ninguna rama silenciosa nueva
verificar_documentos          los documentos cuadran
```

Y lo que **no** se toca porque está bien hecho:

- **La capa de transcripción.** `validar.py` descubre ficheros con `glob` en
  **14 sitios**. Es el módulo que ya cumplía la regla 6 antes de que la regla
  existiera; es el modelo a seguir, no el problema.
- **El motor de efectos.** El agregador coincide con el de DiceCloud en orden
  y semántica, y su vocabulario es cerrado y citado.
- **La doctrina de fallar ruidosamente.** `calculo.ca()` se **niega** a
  responder cuando la respuesta depende de un rasgo que no puede conocer.
  `efectos.py` exige elegir cuando hay dos `base` en vez de coger el máximo.
  Eso es lo contrario de adivinar, y es lo que hace fiable a la base.
- **`pg_por_nivel`.** Recalcular desde los valores crudos hace que la regla
  retroactiva de Constitución salga sola. Es el mejor modelado del repo.
- **La disciplina de citar.** Ningún dato entra sin página. Es lo que
  distingue esta base de las cuatro que se investigaron.

---

## 2. El defecto de fondo, ya con ocho casos

Un módulo lleva dentro una **lista escrita a mano** de lo que mira, y esa
lista se queda corta sin que nadie se entere.

| # | Lista | Qué se le escapaba | Estado |
|---|---|---|---|
| 1 | `calculo._CA_SIN_ARMADURA` | 2 de las 4 fórmulas de CA | ✅ cerrada (Fase 14) |
| 2 | `efectos._ORIGENES` | 46 subclases · 4 ficheros de dotes | ✅ cerrada (C1) |
| 3 | `verificar_documentos` cifras | `efectos`, desde la Fase 14 | ✅ cerrada |
| 4 | **`calculo._TABLA_COSTE`** | **la tabla de compra por puntos, duplicada del YAML** | ✅ **cerrada hoy** |
| 5 | `validar._PROMESAS` | **`velocidad`**: 1 de las 3 variables calculables | ✅ **cerrada (A2)** |
| 6 | `verificar_chequeos.FUENTES` | audita 3 de las 6 que declara | ✅ **cerrada (A2)** |
| 7 | `verificar_srd.MAPA` | `slots` (7 clases), `forma_salvaje`, `mov_sin_armadura_m` | ✅ **cerrada (A2)** |
| 8 | `verificar_foundry.MODULOS` | **9 de los 17 pares (carpeta, `type`) sin pedir: 562 registros** | ⬜ medida y declarada → **bloque H** |

> **Lo que el censo corrigió de esta tabla (2026-09-02).** El caso 7 no era el
> que decía. `verificar_srd.MAPA` cubre **todas** las columnas que el SRD de
> Open5e publica de las 12 clases: no se le escapa ninguna. `pb` no es un hueco
> —`validar_clase` lo recalcula con la fórmula del manual en los 240 niveles—,
> y el hueco de verdad es **`slots`**, que se contrasta contra las constantes
> `COMPLETO`/`MEDIO` de `validar.py`, **sin cita de página**: siete clases
> descansan en un literal de Python que ninguna fuente respalda.

**El caso 4, encontrado hoy, es el más ilustrativo de todos.** `calculo.py`
tenía:

```python
# reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.coste_en_puntos
_TABLA_COSTE = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
```

Un comentario señalando dónde vive la autoridad, **y debajo una copia**. La
tabla está también en el YAML, `validar.py` valida **la del YAML**, y
`calculo.py` calculaba con **la suya**. Nadie comparaba las dos: una
corrección en la base habría dejado la aritmética con los valores viejos y
todo en verde.

Arreglado leyendo la tabla de la base. Comprobado: falseando el YAML, el coste
pasa de 27 a 117; antes se quedaba en 27 pasara lo que pasara.

> **Criterio para distinguir un defecto de una constante legítima**, porque no
> todas lo son: es defecto cuando **duplica autoridad que vive en la base** y
> nada compara las copias. No lo es cuando es vocabulario de implementación
> (`_A_METROS`, `_NODOS` del AST, mapas de traducción) ni cuando **falla
> ruidosamente** ante lo desconocido (`_RASGOS_DE_CLASE` lanza
> `ErrorDeEfectos` con una clase que no conoce).

---

## 3. Eficiencia — medido con cProfile, no estimado

**El 98 % del tiempo de `validar.py` era volver a parsear los mismos ficheros.**
1068 llamadas a `yaml.safe_load`; solo `validar_subida()` releía las tablas de
clase 333 veces, una por salto de nivel.

```
                        antes      ahora
validar.py              13,1 s     3,9 s     (3,4×)
mutaciones_efectos         —       138 s
mutaciones_pg              —        53 s
barrido 240 fichas         —       136 s
```

Arreglado con `functools.lru_cache` en los tres lectores calientes
(`calculo.cargar`, `efectos._leer`, `validar._clases_data`) más
`cargar_vocabulario()` y `origenes()`.

**Por qué es seguro, y hay que dejarlo escrito:** las pruebas por mutación
copian la base a un temporal y lanzan `validar.py` **en subproceso**, así que
cada mutación estrena caché. Una caché de proceso no puede servir datos viejos
a la mutación siguiente. El contrato es que **lo devuelto es de solo lectura**;
se comprobó que ningún llamador lo muta.

**Lo que queda de margen (~3,9 s):** `hechizos.json` son 555 KB y hay 24
`yaml.safe_load` directos en `validar.py` que no pasan por ningún lector
cacheado. Bajarlo de 3,9 a ~1,5 s es posible pero **ya no es el cuello de
botella**: el barrido y las mutaciones dominan.

---

## 4. Cobertura de pruebas — la cifra que decide si se puede refactorizar

```
                                       2026-08-31   2026-09-02
chequeos `validar_*` en validar.py :       30           30
  con prueba por mutación          :       11           30
  SIN prueba por mutación          :       19            0
```

> **Cerrado el 2026-09-02 (bloque B).** Las tres suites nuevas están abajo, en
> el §11. La cifra ya no se cuenta a mano: la cuenta `censo.py`, que descubre
> los 30 chequeos del AST de `validar.py` y las suites por patrón.

Los 19 sin red, por orden de a qué afectan:

**Aritmética** (los que más importan para el contrato «personaje legal 1→20»):
`validar_atributos_basicos` · `validar_generacion` · `validar_competencias_clase`
· `validar_ataques` · **`validar_mejoras_de_dote`**

**Contenido y referencias:** `validar_clase` · `validar_dotes` · `validar_especies`
· `validar_trasfondos` · `validar_subclases` · `validar_hechizos` ·
`validar_hechizos_clases` · `validar_rasgos_clase` · `validar_equipo` ·
`validar_habilidades` · `validar_idiomas` · `validar_citas_conjuro` ·
`validar_costes_sin_fuente` · `validar_referencias`

> **Deuda declarada, y es de esta misma sesión:** `validar_mejoras_de_dote` se
> escribió el 2026-08-31 (C3) y **está en la lista de los 19**. Se probó a mano
> —quitar el campo y falsear la característica hacen saltar los dos casos— pero
> no se dejó en una suite. Es exactamente la deuda que este documento critica,
> contraída el mismo día. Tiene prioridad en el bloque B.

## 5. Estructura del código — medida, y no justifica un refactor

```
                     funciones   mediana   > 120 líneas
validar.py               47      35 líneas       5
verificar_personaje.py   21      26 líneas       0
efectos.py               21      18 líneas       0
calculo.py               18       9 líneas       0
```

No hay funciones-monstruo ni enredo: la mediana es sana y solo 5 de 47
funciones pasan de 120 líneas. **Y lo decisivo: ninguno de los ocho defectos
del §2 lo causó la estructura.** Todos eran «falta una aserción de cobertura».
Reorganizar el código no habría evitado ni uno.

**El argumento que zanja la pregunta «¿refactorizamos?»:**

> Un refactor es exactamente igual de seguro que la cobertura de pruebas de lo
> que refactorizas.

Con 19 de 30 chequeos sin red, tocar `validar.py` hoy significa que el 63 % de
sus comprobaciones puede dejar de detectar lo que detectaba **sin que nada
avise**. Sería un fallo silencioso introducido por la limpieza contra los
fallos silenciosos.

**Los dos caminos convergen:** si algún día se refactoriza de verdad, el primer
paso obligatorio es el mismo —cubrir los 19— porque no se puede reestructurar
con seguridad lo que no se puede probar. Así que hacer las mutaciones primero
no es la alternativa al refactor: es su requisito. Elegirlo no cuesta nada, y
probablemente después el refactor ya no parezca necesario.

## 6. El agujero del enfoque actual, y hay que decirlo

La **regla inviolable 6** («la cobertura se descubre, nunca se escribe a mano»)
se añadió a `CONTINUAR.md` el 2026-08-31. **Nada la comprueba.** Es prosa.

Y el propio repo ya había aprendido esa lección, en `FUENTES.md:208`:

> *«Llevaba una semana escrita en FUENTES.md (1500 líneas) y se rompió sin
> querer». **Una regla en prosa no impide nada.***

Es decir: se diagnosticó que las reglas en prosa no impiden nada, se construyó
`verificar_chequeos.py` para convertir una de ellas en script… y la regla 6
nació en prosa igualmente. **Nada impide que aparezca la novena lista.**

Se arreglaron cuatro casos y se listaron otros cuatro. Eso sigue siendo
«arreglar caso por caso», que es justo lo que hay que dejar de hacer.

## 7. El censo — la pieza que cierra el patrón

No se trata de prohibir las listas escritas a mano: detectarlas en el AST sería
una heurística con falsos positivos (`_A_METROS`, los nodos del AST, los mapas
de traducción son legítimos). La invariante real es **contable**:

> **Toda unidad de la base tiene que estar alcanzada por nombre por algún
> chequeo, o declarada como no alcanzable con su motivo.**

Un solo script, `censo.py`, que enumere la base y cruce cada unidad contra lo
que los verificadores tocan de verdad:

| Unidad | Fuente de la lista | Quién debería alcanzarla |
|---|---|---|
| fichero de regla | glob sobre `especies/ clases/ dotes/ trasfondos/ reglas/` | `efectos.origenes()` (ya lo exige) |
| variable calculable | `reglas/efectos.yaml` | un chequeo de «promesa» por variable |
| columna de tabla de clase | las 12 `clases/*.yaml` | `verificar_srd.MAPA` o exención declarada |
| categoría de dato externa | `_verificacion/foundry_srd52/` | `verificar_foundry.MODULOS` o exención |
| chequeo `validar_*` | AST de `validar.py` | una suite de mutación o exención |
| rasgo con texto | las fuentes de efectos | `efectos:` o `no_automatizado` (bloque C) |

Su salida es **un número que solo puede bajar**, y los cuatro casos abiertos
del §2 salen de su informe en vez de salir de que alguien lea el código. El día
que aparezca el noveno, lo canta solo.

Es el mismo salto que ya funcionó dos veces aquí: `verificar_chequeos.py` no
audita chequeo por chequeo sino la regla general, y `efectos.origenes()` no
lista fuentes sino que exige que todas estén clasificadas. El censo es eso un
nivel más arriba.

## 7bis. Qué queda por adoptar de Foundry y DiceCloud

Ya adoptado: el modelo de efectos y el agregador de DiceCloud (Fase 14), su
operación `conditional` (C4 del Plan 17), el `ScaleValue` de Foundry como
`columna`, y su taxonomía de *advancement* en `/subir-nivel` (Fase 16).

Lo que falta, y para qué sirve cada cosa:

- **La «Foundry Note» → bloque D.** Foundry automatiza **76 de 332** rasgos de
  clase/subclase 2024 (23 %) y **declara la frontera dentro del dato**: 380
  registros dicen qué no está automatizado. Aquí la frontera es el silencio.
  Es lo que convierte «no lo hemos hecho» en «lo miramos y no toca».
- **`ModifyItem` → el caso `Maestro en armaduras medias`.** «Sumas **3 (en vez
  de 2)** a tu CA por Destreza» no es `add` ni `set` sobre `ca`: cambia un
  **parámetro de la fórmula de la armadura**. El modelo actual no lo expresa y
  Foundry tiene un tipo para exactamente esto.
- **El grafo de dependencias de DiceCloud.** Detecta ciclos y los registra como
  error explícito en vez de colgarse. `orden_de_calculo()` hace parte; falta
  comprobar que un ciclo real falla ruidosamente (candidato a mutación del
  bloque B).

**Lo que NO se copia, y conviene que quede escrito:** Foundry **no tiene tests**
—su `package.json` trae `build`, `lint` y `watch`—. Sustituyen verificación por
cientos de miles de jugadores. Este proyecto tiene una usuaria, así que sus
3666 valores contrastados y sus 149 mutaciones **son el sustituto correcto** y
no se tocan. De Foundry se copia la arquitectura, nunca la ausencia de pruebas.

## 8. Plan de acción, en orden

Cada bloque dice si necesita el manual.

### Bloque A — el censo · ✅ **HECHO (2026-09-02)**

`censo.py` con las seis filas de la tabla del §7, y su informe. **Antes que
arreglar las cuatro listas abiertas**, porque si se arreglan primero se arreglan
«las que encontró Claude»; con el censo se arreglan «las que hay», y se sabe
cuándo se ha terminado. Resultado en el §11.

### Bloque A2 — las cuatro listas abiertas del §2 · ✅ **HECHO (2026-09-02)**

No tenía bloque propio en la primera versión de este plan: el §8 decía «antes
que arreglar las cuatro listas abiertas» y no decía cuándo se arreglaban. Ahora
que el censo las tiene medidas y declaradas una a una, son un bloque.

### Bloque B — cobertura de mutación de los 19 · ✅ **HECHO (2026-09-02)**

Por orden: primero los cinco de aritmética (empezando por
`validar_mejoras_de_dote`, deuda propia), después los de contenido. Es el
requisito de cualquier refactor futuro, y la red que hoy no existe.

### Bloque C — declarar los 21 efectos (sin manual, ~1 día)

Solo hay **3 variables calculables** (`ca`, `pg_max`, `velocidad`), así que el
hueco funcional son 21 rasgos, no 528. Su texto ya está transcrito y citado.

| | Qué | Cuántos |
|---|---|---|
| C1 | Inequívocos: `Veloz` (+3 m), `Defensa` (+1 CA con armadura), `Don de la fortaleza` (+40 PG) | ~4 |
| C2 | Condición nueva «sin armadura pesada» + `Movimiento rápido` y `Errante` | 2 |
| C3 | Situacionales, como `conditional` | ~14 |
| C4 | Decidir `Maestro en armaduras medias` (cambia el TOPE de Destreza: es el `ModifyItem` de Foundry, no un `add`) | 1 |

### Bloque D — cerrar la puerta (sin manual, ~medio día)

`efectos:` obligatorio en todo rasgo, con `no_automatizado` como respuesta
legítima. **Al final, no al principio:** activarlo antes del bloque C dejaría la
base en rojo durante todo el relleno y no se distinguiría una rotura nueva de
la deuda conocida.

### Bloque E — higiene (sin manual, ~medio día)

`requirements.txt` (PyYAML no está declarado), versión de Python declarada (un
`SyntaxError` de 3.12 tumbó cuatro herramientas y nadie se enteró), y las ~50
líneas de duplicación real: `cargar()` en `calculo.py` y `cobertura.py` (**no
son idénticas**: una hace `sys.exit`, la otra devuelve `None`),
`cargar_yaml()` en `verificar_foundry.py`, y `_es_marcador()` en `validar.py` y
`subir_nivel.py`.

### Bloque H — contrastar lo que el SRD estructurado sí trae · ⬜ **nuevo**

**No estaba en este plan, y lo destapó el censo.** 9 de los 17 pares (carpeta,
`type`) de `_verificacion/foundry_srd52/` —**562 registros**— no los pide
ningún módulo de `verificar_foundry.py`. El mayor es `classes24/feat`: **255
rasgos de clase y subclase del SRD 5.2** que nadie contrasta, y que además son
la fuente de la «Foundry Note» que el §7bis quiere para el bloque D. Contrastar
`classes24/class` cerraría de paso `forma_salvaje` y `mov_sin_armadura_m`, las
dos columnas sin fuente externa del bloque A2.

### Bloque F — refactor

**Solo si después de A-E sigue pareciendo necesario.** La medición del §5 dice
que probablemente no lo sea.

### Bloque G — lo único que necesita el manual

Los casos del bloque C cuyo texto transcrito resulte ambiguo, y la revisión de
descripciones de conjuro (residuo medido ~11 %), que la usuaria lleva contra el
manual por decisión propia.

## 9. Criterio de cierre

1. ✅ `censo.py` existe y su número es 0, o lo que no es 0 está declarado con su
   motivo. **Hecho el 2026-09-02**: 0 sin declarar.
2. ✅ Los 30 chequeos `validar_*` tienen prueba por mutación, o exención
   declarada. **Hecho el 2026-09-02**: 30/30, sin exenciones.
3. Los 21 candidatos a efecto, a cero. **Los 9 de `velocidad` cerrados el
   2026-09-02** (A2): quedan los de `ca` y `pg_max`.
4. Quitar `efectos:` de cualquier rasgo hace fallar a `validar.py`.
5. En todo momento: `validar.py` 0 errores, 17/17 fichas, barrido 240/240,
   contrastes en 646 + 3020, mutaciones en verde.

## 10. Lo que este plan no promete

No promete que no aparezca un noveno caso del patrón. Promete que **el día que
aparezca lo dirá el censo**, en vez de esperar a que alguien lea el código con
ojos frescos. Esa es la diferencia entre una auditoría y un espiral: no que no
haya defectos, sino que el repo sepa contar los que le quedan.

---

## 11. Resultado — bloques A y B, ejecutados el 2026-09-02

### Bloque A · `censo.py`

Un script que enumera **seis clases de unidad** de la base —siete desde el
bloque A2— y exige que cada
una esté alcanzada por nombre por algún chequeo, o declarada —con su motivo—
en `_verificacion/censo_exenciones.yaml`. Ninguno de los seis universos se
escribe a mano: se descubren por glob, por AST o por el propio vocabulario de
la base; y ningún alcanzador se copia: se leen los objetos que los módulos
usan de verdad (`efectos.origenes()`, `validar._PROMESAS`,
`verificar_srd.MAPA`, las llamadas a `verificar_foundry.paquete()`).

```
✅ 681 unidades censadas · 0 SIN DECLARAR · 532 pendientes declaradas
```

> Esas son las cifras **al cerrar el bloque A**. El A2 le añadió una séptima
> fila (los módulos de herramienta) y cerró 17 pendientes: hoy son **697
> unidades y 515 pendientes**. Ver el §12.

| Fila | Universo | Alcanzadas | Declaradas |
|---|---|---|---|
| ficheros de regla | 49 | 49 | — |
| variables calculables | 3 | 2 | 1 pendiente (A2) |
| columnas de tabla de clase | 63 | 30 | 24 exentas · 9 pendientes |
| categorías de dato externo | 17 | 7 | 10 pendientes (H) |
| chequeos `validar_*` | 30 | **30** | — |
| rasgos con texto | 519 | 7 | 512 pendientes (C+D) |

**Dos declaraciones, y la diferencia importa.** `exentas` = la unidad no debe
alcanzarse por ahí, y se dice quién responde por ella; es permanente.
`pendientes` = hueco real, con el bloque que lo cierra; es deuda, y solo puede
bajar. Una declaración que ya no corresponda a ninguna unidad **hace fallar al
censo**: el manifiesto no puede pudrirse en silencio, que es como empezaron los
ocho. Los comodines (`prefijo:*`) solo valen en `pendientes` y el informe
imprime siempre cuántas unidades cubre cada uno.

Y el censo tiene su propia prueba por mutación, porque un contador que no
detecta una unidad nueva sería el mismo defecto con una capa de ceremonia
encima: **`mutaciones_censo.py` 18/18**, con una unidad nueva por cada una de
las seis filas, un alcanzador vaciado, dos promesas falsas de cobertura, tres
formas de pudrir el manifiesto, y una que comprueba que el comodín de los 512
rasgos **deja ver crecer el recuento** en vez de esconderlo.

### Bloque B · los 19 chequeos sin red

```
mutaciones_aritmetica.py     31/31    5 chequeos
mutaciones_contenido.py      47/47   11 chequeos
mutaciones_referencias.py    10/10    3 chequeos
```

Las tres comparten `_verificacion/_arnes.py`, escrito una sola vez en lugar de
copiar por cuarta, quinta y sexta vez las ~40 líneas de `_copia`/`_falla_por`
que llevan las once suites viejas (el §8-E ya las tenía anotadas). **Las once
viejas no se tocan**: reescribir la red mientras se la usa para tender el resto
es exactamente el refactor sin cobertura que el §5 desaconseja.

Cada suite **declara en `CHEQUEOS` qué cubre**, y la declaración no es gratis:
el censo exige que la suite mencione la etiqueta que ese chequeo imprime, así
que no se puede apuntar cobertura que no se ejerce. Dos de las mutaciones del
censo comprueban justamente eso.

### Lo que salió al hacerlo, y no estaba en este plan

1. **Dos de los treinta chequeos no pueden fallar.** `validar_costes_sin_fuente`
   y `validar_referencias` solo llenan `warn`: nunca añaden nada a `err`. Un
   conjuro citado por una especie y ausente de `hechizos.json` —integridad
   referencial rota— sale como un ⚠ entre otros treinta y `validar.py` termina
   con «0 errores». No se ha cambiado: convertirlos en error es una decisión
   sobre qué bloquea la base, no una prueba. Lo que sí se prueba es la garantía
   que **sí** dan —que el aviso aparezca— y queda anotado para decidirlo.

2. **Las tablas `COMPLETO`/`MEDIO` de `validar.py` no tienen cita.** Son los
   espacios de conjuro contra los que se contrasta la progresión de 7 clases, y
   el SRD de Open5e solo publica los del Brujo. No es el defecto del §2 —las
   copias sí se comparan— pero sí una autoridad sin página por encima de una
   base citada. Declarado como pendiente del bloque A2.

3. **562 registros del SRD 5.2 estructurado sin contrastar**, entre ellos los
   **255 rasgos de clase y subclase** de `classes24/feat`. Es el bloque H.

4. **`verificar_documentos.py` llevaba su propia lista a mano** de qué suites
   ejecutar: diez nombres literales. Se habría quedado corta hoy mismo —las
   tres suites nuevas habrían nacido con sus cifras sin vigilar—. Ahora se
   descubren por patrón, con `mutaciones_foundry.py` declarada aparte por
   lenta. Y lanzaba **todas a la vez**: con trece suites en cuatro núcleos eso
   no va más rápido, va mucho más lento. Una por núcleo, y las catorce en
   verde tardan **4,5 minutos**, igual que las diez de antes.

5. **Tres mutaciones propias mal apuntadas**, encontradas por dar «no
   detectada»: una tocaba una de las **dos** llamadas a `paquete("feats24",
   "feat")`, otra mutaba una clase sin segunda fuente con la que contrastar, y
   otra cambiaba un campo que el chequeo no lee. En los tres casos el fallo era
   de la mutación, no del chequeo — el mismo tropiezo que `mutaciones_efectos.py`
   ya tenía documentado. Cada una lleva ahora escrito por qué está donde está.

6. **`validar_referencias` encabeza su línea con ⚠**, no con ✅, en cuanto
   tiene un aviso. El arnés buscaba solo ✅/❌ y la línea entera desaparecía:
   las mutaciones salían «no detectadas» cuando lo que fallaba era el arnés.

7. **El censo se pilló a sí mismo una promesa autosatisfecha.** La garantía de
   que una suite no puede apuntarse cobertura que no ejerce era «que mencione
   la etiqueta del chequeo». Pero apuntarse `validar_idiomas` **mete la cadena
   «idiomas» en el fichero**, así que la promesa se validaba a sí misma. Lo
   destapó `mutaciones_censo.py` con esa mutación exacta y se arregló contrastando la etiqueta contra el fichero **sin la
   propia declaración**. Es la razón de que un verificador nuevo nazca con su
   suite el mismo día y no «cuando haya tiempo».

8. **El censo tardaba 10,4 s y ahora tarda 0,6 s.** Casi todo era parsear con
   `yaml.safe_load` los 1372 ficheros del SRD estructurado para leerles un solo
   campo. Se lee la línea `type:` en su lugar; mismo resultado, y su prueba por
   mutación pasó de ~50 minutos a menos de 4.

---

## 12. Resultado — bloque A2, ejecutado el 2026-09-02

Las cuatro listas que el §2 dejaba abiertas, cerradas con el mismo gesto de
siempre: **la cobertura se descubre**. Ninguna se arregló «a mano»: en las
cuatro, la lista desaparece y la sustituye algo que se lee de la base.

### Caso 5 · `validar._PROMESAS` → las promesas viven junto a su variable

`_PROMESAS` era una tupla de dos entradas en `validar.py` para **tres**
variables calculables: `velocidad` entró en el motor el 2026-08-30 y nadie
añadió sus frases, así que durante tres días un rasgo podía prometer velocidad
en su prosa y no declararla sin que saltara nada.

Ahora cada variable `calculada` de `reglas/efectos.yaml` trae sus `promesas`, y
**declarar una sin ellas es un error**: no se puede añadir una cuarta y
olvidarse. Al enchufarlo, la base se puso en rojo con **nueve rasgos** que
prometían velocidad y no la declaraban. Los nueve, resueltos:

| Cómo | Cuántos | Cuáles |
|---|---|---|
| `add` permanente | 3 | `Veloz` (+3 m), `Don de la velocidad` (+9 m), `Aura de celeridad` (+3 m) |
| `add` + condición nueva `sin_armadura_pesada` | 2 | `Movimiento rápido` (Bárbaro N5), `Errante` (Explorador N6) |
| `conditional` (cierto, citado, y a propósito sin calcular) | 5 | `Atacante a la carga`, `Emboscador pavoroso`, `Paradigma elemental`, `Forma grande`, y la mitad de `Aura de celeridad` que afecta a los aliados |

La condición `sin_armadura_pesada` **no es `sin_armadura` con otro nombre**: el
Bárbaro conserva su +3 m con armadura ligera o media y solo lo pierde con la
pesada, mientras que el Monje lo pierde con cualquiera. Sin ella los dos
rasgos habrían tenido que mentir eligiendo la condición que no es. Medido:
Bárbaro N4 → 9 m, N5 → 12 m, N5 con cota de malla → 9 m.

`efectos` pasa de **8 a 18**.

### Caso 6 · `verificar_chequeos.FUENTES` → los ficheros se descubren

De las seis rutas que declaraba, **tres no aportaban ni una rama**:
`verificar_srd.py`, `cobertura.py` y `verificar_documentos.py` no tienen
ninguna función `validar_*`/`verificar_*` —sus chequeos viven en `main()`—, así
que estaban en la lista, se leían enteras y no se auditaba nada de ellas.
**Estar en la lista parecía cobertura y no lo era**, que es peor que faltar.

Ahora los ficheros se descubren (`*.py` de la raíz) y se audita también `main`.
El ámbito nuevo sacó a la luz **9 ramas silenciosas** que nadie miraba; la
línea base pasa de 54 a 64 una vez, contadas y visibles, y desde ahí solo puede
bajar. Un módulo sin ninguna función auditable no es un fallo —`materiales.py`
y `prerrequisitos.py` son bibliotecas— pero tiene que estar **declarado**, y lo
exige la fila nueva del censo.

De paso se arregló un falso positivo de la propia herramienta: `verificar_srd.py`
no acumula en `err`, imprime «⚠ …» directamente, y eso **es** avisar. Un `print`
con marca de aviso ya cuenta; uno sin ella, no.

### Caso 7 · `verificar_srd.MAPA` → la autoridad de los espacios se cita

Lo primero que salió al medirlo es que **el caso no era el que decía**: `MAPA`
cubre *todas* las columnas que el SRD de Open5e publica de las 12 clases, no se
le escapa ninguna. El hueco real estaba debajo: `COMPLETO` y `MEDIO`, dos
tablas literales en `validar.py` **sin cita de página**, eran la autoridad
contra la que se contrastaban las progresiones de 7 clases. Si el manual y el
literal discrepaban, ganaba el literal.

- `COMPLETO` **ya estaba en la base, citada**: es la tabla de espacios de
  multiclase de `reglas/generacion_personaje.yaml` (pdf 47 = libro 45). Se lee.
  Es el arreglo de `_TABLA_COSTE` otra vez.
- `MEDIO` **no se copia ni se inventa: se deriva** con la regla que el propio
  manual imprime al lado —«la mitad, redondeando arriba»—. Comprobado nivel a
  nivel que reproduce el literal en los 20.
- Y el chequeo que comparaba esa tabla contra `COMPLETO` habría quedado
  **tautológico**: se sustituyó por lo que ese contraste no ve (20 filas, en
  orden, sin columnas ausentes). Un chequeo tautológico en verde es peor que
  ninguno: parece que cubre algo.

### Caso 8 · `verificar_foundry.MODULOS` → medido, y es el bloque H

No se cierra aquí, y no por falta de ganas: son **562 registros** de nueve
categorías del SRD 5.2 estructurado que ningún módulo pide, y escribirlos es
trabajo de su propio bloque. Lo que sí cambia es que ya no es «categorías sin
contrastar»: son nueve pares (carpeta, `type`) contados, cada uno declarado con
lo que costaría y lo que daría.

### Y un bug que solo podía salir teniendo el dato

`conditional` existía en el vocabulario desde el Plan 17 y **ninguna ficha
había alcanzado nunca un rasgo que lo usara**. Al declarar los cinco de
velocidad, el motor reventó: `calcular_de_ficha()` resolvía las fórmulas antes
de filtrar los `conditional`, que a propósito no tienen fórmula. Es el modo de
fallo del proyecto en pequeño —lo escrito era correcto, y lo que faltaba no lo
miraba nadie— y lo destapó tener por fin el dato, no leer el código.

### Cifras al cerrar

```
censo.py               697 unidades · 0 sin declarar · 515 pendientes
validar.py             0 errores · 18 efectos (eran 8)
verificar_chequeos     64 silenciosas · 4 TOLERADO · línea base 64
mutaciones_aritmetica  32/32     mutaciones_contenido  49/49
mutaciones_censo       18/18     mutaciones_efectos    26/26
17/17 fichas · barrido 240/240
```
