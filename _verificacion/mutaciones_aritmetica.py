#!/usr/bin/env python3
"""Prueba por mutación de los cinco chequeos de ARITMÉTICA sin red (bloque B).

Estos cinco son los que sostienen el contrato del proyecto —«un personaje legal
de nivel 1 a 20»— y hasta hoy ninguno había visto nunca un dato malo:

    validar_atributos_basicos   validar_generacion   validar_competencias_clase
    validar_ataques             validar_mejoras_de_dote

`validar_mejoras_de_dote` va el primero a propósito. Se escribió el 2026-08-31
para cerrar el defecto de las dotes —el verificador estaba INVERTIDO: aceptaba
la ficha con el +1 perdido y rechazaba la correcta— y se dejó sin suite el
mismo día en que el plan criticaba justo eso. Es deuda propia, y esta es la
primera que se paga.

Cada mutación comprueba **su** chequeo por la etiqueta que imprime, no que
`validar.py` falle: una mutación que rompe la base entera y hace saltar a otro
chequeo no demuestra nada sobre este.

    python3 _verificacion/mutaciones_aritmetica.py
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _arnes import principal, sust                     # noqa: E402

CHEQUEOS = ("validar_mejoras_de_dote", "validar_atributos_basicos",
            "validar_conjuros_cd",
            "validar_generacion", "validar_competencias_clase",
            "validar_ataques")

GEN = "reglas/generacion_personaje.yaml"
BARB = "clases/barbaro.yaml"
GENERALES = "dotes/generales.yaml"


# ══ mejoras de dote · «mejoras de dote» ═══════════════════════════════════
# El defecto real: 54 de las 75 dotes conceden «Mejora de característica: X
# +1», y ese +1 vivía SOLO dentro de la cadena `descripcion`. Aquí se rompe
# por los dos lados —prosa sin estructura y estructura sin prosa— porque el
# chequeo existe para que las dos mitades no puedan separarse.

def md_prosa_sin_estructura(r):
    sust(r, GENERALES,
         "    mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Carisma]}\n"
         '    descripcion: "Mejora de característica: Carisma +1',
         '    descripcion: "Mejora de característica: Carisma +1')
    return ("«Actor» pierde su `mejora_caracteristica` y conserva el texto: EL "
            "caso real, el +1 que no aplicaría nadie")


def md_estructura_sin_prosa(r):
    sust(r, GENERALES,
         'descripcion: "Mejora de característica: Carisma +1 (máx. 20). Suplantación',
         'descripcion: "Suplantación')
    return ("«Actor» conserva la estructura y pierde la frase del manual: una "
            "mejora que ningún texto cita es un dato inventado")


def md_ida_y_vuelta_rota(r):
    sust(r, GENERALES,
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Carisma]}",
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Sabiduría]}")
    return ("«Actor» declara Sabiduría y su texto dice Carisma: la ida y vuelta "
            "deja de cuadrar palabra por palabra")


def md_maximo_movido(r):
    sust(r, GENERALES,
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Destreza]}",
         "mejora_caracteristica: {cantidad: 1, maximo: 22, entre: [Destreza]}",)
    return "«Acechador» con máximo 22 y «(máx. 20)» en su texto"


def md_caracteristica_inventada(r):
    sust(r, GENERALES,
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Fuerza, Destreza]}\n"
         '    descripcion: "Mejora de característica: Fuerza o Destreza',
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Fuerza, Vigor]}\n"
         '    descripcion: "Mejora de característica: Fuerza o Vigor')
    return ("«Apresador» entre Fuerza y «Vigor», que no es una de las seis "
            "características")


def md_dote_sin_mejora(r):
    sust(r, "dotes/origen.yaml",
         'descripcion: "Puntos de suerte:', 'descripcion: "Suerte pura:')
    return ("tocar el texto de «Afortunado», que no concede mejora ninguna: sin "
            "promesa no hay deuda")


def md_otra_dote_con_mejora(r):
    sust(r, GENERALES,
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Carisma]}\n"
         '    descripcion: "Mejora de característica: Carisma +1 (máx. 20). Suplantación',
         "mejora_caracteristica: {cantidad: 1, maximo: 20, entre: [Sabiduría]}\n"
         '    descripcion: "Mejora de característica: Sabiduría +1 (máx. 20). Suplantación')
    return ("cambiar «Actor» a Sabiduría EN LAS DOS MITADES: la dote quedaría "
            "mal transcrita, pero eso no lo mira este chequeo — mira que las "
            "dos mitades digan lo mismo, y lo dicen")


# ══ atributos básicos · «atributos básicos» ═══════════════════════════════

def ab_caracteristica_inventada(r):
    sust(r, BARB, "caracteristica_principal: Fuerza", "caracteristica_principal: Vigor")
    return "el Bárbaro con «Vigor» como característica principal"


def ab_aptitud_incoherente(r):
    sust(r, "clases/mago.yaml", "caracteristica_principal: Inteligencia",
         "caracteristica_principal: Destreza")
    return ("el Mago con principal Destreza y aptitud mágica Inteligencia: dos "
            "campos del mismo fichero que dejan de concordar")


def ab_oro_fuera_de_la_ultima(r):
    sust(r, BARB, 'b: "75 po"', 'b: "hacha a dos manos y 15 po"')
    return ("la última opción de equipo del Bárbaro deja de ser solo oro (el "
            "manual siempre cierra con la bolsa)")


def ab_desfase_de_pagina(r):
    sust(r, BARB, "fuente: {pagina_pdf: 53, pagina_libro: 51}",
         "fuente: {pagina_pdf: 53, pagina_libro: 50}")
    return ("desfase pdf/libro de 3 en el Bárbaro: el manual entero va con 2, y "
            "un desfase suelto es una cita mal copiada")


def ab_sin_cita(r):
    sust(r, BARB, "  fuente: {pagina_pdf: 53, pagina_libro: 51}\n", "")
    return "`atributos_basicos` del Bárbaro sin cita de página"


def ab_opciones_no_correlativas(r):
    sust(r, BARB, '    b: "75 po"', '    c: "75 po"')
    return "opciones de equipo a/c en vez de a/b: la serie tiene un hueco"


def ab_otro_equipo_valido(r):
    sust(r, BARB, 'a: "hacha a dos manos, 4 hachas de mano, paquete de explorador y 15 po"',
         'a: "hacha a dos manos, 4 hachas de mano, paquete de mazmorreo y 15 po"')
    return ("cambiar el paquete de la opción A: sigue siendo una opción bien "
            "formada con su oro (mal transcrita, pero no es lo que mira esto)")


# ══ generación de personaje · «generación de personaje» ═══════════════════
# El invariante bonito de este chequeo: los tres métodos se atan entre sí. El
# conjunto estándar tiene que costar exactamente los 27 puntos de la compra
# por puntos, así que mover un número de cualquiera de las dos tablas rompe.

def gen_coste_movido(r):
    sust(r, GEN, "      14: 7\n", "      14: 8\n")
    return ("subir a 8 el coste de la puntuación 14: el conjunto estándar deja "
            "de costar 27 puntos — es el caso `_TABLA_COSTE` visto desde el dato")


def gen_conjunto_desordenado(r):
    sust(r, GEN, "- {clase: Bárbaro,    fue: 15, des: 13, con: 14, int: 10, sab: 12, car: 8}",
         "- {clase: Bárbaro,    fue: 13, des: 15, con: 14, int: 10, sab: 12, car: 8}")
    return ("el Bárbaro con 13 en Fuerza y 15 en Destreza: la puntuación más "
            "alta deja de ir a la característica principal")


def gen_reparto_imposible(r):
    sust(r, GEN, "- {clase: Mago,       fue: 8,  des: 12, con: 13, int: 15, sab: 14, car: 10}",
         "- {clase: Mago,       fue: 8,  des: 12, con: 13, int: 16, sab: 14, car: 10}")
    return "el Mago con un 16, que no está en el conjunto estándar 15/14/13/12/10/8"


def gen_modificador_mal(r):
    sust(r, GEN, "      \"12-13\": 1", "      \"12-13\": 2")
    return "el modificador de 12-13 pasa a +2; la fórmula (p-10)//2 da +1"


def gen_multiclase_columna_ausente(r):
    # Desde el 2026-09-02 esta tabla ES la fuente citada de los espacios del
    # lanzador completo (bloque A2), así que su contraste numérico lo hace
    # `validar_clase` contra las 10 clases lanzadoras —mover una fila saca 7
    # en rojo, y eso lo prueba `mutaciones_contenido.py`—. Lo que queda aquí
    # es lo que ese contraste NO ve: que la tabla esté completa.
    sust(r, GEN, '- {nivel: 5,  "1": 4, "2": 3, "3": 2,',
         '- {nivel: 5,  "1": 4, "2": 3,')
    return ("a la tabla de espacios multiclase le falta la columna del nivel 3 "
            "de conjuro en el N5: una columna ausente no es un 0, es un dato "
            "que nadie ha transcrito")


def gen_multiclase_desordenada(r):
    sust(r, GEN, '- {nivel: 5,  "1": 4,', '- {nivel: 6,  "1": 4,')
    return "la tabla de espacios multiclase con dos filas «nivel 6» y ningún 5"


def gen_requisito_incoherente(r):
    sust(r, GEN, 'Bárbaro: {requisito: "Fuerza 13+"}',
         'Bárbaro: {requisito: "Destreza 13+"}')
    return ("el requisito de multiclase del Bárbaro pide Destreza y su "
            "característica principal es Fuerza")


def gen_falta_regla_multiclase(r):
    sust(r, GEN, "  clase_de_armadura:", "  clase_de_armadura_:")
    return "desaparece la regla `clase_de_armadura` del bloque de multiclase"


def gen_descripcion_retocada(r):
    sust(r, GEN, 'descripcion: "Cómo repartir 15/14/13/12/10/8 según la clase.',
         'descripcion: "Reparto de 15/14/13/12/10/8 por clase.')
    return ("reescribir una descripción en prosa: no hay número que cambie, y "
            "este chequeo comprueba números")


# ══ competencias de clase · «competencias de clase» ═══════════════════════

def cc_dado_golpe_inventado(r):
    sust(r, BARB, "dado_golpe: d12", "dado_golpe: d14")
    return "el Bárbaro con dado de golpe d14, que no existe"


def cc_dado_incoherente_con_la_multiclase(r):
    # Se muta el GUERRERO, no el Pícaro. El Pícaro no tiene columna `dado` en
    # su progresión ni sale en los ejemplos de multiclase, así que cambiarle
    # el dado no contradice ninguna segunda fuente: la primera versión de esta
    # mutación daba un «no detectada» que hablaba de la mutación, no del
    # chequeo. El Guerrero sí sale, en «guerrero 5/paladín 5 = 10d10».
    sust(r, "clases/guerrero.yaml", "dado_golpe: d10", "dado_golpe: d8")
    return ("el dado de golpe del Guerrero pasa a d8 y el ejemplo de "
            "multiclase de `reglas/` sigue diciendo «10d10»: dos "
            "transcripciones independientes que dejan de coincidir")


def cc_campo_ausente(r):
    sust(r, BARB, "  herramientas: []\n", "")
    return ("el Bárbaro pierde el campo `herramientas`: un campo AUSENTE no es "
            "lo mismo que uno vacío — vacío es una respuesta, ausente deja al "
            "modelo improvisando")


def cc_habilidad_inventada(r):
    sust(r, BARB, "de: [Atletismo, Intimidación, Naturaleza",
         "de: [Atletismo, Intimidación, Botánica")
    return "«Botánica» en la lista de habilidades del Bárbaro, que no es una de las 18"


def cc_herramientas_vacias(r):
    sust(r, "clases/mago.yaml", "  armaduras: []", "  armaduras: []\n  # nota")
    return ("un comentario junto a `armaduras: []` del Mago: la lista vacía es "
            "una respuesta legítima y completa, no un hueco")


# ══ ataques de conjuro · «ataques de conjuro» ═════════════════════════════
# El vocabulario quedó fijado con doble lectura el 2026-08-30 (deuda D2):
# «Haz un ataque» = el conjuro ES el ataque; «puedes hacer» = se manifiesta y
# el ataque viene después, y entonces tiene que estar declarado en `tiradas`.

def at_cuerpo_a_cuerpo_mal_etiquetado(r):
    sust(r, "hechizos.json", '"tirada": "D20+ata.CaC"', '"tirada": "D20+ata.conj."')
    return ("un conjuro cuyo texto dice «ataque de conjuro cuerpo a cuerpo» "
            "etiquetado como `D20+ata.conj.`: el defecto D2 original")


def at_directo_sin_tiradas(r):
    # Tiene que ser un conjuro que DE VERDAD declare su ataque en `tiradas`:
    # el primer `"tirada": "Directo"` del fichero es un conjuro sin ataque
    # ninguno, al que este chequeo ni mira. *Hoja de fuego* es uno de los
    # cinco de la deuda D2: se manifiesta sin tirada y su ataque vive en
    # `tiradas` con su propia página.
    sust(r, "hechizos.json",
         '"tirada": "Directo",\n   "resumen": "El fuego toma forma."',
         '"tirada": "D20+ata.conj.",\n   "resumen": "El fuego toma forma."')
    return ("«Hoja de fuego» declara su ataque en `tiradas` y su `tirada` pasa "
            "a decir que el lanzamiento ES el ataque: es el criterio de la "
            "deuda D2 al revés")


def at_ataque_a_distancia_movido(r):
    sust(r, "hechizos.json", '"tirada": "D20+ata.conj."', '"tirada": "TdS Destreza"')
    return ("un ataque de conjuro a distancia convertido en tirada de "
            "salvación: el texto sigue diciendo «ataque»")


def at_texto_sin_ataque(r):
    sust(r, "hechizos.json", '"nombre": "Luz"', '"nombre": "Luz mágica"')
    return ("renombrar un truco que no describe ningún ataque: este chequeo "
            "solo mira los conjuros cuyo texto habla de atacar")


# ── CD de conjuros (auditoría 2026-09-05) ────────────────────────────────
# La fórmula entró en la base viniendo de `calculo.py`, donde estaba cableada
# con su cita en un comentario. Lo destapó el mandato «el calculista»: dos
# agentes independientes pararon en el mismo sitio porque la base no la
# definía. Traerla no basta — hay que impedir que las dos copias que ahora
# conviven DENTRO del registro (`base:` y su `formula:`) puedan divergir.

def cd_base_cambiada(r):
    sust(r, GEN, "    base: 8\n", "    base: 10\n")
    return ("el `base` de la CD de conjuros pasa a 10 y su `formula` sigue "
            "diciendo «8 +»: dos copias del mismo número sin comparar")


def cd_sin_pagina(r):
    sust(r, GEN, "  pagina: {pdf: 240, libro: 238}\n", "")
    return "la regla de la CD pierde su cita de página"


def cd_bloque_borrado(r):
    """Si la base deja de declararla, `calculo` tiene que NEGARSE, no volver
    a un valor por defecto: ese es todo el punto de haberla traído."""
    sust(r, GEN, "  cd_salvacion:\n", "  cd_salvacion_renombrada:\n")
    return "desaparece `conjuros.cd_salvacion` de la base"


def n_formula_reescrita(r):
    """CONTROL NEGATIVO: la prosa puede redactarse de otro modo mientras siga
    conteniendo el número. Lo que se exige es que las dos copias coincidan,
    no una redacción concreta."""
    sust(r, GEN,
         'formula: "8 + modificador de aptitud mágica + bonificador por competencia"',
         'formula: "8 + mod. de aptitud mágica + bonif. por competencia"')
    return "la fórmula redactada de otra forma, con el mismo 8: es legal"


BLOQUES = [
    ("MEJORAS DE DOTE · la deuda del 2026-08-31", "mejoras de dote",
     [md_prosa_sin_estructura, md_estructura_sin_prosa, md_ida_y_vuelta_rota,
      md_maximo_movido, md_caracteristica_inventada],
     [md_dote_sin_mejora, md_otra_dote_con_mejora]),
    ("ATRIBUTOS BÁSICOS", "atributos básicos",
     [ab_caracteristica_inventada, ab_aptitud_incoherente,
      ab_oro_fuera_de_la_ultima, ab_desfase_de_pagina, ab_sin_cita,
      ab_opciones_no_correlativas],
     [ab_otro_equipo_valido]),
    ("GENERACIÓN DE PERSONAJE · los tres métodos atados entre sí",
     "generación de personaje",
     [gen_coste_movido, gen_conjunto_desordenado, gen_reparto_imposible,
      gen_modificador_mal, gen_multiclase_columna_ausente, gen_multiclase_desordenada,
      gen_requisito_incoherente,
      gen_falta_regla_multiclase],
     [gen_descripcion_retocada]),
    ("COMPETENCIAS DE CLASE", "competencias de clase",
     [cc_dado_golpe_inventado, cc_dado_incoherente_con_la_multiclase, cc_campo_ausente,
      cc_habilidad_inventada],
     [cc_herramientas_vacias]),
    ("CD DE CONJUROS", "CD de conjuros",
     [cd_base_cambiada, cd_sin_pagina, cd_bloque_borrado],
     [n_formula_reescrita]),
    ("ATAQUES DE CONJURO", "ataques de conjuro",
     [at_cuerpo_a_cuerpo_mal_etiquetado, at_directo_sin_tiradas,
      at_ataque_a_distancia_movido],
     [at_texto_sin_ataque]),
]


if __name__ == "__main__":
    sys.exit(principal(__doc__, BLOQUES))
