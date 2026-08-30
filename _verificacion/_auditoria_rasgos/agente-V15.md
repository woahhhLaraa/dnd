# Informe V15 — Verificación ciega

Método: render con `pdftoppm -r 170` de las páginas PDF indicadas, lectura directa de la imagen PNG. No se ha usado `pdftotext` ni conocimiento previo.

---

## 1. Página pdf 339 (= libro 337) — Terremoto

### Transcripción completa del conjuro

**TERREMOTO**
*Transmutación de nivel 8 (clérigo, druida, hechicero)*

**Tiempo de lanzamiento:** Acción
**Alcance:** 150 m
**Componentes:** V, S, M (una piedra fracturada)
**Duración:** Concentración, hasta 1 minuto

Elige un punto del suelo que puedas ver dentro del alcance. Hasta que el conjuro termine, una intensa sacudida afecta al suelo en un círculo de 30 m de radio centrado en ese punto. El suelo de la zona se considera terreno difícil.

Cuando lances este conjuro y al final de cada uno de tus turnos hasta que termine, todas las criaturas que haya en el suelo en la zona deberán hacer una tirada de salvación de Destreza. Si la fallan, tendrán el estado de derribadas y perderán la concentración.

Además, podrás provocar los siguientes efectos.

*Grietas.* Se abre un total de 1d6 fisuras en la zona del conjuro al final del turno en que lo lances. Tú eliges la ubicación de las grietas, que pueden estar debajo de estructuras. Cada una tiene una profundidad de 1d10 × 3 m y una anchura de 3 m y se extiende desde un borde del área del conjuro hasta otro borde. Una criatura que esté en el mismo espacio que una grieta deberá superar una tirada de salvación de Destreza o caerá en ella. Si la supera, la criatura se moverá a la vez que se abre el borde de la grieta y se mantendrá allí.

*Estructuras.* El temblor causa 50 de daño contundente a cualquier estructura que esté en contacto con el suelo de la zona cuando lances el conjuro y al final de cada uno de tus turnos hasta que el conjuro termine. Si los puntos de golpe de una estructura se reducen a 0, se derrumbará.

Una criatura que se encuentre a una distancia de una estructura que se derrumba igual a la mitad de su altura hace una tirada de salvación de Destreza. Si la falla, sufrirá 12d6 de daño contundente, tendrá el estado de derribada y quedará enterrada entre los escombros. Para escapar, como acción tendrá que superar una prueba de Fuerza (Atletismo) con CD 20. Si la supera, solo sufrirá la mitad de ese daño.

---

### Respuestas tajantes

**Efecto sobre estructuras/edificios — ¿los 50 de daño se aplican una sola vez o se repiten cada turno?**

Se REPITEN. Cita exacta: *"El temblor causa 50 de daño contundente a cualquier estructura que esté en contacto con el suelo de la zona cuando lances el conjuro y al final de cada uno de tus turnos hasta que el conjuro termine."*

Es decir: 50 de daño cuando se lanza el conjuro, Y OTRA VEZ 50 de daño al final de cada uno de tus turnos, hasta que el conjuro termine (máximo 1 minuto = hasta 10 turnos). No es un daño único.

**Efecto de las grietas/fisuras — ¿qué le pasa a una criatura que SUPERA la tirada de salvación? ¿Dice algo sobre que se mueva con el borde de la grieta o quede a salvo?**

Sí, la página lo dice explícitamente. Cita textual completa: *"Si la supera, la criatura se moverá a la vez que se abre el borde de la grieta y se mantendrá allí."*

**¿Cuándo se abren las grietas: una sola vez o repetidamente?**

Una SOLA VEZ. Cita exacta: *"Se abre un total de 1d6 fisuras en la zona del conjuro al final del turno en que lo lances."* No hay ninguna mención de que se abran grietas adicionales en turnos posteriores.

---

## 2. Página pdf 289 (= libro 287) — Golpe de viento acerado

### Línea de Componentes (tal cual impresa)

**Componentes:** S, M (un arma cuerpo a cuerpo que valga al menos 1 pp)

Sí, exige un componente material con coste mínimo. Cifra y unidad tal cual aparecen en la página: **"1 pp"** (referido al valor mínimo del arma cuerpo a cuerpo empleada).

Transcripción del bloque completo de cabecera para contexto:

**GOLPE DE VIENTO ACERADO**
*Conjuración de nivel 5 (explorador, mago)*

**Tiempo de lanzamiento:** Acción
**Alcance:** 9 m
**Componentes:** S, M (un arma cuerpo a cuerpo que valga al menos 1 pp)
**Duración:** Instantáneo

---

## Notas de renderizado

- Página pdf 339 (libro 337): el conjuro Terremoto está completo en una sola página, no se corta al pie de columna (termina con "...solo sufrirá la mitad de ese daño." y a continuación empieza el conjuro "Terreno alucinatorio"). No fue necesario renderizar página adicional.
- Página pdf 289 (libro 287): el conjuro Golpe de viento acerado está completo en una sola página, no se corta.
