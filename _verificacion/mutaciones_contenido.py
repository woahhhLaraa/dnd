#!/usr/bin/env python3
"""Prueba por mutación de los once chequeos de CONTENIDO sin red (bloque B).

    validar_clase        validar_especies    validar_trasfondos  validar_dotes
    validar_subclases    validar_rasgos_clase                    validar_equipo
    validar_hechizos     validar_hechizos_clases
    validar_habilidades  validar_idiomas

Son los que sostienen que la transcripción esté COMPLETA y sea COHERENTE: que
haya 10 especies y 16 trasfondos y no 9 y 15, que un rasgo de clase esté en el
nivel que dice su tabla, que el dado de una subclase caiga en los niveles que
esa clase concede, que ninguna dote entre sin página. Ninguno había visto
nunca un dato malo.

`validar_clase` merece una nota: es el único de los treinta cuya etiqueta es
DINÁMICA —imprime el nombre de la clase, «Bárbaro», no una etiqueta fija—, así
que se muta el Bárbaro y se busca su línea. Es también el que compara los
espacios de conjuro contra las tablas `COMPLETO`/`MEDIO` de `validar.py`, que
son constantes SIN cita; el censo lo tiene declarado como pendiente y aquí solo
se comprueba que la comparación existe y muerde.

    python3 _verificacion/mutaciones_contenido.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _arnes import principal, sust                     # noqa: E402

CHEQUEOS = ("validar_clase", "validar_especies", "validar_trasfondos",
            "validar_dotes", "validar_subclases", "validar_rasgos_clase",
            "validar_equipo", "validar_hechizos", "validar_hechizos_clases",
            "validar_habilidades", "validar_idiomas")

ESPECIES = "especies/especies.yaml"
TRASFONDOS = "trasfondos/trasfondos.yaml"
HABILIDADES = "reglas/habilidades.yaml"
IDIOMAS = "reglas/idiomas.yaml"
BARB = "clases/barbaro.yaml"


# ══ clase · etiqueta «Bárbaro» ════════════════════════════════════════════

def cl_pb_movido(r):
    sust(r, BARB, "- {n: 5,  pb: 3", "- {n: 5,  pb: 4")
    return ("el bonificador por competencia del nivel 5 pasa a 4; la fórmula "
            "del manual (2 + (nivel-1)//4) da 3")


def cl_nivel_fuera_de_secuencia(r):
    sust(r, BARB, "- {n: 7,", "- {n: 8,")
    return "dos niveles 8 y ningún 7 en la tabla del Bárbaro"


def cl_edicion_no_sellada(r):
    sust(r, BARB, 'edicion: "2024 (5.5e)"', 'edicion: "2014 (5e)"')
    return "la tabla del Bárbaro sellada como edición 2014"


def cl_espacios_de_lanzador(r):
    sust(r, "clases/mago.yaml", "prep: 6,  slots: [4,2,0,0,0,0,0,0,0]",
         "prep: 6,  slots: [4,3,0,0,0,0,0,0,0]")
    return ("el Mago con un espacio de nivel 2 de más en el nivel 3: deja de "
            "ser la progresión de un lanzador completo")


def cl_tabla_citada_movida(r):
    # Desde el bloque A2 los espacios de conjuro NO son un literal de Python:
    # se leen de la tabla citada de `reglas/generacion_personaje.yaml` (pdf 47
    # = libro 45). Mover una fila de esa tabla tiene que sacar en rojo a las
    # clases lanzadoras, que están transcritas cada una desde su página.
    sust(r, "reglas/generacion_personaje.yaml",
         '- {nivel: 3,  "1": 4, "2": 2,', '- {nivel: 3,  "1": 4, "2": 3,')
    return ("mover el N3 de la tabla CITADA de espacios de conjuro: la "
            "progresión del Mago, transcrita aparte, deja de cuadrar")


def cl_espacios_medio_derivados(r):
    # `MEDIO` era el segundo literal sin cita; ahora se deriva de la tabla
    # citada con la regla del propio manual («la mitad, redondeando arriba»).
    sust(r, "clases/paladin.yaml", "slots: [2,0,0,0,0]", "slots: [3,0,0,0,0]")
    return ("mover los espacios del Paladín, que es lanzador MEDIO: su tabla "
            "se contrasta contra una derivada de la citada, no contra un "
            "literal sin fuente")


def cl_rasgo_renombrado(r):
    sust(r, BARB, '"Instinto salvaje"', '"Instinto primario"', cuenta=1)
    return ("renombrar un rasgo SOLO en la tabla: `validar_rasgos_clase` lo "
            "cazará, pero la tabla en sí sigue bien formada")


# ══ especies · «especies» ═════════════════════════════════════════════════

def es_una_menos(r):
    p = r / ESPECIES
    t = p.read_text(encoding="utf-8")
    i = t.index("  - nombre: Dracónido")
    j = t.index("  - nombre: ", i + 10)
    p.write_text(t[:i] + t[j:], encoding="utf-8")
    return "desaparece el Dracónido: 9 especies donde el manual tiene 10"


def es_sin_pagina(r):
    sust(r, ESPECIES, "  - nombre: Aasimar\n    pagina: {pdf: 188, libro: 186}\n",
         "  - nombre: Aasimar\n")
    return "el Aasimar sin cita de página"


def es_velocidad_imposible(r):
    sust(r, ESPECIES, "  - nombre: Aasimar\n    pagina: {pdf: 188, libro: 186}\n"
         "    tipo: humanoide", "  - nombre: Aasimar\n    pagina: {pdf: 188, libro: 186}\n"
         "    tipo: humanoide\n    _v: x")
    sust(r, ESPECIES, "velocidad_m: 9\n    rasgos:\n      - {nombre: \"Manos curativas\"",
         "velocidad_m: 90\n    rasgos:\n      - {nombre: \"Manos curativas\"")
    return "el Aasimar a 90 m de velocidad, fuera de todo rango del manual"


def es_campo_ausente(r):
    sust(r, ESPECIES, '    tamano: "Mediano (1,5-2,1 m)"\n    velocidad_m: 9',
         "    velocidad_m: 9")
    return "el Dracónido sin campo `tamano`"


def es_rasgo_reescrito(r):
    sust(r, ESPECIES, 'desc: "Resistencia al daño necrótico y al radiante."',
         'desc: "Resistencia al daño radiante y al necrótico."')
    return ("reordenar dos palabras en la descripción de un rasgo: sigue "
            "habiendo 10 especies con sus campos y sus páginas")


# ══ trasfondos · «trasfondos» ═════════════════════════════════════════════

def tr_uno_menos(r):
    p = r / TRASFONDOS
    t = p.read_text(encoding="utf-8")
    i = t.index("  - nombre: Acólito")
    j = t.index("  - nombre: ", i + 10)
    p.write_text(t[:i] + t[j:], encoding="utf-8")
    return "15 trasfondos donde el manual tiene 16"


def tr_dos_caracteristicas(r):
    sust(r, TRASFONDOS, "caracteristicas: [Inteligencia, Sabiduría, Carisma]",
         "caracteristicas: [Inteligencia, Sabiduría]")
    return ("el Acólito con 2 características: en 2024 el trasfondo reparte "
            "siempre sobre 3")


def tr_una_habilidad(r):
    sust(r, TRASFONDOS, "habilidades: [Perspicacia, Religión]",
         "habilidades: [Perspicacia]")
    return "el Acólito con una sola habilidad; el manual da exactamente 2"


def do_citada_por_trasfondo_y_ausente(r):
    sust(r, TRASFONDOS, 'dote: "Iniciado en la magia (clérigo)"',
         'dote: "Iniciado en la nigromancia"')
    return ("el Acólito concede una dote que no está en `dotes/`. El cruce lo "
            "hace `validar_dotes`, no `validar_trasfondos` —el chequeo mira "
            "desde el lado de las dotes—, y por eso esta mutación vive aquí")


def tr_orden_de_habilidades(r):
    sust(r, TRASFONDOS, "habilidades: [Perspicacia, Religión]",
         "habilidades: [Religión, Perspicacia]")
    return "las mismas 2 habilidades en otro orden: siguen siendo 2 y las mismas"


# ══ dotes · «dotes» ═══════════════════════════════════════════════════════

def do_sin_pagina(r):
    sust(r, "dotes/generales.yaml",
         "  - nombre: Acechador\n    pagina: {pdf: 204, libro: 202}\n",
         "  - nombre: Acechador\n")
    return "«Acechador» sin cita de página"


def do_sin_campo_prerrequisito(r):
    sust(r, "dotes/origen.yaml",
         "  - nombre: Afortunado\n    pagina: {pdf: 202, libro: 200}\n    prerrequisito: null\n",
         "  - nombre: Afortunado\n    pagina: {pdf: 202, libro: 200}\n")
    return ("«Afortunado» sin campo `prerrequisito`: ausente no es lo mismo que "
            "`null`, que es la forma de decir «no tiene»")


def do_cuenta_movida(r):
    p = r / "dotes/generales.yaml"
    t = p.read_text(encoding="utf-8")
    i = t.index("  - nombre: Acechador")
    j = t.index("  - nombre: ", i + 10)
    p.write_text(t[:i] + t[j:], encoding="utf-8")
    return "una dote general menos de las que el fichero declara tener"


def do_descripcion_retocada(r):
    sust(r, "dotes/generales.yaml", "Visión ciega hasta 3 m.", "Visión ciega hasta 3 metros.")
    return "reescribir «3 m» como «3 metros» en una dote: sigue con página y prerrequisito"


# ══ subclases · «subclases» ═══════════════════════════════════════════════

def sub_nivel_imposible(r):
    sust(r, "clases/subclases/bardo.yaml", "      - nivel: 3\n        nombre: Juego de pies deslumbrante",
         "      - nivel: 4\n        nombre: Juego de pies deslumbrante")
    return ("un rasgo de subclase del Bardo en el nivel 4, que su clase no "
            "concede (los suyos son 3, 6 y 14)")


def sub_nivel_faltante(r):
    # Los niveles ESPERADOS los deduce el chequeo de los marcadores de
    # `clases/bardo.yaml`, no del campo `niveles_de_subclase` del propio
    # fichero de subclases —que no lee nadie—. Así que el hueco se provoca
    # quitando el rasgo, no cambiando la declaración.
    p = r / "clases/subclases/bardo.yaml"
    txt = p.read_text(encoding="utf-8")
    i = txt.index("      - nivel: 14\n        nombre: Evasión dirigida")
    j = txt.index("  - nombre: Colegio del Conocimiento")
    p.write_text(txt[:i] + txt[j:], encoding="utf-8")
    return ("«Colegio de la Danza» se queda sin su rasgo de nivel 14, que la "
            "tabla del Bardo sí anuncia: la subclase queda incompleta")


def sub_sin_clase(r):
    sust(r, "clases/subclases/bardo.yaml", "clase: Bardo\n", "")
    return "un fichero de subclases sin campo `clase`"


def sub_lema_retocado(r):
    sust(r, "clases/subclases/bardo.yaml", 'lema: "Muévete en armonía con el cosmos."',
         'lema: "Baila en armonía con el cosmos."')
    return "cambiar el lema de una subclase: no es nivel ni página"


# ══ rasgos de clase · «rasgos de clase» ═══════════════════════════════════

def rc_nivel_discrepante(r):
    sust(r, "clases/rasgos/picaro.yaml", '  - nombre: "Ataque furtivo"\n    nivel: 1',
         '  - nombre: "Ataque furtivo"\n    nivel: 2')
    return ("«Ataque furtivo» transcrito en el nivel 2 y anunciado en el 1 por "
            "la tabla del Pícaro: las dos mitades dejan de cuadrar")


def rc_rasgo_sobrante(r):
    sust(r, "clases/rasgos/picaro.yaml", "rasgos:\n",
         'rasgos:\n  - nombre: "Puñalada trapera"\n    nivel: 1\n'
         "    pagina: {pdf: 169, libro: 167}\n    desc: \"Inventado.\"\n")
    return "un rasgo transcrito que la tabla de la clase no anuncia"


def rc_marcador_transcrito(r):
    sust(r, "clases/rasgos/picaro.yaml", "rasgos:\n",
         'rasgos:\n  - nombre: "Mejora de característica"\n    nivel: 4\n'
         "    pagina: {pdf: 169, libro: 167}\n    desc: \"Subes una característica.\"\n")
    return ("«Mejora de característica» transcrita como rasgo: es un MARCADOR "
            "de la tabla, y su regla vive en `reglas/`, no repetida por clase")


def rc_clase_discrepante(r):
    sust(r, "clases/rasgos/picaro.yaml", "clase: Pícaro", "clase: Bribón")
    return "el fichero `rasgos/picaro.yaml` dice ser de la clase «Bribón»"


def rc_desc_reescrita(r):
    sust(r, "clases/rasgos/picaro.yaml", "Una vez por turno, puedes infligir daño adicional",
         "Una vez cada turno, puedes infligir daño adicional")
    return "reescribir una frase del texto de un rasgo: su nivel y su nombre siguen igual"


# ══ equipo · «equipo» ═════════════════════════════════════════════════════

def eq_maestria_inventada(r):
    sust(r, "equipo/armas.yaml", "maestria: Derribar", "maestria: Descuartizar")
    return "un arma con maestría «Descuartizar», que no está en `propiedades_de_maestria`"


def eq_armadura_sin_ca(r):
    sust(r, "equipo/armaduras.yaml",
         '- {nombre: "Armadura acolchada", ca: "11 + mod. Des"',
         '- {nombre: "Armadura acolchada"')
    return "la armadura acolchada sin CA"


def eq_arma_sin_precio(r):
    sust(r, "equipo/armas.yaml",
         '{nombre: Hoz, dano: "1d4 cortante", propiedades: [ligera], maestria: Mellar, peso_kg: 1, precio: "1 po"}',
         '{nombre: Hoz, dano: "1d4 cortante", propiedades: [ligera], maestria: Mellar, peso_kg: 1}')
    return "un arma sin precio"


def eq_peso_retocado(r):
    sust(r, "equipo/armaduras.yaml",
         '- {nombre: "Armadura acolchada", ca: "11 + mod. Des", fuerza: null, sigilo: Desventaja, peso_kg: 4',
         '- {nombre: "Armadura acolchada", ca: "11 + mod. Des", fuerza: null, sigilo: Desventaja, peso_kg: 4.0')
    return "escribir 4.0 en vez de 4 en un peso: es el mismo número"


# ══ hechizos · «hechizos» ═════════════════════════════════════════════════

def he_nivel_invalido(r):
    sust(r, "hechizos.json", '"nivel": 9,', '"nivel": 10,', cuenta=1)
    return "un conjuro de nivel 10; en 2024 la escala llega a 9"


def he_sin_escuela(r):
    sust(r, "hechizos.json", '"escuela": "Evocación",', '"escuela": "",', cuenta=1)
    return "un conjuro sin escuela de magia"


def he_clase_inexistente(r):
    sust(r, "hechizos.json", '"clases": [\n    "Mago"\n   ]',
         '"clases": [\n    "Nigromante"\n   ]')
    return "un conjuro atribuido a la clase «Nigromante», que no existe"


def he_alias_que_es_otro_conjuro(r):
    sust(r, "hechizos.json", '"nombre": "Luz",', '"nombre": "Luz", "alias": ["Bola de fuego"],')
    return "un alias que es el nombre real de otro conjuro: la búsqueda daría dos cosas"


def he_descripcion_retocada(r):
    sust(r, "hechizos.json", '"nombre": "Luz",', '"nombre": "Luz", "_nota_prueba": "x",')
    return "un campo extra en un conjuro: no toca nivel, escuela, página ni clases"


# ══ habilidades · «habilidades» ═══════════════════════════════════════════

def hb_una_menos(r):
    sust(r, HABILIDADES,
         '  - {nombre: Acrobacias, caracteristica: Destreza, desc: "Conservar el equilibrio '
         'en situaciones difíciles o realizar una proeza acrobática."}\n', "")
    return "17 habilidades donde el manual tiene 18"


def hb_caracteristica_inventada(r):
    sust(r, HABILIDADES, "{nombre: Atletismo, caracteristica: Fuerza",
         "{nombre: Atletismo, caracteristica: Vigor")
    return "Atletismo asociado a «Vigor»"


def hb_duplicada(r):
    sust(r, HABILIDADES, "  - {nombre: Historia, caracteristica: Inteligencia",
         "  - {nombre: Atletismo, caracteristica: Inteligencia")
    return "Atletismo dos veces, con dos características distintas"


def hb_desfase_de_pagina(r):
    sust(r, HABILIDADES, "pagina_pdf: 16, pagina_libro: 14",
         "pagina_pdf: 16, pagina_libro: 13")
    return "desfase pdf/libro de 3 en la cita de las habilidades"


def hb_desc_reescrita(r):
    sust(r, HABILIDADES, 'desc: "Saltar más lejos de lo normal',
         'desc: "Saltar más lejos de lo habitual')
    return "reescribir la descripción de Atletismo: sigue habiendo 18 con su característica"


# ══ idiomas · «idiomas» ═══════════════════════════════════════════════════

def id_sin_comun(r):
    sust(r, IDIOMAS, "  - {nombre: Común, origen: Sigil, d12: null}\n", "")
    return ("desaparece «Común» de los idiomas estándar, y todo personaje lo "
            "habla por regla")


def id_duplicado(r):
    sust(r, IDIOMAS, "  - {nombre: Gnomo, origen: Gnomos, d12: 7}",
         "  - {nombre: Elfo, origen: Gnomos, d12: 7}")
    return "«Elfo» dos veces en la tabla de estándar"


def id_en_las_dos_tablas(r):
    sust(r, IDIOMAS, "inusuales:\n", "inusuales:\n  - {nombre: Elfo, origen: Elfos}\n")
    return ("«Elfo» en estándar y en inusuales a la vez: no es un idioma con "
            "dos entradas, es una decisión sin tomar")


def id_desfase_de_pagina(r):
    sust(r, IDIOMAS, "pagina_pdf: 39, pagina_libro: 37", "pagina_pdf: 39, pagina_libro: 36")
    return "desfase pdf/libro de 3 en la cita de los idiomas"


def id_origen_retocado(r):
    sust(r, IDIOMAS, "{nombre: Gigante, origen: Gigantes", "{nombre: Gigante, origen: Ogros")
    return "cambiar el pueblo de origen de un idioma: no es nombre ni tabla ni página"


BLOQUES = [
    ("CLASE · la tabla de 20 niveles (etiqueta dinámica: «Bárbaro»)", "Bárbaro",
     [cl_pb_movido, cl_nivel_fuera_de_secuencia, cl_edicion_no_sellada],
     [cl_rasgo_renombrado]),
    ("CLASE · los espacios de conjuro (etiqueta «Mago»)", "Mago",
     [cl_espacios_de_lanzador, cl_tabla_citada_movida], []),
    ("CLASE · el lanzador medio, derivado de la tabla citada", "Paladín",
     [cl_espacios_medio_derivados], []),
    ("ESPECIES", "especies",
     [es_una_menos, es_sin_pagina, es_velocidad_imposible, es_campo_ausente],
     [es_rasgo_reescrito]),
    ("TRASFONDOS", "trasfondos",
     [tr_uno_menos, tr_dos_caracteristicas, tr_una_habilidad],
     [tr_orden_de_habilidades]),
    ("DOTES", "dotes",
     [do_sin_pagina, do_sin_campo_prerrequisito, do_cuenta_movida,
      do_citada_por_trasfondo_y_ausente],
     [do_descripcion_retocada]),
    ("SUBCLASES", "subclases",
     [sub_nivel_imposible, sub_nivel_faltante, sub_sin_clase], [sub_lema_retocado]),
    ("RASGOS DE CLASE", "rasgos de clase",
     [rc_nivel_discrepante, rc_rasgo_sobrante, rc_marcador_transcrito,
      rc_clase_discrepante], [rc_desc_reescrita]),
    ("EQUIPO", "equipo",
     [eq_maestria_inventada, eq_armadura_sin_ca, eq_arma_sin_precio],
     [eq_peso_retocado]),
    ("HECHIZOS", "hechizos",
     [he_nivel_invalido, he_sin_escuela], [he_descripcion_retocada]),
    ("HECHIZOS ⊆ CLASES", "hechizos ⊆ clases",
     [he_clase_inexistente, he_alias_que_es_otro_conjuro], []),
    ("HABILIDADES", "habilidades",
     [hb_una_menos, hb_caracteristica_inventada, hb_duplicada, hb_desfase_de_pagina],
     [hb_desc_reescrita]),
    ("IDIOMAS", "idiomas",
     [id_sin_comun, id_duplicado, id_en_las_dos_tablas, id_desfase_de_pagina],
     [id_origen_retocado]),
]


if __name__ == "__main__":
    sys.exit(principal(__doc__, BLOQUES))
