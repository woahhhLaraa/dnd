# Encargo: medir la tasa de error de las descripciones de conjuro

Lee esto entero antes de empezar. Tu asignación concreta viene en el mensaje que
te ha lanzado, y la muestra completa está en `MUESTRA_13o.md`.

## Qué es esta tanda y por qué es distinta

**Esto no es una auditoría de barrido: es una medición.** De los 391 conjuros de
la base, 306 se contrastan automáticamente contra el SRD 5.2 — pero solo en su
cabecera (nivel, escuela, componentes, banderas, alcance, duración). **La
`descripcion` no la cubre ninguna fuente externa**, porque el SRD no publica ese
campo. Son 306 textos que nadie ha vuelto a mirar desde que se convirtieron
desde un CSV, y ese CSV lleva **cinco defectos demostrados**.

Auditarlos todos son unas 45 páginas. Antes de decidir si merece la pena, se
audita **una muestra aleatoria de 40** para estimar la tasa de error real. Tú
llevas 10 de esos 40.

Por eso aquí importa muchísimo **no inflar ni deflactar el recuento**: cada
hallazgo tuyo, y cada conjuro que declares limpio, entra en una estadística. Un
falso positivo contamina la medición tanto como un fallo que se te escape. **Si
dudas, dilo en «Dudas» en vez de decidir tú si cuenta.**

## ⛔ La regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Esto es crítico en tu lote: te van a tocar conjuros famosísimos (*Dormir*,
*Bendición*, *Rociada de color*, *Piel pétrea*…) que **cambiaron en 2024**.
*Dormir* ya no funciona por puntos de golpe. Si te descubres pensando «este
conjuro hace X porque siempre lo ha hecho», para y lee la página.

## Cómo leer una página

```bash
mkdir -p /tmp/render
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Genera `/tmp/render/<tu-id>-<pag>.png`. Ábrelo con la herramienta de lectura de
imágenes (Read).

- **`-r 170` es la resolución mínima legible.** No bajes de ahí.
- **`pdftotext` NO es fuente válida** (OCR basura). Solo sirve para localizar.
- **Offset confirmado: `página_pdf = página_libro + 2`.** Tu asignación te da los
  dos números.
- **Un conjuro puede continuar en la página siguiente.** Si el texto se corta a
  mitad de frase o falta el párrafo de «Con un espacio de conjuro de nivel
  superior», renderiza también la siguiente. Varios de la muestra lo hacen.

## Los cinco campos que tienes que comprobar

Estos son exactamente los que ninguna fuente externa cubre. **Los demás campos
(nivel, escuela, componentes V/S/M, concentración, ritual, alcance, duración) ya
están contrastados por script: NO los audites y NO los reportes.**

| Campo | Qué comprobar |
|---|---|
| `descripcion` | **el foco.** Cifras, dados, tipo de daño, tirada de salvación, área, duración de efectos, condiciones aplicadas, y que no falte ningún párrafo |
| `clases` | la lista entre paréntesis de la cabecera, tras «de nivel N» |
| `tirada` | qué tirada exige el conjuro (p. ej. «TdS Des.», «ataque de conjuro»); debe cuadrar con lo que dice la descripción de la página |
| `resumen` | campo nuestro, no del manual. **Solo es hallazgo si contradice a la página**, no por ser breve o no aparecer |
| material (el texto del paréntesis tras la M) | si el registro lo guarda, que coincida con el paréntesis impreso |

## Qué es hallazgo y qué no

**SÍ es hallazgo:**
- Cualquier cifra distinta: dados, metros, CD, duración, número de objetivos.
- Otra característica en la tirada de salvación, u otro tipo de daño.
- Un párrafo entero que falta, sobre todo «Con un espacio de conjuro de nivel
  superior» o «Mejora de truco».
- Una condición/estado distinto del que dice la página.
- Texto que **remite al manual** en vez de traer el dato («ver MdJ», «revisar…»).
  Esto es grave: la base debe ser autosuficiente. **Ya no debería quedar
  ninguno**; si encuentras uno, dilo bien claro.
- Una frase que añade una condición que la página no pone, o que se la salta.

**NO es hallazgo:**
- Diferencias de redacción, puntuación, tildes o mayúsculas.
- Que la descripción sea más densa o esté reordenada respecto a la página: es un
  resumen mecánico, no una transcripción literal.
- Que falte el texto de sabor en cursiva.
- Unidades equivalentes expresadas de otra forma (18 m vs 60 pies).
- Que el `resumen` no esté en la página.

## Cómo entregar

**NO edites ningún fichero de la base.** No toques `hechizos.json`. Las
correcciones las aplica quien te ha lanzado, tras releer él mismo cada página.

Escribe **un solo fichero**:
`/home/larita/Documents/DnD/base-canonica/_verificacion/_auditoria_rasgos/<tu-id>.md`

```markdown
# Auditoría de descripciones (muestra 13o) — lote <X>

Agente: <tu-id> · fecha: 2026-08-22
Páginas leídas: pdf ...
Conjuros revisados: 10 de 10

## Hallazgos

### <Nombre> · pdf <pág>
- **Campo:** descripcion | clases | tirada | resumen | material
- **Dice la base:** «...»
- **Dice la página:** «...» (cita textual)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Revisados sin hallazgo
<los 10 por nombre, con una línea de qué comprobaste en cada uno>

## Dudas / ilegible
```

**Los 10 tienen que aparecer**, con hallazgo o sin él. Si un conjuro te deja
dudas, va en «Dudas», no en «Hallazgos» ni en «sin hallazgo».

## Antes de terminar

¿Has leído la página de los **10**? ¿Has renderizado la página siguiente en los
que el texto continuaba? ¿Has comprobado que no falte el párrafo de «nivel
superior» en los que lo tienen? ¿Algún hallazgo tuyo se apoya en lo que «sabes»
de D&D de la edición de 2014 en vez de en la imagen?

**Y si explicas por qué algo no cuadra, comprueba la explicación igual que el
hallazgo.** En una tanda anterior un agente acertó el hallazgo e inventó la
causa; se comprobó y era falsa. Prefiero «no sé por qué» a una causa inventada.
