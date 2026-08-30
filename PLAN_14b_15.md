# Plan de acción — cerrar la Fase 14 y ejecutar la Fase 15

> Escrito el **2026-08-30**. Todas las cifras de este plan están **medidas**,
> no estimadas: los comandos que las producen están al final de cada bloque.
> Si vuelves a este documento y no cuadran, la base ha cambiado y el plan
> también.

## Lo primero: las dos fases son mucho más pequeñas de lo que decían los documentos

`CONTINUAR.md` describía la 14b como «extenderlo a 391 registros con ~11 % de
residuo», que suena a mes de trabajo y a codificar reglas falsas con su cita al
lado. **No es eso.** Medido sobre `hechizos.json`:

| Superficie | Cifra real |
|---|---|
| Conjuros con **más de una** mención de salvación | **17** |
| Conjuros con salvaciones de **características DISTINTAS** — los que rompen de verdad el campo único | **5** (*Estática sináptica*, *Mano de Bigby*, *Muro de hielo*, *Símbolo*, *Muro prismático*) |
| Conjuros con viñetas o ≥4 puntos y coma | 18 |
| Conjuros con «elige uno / cada capa / modo» | 14 |
| **Unión de candidatos a necesitar lista** | **18** |
| Materiales compuestos ya identificados | **6** (`COSTE_COMPUESTO`) |

**18 conjuros, no 391.** Los 373 restantes tienen una tirada y un material, y el
registro plano los representa bien. Eso convierte la 14b de «remodelar la base»
en **un trabajo acotado y verificable**.

Y la Fase 15 tiene un vocabulario **cerrado y minúsculo**: 75 dotes, 65 con
prerrequisito, y **11 formas distintas** en total.

---

# FASE 14b — cerrar el motor de efectos

## Orden, y por qué es ese

Se ataca primero lo que **tiene red**. La lección de la 14 fue que la suite de
12 fichas cazó un defecto de modelado que ningún chequeo de forma habría visto;
estrenar un modelo nuevo donde existe esa red y no donde no existe es lo que
convirtió aquello en un fallo de una tarde en vez de en un defecto silencioso.

### ✅ 14b-1 · `pg_max` deja de ser un escalar y pasa a ser historia por nivel — **HECHA (2026-08-30)**

**Por qué va primero:** es el mismo salto de modelo que los conjuros (campo
plano → lista), **tiene test de aceptación duro** (las 12 fichas) y es
**prerrequisito de la Fase 16**. Estrena el patrón en material limpio.

1. Añadir a `personajes/_ESQUEMA.md` el bloque `pg_por_nivel`: una entrada por
   nivel con `metodo: tirada|valor_establecido`, el `valor` obtenido y la cita.
   Una tirada no es reproducible: **se guarda el resultado**, no la fórmula.
2. `efectos.py`: `pg_max` recibe como base
   `Σ(pg_por_nivel) + nivel_total × mod_con` en vez de un escalar.
   ⚠️ **El término de Constitución se recalcula entero, no se acumula**
   (`pdf 44 = libro 42`, paso 5: retroactivo). Un motor que sume «lo ganado en
   el nivel N» acierta hasta la primera dote que suba Constitución.
3. `validar.py` / `verificar_personaje.py`: el nivel 1 usa la regla del máximo
   del dado (`pdf 42`); los niveles 2+ usan `puntos_golpe.niveles_siguientes_al_1`.
   El «mínimo de 1» es **del total**, no del dado.
4. **Criterio de cierre:** 12/12 fichas siguen verificando, y una ficha nueva de
   nivel ≥2 verifica con los dos métodos.

**Cerrada.** 13/13 fichas (la nueva es `draconido_hechicero_n3.yaml`, Hechicero 3
con Hechicería Dracónica: ejercita los tres métodos y los dos efectos de
*Resistencia dracónica*). `mutaciones_pg.py` 9/9 → **13/13**, con una mutación
dedicada a la retroactividad. Registro en `FUENTES.md`.

**Queda declarada, no resuelta**, la pregunta abierta ya anotada: si el mod. Con
empeora después, la página no dice si se recalcula hacia atrás el mínimo de 1.

### ✅ 14b-2 · Materiales compuestos: de excepción declarada a dato — **HECHA (2026-08-30)**

Los **6** conjuros de `COSTE_COMPUESTO` viven hoy como una **lista de
excepciones en prosa dentro de `verificar_foundry.py`**. Eso los saca del
contraste externo en vez de representarlos.

1. `materiales: [{nombre, coste, unidad, consume, por_unidad}]` en el registro
   del conjuro. `por_unidad` es lo que distingue «50 po **cada uno** de un par»
   de «100 po» — el **modo de fallo nº 10** («dato agregado») que ya mordió dos
   veces.
2. `coste` se conserva **derivado** de `materiales` para no romper nada, nunca
   escrito a mano. Regla 3 del esquema de efectos: lo ya estructurado no se
   duplica.
3. `COSTE_COMPUESTO` deja de ser una lista de excepciones y pasa a ser lo que
   `verificar_foundry.py` **comprueba**: que la descomposición cuadre con el SRD.

**Criterio de cierre:** los 3012 valores del contraste externo siguen en 0
discrepancias, y los 6 conjuros dejan de estar exentos.

**Cerrada, y encontró más de lo previsto.** El contraste pasó de 3012 a **3020**
valores (0 discrepancias) y aparecieron **dos sumas nuevas** que la página nunca
imprime: *Proyección astral* (1100 = 1000 + 100) y *Conocer las leyendas*
(200 = 4 × 50). Van cuatro en total. Además, el **consumo resultó ser por
material**, no por conjuro. `mutaciones_materiales.py` → 10/10. Registro en
`FUENTES.md`.

### ✅ 14b-3 · `tiradas` como lista, solo donde hace falta — **HECHA (2026-08-30)**

1. **Los 5 duros primero.** Cada uno con **doble lectura independiente** de su
   página (dos agentes Sonnet, briefing escrito, sin verse los informes) — es la
   regla del proyecto, y aquí es obligatoria: se va a **codificar** la regla, y
   *un error con su cita al lado es un error que nadie vuelve a comprobar*
   (amenaza nº 1 del FODA).
2. **Los 13 restantes** se revisan con el mismo método solo si el script los
   sigue marcando después de tener el modelo.
3. `tirada` (singular) **se conserva derivado** de `tiradas` cuando la lista
   tiene un solo elemento — `validar_tirada()` y sus 24 mutaciones siguen
   valiendo sin tocarlos.
4. **El enlace manda sobre la copia.** Cada efecto de conjuro apunta a su
   `pagina` y **no reproduce el texto**: con ~11 % de residuo, corregir la base
   tiene que seguir arreglando el motor.

**Criterio de cierre:** `validar_tirada()` en 0, los 18 candidatos resueltos o
declarados, y ningún conjuro con lista sin doble lectura registrada en
`FUENTES.md`.

**Cerrada, y los «5 duros» resultaron ser 4.** *Estática sináptica* era un falso
positivo de la heurística: su segunda característica venía de «salvación de
Constitución **para mantener la concentración**», que es la regla de
concentración citada de pasada. Los cuatro reales se leyeron **dos veces cada
uno** —y dos de ellos hicieron falta **cuatro** lecturas, porque su cuerpo se
parte de página y ambos lectores avisaron por separado de que faltaba texto.
`mutaciones_tiradas.py` → 13/13. Registro en `FUENTES.md`.

### 14b-4 · Chequeos, mutación y documentos

- `validar_efectos()` cubre también los efectos de conjuro.
- `_verificacion/mutaciones_efectos.py` crece con la familia **AUSENCIA**: una
  descripción con dos salvaciones de características distintas y **una sola**
  entrada en `tiradas` debe saltar. Es el defecto que de verdad existe.
- `verificar_documentos.py` y `cobertura.py` se actualizan **en la misma tanda**,
  no al final: tres documentos desfasados en una sesión ya costaron caro.

---

# ✅ FASE 15 — prerrequisitos de dote evaluables — **HECHA (2026-08-30)**

## El inventario, medido

75 dotes en 4 ficheros · **65 con prerrequisito** · 10 sin él. Y **11 formas**:

| Veces | Forma |
|---|---|
| 29 | `nivel N o más` |
| 10 | `rasgo Estilo de combate` |
| 9 | `nivel N o más, <CAR> o <CAR> N o más` |
| 7 | `nivel N o más, <CAR> N o más` |
| 3 | `nivel N o más, rasgo Lanzamiento de conjuros o Magia del pacto` |
| 2 | `nivel N o más, entrenamiento con armaduras medias` |
| 1 c/u | armaduras ligeras · armaduras pesadas · escudos · `rasgo Lanzamiento de conjuros` · `nivel N o más; <CAR>, <CAR> o <CAR> N o más` |

**Cuatro átomos y dos conectores. Eso es todo:**

- `nivel ≥ N` · `caracteristica ≥ N` · `tiene_rasgo <nombre>` ·
  `entrenamiento_con <categoría>`
- la coma (y un `;`) son **Y**; el «o» dentro de un término es **O**.

**Decisión que ahorra trabajo, y conviene dejarla escrita:** `ANALISIS_REPOS.md`
propone la idea de PCGen (`PREMULT:N`, negación con `!`). **No hace falta.** En
los 65 prerrequisitos reales **no hay ni una negación ni un «N de M»**. Copiar
ese vocabulario sería inventar expresividad que nada usa. Si algún día aparece,
se añade entonces.

## Pasos

### 15-1 · Gramática cerrada
`reglas/prerrequisitos.yaml`: los 4 átomos, los 2 conectores, y la lista cerrada
de categorías de entrenamiento. Mismo patrón que `reglas/efectos.yaml`.

### 15-2 · Los 65, como dato
Se **derivan del texto que ya está en la base y ya fue auditado** (Fase 13n:
dotes, trasfondos y equipo, tasa 0,72 %). **No hace falta reabrir el manual**, y
conviene decirlo: es trabajo de parsing y criterio, no de lectura visual.

### 15-3 · El chequeo fuerte: ida y vuelta
`validar_prerrequisitos()` hace **round-trip**: parsea la prosa a estructura,
**regenera la prosa desde la estructura** y exige que sea idéntica al original.

Es barato y demuestra lo que importa: que **no se perdió ni se inventó nada** al
estructurar. Un parser que ignore un término en silencio hace exactamente lo que
hizo el CSV de origen — dar algo plausible y equivocado.

Y un segundo chequeo: cada `tiene_rasgo` y cada `entrenamiento_con` debe
resolver contra un registro real (`clases/rasgos/`, `equipo/armaduras.yaml`).
Un rasgo mal escrito es el bug `Clerigo` otra vez.

### 15-4 · Prueba por mutación
`_verificacion/mutaciones_prerrequisitos.py`, con las dos mitades de siempre:
**forma** (átomo inventado, conector inventado, rasgo inexistente) y **ausencia**
(un término del texto que no aparece en la estructura → lo caza el round-trip).
Y controles negativos: reordenar términos, y las 10 dotes **sin** prerrequisito,
que no son un defecto.

### 15-5 · Que sirva para algo
`buscar.py`: `dotes_disponibles(ficha)` que evalúa los prerrequisitos contra el
personaje y **falla ruidosamente**. Cero resultados es un error, nunca una lista
vacía — es la regla que nació del bug `Clerigo`.

**Criterio de cierre:** los 65 parsean con round-trip exacto, mutaciones en
verde, y `cobertura.py` responde «¿qué dotes puede tomar este personaje?» — una
pregunta que hoy **no sabe hacer**.

**Cerrada.** Ida y vuelta **65/65 exacto a la primera**, `mutaciones_prerrequisitos.py`
10/10, `buscar.dotes_disponibles()` con el porqué de cada dote, y `cobertura.py`
de 27 a **31 preguntas**. **Una desviación deliberada del paso 15-2:** la
estructura **no** se guarda junto a la prosa — se deriva. Guardarla sería
duplicar un dato derivable, que es la regla 3 del esquema de efectos y el modo
de fallo nº 10. Registro en `FUENTES.md`.

---

## Riesgo principal, y cómo se contiene

El de siempre, y esta vez con un multiplicador: **codificar una regla con su cita
al lado convierte un error en algo que nadie vuelve a comprobar.** Se contiene
con tres cosas que ya funcionaron en la 14:

1. **Enlace a la cita, nunca copia del texto.**
2. **Doble lectura independiente** para todo lo que se codifique desde el manual
   (los 5 conjuros duros). Un informe de agente en blanco no prueba nada.
3. **Ningún chequeo se cree hasta que una mutación lo ha visto fallar.**

## Cómo se comprueba que este plan se cumplió

```bash
python3 validar.py && python3 verificar_srd.py && python3 verificar_foundry.py
python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 _verificacion/mutaciones_efectos.py
python3 _verificacion/mutaciones_pg.py
python3 _verificacion/mutaciones_prerrequisitos.py   # nuevo, Fase 15
python3 verificar_documentos.py
```

Y los inventarios que fijan las cifras de arriba, para volver a medirlos:

```bash
# 18 candidatos a lista de efectos, 5 duros
python3 - <<'PY'
import json, re
H = json.load(open('hechizos.json'))['hechizos']
r = re.compile(r"salvaci[oó]n de (Fuerza|Destreza|Constituci[oó]n|Inteligencia|Sabidur[ií]a|Carisma)", re.I)
duros = [h['nombre'] for h in H if len({c.lower() for c in r.findall(h.get('descripcion') or '')}) > 1]
print(len(duros), duros)
PY

# 11 formas de prerrequisito sobre 65 dotes
python3 - <<'PY'
import yaml, glob, re, collections
c = collections.Counter()
for f in glob.glob('dotes/*.yaml'):
    for d in yaml.safe_load(open(f))['dotes']:
        if d.get('prerrequisito'):
            p = re.sub(r"\b(Fuerza|Destreza|Constitución|Inteligencia|Sabiduría|Carisma)\b", "<CAR>", d['prerrequisito'])
            c[re.sub(r"\d+", "<N>", p)] += 1
print(sum(c.values()), 'prerrequisitos ·', len(c), 'formas')
PY
```
