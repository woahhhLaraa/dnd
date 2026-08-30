# Encargo de verificación independiente (oleada 3, Fase 13p)

Eres un **verificador ciego**. NO has visto ningún informe previo y no debes
buscarlo: en este mismo directorio hay ficheros `agente-B*.md` — **no los abras**.
Tu valor está justamente en no saber qué se espera que contestes.

## Regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D.
Si no lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, dilo — **jamás rellenes**.

**No edites ningún fichero de la base.** Solo lees páginas y escribes tu informe.

## Método de lectura

```bash
pdftoppm -r 170 -f <pag> -l <pag> -png ~/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/v4
```
Genera `/tmp/render/v4-<pag>.png` (relleno con ceros: `v4-313.png`). Léelo con la
herramienta de lectura de imágenes. **`pdftotext` NO es fuente válida** (el OCR de
este PDF es basura). Offset: **página_pdf = página_libro + 2**.

## Preguntas cerradas — contéstalas UNA A UNA con cita textual

### Página pdf 313 (= libro 311)

1. **Muro de espinas** (Wall of Thorns): el conjuro inflige daño en dos momentos
   distintos (al aparecer el muro, y al entrar/terminar el turno en él).
   ¿De qué **tipo** es el daño en cada uno de los dos momentos? Transcribe las dos
   frases completas.
2. **Muro de espinas**: transcribe literalmente el párrafo «Con un espacio de
   conjuro de nivel superior».

### Página pdf 314 (= libro 312)

3. **Muro de fuerza** (Wall of Force): ¿existe en la página alguna excepción
   nombrada que pueda destruir o eliminar el muro? Transcribe la frase completa.

### Página pdf 318 (= libro 316)

4. **Palabra de poder: aturdir** (Power Word Stun): ¿qué **estado** exacto impone
   el conjuro al objetivo? Cita la frase literal. ¿Aparece en algún punto de la
   página la palabra «paralizado» o «parálisis» dentro de este conjuro?

## Formato del informe

Escribe `agente-V4.md` en este directorio. Para cada pregunta: número, cita
textual entre comillas, y una respuesta de una línea. Al final, una sección
«Extras / ilegible» con cualquier problema de legibilidad o cualquier otra
discrepancia que hayas visto de paso en esas páginas.
