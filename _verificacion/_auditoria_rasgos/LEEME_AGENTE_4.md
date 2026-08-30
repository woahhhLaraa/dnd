# Encargo: cerrar las superficies que ninguna fuente externa cubre

Lee esto entero antes de empezar. Tu asignación concreta viene en el mensaje
que te ha lanzado.

## Por qué existe esta tanda

La base tiene cuatro validadores y dos de ellos contrastan contra el SRD 5.2.
Lo que vas a auditar tú **es justo lo que el SRD no publica**: las
descripciones de las dotes, el equipo inicial de los trasfondos y la tabla de
precio y peso del equipo de aventurero. Ningún script puede comprobarlos —
literalmente no hay nada contra lo que compararlos.

Eso significa que **ese dato no lo ha mirado nadie desde que se transcribió**.
La tasa de error observada en las superficies que sí se pudieron contrastar es
del 2,96 %. No hay motivo para pensar que esta sea mejor. La única autoridad es
la página del Manual del Jugador.

## ⛔ La regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Las dotes y el equipo son terreno especialmente resbaladizo: muchas dotes
existían en 2014 con otros prerrequisitos y otros efectos, y **en 2024 casi
todas cambiaron**. Si te descubres pensando «esta dote da +1 a Fuerza porque
siempre lo ha dado», para y mira la página.

## El patrón de error que buscamos

En esta base los defectos **no** suelen estar en el texto mecánico, que sale
bastante bien de la lectura visual. Salen en otros tres sitios, por este orden:

1. **La cita de página.** De los 14 defectos de las dos auditorías anteriores,
   **13 eran citas de página equivocadas**. Es el dato que sostiene la
   auditabilidad de toda la base y el único que ninguna fuente externa puede
   comprobar. **Verifica siempre el número impreso al pie de la página donde
   realmente está la mecánica.**
2. **Campos contiguos intercambiados o contaminados por la fila vecina** — el
   fichero de conjuros vino de un CSV y arrastró varios; en dotes y equipo
   puede pasar igual entre columnas de una tabla (precio de una fila con el
   peso de la siguiente).
3. **Cifras sueltas**: un «30» que se vuelve «3d0», un «8» que se vuelve «3»,
   un «1,5 kg» que se vuelve «15 kg».

**Criterio de citas, ya fijado en este proyecto:** una cita apunta a la página
donde está **la mecánica**, no donde empieza la sección o el capítulo.

## Cómo leer una página

```bash
mkdir -p /tmp/render
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Genera `/tmp/render/<tu-id>-<pag>.png` (ceros a 3 dígitos: `x-204.png`). Ábrelo
con la herramienta de lectura de imágenes (Read).

- **`-r 170` es la resolución mínima legible.** No bajes de ahí. Si una tabla
  de precios te sale apretada, sube a `-r 220` para esa página concreta.
- **`pdftotext` NO es fuente válida** (OCR basura, escaneo a 96 DPI). Solo
  sirve para localizar en qué página está algo.
- **Offset confirmado en TODO el manual: `página_pdf = página_libro + 2`.** Tu
  asignación te da los dos números. El offset no tiene excepciones: si algo no
  cuadra, es la cita la que está mal, no el offset.
- Una entrada puede continuar en la página siguiente. Si el texto se corta,
  renderiza también la siguiente.

## Qué comprobar

Depende de tu lote; tu mensaje te dice cuál es. Los campos son estos:

**Dotes** (`dotes/*.yaml`) — cada entrada tiene `nombre`, `pagina.pdf`,
`pagina.libro`, `prerrequisito`, `repetible`, `descripcion`.

| Campo | Dónde mirarlo |
|---|---|
| `nombre` | el título de la dote |
| `prerrequisito` | la línea «Prerrequisito:» — **`null` significa que la página no trae ninguna**; que falte una línea que sí está es un hallazgo grave |
| `repetible` | la página dice «Repetible» o «Puedes elegir esta dote más de una vez» |
| `descripcion` | los beneficios, uno a uno, con sus cifras |
| `pagina.libro` | el número impreso al pie |

La `descripcion` de las dotes **no es transcripción literal**: es un resumen
denso con las mecánicas separadas por «Nombre del beneficio: …». No reportes
diferencias de redacción. **Reporta si falta un beneficio entero, si una cifra
no coincide, o si dice algo mecánicamente distinto.**

**Trasfondos** (`trasfondos/trasfondos.yaml`) — `nombre`, `pagina`,
`caracteristicas` (las 3), `dote`, `habilidades` (las 2), `herramienta`,
`equipo_a` (la lista completa con las cantidades y el oro final) y `equipo_b`
(la cifra en oro de la opción alternativa).

**El foco de este lote es `equipo_a` y `equipo_b`.** Comprueba **cada objeto,
cada cantidad y la cifra de oro final**, uno a uno. Es lo que nunca se ha
verificado.

**Equipo de aventurero** (`equipo/aventureros.yaml` → `tabla_peso_precio`, y
`equipo/municion.yaml`) — cada objeto tiene `nombre`, `peso_kg` y `precio`.
Compara **contra la tabla del manual, celda a celda**. `peso_kg: null` significa
que la tabla trae un guion («—»); si la tabla trae un número y nosotros
tenemos `null`, es un hallazgo, y al revés también.

## Qué NO es un hallazgo

- Diferencias de puntuación, tildes o mayúsculas.
- Que la descripción esté partida en párrafos o frases de otra forma.
- Que falte el texto de sabor en cursiva.
- Un campo nuestro que no aparece en la página (`repetible: false` cuando la
  página simplemente no dice nada: eso es correcto).
- Unidades expresadas de otra forma equivalente (0,5 kg vs 500 g).

## Cómo entregar

**NO edites ningún fichero de la base.** No toques los `.yaml` ni
`hechizos.json` ni nada fuera de tu informe. Las correcciones las aplica quien
te ha lanzado, tras releer él mismo cada página que señales.

Escribe **un solo fichero**:
`/home/larita/Documents/DnD/base-canonica/_verificacion/_auditoria_rasgos/<tu-id>.md`

```markdown
# Auditoría <dotes|trasfondos|equipo> — lote <N>

Agente: <tu-id> · fecha: 2026-08-22
Páginas leídas: pdf 204, 205, ...
Registros revisados: N de N

## Hallazgos

### <Nombre> · pdf <pág>
- **Campo:** <el campo exacto del YAML>
- **Dice la base:** «...»
- **Dice la página:** «...» (cita textual de lo que has leído)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Revisados sin hallazgo
<lista de nombres>

## Dudas / ilegible
```

Si no encuentras nada, dilo explícitamente y **lista igualmente los registros
revisados**. Un informe vacío sin lista no sirve.

## Antes de terminar

¿Has abierto **todas** las páginas de tu asignación? ¿Has comparado **todos**
los campos de cada registro, no solo los que te llamaron la atención? ¿Has
verificado la **cita de página** de cada uno contra el número impreso al pie —
que es donde salieron 13 de los 14 defectos anteriores? ¿Alguno de tus
hallazgos se apoya en lo que «sabes» de D&D en vez de en la imagen?

**Y si explicas por qué algo no cuadra, comprueba la explicación igual que el
hallazgo.** En una tanda anterior un agente acertó el hallazgo e inventó la
causa (dijo que el PDF tenía páginas duplicadas; se comprobó píxel a píxel y
era falso). Una causa inventada cuesta más tiempo que el hallazgo que ahorra.

**Una ausencia también es un dato.** Si la página no dice algo que esperarías
—un precio que no aparece, un prerrequisito que no está— eso se registra como
evidencia negativa citando dónde has mirado, no se rellena ni se omite.
