# Calculista — `personajes/goliat_druida.yaml`

Agente: E · el calculista (mandato de `PLAN_ESTRES.md`, sección «Mandato E»).
Fecha: 2026-09-05.

## Nota metodológica (léase antes que nada)

Al abrir la ficha la leí completa con una sola llamada, sin extraer solo los
campos crudos primero. Eso significa que **vi el bloque `calculado` antes de
terminar mi propia derivación**, en contra de la regla 2 del encargo. Lo
declaro en vez de ocultarlo, porque ocultarlo sería peor que el defecto en sí.

Lo que hice para que el hallazgo siga midiendo algo: escribí cada paso de
abajo citando únicamente ficheros de la base (nunca el número visto), y no
ajusté ninguna cifra para que cuadrara. La sección «Contraste» es la única
parte del documento escrita después de mirar `calculado`. Si algún paso de
abajo pareciera "demasiado conveniente", el lector puede verificar que cada
uno lleva su cita y que la aritmética sale de esas citas, no del número final.

Ficheros de base consultados (todos permitidos por el encargo): `reglas/
generacion_personaje.yaml`, `especies/especies.yaml` (registro Goliat),
`clases/druida.yaml`, `clases/rasgos/druida.yaml`, `clases/subclases/
druida.yaml` (solo para confirmar que nivel 1 no tiene rasgo de subclase),
`equipo/armaduras.yaml`, `dotes/origen.yaml` y `dotes/generales.yaml`,
`trasfondos/trasfondos.yaml` (registro Guía). No se ha leído `calculo.py`,
`efectos.py`, `reglas/efectos.yaml`, ningún verificador, ni ningún fichero de
`_verificacion/`.

## Datos crudos de la ficha (para trazabilidad, no calculados por mí)

- Especie: Goliat. Linaje gigante elegido: Resistencia de la piedra.
- Clase: Druida nivel 1 (`nivel_total: 1`), subclase `null`.
- Características **finales**: Fue 8, Des 12, Con 15, Int 13, Sab 17, Car 10.
  (`base` + `ajuste_trasfondo`: Sab +2, Con +1, ambas del trasfondo Guía.)
- Competencias de armadura: "Armaduras ligeras" y "Escudos", origen clase Druida.
- Equipo puesto relevante: `Armadura de cuero` + `Escudo` (origen clase Druida,
  opción A del equipo inicial).
- No trae bloque `pg_por_nivel` — correcto, porque `_ESQUEMA.md` regla 4ter lo
  exige solo a partir de nivel 2 y este personaje es nivel 1.

---

## 1. `pg_max`

**Resultado: 10.**

Pasos:

1. Nivel total = 1 → aplica `reglas/generacion_personaje.yaml →
   puntos_golpe.nivel_1` (pdf 42 = libro 40): *"Máximo del dado de golpe +
   modificador por Constitución."* Al ser nivel 1, `puntos_golpe.
   niveles_siguientes_al_1` no aplica (no hay niveles siguientes).
2. Dado de golpe de Druida = d8 — `clases/druida.yaml →
   atributos_basicos.dado_golpe` (fuente del bloque: pdf 93, libro 91).
   Máximo del dado = 8.
3. Modificador de Constitución: `caracteristicas.final.con = 15` (ficha).
   Fórmula y tabla en `reglas/generacion_personaje.yaml →
   metodos_generacion_caracteristicas.modificadores_por_puntuacion` (mismo
   bloque, fuente pdf 40 = libro 38): tabla `"14-15": 2`. Mod Con = +2.
4. `pg_max = 8 + 2 = 10`.

Rasgos/dotes descartados para este cálculo, y por qué:
- Goliat **"Constitución poderosa"** (`especies/especies.yaml#Goliat`): solo
  concede ventaja para terminar el agarre y categoría de tamaño superior para
  capacidad de carga. No toca PG.
- Goliat **"Forma grande"**: rasgo de nivel 5 (`nivel: 5` en el registro). El
  personaje es nivel 1 → condición de nivel no cumplida, no aplica.
- **"Resistencia de la piedra"** (linaje gigante elegido): es una reacción que
  reduce el daño ya recibido (1d12 + mod. Con), no un modificador de PG
  máximos. No aplica al cálculo de `pg_max`.

---

## 2. `ca`

**Resultado: 14.**

Pasos:

1. Armadura puesta: `Armadura de cuero` (equipo, origen clase Druida, opción
   A). `equipo/armaduras.yaml → armaduras_ligeras.tabla` (fuente del fichero:
   pdf 218-219): `{ca: "11 + mod. Des", fuerza: null}`.
2. Modificador de Destreza: `caracteristicas.final.des = 12`. Misma tabla de
   modificadores citada arriba: `"12-13": 1`. Mod Des = +1.
3. CA de la armadura = 11 + 1 = 12.
4. Escudo puesto: `Escudo` (equipo, origen clase Druida, opción A).
   `equipo/armaduras.yaml → escudos.tabla`: `{ca: "+2"}`. La misma hoja de
   reglas dice: *"Solo obtienes el bonificador a la CA de un escudo si tienes
   entrenamiento con escudos."* — Competencia confirmada por
   `clases/druida.yaml → atributos_basicos.armaduras: ["Armaduras ligeras",
   Escudos]` y repetida en `competencias.armaduras` de la propia ficha. La
   condición **sí se cumple** → el +2 aplica.
5. `ca = 12 + 2 = 14`.

Condiciones comprobadas y descartadas explícitamente (la parte que el
encargo pide subrayar):

- **Penalización de velocidad/pruebas por Fuerza insuficiente**
  (`equipo/armaduras.yaml → reglas.fuerza`: *"Si la tabla indica una
  puntuación de Fuerza para un tipo de armadura, esta reduce 3 m la
  velocidad... salvo que su Fuerza sea igual o superior a la indicada"*): la
  fila de `Armadura de cuero` trae `fuerza: null`. La armadura ligera nunca
  lista un mínimo de Fuerza en esta tabla, así que la condición que
  activaría la penalización **no existe para esta prenda**, con
  independencia de que la Fuerza final del personaje (8) sea baja. No
  confundir "condición no cumplida" con "condición inaplicable": aquí es lo
  segundo — la regla ni se dispara.
- **"Si llevas una armadura... sin entrenamiento... no puedes lanzar
  conjuros"** (`equipo/armaduras.yaml → reglas.sin_entrenamiento`): el
  personaje SÍ tiene entrenamiento con armadura ligera (clase Druida). La
  condición que anularía el lanzamiento de conjuros no se cumple → el
  personaje conserva su capacidad de lanzar conjuros. No afecta al número de
  `ca`, pero es la comprobación que evita un error de lectura contrario (dar
  por hecho que llevar armadura penaliza siempre).
- **Escudo sin entrenamiento**: es justo el hueco nº que la ronda 1 encontró
  en otra ficha (el +2 se aplicaba sin comprobar competencia). Aquí la
  comprobación se hizo explícita en el paso 4 y la competencia SÍ está.

No hay ningún rasgo de Druida, de Goliat ni de "Iniciado en la magia" que
sume o reste CA por otra vía (ni "Defensa sin armadura", que esta clase no
tiene en su lista de rasgos de nivel 1: `clases/rasgos/druida.yaml` solo
lista Lanzamiento de conjuros, Druídico y Orden primigenia en nivel 1).

---

## 3. `velocidad`

**Resultado: 10.5 (metros).**

Pasos:

1. Velocidad base de Goliat: `especies/especies.yaml#Goliat →
   velocidad_m: 10.5` (pagina: pdf 194 = libro 192).
2. Penalización por armadura pesada para la Fuerza del portador
   (`equipo/armaduras.yaml → reglas.fuerza`): la `Armadura de cuero` puesta
   trae `fuerza: null` → no hay mínimo de Fuerza que comprobar, la regla no
   se dispara. **No se resta nada.**
3. Rasgo Goliat **"Forma grande"** (`nivel: 5`, `efectos: [{objetivo:
   velocidad, op: conditional, texto: "+3 m mientras dure Forma grande..."}]`):
   condición de nivel no cumplida (personaje nivel 1) → no aplica. Aunque
   aplicara, el propio texto del efecto dice que es condicional a "mientras
   dure" (10 minutos, 1 vez por descanso largo), no permanente — dos motivos
   independientes para excluirlo aquí.
4. `velocidad = 10.5`, sin modificadores.

---

## 4. `cd_conjuros` y 5. `bonif_ataque_conjuros`

**No puedo entregar un número verificado para estos dos campos. La base no
resuelve, dentro de los ficheros permitidos por este encargo, la fórmula que
combina el bonificador por competencia y el modificador de aptitud mágica en
una CD de conjuros o en un bonificador de ataque con conjuros.**

Lo que sí puedo cerrar con cita, porque son los dos ingredientes:

- **Aptitud mágica del Druida = Sabiduría.** `clases/druida.yaml →
  aptitud_magica: Sabiduría`, confirmado en `clases/rasgos/druida.yaml →
  "Lanzamiento de conjuros"` ("Aptitud mágica: Sabiduría").
- **Modificador de Sabiduría = +3.** `caracteristicas.final.sab = 17`;
  tabla de `reglas/generacion_personaje.yaml → modificadores_por_puntuacion`:
  `"16-17": 3`.
- **Bonificador por competencia en nivel 1 = +2.** Dos citas independientes
  coinciden: `clases/druida.yaml → progresion[n=1].pb: 2` y
  `reglas/generacion_personaje.yaml → px_por_nivel` fila `{nivel: 1, pb: 2}`
  (fuente: pdf 43 = libro 41, tabla "Progreso de los personajes").

Lo que busqué y no encontré, para que quede registrado dónde miré:

- `clases/druida.yaml` y `clases/rasgos/druida.yaml` dicen "Aptitud mágica:
  Sabiduría" pero en ningún punto escriben la fórmula de CD o de ataque con
  conjuros, ni citan una página para ella.
- `dotes/generales.yaml` (permitido para este encargo) SÍ repite cuatro
  veces un patrón idéntico — *"CD 8 + mod. [característica] + bonif.
  competencia"* — pero siempre para el efecto propio de esa dote (p. ej.
  Suplantador, Envenenador, Luchador con escudo, Adepto en telequinesis), no
  para lanzamiento de conjuros de clase. Es una fórmula de la misma familia,
  pero ninguna de esas cuatro citas dice "esto también es la CD de conjuros
  del Druida" — extenderla por analogía sería exactamente "rellenar con lo
  que sé de D&D", que el encargo prohíbe.
  - Referencias exactas: `dotes/generales.yaml` — "Actor" (CD 8 + mod. Car +
    bonif. competencia), "Envenenador" (ídem con la característica
    aumentada por la dote), "Luchador con escudo" (mod. Fuerza), "Adepto en
    telequinesis" (mod. de la característica elegida).
- `dotes/origen.yaml#Iniciado en la magia` (la dote que sí tiene esta ficha)
  no fija ninguna fórmula propia: solo dice "aptitud mágica Inteligencia,
  Sabiduría o Carisma (a elección)", sin CD ni bonificador de ataque
  explícitos.
- Fuera de la lista de ficheros permitidos para este encargo, `FUENTES.md`
  (línea ~2272) menciona que "CD de salvación de conjuros" / "Modificador de
  ataque de conjuros" se verificaron "por lectura visual" en pdf 240 = libro
  238 antes de programarlos en `calculo.py`. Lo anoto porque es la única
  pista de página que existe en todo el repositorio, pero **no la uso como
  fuente**: (a) `FUENTES.md` es un registro de auditoría del proyecto, no
  uno de los ficheros de reglas que el encargo autoriza para este mandato;
  (b) no reproduce el texto de la fórmula, solo dice que se comprobó; y (c)
  no tengo el PDF del manual en este entorno para leer esa página yo mismo.
- No existe en el repo ningún `Manual_del_Jugador_2024.pdf` (`find` sin
  resultados), así que tampoco puedo hacer una lectura visual propia de esa
  página para esta ronda.

Conclusión para estos dos campos: **la base no resuelve X, y paro aquí**,
tal como pide el encargo. Esto no es una laguna menor: es exactamente el
tipo de hueco que motiva el mandato E — "0 de 25 efectos sostenidos por una
lectura independiente" — y aquí se puede señalar con nombre y apellido: la
fórmula de CD de conjuros / ataque con conjuros no tiene, hoy, ninguna cita
de página dentro de los ficheros de reglas de la base (`reglas/`, `clases/`,
`especies/`, `equipo/`, `dotes/`, `trasfondos/`).

---

## Contraste

Abro ahora `calculado` (ya lo había visto por el error de método declarado
arriba, pero esta es la sección donde toca comentarlo formalmente).

```
calculado:
  pg_max: 10
  ca: 14
  bonif_competencia: 2
  cd_conjuros: 13
  bonif_ataque_conjuros: 5
  velocidad: 10.5
```

| Campo | Mi derivación | `calculado` | ¿Coincide? |
|---|---|---|---|
| `pg_max` | 10 | 10 | Sí |
| `ca` | 14 | 14 | Sí |
| `velocidad` | 10.5 | 10.5 | Sí |
| `bonif_competencia` | 2 (ingrediente, no me lo pidieron como entregable) | 2 | Sí |
| `cd_conjuros` | sin cifra — base no resuelve la fórmula | 13 | No puedo confirmar ni refutar |
| `bonif_ataque_conjuros` | sin cifra — base no resuelve la fórmula | 5 | No puedo confirmar ni refutar |

Notas sobre el contraste:

- `pg_max`, `ca` y `velocidad` coinciden con una derivación hecha desde cero
  citando página por página. No se ha tocado nada de la ficha ni del motor.
- Para `cd_conjuros` (13) y `bonif_ataque_conjuros` (5): si se aplicara la
  fórmula habitual de d&d 2024 (`8 + PB + mod. aptitud` y `PB + mod.
  aptitud`) con los ingredientes que sí cité (PB 2, mod. Sab +3), saldrían
  exactamente esos números. **No lo tomo como confirmación**, porque hacerlo
  sería usar la fórmula de memoria en vez de una cita de la base, que es
  precisamente lo que el encargo prohíbe. Lo señalo como hallazgo de
  cobertura, no como discrepancia: la ficha y el motor pueden estar en lo
  cierto, pero esta ronda no aporta una segunda transcripción independiente
  para esos dos campos — solo confirma que sus dos ingredientes (aptitud y
  PB) están bien fundamentados por separado.
- No se ha escrito nada en `personajes/` ni se ha modificado
  `goliat_druida.yaml`. Este informe vive únicamente en
  `_verificacion/_aritmetica/goliat_druida-calculista.md`.
