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
# Y el ELENCO de mutaciones que existía el 2026-09-05, que aquel fichero no
# guardaba. Sin él no se puede distinguir «una mutación nueva mide un trozo que
# nunca estuvo cubierto» de «una mutación que se cazaba ha dejado de cazarse»,
# y la suite llamaba regresión a lo primero.
_ELENCO_2026_09_05 = (
    "m_add_invertido", "m_mul_invertido", "m_min_borrado", "m_max_borrado",
    "m_set_borrado", "m_sin_redondeo", "m_minimo_de_pg",
    "m_pg_nivel_1_sin_constitucion", "m_estado_de_equipo_invertido",
    "m_escudo_invertido", "m_condiciones_ignoradas",
)

_ID_DE_FRASE = {
    "el bucle `mul` divide en vez de multiplicar": "m_mul_invertido",
    "desaparece el bucle `min` de la agregación": "m_min_borrado",
    "desaparece el bucle `max` de la agregación": "m_max_borrado",
    "desaparece el bucle `set` de la agregación": "m_set_borrado",
    "se quita el `math.floor` final de la agregación": "m_sin_redondeo",
    "el mínimo de 1 de los PG por nivel pasa a 0": "m_minimo_de_pg",
    "`aplica()` deja de mirar `requiere`: todo efecto se aplica siempre":
        "m_condiciones_ignoradas",
}


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

    cazadas, huecos = 0, []
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
                huecos.append((mut.__name__, desc))
                print(f" ❌ {desc}")
                print("      ↑ NINGUNA ficha la caza: es un hueco de cobertura "
                      "aritmética, no un fallo de esta suite")

    print("─" * 74)

    # La deuda va ENUMERADA y solo puede bajar — el patrón de
    # `chequeos_silenciosos.json` y `rasgos_sin_declarar.json`.
    #
    # ── La identidad es el NOMBRE de la mutación, no su descripción ──────
    # Hasta el 2026-09-06 la línea base guardaba las frases, y eso hacía que
    # el fichero mintiera en las dos direcciones: al reescribir la descripción
    # de `m_mul_invertido` («el bucle `mul`» → «el agregador `mul`») el mismo
    # hueco salió como HUECO NUEVO y la suite dijo «un trozo que antes
    # protegía alguna ficha y ya no», que era falso. Es la misma lección que
    # `verificar_chequeos.py` aprendió esta misma semana con las gemelas: la
    # huella tiene que ser lo que identifica, no lo que se lee.
    #
    # Y con el id estable se puede distinguir lo que de verdad importa:
    #   · un hueco bajo un id que ANTES SE CAZABA  → cobertura perdida, ROJO;
    #   · un hueco bajo un id NUEVO                → una mutación nueva que
    #     mide un trozo que nunca estuvo cubierto. Eso no es una regresión,
    #     es medir mejor, y se anota.
    import json
    base_f = pathlib.Path(__file__).parent / "motor_sin_carga.json"
    _NOTA = ("Trozos del motor que NINGUNA ficha de `personajes/` protege: se "
             "pueden corromper y todas las fichas siguen verificando en verde. "
             "Es deuda enumerada, no permiso. Solo puede bajar por cobertura "
             "perdida, y se salda escribiendo fichas que ejerciten esa "
             "aritmética —el mandato «el calculista»— o dándole al vocabulario "
             "un consumidor exhaustivo, que es como se cerraron `min`, `max` y "
             "`set` en la fase 4. La clave de cada entrada es el NOMBRE de la "
             "mutación, no su texto: reescribir una descripción no puede "
             "parecer una regresión.")
    declarados, elenco_previo = {}, set(_ELENCO_2026_09_05)
    if base_f.exists():
        d = json.loads(base_f.read_text(encoding="utf-8"))
        declarados = d.get("huecos_por_id") or {}
        if d.get("mutaciones"):
            elenco_previo = set(d["mutaciones"])
        if not declarados and d.get("huecos"):
            # Migración única desde la línea base por FRASES (2026-09-06). Se
            # emparejan por el texto que cada mutación devuelve hoy; la que no
            # case es una descripción reescrita, y entra por su id igual.
            declarados = {}
            for h in d["huecos"]:
                declarados[_ID_DE_FRASE.get(h, h)] = h

    ids_hoy = {n for n, _d in huecos}
    nombres = {m.__name__ for m in MUTACIONES}
    # Cerrado: estaba declarado como hueco y hoy lo caza algo.
    cerrados = [n for n in declarados if n in nombres and n not in ids_hoy]
    # Cobertura PERDIDA: la mutación existía y NO estaba declarada como hueco
    # —o sea, alguna ficha la cazaba— y hoy no la caza nadie. Eso es lo único
    # que este chequeo puede prometer, y lo único que pone rojo.
    # Solo cuenta como perdida una mutación que YA EXISTÍA y que entonces no
    # era hueco. Una mutación nueva no puede haber perdido nada.
    cazadas_antes = elenco_previo - set(declarados)
    perdidos = [n for n in ids_hoy if n in cazadas_antes]
    nuevos_medidos = [(n, d) for n, d in huecos if n not in declarados]

    if huecos:
        print("Trozos de motor que hoy no protege ninguna ficha —se saldan "
              "escribiendo fichas que los ejerciten o dando consumidor al "
              "vocabulario, no tocando esta lista:")
        for _n, d in huecos:
            print(f"   · {d}")
    if cerrados:
        print(f"\n ✅ {len(cerrados)} hueco(s) que ya protege algo:")
        for n in cerrados:
            print(f"      · {declarados[n]}")
    for n, d in nuevos_medidos:
        print(f" ℹ hueco medido por una mutación NUEVA (no es cobertura "
              f"perdida):\n      {d}")
    for n in perdidos:
        print(f" 🔴 COBERTURA PERDIDA: alguna ficha cazaba «{n}» y ya no")

    base_f.write_text(json.dumps(
        {"_nota": _NOTA, "_fecha": "2026-09-06",
         "_elenco": "todas las mutaciones que esta suite corre hoy. Sin esta "
                    "lista no se distingue una mutación NUEVA de una que se "
                    "cazaba y ha dejado de cazarse.",
         "mutaciones": sorted(nombres),
         "huecos_por_id": {n: d for n, d in huecos}},
        ensure_ascii=False, indent=1), encoding="utf-8")

    total = len(MUTACIONES)
    print(f"   {cazadas} cazadas por alguna ficha · {len(huecos)} declaradas "
          f"como deuda en `motor_sin_carga.json` · línea base: {len(declarados)}")
    if perdidos:
        print(f"❌ {len(perdidos)} trozo(s) de motor que antes protegía alguna "
              f"ficha y ya no")
    else:
        print("✅ ninguna cobertura de motor perdida")
    print(f"{cazadas + len(huecos)}/{total}")
    return 1 if perdidos else 0


if __name__ == "__main__":
    sys.exit(main())
