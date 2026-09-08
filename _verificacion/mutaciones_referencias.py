#!/usr/bin/env python3
"""Prueba por mutación de los tres chequeos de REFERENCIAS sin red (bloque B).

    validar_citas_conjuro   validar_costes_sin_fuente   validar_referencias

── El hallazgo que salió de escribir esta suite, y cómo se cerró ──────────
Al escribirla (bloque B, 2026-08-31) se descubrió que **dos de los tres no
podían fallar**: `validar_costes_sin_fuente` y `validar_referencias` solo
llenaban `warn`, así que su línea salía en ✅ pasara lo que pasara con el dato.
Un conjuro citado por una especie y ausente de `hechizos.json` —integridad
referencial rota— salía como un ⚠ entre otros treinta y `validar.py` terminaba
con «0 errores». No se puede probar nada de un chequeo que no puede fallar.

Entonces se probó la única garantía que daban —que el AVISO apareciera— y se
dejó anotado que promoverlos era una decisión, no una prueba.

**Tomada el 2026-09-02 (fase 1 del PLAN_19): los dos son ERROR.** Se pudo hacer
sin dejar deuda porque los dos estaban a cero. Esta suite pasa de modo `aviso`
a modo `error` en sus dos bloques, que es exactamente el cambio que se quería
poder hacer: la mutación es la misma, lo que sube es lo que se le exige.

    python3 _verificacion/mutaciones_referencias.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _arnes import principal, sust                     # noqa: E402

CHEQUEOS = ("validar_citas_conjuro", "validar_costes_sin_fuente",
            "validar_referencias")


# ══ citas de conjuro · «citas de conjuro» · ERROR ═════════════════════════
# Este sí falla: la regla 2 del proyecto es que sin página no entra nada.

def ci_sin_pagina(r):
    # La página vive en `fuente.pagina_libro`, no en un campo `pagina` suelto.
    # (La primera versión de esta mutación insertaba un `"pagina": null` junto
    # al nombre, que el chequeo ni mira: un «no detectada» que hablaba de la
    # mutación, no del chequeo.)
    sust(r, "hechizos.json", '"pagina_libro": "306"', '"pagina_libro": ""')
    return "un conjuro con `fuente.pagina_libro` vacío: sin página no entra nada"


def ci_pagina_no_numerica(r):
    sust(r, "hechizos.json", '"pagina_libro": "306"', '"pagina_libro": "306*"')
    return ("`pagina_libro` con el asterisco que ya trajo el CSV: el valor "
            "crudo va en `_pagina_origen_csv`, la cita tiene que ser limpia")


def ci_pagina_con_rango(r):
    sust(r, "hechizos.json", '"pagina_libro": "306"', '"pagina_libro": "306-307"')
    return "`pagina_libro` como rango: una cita apunta a UNA página o no apunta"


def ci_resumen_retocado(r):
    sust(r, "hechizos.json", '"resumen": "El fuego toma forma."',
         '"resumen": "Una hoja de fuego."')
    return "reescribir el resumen de un conjuro: su página sigue ahí y sigue siendo un número"


# ══ costes sin fuente · «costes sin fuente» · SOLO AVISA ══════════════════

def co_coste_sin_verificar(r):
    # `_coste_verificado` no es un booleano: es la FRASE de lo que se leyó en
    # la página («sin coste, comprobado en la página (2026-08-29, K1)»). Se
    # renombra la clave en un conjuro para que desaparezca de ese uno solo.
    p = r / "hechizos.json"
    t = p.read_text(encoding="utf-8")
    i = t.index('"_coste_verificado"')
    p.write_text(t[:i] + '"_coste_NO_verificado"' + t[i + len('"_coste_verificado"'):],
                 encoding="utf-8")
    return ("un conjuro con material fuera del SRD pierde su "
            "`_coste_verificado`: su precio deja de respaldarlo nadie")


def co_varios_sin_verificar(r):
    p = r / "hechizos.json"
    t = p.read_text(encoding="utf-8")
    p.write_text(t.replace('"_coste_verificado"', '"_coste_NO_verificado"'),
                 encoding="utf-8")
    return ("los 53 costes leídos a mano pierden su sello: el error tiene que "
            "CONTARLOS, no solo existir")


def co_material_sin_coste(r):
    sust(r, "hechizos.json", '"nombre": "Luz",', '"nombre": "Luz", "_nota_prueba": "x",')
    return ("un campo extra en un truco sin componente material: no cambia "
            "cuántos conjuros con material quedan fuera del SRD")


# ══ referencias · «referencias» · SOLO AVISA ══════════════════════════════

def re_conjuro_citado_inexistente(r):
    sust(r, "especies/especies.yaml", "Conoces el truco luz.",
         "Conoces el truco fulgor arcano.")
    return ("una especie concede el truco «fulgor arcano», que no está en "
            "`hechizos.json`: el personaje tendría un conjuro que no existe")


def re_conjuro_de_nivel_3_inexistente(r):
    sust(r, "hechizos.json", '"nombre": "Luz",', '"nombre": "Luz mágica",')
    return ("se renombra «Luz» en `hechizos.json` y las especies siguen "
            "citándolo por el nombre viejo: la referencia queda colgando")


def re_texto_sin_conjuros(r):
    sust(r, "especies/especies.yaml", 'desc: "Resistencia al daño necrótico y al radiante."',
         'desc: "Resistencia al daño radiante y al necrótico."')
    return "reescribir un rasgo que no cita ningún conjuro: no hay referencia que romper"


BLOQUES = [
    ("CITAS DE CONJURO · la regla 2: sin página no entra", "citas de conjuro",
     [ci_sin_pagina, ci_pagina_no_numerica, ci_pagina_con_rango],
     [ci_resumen_retocado]),
    ("COSTES SIN FUENTE · el sello es obligatorio", "costes sin fuente",
     [co_coste_sin_verificar, co_varios_sin_verificar], [co_material_sin_coste]),
    ("REFERENCIAS · integridad referencial", "referencias",
     [re_conjuro_citado_inexistente, re_conjuro_de_nivel_3_inexistente],
     [re_texto_sin_conjuros]),
]


if __name__ == "__main__":
    sys.exit(principal(__doc__, BLOQUES))
