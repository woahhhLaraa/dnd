# Hallazgos — Goliat Druida / Guía (nivel 1)

## 1. Qué funcionó bien

- `python3 validar.py && python3 verificar_srd.py && python3 cobertura.py` pasó limpio
  (0 errores, 0 preguntas sin cubrir) antes de empezar.
- `buscar.py clase Druida` entrega `atributos_basicos` completo (dado, salvaciones,
  habilidades, armas/armaduras/herramientas, equipo inicial A/B, `lanzador`,
  `aptitud_magica`) en una sola llamada — suficiente para toda la ficha sin tocar
  `clases/druida.yaml` a mano.
- `buscar.py conjuros-de Druida --nivel 0/1` filtra bien por clase y nivel.
- `calculo.py pg/ca/pb/cd-conjuros/ataque-conjuros` cubrió toda la aritmética
  necesaria; `ca` detecta armadura/escudo por nombre y clase sin que haya que
  calcular el modificador de Destreza a mano.
- El nuevo formato `categoria:` (en vez de `ref:`) para
  `competencias.armas/armaduras` funciona exactamente como describe el
  `_ESQUEMA.md` corregido, y `verificar_categorias()` lo valida contra
  `atributos_basicos` de la clase sin falsos positivos.
- La regla de `cualesquiera` no aplicó aquí (Druida tiene lista cerrada de 8
  habilidades), pero se revisó que Sigilo (trasfondo) no estuviera exigida
  también en la clase — sin conflicto.
- `verificar_personaje.py personajes/goliat_druida.yaml` → **0 problemas** en el
  primer intento tras resolver el punto 2 de abajo.

## 2. Bugs o comportamientos raros

### Desajuste entre `_ESQUEMA.md` y `verificar_personaje.py` para `competencias.herramientas` de origen trasfondo

`_ESQUEMA.md`, regla 6, dice textualmente:

> `competencias.armas`/`.armaduras`/`.herramientas` van como `categoria:`
> (texto literal), no como `ref:` — se comprueban contra la lista real de
> `atributos_basicos` de la clase (**o del trasfondo cuando aplique**), no
> contra `equipo/`.

Pero `verificar_categorias()` en `verificar_personaje.py` (líneas ~95-113) solo
construye `permitidas` recorriendo `ficha.get("clases", [])`; nunca mira
`ficha["trasfondo"]`. El trasfondo Guía concede una herramienta fija
("herramientas de cartógrafo", campo `herramienta` de
`trasfondos/trasfondos.yaml#Guía`) que **no** aparece en
`atributos_basicos.herramientas` de Druida (`["Útiles de herborista"]`).

Repro:
```
competencias:
  herramientas:
    - {categoria: "Útiles de herborista", origen: {clase: Druida}}
    - {categoria: "Herramientas de cartógrafo", origen: {trasfondo: Guía}}
```
da:
```
✗ competencias.herramientas: 'Herramientas de cartógrafo' no está en lo que
  conceden las clases del personaje (['Útiles de herborista'])
```
(reproducido localmente antes de cambiar el formato; no se dejó en el yaml final).

**Workaround usado en la ficha final:** como "Herramientas de cartógrafo" SÍ es
un registro real de `equipo/herramientas.yaml` (a diferencia de una categoría
de arma, que no existe como registro individual), se referenció con `ref:`
en vez de `categoria:`. `_recorrer_refs()` la valida sin problema, y el propio
comentario del código (`# entradas antiguas con ref: las cubre
_recorrer_refs`) confirma que es una ruta que el verificador tolera. El
resultado final pasa con 0 problemas, pero es un parche de la ficha, no una
prueba de que la regla 6 esté implementada como la documenta el esquema.

**Recomendación (no aplicada, toca código vetado):** o bien
`verificar_categorias()` amplía `permitidas` con `trasfondo.get("habilidades"
... )` → en realidad con el campo `herramienta` del trasfondo (y quizá
`armas`/`armaduras` si algún trasfondo llegara a conceder alguna), o bien
`_ESQUEMA.md` se corrige para decir que las herramientas de origen trasfondo
van como `ref:` a `equipo/herramientas.yaml` (ya que sí son objetos reales),
reservando `categoria:` solo para lo que concede la clase.

## 3. Documentación confusa

- La regla 6 de `_ESQUEMA.md` (citada arriba) promete una comprobación contra
  trasfondo que el código no hace — ver punto 2. Cuesta notarlo sin correr el
  verificador y leer su fuente, porque el ejemplo (`_ejemplo_aerin.yaml`) no
  tiene ninguna herramienta de trasfondo poblada (`herramientas: []`), así que
  el caso no aparece ilustrado.
- `equipo/aventureros.yaml` describe "Canalizador druídico" como entrada
  genérica en `descripciones`, pero la tabla real de variantes
  (`canalizadores_druidicos`) usa el nombre largo `"Bastón de madera (también
  bastón)"`, no `"Bastón"` a secas. El texto de
  `atributos_basicos.equipo_inicial.a` de Druida dice literalmente
  "canalizador druídico (bastón)", lo que podría tentar a alguien a escribir
  `ref: "equipo/aventureros.yaml#Bastón"` — y ahí resolvería, pero al objeto
  equivocado (el "Bastón" de `equipo/aventureros.yaml` es un ítem de precio
  "5 po" sin relación declarada con canalizadores, y además "Bastón" también
  existe como arma en `equipo/armas.yaml`, con datos de daño). El ejemplo
  Aerin ya avisa de esta ambigüedad para "Canalizador arcano" / "Bastón",
  pero no hay un aviso equivalente para "Canalizador druídico" — se
  recomienda que quien construya una ficha de Druida/Explorador use la
  ref genérica `equipo/aventureros.yaml#Canalizador druídico` con
  `origen.variante: "Bastón de madera (también bastón)"`, igual que hace
  Aerin con `Canalizador arcano` + `variante: orbe`, en vez de referenciar
  `#Bastón` directamente.

## 4. Huecos de datos

- Ninguno bloqueante. La dote fija de Guía, "Iniciado en la magia (druida)",
  resolvió sin problema contra `dotes/origen.yaml#Iniciado en la magia`
  (dote genérica y repetible; el "(druida)" es la lista de conjuros elegida,
  no un registro aparte).
- El rasgo "Orden primigenia" de Druida (nivel 1) es una elección binaria
  (Guardián/Naturalista) descrita solo en la prosa de
  `clases/rasgos/druida.yaml`, no en un campo estructurado — no bloquea nada
  porque la prosa es clara y citable, pero si en el futuro se automatiza esta
  elección (como se hizo con `atributos_basicos.habilidades.elige`), Orden
  primigenia sería candidata a estructurarse igual.

## 5. Salida final de `verificar_personaje.py`

```
$ python3 verificar_personaje.py personajes/goliat_druida.yaml
29 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```

Ficha: `personajes/goliat_druida.yaml` — Goliat / Druida (Orden primigenia:
Naturalista) / trasfondo Guía, nivel 1. `calculado`: PG 10, CA 14 (cuero +
escudo), BC +2, CD conjuros 13, ataque de conjuros +5.
