# ✅ Plan — estresar el verificador con agentes — **EJECUTADO (2026-08-30 y 2026-09-03)**

> Escrito el **2026-08-30**, después de que el barrido automático diera
> **240/240**. Ese 240/240 no significa que el sistema esté bien: significa que
> **el generador y el verificador están de acuerdo**, que es mucho menos.

## El problema con el generador, dicho claro

`generar_ficha.py` se ganó el sueldo —destapó que el Monje de nivel 6 reventaba
el motor por un 4,5— pero tiene un techo que no puede superar: **solo produce
los errores que se le programaron**. Escribí sus reglas y escribí las del
verificador, así que su acuerdo es en parte una tautología. Prueba lo que
**revienta**; no prueba lo que el verificador **deja pasar en silencio**, que es
el modo de fallo que este proyecto lleva persiguiendo desde el principio: *«un
campo con la forma correcta puede ser basura»* (amenaza nº 3 del `FODA.md`).

Los dos huecos más grandes que se han encontrado —las características que nadie
justificaba, los conjuros que nadie contaba— no los habría encontrado nunca un
generador escrito por la misma mano que el verificador.

## La idea

Varios agentes construyen personajes **leyendo la base**, tomando decisiones
deliberadas: unas **legales** y otras **ilegales**. Cada uno declara por
adelantado y en sobre cerrado qué pretendía que fuera cada cosa. Después se
pasan por el verificador y se cuenta:

| | El verificador salta | El verificador calla |
|---|---|---|
| **La decisión era ILEGAL** | ✅ funciona | 🔴 **HALLAZGO: hueco** |
| **La decisión era LEGAL** | 🔴 **HALLAZGO: falso positivo** | ✅ funciona |

**Las dos casillas rojas valen igual.** Un verificador demasiado estricto es tan
inservible como uno demasiado laxo: el primero hace que la gente lo ignore.

## Las cuatro reglas del método, y por qué

1. **El agente NO lee el código del verificador.** Lee `personajes/_ESQUEMA.md`
   y la base — las reglas—, nunca `verificar_personaje.py` ni `validar.py`. Si
   viera los chequeos, fabricaría violaciones que ya se cazan y evitaría las que
   no: exactamente al revés de lo que hace falta.
2. **El agente NO ejecuta el verificador.** Si pudiera, iteraría hasta ponerlo
   verde y destruiría la señal. Entrega la ficha y se va.
3. **El sobre cerrado se escribe ANTES**, en un fichero aparte: qué decisiones
   tomó, cuáles cree legales, cuáles ilegales y **por qué**, citando la regla de
   la base que cree estar cumpliendo o rompiendo. Sin esto, cualquier resultado
   se racionaliza después.
4. **Ninguna ficha generada entra en `personajes/`.** Van a un directorio de
   pruebas. La base no se toca durante el estrés.

## Los cuatro mandatos

Agentes distintos con encargos distintos, porque buscan cosas distintas:

| Agente | Encargo | Qué caza |
|---|---|---|
| **A · el tramposo sutil** | Personajes que **parecen legales**: números que casi cuadran, un conjuro de más, una mejora repartida mal, una habilidad que la clase no ofrece, una subclase de otra clase | Huecos en los chequeos de contenido |
| **B · el tramposo estructural** | Ataca la **forma**: campos que faltan, refs a registros inexistentes, un `pg_por_nivel` con un hueco, `calculado` escrito a mano con un número plausible | Huecos en los chequeos de estructura |
| **C · el exótico legal** | Solo decisiones **legales pero raras**: la clase con la característica «equivocada», Constitución 8 en un nivel 20, todas las mejoras repartidas +1/+1, un lanzador sin trucos si su tabla lo permite | **Falsos positivos** |
| **D · el abogado del manual** | Lee **la página** de dos o tres reglas y construye personajes que las cumplen al pie de la letra aunque parezcan raros | Reglas que el verificador **interpreta mal**, no que se le escapen |

**C y D son tan importantes como A y B**, y son los que un generador nunca hará.

## Cómo se puntúa

Un script recoge cada ficha, la pasa por `verificar_personaje.py`, y **cruza el
resultado con el sobre cerrado** decisión a decisión. La salida es la tabla de
arriba con nombres y ejemplos, más la lista de las dos casillas rojas.

**Lo que se hace con cada hallazgo:** un hueco se cierra con un chequeo nuevo
**y su prueba por mutación**, como todos los demás. Un falso positivo se corrige
afinando el chequeo, **no relajándolo**, y se convierte en control negativo — que
es lo que ya se hizo con *Mano de Bigby* y con *Estática sináptica*.

## Riesgo, y cómo se contiene

El riesgo es que un agente declare «ilegal» algo que en realidad es legal, y me
haga «arreglar» un chequeo correcto contra una regla inventada. **Se contiene
igual que todo aquí:** el sobre cerrado obliga a **citar la regla de la base**
que se cree romper. Si la cita no existe o no dice eso, el hallazgo se descarta
y queda registrado como descartado — no como arreglado.

## Criterio de cierre

- Las cuatro casillas contadas, con nombres.
- Cada hueco confirmado, cerrado con chequeo **y** mutación.
- Cada falso positivo confirmado, convertido en control negativo.
- Cada hallazgo descartado, **registrado como descartado y por qué**.

---

## Resultado

**20 fichas · 4 agentes · 5 huecos encontrados · 0 falsos positivos confirmados.**

| | El verificador salta | El verificador calla |
|---|---|---|
| **ILEGAL** | ✅ todas las declaradas, tras cerrar los huecos | 🔴 **5 huecos** (ver `FUENTES.md`) |
| **LEGAL** | 🔴 ninguno confirmado | ✅ |

Los cinco: dotes cuyo prerrequisito nadie comprobaba · subclase de otra clase ·
el +2 del escudo sin entrenamiento · la penalización de velocidad por Fuerza ·
y **nueve de las diecisiete fichas de la base violando la regla 6 de su propio
esquema**, que los cuatro agentes copiaron de los ejemplos.

**Defecto del método, registrado:** los cuatro agentes tropezaron con la misma
prohibición (ejecutaron un `python3 -c` para inspeccionar un JSON) y los cuatro
lo declararon solos. El briefing prohibía ejecutar *cualquier* script cuando lo
que importaba era no ejecutar **el verificador**. Si se repite el experimento,
esa es la línea que hay que reescribir.


---

# Ronda 2 — 2026-09-03

Corrida después de cerrar las fases 1, 2 y 3 del `PLAN_19`, con la base muy
cambiada desde la ronda 1. **20 fichas · 4 agentes · 6 huecos · 2 falsos
positivos · 2 defectos de robustez · 3 hallazgos descartados.**

| | El verificador salta | El verificador calla |
|---|---|---|
| **ILEGAL** | ✅ 15 de 21 decisiones de A, y la mayoría de las de B | 🔴 **6 huecos** |
| **LEGAL** | 🔴 **2 falsos positivos** | ✅ el control impecable de B verifica en verde |

## Lo que se corrigió del método antes de correr

1. **La prohibición que la ronda 1 dejó apuntada.** El briefing prohibía
   «ejecutar scripts» cuando lo que importa es no ejecutar **el verificador**.
   Los cuatro agentes de la ronda 1 tropezaron con lo mismo y lo declararon
   solos. Reescrita: prohibido ejecutar los verificadores, permitido `python3
   -c`, `grep` y lo que haga falta para LEER datos. Ningún agente tropezó esta
   vez.
2. **Advertencia sobre las fichas de ejemplo.** En la ronda 1 los cuatro
   agentes copiaron el mismo defecto de los ejemplos. Ahora el briefing dice
   que los ejemplos son para ver la forma del YAML, y que una contradicción
   entre un ejemplo y `_ESQUEMA.md` es un hallazgo por sí sola. **Funcionó**:
   el agente C encontró así el hueco nº 4.
3. **La multiclase queda fuera.** El verificador la rechaza a propósito desde
   la fase 1 del `PLAN_19`, así que una ficha multiclase sería un falso
   positivo garantizado contra una limitación ya declarada: mediría cero.

## Los seis huecos

| # | Hueco | Quién lo encontró |
|---|---|---|
| 1 | **Un conjuro que no es de la lista de la clase pasa.** `hechizos.json` trae `clases:` en cada conjuro y nadie lo mira: un Hechicero con un truco de Mago verifica en verde | A · ficha 2 |
| 2 | **`pg_por_nivel` no se valida contra el dado.** Tres caras del mismo hueco: un `valor` mayor que las caras del dado de la clase (d8 → 9, d12 → 13); un `valor_establecido` que es el de OTRA clase (Guerrero 6, la ficha pone el 7 del Bárbaro) aunque `calculo.valor_establecido_pg()` ya existe y podría contrastarlo; y `metodo: maximo_dado` en un nivel que no es el 1 | A · fichas 3, 4, 5 · B · ficha 2 |
| 3 | **Un idioma con `origen: {especie: …}` inventado pasa.** Ninguna de las 10 especies de la base concede idiomas (`idiomas: []` en todas), y no se comprueba ni el origen ni el número que pide `reglas/idiomas.yaml` («común y otros dos») | A · fichas 1 y 5 · B · ficha 2 |
| 4 | **Un truco listado también como preparado cuenta dos veces.** No es hipotético: `personajes/draconido_hechicero_n4.yaml`, una ficha de la propia base, lleva «Rayo de escarcha» (nivel 0) en `trucos` **y** en `preparados`. La tabla concede 7 preparados y la ficha tiene 6 reales. Barridas las 17 fichas: solo esa | C |
| 5 | **Las claves desconocidas no se rechazan.** `raza:` al nivel superior, `decisiones[].juicio`, `decisiones[].nota`: ninguna está en el esquema y ninguna se rechaza como tal — solo saltan de rebote si su texto pasa de 15 palabras | B · ficha 4 · A y C de rebote |
| 6 | **El tope de 20 y el «+2» están cableados en Python.** `verificar_mejoras` compara `> 20` y exige la forma `+2`/`+1+1` con literales, mientras **42 de las 43 dotes generales** traen `mejora_caracteristica: {cantidad, maximo, entre}` estructurado. La única que no lo trae es «Mejora de característica», justo la que el esquema designa para cada entrada de `mejoras:`. Es el defecto nº 4 del §2 del `PLAN_18` otra vez: autoridad que vive en la base, copiada a Python, sin nadie que compare las copias | D · ficha 5 |

## Los dos falsos positivos

| # | Falso positivo | Quién |
|---|---|---|
| 7 | **`origen: {subclase: …}` no se reconoce.** La lista de orígenes válidos es `("dote","especie","rasgo","trasfondo","clase")` y le falta `subclase`, así que los conjuros de dominio del Clérigo —declarados exactamente como manda el esquema, y que la base tiene en `conjuros_siempre_preparados`— se rechazan uno a uno | B · ficha 2 |
| 8 | **La comparación de competencias distingue mayúsculas.** `trasfondos.yaml` guarda «suministros de calígrafo» en minúscula y `clases/*.yaml` guarda «Armaduras ligeras» con mayúscula; una ficha que escriba la herramienta con la mayúscula natural del castellano se rechaza contra una lista que la contiene. Son dos defectos a la vez: la comparación literal y la base inconsistente entre ficheros | A · fichas 1, 2 y 5 |

## Dos defectos de robustez

9. **`calculo.py` corta con `sys.exit` en vez de informar**, así que el primer
   defecto estructural **oculta todos los demás**: la ficha 3 de B declaraba
   cinco y solo se vio uno. Un verificador que solo enseña el primer problema
   obliga a iterar a ciegas.
10. **Una ficha sin bloque `caracteristicas` revienta con un traceback**
    (`buscar.py:174`, `KeyError`) sin imprimir ni una línea de diagnóstico.
    Rechaza —el código de salida es 1— pero no dice qué falta.

## Tres hallazgos descartados, y por qué

La contención del método funcionó: el sobre obliga a citar la regla, y tres
citas no decían lo que el agente creía.

- **«Telepático» sin prerrequisito de característica** (A). A la declaró ilegal
  por no cumplir «Int, Sab o Car 13+». La base dice `prerrequisito: 'nivel 4 o
  más'`, y nada más. **El verificador tenía razón**: descartado.
- **Habilidad de clase que duplica una del trasfondo** (A, dos fichas). A la
  declaró «ILEGAL probable» diciendo ya en el sobre que no encontraba cita.
  No la hay. Descartado por falta de regla, no por estar comprobado que sea
  legal.
- **La tabla de modificadores para en 20** (D). Es cierto que
  `modificadores_por_puntuacion.tabla` llega hasta 20 mientras los dones
  épicos permiten llegar a 30, pero `calculo.modificador()` usa la fórmula, no
  la tabla, así que no hay defecto en el código. Si la tabla del manual llega
  más allá, es una transcripción incompleta: **pendiente de leer la página**,
  no un hallazgo del estrés.

## Defecto del método en esta ronda, registrado

Los agentes A y C inventaron claves dentro de `decisiones` (`juicio`, `nota`)
para dejar ahí su razonamiento, y eso llenó la salida del verificador de
errores de «texto copiado» que **no eran la decisión que querían medir**. El
sobre ya existe para eso. Si se repite el experimento, el briefing debe decir
que el razonamiento va SOLO en el sobre y que la ficha no lleva comentarios.


---

## Cierre de la ronda 2 — 2026-09-05

**Los diez hallazgos, cerrados.** Y la forma de cerrarlos importa tanto como
el hecho: la clasificación previa dijo que **solo 5 de los 10 eran parches
puntuales genuinos**, así que no se hicieron diez arreglos. Se hicieron
cuatro mecanismos y tres correcciones de dato.

| # | Hallazgo | Cómo se cerró |
|---|---|---|
| 1 | Conjuro que no es de la lista de su clase | Los 391 registros traen `clases`. Se extiende el mecanismo que ya usaban armas/armaduras/herramientas: reúne lo permitido, comprueba membresía |
| 2 | `pg_por_nivel` sin contrastar (3 caras) | Los métodos legales salen de `metodos` y el valor fijo de la tabla citada; `calculo.valor_establecido_pg()` ya existía y ahora se usa para verificar. Cero números cableados |
| 3 | Idioma con origen inventado | Mismo mecanismo que el nº 1, aplicado a la única superficie de la ficha que no pasaba por ningún contraste porque no lleva `ref:` |
| 4 | Truco contado también como preparado | Se comprueba el contenido de la lista, no su longitud: ningún conjuro en las dos listas, y el nivel del conjuro tiene que corresponder con la lista en la que vive |
| 5 | Claves desconocidas del YAML | **Ni una sola clave escrita a mano.** La lista válida se LEE de `personajes/_ESQUEMA.md` —su bloque de ejemplo más la sección «Prosa libre»—. Rechaza las tres que los agentes inventaron y una cuarta que nadie probó |
| 6 | El tope de 20 cableado en Python | «Mejora de característica» gana su `mejora_caracteristica` estructurado, y `validar.py` contrasta el texto de la dote contra su campo: las dos copias ya no pueden divergir |
| 7 | `origen: {subclase: …}` rechazado en falso | Afinado, no relajado: el origen no solo se acepta, se **comprueba** contra `conjuros_siempre_preparados` |
| 8 | Competencias sensibles a mayúsculas | Se normaliza la capitalización, que es ortografía. Las tildes NO, y hay mutación que lo fija |
| 9 | `sys.exit` que tapaba los demás errores | Cada chequeo corre en su propia red: un fallo se convierte en error con su nombre y los demás siguen |
| 10 | `KeyError` mudo | Ídem: nombra el bloque que falta en vez de reventar |

### Tres defectos VIVOS en la base, que los agentes predijeron sin saberlo

Es el resultado más incómodo de la ronda, y el que más justifica repetirla:
**tres de los casos que los agentes inventaron para probar un hueco estaban
ocurriendo de verdad en las fichas del repo.**

| Lo que el agente inventó | Lo que había |
|---|---|
| «Tañido por los muertos» (conjuro de Brujo) en un Hechicero | «Descarga sobrenatural», conjuro de Brujo, en `draconido_hechicero_n4.yaml` |
| Un truco contado entre los preparados | «Rayo de escarcha» en `trucos` **y** en `preparados`, misma ficha |
| «Élfico» en vez del canónico «Elfo» | Las dos fichas de `gnomo_mago` |

El tercero es el más elocuente: **ya era un defecto conocido**.
`_ejemplo_aerin.yaml` lleva escrito el comentario que lo explica y dice que
«ningún validador lo pilló, porque `idiomas` no lleva `ref:`». Se corrigió el
dato en el ejemplo y se dejó vivo en las otras dos, porque nadie cerró el
hueco. Parche puntual en estado puro.

### Un control negativo que se quedó viejo, y por qué se registra

`n_una_sola_clase_sigue_pasando` perturbaba añadiendo un campo extra a la
ficha. Al cerrar el hueco nº 5, esa perturbación pasó a ser ilegal y el
control empezó a fallar. **No era un falso positivo: era el vehículo del
control lo que había dejado de ser legal.** Se le cambió el vehículo y la
intención no se tocó. Merece registro porque la tentación —relajar el chequeo
nuevo para que el control viejo siguiera pasando— es exactamente el error que
el método prohíbe.

### Cifras al cerrar

```
mutaciones_nivel20     48/48 (eran 18 al empezar el día)
18/18 fichas           (17 antes: entra `enano_clerigo_n5.yaml`)
validar.py 0 errores · censo 867 · srd 646 · foundry 3749
verificar_chequeos     67 silenciosas · 20 declaradas `# TOLERADO:`
```

**Lo que la ronda 2 NO cerró, y queda para la auditoría pendiente:** la
pregunta de si el patrón de autoridad duplicada vive también en `calculo.py`,
`efectos.py`, `subir_nivel.py` y `generar_ficha.py`, que ninguna ronda de
estrés ha tocado todavía.
