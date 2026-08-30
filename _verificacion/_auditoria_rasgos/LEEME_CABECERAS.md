# Encargo: pasada de cabeceras (nombres y resúmenes)

Esto **no** es una auditoría de descripciones. Es una pasada rápida y ancha
sobre dos campos que las oleadas anteriores no miraron de verdad.

## Por qué existe este encargo

Dos deudas que salieron a la luz el 2026-08-29:

1. **El `nombre` del conjuro nunca ha sido campo auditable.** La lista de campos
   de todos los briefings anteriores era `descripcion | clases | tirada |
   resumen | material`. El nombre no estaba. Y sin embargo la base lleva **7
   erratas de nombre corregidas** (`Adiviniación`, `Baile irresistibile`,
   `Flecha acida`, `Fuente de la luz lunar`, `Hablar con animales`, y
   `Poliformar` → **Polimorfar** en dos registros). **Las 7 se encontraron de
   rebote, ninguna buscándolas.**

2. **El `resumen` estaba en el briefing pero nadie lo miró.** Las oleadas 1 y 2
   declararon **0 defectos de resumen en 131 conjuros**. La oleada 3 midió
   **4 en 69 (5,8 %)**. Si esa tasa fuera real, la probabilidad de ver cero en
   131 es **0,0004**, y el límite superior compatible con 0/131 es 2,26 % — los
   intervalos **no se solapan**. La conclusión es que el campo se dio por bueno
   sin abrirlo.

Tu lote son conjuros **cuya descripción ya está auditada**. No la vuelvas a
leer. Vas solo a por la cabecera y el resumen.

## ⛔ Las reglas que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D, ni el
SRD inglés. Si no lo has leído en la imagen de la página, no existe.

**LEER, NO DEDUCIR.** Si te preguntas si un nombre está bien escrito, la
respuesta es «la página imprime X», nunca «debería ser Y».

**NO EDITES NINGÚN FICHERO DE LA BASE.** Ni `hechizos.json`, ni los `.yaml`, ni
los `.py`. Solo escribes tu informe.

**Si algo no se lee con claridad, márcalo como ilegible.** Jamás rellenes.

## Cómo leer

```bash
mkdir -p /tmp/render
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png \
  /home/larita/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Genera `/tmp/render/<tu-id>-<pag>.png`. Ábrelo con la herramienta de lectura de
imágenes (Read).

- **`-r 170` es la resolución mínima legible.** Si una cabecera no se lee con
  seguridad, sube a `-r 220` antes de declararla ilegible.
- **`pdftotext` NO es fuente válida** (el OCR de este PDF es basura).
- **Offset: `página_pdf = página_libro + 2`.**
- Tu lote es contiguo: **renderiza cada página una vez** y despacha de golpe
  todos los conjuros que estén en ella.

## Qué comprobar, y solo esto

Los datos están en `/home/larita/Documents/DnD/base-canonica/hechizos.json`
(busca cada conjuro por `nombre`).

### 1. `nombre` — letra a letra

Compara el `nombre` de la base con la **cabecera impresa**, carácter a carácter.
Te importan:

- **letras cambiadas o transpuestas** (`Poliformar` por `Polimorfar`,
  `irresistibile` por `irresistible`);
- **tildes** que falten o sobren (`Adivinacion`, `acida`);
- **artículos y preposiciones** de más o de menos (`Fuente de la luz lunar` vs
  `Fuente de luz lunar`);
- **mayúsculas** en nombres propios.

**No es hallazgo** que la base escriba el nombre con la primera letra en
mayúscula y el manual lo imprima todo en versales: eso es tipografía, no
ortografía. Compara las **letras**, no la caja.

### 2. `resumen` — ¿lo contradice la página?

El `resumen` es un campo **nuestro**, de una línea. No aparece en el manual y no
tiene que aparecer. **Solo es hallazgo si contradice a la página.** Busca:

- **un efecto que la página no concede** — *Impacto certero* resumía «el golpe
  no falla» y la página no da acierto automático;
- **una excepción negada** — *Muro de fuerza* decía «nada puede romperlo» y la
  página nombra *desintegrar*;
- **un estado o término cambiado** — *Palabra de poder: aturdir* decía
  «paraliza» y el estado es **aturdido** (son dos estados distintos del manual);
- **el resumen de otro conjuro** — *Presciencia* llevaba el de *Presencia regia
  de Yolande*, impreso al lado. **Si dos conjuros de tu página tienen nombres
  parecidos, cotéjalos también el uno contra el otro.**

**No es hallazgo** que el resumen sea breve, poético, incompleto, o que no
aparezca en la página. Solo que **diga algo falso**.

Para juzgarlo te basta leer la cabecera y las primeras frases del conjuro: no
necesitas auditar el párrafo entero.

## Cómo entregar

Escribe **un solo fichero**:
`/home/larita/Documents/DnD/base-canonica/_verificacion/_auditoria_rasgos/agente-<tu-id>.md`

```markdown
# Pasada de cabeceras — lote <tu-id>

Agente: <tu-id> · fecha: 2026-08-29
Páginas leídas: pdf ...
Conjuros revisados: N de N

## Hallazgos

### <Nombre en la base> · pdf <pág>
- **Campo:** nombre | resumen
- **Dice la base:** «...»
- **Dice la página:** «...» (cita textual de la cabecera o del texto)
- **Gravedad:** alta | media | baja

## Revisados sin hallazgo
<lista de nombres, para que conste que se miraron uno a uno>

## Dudas / ilegible
```

**Importante:** la lista de «Revisados sin hallazgo» tiene que llevar **todos**
los conjuros de tu lote. Un informe que solo trae hallazgos no permite
distinguir «lo miré y estaba bien» de «no lo miré» — que es justo el problema
que este encargo viene a arreglar.
