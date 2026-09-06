#!/usr/bin/env python3
"""Prueba por mutación de `deuda.py` (fase 1 del PLAN_21 — 2026-09-06).

`deuda.py` lleva la contabilidad de las CINCO líneas base del proyecto. Si
miente, mienten las cinco a la vez —y en la dirección que menos se nota, que es
callar—. Un módulo así no puede existir sin guardián: es literalmente el defecto
que el PLAN_21 persigue, «un verificador que se comprueba a sí mismo no
comprueba nada».

Se le rompe una propiedad cada vez y se exige que salte, contra una copia
desechable de la base. Las propiedades son las que la abstracción existe para
garantizar, y cada una viene de un defecto REAL medido el 2026-09-06:

  · podar            — `rasgos_sin_declarar` era el único que no podía bajar
  · nuevo ≠ perdido  — `mutaciones_motor` llamó regresión a una medición nueva
  · guardar elenco   — sin él, lo anterior es indecidible
  · identidad fija   — tres veces se eligió mal, y las tres el guardián mintió
  · prosa que dura   — la explicación de un fichero no puede borrarla la poda,
                       y conservarla por una LISTA DE CLAVES escrita a mano ya
                       nacía corta: `_migracion_plan21` no estaba en ella

Y dos controles negativos, porque una abstracción que salte al reescribir una
nota obligaría a no tocar la prosa, y unos ficheros que no se pueden explicar
dejan de explicarse.

    python3 _verificacion/mutaciones_deuda.py
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


# ══ Mutaciones de la ABSTRACCIÓN ═════════════════════════════════════════

def m_no_poda(r):
    """Sin poda, la deuda no baja nunca en disco: algo que hoy está cubierto y
    mañana deja de estarlo vuelve a contar como «declarado» en silencio."""
    _sust(r, "deuda.py",
          "        if podar:\n"
          "            self._escribir({**vigentes, **fuera_de_base}, elenco_hoy,",
          "        if False:\n"
          "            self._escribir({**vigentes, **fuera_de_base}, elenco_hoy,")
    return "`Deuda.contrastar` deja de podar lo saldado"


def m_confunde_nuevo_con_perdido(r):
    """El defecto exacto que `mutaciones_motor` tuvo hasta el 2026-09-06."""
    _sust(r, "deuda.py",
          "            perdidos = {k: v for k, v in fuera_de_base.items()\n"
          "                        if k in elenco_previo}",
          "            perdidos = dict(fuera_de_base)")
    return ("todo lo que no está en la línea base cuenta como REGRESIÓN, "
            "aunque nunca se hubiera medido")


def m_no_guarda_elenco(r):
    _sust(r, "deuda.py",
          "        if elenco is not None:\n            doc[\"elenco\"] = sorted(elenco)",
          "        if False:\n            doc[\"elenco\"] = sorted(elenco)")
    return ("`Deuda` deja de guardar el elenco: sin él no se puede distinguir "
            "una medición nueva de una regresión")


def m_identidad_no_se_comprueba(r):
    """Si la identidad puede cambiar en silencio, la línea base deja de
    significar lo mismo y nadie se entera: es la tercera forma del mismo error
    —una huella mal elegida— con la que este proyecto ya ha tropezado tres
    veces."""
    _sust(r, "deuda.py",
          "        if previa is not None and previa != self.identidad:",
          "        if False:")
    _sust(r, "censo.py", 'identidad="fichero-almohadilla-nombre"',
          'identidad="otra-cosa-cualquiera"')
    return ("la identidad de un fichero cambia y `Deuda` no lo comprueba: la "
            "línea base ya no significa lo mismo")


def m_prosa_ajena_se_pierde(r):
    """La regla inviolable 6 dentro del módulo que existe para que las listas
    no se queden atrás: volver a conservar la prosa por una lista de claves
    escrita a mano, como hacía la primera versión."""
    _sust(r, "deuda.py",
          "        propias = set(doc) | {\"_ultima_poda\"}\n"
          "        for k, v in (previo or {}).items():\n"
          "            if k.startswith(\"_\") and k not in propias:\n"
          "                doc[k] = v",
          "        for k in (\"_migracion\", \"_umbral\"):\n"
          "            if previo and k in previo:\n"
          "                doc[k] = previo[k]")
    return ("la prosa propia de un fichero se conserva por una lista de claves "
            "escrita a mano, y lo que no esté en ella se borra al podar")


def m_prosa_vacia_gana(r):
    """El defecto medido el 2026-09-06: `_como_se_salda` en blanco en tres de
    los cinco ficheros, sin forma de repararlo desde el llamador."""
    _sust(r, "deuda.py",
          '            "_nota": (previo or {}).get("_nota") or self.nota,',
          '            "_nota": (previo or {}).get("_nota", self.nota),')
    _sust(r, "deuda.py",
          '            "_como_se_salda": ((previo or {}).get("_como_se_salda")\n'
          '                               or self.como_se_salda),',
          '            "_como_se_salda": (previo or {}).get("_como_se_salda",\n'
          '                                                 self.como_se_salda),')
    return ("una prosa VACÍA en el disco le gana a la del llamador: el campo "
            "que dice cómo se paga una deuda se queda en blanco para siempre")


def m_cerrada_admite_lo_nuevo(r):
    """El defecto REAL del 2026-09-06, el mismo día: al migrar
    `verificar_chequeos` una rama silenciosa en código nuevo dejó de ser roja
    porque nunca había estado en el elenco. `mutaciones_silencios` lo cazó,
    3/6. Aquí se muta la política en su sitio, la abstracción."""
    _sust(r, "deuda.py",
          "        if self.cerrada:\n"
          "            return {**self.perdidos, **self.medidos_nuevos}\n"
          "        return dict(self.perdidos)",
          "        return dict(self.perdidos)")
    return ("una deuda CERRADA admite una entrada que nunca se había medido: "
            "el código nuevo entra en verde")


def m_deuda_saldada_no_sale(r):
    """La poda existe, pero lo saldado se vuelve a escribir: la lista no baja."""
    _sust(r, "deuda.py",
          "            self._escribir({**vigentes, **fuera_de_base}, elenco_hoy,",
          "            self._escribir({**base, **fuera_de_base}, elenco_hoy,")
    return "lo saldado se reescribe en la línea base en vez de salir de ella"


# ══ Controles negativos ══════════════════════════════════════════════════

def n_nota_reescrita(r):
    """La prosa de un fichero de deuda tiene que poder editarse. Si saltara,
    nadie volvería a explicar por qué una deuda está ahí."""
    import json
    p = r / "_verificacion/rasgos_sin_declarar.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["_nota"] = "Redactado de otra forma el " + d.get("_fecha", "hoy") + "."
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return "se reescribe la `_nota` de un fichero de deuda, sin tocar una entrada"


def n_identidad_explicada_reescrita(r):
    """La EXPLICACIÓN de la identidad es prosa; la clave corta es lo que se
    compara. Esa separación se añadió porque la primera versión comparaba la
    frase y saltó contra su propio autor a los diez minutos."""
    import json
    p = r / "_verificacion/motor_sin_carga.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["_identidad_explicada"] = "el nombre de la función, dicho de otra manera"
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return "se reescribe la explicación de la identidad, no la clave"


DEBEN = [m_no_poda, m_confunde_nuevo_con_perdido, m_no_guarda_elenco,
         m_identidad_no_se_comprueba, m_prosa_ajena_se_pierde,
         m_cerrada_admite_lo_nuevo, m_prosa_vacia_gana,
         m_deuda_saldada_no_sale]
NO_DEBEN = [n_nota_reescrita, n_identidad_explicada_reescrita]


# ══ Arnés ════════════════════════════════════════════════════════════════
# **El arnés CREA la situación, y esa es la lección de esta suite.**
#
# La primera versión corría los cinco llamadores contra la base intacta y sacó
# 2/7: con los cinco ficheros en reposo —nada que podar, nada nuevo, nada
# perdido— romper «¿poda?» no cambia ni un byte. Es el mismo error que el
# recableado del `10` de la CA en el PLAN_20: **una mutación que solo cambia el
# comportamiento en una situación que no ocurre, no cambia nada**.
#
# Así que aquí se fabrica cada situación con un fichero de deuda desechable y
# se comprueba la propiedad directamente. Sigue siendo prueba por mutación —se
# corrompe `deuda.py` y se exige que salte—, pero contra un escenario que
# ejercita lo que se rompe.
ESCENARIOS = {
    "poda": {
        "ayer": {"a": "uno", "b": "dos"},
        "hoy": {"a": "uno"},                    # «b» se saldó
        "elenco": {"a", "b"},
        "espera": lambda inf, doc: (list(doc["entradas"]) == ["a"]
                                    and set(inf.saldados) == {"b"}),
        "que_prueba": "lo saldado sale del fichero y se anuncia",
    },
    "medicion_nueva": {
        "ayer": {"a": "uno"},
        "hoy": {"a": "uno", "z": "nunca medido"},
        "elenco": {"a", "z"},                   # «z» NO estaba en el elenco de ayer
        "espera": lambda inf, doc: (set(inf.medidos_nuevos) == {"z"}
                                    and not inf.perdidos),
        "que_prueba": "una medición nueva NO es una regresión",
    },
    "regresion": {
        "ayer": {"a": "uno"},
        "elenco_ayer": {"a", "b"},              # «b» se medía AYER y no era deuda
        "hoy": {"a": "uno", "b": "ha dejado de estar cubierto"},
        "elenco": {"a", "b"},
        "espera": lambda inf, doc: (set(inf.perdidos) == {"b"}
                                    and inf.hay_regresion),
        "que_prueba": "algo que se cubría y ya no, es ROJO",
    },
    "elenco": {
        "ayer": {"a": "uno"},
        "hoy": {"a": "uno"},
        "elenco": {"a", "b", "c"},
        # `_ultima_poda` va aparte de la prosa descubierta —lo escribe este
        # módulo—, así que tiene su propia rama de conservación y su propio
        # riesgo: la migración del 2026-09-06 se llevó el de
        # `efectos_sin_carga.json`, que decía con nombre y apellidos los tres
        # efectos saldados el día antes. Se restauró de git.
        "prosa": {"_ultima_poda": {"fecha": "ayer", "saldados": ["algo"]}},
        "espera": lambda inf, doc: (set(doc.get("elenco") or ()) == {"a", "b", "c"}
                                    and doc.get("_ultima_poda", {}).get("fecha")
                                    == "ayer"),
        "que_prueba": ("el elenco de lo medido queda escrito, y la última poda "
                       "no se pierde cuando no hay poda nueva"),
    },
    # Cada fichero de deuda trae prosa suya —por qué es una lista y no un
    # comodín, qué NO dice, con qué umbral se midió, qué era cada cosa antes de
    # migrarlo—. Si la poda se la come, la deuda queda sin explicación, que es
    # como una deuda enumerada deja de poder saldarse. La primera versión la
    # conservaba por una LISTA DE CLAVES escrita dentro del módulo, y ya nacía
    # corta: `motor_sin_carga.json` traía `_migracion_plan21`, que no estaba en
    # ella.
    # La política, no la medición: `chequeos_silenciosos` dice «ninguna nueva
    # puede aparecer» y no hace excepción con el código recién escrito, que es
    # justo por donde entran. Sin este escenario la migración del 2026-09-06
    # dejó pasar una rama silenciosa nueva en verde, y `mutaciones_silencios`
    # bajó a 3/6.
    "cerrada": {
        "ayer": {"a": "uno"},
        "hoy": {"a": "uno", "z": "nunca medido, y esta lista no admite nada"},
        "elenco": {"a", "z"},
        "cerrada": True,
        "espera": lambda inf, doc: (set(inf.rojos) == {"z"}
                                    and inf.hay_regresion
                                    and not inf.perdidos),
        "que_prueba": ("en una deuda CERRADA lo medido por primera vez "
                       "también es rojo"),
    },
    # El campo que dice CÓMO SE PAGA una deuda estaba vacío en tres de los
    # cinco ficheros el 2026-09-06: el guion que los migró los escribió en
    # blanco, y como el disco mandaba siempre, la prosa que los llamadores sí
    # tenían escrita no podía llegar nunca. Una deuda que no dice cómo se salda
    # es una deuda que nadie salda.
    "prosa_vacia": {
        "ayer": {"a": "uno", "b": "dos"},
        "prosa": {"_nota": "", "_como_se_salda": ""},
        "hoy": {"a": "uno"},
        "elenco": {"a", "b"},
        "espera": lambda inf, doc: (doc.get("_nota") == "n"
                                    and doc.get("_como_se_salda") == "c"),
        "que_prueba": ("una prosa vacía en el disco no le gana a la del "
                       "llamador"),
    },
    "prosa_ajena": {
        "ayer": {"a": "uno", "b": "dos"},
        "prosa": {"_migracion_plan21": "qué era cada cosa antes",
                  "_umbral": "≥3 cadenas", "_lo_que_NO_dice": "nada del resto"},
        "hoy": {"a": "uno"},                    # se poda «b»: hay reescritura
        "elenco": {"a", "b"},
        "espera": lambda inf, doc: all(
            doc.get(k) == v for k, v in
            {"_migracion_plan21": "qué era cada cosa antes",
             "_umbral": "≥3 cadenas",
             "_lo_que_NO_dice": "nada del resto"}.items()),
        "que_prueba": "la prosa propia del fichero sobrevive a la poda",
    },
}


def _ejecuta(raiz, escenario):
    """Corre un escenario contra la `deuda.py` que haya en `raiz`."""
    guion = f"""
import json, pathlib, sys
sys.path.insert(0, {str(raiz)!r})
import deuda as D
f = pathlib.Path({str(raiz)!r}) / "_verificacion" / "_prueba_deuda.json"
if f.exists(): f.unlink()
dd = D.Deuda("_verificacion/_prueba_deuda.json", nota="n", como_se_salda="c",
             identidad="prueba", cerrada={escenario.get("cerrada", False)!r})
dd.contrastar({escenario["ayer"]!r}, elenco_hoy={escenario.get("elenco_ayer", set(escenario["ayer"]))!r})
prosa = {escenario.get("prosa", {})!r}
if prosa:
    _d = json.loads(f.read_text(encoding="utf-8")); _d.update(prosa)
    f.write_text(json.dumps(_d, ensure_ascii=False, indent=1), encoding="utf-8")
inf = dd.contrastar({escenario["hoy"]!r}, elenco_hoy={escenario["elenco"]!r})
doc = json.loads(f.read_text(encoding="utf-8"))
print(json.dumps({{"vigentes": inf.vigentes, "saldados": inf.saldados,
                   "medidos_nuevos": inf.medidos_nuevos, "perdidos": inf.perdidos,
                   "rojos": inf.rojos, "doc": doc}}, ensure_ascii=False))
"""
    r = subprocess.run([sys.executable, "-c", guion], capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr.strip().splitlines()[-1:] 
    import json as _j
    return _j.loads(r.stdout), None


class _Inf:
    def __init__(self, d):
        self.vigentes, self.saldados = d["vigentes"], d["saldados"]
        self.medidos_nuevos, self.perdidos = d["medidos_nuevos"], d["perdidos"]
        self.rojos = d["rojos"]
        self.hay_regresion = bool(self.rojos)


def _todos_los_escenarios_pasan(raiz):
    """¿Se comporta `deuda.py` como promete, en las cuatro situaciones?"""
    fallos = []
    for nombre, esc in ESCENARIOS.items():
        salida, err = _ejecuta(raiz, esc)
        if salida is None:
            fallos.append(f"{nombre}: reventó · {err}")
            continue
        if not esc["espera"](_Inf(salida), salida["doc"]):
            fallos.append(f"{nombre}: {esc['que_prueba']}")
    return fallos


def _identidad_se_comprueba(raiz):
    """Escenario aparte: cambiar la clave de identidad tiene que LANZAR."""
    guion = f"""
import pathlib, sys
sys.path.insert(0, {str(raiz)!r})
import deuda as D
f = pathlib.Path({str(raiz)!r}) / "_verificacion" / "_prueba_ident.json"
if f.exists(): f.unlink()
D.Deuda("_verificacion/_prueba_ident.json", nota="", como_se_salda="",
        identidad="una").contrastar({{"a": "uno"}}, elenco_hoy={{"a"}})
try:
    D.Deuda("_verificacion/_prueba_ident.json", nota="", como_se_salda="",
            identidad="otra").contrastar({{"a": "uno"}}, elenco_hoy={{"a"}})
    print("SIGUIO_ADELANTE")
except ValueError:
    print("PARO_EN_SECO")
"""
    r = subprocess.run([sys.executable, "-c", guion], capture_output=True, text=True)
    # Comparación EXACTA, no subcadena. La primera versión preguntaba
    # `"LANZO" in r.stdout` contra las salidas «LANZO»/«NO_LANZO», y «NO_LANZO»
    # contiene «LANZO»: la propiedad daba por buena justo la respuesta que
    # tenía que delatar. `m_identidad_no_se_comprueba` salió 6/7 por esto.
    return r.stdout.strip() == "PARO_EN_SECO"


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    return raiz


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)

    with tempfile.TemporaryDirectory() as tmp:
        raiz = _copia(tmp)
        fallos = _todos_los_escenarios_pasan(raiz)
        ident = _identidad_se_comprueba(raiz)
    if fallos or not ident:
        print("✗ CONTROL: `deuda.py` ya incumple sus propias promesas sin "
              "tocarla. Arréglalo antes de mutar.")
        for f in fallos:
            print("   ·", f)
        if not ident:
            print("   · la identidad no se comprueba")
        return 1
    print(f" ✅ control · `deuda.py` cumple los {len(ESCENARIOS)} escenarios y "
          f"comprueba la identidad")

    ok = 0
    print("\n Mutaciones que DEBEN notarse")
    for mut in DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            salta = bool(_todos_los_escenarios_pasan(raiz)) or not _identidad_se_comprueba(raiz)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("        ↑ NO DETECTADA — la abstracción puede mentir "
                      "en esto y los cinco ficheros con ella")

    print("\n Controles negativos: NO deben notarse")
    for mut in NO_DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            r = subprocess.run([sys.executable, "censo.py"], cwd=raiz,
                               capture_output=True, text=True)
            verde = r.returncode == 0
            ok += bool(verde)
            print(f"   {'✅' if verde else '❌'} {desc}")
            if not verde:
                print("        ↑ FALSO POSITIVO — la prosa de un fichero de "
                      "deuda tiene que poder editarse")

    total = len(DEBEN) + len(NO_DEBEN)
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
