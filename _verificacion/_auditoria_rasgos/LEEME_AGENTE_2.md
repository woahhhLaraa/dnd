# Encargo: auditar subclases y especies contra la página del manual

Lee esto entero antes de empezar. Tu asignación concreta viene en el mensaje
que te ha lanzado.

Esta es la **segunda tanda**. La primera auditó los 158 rasgos del tronco de
clase y encontró 10 defectos en 158 (6,3 %): **nueve eran citas de página
equivocadas** y uno era prosa que contradecía la propia tabla del fichero. El
texto mecánico estaba bien. Ese es el patrón que se espera aquí también, así
que **las citas de página son la prioridad número uno**.

## Qué es esto y por qué importa

`clases/subclases/<clase>.yaml` y `especies/especies.yaml` son las dos mayores
superficies de la base que **ninguna fuente externa puede confirmar**: el SRD
solo trae 12 de nuestras 48 subclases y no cubre los rasgos de especie. La
única autoridad es la página del Manual del Jugador.

## ⛔ La regla que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses NADA de lo que creas saber sobre D&D. Si no
lo has leído en la imagen de la página, no existe. Si algo no se lee con
claridad, se marca como ilegible y se pregunta — **jamás se rellena**.

Si te descubres pensando «esto es así porque en D&D funciona así», para: eso es
justo el fallo que esta auditoría existe para detectar. Recuerda que 2024
cambió muchas reglas respecto a 2014, y el modelo «recuerda» la versión vieja.

## Cómo leer una página

```bash
mkdir -p /tmp/render
cd /home/larita/Documents/DnD
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png Manual_del_Jugador_2024.pdf /tmp/render/p
```

Genera `/tmp/render/p-<pag>.png` (ceros a 3 dígitos: `p-056.png`). Ábrelo con
la herramienta de lectura de imágenes (Read).

- **`-r 170` es la resolución mínima legible.** No bajes de ahí.
- **`pdftotext` NO es fuente válida** (OCR basura, escaneo a 96 DPI). Solo
  sirve para localizar en qué página está algo.
- **Offset confirmado en TODO el manual: `página_pdf = página_libro + 2`.**
  Los `pagina.pdf` del YAML ya son números de PDF: úsalos tal cual. En la
  primera tanda un agente creyó encontrar páginas duplicadas en el PDF y era
  falso — el offset no tiene excepciones. Si algo parece no cuadrar, es que la
  cita está mal, no el offset.
- **Una subclase suele ocupar más de una página.** Si el texto continúa,
  renderiza también la siguiente. No des un rasgo por ausente sin haber mirado
  la página de al lado.

## Estructura de lo que auditas

**Subclases** (`clases/subclases/<clase>.yaml`): cada subclase tiene `nombre`,
`lema`, **una sola `pagina`** y una lista de `rasgos`, cada uno con `nivel` y
`desc`. Ojo: la página va en la subclase, no en cada rasgo — así que la cita
que compruebas es **dónde empieza la subclase**.

**Especies** (`especies/especies.yaml`): cada especie tiene `nombre`, `pagina`,
`tipo`, `tamano`, `velocidad_m`, `rasgos` (con `nombre` y `desc`) y a veces
`linajes`. Los linajes también son contenido a verificar.

## Qué SÍ es un hallazgo

El texto es un **resumen condensado deliberado**, no una transcripción literal.
Por tanto:

1. **Cita de página falsa** — la subclase (o la especie) no empieza donde dice
   `pagina.pdf`. **Es el defecto más frecuente: compruébalo en todas, una por una.**
2. **Cifras y dados equivocados** — un `2d6` que en la página es `1d6`, 9 m que
   son 18 m, un número de usos distinto.
3. **Nivel equivocado** — el `nivel:` de un rasgo de subclase no coincide con
   el nivel al que la página lo concede. (Los niveles de subclase de cada clase
   están en `niveles_de_subclase` del propio fichero.)
4. **Condición o mecánica cambiada** — «tirada de salvación de Constitución»
   donde la página dice Destreza; «acción adicional» donde dice «acción»; una
   condición que la página exige y el resumen omite, o al revés.
5. **Rasgo, subclase, lineaje o especie que falta o que sobra.**
6. **Un resumen que cambia el sentido** aunque no haya cifras.
7. **Datos de especie mal leídos** — velocidad, tamaño, tipo de criatura, y muy
   en particular el alcance de la visión en la oscuridad.

## Qué NO es un hallazgo

- Que la redacción no sea literal. **Es condensado a propósito.**
- Que falte prosa de ambientación, ejemplos o el texto de sabor.
- Que el resumen sea más corto. Solo importa si pierde o cambia una mecánica.
- El `lema` de una subclase: es una frase de sabor, no una regla.

## Cómo entregar

**NO edites ningún fichero de la base.** No toques `clases/`, `especies/`, ni
nada fuera de tu informe. Las correcciones las aplica quien te ha lanzado, tras
releer él mismo cada página que señales.

Escribe **un solo fichero**:
`_verificacion/_auditoria_rasgos/<tu-id>.md`

```markdown
# Auditoría — <lo que te tocó>

Agente: <tu-id> · fecha: 2026-08-21
Páginas leídas: pdf 56, 57, ...
Elementos revisados: N de N

## Hallazgos

### <Clase/Especie> · <Subclase o rasgo> · pdf <pág>
- **Tipo:** cita de página | cifra | nivel | mecánica | falta | sobra | ilegible
- **Dice el YAML:** «...»
- **Dice la página:** «...» (cita textual de lo que has leído)
- **Gravedad:** alta (cambia el resultado en mesa) | media | baja

## Revisados sin hallazgo
<lista, para saber qué se ha mirado de verdad>

## Dudas / ilegible
```

Si no encuentras nada, dilo explícitamente y **lista igualmente lo revisado**.
Un informe vacío sin lista no sirve.

## Antes de terminar

¿Has abierto **todas** las páginas de tu asignación, y las siguientes cuando el
texto continuaba? ¿Has comprobado la cita de **cada** subclase o especie, no
solo de las que te llamaron la atención? ¿Alguno de tus hallazgos se apoya en
lo que «sabes» de D&D en vez de en la imagen? Si es que sí, quítalo o vuelve a
mirar la página.

**Y sobre todo:** si vas a explicar *por qué* algo no cuadra, comprueba la
explicación igual que el hallazgo. En la primera tanda un agente acertó el
hallazgo y se inventó la causa; eso costó tiempo de verificación.
