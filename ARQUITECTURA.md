# ARQUITECTURA — cómo está construido esto, y por qué así

> **Este documento está ANCLADO.** `verificar_documentos.py` contrasta las dos
> listas de abajo —los módulos de la raíz y las filas del censo— contra el
> disco, **en las dos direcciones**: si aparece un módulo que aquí no está,
> falla; si aquí hay uno que ya no existe, falla también.
>
> No es un adorno del documento: es la condición para que exista. Un
> documento de arquitectura escrito a mano **es** el error que este
> repositorio persigue —una lista que se queda vieja sin que nadie se
> entere—, y el proyecto ya tropezó con eso cinco veces antes de escribirlo
> como regla. Si esta página no se pudiera contrastar, no debería estar.

---

## 1. El error de siempre, nombrado

`PLAN_17` §2 lo llamó **el espiral**, y lo midió: **cinco veces** un módulo
llevaba dentro la lista de los ficheros, campos o columnas que miraba; cinco
veces la lista se quedó corta; y cinco veces la respuesta fue **escribir otro
verificador**. Cada verificador nuevo traía su propia lista, así que traía el
defecto otra vez.

Su forma general —la que hay que reconocer, porque cambia de disfraz—:

> **Algo se declara en un sitio y se comprueba en otro, y nadie comprueba que
> los dos sigan hablando de lo mismo.**

Las caras que ha tenido en este repositorio, todas medidas:

| disfraz | dónde apareció |
|---|---|
| una tupla de ficheros dentro de un módulo | `FUENTES`, `MAPA`, la tupla de `buscar.py` |
| una convención de nombres | `_auditable`: mover una rama de función la escondía |
| una huella mal elegida | el cuerpo sin su condición: 67 ramas colapsaban en 41 |
| una frase como identidad | reescribir una descripción parecía una regresión |
| una cifra en un documento | «las 17 suites» con 18 en el disco |
| una lista de claves a conservar | `_migracion_plan21` se habría borrado en la primera poda |
| un verificador que se comprueba a sí mismo | los seis guardianes del `PLAN_20` |

**Ninguna se cerró con disciplina.** Todas se cerraron poniendo un mecanismo
que las hace fallar cuando vuelven a pasar.

---

## 2. Las cuatro decisiones que sostienen todo

### 2.1 · La base es la autoridad; el código no la duplica

Toda regla sale de la página del manual, transcrita, citada, y vive en YAML o
JSON. El código **lee**; no sabe reglas. Un literal de Python cuyas cadenas
están todas en el vocabulario de una colección de la base es autoridad
duplicada, y por eso el censo tiene una fila que **solo puede tender a cero**:
se salda borrando el literal, no declarándolo.

Corolario que costó caro: `calculo.ca()` cableaba el `10` de la CA sin armadura
mientras la base lo declaraba y `efectos.py` lo leía. Dos implementaciones y
nadie comparándolas.

### 2.2 · La cobertura se descubre, nunca se escribe a mano

Regla inviolable 6. Ningún módulo lleva dentro la lista de lo que mira: se
descubre por `glob`, por AST o por el vocabulario de la base, y se contrasta
contra un manifiesto que declara **también las exclusiones, con su motivo**.

Una convención de nombres es una lista escrita a mano disfrazada, y cuenta
igual: por eso `verificar_chequeos.py` mira **todas** las funciones y no las
que empiezan por `validar_`.

### 2.3 · Lo que no se puede cerrar hoy va ENUMERADO, no bajo un comodín

Un comodín cuenta el crecimiento y lo imprime, pero **no lo impide**. Una lista
enumerada convierte «se ve crecer» en «no puede crecer». Las cinco líneas base
del proyecto las lleva `deuda.py`, con cuatro propiedades que se aprendieron
una a una, a golpes:

1. **podar** — lo saldado sale, así la deuda baja de verdad en disco;
2. **distinguir lo nuevo de lo perdido** — una medición nueva no es una
   regresión, y confundirlas miente en las dos direcciones;
3. **guardar el elenco** — todo lo medido, no solo lo que falló; sin él, lo
   anterior es indecidible;
4. **declarar su identidad** — con qué se compara una entrada con la de ayer,
   escrito DENTRO del fichero. Las tres veces que se eligió mal, el guardián
   mintió.

Y una política por fichero: si una entrada nunca medida es aceptable
(`cerrada=False`) o es roja igual (`cerrada=True`).

### 2.4 · Todo chequeo se prueba por mutación, en las dos direcciones

Se corrompe una copia desechable y se exige que algo salte. **La mitad de cada
suite son controles negativos**: datos raros pero legítimos que NO deben hacer
saltar nada. No es simetría estética — la primera versión del chequeo de dados
se disparaba con su propia documentación.

Dos corolarios que se aprendieron fallando:

- **Una mutación que solo cambia el comportamiento en una situación que no
  ocurre, no cambia nada.** Pasó tres veces; el arnés tiene que FABRICAR la
  situación.
- **Cuando una premisa deja de ser cierta, se le cambia el vehículo a la
  mutación, no se borra.** Borrarla para que cuadre la cuenta es perder el
  chequeo.

---

## 3. Las piezas

### 3.1 · Los verificadores, y qué pregunta hace cada uno

Ninguno repite al otro. Esa es la propiedad que los hace valer.

| módulo | la pregunta |
|---|---|
| `validar.py` | ¿es coherente la base consigo misma? |
| `verificar_srd.py` | ¿coincide con el SRD 5.2, una fuente externa sin traducir? |
| `verificar_foundry.py` | ¿coincide con el SRD estructurado de los packs de Foundry? |
| `cobertura.py` | ¿sabe la base RESPONDER lo que la skill preguntará? |
| `verificar_personaje.py` | ¿es legal esta ficha, se comprueba todo lo que aprueba, y **sigue cuadrando su lectura independiente**? |
| `censo.py` | ¿hay alguna unidad de la base sin ningún chequeo que la alcance? |
| `verificar_chequeos.py` | ¿algún chequeo abandona un registro en silencio? |
| `verificar_documentos.py` | ¿dicen la verdad los documentos de estado? |

### 3.2 · Las bibliotecas y los generadores

| módulo | qué es |
|---|---|
| `calculo.py` | lee la base y deriva; no sabe reglas de memoria |
| `efectos.py` | el motor de efectos: aplica lo que la base declara |
| `buscar.py` | la consulta: con esto el orquestador lee la base |
| `deuda.py` | la deuda enumerada (§2.3), una vez para los cinco ficheros |
| `informar.py` | el muro: un chequeo que revienta HABLA, no mata al informe |
| `materiales.py` | descompone costes de material |
| `prerrequisitos.py` | la gramática de prerrequisitos de dote |
| `generar_ficha.py` | crea fichas; el barrido 1→20 las verifica todas |
| `subir_nivel.py` | sube de nivel consultando la base |
| `_convertir_hechizos.py` | conversor de UN SOLO USO, ya ejecutado |

### 3.3 · Las dos abstracciones comunes, y por qué existen

**`deuda.py`** — había cinco ficheros con el mismo patrón y cinco
implementaciones, cuatro con los bugs que la quinta ya había arreglado. No eran
cinco problemas: era una abstracción escrita cinco veces.

**`informar.py`** — «un chequeo explota en vez de informar» apareció tres veces
en dos días. La tercera se cerró para un módulo, y ahí se quedó. `muro()`
devuelve el fallo COMO DATO del chequeo que lo provocó.

**Y no se traga un `sys.exit`:** un dato que falta en la base tiene que seguir
parando el proceso. Hay un solo sitio donde se declara lo contrario, con su
motivo escrito —`verificar_personaje`, donde lo examinado es la ficha y la
salida es un veredicto sobre la entrada, no un dato que falte—.

### 3.4 · El censo: una pregunta por fila, y todos los universos descubiertos

*(Sin recuento en el encabezado a propósito: una cifra escrita a mano ahí
se queda vieja en cuanto nace una fila. La tabla sí está anclada.)*

Cada fila es «¿hay alguna unidad de esta clase sin nada que la alcance?». El
universo se descubre; lo no alcanzado se declara con motivo o se enumera como
deuda.

| fila | universo |
|---|---|
| `fila_ficheros_de_regla` | los ficheros y directorios de regla |
| `fila_variables` | las variables calculables |
| `fila_columnas` | las columnas de las tablas de clase |
| `fila_datos_externos` | los registros con fuente externa disponible |
| `fila_chequeos` | los chequeos `validar_*` |
| `fila_modulos` | los módulos de herramienta de la raíz |
| `fila_rasgos` | los rasgos con texto |
| `fila_efectos_con_carga` | los efectos que alguna ficha sostiene |
| `fila_constantes_de_dominio` | los literales de Python que duplican la base |
| `fila_guardianes` | los scripts de la raíz sin guardián de su código |
| `fila_lectura_independiente` | las fichas cuya aritmética firma el mismo motor que la calculó |

La novena y la décima cierran el círculo hacia dentro: `fila_guardianes`
**convierte «todo verificador tiene su prueba por mutación» de costumbre en
cuenta**, y «alcanzada» no es «tiene una suite con su nombre», es **alguna
suite escribe su fichero `.py`** — mutar la base prueba que el chequeo caza
datos malos, no que el chequeo no mienta.

Y la undécima lo cierra hacia FUERA, que es lo que ninguna otra puede:
`fila_lectura_independiente` cuenta las fichas que tienen una derivación hecha
a ciegas desde la base. Es la única fila cuyo universo no lo alcanza ningún
chequeo escrito aquí dentro — y por eso es la que mide el límite del §5.

La fila mira que el papel EXISTA. Que siga **diciendo lo mismo que el motor** lo
mira `verificar_personaje.verificar_veredicto`, contra el bloque `veredicto` que
cada derivación lleva al final. Sin eso, una lectura independiente se comprobaba
una vez, el día que se escribió, y caducaba en silencio en cuanto el motor
cambiara — media comprobación, y de la clase que este documento persigue.

---

## 4. Cómo se añade algo sin romper esto

1. **¿Es una regla?** Va a la base, con su página citada. No al código.
2. **¿Es un chequeo?** Lleva su prueba por mutación, con controles negativos, y
   el censo tiene que contarlo.
3. **¿Es un módulo nuevo en la raíz?** Tres cosas a la vez, y las tres fallan
   solas si faltan: entra en `fila_modulos`, entra en `fila_guardianes` —o sea,
   alguna suite tiene que corromper su código— y **entra en la tabla del §3 de
   esta página**, porque el ancla lo exige.
4. **¿Es una lista dentro de un módulo?** No. Se descubre.
5. **¿No se puede cerrar hoy?** Deuda enumerada con `deuda.py`, nunca un
   comodín, nunca un aviso `⚠`.
6. **¿Un falso positivo?** Se corrige **afinando, no relajando**, y se queda
   como control negativo.

---

## 5. Lo que esta arquitectura NO garantiza

Hay que decirlo, porque una garantía sin límite escrito es la siguiente
mentira.

**Un guardián no puede cazar aquello en lo que el motor y el verificador se
equivocan de acuerdo.** Si la regla nunca entró en la base, el motor no la
aplica, el verificador no la exige y las dos partes coinciden — en verde.

Eso solo lo encuentra una lectura independiente. Pasó: dos agentes a ciegas, en
dos clases distintas, dieron números MAYORES que el motor y tenían razón —
«Campeón primordial» y «Cuerpo y mente» subían dos características, y la regla
estaba transcrita y citada **pero solo en la prosa**. Todo personaje de nivel 20
de Bárbaro o Monje salía con números de menos, en verde, durante semanas.

Por eso el mandato «el calculista» de `PLAN_ESTRES.md` no es un extra: es la
única pieza que mira desde fuera del sistema. Mientras haya fichas sin lectura
independiente, la garantía es real pero **acotada, y se sabe dónde**.

---

## 6. Cómo se sabe que esto funciona

No porque se prometa. **Porque el error volvió a pasar cuatro veces durante el
propio `PLAN_21`, y las cuatro lo cazó el mecanismo, no quien escribía:**

- un lector se quedó con la forma vieja del JSON → la suite reventó al correr;
- cuatro ramas silenciosas se escondieron al moverlas a un ayudante → la deuda
  bajó en falso y `verificar_chequeos` lo dijo;
- el detector de la fila 10 contaba *crear* un fichero como *mutarlo*, así que
  **se blindaba solo** → lo dijo su propia mutación;
- una mutación quitaba uno de dos guardianes y no probaba nada → lo dijo el
  marcador.

La diferencia con antes no es que el defecto haya dejado de aparecer. Es que
**ya no sobrevive a la sesión en que aparece.**
