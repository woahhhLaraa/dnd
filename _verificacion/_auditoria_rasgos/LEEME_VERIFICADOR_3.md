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
pdftoppm -r 170 -f <pag> -l <pag> -png ~/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/v3
```
Genera `/tmp/render/v3-<pag>.png` (relleno con ceros: `v3-296.png`). Léelo con la
herramienta de lectura de imágenes. **`pdftotext` NO es fuente válida** (el OCR de
este PDF es basura). Offset: **página_pdf = página_libro + 2**.

## Preguntas cerradas — contéstalas UNA A UNA con cita textual

### Página pdf 296 (= libro 294)

1. **Inflingir heridas** (Inflict Wounds): ¿de qué característica es la tirada de
   salvación que exige el conjuro? Transcribe la frase completa donde aparece.
2. **Impacto certero** (True Strike): ¿dice la página en algún punto que el ataque
   acierte automáticamente, que no pueda fallar, o que otorgue ventaja?
   Transcribe **el texto completo** del conjuro, de principio a fin.

### Página pdf 306 (= libro 304)

3. **Jaula de fuerza** (Forcecage): ¿qué medida da la página para el **diámetro de
   los barrotes** y para la **separación entre ellos**? Cita la frase literal.
4. **Jaula de fuerza**: la frase sobre huir de la jaula, ¿habla de viaje
   **interplanar** o **intraplanar**? Transcribe la frase completa, palabra por
   palabra, respetando el prefijo exacto.

## Formato del informe

Escribe `agente-V3.md` en este directorio. Para cada pregunta: número, cita
textual entre comillas, y una respuesta de una línea. Al final, una sección
«Extras / ilegible» con cualquier problema de legibilidad o cualquier otra
discrepancia que hayas visto de paso en esas páginas.
