#!/usr/bin/env python3
"""Genera fichas legales desde la base, para estresar el sistema (2026-08-30).

**Para qué es.** Los dos huecos más grandes que le quedaban a este proyecto —las
características que nadie justificaba y los conjuros que nadie contaba— no los
encontró ningún razonamiento: los encontró **construir una ficha de nivel 20 y
ver qué se rompía**. Este script hace eso mismo a escala: fabrica personajes
legales de cualquier clase y nivel, deterministas y reproducibles, y los pasa
por `verificar_personaje.py`. Cada fallo es un hallazgo.

**Lo que NO hace, y conviene decirlo.** El equipo inicial de una clase vive como
**prosa** en `atributos_basicos.equipo_inicial.a` («lanza, 5 dagas, herramientas
de artesano…»), no como lista de refs. Este generador no lo parsea: pone la
armadura más pesada que la clase sepa usar —para que la CA varíe y el motor de
efectos trabaje— y deja el resto vacío. Las fichas que produce son **completas
en reglas** (nivel, PG, mejoras, subclase, conjuros, competencias) y **ligeras
en inventario**. Sirven para estresar las reglas, no para jugarlas.

    python3 generar_ficha.py --clase Monje --nivel 20 --salida /tmp/x.yaml
    python3 generar_ficha.py --barrido           # las 12 clases, varios niveles
"""
import argparse
import json
import pathlib
import subprocess
import sys

import yaml

from calculo import B, cargar, _archivo_clase

CARS = ("fue", "des", "con", "int", "sab", "car")
_LARGO = {"fue": "Fuerza", "des": "Destreza", "con": "Constitución",
          "int": "Inteligencia", "sab": "Sabiduría", "car": "Carisma"}
_CORTO = {v: k for k, v in _LARGO.items()}
CONJUNTO = [15, 14, 13, 12, 10, 8]


def _reparto(clase_d):
    """El conjunto estándar repartido: lo mejor a la característica principal,
    luego Constitución, luego el resto. Es una heurística DEL GENERADOR, no una
    regla del manual — por eso queda dicho en `decisiones`."""
    ppal = clase_d["atributos_basicos"].get("caracteristica_principal") or ""
    orden = [_CORTO[p.strip()] for p in ppal.replace(" y ", ",").split(",")
             if p.strip() in _CORTO]
    orden += [c for c in ("con", "des", "sab", "fue", "int", "car") if c not in orden]
    return dict(zip(orden, CONJUNTO))


def _armadura(clase_d):
    """La armadura más pesada que la clase sepa usar, si alguna."""
    arm = [str(a).lower() for a in (clase_d["atributos_basicos"].get("armaduras") or [])]
    d = cargar("equipo/armaduras.yaml")
    for grupo, clave in (("armaduras pesadas", "armaduras_pesadas"),
                         ("armaduras medias", "armaduras_medias"),
                         ("armaduras ligeras", "armaduras_ligeras")):
        if any(grupo in a for a in arm):
            return d[clave]["tabla"][-1]["nombre"]
    return None


def generar(clase, nivel, especie=None, trasfondo=None, subclase=None):
    stem = _archivo_clase(clase)[:-5]
    clase_d = cargar(f"clases/{stem}.yaml")
    ab = clase_d["atributos_basicos"]
    prog = {f["n"]: f for f in clase_d["progresion"]}
    if nivel not in prog:
        sys.exit(f"✗ {clase} no tiene nivel {nivel}")

    esp_l = cargar("especies/especies.yaml")["especies"]
    esp = next((e for e in esp_l if e["nombre"] == especie), esp_l[0])
    tr_l = next(v for v in cargar("trasfondos/trasfondos.yaml").values()
                if isinstance(v, list))
    tr = next((x for x in tr_l if x["nombre"] == trasfondo), tr_l[0])

    base = _reparto(clase_d)
    ajuste = {}
    for i, c in enumerate(tr["caracteristicas"][:2]):
        ajuste[_CORTO[c]] = 2 if i == 0 else 1

    # ── mejoras de característica, una por cada nivel que las conceda
    niveles_mej = [n for n in sorted(prog) if n <= nivel
                   and "Mejora de característica" in (prog[n].get("rasgos") or [])]
    final = {c: base.get(c, 8) + ajuste.get(c, 0) for c in CARS}
    ppal = _reparto(clase_d)
    orden_subida = [c for c in ppal if ppal[c] >= 13] or ["con"]
    mejoras = []
    for n in niveles_mej:
        # Sube de 2 en 2 la mejor característica que no llegue a 20; si todas
        # llegaron, reparte +1 y +1 donde quepa. La dote lo permite y el
        # verificador comprueba que `final` cuadre.
        cand = [c for c in orden_subida if final[c] <= 18]
        if cand:
            sube = {cand[0]: 2}
        else:
            libres = [c for c in CARS if final[c] <= 19][:2]
            if len(libres) < 2:
                sys.exit(f"✗ {clase} N{nivel}: no queda dónde repartir la mejora "
                         f"del nivel {n} sin pasar de 20")
            sube = {libres[0]: 1, libres[1]: 1}
        for k, v in sube.items():
            final[k] += v
        mejoras.append({"nivel": n, "sube": sube,
                        "ref": "dotes/generales.yaml#Mejora de característica"})

    # ── competencias
    hab_bloque = ab.get("habilidades") or {}
    del_trasfondo = list(tr.get("habilidades") or [])
    if hab_bloque.get("cualesquiera"):
        pool = [h["nombre"] for h in cargar("reglas/habilidades.yaml")["habilidades"]]
    else:
        pool = list(hab_bloque.get("de") or [])
    elegidas = [h for h in pool if h not in del_trasfondo][:hab_bloque.get("elige", 0)]

    ficha = {
        "nombre": f"Prueba {clase} {nivel}",
        "jugador": None,
        "nivel_total": nivel,
        "especie": {"ref": f"especies/especies.yaml#{esp['nombre']}"},
        "trasfondo": {"ref": f"trasfondos/trasfondos.yaml#{tr['nombre']}"},
        "clases": [{"clase": clase, "ref": f"clases/{stem}.yaml", "nivel": nivel,
                    "subclase": None}],
        "caracteristicas": {"metodo": "conjunto_estandar", "base": base,
                            "ajuste_trasfondo": ajuste, "final": final},
        "competencias": {
            "salvaciones": list(ab.get("salvaciones") or []),
            "habilidades": [{"nombre": h, "origen": {"clase": clase}} for h in elegidas]
                           + [{"nombre": h, "origen": {"trasfondo": tr["nombre"]}}
                              for h in del_trasfondo],
            "armas": [{"categoria": a, "origen": {"clase": clase}}
                      for a in (ab.get("armas") or [])],
            "armaduras": [{"categoria": a, "origen": {"clase": clase}}
                          for a in (ab.get("armaduras") or [])],
            "herramientas": [],
            "idiomas": [{"nombre": "Común"}],
        },
        "equipo": [],
    }

    # ── subclase, si la tabla la pide
    if any("Subclase de" in r for n in sorted(prog) if n <= nivel
           for r in (prog[n].get("rasgos") or [])):
        subs = (cargar(f"clases/subclases/{stem}.yaml") or {}).get("subclases", [])
        elegida = next((s for s in subs if s["nombre"] == subclase), subs[0])
        ficha["clases"][0]["subclase"] = \
            f"clases/subclases/{stem}.yaml#{elegida['nombre']}"

    arm = _armadura(clase_d)
    if arm:
        ficha["equipo"].append({"ref": f"equipo/armaduras.yaml#{arm}",
                                "origen": {"clase": clase, "nota": "generado"}})

    if mejoras:
        ficha["mejoras"] = mejoras

    # ── PG: siempre valor establecido, para que sea reproducible
    dado = int(str(ab["dado_golpe"]).lstrip("d"))
    import calculo
    fijo = calculo.valor_establecido_pg(clase)
    ficha["pg_por_nivel"] = [{"nivel": 1, "clase": clase, "metodo": "maximo_dado",
                              "valor": dado,
                              "cita": {"archivo": "reglas/generacion_personaje.yaml",
                                       "campo": "puntos_golpe.nivel_1"}}]
    for n in range(2, nivel + 1):
        ficha["pg_por_nivel"].append(
            {"nivel": n, "clase": clase, "metodo": "valor_establecido", "valor": fijo,
             "cita": {"archivo": "reglas/generacion_personaje.yaml",
                      "campo": "puntos_golpe.niveles_siguientes_al_1.tabla_valores_establecidos"}})

    # ── conjuros, si la clase lanza
    fila = prog[nivel]
    if clase_d.get("lanzador") not in (None, "ninguno"):
        H = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
        def lista(niv):
            return sorted(h["nombre"] for h in H
                          if clase in (h.get("clases") or []) and h["nivel"] == niv)
        conj = {}
        if fila.get("trucos"):
            conj["trucos"] = [{"ref": f"hechizos.json#{n}"}
                              for n in lista(0)[:fila["trucos"]]]
        if fila.get("prep"):
            # Se recorren los niveles en orden hasta juntar los que pide la
            # tabla. La primera versión repartía una cuota fija por nivel y se
            # quedaba corta en Explorador y Paladín de nivel 14 (10 de 11):
            # era un fallo del generador, no de la base, y lo destapó el barrido.
            elegidos = []
            for niv in range(1, 10):
                for n in lista(niv):
                    if len(elegidos) >= fila["prep"]:
                        break
                    elegidos.append(n)
                if len(elegidos) >= fila["prep"]:
                    break
            if len(elegidos) < fila["prep"]:
                sys.exit(f"✗ {clase} N{nivel}: la tabla pide {fila['prep']} "
                         f"conjuros preparados y la base solo ofrece "
                         f"{len(elegidos)} para esta clase")
            conj["preparados"] = [{"ref": f"hechizos.json#{n}"} for n in elegidos]
        if conj:
            ficha["conjuros"] = conj

    ficha["decisiones"] = [
        {"en": "generación automática",
         "eleccion": "conjunto estándar repartido por característica principal; "
                     "PG siempre por valor establecido; mejoras a la principal. "
                     "Es una heurística del generador, no una regla del manual.",
         "cita": {"archivo": "reglas/generacion_personaje.yaml",
                  "campo": "metodos_generacion_caracteristicas.conjunto_estandar"}},
        {"en": "generación automática",
         "eleccion": "el equipo inicial vive como prosa en la base, así que esta "
                     "ficha solo lleva armadura; el inventario queda vacío a "
                     "propósito.",
         "cita": {"archivo": f"clases/{stem}.yaml",
                  "campo": "atributos_basicos.equipo_inicial"}},
    ]
    return ficha


def escribir(ficha, ruta):
    p = pathlib.Path(ruta)
    p.write_text(yaml.safe_dump(ficha, allow_unicode=True, sort_keys=False,
                                width=100), encoding="utf-8")
    r = subprocess.run([sys.executable, "verificar_personaje.py", "--calcular", str(p)],
                       cwd=B, capture_output=True, text=True)
    if r.returncode != 0:
        return p, r.stdout + r.stderr
    ficha["calculado"] = yaml.safe_load(r.stdout)["calculado"]
    p.write_text(yaml.safe_dump(ficha, allow_unicode=True, sort_keys=False,
                                width=100), encoding="utf-8")
    return p, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--clase")
    ap.add_argument("--nivel", type=int)
    ap.add_argument("--especie")
    ap.add_argument("--trasfondo")
    ap.add_argument("--subclase")
    ap.add_argument("--salida")
    ap.add_argument("--exhaustivo", action="store_true",
                    help="con --barrido: los 20 niveles y TODAS las subclases")
    ap.add_argument("--barrido", action="store_true",
                    help="las 12 clases en varios niveles, y verifica todas")
    a = ap.parse_args()

    if a.barrido:
        clases = [yaml.safe_load(f.read_text(encoding="utf-8"))["clase"]
                  for f in sorted((B / "clases").glob("*.yaml"))
                  if "progresion" in f.read_text(encoding="utf-8")]
        niveles = list(range(1, 21)) if a.exhaustivo else [1, 3, 5, 8, 11, 14, 17, 20]
        fallos = 0
        tmp = pathlib.Path("/tmp/fichas_estres"); tmp.mkdir(exist_ok=True)
        for c in clases:
            linea = []
            stem = _archivo_clase(c)[:-5]
            subs = [s["nombre"] for s in
                    ((cargar(f"clases/subclases/{stem}.yaml") or {}).get("subclases") or [])]
            for n in niveles:
                # En modo exhaustivo se rota la subclase por nivel, para que las
                # cuatro de cada clase pasen por el verificador.
                sub = subs[n % len(subs)] if (a.exhaustivo and subs) else None
                try:
                    f = generar(c, n, subclase=sub)
                except SystemExit as e:
                    linea.append(f"N{n}:✗gen"); fallos += 1
                    print(f"   {c} N{n}: {e}")
                    continue
                ruta, err = escribir(f, tmp / f"{c.lower()}_{n}.yaml")
                if err:
                    linea.append(f"N{n}:✗calc"); fallos += 1
                    print(f"   {c} N{n}: {err.strip()[:160]}")
                    continue
                r = subprocess.run([sys.executable, "verificar_personaje.py", str(ruta)],
                                   cwd=B, capture_output=True, text=True)
                if r.returncode == 0:
                    linea.append(f"N{n}:✅")
                else:
                    linea.append(f"N{n}:❌"); fallos += 1
                    for l in r.stdout.splitlines():
                        if "✗" in l:
                            print(f"   {c} N{n}: {l.strip()[:170]}")
            print(f"{c:12} " + "  ".join(linea))
        total = len(clases) * len(niveles)
        print("─" * 74)
        print(f"{'✅' if not fallos else '❌'} {total - fallos}/{total} fichas "
              f"generadas y verificadas")
        return 1 if fallos else 0

    if not (a.clase and a.nivel):
        sys.exit("✗ hace falta --clase y --nivel, o --barrido")
    f = generar(a.clase, a.nivel, a.especie, a.trasfondo, a.subclase)
    ruta, err = escribir(f, a.salida or f"/tmp/{a.clase.lower()}_{a.nivel}.yaml")
    if err:
        sys.exit(err)
    print(f"escrita {ruta}")
    print(yaml.safe_dump(f.get("calculado"), allow_unicode=True, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
