# Hallazgos — creación de Ithariel Solvane (Aasimar / Clérigo / Acólito, nivel 1)

## 1. Qué funcionó bien

- Precondición completa: `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasó limpia (0 errores, 646 valores contrastados contra SRD, cobertura 100% de las preguntas simuladas).
- `python3 buscar.py clase Clérigo` devolvió todo lo necesario: dado de golpe (d8), salvaciones, 5 habilidades a elegir 2, armas/armaduras competentes, equipo A/B, `lanzador: completo`, `aptitud_magica: Sabiduría` y la progresión completa (trucos/prep/slots por nivel).
- `python3 -c "import yaml; ..."` sobre `especies/especies.yaml` y `trasfondos/trasfondos.yaml` dio el registro completo de Aasimar (incluida la elección de tamaño Mediano/Pequeño, explícita en el campo `tamano`) y de Acólito (características ajustables, dote fija, habilidades fijas, equipo A/B, herramienta fija).
- `clases/rasgos/clerigo.yaml` (rasgo "Lanzamiento de conjuros") trae explícitamente trucos y conjuros *recomendados* ("se recomiendan guía, llama sagrada y taumaturgia" / "se recomiendan bendición, curar heridas, escudo de fe y saeta guía"), lo cual hizo la elección de conjuros trivial y bien fundamentada.
- `python3 calculo.py pg/ca/pb/cd-conjuros/ataque-conjuros` calculó todo sin aritmética manual: PG 10 (d8, Con 14), CA 16 (Camisa de malla + escudo, Des 12), PB 2, CD conjuros 13, bonif. ataque conjuros 5 (Sab 17).
- Las 28 referencias de la ficha final resolvieron a la primera con `buscar.equipo()` / `buscar.conjuro()` / `buscar.dote()` etc. `verificar_personaje.py` terminó en 0 problemas.

## 2. Bugs o comportamientos raros de las herramientas

### 2a. La heurística "≤15 palabras" de `verificar_sin_copias` rechaza prosa libre 100% original, no solo texto copiado

Al escribir `historia:` y `personalidad:` (prosa libre explícitamente permitida por `_ESQUEMA.md`: "nombre, historia personal, descripción física, personalidad") como un único bloque de varias frases, `verificar_personaje.py` los marcó como "posible texto copiado":

```
$ python3 verificar_personaje.py personajes/aasimar_clerigo.yaml
❌ 2 problemas:
  ✗ posible texto copiado en 'historia' (>15 palabras seguidas): 'Criado desde niño en un templo de montaña tras aparecer en s'…
  ✗ posible texto copiado en 'personalidad' (>15 palabras seguidas): 'Sereno y metódico, habla poco pero escucha mucho. Lleva un r'…
```
Ninguna de esas dos frases coincide con nada de la base — es puramente una heurística de longitud, no una comparación real contra `desc`. Tuve que reescribir `historia` y `personalidad` como listas de frases cortas (cada una <15 palabras) para que pasara, lo cual no mejora la trazabilidad en absoluto, solo esquiva el contador de palabras por nodo YAML. Ya lo había documentado un hallazgo anterior (`personajes/_hallazgos/gnomo_mago.md`, sección 3) sobre decisiones largas; aquí se confirma que también golpea a los campos de prosa libre que el propio esquema dice que están permitidos sin restricción de longitud.

### 2b. Competencias por categoría ("Armas sencillas", "Armaduras medias", "Escudos") no son objetos citables

Confirmando el hallazgo previo de `gnomo_mago.md` (2b): la clase Clérigo lista sus competencias de armas/armaduras como categorías (`["Armas sencillas"]`, `["Armaduras ligeras","Armaduras medias","Escudos"]`), pero no existe ningún registro en `equipo/armas.yaml` o `equipo/armaduras.yaml` con `nombre: "Armas sencillas"` etc.:

```
$ python3 buscar.py equipo "Armaduras medias"
✗ no existe un objeto llamado 'Armaduras medias' en equipo/ (revisa el nombre exacto)
```
Seguí la convención ya usada en `_ejemplo_aerin.yaml`/`gnomo_mago.yaml`: citar un objeto real que el personaje efectivamente lleva (Maza, Camisa de malla, Escudo) como representante de cada categoría de competencia, anotado con `origen.nota`. Funciona y pasa la verificación, pero ni `_ESQUEMA.md` ni `SKILL.md` documentan explícitamente este patrón — cada ficha lo reinventa por su cuenta.

### 2c. `equipo()` ignora qué fichero indica el propio `ref` (ya reportado en `gnomo_mago.md` 2a, revalidado aquí)

No encontré colisiones de nombre en mi ficha (los objetos que usé — Camisa de malla, Escudo, Maza, Símbolo sagrado, Libro, Pergamino, Túnica, Suministros de calígrafo, Paquete de sacerdote — son únicos en toda `equipo/`), pero el comportamiento de fondo sigue siendo el mismo que ya se documentó: `buscar.equipo(nombre)` y `verificar_personaje.py` solo miran el nombre final del `ref`, nunca el fichero/sección indicados antes del `#`. No es un hallazgo nuevo, solo confirmo que sigue vigente.

## 3. Cosas confusas o mal explicadas en la documentación

- **Elección de tamaño de especie**: `SKILL.md` (paso 2) dice "si esa especie tiene una elección interna (ver el campo `tamano` u otros en sus `rasgos`...)" — pero en Aasimar la elección de tamaño vive en el campo `tamano` de la raíz del registro de especie (`"Mediano (...) o Pequeño (...), elegido al seleccionar la especie"`), NO dentro de `rasgos`. El texto del paso 2 sugiere buscar la elección dentro de `rasgos`, lo cual habría hecho que alguien la pasara por alto si no lee el registro completo. Sugerencia: aclarar que el campo `tamano` en sí puede contener una elección, no solo el bloque `rasgos`.
- **`_ejemplo_aerin.yaml` cita un idioma que la base no respalda**: la ficha de ejemplo tiene `{nombre: Élfico, origen: {especie: Elfo}}`, pero (a) `especies/especies.yaml#Elfo` no tiene ningún rasgo ni campo que conceda un idioma, y (b) `reglas/idiomas.yaml` (la única fuente canónica de idiomas) llama al idioma "Elfo", no "Élfico":
  ```
  $ grep -n idioma -i especies/especies.yaml
  (sin resultados para Elfo)
  $ grep -n "nombre: Elfo" reglas/idiomas.yaml
    - {nombre: Elfo, origen: Elfos, d12: "2-3"}
  ```
  Es decir, el ejemplo verificado que `SKILL.md` recomienda seguir "al pie de la letra" contiene un dato que no está respaldado por ningún `ref` real de la base (ni la especie concede idioma, ni el nombre "Élfico" existe en `reglas/idiomas.yaml`). Para mi ficha usé el nombre canónico ("Elfo") y la nota general de `reglas/idiomas.yaml` (todo personaje elige 2 idiomas libres de la tabla estándar) en vez de replicar el patrón del ejemplo.
- **`SKILL.md` paso 8** dice "Idiomas de la especie/trasfondo más los que el trasfondo permita elegir" — para Aasimar y Acólito, ni la especie ni el trasfondo conceden ni permiten elegir idiomas explícitamente; la única regla aplicable es la genérica de `reglas/idiomas.yaml` ("todo personaje sabe común y otros dos, elegidos de la tabla idiomas estándar"). El paso 8 da a entender que siempre hay una elección ligada a especie/trasfondo, cuando en este caso la elección es enteramente libre y viene de una regla general que el paso 8 ni siquiera menciona.
- **Solapamiento de habilidades clase/trasfondo**: Acólito fija Perspicacia y Religión; el Clérigo elige 2 de un conjunto que también incluye Perspicacia y Religión. Ni `_ESQUEMA.md` ni `SKILL.md` dicen qué hacer si las habilidades fijas del trasfondo ya están en la lista de opciones de la clase (¿se pierde la elección, se sustituye, se permite duplicar sin beneficio?). Elegí las dos opciones restantes de la clase (Historia, Medicina) para evitar el solapamiento sin más indicación de la base — decisión razonable pero no verificada por ningún script.

## 4. Huecos de datos en la base

- No hay ninguna tabla que resuelva qué pasa cuando la dote fija de un trasfondo (`"Iniciado en la magia (clérigo)"`) coincide con la propia lista de conjuros de la clase del personaje. La descripción de la dote (`dotes/origen.yaml#Iniciado en la magia`) es genérica para cualquier clase; no hay ninguna nota sobre la redundancia de tomarla con lista "clérigo" siendo ya Clérigo (mecánicamente válido en 2024 — dos trucos extra y un conjuro de nivel 1 siempre preparado con ranura extra — pero nada en la base lo comenta ni lo desaconseja).
- `equipo/aventureros.yaml#Símbolo sagrado` tiene `peso_kg: variable, precio: variable` (igual que el "Canalizador arcano" ya señalado en `gnomo_mago.md`). Mi personaje termina con dos símbolos sagrados (uno del equipo de clase, otro del trasfondo Acólito) y no hay forma de calcular su peso/precio real combinado porque ninguno de los dos registros tiene un valor concreto.
- El campo `cantidad` que añadí a mano al ítem "Pergamino (10 hojas)" no está previsto en `_ESQUEMA.md` — el esquema no tiene ningún mecanismo para expresar cantidades de un mismo objeto. `verificar_personaje.py` lo ignora sin error (no valida claves desconocidas), así que funciona, pero es un hueco de expresividad del esquema más que de la base de datos en sí.

## 5. Estado final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/aasimar_clerigo.yaml
28 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Ficha final en `personajes/aasimar_clerigo.yaml`.
