#!/usr/bin/env python3
"""Prueba por mutación de `validar_subida()` (Fase 16, 2026-08-30).

`subir_nivel.py` deriva de la tabla de cada clase qué pasa al alcanzar un nivel,
y **falla ruidosamente** ante un rasgo que la tabla concede sin texto, una
subclase sin el rasgo del nivel que la tabla promete, o un nivel en el que «no
pasa nada». `validar_subida()` corre esos 333 saltos —12 clases × niveles 2-20,
y los de subclase una vez por subclase— para convertir esos `sys.exit` en
cobertura comprobada en vez de en una sorpresa el día que alguien suba un pícaro
al nivel 10.

Las mutaciones atacan justo esos tres modos de fallo.

    python3 _verificacion/mutaciones_subida.py
"""
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
CHEQUEOS = ("validar_subida",)


def _sust(raiz, rel, viejo, nuevo, n=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, n), encoding="utf-8")


# ══ DEBEN saltar ══════════════════════════════════════════════════════════

def m_rasgo_sin_texto(r):
    # OJO al nivel: `validar_subida()` recorre los saltos 2-20, así que mutar un
    # rasgo de NIVEL 1 no lo ve — y la primera versión de esta mutación tocaba
    # «Ataque furtivo», que el Pícaro tiene en el nivel 1. La mutación estaba
    # mal, no el chequeo. «Acción astuta» es de nivel 2.
    _sust(r, "clases/picaro.yaml", '"Acción astuta"', '"Acción astutísima"')
    return ("la tabla del Pícaro concede «Acción astutísima» (nivel 2) y no hay "
            "texto: la base concedería un rasgo que no sabe explicar")


def m_subclase_sin_su_rasgo(r):
    """La tabla promete «Rasgo de subclase» en un nivel y la subclase no lo tiene."""
    import yaml, json
    p = r / "clases/subclases/picaro.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    s = d["subclases"][0]
    niveles = sorted({x.get("nivel") for x in s["rasgos"] if x.get("nivel")})
    objetivo = niveles[1] if len(niveles) > 1 else niveles[0]
    s["rasgos"] = [x for x in s["rasgos"] if x.get("nivel") != objetivo]
    p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")
    return (f"a «{s['nombre']}» se le quitan los rasgos de nivel {objetivo}, que "
            f"la tabla del Pícaro sí promete")


def m_clase_sin_subclases(r):
    import yaml
    p = r / "clases/subclases/mago.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    d["subclases"] = []
    p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")
    return "el Mago se queda sin subclases y su tabla las pide en el nivel 3"


def m_rasgo_renombrado_en_la_tabla(r):
    _sust(r, "clases/monje.yaml", '"Ataque adicional"', '"Ataque extra"')
    return ("un rasgo renombrado solo en la tabla: deja de casar con su texto "
            "(el defecto que ya produjo el bug `Clerigo`, pero al revés)")


# ══ NO deben saltar ═══════════════════════════════════════════════════════

def n_texto_de_rasgo_cambiado(r):
    _sust(r, "clases/rasgos/picaro.yaml", "desc:", "desc:", 1)
    p = r / "clases/rasgos/picaro.yaml"
    t = p.read_text(encoding="utf-8")
    i = t.index("desc: ")
    j = t.index("\n", i)
    p.write_text(t[:i] + 'desc: "Otro texto para el mismo rasgo."' + t[j:],
                 encoding="utf-8")
    return "reescribir el texto de un rasgo: sigue existiendo y explicándose"


def n_valor_de_columna(r):
    _sust(r, "clases/picaro.yaml", 'ataque_furtivo: "1d6"', 'ataque_furtivo: "2d6"')
    return "cambiar un valor de la columna `ataque_furtivo`: sigue siendo columna"


def n_pb_distinto(r):
    _sust(r, "clases/mago.yaml", "pb: 2", "pb: 3", 1)
    return "otro bonificador por competencia: la subida se sigue derivando igual"


DEBEN = [m_rasgo_sin_texto, m_subclase_sin_su_rasgo, m_clase_sin_subclases,
         m_rasgo_renombrado_en_la_tabla]
NO_DEBEN = [n_texto_de_rasgo_cambiado, n_valor_de_columna, n_pb_distinto]


def _falla_por(raiz, etiqueta="saltos de nivel"):
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
        print("✗ CONTROL: no encuentro la línea del chequeo «saltos de nivel».")
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
