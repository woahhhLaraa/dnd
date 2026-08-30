# Encargo de verificación independiente (oleada 3, lote B4)

Eres un **verificador ciego**. NO has visto ningún informe previo y no debes
buscarlo: en este mismo directorio hay ficheros `agente-B*.md` y `agente-A*.md`
— **no los abras**. Tu valor está justamente en no saber qué se espera que
contestes.

## Regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D.
Si no lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, dilo — **jamás rellenes**.

**No razones por aritmética ni por comparación con el SRD inglés: transcribe lo
que está impreso.** Si te preguntan si una cifra aparece, la respuesta es «sí,
dice X» o «no aparece», nunca «debería ser Y».

**No edites ningún fichero de la base.** Solo lees páginas y escribes tu informe.

## Método de lectura

```bash
pdftoppm -r 170 -f <pag> -l <pag> -png ~/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/v7
```
Genera `/tmp/render/v7-<pag>.png`. Léelo con la herramienta de lectura de
imágenes. **`pdftotext` NO es fuente válida** (el OCR de este PDF es basura).
Offset: **página_pdf = página_libro + 2**. Si un conjuro se corta al pie de una
columna, renderiza también la página siguiente y transcríbelo entero.

## Preguntas cerradas — contéstalas UNA A UNA con cita textual

### Página pdf 322 (= libro 320) — **Poliformar verdadero** (True Polymorph)

1. **Transcribe el texto COMPLETO del conjuro**, de la cabecera al final, palabra
   por palabra, incluidos todos los apartados o viñetas.
2. Sobre ese texto, contesta explícitamente:
   - Cuando una criatura se transforma en otra criatura, ¿qué pasa con sus
     **puntos de golpe**? ¿Asume los de la nueva forma, o **mantiene los suyos**?
     ¿Se mencionan puntos de golpe **temporales**? Cita la frase exacta.
   - ¿Dice el conjuro que termina cuando el objetivo llega a **0 puntos de
     golpe**? Contesta sí o no, y cita la frase donde se diga (o di de forma
     tajante que no aparece).
   - Cuando un **objeto** se convierte en criatura, ¿**cuándo actúa** esa
     criatura? ¿En tu turno, o tiene turno propio? Cita la frase exacta.

### Página pdf 323 (= libro 321) — **Presciencia** (Foresight)

3. Transcribe la **primera frase** del conjuro y di en una línea cuál es su
   efecto. ¿Tiene algo que ver con «imponer presencia», intimidar o el porte
   regio del lanzador?
4. En esa misma página, ¿hay algún conjuro **vecino** cuyo nombre empiece por
   «Presencia…»? Si lo hay, dime su nombre exacto y qué hace en una línea.

### Página pdf 324 (= libro 322) — **Prohibición** (Forbiddance)

5. ¿Qué **superficie** y qué **altura** cubre la barrera? Cita la frase completa
   con las cifras y unidades **exactamente como están impresas**.
6. **Pregunta clave:** ¿aparece impresa en la página alguna equivalencia en
   **pies o pies cuadrados** para esa superficie? Contesta de forma tajante: di
   qué unidades aparecen impresas y si hay o no conversión a unidades imperiales.

## Formato del informe

Escribe `agente-V7.md` en este directorio. Para cada pregunta: número, cita
textual entre comillas, y una respuesta de una línea. Al final, una sección
«Extras / ilegible».
