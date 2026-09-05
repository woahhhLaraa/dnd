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

    for campo, esperado in comprobaciones:
        real = calc.get(campo)
        if real != esperado:
            inf.error(f"calculado.{campo} = {real!r}, pero recalculado da {esperado!r}")


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
    inf.comprobados = getattr(inf, "comprobados", 0) + 1


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
    return bloque, avisos


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
    verificar_habilidades(ficha, inf)
    verificar_categorias(ficha, inf)
    verificar_compra_puntos(ficha, inf)
    verificar_mejoras(ficha, inf)
    verificar_conjuros(ficha, inf)
    verificar_dotes_y_subclase(ficha, inf)
    verificar_forma_competencias(ficha, inf)
    verificar_calculado(ficha, inf)
    verificar_sin_copias(ficha, inf)

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
