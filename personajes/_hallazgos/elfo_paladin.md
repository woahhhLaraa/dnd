# Hallazgos — Elfo Paladín (Marinero), nivel 1

## 1. Qué funcionó bien

- `validar.py`, `verificar_srd.py` y `cobertura.py` pasaron limpios antes de empezar (0 errores, 646 valores contrastados, 0 huecos de cobertura).
- `python3 buscar.py clase "Paladín"` (con tilde) devuelve `atributos_basicos` y `progresion` completos, incluida `lanzador: "medio"` y `aptitud_magica: "Carisma"`.
- Confirmado con mis propios ojos en `clases/paladin.yaml → progresion[0]`: el Paladín SÍ tiene espacios de conjuro en nivel 1 (`slots: [2,0,0,0,0]`, `prep: 2`), a diferencia de 2014. `calculo.py espacios --clase "Paladín" --nivel 1` devuelve exactamente `[2, 0, 0, 0, 0]`, coincide.
- `calculo.py ca --des 11 --con 12 --sab 13 --clase "Paladín" --armadura "Cota de malla" --escudo` → `18` (16 de cota de malla + 2 de escudo, sin sumar Destreza porque es armadura pesada). Correcto.
- `calculo.py cd-conjuros --aptitud 15 --nivel 1` → `12` y `calculo.py ataque-conjuros --aptitud 15 --nivel 1` → `4`, ambos consistentes con 8+pb(2)+mod(2) y pb(2)+mod(2) — y `verificar_personaje.py` recalcula exactamente lo mismo internamente (usa `lanzador not in (None, "ninguno")`, así que "medio" entra bien en la comprobación).
- `python3 verificar_personaje.py personajes/elfo_paladin.yaml` → **0 problemas** en el primer intento tras aplicar la lección de la ronda anterior (categorías literales para armas/armaduras, `ref:` solo para herramientas concretas).
- El linaje "Elfo de los bosques" con aptitud mágica Carisma para el linaje élfico, y "Sentidos agudos → Perspicacia" (evitando duplicar Percepción, ya fija por Marinero) quedaron documentados en `especie.rasgos_elegidos` como pidió la tarea.

## 2. Bugs o comportamientos raros

**Bug real — `verificar_habilidades()` ignora habilidades otorgadas por rasgos de especie.**
`verificar_personaje.py`, función `verificar_habilidades` (líneas ~116-145), construye el conjunto `permitidas` solo a partir de `clase.atributos_basicos.habilidades.de` + `trasfondo.habilidades`. Nunca consulta la especie. El Elfo tiene el rasgo "Sentidos agudos" que concede competencia elegida en Percepción, Perspicacia o Supervivencia — una elección igual de legítima que la de clase/trasfondo — pero si el jugador elige una habilidad que no está también en la lista de la clase o del trasfondo, el verificador la rechaza como inventada.

Reproducido con una copia de la ficha, cambiando `Perspicacia` (que por coincidencia SÍ está en la lista del Paladín) por `Supervivencia` (que no está ni en Paladín ni en Marinero):

```
$ python3 verificar_personaje.py /tmp/.../test_supervivencia.yaml
17 referencias comprobadas.
❌ 1 problemas:
  ✗ habilidades elegidas fuera de lo permitido por clase/trasfondo: ['Supervivencia']
```

En mi ficha final elegí `Perspicacia` precisamente para esquivar este bug (está en la lista de clase del Paladín), pero es suerte de la elección, no una garantía del validador. Cualquier personaje Elfo que use "Sentidos agudos" para elegir Supervivencia (o Percepción si su clase/trasfondo no la ofrecen) fallará la verificación aunque la ficha sea mecánicamente correcta. No toqué `verificar_personaje.py` — solo lo dejo anotado.

## 3. Documentación confusa

- `_ESQUEMA.md` regla 6 dice que `competencias.armas/.armaduras/.herramientas` van "como `categoria:` (texto literal), no como `ref:`" — pero en la práctica, y confirmado leyendo `verificar_categorias()`, esa regla en sentido estricto solo se aplica de forma dura a `armas`/`armaduras` (categorías genéricas tipo "Armas marciales" que no son registros de `equipo/`). `herramientas` normalmente SÍ es una `ref:` a un objeto concreto real de `equipo/herramientas.yaml` (p. ej. "Herramientas de navegante"), porque a diferencia de las categorías de armas/armaduras, una herramienta de trasfondo sí es un registro individual existente. El código lo permite (`if not isinstance(e, dict) or "categoria" not in e: continue`) pero el texto de la regla 6, tal como está redactado, sugiere que las tres claves se comportan igual, y no es así. Los ejemplos previos (`personajes/*.yaml` de la ronda anterior) confirman el patrón `ref:` para herramientas, pero la letra de la regla no lo distingue explícitamente.
- La misma regla 6 y el comentario del esquema de línea 118 dicen que las categorías "se comprueban contra la lista real de `atributos_basicos` de la clase (**o del trasfondo cuando aplique**)" — pero el código de `verificar_categorias()` solo itera `ficha.get("clases", [])`, nunca `ficha.get("trasfondo")`. No me afectó (Marinero no otorga competencia de armas/armaduras), pero la documentación promete una verificación contra el trasfondo que el código no realiza.

## 4. Huecos de datos

- Ninguno relevante para este personaje. `especies/especies.yaml#Elfo`, `trasfondos/trasfondos.yaml#Marinero` y `clases/paladin.yaml` tenían todo lo necesario (linajes, dote de trasfondo, equipo A/B, progresión completa con columnas extra `canalizar`/`prep`).
- Nota menor: `reglas/idiomas.yaml` no está referenciado por `verificar_personaje.py` en absoluto (no hay ninguna verificación de idiomas) — así que un idioma inventado en `competencias.idiomas` pasaría sin detectarse, igual que el bug real de la ronda anterior que motivó el comentario en `_ejemplo_aerin.yaml`. No lo probé por no desviarme del entregable, pero lo dejo anotado como hueco de cobertura del verificador, no de la base.

## 5. Salida final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/elfo_paladin.yaml
17 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```
