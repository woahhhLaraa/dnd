#!/usr/bin/env python3
"""Consulta determinista de la base canónica D&D 2024 (5.5e).

Regla de diseño (ver CONTINUAR.md): cero resultados debe ser un ERROR,
jamás una lista vacía silenciosa. Una lista vacía es lo que hace que un LLM
concluya "no hay" e improvise con reglas de 2014 — el bug `Clerigo` (ver
FUENTES.md) nació exactamente así. Por eso toda consulta aquí valida su
entrada (clase, nombre) ANTES de filtrar: si la entrada es inválida, se
aborta con `sys.exit`, nunca se devuelve `[]`.

Uso como librería (import) o CLI:
    python3 buscar.py clase Mago
    python3 buscar.py conjuro "Hechizar persona"
    python3 buscar.py conjuros-de Bardo --nivel 1
    python3 buscar.py equipo "Armadura de cuero"
    python3 buscar.py dote Acechador
    python3 buscar.py especie Aasimar
    python3 buscar.py trasfondo Noble
"""
import argparse
import json
import sys

from calculo import B, cargar, _archivo_clase  # noqa: reutiliza lo ya escrito


def clase(nombre):
    """Devuelve el dict completo de clases/<clase>.yaml. Falla si el nombre
    no es una de las 12 canónicas (typo, sin tilde, etc.)."""
    archivo = _archivo_clase(nombre)  # ya hace sys.exit si no existe
    return cargar(f"clases/{archivo}")


def _hechizos():
    return cargar("hechizos.json")["hechizos"]


def conjuro(nombre):
    """Busca un conjuro por nombre exacto o alias. Falla si no existe —
    nunca devuelve None en silencio."""
    nombre_norm = nombre.strip().lower()
    for h in _hechizos():
        if h["nombre"].strip().lower() == nombre_norm:
            return h
        for al in h.get("alias") or []:
            if al.strip().lower() == nombre_norm:
                return h
    sys.exit(f"✗ no existe un conjuro llamado {nombre!r} en hechizos.json "
              f"(revisa tildes y el nombre exacto)")


def conjuros_de(nombre_clase, nivel=None):
    """Conjuros de una clase, opcionalmente filtrados por nivel. La clase se
    valida primero (vía `clase()`): si pasa, una lista vacía aquí SÍ es una
    respuesta legítima (esa clase no tiene conjuros de ese nivel todavía),
    no un fallo — la validación previa es lo que lo garantiza."""
    clase(nombre_clase)  # valida el nombre, con tilde y todo
    out = [h for h in _hechizos() if nombre_clase in h.get("clases", [])]
    if nivel is not None:
        out = [h for h in out if h.get("nivel") == nivel]
    return out


def equipo(nombre, archivo=None):
    """Busca un objeto por nombre exacto en cualquiera de los ficheros de
    equipo/ (tabla_peso_precio, armas, armaduras, herramientas, munición,
    objetos_de_rasgo_de_clase). Falla si no existe.

    Hay nombres que se repiten en ficheros distintos y significan cosas
    distintas (p. ej. "Bastón" es un arma en armas.yaml — 1d6 contundente,
    2 pp — y también una variante de canalizador arcano en aventureros.yaml
    — 5 po). Sin `archivo`, se devuelve el primer fichero que lo tenga (en
    el orden de abajo), que puede NO ser el que el jugador quería: por eso
    una `ref` en una ficha de personaje debería pasar `archivo` siempre que
    el nombre no sea inequívoco por sí solo."""
    nombre_norm = nombre.strip().lower()

    def walk(o):
        if isinstance(o, dict):
            n = o.get("nombre")
            if isinstance(n, str) and n.strip().lower() == nombre_norm:
                return o
            for v in o.values():
                r = walk(v)
                if r is not None:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r is not None:
                    return r
        return None

    orden = ("armas.yaml", "armaduras.yaml", "herramientas.yaml",
             "aventureros.yaml", "municion.yaml")
    if archivo:
        fn = archivo.split("/")[-1]
        if fn not in orden:
            sys.exit(f"✗ equipo/{fn} no es un fichero de equipo conocido")
        d = cargar(f"equipo/{fn}")
        r = walk(d)
        if r is not None:
            return r
        sys.exit(f"✗ no existe un objeto llamado {nombre!r} en equipo/{fn} "
                  f"(sí podría existir en otro fichero de equipo/ con el mismo "
                  f"nombre y otro significado — por eso la ref debe ser explícita)")

    # Busca en TODOS los ficheros y, si el nombre aparece en más de uno con
    # significado distinto (como "Bastón": arma en armas.yaml, canalizador
    # arcano en aventureros.yaml), exige `archivo` en vez de devolver el
    # primero en silencio — esa elección arbitraria fue justo el bug que dos
    # agentes de la ronda 2 señalaron por separado.
    encontrados = []
    for fn in orden:
        d = cargar(f"equipo/{fn}")
        r = walk(d)
        if r is not None:
            encontrados.append((fn, r))
    if len(encontrados) == 1:
        return encontrados[0][1]
    if len(encontrados) > 1:
        ficheros = ", ".join(f"equipo/{fn}" for fn, _ in encontrados)
        sys.exit(f"✗ {nombre!r} existe en más de un fichero de equipo/ con "
                  f"significados distintos ({ficheros}) — pasa `archivo` "
                  f"para elegir cuál")
    sys.exit(f"✗ no existe un objeto llamado {nombre!r} en equipo/ "
              f"(revisa el nombre exacto)")


def dote(nombre):
    """Busca una dote por nombre exacto en dotes/*.yaml. Falla si no existe."""
    nombre_norm = nombre.strip().lower()
    for fn in ("generales.yaml", "origen.yaml", "estilo_de_combate.yaml",
               "don_epico.yaml"):
        d = cargar(f"dotes/{fn}")
        for dt in d["dotes"]:
            if dt["nombre"].strip().lower() == nombre_norm:
                return dt
    sys.exit(f"✗ no existe una dote llamada {nombre!r} en dotes/ "
              f"(revisa el nombre exacto)")


def especie(nombre):
    nombre_norm = nombre.strip().lower()
    d = cargar("especies/especies.yaml")
    for e in d["especies"]:
        if e["nombre"].strip().lower() == nombre_norm:
            return e
    sys.exit(f"✗ no existe una especie llamada {nombre!r} en "
              f"especies/especies.yaml (revisa el nombre exacto)")


def trasfondo(nombre):
    nombre_norm = nombre.strip().lower()
    d = cargar("trasfondos/trasfondos.yaml")
    for t in d["trasfondos"]:
        if t["nombre"].strip().lower() == nombre_norm:
            return t
    sys.exit(f"✗ no existe un trasfondo llamado {nombre!r} en "
              f"trasfondos/trasfondos.yaml (revisa el nombre exacto)")


# ── CLI ────────────────────────────────────────────────────────────────
# ── Qué dotes puede tomar un personaje (Fase 15) ─────────────────────────
_CAR_LARGA = {"fue": "Fuerza", "des": "Destreza", "con": "Constitución",
              "int": "Inteligencia", "sab": "Sabiduría", "car": "Carisma"}


def _perfil(ficha):
    """Lo que un prerrequisito necesita saber del personaje, sacado SOLO de la
    ficha y de la base — nunca de lo que el LLM crea recordar."""
    import yaml
    cars = {_CAR_LARGA[k]: v
            for k, v in (ficha["caracteristicas"]["final"]).items()
            if k in _CAR_LARGA}

    rasgos, entrenamientos = [], []
    for c in ficha.get("clases", []):
        d = cargar(c["ref"].split("#")[0])
        for fila in d.get("progresion", []):
            if fila["n"] <= c["nivel"]:
                rasgos += [r for r in fila.get("rasgos", [])]
        sub = (c.get("subclase") or "").split("#")
        if len(sub) > 1:
            for s in (cargar(sub[0]) or {}).get("subclases", []):
                if s["nombre"] == sub[1]:
                    rasgos += [r["nombre"] for r in (s.get("rasgos") or [])
                               if (r.get("nivel") or 1) <= c["nivel"]]
    for a in (ficha.get("competencias") or {}).get("armaduras", []) or []:
        entrenamientos.append(a.get("categoria"))

    return {"nivel_total": ficha["nivel_total"], "caracteristicas": cars,
            "rasgos": rasgos, "entrenamientos": [e for e in entrenamientos if e]}


def dotes_disponibles(ficha):
    """Las dotes que este personaje **puede** tomar, con el porqué de cada una.

    Falla ruidosamente, como todo en este fichero: si ninguna dote sale
    disponible, es un error, **nunca una lista vacía**. Una lista vacía es lo
    que hace que el LLM concluya «no hay» e improvise — la regla que nació del
    bug `Clerigo`.
    """
    import prerrequisitos as P
    perfil = _perfil(ficha)
    disponibles, bloqueadas = [], []
    for f in sorted((B / "dotes").glob("*.yaml")):
        d = cargar(f"dotes/{f.name}") or {}
        for x in d.get("dotes", []):
            est = P.analizar(x.get("prerrequisito"))
            cumple, motivos = P.evaluar(est, perfil)
            fila = {"nombre": x["nombre"], "categoria": d.get("categoria"),
                    "prerrequisito": x.get("prerrequisito"), "porque": motivos}
            (disponibles if cumple else bloqueadas).append(fila)

    if not disponibles:
        sys.exit(f"✗ ninguna dote disponible para un personaje de nivel "
                 f"{perfil['nivel_total']}. Eso es sospechoso: hay 10 dotes sin "
                 f"prerrequisito alguno, así que la lista no debería quedar "
                 f"vacía nunca. Revisa la ficha antes de creerte el resultado.")
    return {"perfil": perfil, "disponibles": disponibles,
            "bloqueadas": bloqueadas}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("clase")
    p.add_argument("nombre")

    p = sub.add_parser("conjuro")
    p.add_argument("nombre")

    p = sub.add_parser("conjuros-de")
    p.add_argument("clase")
    p.add_argument("--nivel", type=int)

    p = sub.add_parser("equipo")
    p.add_argument("nombre")
    p.add_argument("--archivo", help="p. ej. equipo/aventureros.yaml, para desambiguar nombres repetidos")

    p = sub.add_parser("dote")
    p.add_argument("nombre")

    p = sub.add_parser("especie")
    p.add_argument("nombre")

    p = sub.add_parser("trasfondo")
    p.add_argument("nombre")

    p = sub.add_parser("dotes-disponibles",
                       help="qué dotes puede tomar una ficha, y por qué")
    p.add_argument("ficha", help="p. ej. personajes/enano_guerrero.yaml")

    a = ap.parse_args()

    resultado = {
        "clase": lambda: clase(a.nombre),
        "conjuro": lambda: conjuro(a.nombre),
        "conjuros-de": lambda: conjuros_de(a.clase, a.nivel),
        "equipo": lambda: equipo(a.nombre, archivo=a.archivo),
        "dote": lambda: dote(a.nombre),
        "especie": lambda: especie(a.nombre),
        "trasfondo": lambda: trasfondo(a.nombre),
        "dotes-disponibles": lambda: dotes_disponibles(
            cargar(a.ficha) if not a.ficha.startswith("/") else None),
    }[a.cmd]()

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
