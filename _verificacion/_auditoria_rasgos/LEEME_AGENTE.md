# Encargo: auditar los rasgos de clase contra la página del manual

Lee esto entero antes de empezar. Tu asignación concreta (qué clases te tocan)
viene en el mensaje que te ha lanzado.

## Qué es esto y por qué importa

`clases/rasgos/<clase>.yaml` guarda el **texto de los 158 rasgos del tronco de
clase** de D&D 2024 en castellano. Se transcribieron por lectura visual el
2026-08-19 y **nadie los ha vuelto a mirar desde entonces**. Ninguna fuente
externa puede confirmarlos: el SRD no los cubre. La única autoridad es la
página del Manual del Jugador.

Es además la zona de mayor riesgo del proyecto, por un motivo concreto: es
**exactamente donde las reglas cambiaron de 2014 a 2024** (Furia, Ataque
furtivo, Maestrías con armas — que en 2014 ni existían). Un modelo que tire de
su conocimiento previo rellenará huecos con la edición equivocada y sonará
perfectamente convincente al hacerlo.

## ⛔ La regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Si te descubres pensando «esto es así porque en D&D funciona así», para: eso es
justo el fallo que esta auditoría existe para detectar.

## Cómo leer una página

```bash
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/p
```

Genera `/tmp/render/p-<pag>.png` (rellena con ceros a 3 dígitos: `p-053.png`).
Ábrelo con la herramienta de lectura de imágenes (Read).

- **`-r 170` es la resolución mínima legible.** No bajes de ahí.
- **`pdftotext` NO es fuente válida**: el OCR de este PDF es basura (escaneo a
  96 DPI). Solo sirve para localizar en qué página está algo, nunca para leer
  un dato.
- **Offset confirmado en todo el manual: `página_pdf = página_libro + 2`.**
  Los `pagina.pdf` del YAML ya son números de PDF: úsalos tal cual.

Crea `/tmp/render` si no existe. Puedes renderizar varias páginas de golpe.

## Qué SÍ es un hallazgo

El campo `fidelidad: condensado` de estos ficheros es **deliberado**: el texto
es un resumen mecánico, no una transcripción literal. Por tanto:

1. **Cifras y dados equivocados** — un `2d6` que en la página es `1d6`, un
   alcance de 9 m que son 18 m, un número de usos distinto.
2. **Nivel equivocado** — el `nivel:` del rasgo no coincide con el nivel al que
   la página (o la tabla de la clase) lo concede.
3. **Cita de página falsa** — el rasgo no está en la página que dice `pagina.pdf`.
   **Esto ya ha pasado**: dos rasgos del Clérigo citaban páginas erróneas.
   Compruébalo en todos.
4. **Condición o mecánica cambiada** — «tirada de salvación de Constitución»
   donde la página dice Destreza; «acción adicional» donde dice «acción»;
   una condición que la página exige y el resumen omite, o al revés.
5. **Rasgo que falta o que sobra** — la página describe un rasgo del tronco de
   clase que no está en el YAML, o el YAML tiene uno que no aparece.
6. **Un resumen que cambia el sentido** aunque no haya cifras de por medio.

## Qué NO es un hallazgo

- Que la redacción no sea literal. **Es condensado a propósito.** No reportes
  «el manual lo dice con otras palabras».
- Que falte prosa de ambientación o ejemplos.
- Que el resumen sea más corto. Solo importa si pierde o cambia una mecánica.
- Rasgos de **subclase** (viven en `clases/subclases/`, no te tocan).

## Cómo entregar

**NO edites ningún fichero de la base.** No toques `clases/`, `hechizos.json`,
ni nada fuera de tu informe. Las correcciones las aplica quien te ha lanzado,
tras revisarlas.

Escribe **un solo fichero**:
`_verificacion/_auditoria_rasgos/<tu-id>.md`

con esta forma:

```markdown
# Auditoría de rasgos — <clases que te tocaron>

Agente: <tu-id> · fecha: 2026-08-21
Páginas leídas: pdf 53, 54, 55, ...
Rasgos revisados: N de N

## Hallazgos

### <Clase> · <Nombre del rasgo> · pdf <pág>
- **Tipo:** cifra | nivel | cita de página | mecánica | falta | sobra | ilegible
- **Dice el YAML:** «...»
- **Dice la página:** «...» (cita textual de lo que has leído)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Rasgos revisados sin hallazgo
<lista de nombres, para saber qué se ha mirado de verdad>

## Dudas / ilegible
<lo que no hayas podido leer con claridad>
```

Si no encuentras nada, dilo explícitamente y lista igualmente los rasgos
revisados. Un informe vacío sin lista no sirve: hay que poder saber qué se
miró.

## Antes de terminar

Repasa: ¿has abierto **todas** las páginas de tu asignación? ¿Has comprobado la
cita de página de **cada** rasgo, no solo de los que te llamaron la atención?
¿Alguno de tus hallazgos se apoya en lo que «sabes» de D&D en vez de en la
imagen? Si es que sí, quítalo o vuelve a mirar la página.
