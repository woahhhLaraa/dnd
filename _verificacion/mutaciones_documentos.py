#!/usr/bin/env python3
"""Prueba por mutación de `verificar_documentos.py` (auditoría del 2026-09-03).

`verificar_documentos.py` es el módulo que vigila que CONTINUAR.md y FODA.md no
mientan. Llevaba desde la Fase 14 sin una sola prueba por mutación: era el
único chequeo del proyecto que nadie había visto fallar nunca. Y falló.

El 2026-09-03 la reescritura de CONTINUAR.md se llevó por delante cuatro
anclas —las dos cifras de contraste externo, la línea de INTEGRIDAD con sus
ocho números y el recuento de mejoras de dote—. Once cifras dejaron de
contrastarse contra la realidad, y el script siguió imprimiendo «los documentos
de estado cuadran con la base», porque una promesa que DESAPARECE solo
generaba un `⚠` que no contaba como error. El agujero no estaba en lo que el
módulo comprobaba: estaba en lo que dejaba de comprobar sin decirlo.

Así que aquí se le rompen los documentos de dos maneras que son distintas a
propósito:

  · BORRANDO una promesa   — el modo de fallo que se le escapó de verdad
  · FALSEANDO una cifra    — el modo de fallo que sí cazaba

y se exige que las dos salgan en rojo. Más dos controles negativos, porque un
chequeo de documentos que salte al reescribir una frase obliga a no tocar la
prosa, y unos documentos que no se pueden reescribir dejan de leerse — que es
justo como CONTINUAR.md llegó a tener 1172 líneas.

    python3 _verificacion/mutaciones_documentos.py
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


def _borra_linea(raiz, rel, aguja):
    p = raiz / rel
    lineas = p.read_text(encoding="utf-8").splitlines(keepends=True)
    quedan = [l for l in lineas if aguja not in l]
    assert len(quedan) < len(lineas), f"no encuentro «{aguja}» en {rel}"
    p.write_text("".join(quedan), encoding="utf-8")


# ══ BORRAR una promesa: el fallo que se le escapó ════════════════════════

def d_ancla_srd_borrada(r):
    _borra_linea(r, "CONTINUAR.md", "`verificar_srd.py` -> ")
    return ("CONTINUAR.md deja de prometer la cifra del SRD: 646 valores que "
            "nadie contrasta ya contra la salida real")


def d_ancla_foundry_borrada(r):
    _borra_linea(r, "CONTINUAR.md", "`verificar_foundry.py` -> ")
    return ("CONTINUAR.md deja de prometer la cifra de Foundry: 3749 valores "
            "sin contrastar")


def d_linea_integridad_borrada(r):
    _borra_linea(r, "CONTINUAR.md", "- INTEGRIDAD: ")
    return ("desaparece la línea de INTEGRIDAD: OCHO cifras dejan de "
            "compararse de golpe, que es exactamente lo que pasó el 2026-09-03")


def d_mejoras_borrada(r):
    _borra_linea(r, "CONTINUAR.md", "mejoras de dote estructuradas")
    return ("CONTINUAR.md deja de decir cuántas mejoras de dote hay")


def d_cuenta_de_suites_borrada(r):
    """Ancla nueva de la fase 1 del PLAN_21. La frase decía «las 17 suites»
    con 18 en el disco, y lo decía justo donde presume de que se descubren
    por patrón: la única cuenta de esa frase que había que recordar a mano."""
    _borra_linea(r, "CONTINUAR.md", "suites de `_verificacion/mutaciones_*.py`")
    return ("CONTINUAR.md deja de decir cuántas suites de mutación hay: la "
            "cuenta vuelve a poder quedarse atrás en silencio")


# ══ FALSEAR una cifra: el fallo que sí cazaba ════════════════════════════

def f_cifra_srd(r):
    _sust(r, "CONTINUAR.md", "-> 646 valores", "-> 645 valores")
    return "CONTINUAR.md dice 645 valores del SRD y la realidad da 646"


def f_cifra_integridad(r):
    """La cifra se DERIVA del documento, no se escribe aquí.

    Iba cableada como «INTEGRIDAD: 683 dados» y se rompió el 2026-09-06, cuando
    el barrido de dados pasó a 684 —el `d6` de la cabecera de una ficha nueva
    entra en la cuenta, porque recorre todos los `.yaml`—. Una mutación que
    copia un número del documento que vigila se desincroniza exactamente igual
    que el documento: la misma lección, un nivel más arriba.
    """
    import re as _re
    p = r / "CONTINUAR.md"
    t = p.read_text(encoding="utf-8")
    m = _re.search(r"INTEGRIDAD: (\d+) dados", t)
    assert m, "CONTINUAR.md ya no enumera los dados en su línea de INTEGRIDAD"
    n = int(m.group(1))
    p.write_text(t.replace(m.group(0), f"INTEGRIDAD: {n + 1} dados", 1),
                 encoding="utf-8")
    return (f"CONTINUAR.md dice {n + 1} dados dentro de la línea de INTEGRIDAD, "
            f"y la realidad da {n}")


def f_cifra_mejoras(r):
    # Pasó de 54 a 55 el 2026-09-03: «Mejora de característica» era la única
    # de las 43 dotes sin `mejora_caracteristica` estructurado, y al añadírselo
    # el chequeo cuenta una más. La mutación sigue el dato, no lo fija.
    _sust(r, "CONTINUAR.md", "- 55 mejoras de dote", "- 56 mejoras de dote")
    return "CONTINUAR.md dice 56 mejoras de dote y las dotes traen 55"


def d_arquitectura_borrada(r):
    """Sin la página, el repo deja de decir cómo está construido."""
    (r / "ARQUITECTURA.md").unlink()
    return ("desaparece ARQUITECTURA.md: el repo deja de describir su propia "
            "arquitectura y nadie lo nota")


def d_modulo_nuevo_sin_documentar(r):
    """La dirección que de verdad importa: **la página se queda corta**. Es la
    forma exacta del error que este repositorio persigue —una lista escrita a
    mano que no crece con lo que describe— y aquí se le exige que falle."""
    (r / "verificar_inventado.py").write_text(
        "#!/usr/bin/env python3\n\"\"\"Un módulo nuevo que nadie documenta.\"\"\"\n",
        encoding="utf-8")
    return ("un módulo nuevo en la raíz que ARQUITECTURA.md no nombra: la "
            "página se ha quedado corta")


def d_modulo_muerto_documentado(r):
    """La otra dirección: la página describe algo que ya no existe. Sin este
    chequeo, borrar un módulo dejaría su descripción viva — que es como el
    manifiesto del censo llegó a tener ocho declaraciones muertas."""
    _sust(r, "ARQUITECTURA.md",
          "| `materiales.py` | descompone costes de material |",
          "| `materiales.py` | descompone costes de material |\n"
          "| `verificar_borrado.py` | un módulo que ya no existe |")
    return ("ARQUITECTURA.md describe un módulo que no está en el disco: la "
            "página se ha quedado vieja")


def d_fila_nueva_sin_documentar(r):
    """Lo mismo con las filas del censo, que son la otra lista de la página."""
    _sust(r, "censo.py",
          "def fila_guardianes():\n",
          "def fila_inventada():\n"
          "    return Fila('inventada', 'inventada', {}, set(), 'nada')\n\n\n"
          "def fila_guardianes():\n")
    # El anclaje se pone en el CIERRE del paréntesis de `FILAS`, no en el
    # nombre de la última fila: anclar en `fila_guardianes)` dejó de encajar en
    # cuanto nació la fila 11 y esta suite reventó entera. Es la misma familia
    # de defecto que la propia página vigila —algo escrito en un sitio que se
    # queda viejo cuando cambia otro—, dentro de su prueba.
    _sust(r, "censo.py", "fila_lectura_independiente)",
          "fila_lectura_independiente, fila_inventada)")
    return ("una fila nueva del censo que ARQUITECTURA.md no nombra")


def f_cuenta_de_suites(r):
    """Falsear la cuenta es el otro modo: el que ya pasó, con 17 escrito y 18
    en el disco. Se pone una de menos, que es la dirección en que se desfasa
    sola —nace una suite y nadie toca el documento—."""
    import re as _re
    p = r / "CONTINUAR.md"
    t = p.read_text(encoding="utf-8")
    m = _re.search(r"[Ll]as (\d+) suites de `_verificacion/mutaciones_\*\.py`", t)
    assert m, "no encuentro la cuenta de suites en CONTINUAR.md"
    p.write_text(t[:m.start(1)] + str(int(m.group(1)) - 1) + t[m.end(1):],
                 encoding="utf-8")
    return ("CONTINUAR.md dice una suite de menos de las que hay en el disco")


def f_total_externo_foda(r):
    _sust(r, "FODA.md", "**4.395 valores**", "**4.396 valores**")
    return "FODA.md suma mal el contraste externo: 4396 en vez de 646 + 3749"


# ══ Controles negativos ══════════════════════════════════════════════════

def n_intacta(r):
    return "los documentos sin tocar: tiene que salir en verde"


def n_prosa_reescrita(r):
    _sust(r, "CONTINUAR.md",
          "### Las cifras que este documento promete",
          "### Las cifras que este fichero promete (y que se contrastan solas)")
    _sust(r, "CONTINUAR.md",
          "- 55 mejoras de dote estructuradas, leídas de `dotes/*.yaml`",
          "- 55 mejoras de dote estructuradas en la base, una por dote general")
    return ("se reescribe la prosa de alrededor SIN tocar una sola cifra: los "
            "documentos tienen que poder editarse")


DEBEN = [d_ancla_srd_borrada, d_ancla_foundry_borrada,
         d_linea_integridad_borrada, d_mejoras_borrada,
         d_cuenta_de_suites_borrada, d_arquitectura_borrada,
         d_modulo_nuevo_sin_documentar, d_modulo_muerto_documentado,
         d_fila_nueva_sin_documentar,
         f_cifra_srd, f_cifra_integridad, f_cifra_mejoras,
         f_cuenta_de_suites, f_total_externo_foda]
NO_DEBEN = [n_intacta, n_prosa_reescrita]


def _falla(raiz):
    # `--rapido` salta las suites de mutación (esta incluida: no se llama a sí
    # misma). Lo que se está probando es el contraste documento↔realidad, y
    # eso sí se ejecuta entero.
    res = subprocess.run([sys.executable, "verificar_documentos.py", "--rapido"],
                         cwd=raiz, capture_output=True, text=True)
    return res.returncode != 0, res.stdout + res.stderr


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    return raiz


def main():
    print(__doc__.split("\n\n")[0])
    print("═" * 74)

    falla, salida = _falla(BASE)
    if falla:
        print("✗ CONTROL: `verificar_documentos.py` ya falla con los documentos "
              "intactos. Arréglalo antes de mutar.")
        print(salida[-2500:])
        return 1

    ok = 0
    total = len(DEBEN) + len(NO_DEBEN)

    for mut in DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            falla, _ = _falla(raiz)
            if falla:
                ok += 1
                print(f" ✅ CAZADA · {desc}")
            else:
                print(f" ❌ SE ESCAPA · {desc}")

    for mut in NO_DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            falla, sal = _falla(raiz)
            if not falla:
                ok += 1
                print(f" ✅ CONTROL NEGATIVO · {desc}")
            else:
                print(f" ❌ FALSO POSITIVO · {desc}")
                print("    " + "\n    ".join(sal.splitlines()[-6:]))

    print("─" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total} "
          f"({len(DEBEN)} detecciones + {len(NO_DEBEN)} controles negativos)")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
