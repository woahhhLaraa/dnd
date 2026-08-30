#!/usr/bin/env python3
"""Prueba por mutación de `validar_puntos_golpe()` (2026-08-30).

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada.

Qué vigila el chequeo. La tabla "Puntos de golpe establecidos por clase"
(pdf 44 = libro 42) y los `dado_golpe` de las 12 clases se transcribieron **por
separado**, de páginas distintas y en sesiones distintas. Eso las hace
contrastables sin abrir el manual: el valor fijo es siempre `(caras / 2) + 1`.
No demuestra que la tabla esté bien copiada — demuestra que las dos
transcripciones **cuentan la misma historia**, y avisa cuando una se rompe.

Las mutaciones atacan **en las dos direcciones**, a propósito: romper la tabla
y romper el dado de la clase. Un chequeo cruzado que solo se probara por un
lado no habría demostrado que es cruzado.

    python3 _verificacion/mutaciones_pg.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
REGLAS = "reglas/generacion_personaje.yaml"


def _sust(raiz, rel, viejo, nuevo, n=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:60]!r}"
    p.write_text(t.replace(viejo, nuevo, n), encoding="utf-8")


# ══ Mutaciones que DEBEN saltar ═══════════════════════════════════════════

def m_valor_de_tabla(r):
    _sust(r, REGLAS, "- {clases: [Bárbaro], valor: 7}", "- {clases: [Bárbaro], valor: 8}")
    return "Bárbaro con 8 PG por nivel: deja de cuadrar con su d12"


def m_dado_de_clase(r):
    """La otra dirección del contraste: no la tabla, la clase."""
    _sust(r, "clases/mago.yaml", 'dado_golpe: d6', 'dado_golpe: d8')
    return "el Mago pasa a d8: la tabla sigue diciendo 4 y ya no cuadra"


def m_clase_ausente(r):
    _sust(r, REGLAS,
          "- {clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}",
          "- {clases: [Bardo, Brujo, Clérigo, Druida, Monje], valor: 5}")
    return "falta el Pícaro y la tabla declara cubrir las 12 clases"


def m_clase_repetida(r):
    _sust(r, REGLAS, "- {clases: [Hechicero, Mago], valor: 4}",
          "- {clases: [Hechicero, Mago, Bárbaro], valor: 4}")
    return "el Bárbaro en dos filas a la vez, con dos valores distintos"


def m_clase_inventada(r):
    _sust(r, REGLAS, "- {clases: [Bárbaro], valor: 7}",
          "- {clases: [Bárbaro, Nigromante], valor: 7}")
    return "una clase que no existe en la base"


def m_sin_pagina(r):
    _sust(r, REGLAS, "    pagina: {pdf: 44, libro: 42}\n"
                     '    seccion: "Subir de nivel, paso 2', "    seccion: \"Subir de nivel, paso 2")
    return "la regla de niveles siguientes al 1 se queda sin cita de página"


# ══ Controles negativos: NO deben saltar ═════════════════════════════════

def n_orden_de_filas(r):
    _sust(r, REGLAS,
          "        - {clases: [Bárbaro], valor: 7}\n"
          "        - {clases: [Explorador, Guerrero, Paladín], valor: 6}",
          "        - {clases: [Explorador, Guerrero, Paladín], valor: 6}\n"
          "        - {clases: [Bárbaro], valor: 7}")
    return "reordenar las filas: el orden no es un dato"


def n_titulo_distinto(r):
    _sust(r, REGLAS, 'titulo: "Puntos de golpe establecidos por clase"',
          'titulo: "Puntos de golpe establecidos por clase "')
    return "un espacio de más en el título: es prosa, no una clave"


def n_cobertura_parcial_declarada(r):
    """Si la tabla NO dice cubrir las 12, faltar una no es un defecto."""
    _sust(r, REGLAS, "      _todas_las_clases: true", "      _todas_las_clases: false")
    _sust(r, REGLAS,
          "- {clases: [Bardo, Brujo, Clérigo, Druida, Monje, Pícaro], valor: 5}",
          "- {clases: [Bardo, Brujo, Clérigo, Druida, Monje], valor: 5}")
    return ("falta el Pícaro pero la tabla ya NO declara cubrirlas todas: el "
            "chequeo respeta lo declarado en vez de imponer su suposición")


# ══ CARGA · ¿sostiene la historia de PG a la ficha de nivel 3? ═══════════
# La ficha `draconido_hechicero_n3.yaml` existe para esto: nivel 1 por máximo
# del dado, nivel 2 por valor establecido, nivel 3 por tirada, más el efecto de
# subclase *Resistencia dracónica*. Si la historia fuera decorativa, mutarla no
# rompería nada.
N3 = "personajes/draconido_hechicero_n3.yaml"


def c_valor_de_un_nivel(r):
    _sust(r, N3, "metodo: valor_establecido, valor: 4", "metodo: valor_establecido, valor: 5")
    return "el nivel 2 pasa de 4 a 5 PG: el total guardado deja de cuadrar"


def c_nivel_ausente(r):
    p = r / N3
    t = p.read_text(encoding="utf-8")
    i = t.index("  - {nivel: 3, clase: Hechicero")
    j = t.index("\n\n", i)
    p.write_text(t[:i] + t[j+1:], encoding="utf-8")
    return "falta el nivel 3 en la historia: no hay una entrada por nivel"


def c_constitucion_retroactiva(r):
    """La trampa anotada: subir Con debe subir los PG en 1 POR NIVEL (=3)."""
    _sust(r, N3, "final: {fue: 8, des: 14, con: 14, int: 10, sab: 12, car: 17}",
                 "final: {fue: 8, des: 14, con: 16, int: 10, sab: 12, car: 17}")
    _sust(r, N3, "  pg_max: 24", "  pg_max: 25")
    return ("Con 14→16 (+1 al modificador) con los PG subidos solo en 1: deben "
            "subir 3, uno por nivel alcanzado (pdf 44, paso 5)")


def n_historia_intacta(r):
    _sust(r, N3, 'jugador: null', 'jugador: "Larita"')
    return "cambiar un campo de prosa libre: no toca la aritmética"


CARGA_DEBEN = [c_valor_de_un_nivel, c_nivel_ausente, c_constitucion_retroactiva]
CARGA_NO_DEBEN = [n_historia_intacta]


DEBEN = [m_valor_de_tabla, m_dado_de_clase, m_clase_ausente, m_clase_repetida,
         m_clase_inventada, m_sin_pagina]
NO_DEBEN = [n_orden_de_filas, n_titulo_distinto, n_cobertura_parcial_declarada]


def _ficha_n3_falla(raiz):
    """¿Se entera la ficha de nivel 3? Aquí el chequeo no es `validar.py` sino
    `verificar_personaje.py`, que es quien recalcula la historia."""
    r = subprocess.run([sys.executable, "verificar_personaje.py",
                        str(raiz / "personajes/draconido_hechicero_n3.yaml")],
                       cwd=raiz, capture_output=True, text=True)
    return r.returncode != 0


def _falla_por(raiz, etiqueta="puntos de golpe"):
    res = subprocess.run([sys.executable, "validar.py"], cwd=raiz,
                         capture_output=True, text=True)
    for ln in res.stdout.splitlines():
        s = ln.strip()
        if s.startswith(f"✅ {etiqueta}") or s.startswith(f"❌ {etiqueta}"):
            return s.startswith("❌"), res.stdout
    return None, res.stdout + res.stderr


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)
    salta, out = _falla_por(BASE)
    if salta is None:
        print("✗ CONTROL: no encuentro la línea del chequeo «puntos de golpe».")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla. Arréglalo antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo")

    ok = 0
    for etiqueta, muts, esperado, prueba in (
            ("Mutaciones que DEBEN saltar", DEBEN, True, None),
            ("Controles negativos: NO deben saltar", NO_DEBEN, False, None),
            ("CARGA · la historia de PG en una ficha de nivel 3",
             CARGA_DEBEN, True, _ficha_n3_falla),
            ("CARGA · controles negativos", CARGA_NO_DEBEN, False, _ficha_n3_falla)):
        print(f"\n {etiqueta}")
        for mut in muts:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = pathlib.Path(tmp) / "base"
                shutil.copytree(BASE, raiz, symlinks=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                desc = mut(raiz)
                salta = prueba(raiz) if prueba else _falla_por(raiz)[0]
                bien = bool(salta) is esperado
                ok += bien
                print(f"   {'✅' if bien else '❌'} {desc}")
                if not bien:
                    print("        ↑ " + ("NO DETECTADA" if esperado
                                           else "FALSO POSITIVO"))

    total = len(DEBEN) + len(NO_DEBEN) + len(CARGA_DEBEN) + len(CARGA_NO_DEBEN)
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
