> # ⛔ DOCUMENTO OBSOLETO — archivado el 2026-08-29
>
> **No lo uses para decidir nada.** Se conserva solo como registro de en qué
> estado se creía que estaba la base el 2026-08-19, y de qué se aprendió desde
> entonces. El análisis vigente está en **`FODA.md`**.
>
> Qué quedó desfasado, y por qué importa:
>
> - **Debilidad 1 («155 rasgos de clase sin texto») → cerrada.** Los 158 rasgos
>   del tronco tienen texto desde la Fase 10.
> - **Debilidad 2 («bug `Clerigo` sin tilde») → cerrada.** Hoy hay 0 apariciones
>   de `"Clerigo"` en la base, y `validar_hechizos_clases()` cruza los 391
>   conjuros contra los nombres de clase reales.
> - **Debilidad 4 («no existe la capa de recuperación») → cerrada** por
>   `buscar.py`, que además falla ruidosamente ante 0 resultados.
> - **Debilidad 3 («fidelidad mixta y no declarada») → cerrada el 2026-08-29**,
>   que era la única que seguía viva.
> - **Su «Conclusión operativa» manda hacer las Fases 9c y 10, ambas cerradas.**
>   Ese es el motivo real de archivarlo: quien lo leyera y le hiciera caso
>   trabajaría una semana hacia atrás.
> - La sección «Margen de error» ya se marcó desfasada el 2026-08-22, y hoy lo
>   está aún más: no conocía la tasa del 17,5 % de las descripciones de conjuro.

# FODA — la base canónica como sustrato de un orquestador LLM

> Fecha: 2026-08-19. Sustituye al análisis de `~/Downloads/Analisis_Base_Canonica_DnD.md`,
> escrito cuando las Fases 5, 6 y 3 seguían abiertas (sus tres "Debilidades"
> ya están cerradas: dotes, equipo y 48/48 subclases).
> Premisa: **todo lo interpretativo lo ejecuta un LLM**; la base es su única
> fuente de verdad y el código, su calculadora y su filtro.

Todo lo que sigue está medido sobre la base real, no estimado.

---

## 💪 Fortalezas

1. **Trazabilidad por dato, no por archivo.** Cada clase, subclase, dote,
   conjuro, especie y trasfondo lleva su página. Esto es lo que hace
   *verificable* la directiva de auditor "denegado por defecto, cita la regla":
   un humano puede abrir el PDF y comprobar la cita. Sin esto, el auditor sería
   teatro.
2. **Invariantes cruzados y probados por mutación.** `validar.py` no repite el
   dato del manual: cruza tablas transcritas por separado (el conjunto estándar
   cuesta exactamente los 27 puntos de la compra por puntos; la tabla multiclase
   coincide con la del lanzador completo; la característica principal concuerda
   en tres sitios). Se probó con 8 corrupciones deliberadas: 8 detectadas.
3. **Edición sellada y cuarentena explícita.** Cada archivo declara
   `edicion: "2024 (5.5e)"`. El 2014 está documentado como veto, no como olvido.
4. **Estructura ya apta para recuperación barata.** Los conjuros tienen `nivel`,
   `clases`, `componentes`, `concentracion`, `ritual`, `escuela` como campos.
   Se puede filtrar con un `if` determinista y reproducible — sin embeddings,
   sin similitud, sin sorpresas.
5. **La matemática ya es dato, no prosa.** Progresión, espacios de conjuro,
   compra por puntos y multiclase están en tablas. El LLM no tiene que sumar
   nada: puede pedirle el número al código.

## 📉 Debilidades

1. **🔴 155 rasgos de clase base existen solo como nombre, sin texto.**
   La base sabe que un bárbaro de nivel 1 tiene "Furia", "Defensa sin armadura"
   y "Maestría con armas" — pero **no sabe qué hacen**. Ídem "Ataque furtivo",
   "Acción súbita", "Imponer las manos", "Artes marciales". Las subclases sí
   tienen texto (`desc`), las dotes también (`descripcion`), los conjuros
   también. El hueco está exactamente en el tronco de las 12 clases.
   *Es la debilidad que bloquea todo lo demás, y la explico en Amenazas.*
2. **🔴 Bug referencial vivo: `Clerigo` sin tilde.** En `hechizos.json` los 116
   conjuros de clérigo están etiquetados `"Clerigo"`, mientras toda la base usa
   `Clérigo`. Un filtro por el nombre canónico **devuelve 0 resultados**.
   Además, `Hablar con animales` no tiene ninguna clase asignada.
   `validar.py` no lo detecta: nunca cruza `hechizos.clases` con los nombres
   de clase reales.
3. **Fidelidad mixta y no declarada.** Los conjuros son transcripción literal
   del manual; las dotes y subclases son resúmenes condensados ("Mejora de
   característica: Destreza +1 (máx. 20). Visión ciega hasta 3 m…"). Un auditor
   al que se le exige "citar textualmente" citará, según el caso, o el manual o
   una paráfrasis nuestra — y nada en el archivo distingue una cosa de la otra.
4. **No existe todavía la capa de recuperación.** `hechizos.json` son 435 KB,
   ~111 000 tokens: cargarlo entero es justo el fallo "lost in the middle" que
   el análisis original anticipaba. El filtro que lo evita está diseñado, no
   escrito.
5. **La clave primaria es el nombre en español con tildes.** No hay
   identificadores estables. La debilidad 2 es precisamente ese diseño fallando
   una vez; volverá a fallar con cada tilde, mayúscula o sinónimo.
6. **No hay ficha de personaje ni catálogo legible por máquina.** El
   orquestador no tiene forma de descubrir qué contiene la base sin que alguien
   se lo cuente en el prompt.

## 🚀 Oportunidades

1. **Auditor con cita verificable.** Es el diferencial real frente a cualquier
   chatbot de D&D: no "creo que puedes", sino "puedes, por la pág. 51, y aquí
   está el texto". Ya hay página en todo; falta exigirlo en el prompt.
2. **Autosuficiencia total al cerrar los 155 rasgos.** Con ese hueco cubierto,
   el LLM puede operar con el conocimiento previo **vetado al 100 %**, que es la
   única manera de que el veto sea comprobable en lugar de aspiracional.
3. **RAG determinista sin embeddings.** Los campos para filtrar ya existen. Un
   recuperador de 100 líneas da resultados reproducibles y auditables — mejor
   que una búsqueda semántica para un dominio de reglas cerradas.
4. **Detector de combos RAW.** Solo es posible *después* de tener el texto de
   los rasgos base: hoy se puede cruzar maestrías × dotes, pero no
   maestrías × rasgos de clase, que es donde viven los combos interesantes.
5. **La ficha como registro de decisiones citadas**, no como estado. Si cada
   elección guarda la regla y la página que la autorizó, el personaje se vuelve
   auditable y reconstruible, y el "retraining" de 2024 (cambiar conjuro o
   maestría al subir) tiene contra qué comprobarse.
6. **Nicho real:** D&D 2024 en español con esta trazabilidad no existe público.

## ⚠️ Amenazas

1. **🔴 La amenaza compuesta: D1 × pre-entrenamiento.** El hueco de los 155
   rasgos coincide **exactamente** con las reglas que el LLM cree conocer mejor
   de 2014 — y varias cambiaron en 2024 (Furia, las condiciones del Ataque
   furtivo, y las Maestrías de arma, que directamente no existían). El modelo no
   dirá "no lo tengo": rellenará el hueco con algo fluido, plausible y de la
   edición vetada. Es el fallo más probable, el más silencioso y el que ocurre
   ya en el nivel 1.
2. **Un filtro roto es peor que ningún filtro.** El bug `Clerigo` devuelve una
   lista vacía, no un error. Un orquestador que recibe "0 conjuros" concluye que
   no hay, y improvisa. Todo recuperador debe **fallar ruidosamente** ante 0
   resultados en un caso donde debería haberlos.
3. **Complacencia (el "yes-man").** Sigue vigente lo que decía el análisis
   original, con un matiz: el rol de auditor estricto solo funciona si hay texto
   que citar. Mientras falten los 155 rasgos, exigir cita en esos casos deja al
   modelo eligiendo entre desobedecer o inventar la cita.
4. **Deriva ficha↔base.** Si la ficha guarda el texto copiado de un rasgo, al
   corregir la base todos los personajes quedan desincronizados en silencio.
   Guardar referencias (`clase+nivel+nombre`), nunca copias.
5. **Legal.** Esto es transcripción de material con copyright: uso personal. Lo
   único redistribuible es el SRD 5.2 (CC-BY-4.0) de `_verificacion/`.
6. **Erosión del método en la Fase 8.** Es la primera fase sin página que
   citar. El riesgo es que la disciplina "consultar, no recordar" se relaje
   justo cuando se escribe el código que decide qué se autoriza.

---

## 📏 Margen de error de la base (medido el 2026-08-21)

No hay **un** margen de error: hay dos poblaciones con procedencias distintas
y tasas que difieren en un orden de magnitud, más una superficie que nadie ha
comparado con nada. Todo lo que sigue está medido, no estimado; los intervalos
son Clopper-Pearson exactos al 95 %.

### 1. Lo que viene del CSV (los 391 conjuros)

| Unidad | Medido | IC 95 % |
|---|---|---|
| por conjuro | 9 malos / 304 contrastados = **2,96 %** | 1,36 % – 5,55 % |
| por valor | 16 / 1.824 = **0,88 %** | 0,50 % – 1,42 % |

> ⚠️ **Estas cifras quedaron desfasadas el 2026-08-22.** Miden solo los campos
> que el SRD contrasta (cabecera y banderas). La **descripción** de los conjuros
> se midió aparte en la Fase 13o con una muestra aleatoria de 40: **17,5 % de
> error por conjuro** (IC 95 % 7,3 % – 32,8 %), ≈ 54 conjuros malos de 306.
> Es un orden de magnitud peor y es la cifra que manda. Ver `CONTINUAR.md`.

Los 9 están corregidos. El residuo vive en los **87 conjuros que el SRD no
cubre**: proyectando la misma tasa quedan **≈ 2,6 conjuros con error** (entre
1,2 y 4,8). Es la parte débil de la base, y van **tres veces** que este CSV
falla: el duplicado de *Hablar con animales*, la escuela ausente del
*Sanctasanctórum* y ahora estos nueve. **«Datos ya estructurados» no significa
datos correctos** — de hecho salió peor parado que la lectura visual.

### 2. Lo que viene de lectura visual

| Superficie | Medido | IC 95 % |
|---|---|---|
| tablas de clase | 0 / 646 | 0 % – 0,57 % |
| armas, armaduras, especies, dotes, trasfondos | 0 / 233 | — |
| **conjunto (contraste externo)** | **0 / 879** | **0 % – 0,42 %** |
| rasgos de clase (auditoría visual, 2026-08-21) | 10 / 158 = **6,3 %** | 3,1 % – 11,3 % |
| subclases (auditoría visual, 2026-08-21) | 4 / 48 = **8,3 %** | 2,3 % – 20,0 % |
| especies (auditoría visual, 2026-08-21) | 0 / 10 | 0 % – 30,8 % |

Un orden de magnitud mejor que el CSV en lo numérico. Pero la fila de los
rasgos de clase es la que de verdad enseña algo: al releerlos uno a uno
aparecieron **10 defectos en 158**, un 6,3 %. Nueve eran **citas de página**
—invisibles a cualquier contraste numérico, porque el dato citado era
correcto— y uno era prosa equivocada. Es la prueba directa de lo que dice el
apartado 4: el 0 % de la fila de arriba mide una cosa distinta de la que
falla.

### 3. La superficie que nadie ha contrastado

Ya es pequeño. **Cerrado el 2026-08-21:** dotes y trasfondos (estructura),
los 158 rasgos de clase, las 48 subclases con sus 241 rasgos, las 10 especies
con sus 38 rasgos y 14 linajes, las 25 herramientas, y tres de los ocho campos
sueltos de los conjuros (alcance, duración, tiempo de lanzamiento). **Queda sin
comparar con nada:**

- **5 campos de los 391 conjuros** (clases, tirada, resumen, descripción, y el
  material concreto de los componentes)
- 121 objetos de equipo de aventurero y munición
- la **descripción** de las 75 dotes y el equipo inicial de los 16 trasfondos
  (lo contrastado es su estructura, no su texto)
- **los 87 conjuros que el SRD no cubre**, que siguen siendo el residuo medido

De las tres auditorías visuales salieron **14 defectos**, y el patrón es
inequívoco: **13 eran citas de página** y solo **uno era contenido** (la nota
del Pícaro). El texto mecánico de 158 rasgos de clase, 241 de subclase y 38 de
especie resultó correcto. La lectura visual original era buena; lo que fallaba
sistemáticamente era **dónde decía que estaba cada cosa** — justo el dato que
sostiene la promesa de auditabilidad del proyecto, y el único que ninguna
fuente externa puede comprobar.

### 4. El matiz que impide fiarse del 0,42 %

Ese cero cubre **cifras y banderas**, no prosa ni citas. Y los defectos que
históricamente han aparecido en material de lectura visual eran precisamente de
otro tipo: las dos citas de página falsas del Clérigo, la interpretación de las
habilidades del Bardo, el idioma inventado en `_ejemplo_aerin.yaml`. **Ninguno
lo habría cazado un contraste numérico** — la de las citas la pilló un
invariante interno, no el SRD.

Conclusión: *0 errores en 879 valores numéricos* ≠ *la lectura visual está
limpia*. Significa que su parte numérica lo está.

### 5. Traducido al uso real

- **Lanzador de nivel 1 que elige ~6 conjuros:** ≈ **3,9 %** de que algún dato
  mecánico esté mal (≈1,3 de sus conjuros salen del tramo sin contrastar).
- **No lanzador:** tabla de clase, armas, armaduras, especie, dote y trasfondo
  están contrastados con 0 errores. Su riesgo residual está en el **texto** de
  los rasgos de clase, que es ciego.

### 6. Qué bajaría el margen, y cuánto cuesta

| Acción | Cierra | Coste |
|---|---|---|
| 8 campos restantes de los conjuros contra `spells24` | ~2.400 valores más | bajo (mismo pack, código nuevo) |
| Equipo restante contra `equipment24` | 146 objetos | bajo |
| ~~Los 87 conjuros fuera del SRD~~ | ✅ auditados (Fase 13m, 2026-08-22) | |
| **Las 266 descripciones de conjuro sin auditar** | **el residuo real: 17,5 % medido** | **lectura visual, sin atajo** |
| **Rasgos de clase, subclases, rasgos de especie** | la mayor superficie ciega | **lectura visual, sin atajo** |

Las dos últimas no tienen alternativa: el SRD no las cubre, así que ninguna
fuente externa puede confirmarlas. Solo la página del manual.

---

## Conclusión operativa

La base es **fuerte donde se la ha auditado y ciega donde no se ha mirado**. Las
fortalezas son reales y medidas; las dos debilidades marcadas en rojo son
bloqueantes y, hasta cerrarlas, cualquier skill construida encima produce
personajes contaminados con 2014 desde el nivel 1 — sin avisar.

Orden recomendado antes de la Fase 8:

1. **Fase 9c — arreglar la integridad de `hechizos.json`** (barato: normalizar
   `Clerigo`→`Clérigo`, asignar las clases de `Hablar con animales` leyendo su
   página, y añadir a `validar.py` el cruce `hechizos.clases ⊆ clases/*.yaml`
   más un aviso ante listas vacías).
2. **Fase 10 — transcribir el texto de los 155 rasgos de clase base**, por
   lectura visual, con página, como se hizo con subclases y dotes. Es la fase
   más larga que queda y la que convierte la base en autosuficiente.
3. **Fase 8 — skills**, ya sobre una base que no necesita que el LLM "sepa" D&D.

Y una decisión de diseño que conviene tomar antes de escribir la ficha: marcar
en cada texto si es **literal** o **condensado**, para que el auditor sepa qué
está citando.
