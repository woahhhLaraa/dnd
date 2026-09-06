#!/usr/bin/env python3
"""Prueba por mutación de `verificar_chequeos.py` (auditoría del 2026-09-05).

`verificar_chequeos.py` es el guardián de las ramas que abandonan un registro
sin decir nada. **No lo guardaba nadie**, y tenía dentro el defecto que
persigue: su huella era `fichero::funcion::cuerpo`, y el cuerpo de casi todas
las ramas es la palabra `continue`. Medido antes de arreglarlo:

    67 ramas silenciosas → 41 huellas distintas

Es decir: una rama silenciosa NUEVA que fuera gemela textual de otra ya
declarada entraba sin que nadie lo dijera. Y tres lo hicieron — la deuda subió
de 64 a 67 mientras el chequeo imprimía «✅ ninguna rama silenciosa nueva».
Es el mismo modo de fallo que la fase 0 de `PLAN_20_AUDITORIA.md` cerró en
`censo.py`: un guardián cuya deuda enumerada puede crecer en silencio.

El arreglo mete la CONDICIÓN en la huella (67 → 65 huellas distintas), y las
gemelas que quedan —la misma guarda escrita dos veces en la misma función—
llevan un ordinal. Esta suite es la prueba de que el arreglo muerde: la
primera mutación es exactamente el caso que antes pasaba callado.

    python3 _verificacion/mutaciones_silencios.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent

# La rama de la que se hacen las gemelas. Existe hoy en `validar_efectos` y
# está en la línea base declarada: duplicarla no añade ninguna condición nueva
# al fichero, solo una APARICIÓN más de una que ya estaba.
GEMELA = '''    for ef in declarados:
        if not ef.get("columna"):
            continue
'''


def _sust(raiz, rel, viejo, nuevo, cuenta=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, cuenta), encoding="utf-8")


# ══ DEBEN salir ══════════════════════════════════════════════════════════

def u_gemela_de_una_declarada(r):
    """LA mutación de esta suite. Con la huella vieja esta rama era
    indistinguible de la que ya estaba declarada y NO salía."""
    _sust(r, "validar.py", GEMELA, GEMELA + GEMELA)
    return ("una rama silenciosa nueva IDÉNTICA a otra ya declarada "
            "(misma función, misma condición, mismo cuerpo)")


def u_condicion_nueva(r):
    _sust(r, "validar.py", GEMELA,
          '    for ef in declarados:\n'
          '        if not ef.get("columna_inventada"):\n'
          '            continue\n' + GEMELA)
    return "una rama silenciosa nueva con una condición que no existía"


def u_rama_escondida_en_un_ayudante(r):
    """El agujero que abrió el muro de la fase 2, y que lo cazó a los cinco
    minutos: hasta el 2026-09-06 solo se miraban las ramas de `validar_*`,
    `verificar_*` y `main`, así que **mover una rama silenciosa a un ayudante
    con otro nombre la hacía desaparecer de la línea base, en verde**, con la
    poda dándola por saldada. Pasó de verdad, cuatro veces, sacando el cuerpo
    de un bucle a `_ramas_de()`.

    La mutación es esa: la rama nueva no va en un `validar_*`, va en un
    ayudante de guion bajo que el chequeo llama. Si el verificador vuelve a
    mirar solo por prefijo, no la ve y esto sale en verde.
    """
    _sust(r, "validar.py",
          "def validar_dados():\n",
          "def _ayudante_de_dados(declarados):\n" + GEMELA + "\n\n"
          "def validar_dados():\n")
    return ("una rama silenciosa nueva metida en un AYUDANTE `_con_guion_bajo`, "
            "no en un `validar_*`: moverla de función no puede esconderla")


def u_gemela_en_otra_funcion(r):
    """La huella lleva la función: la misma guarda en otra función es otra
    rama, no la misma. Si no lo fuera, mover código de sitio la escondería."""
    _sust(r, "validar.py",
          "def validar_dados():\n",
          "def validar_dados():\n"
          "    declarados = []\n" + GEMELA)
    return ("la misma guarda, palabra por palabra, pero en otra función "
            "(`validar_dados`)")


# ══ NO DEBEN salir: controles negativos ══════════════════════════════════

def n_rama_que_avisa(r):
    """Una rama nueva que DICE algo no es silenciosa. Si saltara, el chequeo
    obligaría a declarar ruido y el manifiesto dejaría de leerlo nadie."""
    _sust(r, "validar.py", GEMELA,
          '    for ef in declarados:\n'
          '        if not ef.get("columna_inventada"):\n'
          '            err.append(f"{ef}: sin columna")\n'
          '            continue\n' + GEMELA)
    return "una rama nueva que avisa antes de abandonar el registro"


def n_rama_declarada(r):
    _sust(r, "validar.py", GEMELA,
          '    for ef in declarados:\n'
          '        if not ef.get("columna_inventada"):\n'
          '            continue  # TOLERADO: no existe tal columna\n' + GEMELA)
    return "una rama nueva silenciosa pero declarada con `# TOLERADO:`"


def n_rama_movida_de_linea(r):
    """La huella NO lleva el número de línea, a propósito: editar por encima
    de una rama no puede invalidar el fichero de la línea base."""
    _sust(r, "validar.py", "def validar_efectos():\n",
          "def validar_efectos():\n    # " + "empuje\n    # " * 12 + "final\n")
    return "doce líneas de comentario que desplazan todas las ramas del fichero"


DEBEN = [u_gemela_de_una_declarada, u_condicion_nueva,
         u_gemela_en_otra_funcion, u_rama_escondida_en_un_ayudante]
NO_DEBEN = [n_rama_que_avisa, n_rama_declarada, n_rama_movida_de_linea]


# ══ Arnés ════════════════════════════════════════════════════════════════
def _falla(raiz):
    r = subprocess.run([sys.executable, "verificar_chequeos.py"],
                       cwd=raiz, capture_output=True, text=True)
    return r.returncode != 0, r.stdout + r.stderr


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return raiz


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)

    falla, salida = _falla(BASE)
    if falla:
        print("✗ CONTROL: `verificar_chequeos.py` ya falla con la base "
              "intacta. Arréglalo antes de mutar.")
        print(salida[-1500:])
        return 1
    print(" ✅ control · la base intacta pasa `verificar_chequeos.py`")

    ok = 0
    print("\n Mutaciones que DEBEN salir")
    for mut in DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            desc = mut(raiz := _copia(tmp))
            salta, _ = _falla(raiz)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("        ↑ NO DETECTADA — una rama silenciosa nueva "
                      "entra sin que nadie lo diga")

    print("\n Controles negativos: NO deben salir")
    for mut in NO_DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            desc = mut(raiz := _copia(tmp))
            salta, _ = _falla(raiz)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — obliga a declarar ruido")

    total = len(DEBEN) + len(NO_DEBEN)
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
