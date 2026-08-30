# Encargo: la línea de Componentes de los conjuros fuera del SRD

Encargo corto y muy acotado. **Solo una línea por conjuro.** No audites la
descripción, ni las clases, ni nada más.

## Por qué existe

`verificar_foundry.py` contrasta desde el 2026-08-29 el **coste del componente
material** contra el SRD 5.2 — 309 conjuros, 303 coinciden. Pero **33 conjuros
de la base no están en el SRD**, así que ninguna fuente externa puede
comprobarlos. Todos tienen componente material y `coste: null`, y esa
combinación puede significar dos cosas distintas:

- **el material no cuesta nada** (lo normal: «una pizca de fósforo»), o
- **el coste se perdió en la conversión del CSV**.

Ya pasó una vez: *Golpe de viento acerado* tenía `coste: null` sobre una página
que exige «un arma cuerpo a cuerpo que valga al menos **1 pp**». Lo encontró una
muestra aleatoria, por casualidad. Esto cierra la bolsa entera.

## ⛔ Las reglas que no puedes romper

**CONSULTAR, NO RECORDAR.** No uses nada de lo que creas saber sobre D&D, ni el
SRD inglés. Si no lo has leído en la imagen, no existe.

**LEER, NO DEDUCIR.** Transcribe lo impreso. Nunca digas qué «debería» decir.

**NO CALCULES NADA.** Si la página dice «50 po **cada uno**» de un par de
anillos, tu respuesta es «50 po cada uno», **nunca «100 po»**. Este error existe
de verdad en la base (*Vínculo protector*) y se detectó justamente porque
alguien había sumado en vez de transcribir.

**NO EDITES NINGÚN FICHERO DE LA BASE.** Solo escribes tu informe.

Si una cifra no se lee con seguridad total, **sube a `-r 220` o recorta la
región** antes de darla por buena. Si aun así no se lee, márcala como ilegible.

## Cómo leer

```bash
pdftoppm -r 170 -f <pag_pdf> -l <pag_pdf> -png \
  /home/larita/Documents/DnD/Manual_del_Jugador_2024.pdf /tmp/render/<tu-id>
```

Lee el PNG con la herramienta de imágenes. `pdftotext` **NO** es fuente válida.
Offset: `página_pdf = página_libro + 2`.

La línea que buscas está en la cabecera del conjuro, justo debajo del nombre y
la escuela, con el formato:

> **Componentes:** V, S, M (una pizca de fósforo)

## Qué contestar, por cada conjuro

1. **Transcribe la línea `Componentes` COMPLETA**, palabra por palabra,
   incluido todo lo que va dentro del paréntesis.
2. Contesta las tres preguntas, por separado:
   - **¿El material tiene un coste mínimo?** Si lo tiene, di la **cifra y la
     unidad exactamente como se imprimen** (`po`, `pp`, `pc`). Si no lo tiene,
     di «sin coste» de forma tajante.
   - **¿Se consume** como parte del conjuro? Sí o no, con la frase que lo diga.
   - **¿El coste es por unidad o por conjunto?** Solo si la página usa
     expresiones como «cada uno», «por cadáver», «por objetivo». Si no dice nada
     de eso, di «coste único».

## Cómo entregar

Escribe `agente-<tu-id>.md` en este directorio:

```markdown
# Costes de material — lote <tu-id>

Agente: <tu-id> · fecha: 2026-08-29
Páginas leídas: pdf ...
Conjuros revisados: N de N

## <Nombre> · pdf <pág>
- **Componentes (literal):** «V, S, M (...)»
- **Coste:** sin coste | N po|pp|pc
- **Se consume:** sí | no
- **Por unidad:** coste único | «cada uno» / «por X»

## Dudas / ilegible
```

**Todos los conjuros de tu lote deben aparecer**, tengan coste o no. Un «sin
coste» comprobado es un resultado tan útil como un hallazgo: es lo que permite
cerrar la bolsa en vez de dejarla en «no se sabe».
