# Encargo: auditar las descripciones de conjuro (Fase 13p)

Lee esto entero antes de empezar. Tu lote concreto está en `LOTES_13p.md`, en la
sección con tu identificador.

## Por qué se hace esta tanda

Una muestra aleatoria de 40 de estos conjuros (Fase 13o) dio **7 defectos: un
17,5 % de error**. Es un orden de magnitud peor que cualquier otra parte de la
base (2,96 % en los campos que el SRD contrasta, 0,72 % en dotes y equipo).

La razón: la `descripcion` de los conjuros **no la cubre ninguna fuente
externa**. El SRD no publica ese campo, así que ningún script puede
contrastarlo, y nadie lo ha vuelto a mirar desde que se convirtió desde un CSV
que ha demostrado ser malo.

**Aquí no estás buscando erratas: estás buscando reglas falsas.** Uno de los 7
defectos era un conjuro cuya descripción entera era la de OTRO conjuro. Otro
inventaba una mecánica que no existe en el manual.

## ⛔ Las reglas que no puedes romper

**LEER, NO DEDUCIR.** En la oleada 3 un auditor dedujo que una conversión era
falsa **por aritmética y por comparación con el SRD inglés**, en vez de leer la
página. Acertó — pero un acierto por el método equivocado **es indistinguible
de un acierto por casualidad**, y obliga a releerlo todo. Si te preguntas si
una cifra aparece, la respuesta es «sí, dice X» o «no aparece», **nunca
«debería ser Y»**.


**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Esto no es retórica en este lote concreto. **Un defecto real encontrado fue una
regla de la edición de 2014 metida en la base como si fuera de 2024**
(*Apariencia*, con su prueba de Investigación que en 2024 ya no existe). El CSV
de origen arrastra memoria de la edición vieja. Si una descripción te «suena
bien», sospecha más, no menos.

## Los seis modos de fallo confirmados

Búscalos activamente, en este orden:

1. **Descripción de otro conjuro.** *Aura sagrada* tenía, palabra por palabra,
   el texto de *Aura mágica de Nystul* — impreso en la misma página. **Lo
   primero que debes comprobar de cada conjuro es que la descripción hable de lo
   que dice la cabecera.** Si un conjuro de nivel 8 de clérigo describe una
   ilusión de nivel 2 de mago, ya has encontrado uno.
2. **Reglas de 2014.** Pruebas de característica, mecánicas de puntos de golpe
   totales, componentes o duraciones de la edición anterior.
3. **Párrafo entero que falta.** Sobre todo «Con un espacio de conjuro de nivel
   superior» y «Mejora de truco», pero también párrafos de reglas en medio del
   texto (a *Muro de piedra* le faltaba el de los muros de más de 6 m).
4. **Cifras cambiadas.** Dados, metros, CD, duraciones, número de objetivos.
   *Espejismo arcano* decía «1 km cuadrados» donde la página dice «zona cuadrada
   de 1,5 km de lado».
5. **Nombres de tabla inventados.** *Controlar el clima* traía seis estados con
   nombres que no están en el manual. Si el conjuro tiene una tabla o una lista
   de opciones elegibles, **coteja cada nombre**.
6. **Conversiones de unidad falsas.** La base añade equivalencias en pies,
   millas o yardas que el manual no trae. *Crecimiento vegetal* decía «0,46
   yardas» donde son millas. **Comprueba que la conversión sea aritméticamente
   correcta y que la unidad sea la que toca.**
7. **Regla inventada que tapa a la real.** No es texto que falte: es texto de
   más **que suena a regla**. *Creación* prohibía algo que el manual permite y
   omitía la prohibición que sí impone; *Dominar monstruo* concedía un «control
   total de las acciones del objetivo» que la página no da; *Mente en blanco*
   concedía inmunidad a «conjuros de adivinación», categoría que la página **no
   nombra jamás**, y a la vez callaba la cláusula de observación remota que sí
   impone. **Las dos mitades del error pueden empujar en direcciones opuestas,
   así que el párrafo tiene el tamaño correcto.** No juzgues por longitud.
8. **Lista de `clases` corta.** *Clarividencia* decía `["Mago"]` donde la
   cabecera lista cuatro clases. **Una lista corta pasa por lista buena.**
   Cotéjala una a una contra el paréntesis de la cabecera.
9. **Contaminación del conjuro vecino.** Es el modo de fallo estructural del
   CSV de origen y va por su **quinto** caso, todos entre conjuros **impresos
   uno al lado del otro**: *Aura sagrada*/*Aura mágica de Nystul*,
   *Polimorfar verdadero*/*Polimorfar*, *Presciencia*/*Presencia regia de
   Yolande*, *Curar heridas en masa*/*Curar en masa*. **Cuando dos conjuros de
   tu página tengan nombres parecidos, cotéjalos el uno contra el otro además
   de contra la página.**

## Cómo leer una página

```bash
mkdir -p /tmp/render
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Genera `/tmp/render/<tu-id>-<pag>.png`. Ábrelo con la herramienta de lectura de
imágenes (Read).

- **`-r 170` es la resolución mínima legible.** Para una tabla apretada, sube a
  `-r 220`, o recorta una región con `-x -y -W -H` para leerla más grande.
- **`pdftotext` NO es fuente válida** (OCR basura). Solo sirve para localizar.
- **Offset confirmado: `página_pdf = página_libro + 2`.**
- **Tu lote es contiguo por página a propósito:** varios conjuros comparten
  página, así que **renderiza cada página una vez y audita de golpe todos los
  conjuros tuyos que estén en ella**. No la renderices una vez por conjuro.
- **Si un conjuro se corta al final de la página, renderiza la siguiente.** Es
  donde se esconden los párrafos que faltan.

## Los cinco campos que auditas

**NO audites nivel, escuela, componentes V/S/M, concentración, ritual, alcance
ni duración: ya están contrastados por script.** Si ves una discrepancia ahí,
menciónala en «Dudas», pero no es tu lote.

| Campo | Qué comprobar |
|---|---|
| `nombre` | **NUEVO.** Transcribe la cabecera impresa y compárala letra a letra. La base lleva **7 erratas de nombre corregidas** (`Adiviniación`, `Baile irresistibile`, `Flecha acida`, `Poliformar`→**Polimorfar** ×2…) y **las 7 se encontraron de rebote, ninguna buscándolas** |
| `descripcion` | **el foco**, con los nueve modos de fallo de arriba |
| `clases` | la lista entre paréntesis de la cabecera |
| `tirada` | qué tirada exige; debe cuadrar con la descripción de la página |
| `resumen` | campo nuestro. **Solo es hallazgo si contradice a la página** — pero míralo de verdad: en la oleada 3 fueron **4 de los 15 defectos**, y los cuatro contradecían la `descripcion` correcta que llevaban al lado |
| material (texto del paréntesis tras la M) | si el registro lo guarda |

**Sobre `tirada`:** muchos conjuros dicen `"Directo"`. Hay una decisión de
diseño pendiente sobre qué significa exactamente ese valor, así que **si el
único problema de un conjuro es que dice `Directo` y su descripción pide una
salvación, ponlo en «Dudas», no en «Hallazgos»**. Ya está contado aparte.

## 📏 Encargo extra de esta oleada: ¿imprime pies esta página?

Hay una decisión abierta que depende de un dato que solo tú puedes traer.
**Seis páginas leídas por cuatro verificadores distintos no traen ni una sola
unidad imperial**: el manual castellano parece ser íntegramente métrico, y las
~550 equivalencias «N m / M pies» de la base serían todas añadido nuestro.

Por eso, **en tu informe, además de los hallazgos, incluye una sección
`## Unidades` que conteste de forma tajante, página por página**:

> pdf NNN: solo métricas | imprime también «X pies» en «…cita…»

Basta con mirar si en la página aparece impresa alguna cifra seguida de
«pies», «pulgadas», «yardas», «millas» o «pies cuadrados». **Es un dato de
observación, no un juicio**: si no aparece ninguna, dilo; si aparece una sola,
cítala entera, porque cambiaría la decisión.

## Qué NO es hallazgo

- Diferencias de redacción, puntuación, tildes o mayúsculas.
- Que la descripción sea más densa o esté reordenada: es un resumen mecánico,
  no una transcripción literal.
- Que falte el texto de sabor en cursiva.
- Unidades equivalentes bien convertidas (18 m vs 60 pies) — **eso va a la
  sección `## Unidades`, no a Hallazgos.**
- Que el `resumen` no aparezca en la página.

## Cómo entregar

**NO edites ningún fichero de la base.** No toques `hechizos.json`. Las
correcciones las aplica quien te ha lanzado, tras releer él mismo cada página.

Escribe **un solo fichero**:
`/home/larita/Documents/DnD/base-canonica/_verificacion/_auditoria_rasgos/agente-<tu-id>.md`

```markdown
# Auditoría de descripciones (Fase 13p) — lote <tu-id>

Agente: <tu-id> · fecha: 2026-08-29
Páginas leídas: pdf ...
Conjuros revisados: N de N

## Hallazgos

### <Nombre> · pdf <pág>
- **Campo:** nombre | descripcion | clases | tirada | resumen | material
- **Modo de fallo:** 1-9 de la lista del briefing, o «otro»
- **Dice la base:** «...»
- **Dice la página:** «...» (cita textual)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Revisados sin hallazgo
<todos, por nombre>

## Unidades
pdf NNN: solo métricas | imprime «X pies» en «…»

## Dudas / ilegible
```

**Todos los conjuros de tu lote tienen que aparecer**, con hallazgo o sin él. Un
informe que no los liste no sirve: no se puede distinguir de «no lo he mirado».

## Antes de terminar

¿Has abierto la página de **todos** los conjuros de tu lote? ¿Has comprobado en
cada uno que **la descripción corresponda al conjuro de la cabecera**? ¿Has
renderizado la página siguiente donde el texto se cortaba? ¿Has verificado
aritméticamente las conversiones de unidad? ¿Algún hallazgo tuyo se apoya en lo
que «sabes» de D&D en vez de en la imagen?

**Y si explicas por qué algo no cuadra, comprueba la explicación igual que el
hallazgo.** Prefiero «no sé por qué» a una causa inventada.
