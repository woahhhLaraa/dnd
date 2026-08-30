#!/usr/bin/env python3
"""Motor de efectos de la base canónica D&D 2024 (5.5e) — Fase 14.

Una regla de personaje deja de ser una rama de Python y pasa a ser **un dato
citado** que vive junto al texto del rasgo que la concede. El motor los recoge,
los agrega en un orden fijo y determinista, y falla ruidosamente cuando no sabe.

Por qué existe (y no es refactor por gusto): `calculo.py` tenía las fórmulas de
"Defensa sin armadura" como `lambda` indexadas por nombre de clase, y por eso
conocía **2 de las 4** que hay en la base — se le escapaban las de subclase
(*Juego de pies deslumbrante* del Bardo, *Resistencia dracónica* del Hechicero).
Y `bonus_pg_especie` era un campo de la ficha que cubría **1 de los 2** efectos
sobre PG máximos. Una regla cableada no se puede citar, no se puede validar, y
no se entera de que existe una quinta.

Vocabulario cerrado en `reglas/efectos.yaml`. Contrato en
`reglas/_ESQUEMA_efectos.md`.

    python3 efectos.py explicar --ficha personajes/draconido_monje.yaml
"""
import argparse
import ast
import math
import pathlib
import sys

import yaml

B = pathlib.Path(__file__).parent


class ErrorDeEfectos(Exception):
    """Se lanza siempre que el motor no sabe. Nunca se devuelve un número
    plausible: eso es lo que hace que el LLM concluya «ya está» e improvise."""


# ── Fórmulas ─────────────────────────────────────────────────────────────
# Aritmética entera sobre variables declaradas, y nada más. Se usa `ast` con
# una lista blanca en vez de `eval()`: una fórmula sale de un fichero YAML de
# la base, y `eval()` sobre datos convierte una errata en ejecución de código.
_NODOS = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Constant,
          ast.Add, ast.Sub, ast.Mult, ast.USub, ast.UAdd, ast.Load, ast.Call)
_FUNCIONES = {"min": min, "max": max}


def variables_de(formula):
    """(Una `columna` no menciona variables: su valor sale de la tabla.)"""
    """Nombres de variable que menciona una fórmula. Es lo que construye el
    grafo de dependencias."""
    try:
        arbol = ast.parse(str(formula), mode="eval")
    except SyntaxError as e:
        raise ErrorDeEfectos(f"fórmula no parseable: {formula!r} ({e.msg})")
    return {n.id for n in ast.walk(arbol)
            if isinstance(n, ast.Name) and n.id not in _FUNCIONES}


def evaluar(formula, entorno):
    arbol = ast.parse(str(formula), mode="eval")
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, _NODOS):
            raise ErrorDeEfectos(
                f"fórmula con sintaxis no permitida ({type(nodo).__name__}): "
                f"{formula!r}. Solo enteros, variables declaradas y + - *")
        if isinstance(nodo, ast.Constant) and not isinstance(nodo.value, int):
            raise ErrorDeEfectos(f"solo enteros en las fórmulas: {formula!r}")
        if isinstance(nodo, ast.Call):
            if not (isinstance(nodo.func, ast.Name)
                    and nodo.func.id in _FUNCIONES and len(nodo.args) == 2):
                raise ErrorDeEfectos(
                    f"solo se permiten min(a, b) y max(a, b): {formula!r}")
            continue
        if isinstance(nodo, ast.Name) and nodo.id in _FUNCIONES:
            continue
        if isinstance(nodo, ast.Name) and nodo.id not in entorno:
            raise ErrorDeEfectos(
                f"la fórmula {formula!r} usa {nodo.id!r}, que no es una "
                f"variable declarada en reglas/efectos.yaml")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            v = entorno[n.id]
            if v is None:
                raise ErrorDeEfectos(
                    f"la fórmula {formula!r} necesita {n.id!r} y todavía no "
                    f"tiene valor")
            return v
        if isinstance(n, ast.Call):
            return _FUNCIONES[n.func.id](ev(n.args[0]), ev(n.args[1]))
        if isinstance(n, ast.UnaryOp):
            return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        a, b = ev(n.left), ev(n.right)
        return a + b if isinstance(n.op, ast.Add) else \
               a - b if isinstance(n.op, ast.Sub) else a * b

    return ev(arbol)


# ── Vocabulario ──────────────────────────────────────────────────────────
def cargar_vocabulario():
    v = yaml.safe_load((B / "reglas/efectos.yaml").read_text(encoding="utf-8"))
    for clave in ("variables", "operaciones", "condiciones", "base_multiple"):
        if clave not in v:
            raise ErrorDeEfectos(f"reglas/efectos.yaml no declara «{clave}»")
    return v


# ── Recolección: de dónde salen los efectos ──────────────────────────────
# Un efecto vive PEGADO al registro que lo concede, con la página de ese
# registro. Nunca se copia a la ficha: la ficha referencia el rasgo, y si la
# base se corrige el personaje se entera. Es la regla central de
# `personajes/_ESQUEMA.md` aplicada a la aritmética.
_ORIGENES = (
    ("especies/especies.yaml", ("especies", "rasgos")),
    ("clases/rasgos/barbaro.yaml", ("rasgos",)),
    ("clases/rasgos/bardo.yaml", ("rasgos",)),
    ("clases/rasgos/brujo.yaml", ("rasgos",)),
    ("clases/rasgos/clerigo.yaml", ("rasgos",)),
    ("clases/rasgos/druida.yaml", ("rasgos",)),
    ("clases/rasgos/explorador.yaml", ("rasgos",)),
    ("clases/rasgos/guerrero.yaml", ("rasgos",)),
    ("clases/rasgos/hechicero.yaml", ("rasgos",)),
    ("clases/rasgos/mago.yaml", ("rasgos",)),
    ("clases/rasgos/monje.yaml", ("rasgos",)),
    ("clases/rasgos/paladin.yaml", ("rasgos",)),
    ("clases/rasgos/picaro.yaml", ("rasgos",)),
    ("clases/subclases/bardo.yaml", ("subclases", "rasgos")),
    ("clases/subclases/hechicero.yaml", ("subclases", "rasgos")),
)


def _descender(nodo, camino):
    """Recorre `camino` por listas anidadas y devuelve (registro, ancestros)."""
    if not camino:
        yield nodo, []
        return
    for hijo in nodo.get(camino[0], []) or []:
        for reg, anc in _descender(hijo, camino[1:]):
            yield reg, [hijo] + anc


def efectos_declarados(rutas=None):
    """Todos los efectos que hay en la base, con su procedencia. Se usa tanto
    para calcular como para que `validar.py` los revise sin duplicar lógica."""
    salida = []
    for rel, camino in (rutas or _ORIGENES):
        f = B / rel
        if not f.exists():
            raise ErrorDeEfectos(f"origen de efectos inexistente: {rel}")
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for reg, ancestros in _descender(doc, list(camino)):
            for ef in reg.get("efectos", []) or []:
                salida.append(dict(
                    ef,
                    _archivo=rel,
                    _rasgo=reg.get("nombre"),
                    _nivel=reg.get("nivel"),
                    _contenedor=(ancestros[0].get("nombre") if ancestros else None),
                ))
    return salida


# ── Estado: qué condiciones cumple el personaje ──────────────────────────
_ARMADURAS = ("armaduras_ligeras", "armaduras_medias", "armaduras_pesadas")


def estado_de_equipo(refs):
    """Deduce las condiciones del equipo de la ficha. Lo deduce el código a
    partir de `equipo/armaduras.yaml`, no el LLB a ojo."""
    d = yaml.safe_load((B / "equipo/armaduras.yaml").read_text(encoding="utf-8"))
    nombres = {a["nombre"].lower() for g in _ARMADURAS for a in d[g]["tabla"]}
    escudos = {e["nombre"].lower() for e in d["escudos"]["tabla"]}
    llevados = {r.split("#")[-1].lower() for r in refs}
    con_arm = bool(llevados & nombres)
    con_esc = bool(llevados & escudos)
    return {"con_armadura": con_arm, "sin_armadura": not con_arm,
            "con_escudo": con_esc, "sin_escudo": not con_esc}


def aplica(ef, estado, vocab):
    for c in ef.get("requiere", []) or []:
        if c not in vocab["condiciones"]:
            raise ErrorDeEfectos(
                f"condición no declarada: {c!r} en «{ef.get('_rasgo')}» "
                f"({ef.get('_archivo')})")
        if not estado.get(c):
            return False
    return True


# ── Agregación ───────────────────────────────────────────────────────────
def valor_de_columna(clase_stem, columna, nivel_clase):
    """El valor de una columna de la progresión al nivel dado.

    Es el `ScaleValue` de Foundry (`ANALISIS_REPOS.md` §2) resuelto sin
    inventar nada: la tabla dispersa **ya está** en `clases/<clase>.yaml`, así
    que se lee. Copiarla dentro del efecto sería duplicar un dato derivable.
    """
    d = yaml.safe_load((B / f"clases/{clase_stem}.yaml").read_text(encoding="utf-8"))
    for fila in d.get("progresion", []):
        if fila["n"] == nivel_clase:
            if columna not in fila:
                raise ErrorDeEfectos(
                    f"la progresión de {d.get('clase')} no tiene columna "
                    f"{columna!r} en el nivel {nivel_clase}")
            return fila[columna]
    raise ErrorDeEfectos(f"{d.get('clase')} no tiene nivel {nivel_clase}")


def _num(ef, entorno):
    """El valor de un efecto: el de su `columna` si ya vino resuelto, o el de su
    fórmula si no.

    Existe porque los dos caminos son distintos: una `formula` es aritmética
    **entera** escrita a mano y `evaluar()` rechaza decimales a propósito; una
    `columna` trae el número tal cual lo imprime la tabla, y ahí **sí** los hay
    — «Movimiento sin armadura» del Monje vale 4,5 m en el nivel 6. Pasar la
    columna por el evaluador reventaba el cálculo de cualquier monje de nivel
    6, 14 o 17, y no se vio hasta generar fichas de todos los niveles: la única
    ficha que sostenía el efecto era de nivel 2, donde la columna vale 3.
    """
    if ef.get("_valor") is not None:
        return ef["_valor"]
    return evaluar(ef["formula"], entorno)


def agregar(variable, efectos, base, entorno, eleccion=None, decimal=False):
    """El orden fijo de `reglas/efectos.yaml → orden_de_agregacion`.

    La única divergencia con DiceCloud está en varios `base` a la vez: allí se
    toma el máximo, aquí se EXIGE la elección, porque eso es lo que dice
    `reglas/generacion_personaje.yaml → multiclase.clase_de_armadura`.
    """
    por_op = {}
    for ef in efectos:
        por_op.setdefault(ef["op"], []).append(ef)

    bases = por_op.get("base", [])
    if len(bases) > 1:
        etiquetas = [f"{e['_rasgo']} ({e['_archivo']})" for e in bases]
        if eleccion is None:
            raise ErrorDeEfectos(
                f"«{variable}» tiene {len(bases)} formas de calcularse y el "
                f"manual dice que solo puede beneficiarse de UNA, A ELEGIR "
                f"(reglas/generacion_personaje.yaml → clase_de_armadura). "
                f"Declara cuál en `elecciones.{variable}_base` de la ficha. "
                f"Aplicables: {'; '.join(etiquetas)}")
        elegidos = [e for e in bases if e["_rasgo"] == eleccion]
        if not elegidos:
            raise ErrorDeEfectos(
                f"«{eleccion}» no es una de las formas aplicables de calcular "
                f"«{variable}»: {'; '.join(etiquetas)}")
        bases = elegidos

    if bases:
        valor = _num(bases[0], entorno)
    elif base is not None:
        valor = base
    else:
        raise ErrorDeEfectos(
            f"«{variable}» no tiene valor base ni ningún efecto `base` que lo "
            f"fije, y algo lo está pidiendo")

    for ef in por_op.get("add", []):
        valor += _num(ef, entorno)
    for ef in por_op.get("mul", []):
        valor *= _num(ef, entorno)
    for ef in por_op.get("min", []):
        valor = max(valor, _num(ef, entorno))
    for ef in por_op.get("max", []):
        valor = min(valor, _num(ef, entorno))
    for ef in por_op.get("set", []):
        valor = _num(ef, entorno)
    # DiceCloud redondea hacia abajo «salvo stats decimales». La velocidad es
    # una de ellas: 4,5 m es media casilla de verdad, no un redondeo.
    return valor if decimal else math.floor(valor)


# ── Grafo de dependencias ────────────────────────────────────────────────
def orden_de_calculo(pendientes, efectos_por_var, bases, vocab):
    """Orden topológico. Un ciclo se registra como error EXPLÍCITO, nunca se
    devuelve un número plausible: es la doctrina de `buscar.py` (fallar
    ruidosamente) aplicada a la aritmética, y la idea es de DiceCloud
    (`type: 'dependencyLoop'`)."""
    deps = {}
    for v in pendientes:
        d = set()
        for ef in efectos_por_var.get(v, []):
            # Un efecto con `columna` no menciona variables: su valor sale de la
            # tabla de la clase, así que no crea dependencias.
            if ef.get("formula") is not None:
                d |= variables_de(ef["formula"])
        if bases.get(v) is not None and isinstance(bases[v], str):
            d |= variables_de(bases[v])
        deps[v] = d & set(pendientes)

    orden, vistos, en_curso = [], set(), []

    def visitar(v):
        if v in vistos:
            return
        if v in en_curso:
            ciclo = " → ".join(en_curso[en_curso.index(v):] + [v])
            raise ErrorDeEfectos(f"ciclo de dependencias entre efectos: {ciclo}")
        en_curso.append(v)
        for d in sorted(deps[v]):
            visitar(d)
        en_curso.pop()
        vistos.add(v)
        orden.append(v)

    for v in sorted(pendientes):
        visitar(v)
    return orden


# ── API principal ────────────────────────────────────────────────────────
def calcular(entradas, efectos, bases, estado, elecciones=None):
    """Devuelve `{variable: valor}` para las variables `calculada` pedidas.

    `entradas`  — mod_des, pb, nivel_total… los valores que no produce nadie.
    `efectos`   — lista ya filtrada por lo que el personaje TIENE.
    `bases`     — valor o fórmula base por variable (p. ej. pg_max de calculo.py).
    `estado`    — condiciones (sin_armadura…), de `estado_de_equipo()`.
    """
    vocab = cargar_vocabulario()
    elecciones = elecciones or {}
    for v in entradas:
        if v not in vocab["variables"]:
            raise ErrorDeEfectos(f"variable de entrada no declarada: {v!r}")

    aplicables = [e for e in efectos if aplica(e, estado, vocab)]
    for ef in aplicables:
        if ef["op"] not in vocab["operaciones"]:
            raise ErrorDeEfectos(
                f"operación no declarada: {ef['op']!r} en «{ef.get('_rasgo')}»")
        if ef["objetivo"] not in vocab["variables"]:
            raise ErrorDeEfectos(
                f"objetivo no declarado: {ef['objetivo']!r} en "
                f"«{ef.get('_rasgo')}»")

    por_var = {}
    for ef in aplicables:
        por_var.setdefault(ef["objetivo"], []).append(ef)

    pendientes = sorted(set(por_var) | set(bases))
    entorno = dict(entradas)
    for v in orden_de_calculo(pendientes, por_var, bases, vocab):
        b = bases.get(v)
        if b is None:
            decl = vocab["variables"][v].get("base_por_defecto")
            b = evaluar(decl, entorno) if decl else None
        elif isinstance(b, str):
            b = evaluar(b, entorno)
        entorno[v] = agregar(v, por_var.get(v, []), b, entorno,
                             elecciones.get(f"{v}_base"),
                             decimal=bool(vocab["variables"][v].get("decimal")))
    return {v: entorno[v] for v in pendientes}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("listar", help="todos los efectos declarados en la base")
    p = sub.add_parser("explicar", help="qué efectos aplica una ficha y por qué")
    p.add_argument("--ficha", required=True)
    a = ap.parse_args()

    if a.cmd == "listar":
        efs = efectos_declarados()
        print(f"{len(efs)} efectos declarados en la base\n" + "─" * 74)
        for e in efs:
            req = ",".join(e.get("requiere", []) or []) or "—"
            print(f" {e['objetivo']:<10} {e['op']:<5} {str(e['formula']):<28} "
                  f"[{req}]  ← {e['_rasgo']} · {e['_archivo']}")
    else:
        import verificar_personaje  # noqa: reutiliza su resolución de refs
        print("usa `python3 verificar_personaje.py <ficha>`: el motor va dentro")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ── De la ficha a los efectos que de verdad tiene el personaje ───────────
_RASGOS_DE_CLASE = {
    "Bárbaro": "barbaro", "Bardo": "bardo", "Brujo": "brujo",
    "Clérigo": "clerigo", "Druida": "druida", "Explorador": "explorador",
    "Guerrero": "guerrero", "Hechicero": "hechicero", "Mago": "mago",
    "Monje": "monje", "Paladín": "paladin", "Pícaro": "picaro",
}

_RE_CA = None


def efectos_de_equipo(refs, entrenamientos=None, fuerza=None):
    """Efectos que aporta lo que el personaje lleva puesto.

    Se DERIVAN del campo `ca` que ya tiene cada registro de
    `equipo/armaduras.yaml`; no se escriben a mano en el YAML.

    **Dos reglas del bloque `reglas` de ese fichero, que hasta el 2026-08-30 el
    motor ignoraba** — las destapó un agente construyendo personajes a
    propósito, no ningún chequeo:

      · «Solo obtienes el bonificador a la CA de un escudo **si tienes
        entrenamiento con escudos**.» El motor sumaba el +2 siempre, así que un
        mago con escudo salía con 2 puntos de CA que no le tocan.
      · «Si la tabla indica una puntuación de Fuerza para un tipo de armadura,
        esta **reduce 3 m la velocidad** de quien la lleve, salvo que su Fuerza
        sea igual o superior a la indicada.» El motor no la aplicaba nunca. Escribir «+2»
    otra vez al lado del «+2» que ya está es el modo de fallo nº 10 de este
    proyecto («dato agregado»): dos copias que nadie vuelve a comparar y que
    divergen en silencio la primera vez que alguien corrige una.
    """
    import re
    d = yaml.safe_load((B / "equipo/armaduras.yaml").read_text(encoding="utf-8"))
    pag = {"pdf": 218, "libro": 216}
    idx = {}
    for g in _ARMADURAS:
        for a in d[g]["tabla"]:
            idx[a["nombre"].lower()] = ("armadura", a)
    for e in d["escudos"]["tabla"]:
        idx[e["nombre"].lower()] = ("escudo", e)

    salida = []
    for ref in refs:
        clave = ref.split("#")[-1].lower()
        if clave not in idx:
            continue
        tipo, reg = idx[clave]
        marco = {"_archivo": "equipo/armaduras.yaml", "_rasgo": reg["nombre"],
                 "_nivel": None, "_contenedor": None, "objetivo": "ca",
                 "pagina": pag, "requiere": []}
        if tipo == "escudo":
            entrenado = any("escudo" in str(e).lower()
                            for e in (entrenamientos or []))
            if entrenado:
                salida.append(dict(marco, op="add",
                                   formula=str(reg["ca"]).replace("+", "").strip()))
            continue
        f = str(reg["ca"])
        m = re.match(r"^(\d+)(?:\s*\+\s*mod\.\s*Des(?:\s*\(máx\.\s*(\d+)\))?)?$", f)
        if not m:
            raise ErrorDeEfectos(
                f"fórmula de CA no reconocida en {reg['nombre']!r}: {f!r}")
        termino = ""
        if "mod. Des" in f:
            termino = (f" + min(mod_des, {m.group(2)})" if m.group(2)
                       else " + mod_des")
        salida.append(dict(marco, op="base", formula=m.group(1) + termino))
        # La penalización de velocidad por Fuerza insuficiente.
        req = reg.get("fuerza")
        if req and fuerza is not None and fuerza < req:
            salida.append(dict(marco, objetivo="velocidad", op="add",
                               formula="-3",
                               _regla=f"equipo/armaduras.yaml → reglas.fuerza: "
                                      f"{reg['nombre']} pide Fuerza {req} y el "
                                      f"personaje tiene {fuerza}"))
    return salida


def efectos_de_ficha(ficha):
    """Los efectos que el personaje tiene DERECHO a usar: los de su especie,
    los de sus clases hasta el nivel que lleva en cada una, los de su subclase
    y los de su equipo. `nivel_clase` se resuelve por clase, no globalmente."""
    salida = []
    esp = ficha["especie"]["ref"].split("#")[-1]
    for ef in efectos_declarados([("especies/especies.yaml", ("especies", "rasgos"))]):
        if ef["_contenedor"] == esp:
            salida.append(dict(ef, _nivel_clase=None))

    for c in ficha.get("clases", []):
        nombre, nivel = c["clase"], c["nivel"]
        stem = _RASGOS_DE_CLASE.get(nombre)
        if stem is None:
            raise ErrorDeEfectos(f"clase desconocida: {nombre!r}")
        for rel, camino, filtro in (
                (f"clases/rasgos/{stem}.yaml", ("rasgos",), None),
                (f"clases/subclases/{stem}.yaml", ("subclases", "rasgos"),
                 (c.get("subclase") or "").split("#")[-1] or None)):
            if not (B / rel).exists():
                continue
            for ef in efectos_declarados([(rel, camino)]):
                if filtro is not None and ef["_contenedor"] != filtro:
                    continue
                if filtro is None and camino[0] == "subclases":
                    continue
                if (ef["_nivel"] or 1) > nivel:
                    continue
                salida.append(dict(ef, _nivel_clase=nivel))

    entren = [a.get("categoria") for a in
              ((ficha.get("competencias") or {}).get("armaduras") or [])]
    fue = ((ficha.get("caracteristicas") or {}).get("final") or {}).get("fue")
    salida += [dict(e, _nivel_clase=None)
               for e in efectos_de_equipo([q["ref"] for q in ficha.get("equipo", [])],
                                          entren, fue)]
    return salida


def calcular_de_ficha(ficha, mods, pb, pg_base):
    """Punto de entrada único desde `calculo.py` / `verificar_personaje.py`.

    `nivel_clase` es por efecto: un rasgo de Hechicero escala con los niveles
    de Hechicero, no con el nivel total. Por eso cada efecto se evalúa con su
    propio entorno en vez de con uno global.
    """
    efs = efectos_de_ficha(ficha)
    estado = estado_de_equipo([q["ref"] for q in ficha.get("equipo", [])])
    entradas = dict(mods, pb=pb, nivel_total=ficha["nivel_total"], nivel_clase=0)

    # Cada efecto lleva su `nivel_clase`; se resuelve su fórmula a un entero
    # ANTES de agregar, para que ninguna variable signifique dos cosas a la vez.
    vocab = cargar_vocabulario()
    resueltos = []
    for ef in efs:
        if not aplica(ef, estado, vocab):
            continue
        ent = dict(entradas, nivel_clase=ef.get("_nivel_clase") or 0)
        if ef.get("columna"):
            # `columna` lee la tabla dispersa de la clase que concede el efecto:
            # el stem sale de su propio `_archivo`, así que no hace falta
            # pasárselo por fuera ni escribirlo dos veces.
            stem = pathlib.Path(ef["_archivo"]).stem
            v = valor_de_columna(stem, ef["columna"], ent["nivel_clase"])
            resueltos.append(dict(ef, _valor=v, formula=None))
        else:
            resueltos.append(dict(ef, formula=str(evaluar(ef["formula"], ent))))

    esp = yaml.safe_load((B / "especies/especies.yaml").read_text(encoding="utf-8"))
    nombre_esp = ficha["especie"]["ref"].split("#")[-1]
    vel = next((e.get("velocidad_m") for e in esp.get("especies", [])
                if e["nombre"] == nombre_esp), None)
    bases = {"ca": None, "pg_max": pg_base}
    if vel is not None:
        bases["velocidad"] = vel
    return calcular(entradas, resueltos, bases, estado, ficha.get("elecciones"))
