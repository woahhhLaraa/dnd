# PLAN 19 — del estado de hoy al producto completo

> Escrito el **2026-09-02**, después de cerrar los bloques A, B, A2, C y D del
> `PLAN_18`. Todas las cifras están **medidas**, no estimadas, y los comandos
> que las producen están al final.
>
> Este documento **sustituye al `PLAN_18` como plan de trabajo vigente**. El 18
> se queda como registro de lo que se hizo y de por qué: sus §11 a §14 son el
> resultado de cada bloque, con lo que el censo destapó y no estaba previsto.
>
> **Dos decisiones del usuario, tomadas hoy y ya dentro del plan:**
> la multiclase se **cierra ahora y se automatiza después**, y las conversiones
> a pies **se borran del texto**.

---

## 1. Contexto

**Qué es el producto.** Una base de reglas de D&D 2024 en castellano, transcrita
del manual por lectura visual, con la que un LLM orquestador crea y sube de
nivel personajes **sin usar nada de su conocimiento previo**. Toda autoridad
vive en la base, citada por página.

**Dónde estamos.** El `PLAN_18` tenía siete bloques; hoy están hechos **A, B,
A2, C y D**. Eso cerró el defecto que el repo arrastraba —las listas de
cobertura escritas a mano, ocho casos— y puso la red que faltaba:

```
censo.py               697 unidades · 0 sin declarar · 492 pendientes
validar.py             0 errores · 25 efectos (eran 7)
chequeos validar_*     30/30 con prueba por mutación (eran 11/30)
contraste externo      646 (SRD) + 3.020 (Foundry) = 3.666 valores
fichas                 17/17 · barrido 12 clases × 20 niveles = 240/240
```

**Qué falta, y es lo que ordena este plan.** Con la red puesta, lo que queda ya
no es infraestructura: es **superficie sin verificar** y **producto sin cubrir**.

**Dos decisiones tomadas hoy** por el usuario, y están en el plan:
1. La multiclase: **cerrar el agujero ahora, automatizar después**.
2. Las conversiones a pies: **borrarlas del texto**.

---

## 2. Lo que falta para el producto completo, medido

| Hueco | Tamaño | ¿Bloquea el producto? |
|---|---|---|
| ~~El verificador **aprueba fichas multiclase sin comprobarlas**~~ | eran **4**, no 3 | ✅ cerrado (fase 1) |
| Residuo de error en descripciones de conjuro | **~11 %** (IC 3,1-26,1) | 🔴 sí: es lo que la base entrega |
| ~~Conversiones a pies que el manual no imprime~~ | 543 borradas de 399 registros | ✅ cerrado (fase 2) |
| Registros del SRD 5.2 que nadie contrasta | **562**, de ellos 255 rasgos de clase | 🟠 superficie sin verificar |
| Rasgos que no dicen si tocan una variable | **480** (enumerados, solo bajan) | 🟠 frontera |
| Multiclase automatizada | reglas ya transcritas, sin ejecutar | 🔴 sí: personajes que no se pueden montar |
| ~~Dos chequeos que **no pueden fallar**~~ | los dos estaban a cero | ✅ cerrado (fase 1) |
| ~~Reproducibilidad~~ | `requirements.txt` + `.python-version`, y los 33 módulos se compilan en cada pasada | ✅ cerrado (fase 1) |

---

## 3. Fase 1 · Que un «✅» signifique lo que dice — ✅ **HECHA (2026-09-02)**

**Qué logra:** hoy hay tres sitios donde el sistema aprueba lo que no ha
comprobado. Esta fase los cierra. Es la más barata y la que más engaño quita.

**1a · La multiclase deja de aprobarse sin mirar.**
`verificar_personaje.py` degrada tres chequeos a aviso cuando hay más de una
clase — `verificar_calculado()` (229), `verificar_mejoras()` (400) y
`verificar_conjuros()` (468)— y la ficha imprime «✅ FICHA VERIFICADA — 0
problemas». Los tres avisos pasan a **error**: una ficha multiclase se rechaza
con el motivo y el puntero a `reglas/generacion_personaje.yaml → multiclase`.
Es el tercer caso confirmado de la amenaza nº 3 del `FODA.md`.

**1b · Los dos chequeos que solo avisan.**
`validar_costes_sin_fuente()` y `validar_referencias()` nunca llenan `err`. Una
referencia rota entre una especie y `hechizos.json` sale como ⚠ y `validar.py`
termina con «0 errores». Pasan a error, con la deuda conocida declarada si
queda alguna.

**1c · Higiene (bloque E).** `requirements.txt` (PyYAML no está declarado),
versión de Python declarada y comprobada al arrancar —un `SyntaxError` de 3.12
tumbó cuatro herramientas y nadie se enteró—, y las ~50 líneas duplicadas:
`cargar()` en `calculo.py` y `cobertura.py` (**no son idénticas**: una hace
`sys.exit`, la otra devuelve `None`), `cargar_yaml()` en `verificar_foundry.py`
y `_es_marcador()` en `validar.py` y `subir_nivel.py`.

**Se comprueba:** una ficha multiclase de prueba **se rechaza**; mutaciones
nuevas en `mutaciones_referencias.py` que pasan de modo `aviso` a modo `error`;
`validar.py`, `censo.py` y las 14 suites en verde.

---

## 4. Fase 2 · Quitar del texto lo que el manual no imprime — ✅ **HECHA (2026-09-02)**

**Qué logra:** `fidelidad: literal` deja de convivir con texto que la base
añadió. Es la debilidad nº 2 del `FODA.md`, y la decisión ya está tomada.

**Qué se toca:** 543 conversiones en 298 conjuros de `hechizos.json`, con la
forma `6 m / 20 pies`, repartidas en `descripcion` (321) y `alcance.texto`
(222). Se borra el `/ N pies` y queda lo que el manual imprime: `6 m`.
Nueve lectores independientes sobre 23 páginas no vieron **ni una** unidad
imperial.

**Y el chequeo cambia de sentido, que es la mitad importante:**
`validar_conversiones()` comprueba hoy que estén *bien calculadas*. Pasa a
comprobar que **no haya ninguna**, para que no vuelvan a entrar. La cifra que
`CONTINUAR.md` promete (543) y que `verificar_documentos.py` vigila baja a 0, y
`_meta._conversiones_nota` de `hechizos.json` pasa a registrar el borrado en vez
de declarar el añadido.

**Se comprueba:** `validar.py` 0 errores con la nueva semántica; una mutación
que reintroduce una conversión **debe** saltar; `verificar_documentos.py` en
verde con la cifra nueva.

---

## 5. Fase 3 · Contrastar los 562 registros del SRD que nadie mira (bloque H)

**Qué logra:** es la fase con más error latente por unidad de trabajo, porque
contrasta contra una fuente independiente texto que hoy **no mira nadie**. Sube
la superficie externa de 3.666 a ~4.200 valores, y sobre todo mete en el
contraste los **255 rasgos de clase y subclase** de `classes24`.

El censo midió que 9 de los 17 pares (carpeta, `type`) de
`_verificacion/foundry_srd52/` no los pide ningún módulo de
`verificar_foundry.py`. Por orden de valor:

| Par | Registros | Qué cierra |
|---|---|---|
| `classes24/feat` | 255 | los rasgos de clase y subclase — **y produce la «Foundry Note»** |
| `classes24/class` | 12 | los advancements: dado de golpe, competencias y los `ScaleValue` por nivel → cierra `columna:druida.forma_salvaje` y `columna:monje.mov_sin_armadura_m`, las dos únicas columnas sin fuente externa |
| `origins24/feat` | 36 | las dotes de **origen**, que viven fuera de `feats24` y por eso `verificar_dotes` no las pedía |
| `equipment24/consumable`, `container`, `loot` | 234 | munición, contenedores y materiales |
| `classes24/subclass`, `classes24/weapon`, `spells24/consumable`, `tables24` | 61 | decidir alcance antes de escribir |

**Cómo:** módulos nuevos en `verificar_foundry.py` siguiendo el patrón que ya
existe — emparejar por clave independiente del idioma y **deducir** los
vocabularios exigiendo biyección, nunca traducir. Cada módulo entra en
`MODULOS`, y el censo deja de contarlos como pendientes.

**Se comprueba:** `verificar_foundry.py` con las categorías nuevas y 0
discrepancias (o discrepancias reales, que son hallazgos); `censo.py` con la
fila de datos externos a 0 pendientes; `mutaciones_foundry.py` ampliada.

---

## 6. Fase 4 · Los 480 rasgos, con la «Foundry Note» como guía

**Qué logra:** la frontera explícita entre «no lo hemos mirado» y «lo miramos y
no toca», que es lo que el bloque D dejó a medias **a propósito**: no se
fabricaron 480 motivos sin leer los rasgos.

**Por qué esta fase depende de la 3, y por qué eso la hace barata:** Foundry
declara en el dato qué automatiza y qué no —**380 registros** lo dicen—. Con
`classes24` ya contrastado, la mayoría de los 480 se resuelve **cruzando con lo
que Foundry ya decidió**, y a mano solo quedan los que discrepan o los que
Foundry no cubre. Eso convierte «leer 480 rasgos» en «leer los que nadie ha
mirado todavía».

**Qué se toca:** `no_automatizado:` con su motivo en cada rasgo resuelto, y
`_verificacion/rasgos_sin_declarar.json` encogiendo. La lista **solo puede
bajar** y un rasgo nuevo sin declarar ya hace fallar a `validar.py`.

**Se comprueba:** `censo.py` con la fila de rasgos bajando; `validar.py` exige
motivo en cada `no_automatizado`; `mutaciones_efectos.py` (familia PUERTA) sigue
en verde.

---

## 7. Fase 5 · El residuo del 11 % en las descripciones de conjuro

**Qué logra:** que el texto que la base entrega sea fiable. **Es el defecto de
fondo del producto**: todo lo demás verifica estructura y cifras; esto es la
prosa que el jugador lee.

**El dato que manda:** la muestra aleatoria post-corrección del 2026-08-29 dio
**4 defectos en 36 conjuros = 11,1 %** (IC 3,1-26,1), y los cuatro estaban en
conjuros **ya auditados** —dos habían pasado por una oleada ese mismo día—. La
lección ya está registrada: **auditar no deja limpio**.

**Es la fase que necesita el manual**, y la lleva la usuaria por decisión
propia. Método ya probado en el repo: lectura de la página, doble lectura
independiente cuando hay discrepancia, y el hallazgo se descarta **registrado
como descartado** si la cita no dice lo que se creía.

**Cuidado con el modo de fallo conocido:** un informe de agente en blanco no
prueba nada —las oleadas 1-2 declararon auditar el `resumen` y dieron 0 defectos
en 131 conjuros cuando la oleada 3 midió 5,8 %—. Cada tanda cierra con una
**muestra aleatoria nueva** que mida el residuo, no con la declaración de quien
auditó.

**Se comprueba:** una muestra aleatoria post-tanda, con semilla fija y
reproducible, como `MUESTRA_POST.json`.

---

## 8. Fase 6 · Automatizar la multiclase

**Qué logra:** que el producto cubra los personajes que hoy rechaza (tras la
fase 1) y que hasta hoy aprobaba sin mirar.

**Está más cerca de lo que parece.** Las reglas **ya están transcritas y
citadas** en `reglas/generacion_personaje.yaml → multiclase`: requisitos por
clase, PG con el dado de cada clase, bonificador por competencia, competencias
al multiclasear, clase de armadura, ataque adicional y la tabla de espacios de
conjuro (pdf 47 = libro 45, ya usada como autoridad desde el bloque A2). Y el
motor de efectos **ya itera sobre varias clases** con su `nivel_clase` propio.

**Qué falta:** ejecutarlas. `subir_nivel.py:144` sale con «la multiclase todavía
no se sube automáticamente»; los tres chequeos de la fase 1 pasan de rechazar a
comprobar de verdad; y `/personaje` y `/subir-nivel` ganan el paso de elección
de clase con su prerrequisito.

**Se comprueba:** fichas multiclase reales en `personajes/` (p. ej. clérigo
5/paladín 5, que es el ejemplo que el propio manual usa para los dados de
golpe), su suite de mutación, y el barrido ampliado.

---

## 9. Rutina, no fase · Estrés con agentes

**Qué logra:** lo único que encuentra lo que ningún chequeo escrito por la misma
mano encuentra. `PLAN_ESTRES.md` lo dejó montado y **no se ha vuelto a correr
desde el 2026-08-30**, con la base muy cambiada desde entonces.

Cuatro agentes construyen personajes leyendo la base —el tramposo sutil, el
tramposo estructural, **el exótico legal** y el abogado del manual—, con sobre
cerrado escrito antes, sin leer el código del verificador y sin ejecutarlo. Las
dos casillas rojas (hueco y falso positivo) valen igual.

**Se corre después de cada fase grande**, no una vez.

---

## 10. Fase 7 · Refactor — solo si después sigue pareciendo necesario

La medición del `PLAN_18` §5 sigue vigente: mediana de 35 líneas por función en
`validar.py`, y **ninguno de los ocho defectos del §2 lo causó la estructura**.
Lo que bloqueaba el refactor —11 de 30 chequeos sin red— ya no bloquea: son
30/30. Así que ahora es una opción real, y probablemente innecesaria.

---

## 11. Orden recomendado y por qué

```
1 · el «✅» que miente        barato, y quita engaño          ~1 día
2 · las conversiones          decisión tomada, mecánico       ~1 día
3 · el SRD sin contrastar     más error latente por esfuerzo  ~2-3 días
4 · los 480 rasgos            barata SOLO después de la 3     ~1-2 días
6 · multiclase                producto sin cubrir             ~2-3 días
5 · el residuo del 11 %       la larga, con el manual         en paralelo
```

La 5 va **en paralelo** desde el principio: es la única que necesita el manual,
la lleva la usuaria, y no bloquea a ninguna otra.

## 12. Criterio de producto completo

1. Un personaje legal cualquiera —**monoclase o multiclase**, 1→20— se crea y se
   sube consultando solo la base, y el verificador comprueba **todo** lo que
   aprueba: ningún chequeo se degrada a aviso.
2. `censo.py` a **0 pendientes**, no solo a 0 sin declarar.
3. Toda superficie con fuente externa disponible, contrastada: los 562 registros
   dentro.
4. El texto que la base entrega, con residuo medido y **bajando**, con la
   muestra que lo demuestre.
5. En todo momento: `validar.py` 0 errores, las suites de mutación en verde, y
   `verificar_documentos.py` diciendo que los documentos no mienten.

## 13. Verificación de cada fase

```bash
python3 validar.py && python3 censo.py && python3 verificar_chequeos.py
python3 verificar_srd.py && python3 verificar_foundry.py && python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 generar_ficha.py --barrido --exhaustivo
python3 verificar_documentos.py        # corre las 14 suites de mutación (~5 min)
```

Y la regla que no cambia: **todo hueco que se cierre lleva su chequeo y su
prueba por mutación**; todo falso positivo se corrige afinando el chequeo, no
relajándolo, y se queda como control negativo.


---

## 14. Resultado — fase 1, ejecutada el 2026-09-02

### Eran cuatro, no tres

La medición que ordenó este plan decía tres chequeos degradados. **Eran
cuatro.** El que faltaba, `verificar_dotes_y_subclase()`, es además el peor:
se saltaba justamente los tres huecos que el estrés con agentes había
destapado —la subclase de otra clase, el prerrequisito de dote sin comprobar—,
así que **una ficha multiclase esquivaba en silencio los chequeos escritos para
cazar lo que se colaba en silencio**. Apareció al escribir el arreglo, no al
planificarlo: la cuarta rama no usaba la misma redacción que las otras tres.

Los cuatro comparten ahora una puerta, `una_sola_clase()`, que registra el
motivo **una sola vez**: repetir el mismo error por cada chequeo que se salta
entierra el motivo bajo su propio ruido.

### Los dos chequeos que no podían fallar, promovidos sin dejar deuda

`validar_costes_sin_fuente` y `validar_referencias` pasan a error. Se pudo
hacer limpio porque **los dos estaban a cero**: los 52 conjuros con material
fuera del SRD llevan su `_coste_verificado`, y los 18 conjuros que las especies
citan resuelven.

**Y salió un bug de rótulo debajo.** `main()` imprimía `⚠` para
`validar_referencias` aunque hubiera errores —daba igual mientras el chequeo no
pudiera tener ninguno—, así que al promoverlo su prueba por mutación daba «no
detectada» cuando lo que fallaba era el rótulo. El marcador dice ahora la
verdad: ❌ si hay errores, ⚠ si solo hay avisos, ✅ si no hay nada.

### `_es_marcador` no era duplicación: era el defecto nº 4 otra vez

El plan lo listaba como «~50 líneas duplicadas». Al mirarlo, las dos copias de
`_es_marcador` **ya habían divergido**: `validar.py` normalizaba con `.strip()`
y exigía «Subclase de » con espacio final; `subir_nivel.py` no normalizaba y
aceptaba «Subclase de» sin él. Un rasgo llamado «Subclase deluxe» era marcador
para una y rasgo para la otra.

Y el vocabulario **vive en la base**, en `reglas/subida_de_nivel.yaml →
marcadores`. O sea que no era duplicación entre dos módulos: era el defecto nº 4
del §2 del `PLAN_18` (`_TABLA_COSTE`) por tercera vez —autoridad que vive en la
base, copiada en Python, sin nadie comparando las copias—. Se lee.

### La reproducibilidad, cerrada por donde de verdad falló

El `SyntaxError` del 2026-08-31 no ocurrió por falta de un número en un
fichero: ocurrió porque **nadie ejecutaba `verificar_foundry.py`**, y cuatro
herramientas estuvieron muertas sin que saltara nada. Así que además de
declarar (`requirements.txt` con la única dependencia real, `.python-version`
con el suelo), `verificar_documentos.py` **compila los 33 módulos en cada
pasada**. Cuesta un segundo y cierra el fallo que de verdad ocurrió.

**Su límite, dicho:** comprueba la sintaxis contra el intérprete que corre. NO
caza código válido aquí e inválido en la versión mínima —justo el caso
original, porque el analizador de f-strings cambió en 3.12 y
`ast.feature_version` no lo rebaja—. Para eso hace falta ejecutar en la versión
mínima, y eso es CI, no un chequeo.

### Y un falso positivo que el propio cierre creó

Al sustituir los cuatro avisos por `if not una_sola_clase(...): return`,
`verificar_chequeos.py` marcó las ramas nuevas como **silenciosas**: miraba el
cuerpo de la rama, y quien habla ahí es la **condición**. Ahora mira las dos.
Es una mejora real de la herramienta, no un parche: cualquier rama cuya
condición sea la llamada que reporta estaba mal contada.

### Cifras al cerrar

```
validar.py             0 errores · 25 efectos
censo.py               697 unidades · 0 sin declarar · 492 pendientes
verificar_documentos   33 módulos compilan · Python 3.11 ≥ 3.11 · 1 dependencia
mutaciones_nivel20     18/18 (eran 15: entra la familia MULTICLASE)
mutaciones_referencias 10/10, ahora en modo ERROR y no aviso
17/17 fichas · barrido 240/240 · una ficha multiclase se RECHAZA
```


---

## 15. Resultado — fase 2, ejecutada el 2026-09-02

### Lo borrado

543 equivalencias en **399 registros de 298 conjuros**: 321 en `descripcion` y
222 en `alcance.texto`. El texto quedó como la página lo imprime —«6 m»,
«3 m»— y el chequeo cambió de sentido: de «bien calculadas» a **«ninguna en
texto citable»**, para que no vuelvan a entrar.

### Lo que NO se borró, y no estaba en el plan

`alcance` no era solo texto: guarda `metros`, `pies` y `casillas` como **campos
estructurados**, y `verificar_foundry.py` contrasta `alcance.pies` contra el
SRD **número contra número**. Borrarlos habría dejado 218 alcances sin fuente
externa.

Así que la línea no es «conversiones sí / conversiones no», sino **cita frente
a dato derivado**: fuera del texto que la base presenta como del manual, dentro
como campo declarado. Y su aritmética se sigue comprobando —la segunda mitad
del chequeo—, porque si no, vaciar el texto habría **abierto un hueco donde
antes había un chequeo**.

### Un defecto que la conversión tapaba

*Cofre oculto de Leomund* decía «0,34 m / 1 pies³», con el cúbico **solo en la
unidad añadida**. Quitar el añadido dejaba «0,34 m» —metros lineales para un
volumen—. Queda como «0,34 m³», que es lo que dice la propia frase dos palabras
después: «(90 cm por 60 cm por 60 cm)» son 0,324 m³. La deducción sale del mismo
registro, no de fuera, y queda anotada como **pendiente de confirmar contra la
página** en la tanda de la fase 5.

Y un segundo caso que ninguna regex general cazaba: *Sanctasanctórum privado de
Mordenkainen* convertía un RANGO —«de 1,5 a 30 m / 5 a 100 pies»—, con otro
rango entre la barra y la unidad.

### Y dos mutaciones mías que estaban mal, no el chequeo

Al rehacer la suite —el cambio de sentido convierte sus controles negativos en
detecciones: **una conversión correcta también sobra**— escribí dos controles
falsos:

- uno ponía `metros: 36.0` en *Bola de fuego*, que son 45 m: el falso positivo
  hablaba de la mutación, no del chequeo;
- otro llamaba «redondeo legítimo» a 119 pies por 120. **No lo es**: la
  tolerancia es absoluta precisamente porque «el menor defecto real desvía 1
  entero». Medido al arreglarlo: **los 436 pares derivados de la base son
  exactos**, desviación 0,0000, porque con metros múltiplos de 1,5 el factor de
  juego no deja resto. El control honesto es un valor no múltiplo —0,34 m → «1»
  pie, exacto 1,13—, que la tolerancia sí debe admitir.

### Cifras al cerrar

```
validar.py             0 errores · conversiones (436 derivados · 0 coladas)
verificar_foundry      3020 valores · 0 discrepancias (sigue usando alcance.pies)
mutaciones_conversiones 16/16 (eran 13: entra la mitad DERIVADOS)
17/17 fichas · barrido 240/240 · censo 697 · 0 sin declarar
```

---

## 16. Resultado — fase 3, primera mitad, ejecutada el 2026-09-03

La fase 3 pedía contrastar los 562 registros del SRD que nadie miraba. Esta
primera mitad cierra **las dos rebanadas más grandes de `classes24`** y, de
paso, arregla un defecto del propio censo que las hacía invisibles.

### 16.1 · Las clases (`classes24/class`, 12 registros)

`verificar_clases()` contrasta dado de golpe, tipo de lanzador, oro inicial y
—lo que de verdad faltaba— **las escalas por nivel** contra nuestra tabla de
progresión: **536 valores**. Cierra `columna:druida.forma_salvaje` y
`columna:monje.mov_sin_armadura_m`, que eran las dos únicas columnas sin fuente
externa, y el par `externo:classes24/class`.

Encontró **una discrepancia real**: Foundry modela los puntos de concentración
del monje como una escala lineal `valor = nivel`, con 1 en el nivel 1; nuestra
tabla pone 0. Manda la nuestra, y la evidencia es interna y citada: el rasgo
que los concede, «Concentración de monje», es de **nivel 2** (pdf 151 = libro
149) y su propio texto transcrito dice «2 en nivel 2 […] hasta 20 en nivel 20».
Un monje de nivel 1 no tiene el rasgo. **La página no se ha releído**, y así
queda dicho en la propia declaración.

### 16.2 · Los rasgos de clase (`classes24/*/class-features/`, 159 registros)

`verificar_rasgos_clase()` contrasta **135 valores**: nivel a nivel, qué
niveles de cada clase conceden rasgo y cuántos.

**Lo que NO hace, y se midió antes de decidirlo:** no empareja los nombres. De
los 146 rasgos con nivel, la unicidad solo fuerza 75 parejas, y de esas solo
dos términos ingleses aparecen más de una vez —«Epic Boon» y «Channel
Divinity»—. Una biyección que no exige nada es un diccionario escrito a mano
con otro nombre, así que se contrasta la **estructura**, que sí tiene dos
fuentes independientes.

**Diecisiete niveles cuentan distinto**, y cada uno lleva su declaración con el
par exacto que se examinó —si cualquiera de los dos lados cambia, la venda se
cae—. Trece son granularidad del pack (Pericia concedida dos veces, `Indómito`
con usos crecientes, `Mystic Arcanum` por nivel de conjuro, rasgos que el pack
publica sin fecha). **Cuatro son discrepancias de verdad**, todas del mismo
tipo —el pack fecha un rasgo en un nivel y nosotros en otro— y todas
**pendientes de leer la página**:

| Rasgo | El pack | Nosotros |
|---|---|---|
| `Deflect Energy` / Desviar energía (monje) | N3 | N13 |
| `Relentless Hunter` / Cazador persistente (explorador) | N14 | N13 |
| `Cunning Strike` / Golpe astuto (pícaro) | N2 | N5 |
| `Self-Restoration` / Autorrestablecimiento (monje) | no lo trae | N10 |

### 16.3 · El defecto del censo que esto destapó

El censo contaba el dato externo por pares `(carpeta, type)`. Pero
`classes24/feat` mete en el mismo saco **cuatro cosas con cuatro contrastes
distintos**: rasgos de clase (159), rasgos de subclase (58), metamagias (10) e
invocaciones (28). Un módulo que contrastara solo los primeros habría cerrado
el par entero, dando por miradas 96 unidades que nadie mira. Es el defecto nº 4
del §2 del `PLAN_18` con otro disfraz.

Arreglado: la unidad del censo es ahora la terna **(carpeta, rebanada, `type`)**
—la rebanada es la subcarpeta con que el pack se agrupa él solo, no una
elección nuestra—, y `paquete()` acepta `sub=` para que una llamada declare qué
rebanada promete. Una llamada sin `sub=` sigue prometiendo el `type` entero, así
que nada de lo que ya estaba en verde cambió de estado. El censo pasa de **697
a 867 unidades**.

Los comodines del manifiesto admiten ahora `*` en cualquier posición, no solo
al final, porque desde el cambio la parte que varía suele estar en medio
(`externo:equipment24/*/container`).

### 16.4 · La otra mitad de `classes24` sigue bloqueada, y por qué

Los 58 rasgos de subclase y las 12 subclases **no se pueden contrastar todavía**:
el SRD publica una subclase por clase y nosotros cuatro, y hay que saber cuál
es cuál. Se midió si la identidad era deducible sin traducir:

- por **vector de niveles**: no discrimina, hay empates en casi todas las clases;
- por **huella numérica del texto** —la misma técnica que empareja armas—:
  acierta en **11 de 12**, pero en paladín deja un **empate a cuatro**.

Un empate no es una deducción, así que queda declarado como pendiente con la
medición dentro. Metamagias e invocaciones están bloqueadas por otra cosa: la
base las trae como bloque de texto dentro de un rasgo, no como registros con
nombre, y hay que decidir la forma antes de escribir el módulo.

### 16.5 · Un hallazgo que no toca a esta fase

El bárbaro tiene **dos rasgos distintos con el mismo nombre** —«Golpe brutal
mejorado» en N13 y en N17—, y el pack los distingue con un «(2)». La
duplicación es fiel al manual, pero significa que **el nombre no es clave**: un
orquestador que elija rasgos por nombre no puede distinguirlos. No se ha
tocado; queda anotado aquí porque el chequeo que lo detecte va en `validar.py`,
con su prueba por mutación, y eso es trabajo propio.

### Cifras al cerrar

```
validar.py             0 errores
verificar_srd           646 valores · 0 discrepancias
verificar_foundry      3691 valores · 0 discrepancias  (eran 3020)
externo total          4337 valores
censo.py                867 unidades · 0 sin declarar · 594 pendientes
mutaciones_foundry      42/42 (eran 29)
mutaciones_censo        20/20 (eran 18)
verificar_chequeos      65 silenciosas · 12 TOLERADO · línea base 64
17/17 fichas · barrido 240/240 · verificar_documentos en verde
```
