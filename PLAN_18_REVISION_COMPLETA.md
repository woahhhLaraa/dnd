# PLAN 18 — Revisión completa del código y plan de acción

> Escrito el **2026-08-31**, después de aplicar el Plan 17 (C1, C3, C4). Todas
> las cifras están **medidas hoy** con los comandos que se citan al lado.
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
| 5 | `validar._PROMESAS` | **`velocidad`** — los 10 huecos | ⬜ abierta |
| 6 | `verificar_chequeos.FUENTES` | audita 3 de las 6 que declara | ⬜ abierta |
| 7 | `verificar_srd.MAPA` | `pb`, `forma_salvaje`, `mov_sin_armadura_m` | ⬜ abierta |
| 8 | `verificar_foundry.MODULOS` | categorías sin contrastar | ⬜ abierta |

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
chequeos `validar_*` en validar.py : 30
  con prueba por mutación          : 11   (37 %)
  SIN prueba por mutación          : 19
```

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

### Bloque A — el censo (sin manual, ~1 día) · **VA PRIMERO**

`censo.py` con las seis filas de la tabla del §7, y su informe. **Antes que
arreglar las cuatro listas abiertas**, porque si se arreglan primero se arreglan
«las que encontró Claude»; con el censo se arreglan «las que hay», y se sabe
cuándo se ha terminado.

### Bloque B — cobertura de mutación de los 19 (sin manual, ~2 días)

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

### Bloque F — refactor

**Solo si después de A-E sigue pareciendo necesario.** La medición del §5 dice
que probablemente no lo sea.

### Bloque G — lo único que necesita el manual

Los casos del bloque C cuyo texto transcrito resulte ambiguo, y la revisión de
descripciones de conjuro (residuo medido ~11 %), que la usuaria lleva contra el
manual por decisión propia.

## 9. Criterio de cierre

1. `censo.py` existe y su número es 0, o lo que no es 0 está declarado con su
   motivo.
2. Los 30 chequeos `validar_*` tienen prueba por mutación, o exención declarada.
3. Los 21 candidatos a efecto, a cero.
4. Quitar `efectos:` de cualquier rasgo hace fallar a `validar.py`.
5. En todo momento: `validar.py` 0 errores, 17/17 fichas, barrido 240/240,
   contrastes en 646 + 3020, mutaciones en verde.

## 10. Lo que este plan no promete

No promete que no aparezca un noveno caso del patrón. Promete que **el día que
aparezca lo dirá el censo**, en vez de esperar a que alguien lea el código con
ojos frescos. Esa es la diferencia entre una auditoría y un espiral: no que no
haya defectos, sino que el repo sepa contar los que le quedan.
