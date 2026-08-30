#!/usr/bin/env python3
"""Prueba por mutación de `validar_tiradas()` (Fase 14b-3, 2026-08-30).

`tirada` es un campo único y responde a **una sola** pregunta: ¿el conjuro exige
una tirada para manifestarse? Lo que no puede decir es **cuántas tiradas pide y
de qué tipo cada una**. Cuatro conjuros lo rompen, y se leyeron dos veces cada
uno:

  · *Símbolo*         — 6 modos con salvación propia (Sab o Con), más una
                        PRUEBA de Sabiduría (Percepción) para detectar el glifo,
                        que no es salvación ni ataque.
  · *Muro prismático* — la salvación de Destreza se hace UNA VEZ POR CAPA
                        (siete), y las capas 6 y 7 añaden salvación propia.
  · *Mano de Bigby*   — un modo, «Puño cerrado», **no es salvación sino tirada
                        de ataque**. El campo único decía `Directo`.
  · *Muro de hielo*   — dos salvaciones distintas en momentos distintos.

El chequeo tiene dos mitades y, como siempre, la segunda es la que importa:
**FORMA** (vocabulario, `cuando`, página) y **AUSENCIA** (una descripción que
exige salvaciones de varias características y ningún `tiradas` que lo diga).

Y un control negativo que no es hipotético: *Estática sináptica* menciona
«tirada de salvación de Constitución **para mantener la concentración**», que es
la regla de concentración citada de pasada y **no** una salvación que el conjuro
exija. La heurística contaba 5 conjuros; la lectura de la página dijo 4. Si el
chequeo vuelve a contarla, salta aquí.

    python3 _verificacion/mutaciones_tiradas.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def _conjuro(raiz, nombre, fn):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    fn(h)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ══ AUSENCIA — el defecto que de verdad existía ══════════════════════════

def a_lista_borrada_simbolo(r):
    def f(h): del h["tiradas"]
    _conjuro(r, "Símbolo", f)
    return ("Símbolo sin `tiradas`: 6 modos con salvaciones de Sab y Con "
            "aplastados en un solo campo, como estaban antes")


def a_lista_borrada_bigby(r):
    def f(h): del h["tiradas"]
    _conjuro(r, "Mano de Bigby", f)
    return "Mano de Bigby sin `tiradas`: pierde que un modo es tirada de ataque"


def a_salvacion_perdida(r):
    def f(h): h["tiradas"] = [t for t in h["tiradas"] if t["tipo"] != "TdS Con."]
    _conjuro(r, "Muro de hielo", f)
    return "se pierde la salvación de Constitución del aire gélido"


# ══ FORMA ════════════════════════════════════════════════════════════════

def f_salvacion_inventada(r):
    def f(h):
        h["tiradas"].append({"tipo": "TdS Car.", "cuando": "inventado",
                             "pagina": {"pdf": 314, "libro": 312}})
    _conjuro(r, "Muro de hielo", f)
    return "una salvación de Carisma que la descripción no pide"


def f_tipo_inventado(r):
    def f(h): h["tiradas"][0]["tipo"] = "TdS Suerte"
    _conjuro(r, "Símbolo", f)
    return "tipo «TdS Suerte», fuera del vocabulario"


def f_sin_cuando(r):
    def f(h): del h["tiradas"][1]["cuando"]
    _conjuro(r, "Símbolo", f)
    return "una tirada sin `cuando`: no dice en qué modo se hace"


def f_sin_pagina(r):
    def f(h): del h["tiradas"][0]["pagina"]
    _conjuro(r, "Muro prismático", f)
    return "una tirada sin cita de página (regla 2)"


def f_pagina_no_numerica(r):
    def f(h): h["tiradas"][0]["pagina"] = {"pdf": "315*", "libro": 313}
    _conjuro(r, "Muro prismático", f)
    return "página con asterisco, la errata que ya trajo el CSV"


# ══ Controles negativos ══════════════════════════════════════════════════

def n_reordenar(r):
    def f(h): h["tiradas"] = list(reversed(h["tiradas"]))
    _conjuro(r, "Símbolo", f)
    return "reordenar la lista: el orden no cambia qué salvaciones se piden"


def n_reescribir_cuando(r):
    def f(h): h["tiradas"][0]["cuando"] = "otra redacción del mismo momento"
    _conjuro(r, "Muro de hielo", f)
    return "reescribir un `cuando`: es prosa descriptiva"


def n_modo_sin_tirada(r):
    def f(h):
        h["tiradas"].append({"tipo": "Ninguna", "cuando": "un modo sin tirada",
                             "pagina": {"pdf": 310, "libro": 308}})
    _conjuro(r, "Mano de Bigby", f)
    return "añadir un modo `Ninguna`: no aporta salvación, no rompe el cotejo"


def n_concentracion_no_cuenta(r):
    """EL control que importa: el falso positivo real de la heurística."""
    def f(h):
        h["descripcion"] += (" El objetivo también hará una tirada de salvación "
                             "de Carisma para mantener la concentración.")
    _conjuro(r, "Estática sináptica", f)
    return ("a Estática sináptica se le añade «salvación de Carisma PARA "
            "MANTENER LA CONCENTRACIÓN»: es la regla de concentración citada, "
            "no una salvación del conjuro — no debe exigir `tiradas`")


def n_conjuro_de_una_salvacion(r):
    def f(h): pass
    _conjuro(r, "Bola de fuego", f)
    return "un conjuro normal, de una sola salvación y sin `tiradas`: no es defecto"


AUSENCIA = [a_lista_borrada_simbolo, a_lista_borrada_bigby, a_salvacion_perdida]
FORMA = [f_salvacion_inventada, f_tipo_inventado, f_sin_cuando, f_sin_pagina,
         f_pagina_no_numerica]
NO_DEBEN = [n_reordenar, n_reescribir_cuando, n_modo_sin_tirada,
            n_concentracion_no_cuenta, n_conjuro_de_una_salvacion]


# ══ ATAQUES · la etiqueta tiene que decir lo que dice el texto ═══════════
# Antes de fijar el criterio (2026-08-30), los 11 conjuros con «ataque de
# conjuro cuerpo a cuerpo» llevaban TRES etiquetas distintas y ningún chequeo lo
# veía, porque las tres estaban en el vocabulario.

def q_obligatorio_como_directo(r):
    def f(h): h["tirada"] = "Directo"
    _conjuro(r, "Agarre electrizante", f)
    return ("«Agarre electrizante» dice «Haz un ataque» y se etiqueta `Directo` "
            "sin declararlo en `tiradas`: el ataque quedaría solo en la prosa")


def q_cac_como_distancia(r):
    def f(h): h["tirada"] = "D20+ata.conj."
    _conjuro(r, "Látigo de espinas", f)
    return ("un ataque cuerpo a cuerpo etiquetado como los 14 a distancia: la "
            "confusión exacta que había")


def q_opcional_sin_tiradas(r):
    def f(h): del h["tiradas"]
    _conjuro(r, "Arma espiritual", f)
    return ("«Arma espiritual» se manifiesta sin tirada («puedes hacer») y se le "
            "quita `tiradas`: su ataque deja de poder calcularse")


def q_declarado_pero_no_directo(r):
    def f(h): h["tirada"] = "D20+ata.CaC"
    _conjuro(r, "Mano de Bigby", f)
    return ("«Mano de Bigby» declara su ataque en `tiradas` (la mano se crea sin "
            "tirada) y aun así etiqueta el conjuro como ataque")


def n_bigby_intacto(r):
    def f(h): h["resumen"] = "Otro resumen para la mano."
    _conjuro(r, "Mano de Bigby", f)
    return ("«Mano de Bigby» con `Directo` + `tiradas`: su «Haz un ataque» está "
            "DENTRO de un modo, no en el lanzamiento — control del falso "
            "positivo que dio la primera versión del chequeo")


def n_distancia_normal(r):
    def f(h): h["resumen"] = "Otro resumen."
    _conjuro(r, "Rayo de escarcha", f)
    return "un ataque a distancia normal con `D20+ata.conj.`: no es defecto"


ATAQUES_DEBEN = [q_obligatorio_como_directo, q_cac_como_distancia,
                 q_opcional_sin_tiradas, q_declarado_pero_no_directo]
ATAQUES_NO_DEBEN = [n_bigby_intacto, n_distancia_normal]


def _falla_por(raiz, etiqueta="tiradas por efecto"):
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
        print("✗ CONTROL: no encuentro la línea del chequeo «tiradas por efecto».")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla. Arréglalo antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo")

    ok = 0
    for etiqueta, muts, esperado in (
            ("AUSENCIA · información que se pierde sin la lista", AUSENCIA, True),
            ("FORMA · listas mal escritas", FORMA, True),
            ("Controles negativos: NO deben saltar", NO_DEBEN, False),
            ("ATAQUES · la etiqueta contra el texto", ATAQUES_DEBEN, True),
            ("ATAQUES · controles negativos", ATAQUES_NO_DEBEN, False)):
        etiqueta_chequeo = ("ataques de conjuro" if etiqueta.startswith("ATAQUES")
                            else "tiradas por efecto")
        print(f"\n {etiqueta}")
        for mut in muts:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = pathlib.Path(tmp) / "base"
                shutil.copytree(BASE, raiz, symlinks=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                desc = mut(raiz)
                salta, _ = _falla_por(raiz, etiqueta_chequeo)
                bien = bool(salta) is esperado
                ok += bien
                print(f"   {'✅' if bien else '❌'} {desc}")
                if not bien:
                    print("        ↑ " + ("NO DETECTADA" if esperado
                                           else "FALSO POSITIVO"))

    total = (len(AUSENCIA) + len(FORMA) + len(NO_DEBEN)
             + len(ATAQUES_DEBEN) + len(ATAQUES_NO_DEBEN))
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
