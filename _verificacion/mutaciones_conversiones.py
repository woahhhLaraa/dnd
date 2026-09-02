#!/usr/bin/env python3
"""Prueba por mutación de `validar_conversiones()` (en `validar.py`).

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable, la
corrompe de una forma distinta cada vez, y comprueba que `validar.py`
**salta**.

── El chequeo cambió de sentido el 2026-09-02, y esta suite con él ────────
Antes comprobaba que las 543 equivalencias «6 m / 20 pies» del texto
estuvieran **bien calculadas**. Lo estaban. El problema era otro: **el manual
castellano no imprime ni una sola unidad imperial** —nueve lectores sobre 23
páginas—, así que las había añadido la base. Se borraron (fase 2 del PLAN_19)
y el chequeo pasa a impedir que vuelvan.

Eso parte la suite en dos mitades, y la segunda hereda todo lo que la primera
había aprendido:

  · TEXTO — cualquier conversión en `descripcion` o `alcance.texto` es error,
    esté bien o mal calculada. Aquí las viejas mutaciones siguen sirviendo,
    pero por otra razón: ya no saltan por ser falsas, saltan por existir. Y
    los que eran controles NEGATIVOS —conversiones correctas— pasan a ser
    detecciones: una conversión correcta también sobra.

  · DERIVADOS — `alcance.metros`/`pies`/`casillas` NO se borraron: no son
    texto que finja ser del manual, son dato, y `verificar_foundry.py`
    contrasta `alcance.pies` contra el SRD número contra número. Su aritmética
    sigue comprobándose, así que **aquí se muda todo lo que esta suite sabía**
    y que si no se habría perdido al vaciar el texto:

      – la base mezcla **tres notaciones decimales** en datos correctos:
        «1,5» (castellana), «0.9» (inglesa) y «1’5» (apóstrofe tipográfico), y
        además el punto de millar («5.000»). Un parser que asuma una sola
        convierte datos buenos en errores: así salieron cinco falsos positivos
        en la primera versión;
      – el factor es el **de juego** (5 pies = 1,5 m), no el físico (3,28084).
        Medido sobre las 548 conversiones de entonces: el de juego dejaba 539
        exactas y el físico solo 313. Elegir mal el factor no da un chequeo
        estricto, da cientos de falsos positivos;
      – la tolerancia es **absoluta** porque el redondeo legítimo que más se
        desvía («0,9 mi» por 0,93) lo hace un 3,4 % relativo, más que «30 m /
        98 pies», que es un defecto.

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


# ── Helper para mutar los campos DERIVADOS de `alcance` ───────────────────
def _alcance(raiz, nombre, campo, valor):
    import json
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    h.setdefault("alcance", {})[campo] = valor
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")


# ══ TEXTO · ninguna conversión vuelve a entrar ════════════════════════════
# Todas saltan por EXISTIR, no por ser falsas. Por eso están aquí también las
# que antes eran controles negativos: una conversión correcta sobra igual.

def m_nube_de_dagas_reintroducida(r):
    """El defecto original, tal cual: 1,5 m convertidos a 10 pies."""
    _hechizo(r, "Nube de dagas", "descripcion",
             lambda s: s.replace("cubo de 1,5 m centrado",
                                 "cubo de 1,5 m / 10 pies centrado"))
    return "«1,5 m / 10 pies» reintroducido en Nube de dagas (el defecto original)"


def m_conversion_correcta_tambien_sobra(r):
    """La que antes era un control negativo. **Este es el cambio de sentido.**"""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Un radio de 1,5 m / 5 pies.")
    return ("una conversión CORRECTA («1,5 m / 5 pies»): antes era un control "
            "negativo y ahora es una detección — el manual no la imprime")


def m_conversion_en_alcance_texto(r):
    _hechizo(r, "Bola de fuego", "descripcion", lambda s: s)   # no-op
    _alcance(r, "Bola de fuego", "texto", "45 m / 150 f / 30 cas")
    return ("la forma vieja de `alcance.texto` («45 m / 150 f / 30 cas») "
            "reintroducida: es el campo del que se borraron 222")


def m_pies_con_factor_fisico(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " El fuego se extiende 30 m / 98 pies.")
    return "conversión con el factor físico (30 m → 98 pies en vez de 100)"


def m_millas_en_prosa(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Se percibe a 1,5 km / 0,9 mi.")
    return "conversión a millas en la prosa, con su redondeo legítimo y todo"


# ══ DERIVADOS · la aritmética que NO se borró ═════════════════════════════

def d_pies_con_factor_fisico(r):
    """El error más probable de quien recalcule a mano: 3,28084 en vez de 5/1,5."""
    _alcance(r, "Bola de fuego", "pies", "98")
    return "`alcance.pies` con el factor físico (36 m → 98 en vez de 120)"


def d_orden_de_magnitud(r):
    _alcance(r, "Bola de fuego", "pies", "1200")
    return "`alcance.pies` con un orden de magnitud de más"


def d_casillas_mal(r):
    _alcance(r, "Bola de fuego", "casillas", "48")
    return "`alcance.casillas` mal contadas (36 m son 24 casillas, no 48)"


def d_metros_movidos(r):
    """Si `metros` cambia y los derivados no, dejan de cuadrar: es el modo de
    fallo del dato derivado — se corrige la fuente y las copias se quedan."""
    _alcance(r, "Bola de fuego", "metros", "18")
    return ("se corrige `alcance.metros` a 18 y nadie recalcula `pies`: el dato "
            "derivado se queda con el valor viejo")


DEBEN_SALTAR = [
    m_nube_de_dagas_reintroducida, m_conversion_correcta_tambien_sobra,
    m_conversion_en_alcance_texto, m_pies_con_factor_fisico, m_millas_en_prosa,
    d_pies_con_factor_fisico, d_orden_de_magnitud, d_casillas_mal,
    d_metros_movidos,
]


# ── Controles negativos: NO deben saltar ──────────────────────────────────
# Las tres notaciones decimales y el punto de millar se mudan del texto a los
# campos derivados, que es donde ahora vive la aritmética. Sin esto, vaciar el
# texto habría tirado a la basura lo que costó cinco falsos positivos aprender.

def n_notacion_castellana(r):
    _alcance(r, "Clarividencia", "metros", "1500")
    _alcance(r, "Clarividencia", "pies", "5000")
    _alcance(r, "Clarividencia", "casillas", "1000")
    return "derivados correctos con notación simple (1500 m → 5000 pies)"


def n_notacion_inglesa(r):
    """Punto decimal: la base lo usa en «0.9 mi» de Tormenta de la venganza.

    Ojo con el valor: *Bola de fuego* son 45 m / 150 pies, así que el control
    tiene que escribir 45 en notación inglesa, no otro número. La primera
    versión ponía «36.0» y daba un falso positivo que hablaba de la mutación,
    no del chequeo.
    """
    _alcance(r, "Bola de fuego", "metros", "45.0")
    return "notación inglesa «45.0» en `metros` (leerla como 450 era el falso positivo)"


def n_apostrofe_tipografico(r):
    """«1’5»: la base lo usa en el alcance de Clarividencia."""
    _alcance(r, "Bola de fuego", "metros", "1’5")
    _alcance(r, "Bola de fuego", "pies", "5")
    _alcance(r, "Bola de fuego", "casillas", "1")
    return "apóstrofe decimal «1’5» (leerlo como 15 era el falso positivo)"


def n_punto_de_millar(r):
    """«5.000»: la base lo usa en Alarma. Era el otro falso positivo."""
    _alcance(r, "Bola de fuego", "metros", "1500")
    _alcance(r, "Bola de fuego", "pies", "5.000")
    _alcance(r, "Bola de fuego", "casillas", "1000")
    return "punto de millar «5.000» en `pies` (leerlo como 5,0 era el falso positivo)"


def n_redondeo_de_valor_no_multiplo(r):
    """El redondeo que la tolerancia SÍ debe admitir, y por qué hace falta.

    Medido el 2026-09-02: **los 436 pares derivados de la base son exactos**,
    desviación 0,0000. Con metros múltiplos de 1,5 el factor de juego no deja
    resto nunca, así que hoy la tolerancia no protege ningún dato real.

    Pero la admite el día que entre un valor que no sea múltiplo —el volumen de
    *Cofre oculto de Leomund* son 0,34 m—, y entonces el redondeo es legítimo:
    0,34 × 10/3 = 1,13 pies, que se escribe «1». La primera versión de este
    control usaba «119 pies por 120», una desviación de un entero: eso NO es
    redondeo, es exactamente el defecto que la tolerancia absoluta separa —«el
    menor defecto real desvía 1 entero»—. El control estaba mal, no el chequeo.
    """
    _alcance(r, "Bola de fuego", "metros", "0,34")
    _alcance(r, "Bola de fuego", "pies", "1")
    _alcance(r, "Bola de fuego", "casillas", "0")
    return ("redondeo legítimo de un valor no múltiplo de 1,5 (0,34 m → «1» "
            "pie, exacto 1,13)")


def n_nota_verificacion_cita_el_valor_malo(r):
    """Una nota de procedencia que cita la conversión que se borró.

    Es el modo de fallo que ya arruinó la primera versión de `validar_dados()`:
    un chequeo probado solo en la dirección de detectar acaba prohibiendo
    documentar lo que corrigió. Y ahora importa el doble: el borrado del
    2026-09-02 dejó notas que citan a propósito el texto viejo.
    """
    _hechizo(r, "Nube de dagas", "_nota_verificacion",
             lambda s: "decía «cubo de 1,5 m / 10 pies»; la página no trae "
                       "conversión y se borró el 2026-09-02.")
    return "_nota_verificacion citando la conversión «1,5 m / 10 pies» ya borrada"


def n_alcance_sin_cifra(r):
    """«Toque» y «Lanzador» no tienen derivados que comprobar."""
    _alcance(r, "Bola de fuego", "texto", "Toque")
    return "un alcance sin cifra: no hay derivado que contrastar, y no pasa nada"


NO_DEBEN_SALTAR = [
    n_notacion_castellana, n_notacion_inglesa, n_apostrofe_tipografico,
    n_punto_de_millar, n_redondeo_de_valor_no_multiplo,
    n_nota_verificacion_cita_el_valor_malo,
    n_alcance_sin_cifra,
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
