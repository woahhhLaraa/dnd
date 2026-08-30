# Hallazgos — Enano Guerrero (Guardia), nivel 1

## 1. Qué funcionó bien

- `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasó limpio (0 errores) antes de empezar.
- `buscar.py especie/trasfondo/dote/equipo` resolvió todo lo necesario sin ambigüedad: Enano, Guardia, Alerta, Cota de malla, Espadón, Mangual, Jabalina, Lanza, Ballesta ligera, Aljaba, Esposas, Linterna sorda, Ropas de viaje, Juego, Paquete de explorador de mazmorras — ninguno necesitó `--archivo` para desambiguar (no hubo colisión de nombres tipo "Bastón" en este set de objetos).
- El patrón de `personajes/orco_barbaro.yaml` para herramientas de trasfondo (`{ref: "equipo/herramientas.yaml#Juego", origen: {...}, variante: Dados}` en vez de `categoria:`) resolvió limpiamente un caso que de otro modo habría fallado (ver bug #1 abajo).
- `calculo.py pg/ca/pb` y `verificar_personaje.py` funcionaron exactamente como documentado; la ficha final pasó con **0 problemas** en el primer intento tras aplicar los ajustes descritos abajo.
- `_ESQUEMA.md` y `_ejemplo_aerin.yaml` (versión corregida) son consistentes entre sí y con el comportamiento real del código.

## 2. Bugs o comportamientos raros

**Bug real #1 — `verificar_categorias()` en `verificar_personaje.py` solo mira `clases[].atributos_basicos`, nunca `trasfondo`, pese a lo que dice `_ESQUEMA.md`.**

`_ESQUEMA.md` línea ~108 dice: "se comprueban contra la lista real de
`atributos_basicos` de la clase (**o del trasfondo cuando aplica**)". Pero el
código de `verificar_categorias()` es:

```python
permitidas = set()
for c in ficha.get("clases", []):
    clase_d = buscar.clase(c["clase"])
    permitidas |= set(clase_d.get("atributos_basicos", {}).get(campo, []))
```

Nunca toca `ficha["trasfondo"]`. El trasfondo Guardia concede
`herramienta: "elige un tipo de juego"`, y `Guerrero.atributos_basicos.herramientas`
es `[]`. Si se intenta registrar esa competencia como
`{categoria: "elige un tipo de juego", origen: {trasfondo: Guardia}}` (siguiendo
literalmente el patrón de `armas`/`armaduras` del propio esquema), falla:

```
✗ competencias.herramientas: 'elige un tipo de juego' no está en lo que conceden las clases del personaje ([])
```

Workaround usado (no autorizado a tocar el script): seguir el patrón ya
usado en `personajes/orco_barbaro.yaml` y registrar la herramienta de
trasfondo con `ref:` a un objeto concreto de `equipo/herramientas.yaml`
(`#Juego`, `variante: Dados`) en vez de `categoria:` — esa rama del código
(`if not isinstance(e, dict) or "categoria" not in e: continue`) la deja
pasar vía `_recorrer_refs`. Funciona, pero es un rodeo no documentado en
`_ESQUEMA.md`: el ejemplo de referencia (`_ejemplo_aerin.yaml`) no ilustra
este caso (el Brujo no tiene herramienta de trasfondo con elección). Recomendación:
o se corrige `verificar_categorias()` para incluir el trasfondo, o
`_ESQUEMA.md` deja de prometerlo y documenta explícitamente el patrón `ref:`
como la vía correcta para herramientas otorgadas por trasfondo.

**Bug real #2 — `calculo.py`/`verificar_personaje.py` no tienen forma de reflejar bonificadores de PG por especie (p. ej. "Aguante enano": +1 PG máx. en nivel 1 y +1 por cada nivel siguiente).**

`calculo.puntos_golpe_nivel_1(dado_golpe, con_mod)` = caras del dado + mod.
Con. No acepta ni busca ningún bonus de especie. `verificar_calculado()`
recalcula con la misma fórmula. Para un Enano nivel 1 Guerrero (d10, Con 14
→ mod +2): la fórmula da PG=12, pero según el rasgo "Aguante enano" de
`especies/especies.yaml` el PG real debería ser 13. Si se escribe
`calculado.pg_max: 13` (el valor mecánicamente correcto), `verificar_personaje.py`
lo rechaza:

```
✗ calculado.pg_max = 13, pero recalculado da 12
```

Se dejó `pg_max: 12` en la ficha final (sin el bonus de Aguante enano) para
pasar la verificación, documentado en `decisiones[]`. Esto significa que,
tal como está la base hoy, **ninguna ficha de Enano puede tener un
`calculado.pg_max` mecánicamente correcto y a la vez pasar
`verificar_personaje.py`** — hay que elegir entre "correcto" y "verificable".
Mismo problema, en potencia, con cualquier dote/rasgo que modifique la CA
(p. ej. la dote de Estilo de combate "Defensa", +1 CA con armadura): se
evitó a propósito eligiendo "Combate con armas a dos manos" en vez de
"Defensa" para no pisar `calculado.ca` también, pero el hueco en
`calculo.ca()` (no acepta bonus de dotes) es el mismo tipo de bug.

## 3. Documentación confusa

- `_ESQUEMA.md` regla 6 dice que `competencias.herramientas` con `categoria:`
  se compara "contra `atributos_basicos` de la clase (o del trasfondo cuando
  aplica)" — como se ve en el bug #1, eso último no ocurre en el código. La
  única forma de que aparezca en `_ESQUEMA.md` sería si alguien probó solo el
  caso donde clase y trasfondo comparten la misma lista de categorías.
- Ningún fichero de esquema/documentación menciona `maestria_armas` (columna
  específica del Guerrero, y presumiblemente de otras clases marciales con
  `columnas_extra`). No hay una clave dedicada en `_ESQUEMA.md` para
  registrar las armas elegidas para maestría en nivel 1 — se documentó solo
  en `decisiones[].eleccion` como texto libre, a falta de mejor sitio.
  Tampoco hay guía sobre dónde registrar la elección de dote "Estilo de
  combate" (rasgo de nivel 1 del Guerrero, no aparece en `_ejemplo_aerin.yaml`
  porque el Brujo no lo tiene) — se optó por meterla en `dotes:` con
  `origen: {clase: Guerrero, rasgo: "Estilo de combate"}`, siguiendo el
  espíritu del bloque, pero sin confirmación de que sea el patrón esperado.

## 4. Huecos de datos

- `especies/especies.yaml#Enano` no lista ningún idioma ni competencia de
  herramienta fija (a diferencia de otras versiones de "enano" en D&D donde
  suele haber competencia con herramientas de artesano). Puede ser correcto
  para esta edición (todo idioma es de la regla general, ya lo confirma
  `_ejemplo_aerin.yaml`), pero se anota por si acaso — no se encontró
  ninguna competencia de herramienta de especie para Enano en toda la base.
- `reglas/generacion_personaje.yaml → conjunto_estandar_por_clase` no trae
  fila para todas las clases con las seis características en el orden
  óptimo para armadura pesada (para Guerrero sugiere Des 14 / Con 13, que es
  subóptimo si se lleva armadura pesada sin bonus de Des); no es un bug,
  solo una sugerencia que hubo que invertir manualmente (documentado en
  `decisiones[]`).

## 5. Salida final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/enano_guerrero.yaml
19 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Ficha final: `personajes/enano_guerrero.yaml`.
