# Cálculo a mano — `enano_clerigo_n5.yaml` — Agente E · el calculista

**Ficha:** Doran Piedrafría. Enano, Clérigo 5 (Dominio de la Guerra), trasfondo Acólito.
**Método:** los cinco valores se derivan solo de ficheros de reglas (`reglas/generacion_personaje.yaml`,
`especies/especies.yaml`, `clases/clerigo.yaml`, `clases/rasgos/clerigo.yaml`,
`clases/subclases/clerigo.yaml`, `equipo/armaduras.yaml`, `equipo/armas.yaml`,
`dotes/*.yaml`, `trasfondos/trasfondos.yaml`) y de los datos crudos de la propia
ficha (`caracteristicas.final`, `competencias`, `equipo`, `dotes`, `mejoras`,
`pg_por_nivel`). No se ha leído `calculo.py`, `efectos.py`, `reglas/efectos.yaml`
ni ningún verificador.

## Nota metodológica — una desviación que hay que declarar

El primer paso de este encargo fue leer la ficha completa con la herramienta de
lectura de fichero, para extraer los datos crudos. La ficha guarda `calculado`
en el mismo fichero que los datos crudos (no hay separación física), así que
esa lectura completa **mostró también `calculado` desde el primer instante**,
antes de escribir una sola línea de derivación propia. Regla 2 del encargo pide
leerlo "solo cuando ya hayas escrito el tuyo".

No he vuelto a abrir el bloque `calculado` en ningún momento posterior — toda
la derivación de abajo se ha rehecho leyendo únicamente los ficheros de reglas
permitidos, sin mirar atrás — pero la ceguera del método queda comprometida
para esta ficha concreta: los cinco números del motor ya eran visibles cuando
empecé a calcular. Lo declaro en vez de ocultarlo, tal como pide el propio
`PLAN_ESTRES.md` para los hallazgos descartados. El lector debe pesar `pg_max`,
`ca` y `velocidad` de abajo sabiendo esto; los dos valores que la base no
resuelve (`cd_conjuros`, `bonif_ataque_conjuros`) no se han visto comprometidos
en la práctica porque para ellos no hay número propio que "encajar" — solo hay
un "no se puede calcular", que es independiente de haber visto el resultado.

---

## Datos crudos usados (de la ficha, no de reglas)

- Especie: Enano. Clase: Clérigo nivel 5, subclase Dominio de la Guerra.
- `caracteristicas.final`: fue 12, des 10, con 14, int 8, sab 18, car 15.
- `competencias.armaduras`: Armaduras ligeras, Armaduras medias, Escudos (origen: clase Clérigo).
- `equipo`: Camisa de malla, Escudo, Maza, Paquete de sacerdote, Símbolo sagrado,
  Suministros de calígrafo, Libro, Pergamino×10, Túnica.
- `dotes`: Iniciado en la magia (origen trasfondo).
- `mejoras`: nivel 4, +1 Sabiduría / +1 Carisma (Mejora de característica).
- `pg_por_nivel`: 5 filas (ver más abajo).

---

## 1. `pg_max`

### Paso 1 — modificador de Constitución

`caracteristicas.final.con = 14`.
Tabla de modificadores: `reglas/generacion_personaje.yaml` →
`metodos_generacion_caracteristicas.modificadores_por_puntuacion.tabla`,
fila `"14-15": 2` (pág. pdf 40, libro 38, la misma fuente del bloque que la contiene).
→ **mod_con = +2**.

### Paso 2 — término del dado, nivel a nivel

Regla citada por la propia ficha en cada fila de `pg_por_nivel`, y verificada
contra `reglas/generacion_personaje.yaml`:

| Nivel | Método | Valor | Regla base | Página |
|---|---|---|---|---|
| 1 | `maximo_dado` | 8 | `puntos_golpe.nivel_1`: "Máximo del dado de golpe + mod. Constitución" | pdf 42, libro 40 |
| 2 | `valor_establecido` | 5 | `puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos`, fila Clérigo = 5 | pdf 44, libro 42 |
| 3 | `valor_establecido` | 5 | ídem | pdf 44, libro 42 |
| 4 | `valor_establecido` | 5 | ídem | pdf 44, libro 42 |
| 5 | `tirada` | 6 | `puntos_golpe.niveles_siguientes_al_1.metodos[tirar]`: tirar el dado y sumar Constitución, mínimo 1 del total | pdf 44, libro 42 |

Verificación de consistencia con la clase: `clases/clerigo.yaml` da
`dado_golpe: d8` (pág. pdf 83, libro 81). El máximo de un d8 es 8, que es
exactamente el valor que la ficha registra en nivel 1 → consistente.
`tabla_valores_establecidos` de `reglas/generacion_personaje.yaml` pone al
Clérigo en la fila `{clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}`
→ los tres 5 de niveles 2-4 son exactamente ese valor → consistente.

**Importante sobre qué es cada "valor":** la regla de `niveles_siguientes_al_1`
dice que el modificador de Constitución se suma *aparte* del dado ("tira el
dado, suma tu modificador... y añade el total"); el valor de la tabla de
valores establecidos (5 para Clérigo) es el promedio del dado *solo*, no el
promedio+Constitución. Los cinco `valor` de la ficha son, pues, la contribución
del dado en cada nivel, y el término de Constitución se añade una sola vez como
`nivel_total × mod_con` (así lo dice explícitamente
`puntos_golpe.aumento_de_constitucion._nota_para_el_motor`, pdf 44/libro 42:
*"El término de Constitución es nivel_total × mod_con... solo el término del
dado es historia acumulada"*).

Suma del término del dado: 8 + 5 + 5 + 5 + 6 = **29**.
Término de Constitución: 5 (nivel_total) × 2 (mod_con) = **10**.

Subtotal (sin rasgos de especie): 29 + 10 = **39**.

### Paso 3 — rasgo de especie: Aguante enano

`especies/especies.yaml`, registro Enano (pág. pdf 192, libro 190), rasgo
"Aguante enano": *"Tus PG máximos aumentan en 1, y en 1 más cada vez que subes
de nivel."*, con efecto estructurado `{objetivo: pg_max, op: add, formula: "nivel_total"}`.
**Aplica** — el personaje es Enano y `nivel_total = 5` → **+5**.

### Paso 4 — qué NO aplica

- **"Duro" (dote de origen, `dotes/origen.yaml`)**: da `+2×nivel_total` a
  PG máximos. **No aplica**: la ficha no la tiene en `dotes:` (solo tiene
  "Iniciado en la magia").
- **"Resistencia dracónica" (subclase Hechicero)**: no aplica, el personaje
  no es Hechicero.
- **"Iniciado en la magia"** (`dotes/origen.yaml`, la única dote de esta
  ficha): su descripción no trae ningún efecto sobre PG máximos — solo
  concede trucos y un conjuro de nivel 1 siempre preparado. **No aplica**.
- **"Mejora de característica" (nivel 4)**: sube Sabiduría y Carisma, no
  Constitución, así que no dispara la regla de "aumento de Constitución"
  (`puntos_golpe.aumento_de_constitucion`, pdf 44/libro 42) que recalcularía
  el término de Constitución. **No aplica** — y es correcto que no aplique,
  porque el modificador de Constitución del personaje no cambió.

### Resultado

**pg_max = 39 + 5 = 44**

---

## 2. `ca` (Clase de Armadura)

### Paso 1 — qué lleva puesto y con qué entrenamiento

`equipo`: Camisa de malla (origen clase, opción A) + Escudo (origen clase,
opción A). `competencias.armaduras`: Armaduras ligeras, **Armaduras medias**,
**Escudos** (las tres con origen clase Clérigo). `clases/clerigo.yaml` confirma
en `atributos_basicos.armaduras: ["Armaduras ligeras", "Armaduras medias", Escudos]`
(pág. pdf 83, libro 81) que el Clérigo trae esas tres competencias de forma
nativa.

### Paso 2 — fórmula de la armadura

`equipo/armaduras.yaml` (pág. pdf 218-219), tabla `armaduras_medias`:
`{nombre: "Camisa de malla", ca: "13 + mod. Des (máx. 2)", fuerza: null}`.

`caracteristicas.final.des = 10` → mod_des = 0 (tabla de
`reglas/generacion_personaje.yaml`, fila `"10-11": 0`).
`min(mod_des, 2) = min(0, 2) = 0`.
→ CA de la armadura = 13 + 0 = **13**.

`fuerza: null` en la fila de Camisa de malla → no hay penalización de
velocidad por Fuerza insuficiente (regla `equipo/armaduras.yaml.reglas.fuerza`),
y tampoco hay ninguna cláusula de "Fuerza mínima" que journal afecte a la CA.

### Paso 3 — el escudo

`equipo/armaduras.yaml`, tabla `escudos`: `{nombre: Escudo, ca: "+2"}`.
Regla `reglas.escudos`: *"Solo obtienes el bonificador a la CA de un escudo si
tienes entrenamiento con escudos."* El personaje SÍ tiene esa competencia
(`competencias.armaduras` incluye "Escudos", origen clase Clérigo) → **aplica**.
→ +2.

### Paso 4 — qué NO aplica

- **Fórmulas de "Defensa sin armadura"** (bárbaro `10+mod_des+mod_con`, monje
  `10+mod_des+mod_sab`, colegio de bardo, resistencia dracónica de hechicero):
  ninguna aplica — todas exigen explícitamente ir *sin armadura* (`requiere:
  [sin_armadura]` en sus propios efectos estructurados), y este personaje
  lleva puesta una Camisa de malla. Además ninguna es un rasgo de Clérigo.
- **Estilo de combate "Defensor"** (`dotes/estilo_de_combate.yaml`, +1 CA con
  armadura): no aplica — la ficha no tiene ninguna dote de esa categoría, y el
  Clérigo (ni su subclase Dominio de la Guerra en los rasgos de nivel ≤5) no
  concede un estilo de combate.
- **"Maestro en armaduras medias"** (tope de Destreza a 3 en vez de 2) y
  similares de `dotes/generales.yaml`: no aplica — no está en `dotes:` de la
  ficha (que solo trae "Iniciado en la magia").
- **Rasgos de especie del Enano** (Afinidad con la piedra, Resistencia enana,
  Visión en la oscuridad, Aguante enano): ninguno toca la CA.
- **Rasgos de Dominio de la Guerra hasta nivel 5** (Conjuros del dominio,
  Golpe guiado, Sacerdote guerrero): ninguno modifica la CA.
- **Túnica** (`equipo/aventureros.yaml`, del trasfondo): es ropa, no armadura;
  no tiene entrada en `equipo/armaduras.yaml` y no aporta CA. Nunca se
  llevaría a la vez que una armadura de cuerpo de todos modos.

### Resultado

**ca = 13 (armadura) + 2 (escudo) = 15**

---

## 3. `velocidad`

### Paso 1 — velocidad base de la especie

`especies/especies.yaml`, registro Enano (pág. pdf 192, libro 190):
`velocidad_m: 9`.

### Paso 2 — penalización por Fuerza insuficiente

`equipo/armaduras.yaml.reglas.fuerza`: *"Si la tabla indica una puntuación de
Fuerza para un tipo de armadura, esta reduce 3 m la velocidad de quien la
lleve, salvo que su Fuerza sea igual o superior a la indicada."* La fila de
Camisa de malla trae `fuerza: null` (no exige una puntuación mínima) →
**la regla no se dispara, con independencia de la Fuerza del personaje** (12).
No hay armadura pesada implicada (esas sí llevan `fuerza: 13/15` en la tabla),
así que este personaje nunca entra en esa condición.

### Paso 3 — qué NO aplica

- **Ningún rasgo de clase o subclase de Clérigo hasta nivel 5** (revisados
  todos los de `clases/rasgos/clerigo.yaml` y `clases/subclases/clerigo.yaml#Dominio de la Guerra`)
  modifica la velocidad.
- **Dotes de velocidad** (`dotes/generales.yaml`, p. ej. la que da +3 m;
  `dotes/don_epico.yaml`, +9 m): no aplican, no están en `dotes:` de la ficha
  y además exigirían nivel/prerrequisitos que esta ficha no declara haber
  cumplido para ellas.
- **Escudo**: no tiene ningún efecto sobre velocidad en `equipo/armaduras.yaml`.

### Resultado

**velocidad = 9 m**

---

## 4. `cd_conjuros` — la base NO resuelve este número

### Lo que sí está en la base

- `clases/clerigo.yaml`, campo `aptitud_magica: Sabiduría` (pág. pdf 84, tabla
  "Rasgos de clérigo") — la aptitud mágica del Clérigo es Sabiduría.
- `caracteristicas.final.sab = 18` → mod_sab = +4 (tabla de
  `reglas/generacion_personaje.yaml`, fila `"18-19": 4`).
- `reglas/generacion_personaje.yaml#px_por_nivel`, fila nivel 5: `pb: 3`
  (pág. pdf 43, libro 41) — coincide con `clases/clerigo.yaml#progresion[n=5].pb: 3`
  (pág. pdf 83). El bonificador por competencia en nivel 5 es, sin ambigüedad, **+3**.

### Lo que NO está — y es lo que hace falta

Ninguno de los ficheros permitidos (`reglas/generacion_personaje.yaml`,
`reglas/habilidades.yaml`, `especies/especies.yaml`, `clases/clerigo.yaml`,
`clases/rasgos/clerigo.yaml`, `clases/subclases/clerigo.yaml`,
`equipo/armaduras.yaml`, `equipo/armas.yaml`, `dotes/origen.yaml`,
`dotes/generales.yaml`, `dotes/estilo_de_combate.yaml`, `dotes/don_epico.yaml`,
`trasfondos/trasfondos.yaml`) transcribe la fórmula general de "CD de
conjuros". Se ha buscado explícitamente:

- `clases/rasgos/clerigo.yaml` (rasgo "Canalizar divinidad") **usa** el
  término "tu CD de conjuros" como si ya estuviera definido en otro sitio
  ("...con salvación de Constitución CD igual a tu CD de conjuros...") pero
  no lo define ahí.
- `clases/rasgos/paladin.yaml` hace exactamente lo mismo ("la CD es la CD de
  conjuros de paladín") — confirma que es un término compartido entre clases,
  definido en algún capítulo general del manual, pero ese capítulo no está
  transcrito en ninguno de los ficheros de reglas de este proyecto (fuera de
  `reglas/efectos.yaml`, que esta tarea tiene prohibido leer).
- El patrón "CD 8 + mod. [característica] + bonif. competencia" **sí**
  aparece, una y otra vez, para salvaciones concretas de dotes, maniobras y
  objetos (`dotes/generales.yaml` ×5, `dotes/don_epico.yaml`,
  `equipo/armas.yaml#derribar`, varios en `equipo/aventureros.yaml`,
  `clases/rasgos/monje.yaml`, `clases/subclases/{picaro,guerrero}.yaml`) —
  pero **ninguna de esas citas dice que esa sea la fórmula de "CD de
  conjuros"**; son la fórmula de la CD de *esa* dote o *ese* rasgo concreto.
  Generalizarla a los conjuros de clérigo sería exactamente rellenar con
  conocimiento externo de D&D, que el encargo prohíbe.

### Conclusión

**La base no resuelve `cd_conjuros`.** No hay un fichero permitido que
transcriba la fórmula, ni una cita que la aplique explícitamente a los
conjuros de clase. Paro aquí: no doy un número propio para este valor.

---

## 5. `bonif_ataque_conjuros` — la base tampoco resuelve este número

Mismo problema que el anterior, y por la misma razón: ningún fichero
permitido dice qué es un "bonificador de ataque con conjuros" ni da su
fórmula. `equipo/aventureros.yaml` menciona la existencia del concepto de
pasada ("...el bonificador de ataque de conjuros del creador", para objetos
mágicos) pero no lo define; no está entre los ficheros que este encargo
permite citar como fuente de reglas de todos modos.

Los únicos datos ciertos que sí aporta la base son los mismos de arriba:
mod_sab = +4, bonificador por competencia (nivel 5) = +3. Cómo se combinan
para dar un bonificador de ataque no está escrito en ningún sitio accesible.

**La base no resuelve `bonif_ataque_conjuros`.** Paro aquí también.

---

## Contraste

Abro ahora el bloque `calculado` de la ficha (con la salvedad ya declarada
arriba: se vio de refilón antes de tiempo por venir en el mismo fichero que
los datos crudos).

```yaml
calculado:
  _origen: {metodo: motor, informe: null, fecha: "2026-09-05"}
  pg_max: 44
  ca: 15
  bonif_competencia: 3
  cd_conjuros: 15
  bonif_ataque_conjuros: 7
  velocidad: 9
```

| Valor | Mío | Motor | ¿Coincide? |
|---|---|---|---|
| `pg_max` | 44 | 44 | **Sí** |
| `ca` | 15 | 15 | **Sí** |
| `velocidad` | 9 | 9 | **Sí** |
| `cd_conjuros` | *(sin dato — la base no lo resuelve)* | 15 | **No contrastable** |
| `bonif_ataque_conjuros` | *(sin dato — la base no lo resuelve)* | 7 | **No contrastable** |

### Lectura de los tres que coinciden

`pg_max`, `ca` y `velocidad` se pudieron derivar íntegramente desde ficheros
de reglas independientes del motor (`generacion_personaje.yaml`,
`especies.yaml`, `clases/clerigo.yaml`, `equipo/armaduras.yaml`), citando
página en cada paso, y los tres coinciden con lo que produjo `calculo.py`.
Con la salvedad metodológica ya declarada (vi el bloque `calculado` de refilón
antes de calcular), esto es evidencia — no prueba definitiva, por esa
salvedad — de que esas tres piezas del motor están calculando lo que la base
dice para esta ficha concreta.

### Lectura de los dos que no se pudieron contrastar

Esto **no es un "coincide" disfrazado**: es exactamente el hallazgo que el
mandato E busca. `cd_conjuros: 15` y `bonif_ataque_conjuros: 7` son
aritméticamente lo que resultaría de aplicar `8 + bonif. competencia + mod.
aptitud mágica` (8+3+4=15) y `bonif. competencia + mod. aptitud mágica`
(3+4=7) — la fórmula estándar de D&D que cualquier jugador conoce de memoria.
Pero **ningún fichero de esta base la transcribe**, ni para conjuros en
general ni para el Clérigo en particular; solo vive, con toda seguridad,
dentro de `reglas/efectos.yaml`/`calculo.py`, que este encargo prohíbe leer
precisamente para poder medir si esa fórmula tiene una segunda transcripción
independiente detrás. **No la tiene** — al menos no en ninguno de los
ficheros que este agente tiene permiso para citar. Esto confirma, para esta
ficha, la fila 8 del censo que motivó el mandato: `cd_conjuros` y
`bonif_ataque_conjuros` siguen en la columna de "0 lecturas independientes".
Si el número del motor es correcto no es porque la base lo sostenga, es
porque coincide con la fórmula que cualquiera que conozca el juego
reconocería — que es exactamente la clase de coincidencia que este proyecto
existe para no tener que confiar.
