#!/usr/bin/env python3
"""Calculadora determinista de la base canónica D&D 2024 (5.5e).

Ninguna de estas cuentas las hace el LLM "a mente": las hace este script,
para que el resultado sea siempre el mismo dado el mismo input y quede
citado de dónde sale cada fórmula. Uso como librería (import) o CLI:

    python3 calculo.py pg --dado d8 --con 14
    python3 calculo.py ca --clase Monje --des 16 --sab 14
    python3 calculo.py cd-conjuros --aptitud 3 --nivel 1
"""
import argparse
import functools
import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

B = pathlib.Path(__file__).parent


@functools.lru_cache(maxsize=None)
def cargar(rel):
    """Lee un fichero de la base. **El resultado se cachea y se comparte.**

    Medido el 2026-08-31 con cProfile sobre `validar.py`: el **98 % del tiempo**
    se iba en `yaml.safe_load`, con 1068 parseos de los mismos ficheros. Solo
    `validar_subida()` gastaba 34 s releyendo las tablas de clase 333 veces,
    una por salto de nivel.

    **Contrato: lo devuelto es de SOLO LECTURA.** Todos los llamadores actuales
    lo respetan (comprobado: ninguno asigna ni muta sobre el resultado). Si
    alguna vez hace falta modificarlo, cópialo primero.

    **Por qué es seguro con las pruebas por mutación:** copian la base a un
    directorio temporal y lanzan `validar.py` en SUBPROCESO, así que cada
    mutación estrena caché. Una caché de proceso no puede servir datos viejos
    a la mutación siguiente.
    """
    f = B / rel
    if not f.exists():
        sys.exit(f"✗ no existe: {rel}")
    if f.suffix == ".json":
        return json.loads(f.read_text(encoding="utf-8"))
    return yaml.safe_load(f.read_text(encoding="utf-8"))


# ── Marcadores de la tabla de clase ─────────────────────────────────────
# «Mejora de característica», «Rasgo de subclase» y «Subclase de <clase>» no
# son rasgos con texto propio: son instrucciones de la tabla, y su vocabulario
# vive en `reglas/subida_de_nivel.yaml → marcadores` con su nota al lado.
#
# Hasta el 2026-09-02 había DOS copias cableadas de esa lista, una en
# `validar.py` y otra en `subir_nivel.py`, y **ya habían divergido**: la
# primera normalizaba con `.strip()` y exigía «Subclase de » con espacio final;
# la segunda no normalizaba y aceptaba «Subclase de» sin él, así que un rasgo
# llamado «Subclase deluxe» era marcador para una y rasgo para la otra. Es el
# defecto nº 4 del §2 del PLAN_18 (`_TABLA_COSTE`) otra vez: un dato que vive
# en la base, copiado en Python, y nadie comparando las copias.
#
# Ahora se lee. Añadir un cuarto marcador al YAML lo reconocen los dos sin
# tocar código, y quitarlo lo deja de reconocer en los dos a la vez.
@functools.lru_cache(maxsize=None)
def _marcadores():
    d = cargar("reglas/subida_de_nivel.yaml") or {}
    literales, patrones = set(), []
    for m in d.get("marcadores") or []:
        if isinstance(m, str):
            literales.add(m.strip())
        elif isinstance(m, dict) and m.get("patron"):
            # «Subclase de <clase>» → prefijo «Subclase de », con su espacio.
            patrones.append(m["patron"].split("<", 1)[0])
        else:
            sys.exit(f"✗ marcador no reconocido en reglas/subida_de_nivel.yaml: "
                     f"{m!r}. Un marcador es un literal o un `patron` con <…>")
    if not literales and not patrones:
        sys.exit("✗ reglas/subida_de_nivel.yaml no declara `marcadores`: sin "
                 "ellos no se distingue una instrucción de la tabla de un "
                 "rasgo con texto propio")
    return frozenset(literales), tuple(patrones)


def es_marcador(nombre):
    """¿Es una instrucción de la tabla y no un rasgo con texto propio?"""
    n = (nombre or "").strip()
    literales, patrones = _marcadores()
    return n in literales or any(n.startswith(pref) for pref in patrones)


# ── Los marcadores, uno a uno y por su nombre ────────────────────────────
# `es_marcador()` responde «¿esto es UN marcador?». Pero la auditoría del
# 2026-09-03 encontró que siete sitios no preguntan eso: preguntan «¿es ESTE
# marcador?» —el de mejora, el de subclase— y para distinguirlos volvían a
# escribir la cadena a mano, con `es_marcador()` leyendo la base al lado sin
# que nadie la usara para esto. Detectar el marcador y despacharlo eran dos
# listas, y solo una se leía.
#
# La base ya los tiene CON NOMBRE: `concesiones`/`elecciones` de
# `reglas/subida_de_nivel.yaml` traen un campo `marcador` bajo una clave
# semántica (`rasgo_de_subclase`, `subclase`, `mejora_caracteristica_o_dote`),
# que además es la misma cadena que `subir_nivel.py` ya emite como `tipo`.
#
# Y el índice se CONTRASTA contra la lista plana `marcadores` en vez de
# confiar en ella: son el mismo dato escrito dos veces DENTRO de la base, y
# hasta hoy nadie las comparaba. Si divergen, se para.
@functools.lru_cache(maxsize=None)
def _marcadores_con_nombre():
    d = cargar("reglas/subida_de_nivel.yaml") or {}
    idx = {}
    for bloque in ("concesiones", "elecciones"):
        for clave, cuerpo in (d.get(bloque) or {}).items():
            if isinstance(cuerpo, dict) and cuerpo.get("marcador"):
                idx[clave] = str(cuerpo["marcador"]).strip()
    if not idx:
        sys.exit("✗ reglas/subida_de_nivel.yaml no da nombre a ningún marcador "
                 "en `concesiones`/`elecciones`: sin eso no se puede pedir uno "
                 "concreto sin volver a escribirlo a mano")
    literales, patrones = _marcadores()
    for clave, m in sorted(idx.items()):
        if not (m in literales or any(m.startswith(p) for p in patrones)):
            sys.exit(f"✗ reglas/subida_de_nivel.yaml se contradice: "
                     f"{_bloque_de(clave)}«{clave}» declara el marcador «{m}» y "
                     f"la lista `marcadores` no lo reconoce. Son el mismo dato "
                     f"escrito dos veces y han divergido")
    return idx


def _bloque_de(clave):
    """Solo para el mensaje de error de arriba: en qué bloque vive la clave."""
    d = cargar("reglas/subida_de_nivel.yaml") or {}
    for bloque in ("concesiones", "elecciones"):
        if clave in (d.get(bloque) or {}):
            return f"{bloque}."
    return ""


def marcador(clave):
    """El literal del marcador que la base llama `clave`, leído de la base."""
    idx = _marcadores_con_nombre()
    if clave not in idx:
        sys.exit(f"✗ reglas/subida_de_nivel.yaml no declara ningún marcador "
                 f"llamado «{clave}». Los que hay: {', '.join(sorted(idx))}")
    return idx[clave]


def es_marcador_de(clave, nombre):
    """¿`nombre` es el marcador que la base llama `clave`?

    Respeta la forma que declare la base: un `patron` con `<…>` compara por
    prefijo («Subclase de <clase>» → «Subclase de »), un literal compara
    entero. Así el «Subclase deluxe» que ya hizo divergir dos copias en la
    Fase 16 no puede volver a colarse por un lado y no por el otro.
    """
    m = marcador(clave)
    n = (nombre or "").strip()
    return n.startswith(m.split("<", 1)[0]) if "<" in m else n == m


# ── Modificador por puntuación ──────────────────────────────────────────
# reglas/generacion_personaje.yaml → modificadores_por_puntuacion
def modificador(puntuacion):
    """(puntuación - 10) / 2, redondeando hacia abajo."""
    import math
    return math.floor((puntuacion - 10) / 2)


# ── Compra por puntos ────────────────────────────────────────────────────
# reglas/generacion_personaje.yaml → metodos_generacion_caracteristicas.coste_en_puntos
#
# La tabla SE LEE de la base; no se copia aquí. Hasta el 2026-08-31 estaba
# cableada como `_TABLA_COSTE = {8:0, 9:1, ...}` **con este mismo comentario
# encima señalando el YAML**, y las dos copias no las contrastaba nadie:
# `validar.py` validaba la del YAML y `calculo.py` calculaba con la suya. Una
# corrección en la base habría dejado la aritmética con los valores viejos y
# todo en verde. Es el mismo defecto que `_CA_SIN_ARMADURA` y `_ORIGENES`, en
# el núcleo aritmético. Regla inviolable 6 de CONTINUAR.md.
def _tabla_coste():
    cp = cargar("reglas/generacion_personaje.yaml")[
        "metodos_generacion_caracteristicas"]["coste_en_puntos"]
    return {int(k): v for k, v in cp["tabla_coste"].items()}


def puntos_totales():
    """El presupuesto de la compra por puntos, leído de la base.

    La ironía del 2026-09-03: la tabla de arriba se arregló para que se leyera,
    con once líneas de comentario explicando por qué, y el TOTAL que la
    acompaña —dos líneas más arriba en el mismo bloque del YAML— se quedó
    cableado como `!= 27` en `verificar_personaje.py` y como dos literales en
    el `main` de aquí abajo.
    """
    cp = cargar("reglas/generacion_personaje.yaml")[
        "metodos_generacion_caracteristicas"]["coste_en_puntos"]
    if "puntos_totales" not in cp:
        sys.exit("✗ reglas/generacion_personaje.yaml no declara "
                 "`coste_en_puntos.puntos_totales`: sin él no hay presupuesto "
                 "contra el que comprobar una compra por puntos")
    return int(cp["puntos_totales"])


def coste_compra_puntos(scores):
    """Suma el coste de las 6 puntuaciones. Lanza si alguna está fuera de tabla."""
    tabla = _tabla_coste()
    total = 0
    for car, val in scores.items():
        if val not in tabla:
            sys.exit(f"✗ {car}={val} fuera del rango de compra por puntos "
                     f"({min(tabla)}-{max(tabla)})")
        total += tabla[val]
    return total


def ajustar_por_trasfondo(base, ajuste):
    """Aplica el ajuste del trasfondo (+2/+1 o +1/+1/+1), tope 20."""
    final = dict(base)
    for car, delta in ajuste.items():
        final[car] = min(20, final.get(car, 0) + delta)
    return final


# ── Puntos de golpe ──────────────────────────────────────────────────────
# Manual_del_Jugador_2024.pdf pdf 42 = libro 40, tabla
# "Puntos de golpe en el nivel 1 por clase": PG nivel 1 = MÁXIMO del dado
# de golpe (12/10/8/6 según clase) + modificador por Constitución. El
# máximo del dado coincide siempre con el número de caras (d12 -> 12, etc.).
def puntos_golpe_nivel_1(dado_golpe, con_mod):
    caras = int(dado_golpe.lstrip("d"))
    return caras + con_mod


# ── Puntos de golpe de los niveles 2+ ────────────────────────────────────
# reglas/generacion_personaje.yaml → puntos_golpe.niveles_siguientes_al_1
# (pdf 44 = libro 42, "Subir de nivel", paso 2). Verificado por dos lectores
# independientes; ver FUENTES.md.
#
# Dos métodos, y el jugador elige por nivel:
#   · tirar el dado de golpe, o
#   · usar el valor establecido de la tabla "Puntos de golpe establecidos por
#     clase" (que resulta ser el promedio del dado redondeado hacia arriba).
# En ambos se suma el modificador por Constitución, **con un mínimo de 1 en el
# TOTAL** — no en el dado.
def valor_establecido_pg(clase):
    """El valor fijo por nivel de una clase, leído de la base (nunca calculado
    como (caras/2)+1: esa coincidencia es lo que `validar_puntos_golpe()` usa
    para CONTRASTAR las dos transcripciones, y calcularla aquí destruiría el
    contraste dejando una sola fuente)."""
    g = cargar("reglas/generacion_personaje.yaml")
    tabla = g["puntos_golpe"]["niveles_siguientes_al_1"]["tabla_valores_establecidos"]
    for fila in tabla["filas"]:
        if clase in fila["clases"]:
            return fila["valor"]
    sys.exit(f"✗ {clase!r} no aparece en la tabla «{tabla['titulo']}»")


def pg_de_subida(valor, con_mod):
    """PG que aporta UN nivel posterior al 1. `valor` es el resultado del dado
    o el valor establecido; el mínimo de 1 es del total."""
    return max(1, valor + con_mod)


def pg_max_de_ficha(ficha, con_mod, dado_golpe_nivel_1):
    """PG máximos por acumulación de la historia de la ficha.

    **Se recalcula entero desde los valores crudos, siempre.** Es lo que hace
    que la regla retroactiva del paso 5 —«cuando tu modificador por Constitución
    aumente en 1, tus puntos de golpe máximos también aumentarán en 1 por cada
    nivel que hayas alcanzado»— salga sola, en vez de tener que aplicarse a
    mano sobre un total ya guardado. Un motor que sumara «lo ganado en el nivel
    N» y lo guardara acertaría hasta la primera dote que subiera Constitución.

    Devuelve `(pg, avisos)`. Los avisos existen porque hay un caso que **la base
    no resuelve**: si algún nivel toca el mínimo de 1, el paso 2 (mínimo por
    nivel) y el paso 5 (+1 por nivel alcanzado) dejan de decir lo mismo, y
    ninguna página leída dice cuál manda. Se avisa en vez de elegir en silencio.
    """
    historia = ficha.get("pg_por_nivel")
    if not historia:
        # Sin historia declarada solo se puede responder por el nivel 1.
        if ficha["nivel_total"] != 1:
            sys.exit(f"✗ la ficha es de nivel {ficha['nivel_total']} y no declara "
                     f"`pg_por_nivel`: los PG de los niveles 2+ son una ELECCIÓN "
                     f"del jugador (tirar o valor establecido) y no se pueden "
                     f"deducir. Ver personajes/_ESQUEMA.md")
        return puntos_golpe_nivel_1(dado_golpe_nivel_1, con_mod), []

    niveles = sorted(e["nivel"] for e in historia)
    if niveles != list(range(1, ficha["nivel_total"] + 1)):
        sys.exit(f"✗ `pg_por_nivel` debe tener una entrada por nivel, del 1 al "
                 f"{ficha['nivel_total']}; tiene {niveles}")

    total, avisos = 0, []
    for e in sorted(historia, key=lambda x: x["nivel"]):
        if e["nivel"] == 1:
            # El nivel 1 es OTRA regla, en otra página (pdf 42 = libro 40):
            # máximo del dado. No es "subir de nivel", así que no le consta
            # mínimo; si la página lo dijera, iría aquí citado.
            total += puntos_golpe_nivel_1(dado_golpe_nivel_1, con_mod)
            continue
        aporta = pg_de_subida(e["valor"], con_mod)
        if e["valor"] + con_mod < 1:
            avisos.append(
                f"nivel {e['nivel']}: el mínimo de 1 se aplica ({e['valor']} "
                f"{con_mod:+d} = {e['valor']+con_mod}). La base NO resuelve qué "
                f"pasa entonces con la regla retroactiva del paso 5; queda "
                f"declarado como límite conocido")
        total += aporta
    return total, avisos


# ── Bonificador por competencia ──────────────────────────────────────────
def bonificador_competencia(nivel_total):
    tabla = cargar("reglas/generacion_personaje.yaml")["px_por_nivel"]["filas"]
    for fila in tabla:
        if fila["nivel"] == nivel_total:
            return fila["pb"]
    sys.exit(f"✗ nivel_total {nivel_total} fuera de la tabla px_por_nivel (1-20)")


# ── Percepción pasiva ─────────────────────────────────────────────────────
# pdf 42 = libro 40: "Percepción pasiva = 10 + modificador para pruebas de
# Sabiduría (Percepción)"
def percepcion_pasiva(sab_mod, competente=False, pb=0, pericia=False):
    bonif = 0
    if pericia:
        bonif = 2 * pb
    elif competente:
        bonif = pb
    return 10 + sab_mod + bonif


# ── Clase de armadura ─────────────────────────────────────────────────────
# FASE 14: aquí vivía `_CA_SIN_ARMADURA`, un diccionario de `lambda` indexado
# por nombre de clase con el Bárbaro y el Monje. Su comentario decía "las dos
# únicas excepciones EN EL TRONCO DE CLASE (confirmado por grep sobre las 12
# clases)" — y era verdad, y por eso mismo era el problema: la base tiene
# CUATRO fórmulas de CA base, y las otras dos están en SUBCLASES (*Juego de
# pies deslumbrante* del Bardo, pdf 66; *Resistencia dracónica* del Hechicero,
# pdf 135). El grep miró donde el `lambda` sabía mirar.
#
# Ahora cada fórmula es un efecto citado junto a su rasgo, y las agrega
# `efectos.py`. Esta función se queda con lo que NO depende de rasgos —
# armadura y escudo — y **se niega a responder** cuando la respuesta dependería
# de un rasgo, en vez de devolver 10 + Des como si tal cosa.
_RE_CA_FORMULA = re.compile(
    r"^(\d+)(?:\s*\+\s*mod\.\s*Des(?:\s*\(máx\.\s*(\d+)\))?)?$"
)


def ca(des_mod, con_mod=0, sab_mod=0, clase=None, armadura=None, escudo=False):
    """Calcula CA. Si `armadura` es un nombre, se busca en equipo/armaduras.yaml
    y se parsea su fórmula. Si `armadura` es None, se usa la Defensa sin
    armadura de la clase (si la tiene) o 10 + mod Des por defecto."""
    if armadura:
        d = cargar("equipo/armaduras.yaml")
        entrada = None
        for grupo in ("armaduras_ligeras", "armaduras_medias", "armaduras_pesadas"):
            for a in d[grupo]["tabla"]:
                if a["nombre"].lower() == armadura.lower():
                    entrada = a
                    break
            if entrada:
                break
        if not entrada:
            sys.exit(f"✗ armadura desconocida: {armadura!r} "
                      f"(no está en equipo/armaduras.yaml)")
        formula = str(entrada["ca"])
        m = _RE_CA_FORMULA.match(formula)
        if not m:
            sys.exit(f"✗ fórmula de CA no reconocida: {formula!r}")
        base = int(m.group(1))
        if "mod. Des" in formula:
            tope = int(m.group(2)) if m.group(2) else None
            aplicado = min(des_mod, tope) if tope is not None else des_mod
            base += aplicado
        valor = base
    else:
        if clase:
            _archivo_clase(clase)  # valida el nombre (falla si está mal escrito)
            if _tiene_ca_de_rasgo(clase):
                sys.exit(
                    f"✗ la CA de {clase} sin armadura la fija un rasgo con "
                    f"efecto declarado; esta función no puede saber si el "
                    f"personaje lo tiene (nivel, subclase, escudo).\n"
                    f"  Usa la ficha: efectos.calcular_de_ficha(...) — o "
                    f"`python3 verificar_personaje.py <ficha>`.")
        valor = 10 + des_mod

    if escudo:
        d = cargar("equipo/armaduras.yaml")
        escudo_entrada = d["escudos"]["tabla"][0]
        valor += int(escudo_entrada["ca"].replace("+", ""))
    return valor


# ── Conjuros: CD y bonificador de ataque ─────────────────────────────────
# El `8` SE LEE de `reglas/generacion_personaje.yaml → conjuros`, citado en
# pdf 240 = libro 238. Hasta el 2026-09-05 estaba cableado aquí con la cita en
# este mismo comentario, que es exactamente donde una regla no puede vivir:
# cableada no se puede citar, ni validar, ni corregir cuando la base cambia.
#
# Lo destapó el mandato «el calculista» de la ronda 3 de estrés: dos agentes
# independientes, calculando a mano dos fichas distintas, pararon en el mismo
# sitio porque la base no definía la fórmula. Es el mismo patrón que
# `_TABLA_COSTE`, `COMPLETO`/`MEDIO` y el tope de 20 de las mejoras.
@functools.lru_cache(maxsize=1)
def _regla_de_conjuros():
    c = cargar("reglas/generacion_personaje.yaml").get("conjuros")
    if not c:
        sys.exit("✗ `reglas/generacion_personaje.yaml` no declara `conjuros`: "
                 "sin esa regla no se puede dar la CD de ningún lanzador")
    return c


def _base_de_conjuros(clave):
    """El `base:` de un sub-bloque de `conjuros`, o un `sys.exit` que DICE qué
    falta.

    Un `[clave]["base"]` a pelo levantaba `KeyError` cuando la base venía sin
    ese sub-bloque, y quien llamaba —`validar.py`— moría antes de imprimir la
    etiqueta de su chequeo: la mutación que borraba el bloque contaba como no
    detectada. Es la familia del hueco nº 10 de la ronda 2 de estrés, un
    chequeo que explota en vez de hablar, y por eso el acceso pasa por aquí:
    faltar un dato de la base es un mensaje, nunca una traza.
    """
    bloque = _regla_de_conjuros().get(clave)
    if not isinstance(bloque, dict) or bloque.get("base") is None:
        sys.exit(f"✗ `reglas/generacion_personaje.yaml → conjuros` no declara "
                 f"`{clave}.base`: sin ese número no se puede dar la CD ni el "
                 f"bonificador de ataque de ningún lanzador")
    return bloque["base"]


def cd_conjuros(aptitud_mod, pb):
    return _base_de_conjuros("cd_salvacion") + aptitud_mod + pb


def bonif_ataque_conjuros(aptitud_mod, pb):
    return _base_de_conjuros("bonificador_ataque") + aptitud_mod + pb


# ── Espacios de conjuro ───────────────────────────────────────────────────
def espacios_de_conjuro(clase, nivel_de_clase):
    """Espacios de una clase lanzadora de un solo tipo, a un nivel dado
    (nivel de ESA clase, no el nivel total del personaje)."""
    d = cargar(f"clases/{_archivo_clase(clase)}")
    for fila in d.get("progresion", []):
        if fila["n"] == nivel_de_clase:
            slots = fila.get("slots")
            if slots is None:
                sys.exit(f"✗ {clase} nivel {nivel_de_clase} no tiene columna "
                          f"'slots' (¿es lanzador?)")
            return slots
    sys.exit(f"✗ {clase} no tiene nivel {nivel_de_clase} en su progresión")


def _tiene_ca_de_rasgo(clase):
    """¿Algún rasgo de esta clase o de sus subclases fija la CA base?

    Se pregunta a los datos, no a una lista escrita a mano: una lista escrita a
    mano es exactamente lo que dejó fuera a las dos fórmulas de subclase.
    """
    import efectos
    stem = _archivo_clase(clase)[:-5]
    rutas = [(f"clases/rasgos/{stem}.yaml", ("rasgos",))]
    if (B / f"clases/subclases/{stem}.yaml").exists():
        rutas.append((f"clases/subclases/{stem}.yaml", ("subclases", "rasgos")))
    return any(e["objetivo"] == "ca" and e["op"] == "base"
               for e in efectos.efectos_declarados(rutas))


def _archivo_clase(nombre):
    mapa = {
        "Bárbaro": "barbaro.yaml", "Bardo": "bardo.yaml", "Brujo": "brujo.yaml",
        "Clérigo": "clerigo.yaml", "Druida": "druida.yaml",
        "Explorador": "explorador.yaml", "Guerrero": "guerrero.yaml",
        "Hechicero": "hechicero.yaml", "Mago": "mago.yaml", "Monje": "monje.yaml",
        "Paladín": "paladin.yaml", "Pícaro": "picaro.yaml",
    }
    if nombre not in mapa:
        sys.exit(f"✗ clase desconocida: {nombre!r} (¿nombre exacto, con tilde?)")
    return mapa[nombre]


# ── CLI ────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("mod", help="modificador de una puntuación")
    p.add_argument("puntuacion", type=int)

    p = sub.add_parser("pg", help="puntos de golpe de nivel 1")
    p.add_argument("--dado", required=True, help="d6/d8/d10/d12")
    p.add_argument("--con", required=True, type=int, help="puntuación de Constitución")

    p = sub.add_parser("pb", help="bonificador por competencia")
    p.add_argument("--nivel", required=True, type=int, help="nivel TOTAL del personaje")

    p = sub.add_parser("percepcion-pasiva")
    p.add_argument("--sab", required=True, type=int)
    p.add_argument("--pb", type=int, default=0)
    p.add_argument("--competente", action="store_true")
    p.add_argument("--pericia", action="store_true")

    p = sub.add_parser("ca")
    p.add_argument("--des", required=True, type=int, help="puntuación de Destreza")
    p.add_argument("--con", type=int, default=10)
    p.add_argument("--sab", type=int, default=10)
    p.add_argument("--clase")
    p.add_argument("--armadura")
    p.add_argument("--escudo", action="store_true")

    p = sub.add_parser("cd-conjuros")
    p.add_argument("--aptitud", required=True, type=int, help="puntuación de la aptitud mágica")
    p.add_argument("--nivel", required=True, type=int, help="nivel TOTAL del personaje")

    p = sub.add_parser("ataque-conjuros")
    p.add_argument("--aptitud", required=True, type=int)
    p.add_argument("--nivel", required=True, type=int)

    p = sub.add_parser("espacios")
    p.add_argument("--clase", required=True)
    p.add_argument("--nivel", required=True, type=int, help="nivel DE LA CLASE")

    p = sub.add_parser("coste-compra")
    p.add_argument("--fue", type=int, required=True)
    p.add_argument("--des", type=int, required=True)
    p.add_argument("--con", type=int, required=True)
    p.add_argument("--int", type=int, required=True, dest="int_")
    p.add_argument("--sab", type=int, required=True)
    p.add_argument("--car", type=int, required=True)

    a = ap.parse_args()

    if a.cmd == "mod":
        print(modificador(a.puntuacion))
    elif a.cmd == "pg":
        print(puntos_golpe_nivel_1(a.dado, modificador(a.con)))
    elif a.cmd == "pb":
        print(bonificador_competencia(a.nivel))
    elif a.cmd == "percepcion-pasiva":
        print(percepcion_pasiva(modificador(a.sab), a.competente, a.pb, a.pericia))
    elif a.cmd == "ca":
        print(ca(modificador(a.des), modificador(a.con), modificador(a.sab),
                 clase=a.clase, armadura=a.armadura, escudo=a.escudo))
    elif a.cmd == "cd-conjuros":
        pb = bonificador_competencia(a.nivel)
        print(cd_conjuros(modificador(a.aptitud), pb))
    elif a.cmd == "ataque-conjuros":
        pb = bonificador_competencia(a.nivel)
        print(bonif_ataque_conjuros(modificador(a.aptitud), pb))
    elif a.cmd == "espacios":
        print(espacios_de_conjuro(a.clase, a.nivel))
    elif a.cmd == "coste-compra":
        scores = {"fue": a.fue, "des": a.des, "con": a.con,
                  "int": a.int_, "sab": a.sab, "car": a.car}
        total = coste_compra_puntos(scores)
        presupuesto = puntos_totales()
        print(total, f"de {presupuesto}" + ("" if total != presupuesto else " ✓"))


if __name__ == "__main__":
    main()
