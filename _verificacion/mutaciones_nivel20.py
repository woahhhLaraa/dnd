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
# Cuarta ficha: la única con una subclase que concede conjuros (ronda 2).
CLERIGO_N5 = "personajes/enano_clerigo_n5.yaml"
# Quinta ficha: la única con un idioma concedido por un RASGO DE CLASE
# («Druídico»), que es el caso que el chequeo de idiomas no puede
# llevarse por delante al cerrar el hueco nº 3.
DRUIDA = "personajes/goliat_druida.yaml"


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


# ══ EL TOPE Y LA CANTIDAD SE LEEN DE LA BASE ═════════════════════════════
# La ronda 2 de estrés destapó que `verificar_mejoras` llevaba el «+2» y el
# tope de 20 CABLEADOS con literales, mientras 42 de las 43 dotes generales ya
# traían `mejora_caracteristica: {cantidad, maximo, entre}` estructurado. La
# que faltaba era «Mejora de característica», justo la que el esquema designa
# para cada entrada de `mejoras:`.
#
# Estas mutaciones no prueban «que salte»: prueban que el número que aplica
# SALE DE LA BASE. Un chequeo con el 20 cableado pasaría las dos primeras.

def m_tope_de_la_dote_bajado(r):
    """Se baja el tope de la dote a 19 SIN tocar la ficha. Las dos fichas de
    nivel 20 tienen una característica en 20 exacto, así que un verificador
    que lea la base tiene que rechazarlas ahora, y uno con el 20 cableado
    seguiría en verde."""
    _sust(r, "dotes/generales.yaml",
          "mejora_caracteristica: {cantidad: 2, maximo: 20, entre: cualquiera}",
          "mejora_caracteristica: {cantidad: 2, maximo: 19, entre: cualquiera}")
    return ("el tope de «Mejora de característica» bajado a 19 en la BASE: la "
            "ficha no se toca, y su 20 exacto deja de ser legal")


def m_cantidad_de_la_dote_cambiada(r):
    """Ídem con la cantidad: si sube a 3, los repartos de +2 de las fichas
    dejan de cuadrar. Un `!= 2` cableado no lo notaría."""
    _sust(r, "dotes/generales.yaml",
          "mejora_caracteristica: {cantidad: 2, maximo: 20, entre: cualquiera}",
          "mejora_caracteristica: {cantidad: 3, maximo: 20, entre: cualquiera}")
    return ("la cantidad de «Mejora de característica» puesta en 3 en la BASE: "
            "los repartos de +2 de las fichas dejan de cuadrar")


def m_estructura_de_la_dote_borrada(r):
    """Sin `mejora_caracteristica` no hay cantidad ni tope que aplicar. El
    verificador tiene que NEGARSE, no suponer los que llevaba cableados."""
    _sust(r, "dotes/generales.yaml",
          "    mejora_caracteristica: {cantidad: 2, maximo: 20, entre: cualquiera}\n",
          "")
    return ("borrada la `mejora_caracteristica` de la dote: el verificador se "
            "queda sin fuente y tiene que negarse, no suponer")


def m_mejora_sin_ref(r):
    """Una entrada de `mejoras:` que no dice de qué dote sale. Antes daba
    igual —se suponía la genérica—; ahora es lo que ata la entrada a su
    autoridad."""
    _editar(r, MONJE, lambda d: d["mejoras"][0].pop("ref", None))
    return "una mejora sin `ref`: no dice de qué dote saca su cantidad y su tope"


def m_reparto_con_parte_negativa(r):
    """`{sab: 3, des: -1}` suma 2 y NO es ninguna de las dos formas que el
    texto permite. El chequeo viejo solo miraba la suma y la forma [2]/[1,1]
    sobre los valores, así que este caso se le colaba."""
    def f(d):
        d["mejoras"][0]["sube"] = {"sab": 3, "des": -1}
        d["caracteristicas"]["final"]["sab"] = 21
        d["caracteristicas"]["final"]["des"] = 17
    _editar(r, MONJE, f)
    return ("un reparto de {sab: 3, des: -1}: suma 2 pero ninguna parte puede "
            "ser 0 ni negativa")


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
           m_mejora_en_nivel_falso, m_supera_veinte,
           m_tope_de_la_dote_bajado, m_cantidad_de_la_dote_cambiada,
           m_estructura_de_la_dote_borrada, m_mejora_sin_ref,
           m_reparto_con_parte_negativa]
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
    """Control: lo que se cierra es la multiclase, no las fichas de siempre.

    Perturbaba con un campo extra (`_nota_prueba`) hasta el 2026-09-05, y
    entonces `verificar_claves()` —que cierra el hueco nº 5 de la ronda 2—
    empezó a rechazar, con razón, cualquier clave que el esquema no
    contemple. El control no era falso: era su VEHÍCULO el que dejó de ser
    legal. Se cambia por uno que sí lo es y la intención no se toca."""
    def edita(d):
        d["jugador"] = "Lara"
    _editar(r, CLERIGO, edita)
    return ("rellenar `jugador` en una ficha de UNA clase: el cierre de la "
            "multiclase no puede llevarse por delante lo que ya funcionaba")


# ══ Ronda 2 de estrés (2026-09-05) ═══════════════════════════════════════
# Los dos FALSOS POSITIVOS que encontró, arreglados AFINANDO y no relajando,
# más los controles negativos que prueban que siguen afinados. La ficha que
# los sostiene es `enano_clerigo_n5.yaml`, que entró en la base por esto: era
# la única superficie —una subclase que concede conjuros— que no ejercitaba
# ninguna de las 17 anteriores, y por eso el falso positivo pudo vivir.

def e_conjuro_de_subclase_inventado(r):
    """El arreglo del falso positivo NO es «acepta `subclase` y calla»: la
    base trae `conjuros_siempre_preparados`, así que el origen se COMPRUEBA."""
    _sust(r, CLERIGO_N5, '"hechizos.json#Arma espiritual", origen: {subclase',
          '"hechizos.json#Bola de fuego", origen: {subclase')
    return ("un conjuro que dice venir del Dominio de la Guerra y no está en "
            "su tabla de siempre preparados")


def e_conjuro_de_subclase_a_destiempo(r):
    """El nivel también se comprueba: `Espíritus guardianes` lo concede el
    dominio en el nivel 5, no en el 3."""
    _sust(r, CLERIGO_N5,
          '"hechizos.json#Espíritus guardianes", origen: {subclase: "Dominio de la Guerra", nivel: 5}',
          '"hechizos.json#Espíritus guardianes", origen: {subclase: "Dominio de la Guerra", nivel: 3}')
    return ("un conjuro de dominio que declara un nivel distinto del que la "
            "tabla de la subclase dice")


def e_conjuro_de_otra_subclase(r):
    _sust(r, CLERIGO_N5,
          '"hechizos.json#Arma mágica", origen: {subclase: "Dominio de la Guerra"',
          '"hechizos.json#Arma mágica", origen: {subclase: "Dominio de la Vida"')
    return ("un conjuro que dice venir de una subclase que no es la del "
            "personaje")


def n_conjuros_de_subclase_bien_declarados(r):
    """CONTROL NEGATIVO, y es el falso positivo que destapó la ronda 2: los
    seis conjuros de dominio del Clérigo, declarados exactamente como manda
    el esquema, se rechazaban uno a uno porque `subclase` no estaba en la
    lista de orígenes que el chequeo sabía reconocer."""
    _sust(r, CLERIGO_N5, "nombre: \"Doran Piedrafría\"",
          "nombre: \"Doran Piedrafría el Sereno\"")
    return ("la ficha con sus 6 conjuros de dominio bien declarados: es "
            "LEGAL y tiene que pasar")


def n_categoria_con_mayuscula(r):
    """CONTROL NEGATIVO, el otro falso positivo: la base guarda la
    herramienta del trasfondo en minúscula y la categoría de la clase con
    mayúscula. Escribirla con la mayúscula natural del castellano es legal;
    la capitalización es ortografía, no dato."""
    _sust(r, CLERIGO_N5, 'categoria: "suministros de calígrafo"',
          'categoria: "Suministros de calígrafo"')
    return ("la herramienta del trasfondo escrita con mayúscula inicial: "
            "es la misma herramienta")


def e_categoria_con_tilde_cambiada(r):
    """Y la contraprueba de que normalizar mayúsculas no se llevó por delante
    las TILDES, que en castellano sí son dato — este proyecto ya perdió
    tiempo con la tilde de `Clérigo`."""
    _sust(r, CLERIGO_N5, 'categoria: "suministros de calígrafo"',
          'categoria: "suministros de caligrafo"')
    return ("la herramienta sin la tilde de «calígrafo»: la tilde SÍ es dato")


# ── Hueco nº 2 de la ronda 2: `pg_por_nivel` sin contrastar ──────────────
# Tres caras del mismo defecto, las tres declaradas por agentes distintos.
# El valor se SUMABA sin mirar si podía salir del dado, y la autoridad ya
# estaba leída desde la Fase 14b-1 en `calculo.valor_establecido_pg()`.

def e_pg_tirada_fuera_del_dado(r):
    _sust(r, CLERIGO_N5, "metodo: tirada, valor: 6", "metodo: tirada, valor: 9")
    return "una tirada de 9 en un d8: el dado no puede darla"


def e_pg_valor_establecido_de_otra_clase(r):
    """El más fino de los tres: el método es correcto y el número existe —es
    el del Bárbaro—, solo que en la tabla de otra clase."""
    _sust(r, CLERIGO_N5, "- {nivel: 4, clase: Clérigo, metodo: valor_establecido, valor: 5,",
          "- {nivel: 4, clase: Clérigo, metodo: valor_establecido, valor: 7,")
    return ("un `valor_establecido` de 7 en un Clérigo, que es el del "
            "Bárbaro: el número existe, en la tabla de otra clase")


def e_pg_maximo_dado_fuera_del_nivel_1(r):
    _sust(r, CLERIGO_N5, "- {nivel: 3, clase: Clérigo, metodo: valor_establecido, valor: 5,",
          "- {nivel: 3, clase: Clérigo, metodo: maximo_dado, valor: 8,")
    return ("`metodo: maximo_dado` en el nivel 3: es la regla del nivel 1, y "
            "vive en otra página")


def n_pg_tirada_al_minimo(r):
    """CONTROL NEGATIVO: un 1 en el dado es legal, por deprimente que sea.
    Un chequeo que exigiera «un valor razonable» sería un chequeo que opina."""
    def edita(d):
        for e in d["pg_por_nivel"]:
            if e["nivel"] == 5:
                e["valor"] = 1
        d["calculado"]["pg_max"] = 39
    _editar(r, CLERIGO_N5, edita)
    return "una tirada de 1 en el d8: es el peor resultado posible, y es legal"


# ── Huecos nº 1 y nº 4: qué hay DENTRO de la lista de conjuros ───────────
# Los dos son el mismo descuido con dos caras: el chequeo contaba la longitud
# de la lista y no miraba qué había dentro.

def e_conjuro_de_otra_clase(r):
    """Hueco nº 1. Lo predijo el agente A con «Tañido por los muertos» en un
    Hechicero, y resultó ser REAL en una ficha de la base: el mismo día se
    encontró «Descarga sobrenatural» —conjuro de Brujo— entre los trucos de
    `draconido_hechicero_n4.yaml`. Los 391 conjuros traen `clases`."""
    _sust(r, MAGO, "- ref: hechizos.json#Amistad",
          "- ref: hechizos.json#Descarga sobrenatural")
    return ("un truco de Brujo entre los de un Mago: los 391 conjuros dicen "
            "de qué listas son y nadie lo miraba")


def e_truco_entre_los_preparados(r):
    """Hueco nº 4, el que estaba VIVO en la base: un conjuro de nivel 0 entre
    los preparados infla el recuento de la tabla sin que nada lo note."""
    _sust(r, CLERIGO_N5, '- {ref: "hechizos.json#Disipar magia", origen: {clase: Clérigo}}',
          '- {ref: "hechizos.json#Reparar", origen: {clase: Clérigo}}')
    return ("un truco (nivel 0) entre los preparados: cuenta contra la tabla "
            "sin ser un conjuro preparado de verdad")


def e_conjuro_repetido_en_las_dos_listas(r):
    """La otra cara: el mismo conjuro en `trucos` y en `preparados`, que es
    exactamente lo que llevaba `draconido_hechicero_n4.yaml`."""
    _sust(r, CLERIGO_N5, '- {ref: "hechizos.json#Disipar magia", origen: {clase: Clérigo}}',
          '- {ref: "hechizos.json#Guía", origen: {clase: Clérigo}}')
    return ("el mismo conjuro en `trucos` y en `preparados`: contaba dos veces")


def n_conjuro_de_dote_de_otra_lista(r):
    """CONTROL NEGATIVO, y es la razón por la que el chequeo del hueco nº 1
    solo mira los conjuros que CUENTAN contra la tabla: «Iniciado en la
    magia» concede conjuros de una lista ELEGIDA —clérigo, druida o mago—,
    que por diseño puede no ser la del personaje."""
    _sust(r, CLERIGO_N5,
          '- {ref: "hechizos.json#Detectar el bien y el mal", origen: {dote: "Iniciado en la magia"}}',
          '- {ref: "hechizos.json#Grasa", origen: {dote: "Iniciado en la magia"}}')
    return ("un conjuro de la lista de MAGO concedido por «Iniciado en la "
            "magia» a un Clérigo: la dote lo permite y no cuenta contra la tabla")


# ── Hueco nº 3: los idiomas, que no llevan `ref:` y por eso nadie miraba ──

def e_idioma_por_especie(r):
    """Lo que dos agentes inventaron por separado, uno con el señuelo de que
    el idioma se llama igual que la especie. Ninguna de las 10 especies de
    esta base concede idiomas."""
    _sust(r, CLERIGO_N5, "    - {nombre: Enano}",
          "    - {nombre: Enano, origen: {especie: Enano}}")
    return ("un idioma que dice venir de la especie: ninguna especie de esta "
            "base concede idiomas")


def e_idioma_fuera_de_tabla(r):
    """El nombre no canónico. Estaba VIVO en dos fichas de la base —«Élfico»
    en vez de «Elfo»—, y el propio `_ejemplo_aerin.yaml` llevaba escrito que
    era un bug real que ningún validador pillaba «porque `idiomas` no lleva
    `ref:`». Se arregló en el ejemplo y se quedó en las otras dos."""
    _sust(r, CLERIGO_N5, "    - {nombre: Gigante}", "    - {nombre: Gigántico}")
    return "un idioma que no está en la tabla: «Gigántico» en vez de «Gigante»"


def e_idioma_de_rasgo_inexistente(r):
    _sust(r, CLERIGO_N5, "    - {nombre: Gigante}",
          "    - {nombre: Gigante, origen: {clase: Clérigo, rasgo: \"Lengua divina\"}}")
    return ("un idioma que dice venir de un rasgo que su clase no tiene")


def e_idiomas_de_mas_por_eleccion(r):
    _sust(r, CLERIGO_N5, "    - {nombre: Gigante}",
          "    - {nombre: Gigante}\n    - {nombre: Goblin, origen: {regla: \"reglas/idiomas.yaml#nota\"}}\n"
          "    - {nombre: Orco, origen: {regla: \"reglas/idiomas.yaml#nota\"}}\n"
          "    - {nombre: Gnomo, origen: {regla: \"reglas/idiomas.yaml#nota\"}}")
    return ("tres idiomas elegidos de la tabla estándar, y la nota concede "
            "«común y otros dos»")


def n_idioma_de_rasgo_de_clase(r):
    """CONTROL NEGATIVO: «Druídico» del Druida y «Jerga de ladrones» del
    Pícaro SÍ son idiomas que un rasgo de clase concede, y las fichas de la
    base los declaran así. El chequeo no puede llevárselos por delante."""
    _sust(r, DRUIDA, "eleccion:", "eleccion:", n=1)
    return ("el Druida con «Druídico» por su rasgo de clase, verificado de "
            "verdad: es legítimo y tiene que seguir pasando")


# ── Hueco nº 5: las claves que el esquema no contempla ───────────────────
# La tentación era rechazar las tres claves que los agentes inventaron. Eso
# habría sido el parche puntual, y la cuarta se colaría igual. La lista de
# claves válidas se LEE de `personajes/_ESQUEMA.md`, así que estas tres
# mutaciones prueban la misma máquina, no tres remiendos.

def e_clave_raza(r):
    _sust(r, CLERIGO_N5, "nivel_total: 5", "nivel_total: 5\nraza: \"Enano\"")
    return "una clave `raza:` duplicando `especie:`, que el esquema no tiene"


def e_clave_en_singular(r):
    """La más traicionera de las tres: `caracteristica` en singular no es una
    clave de más, es el bloque OBLIGATORIO enmascarado — con ella presente,
    quien lea por encima ve un bloque de características que no existe."""
    _sust(r, CLERIGO_N5, "caracteristicas:\n  metodo:",
          "caracteristica:\n  metodo:")
    return ("`caracteristica` en singular: no sobra una clave, falta el "
            "bloque obligatorio")


def e_clave_nunca_vista(r):
    """La que ningún agente probó, y es la que justifica hacerlo por
    descubrimiento: si la lista se hubiera escrito a mano con las tres que
    aparecieron, esta se colaría."""
    _sust(r, CLERIGO_N5, "nivel_total: 5", "nivel_total: 5\ninventario_secreto: 3")
    return ("una clave que nadie había inventado todavía: la lista sale del "
            "esquema, no de los casos que ya se vieron")


def n_clave_de_prosa_libre(r):
    """CONTROL NEGATIVO: `historia` y `personalidad` no están en el bloque de
    ejemplo del esquema, sino en su sección «Prosa libre». Las dos fuentes
    cuentan, y un chequeo que solo leyera el ejemplo rechazaría fichas
    legítimas de la propia base."""
    _sust(r, CLERIGO_N5, "nivel_total: 5",
          "nivel_total: 5\nhistoria: \"Creció entre yunques y letanías.\"")
    return ("un campo `historia:`, que el esquema permite en «Prosa libre» "
            "aunque no salga en su bloque de ejemplo")


# ── Fase 1.2 de la auditoría: de dónde sale el bloque `calculado` ────────
# El muro entre quien escribe el número y quien lo verifica. No arregla la
# aritmética —eso es el mandato «el calculista»—, hace visible si un número
# lo escribió el motor o una lectura independiente de la página.

def e_calculado_sin_origen(r):
    def edita(d):
        d["calculado"].pop("_origen", None)
    _editar(r, CLERIGO_N5, edita)
    return "`calculado` sin `_origen`: no dice de dónde sale"


def e_origen_agente_sin_informe(r):
    """Firmar como lectura independiente sin decir dónde está la lectura."""
    def edita(d):
        d["calculado"]["_origen"] = {"metodo": "agente-manual", "informe": None,
                                     "fecha": "2026-09-05"}
    _editar(r, CLERIGO_N5, edita)
    return ("`_origen: agente-manual` sin `informe:`: una firma que no se "
            "puede ir a leer no vale")


def e_origen_informe_inexistente(r):
    def edita(d):
        d["calculado"]["_origen"] = {
            "metodo": "agente-manual",
            "informe": "_verificacion/_aritmetica/no-existe.md",
            "fecha": "2026-09-05"}
    _editar(r, CLERIGO_N5, edita)
    return "`_origen.informe` apunta a un fichero que no existe"


def e_campo_de_mas_en_calculado(r):
    """Un número en `calculado` que el verificador no recalcula es un número
    inventado: hasta hoy sobraba en silencio."""
    def edita(d):
        d["calculado"]["iniciativa"] = 3
    _editar(r, CLERIGO_N5, edita)
    return "un campo en `calculado` que nadie recalcula"


ESTRES = [e_dote_sin_prerrequisito, e_subclase_de_otra_clase,
          e_competencia_como_ref, e_escudo_sin_entrenamiento,
          e_conjuro_de_subclase_inventado, e_conjuro_de_subclase_a_destiempo,
          e_conjuro_de_otra_subclase, e_categoria_con_tilde_cambiada,
          e_pg_tirada_fuera_del_dado, e_pg_valor_establecido_de_otra_clase,
          e_pg_maximo_dado_fuera_del_nivel_1,
          e_conjuro_de_otra_clase, e_truco_entre_los_preparados,
          e_conjuro_repetido_en_las_dos_listas,
          e_idioma_por_especie, e_idioma_fuera_de_tabla,
          e_idioma_de_rasgo_inexistente, e_idiomas_de_mas_por_eleccion,
          e_clave_raza, e_clave_en_singular, e_clave_nunca_vista,
          e_calculado_sin_origen, e_origen_agente_sin_informe,
          e_origen_informe_inexistente, e_campo_de_mas_en_calculado]
NO_DEBEN = [n_otro_reparto_legal, n_otro_conjuro, n_prosa_de_decisiones,
            n_una_sola_clase_sigue_pasando,
            n_conjuros_de_subclase_bien_declarados, n_categoria_con_mayuscula,
            n_pg_tirada_al_minimo, n_conjuro_de_dote_de_otra_lista,
            n_idioma_de_rasgo_de_clase, n_clave_de_prosa_libre]
MULTICLASE = [m_dos_clases, m_dos_clases_nivel_alto]


def _falla(raiz, ficha):
    r = subprocess.run([sys.executable, "verificar_personaje.py", ficha],
                       cwd=raiz, capture_output=True, text=True)
    return r.returncode != 0


def _falla_cualquiera(raiz):
    return any(_falla(raiz, f)
               for f in (MONJE, MAGO, CLERIGO, CLERIGO_N5, DRUIDA))


# ── Robustez: un fallo no puede llevarse por delante el informe ──────────
# Los dos defectos de robustez de la ronda 2 no son reglas nuevas: son sobre
# CÓMO se informa. Por eso no valen las mutaciones normales, que solo miran
# el código de salida —un traceback también «falla»—. Estas miran la SALIDA.
ROBUSTEZ = []


def _robustez(fn):
    ROBUSTEZ.append(fn)
    return fn


@_robustez
def rb_bloque_ausente_se_explica(raiz):
    """Una ficha sin `caracteristicas` moría con un `KeyError` en
    `buscar.py:174` sin imprimir una sola línea. Rechazaba, pero no decía qué
    faltaba."""
    _sust(raiz, CLERIGO_N5, "caracteristicas:\n  metodo:", "caracteristica:\n  metodo:")
    r = subprocess.run([sys.executable, "verificar_personaje.py", CLERIGO_N5],
                       cwd=raiz, capture_output=True, text=True)
    salida = r.stdout + r.stderr
    bien = (r.returncode != 0 and "Traceback" not in salida
            and "caracteristica" in salida)
    return bien, ("una ficha sin el bloque `caracteristicas`: tiene que "
                  "EXPLICARLO, no reventar con un traceback mudo")


@_robustez
def rb_un_fallo_no_tapa_los_demas(raiz):
    """`calculo` cortaba con `sys.exit` ante un `pg_por_nivel` con un hueco, y
    con él se iban los chequeos que venían detrás: la ficha 3 del agente B
    declaraba CINCO defectos y solo se veía UNO."""
    def edita(d):
        d["pg_por_nivel"] = [e for e in d["pg_por_nivel"] if e["nivel"] != 3]
        d["competencias"]["idiomas"].append({"nombre": "Gigántico"})
    _editar(raiz, CLERIGO_N5, edita)
    r = subprocess.run([sys.executable, "verificar_personaje.py", CLERIGO_N5],
                       cwd=raiz, capture_output=True, text=True)
    salida = r.stdout + r.stderr
    bien = (r.returncode != 0 and "pg_por_nivel" in salida
            and "Gigántico" in salida)
    return bien, ("dos defectos independientes a la vez: el hueco en "
                  "`pg_por_nivel` no puede tapar el idioma inventado")


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

    print("\n Robustez · el informe no se pierde por el primer fallo")
    for fn in ROBUSTEZ:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            bien, desc = fn(raiz)
            ok += bien
            print(f"   {'✅' if bien else '❌'} {desc}")

    total = (len(MEJORAS) + len(CONJUROS) + len(ESTRES) + len(MULTICLASE)
             + len(NO_DEBEN) + len(ROBUSTEZ))
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
