# ✅ Plan — estresar el verificador con agentes — **EJECUTADO (2026-08-30)**

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
