# Hallazgos — creación de Milo Candado (Mediano / Pícaro / Criminal, nivel 1)

## 1. Qué funcionó bien

- `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasan
  limpios (0 errores) antes de empezar; la base está en estado fiable.
- `python3 buscar.py clase Pícaro` da absolutamente todo lo necesario para el
  tronco base: `atributos_basicos` completo (dado de golpe, salvaciones,
  habilidades a elegir, armas, armaduras, herramientas, equipo inicial A/B) y
  la progresión 1-20 con `ataque_furtivo`. Confirma que Pícaro **no** es
  lanzador (`"lanzador": "ninguno"`) y que sí tiene
  `atributos_basicos.herramientas: ["Herramientas de ladrón"]`, como pedía la
  tarea.
- `python3 buscar.py trasfondo Criminal` y la lectura directa de
  `especies/especies.yaml#Mediano` dieron datos limpios y sin ambigüedad
  (Mediano no tiene ninguna elección interna, así que
  `rasgos_elegidos: {}` es correcto).
- `python3 calculo.py pg/ca/pb` calcularon PG=10 (d8 + mod Con +2), CA=14
  (11 armadura de cuero + mod Des +3) y PB=2 sin que tuviera que sumar nada
  a mano.
- `clases/rasgos/picaro.yaml` documenta con detalle el rasgo "Jerga de
  ladrones" (concede el cant + un idioma de elección) y "Pericia" (con la
  recomendación explícita de doblar Juego de manos y Sigilo), lo que permitió
  tomar esas decisiones citando la fuente exacta.
- `python3 verificar_personaje.py personajes/mediano_picaro.yaml` terminó en
  **0 problemas** tras los ajustes descritos en el punto 2.

## 2. Bugs o comportamientos raros de las herramientas

### 2.1. `verificar_sin_copias` en `verificar_personaje.py` contradice la regla 5 del propio `_ESQUEMA.md`

La regla 5 del esquema dice:

> Ningún campo fuera de `decisiones[].cita` puede contener un fragmento de
> más de ~15 palabras que **coincida con una `desc` de la base**: eso es
> señal de que se copió texto en vez de referenciarlo.

Pero la implementación (`verificar_personaje.py`, función
`verificar_sin_copias`, líneas ~188-205) **no compara contra ningún texto de
la base**. Simplemente cuenta palabras de *cualquier* string de la ficha
(fuera de `decisiones[].cita`) y falla si supera 15, sin importar si el
contenido es prosa libre legítima (`historia`, `personalidad`, que el propio
esquema declara exentas: *"La única prosa libre permitida es... nombre,
historia personal, descripción física, personalidad"*) o una explicación de
`decisiones[].eleccion` que no copia nada de la base.

Comando y salida exacta que lo disparó (primera versión de mi ficha, antes de
ajustarla):

```
$ python3 verificar_personaje.py personajes/mediano_picaro.yaml
17 referencias comprobadas.
❌ 8 problemas:
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'método de características: conjunto estándar, repartido segú'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'ajuste de trasfondo: +2 Destreza, +1 Constitución (de las tr'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'habilidades de clase: Percepción, Perspicacia, Engaño, Inves'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'herramienta de trasfondo: herramientas de ladrón (fija, no e'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'idiomas libres adicionales (todo personaje sabe común + otro'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'equipo inicial de clase opción A (armadura de cuero, 2 dagas'…
  ✗ posible texto copiado en 'historia' (>15 palabras seguidas): 'Milo creció robando bolsillos en los muelles de una ciudad p'…
  ✗ posible texto copiado en 'personalidad' (>15 palabras seguidas): 'Encantador y calculador a partes iguales: sonríe primero y e'…
```

Ninguno de esos ocho fragmentos coincide con texto real de la base (lo
comprobé leyendo `clases/rasgos/picaro.yaml`, `trasfondos/trasfondos.yaml` y
`reglas/idiomas.yaml`: no hay ningún `desc` parecido). Son puro texto
original mío. El chequeo los marca solo por longitud.

**Cómo lo esquivé** (sin tocar el script, como exige la tarea): acorté las
`eleccion` a menos de 15 palabras, y partí `historia`/`personalidad` en
listas YAML de fragmentos cortos (cada fragmento < 15 palabras). Esto
funciona porque `verificar_sin_copias` recorre listas elemento a elemento y
cuenta palabras por nodo-string, no por campo lógico completo.

**Esto ya lo hace `personajes/orco_barbaro.yaml`** — su `historia` y
`personalidad` están escritas como listas de fragmentos cortos en vez de
bloques `>` de prosa continua (lo confirmé leyendo el archivo en disco). Eso
sugiere que quien construyó esa ficha se topó con el mismo problema y aplicó
el mismo workaround. El efecto neto es que el esquema *dice* que
`historia`/`personalidad` son prosa libre sin restricción de longitud, pero
en la práctica el validador obliga a trocear esa prosa en fragmentos
artificiales de <15 palabras — una ficha nueva no puede tener un párrafo de
historia fluido y pasar la verificación tal como está escrito el script.

**Impacto:** esto no es un problema menor de estilo — es una discrepancia
real entre lo que el contrato (`_ESQUEMA.md`) promete y lo que el verificador
exige, y el mecanismo de evasión (trocear en lista) socava el propósito
declarado del check ("detectar copia de texto de la base"), porque un
fragmento de más de 15 palabras copiado literalmente de un `desc` real
seguiría sin detectarse si se lo divide en dos strings de 8 palabras cada
uno — el check ni siquiera cumple su propio objetivo antibug.

**Recomendación** (solo como nota, no lo implementé): comparar cada
fragmento contra los `desc` reales de la base (similaridad de subcadena),
tal como dice la regla 5, y eximir explícitamente `historia`/`personalidad`
de cualquier límite de longitud si no hay coincidencia con la base.

## 3. Cosas confusas o mal explicadas en la documentación

- `_ESQUEMA.md` no dice nada sobre qué hacer con el bloque `conjuros:` cuando
  la clase no es lanzadora. Lo deduje del comentario en el propio bloque de
  ejemplo (`# solo si la clase es lanzadora`) y de que Pícaro nivel 1 no
  tiene subclase (`lanzador: "ninguno"` en `clases/picaro.yaml`), así que
  omití el bloque por completo. Funcionó (`verificar_personaje.py` no se
  quejó de que faltara), pero el esquema debería decir explícitamente
  "omite el bloque entero" en vez de dejarlo solo como comentario en el
  ejemplo — un LLM sin ese comentario podría escribir
  `conjuros: {trucos: [], preparados: []}` en vez de omitirlo, que es una
  ambigüedad real (¿está permitido? ¿es incorrecto?).
- `_ESQUEMA.md` regla 5 (el chequeo de "texto copiado") no explica que en la
  práctica hay que trocear `historia`/`personalidad` en fragmentos cortos
  para pasar el verificador — ver hallazgo 2.1. Documentar el
  comportamiento real del script (no solo la intención) habría ahorrado
  iteración.
- El paso 8 de `SKILL.md` ("Idiomas y herramientas") dice "Idiomas de la
  especie/trasfondo más los que el trasfondo permita elegir" — implica que
  la *especie* puede conceder idiomas. Pero revisé `especies/especies.yaml`
  completo (con un grep de `idioma`) y **ninguna especie** en la base
  concede un idioma específico como rasgo (ni Elfo, ni Mediano, ni ninguna
  otra); toda la concesión de idiomas viene de la nota general en
  `reglas/idiomas.yaml` ("todo personaje sabe común + otros dos a elegir")
  y, en el caso del Pícaro, del propio rasgo de clase "Jerga de ladrones".
  El texto de `SKILL.md` debería aclarar que, en esta base, la especie no es
  actualmente una fuente de idiomas (o corregirse si en algún momento se
  añade ese dato a `especies/especies.yaml`).
- **Relacionado y más grave**: `personajes/_ejemplo_aerin.yaml` — el ejemplo
  "ya verificado" que la tarea pide leer como referencia de formato —
  incluye `idiomas: [{nombre: Común}, {nombre: Élfico, origen: {especie:
  Elfo}}]`. Esto es incorrecto en dos sentidos: (a) como se explicó arriba,
  `especies/especies.yaml#Elfo` no tiene ningún rasgo que conceda un
  idioma, así que el `origen: {especie: Elfo}}` no está respaldado por
  ningún dato real de la base; y (b) el nombre canónico en
  `reglas/idiomas.yaml` es **"Elfo"**, no "Élfico" — la tabla de idiomas
  estándar lista `{nombre: Elfo, origen: Elfos, ...}`, nunca "Élfico". El
  verificador no lo detecta porque las entradas de `idiomas` no llevan
  `ref:` (no hay registro contra el que resolverlas), así que
  `verificar_personaje.py` pasa igual (lo comprobé: `python3
  verificar_personaje.py personajes/_ejemplo_aerin.yaml` → `✅ FICHA
  VERIFICADA — 0 problemas`). Como el ejemplo se presenta como "ya
  verificado", esto puede inducir a error a cualquiera que lo use como
  plantilla: parece sugerir que las especies conceden idiomas con nombres
  que en realidad no existen en la base tal cual están escritos.

## 4. Huecos de datos en la base

- `equipo/armas.yaml` no tiene un registro para las categorías de
  competencia tal como las cita `atributos_basicos.armas` de las clases
  ("Armas sencillas", "Armas marciales con la propiedad 'ligera' o
  'sutil'"), solo armas individuales. Mismo hueco para
  `atributos_basicos.armaduras` ("Armaduras ligeras" sí existe como
  registro en `equipo/armaduras.yaml`, así que en este caso concreto no hay
  problema, pero la propiedad "ligera o sutil" de armas marciales no tiene
  ningún registro-categoría). Seguí el patrón ya usado en
  `personajes/orco_barbaro.yaml`: referenciar un arma/armadura concreta que
  el personaje porta como evidencia de la competencia de categoría, con una
  `nota` explicando qué representa. Funciona para pasar el verificador
  (que solo resuelve la ref del arma concreta), pero es una ficha "citando"
  una competencia de categoría con el nombre de un objeto individual — no
  es estrictamente lo que dice `atributos_basicos.armas`. No lo até a un
  ref que efectivamente diga "Armas marciales con la propiedad ligera o
  sutil" porque ese registro no existe en `equipo/armas.yaml`.
- No hay ningún campo en el esquema de ficha (`personajes/_ESQUEMA.md`) para
  registrar el oro/riqueza inicial del personaje (p. ej. los "8 po" que
  sobran de la opción A de clase, o los "50 po" de la opción B de
  trasfondo). Seguí el mismo criterio que `orco_barbaro.yaml`: mencionarlo
  solo en el texto de `decisiones[].eleccion`, sin ningún campo mecánico
  dedicado. Si en algún momento se calcula riqueza total del personaje, no
  hay dónde guardarla de forma trazable.

## 5. Estado final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/mediano_picaro.yaml
17 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```
