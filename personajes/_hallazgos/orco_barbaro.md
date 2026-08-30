# Hallazgos — creación de Orco Bárbaro (Soldado), nivel 1

Ficha final: `personajes/orco_barbaro.yaml` ("Grosh Colmillo Roto").

## 1. Qué funcionó bien

- `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasaron
  limpios los tres, sin necesidad de tocar nada.
- `python3 buscar.py clase Bárbaro` devuelve todo lo necesario para la ficha:
  dado de golpe, salvaciones, habilidades a elegir, armas/armaduras, equipo
  inicial A/B y progresión completa. Fue suficiente para toda la sección de
  clase sin tener que ir a otro fichero.
- `python3 buscar.py equipo "<nombre>"` resuelve por nombre exacto en
  cualquiera de los ficheros de `equipo/` (armas, armaduras, herramientas,
  aventureros), sin que haga falta saber en qué fichero ni bajo qué sección
  anidada vive el objeto. Cómodo.
- `python3 calculo.py ca --des 13 --con 15 --clase Bárbaro` (sin `--armadura`)
  aplicó automáticamente la fórmula de Defensa sin armadura (10 + mod Des +
  mod Con = 13) tal como decía el encargo. No hubo que indicarle nada especial.
- `python3 calculo.py pg --dado d12 --con 15` dio 14 (12 máx + mod Con 2),
  correcto para nivel 1.
- `python3 verificar_personaje.py` fue muy útil para encontrar dos problemas
  reales antes de dar la ficha por buena (ver sección 2).

## 2. Bugs / comportamientos raros de las herramientas

### 2.1 Los `ref:` de competencia de armas/armaduras del propio `_ESQUEMA.md` no resuelven

`_ESQUEMA.md` da como ejemplo:

```yaml
armas: [{ref: "equipo/armas.yaml#Armas sencillas", origen: {clase: Bardo}}]
```

Probé el equivalente para Bárbaro:

```
$ python3 buscar.py equipo "Armas sencillas"
✗ no existe un objeto llamado 'Armas sencillas' en equipo/ (revisa el nombre exacto)
```

Mismo resultado para "Armas marciales", "Armaduras ligeras", "Armaduras
medias" y "Escudos". La razón: `buscar.equipo()` busca un objeto cuyo campo
`nombre` coincida exactamente, y `equipo/armas.yaml` / `equipo/armaduras.yaml`
solo contienen **armas y armaduras individuales**, no un registro para la
categoría en sí (`Armas sencillas` es una clave de la lista `armas` en
`clases/barbaro.yaml#atributos_basicos`, no un objeto de `equipo/`).

Por tanto el propio ejemplo de `_ESQUEMA.md` produciría un error de
"ref rota" en `verificar_personaje.py` si se copiara literalmente. El
ejemplo real y verificado (`_ejemplo_aerin.yaml`) evita el problema
referenciando un arma concreta ("Daga") en vez de la categoría "Armas
sencillas" que en realidad otorga el Brujo — pero eso desdibuja qué
significa esa entrada (¿arma que porta, o competencia de categoría?).

**Solución que apliqué** (documentada también dentro de la ficha, con
comentario `# NOTA:`): referenciar un arma/armadura concreta de cada
categoría que el personaje efectivamente porta, con `origen.nota` aclarando
que representa la competencia de categoría, no un objeto puntual. Funciona
con `verificar_personaje.py` porque solo comprueba que el `nombre` exista,
pero es un rodeo, no una solución de la base. **No toqué `buscar.py` ni
`verificar_personaje.py`** — solo lo reporto.

**Recomendación para la base** (sin implementar, es de solo lectura): o bien
`buscar.equipo()`/`verificar_personaje.py` deberían reconocer nombres de
categoría de armas/armaduras como refs válidas (quizá resolviendo contra las
claves de `atributos_basicos.armas`/`armaduras` de las clases en vez de
contra `equipo/`), o `_ESQUEMA.md` debería dejar de sugerir ese formato de
ref y explicar explícitamente el patrón "arma concreta representando la
categoría" que de hecho usa el ejemplo verificado.

### 2.2 El chequeo anti-copia (`verificar_sin_copias`) no exime `historia`/`personalidad`

`_ESQUEMA.md` dice explícitamente:

> La única prosa libre permitida es la que no tiene equivalente mecánico:
> nombre, historia personal, descripción física, personalidad.

Pero `verificar_personaje.py::verificar_sin_copias` recorre **todo** el árbol
de la ficha (excepto `decisiones[].cita`) y marca error cualquier string de
más de 15 palabras seguidas, sin excluir los campos de prosa libre que el
propio esquema autoriza. Con una `historia` de cinco frases normales (bloque
`>` de YAML, que se colapsa a un único string largo) obtuve:

```
$ python3 verificar_personaje.py personajes/orco_barbaro.yaml
❌ 4 problemas:
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'método de características: conjunto estándar, repartido segú'…
  ✗ posible texto copiado en 'decisiones.eleccion' (>15 palabras seguidas): 'equipo inicial de clase opción A (hacha a dos manos, 4 hacha'…
  ✗ posible texto copiado en 'historia' (>15 palabras seguidas): 'Grosh sirvió una década en la guardia fronteriza de una ciud'…
  ✗ posible texto copiado en 'personalidad' (>15 palabras seguidas): 'Directo hasta la brusquedad, desconfía de las promesas bonit'…
```

La `historia` y `personalidad` son prosa **original**, no copiada de ningún
`desc` de la base — el chequeo es un heurístico de longitud de palabras, no
de coincidencia real de texto, así que no distingue "copiado de la base" de
"prosa larga inventada". Y dos de mis propias entradas en `decisiones[].eleccion`
(fuera de `decisiones[].cita`, que sí está exento) también cayeron, aunque
tampoco eran texto copiado de la base sino resúmenes largos míos.

**Solución que apliqué**: partí `historia` y `personalidad` en listas de
strings cortos (<15 palabras cada uno) y acorté las entradas largas de
`decisiones[].eleccion`. Esto hace pasar la ficha, pero es un formato forzado
por la herramienta, no algo que pida `_ESQUEMA.md` (que muestra `historia`
implícitamente como texto libre sin indicar que deba trocearse). **No toqué
`verificar_personaje.py`.**

**Recomendación**: o el heurístico debería (a) buscar coincidencia real
contra `desc` de la base en vez de solo contar palabras, o (b) eximir
explícitamente `historia`/`personalidad`/`descripcion_fisica` igual que exime
`decisiones[].cita`, ya que `_ESQUEMA.md` los declara zona de prosa libre sin
límite de longitud.

## 3. Cosas confusas o mal explicadas en la documentación

- `_ESQUEMA.md` no menciona el límite de 15 palabras que aplica
  `verificar_personaje.py` a los campos de prosa libre — se descubre solo
  corriendo el verificador y leyendo el mensaje de error, no leyendo la doc.
- `_ESQUEMA.md` muestra `armas`/`armaduras` con refs a categorías
  ("Armas sencillas") que no resuelven contra la base real (ver 2.1); un
  lector que siga el esquema al pie de la letra sin mirar antes
  `_ejemplo_aerin.yaml` se topará con una ref rota sin previo aviso.
- SKILL.md Paso 6 dice "Añade también, sin preguntar, las habilidades fijas
  del trasfondo" pero no advierte que hay que revisar el solapamiento entre
  las habilidades elegibles de la clase y las fijas del trasfondo (en este
  caso, Bárbaro puede elegir Atletismo/Intimidación, que Soldado ya da fijas)
  — si el jugador las elige también por clase quedaría duplicando la entrada
  de competencia. No sé si `verificar_personaje.py` lo detectaría como error
  (no lo probé a propósito, para no ensuciar la ficha final), pero merece una
  nota en la skill.

## 4. Huecos de datos en la base

- No encontré un rasgo de especie ni de idiomas que le dé automáticamente
  "Orco" como idioma al elegir la especie Orco (a diferencia de, por ejemplo,
  Elfo en `_ejemplo_aerin.yaml`, que sí liga "Élfico" a `origen: {especie:
  Elfo}`). Según `reglas/idiomas.yaml`, todo personaje elige libremente
  "común + otros dos" de la tabla estándar — así que elegí Orco y Goblin como
  elección libre, sin `origen: {especie: ...}`, para no inventar un vínculo
  mecánico que la base no confirma. Si la intención de diseño real es que un
  Orco sepa Orco por defecto, ese dato no está en `especies/especies.yaml`
  (revisé el registro completo del Orco: solo trae Aguante incansable,
  Descarga de adrenalina y Visión en la oscuridad, sin campo de idioma).
- No hay registro de categorías de armas/armaduras en `equipo/` (ver 2.1) —
  es un hueco estructural más que un dato faltante puntual.

## 5. Estado final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/orco_barbaro.yaml
19 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```
