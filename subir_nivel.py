#!/usr/bin/env python3
"""Qué pasa al subir de nivel — derivado de la base, nunca recordado (Fase 16).

`/subir-nivel` no puede improvisar qué preguntar. Este script **lee la tabla de
la clase** y devuelve, para cada salto de nivel, dos listas separadas:

  · lo que la base **concede** sin preguntar (rasgos, PB, espacios, columnas);
  · lo que el jugador **elige** y ningún script puede decidir por él (PG,
    subclase, mejora de característica o dote, conjuros).

La separación es el aporte de la taxonomía de *advancement* de Foundry
(`ANALISIS_REPOS.md` §2), reimplementada sobre nuestros datos. El vocabulario
cerrado está en `reglas/subida_de_nivel.yaml`.

**Falla ruidosamente.** Un nivel que no conceda ni pida nada es un error, jamás
una lista vacía: una lista vacía es lo que hace que el LLM concluya «no pasa
nada» y siga. Es la regla que nació del bug `Clerigo`.

    python3 subir_nivel.py --ficha personajes/x.yaml --a 4
    python3 subir_nivel.py --clase Hechicero --de 3 --a 4
"""
import argparse
import json
import sys

import yaml

from calculo import (B, cargar, es_marcador, es_marcador_de, marcador,
                     _archivo_clase)

# Se LEEN de la base —`reglas/subida_de_nivel.yaml → elecciones`/`concesiones`,
# que les da nombre— en vez de escribirse aquí. Eran dos cadenas cableadas al
# lado de un `es_marcador()` que ya leía el fichero: detectar el marcador se
# leía y despacharlo se copiaba. `validar.py` importa `MARCADOR_RASGO_SUB` de
# aquí, así que la copia cableada era además carga estructural.
MARCADOR_MEJORA = marcador("mejora_caracteristica_o_dote")
MARCADOR_RASGO_SUB = marcador("rasgo_de_subclase")


# La copia cableada que había aquí aceptaba «Subclase de» SIN espacio final,
# mientras la de `validar.py` lo exigía: «Subclase deluxe» era marcador para
# una y rasgo para la otra. Se lee de la base (ver `calculo.es_marcador`).
def _es_marcador(nombre):
    return es_marcador(nombre)


def _fila(prog, n):
    for f in prog:
        if f["n"] == n:
            return f
    sys.exit(f"✗ la progresión no tiene nivel {n}")


def _textos_de_rasgo(stem):
    d = cargar(f"clases/rasgos/{stem}.yaml") or {}
    return {r["nombre"]: r for r in d.get("rasgos", [])}


def que_pasa(clase, nivel, subclase=None):
    """Lo que ocurre AL ALCANZAR `nivel` en `clase`."""
    stem = _archivo_clase(clase)[:-5]
    d = cargar(f"clases/{stem}.yaml")
    prog = d.get("progresion") or []
    fila = _fila(prog, nivel)
    previa = _fila(prog, nivel - 1) if nivel > 1 else {}
    textos = _textos_de_rasgo(stem)

    concede, elige = [], []

    # 1. Rasgos con texto propio.
    for r in fila.get("rasgos", []):
        if _es_marcador(r):
            continue
        t = textos.get(r)
        if t is None:
            sys.exit(f"✗ {clase} nivel {nivel} concede «{r}» y no hay texto en "
                     f"clases/rasgos/{stem}.yaml. La base no puede explicar un "
                     f"rasgo que concede.")
        concede.append({"tipo": "rasgo_de_clase", "nombre": r,
                        "pagina": t.get("pagina"),
                        "ref": f"clases/rasgos/{stem}.yaml#{r}"})

    # 2. Marcadores → elecciones o rasgos de subclase.
    for r in fila.get("rasgos", []):
        if es_marcador_de("subclase", r):
            sub = cargar(f"clases/subclases/{stem}.yaml") or {}
            opciones = [s["nombre"] for s in sub.get("subclases", [])]
            if not opciones:
                sys.exit(f"✗ {clase} nivel {nivel} pide subclase y "
                         f"clases/subclases/{stem}.yaml no ofrece ninguna")
            elige.append({"tipo": "subclase", "opciones": opciones,
                          "ref": f"clases/subclases/{stem}.yaml"})
        elif r == MARCADOR_MEJORA:
            elige.append({"tipo": "mejora_caracteristica_o_dote",
                          "como": "+2 a una característica o +1 a dos, o una dote",
                          "dotes": "usa `buscar.py dotes-disponibles <ficha>`: "
                                   "filtra por prerrequisito (Fase 15)"})
        elif r == MARCADOR_RASGO_SUB:
            if not subclase:
                sys.exit(f"✗ {clase} nivel {nivel} concede un rasgo de subclase "
                         f"y la ficha no declara subclase. No se puede saber "
                         f"cuál sin adivinar.")
            sub = cargar(f"clases/subclases/{stem}.yaml") or {}
            s = next((x for x in sub.get("subclases", [])
                      if x["nombre"] == subclase), None)
            if s is None:
                sys.exit(f"✗ subclase {subclase!r} no existe en "
                         f"clases/subclases/{stem}.yaml")
            nuevos = [x for x in (s.get("rasgos") or []) if x.get("nivel") == nivel]
            if not nuevos:
                sys.exit(f"✗ la tabla de {clase} concede «{MARCADOR_RASGO_SUB}» "
                         f"en el nivel {nivel} y «{subclase}» no tiene ninguno "
                         f"de ese nivel")
            for x in nuevos:
                concede.append({"tipo": "rasgo_de_subclase", "nombre": x["nombre"],
                                "subclase": subclase, "pagina": s.get("pagina"),
                                "ref": f"clases/subclases/{stem}.yaml#{subclase}"})

    # 3. Bonificador por competencia, si sube.
    if previa and fila.get("pb") != previa.get("pb"):
        concede.append({"tipo": "bonificador_competencia",
                        "de": previa.get("pb"), "a": fila.get("pb")})

    # 4. Columnas numéricas que cambian: los `ScaleValue` de la tabla.
    for col, val in fila.items():
        if col in ("n", "pb", "rasgos"):
            continue
        antes = previa.get(col)
        if antes == val:
            continue
        tipo = ("espacios_de_conjuro" if col in ("slots", "espacios")
                else "valor_de_tabla")
        entrada = {"tipo": tipo, "columna": col, "de": antes, "a": val}
        (elige if col in ("trucos", "prep") else concede).append(
            entrada if col not in ("trucos", "prep") else
            dict(entrada, como="elige cuáles"))

    # 5. Los PG, que son siempre una elección del jugador.
    elige.append({"tipo": "puntos_de_golpe",
                  "opciones": ["tirada", "valor_establecido"],
                  "ref": "reglas/generacion_personaje.yaml#puntos_golpe.niveles_siguientes_al_1"})

    if not concede and len(elige) <= 1:
        sys.exit(f"✗ {clase} nivel {nivel}: la base dice que no pasa NADA salvo "
                 f"los PG. Eso no es una respuesta creíble — revisa la "
                 f"progresión antes de creértelo.")
    return {"clase": clase, "nivel": nivel, "concede": concede, "elige": elige}


def plan_de_subida(ficha, destino):
    clases = ficha.get("clases", [])
    if len(clases) != 1:
        sys.exit("✗ la multiclase todavía no se sube automáticamente")
    c = clases[0]
    actual = c["nivel"]
    if destino <= actual:
        sys.exit(f"✗ la ficha ya está en nivel {actual}; el destino {destino} "
                 f"no es una subida")
    subclase = (c.get("subclase") or "").split("#")[-1] or None
    pasos = [que_pasa(c["clase"], n, subclase) for n in range(actual + 1, destino + 1)]
    return {"personaje": ficha.get("nombre"), "clase": c["clase"],
            "de": actual, "a": destino, "pasos": pasos}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ficha")
    ap.add_argument("--clase")
    ap.add_argument("--subclase")
    ap.add_argument("--de", type=int)
    ap.add_argument("--a", type=int, required=True)
    a = ap.parse_args()

    if a.ficha:
        salida = plan_de_subida(cargar(a.ficha), a.a)
    elif a.clase:
        desde = (a.de or 0) + 1
        salida = {"clase": a.clase, "de": a.de, "a": a.a,
                  "pasos": [que_pasa(a.clase, n, a.subclase)
                            for n in range(desde, a.a + 1)]}
    else:
        sys.exit("✗ hace falta --ficha o --clase")
    print(json.dumps(salida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
