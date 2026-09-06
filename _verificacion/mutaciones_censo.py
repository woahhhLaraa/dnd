#!/usr/bin/env python3
"""Prueba por mutación de `censo.py` (bloque A del Plan 18 — 2026-09-02).

El censo existe porque ocho veces seguidas una lista escrita a mano se quedó
corta sin que nadie se enterara. Sería una ironía cara que el censo repitiera
el patrón: un contador que no detecta una unidad nueva es exactamente el mismo
fallo, con una capa más de ceremonia encima.

Así que aquí se le rompe la base de once formas distintas —una unidad nueva en
cada una de las seis filas, un alcanzador vaciado, una promesa falsa de
cobertura, un manifiesto podrido— y se exige que **cada una** salga por el
informe. Y cinco controles negativos, porque un censo que dijera «hueco» ante
un dato legítimo obligaría a declarar ruido, y un manifiesto lleno de ruido no
lo lee nadie: que es como se pierde otra vez.

    python3 _verificacion/mutaciones_censo.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
MANIFIESTO = "_verificacion/censo_exenciones.yaml"


def _sust(raiz, rel, viejo, nuevo, cuenta=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, cuenta), encoding="utf-8")


# ══ Una unidad NUEVA en cada fila: el censo tiene que verla ═══════════════

def u_fichero_de_regla(r):
    (r / "reglas" / "maniobras.yaml").write_text(
        "edicion: \"2024 (5.5e)\"\nmaniobras: []\n", encoding="utf-8")
    return ("un fichero de regla nuevo, `reglas/maniobras.yaml`, que ningún "
            "patrón recorre ni el manifiesto excluye")


def u_variable_calculable(r):
    _sust(r, "reglas/efectos.yaml",
          "  velocidad:\n",
          "  iniciativa:\n    tipo: calculada\n    desc: \"bonificador de "
          "iniciativa\"\n  velocidad:\n")
    return ("una cuarta variable calculable (`iniciativa`) sin frase de promesa "
            "en `validar._PROMESAS`")


def u_columna_de_clase(r):
    _sust(r, "clases/picaro.yaml", "ataque_furtivo:", "esquiva_asombrosa: 1, ataque_furtivo:")
    return ("una columna nueva (`esquiva_asombrosa`) en la tabla del Pícaro, "
            "que `verificar_srd.MAPA` no contrasta")


def u_chequeo_nuevo(r):
    p = r / "validar.py"
    t = p.read_text(encoding="utf-8")
    ancla = "def validar_referencias("
    nuevo = ('def validar_conjuros_rituales():\n'
             '    return "conjuros rituales (0)", [], []\n\n\n')
    p.write_text(t.replace(ancla, nuevo + ancla, 1), encoding="utf-8")
    return ("un chequeo nuevo `validar_conjuros_rituales()` sin ninguna suite "
            "de mutación detrás — el caso de `validar_mejoras_de_dote`")


def u_dato_externo(r):
    # `verificar_trasfondos` es el único que pide `origins24/background`, y lo
    # pide una sola vez. (La primera versión de esta mutación tocaba
    # `feats24/feat`, que `verificar_dotes` pide DOS veces: quitando una la
    # categoría seguía pedida y el «no detectada» era de la mutación, no del
    # censo. Es el mismo tropiezo que ya documenta `mutaciones_efectos.py`.)
    _sust(r, "verificar_foundry.py", 'for reg in paquete("origins24", "background"):',
          'for reg in []:')
    return ("`verificar_trasfondos` deja de pedir `origins24/background`: 4 "
            "trasfondos del SRD salen del contraste y el módulo sigue existiendo")


def u_rasgo_nuevo(r):
    # Hasta el bloque D esto era un control «no debe fallar, pero el recuento
    # tiene que subir»: los rasgos sin declarar se tapaban con el comodín
    # `rasgo:*`, que contaba el crecimiento sin impedirlo. Ahora van
    # ENUMERADOS, así que un rasgo nuevo sin declarar tiene que FALLAR. Es
    # exactamente el cambio que el bloque D perseguía, y por eso esta mutación
    # cambia de lista en vez de desaparecer.
    _sust(r, "clases/rasgos/picaro.yaml", "rasgos:\n",
          'rasgos:\n  - nombre: "Reflejos de sombra"\n    nivel: 1\n'
          '    descripcion: "Texto de prueba."\n')
    return ("un rasgo nuevo que no dice si toca alguna variable calculable: "
            "no está en la lista enumerada y no declara nada")


# ══ El alcanzador que se vacía ════════════════════════════════════════════

def a_mapa_recortado(r):
    # Apuntaba a `"Sneak Attack":"ataque_furtivo"` hasta que `verificar_clases()`
    # (2026-09-03) empezó a contrastar esa misma columna por la escala del pack:
    # quitarla del MAPA dejó de dejarla sin mirar, así que la mutación pasó a
    # decir la verdad —no hay hueco— en vez de a probar el censo. Se muda a
    # `enemigo_predilecto`, que hoy SOLO alcanza `verificar_srd.MAPA`.
    _sust(r, "verificar_srd.py", '"Favored Enemy":"enemigo_predilecto", ', '')
    return ("`verificar_srd.MAPA` pierde `enemigo_predilecto`, la única "
            "columna del Explorador que no contrasta ninguna escala: el "
            "contraste sigue en verde y esa columna ya no la mira nadie")


# ══ Promesas de cobertura que no se sostienen ═════════════════════════════

def p_promesa_a_chequeo_inexistente(r):
    _sust(r, "_verificacion/mutaciones_pg.py",
          'CHEQUEOS = ("validar_puntos_golpe",)',
          'CHEQUEOS = ("validar_puntos_de_golpe",)')
    return ("una suite que dice cubrir `validar_puntos_de_golpe`, que no "
            "existe: o se renombró el chequeo, o la promesa es falsa")


def p_promesa_sin_etiqueta(r):
    _sust(r, "_verificacion/mutaciones_pg.py",
          'CHEQUEOS = ("validar_puntos_golpe",)',
          'CHEQUEOS = ("validar_puntos_golpe", "validar_idiomas")')
    return ("una suite que se apunta `validar_idiomas` sin buscar nunca su "
            "etiqueta: declarar cobertura no es tenerla")


# ══ El manifiesto podrido ═════════════════════════════════════════════════

def m_declaracion_muerta(r):
    # Apuntaba a `columna:druida.forma_salvaje` hasta que `verificar_clases()`
    # cerró ese hueco contra las escalas del pack y el censo mismo marcó la
    # declaración como muerta. Se muda a una exención que sigue viva.
    _sust(r, MANIFIESTO, '  - unidad: "columna:barbaro.n"',
          '  - unidad: "columna:barbaro.nivel"')
    return ("una declaración que ya no corresponde a ninguna unidad: da por "
            "mirado lo que nadie mira, que es como empezaron los ocho")


def m_declaracion_borrada(r):
    # Apuntaba a `variable:velocidad` hasta que el bloque A2 cerró ese hueco
    # y borró su declaración —el censo mismo lo exigió, marcándola como
    # muerta—. Se muda a una exención que sigue viva.
    _sust(r, MANIFIESTO,
          '  - unidad: "modulo:materiales.py"\n',
          '  - unidad: "modulo:_nada.py"\n')
    return ("se borra la declaración de `modulo:materiales.py`: el módulo "
            "vuelve a salir SIN DECLARAR (y la declaración huérfana, como muerta)")


def m_comodin_en_exentas(r):
    _sust(r, MANIFIESTO, "exentas:\n",
          'exentas:\n  - unidad: "rasgo:*"\n    motivo: "por las bravas"\n')
    return ("un comodín en `exentas`: una unidad que NO debe alcanzarse se "
            "declara una a una, o el manifiesto se convierte en un perdón")


def m_exenta_y_pendiente(r):
    _sust(r, MANIFIESTO, "pendientes:\n",
          'pendientes:\n  - unidad: "columna:picaro.n"\n    bloque: "A2"\n'
          '    motivo: "a la vez que exenta"\n')
    return ("la misma unidad exenta y pendiente: no es una decisión, es no "
            "haberla tomado")


# ══ Controles negativos: NO deben saltar ══════════════════════════════════

def u_fichero_de_equipo_sin_clasificar(r):
    """Esta mutación **era un control negativo** hasta el 2026-09-05, con este
    comentario: *«un YAML en `equipo/`, que no es directorio de regla: no entra
    en el universo de la fila 1»*. Era falso, y el test fijaba el error como
    correcto: `equipo/armaduras.yaml` **sí** es fuente de efectos —de ahí salen
    la CA de las 12 armaduras, el escudo y el −3 m por Fuerza—, y `equipo`
    faltaba de `_DIRECTORIOS_DE_REGLA`, de donde el censo tomaba su universo.
    El guardián de «la cobertura se descubre» tenía el defecto que persigue,
    con una mutación que lo blindaba.

    Cambió de lista, no se borró: la propiedad que protegía sigue siendo real y
    la protege ahora `n_yaml_en_directorio_no_de_regla`, con un directorio que
    de verdad no es regla."""
    (r / "equipo" / "monturas.yaml").write_text("monturas: []\n", encoding="utf-8")
    return ("un YAML nuevo en `equipo/`, que es directorio de regla PENDIENTE: "
            "la deuda enumerada no lo cubre y sale sin declarar")


def u_directorio_nuevo_sin_declarar(r):
    """**La mutación que habría cazado el defecto original.** Un directorio
    entero de `.yaml` que nadie ha clasificado no puede pasar en silencio: es
    exactamente lo que le pasó a `equipo/` durante toda su vida."""
    (r / "objetos").mkdir()
    (r / "objetos" / "varas.yaml").write_text("varas: []\n", encoding="utf-8")
    return ("un directorio nuevo (`objetos/`) con un `.yaml`, sin declarar en "
            "`fuentes_de_efectos.yaml → directorios`")


def m_clasificacion_de_equipo_muerta(r):
    """Una declaración que apunta a un fichero borrado: da por mirado lo que
    ya no existe y sube el recuento. Fase 0 aplicada a `equipo/`.

    Nació el 2026-09-05 apuntando a `directorios.pendientes.ficheros`, la lista
    con la que `equipo/` entró como deuda declarada. La fase 2.4 vació esa
    lista —`municion.yaml` ya lo valida `validar_equipo`— y el fichero pasó a
    `excluidos` con su motivo. La mutación sigue siendo la misma y sigue
    cazando: lo que cambió es qué declaración se queda muerta."""
    (r / "equipo" / "municion.yaml").unlink()
    return ("un fichero de `equipo/` clasificado en el manifiesto que ya no "
            "existe: declaración muerta")


def u_constante_de_dominio_nueva(r):
    """Fila 9 (fase 3). Un literal de Python cuyas cadenas son TODAS
    vocabulario de una colección de la base es autoridad duplicada, y tiene
    que salir aunque nadie lo haya puesto en la lista."""
    p = r / "buscar.py"
    t = p.read_text(encoding="utf-8")
    p.write_text(t + '\n\n_INVENTADA = ("Bardo", "Clérigo", "Druida", "Mago")\n',
                 encoding="utf-8")
    return ("un literal nuevo en Python con cuatro nombres de clase, que no "
            "está en `constantes_de_dominio.json`")


def u_constante_dentro_de_funcion(r):
    """Si solo se miraran las constantes de módulo, meter el literal dentro de
    una función lo haría desaparecer del censo."""
    p = r / "buscar.py"
    t = p.read_text(encoding="utf-8")
    p.write_text(t + '\n\ndef _inventada():\n'
                     '    return ("Bardo", "Clérigo", "Druida", "Mago")\n',
                 encoding="utf-8")
    return "el mismo literal, pero DENTRO de una función"


def u_declaracion_de_constante_desfasada(r):
    """El diente del `subconjunto`: si la colección crece, el `deja_fuera` de
    la declaración deja de cuadrar y alguien tiene que decidir si lo nuevo
    entra también en el literal. Hoy nada más hace esa pregunta.

    **Cambió de vehículo el 2026-09-06, no de chequeo.** Apuntaba a la
    condición nueva contra el literal de las seis condiciones que
    `estado_de_equipo()` llevaba escrito; la fase 4 derivó ese literal, así que
    la mutación se quedó sin nada que mover — que es el final bueno para una
    constante, y el malo para su prueba. Se traslada al literal de claves que
    `cargar_vocabulario()` EXIGE, que sigue vivo y sigue siendo un subconjunto
    declarado: si `reglas/efectos.yaml` gana una clave de primer nivel, alguien
    tiene que decidir si también se exige.
    """
    p = r / "reglas/efectos.yaml"
    t = p.read_text(encoding="utf-8")
    p.write_text(t + '\nbloque_nuevo:\n  algo: "prueba"\n', encoding="utf-8")
    return ("una clave de primer nivel NUEVA en `reglas/efectos.yaml`: el "
            "literal que `cargar_vocabulario()` exige la deja fuera y su "
            "declaración ya no cuadra")


def n_literal_que_no_es_de_la_base(r):
    """CONTROL NEGATIVO: un literal de tres cadenas que NO son vocabulario del
    juego no es una constante de dominio. Si saltara, la fila obligaría a
    declarar cualquier tupla de texto y el manifiesto se llenaría de ruido."""
    p = r / "buscar.py"
    t = p.read_text(encoding="utf-8")
    p.write_text(t + '\n\n_COLORES = ("rojo", "verde", "azul", "amarillo")\n',
                 encoding="utf-8")
    return "un literal de cuatro cadenas que no son vocabulario de la base"


def n_constante_movida_de_linea(r):
    """CONTROL NEGATIVO: la huella es el CONJUNTO, no la línea. Editar por
    encima de un literal no puede invalidar el fichero de declaraciones — la
    lección que `verificar_chequeos.py` aprendió con las gemelas."""
    p = r / "buscar.py"
    t = p.read_text(encoding="utf-8")
    i = t.index("\n", t.index("import"))
    p.write_text(t[:i] + "\n# " + "\n# ".join(["empuje"] * 12) + t[i:],
                 encoding="utf-8")
    return "doce líneas de comentario que desplazan todos los literales del módulo"


def n_rasgo_no_automatizado(r):
    _sust(r, "clases/rasgos/picaro.yaml", "rasgos:\n",
          'rasgos:\n  - nombre: "Reflejos de sombra"\n    nivel: 1\n'
          '    descripcion: "Texto de prueba."\n    no_automatizado: "no toca '
          'ninguna variable calculable"\n')
    return ("un rasgo nuevo que declara `no_automatizado`: esa ES la respuesta "
            "legítima del bloque D, no un hueco")




def n_yaml_en_directorio_no_de_regla(r):
    """SUSTITUTO del control negativo que se invirtió (ver
    `u_fichero_de_equipo_sin_clasificar` en DEBEN). La propiedad que aquel
    control codificaba —**no todo `.yaml` del repositorio es una regla**— es
    verdadera y hay que seguir protegiéndola; lo que era falso es que
    `equipo/` fuera el ejemplo."""
    (r / "personajes" / "prueba.yaml").write_text("nombre: x\n", encoding="utf-8")
    return ("un YAML en `personajes/`, declarado «no es regla» con su motivo: "
            "no entra en el universo de la fila 1")


def n_columna_ya_contrastada(r):
    _sust(r, "clases/picaro.yaml", 'ataque_furtivo: "1d6"', 'ataque_furtivo: "2d6"')
    return ("cambiar el VALOR de una columna ya contrastada: eso lo rompe "
            "`verificar_srd.py`, no el censo (el censo cuenta cobertura, no calidad)")


def n_suite_sin_chequeos(r):
    (r / "_verificacion" / "mutaciones_experimento.py").write_text(
        '"""Suite nueva que todavía no cubre ningún `validar_*`."""\n',
        encoding="utf-8")
    return ("una suite de mutación sin `CHEQUEOS`: no promete nada, así que no "
            "hay promesa que romper")


def n_exencion_con_motivo(r):
    _sust(r, "clases/picaro.yaml", "ataque_furtivo:", "esquiva_asombrosa: 1, ataque_furtivo:")
    _sust(r, MANIFIESTO, "pendientes:\n",
          'pendientes:\n  - unidad: "columna:picaro.esquiva_asombrosa"\n'
          '    bloque: "A2"\n    motivo: "columna nueva, sin fuente externa que '
          'la publique"\n')
    return ("la MISMA columna nueva, pero declarada con su bloque y su motivo: "
            "para eso está el manifiesto")


def u_rebanada_estrechada(r):
    """La rebanada existe desde el 2026-09-03: `paquete(c, t, sub=...)` promete
    UNA subcarpeta del pack y no el `type` entero. Si el censo no leyera el
    `sub=`, un módulo podría cambiar de rebanada y las 159 unidades que dejó de
    mirar seguirían contadas como alcanzadas."""
    _sust(r, "verificar_foundry.py",
          'paquete("classes24", "feat", sub="class-features")',
          'paquete("classes24", "feat", sub="metamagic-options")')
    return ("`verificar_rasgos_clase` cambia de rebanada: los 159 rasgos de "
            "clase salen del contraste y el módulo sigue pidiendo el mismo pack")


def u_rebanada_nueva(r):
    (r / "_verificacion" / "foundry_srd52" / "classes24" / "barbarian"
     / "class-features-2").mkdir(parents=True)
    (r / "_verificacion" / "foundry_srd52" / "classes24" / "barbarian"
     / "class-features-2" / "inventado.yml").write_text(
        "_id: xxx\nname: Made Up\ntype: feat\nsystem: {}\n", encoding="utf-8")
    return ("una rebanada nueva en el pack: nadie la pide y el censo la tiene "
            "que ver como unidad propia, no diluida en `classes24/feat`")


def m_excluido_muerto(r):
    """El manifiesto del CENSO no podía pudrirse; los de las FILAS sí.

    `Fila.declaradas` no se intersecaba con el universo, y `main()` imprime
    `len(alcanzadas) + len(declaradas)`: una declaración de
    `reglas/fuentes_de_efectos.yaml` que ya no correspondiera a ningún
    fichero **subía el recuento** sin cubrir nada, y `muertas` no la veía
    porque solo recorría `censo_exenciones.yaml`. Es el defecto de la regla 6
    dentro del script que la comprueba (auditoría del 2026-09-05).

    Ojo: NO vale renombrar un excluido existente —eso deja un fichero sin
    clasificar y `origenes()` ya falla en cerrado por ese otro camino—. El
    caso que nadie cazaba es la declaración que apunta a lo que no existe."""
    _sust(r, "reglas/fuentes_de_efectos.yaml", "excluidos:\n",
          'excluidos:\n  - ruta: "clases/inexistente.yaml"\n'
          '    motivo: "fichero que ya no existe"\n')
    return ("un `excluidos:` que apunta a un fichero inexistente: da por "
            "mirado lo que nadie mira, y encima sube el recuento")


def m_deuda_rehecha(r):
    """**Esta mutación CAMBIÓ DE VEHÍCULO el 2026-09-06, no de chequeo.**

    Era `m_deuda_muerta`: añadía a mano un uid obsoleto a
    `rasgos_sin_declarar.json` y exigía que el censo lo cazara, porque hasta la
    fase 1 del PLAN_21 esa fila NO PODABA y una entrada inventada se quedaba
    ahí inflando la lista en silencio. Con `deuda.Deuda` la fila poda: la
    entrada muerta sale sola en la pasada siguiente, se anuncia como saldada, y
    el recuento no se mueve. Medido: el censo sigue en 938 · 0 sin declarar.
    O sea, **la premisa dejó de ser cierta porque el defecto se cerró**, y
    borrar la mutación para que cuadre la cuenta es exactamente lo que este
    proyecto tiene prohibido. La propiedad «una entrada muerta no se queda»
    la prueba ahora el escenario `poda` de `mutaciones_deuda.py`, donde vive.

    Lo que el censo SÍ sigue teniendo que impedir es la otra dirección, que es
    peor y no la miraba nadie: **rehacer la línea base desde cero**. Si el
    fichero no está, `Deuda` lo escribe con lo medido HOY, y los 480 rasgos sin
    declarar pasarían a ser deuda «declarada» de golpe, en verde. Por eso
    `fila_rasgos` exige que exista antes de contrastar nada."""
    (r / "_verificacion/rasgos_sin_declarar.json").unlink()
    return ("se borra el fichero de deuda: sin él la línea base se rehace con "
            "lo medido hoy y 480 rasgos sin declarar quedan «declarados»")


# ══ Fila 10 · guardianes con guardián (fase 3 del PLAN_21) ═══════════════

def u_script_nuevo_sin_guardian(r):
    """Un `.py` nuevo en la raíz al que nadie puede corromperle el código.

    Es la puerta que la fila cierra: hasta el 2026-09-06 se podía añadir un
    verificador entero y **ninguna cuenta se movía**. Los seis guardianes que
    se cazaron a sí mismos en el PLAN_20 entraron así, uno detrás de otro.
    """
    (r / "verificar_inventado.py").write_text(
        "#!/usr/bin/env python3\n"
        '"""Un verificador nuevo que nadie muta."""\n'
        "def verificar_algo():\n"
        "    return 'algo', [], []\n", encoding="utf-8")
    return ("un script nuevo en la raíz que ninguna suite corrompe: se le "
            "puede meter un fallo y todo sigue en verde")


def m_suite_deja_de_mutar_el_script(r):
    """La otra dirección: la suite sigue ahí y en verde, pero ya no toca el
    código que decía guardar.

    Se elige `deuda.py` a propósito, porque `mutaciones_deuda` es su ÚNICO
    guardián. La primera versión de esta mutación quitaba a
    `mutaciones_silencios` de `validar.py`, y no se detectaba: `validar.py`
    también lo muta `mutaciones_muro`, así que seguía guardado. Una mutación
    que quita uno de dos guardianes no prueba nada.
    """
    _sust(r, "_verificacion/mutaciones_deuda.py",
          '"deuda.py"', '"reglas/efectos.yaml"', cuenta=99)
    return ("una suite que deja de mutar el CÓDIGO que decía guardar y pasa a "
            "mutar la base: sigue en verde y deja de ser un guardián")


def n_suite_que_solo_muta_la_base(r):
    """Control negativo, y es el que da sentido a la fila: mutar la base NO
    cuenta como guardar código. `mutaciones_prerrequisitos` es exactamente eso
    —10/10, en verde, y sin tocar una línea de `prerrequisitos.py`—, así que si
    el censo lo contara como guardián, `prerrequisitos.py` saldría cubierto sin
    estarlo. Aquí se añade otra suite del mismo tipo y el censo NO puede
    inmutarse."""
    (r / "_verificacion" / "mutaciones_inventadas.py").write_text(
        "#!/usr/bin/env python3\n"
        '"""Muta la base, no el código."""\n'
        "import pathlib\n"
        "def _sust(raiz, rel, viejo, nuevo):\n"
        "    p = raiz / rel\n"
        "    p.write_text(p.read_text().replace(viejo, nuevo))\n"
        "def m_algo(r):\n"
        '    _sust(r, "clases/picaro.yaml", "Pícaro", "Pícara")\n',
        encoding="utf-8")
    return ("una suite nueva que muta solo la BASE: no convierte en guardado "
            "ningún script de la raíz")


def u_efecto_nuevo_sin_carga(r):
    """Fila 8 (auditoría, fase 1.3). Un efecto nuevo en la base entra en el
    universo, y como ninguna ficha con lectura independiente lo sostiene ni
    está en `efectos_sin_carga.json`, sale SIN DECLARAR. Es la puerta que la
    fila cierra: la deuda enumerada solo puede bajar.

    **Cambió de vehículo el 2026-09-06, no de chequeo.** Colgaba de «Furia»,
    del Bárbaro, y el día que la fila 8 llegó a 25/25 hubo un Bárbaro con
    lectura independiente que la sostenía: el efecto nuevo pasaba a estar
    alcanzado y la mutación dejaba de demostrar nada. Cuelga ahora de un rasgo
    de **Brujo**, que es una de las cuatro clases sin ficha promovida —Brujo,
    Guerrero, Mago y Pícaro—. Si algún día se promueve un Brujo, esta mutación
    volverá a callarse y habrá que mudarla otra vez: queda dicho aquí para que
    la próxima no parezca un fallo del censo.
    """
    p2 = r / "clases/rasgos/brujo.yaml"
    t = p2.read_text(encoding="utf-8")
    viejo = '  - nombre: "Magia del pacto"\n'
    assert viejo in t, "el rasgo del que cuelga esta mutación ya no existe"
    t = t.replace(viejo,
                  viejo
                  + '    efectos:\n'
                    '      - {objetivo: velocidad, op: add, formula: "1",\n'
                    '         pagina: {pdf: 74, libro: 72}}\n', 1)
    p2.write_text(t, encoding="utf-8")
    return ("un efecto NUEVO en la base que ninguna ficha sostiene y que no "
            "está en la deuda enumerada")


DEBEN = [u_fichero_de_regla, u_variable_calculable, u_columna_de_clase,
         u_chequeo_nuevo, u_dato_externo, a_mapa_recortado,
         p_promesa_a_chequeo_inexistente, p_promesa_sin_etiqueta,
         m_declaracion_muerta, m_declaracion_borrada, m_comodin_en_exentas,
         m_exenta_y_pendiente, u_rasgo_nuevo,
         u_rebanada_estrechada, u_rebanada_nueva,
         m_excluido_muerto, m_deuda_rehecha,
         u_efecto_nuevo_sin_carga,
         u_script_nuevo_sin_guardian, m_suite_deja_de_mutar_el_script,
         u_fichero_de_equipo_sin_clasificar, u_directorio_nuevo_sin_declarar,
         m_clasificacion_de_equipo_muerta,
         u_constante_de_dominio_nueva, u_constante_dentro_de_funcion,
         u_declaracion_de_constante_desfasada]
NO_DEBEN = [n_rasgo_no_automatizado, n_yaml_en_directorio_no_de_regla,
            n_columna_ya_contrastada, n_suite_sin_chequeos, n_exencion_con_motivo,
            n_literal_que_no_es_de_la_base, n_constante_movida_de_linea,
            n_suite_que_solo_muta_la_base]
# Mutaciones que NO deben hacer fallar al censo pero SÍ subir su recuento.
# Quedó vacía al cerrar el bloque D: la única que había —el rasgo nuevo— ahora
# tiene que fallar, no solo contarse. Se conserva el mecanismo porque la fila
# de los rasgos no será la última deuda enumerada que aparezca.
CUENTAN = []


def _censo_falla(raiz):
    res = subprocess.run([sys.executable, "censo.py"], cwd=raiz,
                         capture_output=True, text=True)
    return res.returncode != 0, res.stdout + res.stderr


def _cuenta_censada(salida):
    for ln in salida.splitlines():
        if "unidades censadas" in ln:
            return ln.strip()
    return None


def _numero_censado(salida):
    linea = _cuenta_censada(salida) or ""
    for trozo in linea.split():
        if trozo.isdigit():
            return int(trozo)
    return None


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    return raiz


def main():
    print(__doc__.split("\n\n")[0])
    print("═" * 74)

    falla, salida = _censo_falla(BASE)
    if falla:
        print("✗ CONTROL: el censo ya falla con la base intacta. Arréglalo "
              "antes de mutar.")
        print(salida[-2500:])
        return 1
    print(f" ✅ control · la base intacta pasa el censo — {_cuenta_censada(salida)}")
    # Se guarda AQUÍ, antes de los bucles: `salida` se reasigna en cada
    # mutación, y tomar la línea base al final comparaba el recuento con el de
    # la última mutación en vez de con el de la base. Daba «682 → 682» y un
    # rojo que hablaba de esta suite, no del censo.
    base_n = _numero_censado(salida)

    ok = 0
    print("\n Mutaciones que DEBEN salir por el censo")
    for mut in DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            salta, _ = _censo_falla(raiz)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("        ↑ NO DETECTADA — el censo no cubre este caso")

    print("\n Controles negativos: NO deben salir")
    for mut in NO_DEBEN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            salta, salida = _censo_falla(raiz)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — obliga a declarar ruido")

    print("\n Mutaciones que NO deben fallar pero SÍ subir el recuento")
    for mut in CUENTAN:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            desc = mut(raiz)
            falla, sal = _censo_falla(raiz)
            n = _numero_censado(sal)
            bien = (not falla) and n is not None and n > base_n
            ok += bool(bien)
            print(f"   {'✅' if bien else '❌'} {desc}")
            print(f"        censadas: {base_n} → {n}"
                  + ("" if not falla else "  · y además el censo falló, que aquí no toca"))

    total = len(DEBEN) + len(NO_DEBEN) + len(CUENTAN)
    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
