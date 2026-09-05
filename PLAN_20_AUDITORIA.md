# Plan de auditoría — la autoridad que no se puede citar ni contrastar

## Contexto

**De dónde sale.** La ronda 2 de estrés (2026-09-05) encontró 10 defectos en
`verificar_personaje.py`. Al clasificarlos **antes** de arreglarlos, solo 5
eran parches puntuales genuinos: los otros 5 eran la misma familia repetida.
Se cerraron con cuatro mecanismos en vez de diez parches, y la usuaria hizo la
pregunta que ordena este plan:

> *«quién sabe qué tanto del código fue hecho a base de parches puntuales […]
> como "el espiral", donde hacíamos verificación tras verificación cuando la
> solución era una búsqueda»*

**El espiral tiene diagnóstico escrito** (`PLAN_17` §2): cinco veces una lista
escrita a mano se quedó corta, y cada vez la respuesta fue otro verificador.
`censo.py` lo cerró para la cobertura y nació la **regla inviolable 6**.

**Lo que esta auditoría midió:** el censo está en verde —867 unidades, 0 sin
declarar— **y el defecto sigue vivo, dentro del propio censo**.

**Alcance elegido:** inventariar, cerrar, añadir el mecanismo que impida el
sexto, **y** una ronda de estrés sobre los módulos de cálculo. Preocupan por
igual las reglas cableadas sin cita y que la aritmética no tenga fuente
independiente.

---

## Los cinco hallazgos que ordenan el plan (todos verificados a mano)

**1 · El 72 % del motor de efectos es decoración.** Medido hoy: de los **25
efectos declarados, solo 7 los sostiene alguna ficha**. Los otros 18 —entre
ellos `Duro`, el efecto que motivó el Plan 17, y el único `modifica_tope` de la
base— se pueden corromper sin que nada se rompa. `verificar_calculado` ya lo
dice de *una* variable: *«para que el efecto sea carga y no decoración: si no
lo sostuviera ninguna ficha, corromperlo no rompería nada»*.

**2 · Ninguna suite muta el motor.** Las 15 suites mutan la base o las tablas
de los verificadores. Un error aritmético en `calculo.py` o `efectos.py` **no
lo detecta nada**. Y la ficha se escribe con `calculo.py` y se verifica con
`calculo.py`: un error produce una ficha coherente y equivocada.

**3 · El censo hereda un punto ciego y su suite lo blinda.**
`efectos._DIRECTORIOS_DE_REGLA` enumera 5 directorios y le falta `equipo`; y
`censo.py:111` hace `for d in E._DIRECTORIOS_DE_REGLA:` — **el censo toma su
universo de esa tupla**. `equipo/armaduras.yaml` **es fuente de efectos**
(`efectos.py:495` fabrica la CA de 13 armaduras, el −3 m por Fuerza y el
escudo) y no la censa nadie. Y `mutaciones_censo.py:177` tiene un **control
negativo que exige que el censo NO se entere** de un `.yaml` nuevo en `equipo/`.
El guardián de «la cobertura se descubre» tiene el defecto que persigue, con un
test que lo fija como correcto.

**4 · El censo se puede inflar en silencio.** `Fila.__init__` interseca
`alcanzadas` con el universo pero **no interseca `declaradas`**, y `muertas`
solo recorre el manifiesto del censo. Un `excluidos:` podrido en
`reglas/fuentes_de_efectos.yaml` sube el recuento sin avisar.

**5 · 34 constantes de dominio cableadas**, y una lista sin validar. Lo peor
son los **fallos silenciosos latentes**: `efectos.py:245` cablea las 6
condiciones de equipo que el YAML declara — una séptima haría que su efecto
**nunca aplicara, sin ruido**; `efectos.py:341` codifica `orden_de_agregacion`
como bucles mientras su docstring dice que lo lee del YAML **y no lo lee**.
Además `validar.py:622` valida 4 de los 5 ficheros de `equipo/`: **los 5
registros de `municion.yaml` no los valida nada**.

---

## Fase 0 · Que el censo no se pueda inflar — ✅ HECHA (2026-09-05)

> `Fila.declaradas` y `Fila.deuda` se intersecan con el universo, y lo
> que queda fuera sale como declaración muerta **con el nombre de su
> manifiesto delante**, porque el sitio donde ir a borrarla no es el
> mismo. Dos mutaciones nuevas: `mutaciones_censo` 20/20 → **22/22**.
>
> Medido al escribirlas: renombrar un `excluidos:` existente **no** es
> este defecto —deja un fichero sin clasificar y `origenes()` ya falla
> en cerrado por ese camino—. El caso que nadie cazaba es la
> declaración que apunta a lo que no existe.

**Logra:** cierra el único camino por el que las fases siguientes —que escriben
en manifiestos de fila— podrían pasar en verde mintiendo. Va primero por
dependencia dura.

- `censo.py` · `Fila.__init__`: intersecar `declaradas` y `deuda` con el
  universo, y guardar aparte lo que no case.
- `censo.py` · `main()`: las declaraciones de manifiesto propio fuera del
  universo entran en `muertas`, nombrando su manifiesto.
- `mutaciones_censo.py`: `m_excluido_muerto` y `m_deuda_muerta` en `DEBEN`.

**Verificación:** `censo.py` sigue dando 867 · 0 sin declarar (control: hoy no
hay muertas). La suite sube en 2.

---

## Fase 1 · Dar fuente independiente a la aritmética

**Por qué NO se escribe un segundo calculador:** dos implementaciones de la
misma regla divergen y nadie las compara — `_CA_SIN_ARMADURA` con más pasos. El
precedente bueno del repo es otro: `valor_establecido_pg()` lee la tabla
*«nunca calculado como (caras/2)+1: esa coincidencia es lo que
`validar_puntos_golpe()` usa para CONTRASTAR las dos transcripciones»*. La
independencia viene de **fuera del código**.

**1.1 · `_verificacion/mutaciones_motor.py`** — ✅ **HECHA (2026-09-05)**, y su
medición es peor que la estimación del plan:

> **Solo 4 de 11 mutaciones del motor las caza alguna ficha.** Siete trozos de
> motor no los protege nada:
>
> | Hueco | Qué significa |
> |---|---|
> | `aplica()` deja de mirar `requiere` | **todo efecto condicionado se aplicaría siempre** — la CA sin armadura del Bárbaro sumaría llevando cota de malla, y las 18 fichas siguen en verde |
> | desaparecen los bucles `min`, `max` y `set` | tres de las seis operaciones de la agregación se pueden borrar enteras |
> | el bucle `mul` divide en vez de multiplicar | |
> | se quita el `math.floor` final | |
> | el mínimo de 1 de los PG por nivel pasa a 0 | y la base lo trae estructurado sin que nadie lo lea |
>
> Las 4 que sí se cazan: el bucle `add`, los PG del nivel 1 con Constitución, y
> las condiciones `con_armadura`/`con_escudo` invertidas.
>
> La deuda va **enumerada** en `_verificacion/motor_sin_carga.json`, patrón de
> `chequeos_silenciosos.json`: solo puede bajar, se salda **escribiendo fichas
> que ejerciten esa aritmética** —no tocando la lista— y un hueco nuevo hace
> fallar la suite. Esa lista es el encargo literal del mandato «el calculista».

El diseño original:
Muta **el motor**, no la base, y exige que alguna ficha con su `calculado`
congelado falle: `+=`→`-=` en el bucle `add`; borrar el bucle `min`/`max`;
quitar el `math.floor`; `max(1,…)`→`max(0,…)` en `pg_de_subida`; invertir
`not con_arm` en `estado_de_equipo`; saltar los efectos con `requiere`.
**Una mutación que ninguna ficha caza es un hueco de cobertura aritmética, y la
suite lo nombra** — esa lista dirige 1.4.

**1.2 · `_origen` en el bloque `calculado`** — ✅ **HECHA (2026-09-05)**.
El muro es real y está probado: `--calcular` no tiene forma de escribir
`agente-manual`, y las cuatro mutaciones nuevas cazan la firma sin informe, el
informe inexistente, el método inventado y el `_origen` ausente. De propina
saltó un hueco que no estaba en el plan: **un campo de más en `calculado` que
el verificador no recalcula pasaba en silencio** — un número inventado con
aspecto de calculado. Ahora falla. `mutaciones_nivel20` 48/48 → **52/52**.

El diseño original: Hace visible si un número lo
escribió el motor o una lectura independiente:
```yaml
calculado:
  _origen: {metodo: motor, informe: null, fecha: "2026-09-05"}
```
Regla dura: `calcular_bloque()` escribe **siempre** `metodo: motor` y **nunca
puede firmar `agente-manual`**. Si el escritor puede firmar como oráculo, no
hay oráculo. `agente-manual` exige `informe:` a un fichero que exista.
Toca `personajes/_ESQUEMA.md` (de donde `verificar_claves` ya lee las claves),
`verificar_personaje.py` y las 18 fichas.

**1.3 · Fila 8 del censo — «efectos con carga»** — ✅ **HECHA (2026-09-05)**.
Nació como estaba diseñada: **25 unidades · 0 alcanzadas · 25 en deuda
enumerada**. Cero alcanzadas aunque 7 efectos ya se apliquen, porque
«alcanzada» exige que la ficha que lo aplica tenga `_origen: agente-manual` —
una ficha escrita por el motor no sostiene nada: pinchar el motor la movería a
ella también. Censo 867 → **892**.

De propina, otro cableado del mismo día: el informe del censo tenía el texto de
la deuda enumerada **escrito a mano hablando de rasgos**, y al heredar la fila
nueva decía «25 rasgos» de unos efectos. Ahora el texto lo pone la fila; el
informe no sabe de qué habla cada una, la fila sí.

*(Es la fila 8, no la 9: el plan la numeró suponiendo que la de constantes
llegaría antes. Llega después.)*

El diseño original: Convierte el 7/25 en una
cuenta que solo puede subir y dice cuál falta.
- Universo: descubierto con `efectos.efectos_declarados()`, por
  `(archivo, rasgo, objetivo, op)`.
- **Alcanzada:** alguna ficha lo aplica **y** esa ficha tiene
  `_origen.metodo: agente-manual`. Una ficha escrita por el motor no sostiene
  nada: pinchar el motor la movería a ella también.
- Deuda enumerada en `_verificacion/efectos_sin_carga.json`, patrón de
  `rasgos_sin_declarar.json`: solo puede bajar.

Nace **25 unidades · 0 alcanzadas · 25 en deuda**: en verde y sin perdonar nada.

**1.4 · Ronda 3 de estrés, mandato E · «el calculista»** — escrito en
`PLAN_ESTRES.md` el 2026-09-05, primera tanda en marcha.

**Y una corrección al plan, medida al escribirlo:** de los 7 huecos de
`motor_sin_carga.json`, **solo 3 los puede saldar el calculista**. La base
declara ocho operaciones (`base, add, mul, min, max, set, conditional,
modifica_tope`) y **solo usa cuatro**: no existe ni un efecto `mul`, `min`,
`max` o `set` en toda la base. Esos cuatro bucles no los puede ejercitar
ninguna ficha por mucho que se escriba — son caminos de código muertos
respecto al dato de hoy, y eso es **vocabulario sin consumidor (fase 4)**, no
cobertura aritmética. `motor_sin_carga.json` los separa en dos grupos con esa
explicación, porque meterlos en el mismo saco le encargaría al calculista algo
que no puede hacer.

El diseño original: Es **la segunda
transcripción**, y sin ella la fila 9 no sube de 0. Cuarto mandato nuevo en
`PLAN_ESTRES.md`, con las cuatro reglas del método intactas:

> Recibe los datos crudos de una ficha (especie, clases, características,
> equipo, dotes, `pg_por_nivel`) y **no** su bloque `calculado`. Calcula
> `pg_max`, `ca`, `velocidad`, `cd_conjuros` y `bonif_ataque_conjuros` **a
> mano**, escribiendo cada paso y citando la página. Prohibido leer
> `calculo.py`, `efectos.py` y `reglas/efectos.yaml`.

Coinciden → la ficha pasa a `_origen: agente-manual` y **pincha en la fila 9
todos los efectos que aplica**. Divergen → hallazgo, y la derivación escrita
dice de quién es el error. **Se dirige por la fila 9**, empezando por los 18
medidos y priorizando los que 1.1 señale como no cazados por nadie.

**Primera tanda (dos calculistas) — hecha, y con dos resultados.** Los dos
derivaron a mano `pg_max`, `ca` y `velocidad` de dos fichas distintas y **los
seis valores coinciden con el motor**: primer contraste externo real de la
aritmética. Y los dos pararon en el mismo sitio, con la misma frase: ningún
fichero de la base definía la fórmula de `cd_conjuros` ni de
`bonif_ataque_conjuros`. Vivía cableada en `calculo.py`, con su cita **en un
comentario de Python**. Dos agentes independientes redescubrieron por el camino
contrario el hallazgo del inventario.

**Y un defecto del método, que declararon ellos solos:** los datos crudos y el
bloque `calculado` viven en el MISMO fichero, así que leer la ficha es ver los
números. La ceguera se pedía y no se podía cumplir. **Esas dos derivaciones NO
cuentan como segunda transcripción** —una derivación anclada al número que ya
se vio no es independiente, por honesta que sea—, así que las fichas **no** se
promovieron a `_origen: agente-manual` y la fila 8 sigue en 0/25. Contarlas
habría sido el verde que miente. Arreglado con
`verificar_personaje.py --datos-crudos <ficha>`: la ceguera no se pide, se
REPARTE. 🔴 **Queda relanzar la tanda a ciegas** (los dos agentes murieron por
límite de sesión).

---

## Fase 1.5 · El `KeyError` que la propia fase 1 introdujo — ✅ HECHA (2026-09-05)

`validar_conjuros_cd()` terminaba comprobando que `calculo` leyera el `base` de
la base. Con el bloque `cd_salvacion` borrado,
`_regla_de_conjuros()["cd_salvacion"]["base"]` lanzaba `KeyError` y `validar.py`
**moría sin imprimir la etiqueta del chequeo**: la mutación `cd_bloque_borrado`
contaba como no detectada, **35/36**.

**Por qué tiene apartado propio y no un arreglo callado.** Es la misma familia
que el hueco nº 10 de la ronda 2 —un chequeo que explota en vez de hablar—
reaparecida en código escrito el mismo día que se cerró aquella, y por la misma
mano. Que el patrón vuelva tan rápido es el dato: **no basta con arreglar
instancias**.

- `calculo._base_de_conjuros()`: faltar un dato de la base es un mensaje que
  dice QUÉ falta, nunca una traza.
- `validar_conjuros_cd()`: no llama a `calculo` si la estructura ya vino mal, y
  contrasta las DOS fórmulas en vez de solo la CD.

**Medido:** `mutaciones_aritmetica` **36/36** · `validar.py` 0 errores.

---

## Fase 1.6 · El guardián del silencio dejaba crecer su propia deuda — ✅ HECHA (2026-09-05)

**No estaba en el plan: salió de verificar el verde de la fase 1.5.**
`verificar_chequeos.py` imprimía «✅ ninguna rama silenciosa nueva» con **67
ramas silenciosas y una línea base de 64**. Su huella era
`fichero::funcion::cuerpo`, y el cuerpo de casi todas es la palabra `continue`:
las 67 colapsaban en **41 huellas**. Una rama silenciosa nueva que fuera gemela
textual de otra ya declarada entraba sin ruido — y tres lo hicieron.

Es **el hallazgo nº 4 de este mismo plan** (el censo se puede inflar en
silencio) en otro guardián, con una diferencia que lo hace peor: en el censo la
deuda crecía; aquí crecía **mientras el chequeo decía que no**. Y el sexto
guardián sin guardián: ninguna suite mutaba `verificar_chequeos.py`.

- **La huella lleva la condición**, no solo el cuerpo: 67 → **65 huellas
  distintas**. Las gemelas que quedan —la misma guarda escrita dos veces en la
  misma función— llevan un ordinal **por orden de línea, no por número de
  línea**, para que editar por encima no invalide el fichero.
- **Pagadas las dos que se pudieron atribuir:** `verificar_conjuros`
  descartaba en silencio una entrada de conjuro cuyo `ref` no nombra nada.
  Ahora una avisa y la otra se declara.
- **La tercera se deja en deuda enumerada, a propósito:** un `tipo:` mal
  escrito saca una variable del chequeo de `promesas` sin ruido, porque nada
  comprueba que `tipo` esté en un vocabulario cerrado. **Eso es la fase 4.**
  Anotarla como tolerada habría exigido nombrar quién la cubre, y hoy no la
  cubre nadie.
- **`_verificacion/mutaciones_silencios.py`** (nuevo, 6/6): la primera
  mutación es exactamente el caso que antes pasaba callado, y está comprobado
  contra el árbol anterior al arreglo — con la huella vieja da **68
  silenciosas, línea base 64 y «✅ ninguna nueva»**.
- La migración de la línea base va con su `_migracion:` dentro del JSON: las
  huellas nuevas no se pueden comparar una a una con las viejas, así que lo que
  se conserva es **la cuenta, y la cuenta baja** (67 − 2 = 65).

**Lección, que es la de la usuaria:** el arreglo no fue anotar las tres ramas
—eso habría sido el parche puntual—, fue que la huella dejara de mentir.

---

## Fase 2 · El punto ciego de `equipo/`, sin rojo a medias

El orden es contraintuitivo y hay que respetarlo: `origenes()` **lanza** en
cuanto `equipo` entra con ficheros sin clasificar, y lo importan cuatro
módulos. Declarar los 5 ficheros *antes* tampoco vale: tras la fase 0 saldrían
como declaraciones muertas.

**2.1 · Primero el universo se descubre, con `equipo` como deuda declarada.**
`_DIRECTORIOS_DE_REGLA` deja de ser tupla y pasa a `directorios_de_regla()`:
los directorios de primer nivel con `.yaml`, menos los declarados «no son
regla» (`personajes/`, `_verificacion/`, con motivo en
`reglas/fuentes_de_efectos.yaml`). Un directorio nuevo sin declarar es error.
`equipo` entra en el universo **como `pendiente`**: fila 1 de 49 a 54, verde, y
el agujero deja de ser invisible.

**2.2 · Categoría nueva `derivadas`.** La taxonomía binaria de hoy no puede
decir la verdad sobre `armaduras.yaml`: `excluidos` sería mentira (el motor
fabrica sus efectos) y `fuentes` no encaja (ningún registro lleva `efectos:`).

```yaml
derivadas:
  - patron: "equipo/armaduras.yaml"
    deriva: "efectos_de_equipo"     # resuelto por getattr; si no existe, ERROR
    campos:
      - {campo: ca,     objetivo: ca,        op: "base|add"}
      - {campo: fuerza, objetivo: velocidad, op: add}
```
Y los dientes: `efectos.registros_de(rel)` devuelve por registro
`(uid, nombre, alcanzado, motivo)`, y `censo.fila_rasgos` lo llama en vez de
descender ella misma — así la fila 7 no necesita saber la forma de
`armaduras.yaml`. Clasificación: `armaduras.yaml` → `derivadas`; `armas`,
`aventureros`, `herramientas` → `excluidos` con motivo; **`municion.yaml` →
`pendientes`**, porque no lo valida nada.

**2.3 · El control negativo se invierte, no se borra.** Codifica una propiedad
real (no todo `.yaml` es regla), así que:
- `n_fichero_fuera_de_regla` pasa a `DEBEN` como
  `u_fichero_de_equipo_sin_clasificar`, conservando su comentario histórico y
  la línea de por qué cambió de lista.
- Sustituto en `NO_DEBEN`: `n_yaml_en_directorio_no_de_regla` crea
  `personajes/prueba.yaml` y exige que el censo **no** falle.
- Nueva en `DEBEN`: `u_directorio_nuevo_sin_declarar` crea `objetos/x.yaml`.
  Es **la mutación que habría cazado el defecto original**.

**2.4 · Pagar `municion.yaml`** — commit aparte, para separar «declarar» de
«pagar». `validar_equipo` deriva la lista del directorio en vez de la tupla de
`validar.py:622`.

**2.5 · Anclar la cifra del censo en `verificar_documentos.py`.** Hoy
`CONTINUAR.md` y `FODA.md` prometen «867 unidades» y **nadie lo contrasta** —
el mismo modo de fallo que ese script existe para cazar.

**Cifras predichas, a remedir:** fila 1 49→54, fila 7 519→532, total 867→885.

---

## Fase 3 · Fila 8 del censo — «constantes de dominio en Python»

La cabecera del censo rechazó esta fila con un argumento correcto: detectarlas
por la **forma** del literal es una heurística con falsos positivos. Pero no se
aplica a una prueba de **pertenencia**:

> Un literal es constante de dominio si sus cadenas están, **todas**, en el
> vocabulario de **una** colección de la base — descubierta: claves de cada
> mapa, `nombre:` de cada lista, ficheros de cada directorio, valores por ruta
> de clave.

**Medido:** con umbral ≥3 cadenas salen **34 unidades** y **cero** falsos
positivos de los que la cabecera nombra (`_A_METROS`, los nodos AST, los mapas
de traducción se caen solos: la mitad de sus cadenas está en inglés). Con ≥2
salen 75, y 41 son navegación estructural. **El umbral se declara, no se
esconde.**

La prueba de que el criterio no es una racionalización: corrido a ciegas,
imprime las tres copias de la lista de ficheros de `equipo/` —una corta— y
`_DIRECTORIOS_DE_REGLA` como subconjunto. Redescubre solos los hallazgos 3 y 5.

| Clase | Hoy | Exigencia |
|---|---|---|
| copia exacta | 11 | se **deriva** en tiempo de ejecución |
| subconjunto | 21 | se declara con motivo **y enumerando lo que deja fuera** — si la colección crece, la declaración queda muerta → rojo |
| disperso | 2 | se declara con motivo |

**Universo:** cualquier nodo literal `Dict/Set/List/Tuple`, también dentro de
funciones (si solo se miraran las constantes de módulo, mover el literal dentro
de una función lo haría desaparecer). **La identidad es la huella normalizada
del conjunto, no la línea**, para que editar encima no invalide el fichero.

**Nace en verde sin perdonar nada:** `_verificacion/constantes_de_dominio.json`
enumera las 34; solo puede bajar; una huella nueva hace fallar al censo.
**Alcanzada = la constante ya no existe.** Es la única fila que debe tender a
cero.

**Grupos de cierre** (no una a una): listas de ficheros de `equipo/` y `dotes/`
(6) → `glob`; grupos de armadura (4) → accesor; nombres de las 12 clases (2) →
derivar de `clases/*.yaml`; las 6 características y sus abreviaturas (8) → **el
emparejamiento no está en la base**, se añade `reglas/caracteristicas.yaml` con
su página; las 18 habilidades (1) → `reglas/habilidades.yaml`; la página
cableada de `armaduras.yaml` (1) → leer su `fuente`, **que hoy discrepa**.

---

## Fase 4 · Vocabularios cerrados sin consumidor exhaustivo

Cierra los tres casos que **no son constantes** y por eso escapan de la fila 8.
El censo comprueba hoy *base → código*; falta *código → base*.

1. **`condiciones`** — cada una declara *cómo se decide*, y `estado_de_equipo()`
   se construye recorriendo `vocab["condiciones"]`. Una condición sin regla de
   decisión = error.
2. **`orden_de_agregacion`** — pasa a lista de operaciones; `agregar()` itera
   sobre ella. Una operación que no esté ni en el orden ni en «no se agregan» =
   error.
3. **`fuentes_de_valor`** — nadie lo lee; `_num()` lo cablea. Igual.

**Verificación:** tres mutaciones nuevas en `mutaciones_efectos.py`, de la
familia «se añade un término al vocabulario y nadie lo consume». **Hoy ninguna
de las tres salta.**

---

## Lo que NO hay que hacer

1. **No añadir `equipo` a `_DIRECTORIOS_DE_REGLA` a secas.** `origenes()` lanza
   y caen cuatro módulos a la vez. El escalón 2.1 existe para eso.
2. **No declarar los 5 ficheros como `fuentes`.** Metería 208 registros en la
   fila 7 exigiéndoles `efectos:`; 195 no son rasgos. *«Un manifiesto que nadie
   lee es la novena lista a mano.»*
3. **No declarar `armaduras.yaml` como `excluido`.** Mentira documentada, peor
   que el silencio.
4. **No borrar el control negativo.** Se invierte y se le da sustituto.
5. **No escribir un segundo calculador.** Dos motores divergen y nadie los
   compara.
6. **No dejar que `--calcular` firme `agente-manual`.**
7. **No bajar la fila 8 a literales de 2 cadenas** (34 → 75, con 41 de ruido).
8. **No arreglar las 34 constantes antes de tener la fila.** Se arreglarían las
   que encontró alguien leyendo el código — lo que la regla 6 prohíbe.
9. **Ningún chequeo nuevo como aviso `⚠`** (criterio `PLAN_19` §12.1).
10. **No dar por buena ninguna cifra de este documento sin remedirla.**

---

## Orden y dependencias

```
Fase 0  censo no inflable    ✅ hecha
Fase 1  aritmética           ✅ 1.1 mutaciones_motor  ✅ 1.2 _origen  ✅ 1.3 fila 8
                             ✅ 1.4 mandato escrito y primera tanda
                                🔴 tanda A CIEGAS por relanzar
                             ✅ 1.5 el KeyError propio
                             ✅ 1.6 la huella del guardián del silencio
Fase 2  equipo/              2.1 directorios → 2.2 derivadas → 2.3 control → 2.4 municion → 2.5 ancla
Fase 3  fila 9              primero la fila con las 34; luego cada grupo, viéndola bajar
Fase 4  vocabularios        necesita que la fila 9 haya declarado los `for clave in (...)`
```

**Nota de numeración:** la fila de efectos con carga entró como **fila 8** (el
plan la llamaba 9 suponiendo que la de constantes llegaría antes; llega
después). La fase 3 creará la **fila 9**.

**Lo siguiente, por orden:** relanzar la tanda a ciegas del calculista (1.4), y
después la **fase 2** (`equipo/`), que es la primera sin empezar.

Las fases **1 y 2 son independientes** y pueden ir en paralelo (ficheros
disjuntos), salvo 1.3, que quiere los efectos derivados de 2.2: si van en
paralelo nace con 25 y sube al aterrizar 2.2.

**Criterio de cierre:** el censo pasa de 7 a 9 filas y de 867 a ~919 unidades
con 0 sin declarar; la fila 8 tiende a cero; la fila 9 llega a 25/25 vía
estrés; `mutaciones_motor.py` en N/N con al menos una ficha cazando cada
mutación; y la regla 6 gana su corolario: **ningún literal del dominio sin
derivar o sin declarar, y ningún número de la ficha sin una segunda
transcripción.**

## Verificación de cada fase

```bash
python3 validar.py && python3 censo.py && python3 verificar_chequeos.py
python3 verificar_srd.py && python3 verificar_foundry.py && python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 generar_ficha.py --barrido --exhaustivo
python3 _verificacion/mutaciones_motor.py       # nueva, fase 1.1
python3 _verificacion/mutaciones_aritmetica.py # 36/36 desde la fase 1.5
python3 _verificacion/mutaciones_silencios.py  # nueva, fase 1.6
python3 verificar_documentos.py                # corre las suites (~5 min)
```

Y la regla que no cambia: **todo hueco que se cierre lleva su chequeo y su
prueba por mutación**; todo falso positivo se corrige afinando, no relajando, y
se queda como control negativo.

### Ficheros críticos

- `censo.py` — filas 8 y 9, `Fila.declaradas`, universo de directorios
- `efectos.py` — `directorios_de_regla()`, `registros_de()`, `estado_de_equipo()`, `agregar()`
- `reglas/fuentes_de_efectos.yaml` — `directorios:`, `derivadas:`, los 5 de `equipo/`
- `_verificacion/mutaciones_censo.py` — control invertido + 5 mutaciones nuevas
- `verificar_personaje.py` — `_origen` del `calculado` y el muro en `calcular_bloque()`
- `_verificacion/mutaciones_motor.py`, `constantes_de_dominio.json`, `efectos_sin_carga.json` — nuevos
