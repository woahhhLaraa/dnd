#!/usr/bin/env python3
"""Prueba por mutación de `validar_dados()` (en `validar.py`).

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable, la
corrompe de una forma distinta cada vez, y comprueba que `validar.py`
**salta**.

Aquí se prueban **las dos direcciones**, y no por simetría estética: el
riesgo real de este chequeo concreto es el falso positivo. Su primera
versión encontró tres `d0` en la base y los tres estaban dentro de la
`_nota_verificacion` que documenta el arreglo de `Dedo de la muerte` — es
decir, el chequeo se disparaba con su propia documentación. De ahí que la
mitad de las mutaciones de este fichero sean **controles negativos**: datos
raros pero legítimos que **no** deben hacerlo saltar.

    python3 _verificacion/mutaciones_dados.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def _hechizo(raiz, nombre, campo, fn):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    h[campo] = fn(h.get(campo, ""))
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")


def _linea_yaml(raiz, rel, vieja, nueva):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert t.count(vieja) == 1, f"ancla no única en {rel}: {vieja!r}"
    p.write_text(t.replace(vieja, nueva), encoding="utf-8")


# ── Mutaciones que DEBEN saltar ───────────────────────────────────────────

def m_d0_reintroducido(r):
    """El defecto original, tal cual: el «0» de «30» leído como dado."""
    _hechizo(r, "Dedo de la muerte", "descripcion",
             lambda s: s.replace("7d8 + 30", "7d8 + 3d0"))
    return "d0 reintroducido en Dedo de la muerte (el defecto original)"


def m_d7_en_conjuro(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s.replace("8d6", "8d7"))
    return "d7 en la descripción de un conjuro (Bola de fuego)"


def m_d5_en_resumen(r):
    _hechizo(r, "Bola de fuego", "resumen", lambda s: str(s) + " 2d5 extra")
    return "d5 en el resumen de un conjuro"


def m_d3_en_rasgo_de_clase(r):
    p = r / "clases/rasgos/barbaro.yaml"
    t = p.read_text(encoding="utf-8")
    assert "2d10" in t
    p.write_text(t.replace("2d10", "2d3", 1), encoding="utf-8")
    return "d3 en un rasgo de clase (barbaro.yaml)"


def m_d0_en_dote(r):
    p = r / "dotes/generales.yaml"
    t = p.read_text(encoding="utf-8")
    assert "1d8" in t
    p.write_text(t.replace("1d8", "1d0", 1), encoding="utf-8")
    return "d0 en una dote (generales.yaml)"


def m_d13_en_equipo(r):
    p = r / "equipo/armas.yaml"
    t = p.read_text(encoding="utf-8")
    assert "1d8" in t
    p.write_text(t.replace("1d8", "1d13", 1), encoding="utf-8")
    return "d13 en el dado de daño de un arma (armas.yaml)"


DEBEN_SALTAR = [
    m_d0_reintroducido, m_d7_en_conjuro, m_d5_en_resumen,
    m_d3_en_rasgo_de_clase, m_d0_en_dote, m_d13_en_equipo,
]


# ── Controles negativos: NO deben saltar ──────────────────────────────────

def n_nota_verificacion_cita_el_valor_malo(r):
    """Una nota de procedencia que cita el dado corrupto que se corrigió.

    Es el caso que hizo falsear la primera versión del chequeo.
    """
    _hechizo(r, "Bola de fuego", "_nota_verificacion",
             lambda s: "decía «8d0» por error del CSV; corregido a 8d6.")
    return "_nota_verificacion citando un «8d0» ya corregido"


def n_nota_yaml_cita_el_valor_malo(r):
    _linea_yaml(r, "especies/especies.yaml",
                '    _nota: "El OCR cortó la velocidad',
                '    _nota: "Antes decía 1d0 por el OCR. El OCR cortó la velocidad')
    return "_nota de YAML citando un «1d0» ya corregido"


def n_d100_es_valido(r):
    _hechizo(r, "Bola de fuego", "descripcion", lambda s: s + " Tira 1d100.")
    return "1d100 añadido (dado válido, no debe saltar)"


def n_d4_sin_cantidad(r):
    _hechizo(r, "Bola de fuego", "descripcion", lambda s: s + " Tira d4.")
    return "d4 sin número delante (forma válida)"


def n_palabra_con_d_y_digitos(r):
    """Un identificador tipo «Ad20» no es una tirada."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Ref. interna Ad20x y 3d6.")
    return "texto con «Ad20x» pegado a letras (no es una tirada)"


def n_numero_suelto_grande(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Inflige 30 de daño y 2d6 más.")
    return "«30» suelto junto a un dado válido (el caso que se confundió)"


NO_DEBEN_SALTAR = [
    n_nota_verificacion_cita_el_valor_malo, n_nota_yaml_cita_el_valor_malo,
    n_d100_es_valido, n_d4_sin_cantidad, n_palabra_con_d_y_digitos,
    n_numero_suelto_grande,
]


# ── Arnés ─────────────────────────────────────────────────────────────────
def _falla_por_dados(raiz):
    """¿Salta `validar.py` **por el chequeo de dados**, y no por otra cosa?

    Se mira la línea del chequeo, no el código de salida: una mutación podría
    romper otro validador y dar un falso «detectada».
    """
    res = subprocess.run([sys.executable, "validar.py"],
                         cwd=raiz, capture_output=True, text=True)
    for ln in res.stdout.splitlines():
        if ln.strip().startswith(("✅ dados", "❌ dados")):
            return ln.strip().startswith("❌"), res.stdout
    return None, res.stdout


def main():
    print("Prueba por mutación de validar_dados()")
    print("─" * 74)

    salta, out = _falla_por_dados(BASE)
    if salta is None:
        print("✗ CONTROL: no encuentro la línea del chequeo de dados.")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla. Arréglalo antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo de dados\n")

    ok = 0
    total = len(DEBEN_SALTAR) + len(NO_DEBEN_SALTAR)

    print(" Mutaciones que DEBEN saltar")
    for mut in DEBEN_SALTAR:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            salta, _ = _falla_por_dados(raiz)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("        ↑ NO DETECTADA — el chequeo no cubre este caso")

    print("\n Controles negativos: NO deben saltar")
    for mut in NO_DEBEN_SALTAR:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            salta, _ = _falla_por_dados(raiz)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — el chequeo salta con un dato legítimo")

    print("─" * 74)
    print(f"{ok}/{total} comprobaciones correctas "
          f"({len(DEBEN_SALTAR)} detecciones + {len(NO_DEBEN_SALTAR)} controles negativos)")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
