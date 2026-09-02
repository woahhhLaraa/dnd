#!/usr/bin/env python3
"""Arnés común de las pruebas por mutación (bloque B del Plan 18 — 2026-09-02).

Las once suites anteriores se escribieron una a una y cada una trae su propia
copia de `_copia`, `_falla_por` y el bucle de bloques: unas 40 líneas repetidas
nueve veces, que el §8-E del plan ya tenía anotadas como duplicación real. Las
suites del bloque B son tres más y cubren diecinueve chequeos, así que copiarlo
otras tres veces convertiría una molestia en un problema.

Aquí está una sola vez. Las once viejas **no se tocan**: reescribirlas sería
refactorizar la red justo mientras se la usa para tender el resto, y este plan
dice explícitamente que el refactor va después (bloque F).

── El contrato de una mutación ────────────────────────────────────────────
Una mutación es una función `f(raiz) -> str`: corrompe la copia de la base de
UNA forma concreta y devuelve la frase que describe qué corrompió. Se colocan
en dos listas:

  · DEBEN    — el chequeo tiene que saltar. Si no salta, no cubre ese caso.
  · NO DEBEN — el chequeo NO tiene que saltar. Sin estos controles una suite
               en verde solo demuestra que el chequeo es quisquilloso, y un
               chequeo quisquilloso se acaba desactivando.

Y se comprueba **el chequeo que toca, no otro**: `falla_por` busca la línea de
esa etiqueta concreta en la salida de `validar.py`. Una mutación que rompe la
base entera y hace saltar a otro chequeo no demuestra nada sobre este.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def sust(raiz, rel, viejo, nuevo, cuenta=1):
    """Sustitución literal, y **falla si el texto no está**: una mutación que
    no encaja produciría un «no detectada» falso, y ya pasó una vez (la página
    del efecto del Monje en `mutaciones_efectos.py`)."""
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    if viejo not in t:
        raise AssertionError(f"la mutación no encaja en {rel}: {viejo[:80]!r}")
    p.write_text(t.replace(viejo, nuevo, cuenta), encoding="utf-8")


def copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    return raiz


# Los tres marcadores con los que `validar.py` puede encabezar la línea de un
# chequeo. El ⚠ importa y costó un rato encontrarlo: `validar_referencias`
# encabeza con ⚠ en cuanto tiene un solo aviso, así que buscar solo ✅/❌ hacía
# desaparecer su línea entera y las mutaciones salían «no detectadas» cuando lo
# que fallaba era el arnés.
_MARCAS = ("✅", "❌", "⚠")


def _linea_de(salida, etiqueta):
    for ln in salida.splitlines():
        s = ln.strip()
        for marca in _MARCAS:
            if s.startswith(f"{marca} {etiqueta}"):
                return marca, s
    return None, None


def falla_por(raiz, etiqueta):
    """(¿saltó ESE chequeo?, salida). `None` = no se encontró su línea, que es
    distinto de «no saltó» y hay que verlo."""
    res = subprocess.run([sys.executable, "validar.py"], cwd=raiz,
                         capture_output=True, text=True)
    marca, _s = _linea_de(res.stdout, etiqueta)
    if marca is None:
        return None, res.stdout + res.stderr
    return marca == "❌", res.stdout


def avisos_por(raiz, etiqueta):
    """Los avisos (⚠) que cuelgan de la línea de ese chequeo.

    Existe porque DOS de los treinta chequeos —`validar_costes_sin_fuente` y
    `validar_referencias`— no producen errores nunca: solo avisan. Su línea
    sale siempre en ✅ pase lo que pase, así que `falla_por` no puede probar
    nada sobre ellos, y una suite que lo intentara daría un «no detectada»
    que hablaría de la suite, no del chequeo. Lo que sí se puede exigir es
    que el aviso APAREZCA cuando el dato se rompe: es la garantía que ese
    chequeo da de verdad, y hasta ahora tampoco estaba probada.
    """
    res = subprocess.run([sys.executable, "validar.py"], cwd=raiz,
                         capture_output=True, text=True)
    dentro, avisos = False, []
    for ln in res.stdout.splitlines():
        s = ln.strip()
        if not dentro:
            if any(s.startswith(f"{m} {etiqueta}") for m in _MARCAS):
                dentro = True
            continue
        if s.startswith("⚠"):
            avisos.append(s)
        elif s.startswith(_MARCAS + ("──",)):
            break
    return avisos, res.stdout


def _salta(raiz, etiqueta, modo, base_avisos):
    if modo == "error":
        return falla_por(raiz, etiqueta)
    avisos, salida = avisos_por(raiz, etiqueta)
    nuevos = [a for a in avisos if a not in base_avisos]
    return bool(nuevos), salida


def bloque(titulo, etiqueta, deben, no_deben, modo="error", base_avisos=()):
    print(f"\n══ {titulo} " + "═" * max(0, 70 - len(titulo)))
    ok = 0
    if deben:
        print(" Mutaciones que DEBEN saltar")
    for mut in deben:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = copia(tmp)
            desc = mut(raiz)
            salta, salida = _salta(raiz, etiqueta, modo, base_avisos)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if salta is None:
                print(f"        ↑ el chequeo «{etiqueta}» ni siquiera llegó a "
                      f"imprimirse: la mutación tumbó validar.py antes")
                print("        " + salida.strip().splitlines()[-1][:150])
            elif not salta:
                print("        ↑ NO DETECTADA — el chequeo no cubre este caso")
    if no_deben:
        print(" Controles negativos: NO deben saltar")
    for mut in no_deben:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = copia(tmp)
            desc = mut(raiz)
            salta, _ = _salta(raiz, etiqueta, modo, base_avisos)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — salta con un dato legítimo")
    return ok, len(deben) + len(no_deben)


def principal(doc, bloques):
    """`bloques` = [(titulo, etiqueta, deben, no_deben), ...], y opcionalmente
    un quinto elemento `"aviso"` para los chequeos que solo avisan."""
    print(doc.split("\n\n")[0])
    print("═" * 74)

    bloques = [b if len(b) == 5 else (*b, "error") for b in bloques]
    linea_base = {}
    for _titulo, etiqueta, _d, _n, modo in bloques:
        if modo == "aviso":
            linea_base[etiqueta] = avisos_por(BASE, etiqueta)[0]
        salta, salida = falla_por(BASE, etiqueta)
        if salta is None:
            print(f"✗ CONTROL: no encuentro la línea del chequeo «{etiqueta}» "
                  f"en la salida de validar.py.")
            print(salida[-1500:])
            return 1
        if salta:
            print(f"✗ CONTROL: la base sin tocar ya falla por «{etiqueta}». "
                  f"Arréglalo antes de mutar.")
            return 1
    print(f" ✅ control · la base intacta pasa los {len(bloques)} chequeos que "
          f"esta suite cubre")

    ok = total = 0
    for titulo, etiqueta, deben, no_deben, modo in bloques:
        a, b = bloque(titulo, etiqueta, deben, no_deben, modo,
                      linea_base.get(etiqueta, ()))
        ok += a
        total += b

    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1
