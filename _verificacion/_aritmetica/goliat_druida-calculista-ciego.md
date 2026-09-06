# Korrath Pico de Piedra — derivación a mano (calculista ciego)

**Ficha:** `goliat_druida` — Goliat, Druida 1, trasfondo Guía. Nivel total 1.
**Agente:** E · «el calculista», ronda 3 de estrés.
**Fecha:** 2026-09-06.

## Método

Se han calculado a mano `pg_max`, `ca`, `velocidad`, `cd_conjuros` y
`bonif_ataque_conjuros` partiendo **solo** de los datos crudos de la ficha
(sin su bloque `calculado`) y de los ficheros de la base de reglas. Cada paso
cita `fichero → campo` y, cuando el fichero la trae, la página del manual.

Entrada usada:
`/tmp/claude-0/-home-user-dnd/ccce6f54-5659-5d7c-89a3-15e0f610e8cf/scratchpad/crudos/goliat_druida.yaml`
(copia de los datos crudos, sin `calculado`).

### Ficheros de la base consultados

| Fichero | Para qué |
|---|---|
| `especies/especies.yaml` | Goliat: `velocidad_m`, `tamano`, rasgos y linajes |
| `clases/druida.yaml` | `dado_golpe`, `aptitud_magica`, `progresion[n:1].pb`, competencias de armadura, equipo inicial |
| `clases/rasgos/druida.yaml` | Lanzamiento de conjuros, Druídico, Orden primigenia |
| `reglas/generacion_personaje.yaml` | `modificadores_por_puntuacion`, `puntos_golpe.nivel_1`, `conjuros.cd_salvacion`, `conjuros.bonificador_ataque`, `px_por_nivel` |
| `reglas/caracteristicas.yaml` | emparejamiento nombre ↔ abreviatura (`sab` = Sabiduría, etc.) |
| `equipo/armaduras.yaml` | CA de armaduras y escudo, y las 6 reglas de uso |
| `equipo/aventureros.yaml` | contenido del Paquete de explorador, aljaba, petate, tienda, ropas de viaje, canalizador druídico |
| `equipo/armas.yaml`, `equipo/municion.yaml`, `equipo/herramientas.yaml` | comprobar que el resto del equipo no es armadura |
| `trasfondos/trasfondos.yaml` | Guía: características ajustables, dote, equipo |
| `dotes/origen.yaml` | Iniciado en la magia |
| `reglas/fuentes_de_efectos.yaml` | qué ficheros de equipo son (y no son) fuente de efectos calculables |
| `reglas/subida_de_nivel.yaml` | comprobar que nada de nivel >1 aplica |

### Desviaciones cometidas — declaración honesta

1. **Ninguno de nuestros números ha sido visto.** No se han abierto
   `personajes/goliat_druida.yaml`, ni ninguna otra ficha de `personajes/`,
   ni `personajes/_hallazgos/`, ni ningún informe previo de
   `_verificacion/_aritmetica/`, ni `calculo.py`, `efectos.py`,
   `reglas/efectos.yaml` ni verificador alguno. No se ha ejecutado ningún
   verificador.
2. **Desviación menor, declarada:** se listó el **nombre** de los ficheros de
   `_verificacion/_aritmetica/` (con `ls`) para confirmar que el directorio de
   salida existía y que mi nombre de fichero no chocaba con otro. En esa
   lista aparece `goliat_druida-calculista.md`, informe previo sobre esta
   misma ficha. **No se abrió ni se leyó ni una línea de su contenido**; solo
   se vio el nombre, que no contiene ningún número.
3. Se usó `python3` exclusivamente para **leer** `equipo/armaduras.yaml` con
   `yaml.safe_load` y listar sus 13 armaduras + escudo, y para cruzar esa
   lista de nombres contra el equipo llevado. Es lectura de datos, no cálculo:
   los cinco valores del informe están calculados a mano, uno a uno.
4. **CA por defecto sin armadura:** no hizo falta. Korrath lleva armadura, así
   que la derivación no depende de la fórmula «10 + mod. Des» (que, según el
   encargo, está declarada en el fichero que este método no puede abrir).

---

## Paso 0 — Datos de partida (los que alimentan todo lo demás)

### 0.1 Modificadores de característica

Regla: `reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.modificadores_por_puntuacion.formula`
(pdf 40, libro 38): *«(puntuación − 10) / 2, redondeando hacia abajo»*, con
tabla de contraste en el mismo campo (`.tabla`).

Puntuaciones finales de la ficha (`caracteristicas.final`):

| Característica | Puntuación | (P − 10)/2 ↓ | Tabla del fichero | Modificador |
|---|---|---|---|---|
| Fuerza (`fue`) | 8 | (8−10)/2 = −1 | `"8-9": -1` | **−1** |
| Destreza (`des`) | 12 | (12−10)/2 = +1 | `"12-13": 1` | **+1** |
| Constitución (`con`) | 15 | (15−10)/2 = 2,5 → 2 | `"14-15": 2` | **+2** |
| Inteligencia (`int`) | 13 | +1 | `"12-13": 1` | **+1** |
| Sabiduría (`sab`) | 17 | (17−10)/2 = 3,5 → 3 | `"16-17": 3` | **+3** |
| Carisma (`car`) | 10 | 0 | `"10-11": 0` | **0** |

Fórmula y tabla coinciden en las seis. El emparejamiento abreviatura ↔ nombre
sale de `reglas/caracteristicas.yaml → caracteristicas` (`con` = Constitución,
`des` = Destreza, `sab` = Sabiduría).

De paso, comprobación de que las puntuaciones finales son las que dice la
ficha: base `con: 14` + `ajuste_trasfondo.con: 1` = 15 ✔; base `sab: 15` +
`ajuste_trasfondo.sab: 2` = 17 ✔. El reparto +2/+1 está permitido por
`trasfondos/trasfondos.yaml → reparto_caracteristicas` y las dos
características ajustadas (Sabiduría, Constitución) están en
`trasfondos.yaml → Guía.caracteristicas: [Destreza, Constitución, Sabiduría]`
(pdf 185, libro 183).

### 0.2 Bonificador por competencia (PB)

Dos declaraciones independientes, y coinciden:

- `clases/druida.yaml → progresion` fila `{n: 1, pb: 2, …}`
- `reglas/generacion_personaje.yaml → px_por_nivel.filas` fila `{nivel: 1, px: 0, pb: 2}`
  (pdf 43, libro 41, tabla «Progreso de los personajes»)

`nivel_total: 1` ⇒ **PB = +2**.

---

## 1 · `pg_max` — Puntos de golpe máximos

**Regla:** `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1.regla`
(página declarada en el propio campo: `pagina: {pdf: 42, libro: 40}`):

> «Máximo del dado de golpe + modificador por Constitución.»

**Dado de golpe:** `clases/druida.yaml → atributos_basicos.dado_golpe: d8`
(pdf 93, libro 91). Máximo de un d8 = **8**.

**Modificador por Constitución:** +2 (paso 0.1, Con 15).

    pg_max = 8 (máx. d8) + 2 (mod. Con) = 10

**Nada más suma.** Comprobado uno a uno lo que en esta base puede tocar
`pg_max`:

- Rasgos de especie: Goliat (`especies/especies.yaml`, pdf 194, libro 192) no
  tiene ningún rasgo con `objetivo: pg_max` — el único de todo el fichero de
  especies que lo tiene es «Aguante enano» del Enano (línea 67).
- Dotes: la única de la ficha es **Iniciado en la magia**
  (`dotes/origen.yaml → dotes[Iniciado en la magia]`, pdf 203, libro 201): su
  `descripcion` es trucos + un conjuro siempre preparado, sin PG. La dote de
  origen que sí daría PG es **Duro** (`efectos: [{objetivo: pg_max, op: add,
  formula: "2 * nivel_total"}]`), y Korrath no la tiene.
- Reglas de nivel >1 (`puntos_golpe.niveles_siguientes_al_1` y
  `aumento_de_constitucion`, pdf 44, libro 42): **no aplican**, el personaje es
  de nivel 1 y no ha subido ningún nivel. `pg_por_nivel` no existe en la ficha.

> **`pg_max` = 10**

---

## 2 · `ca` — Clase de armadura

### 2.1 Qué lleva puesto: cotejo objeto a objeto contra `equipo/armaduras.yaml`

`equipo/armaduras.yaml` (pdf 218-219, libro 216) contiene exactamente 13
registros: 3 ligeras + 5 medias + 4 pesadas = **12 armaduras**, más **1
escudo**. Cotejo de los 13 objetos de `equipo:` de la ficha contra esa tabla:

| # | Objeto (`ref` de la ficha) | Dónde está de verdad | ¿En `armaduras.yaml`? | Aporta CA |
|---|---|---|---|---|
| 1 | `equipo/armaduras.yaml#Armadura de cuero` | `armaduras_ligeras.tabla` | **Sí** | **11 + mod. Des** |
| 2 | `equipo/armaduras.yaml#Escudo` | `escudos.tabla` | **Sí** | **+2** |
| 3 | `equipo/armas.yaml#Hoz` | `armas.yaml` (1d4 cortante, ligera) | No | 0 |
| 4 | `equipo/aventureros.yaml#Canalizador druídico` (variante «Bastón de madera») | `aventureros.yaml → canalizadores_druidicos` | No | 0 |
| 5 | `equipo/aventureros.yaml#Paquete de explorador` | `aventureros.yaml → tabla_peso_precio` + `descripciones` | No (ver 2.2) | 0 |
| 6 | `equipo/herramientas.yaml#Útiles de herborista` | `herramientas.yaml` | No | 0 |
| 7 | `equipo/armas.yaml#Arco corto` | `armas.yaml` (1d6 perforante, a dos manos) | No | 0 |
| 8 | `equipo/municion.yaml#Flechas` | `municion.yaml` | No | 0 |
| 9 | `equipo/herramientas.yaml#Herramientas de cartógrafo` | `herramientas.yaml` | No | 0 |
| 10 | `equipo/aventureros.yaml#Aljaba` | `aventureros.yaml` | No | 0 |
| 11 | `equipo/aventureros.yaml#Petate` | `aventureros.yaml` | No | 0 |
| 12 | `equipo/aventureros.yaml#Tienda` | `aventureros.yaml` | No | 0 |
| 13 | `equipo/aventureros.yaml#Ropas de viaje` | `aventureros.yaml` (desc.: *«Prendas resistentes diseñadas para viajar por diversos entornos»*) | **No** | 0 |

El nº 13 es el que más se parece a una trampa: «Ropas de viaje» suena a
prenda, pero **no está en `equipo/armaduras.yaml`** — está en
`aventureros.yaml → tabla_peso_precio` (2 kg, 2 po) con una descripción sin
mecánica. No es armadura y no da CA.

### 2.2 Lo que hay dentro del paquete

`equipo/aventureros.yaml → descripciones["Paquete de explorador"]`:

> «Contiene: 10 antorchas, cantimplora, cuerda, 2 frascos de aceite, mochila,
> petate, raciones para 10 días y yesquero.»

Cotejados los ocho contra los 14 nombres de `equipo/armaduras.yaml`:
**ninguno aparece**. El paquete aporta **0** a la CA.

Esto lo respalda además la propia base: `reglas/fuentes_de_efectos.yaml →
excluidos` declara para `equipo/aventureros.yaml` el motivo *«equipo de
aventurero y paquetes: peso y precio. No concede nada calculable»*, y para
`equipo/armas.yaml` *«No modifica ninguna variable calculable del personaje
(pg_max, ca, velocidad)»*. Y `fuentes_de_efectos.yaml → derivadas` señala
`equipo/armaduras.yaml` como la única fuente de equipo con efectos sobre `ca`
y `velocidad`, derivados de sus campos `ca` y `fuerza`.

### 2.3 ¿Puede usarlos de forma efectiva?

`equipo/armaduras.yaml → reglas`:

- `entrenamiento`: *«Cualquiera puede ponerse una armadura […] pero solo quien
  tenga entrenamiento con ese tipo la usa de forma efectiva.»*
- `escudos`: *«Solo obtienes el bonificador a la CA de un escudo si tienes
  entrenamiento con escudos.»*
- `solo_un_tipo`: *«Una criatura no puede llevar puesta más de una armadura ni
  embrazar más de un escudo a la vez.»* — cumple: una armadura, un escudo.

Competencias del personaje: `clases/druida.yaml → atributos_basicos.armaduras:
["Armaduras ligeras", Escudos]`, reflejadas en la ficha
(`competencias.armaduras`). La Armadura de cuero es **ligera**
(`armaduras_ligeras.tabla`) ⇒ entrenado. Escudos ⇒ entrenado. **Los dos
cuentan.** (La cláusula `sin_entrenamiento` —desventaja y no poder lanzar
conjuros— no se activa.)

### 2.4 La suma

    Armadura de cuero ... 11 + mod. Des = 11 + 1 = 12
    Escudo ............... +2
    ---------------------------------------------
    ca = 11 + 1 + 2 = 14

La armadura ligera **no tiene tope al modificador de Destreza** (el
`(máx. 2)` solo aparece en `armaduras_medias`), así que el +1 entra entero.

> **`ca` = 14**

---

## 3 · `velocidad` — en metros

**Base de especie:** `especies/especies.yaml → especies[Goliat].velocidad_m:
10.5` (pdf 194, libro 192). El campo ya viene en metros.

Ahora, las dos cosas que en esta ficha podrían moverla:

### 3.1 El rasgo condicional del Goliat: «Forma grande» — NO se cumple

`especies/especies.yaml → especies[Goliat].rasgos[Forma grande]`
(pdf 194, libro 192):

- `nivel: 5`
- `desc`: *«Acción adicional: cambias a tamaño Grande 10 minutos. Ventaja en
  las pruebas de Fuerza y tu velocidad aumenta en 3 m. 1 vez por descanso
  largo.»*
- `efectos: [{objetivo: velocidad, op: conditional, texto: "+3 m mientras dure
  Forma grande (10 minutos, 1 vez por descanso largo), **no de forma
  permanente**"}]`

**No se cumple la condición, y falla por dos motivos independientes:**

1. **Por nivel:** el rasgo tiene `nivel: 5` y Korrath es de **nivel 1**
   (`nivel_total: 1`). Todavía no posee el rasgo, así que no hay ni siquiera
   algo que activar.
2. **Por naturaleza del efecto:** aunque llegara a nivel 5, el propio efecto
   está marcado `op: conditional` y su texto dice explícitamente *«no de forma
   permanente»*: son 3 m durante 10 minutos, una vez por descanso largo, tras
   gastar una acción adicional. Eso **nunca** entra en el campo `velocidad` de
   la ficha, que es la velocidad permanente del personaje.

El otro rasgo de Goliat con elección, **Linaje gigante**, está resuelto en la
ficha como `Resistencia de la piedra`
(`especies.yaml → Goliat.linajes[Resistencia de la piedra]`): *«Reacción al
recibir daño: tiras 1d12 y sumas tu modificador por Constitución; reduces el
daño en ese total.»* Reducción de daño, **ni velocidad ni CA**. Y
«Constitución poderosa» solo da ventaja contra agarrado y una categoría de
tamaño más para capacidad de carga: tampoco toca la velocidad (la base no
declara ninguna regla de sobrecarga que la reduzca; buscado en `reglas/`,
`equipo/` y `especies/`).

### 3.2 La otra condición, la de la armadura: tampoco se cumple

`equipo/armaduras.yaml → reglas.fuerza`:

> «Si la tabla indica una puntuación de Fuerza para un tipo de armadura, esta
> reduce 3 m la velocidad de quien la lleve, salvo que su Fuerza sea igual o
> superior a la indicada.»

Korrath tiene **Fuerza 8**, la más baja de la ficha, así que esta regla sería
un riesgo real. Pero:

- `Armadura de cuero` → `fuerza: null` (ligera, sin requisito).
- `Escudo` → `fuerza: null`.

En toda la tabla solo tienen requisito de Fuerza tres armaduras **pesadas**
(Cota de malla 13, Armadura de bandas 15, Armadura de placas 15), y Korrath no
lleva ninguna — ni podría usarla con provecho, siendo su entrenamiento solo de
armaduras ligeras. **Sin penalización: −0 m.**

### 3.3 Resultado

    velocidad = 10,5 m (Goliat) + 0 (Forma grande no aplica: nivel 5 y temporal)
                             − 0 (ninguna armadura con requisito de Fuerza)
              = 10,5 m

> **`velocidad` = 10,5 m**

---

## 4 · `cd_conjuros` y `bonif_ataque_conjuros`

### 4.1 ¿Lanza conjuros? Sí

`clases/druida.yaml → lanzador: completo` y
`clases/rasgos/druida.yaml → rasgos[Lanzamiento de conjuros]` (nivel 1, pdf 93,
libro 91). La ficha lo refleja: 3 trucos de clase + 4 conjuros preparados de
nivel 1 + `hablar con los animales` por Druídico, y la progresión de nivel 1
da `trucos: 2, prep: 4, slots: [2,0,…]`. **Procede calcular ambos valores.**

### 4.2 Aptitud mágica

Tres declaraciones concordantes:

- `clases/druida.yaml → aptitud_magica: Sabiduría`
- `clases/druida.yaml → atributos_basicos.caracteristica_principal: Sabiduría`
- `clases/rasgos/druida.yaml → Lanzamiento de conjuros.desc`: *«Aptitud mágica:
  Sabiduría.»*

Modificador de Sabiduría = **+3** (Sab 17, paso 0.1).

### 4.3 Las fórmulas

`reglas/generacion_personaje.yaml → conjuros` (`pagina: {pdf: 240, libro: 238}`,
sección «Tiradas de salvación / Tiradas de ataque»):

- `cd_salvacion.formula`: *«8 + modificador de aptitud mágica + bonificador por
  competencia»*
- `bonificador_ataque.formula`: *«modificador de aptitud mágica + bonificador
  por competencia»*
- `_nota_aptitud`: *«La aptitud mágica de cada clase la declara su propio
  fichero, en `clases/<clase>.yaml → aptitud_magica`.»*

### 4.4 Los números

    cd_conjuros            = 8 + 3 (mod. Sab) + 2 (PB) = 13
    bonif_ataque_conjuros  =     3 (mod. Sab) + 2 (PB) = +5

### 4.5 La segunda fuente de magia da el mismo número

Korrath tiene además la dote **Iniciado en la magia**
(`dotes/origen.yaml → dotes[Iniciado en la magia]`, pdf 203, libro 201), con
`aptitud_elegida: Sabiduría` en la ficha. La dote deja elegir *«Inteligencia,
Sabiduría o Carisma»* como aptitud mágica de sus conjuros (Rociada venenosa,
Resistencia, Buenas bayas), y aquí se eligió **Sabiduría**, la misma que la del
druida. Por tanto sus conjuros usan **la misma CD 13 y el mismo +5**: la ficha
tiene un único par de valores, no dos. (Si se hubiera elegido otra aptitud,
habría dos pares distintos y un solo campo `cd_conjuros` no bastaría para
describir la ficha; conviene tenerlo presente para otras fichas.)

Nota: `Orden primigenia` en su versión **Naturalista** (la elegida) da un truco
extra y un bonificador a pruebas de Conocimiento arcano y Naturaleza; **no**
toca la CD ni el ataque de conjuros. Si se hubiera elegido **Guardián**, habría
dado entrenamiento con armaduras medias, lo que sí habría cambiado el apartado
de la CA — pero no es el caso.

> **`cd_conjuros` = 13 · `bonif_ataque_conjuros` = +5**

---

## Valores derivados

| Valor | Resultado | Derivación en una línea | Cita principal |
|---|---|---|---|
| `pg_max` | **10** | 8 (máx. d8) + 2 (mod. Con 15) | `reglas/generacion_personaje.yaml → puntos_golpe.nivel_1` (pdf 42, libro 40) · `clases/druida.yaml → atributos_basicos.dado_golpe` |
| `ca` | **14** | 11 (cuero) + 1 (mod. Des 12) + 2 (escudo) | `equipo/armaduras.yaml → armaduras_ligeras.tabla` y `escudos.tabla` (pdf 218, libro 216) |
| `velocidad` | **10,5 m** | 10,5 de Goliat; sin modificadores permanentes | `especies/especies.yaml → Goliat.velocidad_m` (pdf 194, libro 192) |
| `cd_conjuros` | **13** | 8 + 3 (mod. Sab 17) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.cd_salvacion` (pdf 240, libro 238) |
| `bonif_ataque_conjuros` | **+5** | 3 (mod. Sab 17) + 2 (PB) | `reglas/generacion_personaje.yaml → conjuros.bonificador_ataque` (pdf 240, libro 238) |

Valores intermedios usados: mod. Fue −1 · mod. Des +1 · mod. Con +2 ·
mod. Int +1 · mod. Sab +3 · mod. Car 0 · PB +2.

**Condición del rasgo de especie:** «Forma grande» del Goliat **NO se cumple**
—el rasgo es de nivel 5 y el personaje es de nivel 1, y además su efecto es
explícitamente temporal («no de forma permanente»)—, así que la velocidad
permanente se queda en los 10,5 m de especie. La segunda condición que podía
mover la velocidad, el requisito de Fuerza de la armadura
(`armaduras.yaml → reglas.fuerza`), tampoco se dispara: ni la Armadura de cuero
ni el Escudo tienen requisito (`fuerza: null`), pese a que la Fuerza 8 del
personaje lo habría activado con cualquier armadura pesada.

**Todo se pudo derivar.** No hay ningún valor de los cinco que la base deje sin
declarar.

---

## Observaciones (ninguna bloquea la derivación)

1. **La fórmula de la CD de conjuros ya está en la base, y se nota.**
   `reglas/generacion_personaje.yaml → conjuros` (añadido el 2026-09-05) trae
   la fórmula con su página. El propio comentario del fichero cuenta que la
   fórmula vivía solo en `calculo.py` y que la destapó este mismo mandato de
   calculistas. Desde este lado del muro se confirma que **el hueco está
   cerrado**: esta derivación no ha tenido que suponer nada sobre la CD.
2. **La CA por defecto sin armadura no se ha necesitado** (Korrath lleva
   armadura). Según el encargo está declarada en el fichero que este método no
   puede abrir; no se apunta como hallazgo.
3. **Punto implícito, no hueco:** ningún fichero de `reglas/` dice en prosa
   «la velocidad de tu ficha es la de tu especie». Se deduce, sin ambigüedad
   real, de que `especies/especies.yaml` es el único sitio de la base que
   declara una velocidad de personaje, y lo hace con un campo explícito en
   metros (`velocidad_m`) para las 10 especies. Lo dejo anotado como
   observación de forma, no como dato que falte.
4. **Hallazgo menor, cosmético, encontrado al contar a mano:**
   `reglas/fuentes_de_efectos.yaml` dice **dos veces** «las 13 armaduras y el
   escudo» (una en el comentario de la sección `derivadas`: *«el motor fabrica
   de ahí la CA de las 13 armaduras, el +2 del escudo…»*; otra en el campo
   `derivadas[equipo/armaduras.yaml].que_es`: *«las 13 armaduras y el escudo»*).
   Eso suma 14. Contando la tabla registro a registro salen **13 en total**:
   3 ligeras + 5 medias + 4 pesadas = **12 armaduras**, más el escudo. El «13»
   está contando ya el escudo, y luego lo vuelve a sumar aparte. Es un desfase
   de uno en un texto descriptivo, sin consecuencia para el cálculo: el propio
   fichero declara que `que_es` *«es para los mensajes de error; no lo consume
   el motor»*, y `campos:` —lo que sí se consume— está bien. Se apunta porque
   es exactamente el tipo de número que nadie vuelve a contar. (Yo mismo lo
   escribí mal en el primer borrador de este informe, como 14 registros, y lo
   corregí al recontar: de ahí sale el hallazgo.)
5. **Aviso de diseño para otras fichas, no para esta:** un solo par de campos
   `cd_conjuros` / `bonif_ataque_conjuros` describe bien a Korrath **porque**
   la aptitud elegida en la dote Iniciado en la magia coincide con la del
   druida (Sabiduría en ambos casos). Un personaje que eligiera en esa dote una
   aptitud distinta de la de su clase tendría **dos** CD y **dos**
   bonificadores de ataque simultáneos, y un único campo no podría
   representarlo. La base permite esa elección (`dotes/origen.yaml → Iniciado
   en la magia`: *«aptitud mágica Inteligencia, Sabiduría o Carisma»*).
