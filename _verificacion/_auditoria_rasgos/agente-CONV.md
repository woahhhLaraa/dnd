# Verificación de conversiones de unidad — agente CONV

Fecha: 2026-08-27
Páginas leídas: pdf 242, 272, 273, 279, 280 (=282 numeración lógica, ver nota), 282, 307, 319, 320, 326, 328, 329, 337

Nota sobre el caso retirado: el coordinador indicó que **Alarma** (libro 240 → pdf 242) era un falso positivo de su script («5.000» leído como «5,0» por el punto de millar). Ya había renderizado y leído esa página antes del aviso, así que lo confirmo aquí: la página 242 sí dice «La alarma te avisará con un sonido dentro de tu mente si estás a 1,5 km o menos de la zona vigilada», sin cifra en pies en ese punto — pero como el coordinador ya determinó que la base es correcta (1,5 km = 5.000 pies, con punto de millar mal parseado por el script), no lo incluyo como hallazgo. Lo dejo fuera de la tabla de resultados por instrucción explícita.

## Resultados

### Detectar magia · pdf 272
- **Dice la base:** «Hasta que el conjuro termine, podrás percibir la presencia de efectos mágicos a 9 m / 30 pies o menos de ti. [...] El conjuro no puede atravesar 30 cm / 11 pulgadas de piedra, tierra o madera, 2,5 cm / 0,9 pulgada de metal o una lámina fina de plomo.»
- **Dice la página (cita textual):** «Hasta que el conjuro termine, podrás percibir la presencia de efectos mágicos a 9 m o menos de ti. Si percibes alguno, puedes usar una acción de magia para ver una débil aura alrededor de cualquier objeto o criatura visible dentro de la zona que esté afectada por la magia y, si el efecto lo creó un conjuro, distingues a qué escuela mágica pertenece. El conjuro no puede atravesar 30 cm de piedra, tierra o madera, 2,5 cm de metal o una lámina fina de plomo.»
- **¿Trae la página conversión a pulgadas (o a pies, en el otro punto)?** No, en ningún caso. Solo cifras métricas: 9 m, 30 cm, 2,5 cm.
- **Veredicto:** la base añade dos conversiones que el manual no trae («11 pulgadas» y «0,9 pulgada»). El mismo texto («El conjuro no puede atravesar 30 cm de piedra, tierra o madera, 2,5 cm de metal o una lámina fina de plomo») aparece también en Detectar el bien y el mal y en Detectar pensamientos en páginas vecinas, siempre sin conversión a pulgadas, lo que corrobora que la fórmula estándar del manual no lleva esa conversión.

### Disco flotante de Tenser · pdf 273
- **Dice la base:** «Este conjuro crea un plano de fuerza horizontal de 90 cm / 1 pie de diámetro y 2,5 cm / 1 pulgada de grosor que flota 90 cm / 1 pie por encima del suelo [...]»
- **Dice la página (cita textual):** «Este conjuro crea un plano de fuerza horizontal de 90 cm de diámetro y 2,5 cm de grosor que flota 90 cm por encima del suelo en un espacio sin ocupar de tu elección que puedas ver dentro del alcance.»
- **¿Trae la página conversión a pies?** No. Ni en el diámetro ni en la altura de flotación. (El grosor de 2,5 cm tampoco lleva conversión a pulgadas en la página, aunque ese punto no era parte de la pregunta.)
- **Veredicto:** la base añade una conversión que el manual no trae, dos veces («90 cm / 1 pie» en dos ocasiones).

### Localizar criatura · pdf 307
- **Dice la base:** «Puedes localizar una criatura específica que conozcas o la más cercana de un tipo que hayas visto de cerca 3 m / 9 pies al menos una vez.»
- **Dice la página (cita textual):** «El conjuro puede localizar a una criatura específica que conozcas o a la criatura más cercana de un tipo específico (como un humano o un unicornio) si has visto a una criatura así de cerca (a 9 m o menos) al menos una vez.»
- **¿Trae la página conversión a pies?** No, la página solo dice «9 m», sin ninguna cifra en pies.
- **Veredicto:** la cifra de la base es errónea. La página dice «9 m», no «3 m»; y el «9 pies» que la base presenta como conversión no es tal cosa — es, en realidad, el propio valor en metros de la página (9) trasplantado al campo de pies, mientras que el campo de metros de la base quedó con un «3» que no aparece en la página. No puedo determinar con certeza el origen exacto del error (parece una confusión de dígitos al transcribir, pero es una hipótesis, no un hecho verificado en la página).

### Esfera congelante de Otiluke · pdf 279–280 (numeración de libro; en el pdf son 281–282)
- **Dice la base:** «[...] u obtener un orbe frío que tú o un aliado podéis lanzar con la mano (alcance 12 m / 39 pies) o con honda (alcance normal) [...]»
- **Dice la página (cita textual, continúa de pdf 281 a pdf 282):** «En cualquier momento, tú o una criatura a la que le entregues el orbe podéis lanzarlo con la mano (hasta un alcance de 12 m) o arrojarlo con una honda (hasta el alcance normal de la honda).»
- **¿Trae la página conversión a pies?** No. Solo «12 m», sin cifra en pies.
- **Veredicto:** la base añade una conversión que el manual no trae.

### Pasamuros · pdf 319–320 (numeración de libro; en el pdf son 319 y la descripción continúa en la 320)
- **Dice la base:** «Tú eliges las dimensiones de la abertura: hasta 1,5 m / 45 pies de ancho, 2,4 m / 8 pies de alto y 6 m / 20 pies de largo.»
- **Dice la página (cita textual, pdf 320):** «Tú eliges las dimensiones de la abertura: hasta 1,5 m de ancho, 2,4 m de alto y 6 m de largo.»
- **¿Trae la página conversión a pies?** No, en ninguna de las tres dimensiones.
- **Veredicto:** la base añade una conversión que el manual no trae, y además la cifra es doblemente sospechosa: «45 pies» no es ni la conversión física de 1,5 m (≈4,9 pies) ni la convención de juego habitual del propio manual (1,5 m = 5 pies, como se ve en Alarma o en otros conjuros de esta misma base). No he podido verificar en la página de dónde saldría el «45»; solo puedo confirmar que no está en el texto del manual en ese punto.

### Ráfaga de viento · pdf 326
- **Dice la base:** «Cualquier criatura que esté en la línea deberá gastar 2 m / 7,5 pies de movimiento por cada metro que se mueva para acercarse a ti.»
- **Dice la página (cita textual):** «Cualquier criatura que esté en la línea deberá gastar 2 m de movimiento por cada metro que se mueva para acercarse a ti.»
- **¿Trae la página conversión a pies?** No.
- **Veredicto:** la base añade una conversión que el manual no trae.

### Recluir · pdf 328–329
- **Dice la base:** «Puedes establecer una condición para que el conjuro termine antes de tiempo, [...] pero debe ocurrir o ser visible a 1,5 km / 4921 pies o menos del objetivo.»
- **Dice la página (cita textual, pdf 329):** «Puedes establecer una condición para que el conjuro termine antes de tiempo, que puede ser cualquier cosa que elijas, pero debe ocurrir o ser visible a 1,5 km o menos del objetivo.»
- **¿Trae la página conversión a pies?** No.
- **Veredicto:** la base añade una conversión que el manual no trae. (Nota aparte: «4921 pies» es la conversión física exacta de 1,5 km, no la convención de juego de 5 pies por 1,5 m que usa el resto del manual; es un dato añadido con un criterio distinto al del propio libro, pero eso no cambia el veredicto — la página no trae ninguna cifra en pies ahí.)

### Telaraña · pdf 337
- **Dice la base:** «Sobre superficie plana tienen 1,5 m / 20 pies de profundidad.»
- **Dice la página (cita textual):** «Las telarañas dispuestas sobre una superficie plana tienen una profundidad de 1,5 m.»
- **¿Trae la página conversión a pies?** No.
- **Veredicto:** la base añade una conversión que el manual no trae. (De paso, en la misma página tampoco hay conversión a pies para el cubo de telarañas de 6 m de lado ni para el cubo de 1,5 m de lado que arde con el fuego, aunque esos puntos no forman parte de esta auditoría.)

## Dudas / ilegible

Ninguna de las ocho páginas presentó problemas de legibilidad a 170 dpi; todas las cifras métricas citadas se leyeron con claridad. No hubo que recurrir a mayor resolución ni a recortes.

Los ocho casos comparten un mismo patrón: en cada uno, el manual del jugador en castellano da la medida **solo en metros/centímetros**, sin ninguna conversión a pies ni pulgadas en el punto exacto señalado. La base añade esa conversión en los ocho casos, y en dos de ellos (Localizar criatura y, más dudosamente, Pasamuros) la cifra añadida ni siquiera es coherente con ninguna convención de conversión reconocible (ni la física, ni la de juego que usa el resto del manual).
