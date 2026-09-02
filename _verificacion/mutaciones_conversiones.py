#!/usr/bin/env python3
"""Prueba por mutación de `validar_conversiones()` (en `validar.py`).

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable, la
corrompe de una forma distinta cada vez, y comprueba que `validar.py`
**salta**.

Aquí los controles negativos pesan tanto como las detecciones, y por una
razón medida: la primera versión de este chequeo dio **cinco falsos
positivos**, todos por el parser de números y no por la aritmética. La base
mezcla **tres notaciones decimales distintas** en conversiones correctas
—«1,5» (castellana), «0.9» (inglesa) y «1’5» (apóstrofe tipográfico)— y
además usa el punto como separador de millar («5.000 pies»). Un parser que
asuma una sola notación convierte datos buenos en errores.

La aritmética tiene su propia trampa, ya documentada en `ESTADO_13p.md`: el
factor correcto es el **de juego** (5 pies = 1,5 m), no el físico (3,28084).
Medido sobre las 548 conversiones a pies de la base, el de juego deja 539
exactas y el físico solo 313. Elegir mal el factor no da un chequeo estricto:
da cientos de falsos positivos.

    python3 _verificacion/mutaciones_conversiones.py
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
CHEQUEOS = ("validar_conversiones",)


def _hechizo(raiz, nombre, campo, fn):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    h[campo] = fn(h.get(campo, ""))
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")


# ── Mutaciones que DEBEN saltar ───────────────────────────────────────────

def m_nube_de_dagas_reintroducida(r):
    """El defecto original, tal cual: 1,5 m convertidos a 10 pies."""
    _hechizo(r, "Nube de dagas", "descripcion",
             lambda s: s.replace("cubo de 1,5 m centrado",
                                 "cubo de 1,5 m / 10 pies centrado"))
    return "«1,5 m / 10 pies» reintroducido en Nube de dagas (el defecto original)"


def m_pies_con_factor_fisico(r):
    """El error de convención: convertir con 3,28084 en vez de 5/1,5.

    Es el fallo más probable de quien añada una conversión a mano, porque
    3,28084 es el factor «correcto» fuera del juego.
    """
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " El fuego se extiende 30 m / 98 pies.")
    return "conversión con el factor físico (30 m → 98 pies en vez de 100)"


def m_orden_de_magnitud(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Alcanza 6 m / 200 pies.")
    return "conversión con un orden de magnitud de más (6 m → 200 pies)"


def m_unidad_equivocada(r):
    """*Crecimiento vegetal* decía «0,46 yardas» donde eran millas."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Cubre 1 km / 0,6 yardas.")
    return "unidad equivocada (1 km → «0,6 yardas», que son millas)"


def m_casillas_mal(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un radio de 9 m / 12 cas.")
    return "casillas mal contadas (9 m son 6 casillas, no 12)"


def m_centimetros_mal(r):
    """El caso de Disco flotante de Tenser: 90 cm declarados como 1 pie."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un grosor de 90 cm / 1 pie.")
    return "centímetros mal convertidos (90 cm son 3 pies, no 1)"


DEBEN_SALTAR = [
    m_nube_de_dagas_reintroducida, m_pies_con_factor_fisico,
    m_orden_de_magnitud, m_unidad_equivocada, m_casillas_mal,
    m_centimetros_mal,
]


# ── Controles negativos: NO deben saltar ──────────────────────────────────

def n_notacion_castellana(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un radio de 1,5 m / 5 pies.")
    return "notación castellana «1,5 m / 5 pies» (correcta)"


def n_notacion_inglesa(r):
    """«0.9» con punto decimal: la base lo usa en Tormenta de la venganza."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un alcance de 1,5 km / 0.9 mi.")
    return "notación inglesa «0.9 mi» (correcta; leerla como 9 era el falso positivo)"


def n_apostrofe_tipografico(r):
    """«1’5 km»: la base lo usa en el alcance de Clarividencia."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un alcance de 1’5 km / 0,9 mi.")
    return "apóstrofe decimal «1’5 km» (correcto; leerlo como 5 km era el falso positivo)"


def n_punto_de_millar(r):
    """«5.000 pies»: la base lo usa en Alarma. Era el otro falso positivo."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Se oye a 1,5 km / 5.000 pies.")
    return "punto de millar «5.000 pies» (correcto; leerlo como 5,0 era el falso positivo)"


def n_redondeo_a_la_baja(r):
    """«1,5 km / 0,9 mi»: el valor exacto es 0,93 y la base escribe 0,9.

    Es el redondeo legítimo que más se desvía de toda la base (3,4 % relativo,
    0,032 absoluto) y aparece en cuatro conjuros reales — Clarividencia,
    Tsunami, Tormenta de la venganza y Tormenta de meteoritos. Es la razón de
    que la tolerancia sea **absoluta**: en relativo, este dato bueno se desvía
    más que «30 m / 98 pies», que es un defecto.
    """
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Se percibe a 1,5 km / 0,9 mi.")
    return "redondeo legítimo «0,9 mi» por 0,93 (la desviación mayor de la base)"


def n_pulgada_redondeada(r):
    """«2,5 cm / 1 pulgada»: el valor exacto es 0,98. Lo usan cuatro conjuros."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " No atraviesa 2,5 cm / 1 pulgada de metal.")
    return "redondeo legítimo «1 pulgada» por 0,98"


def n_nota_verificacion_cita_el_valor_malo(r):
    """Una nota de procedencia que cita la conversión corrupta que se corrigió.

    Es el modo de fallo que ya arruinó la primera versión de `validar_dados()`:
    un chequeo probado solo en la dirección de detectar acaba prohibiendo
    documentar lo que corrigió.
    """
    _hechizo(r, "Nube de dagas", "_nota_verificacion",
             lambda s: "decía «cubo de 1,5 m / 10 pies»; la página no trae "
                       "conversión y 1,5 m son 5 pies. Corregido.")
    return "_nota_verificacion citando la conversión «1,5 m / 10 pies» ya corregida"


NO_DEBEN_SALTAR = [
    n_notacion_castellana, n_notacion_inglesa, n_apostrofe_tipografico,
    n_punto_de_millar, n_redondeo_a_la_baja, n_pulgada_redondeada,
    n_nota_verificacion_cita_el_valor_malo,
]


# ── Arnés ─────────────────────────────────────────────────────────────────
def _falla_por_conversiones(raiz):
    """¿Salta `validar.py` **por el chequeo de conversiones**, y no por otra cosa?

    Se mira la línea del chequeo, no el código de salida: una mutación podría
    romper otro validador y dar un falso «detectada».
    """
    res = subprocess.run([sys.executable, "validar.py"],
                         cwd=raiz, capture_output=True, text=True)
    for ln in res.stdout.splitlines():
        if ln.strip().startswith(("✅ conversiones", "❌ conversiones")):
            return ln.strip().startswith("❌"), res.stdout
    return None, res.stdout


def main():
    print("Prueba por mutación de validar_conversiones()")
    print("─" * 74)

    salta, out = _falla_por_conversiones(BASE)
    if salta is None:
        print("✗ CONTROL: no encuentro la línea del chequeo de conversiones.")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla el chequeo de conversiones.")
        print("  Hay defectos reales pendientes de corregir; arréglalos antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo de conversiones\n")

    ok = 0
    total = len(DEBEN_SALTAR) + len(NO_DEBEN_SALTAR)

    print(" Mutaciones que DEBEN saltar")
    for mut in DEBEN_SALTAR:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            salta, _ = _falla_por_conversiones(raiz)
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
            salta, _ = _falla_por_conversiones(raiz)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — el chequeo salta con un dato legítimo")

    print("─" * 74)
    print(f"{ok}/{total} correctas"
          f"  ({len(DEBEN_SALTAR)} detecciones + {len(NO_DEBEN_SALTAR)} controles negativos)")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
