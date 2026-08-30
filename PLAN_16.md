# ✅ Plan de acción — Fase 16: `/subir-nivel` — **EJECUTADO (2026-08-30)**

> Escrito y ejecutado el **2026-08-30**. Las cifras están **medidas**, no
> estimadas; los comandos que las producen están al final.

## Lo que la Fase 16 se encuentra hecho

Las Fases 14 y 15 le dejaron resuelto casi todo lo que la bloqueaba:

- **los PG de cada nivel se calculan** desde `pg_por_nivel` (14b-1), con la
  retroactividad de Constitución saliendo sola;
- **las reglas de personaje son dato citado** que agrega `efectos.py` (14);
- **las dotes se filtran por prerrequisito** con `buscar.dotes_disponibles()` (15).

## 🔴 Y una deuda que la Fase 14 dejó, y hay que pagar primero

**La Fase 14 rompió un paso documentado de la skill `/personaje` y nadie se
enteró.** Su paso 10 manda ejecutar:

```bash
python3 calculo.py ca --des 16 --con 14 --sab 14 --clase Monje
```

y desde la Fase 14 eso **sale con error** a propósito (la CA de 4 clases la
fija un rasgo y la función se niega a adivinar). Es correcto que falle, pero la
skill sigue mandándolo. **Ningún chequeo mira las skills**, así que el desfase
vivía igual que vivían los documentos de estado antes de
`verificar_documentos.py`.

## El inventario de «qué puede pasar al subir de nivel», medido

Foundry resuelve esto con nueve tipos de *advancement* (`ANALISIS_REPOS.md` §2).
De esos nueve, **lo que nuestra base ejercita de verdad** es:

| Qué pasa | Dónde está en la base | Cuánto |
|---|---|---|
| Rasgo nuevo de clase | `progresion[].rasgos[]` + `clases/rasgos/` | todos los niveles |
| **Subclase** | marcador `Subclase de <clase>` | **12x, siempre en nivel 3** |
| **Mejora de característica** (o dote) | marcador `Mejora de característica` | **51x**, niveles 4, 6, 8, 10, 12, 14, 16 |
| **Rasgo de subclase** | marcador `Rasgo de subclase` | **35x**, niveles 6-20 |
| **Valor de tabla** (`ScaleValue`) | columnas numéricas de `progresion` | 12 clases, 1-5 columnas cada una |
| Espacios de conjuro | columna `slots` / `espacios` | las lanzadoras |
| Puntos de golpe | `reglas/generacion_personaje.yaml → puntos_golpe` | todos |
| Bonificador por competencia | columna `pb` | todos |

**No se copian los nueve tipos de Foundry.** `Size` y `ModifyItem` no los usa
nada en esta base; declararlos sería la misma expresividad inventada que la
Fase 15 rechazó de PCGen.

## Los pasos

### 16-0 · Pagar la deuda: `/personaje` vuelve a funcionar
`verificar_personaje.py --calcular` imprime el bloque `calculado` que la ficha
debería tener, usando el motor de efectos. La skill deja de llamar a
`calculo.py ca --clase` y usa eso.

### 16-1 · `reglas/subida_de_nivel.yaml`
El vocabulario cerrado de lo que puede pasar, con su procedencia en la base.

### 16-2 · `subir_nivel.py`
Dado `(ficha, nivel destino)`, **deriva de la base** la lista de lo que ocurre y
qué hay que elegir. Determinista y **falla ruidosamente**: un nivel sin nada que
conceder es un error, nunca una lista vacía.

### 16-3 · `validar_subida()`
Los 12 × 19 saltos de nivel producen lista resoluble, y todo marcador cae en un
nivel que la base sabe explicar.

### 16-4 · Subir una ficha de verdad
`draconido_hechicero_n3.yaml` → nivel 4: ejercita PG por elección, la
**Mejora de característica vs dote** (con `dotes_disponibles`) y el reverificado.

### 16-5 · La skill `/subir-nivel`
Orquesta lo anterior. **No decide reglas**: las pide a los scripts.

### 16-6 · Mutaciones y documentos
`mutaciones_subida.py`, y `verificar_documentos.py` pasa a comprobar **también
que los comandos citados en las skills funcionen** — la deuda de 16-0 no se
vuelve a repetir.

## Cómo se comprueba

```bash
python3 validar.py && python3 verificar_srd.py && python3 cobertura.py
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 subir_nivel.py --ficha personajes/draconido_hechicero_n3.yaml --a 4
python3 _verificacion/mutaciones_subida.py
python3 verificar_documentos.py
```

---

## Resultado

| Paso | Resultado |
|---|---|
| 16-0 | `verificar_personaje.py --calcular` imprime el bloque `calculado`; `/personaje` paso 10 corregido |
| 16-1 | `reglas/subida_de_nivel.yaml`, con los tipos que la base **ejercita de verdad** (no los nueve de Foundry) |
| 16-2 | `subir_nivel.py` separa `concede` de `elige` y falla ruidosamente |
| 16-3 | `validar_subida()` → **333 saltos** (12 clases × niveles 2-20, y los de subclase una vez por subclase), **0 errores**, 8 segundos |
| 16-4 | `personajes/draconido_hechicero_n4.yaml`: subido de 3 a 4, `pg_max` 24 → **31**, dote *Lanzador ritual* elegida por prerrequisito |
| 16-5 | Skill `/subir-nivel` |
| 16-6 | `mutaciones_subida.py` **7/7** · `verificar_documentos.py` comprueba ahora **también las skills** |
