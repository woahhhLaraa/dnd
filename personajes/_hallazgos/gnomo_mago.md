# Hallazgos — creación de Fippen Cascabelroble (Gnomo / Mago / Erudito, nivel 1)

## 1. Qué funcionó bien

- `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasaron limpios (0 errores, 646 valores contrastados contra SRD, cobertura 100%).
- `python3 buscar.py clase Mago`, `buscar.py especie Gnomo`, `buscar.py trasfondo Erudito` devolvieron toda la información necesaria para la ficha (dado de golpe, salvaciones, habilidades a elegir, equipo A/B, progresión de trucos/preparados nivel 1-20, linajes de Gnomo, dote fija del trasfondo).
- `buscar.py conjuros-de Mago --nivel 0` y `--nivel 1` listaron los conjuros disponibles con toda su mecánica citable.
- `calculo.py pg/ca/pb/cd-conjuros/ataque-conjuros` calcularon todos los números sin que tuviera que sumar nada a mano: PG 8, CA 12, PB 2, CD conjuros 13, bonif. ataque conjuros 5.
- La nota `precio_nota` del registro "Libro de conjuros" en `equipo/aventureros.yaml#objetos_de_rasgo_de_clase` explica con precisión por qué ese objeto no se compra (aclara una ambigüedad real de la tabla original del manual).

## 2. Bugs o comportamientos raros de las herramientas

### 2a. `buscar.equipo()` / `verificar_personaje.py` no comprueban que el objeto viva en el fichero citado en el `ref`

`buscar.py` busca por nombre en **todos** los ficheros de `equipo/` en un orden fijo (`armas.yaml`, `armaduras.yaml`, `herramientas.yaml`, `aventureros.yaml`, `municion.yaml`) y devuelve el primer resultado, ignorando de qué fichero venía la pregunta. `verificar_personaje.py` hace lo mismo: para cualquier `ref` que empiece por `"equipo/"`, solo llama a `buscar.equipo(nombre)` con el último segmento del ref — nunca comprueba que el nombre esté realmente en el fichero indicado por el propio `ref`.

Comando y evidencia:
```
$ grep -rn "Bastón" equipo/*.yaml
equipo/armas.yaml:28:  - {nombre: Bastón, dano: "1d6 contundente", ..., precio: "2 pp"}
equipo/aventureros.yaml:90:  - {nombre: Bastón, peso_kg: 2, precio: "5 po"}

$ python3 buscar.py equipo "Bastón"
{... "precio": "2 pp" ...}   # siempre devuelve el arma, nunca el objeto de aventureros.yaml
```
Consecuencia: una ficha podría escribir `ref: "equipo/aventureros.yaml#Bastón"` (el objeto de 5 po que no es arma) y `verificar_personaje.py` la daría por buena citando en realidad el arma de 2 pp, sin avisar de la discrepancia. Es un hueco real de trazabilidad, no crítico pero sí engañoso — lo evité en mi ficha citando siempre `equipo/armas.yaml#Bastón` explícitamente para el bastón-arma del trasfondo Erudito.

### 2b. El ejemplo verificado (`_ejemplo_aerin.yaml`) no tiene ningún problema visible aquí, pero al leerlo por encima pensé que citaba `equipo/armas.yaml#"Armas sencillas"` (una categoría, no un objeto) — al comprobar con `buscar.py equipo "Armas sencillas"` da error:
```
$ python3 buscar.py equipo "Armas sencillas"
✗ no existe un objeto llamado 'Armas sencillas' en equipo/ (revisa el nombre exacto)
```
Era una lectura mía errónea del ejemplo (en realidad cita `#Daga`), pero confirma que la base **no tiene** un registro para la categoría "Armas sencillas" como tal — si alguien intentara citarla literalmente (como hice yo al principio, antes de corregirlo), la ref rompería. Documentado aquí por si ayuda a quien construya la próxima ficha: la competencia de armas por categoría debe citarse contra un arma concreta que el personaje lleve, no contra el nombre de la categoría.

## 3. Cosas confusas o mal explicadas en SKILL.md / _ESQUEMA.md

- Ni `_ESQUEMA.md` ni `SKILL.md` dicen qué hacer cuando la clase (Mago) o el trasfondo (Erudito, vía la dote "Iniciado en la magia") o la especie (Gnomo, vía el linaje "Gnomo de los bosques") conceden trucos/conjuros **adicionales** a los de la progresión de clase. El bloque `conjuros:` del esquema es una lista plana sin campo `origen` en el ejemplo (`_ejemplo_aerin.yaml` no tiene ese caso). Tuve que decidir por mi cuenta añadir `origen:` a cada entrada de `trucos`/`preparados` para no perder la trazabilidad de cuáles vienen de la clase, cuáles de la dote y cuáles del linaje — funcionó y `verificar_personaje.py` no lo penaliza, pero el esquema no lo prescribe ni lo prohíbe explícitamente.
- `verificar_personaje.py` no valida en absoluto que el número de trucos/preparados coincida con `progresion[nivel].trucos`/`.prep` de la clase — solo resuelve refs. Esto significa que una ficha con demasiados o muy pocos conjuros pasa igual. Podría ser intencional (fuera del alcance actual, según el docstring del script), pero SKILL.md no lo avisa; solo dice "ofrece el número que indique la progresión", sin mencionar que nadie lo comprueba después.
- El límite de "≤15 palabras seguidas" de `verificar_sin_copias` se disparó varias veces con frases mías perfectamente originales (nunca copiadas de una `desc`) solo por ser largas — el error decía "posible texto copiado" cuando en realidad era una decisión propia resumida en una frase larga. El mensaje de error no aclara que es una heurística de longitud pura, no una comparación real contra el texto de la base; tuve que acortar las frases sin que eso mejorara la trazabilidad, solo para pasar el chequeo.

## 4. Huecos de datos en la base

- No existe una tabla "Canalizadores arcanos" con variantes (bastón, orbe, varita, etc.) y su coste/peso específico — solo el registro genérico `equipo/aventureros.yaml#Canalizador arcano` con `peso_kg: variable, precio: variable`. El ejemplo (`_ejemplo_aerin.yaml`) ya trabaja alrededor de esto con un campo `variante:` libre en `origen`, que es lo que también hice yo; pero si se necesitara el precio real de un canalizador arcano en forma de bastón, la base no lo tiene.
- Colisión de nombres "Bastón" (arma en `armas.yaml`, 2 pp) vs "Bastón" (objeto en `aventureros.yaml`, 5 po) — ver hallazgo 2a. No es un error de la base en sí (son objetos reales y distintos del manual), pero la falta de desambiguación en `buscar.py equipo()` hace que el segundo sea efectivamente inalcanzable por nombre simple.

## 5. Estado final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/gnomo_mago.yaml
28 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Ficha final en `personajes/gnomo_mago.yaml`.
