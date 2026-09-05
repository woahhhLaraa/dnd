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

def m_add_invertido(r):
    _sust(r, "efectos.py", "    for ef in por_op.get(\"add\", []):\n        valor += _num(ef, entorno)",
          "    for ef in por_op.get(\"add\", []):\n        valor -= _num(ef, entorno)")
    return "el bucle `add` resta en vez de sumar"


def m_min_borrado(r):
    _sust(r, "efectos.py", "    for ef in por_op.get(\"min\", []):\n        valor = max(valor, _num(ef, entorno))\n", "")
    return "desaparece el bucle `min` de la agregación"


def m_max_borrado(r):
    _sust(r, "efectos.py", "    for ef in por_op.get(\"max\", []):\n        valor = min(valor, _num(ef, entorno))\n", "")
    return "desaparece el bucle `max` de la agregación"


def m_set_borrado(r):
    _sust(r, "efectos.py", "    for ef in por_op.get(\"set\", []):\n        valor = _num(ef, entorno)\n", "")
    return "desaparece el bucle `set` de la agregación"


def m_sin_redondeo(r):
    """El `math.floor` final. DiceCloud redondea hacia abajo salvo en las
    variables decimales; quitarlo deja CA y PG con parte fraccionaria."""
    _sust(r, "efectos.py", "return valor if decimal else math.floor(valor)",
          "return valor")
    return "se quita el `math.floor` final de la agregación"


def m_mul_invertido(r):
    _sust(r, "efectos.py", "        valor *= _num(ef, entorno)",
          "        valor /= _num(ef, entorno)")
    return "el bucle `mul` divide en vez de multiplicar"


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
    """`sin_armadura` es la condición de la que cuelgan las cuatro fórmulas
    de CA base de la base (Bárbaro, Monje, y dos subclases)."""
    _sust(r, "efectos.py", '"con_armadura": con_arm, "sin_armadura": not con_arm',
          '"con_armadura": not con_arm, "sin_armadura": con_arm')
    return "`con_armadura` y `sin_armadura` intercambiadas"


def m_escudo_invertido(r):
    _sust(r, "efectos.py", '"con_escudo": con_esc, "sin_escudo": not con_esc',
          '"con_escudo": not con_esc, "sin_escudo": con_esc')
    return "`con_escudo` y `sin_escudo` intercambiadas"


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


MUTACIONES = [
    m_add_invertido, m_mul_invertido, m_min_borrado, m_max_borrado,
    m_set_borrado, m_sin_redondeo,
    m_minimo_de_pg, m_pg_nivel_1_sin_constitucion,
    m_estado_de_equipo_invertido, m_escudo_invertido, m_condiciones_ignoradas,
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
                huecos.append(desc)
                print(f" ❌ {desc}")
                print("      ↑ NINGUNA ficha la caza: es un hueco de cobertura "
                      "aritmética, no un fallo de esta suite")

    print("─" * 74)

    # La deuda va ENUMERADA y solo puede bajar — el patrón de
    # `chequeos_silenciosos.json` y `rasgos_sin_declarar.json`. Siete huecos
    # medidos el 2026-09-05 no se pueden cerrar hoy: cerrarlos es escribir
    # fichas que ejerciten esos trozos de motor, y eso es el mandato «el
    # calculista» de la ronda 3 de estrés. Lo que NO puede pasar es que
    # aparezca uno nuevo sin que nadie lo note.
    import json
    base_f = pathlib.Path(__file__).parent / "motor_sin_carga.json"
    if base_f.exists():
        declarados = json.loads(base_f.read_text(encoding="utf-8"))["huecos"]
    else:
        declarados = list(huecos)
        base_f.write_text(json.dumps(
            {"_nota": "Trozos del motor que NINGUNA ficha de `personajes/` "
                      "protege: se pueden corromper y todas las fichas siguen "
                      "verificando en verde. Es deuda enumerada, no permiso. "
                      "Solo puede bajar, y se salda escribiendo fichas que "
                      "ejerciten esa aritmética — el mandato «el calculista» "
                      "de la ronda 3 de estrés, no tocando esta lista.",
             "_fecha": "2026-09-05", "huecos": huecos},
            ensure_ascii=False, indent=1), encoding="utf-8")

    nuevos = [h for h in huecos if h not in declarados]
    cerrados = [h for h in declarados if h not in huecos]

    if huecos:
        print("Trozos de motor que hoy no protege ninguna ficha —se saldan "
              "escribiendo fichas que los ejerciten, no tocando esta lista:")
        for h in huecos:
            print(f"   · {h}")
    if cerrados:
        print(f"\n ✅ {len(cerrados)} hueco(s) que ya protege alguna ficha:")
        for h in cerrados:
            print(f"      · {h}")
        base_f.write_text(json.dumps(
            {"_nota": json.loads(base_f.read_text(encoding="utf-8"))["_nota"],
             "_fecha": "2026-09-05", "huecos": huecos},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print("      (línea base actualizada: la deuda solo puede bajar)")
    for h in nuevos:
        print(f" 🔴 HUECO NUEVO, no estaba en la línea base:\n      {h}")

    # La cuenta final dice «cazadas O DECLARADAS», que es el mismo idioma que
    # usa `censo.py` («alcanzadas o declaradas en su manifiesto»). Un hueco
    # NUEVO no está en la línea base, así que no cuenta como declarado y la
    # fracción baja sola — que es lo que `verificar_documentos.py` mira.
    declarados_hoy = sum(1 for h in huecos if h in declarados)
    total = len(MUTACIONES)
    print(f"   {cazadas} cazadas por alguna ficha · {declarados_hoy} declaradas "
          f"como deuda en `motor_sin_carga.json` · línea base: {len(declarados)}")
    if nuevos:
        print(f"❌ {len(nuevos)} trozo(s) de motor que antes protegía alguna "
              f"ficha y ya no")
    else:
        print("✅ ningún hueco de cobertura aritmética nuevo")
    print(f"{cazadas + declarados_hoy}/{total}")
    return 1 if nuevos else 0


if __name__ == "__main__":
    sys.exit(main())
