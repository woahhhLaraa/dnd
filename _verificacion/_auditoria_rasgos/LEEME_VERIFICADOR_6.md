# Encargo de verificación independiente (oleada 3, lote B1)

Eres un **verificador ciego**. NO has visto ningún informe previo y no debes
buscarlo: en este mismo directorio hay ficheros `agente-B*.md` y `agente-A*.md`
— **no los abras**. Tu valor está justamente en no saber qué se espera que
contestes.

## Regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D.
Si no lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, dilo — **jamás rellenes**.

**No edites ningún fichero de la base.** Solo lees páginas y escribes tu informe.

## Método de lectura

```bash
pdftoppm -r 170 -f <pag> -l <pag> -png ~/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/v6
```
Genera `/tmp/render/v6-<pag>.png` (relleno con ceros: `v6-309.png`). Léelo con la
herramienta de lectura de imágenes. **`pdftotext` NO es fuente válida** (el OCR de
este PDF es basura). Offset: **página_pdf = página_libro + 2**.

Si un conjuro empieza en una página y sigue en la siguiente, **renderiza también
la siguiente** y transcríbelo entero. No des por terminado un conjuro que se
corta al pie de una columna.

## Preguntas cerradas — contéstalas UNA A UNA con cita textual

### Página pdf 309 (= libro 307) — **Mal de ojo** (Eyebite)

1. El conjuro ofrece varias **opciones de efecto** entre las que elegir.
   **Transcribe el nombre EXACTO de cada opción tal y como está impreso** (suelen
   ir en negrita o cursiva), y a continuación el texto completo de cada una.
   Copia los nombres literalmente, sin normalizarlos ni traducirlos.

### Página pdf 312 (= libro 310) — **Mensajero animal** (Animal Messenger)

2. ¿Qué **distancia** recorre la bestia por cada 24 horas, y qué distancia si
   puede volar? Cita la frase completa con las cifras y unidades exactas tal como
   están impresas.

### **Mente en blanco** (Mind Blank) — busca el conjuro; puede estar en pdf 312 (= libro 310) o pdf 313 (= libro 311)

3. **Transcribe el texto COMPLETO del conjuro**, de la cabecera al final, palabra
   por palabra. Dime en qué página pdf lo has encontrado y qué número aparece
   impreso en el pie de esa página.
4. Sobre ese texto, contesta explícitamente:
   - ¿La protección se enuncia contra **«conjuros de adivinación»** en bloque, o
     contra algo más concreto? Cita la frase exacta.
   - ¿Aparece alguna cláusula sobre **observar al objetivo desde lejos**
     (escudriñar / observación remota)? Si aparece, cítala entera; si no aparece
     en absoluto, dilo de forma tajante.

## Formato del informe

Escribe `agente-V6.md` en este directorio. Para cada pregunta: número, cita
textual entre comillas, y una respuesta de una línea. Al final, una sección
«Extras / ilegible» con cualquier problema de legibilidad o cualquier otra
discrepancia que hayas visto de paso en esas páginas.
