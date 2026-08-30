#!/usr/bin/env python3
"""Prueba por mutación de `validar_prerrequisitos()` (Fase 15, 2026-08-30).

El prerrequisito de una dote era prosa. Un LLM que la lee acierta casi siempre,
y «casi siempre» es la **amenaza nº 5 del FODA**: un acierto por el método
equivocado es indistinguible de acertar por casualidad.

El chequeo fuerte es de **IDA Y VUELTA**: se parsea la prosa a estructura, se
reconstruye desde la estructura, y tiene que salir **idéntica**. Demuestra lo
único que importa — que no se perdió ni se inventó nada al estructurar. Un
parser que ignore un término en silencio hace exactamente lo que hizo el CSV de
origen: devolver algo plausible y equivocado.

**Un límite de este chequeo, declarado y no disimulado:** nada comprueba que una
dote *deba* tener prerrequisito. Si alguien borra el de una dote que lo tenía,
el resto sigue cuadrando y el chequeo calla. Está aquí como control negativo con
su nombre, para que quede escrito en vez de descubrirse tarde.

    python3 _verificacion/mutaciones_prerrequisitos.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def _sust(raiz, rel, viejo, nuevo, n=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, n), encoding="utf-8")


# ══ DEBEN saltar ══════════════════════════════════════════════════════════

def m_termino_no_entendido(r):
    _sust(r, "dotes/generales.yaml", "nivel 4 o más, Destreza 13 o más",
          "nivel 4 o superior, Destreza 13 o más")
    return "«nivel 4 o superior»: una redacción que el vocabulario no contempla"


def m_rasgo_inexistente(r):
    _sust(r, "dotes/estilo_de_combate.yaml", "rasgo Estilo de combate",
          "rasgo Estilo de combate épico")
    return "cita un rasgo que no existe (el bug `Clerigo` otra vez)"


def m_entrenamiento_inexistente(r):
    _sust(r, "dotes/generales.yaml", "entrenamiento con armaduras medias",
          "entrenamiento con armaduras místicas")
    return "una categoría de entrenamiento que ninguna clase concede"


def m_caracteristica_inventada(r):
    _sust(r, "dotes/generales.yaml", "nivel 4 o más, Carisma 13 o más",
          "nivel 4 o más, Suerte 13 o más")
    return "«Suerte 13 o más»: no es una de las seis características"


def m_separador_cambiado(r):
    """Rompe el ida y vuelta sin romper el parseo: es el caso sutil."""
    _sust(r, "dotes/generales.yaml", "nivel 4 o más, Inteligencia 13 o más",
          "nivel 4 o más; Inteligencia 13 o más")
    return ("«;» donde ningún término lleva comas: parsea bien pero el ida y "
            "vuelta ya no reproduce el original")


def m_alternativa_perdida(r):
    _sust(r, "dotes/generales.yaml",
          "nivel 4 o más; Inteligencia, Sabiduría o Carisma 13 o más",
          "nivel 4 o más; Inteligencia, Sabiduría, Carisma 13 o más")
    return ("«Inteligencia, Sabiduría, Carisma» sin el « o » final: el manual "
            "escribe la alternativa con «o», y sin él el término deja de parsear")


# ══ NO deben saltar ═══════════════════════════════════════════════════════

def n_otro_nivel(r):
    _sust(r, "dotes/generales.yaml", "nivel 4 o más, Destreza 13 o más",
          "nivel 6 o más, Destreza 13 o más")
    return "otro nivel mínimo: sigue siendo gramática válida"


def n_otro_minimo(r):
    _sust(r, "dotes/generales.yaml", "nivel 4 o más, Carisma 13 o más",
          "nivel 4 o más, Carisma 15 o más")
    return "otro mínimo de característica: gramática válida"


def n_descripcion_cambiada(r):
    _sust(r, "dotes/origen.yaml", "Puntos de suerte:", "Puntos de fortuna:")
    return "cambiar la descripción de una dote: no toca el prerrequisito"


def n_prerrequisito_borrado(r):
    """El límite declarado: nada dice que una dote DEBA tener prerrequisito."""
    _sust(r, "dotes/generales.yaml",
          'prerrequisito: "nivel 4 o más, Carisma 13 o más"',
          "prerrequisito: null")
    return ("borrar un prerrequisito entero: el chequeo NO lo ve, y está aquí "
            "para que ese límite quede escrito en vez de descubrirse tarde")


DEBEN = [m_termino_no_entendido, m_rasgo_inexistente, m_entrenamiento_inexistente,
         m_caracteristica_inventada, m_separador_cambiado, m_alternativa_perdida]
NO_DEBEN = [n_otro_nivel, n_otro_minimo, n_descripcion_cambiada,
            n_prerrequisito_borrado]


def _falla_por(raiz, etiqueta="prerrequisitos"):
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
        print("✗ CONTROL: no encuentro la línea del chequeo «prerrequisitos».")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla. Arréglalo antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo")

    ok = 0
    for etiqueta, muts, esperado in (("Mutaciones que DEBEN saltar", DEBEN, True),
                                     ("Controles negativos: NO deben saltar",
                                      NO_DEBEN, False)):
        print(f"\n {etiqueta}")
        for mut in muts:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = pathlib.Path(tmp) / "base"
                shutil.copytree(BASE, raiz, symlinks=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                desc = mut(raiz)
                salta, _ = _falla_por(raiz)
                bien = bool(salta) is esperado
                ok += bien
                print(f"   {'✅' if bien else '❌'} {desc}")
                if not bien:
                    print("        ↑ " + ("NO DETECTADA" if esperado
                                           else "FALSO POSITIVO"))

    total = len(DEBEN) + len(NO_DEBEN)
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
