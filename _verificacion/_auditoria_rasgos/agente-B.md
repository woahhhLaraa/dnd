# Auditoría de rasgos — Clérigo, Druida, Explorador, Hechicero

Agente: agente-B · fecha: 2026-08-21
Páginas leídas: pdf 83, 84, 85, 93, 94, 95, 96, 105, 106, 107, 125, 126, 127
Rasgos revisados: 43 de 43

## Hallazgos

### Druida · Druídico · pdf 93 (YAML) → real: pdf 94
- **Tipo:** cita de página falsa
- **Dice el YAML:** `pagina: {pdf: 93, libro: 91}`
- **Dice la página:** el pdf 93 (libro 91) contiene únicamente "Nivel 1: Lanzamiento de conjuros" (columna derecha completa). El apartado "Nivel 1: Druídico" está en el pdf 94 (pie de página "92"), bajo la tabla "Rasgos de druida", columna izquierda.
- **Gravedad:** media (el contenido del resumen es correcto, pero la cita de página no localiza el rasgo)

### Druida · Orden primigenia · pdf 93 (YAML) → real: pdf 94
- **Tipo:** cita de página falsa
- **Dice el YAML:** `pagina: {pdf: 93, libro: 91}`
- **Dice la página:** "Nivel 1: Orden primigenia" está en el pdf 94 (libro 92), columna izquierda, justo debajo de Druídico, no en el pdf 93.
- **Gravedad:** media

### Druida · Compañero salvaje · pdf 93 (YAML) → real: pdf 94
- **Tipo:** cita de página falsa
- **Dice el YAML:** `pagina: {pdf: 93, libro: 91}`
- **Dice la página:** "Nivel 2: Compañero salvaje" está en el pdf 94 (libro 92), columna derecha.
- **Gravedad:** media

### Druida · Forma salvaje · pdf 93 (YAML) → real: pdf 94
- **Tipo:** cita de página falsa
- **Dice el YAML:** `pagina: {pdf: 93, libro: 91}`
- **Dice la página:** "Nivel 2: Forma salvaje" está en el pdf 94 (libro 92), columna derecha, debajo de Compañero salvaje.
- **Gravedad:** media

> Los cuatro rasgos anteriores están agrupados en la misma página real (pdf 94 / libro 92), la que contiene la tabla "Rasgos de druida". El YAML les puso a los cuatro la página de "Lanzamiento de conjuros" (pdf 93) en vez de la suya. El contenido de los cuatro resúmenes es fiel a lo que dice esa página 94; solo falla la cita.

### Explorador · Maestría con armas · pdf 105 (YAML) → real: pdf 106
- **Tipo:** cita de página falsa
- **Dice el YAML:** `pagina: {pdf: 105, libro: 103}`
- **Dice la página:** el pdf 105 (libro 103) solo cubre "Lanzamiento de conjuros" y el inicio de "Enemigo predilecto". El apartado "Nivel 1: Maestría con armas" está en el pdf 106 (libro 104), bajo la tabla "Rasgos de explorador". Texto de la página: "Tu entrenamiento con armas te permite utilizar las propiedades de maestría con dos tipos de armas de tu elección con las que tengas competencia, como arcos largos y espadas cortas. Tras finalizar un descanso largo, puedes cambiar los tipos de armas elegidas." — coincide con el resumen del YAML, solo cambia la página.
- **Gravedad:** media

## Verificación de las dos citas ya corregidas (Clérigo)

Comprobado con lupa: en el YAML actual, **Orden divina** y **Canalizar divinidad** citan ambas `pdf: 84` (libro 82), y en esa página (pdf 84) aparecen efectivamente los apartados "Nivel 1: Orden divina" y "Nivel 2: Canalizar divinidad", justo debajo de la tabla "Rasgos de clérigo". La corrección es correcta y se mantiene.

## Nota sobre paginación (Druida, pdf 93→96)

El PDF del manual repite físicamente el contenido de las páginas del libro 93 y 94: aparecen una vez en pdf 93/94 y una segunda vez, idénticas, en pdf 95/96 (confirmado por hash de archivo distinto pero contenido visual e impreso idéntico, incluido el pie de página "93"/"94"). Es decir, el "hueco" pdf 94→95 que se preguntaba en el encargo no esconde ningún rasgo perdido: pdf 94 es la página con la tabla + Druídico/Orden primigenia/Compañero salvaje/Forma salvaje (ver hallazgos arriba), y su contenido reaparece duplicado en pdf 96 junto con "Nivel 20: Archidruida". El YAML cita correctamente pdf 95 y pdf 96 para los rasgos de nivel 5 en adelante (coincide con el patrón de offset pdf=libro+2 usado en el resto del fichero), así que esas citas están bien. No hay ningún rasgo de druida sin transcribir.

## Rasgos revisados sin hallazgo

**Clérigo** (9/9): Lanzamiento de conjuros, Orden divina, Canalizar divinidad, Abrasar muertos vivientes, Golpes benditos, Intercesión divina, Golpes benditos mejorados, Don épico, Intercesión divina mayor.

**Druida** (11/11, con 4 hallazgos de cita arriba): Lanzamiento de conjuros, Druídico*, Orden primigenia*, Compañero salvaje*, Forma salvaje*, Resurgimiento salvaje, Furia elemental, Furia elemental mejorada, Conjurar como bestia, Don épico, Archidruida. (*= contenido correcto, cita de página errónea, ver hallazgos)

**Explorador** (15/15, con 1 hallazgo de cita arriba): Lanzamiento de conjuros, Enemigo predilecto, Maestría con armas*, Estilo de combate, Explorador hábil, Ataque adicional, Errante, Pericia, Infatigable, Cazador persistente, Velo de la naturaleza, Cazador preciso, Sentidos salvajes, Don épico, Azote de enemigos. (*= contenido correcto, cita de página errónea, ver hallazgo)

**Hechicero** (8/8): Lanzamiento de conjuros, Hechicería innata, Fuente de magia, Metamagia, Recuperación mágica, Encarnación mágica, Don épico, Apoteosis arcana.

También se comprobó el nivel (`nivel:`) de los 43 rasgos contra la columna "Rasgos de clase" de las cuatro tablas oficiales (pdf 84, 94/96, 106, 126): todos coinciden.

Se revisaron también las cifras mecánicas citadas en los resúmenes (dados de Chispa divina 1d8→2d8/3d8/4d8 por nivel, Golpe divino 1d8→2d8, Golpe primordial 1d8→2d8, puntos de hechicería y tabla "Crear espacios de conjuro", progresión de usos de Canalizar divinidad/Forma salvaje/Enemigo predilecto, dado de Azote de enemigos d6→d10, etc.) contra las tablas y el texto de página: todas coinciden.

## Dudas / ilegible

Ninguna página resultó ilegible a 170 dpi. Una limitación de alcance: el rasgo "Metamagia" del Hechicero (pdf 127) enumera diez opciones; dentro del rango de páginas asignado (125-127) solo pude leer el texto completo de dos opciones (Conjuro acelerado, Conjuro buscador), que coinciden con el YAML. El resto de las opciques de metamagia (Conjuro cuidadoso, distante, extendido, gemelo, intensificado, potenciado, sutil, transmutado) están descritas en páginas posteriores (128+), fuera de mi asignación, así que no pude verificar su texto contra el YAML — lo señalo por si otro agente cubre esas páginas.
