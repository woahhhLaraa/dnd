# CONTINUAR — punto exacto de reanudación

> **Empieza aquí.** Todo el estado está en disco: **no depende de ninguna
> conversación previa.**
>
> Orden de lectura para retomar:
> 1. **este fichero**, empezando por «EMPIEZA AQUÍ SI RETOMAS EN OTRA
>    CONVERSACIÓN» — qué hay, qué falta, con qué números;
> 2. **`PLAN_18_REVISION_COMPLETA.md`** — **el plan de trabajo vigente**. Trae
>    los ocho casos del defecto de fondo, las cifras medidas y el orden de
>    los bloques A-G;
> 3. **`FUENTES.md`** — procedencia y las correcciones registradas, la más
>    reciente arriba (es largo; se lee por la sección que toque, no entero);
> 4. **`FODA.md`** — análisis vigente, si vas a decidir arquitectura;
> 5. **`PLAN_17_SALIR_DEL_ESPIRAL.md`** — solo por su §1 (investigación sobre
>    Foundry dnd5e y DiceCloud, leyendo su código) y su §2 (el diagnóstico del
>    espiral). Sus puntos abiertos están absorbidos en el 18;
> 6. **`_verificacion/_auditoria_rasgos/ESTADO_13p.md`** — detalle de la
>    auditoría de conjuros y las decisiones que salieron de ella.
>
> ⛔ **`FODA_2026-08-19_OBSOLETO.md` fue BORRADO el 2026-08-31** (Plan 17, §5).
> Describía una base de hace diez días y mandaba hacer fases ya cerradas; un
> documento del que hay que avisar «no lo leas» es un documento que ya sobra.
> Sigue en el historial de git si alguna vez hace falta.

Última actualización: **2026-09-02** — **bloques A y B del Plan 18 hechos**:
existe `censo.py` y los 30 chequeos `validar_*` tienen prueba por mutación.
Ver «EMPIEZA AQUÍ» más abajo.

---

## 🔎 EMPIEZA AQUÍ SI RETOMAS EN OTRA CONVERSACIÓN (2026-09-02)

**El plan de trabajo vigente es `PLAN_18_REVISION_COMPLETA.md`.** Absorbe lo
que quedaba abierto del 17. El 17 se conserva solo por su investigación sobre
Foundry y DiceCloud y por el diagnóstico del espiral.

### El estado en un vistazo

```bash
python3 validar.py            # 0 errores · 2,6 s
python3 verificar_srd.py      # 646 valores · 0 discrepancias
python3 verificar_foundry.py  # 3020 valores · 0 discrepancias
python3 cobertura.py          # 262 preguntas · 0 sin responder
python3 censo.py              # 697 unidades · 0 sin declarar · 515 pendientes
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done   # 17/17
python3 generar_ficha.py --barrido --exhaustivo   # 240/240 · 136 s
```

### Lo que se descubrió, y hay que entender antes de tocar nada

**1. Un mismo defecto, ocho veces: la cobertura escrita a mano.** Un módulo
lleva dentro la lista de lo que mira, y esa lista se queda corta sin que nadie
se entere. Cuatro cerrados (`_CA_SIN_ARMADURA`, `_ORIGENES`, las cifras de
`verificar_documentos`, `_TABLA_COSTE`) y, desde el **2026-09-02**, los cuatro
que quedaban: `validar._PROMESAS`, `verificar_chequeos.FUENTES` y
`verificar_srd.MAPA` cerrados, y `verificar_foundry.MODULOS` **medido y
declarado** —562 registros del SRD que nadie contrasta— como bloque H. Detalle
en el §2 y el §12 del Plan 18.

**2. El verificador estaba INVERTIDO con las dotes.** Una ficha de nivel 1 que
tomaba `Duro` y aplicaba bien su +2 PG era **rechazada**, y la misma ficha con
el +2 perdido pasaba con «0 problemas». Cerrado el 2026-08-31 (C1/C3 del Plan
17). La prueba de que sigue del derecho está en el §0 de ese documento.

**3. La regla inviolable 6 ya no es prosa: la comprueba `censo.py`.** (Siete
filas desde el bloque A2: se le añadió la de los módulos de herramienta.) Se añadió
el 2026-08-31 sin nada que la hiciera cumplir, y el propio repo ya tenía escrita
la lección en `FUENTES.md:208`: *«una regla en prosa no impide nada»*. Desde el
**2026-09-02** hay un script que enumera **siete clases de unidad** de la base y
exige que cada una esté alcanzada por algún chequeo o declarada con su motivo en
`_verificacion/censo_exenciones.yaml`. Hoy: **697 unidades, 0 sin declarar**. El
día que aparezca la novena lista, lo canta el censo.

**4. Los 30 chequeos `validar_*` YA tienen prueba por mutación** (eran 11 el
2026-08-31). El bloque B añadió tres suites —aritmética 31/31, contenido 47/47,
referencias 10/10— y la cifra ya no se cuenta a mano: la cuenta el censo, que
descubre los chequeos del AST de `validar.py` y las suites por patrón. **Con la
red puesta, el refactor del bloque F ya es una opción**, aunque la medición del
§5 del plan sigue diciendo que probablemente no haga falta.

**5. El 98 % del tiempo de `validar.py` era reparsear los mismos ficheros.**
1068 llamadas a `yaml.safe_load`. Con `lru_cache` en los lectores: **13,1 s →
3,9 s**. Seguro porque las mutaciones corren en subproceso sobre una copia.
**Contrato: lo que devuelven los lectores es de SOLO LECTURA.**

### Lo que queda, por orden (Plan 18 §8)

| Bloque | Qué | ¿Manual? |
|---|---|---|
| ~~**A**~~ | ~~`censo.py`~~ | ✅ **hecho (2026-09-02)** |
| ~~**B**~~ | ~~Mutaciones para los 19 chequeos sin red~~ | ✅ **hecho (2026-09-02)** |
| ~~**A2**~~ | ~~Las cuatro listas abiertas del §2~~ | ✅ **hecho (2026-09-02)** |
| **C** | Declarar los efectos que faltan. **Los 9 de `velocidad` ya están** (A2); quedan los de `ca` y `pg_max` — **lo siguiente** | no |
| **D** | `efectos:` obligatorio + `no_automatizado` | no |
| **E** | `requirements.txt`, versión de Python, ~50 líneas duplicadas | no |
| **H** | Contrastar los **562 registros** del SRD estructurado que nadie pide, entre ellos los 255 rasgos de `classes24` — **lo destapó el censo** | no |
| **F** | Refactor, **solo si sigue pareciendo necesario** | no |
| **G** | Los casos ambiguos y las descripciones de conjuro | **sí** |

### Y tres cosas que salieron al hacer A, B y A2, y conviene saber antes de tocar

- **Dos de los 30 chequeos no pueden fallar.** `validar_costes_sin_fuente` y
  `validar_referencias` solo llenan `warn`. Una referencia rota entre una
  especie y `hechizos.json` sale como ⚠ y `validar.py` termina con «0 errores».
  Está probado que el **aviso** salta; convertirlo en error es una decisión
  pendiente, no un descuido.
- ✅ **`COMPLETO`/`MEDIO` ya no existen** (A2): la tabla del lanzador completo
  se lee de la base, citada (pdf 47 = libro 45), y la del medio se DERIVA de
  ella con la regla del propio manual.
- **Ningún chequeo mira `classes24`**, que son 279 registros del SRD 5.2 sobre
  clases y subclases — la fuente natural de la «Foundry Note» del bloque D.

---

## 🔧 Qué pasó el 2026-08-31 — se aplicó el Plan 17 (C1, C3, C4)

Plan y método en **`PLAN_17_SALIR_DEL_ESPIRAL.md`**, escrito tras leer el
código real de Foundry dnd5e y DiceCloud.

**El defecto que se cierra, y estaba invertido.** 54 de las 75 dotes conceden
«Mejora de característica: X +1», y ese +1 vivía solo dentro de la cadena
`descripcion`. `efectos.py` tampoco miraba `dotes/`. Resultado medido:

| Ficha | Antes | Ahora |
|---|---|---|
| `Duro` (nivel 1) con su +2 PG aplicado — CORRECTA | ❌ rechazada | ✅ |
| `Duro` con el +2 perdido — ROTA | ✅ «0 problemas» | ❌ |
| `Actor` (nivel 4) con su +1 Car aplicado — CORRECTA | ❌ rechazada | ✅ |
| `Actor` con el +1 perdido — ROTA | ✅ «0 problemas» | ❌ |

**La causa raíz, y por qué era el mismo error de siempre.** `efectos._ORIGENES`
era una tupla de 15 rutas escritas a mano: conocía 2 de las 48 subclases y 0 de
los 4 ficheros de dotes. Es exactamente lo que la cabecera de
`reglas/efectos.yaml` condena para las fórmulas de CA cableadas —«no se entera
de que hay una quinta»—, repetido un nivel más arriba: un diccionario de
FÓRMULAS sustituido por una tupla de RUTAS.

**Lo que se hizo:**

- **C1** — `_ORIGENES` desaparece. `efectos.origenes()` descubre las fuentes por
  patrón y las contrasta con el manifiesto nuevo `reglas/fuentes_de_efectos.yaml`.
  Un fichero de regla que ningún patrón sepa recorrer y que no esté declarado
  como excluido **es un error**. De 15 fuentes cableadas a **30 descubiertas**.
- **C3** — `mejora_caracteristica` estructurado en las 54 dotes, derivado de la
  prosa YA citada con **ida y vuelta 54/54 exacta** (el método de la Fase 15).
  La ida y vuelta salvó un error real: los **12 dones épicos dicen «máx. 30»**,
  no 20. `verificar_personaje.py` cuenta el +1 de la dote en `final`, y la ficha
  declara su elección con `sube:`.
- **C4** — `conditional` entra al vocabulario (de DiceCloud): un efecto citado
  que guarda texto y **no** se agrega. Filtrado en `agregar()`.
- Borrado `clases/subclases/_borrador_mapa.yaml` (borrador no verificado que
  ningún script leía, y que con C1 habría pasado a ser fuente).

**Defecto encontrado en los propios datos:** `personajes/draconido_hechicero_n4.yaml`
tomaba `Lanzador ritual` (+1 a Int/Sab/Car) y **no aplicaba el +1**. Estaba con
Carisma 17, CD 13, ataque +5 y CA 15 cuando debía ser 18/14/+6/16. Corregida y
documentada en su bloque `decisiones`.

**Lo que NO se hizo, y por qué:** la Fase C5 (declarar los ~528 registros de
rasgo) exige leer el manual página a página. La regla 1 del proyecto lo
prohíbe de cualquier otra forma, así que queda abierta. C2 (hacer `efectos:`
obligatorio) va después de C5, no antes, para no dejar la base en rojo durante
todo el relleno.

---

## Dónde vive esto (nuevo, 2026-08-30)

**El proyecto está en git**, en un repositorio privado:
`git@github.com:woahhhLaraa/dnd.git`, rama `master`. Hasta el 2026-08-30 no
tenía control de versiones ninguno, que era su mayor fragilidad operativa: un
`sed` mal escrito sobre 391 conjuros no tenía vuelta atrás, y este documento
llevaba semanas siendo la única memoria del proyecto.

`.gitignore` solo excluye `__pycache__` y `.pyc`. **El SRD de `_verificacion/`
va dentro a propósito** (13 de los 16 MB): sin él los contrastes externos no son
reproducibles, y es CC-BY-4.0.

## Qué es esto

Una base de datos canónica de **D&D 2024 (5.5e) en castellano**, transcrita del
Manual del Jugador por lectura visual de las páginas del PDF, pensada para que
un **LLM orquestador** cree y suba de nivel personajes **sin usar nada de su
conocimiento previo**. Toda la autoridad vive en la base; el LLM solo consulta
y arbitra citando.

Eso impone las **reglas inviolables** del final de este documento. La más
importante: *consultar, no recordar*.

## Estado en cuatro comandos

```bash
python3 validar.py            # coherencia interna    -> 0 errores
python3 verificar_srd.py      # contraste externo     -> 646 valores, 0 discrepancias
python3 verificar_foundry.py  # contraste externo     -> 3020 valores, 0 discrepancias
python3 cobertura.py          # ¿puede responder?     -> 0 preguntas sin responder
python3 censo.py              # ¿algo sin chequeo?    -> 0 unidades sin declarar
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done   # 12/12
```

Y las pruebas por mutación, que es lo que da derecho a fiarse de lo anterior:

```bash
python3 _verificacion/mutaciones_dados.py         # dados
python3 _verificacion/mutaciones_conversiones.py  # conversiones de unidad
python3 _verificacion/mutaciones_integridad.py    # tirada, vecindad, ortografía -> 24/24
python3 _verificacion/mutaciones_foundry.py       # contraste externo            -> 29/29
```

Y las tres del bloque B (2026-09-02), que cierran los 19 chequeos que no
tenían red, más la del censo:

```bash
python3 _verificacion/mutaciones_aritmetica.py    # los 5 de aritmética  -> 32/32
python3 _verificacion/mutaciones_contenido.py     # los 11 de contenido  -> 49/49
python3 _verificacion/mutaciones_referencias.py   # los 3 de referencias -> 10/10
python3 _verificacion/mutaciones_censo.py         # el propio censo      -> 18/18
```

**No hace falta acordarse de ninguna:** `verificar_documentos.py` las descubre
por patrón desde el 2026-09-02 (antes llevaba los diez nombres escritos a
mano) y comprueba que sus cifras coincidan con lo que digan los documentos.

Y uno que comprueba **este mismo fichero**:

```bash
python3 verificar_documentos.py   # ¿las cifras de CONTINUAR.md y FODA.md son ciertas?
python3 verificar_chequeos.py     # ¿algún chequeo abandona un registro EN SILENCIO?
```

Existe porque el 2026-08-29 hubo que corregir **tres documentos de estado** que
describían como pendiente algo ya hecho. En un proyecto cuyo estado vive en
disco, **un documento desfasado es un defecto de datos, no de estilo**: quien lo
lea trabajará hacia atrás. No puede comprobar la prosa, pero sí las cifras, que
es donde el desfase se vuelve mentira comprobable.

`validar.py` debe dar, dentro de «INTEGRIDAD»: 683 dados · 543 conversiones ·
391 conjuros en `tirada` · 677 pares de vecindad · 782 campos de ortografía ·
391 citas de conjuro · 52 costes sin fuente externa · 18 efectos · 6
materiales descompuestos · 8 conjuros con `tiradas` por efecto · 25 ataques
de conjuro contrastados contra su texto · 65 prerrequisitos de dote evaluables ·
333 saltos de nivel derivables · **54 mejoras de dote** (chequeo nuevo, C3 del
Plan 17). Los `efectos` pasaron de 7 a **8** el 2026-08-31 (`Duro` es la primera
dote con efecto declarado, posible solo desde que C1 hizo que el motor mire
`dotes/`) y de 8 a **18** el 2026-09-02: el bloque A2 metió las frases de
promesa de `velocidad` en la base y eso destapó **nueve rasgos** que la
prometían en su texto sin que nadie pudiera calcularla. **Todo a 0
errores**, con un aviso esperado: la CA base sin armadura (`10 + mod_des`) no
tiene página citada, y está declarado como hueco abierto, no inventado.

Si todo eso da eso, la base está como se dejó. Contenido cerrado: 391
conjuros, 12 clases con tabla completa y competencias, 48 subclases, 158
rasgos de clase con texto, 75 dotes, 10 especies, 16 trasfondos, equipo,
munición, habilidades, idiomas, reglas de generación y multiclase.

**No queda manual que transcribir, y desde el 2026-08-29 tampoco queda manual
que auditar:** cerradas la Fase 13p (descripciones) y la 13q (nombres y
resúmenes). Lo que queda es **diseño de producto** (Fases 14-16) más una lista
corta de flecos, en «Lo que queda abierto» más abajo.

## 👉 Lo que queda por hacer

### Fase 8a — cimientos + `/personaje` (✅ construida, 2026-08-19)

Las tres decisiones de producto ya están tomadas y construidas:

1. **Estado del personaje** → `personajes/<nombre>.yaml`, dentro de la base.
   Contrato en `personajes/_ESQUEMA.md`; ejemplo verificado en
   `personajes/_ejemplo_aerin.yaml`.
2. **Interacción** → paso a paso, preguntando, mostrando solo lo que la base
   permite en cada paso (`.claude/skills/personaje/SKILL.md`).
3. **Automatización** → toda la aritmética la hace `calculo.py` (nunca el
   LLM a mente); las consultas deterministas que fallan ruidosamente viven
   en `buscar.py`; la trazabilidad la comprueba `verificar_personaje.py`.

Para crear un personaje: `/personaje` (skill de proyecto, ámbito
`base-canonica/`). Antes de tocar estos ficheros, correr los tres
validadores de la base + `python3 verificar_personaje.py <ficha>` sobre
cualquier ficha existente.

### Plan ampliado tras el análisis de repos (2026-08-21)

`ANALISIS_REPOS.md` cambió el orden de trabajo. `/subir-nivel` sigue siendo el
destino, pero construirla directamente sobre `calculo.py` tal como está
significaría heredar sus casos cableados y un contraste externo que solo cubría
tablas de clase.

| Fase | Qué | Estado |
|---|---|---|
| **13** | Verificación ancha + auditoría visual de lo que ninguna fuente externa cubre | ✅ **hecha (2026-08-21)**; 13m cerrada el 2026-08-22 |
| **13m** | Auditoría visual de los 87 conjuros fuera del SRD | ✅ **cerrada (2026-08-22)**, cola aplicada |
| **13n** | **Cierre de la lectura visual**: 4 placeholders transcritos, dotes + trasfondos + equipo auditados (5 agentes), `validar_dados()` | ✅ **hecha (2026-08-22)** |
| **13o** | **Muestra aleatoria de 40 descripciones de conjuro** | ✅ hecha (2026-08-22): midió **17,5 %** y bloqueó la Fase 14. **Acertó**: el valor final sobre 305 fue 15,7 % |
| **13p** | Auditar las 266 descripciones restantes | ✅ **CERRADA (2026-08-29)**. 305 conjuros auditados, **48 con defecto = 15,7 %** (IC 11,8-20,3 %). Detalle en `_verificacion/_auditoria_rasgos/ESTADO_13p.md` |
| **13q** | Pasada de cabeceras: `nombre` y `resumen` de los 302 ya auditados | ✅ **hecha (2026-08-29)**: 16 correcciones, 13 de ellas en `resumen` |
| **13r** | Costes del componente material: módulo nuevo contra el SRD (309) + lectura de los 52 sin fuente externa | ✅ **hecha (2026-08-29)**: 5 correcciones, y el modo de fallo «dato agregado» |
| **13s** | **Muestra aleatoria POST-corrección** — ¿cuánto error QUEDA? | ✅ **hecha (2026-08-29)**: 4 de 36 = **11,1 %** (IC 3,1-26,1). Es el número con el que se entra en la Fase 14 |
| **14** | Motor de efectos (modelo DiceCloud): las reglas dejan de ser `if` de Python y pasan a ser dato citado | ✅ **cerrada la mitad de STATS (2026-08-29)**: `efectos.py`, 6 efectos citados, `validar_efectos()`, mutaciones 20/20, 12/12 fichas. La mitad de CONJUROS sigue abierta → **14b** |
| **14b** | ✅ **CERRADA (2026-08-30)**. Plan en `PLAN_14b_15.md`. **14b-1, 14b-2 y 14b-3 ✅ hechas.** `pg_max` como historia por nivel · material compuesto contrastado · `tiradas` por efecto en los 4 conjuros que rompían el campo único. **La Fase 14 queda cerrada.** Efectos de conjuro: un conjuro es una lista de efectos, no un registro plano (*Símbolo* 6 modos, *Muro prismático* 7 capas, `coste` compuesto) | ⬜ **SIGUIENTE.** El vocabulario ya está probado por mutación; falta extenderlo a 391 registros con ~11 % de residuo |
| **15** | Prerrequisitos evaluables: 65 de las 75 dotes, **11 formas** con **4 átomos y 2 conectores**, **0 negaciones** | ✅ **CERRADA (2026-08-30)**: ida y vuelta 65/65, `buscar.dotes_disponibles()`, mutaciones 10/10 |
| **16 (= 8b)** | `/subir-nivel` con la taxonomía de *advancement* de Foundry | ✅ **CERRADA (2026-08-30)**: `subir_nivel.py`, `validar_subida()` sobre **333 saltos**, skill `/subir-nivel`, y una ficha subida de verdad de nivel 3 a 4. Plan en `PLAN_16.md` |

---

## 📌 Estado exacto al cerrar el 2026-08-21

**Lee esto si retomas el proyecto en otra conversación.** Todo lo que sigue
está en disco y es reproducible con los cuatro comandos de arriba.

### Lo que se hizo hoy

1. **Se investigaron DiceCloud, Foundry dnd5e, PCGen y Open5e** leyendo su
   código, no sus README → `ANALISIS_REPOS.md`. Conclusión: ninguno aporta
   contenido que sustituya a la base (todos son inglés y/o subconjunto SRD);
   lo que aportan es arquitectura. Material descargado en
   `_verificacion/foundry_srd52/` (datos) y `../_referencias/` (código, fuera
   de la base a propósito).

2. **`verificar_foundry.py` — cuarto validador, 8 módulos, 2689 valores.**
   Contrasta conjuros (banderas + alcance/duración/tiempo), armas, armaduras,
   especies, dotes, trasfondos y herramientas contra el SRD 5.2 estructurado.
   **No traduce: empareja por claves independientes del idioma y deduce los
   vocabularios**, exigiendo que sean biyecciones. Probado por mutación en
   `_verificacion/mutaciones_foundry.py` → **29/29**.

3. **Cuatro auditorías visuales con 12 agentes Sonnet** (tres tandas de 4),
   ficheros disjuntos, informes en `_verificacion/_auditoria_rasgos/`. Los
   agentes **solo informan**; las correcciones se aplicaron tras releer la
   página. Cubrieron los 158 rasgos de clase, las 48 subclases con sus 241
   rasgos, las 10 especies con sus 38 rasgos y 14 linajes, y los 87 conjuros
   que el SRD no cubre.

4. **71 defectos propios corregidos**, todos verificados en la página antes de
   tocar nada:
   - **41** de `consume_material` (el mayor defecto de la base, ver 13m)
   - 9 en `hechizos.json` (componentes V/S invertidos, concentración marcada
     como ritual, dos escuelas equivocadas) — heredados del CSV de origen
   - 13 citas de página falsas (9 en rasgos de clase, 4 en subclases)
   - 4 descripciones/nombres de conjuro (`Mano de Bigby`, `Insecto gigante`,
     `Desintegrar`, `Adivinación`) + el coste espurio de `Toque helado`
   - 1 error de contenido: la `nota` de `clases/picaro.yaml` decía «mejoras
     extra en niveles 6 y 10» contradiciendo su propia tabla
   - 1 cita de fichero: la `fuente` de `equipo/herramientas.yaml`

5. **Cinco casos en los que el SRD se equivoca y manda el manual**, anotados
   como excepciones **citadas** dentro de `verificar_foundry.py` (no
   silenciadas): *Patrón hipnótico* ×2, *Prohibición*, *Mal de ojo*,
   *Alzar a los muertos*, más el peso de los *Útiles de herborista*.

6. **`validar.py` — un invariante ampliado.** El chequeo de orden de página
   bloqueaba una cita correcta («Acción súbita (dos usos)», que el manual
   describe una sola vez); ahora contempla las repeticiones distinguidas con
   paréntesis. Probado por mutación: 3/3.

7. **Margen de error medido** con intervalos Clopper-Pearson exactos →
   sección «📏 Margen de error» de `FODA.md`.

### Lo que enseñó, y conviene no olvidar

- **El CSV de conjuros es la parte débil de la base.** Van tres veces que
  falla. «Datos ya estructurados» no significa datos correctos: salió peor
  parado que la lectura visual.
- **De los 14 defectos de las auditorías visuales, 13 eran citas de página y
  solo 1 era contenido.** El texto mecánico estaba bien. Lo que falla
  sistemáticamente es *dónde* se dice que está cada cosa — y es justo el dato
  que sostiene la auditabilidad, el único que ninguna fuente externa puede
  comprobar.
- **Criterio de citas, ya fijado:** una cita apunta a la página donde está la
  **mecánica**, no donde empieza la sección. (Nació de rechazar dos hallazgos
  sobre Elfo y Tiefling.)
- **El fallo silencioso reaparece solo.** Dos veces hoy un registro dejó de
  emparejar y **desapareció del contraste sin dar error** (maestrías de arma,
  precio de herramienta). Cualquier módulo nuevo debe tratar «se cayó del
  emparejamiento» como error, no como ausencia.
- **Verificar el trabajo de un agente incluye verificar su explicación.** Un
  agente acertó un hallazgo e inventó la causa (páginas duplicadas en el PDF,
  falso: comprobado píxel a píxel).
- **Cuando tres agentes independientes señalan lo mismo, es real.** Así salió
  el bug de `consume_material`. Y la causa no estaba donde parecía: el CSV sí
  tenía el dato bueno (el asterisco), solo que la conversión leyó otra columna.
  **Antes de dar un campo por irrecuperable, mira si la fuente lo codificaba
  en otro sitio.**
- **Un campo lleno puede estar más vacío que uno nulo.** Cinco conjuros decían
  «(Revisar efectos en el MdJ)»: ningún chequeo de completitud los veía. Si un
  dato remite al manual, la base ha dejado de ser autosuficiente.
- **Un dato con la forma correcta puede ser basura.** `3d0` pasó las cuatro
  capas porque es sintácticamente un dado. La validación de forma no basta: hay
  que validar también el **vocabulario** (qué caras existen, qué unidades, qué
  escuelas). De ahí `validar_dados()`.
- **Prueba los chequeos nuevos en las dos direcciones.** La primera versión de
  `validar_dados()` se disparaba con su propia documentación: encontró tres
  `d0` y los tres estaban en la `_nota_verificacion` que explica el arreglo. Un
  chequeo probado solo en la dirección de detectar acaba prohibiendo documentar
  lo que corrigió. Por eso `mutaciones_dados.py` lleva 6 controles negativos.
- **Un informe de agente en blanco no prueba nada por sí solo.** En la tanda del
  22 salieron cuatro lotes limpios de cinco. Antes de darlos por buenos se
  remuestrearon dos superficies enteras a mano (la tabla de equipo de libro 223
  y dos trasfondos) y coincidieron. Sin ese contraste, «0 hallazgos» es
  indistinguible de «no lo he mirado».

### 🔴 Lo que queda ciego, por orden de importancia

| Superficie | Estado |
|---|---|
| ~~87 conjuros fuera del SRD~~ | ✅ auditados (Fase 13m) |
| ~~Descripción de las 75 dotes~~ | ✅ auditadas (Fase 13n) — 1 hallazgo |
| ~~Equipo inicial de los 16 trasfondos~~ | ✅ auditado (Fase 13n) — 0 hallazgos |
| ~~121 objetos de equipo y munición~~ | ✅ auditados (Fase 13n) — 0 hallazgos |
| ~~Descripción de los 306 conjuros del SRD~~ | ✅ **auditados los 305 emparejados** (Fase 13p). Tasa final **15,7 %**, 48 conjuros corregidos |
| ~~`nombre` y `resumen` de los conjuros~~ | ✅ **auditados** (Fase 13q): 3 erratas de nombre y 13 resúmenes falsos |
| ~~Campo `clases` de los conjuros~~ | ✅ contrastado (módulo `conjuros-clases`, 278 conjuros) |
| ~~Conversiones de unidad~~ | ✅ chequeo permanente (`validar_conversiones`, 562 equivalencias) |

## 📌 Estado al cerrar el 2026-08-27

**Se retomó la Fase 13p, que estaba parada con la oleada 1 sin recoger.** Hechas
dos oleadas completas: **131 de los 266 conjuros auditados, 19 defectos
aplicados**, todos con doble lectura. Detalle en `FUENTES.md` (oleadas 1 y 2) y
progreso en `ESTADO_13p.md`.

**La tasa medida se sostiene: 14,5 % (19/131)**, dentro del IC de la muestra
aleatoria de la Fase 13o (17,5 %, IC 7,3 %–32,8 %). No era un artefacto del
muestreo. La Fase 14 sigue bloqueada. *(Al cerrar el 2026-08-27. Se desbloqueó el 29 y su mitad de stats quedó cerrada ese mismo día.)*

### Lo que enseñó, y no estaba en la lista

- **Dos modos de fallo nuevos**, ambos invisibles a cualquier chequeo previo:
  - **7 · Regla inventada que tapa a la real.** *Creación* prohibía algo que el
    manual permite y omitía la prohibición que sí impone. *Dominar monstruo*
    concedía un «control total de las acciones del objetivo» que la página no
    da. No es texto que falte: es texto de más que **suena a regla**.
  - **8 · Lista de `clases` mal.** *Clarividencia* decía `["Mago"]` donde la
    cabecera lista cuatro clases. **Una lista corta pasa por lista buena** — el
    cruce `hechizos ⊆ clases` solo ve nombres inexistentes. Ya tiene chequeo:
    módulo `conjuros-clases`, 278 conjuros contrastados.
- **Una regla puede estar invertida y sonar perfecta.** *Geas* decía que el
  objetivo «falla automáticamente» donde el manual dice que **la supera**
  automáticamente. Las dos versiones son fluidas y plausibles; solo la página
  distingue.
- **Dos métodos independientes que coinciden valen más que dos pasadas del
  mismo.** *Engañar* lo encontraron el mismo día un agente leyendo la página y
  el script nuevo contrastando contra el SRD, sin saber el uno del otro.
- **La lista de conversiones sospechosas del 22 estaba incompleta** (decía 6,
  eran 9): el barrido a mano no cubría km→pies. Un chequeo permanente encuentra
  lo que un barrido de usar y tirar se deja.

### Reparto de modelos (regla nueva, 2026-08-27)

**Toda lectura la hace un agente Sonnet; Opus piensa, valida y aplica.** Leer
páginas es lo más caro del proyecto y no necesita el modelo grande; el criterio
sí. La regla «releer personalmente antes de aplicar» se cumple ahora con un
**segundo agente independiente** que relee la página **sin ver el informe del
primero**, contestando preguntas cerradas. Los 10 hallazgos de la oleada 2
pasaron por ahí y los 10 se confirmaron. Método en `ESTADO_13p.md`.

## 📌 Qué pasó el 2026-08-29 — **la lectura visual ha terminado**

Sesión larga. Se cerraron **la Fase 13p** (descripciones de conjuro), **la 13q**
(nombres y resúmenes), **los cinco flecos previos** a la Fase 14 y **los costes
de material**. Se aplicaron **~80 correcciones** y se escribieron **seis
chequeos permanentes nuevos**. Todo está registrado en `FUENTES.md`, entrada por
entrada y con su página.

### Superficies auditadas, y con qué resultado

| Superficie | Auditados | Con defecto | Tasa |
|---|---|---|---|
| Descripciones de conjuro (Fase 13p) | 305 | 48 | **15,7 %** (IC 11,8-20,3) |
| `resumen` (Fase 13q) | 302 | 13 | 4,3 % |
| `nombre` (Fase 13q) | 302 | 3 | 1,0 % |
| Coste del material dentro del SRD | 309 | 2 | 0,6 % |
| Coste del material fuera del SRD | 52 | 3 | 5,8 % |
| **Muestra aleatoria POST-corrección** | **36** | **4** | **11,1 %** (IC 3,1-26,1) |

**No queda superficie de conjuro sin contrastar.** Descripciones, nombres,
resúmenes, `clases`, `tirada`, costes dentro y fuera del SRD: todo mirado.

### 🚨 El dato que manda ahora: el residuo, no la tasa inicial

**~11 % de residuo (IC 3,1-26,1) sobre texto YA corregido.** Dos lecturas, y la
segunda importa más:

- **No se puede afirmar que la tasa haya bajado.** El IC de la muestra se solapa
  entero con el de antes (15,7 %). Con n=36 no se distingue un 11 % de un 16 %.
- **Sí se puede afirmar que auditar no deja limpio.** **Los 4 defectos de la
  muestra estaban en conjuros ya auditados**, y dos habían pasado por la
  oleada 4 *ese mismo día*. *Terremoto* llevaba tres correcciones aplicadas por
  la tarde y aún escondía dos reglas mal.

**Criterio de parada, ya fijado:** el objetivo no es «texto sin errores» sino
**«texto con un margen conocido»**. Perseguir el cero no converge — el coste por
defecto encontrado subió de 6,4 a 9,0 lecturas, y llegar al 1 % pediría ~900
lecturas más.

**Dónde sí queda margen barato: el código.** De los 4 defectos residuales, **2
eran atacables sin abrir el manual**. Cada chequeo escrito hoy encontró defectos
en su primera ejecución. La lectura visual tocó techo; el código no.

### Los seis chequeos nuevos (todos probados por mutación)

| Chequeo | Dónde | Qué vigila |
|---|---|---|
| `validar_tirada()` | `validar.py` | vocabulario cerrado + concordancia con la propia descripción |
| `validar_vecindad()` | `validar.py` | `resumen` idéntico entre vecinos (error) y solapamiento alto (aviso) |
| `validar_ortografia()` | `validar.py` | inglés sin traducir, palabras pegadas, «salvamento» |
| `validar_citas_conjuro()` | `validar.py` | `pagina_libro` numérica en los 391 |
| `validar_costes_sin_fuente()` | `validar.py` | coste verificado en los 52 conjuros fuera del SRD |
| coste del material | `verificar_foundry.py` | la cifra contra el SRD (+45 valores: 2967 → 3012; la Fase 14b-2 lo subió a **3020** al dejar de eximir a los 6 compuestos) |

### Decisiones tomadas, para no volver a abrirlas

1. **Semántica de `tirada`.** `TdS X` = la salvación **dispara** el conjuro;
   `Directo` = el conjuro **se manifiesta igual** y la salvación modula. Deducida
   de los datos (conjuros gemelos coinciden; la primera salvación cae en la
   mediana del 24 % del texto en los `TdS` y del 48 % en los `Directo`).
   4 correcciones, 10 confirmaciones, marcadas con `_tirada_revisada`.
2. **`coste` = valor mínimo del material**, se consuma o no. Lo que se gasta lo
   dice `consume_material`. **Revierte una decisión del 22 de agosto** que
   confundía ambos campos (ver `FUENTES.md`).
3. **Criterio de cita:** en conjuros, `pagina_libro` es donde **empieza** el
   conjuro; en rasgos, donde está la **mecánica**. No es incoherencia: un conjuro
   tiene cabecera propia, un rasgo es un fragmento dentro de una sección.
4. **El asterisco de `"310*"` no significaba nada.** Tres hipótesis probadas; la
   mejor falla en 5 de 6 casos leídos. Apartado a `fuente._pagina_origen_csv`.
5. **`fidelidad` declarada** en 38 ficheros YAML y en `_meta` de `hechizos.json`,
   que se declara **`mixto`** — y por qué no se pudo clasificar por registro.
6. **Conversiones a pies:** aparcadas a petición del usuario. **23 páginas
   leídas por nueve lectores no imprimen ni una unidad imperial**: las añadió la
   base entera. Ya declaradas en `_meta` como añadido editorial, así que la base
   no las presenta como cita. Quitarlas del texto (330 en 178 conjuros) es
   preferencia editorial, y el barrido está escrito en `ESTADO_13p.md`.

### Modos de fallo nuevos, descubiertos hoy

- **10 · Dato agregado.** *Vínculo protector* guardaba «100 po» donde la página
  dice «50 po **cada uno**» de un par; *Cofre oculto de Leomund* guardaba
  «5050 po» donde hay **dos materiales** (5000 + 50). No falta texto ni sobra:
  alguien **hizo una operación y guardó el resultado**, perdiendo el desglose.
  Invisible a cualquier chequeo de forma.
- **El `resumen` falla por generalizar.** 13 de 302, y casi todos dicen **más**
  de lo que el conjuro hace: «nadie», «siempre», «no deja retorno», «mágicas».
  Prosa escrita desde el título, no desde el texto.
- **Un epígrafe puede mentir tanto como una regla.** *Shillelagh* titulaba su
  mejora «Con un espacio de conjuro de nivel superior» **siendo un truco**: una
  mecánica imposible, en una frase que aparece correctamente en cientos de
  conjuros y que por eso nadie lee con desconfianza.

### Lo que enseñó el método

- **El remuestreo se ganó el sueldo.** El lote B5 declaró 0 hallazgos en 14; al
  releerlo a ciegas apareció uno real (*Rayo nauseabundo*, con un párrafo que la
  página no trae). La regla «un informe en blanco no prueba nada» pasa de
  prudencia a evidencia.
- **El chequeo que escribes sin haber visto el defecto no cubre el defecto.**
  `validar_tirada()` nació de un campo que *contradecía* al texto, y por eso no
  vio el caso contrario —un campo sin nada con lo que contradecirse—, que es
  *Resurrección*. Lo encontró una relectura.
- **La prueba por mutación encontró un defecto que el chequeo no veía.** Salió
  18/21: dos fallos eran de las mutaciones y **uno era real**, y al arreglarlo
  aparecieron dos erratas más en la base.
- **Una convención que solo vive en prosa se rompe sola.** La de `coste` llevaba
  una semana escrita en `FUENTES.md` (1500 líneas) y se rompió sin querer. Ahora
  vive en `validar.py` y en `_nota_verificacion` dentro de los registros.
- **Los documentos de estado envejecen más rápido de lo que se actualizan.**
  Hoy hubo que corregir **tres** que describían como pendiente algo ya hecho
  (`FODA.md`, `CONTINUAR.md`, `ESTADO_13p.md`). En un proyecto cuyo estado vive
  en disco, **eso es un defecto de datos, no de estilo**: quien los lea trabajará
  hacia atrás. Conviene revisarlos al cerrar cada tanda, no al final.

### ✅ Los flecos previos a la Fase 14 — cerrados el 2026-08-29

| # | Fleco | Resultado |
|---|---|---|
| 1 | Muestra aleatoria post-corrección | ✅ **4 defectos en 36 = 11,1 %** (IC 3,1-26,1). Semilla fija `20260829`, reproducible, en `MUESTRA_POST.json` |
| 2 | Remuestrear el lote B5 (salió 0 de 14) | ✅ **encontró 1 real**: *Rayo nauseabundo* tenía un párrafo de mejora que **la página no trae** |
| 3 | Tipo de acción en los 7 «acción bonus» | ✅ **los 7 correctos**, 0 correcciones. Marcados con `_accion_verificada` |
| 4 | Los 3 avisos de vecindad | ✅ **las 3 parejas legítimas**; el chequeo ya no vuelve a pedir la misma lectura (`_vecindad_verificada`) |
| 5 | Criterio de cita y el asterisco | ✅ `pagina_libro` = donde **empieza** el conjuro, hoy **numérica en los 391**. El asterisco **no tenía semántica**: 3 hipótesis probadas, la mejor falla en 5 de 6 casos leídos. Apartado a `fuente._pagina_origen_csv` |
| 6 | Las ~550 conversiones a pies | ⏸️ **aparcado a petición del usuario.** Ya declaradas en `_meta` como añadido editorial |

### 🚨 El dato con el que se entra en la Fase 14

**Residuo medido: ~11 % (IC 3,1-26,1 %) sobre texto YA corregido.**

Dos cosas hay que leer juntas:

- **No se puede afirmar que la tasa haya bajado.** El IC de la muestra se solapa
  entero con el de antes (15,7 %, IC 11,8-20,3). Con n=36 no se distingue un
  11 % de un 16 %.
- **Sí se puede afirmar que auditar no deja limpio.** **Los 4 defectos de la
  muestra estaban en conjuros ya auditados**, y dos habían pasado por la
  oleada 4 *ese mismo día*. *Terremoto* llevaba tres correcciones aplicadas por
  la tarde y aún escondía dos reglas mal.

**Consecuencia para el criterio de parada, y conviene tenerlo escrito antes de
empezar la 14:** el objetivo no puede ser «texto sin errores» sino **«texto con
un margen conocido»**. Una segunda pasada sobre lo ya auditado sigue
encontrando cosas y una tercera probablemente también, con rendimientos
decrecientes y sin punto de corte natural.

**Qué significa para el motor de efectos:** codificar una regla con su cita
convierte un error en algo que nadie vuelve a comprobar. Con un residuo del
orden del 10 %, la Fase 14 debería **preferir el enlace a la cita sobre la copia
del texto**, para que corregir la base siga arreglando el motor —que es
exactamente la regla que `personajes/_ESQUEMA.md` ya impone a las fichas.

Si se quisiera estrechar el intervalo antes de decidir, hace falta **una muestra
bastante mayor** (n≈150 para separar 11 % de 16 % con confianza), no otra de 36.

### 🎁 Lo que la Fase 14 debe heredar, y conviene no redescubrir

- **Modo de fallo nº 10, nuevo: «dato agregado».** *Vínculo protector* guardaba
  «100 po» donde la página dice «50 po **cada uno**» de un par de anillos, y
  *Cofre oculto de Leomund* guardaba «5050 po» donde la página da **dos
  materiales** (cofre 5000 + réplica 50). No falta texto ni sobra, ni hay
  ninguna cifra «mal»: alguien **hizo una operación y guardó el resultado**,
  perdiendo el desglose. Solo se ve contrastando contra una fuente que conserve
  la descomposición, y es invisible a cualquier chequeo de forma.
- **`coste` no puede representar varios materiales ni precios por unidad.** Seis
  conjuros llevan formato compuesto declarado en `COSTE_COMPUESTO`. Con `tirada`
  van **tres campos** que se quedan cortos por la misma razón: **un conjuro es
  una lista de efectos y de materiales, no un registro plano.**

- **Un conjuro no tiene «una tirada»: tiene efectos, y cada efecto la suya.**
  *Símbolo* tiene 6 modos con salvaciones distintas y *Muro prismático* 7 capas
  que mezclan modular daño con disparar estados. El campo `tirada` no puede
  representarlos, y están anotados con esa limitación en `_tirada_semantica`.
  **El modelo de efectos debería nacer sabiéndolo.**
- ~~**`calculo.py` tiene reglas cableadas**~~ → ✅ **convertidas en dato el
  2026-08-29.** Y al hacerlo se vio que eran peores de lo que se creía:
  `_CA_SIN_ARMADURA` conocía **2 de las 4** fórmulas de CA base de la base (las
  otras dos están en SUBCLASES), y `bonus_pg_especie` cubría **1 de los 2**
  efectos de PG, con un `1` fijo, sin que nadie obligara a rellenarlo — la
  única ficha de Enano lo tenía vacío y verificaba en verde con los PG mal.
  Detalle en `FUENTES.md` y `reglas/_ESQUEMA_efectos.md`.
- **Los cinco casos donde el SRD se equivoca y manda el manual** están anotados
  como excepciones **citadas** dentro de `verificar_foundry.py`, no silenciadas.

## 📌 Qué pasó el 2026-08-29 (segunda sesión) — **Fase 14, mitad de stats**

Las reglas de personaje dejan de ser ramas de Python y pasan a ser **efectos
citados** que viven junto al rasgo que los concede. Lo agrega `efectos.py` con
el orden fijo de DiceCloud, reimplementado (es GPL-3.0; se leen los conceptos,
no se copia código).

### Lo que se encontró al quitar el cableado, que es lo que importa

`calculo.py` decía, en un comentario, *«las dos únicas excepciones en el tronco
de clase, confirmado por grep sobre las 12 clases»*. Era cierto. **La base tiene
cuatro fórmulas de CA base**, y las otras dos están en subclases: *Juego de pies
deslumbrante* (Bardo/Danza, pdf 66) y *Resistencia dracónica* (Hechicero/
Dracónica, pdf 135). **El grep miró donde el `lambda` sabía mirar.**

Y `bonus_pg_especie`, el campo-parche de la ficha, falló de tres maneras a la
vez: cubría 1 de los 2 efectos de PG, guardaba un `1` fijo cuando el rasgo dice
«y en 1 más cada vez que subes de nivel», y **nadie obligaba a rellenarlo** —
`personajes/enano_guerrero.yaml` lo tenía vacío, con `pg_max: 12` donde tocaba
13, y **verificaba en verde**. Corregido, con su entrada en `decisiones`.

### Lo construido

| Pieza | Qué |
|---|---|
| `reglas/efectos.yaml` | Vocabulario cerrado: variables, 6 operaciones, orden de agregación, 4 condiciones |
| `reglas/_ESQUEMA_efectos.md` | El contrato, **y lo que el modelo todavía no representa** |
| `efectos.py` | Gramática de fórmulas (sin `eval()`), agregación, grafo de dependencias con ciclo como error explícito |
| `validar_efectos()` | 6 efectos · 0 errores · 1 aviso declarado |
| `_verificacion/mutaciones_efectos.py` | **26/26** — incluye la familia COLUMNA, que comprueba el escalado por nivel **en toda su escala** |

### La mitad del chequeo que de verdad vale

`validar_efectos()` tiene dos mitades. La de **forma** (objetivo, operación,
condición, variable, página, ciclos) es barata y evidente. La que cubre el
defecto que **de verdad ocurrió** es la de **ausencia**: lee las `desc`
buscando promesas —«CA base», «PG máximos aumentan»— y falla si no hay efecto
detrás. No es un dato malo: es un dato que falta, y ningún chequeo de forma ve
eso nunca.

### Tres decisiones tomadas, para no volver a abrirlas

1. **Varios `base` a la vez = elegir, no maximizar.** DiceCloud usa `max()`; el
   manual dice «solo puede beneficiarse de una, **a elegir**»
   (`reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`). El motor
   exige `elecciones.ca_base` y falla ruidosamente. Coger la mayor acertaría
   casi siempre, que es indistinguible de acertar por casualidad.
2. **Lo ya estructurado no se duplica.** El `+2` del escudo y las fórmulas de
   armadura se derivan del campo `ca` de `equipo/armaduras.yaml`. Escribir el
   `+2` al lado del `+2` es el modo de fallo nº 10 («dato agregado»).
3. **`velocidad` no entra.** «Movimiento sin armadura» es una tabla dispersa con
   decimales — el `ScaleValue` de Foundry — y pide su propia decisión.

### Lo que enseñó

- **La suite de 12 fichas se ganó el sueldo.** La primera versión modelaba el
  tope de Destreza de la armadura («13 + mod. Des (máx. 2)») como `op: max`
  sobre la CA agregada: forma correcta, **sitio equivocado**. Se comía el +2 del
  escudo del clérigo. **Ningún chequeo de forma lo habría visto** — amenaza nº 3
  del FODA, otra vez.
- **Una mutación puede fallar por sí misma.** La de «página con asterisco» salió
  18/19 porque el `replace(..., 1)` pegaba a la página del rasgo en vez de a la
  del efecto. Igual que en la tanda anterior: el fallo era de la mutación.
- **Un hueco declarado vale más que una cita inventada.** La CA base de quien no
  lleva nada (`10 + mod_des`) no tiene página en esta base: venía como literal
  sin cita dentro de `calculo.py`. Está marcada `_falta_cita: true` y el
  validador **avisa hasta que se cierre**. Es una lectura de página.

### 👉 Lo siguiente

**Fase 14b — efectos de conjuro.** El vocabulario ya está probado por mutación
sobre material con test de aceptación; extenderlo a los 391 conjuros es lo que
resuelve el límite conocido de `tirada` (*Símbolo* 6 modos, *Muro prismático* 7
capas) y el `coste` compuesto. Entra con el residuo declarado de ~11 %, y con la
regla que la Fase 14 ya obedece: **enlace a la cita, nunca copia del texto**.

---

## ✅ PG al subir de nivel — leído el 2026-08-30 e **implementado** (Fase 14b-1)

> **Implementado el mismo día.** `pg_max` se calcula desde `pg_por_nivel` (la
> historia de la ficha), la retroactividad de Constitución sale sola, y la ficha
> `personajes/draconido_hechicero_n3.yaml` lo sostiene. `mutaciones_pg.py` →
> 13/13. Lo que sigue abajo es la lectura que lo hizo posible; se conserva
> porque contiene las trampas del modelo.

**La base no tenía la regla.** Solo `dado_golpe` en las 12 clases y una mención
de refilón dentro de `multiclase.puntos_golpe_y_dados_golpe` que remitía a «los
puntos de golpe de la nueva clase como los de *niveles siguientes al 1*» — a una
sección que nadie había escrito. `calculo.py` solo tenía
`puntos_golpe_nivel_1()`. **`/subir-nivel` no podía subir a nadie de nivel.**

**Y `cobertura.py` decía «0 preguntas sin responder».** `cobertura_subir_nivel()`
comprobaba que los rasgos de clase, subclase y especie tuvieran texto, y **nunca
preguntaba por los PG**. El chequeo cubría lo que su autor recordaba — el mismo
patrón que dejó dos fórmulas de CA fuera de `calculo.py`. Ya pregunta: el bloque
pasó de 15 a **27 preguntas**.

**Leído por dos agentes Sonnet independientes** de la misma página (pdf 44 =
libro 42), sin verse los informes: `agente-PG-A.md` y `agente-PG-B.md`.
**Coinciden literalmente**, incluidas las cuatro filas de la tabla y las dos
ausencias. Ya está en `reglas/generacion_personaje.yaml → puntos_golpe`.

### Lo que dice el manual, y no es lo que uno recuerda

- **Nivel 1** → máximo del dado + mod. Con (pdf 42 = libro 40). Ya implementado.
- **Niveles siguientes** → **dos métodos, a elección del jugador** (pdf 44):
  1. **Tirar** el dado de golpe y sumar el mod. Con, **con un mínimo de 1 en el
     TOTAL** (no en el dado);
  2. **Valor establecido** de la tabla *«Puntos de golpe establecidos por
     clase»*: Bárbaro 7 · Explorador/Guerrero/Paladín 6 ·
     Bardo/Brujo/Clérigo/Druida/Monje/Pícaro 5 · Hechicero/Mago 4.

  **El «máximo del dado» NO es la regla de los niveles siguientes**: los dos
  lectores confirman que la palabra «máximo» nunca acompaña a «dado de golpe» en
  esa página. La alternativa a tirar es un **valor fijo**, que resulta ser el
  promedio redondeado arriba — y eso permite contrastarlo contra el `dado_golpe`
  de cada clase sin abrir el manual: `validar_puntos_golpe()`, **9/9 por
  mutación**, atacando en las dos direcciones (romper la tabla y romper el dado).

### 🚨 Lo que la fase que lo implemente NO debe descubrir por las malas

1. **El aumento de Constitución es RETROACTIVO** (pdf 44, paso 5): *«tus puntos
   de golpe máximos también aumentarán en 1 por cada nivel que hayas
   alcanzado»*. **Los PG máximos no son la suma de lo ganado en cada nivel.**

   ```
   pg_max = Σ(dado tirado o valor fijo, por nivel)   ← historia, se guarda
          + nivel_total × mod_con                     ← se RECALCULA entero
   ```

   Un motor que sume «lo ganado en el nivel N» y lo guarde da el número correcto
   **hasta la primera dote que suba Constitución**, y a partir de ahí se
   equivoca en silencio. Es el mismo género que la deriva ficha↔base de la
   amenaza nº 6 del FODA.
2. **El método es una elección del jugador, por nivel.** El motor **no puede
   calcularlo**: tiene que leerlo de la ficha, como una `decision` más. Una
   tirada no es reproducible, así que lo que se guarda es el **resultado**, con
   el nivel al que corresponde. Esto es lo primero que el modelo de efectos no
   cubre hoy: `pg_max` recibe un `base` de `calculo.py` y punto.
3. **Pregunta abierta, declarada y no inventada:** el «mínimo de 1» se aplica al
   total de cada subida. Si un mod. Con negativo **empeora** después, ¿se
   recalcula ese mínimo hacia atrás? **La página no lo dice.** No lo resuelvas
   adivinando: o se encuentra en otra página, o se declara como límite conocido.

### Dónde encaja

Es **prerrequisito de la Fase 16 (`/subir-nivel`)** y toca la **14b**: `pg_max`
deja de tener un `base` escalar y pasa a tener una **historia por nivel**, que
es el mismo salto que los conjuros («un conjuro es una lista de efectos, no un
registro plano»). Conviene resolver los dos con el mismo vocabulario.

---

## 👉 Lo que queda, al cerrar el 2026-08-30

Las Fases 13 a 16 están **cerradas** y la deuda declarada, **saldada** salvo dos
puntos que son decisión del usuario. Lo que queda no es construir: es
**estresar el sistema creando personajes** y ver qué se rompe — el método que
acaba de destapar los dos huecos más grandes que quedaban.

| Pendiente | Estado |
|---|---|
| Estrés automático: `generar_ficha.py --barrido --exhaustivo` | ✅ **240/240** (12 clases × 20 niveles, rotando subclase). Destapó el fallo decimal del Monje |
| Estrés con agentes: decisiones legales e ilegales | ✅ **hecho**: 20 fichas, **5 huecos** cerrados, 0 falsos positivos. Ver `PLAN_ESTRES.md` y `FUENTES.md` |
| Multiclase | ⏸️ aparcada por decisión del usuario |
| Conversiones a pies (330 en 178 conjuros) | ⏸️ aparcadas; se conservan declaradas en `_meta` |
| **5 menciones imperiales SIN pareja métrica** | 🔴 **abierto y localizado** — ver `FUENTES.md`. Son 5 lecturas de página |

---

## ✅ Nivel 20 monoclase — funciona de punta a punta (2026-08-30)

El sistema **construye, verifica y sube fichas monoclase de nivel 1 a 20**, con
cada número trazable a su regla citada. Lo sostienen dos fichas reales:
`draconido_monje_n20.yaml` (Monje 20, `pg_max` 143 · CA 19 · velocidad 18) y
`gnomo_mago_n20.yaml` (Mago 20, **55 referencias**, CD 19).

Construirlas destapó **los dos huecos más grandes que quedaban**, y ninguno era
un dato malo sino un dato que nadie ataba a su fuente: las **características
finales** no las justificaba nadie (un monje con las seis a 20 verificaba en
verde) y **nadie contaba los conjuros** (la ficha de ejemplo de la base llevaba
1 preparado donde su tabla concede 2). Los dos cerrados, con `mejoras`,
`verificar_conjuros()` y `mutaciones_nivel20.py` → 15/15. Detalle en `FUENTES.md`.

**Sigue pendiente la multiclase**, por decisión del usuario.

## ✅ La deuda declarada — saldada el 2026-08-30 (ver `PLAN_DEUDA.md`)

Las cuatro deudas que se podían cerrar están cerradas: la ceguera de
`validar_tirada()` (**9 conjuros**, 3 con `tirada` sin contrastar), las **tres
etiquetas** del ataque cuerpo a cuerpo (6 correcciones y un chequeo nuevo), la
**cita ausente** de la CA base (pdf 43 = libro 41, doble lectura) y el
**escalado por nivel** (`velocidad`, leído de la columna). Quedan dos, y las dos
son **decisión del usuario**: la multiclase y las conversiones a pies.

Lo que sigue es la redacción original del problema, que se conserva porque
explica por qué existían.

## 🔴 Lo que la Fase 14b-3 destapó (redacción original)

Dos cosas medidas, ninguna tocada, las dos baratas y sin abrir el manual:

1. **`validar_tirada()` está ciego en los registros condensados.** Usa
   `_RE_SALVACION`, que exige el «tirada de salvación de X» **completo**, y
   `hechizos.json` se declara `fidelidad: mixto` porque parte del texto **elide
   «tirada de»** (*Muro de hielo* dice «hace salvación de Destreza»). En esos
   registros la coherencia `tirada`↔descripción **nunca se comprobó**. Cuántos
   son, no se ha medido. `validar_tiradas()` ya usa la forma laxa; unificar las
   dos es trabajo de una tarde.
2. **11 conjuros dicen «ataque de conjuro cuerpo a cuerpo» y se etiquetan de
   tres formas distintas:** 4 con `D20+ata.conj.`, 3 con `D20+ata.CaC` y 4 con
   `Directo`. Los tres valores están en el vocabulario, así que el chequeo no lo
   ve — «un campo con la forma correcta puede ser basura», amenaza nº 3 del
   FODA. Normalizarlo pide **decidir qué distingue los dos términos**, que es
   criterio, no limpieza.

---

## 📌 El dato que mandaba, y cómo terminó

> La muestra aleatoria de la Fase 13o dio 7 defectos en 40 conjuros: **17,5 %**
> (IC 95 % 7,3-32,8 %), y proyectaba ≈54 conjuros con error sobre los 306.

**Se auditaron los 305 y salieron 48 (15,7 %).** La proyección era buena y la
Fase 14 estaba correctamente bloqueada. **Ya no lo está.**

| Superficie | Tasa medida |
|---|---|
| Campos que el SRD contrasta | 2,96 % |
| Dotes, trasfondos, equipo (lectura visual) | 0,72 % |
| `nombre` de conjuro | 1,0 % |
| `resumen` de conjuro | 4,3 % |
| **Descripciones de conjuro (antes de corregir)** | **15,7 %** |

### ~~Decisión pendiente: la semántica de `tirada`~~ → ✅ cerrada el 2026-08-29

**52 de los 391 conjuros** dicen `tirada: "Directo"` mientras su descripción
exige salvación (47) o ataque de conjuro (5). El campo viene literal de la
columna `como_usar` del CSV y **ningún script lo consume**. Antes de tocarlo hay
que **definir qué significa «Directo»**: ¿«el conjuro no exige tirada» o «el
disparador es automático aunque luego haya salvación»? Con la primera lectura
son 52 defectos; con la segunda, unos cuantos menos. **No se corrigió nada
porque adivinar la semántica y aplicar 52 cambios es peor que dejarlo anotado.**
Cuando se decida, el chequeo es trivial de automatizar: la descripción ya dice
qué tirada pide, y contrastarla con el campo es una regex.

### Cómo se lanza una tanda de auditoría (funcionó dos veces)

1. Briefing común en `_verificacion/_auditoria_rasgos/LEEME_AGENTE*.md` — la
   regla 1, el método `pdftoppm -r 170`, el offset `pdf = libro + 2`, qué es
   hallazgo y qué no, y **prohibición explícita de editar la base**.
2. Repartir en 4 lotes **disjuntos** y equilibrados por número de registros.
3. Cada agente escribe `_verificacion/_auditoria_rasgos/agente-<X>.md`.
4. **Releer personalmente la página de cada hallazgo** antes de aplicarlo.
5. Correr los cuatro validadores + las 12 fichas de personaje.


### ✅ Fase 13m — cerrada (cola aplicada el 2026-08-22)

Los 4 agentes auditaron los 87 conjuros que el SRD no cubre. **Aplicado y
verificado en la página por Opus el 21:**

- **41 conjuros con `consume_material` mal** — el mayor defecto de la base. La
  conversión usó la columna `gp` del CSV («tiene precio») en vez del asterisco
  del coste («se consume»). Detalle y evidencia en `FUENTES.md`.
- **`Mano de Bigby`** — su descripción decía «(Revisar efectos en el MdJ)»;
  transcrita entera desde pdf 309-310.
- **`Insecto gigante`** — faltaba «la mitad del» nivel: duplicaba los ataques.
- **`Desintegrar`** — faltaba la cláusula del polvo gris al llegar a 0 PG.
- **`Adiviniación` → `Adivinación`** (errata en el nombre) y `Toque helado`
  (coste espurio heredado de la fila contigua del CSV).

**La cola quedó cerrada el 2026-08-22.** Los 8 hallazgos pendientes se releyeron
en la página y se aplicaron; **tabla completa con página y evidencia en
`FUENTES.md`**, sección «Fase 13m — cierre de la cola». Resumen: los 8
«Castigo…» llevan ya la restricción «con un arma cuerpo a cuerpo o un ataque sin
armas»; `Brazos de Hadar` dice «**su**» siguiente turno; `Cautiverio` nombra
bien «presidio cercado» y «sueño»; `Burla dañina` corrige «stuileshacia» y
`Vicious Mockery`; las tres erratas de nombre (`Baile irresistible de Otto`,
`Flecha ácida de Melf`, `Fuente de luz lunar`) se arreglaron **con `alias` al
nombre viejo**; y `Conjurar lluvia de flechas` pierde el `coste` («1 pc» es el
umbral de valor del arma, no un coste que se gaste).

**⚠️ Lo que enseñó el apagón.** La PC se apagó de golpe a media faena. La base no
sufrió nada —`hechizos.json` quedó íntegro y los cuatro validadores en verde—
pero **siete correcciones quedaron escritas sin su registro en `FUENTES.md`**:
la base y su procedencia se desincronizaron en silencio, que es justo lo que la
regla «citar siempre» existe para impedir. Se reconstruyó a posteriori
contrastando el JSON contra los informes de agente. **Si se vuelve a trabajar
por tandas largas, escribir el registro con cada tanda aplicada, no al final.**

**Defecto nuevo hallado al revisar tras el apagón, ajeno a la cola:**
`Dedo de la muerte` decía **`7d8 + 3d0`** de daño necrótico; la página (pdf 270
= libro 268) dice **`7d8 + 30`**. El `0` de «30» lo leyó la conversión del CSV
como notación de dado. **Sobrevivió a las cuatro capas de validación porque
`3d0` es un dado sintácticamente válido** — cuarta vez que el CSV de conjuros
mete un defecto. Sugiere un chequeo nuevo: **ningún dado de la base debe tener
caras distintas de 4, 6, 8, 10, 12, 20 o 100**, que habría cazado este caso sin
leer la página.

**Deuda declarada: saldada el 2026-08-22.** Los 4 conjuros que remitían al
manual (`Deseo`, `Guardas y guardias`, `Símbolo`, `Muro prismático`) están
transcritos y `PLACEHOLDERS_CONOCIDOS` de `validar.py` **queda vacío**. A partir
de ahora cualquier descripción que remita al MdJ es un **error**, no un aviso.
Al transcribirlos salieron tres defectos de contenido en el texto que ya había;
el peor, `Símbolo` pidiendo una prueba de Inteligencia (Investigación) donde el
manual pide **Sabiduría (Percepción)**. Detalle en `FUENTES.md`, Fase 13n.

**Por qué 14 antes que 16.** `calculo.py:103` tiene las reglas cableadas
(`_CA_SIN_ARMADURA` con lambdas para Bárbaro y Monje), y `personajes/_ESQUEMA.md`
admite que `bonus_pg_especie` es un parche para un rasgo que no era
representable. Una skill de subida de nivel multiplica esos casos por 20
niveles × 12 clases. Convertirlos en dato **antes** evita reescribir la skill
después.

---

### Fase 8b → renumerada como Fase 16, `/subir-nivel` (pendiente)

> **Antes de diseñarla, lee `ANALISIS_REPOS.md` (2026-08-21).** Foundry dnd5e
> ya tiene resuelta la taxonomía de «qué puede pasar al subir de nivel» en
> nueve tipos de *advancement* (`../_referencias/foundry-advancement/`), y
> DiceCloud tiene el modelo de efectos y el orden de agregación que le falta a
> `calculo.py`. Ahorra inventarse el vocabulario desde cero.

Reutiliza `calculo.py`, `buscar.py` y `verificar_personaje.py` tal cual —
no hace falta ampliarlos salvo que subir de nivel necesite una función que
hoy no existe (p. ej. PG de niveles siguientes al 1, que es «promedio del
dado + mod Con, redondeado arriba» según el manual — falta verificar la
página exacta antes de codificarla, igual que se hizo con la Fase 8a).
Flujo esperado: leer `clases/<clase>.yaml → progresion` para el nivel
destino, mostrar los rasgos nuevos (texto de `clases/rasgos/` o
`clases/subclases/`), preguntar las elecciones que traiga ese nivel (mejora
de característica vs. dote, subclase si toca, conjuros nuevos), actualizar
la ficha y volver a correr `verificar_personaje.py`.

La arquitectura acordada, y **por qué** (detalle en `FODA.md`):

1. **Tiempo de construcción** — `validar.py` + `verificar_srd.py` +
   `cobertura.py`. La skill los corre **una vez como precondición** al arrancar
   y se niega a funcionar si fallan. No por consulta: la base no cambia
   mientras el LLM trabaja.
2. **Tiempo de consulta** — scripts de búsqueda deterministas que **fallan
   ruidosamente**. Cero resultados debe ser un error, jamás una lista vacía:
   una lista vacía es lo que hace que el LLM concluya «no hay» e improvise.
   Esta regla nació del bug `Clerigo` (ver `FUENTES.md`).
3. **Tiempo de decisión** — cada cambio en la ficha guarda la **referencia** que
   lo autorizó (`clase+nivel+rasgo`, nombre de conjuro, página), nunca una copia
   del texto: si se guardan copias, al corregir la base los personajes quedan
   desincronizados en silencio. Un verificador comprueba **por código** que la
   ficha final solo contiene cosas trazables a registros reales, para que la
   palabra del LLM nunca sostenga nada.

**Aviso para quien diseñe la skill:** hay dos casos que parecen datos normales
y no lo son. Trátalos explícitamente o la skill improvisará:

- **Objetos sin precio.** `equipo/aventureros.yaml` →
  `objetos_de_rasgo_de_clase` (hoy solo el `Libro de conjuros` del Mago). Son
  objetos que un rasgo concede y el manual **no vende**: `precio: null`
  significa «no existe precio», no «falta el dato». Si el usuario elige la
  opción B (oro en vez de equipo), el libro de conjuros lo sigue teniendo,
  porque nace del rasgo y no de la bolsa.
- **Elecciones abiertas.** El Bardo elige tres habilidades **cualesquiera**:
  su `habilidades` lleva `cualesquiera: true` y `literal` con la cita. El
  campo `de` es la expansión de las 18, puesta para poder ofrecerlas por
  pantalla, **no una restricción de la clase**. Una skill que trate `de` como
  lista cerrada acertará por casualidad; una que lea `cualesquiera` acertará
  siempre.

## 🔍 Verificado hoy contra un análisis externo (2026-08-19)

Llegó un `Analisis_Actualizado_Base_Canonica.md` (en `~/Downloads`) que
describía la base **antes** del cierre de hoy — daba por abiertos los 79
huecos de Fase 11 y el libro de conjuros, que ya estaban cerrados. Dos de sus
puntos sí eran nuevos y se contrastaron contra el código real:

- **"Falta un campo `categoria` en equipo" → descartado, ya resuelto.**
  Probado en vivo: `resuelve("canalizador arcano (bastón)", inv)` y
  `resuelve("instrumento musical a elección", inv)` devuelven `True`. El
  mecanismo ya existe, solo que no es un campo `categoria:` explícito: en
  `equipo/*.yaml`, cualquier clave cuyo valor es una lista de diccionarios
  actúa como categoría enumerable (`inventario_equipo()` en `cobertura.py`,
  función `walk()`), y `coincide()` hace matching tolerante a singular/plural
  y a paréntesis. Añadir el campo sería redundante con algo que ya funciona.

- **"Falta el metadato `fidelidad: literal/condensado` por registro" → ✅ hecho
  el 2026-08-29.** 26 ficheros YAML llevan `fidelidad` a nivel de fichero
  (`condensado` en dotes, subclases, especies y las 81 descripciones de equipo;
  `estructurado` en las tablas y listas que no son prosa), y `hechizos.json` lo
  declara en `_meta`.

  **`hechizos.json` se declara `mixto`, y esa es la parte que importa.** El
  análisis externo de 2026-08-19 daba por hecho que era `literal`; no lo es. Se
  intentó clasificarlo registro a registro con marcadores automáticos (viñetas,
  `TdS`, `PG`, `VD`) y **no resultó fiable**: el marcador más frecuente era la
  conversión «N m / M pies», que no es condensación sino **añadido editorial**.
  Declararlo `mixto` con la explicación de por qué vale más que una
  clasificación inventada. Si algún día hace falta por registro, es trabajo de
  criterio, no de regex.

## Mapa de ficheros

| Ruta | Qué hay |
|---|---|
| `clases/<clase>.yaml` | Tabla de progresión 1-20 + `atributos_basicos` (dado de golpe, salvaciones, habilidades, armas, armaduras, herramientas, característica principal, equipo inicial) |
| `clases/rasgos/<clase>.yaml` | **Texto** de los 158 rasgos del tronco de clase |
| `clases/subclases/<clase>.yaml` | 48 subclases con el texto de sus rasgos |
| `clases/_ESQUEMA_atributos_basicos.md` | Contrato del bloque `atributos_basicos` |
| `clases/rasgos/_ESQUEMA.md` | Contrato de los ficheros de rasgos |
| `reglas/generacion_personaje.yaml` | Métodos de características, conjunto estándar por clase, multiclase, `px_por_nivel` |
| `reglas/habilidades.yaml` | Las 18 habilidades y su característica |
| `reglas/idiomas.yaml` | Idiomas estándar e inusuales |
| `especies/`, `trasfondos/`, `dotes/`, `equipo/` | Orígenes, dotes y equipo (incl. `municion.yaml` y `objetos_de_rasgo_de_clase`) |
| `hechizos.json` | 391 conjuros con descripción literal, filtrables por `clases` y `nivel` |
| `_verificacion/` | SRD 5.2 (CC-BY-4.0) en Markdown y, desde 2026-08-21, `foundry_srd52/` con el mismo SRD ya estructurado campo a campo |
| `PLAN_14b_15.md` | **Plan de acción para cerrar la Fase 14 y ejecutar la 15** (2026-08-30). Contiene las cifras medidas que hacen ambas fases mucho más pequeñas de lo que decían los documentos: 18 conjuros necesitan lista (no 391), y los prerrequisitos son 11 formas |
| `ANALISIS_REPOS.md` | Qué aportan DiceCloud, Foundry dnd5e, PCGen y Open5e (investigación 2026-08-21) |
| `personajes/` | Fichas de personaje (`_ESQUEMA.md` es el contrato, `_ejemplo_aerin.yaml` un ejemplo verificado) |
| `calculo.py` | Toda la aritmética de personaje (PG, CA, CD, bonificadores, espacios, coste por puntos) |
| `buscar.py` | Consulta determinista que falla ruidosamente (clase/conjuro/objeto inexistente → error, nunca `[]`) |
| `verificar_personaje.py` | Trazabilidad de una ficha: cada `ref:` real, `calculado` recalculado y comparado |
| `verificar_foundry.py` | Contraste ancho contra el SRD 5.2 estructurado en 6 módulos (conjuros, armas, armaduras, especies, dotes, trasfondos). No traduce: empareja por claves independientes del idioma y deduce los vocabularios, exigiendo que sean biyecciones |
| `_verificacion/mutaciones_foundry.py` | Prueba por mutación del anterior (29/29; tarda >10 min) |
| `_verificacion/_auditoria_rasgos/` | Informes de las dos auditorías visuales (rasgos de clase, subclases, especies) y los dos briefings que se dieron a los agentes |
| `_verificacion/glosario_especies.yaml` | Único puente es↔en escrito a mano, y solo porque son nombres propios; cada pareja se comprueba con velocidad + visión en la oscuridad |
| `efectos.py` · `reglas/efectos.yaml` · `reglas/_ESQUEMA_efectos.md` | **Motor de efectos (Fase 14)**: las reglas de personaje como dato citado junto al rasgo que las concede, no como `if` de Python |
| `_verificacion/mutaciones_efectos.py` | Prueba por mutación del motor y de `validar_efectos()` (26/26) |
| `materiales.py` | La descomposición del componente material, y la ÚNICA implementación de la derivación `materiales → coste` (Fase 14b-2) |
| `_verificacion/mutaciones_materiales.py` | Prueba por mutación de `validar_materiales()` (10/10) |
| `_verificacion/mutaciones_tiradas.py` | Prueba por mutación de `validar_tiradas()` y `validar_ataques()` (19/19) |
| `prerrequisitos.py` · `reglas/prerrequisitos.yaml` | **Prerrequisitos de dote evaluables (Fase 15)**: gramática cerrada, parseo con ida y vuelta exacto, y evaluación contra un personaje |
| `_verificacion/mutaciones_prerrequisitos.py` | Prueba por mutación de `validar_prerrequisitos()` (10/10) |
| `_verificacion/mutaciones_pg.py` | Prueba por mutación de `validar_puntos_golpe()` (13/13), en las dos direcciones del contraste cruzado |
| `subir_nivel.py` · `reglas/subida_de_nivel.yaml` | **Qué pasa al subir de nivel (Fase 16)**, derivado de la tabla de la clase: separa lo que la base CONCEDE de lo que el jugador ELIGE |
| `_verificacion/mutaciones_subida.py` | Prueba por mutación de `validar_subida()` (7/7) |
| `generar_ficha.py` | **Generador determinista de fichas legales** para estresar el sistema. `--barrido --exhaustivo` = 240 fichas. Su límite: solo produce los errores que se le programaron |
| `_verificacion/mutaciones_nivel20.py` | Prueba por mutación de `verificar_mejoras()`, `verificar_conjuros()` y los tres chequeos del estrés (15/15), sobre las dos fichas de nivel 20 |
| `PLAN_16.md` | Plan de la Fase 16, con el inventario medido de «qué puede pasar al subir» |
| `.claude/skills/personaje/` | Skill `/personaje` — creación paso a paso de nivel 1 |
| `.claude/skills/subir-nivel/` | Skill `/subir-nivel` — subida de nivel sobre una ficha existente |

## Método de lectura visual (si hay que leer más manual)

```bash
pdftoppm -r 170 -f <pag> -l <pag> -png ../Manual_del_Jugador_2024.pdf /tmp/render/p
```
Genera `/tmp/render/p-<pag>.png` (rellena con ceros: `p-085.png`). Léelo con la
herramienta de lectura de imágenes. **`-r 170` es la resolución mínima legible.**

**El OCR de este PDF es basura (escaneo a 96 DPI): `pdftotext` NO es fuente
válida para ningún dato.** Solo sirve para localizar en qué página está algo.

Offset confirmado en todo el manual: **página_pdf = página_libro + 2**.

## Cómo se ha trabajado (y conviene seguir haciéndolo)

- **Reparto por modelo:** la lectura visual se delega a agentes Sonnet; el
  diseño, el código y las decisiones, a Opus. Ficheros disjuntos para que
  puedan correr en paralelo sin pisarse.
- **Nada se da por bueno porque un script diga «0 errores».** Los tres defectos
  más graves de este proyecto — la tilde de `Clérigo`, dos citas de página
  falsas, y 80 huecos de cobertura — sobrevivieron a validaciones en verde.
  Todo trabajo de agente se verifica contra el manual por muestreo, priorizando
  lo que cambió en 2024 y lo que nadie ha vuelto a mirar.
- **Cada chequeo nuevo se prueba por mutación** antes de confiar en él: se
  corrompe la base a propósito en una copia desechable y se comprueba que
  salta. Un validador que nunca ha visto un dato malo no demuestra nada.
- **Una ausencia también es un dato, y se documenta como tal.** El
  `Libro de conjuros` no tiene precio porque el manual no lo vende; eso se
  registró con la evidencia negativa citada (las dos páginas que podrían
  haberlo contradicho) en vez de inventar una cifra. Cuando el manual no dice
  algo, la respuesta correcta es «el manual no lo dice, y aquí está dónde
  miré», nunca un hueco silencioso.

## Reglas inviolables

1. **Consultar, no recordar.** Todo dato de reglas sale de la página del manual,
   nunca de lo que el modelo «sepa» de D&D.
2. **Citar siempre.** Sin página citada, un dato no entra en la base.
3. **Decir «no lo tengo».** Si algo no se lee con claridad, se marca y se
   pregunta. Nunca se rellena.
4. **Solo edición 2024.** El manual EDGE de la papelera (2014) está vetado.
5. **Validar antes de dar por cerrada una fase.**
6. **La cobertura se descubre, nunca se escribe a mano.** *(nueva, 2026-08-31)*
   Ningún módulo puede llevar dentro la lista de los ficheros, campos o
   columnas que mira. Se descubre por patrón y se contrasta contra un
   manifiesto que declara **también las exclusiones, con su motivo**. Un
   fichero que nadie sepa clasificar es un error, no un salto silencioso.

   **Por qué es inviolable y no una preferencia:** este error apareció
   **cinco veces**, escrito en momentos distintos, sin que nadie lo copiara
   a propósito:

   | Lista escrita a mano | Qué se le escapaba | Estado |
   |---|---|---|
   | `efectos._ORIGENES` | 46 subclases · 4 ficheros de dotes | ✅ cerrada (C1) |
   | `verificar_documentos` (cifras) | `efectos` desde la Fase 14 | ✅ cerrada |
   | `verificar_chequeos.FUENTES` | audita 3 de las 6 que declara | ✅ cerrada (A2) |
   | `verificar_srd.MAPA` | `slots`, `forma_salvaje`, `mov_sin_armadura_m` | ✅ cerrada (A2) |
   | `verificar_foundry.MODULOS` | 9 pares (carpeta, `type`) · 562 registros | ⬜ medida y declarada → bloque H |
   | `validar._PROMESAS` | `velocidad`, y con ella 9 rasgos | ✅ cerrada (A2) |

   Cuando el mismo defecto sale cinco veces no es descuido repetido: es que
   la forma de trabajar lo invitaba. `validar.py` ya lo hacía bien —descubre
   con `glob` en 14 sitios— y era el ejemplo que los demás no siguieron.

   **El corolario, y es el que duele:** se verificaba con obsesión que los
   datos escritos fueran correctos (3666 valores externos, 149 mutaciones) y
   **no se verificaba nunca que estuvieran todos**. Comprobar la calidad de
   lo que hay no dice nada de lo que falta.
