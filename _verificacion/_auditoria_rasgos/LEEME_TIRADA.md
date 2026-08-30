# Encargo: ¿qué dispara cada conjuro? (semántica del campo `tirada`)

Encargo corto y muy acotado. **Una sola pregunta por conjuro.**

## Contexto: qué se está decidiendo

Cada conjuro de la base tiene un campo `tirada`. La mayoría dice `"Directo"`, y
ese valor **nunca se definió**. Se ha fijado ahora esta lectura:

> **`TdS <característica>`** — la tirada de salvación **decide si el conjuro
> afecta al objetivo**. Es el disparador: si la supera, no le pasa (o no le pasa
> lo principal).
>
> **`Directo`** — el conjuro **se manifiesta igualmente**, sin que ninguna tirada
> lo dispare. Puede haber salvaciones después, pero son para **modular el daño**
> o para **librarse de un estado ya aplicado**, no para evitar el conjuro.

Ejemplos ya resueltos, para que calibres:

| Conjuro | Valor | Por qué |
|---|---|---|
| *Hechizar persona* | `TdS Sab.` | la salvación decide si queda hechizado |
| *Muro de fuego* | `Directo` | el muro **aparece igual**; la salvación es de quien esté en su área |
| *Palabra de poder: matar* | `Directo` | el efecto es automático según los puntos de golpe |
| *Esfera de llamas* | ? | **tuyo** |

## ⛔ Las reglas que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D, ni el
SRD inglés. Si no lo has leído en la imagen de la página, no existe.

**LEER, NO DEDUCIR.** Transcribe lo impreso. Nunca digas qué «debería» decir.

**NO EDITES NINGÚN FICHERO DE LA BASE.** Solo escribes tu informe.

Si algo no se lee con claridad, márcalo como ilegible. **Jamás rellenes.**

## Cómo leer

```bash
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png \
  /home/larita/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Lee el PNG con la herramienta de imágenes. `pdftotext` **NO** es fuente válida.
Offset: `página_pdf = página_libro + 2`. Si el conjuro se corta al pie de una
columna, renderiza también la página siguiente.

## Qué tienes que contestar, por cada conjuro de tu lista

1. **Transcribe la primera frase donde aparece una tirada de salvación**, entera
   y literal, con lo que viene inmediatamente después (qué pasa si la falla y
   qué pasa si la supera).

2. **Contesta a esta pregunta, y solo a esta:**

   > ¿Esa tirada de salvación **decide si el conjuro afecta al objetivo**, o el
   > efecto **se produce igualmente** y la tirada solo reduce el daño / evita un
   > estado añadido?

   Responde con una de estas tres etiquetas, y justifícala con la cita:
   - **DISPARADOR** — si la supera, el conjuro no le afecta (o no le hace lo
     principal). Ej.: «deberá superar una tirada de salvación de Sabiduría **o**
     quedará hechizado».
   - **MODULA** — el efecto ocurre igual; la salvación solo cambia cuánto daño
     recibe o si sufre un estado adicional. Ej.: «sufrirá 8d6 si la falla **o la
     mitad** si la supera» sobre un conjuro que crea un muro o un área.
   - **DUDOSO** — no lo distingues con claridad. **Es una respuesta válida y
     preferible a adivinar**; explica por qué dudas.

3. Si el conjuro tiene **más de una** tirada de salvación, di cuál es la primera
   y qué papel juega **cada una**.

## Cómo entregar

Escribe `agente-<tu-id>.md` en este directorio:

```markdown
# Semántica de `tirada` — lote <tu-id>

Agente: <tu-id> · fecha: 2026-08-29
Páginas leídas: pdf ...

## <Nombre del conjuro> · pdf <pág>
- **Cita:** «...»
- **Veredicto:** DISPARADOR | MODULA | DUDOSO
- **Por qué:** una o dos líneas
- **Otras salvaciones del conjuro:** (si las hay)

## Dudas / ilegible
```
