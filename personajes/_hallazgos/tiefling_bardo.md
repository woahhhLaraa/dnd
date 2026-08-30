# Hallazgos — creación de Vesper Cindertongue (Tiefling / Bardo / Artesano, nivel 1)

Ficha: `personajes/tiefling_bardo.yaml`

## 1. Qué funcionó bien

- Las tres comprobaciones previas (`validar.py`, `verificar_srd.py`, `cobertura.py`) pasaron limpias antes de empezar, tal como exige la skill.
- `python3 buscar.py clase Bardo` entrega el bloque `atributos_basicos` completo, incluyendo el caso especial `cualesquiera: true` + `literal` para las habilidades, exactamente como lo describe `clases/_ESQUEMA_atributos_basicos.md`.
- `python3 buscar.py equipo "<nombre>"` resuelve tanto entradas de nivel superior (`Daga`, `Bolsa`, `Herramientas de herrero`) como variantes anidadas dentro de listas (`Laúd`, `Flauta`, `Tambor` dentro de `otras_herramientas → Instrumento musical → variantes`) buscando directamente por `nombre`, sin que haya que conocer la ruta interna. Cómodo y consistente.
- `python3 calculo.py pg/ca/pb/cd-conjuros/ataque-conjuros` dio todos los números sin ambigüedad; los cinco valores de `calculado` en la ficha final coinciden con lo recalculado por `verificar_personaje.py`.
- `reglas/idiomas.yaml` documenta explícitamente la regla general "todo personaje sabe común + 2 más de la tabla estándar", que ni la especie Tiefling ni el trasfondo Artesano mencionan — sin esa nota no habría manera de justificar los idiomas adicionales del personaje.
- `python3 verificar_personaje.py personajes/tiefling_bardo.yaml` terminó en verde: **26 referencias comprobadas, ✅ FICHA VERIFICADA — 0 problemas.**

## 2. Bugs / comportamientos raros de las herramientas

### Bug real: `cualesquiera: true` desactiva TODA comprobación de habilidades, no solo la restricción de lista

`verificar_habilidades()` en `verificar_personaje.py` (líneas ~95-113) hace esto:

```python
if cualesquiera:
    return  # cualquier habilidad de las 18 es válida; no hay más que comprobar
```

El comentario dice "cualquiera de las 18 es válida", pero el código no comprueba que la habilidad elegida esté siquiera entre las 18 canónicas de `reglas/habilidades.yaml` — simplemente no comprueba nada. Reproducido así:

```bash
cp personajes/tiefling_bardo.yaml /tmp/test_cualesquiera.yaml
sed -i 's/nombre: Sigilo,         origen: {clase: Bardo}/nombre: "Cocina inventada", origen: {clase: Bardo}/' /tmp/test_cualesquiera.yaml
python3 verificar_personaje.py /tmp/test_cualesquiera.yaml
```

Salida:
```
26 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Con `cualesquiera: true` el script acepta literalmente cualquier cadena como nombre de habilidad ("Cocina inventada"), no solo las 18 habilidades reales que el propio `literal` de la clase promete ("tres cualesquiera... consulta el capítulo 1" se refiere a las 18 habilidades del capítulo 1, no a "cualquier texto"). Para el caso concreto de mi ficha esto no importó — elegí Interpretación/Engaño/Sigilo, que son habilidades reales — pero es un hueco real: la comprobación debería seguir verificando `elegidas ⊆ (las 18 canónicas)` incluso cuando `cualesquiera: true`, y solo saltarse la restricción más fina de `de`/clase.

Sugerencia (no aplicada, es de solo lectura): en vez de `return`, hacer `permitidas |= set(reglas_habilidades_canonicas)` antes de comprobar `fuera`.

### Inconsistencia de documentación: `_ESQUEMA.md` muestra refs de equipo a nivel de categoría que no resuelven

El ejemplo genérico en `personajes/_ESQUEMA.md` (bloque `competencias.armas`/`competencias.armaduras`) usa:

```yaml
armas: [{ref: "equipo/armas.yaml#Armas sencillas", origen: {clase: Bardo}}]
armaduras: [{ref: "equipo/armaduras.yaml#Armaduras ligeras", origen: {clase: Bardo}}]
```

Pero `buscar.equipo()` (usado por `verificar_personaje.py` para resolver cualquier ref bajo `equipo/`) busca por `nombre` exacto de un objeto concreto, no por categoría:

```bash
python3 buscar.py equipo "Armaduras ligeras"
✗ no existe un objeto llamado 'Armaduras ligeras' en equipo/ (revisa el nombre exacto)
python3 buscar.py equipo "Armas sencillas"
✗ no existe un objeto llamado 'Armas sencillas' en equipo/ (revisa el nombre exacto)
```

Es decir: si alguien sigue el ejemplo del propio `_ESQUEMA.md` al pie de la letra para `competencias.armas`/`armaduras`, `verificar_personaje.py` falla con "ref rota". El ejemplo *realmente verificado*, `personajes/_ejemplo_aerin.yaml`, no comete este error — usa objetos concretos (`equipo/armas.yaml#Daga`, `equipo/armaduras.yaml#Armadura de cuero`). Para mi ficha seguí el patrón de `_ejemplo_aerin.yaml` (objetos concretos que el personaje realmente porta) en vez del de `_ESQUEMA.md`, y así pasó la verificación. Recomendación: corregir el ejemplo de `_ESQUEMA.md` para que coincida con lo que la herramienta realmente acepta.

## 3. Cosas confusas o mal explicadas en la documentación

- `_ESQUEMA.md` no aclara qué hacer con rasgos de **especie** que otorgan un conjuro/truco propio fuera de la lista de la clase (caso Tiefling: "Presencia sobrenatural" da el truco Taumaturgia, que ni siquiera está en la lista de conjuros de Bardo — solo de Clérigo en `hechizos.json`). No hay una convención documentada sobre si eso va dentro de `conjuros.trucos` (como hice yo, con `origen: {especie: Tiefling, rasgo: "Presencia sobrenatural"}`) o en otro bloque. `verificar_personaje.py` no cuenta ni valida el número ni el origen de los trucos/preparados contra `progresion` de la clase, así que técnicamente cualquier convención "pasa", pero sería útil que `_ESQUEMA.md` o `SKILL.md` dijeran explícitamente cómo marcar un conjuro de origen racial para que dos fichas no lo hagan de formas distintas.
- El Paso 6 de `SKILL.md` dice "La clase ofrece `atributos_basicos.habilidades.elige` opciones de `atributos_basicos.habilidades.de`" y solo después menciona el caso `cualesquiera`. Para Bardo, `elige: 3` y `de` son *ambos* engañosos si se leen aislados: `de` no es una lista restrictiva (contiene las 18 igual que `reglas/habilidades.yaml`), es un relleno de conveniencia. El propio `_ESQUEMA_atributos_basicos.md` lo explica bien, pero `SKILL.md` podría enlazarlo más explícitamente en vez de solo mencionarlo de pasada.
- `SKILL.md` no dice qué hacer cuando la clase otorga competencia con "instrumentos musicales a elección" o "herramientas de artesano a elección" (Bardo: "Tres instrumentos musicales a elección"; Artesano: "elige un tipo de herramientas de artesano"). No hay un paso equivalente al de habilidades que diga "elige N de la tabla `equipo/herramientas.yaml`". Tuve que inferir el patrón yo mismo buscando en `equipo/herramientas.yaml → otras_herramientas → Instrumento musical → variantes`.

## 4. Huecos de datos en la base

- No encontré un campo de idiomas propio en `especies/especies.yaml#Tiefling` ni en `trasfondos/trasfondos.yaml#Artesano`. Los dos idiomas adicionales del personaje (más allá de Común) solo pudieron justificarse citando la nota general de `reglas/idiomas.yaml`, no un campo específico de especie/trasfondo. Si el manual real le da a alguna especie/trasfondo un idioma fijo, no está transcrito (o Tiefling/Artesano de verdad no lo tienen — no puedo confirmarlo sin el manual).
- El Legado infernal del Tiefling (`especies/especies.yaml#Tiefling → linajes`) da a nivel 3 y 5 conjuros adicionales ("Reprensión infernal", "Oscuridad" para el linaje Infernal), pero no hay una `ref` operable a un hechizo concreto en `hechizos.json` para esos nombres — no lo comprobé a fondo porque no aplican a nivel 1, pero si `_subir-nivel` los necesita más adelante convendría verificar que existen en `hechizos.json` con esos nombres exactos.

## 5. Estado final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/tiefling_bardo.yaml
26 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```
