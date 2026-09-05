# Procedencia de la base canónica

**Edición única: D&D 2024 (5.5e), castellano.** Todo registro va sellado.
Material de otras ediciones está prohibido en esta base.

## Fuentes primarias

| Fuente | Naturaleza | Usada para |
|---|---|---|
| `../Manual_del_Jugador_2024.pdf` (388 pág) | Escaneo 96 DPI + capa OCR Tesseract | Clases, especies, trasfondos, dotes, equipo |
| `../PHB_2024_EN.pdf` (389 pág) | Escaneo 109 DPI + OCR | Contraste independiente del anterior |
| `_origen_hechizos.csv` (392 filas) | Datos ya estructurados, sin OCR — y **la fuente menos fiable de todas**: ha fallado tres veces (un conjuro duplicado, una escuela ausente, y 9 conjuros con campos invertidos). Ver correcciones | `hechizos.json` (391 conjuros) |

## Auxiliares (no autoridad para creación de personajes)

- `../Guia del Dungeon Mater (Ingles-DnDBeyond).pdf` — nativo digital. Objetos mágicos.
- `../Manual de Monstruos - Ingles.pdf` — nativo digital. Familiares y compañeros.

## ⛔ Cuarentena

- **`★ D&D® Manual del Jugador™(errataless-EDGE).pdf`** — edición española 2018 del
  manual **2014**. Incompatible: 0 menciones de «maestría de arma» frente a 57 en el
  2024. Mezclarlo produce reglas que suenan correctas y no existen. En la papelera.
- **`Raton/Fichas de clase.pdf`, `ESPECIES.pdf`, `Transfondos.pdf`** — resúmenes hechos
  por fans (tipografías no oficiales; remiten a tablas que no incluyen). Fuente
  secundaria: sirven para contrastar, nunca como origen de un dato.

## Método de verificación

Cinco capas, de barata a cara; cada una solo actúa sobre lo que la anterior no resolvió.

1. **OCR castellano** — `pdftotext -layout`. Fiable en nombres de rasgos.
2. **OCR inglés** — mismo libro, errores independientes; tapa los huecos del anterior.
3. **Invariantes** — deducibles sin el manual (ver `validar.py`).
4. **Lectura visual** — recorte de la página ampliado, leído directamente.
5. **Contraste contra el SRD 5.2** — fuente oficial independiente bajo CC-BY-4.0
   (ver `_verificacion/LEEME.md`, `verificar_srd.py` y `verificar_foundry.py`).
   Confirma, no completa: solo cubre un subconjunto del manual, y **cuando
   discrepa no siempre tiene razón** — hay 5 casos documentados en los que
   manda el manual.
6. **Auditoría visual por agentes** — releer la página de lo que ninguna fuente
   externa cubre, en lotes disjuntos, con el hallazgo verificado después por
   quien lanza los agentes. Es la capa más cara y la única que llega a las
   subclases, los rasgos de clase y las citas de página. Método e informes en
   `_verificacion/_auditoria_rasgos/`.

Tesseract falla en estos escaneos porque 96 DPI queda muy por debajo de los ~300 DPI
que necesita. La imagen en sí es perfectamente legible: el problema era el motor de OCR,
no el escaneo.

## Estado

| Fase | Contenido | Estado |
|---|---|---|
| 1 | 391 conjuros → `hechizos.json` | ✅ conversión directa |
| 2 | 12 tablas de clase → `clases/*.yaml` | ✅ lectura visual, validadas |
| 3 | Subclases | ✅ 12/12 clases, 48/48 subclases, lectura visual, validadas |
| 4 | Especies y trasfondos (cap. 4) | ✅ 16 trasfondos + 10 especies, verificados |
| 5 | Dotes (cap. 5): 75 dotes (10 origen, 43 generales, 10 estilo de combate, 12 don épico) | ✅ lectura visual, validadas |
| 6 | Equipo y maestrías (cap. 6): armas, armaduras, herramientas, equipo de aventureros, monturas/vehículos, servicios, fabricar equipo | ✅ lectura visual, validadas |
| 7 | `validar.py` — 15 funciones de coherencia interna | ✅ clases, orígenes, dotes, equipo, hechizos, creación de personaje e integridad referencial |
| 7b | `verificar_srd.py` | ✅ 646 valores contra el SRD 5.2, 0 discrepancias |
| 9 | `reglas/generacion_personaje.yaml` + `atributos_basicos` en las 12 `clases/*.yaml` (característica principal, equipo inicial, multiclase) | ✅ lectura visual, validada |
| 9b | `validar_atributos_basicos()` y `validar_generacion()` en `validar.py` | ✅ probadas por mutación (8/8 detectadas) |
| 9c | Integridad de `hechizos.json` (tilde de `Clérigo`, duplicado) + `validar_hechizos_clases()` y `validar_rasgos_clase()` | ✅ probadas por mutación (11/11 detectadas) |
| 10 | Texto de los rasgos de clase base → `clases/rasgos/*.yaml` (158 entradas, 12/12 clases) | ✅ lectura visual, validada |
| 7c | `cobertura.py` — ¿puede la base responder lo que la skill preguntará? | ✅ probado por mutación (8/8) |
| 11 | Competencias de clase (6 campos × 12), `reglas/habilidades.yaml`, `reglas/idiomas.yaml`, `px_por_nivel`, `equipo/municion.yaml` | ✅ lectura visual + reestructuración; 17/17 mutaciones |
| 12 | Cierre de cobertura (`Libro de conjuros`), competencias de Bárbaro/Bardo/Brujo contrastadas, duplicados del Bardo | ✅ lectura visual; 2/2 mutaciones |
| — | `FODA.md` | 📊 Análisis de la base como sustrato de un orquestador LLM |
| — | `CONTINUAR.md` | 📍 Punto exacto de reanudación y método |
| 8a | Cimientos deterministas: `calculo.py`, `buscar.py`, `verificar_personaje.py`, `personajes/_ESQUEMA.md`, skill `/personaje` | ✅ funciones contrastadas contra el manual (pdf 42, 240) y probadas por mutación (4/4) |
| — | `ANALISIS_REPOS.md` | 🔍 Qué aportan DiceCloud, Foundry dnd5e, PCGen y Open5e (leído su código, no sus README) |
| 13a-d | `verificar_foundry.py` — contraste ancho contra el SRD 5.2 estructurado: conjuros (banderas), armas, armaduras, especies | ✅ 9 errores propios hallados y corregidos |
| 13e-f | Módulos de dotes y trasfondos, **sin puente de nombres** | ✅ 75/75 dotes conformes a su patrón de categoría; 4 trasfondos emparejados por trío de características |
| 13g | Margen de error de la base, medido con IC exactos | 📏 en `FODA.md` |
| 13h | Conjuros: alcance, duración y tiempo de lanzamiento | ✅ +423 valores; 2 casos en que manda el manual |
| 13i | **Auditoría visual de los 158 rasgos de clase** (4 agentes Sonnet) | ✅ 10 hallazgos (9 citas + 1 contenido), todos releídos y aplicados |
| 13j | Herramientas, con huérfanas declaradas por nombre | ✅ 18/25 emparejadas; 5 características deducidas sin conflicto |
| 13k | **Auditoría visual de las 48 subclases y las 10 especies** (4 agentes Sonnet) | ✅ 4 hallazgos (todos citas); 2 hallazgos rechazados tras releer |
| **13m** | **Auditoría visual de los 87 conjuros fuera del SRD** (4 agentes Sonnet) | ✅ 22 hallazgos aplicados; **cola cerrada el 2026-08-22** |
| **13n** | **Cierre de la lectura visual**: los 4 placeholders transcritos + auditoría de dotes, trasfondos y equipo (5 agentes) + `validar_dados()` | ✅ **hecha (2026-08-22)** |
| **13o** | **Muestra aleatoria de 40 descripciones de conjuro** — medición de la última superficie ciega | ⚠️ **hecha (2026-08-22): 17,5 % de error** |
| **13p** | **Auditoría de las 266 descripciones restantes**, en 4 oleadas de 5 lotes | 🟡 **131/266 (2026-08-27)**: oleadas 1 y 2 cerradas, 19 defectos aplicados, tasa 14,5 % |
| 13q | `validar_conversiones()` + módulo `conjuros-clases` — dos superficies ciegas convertidas en chequeo automático | ✅ **hecho (2026-08-27)**; mutaciones 13/13 |
| 14 | Motor de efectos (modelo DiceCloud) | ⬜ pendiente |
| 15 | Prerrequisitos evaluables (idea de PCGen) | ⬜ pendiente |
| 16 (ex 8b) | Skill `/subir-nivel` | ⬜ pendiente |

**Estado al cerrar el 2026-08-27:**

```
python3 validar.py           -> 0 errores  (671 tiradas de dado, 562 conversiones)
python3 verificar_srd.py     -> 646 valores, 0 discrepancias
python3 verificar_foundry.py -> 2967 valores, 0 discrepancias   (9 módulos)
python3 cobertura.py         -> 0 preguntas sin responder
python3 _verificacion/mutaciones_foundry.py      -> 25/25 detectadas
python3 _verificacion/mutaciones_dados.py        -> 12/12 (6 detecciones + 6 controles negativos)
python3 _verificacion/mutaciones_conversiones.py -> 13/13 (6 detecciones + 7 controles negativos)
```

Más las **12 fichas de `personajes/`**, que pasan `verificar_personaje.py` sin
regresión.

**Balance del día:** 24 defectos propios corregidos (9 de conjuros, 13 citas de
página, 1 de contenido, 1 de cita de fichero) y 5 casos anotados en los que el
SRD se equivoca y manda el manual. Contenido cerrado; el punto exacto de
reanudación y lo que sigue ciego están en `CONTINUAR.md`.

### Nota sobre la Fase 5

Buscando «Prerrequisito» en el capítulo de Dotes (pág. 201-214) el OCR devuelve
**cero** coincidencias, cuando cada dote lleva uno. Ese capítulo va por lectura
visual obligatoria; sin prerrequisito, una dote no entra en la base.

### Por qué no son redundantes

La lección que costó descubrirlos: un dato puede ser perfectamente coherente y
aun así **no estar**. Tras marcar «0 errores» durante fases enteras,
`cobertura.py` reveló 80 preguntas sin respuesta — entre ellas el dado de
golpe de 11 clases, sin el cual no hay puntos de golpe. Coherencia no es
completitud.

### Nota sobre la Fase 9b — invariantes que atan tablas entre sí

Las comprobaciones nuevas no repiten el dato del manual: cruzan tablas
transcritas por separado, de modo que un error de lectura en una sola de ellas
rompe la coherencia. Las tres que más cubren:

- **El conjunto estándar cuesta exactamente 27 puntos.** 15+14+13+12+10+8 vale
  9+7+5+4+2+0 = 27 en la tabla de compra por puntos. Cualquier cifra mal leída
  en *cualquiera* de las dos tablas desajusta la suma.
- **La tabla de espacios de conjuro multiclase es idéntica a la de un lanzador
  completo**, que ya estaba en `validar.py` como invariante desde la Fase 2.
- **La característica principal se comprueba en tres sitios a la vez**:
  `atributos_basicos` de la clase, la fila del conjunto estándar por clase (la
  puntuación más alta va a la principal) y el requisito de multiclase (≥13).
  Tocar uno solo de los tres hace saltar los otros dos.

Se probaron por mutación: 8 corrupciones deliberadas (transposición de una fila,
cifra de coste alterada, fila de espacios corrompida, aptitud mágica
incoherente, desfase de página erróneo, opción de oro fuera de sitio, bloque
ausente, conector `y`/`o` cambiado) — las 8 detectadas.

### Los cuatro validadores, y qué pregunta responde cada uno

| Script | Pregunta que responde | Superficie |
|---|---|---|
| `validar.py` | ¿Es la base coherente **consigo misma**? | toda |
| `verificar_srd.py` | ¿Coincide con el SRD 5.2 vía Open5e? | 12 tablas de clase (646 valores) |
| `verificar_foundry.py` | ¿Coincide con el SRD 5.2 estructurado? | conjuros, armas, armaduras, especies, dotes, trasfondos, herramientas (2689 valores, 8 módulos) |
| `cobertura.py` | ¿Puede la base **responder** lo que las skills preguntarán? | preguntas simuladas |
| `_verificacion/mutaciones_foundry.py` | ¿**Detecta** el verificador un dato malo? | 25 corrupciones deliberadas |

## Correcciones registradas

- **Dos conjuros mal puestos en una ficha de la base → ronda 2 de estrés
  (2026-09-05)** — `personajes/draconido_hechicero_n4.yaml` llevaba dos
  defectos que ningún chequeo miraba, porque los dos chequeos de conjuros
  **contaban la longitud de la lista sin mirar qué había dentro**:

  | Defecto | Qué pasaba |
  |---|---|
  | «Descarga sobrenatural» entre los trucos | Es conjuro de **Brujo**, en un Hechicero. Los 391 conjuros de `hechizos.json` traen `clases`, y nadie lo consultaba |
  | «Rayo de escarcha» en `trucos` **y** en `preparados` | Es de nivel 0, así que de los 7 preparados que concede la tabla la ficha tenía **6 reales** |

  El primero lo **predijo** el agente A de la ronda de estrés con un caso
  inventado («Tañido por los muertos» en un Hechicero) y resultó estar vivo en
  la base; el segundo lo encontró el agente C leyendo los ejemplos, que es
  justo lo que el briefing de esa ronda pedía por primera vez.

  Corregido: el truco de Brujo pasa a «Estallido mágico» y el preparado
  duplicado a «Armadura de mago», los dos de la lista real del Hechicero.
  Y los dos huecos quedan cerrados con chequeo y mutación, no solo el dato:
  ahora se comprueba que cada conjuro que cuenta contra la tabla sea de la
  lista de su clase, que ninguno esté en las dos listas, y que el nivel del
  conjuro corresponda con la lista en la que vive.

- **El verificador aprobaba la ficha mal y rechazaba la buena → C1/C3/C4 del
  Plan 17 (2026-08-31)** — el defecto más grave encontrado hasta la fecha, y
  no era un dato equivocado: era un dato **que nadie miraba**.

  **Medido, con la ficha de nivel 1 del propio repo:**

  | Ficha | Veredicto antes |
  |---|---|
  | `Duro` (dote de origen) con su +2 PG aplicado — CORRECTA | ❌ rechazada |
  | `Duro` con el +2 perdido — ROTA | ✅ «0 problemas» |
  | `Actor` (nivel 4) con su +1 Carisma aplicado — CORRECTA | ❌ rechazada |
  | `Actor` con el +1 perdido — ROTA | ✅ «0 problemas» |

  **Causa:** `efectos._ORIGENES` era una tupla de 15 rutas escritas a mano.
  Conocía 2 de las 48 subclases y **0 de los 4 ficheros de dotes**. Y 54 de
  las 75 dotes conceden «Mejora de característica: X +1» dentro de una cadena
  de texto, sin campo donde declararlo. Es el mismo defecto que la cabecera de
  `reglas/efectos.yaml` condena para las fórmulas de CA cableadas, repetido un
  nivel más arriba: un diccionario de FÓRMULAS sustituido por una tupla de
  RUTAS.

  **Corregido sin transcribir nada nuevo.** `mejora_caracteristica` se DERIVÓ
  de la prosa ya citada, con **ida y vuelta 54/54 exacta** — el método de la
  Fase 15. `validar_mejoras_de_dote()` la exige de forma permanente y salta en
  los dos sentidos (prosa sin estructura, estructura sin prosa).

  **Lo que la ida y vuelta evitó, y es el motivo de hacerla así:** los **12
  dones épicos dicen «máx. 30», no 20**. Dar por hecho el 20 —que es lo que
  «se sabe» de D&D— habría inventado una regla para 12 dotes. La ida y vuelta
  lo hizo imposible antes de escribir nada.

- **`personajes/draconido_hechicero_n4.yaml`: Carisma 17 → 18 (2026-08-31)** —
  la ficha tomaba `Lanzador ritual`, que concede +1 a Inteligencia, Sabiduría
  o Carisma, y **no aplicaba el +1**. Arrastraba CD 13, bonificador de ataque
  +5 y CA 15 donde debían ser 14, +6 y 16. Se elige Carisma por ser la aptitud
  mágica del Hechicero, y consta en el bloque `decisiones` de la ficha con su
  cita. Nadie lo detectaba porque el +1 de una dote no tenía dónde entrar: el
  esquema exigía `final == base + ajuste_trasfondo + mejoras`, y una dote no
  era ninguna de las tres.

- **`dotes/origen.yaml#Duro`: primer efecto de dote declarado (2026-08-31)** —
  `{objetivo: pg_max, op: add, formula: "2 * nivel_total"}` (pdf 203 = libro
  201). El texto da dos reglas —al adquirirla, el doble del nivel; después, +2
  por nivel— que **juntas equivalen** a la forma cerrada declarada. No se
  simplifica ninguna regla: se declara lo que el propio texto produce en todos
  los niveles.


- **«¿Cómo sabemos que no volverá a pasar?» → `verificar_chequeos.py`
  (2026-08-30)** — la respuesta honesta era **no lo sabemos**, y este proyecto ya
  tenía la prueba: la convención de `coste` *«llevaba una semana escrita en
  FUENTES.md (1500 líneas) y se rompió sin querer»*. Una regla en prosa no
  impide nada. Así que la regla —«ninguna rama de chequeo abandona un registro
  en silencio»— pasa a comprobarla un script.

  **Recorre el AST** de los verificadores y busca, dentro de las funciones
  `validar_*` / `verificar_*`, las ramas que terminan en `continue`, `pass` o
  `return` **sin llamar a ningún avisador**. Una tolerancia legítima se firma con
  `# TOLERADO: <quién lo cubre>` y sale declarada en el informe.

  **El resultado fue incómodo y por eso vale: 59 ramas silenciosas.** El patrón
  que costó dos defectos no era una excepción — era la norma.

  **Y una de ellas la había escrito yo esa misma tarde.** Los tres chequeos
  nuevos de nivel 20 (`verificar_mejoras`, `verificar_conjuros`,
  `verificar_dotes_y_subclase`) hacían `if len(clases) != 1: return` **sin decir
  nada**: cualquier ficha multiclase se saltaba los tres. La ficha `a-5` del
  agente A lo demostró —pasó con un solo error— y **no lo vi al puntuar**.
  Convertidos en avisos que **nombran lo que no se comprobó**.

  **Cómo garantiza algo, que es lo que se preguntaba.** Con una **línea base
  declarada** en `_verificacion/chequeos_silenciosos.json`: las 59 quedan
  contadas y listadas una a una —deuda visible, no perdón— y **ninguna nueva
  puede aparecer** sin que el chequeo lo diga con nombre y apellidos. Cada rama
  que se anota o empieza a avisar sale de la lista. **La deuda solo puede bajar**;
  va por **54**. Corre dentro de `verificar_documentos.py`, en la rutina.

  **Su límite, dicho por delante:** no puede ver un chequeo que sencillamente
  **no existe**. Nadie contaba los conjuros y esto no lo habría dicho. Para esos
  hace falta que alguien construya personajes a propósito — por eso el estrés
  con agentes de `PLAN_ESTRES.md` es rutina y no anécdota.

- **Causa raíz de los ejemplos defectuosos: una rama de tolerancia (2026-08-30)**
  — no fueron «malos ejemplos» ni descuido al escribir las fichas. Las fichas
  **eran correctas cuando se escribieron**. La secuencia, reconstruida del
  propio registro:

  1. El esquema **exigía `ref:`** para las competencias
     (`equipo/armas.yaml#Armas sencillas`).
  2. Eso resultó ser imposible: esas categorías **no existen como registros** en
     `equipo/`, solo las armas concretas. *«Tres de cinco agentes chocaron con
     esto y lo sortearon citando un arma concreta en su lugar»* (ronda 2 de
     pruebas, ya en este mismo fichero).
  3. Se corrigió el esquema: pasan a ser `categoria:` con texto literal.
  4. **Las fichas ya escritas no se migraron.**
  5. Y en `verificar_categorias()` se dejó esta línea:

     ```python
     if not isinstance(e, dict) or "categoria" not in e:
         continue  # entradas antiguas con `ref:` las cubre _recorrer_refs
     ```

  **Ahí está la causa.** La rama era razonable el día que se escribió —dejar
  convivir los dos formatos mientras se migraba— pero **nada reclamaba la
  migración**, así que no ocurrió. La tolerancia no aplazó el desfase: **lo
  volvió invisible, y por tanto permanente**. Y las fichas viejas enseñaron el
  formato viejo a todo el que vino después, agentes incluidos.

  **Es la segunda vez que pasa exactamente esto.** `COSTE_COMPUESTO` era una
  lista de excepciones que sacaba seis conjuros del contraste externo «porque el
  modelo no los representaba»; al quitarla en la Fase 14b-2 aparecieron **dos
  sumas que ninguna página imprime**, escondidas ahí desde el principio. Mismo
  mecanismo: una exención declarada de buena fe, que deja de doler y por eso
  deja de arreglarse.

  **Regla nueva del proyecto, y esta se paga cara cada vez que se olvida:**

  > **Una rama de tolerancia en un chequeo es deuda con fecha de caducidad, no
  > una decisión.** Si se admite un formato viejo, la migración va **en la misma
  > tanda**, no «cuando toque». Y si de verdad hay que aplazarla, la rama emite
  > un **aviso que nombra los registros pendientes** y converge a cero — como
  > hacen `_tirada_revisada` y `_vecindad_verificada`, que sí funcionaron.

  Rama eliminada; hoy la forma la exige `verificar_forma_competencias()` como
  error. Se barrieron los verificadores buscando otras: **era la única**.

- **Estrés con agentes: cinco huecos que el generador jamás habría encontrado
  (2026-08-30)** — cuatro agentes construyeron **20 fichas** leyendo la base,
  con decisiones deliberadas legales e ilegales, **sin ver el código del
  verificador y sin poder ejecutarlo**, y declarando en un sobre cerrado —antes
  de la corrección— qué pretendía ser cada decisión y qué regla citaba. Método y
  puntuación en `PLAN_ESTRES.md`.

  **Por qué hacía falta:** el barrido automático daba 240/240, y eso no
  significaba que el sistema estuviera bien — significaba que **el generador y
  el verificador estaban de acuerdo**, y los escribí los dos. Un generador solo
  produce los errores que se le programaron: encuentra lo que revienta, no lo
  que el verificador **deja pasar en silencio**.

  **Los cinco huecos, todos de la segunda clase:**

  | # | Hueco | Quién lo destapó |
  |---|---|---|
  | 1 | **Las dotes que el personaje TIENE no se comprobaban.** La Fase 15 sabía *ofrecer* las que puede tomar y nadie miraba las que ya lleva: un Guerrero con Inteligencia 8 llevaba «Mente aguda», que pide 13 | A |
  | 2 | **La subclase podía ser de otra clase.** Un Pícaro con «Campeón» del Guerrero pasaba en verde: la ref resolvía… en otro fichero | A |
  | 3 | **El +2 del escudo se sumaba sin entrenamiento.** `equipo/armaduras.yaml → reglas.escudos` dice «Solo obtienes el bonificador a la CA de un escudo **si tienes entrenamiento con escudos**» | D |
  | 4 | **La penalización de velocidad por Fuerza insuficiente no se aplicaba nunca.** Misma sección: «reduce 3 m la velocidad de quien la lleve, salvo que su Fuerza sea igual o superior» | D |
  | 5 | **Nueve de las diecisiete fichas de la base violaban la regla 6 de su propio esquema**, declarando competencias como `ref:` a un objeto en vez de `categoria:` | efecto colateral de (3) |

  **El quinto es el más instructivo.** La regla 6 existe por una razón
  documentada —«Armas sencillas» no es un registro de `equipo/`, solo existen
  las armas concretas— y aun así **nueve fichas la rompían y nada lo
  comprobaba**. Y lo que lo cierra: **los cuatro agentes copiaron el defecto**,
  porque aprendieron el formato de las fichas de ejemplo. Un ejemplo malo enseña
  más rápido que un esquema bueno.

  **Los cuatro hallazgos de reglas están cerrados** con su chequeo y su prueba
  por mutación (`mutaciones_nivel20.py` → **15/15**), las 17 fichas migradas al
  formato del esquema, y el barrido de regresión sigue en **240/240**.

  **Confirmación limpia del método:** la ficha `d-2` —armadura pesada con Fuerza
  10, que su agente declaró **legal** y predijo velocidad 6— fallaba antes de la
  corrección y **pasa después, con exactamente el 6 que él había calculado**.

  **Lo que se descartó, y por qué.** Casi todos los fallos del agente C (que
  tenía prohibido cometer ilegalidades) eran el formato `ref:` heredado de los
  ejemplos, no falsos positivos del verificador; los demás fueron errores suyos
  de cálculo (la velocidad del Goliat es 10,5, no 9) o competencias que su clase
  no concede. **Ningún falso positivo confirmado.**

  **Y un defecto del método, que conviene registrar:** **los cuatro agentes
  tropezaron con la misma prohibición** —ejecutaron un `python3 -c` para
  inspeccionar la forma de `hechizos.json`— y **los cuatro lo declararon por su
  cuenta**. Prohibí ejecutar *cualquier* script cuando lo que importaba era no
  ejecutar el verificador. El briefing estaba mal calibrado, no ellos.

- **El barrido de fichas generadas: 240 personajes, y un fallo que ninguna
  mutación había visto (2026-08-30)** — `generar_ficha.py` fabrica fichas
  legales desde la base, deterministas y reproducibles, y las pasa por
  `verificar_personaje.py`. Se corrió sobre **las 12 clases × los 20 niveles**,
  rotando subclase: **240 fichas**.

  **Lo que destapó, y es el hallazgo del día:** el Monje de nivel 6 **reventaba
  el motor**. «Movimiento sin armadura» escala a **4,5 m** en ese nivel, y la
  ruta de `columna` pasaba el valor por el evaluador de fórmulas, que rechaza
  decimales **a propósito** (las fórmulas escritas a mano son aritmética
  entera). Los niveles 6, 14 y 17 de cualquier monje eran incalculables.

  **Por qué no lo vio nadie antes:** la única ficha que sostenía ese efecto era
  de **nivel 2**, donde la columna vale 3 — un entero. **Una escala probada en
  un solo punto no está probada**, y ni el chequeo ni sus mutaciones podían
  saberlo porque los dos miraban ese mismo punto.

  Arreglado separando los dos caminos (`_num()`: una `columna` trae el número
  tal cual lo imprime la tabla; una `formula` sigue siendo entera), y **cerrado
  con un chequeo que recorre la escala entera**: todo efecto con `columna` tiene
  que resolverse en **todos** los niveles de su clase. Dos mutaciones nuevas lo
  prueban (columna no numérica en el nivel 6; columna que desaparece en el 14)
  → `mutaciones_efectos.py` **26/26**.

  El barrido también destapó un fallo **del propio generador** —repartía una
  cuota fija de conjuros por nivel y se quedaba en 10 de los 11 que piden
  Explorador y Paladín en el nivel 14—, que no era defecto de la base.

  **Y su límite, dicho por delante:** un generador solo puede producir los
  errores que se le hayan programado. Prueba las reglas contra sí mismas y
  encuentra lo que revienta, no lo que el verificador **deja pasar**. Para eso
  hace falta que quien construya el personaje tome decisiones que el generador
  no sabe tomar — el plan de agentes de `PLAN_ESTRES.md`.

- **🔴 ABIERTO — cinco menciones imperiales SIN pareja métrica (medido el
  2026-08-30)** — al inventariar las conversiones a pies para decidir qué hacer
  con ellas aparecieron **322 del patrón conocido** («N m / N pies») en 176
  conjuros… y **ocho que no encajan**. Cinco de esas ocho son de otro género y
  **no son añadido editorial sino posible sustitución**: dan la medida **solo en
  unidades imperiales**, sin el valor métrico al lado.

  | Conjuro | Lo que guarda la base |
  |---|---|
  | *Muro de espinas* (libro 311) | «Moverse a través de la pared cuesta **4 pies** de movimiento por cada pie…» |
  | *Excursión etérea* (libro 282) | «…daño por fuerza igual al **doble de pies** movidos» |
  | *Portal* (libro 320) | «el portal puede tener entre **5 y 20 pies** de diámetro (1,5 a 6 m)» |
  | *Crear muerto viviente* (libro 266) | «a **120 pies (36 m)** o menos» — imperial primero, métrico entre paréntesis |
  | *Proyectar imagen* (libro 323) | «moverla hasta **60 pies/18 m**» — imperial primero |

  **Por qué importa:** `_meta` de `hechizos.json` declara que las conversiones
  son **añadido editorial** porque «23 páginas leídas por nueve lectores no
  imprimen ni una sola unidad imperial». Si eso es cierto, estos cinco no son un
  añadido: **el valor métrico del manual se perdió o se invirtió**, que es un
  defecto de otra familia. Los tres primeros ni siquiera tienen métrico que
  recuperar.

  **No se ha tocado nada**: son cinco lecturas de página, y hasta hacerlas no se
  sabe si el manual imprime ahí una cifra métrica distinta. Queda anotado con
  sus páginas para que la próxima tanda lo tenga localizado.

- **Fichas de nivel 20 monoclase: dos huecos que solo se ven al construir una
  (2026-08-30)** — la forma más rápida de saber si el sistema aguantaba el nivel
  20 era **construir una ficha y ver qué se rompía**. Se rompieron dos cosas, y
  ninguna era un dato malo: eran datos que **nadie ataba a su fuente**.

  **1 · Las características finales no las justificaba nadie.** Un monje de
  nivel 20 con **las seis características a 20** y ninguna explicación
  **verificaba en verde**. `caracteristicas.final` se escribía a mano y nada lo
  ataba a `base` + `ajuste_trasfondo` + las mejoras tomadas. En una base cuyo
  lema es que nada entra sin cita, era el hueco más grande que quedaba.

  Cerrado con el bloque `mejoras` y `verificar_mejoras()`, que comprueba cuatro
  cosas: que la suma cuadre **característica a característica**; que cada mejora
  reparta lo que dice la dote (`dotes/generales.yaml#Mejora de característica`,
  pdf 209 = libro 207: «Aumenta en 2 una puntuación… o aumenta dos en 1 cada
  una. No puede superar 20»); que ninguna pase de 20; y que **cada nivel de
  mejora esté gastado**, en una mejora o en una dote con `origen.nivel`, ni de
  más ni de menos. Los niveles de mejora se leen de la progresión de la clase,
  no de una lista escrita a mano.

  **2 · Nadie contaba los conjuros.** Un mago de nivel 20 con dos trucos habría
  pasado igual. Y al contar aparecieron cinco fichas con más conjuros de los que
  concede su tabla — **todos justificados, pero solo en la prosa de
  `decisiones`, que ningún script lee**. Se reutiliza la convención que el
  equipo ya usaba: cuenta contra la tabla lo que viene del lanzamiento normal de
  la clase; todo extra —dote, especie, opción de orden, o con `nota` de «no
  cuenta contra el límite»— tiene que **declarar de dónde sale**.

  **Y salió un defecto real en la ficha de ejemplo de la propia base.**
  `_ejemplo_aerin.yaml` llevaba **1 conjuro preparado donde la tabla del Brujo
  concede 2**. Estaba ahí desde la Fase 8a, invisible porque nadie contaba.
  Corregido con *Maleficio* y su entrada en `decisiones`.

  **Las dos fichas que lo sostienen:** `draconido_monje_n20.yaml` (Monje 20 /
  Guerrero de la Mano Abierta: 4 mejoras, 20 niveles de PG, `pg_max` 143, CA 19,
  velocidad 18 por la columna del rasgo) y `gnomo_mago_n20.yaml` (Mago 20 /
  Evocador, **55 referencias**: 5 trucos y 25 preparados de clase más los
  extras declarados de dote y especie, `pg_max` 142, CD de conjuros 19).
  `_verificacion/mutaciones_nivel20.py` → **11/11** *(esa tarde; la suite creció a 15/15 al cerrar los huecos del estrés con agentes, más abajo)*.

  **Lo que esto deja hecho:** el sistema construye, verifica y sube fichas
  monoclase **de nivel 1 a 20**, con cada número trazable a su regla citada.

- **La deuda declarada, saldada (2026-08-30)** — cuatro de las seis deudas
  anotadas en `CONTINUAR.md` se cerraron; las dos que quedan son decisión del
  usuario. Plan y resultado en `PLAN_DEUDA.md`. **Lo primero fue medirlas, y dos
  resultaron mucho más pequeñas de lo que decían los documentos.**

  **1 · La ceguera de `validar_tirada()`: 9 conjuros, no «no medido».** El
  chequeo usaba `_RE_SALVACION`, que exige el «tirada de salvación de X»
  completo, y `hechizos.json` se declara `fidelidad: mixto` porque parte del
  texto **elide «tirada de»**. Nueve conjuros quedaban fuera y **tres** de ellos
  llevaban un `tirada: TdS X` que nunca se había contrastado. Unificado a la
  forma laxa: los tres cuadran.

  **2 · Las tres etiquetas del ataque cuerpo a cuerpo, y no era lo que
  parecía.** Los 14 conjuros con «ataque de conjuro **a distancia**» usan
  **todos** `D20+ata.conj.`, sin una excepción — eso fija el vocabulario. Para
  los 11 «cuerpo a cuerpo» hacía falta un criterio, y **la página lo da**: dos
  lectores independientes leyeron *Arma espiritual* y *Enredadera*
  (`agente-ATQ-G.md`, `agente-ATQ-H.md`) y coincidieron palabra por palabra en
  el verbo que decide:

  > «**Haz** un ataque de conjuro…» → el conjuro **es** el ataque
  > «**puedes hacer** un ataque…» → el conjuro **se manifiesta igual** y el
  > ataque viene después

  **Dos de mis suposiciones estaban invertidas**, y solo la lectura lo vio:
  *Arma espiritual* dice «puedes hacer» (luego es `Directo`, no un ataque) y
  *Enredadera* dice «Haz» (luego es un ataque, no `Directo`). **6 correcciones**
  en total, `tiradas` añadido a 4 conjuros, y el reparto queda sin ambigüedad:
  **6** `D20+ata.CaC` · **5** `Directo` con su ataque en `tiradas` · **14**
  `D20+ata.conj.`. El chequeo nuevo `validar_ataques()` contrasta **25 ataques
  contra su propio texto**.

  **3 · La cita que faltaba, cerrada.** «Clase de armadura. Sin armadura ni
  escudo, tu clase de armadura base es 10 más el modificador por Destreza…»
  (**pdf 43 = libro 41**), leída por dos lectores independientes que coinciden
  palabra por palabra (`agente-CA-E.md`, `agente-CA-F.md`). **Y confirma una
  sospecha:** la página condiciona la fórmula a «sin armadura **NI ESCUDO**» y
  remite al capítulo 6 en cuanto hay una u otro. El efecto por defecto **no**
  lleva esa condición —sería quedarse sin base ninguna—: el modelo lo resuelve
  como lo resuelve el manual, con la armadura aportando su `base` y el escudo su
  `add` desde `equipo/armaduras.yaml`, cuyo bloque `reglas` **es** el capítulo 6.
  La condición queda citada, no perdida. El aviso permanente desaparece y pasa a
  **error** si alguien añade una variable con base y sin cita.

  **4 · El escalado por nivel, sin inventar ningún escalado.** `velocidad` entra
  en el vocabulario con dos piezas nuevas: `columna:`, que **lee** la tabla
  dispersa de la progresión en vez de copiarla (la de «Movimiento sin armadura»
  **ya existía** como columna `mov_sin_armadura_m`), y `decimal: true`, porque
  4,5 m es media casilla real y no un redondeo — el Goliat sale a **10,5 m** sin
  truncar. Ficha nueva `draconido_monje_n2.yaml` que lo sostiene: **con escudo
  pierde a la vez la CA y el movimiento** (15→14, 12→9), así que el efecto es
  carga y no decoración.

  **Dos falsos positivos propios.** El chequeo de ataques marcó a *Mano de
  Bigby*: su «Haz un ataque» está **dentro de un modo**, no en el lanzamiento —
  se afinó para que la estructura (`tiradas`, con su página y su doble lectura)
  mande sobre el verbo. Y `validar_dados()` contó un `D3` que era **mi propia
  nota** («deuda D3») dentro de un bloque YAML: su filtro salta la línea
  `_nota:` pero **no las de continuación del bloque**. Es una limitación real
  del filtro, hoy esquivada reescribiendo la nota.

- **Fase 16 — `/subir-nivel`, y la deuda que la Fase 14 había dejado escondida
  (2026-08-30)** — al empezar la fase apareció que **la Fase 14 había roto un
  paso documentado de la skill `/personaje` y nadie se había enterado**. Su
  paso 10 mandaba ejecutar `python3 calculo.py ca --clase Monje`, y desde que
  las fórmulas de CA son efectos citados esa función **sale con error a
  propósito** (no puede saber el nivel, la subclase ni el escudo). Que falle es
  correcto; que la skill siguiera mandándolo, no.

  **Ningún chequeo miraba las skills.** Es exactamente el mismo agujero que
  tenían los documentos de estado antes de `verificar_documentos.py`, y en un
  proyecto cuyo estado vive en disco **una skill desfasada es un defecto de
  datos**: quien la siga trabajará hacia atrás.

  **Pagado:** `verificar_personaje.py --calcular` imprime el bloque `calculado`
  ya agregado desde la ficha entera, y las dos skills lo usan. Y
  `verificar_documentos.py` comprueba ahora que **los scripts y subcomandos que
  las skills mandan usar existan**. Con su límite escrito al lado: **esto no
  habría cazado aquella rotura** —`calculo.py ca --clase` existía y sus flags
  eran válidas; lo que falló fue el resultado en ejecución para 4 clases—, así
  que queda dicho en vez de fingir que el agujero está cerrado.

  **El vocabulario de subida se midió, no se copió.** `ANALISIS_REPOS.md` §2
  describe los **nueve** tipos de *advancement* de Foundry. Se declaran solo los
  que esta base ejercita: `Size` y `ModifyItem` no los usa nada, y declararlos
  sería la misma expresividad inventada que la Fase 15 rechazó de PCGen. Medido:
  **12** marcadores de subclase (siempre nivel 3), **51** de mejora de
  característica (niveles 4-16), **35** de rasgo de subclase (niveles 6-20), más
  las columnas de escala de cada clase.

  **`subir_nivel.py` separa lo que la base CONCEDE de lo que el jugador ELIGE**,
  que es lo único que aporta la taxonomía de Foundry, y **falla ruidosamente**:
  un rasgo que la tabla concede sin texto, una subclase sin el rasgo del nivel
  que la tabla promete, o un nivel en el que «no pasa nada» son errores, nunca
  una lista vacía.

  **`validar_subida()` corre los 333 saltos** —12 clases × niveles 2-20, y los
  de subclase una vez por subclase— en 8 segundos: **0 errores**. La base sabe
  explicar todos los niveles de todas las clases y subclases.

  **Y se subió una ficha de verdad**, que es la prueba que importa:
  `personajes/draconido_hechicero_n4.yaml`, de nivel 3 a 4. Ejercita las tres
  piezas nuevas a la vez — los PG por elección (`pg_max` 24 → **31**, con el
  término de Constitución recalculado y *Resistencia dracónica* escalando con el
  nivel de clase), la **dote elegida por prerrequisito** (*Lanzador ritual*, el
  único de los 65 con separador `;` y alternativa de tres características), y el
  bloque `calculado` pedido al script en vez de escrito a mano.

  `_verificacion/mutaciones_subida.py` → **7/7**.

  **Dos falsos positivos propios, otra vez de las mutaciones y no del chequeo.**
  Uno mutaba un rasgo de **nivel 1**, que `validar_subida()` no recorre (empieza
  en el 2); el otro usaba un formato de columna que no existe
  (`ataque_furtivo: 1` en vez de `"1d6"`). Van tres tandas seguidas en que el
  fallo estaba en la mutación: conviene contarlo, porque es la señal de que las
  mutaciones se escriben con la misma prisa con la que se escribiría el defecto.

- **Fase 15 — prerrequisitos de dote evaluables (2026-08-30)** — el
  prerrequisito de una dote era **prosa**: «nivel 4 o más, Fuerza o Destreza 13
  o más». Un LLM que la lee acierta casi siempre, y «casi siempre» es la
  **amenaza nº 5 del FODA**: un acierto por el método equivocado es
  indistinguible de acertar por casualidad.

  **El inventario decidió el diseño, no al revés.** 75 dotes · **65 con
  prerrequisito** · **11 formas distintas**, que se descomponen en **4 átomos y
  2 conectores**: `nivel ≥ N`, `característica ≥ N` (con alternativas), `rasgo`
  (con alternativas) y `entrenamiento con <categoría>`; la coma es **Y** y el
  «o» interno es **O**.

  **Decisión, y ahorra trabajo:** `ANALISIS_REPOS.md` §5 propone copiar la idea
  de PCGen —negación con `!` y «N de M» (`PREMULT:N`)—. **No hace falta:** en
  los 65 prerrequisitos reales **no hay ni una negación ni un solo «N de M»**.
  Copiarlo sería inventar expresividad que nada usa, y una gramática con ramas
  que ningún dato ejercita es una gramática sin probar.

  **El punto y coma no era un segundo conector.** Aparece **una sola vez** en
  los 65, y por una razón: el término que lo sigue lleva comas dentro («nivel 4
  o más; Inteligencia, Sabiduría o Carisma 13 o más»). Es el mismo «y», escrito
  con el separador que no genera ambigüedad. El renderizador aplica ese mismo
  criterio, y por eso el ida y vuelta reproduce el original.

  **Segunda decisión: se DERIVA, no se duplica.** El plan original decía guardar
  la estructura junto a la prosa en `dotes/*.yaml`. **No se hizo**, y a
  propósito: sería justo lo que la regla 3 de `reglas/_ESQUEMA_efectos.md`
  prohíbe —dos copias del mismo dato que nadie vuelve a comparar y que divergen
  en silencio—, el modo de fallo nº 10. El parseo es determinista y el ida y
  vuelta lo demuestra en los 65, así que la prosa citada sigue siendo la única
  fuente.

  **El chequeo fuerte es de ida y vuelta.** `validar_prerrequisitos()` parsea la
  prosa, la reconstruye desde la estructura y exige que salga **idéntica**:
  **65/65 exactos**. Eso demuestra que no se perdió ni se inventó nada. Y un
  segundo chequeo con precedente: cada rasgo citado («Estilo de combate»,
  «Lanzamiento de conjuros», «Magia del pacto») y cada categoría de
  entrenamiento tienen que **resolver a un registro real** — citar un rasgo que
  no existe es el bug `Clerigo` otra vez.

  **Y sirve para algo:** `buscar.dotes_disponibles(<ficha>)` devuelve qué dotes
  puede tomar un personaje **con el porqué de cada una**, y **falla ruidosamente**
  si la lista sale vacía (hay 10 dotes sin prerrequisito alguno, así que vacía
  es siempre sospechoso). `cobertura.py` pasa de 27 a **31 preguntas**.

  `_verificacion/mutaciones_prerrequisitos.py` → **10/10**.

  **Un límite declarado, no disimulado:** nada comprueba que una dote *deba*
  tener prerrequisito. Si alguien borra el de una dote que lo tenía, el resto
  sigue cuadrando y el chequeo calla. Está escrito como control negativo con su
  nombre, para que quede dicho en vez de descubrirse tarde.

- **Fase 14b-3 — `tiradas` por efecto: el campo único deja de aplastar la
  información (2026-08-30)** — `tirada` es un solo campo y responde a **una
  sola** pregunta: ¿el conjuro exige una tirada para manifestarse? Esa pregunta
  sigue siendo válida y `validar_tirada()` la sigue vigilando sin cambios. Lo
  que el campo no podía decir es **cuántas tiradas pide el conjuro y de qué tipo
  cada una**.

  **Los «cinco duros» resultaron ser cuatro.** *Estática sináptica* era un
  **falso positivo de la heurística**: su segunda característica venía de
  «tirada de salvación de Constitución **para mantener la concentración**», que
  es la regla de concentración citada de pasada, no una salvación que el conjuro
  exija. Los dos lectores lo vieron bien; la regex no. Está convertido en
  control negativo de `mutaciones_tiradas.py`.

  | Conjuro | Lo que el campo único no podía decir |
  |---|---|
  | *Símbolo* | **6 modos** con salvación propia (Aturdimiento Sab · Discordia Sab · Dolor Con · Muerte Con · Sueño Sab · Terror Sab), **más una PRUEBA** de Sabiduría (Percepción) para detectar el glifo, que no es salvación ni ataque |
  | *Muro prismático* | la salvación de Destreza se hace **una vez por capa** (siete), y las capas 6 (Añil) y 7 (Violeta) añaden salvación propia |
  | *Mano de Bigby* | **4 modos**, y uno de ellos —«Puño cerrado»— **no es salvación sino tirada de ataque**. El campo decía `Directo` |
  | *Muro de hielo* | dos salvaciones distintas en momentos distintos (al aparecer el muro; al cruzar el aire gélido) |

  **Hicieron falta cuatro lecturas, no dos.** Dos de los conjuros **se parten de
  página** —*Símbolo* empieza en libro 332 y su cuerpo entero está en el 333;
  *Mano de Bigby* empieza en el 307 y sigue en el 308— y **los dos primeros
  lectores avisaron por separado** de que faltaba texto en vez de rellenarlo.
  Se rindieron dos lectores nuevos sobre las páginas de continuación, y también
  coincidieron. Por eso **cada efecto lleva la página donde de verdad está**, no
  la del principio del conjuro.

  **Las descripciones de la base estaban completas.** No había hueco de
  transcripción: los 6 modos y los 4 modos ya estaban escritos. **El defecto era
  solo del modelo**, exactamente como lo había declarado `_tirada_semantica`.

  **Una discrepancia del propio manual, reproducida y no normalizada.** En
  *Símbolo*, el párrafo de introducción lista «aturdimiento, discordia, dolor,
  muerte, **miedo** o sueño», pero el epígrafe de la sexta variante dice
  **«Terror»**. Los dos lectores lo señalaron por separado. La base imprime las
  dos palabras porque así están en la página; corregir una sería inventar.

  **El chequeo, y su mitad que importa.** `validar_tiradas()` cubre la **forma**
  (vocabulario, `cuando`, página numérica) y, sobre todo, la **AUSENCIA**: si la
  descripción exige salvaciones de más de una característica y no hay lista, es
  error. Además hace **ida y vuelta**: lo declarado tiene que ser exactamente lo
  que pide el texto, ni una salvación inventada ni una perdida.
  `_verificacion/mutaciones_tiradas.py` → **13/13**.

  **Un descubrimiento lateral sobre `validar_tirada()`, que conviene no
  olvidar.** El chequeo usa `_RE_SALVACION`, que exige el «tirada de salvación
  de X» **completo** — y `hechizos.json` se declara `fidelidad: mixto`
  precisamente porque parte del texto quedó condensado y **elide «tirada de»**:
  *Muro de hielo* dice «hace salvación de Destreza». Con la regex estricta, ese
  conjuro **no tiene ninguna salvación detectable**, así que su coherencia nunca
  se comprobó. El chequeo nuevo usa la forma laxa. **Cuántos conjuros más están
  en esa sombra no se ha medido: queda abierto.**

  **Y una incoherencia abierta, medida y no tocada.** De los **11 conjuros** cuya
  descripción dice «ataque de conjuro cuerpo a cuerpo», **4** llevan
  `D20+ata.conj.`, **3** llevan `D20+ata.CaC` y **4** dicen `Directo`.
  `validar_tirada()` no lo ve porque los tres valores están en el vocabulario —
  otra vez «un campo con la forma correcta puede ser basura». Normalizarlos exige
  decidir qué distingue los dos términos, que es criterio y no limpieza, así que
  se anota en vez de arreglarse a ciegas.

- **Fase 14b-2 — el componente material, descompuesto: dos sumas más que la
  página nunca imprimió (2026-08-30)** — `componentes.coste` era un solo string,
  y los seis conjuros con varios materiales vivían como **exención declarada** en
  `COSTE_COMPUESTO` dentro de `verificar_foundry.py`: salían del contraste
  externo en vez de representarse. Al descomponerlos aparecieron **dos datos
  agregados nuevos**, del mismo género que *Vínculo protector* y *Cofre oculto
  de Leomund*:

  | Conjuro | La base guardaba | La página dice |
  |---|---|---|
  | *Proyección astral* | `1100 po/u*` | jacinto **1000 po** + lingote de plata **100 po**, «por cada objetivo del conjuro», **los dos se consumen** (pdf 324 = libro 322) |
  | *Conocer las leyendas* | `250 po* / 200 po` | incienso **250 po** (se consume) + **cuatro tiras de marfil** de **50 po** (pdf 263 = libro 261) |

  `1100` es `1000 + 100`; `200` es `4 × 50`. **Van cuatro sumas** que ninguna
  página imprime. Los **dos lectores independientes** (`agente-MAT-A.md`,
  `agente-MAT-B.md`) coinciden literalmente en las seis cláusulas y **los dos
  declaran por separado que en ninguna de las cinco páginas aparece una cifra
  que sea la suma de dos materiales**.

  **Y un tercer defecto de modelo, no de dato: el consumo era por conjuro.**
  `consume_material` es un solo booleano, pero en *Clon* se consume el diamante
  y **no** el recipiente, y en *Conocer las leyendas* el incienso y **no** las
  tiras. Ahora `consume` es **por material**; el booleano único se conserva
  **derivado** (`any`), porque el SRD también publica uno solo y es contra eso
  contra lo que se contrasta.

  **Una ambigüedad declarada, no resuelta.** La página castellana dice «cuatro
  tiras de marfil que valgan al menos 50 po», **sin «cada una»**; el SRD inglés
  sí dice «50+ GP each». Los dos lectores lo señalaron por separado. Manda el
  manual: se guarda 50 sin declarar por-unidad, y la ambigüedad queda escrita en
  el propio registro (`_ambiguo`).

  **Lo construido:** `materiales.py` (la ÚNICA implementación de la derivación
  `materiales → coste`, para que `validar.py` y `verificar_foundry.py` no puedan
  discrepar), `validar_materiales()` con un chequeo de **ida y vuelta** —`coste`
  debe ser idéntico al que produce la descomposición, así que reescribir el
  total a mano deja de cuadrar—, y `_verificacion/mutaciones_materiales.py`
  → **10/10**.

  **El contraste externo sube de 3012 a 3020 valores**: los seis dejan de estar
  exentos y se comparan material a material contra el SRD, que es la única
  fuente que **conserva la descomposición** y por tanto la única capaz de ver
  este modo de fallo.

  **Dos falsos positivos propios, que conviene registrar.**
  1. La primera versión de `validar_materiales()` marcó **26 conjuros sanos**
     porque su regex no contemplaba el asterisco de «se consume» (`«10 po*»`),
     que es convención vieja de esta base. El chequeo estaba mal, no el dato.
  2. En `verificar_foundry.py` llamé `srd` a una lista local y **pisé el
     diccionario del pack**: desde el primer conjuro compuesto, ningún conjuro
     posterior emparejaba, y el contraste cayó de **3012 a 1818 valores sin un
     solo error**. Lo delató **la cifra**, no un fallo — que es exactamente para
     lo que se publica y se vigila el total contrastado.

- **Fase 14b-1 — `pg_max` deja de ser un escalar (2026-08-30)** — los puntos de
  golpe máximos pasan a calcularse desde la **historia de la ficha**: una
  entrada por nivel con el método elegido (`maximo_dado` en el 1, `tirada` o
  `valor_establecido` en los siguientes) y el valor crudo obtenido.

  **Por qué la historia y no un total guardado.** El paso 5 de «Subir de nivel»
  (pdf 44 = libro 42) dice que cuando el modificador por Constitución aumenta en
  1, los PG máximos aumentan «en 1 **por cada nivel que hayas alcanzado**». Es
  **retroactivo**. Un motor que sumara «lo ganado en el nivel N» y guardara el
  total acertaría **hasta la primera dote que subiera Constitución**, y a partir
  de ahí se equivocaría en silencio — el mismo género que la deriva ficha↔base
  de la amenaza nº 6 del FODA. Recalculando entero desde los valores crudos, la
  regla del paso 5 **sale sola** en vez de tener que aplicarse a mano.
  Comprobado: en un personaje de nivel 3, subir Constitución de 14 a 16 sube los
  PG en **3**, no en 1.

  **El método es una elección del jugador y el motor no lo adivina.** Una tirada
  no es reproducible, así que se guarda el **resultado**. Si una ficha de nivel
  ≥2 no declara `pg_por_nivel`, `calculo.pg_max_de_ficha()` **se niega** en vez
  de suponer un método.

  **Un caso que la base no resuelve, avisado en vez de decidido.** El «mínimo de
  1» del paso 2 se aplica al **total** (valor + mod. Con), no al dado. Si algún
  nivel lo toca, el paso 2 y el paso 5 dejan de decir lo mismo y **ninguna
  página leída dice cuál manda**. El verificador emite un aviso nombrando el
  nivel. Regla 3: decir «no lo tengo».

  **Prueba de carga:** ficha nueva `personajes/draconido_hechicero_n3.yaml`
  (Hechicero 3, Hechicería Dracónica), que ejercita los tres métodos en sus tres
  niveles **y** los dos efectos de *Resistencia dracónica* — el `pg_max` que el
  campo-parche no podía representar y la fórmula de CA que `calculo.py` no
  conocía. `_verificacion/mutaciones_pg.py` pasa de 9/9 a **13/13**, con una
  mutación dedicada a la retroactividad. **13/13 fichas verificadas.**

  **`valor_establecido_pg()` lee la tabla, no la calcula.** El valor fijo
  coincide con `(caras/2)+1`, pero calcularlo aquí destruiría el contraste
  cruzado de `validar_puntos_golpe()`, que existe precisamente porque hay **dos**
  transcripciones independientes que deben cuadrar.

- **La regla de PG al subir de nivel no estaba en la base (2026-08-30)** — un
  hueco de contenido, no una errata. La base tenía `dado_golpe` en las 12 clases
  y `puntos_golpe_nivel_1()` en `calculo.py`, y **nada más**: la regla de los
  niveles posteriores al 1 no existía en ningún fichero. Lo único que la
  mencionaba era `multiclase.puntos_golpe_y_dados_golpe`, que remitía a «los
  puntos de golpe de la nueva clase como los de *niveles siguientes al 1*» — **a
  una sección que nadie había escrito**. `/subir-nivel` (Fase 16) no podía subir
  a nadie de nivel.

  **Y `cobertura.py` daba «0 preguntas sin responder».** `cobertura_subir_nivel()`
  comprobaba que los rasgos de clase, subclase y especie tuvieran texto
  consultable y **nunca preguntaba por los PG**, que son el paso 2 de «Subir de
  nivel» en el manual. El chequeo cubría lo que su autor recordaba — **el mismo
  patrón que dejó dos fórmulas de CA fuera de `calculo.py`**. Con la pregunta
  añadida, el bloque pasó de 15 a 27.

  **Método:** dos agentes Sonnet leyeron **la misma página de forma
  independiente**, sin ver el informe del otro (`agente-PG-A.md`,
  `agente-PG-B.md`, briefing en `LEEME_PG_NIVEL.md`). **Coinciden literalmente**
  en el texto de los pasos 2 y 5, en el título de la tabla, en sus cuatro filas
  y en **las dos ausencias** (la palabra «máximo» no acompaña nunca a «dado de
  golpe» en esa página, y la regla del nivel 1 no está ahí).

  **Transcrito** en `reglas/generacion_personaje.yaml → puntos_golpe`
  (pdf 44 = libro 42, «Subir de nivel», pasos 2 y 5):

  - **Tirar** el dado de golpe + mod. Con, **mínimo 1 en el TOTAL** (no en el dado).
  - O el **valor establecido** de la tabla «Puntos de golpe establecidos por
    clase»: Bárbaro 7 · Explorador/Guerrero/Paladín 6 ·
    Bardo/Brujo/Clérigo/Druida/Monje/Pícaro 5 · Hechicero/Mago 4.
  - **El aumento del modificador por Constitución es RETROACTIVO**: sube los PG
    máximos «en 1 por cada nivel que hayas alcanzado».

  **La regla del nivel 1 y la de los niveles siguientes son distintas y viven en
  páginas distintas.** El «máximo del dado» es la del nivel 1 (pdf 42 = libro
  40); la alternativa a tirar en niveles posteriores es un **valor fijo**, no el
  máximo.

  **Chequeo nuevo, y es cruzado.** El valor fijo de cada clase resulta ser
  `(caras / 2) + 1`, así que la tabla (pdf 44) y los `dado_golpe` de las 12
  clases — transcritos por separado, de páginas y sesiones distintas — se
  contrastan **sin abrir el manual**. `validar_puntos_golpe()`, probado por
  `_verificacion/mutaciones_pg.py` → **13/13**, con mutaciones **en las dos
  direcciones**: romper la tabla y romper el dado de la clase. Un contraste
  cruzado probado por un solo lado no habría demostrado que es cruzado.

  **No se implementó el cálculo, a propósito**, y queda anotado en
  `CONTINUAR.md` lo que la fase que lo haga no debe descubrir por las malas: los
  PG máximos **no son una suma acumulada** (el término de Constitución se
  recalcula entero), el método es **una elección del jugador por nivel** que el
  motor tiene que leer de la ficha y no puede calcular, y **queda una pregunta
  abierta declarada**: si un mod. Con negativo empeora después, la página no
  dice si el «mínimo de 1» se recalcula hacia atrás. Se declara en vez de
  adivinarla.

- **Las cifras de las pruebas por mutación estaban desfasadas en cuatro sitios
  (2026-08-29)** — al retomar el proyecto, los documentos de estado decían:

  | Documento | Decía | La realidad |
  |---|---|---|
  | `FODA.md` (×2) | `mutaciones_integridad` 23/23 | **24/24** |
  | `ESTADO_13p.md` | `mutaciones_integridad` 21/21 | **24/24** |
  | `CONTINUAR.md` | `mutaciones_foundry` 21/21 **y** 25/25 **y** 29/29 | **29/29** |
  | `FODA.md` | `mutaciones_foundry` 25/25 | **29/29** |

  `CONTINUAR.md` se contradecía **a sí mismo tres veces** sobre la misma cifra.

  **Por qué sobrevivió:** `verificar_documentos.py` contrastaba las cifras de
  los validadores y **ninguna de las suites de mutación** — justo el bloque
  donde las cifras cambian cada vez que se añade una mutación y nadie vuelve a
  mirar el `.md`. El chequeo existía y miraba a otro lado, que es el mismo
  patrón que `_CA_SIN_ARMADURA` y su grep.

  **Corregido y cerrado por código.** `verificar_documentos.py` ahora **ejecuta**
  `mutaciones_dados` (12/12), `mutaciones_conversiones` (13/13),
  `mutaciones_integridad` (24/24) y `mutaciones_efectos` (20/20) y compara con
  lo que prometen los documentos. `mutaciones_foundry` queda fuera porque tarda
  más de diez minutos —un chequeo que nadie corre por lento no chequea nada— y
  de esa se comprueba que los documentos **no se contradigan entre sí**, que es
  lo que aquí falló. El modo completo es el **defecto**; `--rapido` lo salta.

  **La primera versión del chequeo dio tres falsos positivos**, y conviene que
  conste: la regex `mutaciones_dados[^\n]*?(\d+)/(\d+)` cruzaba de línea en
  `FODA.md`, donde varios scripts se listan en la misma frase, y se llevaba la
  cifra del siguiente. Se acotó con `(?:(?!mutaciones_)[^\n])*?`.

- **Fase 14 — motor de efectos: las reglas dejan de ser `if` de Python
  (2026-08-29)** — `calculo.py` traía las fórmulas de "Defensa sin armadura"
  como `lambda` indexadas por nombre de clase, con este comentario:

  > *Son las dos únicas excepciones en el tronco de clase (confirmado por grep
  > sobre las 12 clases).*

  Era cierto, y por eso mismo era el problema. **La base tiene CUATRO fórmulas
  de CA base**, y las otras dos están en subclases: *Juego de pies
  deslumbrante* (Colegio de la Danza, pdf 66 = libro 64) y *Resistencia
  dracónica* (Hechicería Dracónica, pdf 135 = libro 133). **El grep miró donde
  el `lambda` sabía mirar.** Un caso cableado no puede descubrir que existe una
  quinta regla; un dato validado, sí.

  Lo mismo con los PG máximos. `personajes/_ESQUEMA.md` tenía un campo
  `bonus_pg_especie` que el propio esquema admitía como parche, y falló de tres
  maneras a la vez:

  1. cubría **1 de los 2** efectos de PG de la base (*Resistencia dracónica*
     también sube PG, +3 en nivel 3 y +1 por nivel de hechicero, y no tenía
     dónde declararse);
  2. guardaba un `1` fijo cuando *Aguante enano* dice «y en 1 más **cada vez que
     subes de nivel**» — correcto en nivel 1 y silenciosamente falso desde el 2;
  3. **nadie obligaba a rellenarlo**, y por eso
     `personajes/enano_guerrero.yaml` lo tenía vacío: `pg_max: 12` donde tocaba
     13. **La única ficha de Enano de la base verificaba en verde con los PG
     mal**, y el comentario que justificaba el campo citaba justo ese caso
     («bug real hallado en ronda 2: Guerrero/Enano») sin que nadie comprobara
     que se había aplicado.

  **Corregido.** `personajes/enano_guerrero.yaml` → `pg_max: 13`, con su
  entrada en `decisiones`. La corrección es de **coherencia interna** —la ficha
  contradecía al registro ya auditado de `especies/especies.yaml` (pdf 192 =
  libro 190)—, no de transcripción: no hizo falta reabrir el manual.

  **Lo construido:**

  | Pieza | Qué |
  |---|---|
  | `reglas/efectos.yaml` | Vocabulario **cerrado**: variables, las 6 operaciones, el orden de agregación y las 4 condiciones |
  | `reglas/_ESQUEMA_efectos.md` | El contrato, y lo que el modelo **no** representa todavía |
  | `efectos.py` | El motor: gramática de fórmulas, agregación, grafo de dependencias |
  | `validar_efectos()` | Chequeo nuevo en `validar.py` (6 efectos, 0 errores) |
  | `_verificacion/mutaciones_efectos.py` | **20/20** (14 detecciones + 6 controles negativos) |

  **Los 6 efectos declarados**, cada uno con la página del rasgo que lo concede:
  `ca` base ×4 (Bárbaro pdf 53, Monje pdf 151, Bardo/Danza pdf 66, Hechicero/
  Dracónica pdf 135) y `pg_max` add ×2 (Enano pdf 192, Hechicero pdf 135).

  **Tres decisiones de diseño, para no volver a abrirlas:**

  1. **Varios `base` a la vez = elegir, no maximizar.** DiceCloud agrega varios
     `base` con `max()`. El manual dice otra cosa: «solo puede beneficiarse de
     una, **a elegir**» (`reglas/generacion_personaje.yaml →
     multiclase.clase_de_armadura`). El motor **exige** la elección en
     `elecciones.ca_base` y falla ruidosamente si no la hay. Coger la mayor
     acertaría casi siempre — y eso es indistinguible de acertar por casualidad.
  2. **Lo ya estructurado no se duplica como efecto.** El `+2` del escudo y las
     fórmulas de armadura se **derivan** en código del campo `ca` de
     `equipo/armaduras.yaml`. Escribir el `+2` al lado del `+2` es el modo de
     fallo nº 10 («dato agregado»): dos copias que divergen en silencio.
  3. **`velocidad` NO entra en esta pasada.** «Movimiento sin armadura» del
     Monje (+3 m en nivel 2, +4,5 en el 6…) es una tabla dispersa con
     decimales — el `ScaleValue` de Foundry — y pide su propia decisión de
     modelo. Se declara el hueco en vez de inventar un escalado.

  **Un defecto de modelado, cazado por las 12 fichas.** La primera versión
  representaba el tope de Destreza de una armadura («13 + mod. Des (máx. 2)»)
  como `op: max` sobre la CA agregada. Forma correcta, **sitio equivocado**: el
  tope acota el término de Destreza, no la CA final, y se comía el +2 del
  escudo del clérigo (CA 15 donde la ficha decía 16). Lo cazó la suite de 12
  fichas, no ningún chequeo de forma — **otra vez el patrón de la amenaza nº 3
  del FODA**. Hoy la armadura es **un solo efecto `base`** con la fórmula tal y
  como la imprime la tabla, `min(mod_des, 2)` incluido.

  **Un hueco declarado, no tapado.** La CA de quien no lleva nada
  (`10 + mod_des`) **no tiene página citada en esta base**: venía como literal
  sin cita dentro de `calculo.py`. Se declara con `_falta_cita: true` y
  `validar_efectos()` **avisa mientras siga abierta**. Cerrarla es una lectura
  de página. Regla 3: decir «no lo tengo» en vez de inventar la cita.

  **Y `calculo.ca()` ahora se niega en vez de mentir.** Si la CA sin armadura de
  una clase depende de un rasgo, la función sale con error y remite a la ficha,
  en lugar de devolver `10 + mod. Des` como hacía con el Bardo y el Hechicero.
  Lo pregunta a los datos (`efectos_declarados()`), no a una lista escrita a
  mano — que es lo que dejó fuera a las dos fórmulas de subclase.

- **`verificar_documentos.py` — un quinto validador, para los documentos
  (2026-08-29)** — el 29 de agosto hubo que corregir **tres documentos de estado
  que describían como pendiente algo ya hecho**: `FODA.md` mandaba ejecutar las
  Fases 9c y 10 (ambas cerradas), `CONTINUAR.md` decía «lo único pendiente es la
  Fase 8» y daba por hacer la tarea de `fidelidad` que se acababa de completar, y
  `ESTADO_13p.md` daba por abiertos el remuestreo de B5 y tres avisos de
  vecindad cerrados ese mismo día.

  **Tres en una sesión, y ninguno lo detectó ningún chequeo** — porque ningún
  chequeo miraba los documentos. En un proyecto cuyo estado **vive en disco y no
  en la conversación**, `CONTINUAR.md` no es documentación: es el dato con el que
  otra sesión decide qué hacer. **Un documento desfasado es un defecto de datos.**

  El script no puede comprobar la prosa, pero sí **las cifras**, que es donde el
  desfase se vuelve mentira comprobable: contrasta lo que `CONTINUAR.md` promete
  (646 y 3012 valores, más las siete cifras de la línea de INTEGRIDAD) y lo que
  `FODA.md` afirma (3658 valores externos) **contra la salida real de los
  validadores**, y comprueba que ningún documento vivo remita al FODA archivado
  sin marcarlo como tal. **11 comprobaciones, todas en verde.**

  Es la misma doctrina que el resto del proyecto aplicada un nivel más arriba:
  si un dato no se comprueba, se pudre en silencio. Solo que aquí el dato que se
  pudría era **el que dice qué hacer a continuación**.

- **Remuestreo del lote B5: la regla de la casa, validada empíricamente
  (2026-08-29)** — el lote B5 declaró **0 hallazgos en 14 conjuros**. Por la
  regla «un informe en blanco no prueba nada por sí solo», otro agente (R5)
  releyó los mismos 14 **de cero y sin ver su informe**.

  **Encontró uno real.** *Rayo nauseabundo* (pdf 328 = libro 326) llevaba un
  párrafo «Con un espacio de conjuro de nivel superior. El daño aumenta en 1d8
  por cada nivel…» que **la página no trae**: la entrada termina en «hasta el
  final de tu siguiente turno» y ahí acaba la columna. Verificado a ciegas por
  V13, que además comprobó que la página siguiente empieza con la continuación
  de *Recluir*, descartando un corte de página. De paso, su `resumen` llevaba una
  coma final por punto.

  **Es la primera vez que el remuestreo demuestra su valor con un caso
  concreto.** La regla existía desde el 22 de agosto por prudencia; ahora hay
  evidencia de que un lote limpio de 14 puede esconder un defecto, y del tipo
  peor: **una regla de más**, no un dato que falte.

- **Los 52 costes fuera del SRD, cerrados a mano — y una convención rota que
  llevaba una semana en la base (2026-08-29)** — el módulo nuevo cubre los 309
  conjuros que el SRD publica; **52 quedaban sin fuente externa posible**. Se
  leyeron sus líneas de `Componentes` una a una (lotes K1-K5).

  ⚠️ **La bolsa era mayor de lo que se creyó al empezar.** El recuento inicial
  dijo «33»: solo los de `coste: null`. Pero **los 19 que ya tenían coste
  tampoco estaban contrastados por nada**, y ahí es donde puede haber una cifra
  *mal*, no solo ausente. Lo destapó el propio chequeo al ejecutarse por primera
  vez, no el análisis previo.

  **Resultado: 31 «sin coste» confirmados, 18 cifras confirmadas, 3 corregidas.**

  | Conjuro | Corrección |
  |---|---|
  | *Cofre oculto de Leomund* | `coste` decía «**5050 po**» — **la suma de dos materiales**: el cofre (5000 po) y su réplica Diminuta (50 po). **La página nunca imprime «5050»** |
  | *Conjurar lluvia de flechas* | `null` → **`1 pc`** (ver la incoherencia de convención, abajo) |
  | *Conjurar descarga de proyectiles* | `null` → **`1 pc`** (ídem) |

  ***Cofre oculto de Leomund* es el segundo caso de «la base calculó en vez de
  transcribir»**, tras *Vínculo protector* ese mismo día. Van dos en una tarde, y
  los dos salieron del mismo sitio: contrastar contra una fuente que conserva la
  descomposición. Es un modo de fallo que **no estaba en la lista de nueve** y
  que merece nombre propio: **dato agregado**. No falta texto, no sobra, ninguna
  cifra está «mal» — simplemente alguien hizo una suma y guardó el resultado,
  perdiendo el desglose que la página sí da.

  ### La incoherencia: qué significa `coste`

  Cuatro conjuros comparten el mismo texto —«un arma … **que valga al menos X**»—
  y la base los trataba de dos maneras opuestas:

  | Conjuro | `coste` antes | |
  |---|---|---|
  | *Impacto certero* | `1 pc` | ✔ con coste |
  | *Golpe de viento acerado* | `1 pp` | ✔ con coste (puesto hoy) |
  | *Conjurar lluvia de flechas* | `null` | ✘ **sin coste** |
  | *Conjurar descarga de proyectiles* | `null` | ✘ **sin coste** |

  Los dos `null` venían de una decisión del **2026-08-22**, razonada así: «es un
  umbral de valor del arma, que no se pierde, **no un coste que se gaste**».

  **Esa decisión confundía dos campos distintos.** Lo que se gasta lo dice
  `consume_material`, que existe justamente para eso — y **39 de los 70 conjuros
  con coste declarado NO consumen su material** (*Identificar*, *Augurio*,
  *Clarividencia*, toda la familia *Invocar…*). Es decir: la convención de facto
  de la base es que **`coste` = valor mínimo del material**, se gaste o no. La
  decisión del 22 era la anómala, y encima ni siquiera se aplicó a *Impacto
  certero*, que llevaba `1 pc` con el mismo texto.

  **Unificados los cuatro con coste**, que es lo que hace además que el módulo
  nuevo pueda contrastarlos contra el SRD sin declarar excepciones.

  **Y conviene decir de quién es el error.** La incoherencia existía desde el 22;
  hoy se **agravó** al ponerle coste a *Golpe de viento acerado* sin haber visto
  la convención contraria que ya estaba escrita en este mismo fichero. La lección
  no es «leer más FUENTES.md» —tiene 1500 líneas— sino que **una convención que
  solo vive en prosa se rompe sola**: por eso ahora vive en `validar.py` como
  chequeo y en `_nota_verificacion` dentro de los cuatro registros.

  ### El chequeo que impide que la bolsa se reabra

  `validar_costes_sin_fuente()` avisa de todo conjuro con material **fuera del
  SRD** que no lleve `_coste_verificado`. **El resultado negativo cuenta igual
  que el positivo**: marcar «sin coste, comprobado en la página» es lo que
  distingue «lo miramos y no cuesta nada» de «nadie lo ha mirado» — la ambigüedad
  exacta que dejó pasar *Golpe de viento acerado*. El aviso converge a cero y
  vuelve a saltar con cualquier conjuro nuevo.

- **Los costes de material, contrastados por primera vez: módulo nuevo y
  2 defectos (2026-08-29)** — el módulo de conjuros de `verificar_foundry.py`
  comprobaba `consume_material` pero **no la cifra del coste**. La superficie la
  destapó la muestra post-corrección, con *Golpe de viento acerado* en `null`
  sobre una página que exige «un arma cuerpo a cuerpo que valga al menos 1 pp».

  **El SRD no publica el coste como número:** lo lleva dentro del texto inglés
  del material («worth 1,000+ GP», «1 Copper Piece»). Se extrae con regex y se
  compara sin traducir nada más que las tres unidades (GP→po, SP→pp, CP→pc).

  **Resultado: 309 conjuros emparejados, 303 coinciden exactamente**, 5 llevan
  formato compuesto declarado y **2 eran defectos**:

  | Conjuro | Corrección | Página |
  |---|---|---|
  | *Vínculo protector* | `coste` decía «**100 po**» — **la suma del par**. La página dice «un par de anillos de platino que valgan al menos **50 po CADA UNO**». Ahora «50 po/anillo» | pdf 345 |
  | *Indetectable* | «**25\***» → «**25 po\***»: **faltaba la unidad**, así que ningún script podía leer la cifra | pdf 296 |

  ***Vínculo protector* es el interesante: la base había CALCULADO en vez de
  transcribir.** 100 = 2 × 50 es aritméticamente impecable y factualmente falso
  como cita: quien preguntara el precio de un anillo obtenía el del par. Es un
  modo de fallo que no estaba en la lista —no es texto que falte, ni cifra
  cambiada, ni regla inventada: es **una operación hecha sobre el dato antes de
  guardarlo**— y solo se ve contrastando contra una fuente que conserve el
  «cada uno».

  **Los 5 compuestos son un límite del modelo, no defectos**, y se declaran en
  `COSTE_COMPUESTO` en vez de silenciarse: *Clon* y *Conocer las leyendas*
  tienen **dos materiales con precio distinto**, y *Crear muerto viviente*,
  *Proyección astral* y *Vínculo protector* tienen precio **por unidad**
  (por cadáver, por objetivo, por anillo). `coste` es un solo string y no puede
  representar ninguno de los dos casos. **Es el mismo límite que el campo
  `tirada`**, y otra cosa que la Fase 14 debería heredar resuelta.

  El contraste sube `verificar_foundry.py` de **2967 a 3012 valores**, con 4
  mutaciones nuevas en `mutaciones_foundry.py` (coste borrado, cifra cambiada,
  unidad cambiada, y coste ilegible no declarado).

  **Nota sobre el alcance real de este chequeo:** cubre los 309 conjuros que el
  SRD publica. *Golpe de viento acerado* —el que destapó todo— **no está en el
  SRD**, así que su corrección vino de la lectura y **el chequeo no lo protege**.
  De los 144 conjuros con material y `coste: null`, los que quedan fuera del SRD
  siguen sin fuente externa que los contraste.

- **🔬 Muestra aleatoria POST-corrección: el residuo medido (2026-08-29)** —
  la pregunta que ninguna medición anterior respondía. Todo lo medido hasta hoy
  decía cuánto error **había**; esto dice cuánto **queda**.

  **Método:** 36 conjuros elegidos con `random.seed(20260829)` —semilla fija,
  muestra **reproducible** y no elegible a dedo, guardada en
  `MUESTRA_POST.json`— auditados con el briefing completo (`LEEME_AGENTE_7.md`)
  por cuatro agentes que **no sabían que era una muestra de control**.

  ### El resultado: 4 defectos en 36 = 11,1 % (IC 95 % 3,1 % – 26,1 %)

  | Conjuro | Auditado en | Qué se le había escapado |
  |---|---|---|
  | *Terremoto* | oleada 4, **hoy**, con 3 correcciones ya aplicadas | los 50 de daño a estructuras **se repiten al final de cada turno**, no una sola vez (hasta ×10 de diferencia); y faltaba «si la supera, la criatura se moverá a la vez que se abre el borde de la grieta» |
  | *Antipatía/simpatía* | oleada 1 | admitía solo «criatura» donde la página dice «criatura **u objeto**», y calificaba el tipo como «**inteligente**», palabra que **no aparece en la página**: resto de 2014 |
  | *Golpe de viento acerado* | oleada 2 | `componentes.coste` en `null`; la página exige «un arma cuerpo a cuerpo que valga al menos **1 pp**» |
  | *Rociada venenosa* | oleada 4, **hoy** | «el **ojetivo**» (errata tipográfica, no regla falsa) |

  ### Lo que este número sí dice, y lo que no

  **NO dice que la tasa haya bajado.** El IC de la muestra (3,1-26,1 %) se
  solapa por completo con el de antes de corregir (15,7 %, IC 11,8-20,3 %). Con
  n=36 **no se distingue un 11 % de un 16 %**. Afirmar una mejora con estos
  datos sería exactamente el tipo de conclusión que este proyecto lleva un mes
  evitando.

  **SÍ dice, y es lo importante, que auditar un conjuro no lo deja limpio.**
  **Los cuatro defectos estaban en conjuros ya auditados** — los cuatro. Y dos
  de ellos habían pasado por la oleada 4 **ese mismo día**. *Terremoto* es el
  caso extremo: auditado, **tres correcciones aplicadas por la tarde**, y aún
  escondía dos reglas mal, una de ellas capaz de multiplicar por diez el daño a
  estructuras.

  ### La consecuencia para el criterio de parada

  **El objetivo no puede ser «texto sin errores»: tiene que ser «texto con un
  margen conocido».** Una segunda pasada sobre lo ya auditado sigue encontrando
  cosas, y una tercera probablemente también — con rendimientos decrecientes y
  sin punto de corte natural. Perseguir el cero con estas herramientas no
  converge.

  Lo que la base tiene, y casi ningún proyecto así tiene, es **la cifra**: un
  residuo del orden del 10 %, medido con intervalo, sobre texto ya corregido.
  Con eso se puede decidir; sin eso solo se puede suponer.

- **Los 7 «acción bonus»: el tipo de acción era correcto (2026-08-29)** —
  quedaba comprobar si la normalización del anglicismo había tapado un error de
  fondo: se corrigió la **palabra** («acción adicional»), no se había mirado si
  el **tipo de acción** era el del manual. **Lo era en los siete**: *Animar
  objetos*, *Caldero burbujeante de Tasha*, *Clarividencia*, *Crear muerto
  viviente*, *Orden imperiosa*, *Ralentizar* y *Sirviente invisible*. Cero
  correcciones; los siete llevan `_accion_verificada`.

  **Vale la pena anotar el resultado negativo**, no solo los hallazgos: la duda
  era razonable —el CSV ya había elegido mal en otros campos— y ahora está
  cerrada con la página delante en vez de por suposición.

- **La semántica de `tirada: "Directo"`, decidida y aplicada (2026-08-29)** —
  llevaba abierta desde la conversión del CSV. **Ya no lo está.**

  ### La definición, deducida de los datos

  > **`TdS <car.>`** — la tirada de salvación **decide si el conjuro afecta al
  > objetivo**. Es el disparador.
  > **`Directo`** — el conjuro **se manifiesta igualmente**. Puede haber
  > salvaciones después, pero **modulan el daño** o permiten librarse de un
  > estado ya aplicado; no evitan el conjuro.

  No se eligió a dedo. Dos indicios independientes la sostienen:

  - **Los conjuros gemelos coinciden.** *Inmovilizar persona*/*monstruo*,
    *Dominar persona*/*monstruo*, *Hechizar persona*/*monstruo* y
    *Sugestión*/*Sugestión en masa* dicen los ocho `TdS Sab.`;
    *Curar heridas*/*en masa* y *Muro de fuego*/*Muro de espinas* dicen
    `Directo`. Si el campo fuera ruido del CSV, los pares no coincidirían.
  - **Las dos poblaciones están separadas** por dónde aparece la primera
    salvación en el texto: **mediana del 24 % en los `TdS` frente al 48 % en
    los `Directo`**.

  ### Las 4 correcciones

  | Conjuro | Corrección | Cita |
  |---|---|---|
  | *Mal de ojo* | `Directo` → **`TdS Sab.`** | «deberá superar una tirada de salvación de Sabiduría **o** se verá afectada por uno de los efectos» |
  | *Levitar* | `Directo` → **`TdS Con.`** | «**no afecta** a una criatura no voluntaria que supere una tirada de salvación de Constitución» |
  | *Polimorfar verdadero* | `Directo` → **`TdS Sab.`** | «si la supera, **el conjuro no le afectará**» |
  | *Tormenta de la venganza* | `Directo` → **`TdS Con.`** | «**o** sufrirán 2d6 de trueno y quedarán ensordecidas» |

  Los otros 10 candidatos se **confirmaron correctos** leyendo la página, y los
  14 llevan ahora `_tirada_revisada` y `_tirada_semantica` con el veredicto y su
  razón.

  ### 🔬 El juicio NO se pudo automatizar, y se intentó dos veces

  **Primero por posición.** El umbral del primer tercio marcó 14 candidatos y la
  lectura dijo que **4 eran correctos** (*Castigo abrumador*, *Castigo furioso*,
  *Cono de frío*, *Esfera de llamas*: en los cuatro el daño ocurre igual y la
  salvación solo lo modula). Un 29 % de falsos positivos.

  **Después por estructura del texto** («o la mitad del daño» frente a «o
  quedará…»). Tampoco: falló en *Terremoto* y *Tormenta de la venganza*, que son
  **gramaticalmente idénticos y semánticamente opuestos**.

  Por eso el chequeo **avisa de lo no revisado en vez de decidir**: los registros
  verificados llevan `_tirada_revisada`, el aviso converge a cero según se leen
  las páginas —**hoy está en cero**— y vuelve a saltar con cualquier conjuro
  nuevo. Convertirlo en error duro habría obligado a declarar excepciones a mano
  en un tercio de los casos, que es peor que un aviso.

  ### ⚠️ Hallazgo de diseño: el campo `tirada` es un modelo insuficiente

  Dos conjuros no caben en él, y no por estar mal transcritos:

  - ***Símbolo*** tiene **seis modos** (Aturdimiento, Discordia, Dolor, Muerte,
    Sueño, Terror) con **salvaciones distintas**: cinco disparan un estado y
    «Muerte» modula el daño.
  - ***Muro prismático*** tiene **siete capas**: las 1-5 modulan daño, las 6-7
    disparan estados.

  **Un conjuro no tiene «una tirada»: tiene efectos, y cada efecto tiene la
  suya.** Los dos quedan como `Directo` —el conjuro se manifiesta sin tirada— con
  la limitación anotada en `_tirada_semantica`. **Es exactamente el problema que
  la Fase 14 viene a resolver**, y conviene que su modelo de efectos nazca
  sabiéndolo en vez de descubrirlo a mitad de camino.

  De paso, *Símbolo* trae una **discrepancia del propio libro**: su párrafo
  introductorio llama «miedo» al sexto modo, cuyo epígrafe real es «**Terror**».

- **Fase 13p — oleada 4 CERRADA: la lectura visual de los conjuros termina
  (2026-08-29)** — lotes B5-B9, **65 conjuros**, libro 323-343. **9 conjuros con
  defecto (13,8 %), 15 correcciones aplicadas, 0 hallazgos rechazados.**
  Verificados a ciegas por V9, V10 y V11, más dos relecturas directas de Opus
  mientras los agentes estuvieron caídos por un límite de API.

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Urna mágica* | **la mecánica estaba invertida**: «Tu cuerpo va al recipiente» → el cuerpo queda **catatónico** y es el **alma** la que entra. Y «no puedes hacer nada» → sí hay una acción. Faltaban la restricción a **humanoides**, el requisito de **verlos**, las dos protecciones nombradas (*círculo mágico*, *protección contra el bien y el mal*) y la destrucción final del recipiente | 5 + 7 + 3 | pdf 343-344 |
  | *Teletransporte* | el objeto «debe caber en un **cubo de 3 metros**» → «debe ser **Grande o más pequeño**». 2024 usa **categoría de tamaño**, no medidas | 2 (regla de 2014) | pdf 338 |
  | *Teletransporte* | «la **tabla de accidentes**» → «**Resultado del teletransporte**» | 5 | pdf 338 |
  | *Terremoto* | «Se abren 1d6 fisuras **por turno**» → **una sola vez**, «al final del turno en que lo lances». Multiplicaba el efecto por la duración | 4 | pdf 339 |
  | *Terremoto* | epígrafe «**Temblor**» → «**Estructuras**» | 5 | pdf 339 |
  | *Tormenta de la venganza* | faltaba que en los turnos 5-10 la zona queda «**muy oscura**» | 3 | pdf 341 |
  | *Shillelagh*, *Sugestión en masa* ×3, *Sirviente invisible* | ver el bloque del lote B7 | — | pdf 334-336 |
  | *Reencarnar*, *Resurrección* ×4 | ver el bloque del lote B6 | — | pdf 329, 331 |
  | *Terremoto*, *Tormenta de la venganza* | «**salvamento**» → «tirada de salvación» | anglicismo | — |

  ### 📊 La Fase 13p, cerrada y medida

  **48 conjuros con defecto de 305 auditados = 15,7 %** (las cuatro oleadas más
  la muestra aleatoria de la Fase 13o). IC 95 % exacto: **11,9 % – 20,2 %**.

  | Oleada | Conjuros | Con defecto | Tasa |
  |---|---|---|---|
  | 13o (muestra aleatoria) | 40 | 7 | 17,5 % |
  | 1 | 63 | 9 | 14,3 % |
  | 2 | 68 | 10 | 14,7 % |
  | 3 | 69 | 13 | 18,8 % |
  | 4 | 65 | 9 | 13,8 % |
  | **Total** | **305** | **48** | **15,7 %** |

  **La muestra aleatoria de la Fase 13o acertó.** Midió 17,5 % con IC 7,3–32,8 %
  sobre 40 conjuros, y el valor final sobre los 306 es 15,7 %. La decisión de
  **bloquear la Fase 14** sobre la base de esa muestra estaba bien tomada: de
  haber construido el motor de efectos sobre este texto, habría codificado
  **casi 50 reglas falsas con su cita de página al lado**.

  **Ninguna oleada bajó de forma clara.** 14,3 → 14,7 → 18,8 → 13,8 % es ruido
  alrededor del 15 %: el defecto estaba repartido por todo el capítulo, no
  concentrado en un tramo malo. Era una propiedad del CSV de origen, no un
  accidente de transcripción.

  **Lo que más ha aparecido no son cifras mal copiadas: son reglas que no
  existen.** El modo de fallo 7 (regla inventada) y el 3 (cláusula que falta) se
  reparten la mayoría de los casos graves — *Mente en blanco*, *Dominar
  monstruo*, *Creación*, *Resurrección*, *Sugestión en masa*, *Urna mágica*. Y
  todos comparten la misma propiedad: **el párrafo tenía la longitud correcta**.

  ### ⚠️ Salvedad: dos lotes limpios sin remuestrear

  **B5 (0 de 14)** salió sin un solo hallazgo. Por la regla de la casa —«un
  informe en blanco no prueba nada por sí solo»— **debería remuestrearse a mano
  antes de darlo por bueno**. Se deja anotado y sin hacer: es lo único de la
  Fase 13p que queda a medias.

- **Pasada de cabeceras: 16 correcciones en 302 conjuros (2026-08-29)** —
  lotes C1, C2, C3 y C4, **completa**. Encargo nuevo (`LEEME_CABECERAS.md`) que audita
  **solo `nombre` y `resumen`** de conjuros cuya descripción ya estaba auditada.
  Nació de dos deudas que destapó un inventario del estado real:

  1. **El `nombre` no había sido nunca campo auditable.** La lista de campos de
     todos los briefings anteriores era `descripcion | clases | tirada | resumen
     | material`. Y sin embargo la base llevaba **7 erratas de nombre corregidas,
     las 7 encontradas de rebote**.
  2. **El `resumen` estaba en el briefing pero nadie lo miraba.** Las oleadas 1-2
     declararon **0 defectos de resumen en 131 conjuros**; la oleada 3 midió
     **4 en 69 (5,8 %)**. P(0 en 131 con esa tasa) = **0,0004**, y el límite
     superior compatible con 0/131 es 2,26 %: **los intervalos no se solapan.**

  **El resultado confirma las dos sospechas.**

  | Conjuro | Campo | Corrección | Página |
  |---|---|---|---|
  | *Arma magica* → ***Arma mágica*** | nombre | **octava errata de nombre**: faltaba la tilde | pdf 247 |
  | *Cordón de flechas* | resumen | «4 flechas **mágicas**» → la página dice «flechas o virotes **NO mágicos**». Contradicción directa | pdf 267 |
  | *Castigo cegador* | resumen | «**Oscuridad** que ciega **y confunde**» → el daño es **radiante** y no hay confusión alguna | pdf 257 |
  | *Castigo desterrador* | resumen | «Exilio que **no deja retorno**» → el objetivo **reaparece donde estaba** al terminar | pdf 257 |
  | *Consagrar* | resumen | «queda bendecido» → el conjuro permite poder sagrado **o impío** | pdf 263 |
  | *Conjurar seres del bosque* | resumen | «Invocas **3 espiritus elementales**» → son **espíritus de la naturaleza**, la página **no da número**, y «espiritus» iba sin tilde | pdf 263 |
  | *Enmarañar* | resumen | «Apresas a **una** criatura» → es efecto de **área**, apresa a varias | pdf 279 |
  | *Palabra de regreso* | resumen | «Un regreso **impuesto**» → las criaturas son **voluntarias** | pdf 319 |
  | *Prohibición* | resumen | «**Nadie** cruza este umbral» → solo bloquea **viajes mágicos**; se puede entrar andando | pdf 324 |
  | *Explosion solar* → ***Explosión solar*** | nombre | **novena errata**: faltaba la tilde | pdf 284 |
  | *Inflingir heridas* → ***Infligir heridas*** | nombre | **décima errata**: «infli**n**gir» no existe — el verbo castellano es **infligir**. Llevaba mal el nombre desde la conversión del CSV | pdf 294 |
  | *Geas* | resumen | «Una orden que **no caduca**» → la duración son **30 días** | pdf 286 |
  | *Globo de invulnerabilidad* | resumen | «**Nada** puede tocarte» → solo bloquea conjuros de **nivel 5 o inferior** | pdf 286 |
  | *Jaula de fuerza* | resumen | «Nada entra, **nada sale**» → hay salida: teletransporte con salvación de Carisma | pdf 306 |
  | *Laberinto* | resumen | «Los muros **cambian según tu voluntad**» → no está en la página; el semiplano es fijo | pdf 306 |
  | *Localizar criatura* | resumen | «La presa **siempre** aparece» → falla a más de 300 m, con plomo de por medio o si cambia de forma | pdf 307 |

  **13 de las 16 correcciones son de `resumen`: una tasa del 4,3 % (13/302) en un
  campo que se daba por limpio** — y consistente con el 5,8 % que midió la
  oleada 3. Frente al **0 % que declararon las oleadas 1-2**, queda confirmado
  que aquellos informes no abrieron el campo. Y ninguna es un matiz de estilo — todas dicen algo que la
  página contradice: un número que no existe, un tipo de daño equivocado, una
  permanencia que el conjuro no tiene, un «nadie» donde el manual dice «ningún
  viaje mágico».

  **El patrón del campo `resumen` ya está claro: falla por generalizar.** Casi
  todos los defectos son el resumen diciendo **más** de lo que el conjuro hace —
  «nadie», «no deja retorno», «mágicas», «impuesto»—, o poniendo una cifra que la
  página no da. Es prosa escrita de memoria a partir del título, no del texto.

  **En 302 cabeceras aparecieron 3 erratas de nombre** (1,0 %), que sube el total
  histórico a **11**. La peor es ***Inflingir heridas* → *Infligir heridas***:
  «inflingir» no es una palabra —el verbo es *infligir*— y el error llevaba ahí
  desde la conversión del CSV, **sobreviviendo a una auditoría de su descripción
  y a una corrección de su campo `tirada` hechas hoy mismo**. Nadie miraba el
  nombre, así que nadie lo veía, aunque estuviera en la primera línea del
  registro que se estaba corrigiendo.

  Esa superficie está mucho mejor de lo que sugerían las 7 erratas anteriores
  —1 de cada 100, no 1 de cada 50— pero **hubo que mirarla para saberlo**, que es
  justo lo que no se había hecho nunca.

- **Fase 13p — oleada 4, lote B7: 5 correcciones, y un anglicismo que estaba en
  6 conjuros más (2026-08-29)** — 12 conjuros, libro 330-334. Los 5 hallazgos
  verificados a ciegas por V9: **los 5 confirmados, 0 rechazados**.

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Shillelagh* | el párrafo de mejora se titulaba «Con un espacio de conjuro de nivel superior»; el manual dice **«Mejora de truco»**. **Es un truco: no tiene espacios de conjuro que gastar**, así que la etiqueta describía una mecánica imposible | 5 | pdf 334 |
  | *Sugestión en masa* | faltaba el límite **«(de no más de 25 palabras)»** de la sugerencia | 3 | pdf 336 |
  | *Sugestión en masa* | sobraba «Criaturas inmunes a hechizos no se ven afectadas» — **ausente por completo de la página** | 7 (regla inventada) | pdf 336 |
  | *Sugestión en masa* | sobraba «Puedes especificar condiciones para tareas especiales durante la duración» — **ausente por completo** | 7 | pdf 336 |
  | *Sirviente invisible* | «como **acción bonus**» → «como **acción adicional**» | anglicismo | pdf 335 |

  ***Shillelagh* es el mejor argumento a favor de auditar los epígrafes.** No es
  un dato numérico ni una regla inventada: es una **etiqueta** que promete algo
  estructuralmente imposible —escalar un truco con espacios de conjuro— y que
  nadie leería con desconfianza porque esa frase aparece, correctamente, en
  cientos de conjuros de la base.

  **Y el anglicismo no estaba solo.** Al añadir «acción bonus» al detector de
  inglés crudo aparecieron **6 conjuros más** con el mismo defecto: *Orden
  imperiosa*, *Clarividencia*, *Ralentizar*, *Animar objetos*, *Caldero
  burbujeante de Tasha* y *Crear muerto viviente*. Los 7 normalizados a «acción
  adicional», que es el término del manual.

  ⚠ **Lo que esta normalización NO hace, y conviene no olvidarlo:** corrige la
  **palabra**, no comprueba que el **tipo de acción** sea el correcto. Si la
  conversión del CSV eligió mal entre «acción» y «acción adicional» en alguno de
  los 7, el texto ahora está en buen castellano y sigue diciendo una regla falsa.
  **Los 7 quedan pendientes de una lectura que confirme el tipo de acción**, y
  ese campo no lo cubre ningún script: `tiempo_lanzamiento` sí está contrastado,
  pero las acciones que aparecen **dentro** de la descripción no.

  **La primera lista de inglés crudo no cazaba «acción bonus»** porque solo
  buscaba términos ingleses aislados y en mayúscula (*Dash*, *Dodge*). Media
  expresión traducida a medias se le escapaba entera. Es la tercera vez hoy que
  un detector solo ve la forma exacta del defecto que lo inspiró.

- **Fase 13p — oleada 4, lote B6 + dos hallazgos del chequeo nuevo:
  6 correcciones (2026-08-29)** — 13 conjuros, libro 327-329. Los verificadores
  Sonnet estaban caídos por un límite de API, así que **la relectura la hizo
  Opus sobre la página**, que es la regla original del proyecto: delegar en
  Sonnet era una optimización de coste, no un requisito de corrección.

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Reencarnar* | tabla 1d10 con **dos parejas invertidas**: la base decía 3 Enano / 4 Elfo / 7 Mediano / 8 Humano; el manual imprime **3 Elfo / 4 Enano / 7 Humano / 8 Mediano** | 5 (nombres de tabla) | pdf 329 |
  | *Resurreción* → ***Resurrección*** | errata en el nombre: faltaba una «c». Corregido con `alias` | errata de nombre | pdf 331 |
  | *Resurrección* | inventaba **dos reglas**: «si el alma es libre y voluntaria» y la distinción entre enfermedades normales y mágicas. **La página solo dice que neutraliza «cualquier veneno»** | 7 (regla inventada) | pdf 331 |
  | *Resurrección* | «-4 a **tiradas de ataque, salvaciones y pruebas de característica**» → «-4 a las **pruebas con d20**». 2024 unificó las tres en una sola | 2 (regla de 2014) | pdf 331 |
  | *Resurrección* | `tirada` «TdS Sab.» → «Directo»: **la página no pide ninguna tirada de salvación** | otro | pdf 331 |
  | *Atadura planar* | «debe superar una **prueba** de Carisma» → «**tirada de salvación** de Carisma». Además faltaban el «círculo mágico **invertido**» y la cláusula de qué pasa si estás en otro plano | 5 + 3 | pdf 248 |
  | *Tsunami* | «**salvamento** de Fuerza» ×2 → «tirada de salvación»; «una vez por **turno**» → «por **asalto**»; y faltaba que el muro se aleja «**junto con todas las criaturas que haya en su interior**» | 5 + 3 | pdf 343 |

  ***Resurrección* es el registro más dañado que ha aparecido en toda la Fase
  13p:** cuatro defectos en un solo conjuro, uno de ellos en el nombre y otro en
  un campo (`tirada`) que contradecía a la propia página. Y los tres modos de
  fallo que acumula son distintos entre sí — regla inventada, regla de 2014, y
  campo sin respaldo en el texto.

  **`Atadura planar` estrena un modo de fallo que conviene nombrar: prueba de
  característica donde el manual pide salvación.** No son lo mismo —una prueba
  usa el bonificador de competencia si aplica, una salvación no— y la frase
  suena igual de natural en los dos sentidos. Es el mismo tipo de error que
  *Geas*: fluido, plausible, y solo la página lo distingue.

- **`validar_tirada()` tenía un hueco, y lo encontró una relectura, no el
  chequeo (2026-08-29)** — la primera versión comparaba la característica
  declarada contra las salvaciones **mencionadas en la descripción**, así que
  cuando el texto **no mencionaba ninguna**, pasaba de largo. Es justo el caso de
  *Resurrección*.

  Ampliado: si `tirada` declara una salvación y la descripción no menciona
  **ninguna**, es error. Hizo falta una detección **laxa** para no dar falsos
  positivos, porque la base condensa a veces «tirada de salvación de X» en
  «tirada de X». Y de paso destapó **`salvamento`** (*Tsunami*), término que no
  es del manual y que ahora sale como aviso propio: delata texto nunca leído
  contra la página. Mutaciones: **23/23**, con el caso nuevo y su control
  negativo.

  **La lección se repite: el chequeo que escribes sin haber visto el defecto no
  cubre el defecto.** `validar_tirada()` nació de *Inflingir heridas* —campo que
  contradice al texto— y por eso solo sabía mirar contradicciones. El caso
  contrario, un campo que **no tiene con qué contradecirse**, hubo que verlo en
  una página para que se le ocurriera a nadie.

- **Tres chequeos de integridad textual nuevos, y 5 defectos que encontraron el
  primer día (2026-08-29)** — `validar_tirada()`, `validar_vecindad()` y
  `validar_ortografia()` en `validar.py`, probados por mutación en
  `_verificacion/mutaciones_integridad.py` → **21/21**, la mitad controles
  negativos. Ninguno necesita el manual.

  | Chequeo | Qué vigila | Encontró al ejecutarse |
  |---|---|---|
  | `tirada` | vocabulario cerrado **y** concordancia con la propia `descripcion` | las 5 erratas de formato ya corregidas; 53 `Directo` como aviso |
  | `vecindad` | `resumen` idéntico entre conjuros de la misma página (error) y solapamiento alto (aviso) | ***Curar heridas en masa*** **y** ***Curar en masa*** **con el mismo resumen** |
  | `ortografía` | inglés sin traducir y palabras pegadas | ***Hacer añicos*** **y** ***Estática sináptica***: «tirada **desalvación**» |

  **Correcciones aplicadas a partir de ellos:**

  | Conjuro | Corrección | Página |
  |---|---|---|
  | *Curar heridas en masa* | `resumen` «La sanación alcanza a todos» → «Una ola cura a seis a la vez». Lo llevaban **los dos** conjuros | pdf 269 |
  | *Curar en masa* | `resumen` → «700 puntos repartidos a tu antojo». Verificado por V8: nivel 9, sin esfera ni tope de criaturas, sin párrafo de mejora | pdf 269 |
  | *Hacer añicos* | «tirada **desalvación** de Constitución» → «tirada **de salvación**» | — |
  | *Estática sináptica* | «tirada **desalvación** de Inteligencia» → «tirada **de salvación**» | — |

  **El caso de `Curar…en masa` es el quinto de contaminación por vecindad**, y
  el primero que encuentra un script en vez de un agente. El resumen era tan
  genérico que **servía por igual a los dos conjuros** — que es exactamente por
  qué nadie lo había visto: no era falso de un modo visible, era **vacío**.

  **La prueba por mutación se ganó el sueldo dos veces.** Salió 18/21 a la
  primera. Dos fallos eran de las mutaciones (usaban conjuros de páginas
  distintas para probar un chequeo que solo compara vecinos: **la mutación
  estaba mal, no el chequeo**) y **uno era real**: la partición de palabras
  empezaba en la letra 3 y no veía «elconjuro». Al bajarla a 2 aparecieron
  **las dos «desalvación» reales** — un defecto que el chequeo no habría
  encontrado nunca sin su propia prueba.

  **Y confirmó el riesgo que estos chequeos tienen de verdad: el falso
  positivo.** La primera versión de `validar_vecindad()` daba **15 falsos
  positivos** porque el manual repite texto de verdad entre conjuros hermanos
  (*Dominar persona*/*Dominar monstruo* comparten párrafos **porque así están
  impresos**). Ninguna medida de solapamiento distingue «el manual repite» de
  «el CSV calcó» sin abrir la página, así que **el chequeo se rediseñó para
  priorizar lectura, no para decidir**: el solapamiento es aviso ordenado por
  gravedad, y lo único que es error duro es el resumen idéntico.

- **Campo `fidelidad` declarado en toda la base (2026-08-29)** — cerrada la
  **única debilidad del FODA que seguía viva** desde el 2026-08-19. 26 ficheros
  YAML con `fidelidad` a nivel de fichero (`condensado` para dotes, subclases,
  especies y las 81 descripciones de equipo; `estructurado` para las tablas y
  listas que no son prosa), más `_meta.fidelidad` en `hechizos.json`.

  **`hechizos.json` se declara `mixto`, y esa es la parte honesta.** Se intentó
  clasificarlo registro a registro con marcadores automáticos (viñetas, `TdS`,
  `PG`, `VD`, `mod.`) y **no es fiable**: el marcador más frecuente resultó ser
  la conversión «N m / M pies» —175 de 188 casos—, que no es condensación sino
  **añadido editorial**. Declararlo `mixto` con la explicación de por qué vale
  más que una clasificación inventada que se sostendría sola hasta que alguien
  la comprobara. Si algún día hace falta por registro, es trabajo de criterio,
  no de regex.

  De paso, `_meta` lleva ahora una `_conversiones_nota` que dice sin rodeos que
  las equivalencias imperiales **no son texto del manual**, con las seis páginas
  que lo demuestran. Mientras la decisión siga abierta, al menos el fichero ya
  no las presenta como cita.

- **`FODA.md` reescrito; el viejo archivado como
  `FODA_2026-08-19_OBSOLETO.md` (2026-08-29)** — el anterior describía una base
  de hacía diez días: daba por abiertos los 155 rasgos de clase y el bug
  `Clerigo`, **ambos cerrados**, y su «Conclusión operativa» mandaba ejecutar
  las Fases 9c y 10, **ambas hechas**. `CONTINUAR.md` remitía a él para diseñar
  la Fase 8, así que **quien le hiciera caso trabajaría una semana hacia atrás**:
  era una trampa activa, no un documento envejecido. Se conserva con una
  cabecera que enumera qué quedó desfasado y por qué.

- **Fase 13p — oleada 3, lote B4: 5 correcciones aplicadas (2026-08-29)** —
  15 conjuros, libro 319-322. Verificados a ciegas por V7 (releyó pdf 322-324 sin
  ver el informe del auditor): **los 4 hallazgos confirmados, 0 rechazados**, y el
  verificador encontró **uno más que el auditor no vio**.

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Poliformar verdadero* → ***Polimorfar verdadero*** | **errata en el nombre**: el manual imprime «Poli**m**orfar», con m. Lo mismo en *Poliformar* (nivel 4) → ***Polimorfar***. Corregido con `alias` al nombre viejo, como las tres erratas de nombre de la Fase 13m | errata de nombre | pdf 322 |
  | *Polimorfar verdadero* | decía que el objetivo «**asume los puntos de golpe de la forma**» y que el conjuro termina «hasta **0 puntos de golpe**». La página dice que **mantiene sus propios pg** y obtiene además **pg temporales** iguales a los de la nueva forma. **La regla de los 0 pg es de *Polimorfar* (nivel 4), impreso en la misma página** | 1 (texto de otro conjuro) | pdf 322 |
  | *Polimorfar verdadero* | objeto convertido en criatura: «actúa **en tus turnos**» → «**sus turnos van inmediatamente después de los tuyos**». Tiene turno propio | 5 | pdf 322 |
  | *Prohibición* | «4000 m² **/ 13000 pies²** hasta 9 m **/ 30 pies**» → «4000 m² hasta una altura de 9 m». La página **no imprime pies** | 4 | pdf 324 |
  | *Presciencia* | `resumen` «**Imponer presencia**» → «Ver el futuro inmediato». Era el resumen del conjuro **vecino de la misma página**, *Presencia regia de Yolande* | 1 (texto de otro conjuro) | pdf 323 |

  **El modo de fallo 1 aparece dos veces en un solo lote, y las dos por vecindad
  de página.** *Polimorfar verdadero* se contaminó de *Polimorfar*, impreso al
  lado; *Presciencia* se contaminó de *Presencia regia de Yolande*, impreso al
  lado. Es exactamente lo que ya pasó con *Aura sagrada* y *Aura mágica de
  Nystul* en la Fase 13o. **La contaminación por proximidad tipográfica no es
  una casualidad: es el modo de fallo estructural del CSV de origen**, y sugiere
  un chequeo dirigido — comparar cada par de conjuros consecutivos por página en
  busca de solapamiento anómalo de texto.

  **La errata la encontró el verificador, no el auditor.** El auditor transcribió
  el nombre de la base sin notar que el manual lo escribe distinto; el
  verificador, que leía la página a ciegas, lo señaló de oficio. **Es un
  argumento a favor de pedir siempre la transcripción de la cabecera completa**,
  no solo del campo en disputa.

  **Y el auditor razonó donde debía leer.** Dedujo que «13000 pies²» era falso
  **por aritmética y por comparación con el SRD inglés**, no por leer la página.
  Acertó, pero por el método equivocado: el briefing de V7 le prohibió
  expresamente razonar así y le pidió transcribir qué unidades están impresas.
  **Un acierto por el método equivocado es indistinguible de un acierto por
  casualidad, y no se puede aplicar sin releer.**

- **Fase 13p — oleada 3, lote B1: 3 correcciones aplicadas (2026-08-29)** —
  14 conjuros, libro 305-310. Verificados a ciegas por V6 (releyó pdf 309, 312 y
  313 sin ver el informe del auditor): **los 3 confirmados, 0 rechazados**.

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Mente en blanco* | decía inmunidad «a **conjuros de adivinación**» —categoría que **la página no nombra en ningún punto**— y **omitía entera** la cláusula «ningún conjuro (ni siquiera *deseo*) puede conseguir información sobre el objetivo, **observarlo desde lejos** o controlar su mente». Párrafo reescrito con el texto de la página | 7 + 3 | pdf 313 |
  | *Mensajero animal* | «**40 km / 25 millas** por 24 h, **80 km / 50 millas** volando» → «aproximadamente **37,5 km** cada 24 horas, o **75 km** si puede volar». La página no da millas | 4 | pdf 312 |
  | *Mal de ojo* | las tres opciones se llamaban «Dormido», «En pánico» y «Enfermizo»; la página las llama **«Sueño»**, **«Pánico»** y **«Náuseas»**. De paso: «acción **Dash**» era inglés sin traducir («la acción de **correr**») y «Miedo» no es el nombre del estado (**asustado**) | 5 | pdf 309 |

  ***Mente en blanco* es el peor de este lote y estrena una variante del modo 7.**
  No es solo una regla inventada: la base **concedía de más** (inmunidad a toda
  una escuela que el manual nunca menciona) y a la vez **callaba** la protección
  concreta que el manual sí impone (observación remota). Las dos mitades del
  error empujan en direcciones opuestas, así que ninguna revisión «por longitud
  de texto» lo habría visto: el párrafo tenía el tamaño correcto.

  ***Mal de ojo* aporta un modo barato de detección que no necesita el manual:
  inglés sin traducir.** «acción Dash» es un resto del CSV de origen. Un `grep`
  de términos ingleses habituales (*Dash*, *Dodge*, *Disengage*, *Hide*, *Ready*)
  sobre las descripciones costaría un minuto y señala texto que nunca se leyó
  contra la página.

  **Nota de cita, no corregida:** *Mente en blanco* lleva
  `fuente.pagina_libro: "310"`, pero su cabecera está en libro 310 y **todo el
  párrafo de efecto está en libro 311**. Por el criterio fijado —la cita apunta a
  donde está la **mecánica**— debería ser 311. No se ha tocado porque en
  `hechizos.json` la convención de facto es citar donde **empieza** el conjuro, y
  cambiar un solo registro crearía una inconsistencia peor que la que arregla.
  **Es una decisión de criterio pendiente para todo el fichero**, no un defecto
  suelto. Relacionado: el asterisco de valores como `"310*"` o `"316*"` lo copia
  `_convertir_hechizos.py` tal cual desde la columna `page` del CSV y **no tiene
  semántica definida en ningún punto de la base**.

- **Fase 13p — oleada 3 (parcial): 7 correcciones aplicadas (2026-08-29)** —
  lotes **B0, B2 y B3** (40 conjuros, libro 294-318). Los lotes **B1 y B4** se
  habían lanzado el 27 pero nunca llegaron a escribir informe; se relanzaron el
  29 y se registran aparte. Los 7 hallazgos pasaron por **segunda lectura ciega**
  (verificadores V3 y V4, sin ver los informes de los auditores, contestando
  preguntas cerradas): **los 7 coincidieron, 0 rechazados.**

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Inflingir heridas* | `tirada` «TdS **Sab.**» → «TdS **Con.**»; la propia descripción de la base ya decía Constitución. El campo contradecía a su propio texto | otro | pdf 296 |
  | *Impacto certero* | `resumen` «El golpe **no falla**» → «Tu aptitud mágica guía el golpe». La página **no concede acierto automático ni ventaja**: solo cambia la característica de ataque y daño | 7 (regla inventada) | pdf 296 |
  | *Muro de espinas* | el segundo golpe decía «recibiendo **el mismo daño**» (perforante) → «7d8 de daño **cortante**». La página distingue dos tipos y lo confirma su propio escalado: «**los dos tipos de daño** aumentan en 1d8» | otro | pdf 313 |
  | *Jaula de fuerza* | «viaje **intra**planar» → «viaje **inter**planar», y la frase se ajustó a la de la página («si intenta usar el teletransporte o el viaje interplanar para huir, primero deberá hacer una tirada de salvación de Carisma») | 5 | pdf 306 |
  | *Jaula de fuerza* | barrotes de «1,3 cm / ½ pulgada separados 1,3 cm» → «**1,25 cm** de diámetro separados **1,25 cm** entre sí» (la página no da la conversión) | 4 | pdf 306 |
  | *Muro de fuerza* | `resumen` «Nada puede atravesarlo **ni romperlo**» → «Nada lo atraviesa; **solo desintegrar lo destruye**». La `descripcion` sí recogía la excepción; el resumen la tapaba | otro | pdf 314 |
  | *Palabra de poder: aturdir* | `resumen` «Una sílaba que **paraliza**» → «que **aturde**». La página nunca dice «paralizado»; aturdido y paralizado son **dos estados distintos** del manual | 5 | pdf 318 |

  **Tres de los siete son `resumen`, y es un dato nuevo.** Hasta ahora el campo
  `resumen` no se había auditado como superficie propia: es prosa de sabor que
  nadie consume. Pero los tres casos **contradicen a la `descripcion` correcta
  que llevan al lado** — el resumen afirma un acierto automático que no existe,
  niega una excepción que la página nombra, y renombra el estado aplicado. **Un
  resumen falso es una regla falsa en el sitio donde más probable es que alguien
  se pare a leer.** Conviene tratarlo como campo auditable, no decorativo.

  *Inflingir heridas* aporta otro modo barato de detección: **el campo `tirada`
  contradecía a la descripción del mismo registro.** Eso no necesita leer el
  manual — es un contraste interno automatizable con una regex sobre la propia
  descripción, y coincide con la decisión pendiente sobre «Directo».

- **Fase 13p — `Disco flotante de Tenser`: la conversión no la trae la página
  (2026-08-29)** — cerrada la última duda de la tabla de conversiones de
  `ESTADO_13p.md`. El verificador V5 releyó pdf 273 (= libro 271) y transcribió
  el conjuro entero: la página **solo usa unidades métricas** (90 cm de diámetro,
  2,5 cm de grosor, flota 90 cm sobre el suelo) y **no da ninguna equivalencia en
  pies ni pulgadas** — tampoco en los otros tres conjuros de esa página. Se
  eliminaron por tanto las seis conversiones que la base añadía en su
  `descripcion`, con el mismo criterio que ya se aplicó a *Nube de dagas*. De
  paso se corrigió la errata «si te alejas a más de 6 m **pies** de él».

  **Deja abierta una pregunta mayor, anotada en `ESTADO_13p.md`:** si el manual
  castellano nunca imprime equivalencias en pies, entonces las ~560 conversiones
  que `validar_conversiones()` valida en las descripciones **son todas añadidas
  por la base**. Aritméticamente correctas, pero editoriales — y `hechizos.json`
  se declara transcripción **literal**. Es una decisión de producto, no una
  corrección: no se ha tocado nada más.

- **Fase 13p — vocabulario sucio del campo `tirada`, 5 registros (2026-08-29)** —
  al ir a corregir *Inflingir heridas* se contó el vocabulario del campo y salieron
  **15 valores distintos para 6 tiradas posibles**. Cinco eran erratas de formato
  del mismo valor, normalizadas sin cambiar contenido (los seis textos se habían
  leído ya en la página): `TdS Fue,` → `TdS Fue.` (*Muro de viento*), `TdS Des` →
  `TdS Des.` (*Golpe flamígero*), `TdS Dest.` → `TdS Des.` (*Conjurar descarga de
  proyectiles*), `TdS Fuerza` → `TdS Fue.` (*Golpe apresador*), `D20+ata.conj,` →
  `D20+ata.conj.` (*Agarre electrizante*).

  Se conserva **`TdS Int. propia`** (*Contactar con otro plano*) sin normalizar:
  ahí la salvación **la hace el lanzador**, no el objetivo, y «propia» codifica
  esa diferencia real. Es una excepción, no una errata.

  **Es el mismo modo de fallo que `3d0` y que las listas de `clases` cortas:**
  un valor con la forma correcta que ningún chequeo mira. `tirada` no tiene
  vocabulario cerrado y **ningún script lo consume todavía**, así que las cinco
  erratas llevaban ahí desde la conversión del CSV sin que nada las viera.
  **Pendiente: cerrar el vocabulario en `validar.py`**, con su prueba por
  mutación y la excepción de arriba como control negativo.

- **Fase 13p — oleada 2: 10 correcciones aplicadas (2026-08-27)** — lotes A5-A9,
  **68 conjuros**, libro 268-293. Cinco agentes auditores, y por primera vez
  **una segunda lectura ciega**: dos verificadores independientes releyeron las
  páginas de los hallazgos **sin ver los informes de los auditores**, contestando
  preguntas cerradas. **Los 10 coincidieron.** Es el método que sustituye a la
  relectura personal (ver `ESTADO_13p.md`, «Cómo se verifica un hallazgo»).

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Geas* | «**falla** automáticamente si no entiende la orden» → «**la superará** automáticamente». La regla estaba **invertida** | otro | pdf 288 |
  | *Dominar monstruo* | sobraba «Con tu acción, controlas totalmente sus acciones hasta el final de tu siguiente turno» — **la página no concede eso**: solo permite ordenarle usar su reacción gastando la tuya | 7 (regla inventada) | pdf 276 |
  | *Fuerza fantasmal* | «inflige 2d8 psíquico **a objetivos en su área**» → «**al objetivo** si está en el área que ocupa el fantasma o a 1,5 m de él». Convertía un conjuro de objetivo único en uno de área | 4 | pdf 287 |
  | *De la carne a la piedra* | estado «restringido» → «**apresado**» (×2) y «Las **construcciones** resisten» → «Los **autómatas** superan la salvación» | 5 | pdf 270 |
  | *Detectar pensamientos* | «Inteligencia (**Arcana**)» → «Inteligencia (**Conocimiento arcano**)» | 2 (regla de 2014) | pdf 273 |
  | *Hablar con los muertos* | faltaba «y no se siente obligado a darte una respuesta verdadera si eres hostil con él o te reconoce como un enemigo» | 3 | pdf 291 |
  | *Excursión etérea* | «gastando un **pie** adicional por cada **pie**» → «**1 m** adicional por cada **metro**»: la página es métrica | 6 | pdf 284 |
  | *Elementalismo* | «**20 cl** de agua» → «**una taza** de agua limpia»: la cifra era inventada | 4 | pdf 277 |
  | *Engañar* | `clases` → «(bardo, brujo, mago)» | 8 | pdf 278 |
  | *Potenciar característica* | `clases`: sobraba **Paladín**; la cabecera dice «(bardo, clérigo, druida, explorador, hechicero, mago)» | 8 | pdf 323 |

  **`Geas` es el peor de la tanda.** No falta ni sobra texto: la regla dice lo
  contrario de lo que dice el manual. Un conjuro de nivel 5 cuyo objetivo
  *fallaba* la salvación justo cuando el manual dice que la *supera*. Es el modo
  de fallo más difícil de ver leyendo por encima, porque la frase es fluida y
  plausible en las dos direcciones.

  **`Dominar monstruo` confirma el modo de fallo 7** que estrenó *Creación* en
  la oleada 1: una regla escrita que el manual no contiene. Aquí concedía al
  lanzador un control total del objetivo que la página no da — en un conjuro de
  nivel 8, es una diferencia de poder enorme.

  **Los dos hallazgos de `clases` validan el módulo nuevo.** *Engañar* lo
  encontraron **el agente y el script el mismo día, por separado**;
  *Potenciar característica* lo encontró solo el script. Ver el bloque del
  módulo `conjuros-clases` más abajo.

  ### Tasa acumulada de la Fase 13p

  **19 defectos en 131 conjuros auditados = 14,5 %** (oleadas 1 y 2). La muestra
  aleatoria de la Fase 13o había medido 17,5 % con IC 95 % 7,3 %–32,8 %: **la
  medición se sostiene y no era un artefacto de la muestra**. Quedan 135
  conjuros por auditar en las oleadas 3 y 4.

- **Fase 13p — el chequeo de conversiones de unidad, y las 9 que eran falsas
  (2026-08-27)** — la lista de conversiones sospechosas que `ESTADO_13p.md`
  arrastraba desde el 22 estaba **incompleta**: decía 6 y son **9**. Faltaban
  las de km→pies, que el barrido a mano de entonces no cubría. Un agente leyó
  las 8 páginas implicadas y el veredicto fue unánime: **en los 8 casos el
  manual da la medida solo en unidades métricas y la conversión la añadió la
  base.**

  | Conjuro | Decía | Ahora | Página |
  |---|---|---|---|
  | *Detectar magia* | «30 cm / 11 pulgadas» y «2,5 cm / 0,9 pulgada» | «30 cm / **1 pie**» y «2,5 cm / **1 pulgada**» | pdf 272 |
  | *Disco flotante de Tenser* | «90 cm / 1 pie» (×2) | «90 cm / **3 pies**» | pdf 273 |
  | *Localizar criatura* | «**3 m** / 9 pies» | «**9 m** / 30 pies» | pdf 307 |
  | *Esfera congelante de Otiluke* | «12 m / 39 pies» | «12 m / **40 pies**» | pdf 281 |
  | *Pasamuros* | «1,5 m / 45 pies» | «1,5 m / **5 pies**» | pdf 319 |
  | *Telaraña* | «1,5 m / 20 pies» | «1,5 m / **5 pies**» | pdf 337 |
  | *Recluir* | «1,5 km / 4921 pies» | «1,5 km / **5.000 pies**» | pdf 328 |
  | *Ráfaga de viento* | «2 m / 7,5 pies» | «**2 m**», sin conversión | pdf 326 |
  | *Nube de dagas* | «cubo de 1,5 m / 10 pies» | «cubo de **1,5 m**» | pdf 316 |

  **`Localizar criatura` no era un problema de conversión, sino de contenido:**
  la página dice **9 m** y la base decía 3 m. El «9» de los metros había acabado
  en el campo de los pies y el de metros quedó inventado. Lo delató la
  aritmética, no la lectura.

  *Ráfaga de viento* es el único donde no se puso cifra: 2 m no tiene
  equivalente redondo en la cuadrícula (6,67 pies), y **inventar un redondeo
  sería repetir el defecto que se está corrigiendo**.

  **Decisión de diseño que queda anotada, no resuelta:** el manual castellano es
  métrico y, por lo que se ha visto, **no trae conversiones a pies en ninguno de
  estos puntos**. Las 562 equivalencias de la base son una ayuda propia, no una
  cita. Aquí se han corregido las falsas y se ha conservado la convención,
  porque quitarlas solo en 9 sitios dejaría un formato mixto peor que el
  problema. **Si algún día se decide que la base no debe contener datos sin
  página, hay que quitarlas todas o marcarlas como añadido nuestro.**

  **Chequeo nuevo: `validar_conversiones()`**, 562 equivalencias barridas. Dos
  cosas que costó descubrir y conviene no reaprender:

  - **El factor es el de juego (5 pies = 1,5 m), no el físico (3,28084).**
    Medido sobre las 548 conversiones a pies: el de juego deja 539 exactas, el
    físico solo 313. Elegir mal el factor no da un chequeo estricto: da
    cientos de falsos positivos.
  - **La tolerancia tiene que ser absoluta, no relativa.** La primera versión
    usaba un 2 % y hacía justo lo contrario de lo que debía: dejaba pasar
    «30 m / 98 pies» (error de 2 pies) y saltaba con «0,9 mi» (redondeo de
    0,03). Medido sobre la base ya corregida, los redondeos legítimos se
    desvían como mucho **0,032** y el menor defecto real **1 entero**: media
    unidad separa las dos poblaciones con holgura.

  **La base mezcla tres notaciones decimales** en datos correctos —«1,5»,
  «0.9» y «1’5» con apóstrofe tipográfico— además del punto de millar
  («5.000 pies»). La primera versión del chequeo dio **cinco falsos positivos**
  y los cinco eran del parser de números, no de la aritmética. Probado por
  mutación en `_verificacion/mutaciones_conversiones.py`: **13/13, con 7
  controles negativos** — más de la mitad, porque el riesgo real de este
  chequeo era el falso positivo.

- **Fase 13p — módulo `conjuros-clases`: el campo que nadie contrastaba
  (2026-08-27)** — nació del defecto de *Clarividencia* (ver oleada 1). El
  campo `clases` de los conjuros **no lo miraba ningún chequeo**: el contraste
  externo no lo cubría y el cruce interno `hechizos ⊆ clases` solo detecta
  nombres de clase inexistentes, no listas incompletas.

  **La fuente es el SRD 5.2 en Markdown (`_verificacion/srd52/spells.md`)**, no
  los packs de Foundry: Foundry no publica la lista de clases dentro del
  registro del conjuro. Es el mismo SRD y la misma edición, así que no entra
  una fuente nueva.

  **No traduce, deduce**, como el resto de `verificar_foundry.py`: empareja
  cada clase castellana con la inglesa cuyo **conjunto de conjuros** más se le
  parece, y exige biyección. El margen mide la fiabilidad del método y es
  amplio: **la peor pareja correcta da J=0,974 y la mejor pareja falsa 0,588.**

  **278 conjuros contrastados, 2 discrepancias** — y una de ellas, *Engañar*,
  la había encontrado un agente por su cuenta leyendo pdf 278 el mismo día
  (`["Bardo","Explorador","Hechicero","Mago"]` donde la cabecera dice «(bardo,
  brujo, mago)»). **Dos métodos independientes, el mismo hallazgo**, que es la
  señal más fuerte de que algo está realmente roto. Aplicada.

- **Fase 13p — oleada 1: 10 correcciones aplicadas (2026-08-27)** — los cinco
  informes de la oleada 1 (lotes A0-A4, **63 conjuros**, libro 239-267) quedaron
  escritos el 22 sin recoger. Se recogieron releyendo personalmente en la página
  cada hallazgo con `pdftoppm -r 170` (pdf 242, 244, 245, 246, 248, 259, 267,
  268). **Los 9 hallazgos de agente se confirmaron: ninguno fue rechazado.**

  | Conjuro | Corrección | Modo de fallo | Página |
  |---|---|---|---|
  | *Aliado planar* | la escala de pago era «depende de la duración y el peligro»; se transcriben las **tres cifras reales** (100 po/minuto, 1000 po/hora, 10 000 po/día hasta 10 días) más las rebajas por sintonía y por ausencia de peligro | 3 (párrafo que falta) | pdf 242 |
  | *Animar objetos* | faltaban las **tres restricciones** de qué se puede animar (nada que nadie vista o lleve, nada fijo a una superficie, nada Gargantuesco) y el **límite de 150 m** para dar órdenes | 3 | pdf 244 |
  | *Antipatía/simpatía* | «un objeto o criatura grande» → «de tamaño **Enorme o más pequeño**»; añadida la distancia que dispara la salvación (**36 m**); añadido entero el párrafo **«Poner fin al efecto»** con la inmunidad de 1 minuto | 4 + 3 | pdf 245 |
  | *Arma espiritual* | `tirada: "Directo"` → **`"D20+ata.conj."`**: la página dice «puedes hacer inmediatamente un ataque de conjuro cuerpo a cuerpo» | otro | pdf 246 |
  | *Atadura planar* | faltaba la regla de que, si la criatura procede de otro conjuro, **la duración de aquel se amplía hasta igualar la de este** | 3 | pdf 248 |
  | *Clarividencia* | `clases: ["Mago"]` → **`["Bardo","Clérigo","Hechicero","Mago"]`**: la cabecera dice «Adivinación de nivel 3 (bardo, clérigo, hechicero, mago)» | otro | pdf 259 |
  | *Creación* | decía «No puedes usar un objeto creado con este conjuro para crear otro usando este mismo conjuro» — **regla que el manual no contiene**; la real es «si se usa cualquier objeto creado con este conjuro como componente material de otro conjuro, este último fallará» | otro | pdf 267 |
  | *Crear muerto viviente* | nombres de criatura **en inglés sin traducir**: `ghoul`→**gul**, `wight`→**tumulario** (4 apariciones). Las cifras 3/4/5/2/6/3/2 sí coincidían | 5 | pdf 268 |
  | *Crear llama* | `tirada: "Directo"` → **`"D20+ata.conj."`**: la página dice «Haz un ataque de conjuro a distancia» | otro | pdf 268 |
  | *Nube de dagas* | «cubo de 1,5 m / **10 pies**» → «cubo de **1,5 m**»: la página no trae conversión y 1,5 m son 5 pies, no 10 | 6 (conversión falsa) | pdf 316 |

  **`Creación` es el hallazgo más grave de la tanda**, y es un modo de fallo
  nuevo: no es un párrafo que falte ni una cifra cambiada, sino una **regla
  inventada que además tapa a la real**. La base prohibía algo que el manual
  permite y omitía la prohibición que el manual sí impone. Un jugador que
  consultara la base habría jugado con dos reglas equivocadas a la vez.

  **`Clarividencia` es el segundo en gravedad y el más instructivo sobre los
  límites del contraste externo:** tres de sus cuatro clases habían desaparecido
  de la lista. `verificar_foundry.py` no lo veía porque el campo `clases` no está
  entre los que contrasta, y `validar.py` tampoco, porque «Mago» es una clase
  perfectamente válida — el chequeo `hechizos ⊆ clases` solo detecta nombres que
  no existan, no listas incompletas. **Una lista corta pasa por lista buena**, el
  mismo modo de fallo que los placeholders y que `3d0`.

  Dos hallazgos de agente se comprobaron y **no se aplicaron**, con razón
  registrada: la tilde de `Arma magica` (el briefing excluye tildes; queda como
  posible normalización futura) y el «no-muerto» vs «muerto viviente» de
  *Comunión con la naturaleza* (variación de redacción del mismo tipo de
  criatura, no un nombre inventado).

  **El campo `tirada` acumuló 11 avisos más** en esta oleada (los cinco agentes
  los listaron en «Dudas», como pedía el briefing). Dos de ellos **sí se
  aplicaron** —*Arma espiritual* y *Crear llama*— porque no son el caso
  pendiente de decidir: su descripción pide un **ataque de conjuro**, y la base
  ya tiene un valor propio para eso (`D20+ata.conj.`, usado por otros 19
  conjuros). Los otros 9 son el patrón «Directo + salvación», que sigue **sin
  tocar** a la espera de la decisión semántica anotada en `CONTINUAR.md`.

- **Fase 13 — nueve errores en `hechizos.json`, hallados por contraste ancho y
  confirmados en el manual** — `verificar_foundry.py` emparejó 304 de nuestros
  391 conjuros con el SRD por su `nombre_en` y señaló 18 discrepancias. Se
  leyeron **visualmente las 8 páginas** implicadas antes de tocar nada; el
  resultado fue 9 errores nuestros y 2 casos en los que manda el manual:

  | Conjuro | Nuestro | Manual | |
  |---|---|---|---|
  | Contorno borroso (pdf 265) | comp. S | «Componentes: **V**» | ❌ nuestro |
  | Engañar (pdf 278) | comp. V | «Componentes: **S**» | ❌ nuestro |
  | Palabra de regreso (pdf 319) | comp. S | «Componentes: **V**» | ❌ nuestro |
  | Palabra divina (pdf 319) | comp. S | «Componentes: **V**» | ❌ nuestro |
  | Aliento de dragón (pdf 242) | ritual | «Concentración, hasta 1 minuto» | ❌ nuestro |
  | Alterar el propio aspecto (pdf 242) | ritual | «Concentración, hasta 1 hora» | ❌ nuestro |
  | Levitar (pdf 306) | ritual | «Concentración, hasta 10 minutos» | ❌ nuestro |
  | Guardián de la fe (pdf 291) | Evocación | «**Conjuración** de nivel 4» | ❌ nuestro |
  | Paso arbóreo (pdf 320) | Abjuración | «**Conjuración** de nivel 5» | ❌ nuestro |
  | Patrón hipnótico (pdf 320) | V,S,M + conc. | igual | ✅ **manda el manual** |
  | Prohibición (pdf 324) | ritual | «10 minutos **o un ritual**» | ✅ **manda el manual** |

  **El origen es el CSV, no la lectura**: `_origen_hechizos.csv` ya traía esos
  valores mal, y `hechizos.json` los copió fielmente. Es la tercera vez que ese
  CSV falla (antes: el duplicado de *Hablar con animales* y la escuela ausente
  del *Sanctasanctórum*), lo que confirma la advertencia de la tabla de fuentes:
  **datos estructurados no significa datos correctos.**

  Todos los errores son **inversiones de dos campos adyacentes** (V↔S,
  concentración↔ritual), que en el CSV son columnas contiguas. Se comprobó si
  era corrupción sistemática: **no lo es** — de los 44 conjuros contrastables
  con V≠S, 40 coinciden; de los 138 con concentración≠ritual, 133 coinciden.
  Son fallos sueltos.

  **Riesgo residual documentado:** 87 de nuestros 391 conjuros no están en el
  SRD y por tanto nadie los ha contrastado contra nada. Si la tasa observada
  (~9 % entre los de V≠S, ~2 % entre los de concentración≠ritual) se mantiene,
  quedan del orden de 2-3 errores del mismo tipo sin detectar ahí. Solo la
  lectura visual de esas páginas los cerraría.

- **Fase 13 — el verificador no traduce, deduce** — contrastar castellano
  contra inglés tienta a escribir un diccionario de memoria, que es
  exactamente la regla 1 al revés. `verificar_foundry.py` empareja por claves
  independientes del idioma (`nombre_en` en los conjuros; dado + precio +
  categoría en las armas) y **deduce** los vocabularios de los pares
  resultantes, exigiendo después que sean biyecciones consistentes: 8 escuelas
  de magia, 3 tipos de daño y 8 maestrías salieron así, sin un solo conflicto.
  Las armas necesitan tres pasadas encadenadas porque en 2024 hay parejas
  idénticas en todo número —*Glaive* y *Halberd* comparten dado, precio,
  categoría, tipo de daño y peso— y solo la maestría las separa; la maestría,
  a su vez, se deduce de armas sin rival como *Greataxe*. Solo las especies
  llevan glosario escrito a mano (`_verificacion/glosario_especies.yaml`),
  porque son nombres propios y no reglas, y aun así cada pareja se comprueba
  contra dos cifras: velocidad y visión en la oscuridad.

- **Fase 13m — el mayor defecto de toda la base: `consume_material` mal en 41
  conjuros** — la auditoría de los 87 conjuros fuera del SRD (4 agentes) hizo
  que **tres agentes independientes** señalaran el mismo patrón. La causa: la
  conversión del CSV rellenó `consume_material` desde la columna **`gp`**, que
  significa «tiene precio», no «se consume». Son cosas distintas: un material
  puede costar 250 po y ser reutilizable.

  El CSV **sí** codificaba el consumo, en otro sitio: el **asterisco** del
  campo `cost` («500 po*»). Se usó la columna equivocada. Contrastadas ambas
  reglas contra `materials.consumed` del SRD sobre los 304 conjuros
  emparejados: **asterisco 300/304 (98,7 %)** frente a **`gp` 281/304
  (92,4 %)**. Y contra páginas leídas a mano: la regla del asterisco acierta
  **25/25** (8 leídas por mí, 17 por los agentes); `gp` acierta 0/17 en los
  que los agentes verificaron como no consumidos.

  Los 4 casos en que asterisco y SRD discrepaban se resolvieron leyendo la
  página, y tres son excepciones a la regla:
  - *Adivinación* (pdf 241) y *Boca mágica* (pdf 250) — el manual dice «que se
    consume» y el CSV no puso asterisco: **sí se consumen**.
  - *Recluir* (pdf 328) — el manual dice «que se consume» y el SRD no lo marca:
    **manda el manual**, anotado como excepción citada.
  - *Toque helado* (pdf 340) — «Componentes: **V, S**», sin material. Su coste
    «10 po*» era contaminación de la fila contigua del CSV, *Texto ilusorio*,
    que sí lleva ese valor. Se borró coste y consumo.

  **41 conjuros corregidos.** Además se añadieron dos redes: un chequeo externo
  de `consume_material` contra el SRD en `verificar_foundry.py`, y un
  invariante interno en `validar.py` (`consume_material` y `coste` exigen
  componente material) probado por mutación 2/2 — este último es el que habría
  cazado a *Toque helado* sin necesidad de leer la página.

- **Fase 13m — placeholders: la base remitiendo al manual** — auditando
  *Mano de Bigby* apareció el defecto más grave por naturaleza, aunque afecte a
  pocos registros: su `descripcion` contenía literalmente
  «**(Revisar efectos en el MdJ)**» en lugar de los cuatro efectos del conjuro.
  El campo **no estaba vacío**, así que ningún chequeo de completitud podía
  verlo, y la base dejaba de ser autosuficiente justo donde el LLM tiene
  prohibido tirar de memoria.

  Buscado el patrón en los 391: **5 conjuros afectados**. *Mano de Bigby* se
  transcribió entero desde pdf 309-310. Los otros cuatro son tablas largas y
  quedan como **deuda declarada y visible** en `PLACEHOLDERS_CONOCIDOS`
  (`validar.py`), cada uno con su página y qué le falta: *Deseo*,
  *Guardas y guardias*, *Símbolo* y *Muro prismático*. Cualquier marcador **no
  declarado** es error, y una entrada declarada que ya se arregló también
  (para que la lista no envejezca). Probado por mutación 2/2.

- **Fase 13m — tres errores mecánicos más, confirmados en la página**
  - *Insecto gigante* (pdf 297): decía «Ataca = nivel conjuro» cuando el manual
    dice «una cantidad de ataques igual a **la mitad** del nivel de este
    conjuro (redondeado hacia abajo)». **Duplicaba los ataques.** El
    «(redondeado hacia abajo)» que sí estaba era la pista: solo tiene sentido
    si hay una división.
  - *Desintegrar* (pdf 271): la descripción cortaba una frase — «Si este daño
    reduce sus puntos de golpe a 0.» y saltaba a la siguiente. Faltaba «la
    criatura y todos los objetos no mágicos que vista o lleve quedarán
    reducidos a un polvo gris».
  - *Adivinación*: el nombre estaba escrito «**Adiviniación**» (pdf 241).
    Corregido, con `alias` para que una búsqueda por el nombre viejo resuelva.

- **Fase 13m — cierre de la cola, 9 correcciones (2026-08-22)** — la Fase 13m
  quedó el 21 con una cola de hallazgos de agente **sin releer**. Se cerró
  releyendo la página de cada uno con `pdftoppm -r 170`. **Un apagón inesperado
  del equipo interrumpió la sesión**: las siete primeras correcciones ya estaban
  escritas en `hechizos.json` (mtime 10:34) pero **sin registrar aquí**, que es
  exactamente lo que la regla «citar siempre» prohíbe. Este bloque es ese
  registro, reconstruido a posteriori contrastando el JSON contra los informes
  `_verificacion/_auditoria_rasgos/agente-{I,J,K}.md`.

  | Conjuro | Corrección | Página |
  |---|---|---|
  | Los 8 «Castigo…» | `tiempo_lanzamiento` completado con «con un arma cuerpo a cuerpo o un ataque sin armas» — la página nunca permite el ataque a distancia | pdf 256-257 |
  | *Brazos de Hadar* | «hasta el comienzo de **tu** siguiente turno» → «**su**»: el temporizador es el de la criatura afectada, no el del lanzador | pdf 251 |
  | *Cautiverio* | dos de las cinco prisiones mal nombradas: «prisión de cobertura» → «**presidio cercado**», «plomo» → «**sueño**» | pdf 257-258 |
  | *Burla dañina* | texto corrupto «stuileshacia» → «sutiles hacia»; `nombre_en` «Vicios Mockery» → «**Vicious Mockery**» | pdf 252 |
  | *Baile irresistibile de Otto* | → *Baile irresistible de Otto*, con `alias` | pdf 249 |
  | *Flecha acida de Melf* | → *Flecha ácida de Melf*, con `alias` | pdf 286 |
  | *Fuente de la luz lunar* | → *Fuente de luz lunar*, con `alias` | pdf 287 |
  | *Conjurar lluvia de flechas* | `coste: "1 pc"` → `null` | pdf 263 |
  | *Dedo de la muerte* | daño «7d8 + **3d0**» → «7d8 + **30**» | pdf 270 |

  Las tres erratas de nombre se corrigieron **con `alias` al nombre viejo**, para
  que `buscar.py` siga resolviendo una búsqueda por la grafía anterior en vez de
  devolver la lista vacía que hace improvisar al LLM (regla nacida del bug
  `Clerigo`).

  Los dos últimos son de esta sesión y llevan su `_nota_verificacion` dentro del
  propio registro del conjuro:

  - *Conjurar lluvia de flechas* (pdf 263 = libro 261) — «M (un arma cuerpo a
    cuerpo o a distancia que valga al menos 1 pc)». Es un **umbral de valor del
    arma empleada**, que no se pierde, no un coste que se gaste al lanzar. La
    prueba está en la **misma página**: *Conocer las leyendas* y *Consagrar* sí
    dicen «que se consume como parte del conjuro». Mismo criterio que ya tenía
    *Conjurar descarga de proyectiles* (`coste: null`). Es el último resto del
    defecto de `consume_material`: se corrigió el consumo pero quedó el coste.

    > ⛔ **REVISADO EL 2026-08-29: esta decisión era equivocada y se ha
    > revertido.** Confundía `coste` con `consume_material`. Lo que se gasta lo
    > dice el segundo campo, y **39 de los 70 conjuros con coste NO consumen su
    > material**. Los dos conjuros volvieron a `1 pc`. Ver la entrada «Los 52
    > costes fuera del SRD» más arriba.
  - *Dedo de la muerte* (pdf 270 = libro 268) — «sufrirá **7d8 + 30** de daño
    necrótico». El JSON decía **`7d8 + 3d0`**: el `0` de «30» leído como
    notación de dado por la conversión del CSV. **Ningún validador podía verlo,
    porque `3d0` es sintácticamente un dado válido** — el mismo modo de fallo
    que los placeholders: un campo lleno de basura pasa por lleno. Es la cuarta
    vez que el CSV de conjuros mete un defecto, y el primero que sobrevive a las
    cuatro capas de validación.

  **Cifra de `verificar_foundry.py`: 2689, con 7 de sus 16 valores nuevos
  explicados.** Los documentos daban dos números y ninguno reproducible
  (`FUENTES.md` 2514, `CONTINUAR.md` 2673); la ejecución real da **2689**.

  Causa medida, no supuesta: `verificar_conjuros()` **empareja por `nombre_en`**,
  así que arreglar «Vicios Mockery» → «Vicious Mockery» en *Burla dañina* metió
  ese conjuro en el contraste, que antes se caía en silencio. Comprobado
  revirtiendo solo ese campo en una copia desechable: **2689 → 2682, siete
  valores, justo lo que aporta un conjuro.** Es un caso más del fallo silencioso
  ya conocido: *un registro que deja de emparejar desaparece del contraste sin
  dar error*, y aquí el efecto se vio al revés, al reaparecer.

  **Los 9 valores restantes siguen sin explicación.** Se descartó por medición
  que vinieran del texto de `tiempo_lanzamiento` de los ocho «Castigo…»
  (revertirlo no mueve la cifra). No se puede reconstruir más sin el
  `hechizos.json` del 21, que no se conservó. Puede ser sencillamente que el
  2673 escrito a mano nunca fuese exacto. **Se deja anotado como pendiente en
  vez de cerrarlo con una causa plausible.**

- **Fase 13n — cierre de la lectura visual (2026-08-22)** — el objetivo era dejar
  el margen de error en un mínimo aceptable antes de tocar la arquitectura
  (Fases 14-16). Dos frentes: la deuda declarada de conjuros, que hice yo, y las
  tres superficies que ninguna fuente externa cubre, repartidas en **5 agentes
  Sonnet con lotes disjuntos** (briefing en `LEEME_AGENTE_4.md`, informes en
  `agente-{M,N,O,P,Q}.md`). Los agentes solo informan; nada se aplicó sin releer
  yo la página.

  **1. Los 4 placeholders, transcritos. `PLACEHOLDERS_CONOCIDOS` queda vacío.**
  Era el defecto más grave por naturaleza: la base remitiendo al manual justo
  donde el LLM tiene prohibido tirar de memoria.

  | Conjuro | Qué le faltaba | Página |
  |---|---|---|
  | *Deseo* | el texto de los 7 efectos y **el párrafo entero de la tensión** (1d10 necrótico por nivel hasta el descanso largo, Fuerza 3 durante 2d4 días, 33 % de no volver a lanzarlo) | pdf 270-271 |
  | *Guardas y guardias* | los 4 efectos disipables (Escaleras, Pasillos, Puertas, «Otro efecto») y el párrafo de exentos y contraseña | pdf 289-290 |
  | *Símbolo* | los 6 efectos del glifo | pdf 334-335 |
  | *Muro prismático* | la tabla «Capas prismáticas» completa y el párrafo de la CA 10 y el orden de destrucción | pdf 315 |

  **Tres defectos de contenido salieron al transcribir**, en el texto que ya
  había y que nadie había vuelto a mirar:
  - *Símbolo* decía que el glifo se detecta con **Inteligencia (Investigación)**;
    la página dice **Sabiduría (Percepción)**. Característica y habilidad, las dos
    mal. Es un error que cambia la tirada en mesa.
  - *Símbolo* añadía «leer o manipular» a los activadores, que la página no lista.
  - *Muro prismático* decía que el muro «aparece en una pared opaca» — la página
    dice que el propio plano de luz **forma** un muro vertical opaco; el muro es
    el conjuro, no algo que se adhiera a una pared preexistente. Y añadía «o
    inicien su turno ahí» a la condición de ceguera, que la página no exige.

  **Incoherencia del propio manual, registrada sin resolver:** el párrafo de
  entrada de *Símbolo* llama a sus efectos «aturdimiento, discordia, dolor,
  muerte, **miedo** o sueño», pero el epígrafe del sexto dice «**Terror**». Se
  transcriben ambos tal como aparecen, con la contradicción anotada en el
  registro. No nos toca a nosotros arreglar el manual.

  **2. Las tres superficies ciegas, auditadas.** 138 registros contra la página:

  | Lote | Qué | Resultado |
  |---|---|---|
  | agente-M | 32 dotes (origen, estilo de combate, don épico) | **1 hallazgo** |
  | agente-N | 21 dotes generales, pdf 204-207 | sin hallazgos |
  | agente-O | 22 dotes generales, pdf 208-211 | sin hallazgos |
  | agente-P | 16 trasfondos: equipo inicial completo | sin hallazgos |
  | agente-Q | 95 registros de equipo y munición, celda a celda | sin hallazgos |

  El único hallazgo, verificado por mí releyendo la página: **`Afortunado` y
  `Alerta` citaban pdf 203 / libro 201 y están impresas en la página cuyo pie
  dice 200** (pdf 202). Sigue el patrón: 14 de los 15 defectos que han salido de
  auditorías visuales en este proyecto son citas de página.

  **Cuatro lotes limpios se verificaron por muestreo antes de darlos por buenos**,
  porque un informe en blanco no prueba nada por sí solo. Releí entera la tabla
  «Equipo de aventureros» (libro 223) y la comparé por código contra los 82
  registros de la base: **coinciden los 82 en nombre, peso y precio**, sin una
  sola fila corrida. Y releí los trasfondos *Acólito* y *Animador* (libro 178)
  campo a campo, incluido el equipo inicial: exactos.

  **3. Chequeo nuevo: `validar_dados()`.** Ninguna tirada de la base puede usar
  un dado que no existe; las caras válidas son 4, 6, 8, 10, 12, 20 y 100, y el
  barrido de toda la base confirma que no aparece ninguna otra. Nació del `3d0`
  de *Dedo de la muerte*, que sobrevivió a las cuatro capas porque `3d0` es
  sintácticamente un dado. Cubre 669 tiradas en `hechizos.json` y todos los YAML.

  Probado por mutación en `_verificacion/mutaciones_dados.py`: **12/12**, y la
  mitad son **controles negativos**. No es simetría decorativa: la primera
  versión del chequeo se disparaba con su propia documentación —encontró tres
  `d0` y los tres estaban dentro de la `_nota_verificacion` que explica el
  arreglo de *Dedo de la muerte*—. Por eso ignora los campos `_*`, y hay una
  mutación que lo comprueba. **Un chequeo que solo se prueba en la dirección de
  detectar acaba prohibiendo documentar lo que corrigió.**

- **Fase 13k — auditoría de las 48 subclases y las 10 especies (segunda tanda,
  4 agentes Sonnet)** — las dos superficies ciegas que quedaban. 48 subclases
  con 241 rasgos + 38 rasgos de especie + 14 linajes, en unas 45 páginas.
  Informes en `_verificacion/_auditoria_rasgos/`.

  **4 hallazgos reales, los cuatro citas de página**, verificados en la página
  antes de aplicarlos:

  | Clase | Subclase | Citaba | Está en |
  |---|---|---|---|
  | Druida | Círculo de las Estrellas | pdf 102 | **pdf 101** |
  | Druida | Círculo del Mar | pdf 103 | **pdf 102** |
  | Guerrero | Maestro del Combate | pdf 119 | **pdf 121** |
  | Hechicero | Hechicería de Magia Salvaje | pdf 133 | **pdf 132** |

  El del Guerrero era el más grave: **Campeón y Maestro del Combate citaban la
  misma página** (119), cuando la secuencia real es 117 → 119 → 120 → 121.

  **Cero hallazgos** en las 16 subclases de Bárbaro/Bardo/Brujo/Clérigo, en las
  16 de Mago/Monje/Paladín/Pícaro, y en el contenido de las 10 especies: tipo,
  tamaño, velocidad, visión en la oscuridad, 38 rasgos y 14 linajes coinciden
  con la página. El texto mecánico de los 241 rasgos de subclase también.

- **Fase 13k — dos hallazgos de agente rechazados, y el criterio que faltaba
  escribir** — el agente de especies señaló que Elfo cita pdf 191 cuando el
  encabezado «ELFO» empieza en pdf 190, e igual con Tiefling (199 vs 198).
  Comprobado en la página: **pdf 190 y pdf 198 solo llevan ambientación**
  (la historia de los elfos, la descripción de los tres legados del tiefling);
  el bloque de reglas —tipo de criatura, tamaño, velocidad, rasgos— está en
  191 y 199. **Nuestras citas apuntan a las reglas, que es lo que debe citar
  una base de reglas**, y son consistentes con las otras 8 especies (donde
  ambientación y reglas comparten página y no se nota la diferencia).
  Hallazgos rechazados; **criterio anotado aquí para que no vuelva a
  discutirse: una cita apunta a la página donde está la MECÁNICA, no donde
  empieza la sección.**

- **Fase 13j — herramientas contrastadas, y el peso del herborista** — 18 de
  las 25 herramientas emparejan por (precio, peso) y las 5 características
  deducidas de ellas no dan un solo conflicto. Tres no emparejan y están
  **declaradas por nombre** en `verificar_foundry.py`, no contadas: dos son
  categorías del manual con «Peso: variable» (`Instrumento musical`, `Juego`)
  y la tercera es `Útiles de herborista`, donde el manual dice «Inteligencia ·
  1,5 kg» (pdf 223 = libro 221) y el SRD publica 8 lb. Precio y característica
  sí coinciden; manda el manual.

  La lista de huérfanas declaradas nació de una mutación que **no saltaba**:
  al cambiar el precio de una herramienta, esta dejaba de emparejar y
  desaparecía del contraste en silencio — el mismo fallo que ya apareció con
  las maestrías de arma. Con la lista, cualquier huérfana no declarada es
  error. 25/25 mutaciones tras el arreglo.

  De paso se corrigió la `fuente` del propio fichero: decía
  `paginas_pdf: "220-221"` cuando esas son las páginas **de libro**; la tabla
  de herramientas está en pdf 222-223. Ahora lleva los dos campos.

- **Fase 13i — auditoría de los 158 rasgos de clase por lectura visual
  (4 agentes Sonnet en paralelo, ficheros disjuntos)** — era la mayor
  superficie ciega de la base: ninguna fuente externa la cubre y nadie la había
  vuelto a mirar desde su transcripción. Se repartieron las 12 clases en cuatro
  lotes disjuntos (34 páginas). **Los agentes solo informan; no editan la
  base** — las correcciones las aplicó Opus tras releer personalmente cada
  página. Informes en `_verificacion/_auditoria_rasgos/`.

  Resultado: **10 hallazgos en 158 rasgos**, todos verificados contra la página
  antes de tocar nada. Nueve son **citas de página equivocadas**; el texto
  mecánico de los 158 resultó correcto.

  | Clase | Rasgo | Citaba | Está en |
  |---|---|---|---|
  | Druida | Druídico, Orden primigenia, Compañero salvaje, Forma salvaje | pdf 93 | **pdf 94** |
  | Explorador | Maestría con armas | pdf 105 | **pdf 106** |
  | Paladín | Maestría con armas | pdf 159 | **pdf 160** |
  | Mago | Adepto en rituales, Recuperación arcana | pdf 139 | **pdf 140** |
  | Brujo | Astucia mágica | pdf 71 | **pdf 72** |
  | Guerrero | Acción súbita (dos usos) | pdf 116 | **pdf 115** |

  El décimo es el único **error de contenido**, y es el más instructivo:
  `clases/picaro.yaml` decía `nota: "Mejoras de característica extra en niveles
  6 y 10"` cuando su propia tabla de progresión concede mejoras en 4, 8, 10, 12
  y 16 — el nivel 6 del Pícaro es **Pericia**, no una mejora. El «6» está
  copiado de la nota del Guerrero, donde sí es correcto (6 y 14). Confirmado en
  pdf 170: «Vuelves a obtener este rasgo en los niveles 8, 10, 12 y 16».
  **Ningún validador podía verlo**: es prosa libre, y el contraste externo solo
  mira cifras.

  **El invariante de orden de página estaba corto, y bloqueaba una cita
  correcta.** Al corregir «Acción súbita (dos usos)» (N17) a pdf 115,
  `validar_rasgos_clase()` lo marcó como error por retroceder respecto a un
  rasgo de N13. Su excepción solo contemplaba que la tabla repitiera el *mismo*
  nombre en varios niveles, no que los distinguiera con un paréntesis
  («un uso» / «dos usos») describiéndolos una sola vez. Se amplió, y se probó
  por mutación que sigue detectando lo que debe: 3/3 (cita que retrocede en un
  rasgo normal, repetición que cita una página que no es la de la primera,
  repetición que cita una página inventada).

  **Un hallazgo de agente resultó falso y conviene dejarlo escrito.** El agente
  B explicó su hallazgo del Druida afirmando que el PDF tiene las páginas 93-94
  duplicadas físicamente en 95-96. **Es falso**: comparadas píxel a píxel solo
  coinciden en un 9,8 %, y pdf 95 lleva el número de libro 93, con lo que el
  offset `pdf = libro + 2` se cumple sin excepción. Su *hallazgo* (los cuatro
  rasgos están en pdf 94) sí era correcto y se aplicó; su *explicación* no. Es
  la razón exacta por la que la doctrina exige releer la página antes de
  aceptar el trabajo de un agente: el hallazgo y el razonamiento que lo
  acompaña se verifican por separado.

- **Fase 13 — dotes y trasfondos, contrastados sin traducir un solo nombre** —
  eran las dos categorías con 0 % de contraste externo y el SRD apenas cubre
  17 de 75 dotes y 4 de 16 trasfondos, así que un emparejamiento por nombre
  habría cubierto poco y exigido traducir de memoria. Se resolvió por
  estructura:
  - **Dotes:** en el manual el prerrequisito lo fija la **categoría** (origen:
    ninguno · generales: nivel 4 · dones épicos: nivel 19 · estilos de combate:
    el rasgo homónimo). Se deduce ese patrón de cada lado por separado y se
    emparejan las **categorías por su patrón**, no por su nombre; después se
    exige que las **75** dotes cumplan el de la suya. Es justo el chequeo que
    faltaba: el OCR devolvía cero coincidencias de «Prerrequisito» en ese
    capítulo, así que una dote con el prerrequisito caído era el defecto más
    probable. **Ninguna lo tiene: 75/75 conformes.**
  - **Trasfondos:** se emparejan por el **trío de características** que ofrece
    cada uno (en el SRD, el complemento de `locked`). Los 16 tríos de nuestra
    base son distintos entre sí, así que la clave es única y determinista.
    Además, los **16** pasan un invariante que no necesita SRD: la dote que
    concede un trasfondo siempre es una dote de origen.
  - **Hallazgo sobre la fuente, no sobre la base:** el propio SRD es incoherente
    en los dones épicos — 5 de 7 declaran nivel 19 y 2 lo dejan vacío. Nuestra
    base los tiene los 12 con nivel 19. Se toma el patrón mayoritario y se deja
    la incoherencia anotada en el informe.

- **Fase 13 — la prueba por mutación encontró un fallo silencioso** — de las 13
  mutaciones, dos no saltaron a la primera. La primera reveló que 5 armas nunca
  llegaban a emparejarse (se arregló con la tercera pasada). La segunda fue más
  seria: al corromper la maestría de un arma, esta dejaba de emparejar y
  **desaparecía del contraste sin avisar**, en vez de dar error — el mismo
  fallo silencioso que el bug `Clerigo`. Ahora, si conocemos la maestría de un
  arma y ninguno de sus equivalentes posibles la tiene, eso es discrepancia, no
  ambigüedad. 13/13 tras el arreglo (`_verificacion/mutaciones_foundry.py`).

- **`Libro de conjuros` — el manual no lo vende, y eso es el dato** — era el
  último hueco de `cobertura.py`. Resuelto por lectura visual de las dos
  páginas que podían contradecirlo: la tabla «Equipo de aventureros»
  (pdf 225 = libro 223) salta de «Libro» a «Linterna de ojo de buey» sin
  entrada intermedia, y la descripción de «Libro» (25 po, pdf 228 = libro 226)
  es un libro de ficción o no ficción que da +5 a pruebas de Inteligencia:
  no es un libro de conjuros. El del Mago **nace del rasgo** «Lanzamiento de
  conjuros» (pdf 139 = libro 137): objeto Diminuto, 1,5 kg, 100 páginas, sin
  precio de compra. Registrado en `equipo/aventureros.yaml` bajo
  `objetos_de_rasgo_de_clase`, con `precio: null` y la evidencia negativa
  citada. **No se le inventó un precio**: la ausencia se documentó como
  ausencia. Probado por mutación (corromper el nombre reabre el hueco).

- **Bardo: `dado_golpe` y `salvaciones` duplicados** — aparecían dentro de
  `atributos_basicos` y otra vez sueltos en el nivel superior del fichero,
  residuo de la Fase 9 y único fichero de las 12 clases que lo hacía. Los
  valores coincidían, así que nada fallaba; el riesgo era que al corregir uno
  el otro quedara viejo en silencio. Borrados los sueltos:
  `atributos_basicos` es la única autoridad. El cruce `suelto != ab` de
  `validar_atributos_basicos()` **se conserva a propósito** como red por si
  alguien los reintroduce — verificado por mutación (reintroducir `dado_golpe:
  d6` en el nivel superior salta).

- **Bardo: las habilidades eran una interpretación, no una transcripción** — el
  manual dice «Elige tres cualesquiera (consulta el capítulo 1)» (pdf 61 =
  libro 59) y la base guardaba los 18 nombres expandidos. Útil para un script,
  pero perdía el «cualesquiera» y contradecía la regla 3 de
  `clases/_ESQUEMA_atributos_basicos.md`. Ahora conviven: `literal` con la cita
  exacta, `cualesquiera: true`, y `de` como expansión declarada. El esquema lo
  documenta.

- **Competencias de Bárbaro, Bardo y Brujo — contrastadas** — eran las 3 clases
  de 12 cuya Fase 11 nadie había vuelto a mirar (justo donde en la fase
  anterior aparecieron dos citas de página falsas). Leídas pdf 53, 61 y 71:
  las siete filas de cada tabla «Atributos básicos» coinciden con la base.
  **12/12 clases contrastadas contra la página.**

- **Fase 8a — cimientos deterministas de `/personaje`** — se construyeron
  `calculo.py` (aritmética: PG, CA, CD de conjuros, bonificador de ataque de
  conjuros, bonificador por competencia, coste de compra por puntos, tabla
  de espacios de conjuro), `buscar.py` (consulta que falla ruidosamente:
  clase inexistente, conjuro inexistente, objeto inexistente → error
  explícito, nunca `[]` silencioso), `verificar_personaje.py` (trazabilidad:
  cada `ref:` de una ficha debe resolver a un registro real, y el bloque
  `calculado` se recalcula y se compara) y `personajes/_ESQUEMA.md` (el
  contrato: todo dato mecánico es una referencia, nunca una copia de texto).
  Dos fórmulas se verificaron por lectura visual antes de codificarlas:
  «Puntos de golpe en el nivel 1 por clase» (pdf 42 = libro 40) y «CD de
  salvación de conjuros» / «Modificador de ataque de conjuros» (pdf 240 =
  libro 238). `verificar_personaje.py` se probó por mutación: 4/4 detectadas
  (ref rota, `calculado` corrompido a mano, habilidad fuera de lo permitido,
  compra por puntos que no suma 27). Hay un ejemplo completo y verificado en
  `personajes/_ejemplo_aerin.yaml`.

- **Fase 8a, prueba de estrés — 5 agentes Sonnet en paralelo, 5 personajes
  distintos** — cada uno construyó un personaje de nivel 1 (Bárbaro/Orco,
  Mago/Gnomo, Bardo/Tiefling, Clérigo/Aasimar, Pícaro/Mediano) usando las
  herramientas recién escritas, sin coordinarse entre sí. Encontraron 4
  problemas reales, 3 de ellos confirmados de forma independiente por más
  de un agente — la señal más fuerte de que algo estaba realmente roto:
  - **`cualesquiera: true` desactivaba la validación de habilidades por
    completo** en vez de solo ampliarla a las 18 canónicas: una habilidad
    inventada («Cocina inventada») pasaba `verificar_personaje.py` intacta.
    Corregido: ahora sigue exigiendo que esté entre las 18 de
    `reglas/habilidades.yaml`.
  - **`verificar_sin_copias()` no exceptuaba la prosa libre** que
    `_ESQUEMA.md` permite sin límite (`historia`, `personalidad`...): dos
    agentes tuvieron que trocear su propia prosa original en fragmentos
    cortos para poder pasar la verificación. Corregido con una lista
    explícita de campos exentos.
  - **`personajes/_ejemplo_aerin.yaml`, el ejemplo que la skill recomienda
    seguir «al pie de la letra», tenía un dato inventado**: citaba el
    idioma «Élfico» (el nombre canónico en `reglas/idiomas.yaml` es «Elfo»)
    como concedido por la especie Elfo, cuando ninguna especie de la base
    concede idiomas — es una elección libre general, no un regalo racial.
    Pasaba sin más porque el campo `idiomas` no llevaba `ref:` que lo
    delatara. Corregido.
  - **El propio esquema pedía `ref:` a categorías de armas/armaduras**
    (`equipo/armas.yaml#Armas sencillas`) que no existen como registros
    individuales en `equipo/` — solo hay armas concretas ahí. Tres de cinco
    agentes chocaron con esto y lo sortearon citando un arma concreta en su
    lugar. Corregido: `competencias.armas/armaduras/herramientas` ahora
    van como `categoria:` (texto literal contrastado contra
    `atributos_basicos` de la clase), no como `ref:` a equipo/.
  - **Bug menor de ambigüedad**: `buscar.equipo("Bastón")` sin más contexto
    devuelve el primer fichero que lo tenga (el arma, 2 pp), pero también
    existe un «Bastón» distinto como variante de canalizador arcano en
    `equipo/aventureros.yaml` (5 po). Un solo agente lo notó al pasar.
    `buscar.equipo()` ahora acepta un `archivo` opcional para desambiguar,
    y `verificar_personaje.py` lo usa siempre que resuelve una ref de
    equipo.

  Los cinco personajes y sus fichas de hallazgos completas quedan en
  `personajes/*.yaml` y `personajes/_hallazgos/*.md`. Las cinco fichas
  pasan `verificar_personaje.py` con el verificador ya corregido, y los
  tres validadores de la base siguen en verde — nada de esto tocó
  `clases/`, `hechizos.json`, etc.

- **Fase 8a, prueba de estrés ronda 2 — 5 agentes Sonnet más, las 5 clases
  que faltaban** (Guerrero/Enano/Guardia, Druida/Goliat/Guía,
  Explorador/Humano/Vagabundo, Monje/Dracónido/Ermitaño, Paladín/Elfo/Marinero
  — con esto 10 de las 12 clases quedan probadas; faltan Brujo y Hechicero). Confirmaron que Explorador y
  Paladín lanzan conjuros desde nivel 1 en esta edición (`lanzador: medio`,
  `calculo.py cd-conjuros`/`ataque-conjuros` correctos para ese caso) y que
  la fórmula de CA del Monje (10+Des+Sab) se aplica bien. Encontraron 4
  problemas reales, el primero confirmado por **5 de 5 agentes**:
  - **`verificar_categorias()` nunca miraba el trasfondo**, solo las clases
    — pese a que el propio `_ESQUEMA.md` decía que sí. Toda herramienta de
    trasfondo (cartógrafo, ladrón, herborista, juego...) se rechazaba.
    Corregido: ahora suma `trasfondo.herramienta` a lo permitido, y si el
    trasfondo dice «elige un tipo de X» (elección abierta), no restringe.
  - **`verificar_habilidades()` no contaba las habilidades que concede un
    rasgo de especie** (p. ej. Elfo → «Sentidos agudos»: Percepción,
    Perspicacia o Supervivencia; Humano → «Diestro»: cualquiera). No hay
    campo estructurado para esto en `especies.yaml`, así que se detecta por
    texto («Competencia en...» en el `desc` del rasgo). Corregido.
  - **Ningún bono de PG por especie era representable** (Enano → «Aguante
    enano»: +1 en nivel 1), así que un Enano nunca podía pasar
    `calculado.pg_max`. Se añadió el campo opcional `bonus_pg_especie` al
    esquema, que `verificar_personaje.py` suma al recalcular.
  - **`buscar.equipo()` sin `archivo` devolvía el primer fichero que
    encontraba en silencio** cuando un nombre existe en más de uno con
    significado distinto (el caso "Bastón", ahora también visto con "Bastón
    de madera" del canalizador druídico). Corregido: ahora, si hay más de
    una coincidencia y no se especifica `archivo`, falla pidiendo que se
    desambigüe — en vez de adivinar.

  Las 4 correcciones se probaron con caso positivo + caso negativo cada
  una (p. ej.: una herramienta de trasfondo legítima ahora pasa, una
  inventada sigue fallando). Las 11 fichas de personaje existentes (10 de
  las dos rondas + el ejemplo) se re-verificaron contra el código corregido
  sin ninguna regresión, y los tres validadores de la base siguen en verde.

- **Clérigo: dos citas de página erróneas en `clases/rasgos/clerigo.yaml`** — «Orden
  divina» (N1) se citó en pdf 85 y «Canalizar divinidad» (N2) en pdf 83, cuando ambas
  están en **pdf 84 = libro 82** (verificado visualmente). Los textos eran correctos;
  solo fallaban las citas. Lo delató un invariante nuevo: dentro de una clase, la
  página citada no puede retroceder al subir de nivel, porque el manual expone los
  rasgos en orden. Ese chequeo vive ya en `validar_rasgos_clase()`, con la excepción
  de los rasgos que la tabla concede en varios niveles y se describen una sola vez.

- **`Clerigo` sin tilde (116 conjuros)** — `hechizos.json` etiquetaba la clase como
  `Clerigo`, mientras el resto de la base usa `Clérigo`. Un filtro por el nombre
  canónico devolvía **0 resultados en silencio**: el peor fallo posible para un
  orquestador LLM, que concluye «no hay conjuros» e improvisa. Normalizado, y
  `validar_hechizos_clases()` cruza ahora `hechizos[].clases` contra el campo
  `clase` real de cada `clases/*.yaml` para que no pueda repetirse.
- **«Hablar con animales» — entrada duplicada, eliminada** — el CSV de origen traía
  dos filas para *Speak with Animals* (líneas 814 y 821). Una, `Hablar con los
  animales`, es fiel a la pág. 289 (alcance Lanzador, 10 minutos, Acción o ritual,
  cuatro clases); la otra, `Hablar con animales`, tenía la lista de clases vacía y
  alcance/duración que **contradicen esa misma página** (Toque, 8 h). Se eliminó la
  corrupta y se añadió `alias: ["Hablar con animales"]` a la correcta, para que una
  búsqueda por el nombre truncado siga resolviendo. La fila original permanece en
  `_origen_hechizos.csv` (recuperable). Total: 392 → 391.

- **Sanctasanctórum privado de Mordenkainen** — el CSV no traía escuela.
  Verificada como *Abjuración* en la tabla «Conjuros de mago de nivel 4»,
  PDF pág. 144. No se rellenó de memoria.
- **Erudito (trasfondo)** — el OCR perdió dos de sus tres puntuaciones y leyó
  «pergamino (3 hojas)» en vez de 8. Corregido por lectura visual (PDF pág. 184).
- **Tiefling** — el OCR cortó la velocidad. Confirmada en 9 m (PDF pág. 199).
- **Reprensión infernal** — transcrito por error como «Represión infernal».
  Lo detectó el chequeo de integridad contra `hechizos.json` y se corrigió
  releyendo la tabla «Legados infernales» (PDF pág. 199).

- **Fase 13o — muestra aleatoria de descripciones: 17,5 % de error (2026-08-22)**
  — la última superficie ciega eran las `descripcion` de los conjuros que sí
  están en el SRD: `verificar_foundry.py` les contrasta la cabecera, pero el SRD
  **no publica el texto**, así que nadie lo había mirado desde la conversión del
  CSV. Auditarlas todas son ~45 páginas; antes de comprometerlas se midió la
  tasa con una **muestra aleatoria de 40 sobre los 306 emparejados**.

  Muestra reproducible: `random.seed(20260822)` sobre la lista ordenada por
  `nombre`; manifiesto y reparto en `_auditoria_rasgos/MUESTRA_13o.md`, briefing
  en `LEEME_AGENTE_5.md`, informes en `agente-{R,S,T,U}.md`. Cada hallazgo fue
  releído en la página por Opus antes de aplicarse.

  ### Resultado: 7 de 40 conjuros con defecto

  ```
  python3 _verificacion/intervalo.py 7 40 306
  7 de 40 = 17,50 %   ·   IC 95 % exacto: 7,34 % – 32,78 %
  proyección sobre 306: ≈ 53,5 conjuros con error (22,5 – 100,3)
  ```

  **Es un orden de magnitud peor que cualquier otra superficie medida** — 2,96 %
  en los campos que el SRD sí cubre, 0,72 % en las superficies de lectura visual
  de la Fase 13n. La conclusión es directa: **el texto de los conjuros nunca
  estuvo verificado, y no lo está**.

  | Conjuro | Defecto | Gravedad |
  |---|---|---|
  | *Aura sagrada* | su `descripcion` era **íntegramente la de «Aura mágica de Nystul»**, otro conjuro de la misma página | crítica |
  | *Apariencia* | **inventaba una prueba de Inteligencia contra la CD** que no está en la página (es la regla de 2014) | crítica |
  | *Simulacro* | «actúa en **su** turno» donde la página dice «en **tu** turno»: cambia quién lo controla | alta |
  | *Muro de piedra* | faltaba el párrafo de los muros de más de 6 m y la cláusula «y no se puede disipar» | alta |
  | *Espejismo arcano* | «1 km cuadrados» donde la página dice «zona cuadrada de **1,5 km de lado**» | alta |
  | *Controlar el clima* | seis nombres de estado inventados en sus tres tablas (*Templado*, *Frío extremo*, *Galerna*, *Tempestad*, *Nubes escasas*, *Cielo cubierto…*) | media |
  | *Crecimiento vegetal* | «0,46 **yardas**» donde son **millas** (750 m) | baja |

  ### Los dos modos de fallo nuevos

  1. **Descripción intercambiada con la de otro conjuro.** *Aura sagrada* es lo
     peor que puede pasarle a esta base: nombre, nivel, escuela, componentes y
     clases correctos, y las reglas de otro conjuro. **Ningún validador podía
     verlo** y el contraste con el SRD tampoco, porque no cubre el texto. Se
     buscó por código si había más: barrido de similitud sobre los 391, **un
     solo caso**. Los otros pares que salieron (*Palabra de curación* / *…en
     masa*, *Inmovilizar persona* / *…monstruo*) son redacciones paralelas
     legítimas del manual, comprobadas una a una.
  2. **Reglas de 2014 coladas como si fueran de 2024.** *Apariencia* traía la
     prueba de Investigación de la edición vieja. Es exactamente lo que la regla
     «consultar, no recordar» existe para impedir, y demuestra que el CSV de
     origen **no era una transcripción del manual de 2024**, sino texto con
     memoria de la edición anterior mezclada.

  ### Hallazgo sistemático aparte: el campo `tirada`

  Dos agentes, por su cuenta, dudaron del mismo campo. Medido por código sobre
  los 391: **52 conjuros dicen `tirada: "Directo"` mientras su propia
  descripción exige una tirada de salvación (47) o un ataque de conjuro (5)** —
  entre ellos *Bola de fuego* no, pero sí *Espíritus guardianes*, *Nube
  apestosa*, *Patrón hipnótico* o *Guardián de la fe*.

  **No se ha tocado, y a propósito.** El campo viene literal de la columna
  `como_usar` del CSV, **ningún script de la base lo consume**, y su semántica
  nunca se definió: no está escrito en ninguna parte si «Directo» significa «el
  conjuro no exige tirada» o «el disparador principal es automático» (que sería
  defendible en *Castigo abrasador*, donde la salvación es para escapar). **Es
  una decisión de diseño pendiente, no un defecto que aplicar**; corregir 52
  registros adivinando la semántica sería peor que dejarlos. Queda anotado en
  `CONTINUAR.md` como decisión a tomar.
