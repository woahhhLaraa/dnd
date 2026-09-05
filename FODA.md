# FODA — la base canónica como sustrato de un orquestador LLM

> Fecha: **2026-08-29**. Sustituye a `FODA_2026-08-19_OBSOLETO.md` (borrado el 2026-08-31; en el
> historial de git), cuyas
> debilidades 1, 2, 3 y 4 están todas cerradas y cuya «Conclusión operativa»
> mandaba hacer dos fases que ya se hicieron.
> Premisa: **todo lo interpretativo lo ejecuta un LLM**; la base es su única
> fuente de verdad y el código, su calculadora y su filtro.

Todo lo que sigue está medido sobre la base real, no estimado. Los números se
reproducen con los cinco comandos del final.

---

## 💪 Fortalezas

1. **Trazabilidad por dato, no por archivo.** Cada clase, subclase, dote,
   conjuro, especie y trasfondo lleva su página. Es lo que hace *verificable*
   la directiva «denegado por defecto, cita la regla»: un humano puede abrir el
   PDF y comprobarla. Sin esto, el auditor sería teatro.
2. **Contenido cerrado.** 391 conjuros, 12 clases con tabla completa, 48
   subclases, 158 rasgos de clase con texto, 75 dotes, 10 especies, 16
   trasfondos, equipo, munición, habilidades, idiomas, generación y multiclase.
   **No queda manual que transcribir.**
3. **Cuatro validadores independientes, y ninguno repite al otro.**
   `validar.py` cruza tablas transcritas por separado; `verificar_srd.py` y
   `verificar_foundry.py` contrastan **4.395 valores** contra fuentes externas
   sin traducir (emparejan por claves independientes del idioma y exigen
   biyección); `cobertura.py` pregunta si la base sabe responder.
4. **Cada chequeo nuevo se prueba por mutación, en las dos direcciones.**
   `mutaciones_dados.py` (12/12), `mutaciones_conversiones.py` (16/16),
   `mutaciones_integridad.py` (24/24), `mutaciones_efectos.py` (36/36),
   `mutaciones_pg.py` (13/13), `mutaciones_materiales.py` (10/10),
   `mutaciones_tiradas.py` (19/19), `mutaciones_prerrequisitos.py` (10/10), `mutaciones_subida.py` (7/7), `mutaciones_nivel20.py` (42/42) y
   `mutaciones_foundry.py` (47/47). La mitad
   de cada suite son **controles negativos**: datos raros pero legítimos que no
   deben hacer saltar nada. No es simetría estética — la primera versión del
   chequeo de dados se disparaba con su propia documentación.
5. **La matemática ya es dato, no prosa.** Progresión, espacios de conjuro,
   compra por puntos y multiclase están en tablas. El LLM no suma nada.
6. **Fidelidad declarada** (desde el 2026-08-29). Cada fichero dice si su texto
   es `literal`, `condensado` o `estructurado`, y `hechizos.json` se declara
   `mixto` **con la explicación de por qué no se pudo clasificar por registro**.
   Un auditor al que se le exige citar textualmente ya sabe qué está citando.
7. **La base sabe cuánto se equivoca.** Es lo más raro de este proyecto: hay
   tasas medidas con intervalo de confianza por superficie, no una sensación.

### Lo que se aprendió mirando a los maduros (2026-08-31)

Leído el código real de Foundry dnd5e y DiceCloud, no sus README:

- **Foundry automatiza 76 de 332 rasgos de clase/subclase 2024 (23 %).** El
  resto es texto. No resolvieron el problema automatizando todo: lo
  resolvieron **no intentándolo**, y **declarando la frontera dentro del
  dato** — 380 registros llevan una «Foundry Note» que dice qué no está
  automatizado. Aquí la frontera era el silencio.
- **Foundry no tiene tests.** Su `package.json` trae `build`, `lint` y
  `watch`. Sustituyen verificación por cientos de miles de jugadores. Este
  proyecto tiene una usuaria, así que sus 4395 valores y sus mutaciones
  **son el sustituto correcto** y no se tocan. De Foundry se copia la
  arquitectura, nunca la ausencia de pruebas.
- **Una dote que sube una característica usa en Foundry el MISMO mecanismo
  que la mejora de nivel 4** (`advancement/AbilityScoreImprovement`). Un solo
  camino, por eso no se puede olvidar conectar uno de los dos.
- **DiceCloud tiene 11 operaciones; aquí había 6.** La que faltaba y cierra
  el espiral es `conditional`: un efecto citado que guarda texto y no se
  calcula. Adoptada el 2026-08-31.

## 📉 Debilidades

1. **~~Las descripciones de conjuro~~ → ✅ auditadas y corregidas (2026-08-29).**
   La Fase 13p cerró con **48 defectos en 305 conjuros = 15,7 %** (IC 95 %
   **11,8 % – 20,3 %**), los 48 corregidos contra la página. Era **un orden de
   magnitud peor** que cualquier otra superficie, y por eso bloqueaba la Fase 14:

   | Superficie | Tasa medida (antes de corregir) |
   |---|---|
   | Campos que el SRD contrasta | 2,96 % |
   | Dotes, trasfondos, equipo (lectura visual) | 0,72 % |
   | `nombre` de conjuro | 1,0 % |
   | `resumen` de conjuro | 4,3 % |
   | **Descripciones de conjuro** | **15,7 %** |

   **El residuo SÍ está medido (2026-08-29):** una muestra aleatoria
   post-corrección de 36 conjuros dio **4 defectos = 11,1 %** (IC 3,1-26,1).
   No prueba que la tasa haya bajado —los intervalos se solapan— pero **sí que
   auditar no deja limpio**: los 4 estaban en conjuros ya auditados, y dos
   habían pasado por la oleada 4 ese mismo día.
2. **✅ CERRADA (2026-09-02) — las conversiones a pies, borradas.**
   *(era 🔴: añadido editorial en un fichero declarado literal)*

   **23 páginas leídas por nueve lectores independientes no imprimen ni una
   sola unidad imperial**: el manual castellano es métrico y las conversiones
   las añadió la base entera. `validar_conversiones()` comprobaba que
   estuvieran bien calculadas —lo estaban, las 543— pero **nadie comprobaba
   que debieran existir**, que era la pregunta.

   Borradas en la fase 2 del `PLAN_19`: 543 equivalencias en 399 registros de
   298 conjuros, de `descripcion` (321) y `alcance.texto` (222). El chequeo
   cambió de sentido y ahora **impide que vuelvan**.

   **Lo que NO se borró, porque no es cita sino dato:** `alcance.metros`,
   `alcance.pies` y `alcance.casillas` siguen ahí. `verificar_foundry.py`
   contrasta `alcance.pies` contra el SRD número contra número, y borrarlos
   habría dejado 218 alcances sin fuente externa. Su aritmética se sigue
   comprobando, así que vaciar el texto no abrió ningún hueco.

   **Y el borrado destapó un defecto que la conversión tapaba:** *Cofre oculto
   de Leomund* decía «0,34 m / 1 pies³», con el cúbico solo en la unidad
   añadida — quitarla dejaba «0,34 m», metros lineales para un volumen. Queda
   como «0,34 m³», que es lo que dice la propia frase dos palabras después
   («90 cm por 60 cm por 60 cm» = 0,324 m³), anotado y pendiente de confirmar
   contra la página.
3. **~~El campo `tirada`~~ → ✅ cerrado (2026-08-29).** Llegó a tener **15
   valores distintos para 6 tiradas posibles** porque ningún script lo consumía.
   Hoy tiene vocabulario cerrado, contraste contra su propia descripción, y la
   semántica de `Directo` **decidida y verificada en la página**.
   **El límite del modelo → ✅ resuelto el 2026-08-30 (Fase 14b-3).** *Símbolo*
   (6 modos), *Muro prismático* (7 capas), *Mano de Bigby* (4 modos, uno de
   ellos **tirada de ataque**) y *Muro de hielo* tienen ahora `tiradas`, una
   lista con la página de cada efecto. `tirada` sigue respondiendo a su pregunta
   —¿exige tirada para manifestarse?— y `validar_tiradas()` exige que lo
   declarado sea **exactamente** lo que pide el texto.
4. **La clave primaria sigue siendo el nombre en español con tildes.** No hay
   identificadores estables. Van **11 erratas de nombre corregidas**, todas
   parcheadas con `alias`. La peor, `Inflingir heridas` → **`Infligir heridas`**:
   «inflingir» no es una palabra, y el error **sobrevivió el mismo día a una
   auditoría de su descripción y a una corrección de su campo `tirada`** porque
   nadie miraba el nombre. El diseño volverá a fallar con cada tilde o sinónimo.
5. **~~`calculo.py` tiene reglas cableadas~~ → ✅ convertidas en dato
   (2026-08-29, Fase 14).** Y al quitarlas se vio que eran peores de lo que
   decían de sí mismas. `_CA_SIN_ARMADURA` llevaba el comentario «las dos únicas
   excepciones **en el tronco de clase**, confirmado por grep sobre las 12
   clases»: era cierto, y por eso mismo era el problema — **la base tiene cuatro
   fórmulas de CA base**, y las otras dos están en subclases. El grep miró donde
   el `lambda` sabía mirar.

   `bonus_pg_especie` falló de tres maneras a la vez: cubría **1 de los 2**
   efectos de PG de la base, guardaba un `1` fijo cuando el rasgo dice «y en 1
   más cada vez que subes de nivel», y **nadie obligaba a rellenarlo** — la
   única ficha de Enano lo tenía vacío y **verificaba en verde con los PG mal**.

   Hoy son 6 efectos citados que agrega `efectos.py`, con `validar_efectos()` y
   **20/20 por mutación**. **Queda un hueco declarado**, no tapado: la CA de
   quien no lleva nada (`10 + mod_des`) no tiene página citada en esta base, y
   el validador avisa hasta que se cierre.
6. **~~El proyecto no tenía control de versiones~~ → ✅ resuelto (2026-08-30).**
   Era la mayor fragilidad **operativa**, y no aparecía en ninguna lista porque
   no es un defecto de datos: durante semanas, un `sed` mal escrito sobre los
   391 conjuros no tenía vuelta atrás, y cada corrección de esta sesión se hizo
   sobre ficheros sin red. Hoy está en un repositorio privado con su historia.
   **Lo que esto habilita**, y es la razón de haberlo hecho ahora: revisión de
   código independiente sobre el diff — las ~1.400 líneas de módulos nuevos de
   la última tanda **no las ha revisado nadie**, y en ellas ya aparecieron
   cuatro defectos, **dos de ellos silenciosos**.
8. **🔴 La cobertura se escribía a mano, y por eso el motor no veía media
   base.** *(descubierto y medido el 2026-08-31)*

   `efectos._ORIGENES` era una tupla de 15 rutas literales: conocía **2 de las
   48 subclases** y **0 de los 4 ficheros de dotes**. Consecuencia medida, y
   estaba **invertida**:

   | Ficha | Veredicto antes |
   |---|---|
   | `Duro` (dote de origen, nivel 1) con su +2 PG aplicado — CORRECTA | ❌ rechazada |
   | `Duro` con el +2 perdido — ROTA | ✅ «0 problemas» |

   Es decir: el verificador **aprobaba la ficha mal y rechazaba la buena**, en
   el primer personaje que se crea, con una dote corriente del manual. 54 de
   las 75 dotes conceden «+1 a característica» y ninguna tenía dónde
   declararlo; `efectos.py` tampoco miraba `dotes/`.

   **Lo grave no es el fallo, es que es el mismo de la debilidad 5** un nivel
   más arriba. La cabecera de `reglas/efectos.yaml` condena las reglas
   cableadas —«no se entera de que hay una quinta»— y doce líneas después
   había una tupla cableada de RUTAS en vez de un diccionario cableado de
   FÓRMULAS. Se diagnosticó la enfermedad con precisión y se reprodujo en la
   línea siguiente.

   **Y apareció cinco veces en total**, en módulos escritos en momentos
   distintos: `_ORIGENES`, las cifras de `verificar_documentos`,
   `verificar_chequeos.FUENTES` (audita 3 de las 6 fuentes que declara),
   `verificar_srd.MAPA` (deja `pb` sin contraste externo) y
   `verificar_foundry.MODULOS`. Cuando el mismo defecto sale cinco veces sin
   que nadie lo copie, la causa es el método, no el despiste.

   ✅ **Cerradas las cinco** (2026-09-02, bloque A2): `verificar_chequeos`
   descubre sus fuentes y audita también `main` —lo que sacó a la luz 9 ramas
   que nadie miraba, en los tres ficheros que estaban en la lista sin aportar
   nada—; las columnas que `verificar_srd.MAPA` no puede cubrir están o
   contrastadas contra una tabla citada o declaradas una a una; y
   `verificar_foundry.MODULOS` tiene sus 9 categorías sin pedir medidas y
   declaradas como bloque H. La regla 6 ya no depende de que nadie se
   despiste: la cuenta `censo.py`.

   **La lección de fondo, que vale para todo el proyecto:** se verificaba con
   obsesión que **lo escrito fuera correcto** y nunca que **estuviera todo**.
   4395 valores contrastados y las mutaciones no dicen nada sobre los
   registros que ningún módulo llega a mirar.

9. **✅ CERRADA (2026-09-02) — los 30 chequeos `validar_*` ya tienen prueba
   por mutación.** Eran 11 de 30 el 2026-08-31.

   El bloque B del Plan 18 añadió tres suites: `mutaciones_aritmetica` 32/32 (5
   chequeos, empezando por `mejoras_de_dote`, que era deuda del mismo día),
   `mutaciones_contenido` 49/49 (11) y `mutaciones_referencias` 10/10 (3). La
   cifra **ya no se cuenta a mano**: la cuenta `censo.py`, que descubre los
   chequeos del AST de `validar.py` y las suites por patrón.

   **Lo que esto desbloquea:** un refactor es exactamente igual de seguro que
   la cobertura de pruebas de lo que se refactoriza. Con la red puesta, el
   bloque F ya es una opción real y no una apuesta.

   **Y lo que salió al tenderla, que es una debilidad nueva:** *dos de los
   treinta chequeos no pueden fallar.* `validar_costes_sin_fuente` y
   `validar_referencias` solo llenan `warn`. Una referencia rota entre una
   especie y `hechizos.json` sale como ⚠ y `validar.py` termina con «0
   errores». Está probado que el aviso salta; que además bloquee es una
   decisión pendiente.

   Y la estructura, medida, **no justifica un refactor**: mediana de 35 líneas
   por función en `validar.py`, 9 en `calculo.py`, y solo 5 de 47 funciones por
   encima de 120 líneas. Ninguno de los ocho defectos de la debilidad 8 lo
   causó la estructura; todos eran falta de una aserción de cobertura.

10. **✅ CERRADA (2026-09-02) — la regla inviolable 6 ya no es prosa.**
   *(era 🔴 desde el 2026-08-31, el mismo día en que se escribió)*

   `censo.py` la convierte en una cuenta: **867 unidades censadas, 0 sin
   declarar, 492 pendientes con su bloque y su motivo**. Siete clases de unidad
   —la séptima, los módulos de herramienta, la añadió el bloque A2—, siete
   universos descubiertos (glob, AST y el vocabulario de la base), y un
   manifiesto —`_verificacion/censo_exenciones.yaml`— donde lo que no se
   alcanza se declara una a una. Una declaración que ya no corresponda a
   ninguna unidad hace fallar al censo, así que el manifiesto tampoco puede
   pudrirse. Y tiene su propia prueba por mutación: **42/42**.

   Lo que sigue es el diagnóstico original, que conviene no perder:

   Se añadió «la cobertura se descubre, nunca se escribe a mano» a
   `CONTINUAR.md` tras encontrar ocho casos del defecto. **Nada la impide.**
   Puede aparecer el noveno mañana.

   Es literalmente la lección que este repo ya había registrado en
   `FUENTES.md:208` —*«una regla en prosa no impide nada»*— y que motivó
   escribir `verificar_chequeos.py`. Se diagnosticó el problema de las reglas
   en prosa, se convirtió una en script, y la siguiente nació en prosa igual.

   **La salida no es prohibir listas** (detectarlas en el AST daría falsos
   positivos con los mapas de traducción y los nodos del AST) sino una
   invariante contable: *toda unidad de la base tiene que estar alcanzada por
   nombre por algún chequeo, o declarada como no alcanzable con su motivo*.
   Eso es `censo.py`, el bloque A del Plan 18, y va antes que arreglar las
   cuatro listas que quedan: si se arreglan primero, se arreglan «las que
   alguien encontró»; con el censo, «las que hay».

11. **`hechizos.json` pesa 564 KB.** Cargarlo entero es el fallo «lost in the
   middle». `buscar.py` lo evita, pero hay que usarlo siempre.

## 🚀 Oportunidades

1. **Auditor con cita verificable.** El diferencial real: no «creo que puedes»,
   sino «puedes, por la pág. 51, y aquí está el texto».
2. **Chequeos baratos que no necesitan el manual, y que siguen dando.** Los
   tres añadidos el 29 de agosto encontraron **5 defectos reales en su primera
   ejecución** (dos resúmenes calcados, dos «tirada desalvación», y el vocabulario
   de `tirada`). Quedan ideas de la misma familia sin explotar: cotejar el campo
   `material` contra el paréntesis de la cabecera, o los nombres castellanos
   contra `nombre_en`.
3. **Superficies ya cerradas que no hay que repetir:** descripciones, nombres,
   resúmenes, `clases`, `tirada` y **el coste del material dentro y fuera del
   SRD**. No queda superficie de conjuro sin contrastar.
4. **Autosuficiencia real.** `PLACEHOLDERS_CONOCIDOS` está vacío: ninguna
   descripción remite ya al manual. El veto al conocimiento previo es
   comprobable, no aspiracional.
5. **RAG determinista sin embeddings.** Los campos para filtrar ya existen, y
   `buscar.py` falla ruidosamente ante 0 resultados.
6. **Nicho real:** D&D 2024 en español con esta trazabilidad no existe público.

## ⚠️ Amenazas

1. **~~Construir la Fase 14 sobre texto con un 16 % de error~~ → conjurada.**
   Era la razón por la que 13p bloqueaba a 14, y la medición resultó acertada: de
   haberla construido antes, el motor habría codificado **casi 50 reglas falsas
   con su cita de página al lado** — y **un error con página al lado es un error
   que nadie va a volver a comprobar**. La Fase 14 **ya no está bloqueada**.
2. **🔴 El CSV de origen sigue siendo la parte débil, y falla por vecindad.**
   Van **cinco** casos de contaminación entre conjuros *impresos uno al lado del
   otro* (`Aura sagrada`, `Polimorfar verdadero`, `Presciencia`, y los dos
   `Curar…en masa`). No es descuido de un transcriptor: es la geometría del CSV.
   `validar_vecindad()` lo vigila, pero **solo puede priorizar lectura, no
   decidir**: el manual repite texto de verdad entre conjuros hermanos.
3. **🔴 Una rama de tolerancia en un chequeo es deuda invisible.** Va por su
   **tercer** caso confirmado —y el tercero es el más ilustrativo: hasta el
   2026-09-02, `verificar_personaje.py` degradaba **cuatro** chequeos a aviso
   en cuanto la ficha traía más de una clase, y la ficha imprimía «✅ FICHA
   VERIFICADA — 0 problemas». El verificador aprobaba lo que no había mirado, y
   el cuarto chequeo degradado era precisamente el que cazaba los huecos del
   estrés con agentes. Cerrado en la fase 1 del `PLAN_19`: se rechaza.
   Los dos anteriores costaron semanas: `COSTE_COMPUESTO`
   sacaba seis conjuros del contraste externo y escondía dos sumas inventadas;
   el `continue  # entradas antiguas con ref:` de `verificar_categorias()` dejó
   que **nueve de diecisiete fichas** violaran la regla 6 del esquema, y esas
   fichas enseñaron el formato malo a todo el que vino después. Una exención se
   escribe de buena fe, deja de doler, y por eso deja de arreglarse. **Si se
   admite un formato viejo, la migración va en la misma tanda**; y si se aplaza,
   el aviso nombra los registros pendientes y converge a cero.
4. **Un campo con la forma correcta puede ser basura, y ningún chequeo de forma
   lo ve.** `3d0` pasó cuatro capas por ser sintácticamente un dado; una lista
   `clases` corta pasa por lista buena; un `resumen` falso pasa por prosa de
   sabor. **El patrón se repite y seguirá apareciendo en campos que hoy nadie
   mira.**
5. **Un informe de agente en blanco no prueba nada.** Y ya ha pasado: las
   oleadas 1-2 declaraban auditar el `resumen` y dieron **0 defectos en 131
   conjuros**, cuando la oleada 3 midió 5,8 %. La probabilidad de ese cero es
   **0,0004**. El campo estaba en el briefing y nadie lo miró.
6. **Un acierto por el método equivocado no vale.** Un auditor dedujo un defecto
   por aritmética y por el SRD inglés en vez de leer la página. Acertó, pero eso
   es indistinguible de acertar por casualidad.
7. **Deriva ficha↔base.** Si la ficha guarda texto copiado, al corregir la base
   los personajes quedan desincronizados en silencio. Guardar referencias.
8. **Legal.** Transcripción de material con copyright: uso personal. Lo único
   redistribuible es el SRD 5.2 (CC-BY-4.0) de `_verificacion/`.

---

## 🧭 El problema de fondo: cuándo parar de auditar

**Cada oleada descubre una superficie que nadie miraba.** La 1 descubrió el
campo `clases`; la 3, el `resumen` y los nombres de conjuro. Terminar la
oleada 4 no significará que el texto esté limpio — significará que las
*descripciones* lo están.

Si la condición para empezar la Fase 14 es «no encontrar nada», **no se cumple
nunca**. Conviene fijar el criterio por escrito antes de llegar:

> Cerrar la Fase 13p y la pasada de cabeceras, **medir el residuo**, y arrancar
> la Fase 14 aceptando ese residuo declarado — en vez de perseguir el cero.

**Las dos están cerradas (2026-08-29).** El criterio se cumplió: 305
descripciones y 302 cabeceras auditadas, 64 defectos corregidos, tasas medidas
con intervalo. **Queda arrancar la Fase 14** — y, si se quiere medir el residuo
de verdad, una muestra aleatoria nueva *después* de las correcciones, que es lo
único que diría cuánto error queda en lugar de cuánto había.

La base tiene lo que hace falta para decidir así: tasas con intervalo, no
sensaciones. Perseguir el cero con estas herramientas es más caro que declarar
el margen y seguir.

## 📏 Cómo se reproduce todo esto

```bash
python3 validar.py            # coherencia interna
python3 verificar_srd.py      # 646 valores contra el SRD
python3 verificar_foundry.py  # 3749 valores contra el SRD estructurado
python3 cobertura.py          # ¿puede responder?
python3 _verificacion/mutaciones_integridad.py   # 24/24
python3 _verificacion/mutaciones_efectos.py      # 36/36
python3 _verificacion/mutaciones_pg.py           # 13/13
python3 _verificacion/mutaciones_materiales.py   # 10/10
python3 _verificacion/mutaciones_tiradas.py      # 19/19
python3 _verificacion/mutaciones_prerrequisitos.py # 10/10
python3 _verificacion/mutaciones_subida.py       # 7/7
python3 _verificacion/mutaciones_nivel20.py      # 42/42
python3 _verificacion/intervalo.py 48 305 306    # la tasa del 15,7 % (antes de corregir)
python3 _verificacion/intervalo.py 4 36 306      # el residuo del 11,1 % (después)
```
