# Fase 13p — ✅ CERRADA el 2026-08-29

> Este fichero cubre la Fase 13p (descripciones) y las decisiones que salieron
> de ella. Lo posterior del mismo día —13q (nombres y resúmenes), 13r (costes
> de material) y **13s (la muestra POST-corrección)**— está en `CONTINUAR.md`
> y, con detalle, en `FUENTES.md`.
>
> **El número que importa hoy no es el 15,7 % de aquí, sino el residuo:
> ~11 % (IC 3,1-26,1) medido sobre texto YA corregido.**

Última actualización: **2026-08-29**. Todo el estado está aquí; no depende de
ninguna conversación.

## Plan

266 conjuros (los 306 emparejados con el SRD menos los 40 de la muestra 13o),
repartidos en **20 lotes contiguos por página** — manifiesto completo en
`LOTES_13p.md`, briefing en `LEEME_AGENTE_6.md`.

Motivo: la muestra aleatoria de la Fase 13o midió **17,5 % de error** en este
campo (`python3 _verificacion/intervalo.py 7 40 306`). No se puede empezar la
Fase 14 sobre este texto.

## Progreso

| Oleada | Lotes | Conjuros | Estado |
|---|---|---|---|
| 1 | A0, A1, A2, A3, A4 | 63 (libro 239-267) | ✅ **cerrada 2026-08-27**: 9 hallazgos verificados y aplicados |
| 2 | A5, A6, A7, A8, A9 | 68 (libro 268-293) | ✅ **cerrada 2026-08-27**: 10 hallazgos verificados y aplicados |
| 3 | B0, B1, B2, B3, B4 | 69 (libro 294-322) | ✅ **cerrada 2026-08-29**: 13 conjuros con defecto, 15 correcciones aplicadas. B1 y B4 se relanzaron (el 27 no llegaron a escribir informe) |
| 4 | B5, B6, B7, B8, B9 | 65 (libro 323-343) | ✅ **cerrada 2026-08-29**: 9 conjuros con defecto (13,8 %), 15 correcciones |

## ✅ Resultado final

**48 conjuros con defecto de 305 auditados = 15,7 %** (las cuatro oleadas más la
muestra aleatoria de la Fase 13o). IC 95 % exacto: **11,8 % – 20,3 %**.

| Oleada | Conjuros | Con defecto | Tasa |
|---|---|---|---|
| 13o (muestra aleatoria) | 40 | 7 | 17,5 % |
| 1 | 63 | 9 | 14,3 % |
| 2 | 68 | 10 | 14,7 % |
| 3 | 69 | 13 | 18,8 % |
| 4 | 65 | 9 | 13,8 % |
| **Total** | **305** | **48** | **15,7 %** |

**La muestra aleatoria acertó.** Midió 17,5 % sobre 40 conjuros y el valor final
es 15,7 %: bloquear la Fase 14 sobre esa base fue la decisión correcta. De haber
construido el motor de efectos sobre este texto, habría codificado **casi 50
reglas falsas con su cita de página al lado**.

**Ninguna oleada bajó de forma clara** (14,3 → 14,7 → 18,8 → 13,8 %): el defecto
estaba repartido por todo el capítulo. Era una propiedad del CSV de origen, no un
tramo mal transcrito.

**✅ El lote B5 (0 de 14) se remuestreó el 2026-08-29, y encontró 1 defecto
real:** *Rayo nauseabundo* llevaba un párrafo de mejora que la página no trae.
La regla «un informe en blanco no prueba nada por sí solo» queda validada con un
caso concreto, no solo por prudencia. Detalle en `FUENTES.md`.

**No queda ninguna oleada por lanzar.** Lo que sigue abierto son las decisiones
de la sección siguiente y el remuestreo de B5.

## Resultado de la oleada 1 (cerrada el 2026-08-27)

**9 hallazgos de agente, los 9 confirmados en la página, 0 rechazados.** Más la
corrección de *Nube de dagas* que venía pendiente de la lista de conversiones.
Tabla completa con página y evidencia en `FUENTES.md`, sección «Fase 13p —
oleada 1».

**Tasa observada: 9 defectos en 63 conjuros = 14,3 %**, coherente con el 17,5 %
que midió la muestra aleatoria de la Fase 13o (su IC 95 % era 7,3 %–32,8 %). La
proyección de ≈ 54 conjuros con error sobre los 306 **se sostiene**; no era un
artefacto de la muestra.

Dos modos de fallo nuevos, que conviene añadir a la lista del briefing:

7. **Regla inventada que tapa a la real.** *Creación* prohibía algo que el
   manual permite («no puedes usar un objeto creado para crear otro») y omitía
   la prohibición que el manual sí impone (el objeto creado hace fallar
   cualquier conjuro que lo use como componente material). No es un párrafo que
   falte ni una cifra cambiada: es una regla escrita que no existe.
8. **Lista de clases incompleta.** *Clarividencia* decía `["Mago"]` donde la
   cabecera dice «(bardo, clérigo, hechicero, mago)». **Ningún validador podía
   verlo**: `verificar_foundry.py` no contrasta el campo `clases`, y el chequeo
   `hechizos ⊆ clases` de `validar.py` solo detecta nombres inexistentes, no
   listas cortas. Una lista corta pasa por lista buena — el mismo modo de fallo
   que los placeholders y que `3d0`.

**Tarea que salió de aquí: ✅ hecha el 2026-08-27.** El módulo
`conjuros-clases` de `verificar_foundry.py` contrasta el campo `clases` contra
el SRD 5.2 en Markdown (Foundry no publica ese campo). **278 conjuros, 2
discrepancias**: *Engañar* —que un agente encontró el mismo día leyendo la
página, dos métodos independientes— y *Potenciar característica*, que solo vio
el script. Deduce el vocabulario de clases por solapamiento de conjuntos y
exige biyección; el margen es amplio (peor pareja correcta J=0,974, mejor
pareja falsa 0,588). Detalle en `FUENTES.md`.

## Resultado de la oleada 3 (cerrada el 2026-08-29)

**13 conjuros con defecto en 69 auditados (18,8 %), 15 correcciones aplicadas,
0 hallazgos rechazados.** Cinco lotes (B0-B4) y cuatro verificadores ciegos
(V3, V4, V6, V7). Tabla completa con página y evidencia en `FUENTES.md`.

Lo que estrenó esta oleada, y conviene arrastrar al briefing de la oleada 4:

- **El campo `resumen` es superficie auditable, no decoración.** Cuatro de los 15
  defectos estaban ahí, y todos **contradecían la `descripcion` correcta que
  llevan al lado**: un acierto automático que no existe (*Impacto certero*), una
  excepción negada (*Muro de fuerza*), un estado renombrado (*Palabra de poder:
  aturdir*) y un resumen que era el del conjuro vecino (*Presciencia*).
- **Los nombres de conjuro también fallan.** *Poliformar* → **Polimorfar**, con m,
  en dos registros. **Lo vio el verificador, no el auditor**, porque transcribía
  la cabecera entera a ciegas. Pide siempre la cabecera completa.
- **Contaminación por vecindad tipográfica, dos veces en un lote.** *Polimorfar
  verdadero* llevaba reglas de *Polimorfar*, y *Presciencia* el resumen de
  *Presencia regia de Yolande* — los dos impresos al lado en la misma página.
  Con *Aura sagrada* de la Fase 13o van tres. **No es casualidad: es el modo de
  fallo estructural del CSV de origen.**
- **El campo `tirada` puede contradecir a su propia descripción.** *Inflingir
  heridas* decía «TdS Sab.» mientras su texto pedía Constitución. Eso se detecta
  con una regex, sin abrir el manual.
- **Un auditor razonó donde debía leer.** Dedujo que «13000 pies²» era falso por
  aritmética y por el SRD inglés. Acertó, pero **un acierto por el método
  equivocado no se distingue de un acierto por casualidad**: el briefing del
  verificador debe prohibir expresamente razonar en vez de transcribir.

## Resultado de la oleada 2 (cerrada el 2026-08-27)

**10 hallazgos, los 10 confirmados por una segunda lectura ciega.** Los peores:
*Geas* tenía la regla **invertida** («falla» donde el manual dice «supera»
automáticamente) y *Dominar monstruo* concedía un **control total del objetivo
que la página no da** — segundo caso del modo de fallo 7, tras *Creación*.

Modo de fallo 8 confirmado dos veces más (*Engañar*, *Potenciar
característica*): **el campo `clases` era la superficie ciega que nadie
miraba.** Ya tiene chequeo automático.

## Cómo se verifica un hallazgo (reparto de modelos)

La regla «releer personalmente la página antes de aplicar» sigue vigente, pero
**la lectura la hace un agente Sonnet, no Opus** (ahorro de tokens; leer no
necesita el modelo grande, decidir sí). Se cumple así:

1. El agente auditor informa. **No edita nada.**
2. Un **segundo agente Sonnet independiente** relee la página del hallazgo sin
   ver el informe del primero.
3. Opus compara los dos informes, decide y aplica.

Dos lecturas independientes que coinciden valen como verificación. Lo que no
vale es aplicar el hallazgo de un solo agente sin contraste — la regla nació de
que un agente acertó un hallazgo e **inventó la causa** (las páginas duplicadas
del Druida, falso, comprobado píxel a píxel).

## Hallazgo transversal encontrado por código (no por agentes)

Barrido aritmético de **las 342 conversiones de unidad** de `hechizos.json`
(«N m / M pies»): **6 son falsas**. La base añade equivalencias en pies que el
manual no trae y varias están mal calculadas.

| Conjuro | Dice la base | Debería | Estado |
|---|---|---|---|
| Pasamuros | «1,5 m / 45 pies» | ~4,9 pies | ✅ **corregido**; reconfirmado por el lote B3 (2026-08-29) |
| Telaraña | «1,5 m / 20 pies» | — | ✅ **cerrado 2026-08-29**: B8 leyó pdf 339 y la página solo dice «6 m de lado» y «1,5 m»; **no imprime ningún pie**. La conversión de la base es correcta de cálculo pero añadida |
| Ráfaga de viento | «2 m / 7,5 pies» | — | ✅ **cerrado 2026-08-29**: B5 leyó pdf 325-329, todas métricas, y verificó las conversiones del conjuro una a una: correctas |
| **Nube de dagas** | «cubo de 1,5 m / 10 pies» | la página dice solo «**un cubo de 1,5 m**», sin conversión; 1,5 m son 5 pies | ✅ **APLICADO 2026-08-27** (pdf 316 = libro 314) |
| Disco flotante de Tenser | «90 cm / 1 pie» (×2) | — | ✅ **cerrado 2026-08-29**: V5 leyó pdf 273 y la página **no da ninguna conversión**; se eliminaron las 6 del conjuro (criterio de *Nube de dagas*) |
| Disco flotante de Tenser | «2,5 cm / 1 pulgada» | correcto (0,98) — falso positivo de la primera versión del chequeo | ✅ descartado |

**Dato incómodo:** `Nube de dagas` y `Disco flotante de Tenser` **pasaron limpios
la Fase 13m**. El briefing de aquella tanda no mencionaba las conversiones de
unidad, así que nadie las miró. **Los 85 conjuros fuera del SRD necesitan una
pasada solo de conversiones**, aunque su texto ya se auditara.

## ✅ El chequeo de conversiones ya es permanente

`validar_conversiones()` vive en `validar.py` y contrasta hoy **556
equivalencias** en verde, con tolerancia **absoluta** (media unidad) y no
relativa — la primera versión, con un 2 % relativo, dejaba pasar «30 m / 98
pies» y saltaba con un redondeo de 0,03. El factor va **desde metros**
(1 m = 3,28084 pies = 39,3701 pulgadas = 1,09361 yardas = 1/1609,344 millas).

## 🔶 Decisiones pendientes

**Solo queda una** (las otras dos se cerraron el 2026-08-29 y se conservan
abajo tachadas, con lo que se decidió y por qué).

### 1. Las conversiones a pies — 🔴 la evidencia ya es concluyente

**23 páginas del capítulo de conjuros, leídas por nueve lectores distintos que
no se conocían entre sí, no imprimen ni una sola unidad imperial.**

| Quién | Páginas pdf |
|---|---|
| Oleadas 1-2 | 284, 316 |
| V3, V5, V6, V7 | 273, 306, 312, 324 |
| Opus (relectura directa) | 248, 329, 331, 343 |
| B5 | 325, 326, 327, 328, 329 |
| B6 | 329, 330, 331 |
| B7 | 332-337 |
| B9 | 343, 344, 345 |

**23 páginas muestreadas de las 107 del capítulo (21 %), cero positivos.** El
límite superior 95 % de la proporción de páginas que podrían imprimir pies y
habérsenos escapado es del **12,2 %** — y para que las ~550 conversiones de la
base fueran del manual, la proporción tendría que ser cercana al 100 %.

**Conclusión: las conversiones imperiales de `descripcion` las añadió la base,
todas.** Aritméticamente correctas —`validar_conversiones()` funciona— pero
**editoriales**. `validar_conversiones()` comprueba que estén bien calculadas;
**nadie comprueba que deban existir**.

#### Qué se ha hecho ya (opción b, la no destructiva)

`hechizos.json` lleva en `_meta` una **`_conversiones_nota`** que declara sin
rodeos que las equivalencias imperiales no son texto del manual, con las páginas
que lo demuestran, y `_meta.fidelidad` dice `mixto`. **La base ya no presenta
como cita algo que no lo es**, que era el problema de fondo.

#### Lo que queda por decidir (opción a): ¿se quitan del texto?

Es una preferencia editorial, no una corrección: si se quieren pies en mesa, la
nota ya avisa de que son nuestros. Si se prefiere que `descripcion` sea
métrica como el manual, el cambio es mecánico y está medido — **330
equivalencias en 178 conjuros**. Se han ido quitando de una en una según las
tocaba una auditoría (*Nube de dagas*, *Disco flotante de Tenser*, *Prohibición*,
*Jaula de fuerza*, *Mensajero animal*, *Tsunami*, *Atadura planar*), que es lo
peor de las dos opciones: deja la base a medio camino.

**Si se decide (a), el barrido es este** (hacer copia antes; `alcance` NO se
toca, que ahí `metros`/`pies`/`casillas` es estructura propia y deliberada):

```python
import json, re
d = json.load(open('hechizos.json', encoding='utf-8'))
RE = re.compile(r'(\d[\d,\.]*\s*(?:m|cm|km))\s*/\s*[\d,\.]+\s*'
                r'(?:pies|pie|pulgadas?|yardas?|millas?)')
for c in d['hechizos']:
    c['descripcion'] = RE.sub(r'\1', c['descripcion'])
```

### 2. ~~La semántica de `tirada: "Directo"`~~ → ✅ **decidida (2026-08-29)**

> **`TdS <car.>`** = la salvación **decide si el conjuro afecta al objetivo**.
> **`Directo`** = el conjuro **se manifiesta igualmente**; las salvaciones
> posteriores modulan el daño o liberan de un estado ya aplicado.

Deducida de los datos (los conjuros gemelos coinciden; la primera salvación cae
en la mediana del 24 % del texto en los `TdS` y del 48 % en los `Directo`).
**4 correcciones**: *Mal de ojo*, *Levitar*, *Polimorfar verdadero* y *Tormenta
de la venganza* pasan a `TdS`. Los otros 10 candidatos, confirmados correctos.
Detalle en `FUENTES.md`.

**El juicio no se automatiza** —se intentó por posición y por estructura del
texto, y ambos fallaron— así que el chequeo **avisa de lo no revisado**:
`_tirada_revisada` marca los verificados y el aviso está **hoy en cero**.

**Y deja un aviso para la Fase 14:** *Símbolo* (6 modos) y *Muro prismático*
(7 capas) tienen **una salvación distinta por efecto**. Un conjuro no tiene «una
tirada»: tiene efectos, y cada uno la suya. El modelo de efectos debería nacer
sabiéndolo.

### 3. ~~Cerrar el vocabulario del campo `tirada`~~ → ✅ **hecho (2026-08-29)**

`validar_tirada()` cierra el vocabulario a los 9 valores válidos **y** contrasta
el campo contra la salvación que pide su propia `descripcion` — el defecto de
*Inflingir heridas* se caza ya sin abrir el manual. `TdS Int. propia`
(*Contactar con otro plano*, donde la salvación la hace el lanzador) queda como
**excepción declarada y control negativo** de la prueba por mutación: si alguien
la «normaliza», la base pierde algo que el manual sí distingue.

Los 53 `Directo` con salvación en el texto salen como **aviso, no error**:
marcarlos como error sería contestar la decisión 2 por la puerta de atrás.

**Lo que sigue abierto de este campo es solo la semántica de «Directo»**
(decisión 2 de arriba).

## 📌 Modo de fallo nuevo (oleada 3): el campo `resumen`

**Tres de los siete hallazgos de la oleada 3 estaban en `resumen`**, un campo que
hasta ahora nadie auditaba por considerarlo prosa de sabor. Los tres
**contradecían la `descripcion` correcta que llevan al lado**: *Impacto certero*
prometía un acierto automático que la página no da, *Muro de fuerza* negaba la
excepción de *desintegrar* que la página nombra, y *Palabra de poder: aturdir*
llamaba «paraliza» a un estado que el manual distingue de «aturdido».

**Un resumen falso es una regla falsa en el sitio donde más probable es que
alguien se pare a leer.** Añádase a la lista de superficies auditables del
briefing de la oleada 4.


## 🔧 Chequeos permanentes añadidos el 2026-08-29

Tres, todos en `validar.py`, ninguno necesita el manual, probados por mutación
en `_verificacion/mutaciones_integridad.py` → **24/24** (la mitad, controles
negativos). **Encontraron 5 defectos reales en su primera ejecución.**

| Chequeo | Error duro | Aviso |
|---|---|---|
| `validar_tirada()` | valor fuera del vocabulario; `tirada` que contradice a su propia descripción | los 53 `Directo` con salvación |
| `validar_vecindad()` | `resumen` **idéntico** entre dos conjuros de la misma página | solapamiento ≥34 % de texto, ordenado por gravedad |
| `validar_ortografia()` | inglés sin traducir; palabras pegadas | — |

**Por qué el de vecindad solo avisa.** Su primera versión daba **15 falsos
positivos**: el manual repite texto de verdad entre conjuros hermanos
(*Dominar persona*/*Dominar monstruo*, *Inmovilizar persona*/*Inmovilizar
monstruo* comparten párrafos **porque así están impresos**). Ninguna medida de
solapamiento distingue «el manual repite» de «el CSV calcó» sin abrir la página.
Lo único que se dejó como error duro es el `resumen` idéntico, que no tiene
lectura inocente: los resúmenes los escribimos nosotros, uno por conjuro.

**Los tres avisos de solapamiento se cerraron el 2026-08-29 (V12): las tres
parejas son LEGÍTIMAS** — el manual las imprime así, y la base conserva todas
las diferencias reales (nivel, clases, alcance, objetivos, coste, escalado).
Llevan `_vecindad_verificada`, y el chequeo ya no vuelve a pedir la misma
lectura: si no, el aviso pediría releerlas para siempre hasta ser ruido que
nadie mira.

### Lo que enseñó escribirlos

- **La prueba por mutación encontró un defecto que el chequeo no veía.** Salió
  18/21: dos fallos eran de las mutaciones (probaban un chequeo de vecinos con
  conjuros de páginas distintas) y **uno era real** — la partición de palabras
  empezaba en la letra 3 y no veía «elconjuro». Al bajarla a 2 aparecieron **las
  dos «tirada desalvación»** de *Hacer añicos* y *Estática sináptica*.
- **Un campo vacío puede ser peor que uno falso.** El resumen calcado de las dos
  curaciones («La sanación alcanza a todos») era tan genérico que **servía por
  igual a los dos conjuros**. No era falso de un modo visible: era vacío, y por
  eso ninguna lectura lo había marcado.
- **Los falsos positivos se declaran uno a uno, no se ahogan subiendo umbrales.**
  La señal es tan escasa (2 defectos reales en 782 campos) que perderla saldría
  más caro que mantener una lista de excepciones con nombre y razón.
