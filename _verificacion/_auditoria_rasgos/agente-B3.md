# Auditoría de descripciones (Fase 13p) — lote B3

Agente: B3 · fecha: 2026-08-27
Páginas leídas: pdf 318, 319, 320, 321 (libro 316-319; 321 se renderizó para comprobar
si algún conjuro se cortaba al final de página 320 — ninguno de mi lote lo hacía).
Conjuros revisados: 14 de 14

## Hallazgos

### Palabra de poder: aturdir · pdf 318

- **Campo:** resumen
- **Modo de fallo:** otro (el resumen nombra un estado distinto al que aplica la página)
- **Dice la base:** resumen = «Una sílaba que paraliza.»
- **Dice la página:** «Abrumas la mente de una criatura que puedas ver dentro del alcance. Si el objetivo tiene 150 puntos de golpe o menos, tendrá el estado de aturdido. [...] El objetivo aturdido hace una tirada de salvación de Constitución al final de cada uno de sus turnos [...]». La página nunca usa la palabra «paraliza» ni «parálisis»; el estado que impone es «aturdido», que es un estado distinto de «paralizado» en el manual (ambos existen como estados separados).
- **Gravedad:** baja — el campo `descripcion` en sí es correcto («tendrá el estado de aturdido»), el error está solo en el resumen decorativo, pero puede inducir a confundir el estado aplicado con el de Paralizado si alguien solo lee el resumen.

## Revisados sin hallazgo

- Orden imperiosa (pdf 318) — clases, tirada («TdS Sab.» cuadra con «tirada de salvación de Sabiduría»), las 5 órdenes (Acércate, Detente, Huye, Póstrate, Suelta) y el párrafo de mejora por espacio superior cuadran palabra por palabra con la página.
- Oscuridad (pdf 318) — clases, descripción (esfera de 4,5 m, emanación de 4,5 m, disipación de luces de nivel 2 o inferior) cuadran con la página.
- Palabra de curación (pdf 318) — clases, descripción y mejora por espacio superior (2d4 por nivel) cuadran.
- Palabra de curación en masa (pdf 318) — clases, descripción y mejora por espacio superior (1d4 por nivel sobre 3) cuadran.
- Palabra de poder: matar (pdf 319) — clases, descripción (100 pg / 12d12 psíquico) cuadran exactamente.
- Palabra de poder: sanar (pdf 319) — clases, descripción (recupera todos los pg, termina asustada/aturdida/envenenada/hechizada/paralizada, reacción para levantarse) cuadran.
- Palabra de regreso (pdf 319) — clases, descripción (hasta 5 criaturas voluntarias a 1,5 m, santuario designado previamente) cuadran. Conversión 1,5 m / 5 pies es aritméticamente correcta.
- Palabra divina (pdf 319) — clases, tirada («TdS Car.»), descripción y tabla «Efectos de palabra divina» (0-20 muere, 21-30 aturdido/cegado/ensordecido 1 h, 31-40 cegado/ensordecido 10 min, 41-50 ensordecido 1 min) cuadran con la página (el orden en la base está invertido respecto a la tabla del libro, pero el contenido de cada franja es idéntico — no es hallazgo).
- Parar el tiempo (pdf 319) — clases, descripción (1d4+1 turnos, termina si afecta a otra criatura/objeto ajeno, o si te alejas más de 300 m) cuadran. Conversión 300 m / 1000 pies es aritméticamente correcta (misma tasa que el resto del libro).
- Pasamuros (pdf 319-320) — clases, descripción íntegra revisada con atención especial por el aviso del encargo: las tres dimensiones de la base («1,5 m / 5 pies» de ancho, «2,4 m / 8 pies» de alto, «6 m / 20 pies» de largo) cuadran exactamente con los valores en metros de la página («hasta 1,5 m de ancho, 2,4 m de alto y 6 m de largo») y las conversiones a pies son aritméticamente correctas. No queda rastro de la conversión falsa mencionada («45 pies»); el resto del texto (aparición del pasaje, ausencia de inestabilidad, expulsión sin daño al terminar) también cuadra.
- Paso arbóreo (pdf 320) — clases, descripción íntegra (150 m/500 pies, gasto de 1,5 m/5 pies de movimiento, una sola vez por turno, debe terminar el turno fuera de un árbol) cuadra con el texto que continúa entre las dos columnas de la página 320.
- Paso brumoso (pdf 320) — clases, descripción (teletransporte hasta 9 m/30 pies a espacio sin ocupar que puedas ver) cuadra.
- Patrón hipnótico (pdf 320) — clases y descripción (cubo de 9 m/30 pies, salvación de Sabiduría, estado de hechizadas con velocidad 0 e incapacitadas, termina si reciben daño o alguien las sacude) cuadran con la página.

## Dudas / ilegible

- **Patrón hipnótico:** `tirada` = «Directo», pero la descripción exige explícitamente «una tirada de salvación de Sabiduría» como mecánica de resolución. Según el criterio del encargo, esto se reporta en dudas y no en hallazgos porque ya está contado aparte como decisión de diseño pendiente sobre el valor «Directo».
- **Orden imperiosa:** el campo `fuente.pagina_libro` trae el valor `"316*"` (con asterisco), a diferencia del resto de mi lote que no lo llevan. No sé qué codifica ese asterisco; no es un campo de mi auditoría pero lo señalo por si es relevante para otra fase.
- Ningún conjuro de mi lote presentó texto ilegible en el render a 170 dpi.
