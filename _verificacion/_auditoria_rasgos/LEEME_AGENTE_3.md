# Encargo: auditar los conjuros que ninguna fuente externa cubre

Lee esto entero antes de empezar. Tu asignación concreta viene en el mensaje
que te ha lanzado.

## Por qué este lote es el más importante de todos

`hechizos.json` tiene 391 conjuros. 304 se han contrastado contra el SRD 5.2 y
**ahí aparecieron 9 errores reales** (2,96 % de los conjuros). Los otros **87 no
están en el SRD**: nadie los ha comparado nunca con nada. Proyectando la misma
tasa, es razonable esperar **2 o 3 errores escondidos entre ellos**, y tú vas a
revisar una cuarta parte.

Es el único hueco de la base con una cifra de riesgo concreta. No hay atajo
posible: la única autoridad es la página del Manual del Jugador.

## ⛔ La regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Los conjuros son justo donde más tentador resulta tirar de memoria, porque el
modelo «recuerda» muchos de 2014 y varios cambiaron en 2024. Si te descubres
pensando «este conjuro es de concentración porque siempre lo ha sido», para y
mira la línea **Duración** de la página.

## El fallo que estamos buscando (ya lo hemos visto 9 veces)

`hechizos.json` viene de un CSV, y su patrón de error es **inversión de dos
campos contiguos**:

- **V y S intercambiados** — la base dice «Componentes: S» y la página dice «V»
  (pasó en *Contorno borroso*, *Engañar*, *Palabra de regreso*, *Palabra divina*)
- **concentración y ritual intercambiados** — la base marca `ritual: true` y la
  página dice «Duración: Concentración, hasta X» (pasó en *Aliento de dragón*,
  *Alterar el propio aspecto*, *Levitar*)
- **escuela equivocada** (pasó en *Guardián de la fe* y *Paso arbóreo*)

**Compara esos campos uno a uno, letra a letra, en todos tus conjuros.** No los
des por buenos porque «suenen bien».

## Cómo leer una página

```bash
mkdir -p /tmp/render
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/p
```

Genera `/tmp/render/p-<pag>.png` (ceros a 3 dígitos: `p-244.png`). Ábrelo con
la herramienta de lectura de imágenes (Read).

- **`-r 170` es la resolución mínima legible.** No bajes de ahí.
- **`pdftotext` NO es fuente válida** (OCR basura, escaneo a 96 DPI). Solo
  sirve para localizar en qué página está algo.
- **Offset confirmado en TODO el manual: `página_pdf = página_libro + 2`.** Tu
  asignación ya te da los dos números. El offset no tiene excepciones: si algo
  no cuadra, es la cita la que está mal.
- Un conjuro puede continuar en la página siguiente. Si el texto se corta,
  renderiza también la siguiente.

## Qué comprobar, campo por campo

Cada conjuro del manual tiene una cabecera con esta forma:

```
NOMBRE DEL CONJURO
Escuela de nivel N (clases que lo tienen)
Tiempo de lanzamiento: ...
Alcance: ...
Componentes: V, S, M (material)
Duración: ...
```

Y en `hechizos.json` cada conjuro tiene estos campos. Compruébalos **todos**:

| Campo del JSON | Dónde mirarlo en la página |
|---|---|
| `nivel` | «…de nivel N» (un truco es `nivel: 0`) |
| `escuela` | la palabra antes de «de nivel N» |
| `clases` | la lista entre paréntesis tras el nivel |
| `tiempo_lanzamiento` | línea «Tiempo de lanzamiento» |
| `alcance` | línea «Alcance» (comprueba también `metros`/`pies` si los hay) |
| `duracion` | línea «Duración» |
| `componentes.verbal/somatico/material` | línea «Componentes»: V, S, M |
| `componentes.coste` / `consume_material` | el paréntesis tras la M, si trae precio o dice «se consume» |
| `concentracion` | `true` **solo si** la Duración dice «Concentración» |
| `ritual` | `true` **solo si** el Tiempo de lanzamiento dice «o un ritual» |
| `fuente.pagina_libro` | el número impreso al pie de la página |

**Ojo con `concentracion` y `ritual`:** son campos distintos que viven en
líneas distintas de la página. Un conjuro puede tener los dos, uno o ninguno.

A diferencia de los rasgos de clase, aquí `descripcion` es **transcripción
literal**, no un resumen. Aun así, **no reportes diferencias de redacción
menores**: reporta solo si la descripción dice algo mecánicamente distinto
(otra cifra, otro dado, otra tirada de salvación, otra condición) o si le falta
un párrafo entero, como el de «Con un espacio de conjuro de nivel superior».

## Qué NO es un hallazgo

- Diferencias de puntuación, tildes o mayúsculas.
- Que el `resumen` no aparezca en la página: es un campo nuestro, no del manual.
- Que la descripción esté partida en párrafos de otra forma.
- Que falte el texto de sabor en cursiva de antes de la descripción.

## Cómo entregar

**NO edites ningún fichero de la base.** No toques `hechizos.json` ni nada
fuera de tu informe. Las correcciones las aplica quien te ha lanzado, tras
releer él mismo cada página que señales.

Escribe **un solo fichero**:
`_verificacion/_auditoria_rasgos/<tu-id>.md`

```markdown
# Auditoría de conjuros — lote <N>

Agente: <tu-id> · fecha: 2026-08-21
Páginas leídas: pdf 244, 246, ...
Conjuros revisados: N de N

## Hallazgos

### <Nombre del conjuro> · pdf <pág>
- **Campo:** nivel | escuela | clases | tiempo_lanzamiento | alcance | duracion | componentes | concentracion | ritual | cita de página | descripción
- **Dice el JSON:** «...»
- **Dice la página:** «...» (cita textual de lo que has leído)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Revisados sin hallazgo
<lista de nombres>

## Dudas / ilegible
```

Si no encuentras nada, dilo explícitamente y **lista igualmente los conjuros
revisados**. Un informe vacío sin lista no sirve.

## Antes de terminar

¿Has abierto **todas** las páginas de tu asignación? ¿Has comparado los **nueve
campos** de cada conjuro, no solo los que te llamaron la atención? ¿Has mirado
`concentracion` y `ritual` por separado, en sus dos líneas distintas? ¿Alguno
de tus hallazgos se apoya en lo que «sabes» de D&D en vez de en la imagen?

**Y si explicas por qué algo no cuadra, comprueba la explicación igual que el
hallazgo.** En una tanda anterior un agente acertó el hallazgo e inventó la
causa; eso cuesta tiempo de verificación.
