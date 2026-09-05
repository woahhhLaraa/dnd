#!/usr/bin/env python3
"""Verificador de trazabilidad de una ficha en personajes/<nombre>.yaml.

No es un validador de reglas nuevas: comprueba que la ficha respeta el
contrato de personajes/_ESQUEMA.md — que todo dato mecánico es una
REFERENCIA a un registro real de la base, y que el bloque `calculado` es
justo lo que `calculo.py` produciría a partir del resto de la ficha. Una
ficha que pase este script no puede sostenerse en la palabra del LLM: todo
lo que dice es trazable.

Alcance actual: personajes de una sola clase, de nivel 1 a 20.

**La multiclase se RECHAZA, no se avisa (2026-09-02, fase 1 del PLAN_19).**
Hasta hoy **cuatro** chequeos se degradaban a aviso cuando la ficha traía más
de una clase —la recomputación de `calculado`, la justificación de las mejoras
de característica, el recuento de conjuros y las dotes y subclases— y la ficha
terminaba imprimiendo
«✅ FICHA VERIFICADA — 0 problemas». Es decir: el verificador aprobaba lo que
no había comprobado, que es el peor resultado posible de los tres:

  · rechazarla dice la verdad y no cuesta nada;
  · comprobarla de verdad es la fase 6 del plan;
  · **aprobarla sin mirar enseña a confiar en un ✅ que no significa nada.**

El cuarto era el más feo: se saltaba los tres huecos que el estrés con agentes
había destapado —la subclase de otra clase, el prerrequisito de dote sin
comprobar—, así que una ficha multiclase esquivaba en silencio los chequeos
escritos para cazar lo que se colaba en silencio.

Es el tercer caso confirmado de la amenaza nº 3 del `FODA.md` —«una rama de
tolerancia en un chequeo es deuda invisible»—, y los dos anteriores costaron
semanas: `COSTE_COMPUESTO` escondía dos sumas inventadas, y un `continue` dejó
que nueve de diecisiete fichas violaran la regla 6 de su propio esquema.

Uso: python3 verificar_personaje.py personajes/aerin.yaml
"""
import functools
import pathlib
import re
import sys

import calculo
import efectos
import buscar
from calculo import cargar


class Informe:
    def __init__(self):
        self.errores = []
        self.avisos = []
        # Cuántas afirmaciones se han contrastado de verdad. No es decoración:
        # un chequeo que no suma aquí es un chequeo que no miró nada, y esa
        # diferencia —entre «pasó» y «no se comprobó»— es la que este proyecto
        # lleva persiguiendo desde el principio.
        self.comprobados = 0

    def error(self, msg):
        self.errores.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)


# Los tres chequeos que no saben multiclase comparten esta puerta. Se dice
# UNA vez, no tres: repetir el mismo error por cada chequeo que se salta
# entierra el motivo real bajo su propio ruido.
_MOTIVO_MULTICLASE = (
    "MULTICLASE: esta ficha declara {n} clases y este verificador solo sabe "
    "comprobar una. NO se recomputa `calculado`, NO se justifican las mejoras "
    "de característica, NO se cuentan los conjuros contra la tabla y NO se "
    "comprueban ni los prerrequisitos de las dotes ni que la subclase sea de "
    "su clase. Hasta el "
    "2026-09-02 esto era un aviso y la ficha pasaba con «0 problemas»: el "
    "verificador aprobaba lo que no había mirado. Las reglas están transcritas "
    "y citadas en `reglas/generacion_personaje.yaml → multiclase`; "
    "automatizarlas es la fase 6 del PLAN_19.")


def una_sola_clase(ficha, inf):
    """¿Puede este verificador responder por esta ficha? Si no, lo dice."""
    n = len(ficha.get("clases") or [])
    if n == 1:
        return True
    if not any(s.startswith("MULTICLASE:") for s in inf.errores):
        inf.error(_MOTIVO_MULTICLASE.format(n=n))
    return False


# ── Resolución de referencias ────────────────────────────────────────────
def resolver_ref(ref, inf):
    """`ref` tiene forma 'archivo.yaml#Nombre' o 'archivo.yaml#seccion#Nombre'.
    Devuelve True si resuelve a un registro real; si no, registra el error
    y devuelve False. No lanza: una ficha con una ref rota debe reportarse
    junto al resto de problemas, no abortar en la primera."""
    partes = ref.split("#")
    archivo = partes[0]
    nombre = partes[-1]

    try:
        if archivo.startswith("especies/"):
            buscar.especie(nombre)
        elif archivo.startswith("trasfondos/"):
            buscar.trasfondo(nombre)
        elif archivo == "hechizos.json":
            buscar.conjuro(nombre)
        elif archivo.startswith("equipo/"):
            # Se pasa `archivo` para desambiguar nombres repetidos entre
            # ficheros de equipo/ (p. ej. "Bastón": arma vs. canalizador
            # arcano) — sin esto, una ref mal apuntada "verificaría" citando
            # el objeto equivocado en silencio.
            buscar.equipo(nombre, archivo=archivo)
        elif archivo.startswith("dotes/"):
            buscar.dote(nombre)
        elif archivo.startswith("clases/subclases/"):
            clase_archivo = archivo.split("/")[-1]
            d = cargar(f"clases/subclases/{clase_archivo}")
            if not any(s["nombre"] == nombre for s in d.get("subclases", [])):
                raise SystemExit(f"✗ subclase {nombre!r} no está en {archivo}")
        elif archivo.startswith("clases/"):
            # "clases/<clase>.yaml" (ref directa a la clase, sin "#") o
            # "clases/<clase>.yaml#<rasgo>" (ref a un rasgo del tronco):
            # en ambos casos basta con que el fichero de clase exista.
            cargar(archivo)
        else:
            inf.error(f"ref con prefijo no reconocido: {ref!r}")
            return False
    except SystemExit as e:
        inf.error(f"ref rota: {ref!r} ({e})")
        return False
    return True


def _recorrer_refs(nodo, inf, contador):
    if isinstance(nodo, dict):
        if "ref" in nodo and isinstance(nodo["ref"], str):
            contador[0] += 1
            resolver_ref(nodo["ref"], inf)
        for v in nodo.values():
            _recorrer_refs(v, inf, contador)
    elif isinstance(nodo, list):
        for v in nodo:
            _recorrer_refs(v, inf, contador)


# ── Categorías de armas/armaduras/herramientas ────────────────────────────
def _norm_cat(s):
    """Un nombre de categoría, comparable: se le quitan los espacios de sobra
    y la capitalización, que no son dato. Las tildes se quedan."""
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def verificar_categorias(ficha, inf):
    """`competencias.armas/armaduras/herramientas` van como texto literal de
    categoría (no `ref:` a equipo/ — esas categorías no son registros
    individuales ahí). Se comprueba que cada una esté en lo que conceden las
    clases del personaje, y —solo para `herramientas`, que es el único
    campo que un trasfondo puede otorgar— también el trasfondo.

    (Bug real hallado en la ronda 2 de pruebas: la versión anterior solo
    miraba las clases. Lo confirmaron 5 de 5 agentes de forma independiente
    — Explorador/Vagabundo, Guerrero/Guardia, Paladín/Marinero,
    Monje/Ermitaño, Druida/Guía — cada uno con una herramienta de trasfondo
    legítima rechazada por el verificador.)"""
    comp = ficha.get("competencias", {})
    tf_herramienta = None
    tf_abierta = False
    if ficha.get("trasfondo", {}).get("ref"):
        nombre_tf = ficha["trasfondo"]["ref"].split("#")[-1]
        tf = buscar.trasfondo(nombre_tf)
        tf_herramienta = tf.get("herramienta")
        if tf_herramienta and tf_herramienta.strip().lower().startswith("elige"):
            tf_abierta = True  # "elige un tipo de juego/instrumento/..."

    for campo in ("armas", "armaduras", "herramientas"):
        entradas = comp.get(campo, [])
        permitidas = set()
        for c in ficha.get("clases", []):
            clase_d = buscar.clase(c["clase"])
            permitidas |= set(clase_d.get("atributos_basicos", {}).get(campo, []))
        if campo == "herramientas" and tf_herramienta and not tf_abierta:
            permitidas.add(tf_herramienta)
        for e in entradas:
            if not isinstance(e, dict) or "categoria" not in e:
                # ⛔ AQUÍ HABÍA UNA RAMA DE TOLERANCIA, y es la causa raíz de que
                # nueve de las diecisiete fichas violaran la regla 6 durante
                # semanas sin que nada lo dijera. Decía:
                #
                #     continue  # entradas antiguas con `ref:` las cubre _recorrer_refs
                #
                # Era razonable cuando se escribió: el esquema **antes exigía
                # `ref:`**, cambió a `categoria:` (ver FUENTES.md, la corrección
                # de la ronda 2 de pruebas), y esta rama dejaba convivir los dos
                # formatos mientras se migraban las fichas. **La migración nunca
                # ocurrió**, porque nada la reclamaba: la rama hacía el desfase
                # invisible y por tanto permanente. Y las fichas viejas
                # enseñaron el formato viejo a todo el que vino después.
                #
                # Hoy la forma la exige `verificar_forma_competencias()`. Esto
                # se queda como error para que no haya dos sitios donde tolerar
                # lo mismo.
                inf.error(f"competencias.{campo}: entrada sin `categoria` "
                          f"({e!r}). La regla 6 del esquema no admite `ref`")
                continue
            if campo == "herramientas" and tf_abierta:
                # TOLERADO: el trasfondo dice «elige un tipo de …», así que no
                # hay lista contra la que contrastar. Lo cubre el propio
                # `atributos_basicos`/`trasfondos.yaml`, que declara la apertura.
                continue
            cat = e["categoria"]
            # La comparación NORMALIZA MAYÚSCULAS, y eso es afinar el chequeo,
            # no relajarlo: la capitalización de un nombre de categoría es
            # ortografía, no dato. La base misma es inconsistente —
            # `trasfondos.yaml` guarda «suministros de calígrafo» en minúscula
            # y `clases/*.yaml` guarda «Armaduras ligeras» con mayúscula—, así
            # que una ficha que escribiera la herramienta con la mayúscula
            # natural del castellano se rechazaba contra una lista que la
            # contenía. Lo destapó la ronda 2 de estrés (agente A, 3 fichas).
            #
            # Las TILDES no se normalizan a propósito: en castellano sí son
            # dato, y este proyecto ya perdió tiempo con la tilde de `Clérigo`.
            if _norm_cat(cat) not in {_norm_cat(p) for p in permitidas}:
                inf.error(f"competencias.{campo}: {cat!r} no está en lo que "
                          f"conceden las clases (ni el trasfondo, si aplica) "
                          f"del personaje ({sorted(permitidas)})")


# ── Habilidades permitidas ────────────────────────────────────────────────
def verificar_habilidades(ficha, inf):
    comp = ficha.get("competencias", {})
    elegidas = {h["nombre"] for h in comp.get("habilidades", [])}
    if not elegidas:
        return

    permitidas = set()
    cualesquiera = False

    for c in ficha.get("clases", []):
        clase_d = buscar.clase(c["clase"])
        hab = clase_d.get("atributos_basicos", {}).get("habilidades", {})
        permitidas |= set(hab.get("de", []))
        if hab.get("cualesquiera"):
            cualesquiera = True

    if ficha.get("trasfondo", {}).get("ref"):
        nombre_tf = ficha["trasfondo"]["ref"].split("#")[-1]
        tf = buscar.trasfondo(nombre_tf)
        permitidas |= set(tf.get("habilidades", []))

    # Algunas especies conceden competencia en habilidad por un rasgo (p. ej.
    # Elfo → "Sentidos agudos": Percepción, Perspicacia o Supervivencia;
    # Humano → "Diestro": una habilidad de tu elección). No es un campo
    # estructurado en especies/especies.yaml, así que se detecta por texto.
    # (Bug real hallado en la ronda 2: Paladín/Elfo — Perspicacia era
    # legítima por "Sentidos agudos" y el verificador la rechazaba porque
    # solo miraba clase y trasfondo.)
    if ficha.get("especie", {}).get("ref"):
        nombre_esp = ficha["especie"]["ref"].split("#")[-1]
        esp = buscar.especie(nombre_esp)
        canonicas_18 = {h["nombre"] for h in cargar("reglas/habilidades.yaml")["habilidades"]}
        for r in esp.get("rasgos", []):
            desc = r.get("desc", "")
            if "Competencia en" not in desc:
                continue
            if "de tu elección" in desc or "cualquier habilidad" in desc:
                cualesquiera = True
            else:
                permitidas |= {h for h in canonicas_18 if h in desc}

    if cualesquiera:
        # "Cualesquiera" abre la lista a las 18 canónicas — NO a cualquier
        # string. Sigue habiendo una lista cerrada, solo que es más grande.
        # (bug real hallado en pruebas: esto devolvía antes sin comprobar
        # nada, y una habilidad inventada pasaba la verificación intacta.)
        canonicas = {h["nombre"] for h in cargar("reglas/habilidades.yaml")["habilidades"]}
        permitidas |= canonicas

    fuera = elegidas - permitidas
    if fuera:
        inf.error(f"habilidades elegidas fuera de lo permitido por clase/trasfondo: "
                  f"{sorted(fuera)}")


# ── Compra por puntos ────────────────────────────────────────────────────
def verificar_compra_puntos(ficha, inf):
    car = ficha.get("caracteristicas", {})
    if car.get("metodo") != "compra_puntos":
        return
    total = calculo.coste_compra_puntos(car["base"])
    # El presupuesto se LEE de la base (auditoría del 2026-09-03): era un `27`
    # cableado aquí mientras la tabla de coste del MISMO bloque del YAML ya se
    # leía, con un comentario encima explicando por qué había que leerla.
    presupuesto = calculo.puntos_totales()
    if total != presupuesto:
        inf.error(f"compra por puntos suma {total}, debería ser {presupuesto}")


# ── Recomputar `calculado` ────────────────────────────────────────────────
def verificar_calculado(ficha, inf):
    clases = ficha.get("clases", [])
    if not una_sola_clase(ficha, inf):
        return
    if clases[0]["nivel"] != ficha["nivel_total"]:
        inf.error(f"nivel_total {ficha['nivel_total']} no coincide con el nivel "
                  f"de la única clase ({clases[0]['nivel']})")
        return

    c = clases[0]
    clase_d = buscar.clase(c["clase"])
    ab = clase_d["atributos_basicos"]
    final = ficha["caracteristicas"]["final"]

    con_mod = calculo.modificador(final["con"])
    des_mod = calculo.modificador(final["des"])
    sab_mod = calculo.modificador(final["sab"])

    # FASE 14 · PG y CA los agrega ahora `efectos.py` a partir de efectos
    # citados junto a cada rasgo, no de casos cableados aquí.
    #
    # Lo que había antes, y por qué se va:
    #   · `bonus_pg_especie` — un campo de la ficha que el propio esquema
    #     admitía como parche porque "Aguante enano" era prosa. Cubría 1 de los
    #     2 efectos sobre PG máximos de la base (*Resistencia dracónica* del
    #     Hechicero no tenía dónde ponerse), guardaba un 1 fijo que solo es
    #     correcto en nivel 1 ("y en 1 más cada vez que subes de nivel"), y
    #     nadie obligaba a rellenarlo: la única ficha de Enano de la base lo
    #     tenía vacío y verificaba en verde con los PG mal.
    #   · `calculo.ca(clase=...)` — conocía 2 de las 4 fórmulas de CA base.
    mods = {"mod_" + k: calculo.modificador(v) for k, v in final.items()}
    # Los PG salen de la HISTORIA de la ficha, no de un escalar: cada nivel
    # posterior al 1 guarda si se tiró el dado o se usó el valor establecido, y
    # el total se recalcula entero desde esos valores crudos. Así la regla
    # retroactiva del modificador por Constitución (pdf 44, paso 5) sale sola.
    pg_base, avisos_pg = calculo.pg_max_de_ficha(ficha, con_mod, ab["dado_golpe"])
    for a in avisos_pg:
        inf.aviso(a)
    try:
        agregado = efectos.calcular_de_ficha(
            ficha, mods, calculo.bonificador_competencia(ficha["nivel_total"]),
            pg_base)
    except efectos.ErrorDeEfectos as e:
        inf.error(f"el motor de efectos no puede calcular esta ficha: {e}")
        return
    pg_esperado, ca_esperada = agregado["pg_max"], agregado["ca"]

    pb_esperado = calculo.bonificador_competencia(ficha["nivel_total"])

    calc = ficha.get("calculado", {})
    comprobaciones = [
        ("pg_max", pg_esperado),
        ("ca", ca_esperada),
        ("bonif_competencia", pb_esperado),
    ]
    # La velocidad entró en el motor con la deuda 4: es la primera variable que
    # se calcula leyendo una COLUMNA de la progresión («Movimiento sin
    # armadura» del Monje). Se comprueba en la ficha para que el efecto sea
    # carga y no decoración: si no lo sostuviera ninguna ficha, corromperlo no
    # rompería nada.
    if "velocidad" in agregado:
        comprobaciones.append(("velocidad", agregado["velocidad"]))

    if clase_d.get("lanzador") not in (None, "ninguno"):
        aptitud = clase_d["aptitud_magica"].lower()
        mapa = {"inteligencia": "int", "sabiduría": "sab", "carisma": "car"}
        clave = mapa.get(aptitud)
        if clave:
            apt_mod = calculo.modificador(final[clave])
            comprobaciones.append(("cd_conjuros", calculo.cd_conjuros(apt_mod, pb_esperado)))
            comprobaciones.append(("bonif_ataque_conjuros",
                                    calculo.bonif_ataque_conjuros(apt_mod, pb_esperado)))

    sobran = set(calc) - {c for c, _ in comprobaciones} - {"_origen"}
    if sobran:
        inf.error(f"`calculado` trae campos que el verificador no recalcula: "
                  f"{sorted(sobran)}. Un número en `calculado` que nadie "
                  f"contrasta es un número inventado")
    for campo, esperado in comprobaciones:
        real = calc.get(campo)
        if real != esperado:
            inf.error(f"calculado.{campo} = {real!r}, pero recalculado da {esperado!r}")


# ── De dónde sale el bloque `calculado` ──────────────────────────────────
# Fase 1.2 de la auditoría (2026-09-05). El problema que cierra es de forma,
# no de aritmética: la ficha se ESCRIBE con `calculo`/`efectos` (por
# `--calcular`) y se VERIFICA recalculando con `calculo`/`efectos`. El círculo
# está cerrado, así que un error del motor produce una ficha coherente y
# equivocada, y sale en verde. `mutaciones_motor.py` lo midió: 7 de 11 trozos
# del motor se pueden corromper sin que ninguna ficha se queje.
#
# Esto no arregla la aritmética —eso lo hace el mandato «el calculista» de la
# ronda 3 de estrés—, pero hace VISIBLE lo que hoy es invisible: si un número
# lo escribió el motor o una lectura independiente de la página.
#
# La regla dura, y es la que da sentido a todo: `calcular_bloque()` escribe
# SIEMPRE `metodo: motor` y NUNCA puede firmar `agente-manual`. Si el
# escritor puede firmar como oráculo, no hay oráculo.
_METODOS_DE_ORIGEN = ("motor", "agente-manual")


def verificar_origen_del_calculado(ficha, inf):
    calc = ficha.get("calculado")
    if not isinstance(calc, dict):
        # TOLERADO: la ausencia del bloque entero la caza `verificar_calculado`,
        # que lo compara campo a campo y saca un error por cada uno. Repetirlo
        # aquí daría dos mensajes para un solo defecto.
        return
    o = calc.get("_origen")
    if not isinstance(o, dict):
        inf.error("`calculado` no dice de dónde sale. Necesita `_origen` con "
                  "`metodo` (" + " | ".join(_METODOS_DE_ORIGEN) + "), porque "
                  "un número escrito por el motor y otro leído a mano de la "
                  "página no valen lo mismo")
        return
    metodo = o.get("metodo")
    if metodo not in _METODOS_DE_ORIGEN:
        inf.error(f"`calculado._origen.metodo` es {metodo!r} y solo vale "
                  f"{list(_METODOS_DE_ORIGEN)}")
        return
    if metodo == "agente-manual":
        informe = o.get("informe")
        if not informe:
            inf.error("`_origen.metodo: agente-manual` sin `informe:`. Un "
                      "número que dice venir de una lectura independiente "
                      "tiene que decir DÓNDE está esa lectura")
            return
        if not (pathlib.Path(__file__).parent / str(informe)).exists():
            inf.error(f"`_origen.informe` apunta a {informe!r} y ese fichero "
                      f"no existe: la derivación tiene que poder leerse")
            return
    inf.comprobados += 1


# ── Las mejoras de característica, que nadie justificaba ─────────────────
# Descubierto el 2026-08-30 al construir la primera ficha de nivel 20: un monje
# con **las seis características a 20** y ninguna justificación **verificaba en
# verde**. `caracteristicas.final` se escribía a mano y nada lo ataba a
# `base` + `ajuste_trasfondo` + las mejoras tomadas. En una base cuyo lema es
# que nada entra sin cita, era el hueco más grande que quedaba.
#
# La regla está entera en `dotes/generales.yaml#Mejora de característica`
# (pdf 209 = libro 207): «Aumenta en 2 una puntuación de característica de tu
# elección, o aumenta dos en 1 cada una. No puede superar 20», `repetible: true`.
_CARS = ("fue", "des", "con", "int", "sab", "car")


def _niveles_de_mejora(ficha):
    """Los niveles en que la tabla de la clase concede «Mejora de
    característica». Se leen de la progresión, no de una lista escrita a mano."""
    c = ficha["clases"][0]
    d = cargar(c["ref"].split("#")[0]) or {}
    return [f["n"] for f in d.get("progresion", [])
            if f["n"] <= c["nivel"]
            and any(calculo.es_marcador_de("mejora_caracteristica_o_dote", r)
                    for r in (f.get("rasgos") or []))]


# ── C3 del Plan 17: el +1 que concede una DOTE ───────────────────────────
# 54 de las 75 dotes conceden «Mejora de característica: X +1». Hasta el
# 2026-08-31 ese +1 no tenía dónde entrar: el esquema exigía
# `final == base + ajuste_trasfondo + mejoras`, y la dote no era ninguna de
# las tres. La consecuencia estaba INVERTIDA — la ficha correcta se rechazaba
# y la rota pasaba en verde con la CD y el ataque un punto por debajo.
#
# La dote declara QUÉ puede subir (`mejora_caracteristica.entre`, contrastado
# contra su propio texto por `validar_mejoras_de_dote`); la ficha declara QUÉ
# eligió (`sube:`), porque es una elección del jugador y el motor no puede
# deducirla. Es la misma división que ya usa `mejoras` para el nivel 4.
def _mejora_de_dote(ref):
    """`mejora_caracteristica` de la dote referenciada, o None."""
    archivo, _, nombre = ref.partition("#")
    d = cargar(archivo) or {}
    for x in d.get("dotes", []) or []:
        if x.get("nombre") == nombre:
            return x.get("mejora_caracteristica")
    return None


def _valida_reparto(quien, mej, sube, final, inf):
    """Comprueba un reparto `sube:` contra el `mejora_caracteristica` que la
    dote declara EN LA BASE.

    Es el ÚNICO camino, y eso es el punto. Foundry lo dejó escrito (ver
    `PLAN_17` §1.2): allí «una dote que sube una característica usa el MISMO
    mecanismo que la mejora de nivel 4», y por eso no se puede olvidar
    conectar uno de los dos. Aquí eran dos caminos — el de las dotes leía
    `mejora_caracteristica` de la base, y el de `mejoras:` llevaba el `+2` y
    el tope de 20 CABLEADOS—, y el segundo se desincronizó en silencio: la
    ronda 2 de estrés lo destapó cuando una dote con `maximo: 30` chocó
    contra un `> 20` de Python que ninguna página respaldaba.
    """
    cant, tope, entre = mej.get("cantidad"), mej.get("maximo"), mej.get("entre")
    valores = list(sube.values())
    # Las formas legales de repartir `cantidad` son sus particiones en partes
    # de 1 o más: con `cantidad: 1` solo cabe [1]; con 2, [2] y [1,1] — que es
    # exactamente lo que dice el texto de la dote genérica. No hace falta un
    # campo `reparto:` que lo repita, y en cambio SÍ hace falta exigir que
    # ninguna parte sea 0 o negativa: `{fue: 3, des: -1}` suma 2 y no es
    # ninguna de las dos formas.
    if (sum(valores) != cant
            or any(not isinstance(v, int) or v < 1 for v in valores)):
        inf.error(f"{quien} concede +{cant} y la ficha reparte {sube!r}: cada "
                  f"parte tiene que ser de 1 o más y sumar exactamente {cant}")
    for k in sube:
        if k not in _CARS:
            inf.error(f"{quien} sube {k!r}, que no es una característica")
            continue
        if isinstance(entre, list):
            permitidas = {_ABREV[c] for c in entre}
            if k not in permitidas:
                inf.error(f"{quien} solo permite subir {entre}, y la ficha "
                          f"sube {k!r}")
        valor = (final or {}).get(k)
        if isinstance(valor, int) and isinstance(tope, int) and valor > tope:
            inf.error(f"{quien} deja {k} en {valor} y su texto dice "
                      f"«máx. {tope}»")


def _subidas_por_dote(ficha, inf):
    """{caracteristica: total} que aportan las dotes de la ficha. Valida de
    paso que lo elegido sea una de las opciones que la dote permite."""
    total = {}
    for dt in ficha.get("dotes", []) or []:
        ref = dt.get("ref", "")
        mej = _mejora_de_dote(ref)
        nombre = ref.split("#")[-1]
        sube = dt.get("sube") or {}
        if not mej:
            if sube:
                inf.error(f"la dote «{nombre}» no concede mejora de "
                          f"característica y la ficha le pone `sube: {sube!r}`")
            continue
        if not sube:
            inf.error(f"la dote «{nombre}» concede una mejora de "
                      f"característica y la ficha no dice en qué la gastó. "
                      f"Añade `sube:` a esa dote (opciones: "
                      f"{mej.get('entre')})")
            continue
        final = (ficha.get("caracteristicas") or {}).get("final") or {}
        _valida_reparto(f"«{nombre}»", mej, sube, final, inf)
        for k, v in sube.items():
            total[k] = total.get(k, 0) + v
    return total


_ABREV = {"Fuerza": "fue", "Destreza": "des", "Constitución": "con",
          "Inteligencia": "int", "Sabiduría": "sab", "Carisma": "car"}


def verificar_mejoras(ficha, inf):
    if not una_sola_clase(ficha, inf):
        return
    car = ficha.get("caracteristicas") or {}
    base, ajuste = car.get("base") or {}, car.get("ajuste_trasfondo") or {}
    final = car.get("final") or {}
    mejoras = ficha.get("mejoras") or []
    por_dote = _subidas_por_dote(ficha, inf)

    # 1. La suma tiene que cuadrar, característica a característica.
    for k in _CARS:
        de_mejoras = sum((m.get("sube") or {}).get(k, 0) for m in mejoras)
        de_dotes = por_dote.get(k, 0)
        esperado = base.get(k, 0) + ajuste.get(k, 0) + de_mejoras + de_dotes
        if final.get(k) != esperado:
            inf.error(f"caracteristicas.final.{k} = {final.get(k)!r}, pero "
                      f"base {base.get(k)} + trasfondo {ajuste.get(k, 0)} + "
                      f"mejoras {de_mejoras} + dotes {de_dotes} "
                      f"= {esperado}. Una puntuación sin justificar es una "
                      f"puntuación inventada")

    # 2. Cada mejora reparte lo que dice LA DOTE QUE LA CONCEDE, leída de la
    #    base por el `ref:` de la propia entrada. Aquí vivía el defecto que
    #    destapó la ronda 2 de estrés: el `+2` y el tope de 20 estaban
    #    cableados con literales, y `dotes/generales.yaml#Mejora de
    #    característica` era la única de las 43 dotes sin
    #    `mejora_caracteristica` estructurado — justo la que el esquema
    #    designa para cada entrada de `mejoras:`. Ya lo trae, y este bucle lo
    #    lee por el mismo camino que las dotes.
    for m in mejoras:
        sube = m.get("sube") or {}
        ref = m.get("ref") or ""
        mej = _mejora_de_dote(ref)
        quien = f"la mejora de nivel {m.get('nivel')}"
        if not mej:
            inf.error(f"{quien} no dice de qué dote sale, o su `ref` no "
                      f"resuelve a una que conceda mejora de característica: "
                      f"{ref!r}. Sin eso no hay cantidad ni tope que aplicar "
                      f"—y cablearlos aquí fue el defecto que la ronda 2 de "
                      f"estrés destapó")
            continue
        _valida_reparto(quien, mej, sube, final, inf)

    # 3. Cada nivel con «Mejora de característica» tiene que estar gastado:
    #    o en una mejora, o en una dote tomada en ese nivel. Ni de más ni de
    #    menos — que sobren mejoras es tan defecto como que falten.
    niveles = _niveles_de_mejora(ficha)
    usados = {m.get("nivel") for m in mejoras}
    usados |= {(d.get("origen") or {}).get("nivel")
               for d in (ficha.get("dotes") or [])}
    for n in niveles:
        if n not in usados:
            inf.error(f"el nivel {n} concede «Mejora de característica» y la "
                      f"ficha no dice en qué se gastó (ni `mejoras` ni una dote "
                      f"con `origen.nivel: {n}`)")
    for n in sorted(x for x in usados if x is not None):
        if n not in niveles:
            inf.error(f"la ficha gasta una mejora en el nivel {n}, y la tabla "
                      f"de {ficha['clases'][0]['clase']} no concede ninguna ahí")


# ── Cuántos conjuros lleva la ficha, contra la tabla de la clase ─────────
# Otro hueco que salió al construir la primera ficha de nivel 20: **nadie
# contaba los conjuros**. Un mago de nivel 20 con dos trucos verificaba en
# verde, y varias fichas de nivel 1 llevaban más de los que concede su tabla.
#
# Los excesos resultaron estar todos justificados —dotes como «Iniciado en la
# magia», rasgos de especie, opciones de orden— pero **solo en la prosa de
# `decisiones`**, que ningún script lee. Se reutiliza la convención que el
# equipo ya usa: un conjuro con `origen:` es un extra y tiene que decir de
# dónde sale; uno sin `origen:` cuenta contra la tabla.
# Las fuentes de un conjuro EXTRA que este chequeo sabe reconocer. Vive como
# constante porque el mensaje de error la nombra: un origen que no esté aquí
# tiene que salir por pantalla con la lista de los que sí, no como un «no dice
# de qué sale» que parece culpa de la ficha cuando es un hueco del chequeo.
_ORIGENES_DE_CONJURO = ("dote", "especie", "rasgo", "trasfondo", "clase",
                        "subclase")


def _comprueba_conjuro_de_subclase(ficha, entrada, origen, clave, inf):
    """Un conjuro que dice venir de la subclase tiene que estar de verdad en
    la tabla `conjuros_siempre_preparados` de esa subclase, a un nivel que el
    personaje ya haya alcanzado."""
    c = ficha["clases"][0]
    sub_ref = (c.get("subclase") or {}).get("ref") if isinstance(c.get("subclase"), dict) else c.get("subclase")
    nombre_sub = str(origen.get("subclase") or "").strip()
    if not sub_ref:
        inf.error(f"conjuros.{clave}: {entrada.get('ref')!r} dice venir de la "
                  f"subclase {nombre_sub!r} y la ficha no declara subclase")
        return
    doc = cargar(str(sub_ref).split("#")[0]) or {}
    sub = next((x for x in (doc.get("subclases") or [])
                if x.get("nombre") == str(sub_ref).split("#")[-1]), None)
    if sub is None:
        return          # la ref rota la caza `_recorrer_refs`, no este chequeo
    if nombre_sub and nombre_sub != sub.get("nombre"):
        inf.error(f"conjuros.{clave}: {entrada.get('ref')!r} dice venir de "
                  f"{nombre_sub!r} y la subclase de la ficha es "
                  f"{sub.get('nombre')!r}")
        return
    tabla = sub.get("conjuros_siempre_preparados") or {}
    if not tabla:
        inf.error(f"conjuros.{clave}: {entrada.get('ref')!r} dice venir de la "
                  f"subclase {sub.get('nombre')!r}, y esa subclase no tiene "
                  f"tabla de conjuros siempre preparados en la base")
        return
    nombre_conj = str(entrada.get("ref") or "").split("#")[-1]
    concedidos = {}
    for niv, lista in tabla.items():
        for n in (lista or []):
            concedidos.setdefault(n, int(niv))
    if nombre_conj not in concedidos:
        inf.error(f"conjuros.{clave}: {nombre_conj!r} dice venir de "
                  f"{sub.get('nombre')!r} y no está en su tabla de conjuros "
                  f"siempre preparados ({sorted(concedidos)})")
        return
    exige = concedidos[nombre_conj]
    if c["nivel"] < exige:
        inf.error(f"conjuros.{clave}: {nombre_conj!r} lo concede "
                  f"{sub.get('nombre')!r} en el nivel {exige} y el personaje "
                  f"es de nivel {c['nivel']}")
        return
    declarado = origen.get("nivel")
    if declarado is not None and int(declarado) != exige:
        inf.error(f"conjuros.{clave}: {nombre_conj!r} declara `nivel` "
                  f"{declarado} y la tabla de {sub.get('nombre')!r} lo "
                  f"concede en el {exige}")
        return
    inf.comprobados += 1


def verificar_conjuros(ficha, inf):
    if not una_sola_clase(ficha, inf):
        return
    c = ficha["clases"][0]
    clase_d = cargar(c["ref"].split("#")[0]) or {}
    if clase_d.get("lanzador") in (None, "ninguno"):
        return
    fila = next((f for f in clase_d.get("progresion", []) if f["n"] == c["nivel"]), None)
    if fila is None:
        return
    conj = ficha.get("conjuros") or {}

    # Hueco nº 4 de la ronda 2: un conjuro puede estar en las DOS listas, y
    # entonces cuenta dos veces. No es hipotético — lo encontró el agente C en
    # una ficha de la propia base: `draconido_hechicero_n4.yaml` llevaba «Rayo
    # de escarcha» (nivel 0) en `trucos` y también en `preparados`, así que de
    # los 7 preparados que concede la tabla tenía 6 reales. El chequeo contaba
    # la LONGITUD de la lista sin mirar qué había dentro.
    vistos = {}
    for clave in ("trucos", "preparados"):
        for entrada in (conj.get(clave) or []):
            ref = str(entrada.get("ref") or "")
            nombre_c = ref.split("#")[-1]
            if not nombre_c:
                continue
            if nombre_c in vistos:
                inf.error(f"conjuros: {nombre_c!r} aparece en "
                          f"`{vistos[nombre_c]}` y otra vez en `{clave}`. Un "
                          f"conjuro repetido cuenta dos veces contra la tabla")
            else:
                vistos[nombre_c] = clave
    # Y el nivel tiene que corresponder con la lista en la que vive: los
    # trucos son de nivel 0 y los preparados de nivel 1 o más.
    for clave, nivel_esperado in (("trucos", 0), ("preparados", None)):
        for entrada in (conj.get(clave) or []):
            nombre_c = str(entrada.get("ref") or "").split("#")[-1]
            if not nombre_c:
                continue
            reg = buscar.conjuro(nombre_c)
            niv = reg.get("nivel")
            if nivel_esperado == 0 and niv != 0:
                inf.error(f"conjuros.trucos: {nombre_c!r} es de nivel {niv}, "
                          f"no es un truco")
            elif nivel_esperado is None and niv == 0:
                inf.error(f"conjuros.preparados: {nombre_c!r} es un truco "
                          f"(nivel 0) y está entre los preparados, donde "
                          f"infla el recuento de la tabla")
            else:
                inf.comprobados += 1

    for clave, columna in (("trucos", "trucos"), ("preparados", "prep")):
        esperado = fila.get(columna)
        if esperado is None:
            continue
        # Cuenta contra la tabla lo que viene del lanzamiento NORMAL de la
        # clase: sin `origen`, o con un `origen` que solo nombra la clase (y a
        # lo sumo su rasgo «Lanzamiento de conjuros»). Todo lo demás —una dote,
        # un rasgo de especie, una opción de orden, o cualquier entrada con
        # `nota` de «no cuenta contra el límite»— es un extra y ya venía
        # declarado así en las fichas.
        def _de_clase(s):
            o = s.get("origen")
            if not o:
                return True
            if "nota" in o:
                return False
            if set(o) - {"clase", "rasgo"}:
                return False
            if o.get("clase") != c["clase"]:
                return False
            return o.get("rasgo", "Lanzamiento de conjuros") == "Lanzamiento de conjuros"

        lista = conj.get(clave) or []
        de_clase = [s for s in lista if _de_clase(s)]
        extras = [s for s in lista if not _de_clase(s)]

        # Hueco nº 1 de la ronda 2 de estrés: se CONTABAN los conjuros contra
        # la tabla y no se miraba si eran de la clase. Un Hechicero con un
        # truco de Brujo/Clérigo/Mago verificaba en verde. Los 391 conjuros
        # traen `clases` en `hechizos.json`, así que la fuente estaba ahí
        # desde siempre — es el mismo mecanismo que ya usan armas, armaduras
        # y herramientas: reúne lo permitido, comprueba membresía.
        #
        # Solo se comprueban los que CUENTAN contra la tabla. Los extras no:
        # «Iniciado en la magia» concede conjuros de una lista ELEGIDA
        # (clérigo, druida o mago), que por diseño puede no ser la del
        # personaje, y un rasgo de especie o de subclase igual.
        for s_ in de_clase:
            nombre_c = str(s_.get("ref") or "").split("#")[-1]
            reg = buscar.conjuro(nombre_c) if nombre_c else None
            if not reg:
                # TOLERADO: una ref que no resuelve ya la caza `_recorrer_refs`,
                # que recorre TODAS las del fichero y falla ruidosamente. Aquí
                # solo se evita repetir el mismo error con otras palabras.
                continue
            suyas = reg.get("clases") or []
            if suyas and c["clase"] not in suyas:
                inf.error(f"conjuros.{clave}: {nombre_c!r} no es un conjuro de "
                          f"{c['clase']} (sus listas son {suyas}). Si viene de "
                          f"otra fuente, dilo con `origen:`")
            else:
                inf.comprobados += 1
        if len(de_clase) != esperado:
            inf.error(
                f"conjuros.{clave}: la tabla de {c['clase']} nivel {c['nivel']} "
                f"concede {esperado} y la ficha trae {len(de_clase)} sin "
                f"`origen` (más {len(extras)} declarados como extra). Un "
                f"conjuro de más sin fuente es un conjuro inventado")
        for s in extras:
            o = s.get("origen") or {}
            if not any(k in o for k in _ORIGENES_DE_CONJURO):
                inf.error(f"conjuros.{clave}: {s.get('ref')!r} declara `origen` "
                          f"sin decir de qué sale: {o!r}. Fuentes que este "
                          f"chequeo sabe reconocer: {sorted(_ORIGENES_DE_CONJURO)}")
                continue
            # `subclase` no estaba en la lista, y era un FALSO POSITIVO de los
            # que más duelen: los conjuros de dominio del Clérigo —declarados
            # exactamente como manda el esquema— se rechazaban uno a uno. Lo
            # destapó la ronda 2 de estrés (agente B, ficha 2).
            #
            # Se arregla AFINANDO, no relajando: la base trae la tabla en
            # `conjuros_siempre_preparados`, así que el origen no solo se
            # acepta, se COMPRUEBA. Un conjuro de dominio inventado, o puesto
            # a un nivel al que la subclase todavía no lo concede, ahora salta.
            if "subclase" in o:
                _comprueba_conjuro_de_subclase(ficha, s, o, clave, inf)


# ── Tres huecos que destapó el estrés con agentes (2026-08-30) ───────────
# Ninguno lo habría encontrado el generador automático: los tres son cosas que
# el verificador **dejaba pasar en silencio**, no cosas que reventaran.
def verificar_dotes_y_subclase(ficha, inf):
    # El CUARTO chequeo degradado, y el que peor pinta tenía: se saltaba
    # justamente los tres huecos que el estrés con agentes había destapado
    # —la subclase de otra clase, el prerrequisito de dote sin comprobar—, o
    # sea que una ficha multiclase esquivaba en silencio los chequeos escritos
    # para cazar lo que se colaba en silencio.
    if not una_sola_clase(ficha, inf):
        return
    c = ficha["clases"][0]

    # 1. La subclase tiene que ser DE SU CLASE. Un Pícaro con la subclase
    #    «Campeón» del Guerrero pasaba en verde: la ref resolvía, porque el
    #    registro existe… en otro fichero.
    sub = c.get("subclase")
    if sub:
        archivo = sub.split("#")[0]
        esperado = f"clases/subclases/{c['ref'].split('/')[-1]}"
        if archivo != esperado:
            inf.error(f"la subclase {sub!r} no es de {c['clase']}: debería salir "
                      f"de {esperado}")
        else:
            nombre = sub.split("#")[-1]
            d = cargar(archivo) or {}
            if not any(s["nombre"] == nombre for s in d.get("subclases", [])):
                inf.error(f"la subclase {nombre!r} no existe en {archivo}")
            niveles = [f["n"] for f in (cargar(c["ref"].split("#")[0]) or {}).get("progresion", [])
                       if any(calculo.es_marcador_de("subclase", r)
                              for r in (f.get("rasgos") or []))]
            if niveles and c["nivel"] < min(niveles):
                inf.error(f"la ficha declara subclase en el nivel {c['nivel']} y "
                          f"{c['clase']} no la concede hasta el {min(niveles)}")

    # 2. Las dotes que el personaje TIENE deben cumplir su prerrequisito.
    #    La Fase 15 construyó `buscar.dotes_disponibles()` para OFRECER las que
    #    puede tomar, y nadie comprobaba las que ya lleva puestas: un Guerrero
    #    con Inteligencia 8 llevaba «Mente aguda», que pide 13.
    try:
        import prerrequisitos as P
        import buscar
    except ImportError:
        return
    perfil = buscar._perfil(ficha)
    for x in ficha.get("dotes", []) or []:
        ref = x.get("ref", "")
        archivo, _, nombre = ref.partition("#")
        d = cargar(archivo) or {}
        dote = next((y for y in d.get("dotes", []) if y["nombre"] == nombre), None)
        if dote is None:
            # TOLERADO: la ref rota la caza `_recorrer_refs`, que recorre TODAS
            # las refs de la ficha. Avisar aquí también sería el mismo error dos
            # veces.
            continue
        try:
            est = P.analizar(dote.get("prerrequisito"))
        except P.ErrorDePrerrequisito:
            continue                      # lo caza `validar_prerrequisitos()`
        cumple, motivos = P.evaluar(est, perfil)
        if not cumple:
            fallan = [m for m in motivos if m.startswith("✗")]
            inf.error(f"la dote «{nombre}» pide «{dote['prerrequisito']}» y el "
                      f"personaje no lo cumple: {'; '.join(fallan)}")


def verificar_forma_competencias(ficha, inf):
    """Regla 6 de `_ESQUEMA.md`: las competencias van como `categoria:` (texto
    literal), **nunca** como `ref:` a un objeto.

    No es formalismo: «Armas sencillas» no existe como registro en `equipo/`,
    solo existen las armas concretas. Poner un objeto en su lugar confunde
    «tengo una daga» con «sé usar armas sencillas». **Nueve de las diecisiete
    fichas de la base lo hacían** y nada lo comprobaba.
    """
    for k in ("armas", "armaduras", "herramientas"):
        for x in (ficha.get("competencias") or {}).get(k) or []:
            if "categoria" not in x:
                inf.error(f"competencias.{k}: {x!r} no declara `categoria`. La "
                          f"regla 6 del esquema exige el texto literal de la "
                          f"categoría, no una `ref` a un objeto concreto")


# ── Copia de texto en vez de referencia ──────────────────────────────────
# Campos donde _ESQUEMA.md permite prosa libre sin límite de longitud
# (nombre, historia, personalidad, notas del jugador...). Todo lo demás que
# no esté aquí y tenga 15+ palabras seguidas es sospechoso: o es una
# descripción copiada de la base donde debería haber una `ref`, o es un
# campo que el esquema no contempla y conviene que alguien lo revise.
_CAMPOS_PROSA_LIBRE = {
    "nombre", "jugador", "historia", "personalidad", "descripcion_fisica",
    "alineamiento", "notas", "trasfondo_narrativo",
}


def verificar_sin_copias(ficha, inf):
    """Heurística: ningún valor de texto fuera de 'decisiones[].cita' y de
    los campos de prosa libre debería tener 15+ palabras seguidas — eso es
    prosa copiada, no una referencia.

    (Bug real hallado en pruebas de 5 agentes: la versión anterior no
    exceptuaba historia/personalidad, que el propio esquema declara como
    prosa libre sin restricción — daba falsos positivos en toda ficha con
    trasfondo narrativo escrito de un tirón.)"""
    def walk(nodo, ruta):
        if isinstance(nodo, dict):
            for k, v in nodo.items():
                if ruta == "decisiones" and k == "cita":
                    continue
                if k in _CAMPOS_PROSA_LIBRE:
                    continue
                if ruta == "decisiones" and k == "eleccion":
                    continue  # explicación del LLM, no texto de la base
                walk(v, f"{ruta}.{k}" if ruta else k)
        elif isinstance(nodo, list):
            for i, v in enumerate(nodo):
                walk(v, ruta)
        elif isinstance(nodo, str):
            if len(nodo.split()) > 15:
                inf.error(f"posible texto copiado en {ruta!r} (>15 palabras seguidas): "
                          f"{nodo[:60]!r}…")
    walk(ficha, "")


def calcular_bloque(ficha):
    """El bloque `calculado` que esta ficha DEBERÍA tener.

    Existe porque la Fase 14 rompió un paso documentado de la skill
    `/personaje` sin que nadie se enterara: su paso 10 mandaba ejecutar
    `calculo.py ca --clase Monje`, y desde que las fórmulas de CA son efectos
    citados esa función **se niega a responder** cuando la CA depende de un
    rasgo (que es lo correcto: no puede saber el nivel, la subclase ni el
    escudo). Correcto que falle, pero la skill seguía mandándolo.

    Aquí se calcula desde la ficha entera, que es lo único que tiene la
    información suficiente. La skill escribe la ficha sin `calculado`, llama a
    esto y pega el resultado.
    """
    clases = ficha.get("clases", [])
    if len(clases) != 1:
        sys.exit("✗ --calcular solo sabe de personajes de una sola clase")
    c = clases[0]
    clase_d = buscar.clase(c["clase"])
    ab = clase_d["atributos_basicos"]
    final = ficha["caracteristicas"]["final"]
    con_mod = calculo.modificador(final["con"])
    mods = {"mod_" + k: calculo.modificador(v) for k, v in final.items()}
    pg_base, avisos = calculo.pg_max_de_ficha(ficha, con_mod, ab["dado_golpe"])
    pb = calculo.bonificador_competencia(ficha["nivel_total"])
    agregado = efectos.calcular_de_ficha(ficha, mods, pb, pg_base)

    bloque = {"pg_max": agregado["pg_max"], "ca": agregado["ca"],
              "bonif_competencia": pb}
    if "velocidad" in agregado:
        bloque["velocidad"] = agregado["velocidad"]
    if clase_d.get("lanzador") not in (None, "ninguno"):
        clave = {"inteligencia": "int", "sabiduría": "sab",
                 "carisma": "car"}.get(clase_d["aptitud_magica"].lower())
        if clave:
            apt = calculo.modificador(final[clave])
            bloque["cd_conjuros"] = calculo.cd_conjuros(apt, pb)
            bloque["bonif_ataque_conjuros"] = calculo.bonif_ataque_conjuros(apt, pb)
    # SIEMPRE `motor`, y no hay parámetro para cambiarlo. Este es el escritor:
    # si pudiera firmar `agente-manual`, la firma no valdría nada. Un número
    # solo puede declararse leído a mano si lo escribió una lectura a mano.
    import datetime
    bloque["_origen"] = {"metodo": "motor", "informe": None,
                         "fecha": datetime.date.today().isoformat()}
    return bloque, avisos


# ── Claves que el esquema no contempla ───────────────────────────────────
# Hueco nº 5 de la ronda 2: una clave inventada NO se rechazaba. Un `raza:`
# duplicando `especie:`, un `caracteristica:` en singular enmascarando que
# falta el bloque obligatorio, un `decisiones[].nota` — tres agentes metieron
# tres claves distintas y ninguna saltó como tal; solo saltaban de rebote si
# su texto pasaba de 15 palabras.
#
# La tentación era rechazar esas tres. Eso habría sido el parche puntual:
# la cuarta clave inventada volvería a colarse. Lo que se hace es leer la
# lista de claves válidas **del propio `_ESQUEMA.md`** —el bloque de ejemplo
# más la sección «Prosa libre»— y contrastar contra ella. El esquema es el
# contrato, así que es el esquema quien tiene que decir qué cabe; si mañana
# gana un campo, el chequeo lo aprende solo. Es la regla inviolable 6
# aplicada a la forma de la ficha: la lista se DESCUBRE, no se teclea.
@functools.lru_cache(maxsize=1)
def _claves_del_esquema():
    ruta = pathlib.Path(__file__).parent / "personajes" / "_ESQUEMA.md"
    if not ruta.exists():
        return frozenset()
    t = ruta.read_text(encoding="utf-8")
    claves = set()
    for bloque in re.findall(r"```yaml\n(.*?)```", t, re.S):
        limpio = "\n".join(l for l in bloque.splitlines()
                           if not l.strip().startswith("#"))
        claves |= set(re.findall(r"^([a-zA-Z_][\w]*):", limpio, re.M))
    sec = re.search(r"## Prosa libre.*?\n(.*?)\n##", t, re.S)
    if sec:
        claves |= set(re.findall(r"`([a-z_]+)`", sec.group(1)))
    return frozenset(claves)


def verificar_claves(ficha, inf):
    permitidas = _claves_del_esquema()
    if not permitidas:
        inf.error("no se pudo leer `personajes/_ESQUEMA.md`: sin el contrato "
                  "no se puede comprobar qué claves valen")
        return
    for k in ficha:
        if k in permitidas:
            inf.comprobados += 1
        else:
            inf.error(
                f"la ficha trae la clave {k!r}, que `personajes/_ESQUEMA.md` "
                f"no contempla. O es un descuido —`raza` por `especie`, "
                f"`caracteristica` por `caracteristicas`—, o el esquema tiene "
                f"que documentarla primero")


# ── Idiomas ──────────────────────────────────────────────────────────────
# Hueco nº 3 de la ronda 2 de estrés: un idioma podía declarar el origen que
# le diera la gana y nadie lo miraba. Dos agentes lo destaparon con el mismo
# invento por caminos distintos —«Celestial por ser Aasimar», «Enano por ser
# Enano»—, y el segundo con el señuelo de que el idioma se llama igual que la
# especie. **Ninguna de las 10 especies de esta base concede idiomas**, ni
# ninguno de los 16 trasfondos: se comprobó campo a campo el 2026-09-05.
#
# Es el mismo mecanismo que armas, armaduras y herramientas: reúne lo que la
# base permite, y contrasta. Lo que la base permite son tres cosas, y las
# tres se comprueban:
#   · la ELECCIÓN de la tabla estándar (`reglas/idiomas.yaml` → nota), que
#     concede «común y otros dos»;
#   · un RASGO DE CLASE que conceda uno —«Druídico» del Druida, «Jerga de
#     ladrones» del Pícaro—, y entonces el rasgo tiene que existir de verdad
#     en esa clase y a un nivel ya alcanzado;
#   · nada más.
def verificar_idiomas(ficha, inf):
    idiomas = (ficha.get("competencias") or {}).get("idiomas") or []
    if not idiomas:
        # TOLERADO: que la ficha no declare idiomas es un hueco del ESQUEMA,
        # no de esta comprobación, y lo cubre `verificar_forma_competencias`.
        # Aquí solo se comprueba lo que hay.
        return
    tablas = cargar("reglas/idiomas.yaml") or {}
    validos = {x["nombre"] for grupo in ("estandar", "inusuales")
               for x in (tablas.get(grupo) or []) if isinstance(x, dict)}
    if not validos:
        inf.error("reglas/idiomas.yaml no trae tablas legibles: no se pueden "
                  "comprobar los idiomas")
        return

    por_eleccion = 0
    for e in idiomas:
        if not isinstance(e, dict):
            inf.error(f"competencias.idiomas: entrada que no es un mapa: {e!r}")
            continue
        nombre = e.get("nombre")
        if nombre not in validos:
            inf.error(f"competencias.idiomas: {nombre!r} no está en las tablas "
                      f"de `reglas/idiomas.yaml` (revisa el nombre exacto: la "
                      f"tabla dice «Elfo», no «Élfico»)")
            continue
        o = e.get("origen") or {}
        if not o:
            # TOLERADO: no es abandonar el registro, es aprobarlo. Un idioma
            # sin `origen` es uno de los elegidos, y su nombre ya se ha
            # contrastado contra la tabla tres líneas más arriba.
            inf.comprobados += 1
            continue
        if "especie" in o or "trasfondo" in o:
            inf.error(
                f"competencias.idiomas: {nombre!r} dice venir de "
                f"{'la especie' if 'especie' in o else 'el trasfondo'}, y en "
                f"esta base NINGUNA especie ni trasfondo concede idiomas. Los "
                f"que no vienen de un rasgo de clase se ELIGEN de la tabla "
                f"estándar (`reglas/idiomas.yaml` → nota)")
            continue
        if "regla" in o:
            # TOLERADO: ídem, es la rama que aprueba. Y no se va de rositas:
            # el recuento `por_eleccion` se contrasta al final contra el
            # «común y otros dos» de la nota.
            por_eleccion += 1
            inf.comprobados += 1
            continue
        if "clase" in o and "rasgo" in o:
            # TOLERADO: lo cubre `_comprueba_idioma_de_rasgo`, que es quien
            # habla —aprueba o da el error— para este caso.
            _comprueba_idioma_de_rasgo(ficha, nombre, o, inf)
            continue
        inf.error(f"competencias.idiomas: {nombre!r} declara un `origen` que "
                  f"este chequeo no sabe comprobar: {o!r}")

    # «Común y otros DOS» — la nota de la tabla. Los que vienen de un rasgo de
    # clase van aparte y no cuentan contra ese par.
    if por_eleccion > 2:
        inf.error(f"competencias.idiomas: {por_eleccion} idiomas elegidos de "
                  f"la tabla estándar, y `reglas/idiomas.yaml` concede «común "
                  f"y otros dos»")
    if "Común" not in {e.get("nombre") for e in idiomas if isinstance(e, dict)}:
        inf.error("competencias.idiomas: falta «Común», que la nota de "
                  "`reglas/idiomas.yaml` da a todo personaje")


def _comprueba_idioma_de_rasgo(ficha, nombre, origen, inf):
    """Un idioma que dice venir de un rasgo de clase: el rasgo tiene que
    existir en esa clase, y el personaje haber llegado a su nivel."""
    clase = origen.get("clase")
    rasgo = origen.get("rasgo")
    suya = next((c for c in (ficha.get("clases") or [])
                 if c.get("clase") == clase), None)
    if suya is None:
        inf.error(f"competencias.idiomas: {nombre!r} dice venir de la clase "
                  f"{clase!r} y el personaje no la tiene")
        return
    stem = suya["ref"].split("#")[0].split("/")[-1].replace(".yaml", "")
    doc = cargar(f"clases/rasgos/{stem}.yaml") or {}
    r = next((x for x in (doc.get("rasgos") or [])
              if x.get("nombre") == rasgo), None)
    if r is None:
        inf.error(f"competencias.idiomas: {nombre!r} dice venir del rasgo "
                  f"{rasgo!r} de {clase}, y esa clase no tiene ese rasgo")
        return
    if r.get("nivel", 1) > suya.get("nivel", 1):
        inf.error(f"competencias.idiomas: {rasgo!r} es de nivel "
                  f"{r.get('nivel')} y el personaje es de nivel "
                  f"{suya.get('nivel')}")
        return
    inf.comprobados += 1


# ── `pg_por_nivel`: que el valor CREÍBLE lo sea de verdad ────────────────
# Hueco nº 2 de la ronda 2 de estrés (2026-09-05), y es patrón espiral puro:
# `calculo.pg_max_de_ficha()` SUMABA el `valor` de cada nivel sin mirar si ese
# número podía salir del dado de la clase. Tres agentes lo destaparon por
# caminos distintos y ninguno hizo falta que fuera sutil:
#
#   · un d8 con una tirada de 9, y un d12 con una de 13;
#   · un `valor_establecido` de 7 en un Guerrero, que es el del Bárbaro
#     —el más fino de los tres: el método es correcto y el número existe,
#     solo que en la tabla de OTRA clase—;
#   · `metodo: maximo_dado` en el nivel 3, cuando es la regla del nivel 1.
#
# Lo que duele es que la autoridad ya estaba leída: `calculo.valor_establecido_pg()`
# lee la tabla citada de la base desde la Fase 14b-1, y nadie la usaba para
# verificar. Aquí no se cablea ni un número: los métodos legales salen de
# `metodos` y el valor fijo de la tabla, los dos de la misma página citada.

# Puente entre el `id` que usa la base y el `metodo` que usa el esquema de
# ficha. Son dos vocabularios que nacieron por separado y hay que atarlos en
# algún sitio; se hace aquí, explícito y de dos entradas, en vez de comparar
# a ojo. `maximo_dado` no está: es la regla del nivel 1, que vive en otra
# página (`puntos_golpe.nivel_1`) y no en la lista de métodos de subida.
_METODO_DE_ID = {"tirar": "tirada", "valor_establecido": "valor_establecido"}


def _caras(dado):
    m = re.fullmatch(r"[dD](\d+)", str(dado or "").strip())
    return int(m.group(1)) if m else None


def verificar_pg_por_nivel(ficha, inf):
    """Cada entrada de `pg_por_nivel` declara un método y un valor crudo. Se
    comprueba que el método sea uno de los que la base admite para ese nivel,
    y que el valor pueda salir de donde el método dice."""
    if not una_sola_clase(ficha, inf):
        return
    historia = ficha.get("pg_por_nivel") or []
    if not historia:
        # TOLERADO: sin historia declarada, quien manda es `calculo`, que ya
        # SALE CON ERROR si la ficha es de nivel 2 o más. Duplicar aquí ese
        # rechazo daría dos mensajes para un solo defecto.
        return
    c = ficha["clases"][0]
    clase_d = cargar(c["ref"].split("#")[0]) or {}
    dado = (clase_d.get("atributos_basicos") or {}).get("dado_golpe")
    caras = _caras(dado)
    if caras is None:
        inf.error(f"la clase {c['clase']!r} no declara un dado de golpe "
                  f"legible ({dado!r}): no se puede comprobar `pg_por_nivel`")
        return

    g = cargar("reglas/generacion_personaje.yaml") or {}
    sig = ((g.get("puntos_golpe") or {}).get("niveles_siguientes_al_1") or {})
    metodos_subida = {_METODO_DE_ID[m["id"]]
                      for m in (sig.get("metodos") or [])
                      if m.get("id") in _METODO_DE_ID}
    fijo = calculo.valor_establecido_pg(c["clase"])

    for e in historia:
        if not isinstance(e, dict):
            # TOLERADO: una entrada que no es un mapa la caza `calculo`, que
            # lee `e["nivel"]` de todas y revienta con la entrada delante.
            continue
        n, metodo, valor = e.get("nivel"), e.get("metodo"), e.get("valor")
        if n == 1:
            if metodo != "maximo_dado":
                inf.error(f"pg_por_nivel nivel 1: el método es {metodo!r} y la "
                          f"regla del nivel 1 es el máximo del dado "
                          f"(`puntos_golpe.nivel_1`)")
            elif valor != caras:
                inf.error(f"pg_por_nivel nivel 1: el máximo de un {dado} es "
                          f"{caras} y la ficha declara {valor!r}")
            else:
                inf.comprobados += 1
            continue
        if metodo not in metodos_subida:
            inf.error(f"pg_por_nivel nivel {n}: método {metodo!r}. Para los "
                      f"niveles 2+ la base solo admite "
                      f"{sorted(metodos_subida)} "
                      f"(`puntos_golpe.niveles_siguientes_al_1.metodos`)")
            continue
        if metodo == "valor_establecido":
            if valor != fijo:
                inf.error(f"pg_por_nivel nivel {n}: `valor_establecido` de "
                          f"{c['clase']} es {fijo} y la ficha declara "
                          f"{valor!r} (tabla «{(sig.get('tabla_valores_establecidos') or {}).get('titulo')}»)")
                continue
        elif not (isinstance(valor, int) and 1 <= valor <= caras):
            inf.error(f"pg_por_nivel nivel {n}: una tirada de {dado} da entre "
                      f"1 y {caras}, y la ficha declara {valor!r}")
            continue
        inf.comprobados += 1


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--calcular":
        ficha = cargar(sys.argv[2])
        if ficha is None:
            sys.exit(f"✗ no se pudo leer {sys.argv[2]}")
        bloque, avisos = calcular_bloque(ficha)
        for a in avisos:
            print(f"  ⚠ {a}", file=sys.stderr)
        print("calculado:")
        for k, v in bloque.items():
            print(f"  {k}: {v}")
        return 0
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 verificar_personaje.py [--calcular] "
                 "personajes/<nombre>.yaml")
    ruta = sys.argv[1]
    ficha = cargar(ruta)
    if ficha is None:
        sys.exit(f"✗ no se pudo leer {ruta}")

    inf = Informe()
    contador = [0]
    _recorrer_refs(ficha, inf, contador)

    # Los dos defectos de ROBUSTEZ de la ronda 2 de estrés se arreglan aquí,
    # porque son el mismo problema visto dos veces: un chequeo que revienta se
    # lleva por delante a los que venían detrás.
    #
    #   · una ficha sin bloque `caracteristicas` moría con un `KeyError` en
    #     `buscar.py:174` **sin imprimir una sola línea**: rechazaba, sí, pero
    #     no decía qué faltaba;
    #   · un `pg_por_nivel` con un hueco hacía `sys.exit` desde `calculo`, y
    #     la ficha 3 del agente B declaraba CINCO defectos de los que solo se
    #     veía UNO. Un verificador que solo enseña el primer problema obliga a
    #     iterar a ciegas, que es justo lo que este proyecto no quiere.
    #
    # Cada chequeo corre en su propia red: si revienta, se convierte en un
    # error con su nombre delante y los demás siguen. No se traga nada — un
    # fallo sigue siendo un fallo—, solo se deja de perder el resto del
    # informe por culpa del primero.
    for chequeo in (verificar_claves, verificar_habilidades,
                    verificar_categorias, verificar_compra_puntos,
                    verificar_pg_por_nivel, verificar_idiomas,
                    verificar_origen_del_calculado,
                    verificar_mejoras, verificar_conjuros,
                    verificar_dotes_y_subclase, verificar_forma_competencias,
                    verificar_calculado, verificar_sin_copias):
        try:
            chequeo(ficha, inf)
        except KeyError as e:
            inf.error(f"{chequeo.__name__}: la ficha no trae {e}, y este "
                      f"chequeo lo necesita. Falta un bloque obligatorio "
                      f"(ver `personajes/_ESQUEMA.md`)")
        except SystemExit as e:
            inf.error(f"{chequeo.__name__}: {e}")

    print(f"{contador[0]} referencias comprobadas.")
    for a in inf.avisos:
        print(f"  ⚠ {a}")
    if inf.errores:
        print(f"❌ {len(inf.errores)} problemas:")
        for e in inf.errores:
            print(f"  ✗ {e}")
        return 1
    print("✅ FICHA VERIFICADA — 0 problemas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
