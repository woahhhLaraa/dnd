#!/usr/bin/env python3
"""Prueba por mutación del MOTOR (auditoría del 2026-09-05, fase 1.1).

Las otras 16 suites mutan **la base**: corrompen un YAML o un JSON y exigen
que un chequeo salte. Ninguna muta el motor. Medido antes de escribir esta:

    grep -l 'calculo\\.py"\\|efectos\\.py"' _verificacion/mutaciones_*.py
    → ni una

Y eso importa más de lo que parece, porque la ficha se escribe y se verifica
con el mismo código: `verificar_personaje.py --calcular` produce el bloque
`calculado` con `calculo`/`efectos`, y `verificar_calculado()` lo recalcula
con `calculo`/`efectos` y compara. **Un error en el motor produce una ficha
coherente y equivocada, y sale en verde.**

Lo que rompe el círculo no es un segundo calculador —dos implementaciones de
la misma regla divergen y nadie las compara: `_CA_SIN_ARMADURA` con más
pasos—. Lo rompe que las 18 fichas de `personajes/` llevan su `calculado`
CONGELADO en disco. Si el motor cambia y ninguna ficha se queja, es que
ninguna ficha ejercita ese trozo de motor.

Así que aquí se pincha el motor y se exige que **alguna ficha lo note**:

    · corrompe una operación de `agregar()`, del mínimo de PG, del estado de
      equipo o del filtro de condiciones;
    · corre las 18 fichas SIN `--calcular`, contra su `calculado` de disco;
    · una mutación que ninguna ficha caza es un HUECO DE COBERTURA
      ARITMÉTICA, y la suite lo nombra en vez de callárselo.

Esa lista de huecos es el encargo del mandato «el calculista» de la ronda 3
de estrés (`PLAN_ESTRES.md`): son los trozos de motor que hoy no protege
nada en absoluto.

    python3 _verificacion/mutaciones_motor.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def _sust(raiz, rel, viejo, nuevo, cuenta=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, cuenta), encoding="utf-8")


# ══ Mutaciones del motor ═════════════════════════════════════════════════
# Cada una es una regla del juego escrita en Python. Si nadie la nota, esa
# regla no la sostiene ninguna ficha.

# ── Reescritas el 2026-09-06 (fase 4) ────────────────────────────────────
# `agregar()` ya no lleva un bucle por operación: itera el
# `orden_de_agregacion` que declara la base y aplica `_AGREGADORES[op]`. Las
# mutaciones apuntan ahora a esa tabla, que es donde vive la aritmética.
#
# Y el cambio movió la cuenta: borrar un agregador ya no es invisible. Aunque
# ninguna ficha aplique un efecto `min`, `operaciones_agregadas()` exige que
# toda operación del `orden_de_agregacion` tenga implementación, y `agregar()`
# lo comprueba en cada cálculo. Tres huecos de cobertura se cerraron por una
# razón distinta a la prevista: no porque alguna ficha los ejercite, sino
# porque el vocabulario pasó a tener consumidor exhaustivo.

def m_add_invertido(r):
    _sust(r, "efectos.py", '    "add": lambda valor, n: valor + n,',
          '    "add": lambda valor, n: valor - n,')
    return "el agregador `add` resta en vez de sumar"


def m_min_borrado(r):
    _sust(r, "efectos.py", '    "min": lambda valor, n: max(valor, n),\n', "")
    return "desaparece el agregador `min`"


def m_max_borrado(r):
    _sust(r, "efectos.py", '    "max": lambda valor, n: min(valor, n),\n', "")
    return "desaparece el agregador `max`"


def m_set_borrado(r):
    _sust(r, "efectos.py", '    "set": lambda _valor, n: n,\n', "")
    return "desaparece el agregador `set`"


def m_orden_ignorado(r):
    """El orden lo declara la base y `agregar()` lo itera. Si el motor deja de
    leerlo y vuelve a un orden propio, las dos copias se separan otra vez."""
    _sust(r, "efectos.py", "    for op in orden:\n",
          '    for op in ("set", "add", "mul", "min", "max"):\n')
    return "`agregar()` deja de leer `orden_de_agregacion` y usa un orden propio"


def m_sin_redondeo(r):
    """El `math.floor` final. DiceCloud redondea hacia abajo salvo en las
    variables decimales; quitarlo deja CA y PG con parte fraccionaria."""
    _sust(r, "efectos.py", "return valor if decimal else math.floor(valor)",
          "return valor")
    return "se quita el `math.floor` final de la agregación"


def m_mul_invertido(r):
    _sust(r, "efectos.py", '    "mul": lambda valor, n: valor * n,',
          '    "mul": lambda valor, n: valor / n,')
    return "el agregador `mul` divide en vez de multiplicar"


def m_minimo_de_pg(r):
    """El mínimo de 1 por nivel (pdf 44 = libro 42, paso 2). La base lo trae
    estructurado en `puntos_golpe…metodos[tirar].minimo` y Python lo cablea:
    es además una unidad de la fila 8."""
    _sust(r, "calculo.py", "return max(1, valor + con_mod)",
          "return max(0, valor + con_mod)")
    return "el mínimo de 1 de los PG por nivel pasa a 0"


def m_pg_nivel_1_sin_constitucion(r):
    _sust(r, "calculo.py", "def puntos_golpe_nivel_1", "def puntos_golpe_nivel_1")
    p = r / "calculo.py"
    t = p.read_text(encoding="utf-8")
    i = t.index("def puntos_golpe_nivel_1")
    j = t.index("\ndef ", i + 10)
    trozo = t[i:j]
    assert "con_mod" in trozo
    t = t[:i] + trozo.replace("+ con_mod", "+ 0", 1) + t[j:]
    p.write_text(t, encoding="utf-8")
    return "los PG del nivel 1 dejan de sumar el modificador por Constitución"


def m_estado_de_equipo_invertido(r):
    """`sin_armadura` es la condición de la que cuelgan las cuatro fórmulas de
    CA base de la base (Bárbaro, Monje, y dos subclases).

    Reescrita el 2026-09-06: desde la fase 4, el sentido de cada condición es
    un DATO (`negada:` en `reglas/efectos.yaml`) y `estado_de_equipo()` lo
    aplica genéricamente. Invertir esa aplicación intercambia todas las
    condiciones a la vez, que es la versión de motor de lo que antes eran dos
    mutaciones sobre dos pares escritos a mano."""
    _sust(r, "efectos.py",
          "return {nombre: (not lleva(grupos)) if negada else lleva(grupos)",
          "return {nombre: lleva(grupos) if negada else (not lleva(grupos))")
    return "`estado_de_equipo()` invierte el sentido de todas las condiciones"


def m_negada_ignorada(r):
    """Y la otra mitad: que el motor deje de mirar el `negada` de la base y
    trate todas las condiciones como afirmativas. `sin_armadura` pasaría a ser
    verdadera solo cuando SÍ se lleva armadura."""
    _sust(r, "efectos.py",
          "return {nombre: (not lleva(grupos)) if negada else lleva(grupos)",
          "return {nombre: lleva(grupos)")
    return "`estado_de_equipo()` deja de mirar el `negada:` que declara la base"


def m_condiciones_ignoradas(r):
    """Si `aplica()` deja de mirar `requiere`, TODOS los efectos condicionados
    se aplican siempre: la CA sin armadura del Bárbaro se sumaría llevando
    cota de malla."""
    p = r / "efectos.py"
    t = p.read_text(encoding="utf-8")
    i = t.index("def aplica(")
    j = t.index("\ndef ", i + 10)
    trozo = t[i:j]
    assert "requiere" in trozo, "aplica() ya no mira `requiere`"
    p.write_text(t[:i] + trozo.replace("return ", "return True or ", 1) + t[j:],
                 encoding="utf-8")
    return "`aplica()` deja de mirar `requiere`: todo efecto se aplica siempre"


# Tabla de migración de la línea base del 2026-09-05, que guardaba FRASES, a
# la de hoy, que guarda ids. Se escribe una vez y se queda como registro de
# qué era cada cosa; en cuanto el fichero está en el formato nuevo no se usa.
# La tabla de migración de la línea base del 2026-09-05 —que guardaba FRASES— y
# el elenco de aquel día vivieron aquí hasta el 2026-09-06. Ya no hacen falta:
# el fichero está en el formato de `deuda.Deuda`, con sus ids y su elenco
# dentro, y su historia quedó escrita en el propio JSON (`_migracion_plan21`).
# Borrarlas es parte del punto: la migración se hace una vez, no se conserva
# como código muerto que alguien tenga que volver a entender.

MUTACIONES = [
    m_add_invertido, m_mul_invertido, m_min_borrado, m_max_borrado,
    m_set_borrado, m_sin_redondeo, m_orden_ignorado,
    m_minimo_de_pg, m_pg_nivel_1_sin_constitucion,
    m_estado_de_equipo_invertido, m_negada_ignorada, m_condiciones_ignoradas,
]


# ══ Arnés ════════════════════════════════════════════════════════════════
def _fichas(raiz):
    return sorted((raiz / "personajes").glob("*.yaml"))


def _quien_falla(raiz):
    """Qué fichas se quejan. NUNCA se llama con `--calcular`: el sentido de
    esta suite es contrastar el motor contra el `calculado` congelado."""
    culpables = []
    for f in _fichas(raiz):
        r = subprocess.run([sys.executable, "verificar_personaje.py", str(f)],
                           cwd=raiz, capture_output=True, text=True)
        if r.returncode != 0:
            culpables.append(f.name)
    return culpables


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)

    intactas = _quien_falla(BASE)
    if intactas:
        print(f"✗ CONTROL: con el motor sin tocar ya fallan {intactas}. "
              f"Arréglalo antes de mutar.")
        return 1
    print(f" ✅ control · las {len(_fichas(BASE))} fichas pasan con el motor intacto\n")

    cazadas, huecos = 0, {}
    for mut in MUTACIONES:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            culpables = _quien_falla(raiz)
            if culpables:
                cazadas += 1
                print(f" ✅ {desc}")
                print(f"      la cazan {len(culpables)}: {', '.join(culpables[:3])}"
                      + (" …" if len(culpables) > 3 else ""))
            else:
                huecos[mut.__name__] = desc
                print(f" ❌ {desc}")
                print("      ↑ NINGUNA ficha la caza: es un hueco de cobertura "
                      "aritmética, no un fallo de esta suite")

    print("─" * 74)

    # La deuda va ENUMERADA y solo puede bajar. La contabilidad la lleva
    # `deuda.Deuda` desde la fase 1 del PLAN_21: este fichero era el ÚNICO de
    # los cinco que sabía podar, distinguir lo nuevo de lo perdido y guardar el
    # elenco —lo aprendió el último día y a golpes—, y por eso es el modelo del
    # que salió la abstracción. Aquí se queda solo lo que es suyo: qué es un
    # hueco y cómo se salda.
    import sys as _sys
    _sys.path.insert(0, str(BASE))
    import deuda as D

    dd = D.Deuda(
        "_verificacion/motor_sin_carga.json",
        nota=("Trozos del motor que NINGUNA ficha de `personajes/` protege: se "
              "pueden corromper y todas las fichas siguen verificando en "
              "verde. Es deuda enumerada, no permiso."),
        como_se_salda=("escribiendo fichas que ejerciten esa aritmética —el "
                       "mandato «el calculista»— o dándole al vocabulario un "
                       "consumidor exhaustivo, que es como se cerraron `min`, "
                       "`max` y `set` en la fase 4 del PLAN_20"),
        identidad="nombre-de-mutacion",
        identidad_explicada=("el NOMBRE de la función de mutación. Nunca su "
                             "descripción: reescribir una frase hacía que el "
                             "mismo hueco saliera como nuevo y esta suite "
                             "gritara «cobertura perdida», que era falso"))
    inf = dd.contrastar(dict(huecos), elenco_hoy={m.__name__ for m in MUTACIONES})
    inf.imprimir("Trozos de motor que hoy no protege ninguna ficha —se saldan "
                 "escribiendo fichas que los ejerciten o dando consumidor al "
                 "vocabulario, no tocando esta lista:")

    total = len(MUTACIONES)
    print(f"   {cazadas} cazadas por alguna ficha · {len(huecos)} declaradas "
          f"como deuda en `motor_sin_carga.json` · línea base: {inf.linea_base}")
    if inf.perdidos:
        print(f"❌ {len(inf.perdidos)} trozo(s) de motor que antes protegía "
              f"alguna ficha y ya no")
    else:
        print("✅ ninguna cobertura de motor perdida")
    print(f"{cazadas + len(huecos)}/{total}")
    return 1 if inf.hay_regresion else 0


if __name__ == "__main__":
    sys.exit(main())
