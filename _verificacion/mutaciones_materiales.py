#!/usr/bin/env python3
"""Prueba por mutación de `validar_materiales()` (Fase 14b-2, 2026-08-30).

El defecto que lo motiva es el **modo de fallo nº 10, «dato agregado»**:
`componentes.coste` era un solo string y la base acabó guardando **cuatro sumas
que ninguna página imprime** — *Vínculo protector* «100 po» (un par de anillos
de 50 «cada uno»), *Cofre oculto de Leomund* «5050 po», *Proyección astral*
«1100 po» (1000 + 100) y *Conocer las leyendas* «200 po» (4 × 50). No falta
texto ni sobra, ni hay ninguna cifra «mal»: alguien hizo una operación y guardó
el resultado. **Ningún chequeo de forma ve eso.**

Por eso el chequeo es de **ida y vuelta**: `coste` debe ser IDÉNTICO a lo que
`materiales.render_coste()` produce desde la lista. Si alguien vuelve a escribir
el total a mano, deja de cuadrar.

**Lo que este fichero NO prueba, y conviene saberlo:** el contraste contra el
SRD (`verificar_foundry.py`) tarda más de cuatro minutos por ejecución, así que
mutarlo aquí haría la suite inusable. Ese lado se vigila con la cifra publicada
de valores contrastados — y no es teórico: al escribir la Fase 14b-2 una
variable local llamada `srd` pisó el diccionario del pack, el contraste cayó de
3012 a 1818 valores **sin un solo error**, y lo delató la cifra.

    python3 _verificacion/mutaciones_materiales.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent

# Qué chequeo de `validar.py` cubre esta suite. Lo lee `censo.py` (bloque A
# del Plan 18) para contar qué chequeos tienen red y cuáles no; la promesa no
# es gratis: el censo exige que la suite mencione la ETIQUETA que ese chequeo
# imprime, así que no se puede declarar cobertura que no se ejerce.
CHEQUEOS = ("validar_materiales",)


def _conjuro(raiz, nombre, fn):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    fn(h["componentes"])
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")


# ══ DEBEN saltar ══════════════════════════════════════════════════════════

def m_coste_a_mano(r):
    _conjuro(r, "Clon", lambda c: c.update(coste="3000 po"))
    return "el `coste` de Clon reescrito a mano como 3000 po (1000 + 2000)"


def m_suma_reintroducida(r):
    _conjuro(r, "Cofre oculto de Leomund", lambda c: c.update(coste="5050 po"))
    return "vuelve «5050 po» a Cofre oculto: la suma exacta que el defecto original"


def m_sin_consume(r):
    def f(c):
        del c["materiales"][0]["consume"]
    _conjuro(r, "Clon", f)
    return "un material sin `consume` (en Clon se consume uno y el otro no)"


def m_unidad_inventada(r):
    def f(c):
        c["materiales"][0]["unidad"] = "pl"
        import sys as s; s.path.insert(0, str(BASE))
    _conjuro(r, "Clon", f)
    return "unidad «pl», fuera del vocabulario po/pp/pc"


def m_coste_no_entero(r):
    _conjuro(r, "Clon", lambda c: c["materiales"][0].update(coste="1000"))
    return "coste como string «1000» en vez de entero"


def m_consume_incoherente(r):
    _conjuro(r, "Clon", lambda c: c.update(consume_material=False))
    return "`consume_material` False cuando el diamante sí se consume"


def m_lista_borrada(r):
    def f(c):
        del c["materiales"]
    _conjuro(r, "Proyección astral", f)
    return ("se borra `materiales` dejando un coste compuesto: antes era una "
            "EXENCIÓN declarada, ahora es un error")


# ══ NO deben saltar ═══════════════════════════════════════════════════════

def n_nombre_de_material(r):
    _conjuro(r, "Clon", lambda c: c["materiales"][0].update(nombre="diamante puro"))
    return "renombrar un material: no entra en el coste ni en el round-trip"


def n_nota_ambigua(r):
    _conjuro(r, "Conocer las leyendas",
             lambda c: c["materiales"][1].update(_ambiguo="otra redacción de la nota"))
    return "reescribir la nota de ambigüedad: es prosa declarativa"


def n_coste_simple_con_asterisco(r):
    _conjuro(r, "Revivir", lambda c: c.update(coste="300 po*"))
    return ("un coste simple con asterisco («300 po*», la convención de «se "
            "consume»): la primera versión del chequeo marcó 26 conjuros sanos "
            "por no contemplarlo")


DEBEN = [m_coste_a_mano, m_suma_reintroducida, m_sin_consume, m_unidad_inventada,
         m_coste_no_entero, m_consume_incoherente, m_lista_borrada]
NO_DEBEN = [n_nombre_de_material, n_nota_ambigua, n_coste_simple_con_asterisco]


def _falla_por(raiz, etiqueta="materiales"):
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
        print("✗ CONTROL: no encuentro la línea del chequeo «materiales».")
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
