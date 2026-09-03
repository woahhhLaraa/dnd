#!/usr/bin/env python3
"""Capa 5b de verificación: contrasta conjuros, armas, armaduras y especies
contra el SRD 5.2 ya estructurado campo a campo.

Fuente: `_verificacion/foundry_srd52/` (packs `*24` del sistema dnd5e de
Foundry VTT). Es el mismo SRD 5.2 © Wizards of the Coast, CC-BY-4.0, que ya
teníamos en Markdown en `_verificacion/srd52/`, pero con los datos en campos
en vez de en prosa. No sustituye al manual: si discrepan, manda el Manual del
Jugador y la discrepancia se resuelve leyendo la página.

Complementa a `verificar_srd.py`, que responde la misma pregunta («¿coincide
con una fuente externa?») sobre una superficie distinta: aquel cubre las 12
tablas de clase; este cubre todo lo demás.

── Principio de diseño ────────────────────────────────────────────────────
Este script NO traduce. Traducir de memoria violaría la regla 1 («consultar,
no recordar») y metería el conocimiento previo del modelo justo en la capa
que existe para detectarlo.

En su lugar: se emparejan registros por una clave que no depende del idioma
(el `nombre_en` que ya trae `hechizos.json` desde `_origen_hechizos.csv`, o
una huella numérica en el caso de las armas), y los vocabularios —escuelas
de magia, tipos de daño, propiedades de arma, maestrías— se **deducen** de
los pares emparejados. Después se exige que cada vocabulario sea una
biyección consistente. Si dos registros emparejados discrepan sobre a qué
traduce un término, eso es un hallazgo real y se reporta.

Uso:
    python3 verificar_foundry.py            # todo
    python3 verificar_foundry.py conjuros   # un solo módulo
"""
import collections
import glob
import json
import pathlib
import re
import sys

import yaml

B = pathlib.Path(__file__).parent
FOUNDRY = B / "_verificacion" / "foundry_srd52"


# ── Utilidades ────────────────────────────────────────────────────────────
def cargar_yaml(p):
    return yaml.safe_load(pathlib.Path(p).read_text(encoding="utf-8"))


def paquete(carpeta, tipo=None, sub=None):
    """Todos los registros de un pack de Foundry, opcionalmente de un `type`.

    `sub` acota a los registros cuya carpeta contenedora se llama así —el
    pack los agrupa por su cuenta: `classes24/barbarian/class-features/`,
    `equipment24/martial-melee/`—. Sirve para pedir UNA rebanada cuando el
    resto del `type` todavía no se contrasta, y `censo.py` lo lee: un
    `paquete(c, t)` sin `sub` promete el `type` entero, y uno con `sub`
    promete solo esa rebanada y deja las demás como pendientes con nombre.
    Así una cobertura parcial se ve, en vez de disfrazarse de completa.
    """
    for f in sorted(glob.glob(str(FOUNDRY / carpeta / "**" / "*.yml"), recursive=True)):
        if "_folder" in f:
            continue
        if sub is not None and pathlib.Path(f).parent.name != sub:
            continue
        d = cargar_yaml(f)
        if tipo and d.get("type") != tipo:
            continue
        # La ruta viaja con el registro porque el pack guarda información en
        # ella —de qué clase es el rasgo, en qué rebanada vive— que no está
        # dentro del YAML. La clave lleva guion bajo para que se distinga de
        # los campos que el pack sí trae.
        d["_ruta"] = f
        yield d


class Vocabulario:
    """Correspondencia término_inglés -> término_castellano deducida de los
    pares emparejados, no escrita a mano.

    Cada `observa()` es un voto. Al final, un término con más de un voto
    distinto es una discrepancia: significa que dos registros que la huella
    dice que son el mismo no coinciden en ese campo.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.votos = collections.defaultdict(lambda: collections.defaultdict(list))

    def observa(self, en, es, contexto):
        if en is None or es is None:
            return
        self.votos[en][es].append(contexto)

    def conflictos(self):
        """Un término con más de una traducción observada. Se nombra siempre la
        minoría con sus registros concretos: es donde está el error a revisar."""
        out = []
        for en, opciones in sorted(self.votos.items()):
            if len(opciones) < 2:
                continue
            orden = sorted(opciones.items(), key=lambda kv: -len(kv[1]))
            mayoria, _ = orden[0]
            for es, ctxs in orden[1:]:
                out.append(
                    f"{self.nombre} {en!r}: {len(orden[0][1])} registros dicen "
                    f"{mayoria!r} pero {', '.join(ctxs)} dice(n) {es!r}"
                )
        return out

    def resuelto(self):
        return {en: max(op.items(), key=lambda kv: len(kv[1]))[0]
                for en, op in self.votos.items()}


class Informe:
    def __init__(self, titulo):
        self.titulo = titulo
        self.comprobados = 0
        self.errores = []
        self.notas = []

    def error(self, msg):
        self.errores.append(msg)

    def nota(self, msg):
        self.notas.append(msg)

    def imprime(self):
        estado = "✅" if not self.errores else "❌"
        print(f" {estado} {self.titulo:<24} {self.comprobados:>4} valores contrastados"
              + ("" if not self.errores else f"  · {len(self.errores)} discrepancia(s)"))
        for e in self.errores:
            print(f"      ✗ {e}")
        for n in self.notas:
            print(f"      ℹ {n}")


def norm_txt(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


# ── 13a · Conjuros ────────────────────────────────────────────────────────
# Casos en los que el SRD discrepa y la página del manual nos da la razón.
# Cada uno se leyó visualmente antes de anotarlo aquí: sin esa lectura, una
# excepción es indistinguible de tapar un error propio.

# ── Coste del componente material ─────────────────────────────────────────
#
# Superficie que **nadie contrastaba** hasta el 2026-08-29: el módulo de
# conjuros comprobaba `consume_material` pero no la **cifra**. La descubrió una
# muestra aleatoria post-corrección, cuando `Golpe de viento acerado` resultó
# tener `coste: null` sobre una página que exige «un arma cuerpo a cuerpo que
# valga al menos 1 pp».
#
# El SRD no publica el coste como número: lo lleva **dentro del texto inglés**
# del material («worth 1,000+ GP», «1 Copper Piece»). Se extrae con regex y se
# compara con el nuestro, sin traducir nada más que las tres unidades.
_UNIDAD_SRD = {"GP": "po", "SP": "pp", "CP": "pc",
               "GOLD": "po", "SILVER": "pp", "COPPER": "pc"}
_RE_COSTE_EN = re.compile(r"([\d,]+)\s*\+?\s*(GP|SP|CP)\b", re.I)
_RE_COSTE_EN_LARGO = re.compile(
    r"([\d,]+)\s*\+?\s*(Gold|Silver|Copper)\s+Piece", re.I)
_RE_COSTE_ES = re.compile(r"\s*([\d.,]+)\s*(po|pp|pc)\s*\*?\s*$", re.I)

# Cinco conjuros llevan **dos materiales con precio distinto**, o un precio
# «por unidad», y el campo `coste` es texto libre que los agrega a mano. No son
# defectos: son un límite del modelo —un conjuro puede tener varios materiales
# y `coste` es un solo string— y por eso se declaran en vez de silenciarse.
# ⛔ COSTE_COMPUESTO ya NO exime a nadie del contraste (Fase 14b-2). Se conserva
# como REGISTRO de lo que la base creía antes de descomponer, porque dos de sus
# seis entradas resultaron ser sumas que ninguna página imprime: *Proyección
# astral* guardaba «1100 po» (1000 jacinto + 100 lingote) y *Conocer las
# leyendas* «200 po» (4 tiras × 50). La verdad vive hoy en
# `componentes.materiales` de cada conjuro, verificada por doble lectura.
_COSTE_COMPUESTO_HISTORICO = {
    "Conocer las leyendas": "incienso 250 po (se consume) + cuatro tiras de marfil 200 po",
    "Crear muerto viviente": "150 po de ónice negro POR CADÁVER",
    "Clon": "diamante 1000 po (se consume) + recipiente sellable 2000 po",
    "Proyección astral": "jacinto 1000 po + barra de plata 100 po, POR OBJETIVO",
    "Cofre oculto de Leomund": "cofre 5000 po + réplica Diminuta 50 po; la página "
                               "nunca imprime la suma «5050»",
    "Vínculo protector": "50 po POR ANILLO (un par); la página dice «cada uno», "
                         "así que el total del par NO es el dato que se guarda",
}


def _coste_srd(texto):
    """Extrae (cifra, unidad) del texto inglés del material, o None."""
    m = _RE_COSTE_EN.search(texto) or _RE_COSTE_EN_LARGO.search(texto)
    if not m:
        return None
    return (int(m.group(1).replace(",", "")), _UNIDAD_SRD[m.group(2).upper()])


def _coste_nuestro(valor):
    """Extrae (cifra, unidad) de nuestro campo `coste`, o None, o 'compuesto'."""
    if not valor:
        return None
    m = _RE_COSTE_ES.match(str(valor))
    if not m:
        return "compuesto"
    return (int(m.group(1).replace(".", "").replace(",", "")), m.group(2).lower())


EXCEPCIONES_CONJUROS = {
    ("Patrón hipnótico", "verbal"): (
        "el manual dice «Componentes: V, S, M (una pizca de confeti)» "
        "(pdf 320 = libro 318); el pack del SRD omite el componente verbal"),
    ("Patrón hipnótico", "concentracion"): (
        "el manual dice «Duración: Concentración, hasta 1 minuto» "
        "(pdf 320 = libro 318); el pack del SRD no marca concentración"),
    ("Prohibición", "ritual"): (
        "el manual dice «Tiempo de lanzamiento: 10 minutos o un ritual» "
        "(pdf 324 = libro 322); el pack del SRD no marca el ritual"),
    ("Recluir", "consume_material"): (
        "el manual dice «M (polvo de piedras preciosas que valga al menos "
        "5000 po, que se consume como parte del conjuro)» (pdf 328 = libro "
        "326); el pack del SRD no lo marca como consumido"),
}


def verificar_conjuros():
    """Empareja por `nombre_en`, que viene de `_origen_hechizos.csv` (columna
    `name_ingles`) — es dato de la fuente, no traducción nuestra."""
    inf = Informe("conjuros")
    nuestros = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]

    srd = {}
    for d in paquete("spells24", "spell"):
        srd[d["name"]] = d["system"]

    voc_escuela = Vocabulario("escuela")
    emparejados = 0
    sin_pareja = []

    for h in nuestros:
        en = h.get("nombre_en")
        if not en or en not in srd:
            sin_pareja.append(h["nombre"])
            continue
        s = srd[en]
        emparejados += 1
        ctx = f"{h['nombre']} / {en}"
        props = set(s.get("properties") or [])

        # nivel — comparable directamente, sin vocabulario de por medio
        inf.comprobados += 1
        if h["nivel"] != s.get("level"):
            inf.error(f"{ctx}: nivel nuestro {h['nivel']} vs SRD {s.get('level')}")

        # escuela — se deduce el vocabulario en vez de cablearlo
        voc_escuela.observa(s.get("school"), h["escuela"], ctx)

        # componentes y banderas — booleanos, sin ambigüedad de idioma
        comp = h.get("componentes") or {}
        for campo_srd, campo_nuestro, cont in (
            ("vocal", "verbal", comp),
            ("somatic", "somatico", comp),
            ("material", "material", comp),
            ("concentration", "concentracion", h),
            ("ritual", "ritual", h),
        ):
            inf.comprobados += 1
            esperado = campo_srd in props
            real = bool(cont.get(campo_nuestro))
            if real == esperado:
                continue
            motivo = EXCEPCIONES_CONJUROS.get((h["nombre"], campo_nuestro))
            if motivo:
                inf.nota(f"{ctx} · {campo_nuestro}: discrepa del SRD y "
                         f"mandamos nosotros — {motivo}")
            else:
                inf.error(f"{ctx}: {campo_nuestro} nuestro {real} vs SRD {esperado}")

        # ¿se consume el componente material? Es un campo aparte de las
        # banderas de arriba: el SRD lo publica en `materials.consumed`, no en
        # `properties`. Se comprueba porque aquí vivía el mayor defecto de la
        # base: la conversión del CSV usó su columna `gp` («tiene precio») en
        # vez del asterisco del coste («se consume»), y marcó 41 conjuros de más.
        mat = (s.get("materials") or {})
        if comp.get("material"):
            inf.comprobados += 1
            esperado = bool(mat.get("consumed"))
            real = bool(comp.get("consume_material"))
            if real != esperado:
                motivo = EXCEPCIONES_CONJUROS.get((h["nombre"], "consume_material"))
                if motivo:
                    inf.nota(f"{ctx} · consume_material: discrepa del SRD y "
                             f"mandamos nosotros — {motivo}")
                else:
                    inf.error(f"{ctx}: consume_material nuestro {real} vs "
                              f"SRD {esperado}")

            # …y la CIFRA del coste, que es lo que nadie miraba.
            esp_c = _coste_srd(mat.get("value") or "")
            real_c = _coste_nuestro(comp.get("coste"))
            if real_c == "compuesto":
                # FASE 14b-2: antes esto era una EXENCIÓN — los seis conjuros
                # con varios materiales se declaraban en `COSTE_COMPUESTO` y
                # salían del contraste. Ahora se contrastan de verdad, material
                # a material, porque el SRD **conserva la descomposición** y es
                # la única fuente que puede ver el modo de fallo nº 10: una
                # suma que ninguna página imprime.
                mats = comp.get("materiales")
                if not mats:
                    inf.error(f"{ctx}: coste {comp.get('coste')!r} no se puede "
                              f"leer como «N po|pp|pc» y no declara "
                              f"`materiales` que lo descompongan")
                else:
                    # OJO con los nombres: la primera versión llamó `srd` a
                    # esta lista y PISÓ el diccionario `srd` del pack. A partir
                    # del primer conjuro compuesto, `en not in srd` fallaba para
                    # todos los demás y el contraste caía de 3012 a 1818 valores
                    # en silencio, sin un solo error. Lo delató la CIFRA, no un
                    # fallo: por eso el total contrastado se publica y se vigila.
                    cifras_nuestras = sorted((m["coste"], m["unidad"]) for m in mats)
                    cifras_srd = sorted(
                        (int(g.replace(",", "")), _UNIDAD_SRD[u.upper()])
                        for g, u in _RE_COSTE_EN.findall(mat.get("value") or ""))
                    if not cifras_srd:
                        inf.nota(f"{ctx} · el SRD no publica cifra para este "
                                 f"material; nuestra descomposición "
                                 f"({len(mats)} materiales) queda sin contraste")
                    elif cifras_nuestras != cifras_srd:
                        inf.error(
                            f"{ctx}: nuestros materiales {cifras_nuestras} vs "
                            f"los del SRD {cifras_srd} — el SRD dice "
                            f"«{(mat.get('value') or '')[:90]}»")
                    else:
                        inf.comprobados += len(cifras_nuestras)
            elif esp_c != real_c:
                inf.comprobados += 1
                inf.error(f"{ctx}: coste nuestro {comp.get('coste')!r} vs SRD "
                          f"{esp_c[0]} {esp_c[1]} si lo hay — el SRD dice "
                          f"«{(mat.get('value') or '')[:70]}»")
            elif esp_c is not None:
                inf.comprobados += 1

    for c in voc_escuela.conflictos():
        inf.error(c)
    inf.comprobados += len(voc_escuela.votos)

    res = voc_escuela.resuelto()
    inf.nota(f"{emparejados} conjuros emparejados por nombre inglés · "
             f"{len(res)} escuelas deducidas, todas consistentes"
             if not voc_escuela.conflictos() else
             f"{emparejados} conjuros emparejados")
    if sin_pareja:
        inf.nota(f"{len(sin_pareja)} conjuros nuestros no están en el SRD "
                 f"(esperado: el SRD es subconjunto del manual)")
    return inf


# ── 13b · Armas ───────────────────────────────────────────────────────────
def _precio_a_pc(txt):
    """'20 po' -> 2000 piezas de cobre. 1 po = 10 pp = 100 pc."""
    m = re.fullmatch(r"([\d,.]+)\s*(po|pp|pc|pe|ppt)", norm_txt(txt))
    if not m:
        return None
    v = float(m.group(1).replace(",", "."))
    return {"pc": 1, "pp": 10, "pe": 50, "po": 100, "ppt": 1000}[m.group(2)] * v


_DENOM_A_PC = {"cp": 1, "sp": 10, "ep": 50, "gp": 100, "pp": 1000}


_CATEGORIA = {
    "armas_cuerpo_a_cuerpo_sencillas": "simpleM",
    "armas_a_distancia_sencillas": "simpleR",
    "armas_cuerpo_a_cuerpo_marciales": "martialM",
    "armas_a_distancia_marciales": "martialR",
}


def verificar_armas():
    """Empareja por huella numérica (dado de daño + precio + categoría), que no
    depende del idioma, y desempata en una segunda pasada con el vocabulario de
    tipos de daño deducido en la primera. Las maestrías se deducen igual.

    La categoría no es traducción: sale del nombre del grupo en nuestro YAML
    («cuerpo_a_cuerpo/a_distancia» × «sencillas/marciales») y del campo
    `type.value` del SRD, que codifican exactamente lo mismo."""
    inf = Informe("armas")
    d = cargar_yaml(B / "equipo" / "armas.yaml")
    nuestras = []
    for grupo in _CATEGORIA:
        for a in d.get(grupo, []):
            nuestras.append((grupo, a))

    srd = []
    for reg in paquete("equipment24", "weapon"):
        s = reg["system"]
        props = set(s.get("properties") or [])
        if "mgc" in props:          # armas mágicas: no están en nuestras tablas
            continue
        categoria = (s.get("type") or {}).get("value")
        if categoria not in set(_CATEGORIA.values()):
            continue
        base = (s.get("damage") or {}).get("base") or {}
        precio = s.get("price") or {}
        pc = None
        if precio.get("value") is not None and precio.get("denomination") in _DENOM_A_PC:
            pc = _DENOM_A_PC[precio["denomination"]] * float(precio["value"])
        srd.append({
            "nombre": reg["name"],
            "dado": (base.get("number"), base.get("denomination")),
            "tipos": base.get("types") or [],
            "pc": pc,
            "categoria": categoria,
            "props": props,
            "mastery": s.get("mastery") or None,
        })

    idx = collections.defaultdict(list)
    for w in srd:
        idx[(w["dado"][0], w["dado"][1], w["pc"], w["categoria"])].append(w)

    # nuestro lado, normalizado una sola vez
    pendientes = []
    for grupo, a in nuestras:
        # '1d6 contundente', y también '1 perforante' (cerbatana: daño sin dado)
        m = re.match(r"(\d+)(?:d(\d+))?\s+(\w+)", norm_txt(a.get("dano")))
        if not m:
            inf.error(f"{a['nombre']}: daño ilegible {a.get('dano')!r}")
            continue
        pendientes.append({
            "arma": a,
            "tipo_dano": m.group(3),
            "huella": (int(m.group(1)), int(m.group(2)) if m.group(2) else None,
                       _precio_a_pc(a.get("precio")), _CATEGORIA[grupo]),
        })

    voc_dano = Vocabulario("tipo de daño")
    voc_maestria = Vocabulario("maestría")
    parejas = []
    resto = []

    # ── Pasada 1: solo las huellas inequívocas. De ellas sale el vocabulario.
    for p in pendientes:
        cand = idx.get(p["huella"], [])
        if len(cand) == 1:
            parejas.append((p, cand[0]))
            if len(cand[0]["tipos"]) == 1:
                voc_dano.observa(cand[0]["tipos"][0], p["tipo_dano"],
                                 f"{p['arma']['nombre']} / {cand[0]['nombre']}")
        else:
            resto.append((p, cand))

    # ── Pasada 2: desempatar con el tipo de daño ya deducido.
    dano_es_a_en = {es: en for en, es in voc_dano.resuelto().items()}
    resto2 = []
    huerfanas = 0
    for p, cand in resto:
        if not cand:
            huerfanas += 1
            continue
        esperado_en = dano_es_a_en.get(p["tipo_dano"])
        afinado = [w for w in cand if esperado_en and w["tipos"] == [esperado_en]]
        if len(afinado) == 1:
            parejas.append((p, afinado[0]))
        else:
            resto2.append((p, afinado or cand))

    # ── Pasada 3: desempatar con la maestría deducida en 1 y 2.
    # En 2024 hay parejas de armas idénticas en todo número —Glaive/Halberd
    # comparten dado, precio, categoría, tipo de daño y hasta peso— y solo la
    # maestría las distingue. Como la maestría ya está deducida de las armas
    # inequívocas (p. ej. cleave sale de Greataxe, que no tiene rival), sirve
    # para cerrar el resto sin traducir nada a mano.
    for p, w in parejas:
        voc_maestria.observa(w["mastery"], norm_txt(p["arma"].get("maestria")) or None,
                             f"{p['arma']['nombre']} / {w['nombre']}")
    maestria_es_a_en = {es: en for en, es in voc_maestria.resuelto().items()}
    ambiguas = 0
    matched_by_mastery = set()
    for p, cand in resto2:
        nuestra_maestria = norm_txt(p["arma"].get("maestria"))
        esperada = maestria_es_a_en.get(nuestra_maestria)
        afinado = [w for w in cand if esperada and w["mastery"] == esperada]
        if len(afinado) == 1:
            parejas.append((p, afinado[0]))
            matched_by_mastery.add(id(p))
        elif esperada and not afinado:
            # Conocemos la maestría y NINGUNO de los candidatos la tiene. Eso no
            # es una ambigüedad, es una discrepancia: si se quedara en «sin
            # emparejar» el arma desaparecería del contraste sin avisar, que es
            # justo el fallo silencioso que esta base persigue.
            detalle = ", ".join(
                "{}={}".format(w["nombre"], w["mastery"]) for w in cand)
            inf.error(
                f"{p['arma']['nombre']}: maestría {p['arma'].get('maestria')!r} "
                f"({esperada}), pero ninguno de sus equivalentes posibles la "
                f"tiene ({detalle})")
        else:
            ambiguas += 1

    # ── Verificación sobre todas las parejas ────────────────────────────────
    # Nota honesta: para las parejas cerradas en la pasada 3, la maestría se
    # usó para emparejar, así que ahí no es un chequeo independiente. Lo que
    # sí sigue siéndolo en todos los casos es la CONSISTENCIA del vocabulario:
    # si dos armas obligaran a que 'cleave' signifique dos cosas distintas,
    # `voc_maestria.conflictos()` lo canta.
    for p, w in parejas:
        a = p["arma"]
        ctx = f"{a['nombre']} / {w['nombre']}"
        if id(p) in matched_by_mastery:
            voc_maestria.observa(w["mastery"], norm_txt(a.get("maestria")) or None, ctx)

        # tipo de daño: en pasada 2 sirvió para emparejar, pero en pasada 1 no,
        # así que aquí se comprueba de verdad contra el vocabulario resuelto
        inf.comprobados += 1
        if len(w["tipos"]) == 1:
            esperado = dano_es_a_en.get(p["tipo_dano"])
            if esperado and w["tipos"][0] != esperado:
                inf.error(f"{ctx}: daño nuestro {p['tipo_dano']!r} vs SRD "
                          f"{w['tipos'][0]!r}")

        # nº de propiedades: comparable sin traducir
        inf.comprobados += 1
        nuestras_props = list(a.get("propiedades") or [])
        srd_props = {x for x in w["props"] if x not in ("mgc", "foc")}
        if len(nuestras_props) != len(srd_props):
            inf.error(f"{ctx}: {len(nuestras_props)} propiedades nuestras "
                      f"({', '.join(nuestras_props) or '—'}) vs {len(srd_props)} "
                      f"del SRD ({', '.join(sorted(srd_props)) or '—'})")

    for c in voc_dano.conflictos() + voc_maestria.conflictos():
        inf.error(c)
    inf.comprobados += len(voc_dano.votos) + len(voc_maestria.votos)

    inf.nota(f"{len(parejas)} armas emparejadas en 3 pasadas (dado+precio+categoría, "
             f"luego tipo de daño, luego maestría) · {len(voc_dano.votos)} tipos de "
             f"daño y {len(voc_maestria.votos)} maestrías deducidos, sin conflictos")
    if ambiguas:
        inf.nota(f"{ambiguas} sin emparejar de forma inequívoca ni siquiera por "
                 f"maestría")
    if huerfanas:
        inf.nota(f"{huerfanas} sin equivalente en el SRD")
    return inf


# ── 13c · Armaduras ───────────────────────────────────────────────────────
def verificar_armaduras():
    """Empareja por precio, y contrasta la CA — que en las armaduras es el
    dato que de verdad importa y es puramente numérico."""
    inf = Informe("armaduras")
    d = cargar_yaml(B / "equipo" / "armaduras.yaml")

    srd = {}
    for reg in paquete("equipment24", "equipment"):
        s = reg["system"]
        tipo = (s.get("type") or {}).get("value")
        if tipo not in ("light", "medium", "heavy", "shield"):
            continue
        if "mgc" in set(s.get("properties") or []):
            continue
        precio = s.get("price") or {}
        pc = None
        if precio.get("value") is not None and precio.get("denomination") in _DENOM_A_PC:
            pc = _DENOM_A_PC[precio["denomination"]] * float(precio["value"])
        srd.setdefault(pc, []).append({
            "nombre": reg["name"],
            "ca": (s.get("armor") or {}).get("value"),
            "tipo": tipo,
            "sigilo": bool((s.get("properties") or []) and "stealthDisadvantage" in
                           str(s.get("properties"))) or bool(s.get("stealth")),
            "fuerza": (s.get("strength") if s.get("strength") not in ("", 0) else None),
        })

    emparejadas = ambiguas = 0
    for grupo in ("armaduras_ligeras", "armaduras_medias", "armaduras_pesadas", "escudos"):
        for a in d.get(grupo, {}).get("tabla", []):
            pc = _precio_a_pc(a.get("precio"))
            cand = srd.get(pc, [])
            # afinar por tipo cuando el precio se repite
            esperado_tipo = {"armaduras_ligeras": "light", "armaduras_medias": "medium",
                             "armaduras_pesadas": "heavy", "escudos": "shield"}[grupo]
            cand = [c for c in cand if c["tipo"] == esperado_tipo]
            if len(cand) != 1:
                ambiguas += 1
                continue
            w = cand[0]
            emparejadas += 1
            ctx = f"{a['nombre']} / {w['nombre']}"

            # CA base: extraer el número de nuestra fórmula
            mca = re.match(r"(\d+)", str(a.get("ca")).lstrip("+"))
            inf.comprobados += 1
            if mca and w["ca"] is not None and int(mca.group(1)) != w["ca"]:
                inf.error(f"{ctx}: CA base nuestra {mca.group(1)} vs SRD {w['ca']}")

            # requisito de Fuerza
            inf.comprobados += 1
            nuestra_fue = a.get("fuerza")
            srd_fue = w["fuerza"]
            if bool(nuestra_fue) != bool(srd_fue):
                inf.error(f"{ctx}: requisito de Fuerza nuestro {nuestra_fue!r} "
                          f"vs SRD {srd_fue!r}")
            elif nuestra_fue and srd_fue and int(nuestra_fue) != int(srd_fue):
                inf.error(f"{ctx}: Fuerza nuestra {nuestra_fue} vs SRD {srd_fue}")

    inf.nota(f"{emparejadas} armaduras emparejadas por precio + categoría")
    if ambiguas:
        inf.nota(f"{ambiguas} sin emparejar de forma inequívoca")
    return inf


# ── 13d · Especies ────────────────────────────────────────────────────────
def verificar_especies():
    """Las especies son nombres propios, no reglas: el puente va explícito en
    `_verificacion/glosario_especies.yaml`, con una línea por entrada, para
    que un humano pueda auditarlo de un vistazo. Lo que se contrasta —
    velocidad y tamaño — es numérico."""
    inf = Informe("especies")
    gl_path = B / "_verificacion" / "glosario_especies.yaml"
    if not gl_path.exists():
        inf.nota("falta glosario_especies.yaml — módulo omitido")
        return inf
    glosario = cargar_yaml(gl_path)["especies"]

    por_nombre = {e["nombre"]: e
                  for e in cargar_yaml(B / "especies" / "especies.yaml")["especies"]}
    srd = {reg["name"]: reg["system"] for reg in paquete("origins24", "race")}

    def casillas(metros):
        """1 casilla = 1,5 m = 5 ft. Comparar en casillas evita discutir el
        redondeo que hace la edición española al convertir de pies."""
        return None if metros is None else round(float(metros) / 1.5)

    def vision_oscuridad_m(especie):
        for r in especie.get("rasgos", []):
            if "oscurid" in norm_txt(r.get("nombre")):
                m = re.search(r"(\d+(?:[,.]\d+)?)\s*m", str(r.get("desc", "")))
                return float(m.group(1).replace(",", ".")) if m else None
        return None

    for es, en in glosario.items():
        if en is None:
            continue
        nuestra = por_nombre.get(es)
        if not nuestra:
            inf.error(f"{es}: en el glosario pero no en especies.yaml")
            continue
        s = srd.get(en)
        if s is None:
            inf.error(f"{es}: '{en}' no está en origins24 del SRD")
            continue

        # velocidad
        inf.comprobados += 1
        nuestra_vel = casillas(nuestra.get("velocidad_m"))
        srd_vel = None if (s.get("movement") or {}).get("walk") is None \
            else round(s["movement"]["walk"] / 5)
        if nuestra_vel != srd_vel:
            inf.error(f"{es}/{en}: velocidad nuestra {nuestra.get('velocidad_m')} m "
                      f"({nuestra_vel} casillas) vs SRD "
                      f"{(s.get('movement') or {}).get('walk')} ft "
                      f"({srd_vel} casillas)")

        # visión en la oscuridad
        inf.comprobados += 1
        nuestra_vo = casillas(vision_oscuridad_m(nuestra))
        dv = (s.get("senses") or {}).get("darkvision")
        srd_vo = None if dv is None else round(dv / 5)
        if nuestra_vo != srd_vo:
            inf.error(f"{es}/{en}: visión en la oscuridad nuestra "
                      f"{nuestra_vo} casillas vs SRD {srd_vo} casillas")

    con, sin = ([k for k, v in glosario.items() if v],
                [k for k, v in glosario.items() if not v])
    inf.nota(f"{len(con)} especies contrastadas en velocidad y visión en la "
             f"oscuridad · {len(sin)} sin equivalente en el SRD ({', '.join(sin)})")
    return inf


# ── 13h · Conjuros, los campos que faltaban ───────────────────────────────
_UNIDADES_ES = [
    (r"\basaltos?\b", "asalto"), (r"\bmin\b|\bminutos?\b", "min"),
    (r"\bh\b|\bh\.|\bhoras?\b", "hora"), (r"\bd[ií]as?\b", "dia"),
]


# Igual que EXCEPCIONES_CONJUROS: leídas en la página antes de anotarlas.
EXCEPCIONES_DETALLE = {
    ("Mal de ojo", "alcance"): (
        "el manual dice «Alcance: Lanzador» (pdf 309 = libro 307); el pack del "
        "SRD pone 60 ft, que son los 18 m del efecto («una criatura que puedas "
        "ver a 18 m o menos»), no el alcance del conjuro"),
    ("Alzar a los muertos", "alcance"): (
        "el manual dice «Alcance: Toque» (pdf 243 = libro 241); el pack del SRD "
        "lo marca como Lanzador"),
}


def _cantidad_unidad(texto):
    """'8 horas' -> (8, 'hora') · '1 asalto' -> (1, 'asalto') · 'Instant.' -> None.

    El 'Hasta' de «Hasta 1 minuto» no cambia la cifra: el manual lo usa para
    los conjuros de concentración, que ya se comprueban por su propia bandera.
    """
    t = norm_txt(texto)
    if t.startswith("instant"):
        return (0, "instantaneo")
    if "disipad" in t or "activado" in t:
        return (0, "disipado")
    m = re.search(r"(\d+)", t)
    if not m:
        return None
    for patron, unidad in _UNIDADES_ES:
        if re.search(patron, t):
            return (int(m.group(1)), unidad)
    return None


def verificar_conjuros_detalle():
    """Los 8 campos de `hechizos.json` que la Fase 13 dejó sin contrastar.
    Aquí están los tres que el SRD publica de forma estructurada: alcance,
    duración y tiempo de lanzamiento.

    El alcance en pies se compara **número contra número** (nuestra base ya
    guarda `alcance.pies`), sin vocabulario de por medio. Las unidades de
    duración y los tipos de acción sí llevan vocabulario, y como siempre se
    deduce de los pares y se exige que sea biyección."""
    inf = Informe("conjuros · detalle")
    nuestros = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
    srd = {d["name"]: d["system"] for d in paquete("spells24", "spell")}

    voc_alcance = Vocabulario("unidad de alcance")
    voc_duracion = Vocabulario("unidad de duración")
    voc_accion = Vocabulario("tipo de acción")
    emparejados = 0

    for h in nuestros:
        s = srd.get(h.get("nombre_en"))
        if s is None:
            continue
        emparejados += 1
        ctx = f"{h['nombre']} / {h['nombre_en']}"

        # ── alcance ────────────────────────────────────────────────────────
        r = s.get("range") or {}
        alc = h.get("alcance") or {}
        # algunos alcances del pack son fórmulas de Foundry, no cifras
        # ('15 * pow(2, @scaling.increase)'): esas no son comparables
        if (r.get("units") == "ft"
                and str(r.get("value") or "").strip().isdigit()):
            inf.comprobados += 1
            pies = alc.get("pies")
            motivo = EXCEPCIONES_DETALLE.get((h["nombre"], "alcance"))
            if motivo:
                inf.nota(f"{ctx} · alcance: discrepa del SRD y mandamos "
                         f"nosotros — {motivo}")
            elif pies is None:
                inf.error(f"{ctx}: el SRD da alcance {r['value']} ft y nuestro "
                          f"alcance no tiene cifra ({alc.get('texto')!r})")
            elif int(str(pies).replace(",", ".").split(".")[0]) != int(r["value"]):
                inf.error(f"{ctx}: alcance nuestro {pies} ft vs SRD {r['value']} ft")
        elif r.get("units") in ("self", "touch"):
            # sin cifra: se deduce cómo llamamos nosotros a 'self' y a 'touch'
            if "pies" not in alc and not EXCEPCIONES_DETALLE.get(
                    (h["nombre"], "alcance")):
                voc_alcance.observa(r["units"], norm_txt(alc.get("texto")), ctx)
            elif EXCEPCIONES_DETALLE.get((h["nombre"], "alcance")):
                inf.nota(f"{ctx} · alcance: discrepa del SRD y mandamos "
                         f"nosotros — {EXCEPCIONES_DETALLE[(h['nombre'], 'alcance')]}")

        # ── duración ───────────────────────────────────────────────────────
        d = s.get("duration") or {}
        u, v = d.get("units"), str(d.get("value") or "").strip()
        nuestra = _cantidad_unidad(h.get("duracion"))
        if u and nuestra:
            cant_es, unidad_es = nuestra
            voc_duracion.observa(u, unidad_es, ctx)
            if v.isdigit():
                inf.comprobados += 1
                if int(v) != cant_es:
                    inf.error(f"{ctx}: duración nuestra {h.get('duracion')!r} "
                              f"({cant_es}) vs SRD {v} {u}")

        # ── tiempo de lanzamiento ──────────────────────────────────────────
        a = s.get("activation") or {}
        tipo, val = a.get("type"), a.get("value")
        tl = norm_txt(h.get("tiempo_lanzamiento"))
        if tipo in ("minute", "hour") and val:
            inf.comprobados += 1
            nuestro_tl = _cantidad_unidad(tl)
            if not nuestro_tl or nuestro_tl[0] != int(val):
                inf.error(f"{ctx}: tiempo de lanzamiento nuestro "
                          f"{h.get('tiempo_lanzamiento')!r} vs SRD {val} {tipo}")
        elif tipo in ("action", "bonus", "reaction"):
            # la coletilla ', o ritual' y las condiciones de reacción sobran
            base = re.split(r"\s+o\s+ritual|,", tl)[0].strip()
            voc_accion.observa(tipo, base, ctx)

    for c in (voc_alcance.conflictos() + voc_duracion.conflictos()
              + voc_accion.conflictos()):
        inf.error(c)
    inf.comprobados += (len(voc_alcance.votos) + len(voc_duracion.votos)
                        + len(voc_accion.votos))

    inf.nota(f"{emparejados} conjuros · alcance en pies comparado número contra "
             f"número; {len(voc_alcance.votos)} unidades de alcance, "
             f"{len(voc_duracion.votos)} de duración y {len(voc_accion.votos)} "
             f"tipos de acción deducidos")
    return inf


# ── 13e · Dotes ───────────────────────────────────────────────────────────
def _patron_prerrequisito_srd(prereq):
    """Reduce el prerrequisito del SRD a una etiqueta comparable."""
    if prereq.get("items"):
        return "rasgo:" + ",".join(sorted(prereq["items"]))
    if prereq.get("level"):
        return f"nivel:{prereq['level']}"
    return "ninguno"


def _patron_prerrequisito_nuestro(texto):
    """Lo mismo con nuestra prosa. Deliberadamente tosco: solo distingue las
    cuatro formas que el manual usa, no interpreta el resto de la frase."""
    t = norm_txt(texto)
    if not t:
        return "ninguno"
    m = re.search(r"nivel (\d+)", t)
    if m:
        return f"nivel:{m.group(1)}"
    if "estilo de combate" in t:
        return "rasgo:fighting-style"
    return "otro"


def verificar_dotes():
    """No usa puente de nombres. En el manual, el prerrequisito de una dote lo
    fija su CATEGORÍA (las de origen no piden nada, las generales piden nivel 4,
    los dones épicos nivel 19, los estilos de combate el rasgo homónimo), así
    que se deduce ese patrón de cada lado por separado y se emparejan las
    categorías por su patrón, no por su nombre.

    Es el chequeo que más falta hacía: `FUENTES.md` deja constancia de que el
    OCR devolvía CERO coincidencias de «Prerrequisito» en ese capítulo, así que
    una dote a la que se le haya caído el prerrequisito es el defecto más
    probable — y hasta ahora nada lo comprobaba."""
    inf = Informe("dotes")

    # patrón dominante por subtipo en el SRD
    srd_por_subtipo = collections.defaultdict(collections.Counter)
    for reg in paquete("feats24", "feat"):
        s = reg["system"]
        sub = (s.get("type") or {}).get("subtype")
        if not sub:
            continue        # 'Ability Score Improvement' no lleva subtipo
        srd_por_subtipo[sub][_patron_prerrequisito_srd(s.get("prerequisites") or {})] += 1

    patron_srd = {}
    for sub, c in srd_por_subtipo.items():
        patron, n = c.most_common(1)[0]
        patron_srd[patron] = sub
        if len(c) > 1:
            otros = ", ".join(f"{p}×{k}" for p, k in c.most_common()[1:])
            inf.nota(f"el propio SRD es incoherente en '{sub}': {n} dotes dicen "
                     f"{patron} y {otros} — se toma el mayoritario")

    # patrón dominante por fichero nuestro
    emparejadas = 0
    for f in sorted(glob.glob(str(B / "dotes" / "*.yaml"))):
        d = cargar_yaml(f)
        dotes = d.get("dotes") or []
        if not dotes:
            continue
        patrones = collections.Counter(
            _patron_prerrequisito_nuestro(x.get("prerrequisito")) for x in dotes)
        dominante, n = patrones.most_common(1)[0]
        cat = d.get("categoria", pathlib.Path(f).stem)

        sub = patron_srd.get(dominante)
        if sub is None:
            inf.nota(f"{cat}: patrón {dominante!r} sin equivalente en el SRD "
                     f"(el SRD solo cubre {len(patron_srd)} de nuestras categorías)")
        else:
            emparejadas += 1
            inf.comprobados += 1

        # dentro de la categoría, TODAS deben seguir el patrón dominante
        for x in dotes:
            inf.comprobados += 1
            p = _patron_prerrequisito_nuestro(x.get("prerrequisito"))
            if p != dominante:
                inf.error(f"{cat} · {x['nombre']}: prerrequisito {p!r} "
                          f"({x.get('prerrequisito')!r}) cuando las otras "
                          f"{n} de su categoría dicen {dominante!r}")

    # repetibles: cada dote repetible del SRD debe tener contrapartida repetible
    rep_srd = sum(1 for reg in paquete("feats24", "feat")
                  if (reg["system"].get("prerequisites") or {}).get("repeatable"))
    rep_nuestras = sum(1 for f in glob.glob(str(B / "dotes" / "*.yaml"))
                       for x in (cargar_yaml(f).get("dotes") or [])
                       if x.get("repetible"))
    inf.comprobados += 1
    if rep_nuestras < rep_srd:
        inf.error(f"el SRD marca {rep_srd} dotes repetibles y nosotros solo "
                  f"{rep_nuestras} en toda la base: falta alguna")

    inf.nota(f"{emparejadas} categorías emparejadas por su patrón de "
             f"prerrequisito, sin traducir ningún nombre · "
             f"{rep_nuestras} dotes repetibles nuestras ≥ {rep_srd} del SRD")
    return inf


# ── 13f · Trasfondos ──────────────────────────────────────────────────────
_ABREV = {"str": "Fuerza", "dex": "Destreza", "con": "Constitución",
          "int": "Inteligencia", "wis": "Sabiduría", "cha": "Carisma"}


def verificar_trasfondos():
    """Empareja por el TRÍO DE CARACTERÍSTICAS que ofrece el trasfondo, que en
    el SRD viene como el complemento de `locked` y en nuestra base como
    `caracteristicas`. Los 16 tríos son distintos entre sí, así que la clave es
    única y no hace falta traducir un solo nombre."""
    inf = Informe("trasfondos")
    nuestros = cargar_yaml(B / "trasfondos" / "trasfondos.yaml")["trasfondos"]
    por_trio = {frozenset(t["caracteristicas"]): t for t in nuestros}
    if len(por_trio) != len(nuestros):
        inf.error("dos trasfondos comparten trío de características: la clave "
                  "de emparejamiento deja de ser única")
        return inf

    # Invariante sobre los 16, sin SRD de por medio: la dote que concede un
    # trasfondo es siempre una dote de origen (manual, cap. 4).
    origen = {x["nombre"] for x in cargar_yaml(B / "dotes" / "origen.yaml")["dotes"]}
    for t in nuestros:
        inf.comprobados += 1
        dote = re.sub(r"\s*\(.*\)\s*$", "", str(t.get("dote") or "")).strip()
        if dote not in origen:
            inf.error(f"{t['nombre']}: concede {t.get('dote')!r}, que no está "
                      f"en dotes/origen.yaml")

    voc_hab = Vocabulario("habilidad")
    emparejados = 0
    for reg in paquete("origins24", "background"):
        s = reg["system"]
        adv = s.get("advancement") or []
        asi = next((a for a in adv if a["type"] == "AbilityScoreImprovement"), None)
        if not asi:
            continue
        bloqueadas = set(asi["configuration"].get("locked") or [])
        ofrece = frozenset(v for k, v in _ABREV.items() if k not in bloqueadas)
        nuestro = por_trio.get(ofrece)
        if not nuestro:
            inf.error(f"{reg['name']}: ofrece {sorted(ofrece)} y ningún "
                      f"trasfondo nuestro tiene ese trío")
            continue
        emparejados += 1
        ctx = f"{nuestro['nombre']} / {reg['name']}"

        # oro inicial
        inf.comprobados += 1
        # `wealth` llega como cadena en los packs ('50'), no como número
        oro = s.get("wealth")
        oro = int(oro) if str(oro).strip().isdigit() else None
        m = re.search(r"(\d+)\s*po", norm_txt(nuestro.get("equipo_b")))
        if oro is not None and m and int(m.group(1)) != oro:
            inf.error(f"{ctx}: opción B nuestra {nuestro.get('equipo_b')!r} "
                      f"vs SRD {oro} po")

        # habilidades concedidas: número, y vocabulario deducido
        grants = [g for a in adv if a["type"] == "Trait"
                  for g in (a["configuration"].get("grants") or [])]
        hab_srd = [g.split(":")[-1] for g in grants if g.startswith("skills:")]
        inf.comprobados += 1
        if len(hab_srd) != len(nuestro.get("habilidades") or []):
            inf.error(f"{ctx}: {len(nuestro.get('habilidades') or [])} habilidades "
                      f"nuestras vs {len(hab_srd)} del SRD")
        elif len(hab_srd) == len(nuestro["habilidades"]):
            for a, b in zip(sorted(hab_srd), sorted(nuestro["habilidades"])):
                voc_hab.observa(a, b, ctx)

        # herramienta: presencia/ausencia (el nombre concreto sí sería traducir)
        inf.comprobados += 1
        tiene_srd = any(g.startswith("tool:") for g in grants) or any(
            "tool" in str(c) for a in adv if a["type"] == "Trait"
            for c in (a["configuration"].get("choices") or []))
        if bool(nuestro.get("herramienta")) != tiene_srd:
            inf.error(f"{ctx}: herramienta nuestra {nuestro.get('herramienta')!r} "
                      f"vs SRD {'sí concede' if tiene_srd else 'no concede'}")

    for c in voc_hab.conflictos():
        inf.error(c)

    inf.nota(f"{emparejados} trasfondos emparejados por su trío de "
             f"características (clave única entre los 16, sin traducir nada)")
    inf.nota(f"los 16 comprobados contra el invariante «la dote de un trasfondo "
             f"es siempre de origen»")
    return inf


# ── 13j · Herramientas ────────────────────────────────────────────────────
# Las tres herramientas nuestras que NO emparejan con el SRD, y por qué. Van
# declaradas por nombre a propósito: si una herramienta cualquiera dejara de
# emparejar y esto fuera solo un contador, desaparecería del contraste sin
# avisar — el mismo fallo silencioso del bug `Clerigo`. Con la lista, cualquier
# huérfana no declarada es un error.
HUERFANAS_HERRAMIENTAS = {
    "Instrumento musical":
        "en el manual es una categoría con «Peso: variable» y las variantes "
        "listadas aparte (chirimía, cuerno, dulcémele…); el SRD publica un "
        "registro por instrumento (pdf 223 = libro 221)",
    "Juego":
        "igual que el anterior: categoría con «Peso: —» y variantes (ajedrez "
        "dragón, dados, naipes…) (pdf 223 = libro 221)",
    "Útiles de herborista":
        "el manual dice «Característica: Inteligencia · Peso: 1,5 kg» "
        "(pdf 223 = libro 221) y el SRD publica 8 lb (4 kg). Precio y "
        "característica sí coinciden; manda el manual",
}


def verificar_herramientas():
    """Empareja por (precio, peso), que son números, y desempata por la
    característica cuando hace falta. La característica es lo interesante: es
    un campo que NO entra en la clave de emparejamiento en la mayoría de los
    casos, así que ahí sí se verifica de verdad.

    La conversión de peso es exacta y comprobable: la edición española usa
    1 kg = 2 lb en todo el equipo (verificado en las 37 armas de la Fase 13)."""
    inf = Informe("herramientas")
    d = cargar_yaml(B / "equipo" / "herramientas.yaml")

    srd = collections.defaultdict(list)
    for reg in paquete("equipment24", "tool"):
        s = reg["system"]
        p = s.get("price") or {}
        w = (s.get("weight") or {}).get("value")
        if p.get("denomination") not in _DENOM_A_PC or p.get("value") is None:
            continue
        pc = _DENOM_A_PC[p["denomination"]] * float(p["value"])
        srd[(pc, None if w is None else float(w))].append(
            {"nombre": reg["name"], "ability": s.get("ability")})

    voc = Vocabulario("característica de herramienta")
    unicas, por_caracteristica, ambiguas, huerfanas = [], [], 0, []

    for grupo in ("herramientas_de_artesano", "otras_herramientas"):
        for h in d.get(grupo, []):
            pc = _precio_a_pc(h.get("precio"))
            kg = h.get("peso_kg")
            # algunas entradas nuestras llevan 'variable' en vez de una cifra
            try:
                lb = None if kg is None else float(kg) * 2
            except (TypeError, ValueError):
                lb = "variable"
            cand = [] if lb == "variable" else srd.get((pc, lb), [])
            if not cand:
                motivo = HUERFANAS_HERRAMIENTAS.get(h["nombre"])
                inf.comprobados += 1
                if motivo:
                    huerfanas.append(f"{h['nombre']} — {motivo}")
                else:
                    inf.error(f"{h['nombre']}: sin equivalente en el SRD para "
                              f"(precio {h.get('precio')!r}, peso {kg!r}), y no "
                              f"está declarada como excepción")
                continue
            if len(cand) == 1:
                unicas.append((h, cand[0]))
            else:
                por_caracteristica.append((h, cand))

    # el vocabulario sale solo de las parejas inequívocas
    for h, w in unicas:
        voc.observa(w["ability"], h.get("caracteristica"),
                    f"{h['nombre']} / {w['nombre']}")
    car_es_a_en = {es: en for en, es in voc.resuelto().items()}

    for h, cand in por_caracteristica:
        esperada = car_es_a_en.get(h.get("caracteristica"))
        afinado = [w for w in cand if esperada and w["ability"] == esperada]
        if len(afinado) == 1:
            unicas.append((h, afinado[0]))          # emparejada, no verificable
        elif esperada and not afinado:
            inf.error(f"{h['nombre']}: característica {h.get('caracteristica')!r} "
                      f"({esperada}), y ninguno de sus equivalentes posibles la "
                      f"tiene ({', '.join(w['nombre'] + '=' + str(w['ability']) for w in cand)})")
        else:
            ambiguas += 1

    for c in voc.conflictos():
        inf.error(c)
    inf.comprobados += len(voc.votos) + len(unicas)

    inf.nota(f"{len(unicas)} herramientas emparejadas por (precio, peso) · "
             f"{len(voc.votos)} características deducidas de las inequívocas, "
             f"sin conflictos")
    if ambiguas:
        inf.nota(f"{ambiguas} sin emparejar: comparten precio, peso Y "
                 f"característica con otra")
    for h in huerfanas:
        inf.nota(f"sin equivalente en el SRD, declarada: {h}")
    return inf


def verificar_conjuros_clases():
    """¿Coincide la lista de clases de cada conjuro con la del SRD?

    **Por qué existe.** Lo pidió un defecto real: *Clarividencia* decía
    `["Mago"]` donde la cabecera del manual dice «(bardo, clérigo, hechicero,
    mago)». Tres clases habían desaparecido y **ningún chequeo podía verlo** —
    `verificar_conjuros()` no mira este campo, y el cruce interno
    `hechizos ⊆ clases` de `validar.py` solo detecta nombres de clase que no
    existan, no listas incompletas. *Una lista corta pasa por lista buena*, el
    mismo modo de fallo que los placeholders y que `3d0`. Al escribirlo salió
    un segundo caso, *Engañar*, que un agente había encontrado por su cuenta
    leyendo la página: dos métodos independientes, el mismo hallazgo.

    **La fuente es el SRD 5.2 en Markdown**, no los packs de Foundry: Foundry
    no publica la lista de clases dentro del registro del conjuro (la tiene en
    listas aparte que no vienen en estos packs). Es el mismo SRD 5.2 y la misma
    edición, así que no entra una fuente nueva por la puerta de atrás.

    **No traduce, deduce** (como el resto del script). Los nombres de clase no
    se emparejan por diccionario: para cada clase se toma el **conjunto de
    conjuros que la listan**, y se empareja cada clase castellana con la
    inglesa cuyo conjunto más se le parece (Jaccard), exigiendo que el
    resultado sea una biyección. El margen es enorme y por eso es fiable: la
    peor pareja correcta da 0,974 y la mejor pareja falsa 0,588.
    """
    inf = Informe("conjuros-clases")
    md = B / "_verificacion" / "srd52" / "spells.md"
    if not md.exists():
        inf.error(f"falta {md.relative_to(B)}")
        return inf

    # cabecera del SRD: «_Level 3 Divination (Bard, Cleric, Sorcerer, Wizard)_»
    srd, cur = {}, None
    for ln in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^####\s+(.+?)\s*$", ln)
        if m:
            cur = m.group(1).strip()
            continue
        if cur:
            m2 = re.match(r"^_(?:Level \d|Cantrip)[^(]*\(([^)]*)\)_$", ln.strip())
            if m2:
                srd[cur] = {c.strip() for c in m2.group(1).split(",") if c.strip()}
                cur = None

    nuestros = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
    pares = [(h, srd[h["nombre_en"]]) for h in nuestros if h.get("nombre_en") in srd]
    if not pares:
        inf.error("ningún conjuro emparejó con la lista de clases del SRD: "
                  "el chequeo se ha quedado sin ver la base")
        return inf

    # conjunto de conjuros por clase, a cada lado
    por_es, por_en = collections.defaultdict(set), collections.defaultdict(set)
    for i, (h, cls_en) in enumerate(pares):
        for c in h.get("clases") or []:
            por_es[c].add(i)
        for c in cls_en:
            por_en[c].add(i)

    # deducción del vocabulario por solapamiento, exigiendo biyección
    mapa, usados = {}, {}
    for es, si in sorted(por_es.items()):
        puntuadas = sorted(
            ((len(si & se) / len(si | se), en) for en, se in por_en.items()),
            reverse=True)
        mejor_j, mejor_en = puntuadas[0]
        segundo_j = puntuadas[1][0] if len(puntuadas) > 1 else 0.0
        if mejor_j < 0.7 or mejor_j - segundo_j < 0.2:
            inf.error(f"clase {es!r}: no se deduce a qué clase del SRD "
                      f"corresponde (mejor {mejor_en!r} J={mejor_j:.3f}, "
                      f"segunda J={segundo_j:.3f})")
            continue
        if mejor_en in usados:
            inf.error(f"la deducción de clases no es una biyección: "
                      f"{es!r} y {usados[mejor_en]!r} apuntan ambas a {mejor_en!r}")
            continue
        mapa[es], usados[mejor_en] = mejor_en, es

    if len(mapa) != len(por_es):
        return inf  # sin vocabulario fiable no se compara nada

    inv = {v: k for k, v in mapa.items()}
    for h, cls_en in pares:
        inf.comprobados += 1
        nuestro = {mapa[c] for c in (h.get("clases") or []) if c in mapa}
        falta, sobra = cls_en - nuestro, nuestro - cls_en
        if falta or sobra:
            det = []
            if falta:
                det.append("le falta " + ", ".join(sorted(inv[c] for c in falta)))
            if sobra:
                det.append("le sobra " + ", ".join(sorted(inv[c] for c in sobra)))
            inf.error(f"{h['nombre']} / {h['nombre_en']} (libro "
                      f"{h['fuente']['pagina_libro']}): {'; '.join(det)}")
    return inf


# ── Orquestación ──────────────────────────────────────────────────────────

# ── 19-1 · Clases (bloque H / fase 3 del PLAN_19) ─────────────────────────
#
# `classes24` es el pack más grande que **nadie pedía**: 12 clases con sus
# advancements, 12 subclases y 255 rasgos. El censo (bloque A) lo midió y lo
# declaró como pendiente; esto abre la primera mitad.
#
# Lo que se contrasta aquí son los 12 registros `class`, que traen cuatro
# superficies que ninguna otra fuente cubría:
#
#   · `hd.denomination`      → nuestro `dado_golpe`
#   · `spellcasting`         → nuestro `lanzador`
#   · `wealth`               → el oro de la última opción de equipo inicial
#   · `advancement.ScaleValue` → las columnas numéricas de la progresión,
#     **incluidas las dos que el SRD de Open5e no publica** y que por eso
#     estaban declaradas como pendientes en el censo: `forma_salvaje` del
#     Druida y `mov_sin_armadura_m` del Monje.
#
# El mapa escala→columna es vocabulario de traducción, no cobertura escrita a
# mano: lo que NO se admite es que sobre o falte algo en silencio. Toda escala
# de Foundry tiene que estar mapeada o declarada, y toda columna nuestra tiene
# que estar contrastada o declarada. Lo que quede fuera sale en el informe.

# El mapa clase→nombre inglés **no se copia**: vive en `verificar_srd.MAPA` y
# se lee de allí. Duplicarlo sería el defecto nº 4 del §2 del PLAN_18 otra vez.
_ESCALA_A_COLUMNA = {
    "Rages": "furias",
    "Rage Damage": "dano_furia",
    "Weapon Masteries Known": "maestria_armas",
    "Cantrips Known": "trucos",
    "Max Prepared Spells": "prep",
    "Max Pact Magic Spells": "prep",
    "Inspiration Die": "dado",
    "Channel Divinity Uses": "canalizar",
    "Wild Shape Uses": "forma_salvaje",
    "Second Wind": "tomar_aliento",
    "Martial Arts Die": "artes_marciales",
    "Unarmored Movement": "mov_sin_armadura_m",
    "Focus Points": "puntos_concentracion",
    "Sneak Attack": "ataque_furtivo",
    "Sorcery Points": "puntos_hechiceria",
    "Eldritch Invocations Known": "invocaciones",
}

# Escalas que Foundry modela y nuestra tabla NO tiene como columna.
#
# ⚠ NO son exenciones: son **candidatas a columna que nos falte**, y ésa es
# justamente la clase de hallazgo que este contraste existe para producir. Se
# listan con lo que habría que mirar en la página, y hasta que alguien la lea
# se quedan aquí en vez de desaparecer. Confirmarlas o descartarlas es lectura
# visual, con el protocolo de `CONTINUAR.md` (§ Método de lectura visual).
_ESCALA_SIN_COLUMNA = {
    "Brutal Strike": "Bárbaro · dados de Golpe brutal por nivel",
    "Divine Strike": "Clérigo · dados de Golpe divino por nivel",
    "Wild Shape CR": "Druida · VD máximo de la bestia (0,25 / 0,5 / 1)",
    "Known Forms": "Druida · formas conocidas",
    "Elemental Fury": "Druida · dados de Furia elemental",
    "Action Surge": "Guerrero · usos de Oleada de acción",
    "Indomitable": "Guerrero · usos de Indomable",
    "Aura Distance": "Paladín · alcance del aura, en pies",
}

# Columnas nuestras que Foundry no modela como escala, con su motivo.
_COLUMNA_SIN_ESCALA = {
    "n": "el índice de nivel, no un dato",
    "pb": "el bonificador por competencia; `validar_clase` lo recalcula con la fórmula del manual",
    "slots": "los espacios de conjuro; los contrasta `validar_clase` contra la tabla citada de reglas/generacion_personaje.yaml",
    "espacios": "ídem, la columna del Brujo",
    "nivel_espacios": "nivel de los espacios del Brujo; lo contrasta verificar_srd.py contra 'Slot Level'",
    "enemigo_predilecto": "Explorador; lo contrasta verificar_srd.py contra 'Favored Enemy'",
    "rasgos": "la lista de rasgos, no una cifra",
}

# Celdas concretas en que la escala del SRD discrepa de nuestra tabla y la
# discrepancia está EXPLICADA. Como en `EXCEPCIONES_DETALLE`, cada una dice qué
# evidencia la sostiene — y aquí, además, qué evidencia NO tiene: ninguna de
# estas se ha vuelto a leer en la página, así que se apoyan en lo que la propia
# base ya trae citado. Si algún día se lee y dice otra cosa, manda el manual.
# La clave es (clase, columna, nivel); el valor, la terna
# (lo_nuestro, lo_del_SRD, motivo). Los dos primeros NO son decorado: la
# excepción solo calla si AMBOS lados siguen valiendo exactamente lo que se
# examinó. Si cambia el nuestro, la excepción ya no lo ampara; si cambia el
# del SRD, la fuente externa ha dicho otra cosa y hay que volver a mirar. Sin
# eso, una excepción sería una venda permanente sobre esa celda —justo la
# amenaza nº 3 del FODA: la tolerancia que se vuelve deuda invisible—.
_EXCEPCIONES_ESCALA = {
    ("Monje", "puntos_concentracion", 1): (0, 1, 
        "Foundry modela «Focus Points» como una escala lineal value = nivel, "
        "con 1 en el nivel 1. Nuestra tabla pone 0, y la base lo sostiene "
        "sola: el rasgo que concede los puntos, «Concentración de monje», es "
        "de NIVEL 2 (pdf 151 = libro 149) y su propio texto transcrito dice "
        "«2 en nivel 2, según la columna \"Puntos de concentración\" de la "
        "tabla, hasta 20 en nivel 20». Un monje de nivel 1 no tiene el rasgo, "
        "así que no tiene puntos. La forma de la escala de Foundry —lineal "
        "perfecta de 1 a 20— es la de una fórmula, no la de una columna "
        "impresa con un hueco. NO se ha releído la página para esta celda: la "
        "evidencia es interna y está citada."),
}

# 5 pies = 1,5 m. Es el factor DE JUEGO, el mismo que usa
# `validar_conversiones()`, y no el físico (3,28084): medido sobre la base, el
# de juego deja las conversiones exactas y el físico solo la mitad.
_PIES_POR_METRO = 5 / 1.5


def _escala_expandida(scale, niveles=20):
    """La escala dispersa de Foundry, extendida a los 20 niveles.

    Foundry solo lista los niveles en que el valor CAMBIA; nuestra progresión
    los lista todos, arrastrando el valor y poniendo 0 antes de que empiece.
    """
    out, actual = {}, 0
    puntos = {int(k): v.get("value") for k, v in (scale or {}).items()
              if isinstance(v, dict)}
    for n in range(1, niveles + 1):
        if n in puntos:
            actual = puntos[n]
        out[n] = actual
    return out


def _nuestra_columna(doc, columna):
    return {f["n"]: f.get(columna) for f in (doc.get("progresion") or [])
            if isinstance(f, dict) and "n" in f}


def verificar_clases():
    inf = Informe("clases")
    import verificar_srd as SRD

    # nombre inglés -> stem nuestro, leído del mapa que ya existe
    por_nombre_en = {en: stem for stem, (en, _cols) in SRD.MAPA.items()}
    voc_lanzador = Vocabulario("progresión de lanzador")

    vistas = set()
    for d in paquete("classes24", "class"):
        nom_en = d.get("name")
        stem = por_nombre_en.get(nom_en)
        if stem is None:
            inf.error(f"la clase {nom_en!r} del pack no está en verificar_srd.MAPA: "
                      f"o el SRD trae una clase que no tenemos, o el mapa se quedó corto")
            continue
        vistas.add(stem)
        p = B / "clases" / f"{stem}.yaml"
        if not p.exists():
            inf.error(f"falta clases/{stem}.yaml para la clase {nom_en!r} del pack")
            continue
        doc = cargar_yaml(p)
        ab = (doc.get("atributos_basicos") or {})
        s = d.get("system") or {}
        ctx = f"{doc.get('clase', stem)}"

        # ── dado de golpe ────────────────────────────────────────────────
        hd = (s.get("hd") or {}).get("denomination")
        if hd:
            inf.comprobados += 1
            if str(ab.get("dado_golpe") or "").strip() != str(hd).strip():
                inf.error(f"{ctx}: dado de golpe nuestro "
                          f"{ab.get('dado_golpe')!r} vs SRD {hd!r}")

        # ── tipo de lanzador ─────────────────────────────────────────────
        prog = ((s.get("spellcasting") or {}).get("progression") or "").strip()
        if prog:
            inf.comprobados += 1
            voc_lanzador.observa(prog, str(doc.get("lanzador") or "").strip(), ctx)

        # ── el oro de la última opción de equipo inicial ─────────────────
        # El manual cierra siempre con una opción que es solo oro (lo exige
        # `validar_atributos_basicos`), así que es comparable con `wealth`.
        wealth = s.get("wealth")
        eq = ab.get("equipo_inicial") or {}
        if wealth is not None and eq:
            ultima = str(eq[sorted(eq)[-1]]).strip()
            m = re.fullmatch(r"(\d+)\s*po", ultima)
            inf.comprobados += 1
            if not m:
                inf.error(f"{ctx}: la última opción de equipo es {ultima!r} y no "
                          f"una cifra de oro, así que no se puede contrastar "
                          f"con el `wealth` {wealth} del SRD")
            elif int(m.group(1)) != int(wealth):
                inf.error(f"{ctx}: oro inicial nuestro {m.group(1)} po vs "
                          f"SRD {wealth}")

        # ── las escalas por nivel ────────────────────────────────────────
        nuestras_cols = set()
        for fila in (doc.get("progresion") or []):
            if isinstance(fila, dict):
                nuestras_cols |= set(fila)
        cubiertas = set()
        for a in s.get("advancement") or []:
            if not isinstance(a, dict) or a.get("type") != "ScaleValue":
                # TOLERADO: los demás `advancement` del SRD —competencias,
                # dado de golpe, elección de subclase, concesión de rasgos—
                # no son columnas de la tabla de clase, que es lo único que
                # este bloque contrasta. Lo que sí son columnas nuestras y
                # aquí no aparece lo caza el barrido de abajo
                # (`nuestras_cols - cubiertas`), que no perdona ninguna.
                continue
            titulo = a.get("title")
            columna = _ESCALA_A_COLUMNA.get(titulo)
            if columna is None:
                if titulo not in _ESCALA_SIN_COLUMNA:
                    inf.error(
                        f"{ctx}: el SRD trae la escala {titulo!r} y nadie ha "
                        f"decidido qué columna nuestra es. O se mapea, o se "
                        f"declara como columna que nos falta")
                else:
                    inf.nota(f"{ctx} · el SRD modela {titulo!r} como escala y "
                             f"nuestra tabla no tiene esa columna — "
                             f"{_ESCALA_SIN_COLUMNA[titulo]}. Candidata a "
                             f"columna que falte: pendiente de leer la página")
                continue
            if columna not in nuestras_cols:
                inf.error(f"{ctx}: la escala {titulo!r} debería ser la columna "
                          f"{columna!r} y la progresión no la tiene")
                continue
            cubiertas.add(columna)
            cfg = a.get("configuration") or {}
            esperado = _escala_expandida(cfg.get("scale"))
            unidades = ((cfg.get("distance") or {}).get("units") or "")
            nuestra = _nuestra_columna(doc, columna)
            for n in range(1, 21):
                v_srd, v_nuestro = esperado.get(n), nuestra.get(n)
                if v_srd is None or v_nuestro is None:
                    # TOLERADO: un nivel que una de las dos tablas no lista no
                    # es una discrepancia. Que la columna entera falte sí lo
                    # es, y lo dice el chequeo de arriba.
                    continue
                inf.comprobados += 1
                exc = _EXCEPCIONES_ESCALA.get((ctx, columna, n))
                if exc:
                    esp_nuestro, esp_srd, motivo = exc
                    if (norm_txt(v_nuestro) == norm_txt(esp_nuestro)
                            and norm_txt(v_srd) == norm_txt(esp_srd)):
                        inf.nota(f"{ctx} N{n} · `{columna}`: discrepa del SRD y "
                                 f"mandamos nosotros — {motivo}")
                        continue
                    inf.error(
                        f"{ctx} N{n}: `{columna}` está declarada como excepción "
                        f"para el par (nuestro {esp_nuestro!r}, SRD {esp_srd!r}) "
                        f"y hoy el par es (nuestro {v_nuestro!r}, SRD {v_srd!r}). "
                        f"La excepción ampara UN caso examinado, no la celda: o "
                        f"se vuelve a mirar, o se actualiza la declaración")
                    continue
                if unidades == "ft":
                    # El SRD da pies y nosotros metros: se compara en pies con
                    # el factor de juego, igual que `alcance.pies`.
                    try:
                        propio = float(str(v_nuestro).replace(",", ".")) * _PIES_POR_METRO
                    except ValueError:
                        inf.error(f"{ctx} N{n}: `{columna}` es {v_nuestro!r} y "
                                  f"no es un número")
                        continue
                    if abs(propio - float(v_srd)) > 0.5:
                        inf.error(f"{ctx} N{n}: `{columna}` nuestro {v_nuestro} m "
                                  f"son {propio:g} pies y el SRD da {v_srd}")
                elif norm_txt(v_nuestro) != norm_txt(v_srd):
                    inf.error(f"{ctx} N{n}: `{columna}` nuestro {v_nuestro!r} vs "
                              f"SRD {v_srd!r} (escala {titulo!r})")

        # Y al revés: ninguna columna nuestra puede quedarse sin decidir.
        for col in sorted(nuestras_cols - cubiertas):
            if col in _COLUMNA_SIN_ESCALA:
                # TOLERADO: lo cubre `_COLUMNA_SIN_ESCALA`, que enumera una a
                # una —con su motivo— las columnas nuestras que este pack no
                # publica como escala. Una columna nueva que no esté ahí cae
                # en el `inf.error` de tres líneas más abajo; y una entrada
                # muerta de esa lista la caza `censo.py`, que exige que toda
                # declaración corresponda a algo que existe.
                continue
            _, cols_srd = SRD.MAPA.get(stem, (None, {}))
            if col in cols_srd.values():
                # TOLERADO: lo cubre `verificar_srd.py`, que contrasta esta
                # misma columna contra el mismo pack por otro camino (su
                # `MAPA`). Callar aquí evita contarla dos veces; si dejara de
                # contrastarla, desaparecería de `cols_srd` y esta rama ya no
                # se tomaría.
                continue
            inf.error(f"{ctx}: la columna {col!r} no la contrasta ni "
                      f"`verificar_srd.py` ni ninguna escala de este pack, y "
                      f"no está declarada en `_COLUMNA_SIN_ESCALA`")

    faltan = set(SRD.MAPA) - vistas
    if faltan:
        inf.error(f"clases de nuestra base que el pack no trae: {sorted(faltan)}")
    for c in voc_lanzador.conflictos():
        inf.error(c)
    inf.nota("progresión de lanzador deducida: "
             + ", ".join(f"{en}→{es}" for en, es in sorted(voc_lanzador.resuelto().items())))
    return inf


# ── 13k · Rasgos de clase ─────────────────────────────────────────────────
# El pack agrupa los rasgos de clase en `classes24/<clase>/class-features/`, y
# cada uno declara en `system.prerequisites.level` el nivel al que se obtiene.
# Eso da una fuente externa para lo que hasta hoy solo decía nuestra
# transcripción: QUÉ NIVELES de cada clase conceden rasgo y CUÁNTOS.
#
# Lo que este módulo NO hace, y conviene decirlo antes que nada: **no empareja
# los nombres**. Se probó y no sale. De los 146 rasgos con nivel, la unicidad
# solo fuerza 75 parejas, y de esas solo dos términos ingleses aparecen más de
# una vez —«Epic Boon» y «Channel Divinity»—, así que la biyección no llega a
# exigir nada: sería un diccionario escrito a mano con otro nombre. Se
# contrasta la ESTRUCTURA (nivel a nivel, cuántos rasgos nuevos) que es lo que
# sí tiene dos fuentes independientes.

# Rasgos que el pack publica SIN nivel. No es un descuido nuestro: Foundry los
# concede por otra vía (una elección, un `advancement` de la clase) y no les
# pone `prerequisites.level`. Sin nivel no hay nada que contrastar, así que se
# enumeran uno a uno —si el pack añade otro, el chequeo lo canta— y se dice
# quién responde por cada uno.
_RASGO_SIN_NIVEL = {
    ("guerrero", "Weapon Mastery"): "nuestra tabla lo pone en N1 y el pack no le da nivel; el dato que sí contrasta es la columna `maestria_armas`, que va por escala",
    ("paladin", "Fighting Style"): "el pack lo concede como elección de estilo sin nivel; nuestra tabla lo pone en N2",
    ("explorador", "Extra Attack"): "sin nivel en el pack; nuestra tabla lo pone en N5, igual que guerrero y monje, donde el pack sí lo fecha",
    ("explorador", "Fighting Style"): "ídem que en paladín: elección de estilo sin nivel; nuestra tabla lo pone en N2",
    ("picaro", "Slippery Mind"): "sin nivel en el pack; nuestra tabla lo pone en N15",
}

# Niveles en que las dos fuentes cuentan distinto, con el par EXACTO que se
# examinó. Igual que `_EXCEPCIONES_ESCALA`: la declaración ampara ese par y no
# la casilla, así que si cualquiera de los dos lados cambia, la excepción deja
# de tapar y hay que volver a mirar. Ninguna de estas se ha releído en la
# página; la evidencia es la que se cita en cada una.
_EXCEPCIONES_RASGOS = {
    ("bardo", 9): (
        (), ("Pericia",),
        "el manual concede Pericia dos veces (N2 y N9) y el pack la publica "
        "como un solo rasgo fechado en N2; nuestra tabla lista las dos "
        "concesiones. Granularidad del pack, no dato distinto"),
    ("guerrero", 1): (
        ("Fighting Style", "Second Wind"),
        ("Estilo de combate", "Maestría con armas", "Tomar aliento"),
        "sobra `Maestría con armas`, que el pack publica sin nivel (ver "
        "`_RASGO_SIN_NIVEL`); los otros dos coinciden"),
    ("guerrero", 13): (
        ("Studied Attacks",), ("Ataques estudiados", "Indómito (dos usos)"),
        "sobra la mejora de `Indómito`, que nuestra tabla lista como entrada "
        "propia en cada nivel en que sube y el pack modela como un solo rasgo "
        "con usos crecientes"),
    ("guerrero", 17): (
        (), ("Acción súbita (dos usos)", "Indómito (tres usos)"),
        "las dos son mejoras de rasgos ya obtenidos; ver la excepción de N13"),
    ("monje", 3): (
        ("Deflect Attacks", "Deflect Energy"), ("Desviar ataques",),
        "el pack fecha `Deflect Energy` en N3 junto con `Deflect Attacks`; "
        "nuestra tabla la pone en N13 como rasgo propio. Es la misma "
        "discrepancia que la excepción de («monje», 13), y las dos siguen "
        "PENDIENTES DE LEER LA PÁGINA: hasta entonces mandamos nosotros, "
        "porque `Desviar energía` está transcrito con su página citada"),
    ("monje", 10): (
        ("Heightened Focus",), ("Autorrestablecimiento", "Concentración agudizada"),
        "el pack no trae `Self-Restoration` en ningún nivel: es un hueco SUYO, "
        "no nuestro. Nuestro `Autorrestablecimiento` está transcrito con "
        "página citada"),
    ("monje", 13): (
        (), ("Desviar energía",),
        "la otra mitad de la excepción de («monje», 3): el pack la fecha en N3 "
        "y nosotros en N13. Pendiente de leer la página"),
    ("explorador", 5): (
        (), ("Ataque adicional",),
        "`Extra Attack` lo publica el pack sin nivel (ver `_RASGO_SIN_NIVEL`)"),
    ("explorador", 13): (
        (), ("Cazador persistente",),
        "el pack fecha `Relentless Hunter` en N14 y nuestra tabla en N13. Es "
        "la misma discrepancia que («explorador», 14) y está PENDIENTE DE LEER "
        "LA PÁGINA; hasta entonces mandamos nosotros, con la transcripción "
        "citada"),
    ("explorador", 14): (
        ("Nature's Veil", "Relentless Hunter"), ("Velo de la naturaleza",),
        "la otra mitad de la discrepancia de N13. `Velo de la naturaleza` sí "
        "coincide en N14"),
    ("picaro", 2): (
        ("Cunning Action", "Cunning Strike"), ("Acción astuta",),
        "el pack fecha `Cunning Strike` en N2 y nuestra tabla en N5. Misma "
        "discrepancia que («picaro», 5), PENDIENTE DE LEER LA PÁGINA"),
    ("picaro", 5): (
        ("Uncanny Dodge",), ("Esquiva asombrosa", "Golpe astuto"),
        "`Esquiva asombrosa` coincide; sobra `Golpe astuto`, la otra mitad de "
        "la discrepancia de N2"),
    ("picaro", 6): (
        (), ("Pericia",),
        "segunda concesión de Pericia, como en bardo N9: el pack publica una "
        "sola, fechada en N1"),
    ("picaro", 15): (
        (), ("Mente escurridiza",),
        "`Slippery Mind` lo publica el pack sin nivel (ver `_RASGO_SIN_NIVEL`)"),
    ("brujo", 13): (
        (), ("Arcanum místico (conjuro de nivel 7)",),
        "el pack publica `Mystic Arcanum` como un solo rasgo fechado en N11; "
        "nuestra tabla lista las cuatro concesiones (N11, N13, N15, N17), una "
        "por nivel de conjuro. Granularidad del pack"),
    ("brujo", 15): (
        (), ("Arcanum místico (conjuro de nivel 8)",),
        "ver la excepción de («brujo», 13)"),
    ("brujo", 17): (
        (), ("Arcanum místico (conjuro de nivel 9)",),
        "ver la excepción de («brujo», 13)"),
}


def _indexa_rasgos(registros):
    """Los rasgos de clase del pack, indexados por carpeta y nivel, con el
    nombre COLAPSADO en los dos puntos: el pack publica las opciones de un
    rasgo como registros hermanos («Divine Order», «Divine Order: Protector»,
    «Divine Order: Thaumaturge») y nuestra tabla concede un rasgo, no tres."""
    por_nivel = collections.defaultdict(lambda: collections.defaultdict(set))
    sin_nivel = collections.defaultdict(set)
    for d in registros:
        carpeta = pathlib.Path(d["_ruta"]).parts[-3]
        nivel = ((d.get("system") or {}).get("prerequisites") or {}).get("level")
        nombre = str(d.get("name") or "").split(":")[0].strip()
        if nivel is None:
            sin_nivel[carpeta].add(nombre)
        else:
            por_nivel[carpeta][nivel].add(nombre)
    return por_nivel, sin_nivel


def verificar_rasgos_clase():
    inf = Informe("rasgos de clase")
    import verificar_srd as SRD
    por_nombre_en = {en: stem for stem, (en, _cols) in SRD.MAPA.items()}

    # carpeta del pack -> stem nuestro, deducido del registro `class` que hay
    # en cada una; no se escribe a mano en ningún sitio.
    carpeta_a_stem = {}
    for d in paquete("classes24", "class"):
        stem = por_nombre_en.get(d.get("name"))
        if stem is not None:
            carpeta_a_stem[pathlib.Path(d["_ruta"]).parts[-2]] = stem

    idx_nivel, idx_sin = _indexa_rasgos(
        paquete("classes24", "feat", sub="class-features"))

    usadas_exc, usadas_sn = set(), set()
    for carpeta, stem in sorted(carpeta_a_stem.items()):
        p = B / "clases" / "rasgos" / f"{stem}.yaml"
        if not p.exists():
            inf.error(f"falta clases/rasgos/{stem}.yaml")
            continue
        doc = cargar_yaml(p)
        ctx = str(doc.get("clase") or stem)
        nuestros = collections.defaultdict(list)
        for r in (doc.get("rasgos") or []):
            if isinstance(r, dict) and "nivel" in r:
                nuestros[r["nivel"]].append(str(r.get("nombre") or ""))

        por_nivel, sin_nivel = idx_nivel[carpeta], idx_sin[carpeta]
        for nombre in sorted(sin_nivel):
            if (stem, nombre) in _RASGO_SIN_NIVEL:
                # TOLERADO: lo cubre `_RASGO_SIN_NIVEL`, que enumera uno a uno
                # —con su motivo— los rasgos que el pack publica sin fecha. Uno
                # nuevo cae en el `inf.error` de aquí abajo, y una entrada
                # muerta la caza el recuento del final de la función.
                usadas_sn.add((stem, nombre))
                continue
            inf.error(f"{ctx}: el pack publica el rasgo {nombre!r} sin nivel y "
                      f"nadie ha dicho quién responde por él. O se contrasta, "
                      f"o se declara en `_RASGO_SIN_NIVEL`")

        for n in sorted(set(por_nivel) | set(nuestros)):
            suyos = tuple(sorted(por_nivel.get(n, ())))
            mios = tuple(sorted(nuestros.get(n, ())))
            if not suyos and not mios:
                # TOLERADO: un nivel que ninguna de las dos fuentes usa no es
                # un nivel; aparece solo porque el bucle recorre la unión.
                continue
            exc = _EXCEPCIONES_RASGOS.get((stem, n))
            if exc:
                esp_s, esp_m, motivo = exc
                usadas_exc.add((stem, n))
                if suyos == tuple(sorted(esp_s)) and mios == tuple(sorted(esp_m)):
                    inf.nota(f"{ctx} N{n} · el pack y nuestra tabla cuentan "
                             f"distinto y está declarado — {motivo}")
                    continue
                inf.error(
                    f"{ctx} N{n}: hay una excepción declarada para el par "
                    f"(pack {tuple(esp_s)}, nuestro {tuple(esp_m)}) y hoy el "
                    f"par es (pack {suyos}, nuestro {mios}). La excepción "
                    f"ampara lo que se examinó, no el nivel: o se vuelve a "
                    f"mirar, o se actualiza la declaración")
                continue
            if len(suyos) != len(mios):
                inf.error(
                    f"{ctx} N{n}: el pack concede {len(suyos)} rasgo(s) "
                    f"{suyos} y nuestra tabla {len(mios)} {mios}")
                continue
            # Cuadran: cada rasgo del pack es una afirmación contrastada sobre
            # a qué nivel concede rasgo esta clase, y cuántos.
            inf.comprobados += len(suyos)

    muertas = set(_EXCEPCIONES_RASGOS) - usadas_exc
    if muertas:
        inf.error(f"excepciones de `_EXCEPCIONES_RASGOS` que ya no "
                  f"corresponden a ningún nivel: {sorted(muertas)}. Una "
                  f"declaración muerta es una venda que nadie ve")
    muertas_sn = set(_RASGO_SIN_NIVEL) - usadas_sn
    if muertas_sn:
        inf.error(f"entradas de `_RASGO_SIN_NIVEL` que el pack ya no publica "
                  f"sin nivel: {sorted(muertas_sn)}")
    return inf


MODULOS = {
    "conjuros": verificar_conjuros,
    "conjuros-detalle": verificar_conjuros_detalle,
    "conjuros-clases": verificar_conjuros_clases,
    "armas": verificar_armas,
    "armaduras": verificar_armaduras,
    "especies": verificar_especies,
    "dotes": verificar_dotes,
    "trasfondos": verificar_trasfondos,
    "herramientas": verificar_herramientas,
    "clases": verificar_clases,
    "rasgos-clase": verificar_rasgos_clase,
}


def main():
    if not FOUNDRY.exists():
        sys.exit(f"✗ falta {FOUNDRY} (ver _verificacion/LEEME.md)")

    pedidos = sys.argv[1:] or list(MODULOS)
    for p in pedidos:
        if p not in MODULOS:
            sys.exit(f"✗ módulo desconocido: {p!r} (hay: {', '.join(MODULOS)})")

    print("Contraste contra SRD 5.2 estructurado (CC-BY-4.0 · packs dnd5e de Foundry)")
    print("─" * 74)
    total_ok = total_err = 0
    for p in pedidos:
        inf = MODULOS[p]()
        inf.imprime()
        total_ok += inf.comprobados
        total_err += len(inf.errores)
    print("─" * 74)
    print(f"{total_ok} valores contrastados · "
          + ("✅ 0 discrepancias" if not total_err else f"❌ {total_err} discrepancias"))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
