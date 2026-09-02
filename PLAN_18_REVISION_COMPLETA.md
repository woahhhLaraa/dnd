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

## 2. El defecto de fondo, ya con siete casos

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

## 4. Deuda de código menor (real, pero no urgente)

| Qué | Dónde | Nota |
|---|---|---|
| `cargar()` duplicada | `calculo.py` y `cobertura.py` | **No son idénticas**: la de cobertura devuelve `None` si falta el fichero, la de calculo hace `sys.exit`. Unificar cambiaría comportamiento; hacerlo a propósito o dejarlo documentado |
| `_es_marcador()` duplicada | `subir_nivel.py` y `validar.py` | Misma lógica en dos sitios |
| Tercer lector | `verificar_foundry.cargar_yaml` | Tres formas de leer un YAML en el repo |
| `_TIRADAS_VALIDAS` | `validar.py` | Vocabulario cerrado de reglas que vive **solo en Python**, mientras el de efectos vive en `reglas/efectos.yaml` con cita. Inconsistencia de dónde reside la autoridad |

---

## 5. Cómo aplicar lo que hacen los otros repos (lo que queda)

Ya adoptado: el modelo de efectos y el agregador de DiceCloud (Fase 14), su
operación `conditional` (C4), el `ScaleValue` de Foundry como `columna`, y su
taxonomía de *advancement* en `/subir-nivel` (Fase 16).

Lo que falta por adoptar, y para qué sirve cada cosa:

- **La «Foundry Note» → C2.** Foundry automatiza 76 de 332 rasgos (23 %) y
  **declara la frontera dentro del dato**: 380 registros dicen qué no está
  automatizado. Aquí la frontera es el silencio. Es lo que convierte «no lo
  hemos hecho» en «lo miramos y no toca».
- **`ModifyItem` → el caso `Maestro en armaduras medias`.** «Sumas **3 (en vez
  de 2)** a tu CA por Destreza» no es `add` ni `set` sobre `ca`: **cambia un
  parámetro de la fórmula de la armadura**. El modelo actual no lo expresa.
  Foundry tiene un tipo para exactamente esto.
- **El grafo de dependencias de DiceCloud.** Detecta ciclos y los registra
  como error explícito en vez de colgarse. `orden_de_calculo()` ya hace parte;
  conviene comprobar que un ciclo real falla ruidosamente.

Lo que **NO** se copia, y conviene tenerlo escrito: **Foundry no tiene tests**
(`package.json`: `build`, `lint`, `watch`). Sustituyen verificación por
cientos de miles de jugadores. Este proyecto tiene una usuaria, así que sus
3666 valores contrastados y sus 149 mutaciones son el sustituto correcto.

---

## 6. Plan de acción, en orden

Cada paso dice si **necesita el manual**, porque eso decide si se puede hacer
hoy o no.

### Bloque A — cerrar el patrón (sin manual, ~1 día)

| # | Qué | Por qué va aquí |
|---|---|---|
| **A1** | `_PROMESAS` derivada de las variables `calculada` del vocabulario | **Es la lista que tenía que haber avisado de los 10 huecos de velocidad.** Arreglarla ANTES de rellenar hace que el chequeo diga cuándo has terminado, en vez de fiarte de una lista escrita a mano hoy |
| **A2** | `verificar_chequeos.FUENTES` audita las 6 que declara | Hoy 3 quedan fuera porque su lógica vive en `main()` |
| **A3** | `verificar_srd.MAPA`: toda columna mapeada o declarada no contrastable | Cierra el hueco de `pb`, que es el número del que cuelga la CD |
| **A4** | `verificar_foundry.MODULOS`, igual | Último de los ocho |

### Bloque B — declarar los 21 efectos (sin manual, ~1 día)

Medido: solo hay **3 variables calculables** (`ca`, `pg_max`, `velocidad`), así
que el hueco funcional son **21 rasgos**, no 528. Su texto ya está transcrito
y citado; el método es el de C3 —estructurar la prosa y exigir ida y vuelta—
y solo hace falta el manual si la transcripción resulta ambigua.

| # | Qué | Cuántos |
|---|---|---|
| **B1** | Los inequívocos: `Veloz` (+3 m), `Defensa` (+1 CA con armadura), `Don de la fortaleza` (+40 PG) | ~4 |
| **B2** | Condición nueva «sin armadura pesada» + `Movimiento rápido` y `Errante` | 2 |
| **B3** | Los situacionales, como `conditional` | ~14 |
| **B4** | Decidir `Maestro en armaduras medias` (§5, `ModifyItem`) | 1 |

### Bloque C — cerrar la puerta (sin manual, ~medio día)

| # | Qué |
|---|---|
| **C1** | `efectos:` obligatorio en todo rasgo, con `no_automatizado` como respuesta legítima. **Va al final, no al principio**: activarlo antes de B dejaría la base en rojo durante todo el relleno y no se distinguiría una rotura nueva de la deuda conocida |

### Bloque D — higiene (sin manual, ~medio día)

`requirements.txt` (PyYAML no está declarado), versión de Python declarada
(un `SyntaxError` de 3.12 tumbó cuatro herramientas y nadie se enteró), y
decidir qué hacer con los tres lectores y las dos funciones duplicadas.

### Bloque E — lo único que necesita el manual

Los casos de B en los que el texto transcrito resulte ambiguo, y la revisión
de descripciones de conjuro (residuo medido: ~11 %), que ya has decidido
llevar tú contra el manual.

---

## 7. Criterio de cierre

1. Ninguna de las ocho listas del §2 sigue escrita a mano.
2. Los 21 candidatos de efectos, a cero, contados por un chequeo que **deriva
   su lista del vocabulario**.
3. Quitar `efectos:` de cualquier rasgo hace fallar a `validar.py`.
4. En todo momento: `validar.py` 0 errores, 17/17 fichas, barrido 240/240,
   contrastes en 646 + 3020, y las mutaciones en verde.

---

## 8. Lo que este plan no promete

No promete que no aparezca un noveno caso del patrón. Promete que **la forma
del defecto ya está nombrada, tiene regla propia (la 6 de `CONTINUAR.md`) y se
reconoce a simple vista**: si un módulo lleva dentro una lista de lo que mira,
y esa lista duplica algo que vive en la base, es el mismo error otra vez.

Los cuatro casos cerrados se encontraron mirando; los cuatro abiertos están
localizados y medidos. Eso es lo que separa esto de un espiral.
