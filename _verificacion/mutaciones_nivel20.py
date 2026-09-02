#!/usr/bin/env python3
"""Prueba por mutación de `verificar_mejoras()` y `verificar_conjuros()`
(2026-08-30, al hacer que el sistema sostenga fichas de nivel 20 monoclase).

Los dos chequeos salieron de construir la **primera ficha de nivel 20** y ver
qué pasaba. Pasaba esto:

  · un monje de nivel 20 con **las seis características a 20** y ninguna
    justificación **verificaba en verde**. `caracteristicas.final` se escribía a
    mano y nada lo ataba a `base` + `ajuste_trasfondo` + las mejoras tomadas;
  · **nadie contaba los conjuros**. Un mago de nivel 20 con dos trucos habría
    pasado igual, y una ficha de nivel 1 de la propia base —`_ejemplo_aerin`—
    llevaba **1 conjuro preparado donde su tabla concede 2**.

En una base cuyo lema es que nada entra sin cita, eran los dos huecos más
grandes que quedaban: no datos malos, datos que **nadie ataba a su fuente**.

Las fichas que los sostienen son `draconido_monje_n20.yaml` (4 mejoras, 20
niveles de PG) y `gnomo_mago_n20.yaml` (55 referencias: 5 trucos + 25
preparados de clase, más los extras declarados de dote y especie).

    python3 _verificacion/mutaciones_nivel20.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
MONJE = "personajes/draconido_monje_n20.yaml"
MAGO = "personajes/gnomo_mago_n20.yaml"
# Tercera ficha: la única con escudo Y entrenamiento con escudos.
CLERIGO = "personajes/aasimar_clerigo.yaml"


def _sust(raiz, rel, viejo, nuevo, n=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, n), encoding="utf-8")


def _editar(raiz, rel, fn):
    """Muta sobre el YAML parseado, no sobre el texto.

    Las primeras versiones de estas mutaciones sustituían cadenas literales y se
    rompieron en cuanto las fichas se reescribieron con otro estilo de YAML. Lo
    que se quiere probar es el DATO, no su formato.
    """
    import yaml
    p = raiz / rel
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    fn(d)
    p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110),
                 encoding="utf-8")


# ══ MEJORAS ══════════════════════════════════════════════════════════════

def m_caracteristica_regalada(r):
    _editar(r, MONJE, lambda d: d["caracteristicas"]["final"].update(
        {k: 20 for k in ("fue", "des", "con", "int", "sab", "car")}))
    return ("el monje de nivel 20 con las seis características a 20: el caso "
            "exacto que verificaba en verde antes de este chequeo")


def m_mejora_borrada(r):
    _editar(r, MONJE, lambda d: d.__setitem__(
        "mejoras", [m for m in d["mejoras"] if m["nivel"] != 12]))
    return "se borra la mejora del nivel 12: ese nivel deja de estar gastado"


def m_mejora_de_tres(r):
    _editar(r, MONJE, lambda d: d["mejoras"][0].__setitem__(
        "sube", {"des": 1, "sab": 1, "con": 1}))
    return ("una mejora que reparte +3: la dote dice «+2 a una, o +1 a dos»")


def m_mejora_en_nivel_falso(r):
    _editar(r, MONJE, lambda d: d["mejoras"][0].__setitem__("nivel", 5))
    return "una mejora en el nivel 5, donde la tabla del Monje no concede ninguna"


def m_supera_veinte(r):
    def f(d):
        for m in d["mejoras"]:
            if m["nivel"] == 16:
                m["sube"] = {"sab": 2}
        d["caracteristicas"]["final"]["sab"] = 22
        d["caracteristicas"]["final"]["des"] = 17
    _editar(r, MONJE, f)
    return "una mejora que dejaría Sabiduría en 22: la dote dice «No puede superar 20»"


# ══ CONJUROS ═════════════════════════════════════════════════════════════

def c_truco_de_mas(r):
    _editar(r, MAGO, lambda d: d["conjuros"]["trucos"].append(
        {"ref": "hechizos.json#Rayo de escarcha"}))
    return "un truco de más sin `origen`: el mago pasa de 5 de clase a 6"


def c_preparado_de_menos(r):
    _editar(r, MAGO, lambda d: d["conjuros"]["preparados"].pop(0))
    return "un preparado de menos: 24 donde la tabla de nivel 20 concede 25"


def c_extra_sin_fuente(r):
    def f(d):
        for s in d["conjuros"]["trucos"]:
            if s.get("origen", {}).get("dote"):
                s["origen"] = {"nota": "porque sí"}
                return
    _editar(r, MAGO, f)
    return "un extra cuyo `origen` no dice de qué sale"


# ══ Controles negativos ══════════════════════════════════════════════════

def n_otro_reparto_legal(r):
    def f(d):
        d["mejoras"][0]["sube"] = {"des": 1, "con": 1}
        d["caracteristicas"]["final"]["des"] = 18
        d["caracteristicas"]["final"]["con"] = 15
    _editar(r, MONJE, f)
    return ("repartir +1 y +1 en vez de +2, con `final` actualizado: la dote lo "
            "permite y las cuentas cuadran")


def n_otro_conjuro(r):
    _editar(r, MAGO, lambda d: d["conjuros"]["preparados"][0].__setitem__(
        "ref", "hechizos.json#Detectar magia"))
    return "cambiar QUÉ conjuro se prepara: el chequeo cuenta, no juzga la elección"


def n_prosa_de_decisiones(r):
    _editar(r, MONJE, lambda d: d["decisiones"][0].__setitem__(
        "eleccion", "otra redacción de la misma decisión"))
    return "reescribir una decisión: es prosa libre"


# ══ ESTRÉS · los cuatro huecos que destaparon los agentes ════════════════
# Ninguno lo habría encontrado el generador automático: los cuatro son cosas que
# el verificador **dejaba pasar en silencio**, no cosas que reventaran.

def e_dote_sin_prerrequisito(r):
    # OJO al elegirla: la primera versión puso «Atleta» (Fuerza o Destreza 13),
    # que este mago **sí** cumple con Destreza 17, y la mutación no mordía. Hay
    # que pedir algo que de verdad no tenga: entrenamiento con armaduras medias.
    _editar(r, MAGO, lambda d: d.setdefault("dotes", []).append(
        {"ref": "dotes/generales.yaml#Muy acorazado",
         "origen": {"clase": "Mago", "nivel": 4}}))
    return ("una dote cuyo prerrequisito el personaje NO cumple: la Fase 15 "
            "sabía ofrecer las que puede tomar y nadie miraba las que lleva")


def e_subclase_de_otra_clase(r):
    _editar(r, MONJE, lambda d: d["clases"][0].__setitem__(
        "subclase", "clases/subclases/picaro.yaml#Ladrón"))
    return "un Monje con una subclase de Pícaro: la ref resolvía, en otro fichero"


def e_competencia_como_ref(r):
    _editar(r, MAGO, lambda d: d["competencias"]["armas"].__setitem__(
        0, {"ref": "equipo/armas.yaml#Daga", "origen": {"clase": "Mago"}}))
    return ("una competencia declarada como `ref` a un objeto en vez de "
            "`categoria`: nueve de las diecisiete fichas de la base lo hacían")


def e_escudo_sin_entrenamiento(r):
    """«Solo obtienes el bonificador a la CA de un escudo si tienes
    entrenamiento con escudos» (equipo/armaduras.yaml → reglas.escudos). El
    motor lo sumaba SIEMPRE, y lo destapó un agente, no un chequeo.

    Se le quita al clérigo el entrenamiento con escudos: su CA guardada (16)
    debe dejar de cuadrar, porque ya no le tocan esos 2 puntos. Poner un escudo
    a quien no lo sabe usar no sirve de mutación —el motor, ya corregido, no le
    suma nada y no cambia nada—: hay que quitárselo a quien sí lo usaba.
    """
    _editar(r, CLERIGO, lambda d: d["competencias"].__setitem__(
        "armaduras", [a for a in d["competencias"]["armaduras"]
                      if "escudo" not in a.get("categoria", "").lower()]))
    return ("al clérigo se le quita el entrenamiento con escudos: los 2 puntos "
            "de CA del escudo dejan de tocarle")


MEJORAS = [m_caracteristica_regalada, m_mejora_borrada, m_mejora_de_tres,
           m_mejora_en_nivel_falso, m_supera_veinte]
CONJUROS = [c_truco_de_mas, c_preparado_de_menos, c_extra_sin_fuente]
# ══ MULTICLASE · el «✅» que mentía (fase 1 del PLAN_19, 2026-09-02) ══════
# Hasta hoy CUATRO chequeos de `verificar_personaje.py` se degradaban a aviso
# en cuanto la ficha traía más de una clase —recomputar `calculado`, justificar
# las mejoras de característica, contar los conjuros, y las dotes y subclases—
# y la ficha terminaba imprimiendo «✅ FICHA VERIFICADA — 0 problemas».
#
# El cuarto era el peor: se saltaba justo los tres huecos que el estrés con
# agentes había destapado, así que una ficha multiclase esquivaba en silencio
# los chequeos escritos para cazar lo que se colaba en silencio.
#
# Estas mutaciones prueban las dos mitades: que una ficha multiclase se
# RECHACE, y que las monoclase sigan pasando.

def m_dos_clases(r):
    def edita(d):
        d["nivel_total"] = 2
        d["clases"] = list(d["clases"]) + [
            {"ref": "clases/paladin.yaml", "clase": "Paladín", "nivel": 1,
             "subclase": None}]
    _editar(r, CLERIGO, edita)
    return ("el clérigo pasa a ser clérigo 1/paladín 1: la ficha tiene que "
            "RECHAZARSE, no aprobarse con un aviso")


def m_dos_clases_nivel_alto(r):
    def edita(d):
        d["clases"] = list(d["clases"]) + [
            {"ref": "clases/guerrero.yaml", "clase": "Guerrero", "nivel": 2,
             "subclase": None}]
        d["nivel_total"] = 22
    _editar(r, MONJE, edita)
    return ("el monje de nivel 20 gana 2 niveles de guerrero: ni siquiera con "
            "una ficha que verifica 55 referencias se aprueba lo que no se mira")


def n_una_sola_clase_sigue_pasando(r):
    """Control: lo que se cierra es la multiclase, no las fichas de siempre."""
    def edita(d):
        d["_nota_prueba"] = "campo extra que nadie lee"
    _editar(r, CLERIGO, edita)
    return ("un campo extra en una ficha de UNA clase: el cierre de la "
            "multiclase no puede llevarse por delante lo que ya funcionaba")


ESTRES = [e_dote_sin_prerrequisito, e_subclase_de_otra_clase,
          e_competencia_como_ref, e_escudo_sin_entrenamiento]
NO_DEBEN = [n_otro_reparto_legal, n_otro_conjuro, n_prosa_de_decisiones,
            n_una_sola_clase_sigue_pasando]
MULTICLASE = [m_dos_clases, m_dos_clases_nivel_alto]


def _falla(raiz, ficha):
    r = subprocess.run([sys.executable, "verificar_personaje.py", ficha],
                       cwd=raiz, capture_output=True, text=True)
    return r.returncode != 0


def _falla_cualquiera(raiz):
    return _falla(raiz, MONJE) or _falla(raiz, MAGO) or _falla(raiz, CLERIGO)


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)
    if _falla_cualquiera(BASE):
        print("✗ CONTROL: alguna de las tres fichas ya falla sin tocar nada.")
        return 1
    print(" ✅ control · las tres fichas verifican sin tocar nada")

    ok = 0
    for etiqueta, muts, esperado in (
            ("MEJORAS · características que nadie justificaba", MEJORAS, True),
            ("CONJUROS · cuántos lleva la ficha contra la tabla", CONJUROS, True),
            ("ESTRÉS · los huecos que destaparon los agentes", ESTRES, True),
            ("MULTICLASE · rechazar, no aprobar sin mirar", MULTICLASE, True),
            ("Controles negativos: NO deben saltar", NO_DEBEN, False)):
        print(f"\n {etiqueta}")
        for mut in muts:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = pathlib.Path(tmp) / "base"
                shutil.copytree(BASE, raiz, symlinks=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                desc = mut(raiz)
                salta = _falla_cualquiera(raiz)
                bien = bool(salta) is esperado
                ok += bien
                print(f"   {'✅' if bien else '❌'} {desc}")
                if not bien:
                    print("        ↑ " + ("NO DETECTADA" if esperado
                                           else "FALSO POSITIVO"))

    total = (len(MEJORAS) + len(CONJUROS) + len(ESTRES) + len(MULTICLASE)
             + len(NO_DEBEN))
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
