# Auditoría — Especies (especies/especies.yaml)

Agente: agente-H · fecha: 2026-08-21
Páginas leídas: pdf 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199
Elementos revisados: 10 especies / 10, 38 rasgos / 38, 14 linajes / 14

## Hallazgos

### Elfo · cita de página · pdf 191 (YAML) vs pdf 190 (real)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 191, libro: 189}`
- **Dice la página:** El encabezado de sección **«ELFO»** y todo el texto de
  ambientación (los primeros ~9 párrafos: origen de los elfos, altos elfos,
  drows, elfos de los bosques) aparecen en **pdf 190** (pie de página «188»,
  que es una página de ilustración a sangre con dos columnas de texto abajo).
  El bloque «ATRIBUTOS DE LOS ELFOS» con las reglas mecánicas (tipo, tamaño,
  velocidad, rasgos y tabla de linajes) está en **pdf 191** (pie «189»), que es
  la página que cita el YAML.
- **Gravedad:** media — el contenido mecánico citado (rasgos, linajes) sí está
  en pdf 191, así que un lector que solo mire esa página encontrará las reglas
  completas. Pero la especie **empieza** en pdf 190, no en 191, así que la cita
  no señala el comienzo real de la entrada, incumpliendo el mismo criterio que
  se aplicó al resto de especies (todas las demás citan la página donde
  arranca el encabezado de la especie).

### Tiefling · cita de página · pdf 199 (YAML) vs pdf 198 (real)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 199, libro: 197}`
- **Dice la página:** Exactamente el mismo patrón que Elfo. El encabezado
  **«TIEFLING»** y el texto de ambientación (párrafo introductorio + las tres
  secciones de sabor «Abisal», «Ctónico», «Infernal», sin ninguna regla
  mecánica) están en **pdf 198** — página de ilustración a sangre (retrato de
  las tres estirpes) sin número de página visible en el pie, pero que por el
  offset y la secuencia (Orco termina en pdf 197 / libro 195; «Atributos de
  los tieflings» empieza en pdf 199 / libro 197) corresponde a libro 196. El
  bloque «ATRIBUTOS DE LOS TIEFLINGS» con las reglas (tipo, tamaño, velocidad,
  Legado infernal, Presencia sobrenatural, Visión en la oscuridad y la tabla
  de legados) está en **pdf 199**, que es la página que cita el YAML.
- **Gravedad:** media — mismas razones que en Elfo: el contenido mecánico
  citado sí aparece en la página señalada, pero la especie no «empieza» ahí.
  Esto responde directamente a la pista del encargo sobre el salto 197→199:
  en pdf 198 hay contenido de la especie (el encabezado «TIEFLING» y la
  descripción de los tres legados) que no tiene ninguna página citada en el
  YAML, ya que la única `pagina` de la especie es pdf 199.

## Nota `_nota` del Tiefling — comprobada

El campo dice: *"El OCR cortó la velocidad; confirmada en 9 m por lectura
visual."* En pdf 199, el bloque «Atributos de los tieflings» imprime con
total nitidez **«Velocidad: 9 m»**, sin ningún corte ni ambigüedad tipográfica
en la imagen a 170 DPI. La nota sigue siendo **cierta** en cuanto a su
conclusión (9 m está bien), aunque ya no hace falta advertir de nada: no hay
rastro de un problema de OCR al mirar la página directamente — es un dato
plenamente legible. Se podría simplificar o retirar el campo `_nota`, pero
eso lo decide quien mantiene la base.

## Revisados sin hallazgo

Para cada especie se comprobó: tipo de criatura, tamaño, velocidad, alcance de
visión en la oscuridad (si aplica) y el texto de cada rasgo/linaje contra la
imagen de su página.

- **Aasimar** (pdf 188): tipo humanoide ✓, tamaño Mediano 1,2-2,1 m / Pequeño
  60 cm-1,2 m ✓, velocidad 9 m ✓, visión 18 m ✓. Rasgos: Manos curativas,
  Portador de luz, Resistencia celestial, Visión en la oscuridad, Revelación
  celestial (nivel 3, con las tres opciones Alas celestiales/Fulgor
  interior/Mortaja necrótica) — todos correctos, cifras y CD (8 + Carisma +
  PB) incluidas.
- **Dracónido** (pdf 189): tipo humanoide ✓, tamaño Mediano 1,5-2,1 m ✓,
  velocidad 9 m ✓, visión 18 m ✓. Rasgos: Linaje dracónico, Ataque de aliento
  (cono 4,5 m / línea 9x1,5 m, TdS Destreza CD 8+Constitución+PB, 1d10→2d10
  (nivel 5)→3d10 (11)→4d10 (17), usos = PB por descanso largo), Resistencia al
  daño, Visión en la oscuridad, Vuelo dracónico (nivel 5) — todos correctos.
  Tabla «Ancestros dracónicos» (10 filas) verificada íntegra y correcta.
- **Elfo** (contenido en pdf 190-191, ver hallazgo de cita arriba): tipo
  humanoide ✓, tamaño Mediano 1,5-1,8 m ✓, velocidad 9 m ✓, visión 18 m ✓.
  Rasgos: Linaje élfico, Linaje feérico, Sentidos agudos, Trance, Visión en la
  oscuridad — correctos. 3 linajes (Alto elfo, Drow, Elfo de los bosques) con
  sus beneficios de nivel 1/3/5 verificados contra la tabla «Linajes élficos»
  — todos correctos, incluida la subida de visión a 36 m del Drow y de
  velocidad a 10,5 m del Elfo de los bosques.
- **Enano** (pdf 192): tipo humanoide ✓, tamaño Mediano 1,2-1,5 m ✓, velocidad
  9 m ✓, visión 36 m ✓. Rasgos: Afinidad con la piedra (18 m, 10 minutos,
  usos = PB por descanso largo), Aguante enano, Resistencia enana, Visión en
  la oscuridad — todos correctos.
- **Gnomo** (pdf 193): tipo humanoide ✓, tamaño Pequeño 90 cm-1,2 m ✓,
  velocidad 9 m ✓, visión 18 m ✓. Rasgos: Astucia gnoma, Linaje gnomo, Visión
  en la oscuridad — correctos. 2 linajes (Gnomo de las rocas, Gnomo de los
  bosques) verificados contra el texto — correctos, incluidos los detalles del
  dispositivo mecánico (Diminuto, CA 5, 1 pg, hasta 3 activos, se desarman a
  las 8 horas).
- **Goliat** (pdf 194): tipo humanoide ✓, tamaño Mediano 2,1-2,4 m ✓,
  **velocidad 10,5 m ✓** (única especie con velocidad distinta, confirmado),
  sin visión en la oscuridad (correcto, no aparece en la página). Rasgos:
  Constitución poderosa, Forma grande (nivel 5), Linaje gigante — correctos.
  6 linajes gigantes verificados uno por uno contra el texto — todos
  correctos (Abrasión del fuego 1d10 fuego; Caída de las colinas derribada;
  Excursión de las nubes teletransporte 9 m; Frío de la escarcha 1d6 frío +
  reduce velocidad 3 m; Resistencia de la piedra 1d12+Constitución; Trueno de
  la tormenta 18 m, 1d8 trueno).
- **Humano** (pdf 195): tipo humanoide ✓, tamaño Mediano 1,2-2,1 m / Pequeño
  60 cm-1,2 m ✓, velocidad 9 m ✓, sin visión en la oscuridad (correcto).
  Rasgos: Diestro, Ingenioso, Versátil (dote de origen, se recomienda
  Habilidoso) — correctos.
- **Mediano** (pdf 196): tipo humanoide ✓, tamaño Pequeño 60-90 cm ✓,
  velocidad 9 m ✓, sin visión en la oscuridad (correcto). Rasgos: Agilidad de
  mediano, Fortuna, Sigiloso por naturaleza, Valiente — correctos.
- **Orco** (pdf 197): tipo humanoide ✓, tamaño Mediano 1,8-2,1 m ✓, velocidad
  9 m ✓, visión 36 m ✓. Rasgos: Aguante incansable, Descarga de adrenalina
  (usos = PB por descanso corto o largo), Visión en la oscuridad — correctos.
- **Tiefling** (contenido en pdf 198-199, ver hallazgo de cita arriba): tipo
  humanoide ✓, tamaño Mediano 1,2-2,1 m / Pequeño 90 cm-1,2 m ✓, velocidad
  9 m ✓ (nota comprobada, ver arriba), visión 18 m ✓. Rasgos: Legado infernal,
  Presencia sobrenatural, Visión en la oscuridad — correctos. 3 legados
  (Abisal, Ctónico, Infernal) verificados contra la tabla «Legados
  infernales» — todos correctos.

## Dudas / ilegible

Ninguna. Todas las páginas se leyeron con nitidez a 170 DPI. La página pdf 198
no muestra número de página en el pie (es una lámina a sangre), pero su
contenido y posición en la secuencia son inequívocos.
