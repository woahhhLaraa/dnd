#!/usr/bin/env python3
"""Validador de la base canónica D&D 2024 (5.5e).
No consulta el manual: comprueba coherencia interna. Un dato inventado
que no respete estas reglas hace fallar la validación.
Uso: python3 validar.py
"""
import functools, math, re, json, sys, pathlib
try:
    import yaml
except ImportError:
    yaml = None

B = pathlib.Path(__file__).parent

# ── Espacios de conjuro: la autoridad vive en la base, no aquí ────────────
# Hasta el 2026-09-02 estas dos tablas eran literales de Python **sin cita de
# página**, y eran contra lo que se contrastaban las progresiones de 7 clases.
# No era el defecto del §2 del Plan 18 —las copias sí se comparaban— pero sí
# una autoridad sin fuente por encima de una base citada: si el manual y el
# literal discrepaban, ganaba el literal, y la única forma de enterarse era
# leer `validar.py`. Lo destapó el censo (bloque A) al contar las columnas de
# tabla de clase que nadie contrasta contra una fuente.
#
# La tabla del lanzador completo YA estaba en la base, citada: es
# `multiclase.lanzamiento_de_conjuros_multiclase.tabla_espacios_de_conjuro`
# de `reglas/generacion_personaje.yaml` (pdf 47 = libro 45). Así que se lee.
# Es el mismo arreglo que `_TABLA_COSTE` (caso 4 del §2): un comentario que
# señalaba dónde vive la autoridad, y debajo una copia.
#
# La del lanzador medio **no se copia ni se inventa: se deriva** con la regla
# que el propio manual imprime al lado, en `calculo_nivel_para_tabla` —«la
# mitad (redondeando arriba) de los niveles de explorador y paladín»—. Se
# comprobó nivel a nivel que reproduce exactamente lo que decía el literal en
# los 20 niveles antes de sustituirlo.
_ESPACIOS_MAX = 9          # la escala de conjuros llega a 9 en 2024
_ESPACIOS_MEDIO_MAX = 5    # un lanzador medio no pasa del nivel 5 de conjuro


@functools.lru_cache(maxsize=None)
def _espacios_completo():
    """La tabla de espacios del lanzador completo, leída de la base."""
    f = B / "reglas" / "generacion_personaje.yaml"
    if yaml is None or not f.exists():
        raise RuntimeError("no se puede leer la tabla de espacios de conjuro: "
                           "sin ella no hay contra qué contrastar las clases")
    d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    tabla = (((d.get("multiclase") or {})
              .get("lanzamiento_de_conjuros_multiclase") or {})
             .get("tabla_espacios_de_conjuro") or {})
    filas = tabla.get("filas") or []
    if len(filas) != 20 or not tabla.get("fuente"):
        # Falla ruidosamente: devolver una tabla a medias haría pasar en verde
        # a clases que nadie ha comprobado, que es peor que no comprobar.
        raise RuntimeError(
            "`tabla_espacios_de_conjuro` de reglas/generacion_personaje.yaml "
            f"tiene {len(filas)} filas y "
            f"{'una' if tabla.get('fuente') else 'NINGUNA'} cita: se esperaban "
            "20 filas citadas")
    return [[fila.get(str(j), 0) for j in range(1, _ESPACIOS_MAX + 1)]
            for fila in filas]


@functools.lru_cache(maxsize=None)
def _espacios_medio():
    """La del lanzador medio, DERIVADA de la anterior con la regla citada."""
    completo = _espacios_completo()
    return [completo[math.ceil(n / 2) - 1][:_ESPACIOS_MEDIO_MAX]
            for n in range(1, 21)]

def parse_yaml(p):
    """Parser mínimo para el formato de estas fichas (sin dependencias)."""
    txt = p.read_text(encoding="utf-8")
    meta = {}
    for k in ("clase","edicion","lanzador","aptitud_magica"):
        m = re.search(rf"^{k}:\s*(.+)$", txt, re.M)
        if m: meta[k] = m.group(1).strip().strip('"').split("#")[0].strip()
    filas = []
    for l in txt.splitlines():
        m = re.search(r"\{n:\s*(\d+),(.*)\}\s*$", l)
        if not m: continue
        fila = {"n": int(m.group(1))}
        cuerpo = m.group(2)
        sl = re.search(r"slots:\s*\[([\d,\s]+)\]", cuerpo)
        if sl: fila["slots"] = [int(x) for x in sl.group(1).split(",")]
        for cm in re.finditer(r"(\w+):\s*([^,\[\]]+?)(?=,\s*\w+:|\s*$)", cuerpo):
            k, v = cm.group(1), cm.group(2).strip().strip('"').strip("'")
            if k in ("slots","rasgos","n"): continue
            fila[k] = int(v) if re.fullmatch(r"\d+", v) else v
        ra = re.search(r"rasgos:\s*\[(.*?)\]", cuerpo)
        fila["rasgos"] = [x.strip().strip('"') for x in ra.group(1).split('",') if x.strip()] if ra and ra.group(1).strip() else []
        filas.append(fila)
    return meta, filas

def validar_clase(p):
    err, warn = [], []
    meta, filas = parse_yaml(p)
    nom = meta.get("clase", p.stem)

    if meta.get("edicion") != "2024 (5.5e)":
        err.append(f"edición no sellada como 2024: {meta.get('edicion')!r}")
    if len(filas) != 20:
        err.append(f"{len(filas)} filas, se esperaban 20"); return nom, err, warn

    for i, f in enumerate(filas):
        n = f["n"]
        if n != i + 1:
            err.append(f"nivel fuera de secuencia en fila {i+1}: {n}")
        esperado = 2 + (n - 1) // 4
        if f.get("pb") != esperado:
            err.append(f"N{n}: competencia {f.get('pb')} != {esperado}")

    lanz = meta.get("lanzador")
    if lanz == "completo":
        for f in filas:
            if f.get("slots") != _espacios_completo()[f["n"]-1]:
                err.append(f"N{f['n']}: espacios {f.get('slots')} != "
                           f"{_espacios_completo()[f['n']-1]}")
    elif lanz == "medio":
        for f in filas:
            if f.get("slots") != _espacios_medio()[f["n"]-1]:
                err.append(f"N{f['n']}: espacios {f.get('slots')} != "
                           f"{_espacios_medio()[f['n']-1]}")
    elif lanz in ("ninguno", "pacto"):
        pass
    else:
        err.append(f"tipo de lanzador desconocido: {lanz!r}")

    # monotonía: ninguna de estas columnas puede decrecer al subir de nivel
    for col in ("trucos","prep","invocaciones","puntos_hechiceria","puntos_concentracion",
                "furias","dano_furia","maestria_armas","canalizar","forma_salvaje",
                "enemigo_predilecto","tomar_aliento","espacios","nivel_espacios","mov_sin_armadura_m"):
        vals = [f[col] for f in filas if isinstance(f.get(col), (int, float))]
        if len(vals) == len(filas) and vals != sorted(vals):
            err.append(f"columna '{col}' decrece: {vals}")

    # dados que escalan (d6 -> d8 -> d10 -> d12) nunca bajan
    for col in ("dado","artes_marciales","ataque_furtivo"):
        vals = [str(f.get(col,"")).strip('"') for f in filas if f.get(col)]
        if len(vals) == 20:
            num = [int(re.sub(r".*d","",v)) * (int(re.match(r"(\d*)d",v).group(1) or 1)) for v in vals]
            if num != sorted(num):
                err.append(f"columna '{col}' decrece: {vals}")

    # mejoras de característica: deben existir al menos en 4, 8, 12, 16
    # El marcador se LEE de `reglas/subida_de_nivel.yaml` (auditoría del
    # 2026-09-03): aquí estaba la cadena escrita a mano, y con `in` sobre el
    # texto en vez de la comparación que declara la base.
    import calculo
    mejoras = {f["n"] for f in filas
               if any(calculo.es_marcador_de("mejora_caracteristica_o_dote", r)
                      for r in f["rasgos"])}
    faltan = {4,8,12,16} - mejoras
    if faltan:
        err.append(f"faltan mejoras de característica en niveles {sorted(faltan)}")

    if not re.search(r"pagina_pdf:\s*\d+", p.read_text(encoding="utf-8")):
        err.append("sin cita de página")
    if "verificado:" not in p.read_text(encoding="utf-8"):
        warn.append("sin sello de verificación")
    return nom, err, warn

# Conjuros cuya descripción remite al manual en vez de contener el dato.
# Es el peor defecto posible en esta base: el campo NO está vacío, así que
# ningún chequeo de completitud lo veía, pero la base deja de ser
# autosuficiente justo donde el LLM tiene prohibido tirar de memoria.
# Se descubrió el 2026-08-21 auditando «Mano de Bigby» (ya corregido).
# Cada entrada dice qué falta y dónde está; cualquier marcador NO declarado
# aquí es un error, para que esta deuda no pueda crecer en silencio.
# Conjuros cuya `descripcion` remite al manual en vez de traer el dato, con
# lo que les falta. **Vacío desde el 2026-08-22**: los cuatro que quedaban
# (Deseo, Guardas y guardias, Símbolo y Muro prismático) se transcribieron por
# lectura visual y la base volvió a ser autosuficiente.
#
# Que esté vacío es justo lo que lo hace útil: a partir de ahora **cualquier**
# descripción que remita al MdJ es un error, no un aviso. Si alguna vez hay que
# volver a declarar deuda aquí, se anota con su página y qué falta — nunca se
# deja un hueco silencioso.
PLACEHOLDERS_CONOCIDOS = {}
_RE_PLACEHOLDER = re.compile(r"revisa(?:r)?\b[^.]{0,60}\bMdJ\b", re.I)


def validar_hechizos():
    err, warn = [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "hechizos", ["falta hechizos.json"], []
    d = json.loads(f.read_text(encoding="utf-8"))
    hs = d["hechizos"]
    if d["_meta"]["edicion"] != "2024 (5.5e)":
        err.append("edición no sellada como 2024")
    for h in hs:
        if not h["nombre"]: err.append("hechizo sin nombre")
        if not isinstance(h["nivel"], int) or not 0 <= h["nivel"] <= 9:
            err.append(f"{h['nombre']}: nivel inválido {h['nivel']}")
        if not h["escuela"] or isinstance(h["escuela"], list):
            err.append(f"{h['nombre']}: escuela ausente o ambigua")
        if not h["fuente"]["pagina_libro"]:
            err.append(f"{h['nombre']}: sin cita de página")
        if h["nivel"] == 0 and h["concentracion"] and not h["duracion"]:
            warn.append(f"{h['nombre']}: truco con concentración sin duración")

        # Coherencia interna de los componentes. Nació de un defecto real:
        # la conversión del CSV rellenó `consume_material` desde una columna
        # que en realidad significaba «tiene precio», y `Toque helado` acabó
        # con coste y consumo pese a no tener componente material — el coste
        # se había colado de la fila contigua. Ninguno de los dos campos
        # tiene sentido sin material.
        comp = h.get("componentes") or {}
        if not comp.get("material"):
            if comp.get("consume_material"):
                err.append(f"{h['nombre']}: consume_material sin componente "
                           f"material")
            if comp.get("coste"):
                err.append(f"{h['nombre']}: coste {comp['coste']!r} sin "
                           f"componente material")

        # ¿la descripción remite al manual en vez de traer el dato?
        if _RE_PLACEHOLDER.search(h.get("descripcion") or ""):
            pendiente = PLACEHOLDERS_CONOCIDOS.get(h["nombre"])
            if pendiente:
                warn.append(f"{h['nombre']}: descripción incompleta, remite al "
                            f"manual — falta {pendiente}")
            else:
                err.append(f"{h['nombre']}: la descripción remite al manual "
                           f"(«revisar… en el MdJ») y no está declarada como "
                           f"deuda conocida en PLACEHOLDERS_CONOCIDOS")

    # una deuda declarada que ya no existe también es un error: significa que
    # se corrigió y nadie borró la entrada, y la lista deja de ser fiable
    nombres = {h["nombre"] for h in hs}
    for n in PLACEHOLDERS_CONOCIDOS:
        if n not in nombres:
            err.append(f"PLACEHOLDERS_CONOCIDOS cita {n!r}, que no existe")
        elif not _RE_PLACEHOLDER.search(
                next(h for h in hs if h["nombre"] == n).get("descripcion") or ""):
            err.append(f"{n}: ya no remite al manual — bórralo de "
                       f"PLACEHOLDERS_CONOCIDOS")
    return f"hechizos ({len(hs)})", err, warn


def _yaml_txt(rel):
    f = B / rel
    return f.read_text(encoding="utf-8") if f.exists() else None

def validar_trasfondos():
    err, warn = [], []
    t = _yaml_txt("trasfondos/trasfondos.yaml")
    if t is None: return "trasfondos", ["falta trasfondos/trasfondos.yaml"], []
    bloques = re.split(r"^  - nombre:", t, flags=re.M)[1:]
    if len(bloques) != 16:
        err.append(f"{len(bloques)} trasfondos, se esperaban 16")
    nombres = []
    for b in bloques:
        nom = b.split("\n")[0].strip()
        nombres.append(nom)
        car = re.search(r"caracteristicas:\s*\[(.*?)\]", b)
        if not car:
            err.append(f"{nom}: sin puntuaciones de característica"); continue
        n = len([x for x in car.group(1).split(",") if x.strip()])
        if n != 3:
            err.append(f"{nom}: {n} puntuaciones, se esperaban 3")
        for campo in ("dote:", "habilidades:", "herramienta:", "equipo_a:", "equipo_b:"):
            if campo not in b: err.append(f"{nom}: falta {campo[:-1]}")
        hab = re.search(r"habilidades:\s*\[(.*?)\]", b)
        if hab and len([x for x in hab.group(1).split(",") if x.strip()]) != 2:
            err.append(f"{nom}: no tiene exactamente 2 habilidades")
        if "pdf:" not in b: err.append(f"{nom}: sin cita de página")
    if len(set(nombres)) != len(nombres):
        err.append("hay trasfondos duplicados")
    return f"trasfondos ({len(bloques)})", err, warn

def validar_especies():
    err, warn = [], []
    t = _yaml_txt("especies/especies.yaml")
    if t is None: return "especies", ["falta especies/especies.yaml"], []
    bloques = re.split(r"^  - nombre:", t, flags=re.M)[1:]
    if len(bloques) != 10:
        err.append(f"{len(bloques)} especies, se esperaban 10")
    for b in bloques:
        nom = b.split("\n")[0].strip()
        for campo in ("tipo:", "tamano:", "velocidad_m:", "rasgos:"):
            if campo not in b: err.append(f"{nom}: falta {campo[:-1]}")
        v = re.search(r"velocidad_m:\s*([\d.]+)", b)
        if v and not (6 <= float(v.group(1)) <= 12):
            err.append(f"{nom}: velocidad fuera de rango ({v.group(1)} m)")
        if "pdf:" not in b: err.append(f"{nom}: sin cita de página")
    return f"especies ({len(bloques)})", err, warn

# --- Caras de dado admisibles en D&D 2024 -----------------------------------
# Nació de un defecto real: `Dedo de la muerte` decía «7d8 + 3d0» donde el
# manual dice «7d8 + 30» (pdf 270 = libro 268). El «0» de «30» lo leyó la
# conversión del CSV como notación de dado. Sobrevivió a las cuatro capas de
# validación porque `3d0` es sintácticamente un dado: tiene número y caras.
# Ningún chequeo miraba si esas caras existen. Estas siete son las únicas que
# el juego usa, y el barrido de toda la base lo confirma empíricamente:
# {4: 56, 6: 203, 8: 187, 10: 107, 12: 57, 20: 45, 100: 2} y nada más.
_CARAS_VALIDAS = {4, 6, 8, 10, 12, 20, 100}
_RE_DADO = re.compile(r"(?<![A-Za-z0-9])(\d*)[dD](\d+)(?![0-9])")


def _texto_citable(obj):
    """Concatena el texto de un registro **saltándose los campos `_*`**.

    Los campos que empiezan por guion bajo son metadatos de procedencia
    (`_nota`, `_nota_verificacion`) y **citan a propósito el valor malo** que
    se corrigió. Barrerlos haría que el chequeo se disparase con su propia
    documentación: la primera versión de esta función encontró tres `d0`, y
    los tres estaban dentro de la nota que explica el arreglo de
    `Dedo de la muerte`.
    """
    if isinstance(obj, dict):
        return " ".join(_texto_citable(v) for k, v in obj.items()
                        if not str(k).startswith("_"))
    if isinstance(obj, list):
        return " ".join(_texto_citable(v) for v in obj)
    return str(obj) if obj is not None else ""


def validar_dados():
    """Ninguna tirada de la base puede usar un dado que no existe."""
    err, warn = [], []
    vistos = 0

    f = B / "hechizos.json"
    if f.exists():
        for h in json.loads(f.read_text(encoding="utf-8"))["hechizos"]:
            for m in _RE_DADO.finditer(_texto_citable(h)):
                vistos += 1
                caras = int(m.group(2))
                if caras not in _CARAS_VALIDAS:
                    err.append(f"{h['nombre']}: dado inexistente "
                               f"'{m.group(0)}' — las caras válidas son "
                               f"{sorted(_CARAS_VALIDAS)}")

    for p in sorted(B.rglob("*.yaml")):
        if "_verificacion" in p.parts or "foundry_srd52" in p.parts:
            continue
        # se salta la línea entera de cualquier campo `_*` por el mismo motivo
        lineas = [ln for ln in p.read_text(encoding="utf-8").splitlines()
                  if not re.match(r"\s*_[A-Za-z_]*:", ln)]
        for m in _RE_DADO.finditer("\n".join(lineas)):
            vistos += 1
            caras = int(m.group(2))
            if caras not in _CARAS_VALIDAS:
                err.append(f"{p.relative_to(B)}: dado inexistente "
                           f"'{m.group(0)}' — las caras válidas son "
                           f"{sorted(_CARAS_VALIDAS)}")

    if not vistos:
        err.append("el barrido de dados no encontró ninguna tirada: "
                   "el chequeo se ha quedado sin ver la base")
    return f"dados ({vistos} tiradas)", err, warn


# --- Conversiones de unidad --------------------------------------------------
# Nació de un defecto real: `Nube de dagas` decía «un cubo de 1,5 m / 10 pies»
# donde la página (pdf 316 = libro 314) dice solo «un cubo de 1,5 m», sin
# conversión — y 1,5 m son 5 pies, no 10. La base añade equivalencias que el
# manual no trae, y varias están mal calculadas.
#
# **El factor es el de juego, no el físico.** El manual convierte con la
# convención de la cuadrícula (5 pies = 1,5 m = 1 casilla), no con 3,28084.
# Medido sobre las 548 conversiones a pies de la base: el factor de juego deja
# 539 exactas y el físico solo 313. Usar el físico daría cientos de falsos
# positivos.
#
# Las unidades sin convención de juego (pulgadas, millas, yardas) sí van con el
# factor físico, y **desde metros**: la primera versión de este chequeo aplicó
# el factor de pulgadas sobre metros ya convertidos y dio 14 falsos positivos.
_A_METROS = {"cm": 0.01, "m": 1.0, "km": 1000.0}
_DESDE_METROS = {
    "pies": 5 / 1.5, "pie": 5 / 1.5, "f": 5 / 1.5,   # convención de juego
    "cas": 1 / 1.5,                                   # 1 casilla = 1,5 m
    "pulgadas": 39.3701, "pulgada": 39.3701,
    "millas": 1 / 1609.344, "milla": 1 / 1609.344, "mi": 1 / 1609.344,
    "yardas": 1.09361, "yarda": 1.09361,
}
_RE_CONVERSION = re.compile(
    r"(\d[\d.,’']*)\s*(cm|km|m)\s*/\s*(\d[\d.,’']*)\s*"
    r"(pies|pie|pulgadas|pulgada|millas|milla|yardas|yarda|mi|cas|f)\b"
)


def _num_es(s):
    """Lee un número escrito con cualquiera de las notaciones que usa la base.

    La base **mezcla tres notaciones decimales** —«1,5», «0.9» y «1’5»— y las
    tres aparecen en conversiones correctas. Un parser que asuma una sola las
    convierte en falsos positivos: la primera versión de este chequeo dio 5
    («1’5 km / 0,9 mi» leído como «5 km», y «0.9 mi» leído como 9), todos
    sobre datos buenos. Es la dirección de fallo que obliga a probar un chequeo
    nuevo también en negativo.

    Un punto solo cuenta como separador de millar si van exactamente tres
    dígitos detrás («5.000» = 5000, pero «0.9» = 0,9).
    """
    s = s.strip().replace("’", ",").replace("'", ",")
    if "," in s:
        return float(s.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d+(\.\d{3})+", s):
        return float(s.replace(".", ""))
    return float(s)


def validar_conversiones():
    """Ninguna conversión editorial en el texto citable, y la aritmética de los
    campos derivados de `alcance` correcta.

    ── Por qué este chequeo cambió de sentido el 2026-09-02 ─────────────────
    Antes comprobaba que las equivalencias «6 m / 20 pies» estuvieran **bien
    calculadas**. Estaban: 543 de ellas, todas correctas. El problema era otro,
    y es la debilidad nº 2 del `FODA.md`: **el manual castellano no imprime ni
    una sola unidad imperial.** Nueve lectores independientes sobre 23 páginas
    no vieron ninguna. Las había añadido la base entera, y `fidelidad: literal`
    convivía con texto que la página no imprime. Comprobar que un añadido está
    bien calculado no responde a si el añadido **debe existir**.

    Borradas (fase 2 del PLAN_19), este chequeo pasa a impedir que vuelvan.

    ── Y lo que NO se borró, porque no es cita sino dato ────────────────────
    `alcance` guarda además `metros`, `pies` y `casillas` como campos
    estructurados. Ésos se quedan: no son texto que finja ser del manual, son
    dato derivado, y `verificar_foundry.py` contrasta `alcance.pies` contra el
    SRD **número contra número**. Borrarlos habría dejado sin fuente externa
    los 218 alcances con cifra.

    Su aritmética sí hay que seguir comprobándola —si no, quitar las
    conversiones del texto habría abierto un hueco donde antes había un
    chequeo— así que la segunda mitad la hereda de la versión anterior, con la
    misma tolerancia absoluta y por la misma razón medida.
    """
    err, warn = [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "conversiones (0)", ["falta hechizos.json"], []
    hs = json.loads(f.read_text(encoding="utf-8"))["hechizos"]

    # ── (a) Ninguna conversión en el texto que la base presenta como cita ──
    colados = 0
    for h in hs:
        for campo, txt in (("alcance.texto", (h.get("alcance") or {}).get("texto")),
                           ("descripcion", h.get("descripcion"))):
            for m in _RE_CONVERSION.finditer(str(txt or "")):
                colados += 1
                err.append(
                    f"{h['nombre']} ({campo}): conversión editorial "
                    f"'{m.group(0)}' en texto citable. El manual castellano es "
                    f"métrico y no imprime unidades imperiales; las "
                    f"equivalencias se borraron el 2026-09-02 y no vuelven a "
                    f"entrar. Si hace falta la cifra en pies, va en el campo "
                    f"derivado `alcance.pies`, que no es cita")

    # ── (b) Los campos DERIVADOS de `alcance`, aritméticamente correctos ───
    # Tolerancia **absoluta**, no relativa, y por una razón medida sobre la
    # base ya corregida: los redondeos legítimos desvían como mucho 0,032
    # («0,93 mi» escrito «0,9»), mientras que el menor defecto real desvía 1
    # entero. Media unidad separa las dos poblaciones con holgura. Una
    # tolerancia relativa del 2 % —la primera versión— hacía lo contrario:
    # dejaba pasar «30 m / 98 pies» y saltaba con un redondeo de 0,03.
    derivados = 0
    for h in hs:
        a = h.get("alcance") or {}
        if a.get("metros") is None:
            # TOLERADO: los alcances sin cifra —«Toque», «Lanzador»— no tienen
            # nada que derivar. Que el barrido entero se quede sin ver la base
            # lo caza el `if not derivados` de abajo, que es error.
            continue
        metros = _num_es(str(a["metros"]))
        for campo, unidad in (("pies", "pies"), ("casillas", "cas")):
            if a.get(campo) is None:
                # TOLERADO: cuatro alcances kilométricos nunca tuvieron los
                # campos derivados (Clarividencia, Tsunami y las dos tormentas)
                # y no se les inventan: convertir 1,5 km a pies aquí sería
                # meter en la base un número que nadie ha leído en la página.
                continue
            derivados += 1
            declarado = _num_es(str(a[campo]))
            esperado = metros * _DESDE_METROS[unidad]
            margen = max(0.5, abs(esperado) * 0.005)
            if abs(declarado - esperado) > margen:
                err.append(
                    f"{h['nombre']}: `alcance.{campo}` es {declarado:g} y "
                    f"{metros:g} m son {esperado:.4g}. Es un campo DERIVADO: o "
                    f"está mal calculado, o `metros` no es lo que dice la página")

    if not derivados:
        err.append("el barrido no encontró ningún `alcance` con cifra: el "
                   "chequeo se ha quedado sin ver la base")
    return (f"conversiones ({derivados} derivados · {colados} coladas)",
            err, warn)


def validar_referencias():
    """Integridad referencial: los conjuros citados por las especies deben existir."""
    err, warn = [], []
    f = B / "hechizos.json"
    t = _yaml_txt("especies/especies.yaml")
    if f is None or t is None: return "referencias", [], []
    d = json.loads(f.read_text(encoding="utf-8"))
    idx = {h["nombre"].lower() for h in d["hechizos"]}
    citados = set()
    for m in re.finditer(r"nivel_[35]:\s*\"?([^\"\n,}]+)", t):
        citados.add(m.group(1).strip().rstrip('"'))
    for m in re.finditer(r"truco ([a-záéíóúñ ]+?)[\.,;\"]", t):
        citados.add(m.group(1).strip())
    # ── De aviso a ERROR (fase 1 del PLAN_19, 2026-09-02) ────────────────
    # Una especie que concede un truco que no existe en `hechizos.json` es
    # integridad referencial ROTA: el personaje tendría un conjuro que la base
    # no sabe describir. Salía como un ⚠ entre otros treinta y `validar.py`
    # terminaba con «0 errores». Hoy los 18 citados resuelven, así que
    # promoverlo no deja deuda.
    faltan = sorted(c for c in citados if c.lower() not in idx)
    for c in faltan:
        err.append(f"conjuro citado por una especie y ausente de "
                   f"hechizos.json: '{c}'. El personaje tendría un conjuro que "
                   f"la base no sabe describir")
    return f"referencias ({len(citados)} conjuros citados)", err, warn


def validar_subclases():
    """Cada clase debe tener 4 subclases y sus rasgos deben caer en los
    niveles que la tabla de esa clase ya validada declara."""
    err, warn, info = [], [], []
    d = B / "clases" / "subclases"
    if not d.exists():
        return "subclases", ["falta clases/subclases/"], []

    # niveles de subclase leídos de nuestras tablas de clase ya validadas
    niveles = {}
    for p in sorted((B / "clases").glob("*.yaml")):
        txt = p.read_text(encoding="utf-8")
        m = re.search(r"^clase:\s*(.+)$", txt, re.M)
        if not m: continue
        ns = []
        for l in txt.splitlines():
            mm = re.search(r"\{n:\s*(\d+),.*rasgos:\s*\[(.*?)\]", l)
            if mm and re.search(r"[Ss]ubclase", mm.group(2)):
                ns.append(int(mm.group(1)))
        niveles[m.group(1).strip()] = sorted(ns)

    hechas = 0
    for f in sorted(d.glob("*.yaml")):
        if f.name.startswith("_"): continue
        txt = f.read_text(encoding="utf-8")
        clase = re.search(r"^clase:\s*(.+)$", txt, re.M)
        if not clase:
            err.append(f"{f.name}: sin campo 'clase'"); continue
        clase = clase.group(1).strip()
        hechas += 1
        bloques = re.split(r"^  - nombre:", txt, flags=re.M)[1:]
        if len(bloques) != 4:
            (warn if "pendiente:" in txt else err).append(
                f"{clase}: {len(bloques)}/4 subclases")
        esperados = set(niveles.get(clase, []))
        for b in bloques:
            nom = b.split("\n")[0].strip()
            vistos = {int(x) for x in re.findall(r"nivel:\s*(\d+)", b)}
            fuera = vistos - esperados
            if fuera:
                err.append(f"{clase} / {nom}: rasgos en niveles imposibles {sorted(fuera)} "
                           f"(esperados {sorted(esperados)})")
            faltan = esperados - vistos
            if faltan:
                err.append(f"{clase} / {nom}: faltan niveles {sorted(faltan)}")
            if "pagina:" not in b:
                err.append(f"{clase} / {nom}: sin cita de página")
    info.append(f"{hechas}/12 clases con subclases escritas")
    return f"subclases ({hechas}/12 clases)", err, warn + info

def validar_dotes():
    """Cada archivo dotes/*.yaml debe citar página para cada dote, y toda
    dote referenciada por un trasfondo (campo 'dote:') debe existir aquí."""
    err, warn = [], []
    d = B / "dotes"
    if not d.exists():
        return "dotes", ["falta dotes/"], []

    esperadas = {"origen.yaml": 10, "generales.yaml": 43,
                 "estilo_de_combate.yaml": 10, "don_epico.yaml": 12}
    nombres = set()
    total = 0
    for fn, n_esperado in esperadas.items():
        f = d / fn
        if not f.exists():
            err.append(f"falta dotes/{fn}"); continue
        txt = f.read_text(encoding="utf-8")
        bloques = re.split(r"^  - nombre:", txt, flags=re.M)[1:]
        total += len(bloques)
        if len(bloques) != n_esperado:
            err.append(f"{fn}: {len(bloques)} dotes, se esperaban {n_esperado}")
        for b in bloques:
            nom = b.split("\n")[0].strip().strip('"')
            nombres.add(nom)
            if "pagina:" not in b:
                err.append(f"{fn} / {nom}: sin cita de página")
            if "prerrequisito:" not in b:
                err.append(f"{fn} / {nom}: sin campo prerrequisito (usar null si no tiene)")

    t = _yaml_txt("trasfondos/trasfondos.yaml")
    if t is not None:
        citadas = set()
        for m in re.finditer(r'dote:\s*"([^"]+)"', t):
            base = re.sub(r"\s*\(.*?\)\s*$", "", m.group(1)).strip()
            citadas.add(base)
        faltan = sorted(c for c in citadas if c not in nombres)
        for c in faltan:
            err.append(f"dote citada por un trasfondo y ausente de dotes/: '{c}'")

    return f"dotes ({total})", err, warn

def validar_equipo():
    """Comprueba los YAML de equipo/: que carguen, que cada arma/armadura/
    herramienta/objeto tenga precio y (donde aplique) página o descripción,
    y que las tablas de armas citen solo propiedades y maestrías definidas."""
    err, warn = [], []
    d = B / "equipo"
    if not d.exists():
        return "equipo", ["falta equipo/"], []
    if yaml is None:
        return "equipo", ["PyYAML no disponible: no se pudo validar equipo/"], []

    esperados = ("armas.yaml", "armaduras.yaml", "herramientas.yaml", "aventureros.yaml")
    total = 0
    for fn in esperados:
        f = d / fn
        if not f.exists():
            err.append(f"falta equipo/{fn}")

    armas_f = d / "armas.yaml"
    if armas_f.exists():
        data = yaml.safe_load(armas_f.read_text(encoding="utf-8"))
        props = set(data.get("propiedades", {}))
        maestrias = {k.capitalize() for k in data.get("propiedades_de_maestria", {})}
        for grupo in ("armas_cuerpo_a_cuerpo_sencillas", "armas_a_distancia_sencillas",
                      "armas_cuerpo_a_cuerpo_marciales", "armas_a_distancia_marciales"):
            armas = data.get(grupo, [])
            total += len(armas)
            for a in armas:
                if not a.get("precio"):
                    err.append(f"armas.yaml / {a.get('nombre')}: sin precio")
                if not a.get("maestria"):
                    err.append(f"armas.yaml / {a.get('nombre')}: sin maestría")
                elif a["maestria"] not in maestrias:
                    err.append(f"armas.yaml / {a.get('nombre')}: maestría '{a['maestria']}' no definida en propiedades_de_maestria")

    armaduras_f = d / "armaduras.yaml"
    if armaduras_f.exists():
        data = yaml.safe_load(armaduras_f.read_text(encoding="utf-8"))
        for grupo in ("armaduras_ligeras", "armaduras_medias", "armaduras_pesadas", "escudos"):
            filas = data.get(grupo, {}).get("tabla", [])
            total += len(filas)
            for a in filas:
                if not a.get("ca"):
                    err.append(f"armaduras.yaml / {a.get('nombre')}: sin CA")
                if not a.get("precio"):
                    err.append(f"armaduras.yaml / {a.get('nombre')}: sin precio")

    herr_f = d / "herramientas.yaml"
    if herr_f.exists():
        data = yaml.safe_load(herr_f.read_text(encoding="utf-8"))
        for grupo in ("herramientas_de_artesano", "otras_herramientas"):
            filas = data.get(grupo, [])
            total += len(filas)
            for h in filas:
                if not h.get("utilizar"):
                    err.append(f"herramientas.yaml / {h.get('nombre')}: sin descripción de 'utilizar'")

    avent_f = d / "aventureros.yaml"
    if avent_f.exists():
        data = yaml.safe_load(avent_f.read_text(encoding="utf-8"))
        tabla = data.get("tabla_peso_precio", [])
        desc = data.get("descripciones", {})
        total += len(tabla)
        nombres_tabla = {re.sub(r"\s*\(.*?\)\s*$", "", o["nombre"]).strip() for o in tabla}
        # objetos con reglas propias que deberían tener descripción (variable de precio => probablemente mecánico)
        sin_desc = sorted(n for n in nombres_tabla
                           if n not in desc and n not in
                           {"Canalizador arcano", "Canalizador druídico", "Munición", "Símbolo sagrado"})
        if len(sin_desc) > 5:
            warn.append(f"aventureros.yaml: {len(sin_desc)} objetos de la tabla sin descripción propia (posibles genéricos, revisar si hace falta)")

    return f"equipo ({total} entradas)", err, warn

CARACTERISTICAS = {"Fuerza", "Destreza", "Constitución", "Inteligencia", "Sabiduría", "Carisma"}
ABREV = {"Fuerza": "fue", "Destreza": "des", "Constitución": "con",
         "Inteligencia": "int", "Sabiduría": "sab", "Carisma": "car"}

def _principales(txt):
    """'Fuerza y Carisma' -> (['Fuerza','Carisma'], 'y'); 'Carisma' -> (['Carisma'], None)."""
    partes = re.split(r"\s+(y|o)\s+", str(txt).strip())
    if len(partes) == 1:
        return [partes[0]], None
    return [partes[0], partes[2]], partes[1]

@functools.lru_cache(maxsize=None)
def _clases_data():
    """Carga los 12 clases/*.yaml con PyYAML, indexados por el campo 'clase'.

    Cacheada el 2026-08-31: se llamaba 5 veces y costaba 2,8 s de los 13.
    Solo lectura, como `calculo.cargar`.
    """
    out = {}
    for p in sorted((B / "clases").glob("*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("clase"):
            out[d["clase"]] = (p.name, d)
    return out

def validar_atributos_basicos():
    """El bloque 'atributos_basicos' de cada clases/*.yaml: característica
    principal válida y coherente con la aptitud mágica, equipo inicial con
    opciones bien formadas (la última siempre solo oro) y cita de página con
    el desfase pdf = libro + 2 que rige todo el manual."""
    err, warn = [], []
    if yaml is None:
        return "atributos básicos", ["PyYAML no disponible: no se pudo validar atributos_basicos"], []

    clases = _clases_data()
    if len(clases) != 12:
        err.append(f"{len(clases)} clases legibles, se esperaban 12")

    hechas = 0
    for nom, (fn, d) in sorted(clases.items()):
        ab = d.get("atributos_basicos")
        if not isinstance(ab, dict):
            err.append(f"{nom}: sin bloque atributos_basicos")
            continue
        hechas += 1

        princ = ab.get("caracteristica_principal")
        if not princ:
            err.append(f"{nom}: sin caracteristica_principal")
        else:
            cs, conector = _principales(princ)
            for c in cs:
                if c not in CARACTERISTICAS:
                    err.append(f"{nom}: característica principal desconocida {c!r}")
            if len(cs) == 2 and conector not in ("y", "o"):
                err.append(f"{nom}: conector inválido en caracteristica_principal {princ!r}")
            apt = d.get("aptitud_magica")
            if apt and apt not in cs:
                err.append(f"{nom}: aptitud mágica '{apt}' no figura en la característica principal '{princ}'")

        eq = ab.get("equipo_inicial")
        if not isinstance(eq, dict) or not eq:
            err.append(f"{nom}: sin equipo_inicial")
        else:
            claves = sorted(eq)
            esperadas = [chr(ord("a") + i) for i in range(len(claves))]
            if claves != esperadas:
                err.append(f"{nom}: opciones de equipo {claves} no son una serie a, b, ... ")
            elif len(claves) < 2:
                err.append(f"{nom}: equipo_inicial con una sola opción (el manual siempre da al menos A o B)")
            for k in claves:
                v = str(eq[k]).strip()
                if not v:
                    err.append(f"{nom}: opción {k.upper()} de equipo vacía"); continue
                solo_oro = re.fullmatch(r"\d+ po", v)
                if k == claves[-1] and not solo_oro:
                    err.append(f"{nom}: la última opción de equipo debería ser solo oro, no {v!r}")
                if k != claves[-1]:
                    if solo_oro:
                        err.append(f"{nom}: la opción {k.upper()} es solo oro; el oro va siempre en la última")
                    elif " po" not in v:
                        warn.append(f"{nom}: la opción {k.upper()} no incluye monedas de oro")

        f = ab.get("fuente") or {}
        pdf, libro = f.get("pagina_pdf"), f.get("pagina_libro")
        if not pdf:
            err.append(f"{nom}: atributos_basicos sin cita de página")
        elif libro and pdf - libro != 2:
            err.append(f"{nom}: desfase pdf/libro {pdf}/{libro} != 2")
        if "verificado" not in ab:
            warn.append(f"{nom}: atributos_basicos sin sello de verificación")

    return f"atributos básicos ({hechas}/12)", err, warn

def validar_generacion():
    """reglas/generacion_personaje.yaml. Los tres métodos deben ser
    consistentes entre sí (el conjunto estándar cuesta exactamente los 27
    puntos de la compra por puntos), la tabla del conjunto estándar por clase
    debe repartir esas seis puntuaciones dando la más alta a la característica
    principal, y la tabla de espacios de conjuro multiclase debe coincidir con
    la de un lanzador completo."""
    err, warn = [], []
    f = B / "reglas" / "generacion_personaje.yaml"
    if not f.exists():
        return "generación de personaje", ["falta reglas/generacion_personaje.yaml"], []
    if yaml is None:
        return "generación de personaje", ["PyYAML no disponible: no se pudo validar"], []

    d = yaml.safe_load(f.read_text(encoding="utf-8"))
    if d.get("edicion") != "2024 (5.5e)":
        err.append(f"edición no sellada como 2024: {d.get('edicion')!r}")

    clases = _clases_data()
    principales = {n: (v.get("atributos_basicos") or {}).get("caracteristica_principal")
                   for n, (_, v) in clases.items()}

    # --- métodos de generación ---
    met = d.get("metodos_generacion_caracteristicas") or {}
    arr = (met.get("conjunto_estandar") or {}).get("puntuaciones") or []
    if len(arr) != 6:
        err.append(f"conjunto estándar con {len(arr)} puntuaciones, se esperaban 6")
    if arr != sorted(arr, reverse=True):
        err.append(f"conjunto estándar sin ordenar de mayor a menor: {arr}")

    cp = met.get("coste_en_puntos") or {}
    tabla = cp.get("tabla_coste") or {}
    puntos = cp.get("puntos_totales")
    if tabla:
        ks = sorted(tabla)
        if ks != list(range(min(ks), max(ks) + 1)):
            err.append(f"tabla de coste con huecos: {ks}")
        costes = [tabla[k] for k in ks]
        if costes != sorted(costes) or len(set(costes)) != len(costes):
            err.append(f"tabla de coste no es estrictamente creciente: {costes}")
        if tabla.get(min(ks)) != 0:
            err.append(f"la puntuación más baja ({min(ks)}) debería costar 0, cuesta {tabla[min(ks)]}")
        # invariante que ata los dos métodos: el conjunto estándar cuesta 27
        if arr and all(p in tabla for p in arr):
            total = sum(tabla[p] for p in arr)
            if total != puntos:
                err.append(f"el conjunto estándar cuesta {total} puntos, no los {puntos} de la compra por puntos")
        elif arr:
            fuera = [p for p in arr if p not in tabla]
            err.append(f"puntuaciones del conjunto estándar ausentes de la tabla de coste: {fuera}")
    else:
        err.append("sin tabla de coste en puntos")

    mods = (met.get("modificadores_por_puntuacion") or {}).get("tabla") or {}
    if not mods:
        err.append("sin tabla de modificadores por puntuación")
    # La tabla se contrasta contra `calculo.modificador()`, que es LA
    # implementación que usa todo el proyecto — no contra una copia de la
    # fórmula escrita aquí (auditoría del 2026-09-03). Hasta hoy esta línea
    # decía `(p - 10) // 2`: una TERCERA copia de la misma regla, así que la
    # tabla de la base y la fórmula de `calculo.py` podían divergir sin que
    # este chequeo se enterara — contrastaba validar.py contra la base,
    # dejando fuera justo al módulo que hace la cuenta de verdad.
    #
    # La base trae `formula:` Y `tabla:` a propósito, y esta es la razón de
    # ser de esa duplicación: la fórmula es la implementación y la tabla es su
    # prueba. Es el patrón de `cobertura.py` con las 18 habilidades.
    import calculo
    for k, v in mods.items():
        rango = [int(x) for x in re.findall(r"\d+", str(k))]
        for p in range(rango[0], rango[-1] + 1):
            if calculo.modificador(p) != v:
                err.append(f"modificador de {k} es {v} en la tabla y "
                           f"calculo.modificador({p}) da {calculo.modificador(p)}")
                break

    # --- conjunto estándar por clase ---
    ce = (d.get("conjunto_estandar_por_clase") or {}).get("filas") or []
    if len(ce) != 12:
        err.append(f"conjunto estándar por clase con {len(ce)} filas, se esperaban 12")
    vistas = set()
    for fila in ce:
        nom = fila.get("clase")
        vistas.add(nom)
        if nom not in clases:
            err.append(f"conjunto estándar: clase desconocida {nom!r}"); continue
        vals = [fila.get(a) for a in ("fue", "des", "con", "int", "sab", "car")]
        if None in vals:
            err.append(f"{nom}: fila del conjunto estándar incompleta"); continue
        if sorted(vals, reverse=True) != arr:
            err.append(f"{nom}: {vals} no es un reparto de {arr}")
            continue
        princ = principales.get(nom)
        if not princ:
            continue
        cs, _ = _principales(princ)
        # el manual asigna la puntuación más alta a la característica principal
        # (y la segunda más alta a la segunda, cuando la clase lista dos)
        for i, c in enumerate(cs):
            if c not in ABREV:
                continue
            esperado = arr[i]
            real = fila.get(ABREV[c])
            if real != esperado:
                err.append(f"{nom}: {c} debería llevar {esperado} (característica principal "
                           f"{'primaria' if i == 0 else 'secundaria'}), lleva {real}")
    faltan = set(clases) - vistas
    if faltan:
        err.append(f"clases ausentes del conjunto estándar por clase: {sorted(faltan)}")

    # --- multiclase ---
    mc = d.get("multiclase") or {}
    for k in ("puntos_experiencia", "puntos_golpe_y_dados_golpe", "bonificador_por_competencia",
              "competencias_al_multiclasear", "clase_de_armadura", "ataque_adicional",
              "lanzamiento_de_conjuros_multiclase"):
        if not mc.get(k):
            err.append(f"multiclase: falta la regla '{k}'")

    req = (mc.get("requisitos_por_clase") or {}).get("tabla") or {}
    if len(req) != 12:
        err.append(f"requisitos de multiclase para {len(req)} clases, se esperaban 12")
    for nom, v in req.items():
        if nom not in clases:
            err.append(f"requisito de multiclase para clase desconocida {nom!r}"); continue
        texto = (v or {}).get("requisito", "")
        cs = re.findall(r"([A-ZÁÉÍÓÚ][a-záéíóún]+)\s*13\+", texto)
        conector = re.search(r"13\+\s+(y|o)\s+", texto)
        conector = conector.group(1) if conector else None
        princ = principales.get(nom)
        if not princ:
            continue
        cs_esp, con_esp = _principales(princ)
        if cs != cs_esp or conector != con_esp:
            err.append(f"{nom}: requisito de multiclase '{texto}' no concuerda con "
                       f"la característica principal '{princ}'")

    lz = mc.get("lanzamiento_de_conjuros_multiclase") or {}
    filas = (lz.get("tabla_espacios_de_conjuro") or {}).get("filas") or []
    if len(filas) != 20:
        err.append(f"tabla de espacios multiclase con {len(filas)} filas, se esperaban 20")
    else:
        # ── Qué se comprueba aquí y qué NO, desde el 2026-09-02 ──────────
        # Esta tabla ES la fuente citada de los espacios del lanzador completo
        # (pdf 47 = libro 45): hasta hoy se comparaba contra el literal
        # `COMPLETO` de este mismo fichero, que no tenía cita. Ahora que la
        # autoridad es la tabla, compararla con `_espacios_completo()` sería
        # compararla consigo misma, y un chequeo tautológico en verde es peor
        # que ninguno: parece que cubre algo.
        #
        # El contraste numérico real lo hace `validar_clase()`, que enfrenta
        # esta tabla a las progresiones de las 8 clases de lanzador completo y
        # las 2 de lanzador medio —transcritas cada una desde su propia página
        # del manual—. Se comprobó: mover una fila de esta tabla saca 7 clases
        # en rojo. Aquí quedan las propiedades que ESA comprobación no ve: que
        # la tabla tenga sus 20 filas, en orden, y sin huecos de columna.
        for i, fila in enumerate(filas):
            if fila.get("nivel") != i + 1:
                err.append(f"tabla multiclase: nivel fuera de secuencia en fila {i+1}")
            faltan = [j for j in range(1, _ESPACIOS_MAX + 1) if str(j) not in fila]
            if faltan:
                err.append(f"tabla multiclase N{i+1}: le faltan las columnas "
                           f"{faltan} (un nivel de conjuro ausente no es un 0: "
                           f"es un dato que nadie ha transcrito)")
    if not lz.get("calculo_nivel_para_tabla"):
        err.append("multiclase: falta la regla de cálculo del nivel de lanzador")

    return "generación de personaje", err, warn

# --- Marcadores de la tabla de clase que no son rasgos con texto propio ---
# La lista vivía aquí cableada y otra copia en `subir_nivel.py`, ya divergidas
# (ver la cabecera de `calculo.es_marcador`). Ahora se lee de
# `reglas/subida_de_nivel.yaml → marcadores`, que es donde está declarada.
def _es_marcador(nombre):
    import calculo
    return calculo.es_marcador(nombre)

def validar_hechizos_clases():
    """Integridad referencial hechizos.json -> clases/*.yaml.

    El bug 'Clerigo' (sin tilde) sobrevivió a todas las fases porque nadie
    cruzaba nunca hechizos[].clases con el campo 'clase' real de las clases.
    Un nombre mal escrito no produce un error: produce un filtro que devuelve
    0 conjuros en silencio, y un orquestador LLM que recibe 0 conjuros
    concluye que no hay e improvisa con reglas de 2014.
    """
    err, warn, info = [], [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "hechizos ⊆ clases", ["falta hechizos.json"], []
    if yaml is None:
        return "hechizos ⊆ clases", ["PyYAML no disponible: no se pudo validar"], []

    d = json.loads(f.read_text(encoding="utf-8"))
    hs = d["hechizos"]
    clases = _clases_data()
    validas = set(clases)
    if not validas:
        return "hechizos ⊆ clases", ["no se pudo leer ninguna clases/*.yaml"], []

    reparto, desconocidas, vacias = {}, {}, []
    for h in hs:
        cs = h.get("clases")
        if not isinstance(cs, list):
            err.append(f"{h['nombre']}: campo 'clases' ausente o no es una lista")
            continue
        if not cs:
            vacias.append(h["nombre"])
            continue
        for c in cs:
            reparto[c] = reparto.get(c, 0) + 1
            if c not in validas:
                desconocidas.setdefault(c, []).append(h["nombre"])

    for c, hechizos in sorted(desconocidas.items()):
        cerca = sorted(v for v in validas
                       if v.lower().replace("á","a").replace("é","e").replace("í","i")
                          .replace("ó","o").replace("ú","u")
                       == c.lower().replace("á","a").replace("é","e").replace("í","i")
                          .replace("ó","o").replace("ú","u"))
        pista = f" (¿quisiste decir {cerca[0]!r}?)" if cerca else ""
        err.append(f"clase inexistente en hechizos[].clases: {c!r}{pista} — "
                   f"{len(hechizos)} conjuros, p. ej. {hechizos[0]!r}")

    for n in vacias:
        warn.append(f"{n}: lista 'clases' vacía (ningún filtro por clase lo encontrará)")

    # el mismo conjuro dos veces (mismo título inglés) devuelve resultados
    # duplicados y potencialmente contradictorios a cualquier filtro
    por_en = {}
    for h in hs:
        en = (h.get("nombre_en") or "").strip()
        if en:
            por_en.setdefault(en, []).append(h["nombre"])
    for en, noms in sorted(por_en.items()):
        if len(noms) > 1:
            warn.append(f"conjuro duplicado ({en}): {noms}")

    # los alias existen para que una búsqueda por un nombre alternativo resuelva
    # al conjuro correcto; si un alias choca con el nombre real de otro conjuro
    # (o dos conjuros comparten alias), la búsqueda vuelve a ser ambigua
    nombres = {h["nombre"] for h in hs}
    visto = {}
    for h in hs:
        al = h.get("alias") or []
        if not isinstance(al, list):
            err.append(f"{h['nombre']}: campo 'alias' no es una lista"); continue
        for a in al:
            if a in nombres:
                err.append(f"{h['nombre']}: el alias {a!r} es el nombre real de otro conjuro")
            if a in visto:
                err.append(f"alias {a!r} compartido por {visto[a]!r} y {h['nombre']!r}")
            visto[a] = h["nombre"]

    # una clase lanzadora sin ningún conjuro casi siempre significa filtro roto
    for nom, (_, cd) in sorted(clases.items()):
        lanz = str(cd.get("lanzador", "")).split("#")[0].strip()
        if lanz and lanz != "ninguno" and not reparto.get(nom):
            warn.append(f"{nom} es lanzador '{lanz}' y no tiene ni un conjuro en hechizos.json")

    info.append("reparto: " + ", ".join(f"{c} {n}" for c, n in
                                        sorted(reparto.items(), key=lambda kv: -kv[1])))
    if vacias:
        info.append(f"{len(vacias)} conjuro(s) sin ninguna clase")
    return f"hechizos ⊆ clases ({len(hs)} conjuros)", err, warn + info

def validar_rasgos_clase():
    """clases/rasgos/<clase>.yaml (Fase 10): el texto de los rasgos del tronco.

    Cruce bidireccional de nombres contra progresion[].rasgos[] de
    clases/<clase>.yaml — sobrantes y faltantes son error —, el nivel debe ser
    uno de los que la tabla concede ese rasgo, y cada rasgo necesita página y
    texto. Los archivos aún no escritos no son error: se informa del progreso.
    """
    err, warn, info = [], [], []
    d = B / "clases" / "rasgos"
    if yaml is None:
        return "rasgos de clase", ["PyYAML no disponible: no se pudo validar"], []
    clases = _clases_data()  # {nombre_clase: (fichero, datos)}
    total = len(clases) or 12
    if not d.exists():
        return f"rasgos de clase (0/{total})", [], [f"clases/rasgos/ todavía no existe"]

    # esperados: por clase, {nombre_rasgo: [niveles en que la tabla lo concede]}
    esperados, por_fichero = {}, {}
    for nom, (fn, cd) in clases.items():
        m = {}
        for fila in cd.get("progresion") or []:
            for r in fila.get("rasgos") or []:
                if _es_marcador(r):
                    continue
                m.setdefault(r, []).append(fila["n"])
        esperados[nom] = m
        por_fichero[pathlib.Path(fn).stem] = nom

    hechas = 0
    for f in sorted(d.glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        try:
            rd = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:
            err.append(f"{f.name}: no se puede leer como YAML ({e})"); continue
        if not isinstance(rd, dict):
            err.append(f"{f.name}: contenido inesperado"); continue
        hechas += 1
        clase = rd.get("clase")
        esperada = por_fichero.get(f.stem)
        if not clase:
            err.append(f"{f.name}: sin campo 'clase'"); continue
        if esperada and clase != esperada:
            err.append(f"{f.name}: campo clase {clase!r} no coincide con clases/{f.stem}.yaml ({esperada!r})")
        if clase not in esperados:
            err.append(f"{f.name}: clase {clase!r} no existe en clases/*.yaml"); continue
        if rd.get("edicion") != "2024 (5.5e)":
            err.append(f"{clase}: edición no sellada como 2024: {rd.get('edicion')!r}")

        exp = esperados[clase]
        rasgos = rd.get("rasgos") or []
        if not isinstance(rasgos, list) or not rasgos:
            err.append(f"{clase}: sin lista 'rasgos'"); continue

        vistos = set()
        for r in rasgos:
            if not isinstance(r, dict) or not r.get("nombre"):
                err.append(f"{clase}: entrada de rasgo sin 'nombre'"); continue
            nombre = r["nombre"]
            if _es_marcador(nombre):
                err.append(f"{clase} / {nombre}: es un marcador de la tabla, no se transcribe")
                continue
            if nombre not in exp:
                err.append(f"{clase} / {nombre!r}: rasgo sobrante — no aparece en "
                           f"progresion[].rasgos[] de clases/{f.stem}.yaml")
                continue
            vistos.add(nombre)
            niv = r.get("nivel")
            if niv is None:
                err.append(f"{clase} / {nombre}: sin 'nivel'")
            elif niv not in exp[nombre]:
                err.append(f"{clase} / {nombre}: nivel {niv} no coincide con la tabla de la "
                           f"clase, que lo concede en {exp[nombre]}")
            if not r.get("pagina"):
                err.append(f"{clase} / {nombre}: sin cita de página")
            if "desc" not in r:
                err.append(f"{clase} / {nombre}: sin campo 'desc'")
            elif r["desc"] is None:
                warn.append(f"{clase} / {nombre}: desc null (duda registrada, sin texto todavía)")
            elif not str(r["desc"]).strip():
                err.append(f"{clase} / {nombre}: 'desc' vacía")

        faltan = sorted(set(exp) - vistos)
        for n in faltan:
            err.append(f"{clase} / {n!r}: rasgo faltante — está en la tabla de la clase "
                       f"(N{exp[n][0]}) y no en clases/rasgos/{f.stem}.yaml")

        # El manual expone los rasgos en orden de nivel, así que la página citada
        # no puede retroceder al subir de nivel. Una inversión delata una cita
        # mal copiada — un error que ni el nombre ni el nivel ni la 'desc'
        # revelan, y que rompe la comprobabilidad de la cita, que es lo único
        # que separa a un auditor de un adivino.
        # Excepción: un rasgo que la tabla concede en varios niveles se describe
        # una sola vez, en el más bajo; sus repeticiones citan esa misma página.
        # Eso ocurre de dos formas, y hay que contemplar las dos:
        #   a) la tabla repite el MISMO nombre en varios niveles;
        #   b) la tabla distingue las repeticiones con un paréntesis
        #      ('Acción súbita (un uso)' N2, 'Acción súbita (dos usos)' N17),
        #      pero el manual las describe una sola vez, en la primera.
        # Sin (b), una cita correcta se marcaba como error: pasó con la Acción
        # súbita del Guerrero, descrita entera en pdf 115 aunque el rasgo
        # reaparezca en el nivel 17.
        def _base(n):
            return re.sub(r"\s*\([^)]*\)\s*$", "", str(n or "")).strip()

        primera, primera_base = {}, {}
        for r in rasgos:
            n, pg = r.get("nombre"), (r.get("pagina") or {}).get("pdf")
            if not (n and pg):
                continue
            niv = r.get("nivel", 99)
            if n not in primera or niv < primera[n][0]:
                primera[n] = (niv, pg)
            b = _base(n)
            if b not in primera_base or niv < primera_base[b][0]:
                primera_base[b] = (niv, pg)
        orden = sorted((r for r in rasgos if (r.get("pagina") or {}).get("pdf")),
                       key=lambda r: (r.get("nivel") or 0))
        tope, tope_nom = 0, None
        for r in orden:
            nombre, pg = r.get("nombre"), r["pagina"]["pdf"]
            if len(exp.get(nombre, [])) > 1 and pg == primera[nombre][1]:
                continue  # (a) repetición legítima del mismo texto
            b = _base(nombre)
            if (b != nombre and b in primera_base and pg == primera_base[b][1]
                    and primera_base[b][0] < (r.get("nivel") or 0)):
                continue  # (b) repetición con paréntesis, descrita en la primera
            if pg < tope:
                err.append(f"{clase} / {nombre} (N{r.get('nivel')}): cita pdf {pg}, anterior a "
                           f"la de {tope_nom} pdf {tope} — el manual va en orden de nivel, "
                           f"revisa la cita")
            else:
                tope, tope_nom = pg, f"{nombre} (N{r.get('nivel')})"

    info.append(f"{hechas}/{total} clases con el texto de sus rasgos escrito")
    if hechas < total:
        pendientes = sorted(n for st, n in por_fichero.items()
                            if not (d / f"{st}.yaml").exists())
        if pendientes:
            info.append("pendientes: " + ", ".join(pendientes))
    return f"rasgos de clase ({hechas}/{total})", err, warn + info

# ── FASE 11: competencias de clase, habilidades e idiomas ─────────────────
# Nada de esto repite el manual: cruza tablas transcritas por separado (la
# página «Atributos básicos de <clase>», la tabla de habilidades, los
# trasfondos y los ejemplos de multiclase) de modo que un error de lectura en
# una sola de ellas rompe la coherencia del conjunto.

DADOS_GOLPE = {"d6", "d8", "d10", "d12"}
CAMPOS_FASE11 = ("dado_golpe", "salvaciones", "habilidades", "armas",
                 "armaduras", "herramientas")

def _sinac(s):
    """Minúsculas sin tildes, para cruzar 'Clérigo' con 'clerigo'."""
    tabla = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    return str(s).strip().lower().translate(tabla)

def _habilidades_canonicas():
    """Las 18 habilidades de reglas/habilidades.yaml, o None si aún no existe.

    Devolver None (y no un conjunto vacío) es deliberado: un conjunto vacío
    convertiría 'el fichero no está' en '18 habilidades inexistentes', que es
    justo el falso positivo que impediría trabajar mientras la tabla se
    transcribe.
    """
    f = B / "reglas" / "habilidades.yaml"
    if yaml is None or not f.exists():
        return None
    try:
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(d, dict):
        return None
    filas = d.get("habilidades")
    if not isinstance(filas, list):
        return None
    return {h.get("nombre") for h in filas if isinstance(h, dict) and h.get("nombre")}

def validar_habilidades():
    """reglas/habilidades.yaml — la tabla de las 18 habilidades.

    Comprueba que estén las 18, sin duplicados, cada una con una de las seis
    características. Cruce fuerte: todas las habilidades citadas por los 16
    trasfondos (`trasfondos/trasfondos.yaml`) deben existir en esta tabla —
    dos transcripciones independientes que tienen que cuadrar. El fichero
    todavía inexistente no es error: se informa del progreso.
    """
    err, warn, info = [], [], []
    f = B / "reglas" / "habilidades.yaml"
    if yaml is None:
        return "habilidades", ["PyYAML no disponible: no se pudo validar"], []
    if not f.exists():
        return "habilidades (0/18)", [], ["reglas/habilidades.yaml todavía no existe"]

    d = yaml.safe_load(f.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        return "habilidades", ["reglas/habilidades.yaml no es un mapa YAML"], []
    if d.get("edicion") and d["edicion"] != "2024 (5.5e)":
        err.append(f"edición no sellada como 2024: {d['edicion']!r}")

    filas = d.get("habilidades")
    if not isinstance(filas, list) or not filas:
        return "habilidades (0/18)", ["reglas/habilidades.yaml sin lista 'habilidades'"], []

    vistos = {}
    for h in filas:
        if not isinstance(h, dict):
            err.append(f"entrada que no es un mapa: {h!r}"); continue
        n = h.get("nombre")
        if not n:
            err.append(f"habilidad sin nombre: {h!r}"); continue
        if n in vistos:
            err.append(f"habilidad duplicada: {n!r}")
        vistos[n] = h
        c = h.get("caracteristica")
        if not c:
            err.append(f"{n}: sin característica asociada")
        elif c not in CARACTERISTICAS:
            err.append(f"{n}: característica desconocida {c!r}")
        if not str(h.get("desc") or "").strip():
            warn.append(f"{n}: sin descripción")

    if len(filas) != 18:
        err.append(f"{len(filas)} habilidades, el manual tiene 18")

    fu = d.get("fuente") or {}
    pdf, libro = fu.get("pagina_pdf"), fu.get("pagina_libro")
    if not pdf:
        err.append("reglas/habilidades.yaml sin cita de página")
    elif libro and pdf - libro != 2:
        err.append(f"desfase pdf/libro {pdf}/{libro} != 2")
    if "verificado" not in d:
        warn.append("reglas/habilidades.yaml sin sello de verificación")

    # Cruce fuerte: las habilidades de los trasfondos son otra transcripción
    # de la misma lista cerrada; ninguna puede caer fuera de la tabla.
    tf = B / "trasfondos" / "trasfondos.yaml"
    if tf.exists():
        td = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        usadas = set()
        for t in td.get("trasfondos") or []:
            for hab in t.get("habilidades") or []:
                usadas.add(hab)
                if hab not in vistos:
                    err.append(f"trasfondo {t.get('nombre')}: habilidad {hab!r} no existe "
                               f"en reglas/habilidades.yaml")
        sobran = sorted(set(vistos) - usadas)
        if sobran:
            warn.append(f"{len(sobran)} habilidades que ningún trasfondo usa "
                        f"(normal, pero revisables): {', '.join(sobran)}")

    return f"habilidades ({len(vistos)}/18)", err, warn + info

def validar_idiomas():
    """reglas/idiomas.yaml — «Idiomas estándar» e «Idiomas inusuales».

    Común debe figurar entre los estándar (todo personaje lo habla), ninguna
    entrada puede repetirse ni aparecer en las dos tablas a la vez. Fichero
    inexistente = progreso, no error.
    """
    err, warn, info = [], [], []
    f = B / "reglas" / "idiomas.yaml"
    if yaml is None:
        return "idiomas", ["PyYAML no disponible: no se pudo validar"], []
    if not f.exists():
        return "idiomas (pendiente)", [], ["reglas/idiomas.yaml todavía no existe"]

    d = yaml.safe_load(f.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        return "idiomas", ["reglas/idiomas.yaml no es un mapa YAML"], []
    if d.get("edicion") and d["edicion"] != "2024 (5.5e)":
        err.append(f"edición no sellada como 2024: {d['edicion']!r}")

    grupos = {}
    for g in ("estandar", "inusuales"):
        filas = d.get(g)
        if not isinstance(filas, list) or not filas:
            err.append(f"reglas/idiomas.yaml sin lista '{g}'")
            grupos[g] = []
            continue
        nombres = []
        for it in filas:
            n = it.get("nombre") if isinstance(it, dict) else it
            if not n:
                err.append(f"{g}: entrada sin nombre: {it!r}"); continue
            if n in nombres:
                err.append(f"{g}: idioma duplicado {n!r}")
            nombres.append(n)
        grupos[g] = nombres

    if grupos.get("estandar") and not any(_sinac(n) == "comun" for n in grupos["estandar"]):
        err.append("«Común» no figura entre los idiomas estándar, y todo personaje lo habla")
    solapan = sorted(set(grupos.get("estandar", [])) & set(grupos.get("inusuales", [])))
    if solapan:
        err.append(f"idiomas en las dos tablas a la vez: {', '.join(solapan)}")

    fu = d.get("fuente") or {}
    pdf, libro = fu.get("pagina_pdf"), fu.get("pagina_libro")
    if not pdf:
        err.append("reglas/idiomas.yaml sin cita de página")
    elif libro and pdf - libro != 2:
        err.append(f"desfase pdf/libro {pdf}/{libro} != 2")
    if "verificado" not in d:
        warn.append("reglas/idiomas.yaml sin sello de verificación")

    n = len(grupos.get("estandar", [])) + len(grupos.get("inusuales", []))
    return f"idiomas ({n} entradas)", err, warn + info

def _dado_de_progresion(cd):
    """El dado de golpe según la columna 'dado' de progresion, si la hay.

    Ojo: esa columna NO siempre es el dado de golpe. En Bardo es el dado de
    Inspiración bárdica y sube d6→d12 con el nivel. Distingo por el único
    criterio disponible sin abrir el manual: un dado de golpe es constante en
    los 20 niveles; uno que cambia es un dado de rasgo. Devuelvo
    (dado, motivo_por_el_que_no_cruzo).
    """
    vals = [f.get("dado") for f in (cd.get("progresion") or []) if f.get("dado")]
    if not vals:
        return None, None
    únicos = set(vals)
    if len(únicos) > 1:
        return None, (f"la columna 'dado' de la progresión cambia con el nivel "
                      f"({'/'.join(sorted(únicos))}): es un dado de rasgo, no el de golpe")
    return vals[0], None

def _dados_de_multiclase():
    """Dados de golpe deducidos de los ejemplos de reglas/generacion_personaje.yaml.

    El apartado `multiclase.puntos_golpe_y_dados_golpe` ilustra la suma con
    ejemplos del tipo «guerrero 5/paladín 5 = 10d10» y «clérigo 5/paladín 5 =
    5d8 + 5d10». Esa prosa se transcribió aparte de las páginas de clase, así
    que sirve de segunda opinión sobre el dado de tres clases.
    """
    f = B / "reglas" / "generacion_personaje.yaml"
    if yaml is None or not f.exists():
        return {}
    try:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    txt = str(((d.get("multiclase") or {}).get("puntos_golpe_y_dados_golpe") or {}).get("regla") or "")
    out = {}
    # «a N/b N = XdY + ZdW»  -> a:dY, b:dW
    for m in re.finditer(r"([A-Za-zÁ-Úá-úñÑ]+)\s+\d+\s*/\s*([A-Za-zÁ-Úá-úñÑ]+)\s+\d+\s*=\s*"
                         r"\d+(d\d+)\s*\+\s*\d+(d\d+)", txt):
        out.setdefault(_sinac(m.group(1)), m.group(3))
        out.setdefault(_sinac(m.group(2)), m.group(4))
    # «a N/b N = XdY»  -> ambas dY
    for m in re.finditer(r"([A-Za-zÁ-Úá-úñÑ]+)\s+\d+\s*/\s*([A-Za-zÁ-Úá-úñÑ]+)\s+\d+\s*=\s*"
                         r"\d+(d\d+)(?!\s*\+)", txt):
        out.setdefault(_sinac(m.group(1)), m.group(3))
        out.setdefault(_sinac(m.group(2)), m.group(3))
    return out

def validar_competencias_clase():
    """Los campos de la Fase 11 en `atributos_basicos` de cada clases/*.yaml:
    dado_golpe, salvaciones, habilidades, armas, armaduras y herramientas.

    Reglas: `[]` en armaduras/herramientas es una respuesta válida y completa
    (Mago, Hechicero y Monje no tienen entrenamiento con armaduras); lo que
    deja al LLM improvisando es que el campo FALTE. Por eso una clase a medio
    transcribir —con unos campos nuevos y otros no— es error, mientras que una
    clase con ninguno todavía solo cuenta como pendiente.

    Cruces fuertes:
      · dado_golpe contra el campo suelto `dado_golpe` del nivel superior del
        fichero, si existe;
      · dado_golpe contra la columna `dado` de `progresion`, pero solo cuando
        esa columna es constante en los 20 niveles (si varía es el dado de un
        rasgo —la Inspiración bárdica— y no dice nada de los PG);
      · dado_golpe contra los ejemplos de suma de dados del apartado de
        multiclase de reglas/generacion_personaje.yaml;
      · habilidades.de contra reglas/habilidades.yaml, la misma tabla contra
        la que se cruzan los trasfondos.
    """
    err, warn, info = [], [], []
    if yaml is None:
        return "competencias de clase", ["PyYAML no disponible: no se pudo validar"], []

    clases = _clases_data()
    total = len(clases) or 12
    canon = _habilidades_canonicas()
    if canon is None:
        info.append("reglas/habilidades.yaml aún no existe: no se cruzan las "
                    "listas de habilidades de clase")
    mc = _dados_de_multiclase()

    hechas, pendientes = 0, []
    for nom, (fn, d) in sorted(clases.items()):
        ab = d.get("atributos_basicos")
        if not isinstance(ab, dict):
            continue        # ya lo denuncia validar_atributos_basicos()

        presentes = [c for c in CAMPOS_FASE11 if c in ab]
        if not presentes:
            pendientes.append(nom)
            continue
        faltan = [c for c in CAMPOS_FASE11 if c not in ab]
        for c in faltan:
            err.append(f"{nom}: falta el campo '{c}' en atributos_basicos "
                       f"(la clase ya tiene {', '.join(presentes)}; un campo ausente "
                       f"no es lo mismo que uno vacío)")
        if not faltan:
            hechas += 1

        # ── dado de golpe ────────────────────────────────────────────────
        if "dado_golpe" in ab:
            dg = ab["dado_golpe"]
            if dg not in DADOS_GOLPE:
                err.append(f"{nom}: dado_golpe {dg!r} no es uno de "
                           f"{'/'.join(sorted(DADOS_GOLPE, key=lambda x: int(x[1:])))}")
            suelto = d.get("dado_golpe")
            if suelto and suelto != dg:
                err.append(f"{nom}: dado_golpe {dg!r} en atributos_basicos pero "
                           f"{suelto!r} en el campo suelto del fichero")
            prog, motivo = _dado_de_progresion(d)
            if prog and prog != dg:
                err.append(f"{nom}: dado_golpe {dg!r} pero la columna 'dado' de la "
                           f"progresión dice {prog!r} en los 20 niveles")
            elif motivo:
                info.append(f"{nom}: {motivo}")
            esperado = mc.get(_sinac(nom))
            if esperado and esperado != dg:
                err.append(f"{nom}: dado_golpe {dg!r} contradice el ejemplo de "
                           f"multiclase de reglas/generacion_personaje.yaml ({esperado})")

        # ── salvaciones ──────────────────────────────────────────────────
        if "salvaciones" in ab:
            sv = ab["salvaciones"]
            if not isinstance(sv, list):
                err.append(f"{nom}: salvaciones no es una lista: {sv!r}")
            else:
                if len(sv) != 2:
                    err.append(f"{nom}: {len(sv)} competencias en salvación "
                               f"({', '.join(map(str, sv))}); toda clase tiene exactamente 2")
                if len(set(sv)) != len(sv):
                    err.append(f"{nom}: salvaciones repetidas: {sv!r}")
                for c in sv:
                    if c not in CARACTERISTICAS:
                        err.append(f"{nom}: salvación en característica desconocida {c!r}")

        # ── habilidades ──────────────────────────────────────────────────
        if "habilidades" in ab:
            h = ab["habilidades"]
            if not isinstance(h, dict):
                err.append(f"{nom}: habilidades debería ser {{elige, de}}, no {h!r}")
            else:
                de = h.get("de")
                elige = h.get("elige")
                if not isinstance(de, list) or not de:
                    err.append(f"{nom}: habilidades.de vacío o ausente")
                    de = []
                else:
                    if len(set(de)) != len(de):
                        err.append(f"{nom}: habilidades.de con repeticiones")
                    if canon is not None:
                        for hab in de:
                            if hab not in canon:
                                err.append(f"{nom}: habilidad {hab!r} no existe en "
                                           f"reglas/habilidades.yaml")
                if not isinstance(elige, int) or isinstance(elige, bool):
                    err.append(f"{nom}: habilidades.elige debe ser un entero, no {elige!r}")
                elif elige < 1:
                    err.append(f"{nom}: habilidades.elige = {elige}, debe ser ≥ 1")
                elif de and elige > len(de):
                    err.append(f"{nom}: habilidades.elige = {elige} pero la lista solo "
                               f"ofrece {len(de)} habilidades")
                elif de and elige == len(de):
                    warn.append(f"{nom}: elige {elige} de una lista de {len(de)}: "
                                f"no hay elección real, revisa la fila")

        # ── competencias con armas / armaduras / herramientas ────────────
        for campo, puede_vacio in (("armas", False), ("armaduras", True),
                                   ("herramientas", True)):
            if campo not in ab:
                continue
            v = ab[campo]
            if not isinstance(v, list):
                err.append(f"{nom}: {campo} debe ser una lista (usa [] si la fila "
                           f"dice «Ninguna»), no {v!r}")
                continue
            if not v and not puede_vacio:
                err.append(f"{nom}: {campo} vacío; toda clase tiene alguna competencia con armas")
            for x in v:
                if not isinstance(x, str) or not x.strip():
                    err.append(f"{nom}: entrada vacía o no textual en {campo}: {x!r}")

    if pendientes:
        info.append(f"pendientes ({len(pendientes)}): " + ", ".join(pendientes))
    return f"competencias de clase ({hechas}/{total})", err, warn + info

# ── Chequeo: vocabulario y coherencia del campo `tirada` ──────────────────
#
# Nació de dos defectos de la oleada 3 (2026-08-29). El campo `tirada` viene
# literal de la columna `como_usar` del CSV de origen, **ningún script lo
# consume**, y por eso nadie lo había mirado nunca: tenía **15 valores
# distintos para 6 tiradas posibles**. Cinco eran erratas de formato del mismo
# valor (`TdS Fue,`, `TdS Des`, `TdS Dest.`, `TdS Fuerza`, `D20+ata.conj,`).
# Es el mismo modo de fallo que `3d0` y que las listas de `clases` cortas: un
# valor con la forma correcta que ningún chequeo mira.
_TIRADAS_VALIDAS = {
    "Directo", "D20+ata.conj.", "D20+ata.CaC",
    "TdS Fue.", "TdS Des.", "TdS Con.", "TdS Int.", "TdS Sab.", "TdS Car.",
}
# Excepción **declarada, no silenciada**: en `Contactar con otro plano` la
# salvación la hace el lanzador, no el objetivo. «propia» codifica esa
# diferencia real y por eso no se normaliza. Es el control negativo del
# chequeo: si alguien lo "arregla", pierde información del manual.
_TIRADAS_EXCEPCION = {"Contactar con otro plano": "TdS Int. propia"}
# Un `Directo` cuya primera salvación cae antes de este punto del texto
# contradice el patrón medido (mediana 48 % en los `Directo`, 24 % en los
# `TdS`). Ver la docstring de `validar_tirada()`.
_UMBRAL_DISPARADOR = 1 / 3

_CARACT_DE_ABREV = {
    "Fue.": "Fuerza", "Des.": "Destreza", "Con.": "Constitución",
    "Int.": "Inteligencia", "Sab.": "Sabiduría", "Car.": "Carisma",
}
_CARACTS = r"(Fuerza|Destreza|Constituci[óo]n|Inteligencia|Sabidur[íi]a|Carisma)"
_RE_SALVACION = re.compile(
    r"(?:tirada|tiradas)\s+de\s+salvaci[óo]n\s+de\s+" + _CARACTS, re.I)
# Detección **laxa**: ¿el texto menciona una salvación, escrita como sea? La base
# no siempre dice «tirada de salvación de X»: a veces condensa a «tirada de X» o
# «salvación de X». Hace falta para distinguir «el campo se contradice con el
# texto» de «el texto no habla de salvaciones en absoluto», que es el caso de
# `Resurrección` — declaraba «TdS Sab.» sobre una página que no pide ninguna
# tirada, y la primera versión del chequeo pasaba de largo por no encontrar nada
# con qué comparar.
_RE_SALVACION_LAXA = re.compile(
    r"salvaci[óo]n|salvamento|(?:tirada|tiradas)\s+de\s+" + _CARACTS, re.I)
# «salvamento» no es del manual: es la forma que traía `Tsunami` desde el CSV.
# Se acepta como mención (para no dar un falso «no habla de salvaciones») pero
# se avisa aparte, porque delata texto nunca leído contra la página.
_RE_SALVAMENTO = re.compile(r"\bsalvamento\b", re.I)


def validar_tirada():
    """El campo `tirada` debe usar el vocabulario cerrado **y** concordar con
    la salvación que pide su propia descripción.

    Dos chequeos por el precio de uno, y ninguno necesita el manual:

    1. **Vocabulario.** Cualquier valor fuera de `_TIRADAS_VALIDAS` es error.
    2. **Coherencia interna.** Si `tirada` declara «TdS Sab.» pero la
       descripción del mismo registro solo pide salvación de Constitución, uno
       de los dos miente. Así se cazó `Inflingir heridas` (pdf 296 = libro 294),
       que llevaba «TdS Sab.» sobre un texto que decía Constitución — sin abrir
       el manual.

    **La semántica de «Directo», fijada el 2026-08-29:**

        `TdS <car.>`  la tirada de salvación **decide si el conjuro afecta al
                      objetivo**. Es el disparador.
        `Directo`     el conjuro **se manifiesta igualmente**. Puede haber
                      salvaciones después, pero modulan el daño o permiten
                      librarse de un estado ya aplicado — no evitan el conjuro.

    No es una convención elegida a dedo: se dedujo de los datos. Los conjuros
    **gemelos coinciden** (*Inmovilizar persona*/*monstruo*, *Dominar
    persona*/*monstruo*, *Hechizar persona*/*monstruo* y *Sugestión*/*Sugestión
    en masa* dicen los ocho `TdS Sab.`; *Curar heridas*/*en masa* y *Muro de
    fuego*/*Muro de espinas* dicen `Directo`), y las dos poblaciones están
    separadas por dónde aparece la primera salvación en el texto: **mediana del
    24 % en los `TdS` frente al 48 % en los `Directo`**. Si el campo fuera ruido
    del CSV, ni los pares coincidirían ni habría esa separación.

    **El juicio no se automatiza, y se intentó.** La posición sirve para
    *encontrar* candidatos, no para juzgarlos: de los 14 que marcó, la lectura
    de la página dijo que 4 eran correctos (*Castigo abrumador*, *Castigo
    furioso*, *Cono de frío*, *Esfera de llamas* — en todos el daño ocurre igual
    y la salvación solo lo modula). Un criterio estructural por texto
    («o la mitad del daño» frente a «o quedará…») tampoco acertó: falló en
    *Terremoto* y *Tormenta de la venganza*, que son gramaticalmente idénticos
    y semánticamente opuestos.

    Por eso el chequeo **avisa de lo no revisado en vez de decidir**: los
    registros verificados en la página llevan `_tirada_revisada`, y el aviso
    converge a cero según se leen. Vuelve a saltar con cualquier conjuro nuevo.
    """
    err, warn = [], []
    vistos = 0
    f = B / "hechizos.json"
    if not f.exists():
        return "tirada (0)", ["falta hechizos.json"], []

    directos = 0
    sin_revisar = []
    for h in json.loads(f.read_text(encoding="utf-8"))["hechizos"]:
        t = h.get("tirada")
        if t is None:
            continue
        vistos += 1
        nombre = h["nombre"]

        if _TIRADAS_EXCEPCION.get(nombre) == t:
            pass                                  # excepción citada arriba
        elif t not in _TIRADAS_VALIDAS:
            err.append(f"{nombre}: tirada '{t}' fuera del vocabulario "
                       f"— los valores válidos son {sorted(_TIRADAS_VALIDAS)}")
            continue

        # D1 (2026-08-30): antes esto usaba `_RE_SALVACION`, que exige el
        # «tirada de salvación de X» COMPLETO — y `hechizos.json` se declara
        # `fidelidad: mixto` porque parte del texto **elide «tirada de»**.
        # Nueve conjuros quedaban en la sombra y su coherencia nunca se
        # comprobó; tres de ellos con un `tirada: TdS X` sin contrastar. Se pasa
        # a la forma laxa, la misma que ya usa `validar_tiradas()`, descontando
        # el ruido de la regla de concentración.
        salvaciones = _caracts_de_salvacion(h.get("descripcion", ""))
        if t == "Directo":
            d = h.get("descripcion", "")
            m = _RE_SALVACION_LAXA.search(d)
            if not m or not d:
                continue
            if m.start() / len(d) < _UMBRAL_DISPARADOR:
                # Candidato: en esa posición la salvación suele ser el
                # disparador. **No es error**: hay que leer la página, porque
                # ninguna regla textual lo decide (ver la nota de abajo). El
                # aviso desaparece en cuanto el registro lleva
                # `_tirada_revisada`, así que converge a cero y vuelve a saltar
                # con cualquier conjuro nuevo.
                if not h.get("_tirada_revisada"):
                    sin_revisar.append(nombre)
            else:
                directos += 1
            continue
        if not t.startswith("TdS "):
            continue
        if _RE_SALVAMENTO.search(h.get("descripcion", "")):
            warn.append(f"{nombre}: la descripción dice «salvamento», que no es "
                        f"término del manual («tirada de salvación»)")
        if not salvaciones:
            # Ni una salvación en todo el texto: o falta un párrafo, o el campo
            # se inventó la tirada. Así se caza `Resurrección` (pdf 331), que
            # declaraba «TdS Sab.» sobre un conjuro que no pide ninguna.
            if not _RE_SALVACION_LAXA.search(h.get("descripcion", "")):
                err.append(
                    f"{nombre}: tirada dice '{t}' pero su descripción no menciona "
                    f"ninguna tirada de salvación")
            continue
        abrev = t[4:]
        esperada = _CARACT_DE_ABREV.get(abrev if abrev.endswith(".") else abrev)
        if esperada is None:
            continue
        # comparación sin tildes: la descripción escribe «Constitución» y la
        # tabla «Constitución», pero el OCR del CSV mezcló acentos.
        if _sinac(esperada.lower()) not in salvaciones:
            err.append(
                f"{nombre}: tirada dice '{t}' ({esperada}) pero su descripción "
                f"solo pide salvación de {', '.join(sorted(salvaciones))}")

    if not vistos:
        err.append("el barrido de `tirada` no vio ningún conjuro: "
                   "el chequeo se ha quedado sin ver la base")
    if directos:
        warn.append(f"{directos} conjuros con 'Directo' y salvación tardía "
                    f"— comportamiento normal de área/muro: la salvación modula")
    if sin_revisar:
        warn.append(f"{len(sin_revisar)} conjuros con 'Directo' y salvación "
                    f"temprana SIN revisar en la página: "
                    f"{', '.join(sorted(sin_revisar))}")
    return f"tirada ({vistos} conjuros)", err, warn

# ── Chequeo: contaminación entre conjuros vecinos de la misma página ──────
#
# El modo de fallo estructural del CSV de origen. Va por su tercer caso
# confirmado, y los tres son conjuros **impresos uno al lado del otro**:
#   · `Aura sagrada` llevaba, palabra por palabra, el texto de
#     `Aura mágica de Nystul`            (Fase 13o)
#   · `Polimorfar verdadero` llevaba las reglas de `Polimorfar`, incluida la
#     de terminar a 0 puntos de golpe    (oleada 3, pdf 322)
#   · `Presciencia` llevaba el `resumen` de `Presencia regia de Yolande`
#                                        (oleada 3, pdf 323)
# La conversión leyó la fila contigua.
#
# ⚠ **Este chequeo no puede decidir por sí solo, y no lo intenta.** El manual
# repite texto de verdad entre conjuros emparentados: `Dominar persona` y
# `Dominar monstruo`, `Hechizar persona` y `Hechizar monstruo`, `Inmovilizar
# persona` y `Inmovilizar monstruo` comparten párrafos enteros **porque así
# están impresos**. Ninguna medida de solapamiento distingue «el manual
# repite» de «el CSV calcó» sin abrir la página.
#
# Por eso el solapamiento sale como **aviso ordenado por gravedad**: sirve para
# decidir qué leer primero, no para dar nada por malo. Lo único que sí es error
# duro es un `resumen` **idéntico** en dos conjuros distintos, que no tiene
# lectura inocente: los resúmenes los escribimos nosotros, uno por conjuro.
_LONG_SHINGLE = 6
_UMBRAL_AVISO = 0.34       # Jaccard a partir del cual el par merece una lectura


def _shingles(txt, n=_LONG_SHINGLE):
    pal = re.findall(r"[\wáéíóúüñ]+", txt.lower())
    return {" ".join(pal[i:i+n]) for i in range(len(pal) - n + 1)}


def validar_vecindad():
    """Solapamiento de texto entre conjuros que citan la misma página."""
    err, warn = [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "vecindad (0)", ["falta hechizos.json"], []
    hs = json.loads(f.read_text(encoding="utf-8"))["hechizos"]

    cache = {h["nombre"]: _shingles(h.get("descripcion", "")) for h in hs}

    paginas = {}
    for h in hs:
        pag = str(h.get("fuente", {}).get("pagina_libro", "")).rstrip("*")
        if pag:
            paginas.setdefault(pag, []).append(h)

    pares, sosp = 0, []
    for pag, grupo in sorted(paginas.items()):
        for i in range(len(grupo)):
            for j in range(i + 1, len(grupo)):
                a, b = grupo[i], grupo[j]
                pares += 1

                ra = (a.get("resumen") or "").strip().lower()
                rb = (b.get("resumen") or "").strip().lower()
                if ra and ra == rb:
                    err.append(f"pág. {pag}: '{a['nombre']}' y '{b['nombre']}' "
                               f"tienen el MISMO resumen «{a['resumen']}» "
                               f"— uno de los dos está calcado del otro")

                sa, sb = cache[a["nombre"]], cache[b["nombre"]]
                if not sa or not sb:
                    continue
                jac = len(sa & sb) / len(sa | sb)
                if jac < _UMBRAL_AVISO:
                    continue
                # Una pareja ya leída en la página y declarada legítima deja de
                # avisar: si no, el mismo aviso pediría la misma lectura para
                # siempre y acabaría siendo ruido que nadie mira.
                ya = (b["nombre"] in (a.get("_vecindad_verificada") or "")
                      and a["nombre"] in (b.get("_vecindad_verificada") or ""))
                if not ya:
                    sosp.append((jac, pag, a["nombre"], b["nombre"]))

    for jac, pag, a, b in sorted(sosp, reverse=True):
        warn.append(f"pág. {pag}: '{a}' y '{b}' comparten el {jac:.0%} de su "
                    f"texto — leer la página antes de fiarse")

    if not pares:
        err.append("el barrido de vecindad no comparó ningún par: "
                   "el chequeo se ha quedado sin ver la base")
    return f"vecindad ({pares} pares de página)", err, warn


# ── Chequeo: erratas que delatan texto nunca leído contra la página ───────
#
# Dos detectores baratos que salieron de la oleada 3 y no necesitan el manual.
#
# El primero nació de `Mal de ojo`, que decía «acción **Dash**» — inglés crudo
# del CSV en un campo que se declara transcripción del manual castellano.
# Si hay una palabra en inglés, ese texto no se ha leído nunca contra la página.
# «acción bonus» (Sirviente invisible) no lo cazaba la primera lista: el
# anglicismo no siempre viene en mayúscula ni aislado — a veces es media
# expresión traducida a medias. El manual dice «acción adicional».
_INGLES_CRUDO = [
    "acci[óo]n bonus", "bonus action", "cantrip", "spell save",
    "Dash", "Dodge", "Disengage", "Ready", "Grapple", "Shove",
    "Stunned", "Charmed", "Frightened", "Restrained", "Incapacitated",
    "Blinded", "Deafened", "Poisoned", "Unconscious", "Paralyzed",
    "Petrified", "Exhaustion", "saving throw", "spell slot", "hit points",
]
_RE_INGLES = re.compile(r"\b(" + "|".join(_INGLES_CRUDO) + r")\b")

# El segundo caza palabras pegadas («eseconjuro», «conjurotermine»), que son
# huella de conversión automática. **No hay diccionario de español instalado**
# en la máquina (hunspell está, sus diccionarios no), así que el vocabulario se
# construye con la propia base: una palabra rara que se parte limpiamente en
# dos palabras muy frecuentes es una palabra pegada. Sobre los 391 conjuros da
# 6 sospechosos y 2 reales, así que los falsos positivos se declaran uno a uno
# en vez de subir el umbral y perder señal.
# Falsos positivos declarados uno a uno en vez de subir el umbral: la señal es
# tan escasa (2 defectos reales en 782 campos) que perderla saldría más caro
# que mantener esta lista. `determina`/`determinar` se parten en «de|termina»,
# y los verbos con enclítico en «verbo|los». Bajar la partición a i=2 —para ver
# artículos pegados como «elconjuro»— es lo que hizo aparecer esta familia, y
# de paso destapó las dos «tirada desalvación» reales.
_PEGADAS_FALSAS = {"realizados", "lanzarlos", "superarlas", "atravesarlos",
                   "sujetarlos", "recuperarlos", "convertirlos",
                   "determina", "determinar", "determinado", "determinada",
                   "delante", "delantera", "desenfundar", "desaparecer"}


def validar_ortografia():
    """Inglés sin traducir y palabras pegadas en el texto de los conjuros."""
    err, warn = [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "ortografía (0)", ["falta hechizos.json"], []
    hs = json.loads(f.read_text(encoding="utf-8"))["hechizos"]

    campos = []
    for h in hs:
        for c in ("descripcion", "resumen"):
            campos.append((h["nombre"], c, h.get(c) or ""))

    for nombre, campo, txt in campos:
        for m in sorted({m.group(1) for m in _RE_INGLES.finditer(txt)}):
            err.append(f"{nombre} · {campo}: término inglés sin traducir «{m}»")
        # «salvamento» no existe en el manual: la traducción es «tirada de
        # salvación». Apareció en 3 conjuros (Tsunami, Terremoto, Tormenta de la
        # venganza) y además **cegaba a `validar_tirada()`**, que buscaba la
        # palabra «salvación» para saber si el texto pedía una tirada.
        for m in sorted({m.group(0) for m in _RE_SALVAMENTO.finditer(txt)}):
            err.append(f"{nombre} · {campo}: «{m}» no es término del manual "
                       f"— la traducción es «tirada de salvación»")

    todas = re.findall(r"[a-záéíóúüñ]+", " ".join(t for _, _, t in campos).lower())
    frec = {}
    for w in todas:
        frec[w] = frec.get(w, 0) + 1
    vocab = {w for w, n in frec.items() if n >= 20}

    for nombre, campo, txt in campos:
        for w in sorted({w for w in re.findall(r"[a-záéíóúüñ]{9,}", txt.lower())}):
            if frec.get(w, 0) > 2 or w in _PEGADAS_FALSAS:
                continue
            # Se parte desde i=2 para ver los artículos y preposiciones
            # pegados («elconjuro»): la primera versión empezaba en 3 y ese
            # caso se le escapaba entero. Lo caza la prueba por mutación.
            for i in range(2, len(w) - 2):
                a, b = w[:i], w[i:]
                if a in vocab and b in vocab:
                    err.append(f"{nombre} · {campo}: palabra pegada «{w}» "
                               f"— ¿«{a} {b}»?")
                    break

    if not campos:
        err.append("el barrido de ortografía no vio ningún conjuro: "
                   "el chequeo se ha quedado sin ver la base")
    return f"ortografía ({len(campos)} campos)", err, warn

# ── Chequeo: la cita de página de un conjuro es un número limpio ──────────
#
# **Criterio de cita fijado el 2026-08-29, y es distinto del de los rasgos.**
#
#   · Conjuros  -> `pagina_libro` es la página donde **EMPIEZA** el conjuro.
#   · Rasgos    -> la cita apunta a donde está la **mecánica**, no donde
#                  empieza la sección.
#
# No es una incoherencia: un conjuro es una unidad tipográfica con cabecera
# propia y se localiza por ella, mientras que un rasgo de clase es un fragmento
# dentro de una sección larga, donde apuntar al principio no ayudaría a nadie.
# Es además la convención de facto de los 391 registros. Si algún día hace falta
# saber dónde termina un conjuro que se parte (`Mente en blanco`,
# `Urna mágica`), lo suyo es añadir `pagina_fin`, no mover la cita.
#
# El chequeo existe porque 116 registros traían un asterisco («310*») copiado
# tal cual de la columna `page` del CSV, **sin semántica deducible**: la
# hipótesis «marca los que se parten de página» falla en 5 de los 6 casos que se
# leyeron en la página. Se apartó a `fuente._pagina_origen_csv`.


def validar_citas_conjuro():
    """`fuente.pagina_libro` de cada conjuro debe ser un número limpio."""
    err, warn = [], []
    f = B / "hechizos.json"
    if not f.exists():
        return "citas de conjuro (0)", ["falta hechizos.json"], []
    hs = json.loads(f.read_text(encoding="utf-8"))["hechizos"]

    vistos = 0
    for h in hs:
        pag = h.get("fuente", {}).get("pagina_libro")
        vistos += 1
        if pag is None or not str(pag).strip():
            err.append(f"{h['nombre']}: sin página citada")
        elif not str(pag).strip().isdigit():
            err.append(f"{h['nombre']}: pagina_libro '{pag}' no es un número "
                       f"limpio — el valor crudo del CSV va en "
                       f"`fuente._pagina_origen_csv`")
    if not vistos:
        err.append("el barrido de citas no vio ningún conjuro: "
                   "el chequeo se ha quedado sin ver la base")
    return f"citas de conjuro ({vistos})", err, warn


# ── Chequeo: los costes de material que ninguna fuente externa cubre ──────
#
# `verificar_foundry.py` contrasta el coste contra el SRD, pero **33 conjuros
# de la base no están en el SRD**: para ellos no hay fuente externa posible y
# `coste: null` es ambiguo — puede significar «el material no cuesta nada» o
# «el coste se perdió en la conversión del CSV».
#
# Ya pasó una vez: `Golpe de viento acerado` tenía `coste: null` sobre una
# página que exige «un arma cuerpo a cuerpo que valga al menos 1 pp», y lo
# encontró una muestra aleatoria por casualidad.
#
# La única salida es leer la línea `Componentes` y **declarar el resultado**,
# incluido el negativo: un `_coste_verificado` que diga «sin coste, comprobado»
# vale tanto como uno que diga la cifra. El chequeo avisa de los que aún no lo
# llevan, así que converge a cero y vuelve a saltar con cualquier conjuro nuevo.


def validar_costes_sin_fuente():
    """Todo conjuro fuera del SRD con material debe tener el coste verificado."""
    err, warn = [], []
    f = B / "hechizos.json"
    srd = B / "_verificacion" / "foundry_srd52" / "spells24"
    if not f.exists() or not srd.exists():
        return "costes sin fuente (0)", [], ["falta hechizos.json o el pack del SRD"]

    en_srd = set()
    for p in srd.rglob("*.yml"):
        for ln in p.read_text(encoding="utf-8").splitlines():
            if ln.startswith("name:"):
                en_srd.add(ln.split(":", 1)[1].strip().strip('"\'').lower())
                break

    hs = json.loads(f.read_text(encoding="utf-8"))["hechizos"]
    sin_fuente, sin_verificar = 0, []
    for h in hs:
        if not h.get("componentes", {}).get("material"):
            continue
        if (h.get("nombre_en") or "").strip().lower() in en_srd:
            continue          # lo cubre verificar_foundry.py
        sin_fuente += 1
        if not h.get("_coste_verificado"):
            sin_verificar.append(h["nombre"])

    # ── De aviso a ERROR (fase 1 del PLAN_19, 2026-09-02) ────────────────
    # Este chequeo nunca llenaba `err`, así que su línea salía en ✅ pasara lo
    # que pasara con el dato y `validar.py` terminaba con «0 errores». Lo
    # destapó el bloque B al escribirle su prueba por mutación: no se le podía
    # probar nada porque no podía fallar.
    #
    # Se puede promover sin dejar deuda porque los 52 están a cero hoy: el
    # sello `_coste_verificado` está puesto en todos. Y el coste de que sea
    # error es exactamente el que se quiere — un conjuro nuevo con material
    # fuera del SRD **no entra** hasta que alguien lea su página, que es lo que
    # este chequeo existía para pedir. Ya pasó una vez: `Golpe de viento
    # acerado` tenía `coste: null` sobre una página que exige «un arma cuerpo a
    # cuerpo que valga al menos 1 pp», y lo encontró una muestra por casualidad.
    if not sin_fuente:
        warn.append("ningún conjuro con material queda fuera del SRD: "
                    "¿se ha movido el pack?")
    if sin_verificar:
        err.append(f"{len(sin_verificar)} de {sin_fuente} conjuros con material "
                   f"fuera del SRD sin `_coste_verificado`: "
                   f"{', '.join(sorted(sin_verificar)[:6])}"
                   + (" …" if len(sin_verificar) > 6 else "")
                   + ". Su precio no lo respalda ninguna fuente externa, así "
                     "que hay que leer la página y DECLARAR el resultado, "
                     "incluido el negativo («sin coste, comprobado»)")
    return f"costes sin fuente ({sin_fuente})", err, warn


# ── Chequeo: los efectos (Fase 14) ────────────────────────────────────────
# El defecto que motiva este chequeo: `calculo.py` traía las fórmulas de CA sin
# armadura como `lambda` con el Bárbaro y el Monje, y su comentario decía "las
# dos únicas excepciones en el tronco de clase, confirmado por grep". Era
# cierto y era el problema: hay CUATRO fórmulas, y las otras dos están en
# subclases. El grep miró donde el `lambda` sabía mirar.
#
# Por eso este chequeo tiene dos mitades, y la segunda es la que importa:
#   (a) que los efectos DECLARADOS sean válidos — barato y evidente;
#   (b) que no haya prosa que prometa una mecánica SIN efecto detrás — que es
#       lo que deja fuera al caso que nadie recuerda.
# Las frases de promesa vivían aquí, en una tupla escrita a mano, y conocían 2
# de las 3 variables calculables: `velocidad` entró en el motor el 2026-08-30 y
# nadie las actualizó. Es el caso 5 del §2 del Plan 18, cerrado el 2026-09-02
# leyéndolas de `reglas/efectos.yaml`, donde viven pegadas a su variable. Ver
# `_promesas()` más abajo: una variable `calculada` sin `promesas` es un error.


def validar_efectos():
    err, warn = [], []
    try:
        import efectos as E
    except Exception as e:  # noqa: BLE001
        return "efectos", [f"no se puede importar efectos.py: {e}"], []

    try:
        vocab = E.cargar_vocabulario()
        declarados = E.efectos_declarados()
    except E.ErrorDeEfectos as e:
        return "efectos", [str(e)], []

    # (a) los efectos declarados
    for ef in declarados:
        d = f"«{ef['_rasgo']}» ({ef['_archivo']})"
        if ef.get("objetivo") not in vocab["variables"]:
            err.append(f"objetivo no declarado {ef.get('objetivo')!r} en {d}")
            continue
        if ef.get("op") not in vocab["operaciones"]:
            err.append(f"operación no declarada {ef.get('op')!r} en {d}")
        for c in ef.get("requiere", []) or []:
            if c not in vocab["condiciones"]:
                err.append(f"condición no declarada {c!r} en {d}")
        # Un efecto trae `formula` **o** `columna`, nunca las dos: serían dos
        # fuentes del mismo dato. `columna` (Fase D4) lee la tabla dispersa de
        # la progresión de su clase, así que no menciona variables.
        tiene = [k for k in ("formula", "columna") if ef.get(k) is not None]
        if ef.get("op") == "conditional":
            # C4: no se calcula, se cita. Trae `texto` y NINGUNA fuente de
            # valor — si trajera fórmula, alguien acabaría agregándola.
            if not (ef.get("texto") or "").strip():
                err.append(f"{d}: `conditional` sin `texto`: un efecto que no "
                           f"se calcula tiene que decir qué hace")
            if tiene:
                err.append(f"{d}: `conditional` trae {tiene}, y no debe: es un "
                           f"efecto que NO se calcula")
        elif ef.get("op") == "modifica_tope":
            # Bloque C: nombra la variable acotada y da su valor NUEVO. Se
            # exige `formula` (el valor) y `tope` (a quién acota), y que ese
            # tope sea una variable declarada: un tope sobre algo que no
            # existe no modificaría nada y pasaría en verde.
            if "formula" not in tiene:
                err.append(f"{d}: `modifica_tope` sin `formula`: hay que decir "
                           f"cuál es el tope nuevo")
            variable = ef.get("tope")
            if not variable:
                err.append(f"{d}: `modifica_tope` sin `tope`: hay que decir a "
                           f"qué variable acota el límite que se cambia")
            elif variable not in vocab["variables"]:
                err.append(f"{d}: `modifica_tope` sobre {variable!r}, que no es "
                           f"una variable declarada en reglas/efectos.yaml")
            if not (ef.get("requiere") or []):
                err.append(f"{d}: `modifica_tope` sin `requiere`: un tope que "
                           f"se aplicara siempre cambiaría la CA de cualquier "
                           f"armadura, y el manual lo condiciona")
        elif len(tiene) != 1:
            err.append(f"{d}: un efecto debe traer `formula` O `columna`, "
                       f"y trae {tiene or 'ninguna de las dos'}")
        elif "columna" in tiene:
            stem = pathlib.Path(ef["_archivo"]).stem
            f_clase = B / f"clases/{stem}.yaml"
            if not f_clase.exists():
                err.append(f"{d}: usa `columna` pero {stem} no es una clase")
            else:
                dc = yaml.safe_load(f_clase.read_text(encoding="utf-8")) or {}
                cols = set()
                for fila in dc.get("progresion", []):
                    cols |= set(fila)
                if ef["columna"] not in cols:
                    err.append(f"{d}: la progresión de {dc.get('clase')} no "
                               f"tiene columna {ef['columna']!r}")
        else:
            try:
                usadas = E.variables_de(ef["formula"])
            except E.ErrorDeEfectos as e:
                err.append(f"{e} en {d}")
                continue
            for v in sorted(usadas - set(vocab["variables"])):
                err.append(f"la fórmula de {d} usa {v!r}, que no es variable "
                           f"declarada")
        # Regla 2 del proyecto: sin página citada, un dato no entra en la base.
        pag = ef.get("pagina") or {}
        if not isinstance(pag.get("pdf"), int) or not isinstance(pag.get("libro"), int):
            err.append(f"efecto sin cita de página numérica en {d}")

    # (b) prosa que promete mecánica sin efecto detrás
    #
    # La cobertura de este chequeo se DESCUBRE del vocabulario: toda variable
    # `calculada` tiene que traer sus `promesas`, y no traerlas es un error.
    # Así no se puede añadir una cuarta variable y dejar su prosa sin vigilar,
    # que es exactamente lo que pasó con `velocidad` durante tres días.
    promesas = []
    for nombre, v in (vocab.get("variables") or {}).items():
        if (v or {}).get("tipo") != "calculada":
            continue
        frases = (v or {}).get("promesas")
        if not frases:
            err.append(
                f"la variable calculable «{nombre}» no declara `promesas` en "
                f"reglas/efectos.yaml: sin las frases con las que su prosa la "
                f"anuncia, un rasgo puede prometerla y no declararla y nadie "
                f"lo diría")
            continue
        # ── Coincidencia con LÍMITE DE PALABRA (bloque C, 2026-09-02) ──
        # Buscar la frase como subcadena suelta da falsos positivos que además
        # son invisibles: «a tu ca» casaba dentro de «a tu CApacidad de carga»
        # del rasgo «Constitución poderosa» del Goliat, que no toca la CA de
        # nada. Un falso positivo aquí obliga a declarar ruido, y un
        # manifiesto lleno de ruido no lo lee nadie.
        #
        # El guardián se pone solo donde el borde de la frase es una letra: la
        # promesa «pg máximos +» termina en un signo, y exigirle límite detrás
        # la haría no casar nunca con «PG máximos +40».
        compiladas = []
        for f in frases:
            f = f.lower()
            ini = r"(?<!\w)" if f[:1].isalnum() else ""
            fin = r"(?!\w)" if f[-1:].isalnum() else ""
            compiladas.append(re.compile(ini + re.escape(f) + fin))
        promesas.append((nombre, tuple(compiladas)))

    con_efecto = {(ef["_archivo"], ef["_rasgo"], ef["objetivo"]) for ef in declarados}
    for rel, camino in E.origenes():
        doc = yaml.safe_load((B / rel).read_text(encoding="utf-8"))
        for reg, _anc in E._descender(doc, list(camino)):
            txt = (reg.get("desc") or reg.get("descripcion") or "").lower()
            for objetivo, frases in promesas:
                if not any(f.search(txt) for f in frases):
                    continue
                if (rel, reg.get("nombre"), objetivo) not in con_efecto:
                    err.append(
                        f"«{reg.get('nombre')}» ({rel}) dice en su texto que "
                        f"fija «{objetivo}» y no declara ningún efecto que lo "
                        f"haga: la regla existe pero nadie la puede calcular")

    # ── (b bis) LA PUERTA CERRADA · bloque D (2026-09-02) ────────────────
    # Todo rasgo tiene que decir si toca alguna variable calculable: o trae
    # `efectos:`, o trae `no_automatizado:` con su motivo. Los 496 que hoy no
    # dicen ni una cosa ni la otra están ENUMERADOS en
    # `_verificacion/rasgos_sin_declarar.json`, y esa lista solo puede bajar.
    #
    # Enumerarlos —y no taparlos con un comodín, que es lo que hacía el censo
    # hasta hoy— es la diferencia entre «se ve crecer» y «no puede crecer»: un
    # rasgo que se añada mañana sin declarar nada hace fallar esto.
    import json as _json
    base_f = B / "_verificacion" / "rasgos_sin_declarar.json"
    if not base_f.exists():
        err.append("falta _verificacion/rasgos_sin_declarar.json: sin él no se "
                   "puede distinguir un rasgo nuevo sin declarar de la deuda "
                   "conocida")
    else:
        conocidos = set(_json.loads(base_f.read_text(encoding="utf-8"))["rasgos"])
        vistos, nuevos, resueltos_hoy = set(), [], []
        for rel, camino in E.origenes():
            doc = yaml.safe_load((B / rel).read_text(encoding="utf-8"))
            for reg, _anc in E._descender(doc, list(camino)):
                if not isinstance(reg, dict) or not reg.get("nombre"):
                    continue
                uid = f"{rel}#{reg['nombre']}"
                declara = reg.get("efectos") or reg.get("no_automatizado")
                # `no_automatizado` tiene que traer MOTIVO. Un `true` pelado
                # sería una firma en blanco: dice «lo miramos» sin decir qué
                # se miró, y es indistinguible de callarse.
                na = reg.get("no_automatizado")
                if na is not None and not (isinstance(na, str) and na.strip()):
                    err.append(f"«{reg['nombre']}» ({rel}): `no_automatizado` "
                               f"tiene que traer el motivo, no {na!r}. Decir "
                               f"«lo miramos y no toca» sin decir qué se miró "
                               f"es no decir nada")
                if declara:
                    if uid in conocidos:
                        resueltos_hoy.append(uid)
                    continue
                vistos.add(uid)
                if uid not in conocidos:
                    nuevos.append(uid)
        for uid in nuevos[:20]:
            err.append(f"«{uid.split('#')[-1]}» ({uid.split('#')[0]}) no dice "
                       f"si toca alguna variable calculable: o declara "
                       f"`efectos:`, o `no_automatizado:` con su motivo")
        if len(nuevos) > 20:
            err.append(f"… y {len(nuevos) - 20} rasgos más sin declarar")
        if resueltos_hoy:
            warn.append(f"{len(resueltos_hoy)} rasgos de "
                        f"`rasgos_sin_declarar.json` ya declaran algo: "
                        f"bórralos de la lista, que solo puede bajar")

    # (b2) ningún `efectos:` fuera de los ficheros que el motor recorre.
    # Antes de C1 (Plan 17) esto era el parche al síntoma: `efectos._ORIGENES`
    # era una lista escrita a mano —lo que dejó fuera a las dos fórmulas de CA
    # de subclase— y este chequeo solo avisaba de las consecuencias. Hoy la
    # cobertura la calcula `E.origenes()` contra el manifiesto, así que los
    # ficheros de REGLA ya no pueden quedarse fuera en silencio.
    # Esto sigue haciendo falta para los demás directorios (`equipo/`,
    # `reglas/`…), donde un `efectos:` suelto seguiría sin tener quien lo lea.
    conocidos = {rel for rel, _ in E.origenes()}
    for f in sorted(B.glob("**/*.yaml")):
        rel = f.relative_to(B).as_posix()
        if rel in conocidos or rel.startswith(("_verificacion/", "personajes/")):
            continue
        if re.search(r"^\s*efectos:", f.read_text(encoding="utf-8"), re.M):
            err.append(
                f"{rel} declara `efectos:` y el motor no lo recorre: añádelo a "
                f"`reglas/fuentes_de_efectos.yaml` o el efecto no existe para nadie")

    # (b3) un efecto con `columna` tiene que resolverse en TODOS los niveles de
    # su clase, no en uno.
    #
    # Nace de un fallo real: «Movimiento sin armadura» del Monje se probaba con
    # una única ficha de nivel 2, donde la columna vale 3. En el nivel 6 vale
    # **4,5**, y el motor reventaba porque la ruta de `columna` pasaba el valor
    # por el evaluador de fórmulas, que rechaza decimales a propósito. Ningún
    # chequeo ni ninguna mutación lo vio: lo destapó generar fichas de todos los
    # niveles. Una escala probada en un solo punto no está probada.
    for ef in declarados:
        if not ef.get("columna"):
            continue
        stem = pathlib.Path(ef["_archivo"]).stem
        dc = yaml.safe_load((B / f"clases/{stem}.yaml").read_text(encoding="utf-8"))
        for fila in dc.get("progresion", []):
            try:
                v = E.valor_de_columna(stem, ef["columna"], fila["n"])
            except E.ErrorDeEfectos as e:
                err.append(f"«{ef['_rasgo']}»: {e}")
                continue
            if not isinstance(v, (int, float)):
                err.append(f"«{ef['_rasgo']}»: la columna {ef['columna']!r} vale "
                           f"{v!r} en el nivel {fila['n']}, que no es un número")

    # (c) ciclos, sobre TODO lo declarado a la vez (el peor caso posible)
    por_var = {}
    for ef in declarados:
        por_var.setdefault(ef["objetivo"], []).append(ef)
    try:
        E.orden_de_calculo(sorted(por_var), por_var, {}, vocab)
    except E.ErrorDeEfectos as e:
        err.append(str(e))

    # (d) todo valor base por defecto tiene que estar citado.
    # Nació como aviso (`_falta_cita`) porque la CA base venía sin página desde
    # `calculo.py`. Cerrada esa deuda el 2026-08-30, el aviso pasa a ERROR: si
    # alguien añade una variable con base y sin cita, es la regla 2 del proyecto
    # rota, no un pendiente.
    for nombre, v in vocab["variables"].items():
        if v.get("_falta_cita"):
            warn.append(f"«{nombre}» usa un valor base sin página citada "
                        f"({v.get('base_por_defecto')}) — declarado, no inventado")
            continue
        if v.get("base_por_defecto"):
            pag = v.get("pagina") or {}
            if not isinstance(pag.get("pdf"), int) or not isinstance(pag.get("libro"), int):
                err.append(f"«{nombre}» tiene `base_por_defecto` "
                           f"({v['base_por_defecto']}) sin cita de página")
    return f"efectos ({len(declarados)})", err, warn


# ── Chequeo: la tabla de PG establecidos por clase (2026-08-30) ───────────
# La tabla "Puntos de golpe establecidos por clase" (pdf 44 = libro 42) y los
# `dado_golpe` de las 12 clases se transcribieron por separado, de páginas
# distintas y en sesiones distintas. Eso las hace contrastables **sin abrir el
# manual**: el valor fijo de una clase es siempre (caras / 2) + 1 — d12→7,
# d10→6, d8→5, d6→4 — que es el promedio del dado redondeado hacia arriba.
#
# Es la capa 3 del método (invariantes deducibles). No demuestra que la tabla
# esté bien copiada: demuestra que las dos transcripciones **cuentan la misma
# historia**, y si una se rompe, deja de cuadrar.
def validar_puntos_golpe():
    err, warn = [], []
    g = yaml.safe_load((B / "reglas/generacion_personaje.yaml").read_text(encoding="utf-8"))
    pg = g.get("puntos_golpe")
    if not pg:
        return "puntos de golpe", ["reglas/generacion_personaje.yaml no declara `puntos_golpe`"], []

    sig = pg.get("niveles_siguientes_al_1", {})
    tabla = sig.get("tabla_valores_establecidos", {})
    filas = tabla.get("filas") or []
    if not filas:
        return "puntos de golpe", ["la tabla de PG establecidos por clase está vacía"], []

    for clave, d in (("niveles_siguientes_al_1", sig),
                     ("aumento_de_constitucion", pg.get("aumento_de_constitucion", {}))):
        pag = d.get("pagina") or {}
        if not isinstance(pag.get("pdf"), int) or not isinstance(pag.get("libro"), int):
            err.append(f"`{clave}` sin cita de página numérica")

    dados = {}
    for f in sorted((B / "clases").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        dados[d["clase"]] = d["atributos_basicos"]["dado_golpe"]

    vistas = []
    for fila in filas:
        for c in fila["clases"]:
            vistas.append(c)
            if c not in dados:
                err.append(f"la tabla de PG cita una clase que no existe: {c!r}")
                continue
            caras = int(str(dados[c]).lstrip("d"))
            esperado = caras // 2 + 1
            if fila["valor"] != esperado:
                err.append(
                    f"{c}: la tabla da {fila['valor']} PG por nivel, pero su "
                    f"dado es {dados[c]} y (caras/2)+1 = {esperado}. Una de las "
                    f"dos transcripciones está mal")

    repes = {c for c in vistas if vistas.count(c) > 1}
    if repes:
        err.append(f"clases repetidas en la tabla de PG: {sorted(repes)}")
    faltan = sorted(set(dados) - set(vistas))
    if faltan and tabla.get("_todas_las_clases"):
        err.append(f"la tabla de PG dice cubrir las 12 clases y no cita: {faltan}")

    if not pg.get("aumento_de_constitucion", {}).get("_es_retroactivo"):
        warn.append("el aumento de Constitución ya no está marcado como retroactivo "
                    "— es lo que impide que los PG sean una suma acumulada")
    return f"puntos de golpe ({len(vistas)} clases)", err, warn


# ── Chequeo: el componente material descompuesto (Fase 14b-2) ─────────────
# `componentes.coste` era un solo string, y por eso la base guardó CUATRO sumas
# que ninguna página imprime: *Vínculo protector* «100 po» (par de anillos de 50
# «cada uno»), *Cofre oculto de Leomund* «5050 po», *Proyección astral* «1100
# po» (1000+100) y *Conocer las leyendas* «200 po» (4×50). Modo de fallo nº 10,
# «dato agregado»: alguien hizo una operación y guardó el resultado.
#
# El chequeo fuerte es de **ida y vuelta**: `coste` debe ser IDÉNTICO a lo que
# `materiales.render_coste()` produce desde la lista. Si alguien vuelve a
# escribir el total a mano, deja de cuadrar. Es la misma idea que hace falta
# para los prerrequisitos de la Fase 15.
# El asterisco final es la convención de la base para «se consume» (viene del
# CSV de origen; ver FUENTES.md, la corrección de los 41 `consume_material`).
# La primera versión de este chequeo no lo contemplaba y marcó 26 conjuros
# perfectamente sanos: el chequeo estaba mal, no el dato.
_RE_COSTE_SIMPLE = re.compile(r"^\d+(?:[.,]\d+)?\s*(po|pp|pc)\*?$")


def validar_materiales():
    err, warn = [], []
    import materiales as M
    H = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
    con_lista = 0
    for h in H:
        c = h.get("componentes") or {}
        mats = c.get("materiales")
        coste = c.get("coste")

        if not mats:
            # AUSENCIA: un coste que no es «N po» y no está descompuesto es una
            # cifra que nadie puede volver a comprobar. Antes vivía como
            # excepción declarada en COSTE_COMPUESTO; ahora es un error.
            if coste and not _RE_COSTE_SIMPLE.match(str(coste).strip()):
                err.append(f"«{h['nombre']}»: coste {coste!r} no es «N po|pp|pc» "
                           f"y no declara `materiales` que lo expliquen")
            continue

        con_lista += 1
        d = f"«{h['nombre']}»"
        for m in mats:
            if not m.get("nombre"):
                err.append(f"{d}: un material sin `nombre`")
            if not isinstance(m.get("coste"), int) or m["coste"] <= 0:
                err.append(f"{d}: material {m.get('nombre')!r} con coste "
                           f"{m.get('coste')!r}, que no es un entero positivo")
            if m.get("unidad") not in M.UNIDADES:
                err.append(f"{d}: unidad {m.get('unidad')!r} fuera de "
                           f"{M.UNIDADES}")
            if "consume" not in m:
                err.append(f"{d}: material {m.get('nombre')!r} sin `consume` — "
                           f"en *Clon* se consume uno de los dos y no el otro")

        esperado = M.render_coste(mats)
        if coste != esperado:
            err.append(f"{d}: `coste` guardado {coste!r} ≠ el que produce la "
                       f"descomposición {esperado!r}. `coste` se DERIVA de "
                       f"`materiales`, nunca se escribe a mano")
        esp_cons = M.consume_material(mats)
        if c.get("consume_material") != esp_cons:
            err.append(f"{d}: `consume_material` {c.get('consume_material')!r} "
                       f"≠ el derivado {esp_cons!r}")

        # Y la trampa concreta: que el coste no vuelva a ser una suma.
        suma = sum(m["coste"] * (m.get("cantidad") or 1) for m in mats
                   if isinstance(m.get("coste"), int))
        if len(mats) > 1 and re.search(rf"\b{suma}\b", str(coste)):
            err.append(f"{d}: `coste` contiene {suma}, que es la SUMA de sus "
                       f"materiales. Ninguna página imprime esa suma")
    return f"materiales ({con_lista} descompuestos)", err, warn


# ── Chequeo: la LISTA de tiradas por efecto (Fase 14b-3) ──────────────────
# `tirada` es un solo campo y responde a una sola pregunta: **¿el conjuro exige
# una tirada para manifestarse?** (`Directo` = se manifiesta igual y la
# salvación modula; decidido y verificado el 2026-08-29). Esa pregunta sigue
# siendo válida y `validar_tirada()` la sigue vigilando sin cambios.
#
# Lo que el campo único NO puede decir es **cuántas tiradas pide el conjuro y de
# qué tipo cada una**: *Símbolo* tiene 6 modos con salvaciones distintas,
# *Muro prismático* pide la de Destreza UNA VEZ POR CAPA (siete) y añade dos
# propias en las capas 6 y 7, y *Mano de Bigby* tiene un modo que no es
# salvación sino **tirada de ataque**. Eso vive ahora en `tiradas`, una lista.
#
# El chequeo que importa es el de AUSENCIA: si la descripción exige salvaciones
# de más de una característica y no hay lista, la información está perdida y
# nadie lo notaría.
_TIPOS_TIRADA_EFECTO = _TIRADAS_VALIDAS | {
    "Prueba",    # una prueba de característica: *Símbolo* pide Sab (Percepción)
                 # para detectar el glifo. No es salvación ni ataque.
    "Ninguna",   # el modo existe y no pide tirada: «Mano interpuesta»
}
# La mención «tirada de salvación de Constitución para mantener la
# concentración» NO es una salvación que el conjuro exija: es la regla de
# concentración citada de pasada. Fue el falso positivo que sacó a *Estática
# sináptica* de la lista de conjuros con varias salvaciones — la heurística
# contaba 5 y la lectura de la página dijo 4.
_RE_CONCENTRACION = re.compile(
    r"salvaci[oó]n de (?:Fuerza|Destreza|Constituci[oó]n|Inteligencia|"
    r"Sabidur[ií]a|Carisma)\s+para mantener la concentraci[oó]n", re.I)
_ABREV_DE_CARACT = {
    "fuerza": "Fue.", "destreza": "Des.", "constitucion": "Con.",
    "inteligencia": "Int.", "sabiduria": "Sab.", "carisma": "Car.",
}


# OJO: aquí NO sirve `_RE_SALVACION`, que exige el «tirada de salvación de X»
# completo. `hechizos.json` se declara `fidelidad: mixto` en `_meta` justamente
# porque una parte del texto quedó condensada en la conversión del CSV y **elide
# «tirada de»**: *Muro de hielo* dice «hace salvación de Destreza» donde la
# página dice «hace una tirada de salvación de Destreza». Con la regex estricta,
# este conjuro no tenía NINGUNA salvación detectable — y de paso queda dicho que
# `validar_tirada()` se queda ciego en los registros condensados.
_RE_SALV_LAXA_CAR = re.compile(
    r"salvaci[oó]n\s+de\s+(Fuerza|Destreza|Constituci[oó]n|Inteligencia|"
    r"Sabidur[ií]a|Carisma)", re.I)


def _caracts_de_salvacion(desc):
    """Las características de salvación que el conjuro EXIGE, sin el ruido de
    la regla de concentración."""
    limpio = _RE_CONCENTRACION.sub(" ", desc or "")
    return {_sinac(m.group(1).lower()) for m in _RE_SALV_LAXA_CAR.finditer(limpio)}


# El manual distingue dos redacciones, y la distinción es semántica, no de
# estilo (deuda D2, cerrada el 2026-08-30 con doble lectura de *Arma espiritual*
# y *Enredadera*, que coincidieron palabra por palabra):
#
#   «**Haz** un ataque de conjuro…»        → el conjuro ES el ataque
#   «**puedes hacer** un ataque de conjuro…» → se manifiesta igual, y el ataque
#                                              viene después
#
# Antes de fijarlo, los 11 conjuros con «cuerpo a cuerpo» llevaban TRES
# etiquetas distintas (4 `D20+ata.conj.`, 3 `D20+ata.CaC`, 4 `Directo`) y ningún
# chequeo lo veía, porque las tres estaban en el vocabulario: «un campo con la
# forma correcta puede ser basura», amenaza nº 3 del FODA.
_RE_ATAQUE_CONJURO = re.compile(
    r"(.{0,70}?)ataque de conjuro (cuerpo a cuerpo|a distancia)", re.I)
_RE_OPCIONAL = re.compile(r"puedes\s+(?:hacer|realizar)\b[^.]{0,40}$", re.I)


def _clasifica_ataque(desc):
    """(alcance, opcional) del primer ataque de conjuro del texto, o None."""
    m = _RE_ATAQUE_CONJURO.search(desc or "")
    if not m:
        return None
    return m.group(2).lower(), bool(_RE_OPCIONAL.search(m.group(1)))


def validar_ataques():
    """La etiqueta de ataque tiene que decir lo que dice el texto."""
    err, warn = [], []
    H = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
    vistos = 0
    for h in H:
        clase = _clasifica_ataque(h.get("descripcion", ""))
        if not clase:
            continue
        vistos += 1
        alcance, opcional = clase
        t_actual = h.get("tirada")
        d = f"«{h['nombre']}»"
        # Si el ataque está declarado en `tiradas`, pertenece a un EFECTO del
        # conjuro y no a su lanzamiento — el caso de *Mano de Bigby*, cuyo «Haz
        # un ataque» está dentro del modo «Puño cerrado» mientras la mano se
        # crea sin tirada ninguna. La estructura manda sobre el verbo, porque
        # cada entrada de `tiradas` lleva su propia página y su doble lectura.
        declarado = any(str(x.get("tipo", "")).startswith("D20+")
                        for x in (h.get("tiradas") or []))
        if declarado:
            if t_actual != "Directo":
                err.append(f"{d}: declara su ataque en `tiradas` (luego el "
                           f"conjuro se manifiesta sin él) y su `tirada` dice "
                           f"{t_actual!r} en vez de 'Directo'")
            continue
        esperada = ("Directo" if opcional
                    else "D20+ata.CaC" if alcance == "cuerpo a cuerpo"
                    else "D20+ata.conj.")
        if t_actual != esperada:
            err.append(
                f"{d}: su texto dice «{'puedes hacer' if opcional else 'haz'}» "
                f"un ataque de conjuro {alcance}, así que `tirada` debería ser "
                f"{esperada!r} y dice {t_actual!r}")
        if opcional:
            # Si el conjuro se manifiesta primero, el ataque NO puede quedarse
            # sin declarar: viviría solo en la prosa y nadie podría calcularlo.
            err.append(
                f"{d}: se manifiesta sin tirada («puedes hacer»), así que su "
                f"ataque tiene que estar declarado en `tiradas` y no lo está")
    return f"ataques de conjuro ({vistos})", err, warn


def validar_tiradas():
    err, warn = [], []
    H = json.loads((B / "hechizos.json").read_text(encoding="utf-8"))["hechizos"]
    con_lista = 0
    for h in H:
        lista = h.get("tiradas")
        caracts = _caracts_de_salvacion(h.get("descripcion", ""))

        if not lista:
            # AUSENCIA: varias salvaciones distintas y un solo campo para
            # decirlo. Es el defecto que la Fase 14b-3 viene a cerrar.
            if len(caracts) > 1:
                err.append(
                    f"«{h['nombre']}»: su descripción exige salvaciones de "
                    f"{sorted(caracts)} y no declara `tiradas`: un campo único "
                    f"no puede representarlas y la información se pierde")
            continue

        con_lista += 1
        d = f"«{h['nombre']}»"
        declaradas = set()
        for e in lista:
            if e.get("tipo") not in _TIPOS_TIRADA_EFECTO:
                err.append(f"{d}: tipo de tirada {e.get('tipo')!r} fuera del "
                           f"vocabulario {sorted(_TIPOS_TIRADA_EFECTO)}")
                continue
            if not e.get("cuando"):
                err.append(f"{d}: una tirada sin `cuando` — sin decir en qué "
                           f"modo o momento se hace, la lista no sirve")
            pag = e.get("pagina") or {}
            if not isinstance(pag.get("pdf"), int) or not isinstance(pag.get("libro"), int):
                err.append(f"{d}: la tirada «{e.get('cuando')}» no cita página "
                           f"numérica (regla 2: sin página, un dato no entra)")
            if str(e["tipo"]).startswith("TdS "):
                declaradas.add(_sinac(_CARACT_DE_ABREV.get(e["tipo"][4:], "").lower()))

        # Ida y vuelta: lo declarado tiene que ser exactamente lo que pide el
        # texto. Ni una salvación de más (inventada) ni una de menos (perdida).
        declaradas.discard("")
        if declaradas != caracts:
            faltan = sorted(caracts - declaradas)
            sobran = sorted(declaradas - caracts)
            err.append(
                f"{d}: `tiradas` declara salvaciones de {sorted(declaradas)} y "
                f"su descripción pide {sorted(caracts)}"
                + (f" · faltan {faltan}" if faltan else "")
                + (f" · sobran {sobran}" if sobran else ""))
    return f"tiradas por efecto ({con_lista} conjuros)", err, warn


# ── Chequeo: los prerrequisitos de dote (Fase 15) ─────────────────────────
# El prerrequisito de una dote era prosa: «nivel 4 o más, Fuerza o Destreza 13 o
# más». Un LLM que la lee acierta casi siempre, y «casi siempre» es la amenaza
# nº 5 del FODA: un acierto por el método equivocado es indistinguible de
# acertar por casualidad.
#
# El chequeo fuerte es de **IDA Y VUELTA**: se parsea la prosa a estructura, se
# reconstruye la prosa desde la estructura, y tiene que salir **idéntica**. Eso
# demuestra lo único que importa — que no se perdió ni se inventó nada. Un
# parser que ignore un término en silencio hace lo mismo que hizo el CSV de
# origen: devolver algo plausible y equivocado.
#
# Y un segundo chequeo, del que ya hay precedente: cada rasgo y cada categoría
# de entrenamiento citados tienen que **resolver a un registro real**. Citar un
# rasgo que no existe es el bug `Clerigo` otra vez.
# ── C3 del Plan 17: la mejora de característica que concede una DOTE ──────
# El defecto que cierra esto, medido el 2026-08-31: `Actor` concede «Carisma
# +1» y ese +1 vivía SOLO dentro de la cadena `descripcion`. El esquema exigía
# `final == base + ajuste_trasfondo + mejoras`, y una dote no tenía dónde
# entrar. Resultado invertido: la ficha CORRECTA (Car 18) se rechazaba por
# «puntuación sin justificar», y la ficha ROTA (Car 17, el +1 perdido)
# verificaba en verde con la CD, el ataque y la CA un punto por debajo.
#
# Método: el mismo de la Fase 15 con los prerrequisitos — no se transcribe
# nada nuevo, se ESTRUCTURA la prosa ya citada, y se exige IDA Y VUELTA. Si
# la estructura no reproduce el fragmento del manual palabra por palabra, la
# estructura está mal. 54/54 exactas al escribirse.
#
# Detalle que la ida y vuelta salvó: los 12 dones épicos dicen «máx. 30», no
# «máx. 20». Haber supuesto 20 habría inventado una regla para 12 dotes.
_MEJORA_FRAG = re.compile(
    r'^\s*Mejora de característica:\s*'
    r'(.+?\(máx\.\s*\d+\)(?: a una característica [^.]+)?)\.')
_CARACTS = ("Fuerza", "Destreza", "Constitución", "Inteligencia",
            "Sabiduría", "Carisma")


def _mejora_a_prosa(m):
    """estructura -> fragmento del manual. Es la mitad de vuelta."""
    cant, mx = m.get("cantidad"), m.get("maximo")
    if m.get("restriccion"):
        return f"+{cant} (máx. {mx}) a una característica {m['restriccion']}"
    e = m.get("entre")
    if e == "cualquiera":
        return f"una a elección +{cant} (máx. {mx})"
    if not isinstance(e, list) or not e:
        return None
    if len(e) == 1:
        cuerpo = e[0]
    elif len(e) == 2:
        cuerpo = f"{e[0]} o {e[1]}"
    else:
        cuerpo = ", ".join(e[:-1]) + f" o {e[-1]}"
    return f"{cuerpo} +{cant} (máx. {mx})"


def validar_mejoras_de_dote():
    err, warn = [], []
    n_ok = 0
    for f in sorted((B / "dotes").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        rel = f.relative_to(B).as_posix()
        for x in d.get("dotes", []) or []:
            nom = x.get("nombre")
            desc = str(x.get("descripcion", ""))
            m = _MEJORA_FRAG.match(desc)
            est = x.get("mejora_caracteristica")

            # (a) la prosa promete un +1 y no hay estructura -> el caso Actor
            if m and not est:
                err.append(f"«{nom}» ({rel}) concede una mejora de "
                           f"característica en su texto y no la declara en "
                           f"`mejora_caracteristica`: el +1 no lo aplicaría "
                           f"nadie y la ficha correcta sería la rechazada")
                continue
            # (b) estructura sin prosa que la respalde -> dato inventado
            if est and not m:
                err.append(f"«{nom}» ({rel}) declara `mejora_caracteristica` "
                           f"y su `descripcion` no dice que conceda ninguna: "
                           f"una mejora sin texto que la cite es inventada")
                continue
            if not est:
                # TOLERADO: lo cubren (a) y (b) de arriba. Una dote sin
                # `mejora_caracteristica` cuyo texto tampoco promete ninguna
                # no tiene nada que comprobar; los dos casos en que la
                # ausencia SÍ es un defecto ya han saltado antes de llegar
                # aquí (prosa sin estructura, estructura sin prosa).
                continue

            # (c) ida y vuelta exacta
            generado = _mejora_a_prosa(est)
            if generado != m.group(1):
                err.append(f"«{nom}» ({rel}): `mejora_caracteristica` no "
                           f"reproduce su propio texto.\n"
                           f"        manual:    «{m.group(1)}»\n"
                           f"        estructura: «{generado}»")
                continue

            # (d) el vocabulario de características es cerrado
            e = est.get("entre")
            if isinstance(e, list):
                for c in e:
                    if c not in _CARACTS:
                        err.append(f"«{nom}» ({rel}): {c!r} no es una "
                                   f"característica")
            elif e != "cualquiera":
                err.append(f"«{nom}» ({rel}): `entre` debe ser una lista de "
                           f"características o «cualquiera», y es {e!r}")
            n_ok += 1

    return f"mejoras de dote ({n_ok})", err, warn


def validar_prerrequisitos():
    err, warn = [], []
    import prerrequisitos as P

    voc = P.vocabulario()
    caracts = {_sinac(c.lower()) for c in voc["caracteristicas"]}

    rasgos_reales = set()
    for f in sorted((B / "clases/rasgos").glob("*.yaml")):
        for r in (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("rasgos", []):
            rasgos_reales.add(_sinac(r["nombre"].lower()))
    for f in sorted((B / "clases/subclases").glob("*.yaml")):
        for s in (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("subclases", []):
            for r in (s.get("rasgos") or []):
                rasgos_reales.add(_sinac(r["nombre"].lower()))

    entrenamientos_reales = set()
    for f in sorted((B / "clases").glob("*.yaml")):
        ab = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("atributos_basicos") or {}
        v = ab.get("armaduras")
        for x in (v if isinstance(v, list) else [v] if v else []):
            entrenamientos_reales.add(_sinac(str(x).lower()))

    con_prerr = 0
    for f in sorted((B / "dotes").glob("*.yaml")):
        for d in (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("dotes", []):
            lit = d.get("prerrequisito")
            if not lit:
                continue
            con_prerr += 1
            ctx = f"«{d['nombre']}» ({f.name})"
            try:
                est = P.analizar(lit)
            except P.ErrorDePrerrequisito as e:
                err.append(f"{ctx}: {e}")
                continue

            vuelta = P.renderizar(est)
            if vuelta != lit:
                err.append(f"{ctx}: el ida y vuelta no reproduce el original\n"
                           f"        original: {lit!r}\n"
                           f"        vuelta:   {vuelta!r}")

            for term in est["todos"]:
                if term["tipo"] == "caracteristica":
                    for c in term["cualquiera_de"]:
                        if _sinac(c.lower()) not in caracts:
                            err.append(f"{ctx}: {c!r} no es una de las seis "
                                       f"características")
                elif term["tipo"] == "rasgo":
                    for r in term["cualquiera_de"]:
                        if _sinac(r.lower()) not in rasgos_reales:
                            err.append(f"{ctx}: cita el rasgo {r!r}, que no "
                                       f"existe en clases/rasgos ni en "
                                       f"clases/subclases")
                elif term["tipo"] == "entrenamiento":
                    cat = term["categoria"]
                    if _sinac(cat.lower()) not in entrenamientos_reales:
                        err.append(f"{ctx}: cita entrenamiento con {cat!r}, que "
                                   f"ninguna clase concede en "
                                   f"`atributos_basicos.armaduras`")
                    if cat not in voc["categorias_entrenamiento"]:
                        err.append(f"{ctx}: categoría {cat!r} fuera del "
                                   f"vocabulario declarado")
    return f"prerrequisitos ({con_prerr} dotes)", err, warn


# ── Chequeo: los saltos de nivel (Fase 16) ────────────────────────────────
# `subir_nivel.py` deriva de la tabla de cada clase qué pasa al alcanzar un
# nivel. Este chequeo lo ejecuta para **las 12 clases, los niveles 2-20 y todas
# sus subclases** — 12 × 19 saltos, y los de subclase una vez por subclase — y
# exige que ninguno se caiga.
#
# Por qué merece la pena: `subir_nivel.py` falla ruidosamente ante un rasgo sin
# texto, una subclase sin rasgo del nivel que la tabla promete, o un nivel en el
# que «no pasa nada». Correrlo entero convierte esos `sys.exit` en un chequeo de
# cobertura real, en vez de en una sorpresa el día que alguien suba a un pícaro
# al nivel 10.
def validar_subida():
    err, warn = [], []
    import io, contextlib
    import subir_nivel as SN

    saltos = 0
    for f in sorted((B / "clases").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if "progresion" not in d:
            continue
        clase = d["clase"]
        stem = f.stem
        subs = [s["nombre"] for s in
                ((yaml.safe_load((B / f"clases/subclases/{stem}.yaml")
                                 .read_text(encoding="utf-8")) or {})
                 .get("subclases", []))] or [None]
        for fila in d["progresion"]:
            n = fila["n"]
            if n < 2:
                continue
            # Solo hace falta recorrer todas las subclases en los niveles que
            # conceden un rasgo de subclase; en los demás el resultado no
            # depende de cuál sea.
            necesita_sub = SN.MARCADOR_RASGO_SUB in (fila.get("rasgos") or [])
            for sub in (subs if necesita_sub else [subs[0]]):
                saltos += 1
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        SN.que_pasa(clase, n, sub)
                except SystemExit as e:
                    err.append(f"{clase} N{n}"
                               + (f" / {sub}" if necesita_sub else "")
                               + f": {e}")
                except Exception as e:  # noqa: BLE001
                    err.append(f"{clase} N{n}: excepción inesperada: {e!r}")
    return f"saltos de nivel ({saltos})", err, warn


def main():
    total_err = 0
    print("── CLASES " + "─"*52)
    for p in sorted((B/"clases").glob("*.yaml")):
        nom, err, warn = validar_clase(p)
        total_err += len(err)
        estado = "✅" if not err else "❌"
        print(f" {estado} {nom:<12} {'0 errores' if not err else str(len(err))+' ERRORES'}")
        for e in err:  print(f"      ✗ {e}")
        for w in warn: print(f"      ⚠ {w}")

    print("── ORÍGENES " + "─"*50)
    for fn in (validar_trasfondos, validar_especies):
        nom, err, warn = fn()
        total_err += len(err)
        print(f" {'✅' if not err else '❌'} {nom:<18} {'0 errores' if not err else str(len(err))+' ERRORES'}")
        for e in err[:12]: print(f"      ✗ {e}")

    nom, err, warn = validar_subclases()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<18} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:12]:  print(f"      ✗ {e}")
    for w in warn[:4]:  print(f"      ⚠ {w}")

    nom, err, warn = validar_dotes()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<18} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:20]: print(f"      ✗ {e}")

    nom, err, warn = validar_equipo()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<18} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:20]: print(f"      ✗ {e}")
    for w in warn[:5]: print(f"      ⚠ {w}")

    print("── CREACIÓN DE PERSONAJE " + "─"*37)
    for fn in (validar_atributos_basicos, validar_generacion, validar_puntos_golpe,
               validar_rasgos_clase,
               validar_competencias_clase, validar_habilidades, validar_idiomas):
        nom, err, warn = fn()
        total_err += len(err)
        print(f" {'✅' if not err else '❌'} {nom:<24} {'0 errores' if not err else str(len(err))+' ERRORES'}")
        for e in err[:20]: print(f"      ✗ {e}")
        for w in warn[:5]: print(f"      ⚠ {w}")

    print("── HECHIZOS " + "─"*50)
    nom, err, warn = validar_hechizos()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<12} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:10]: print(f"      ✗ {e}")
    for w in warn[:5]: print(f"      ⚠ {w}")

    nom, err, warn = validar_hechizos_clases()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<12} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:12]: print(f"      ✗ {e}")
    for w in warn[:8]: print(f"      ⚠ {w}")

    print("── INTEGRIDAD " + "─"*48)
    nom, err, warn = validar_dados()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<24} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:20]: print(f"      ✗ {e}")

    nom, err, warn = validar_conversiones()
    total_err += len(err)
    print(f" {'✅' if not err else '❌'} {nom:<24} {'0 errores' if not err else str(len(err))+' ERRORES'}")
    for e in err[:20]: print(f"      ✗ {e}")

    for fn in (validar_tirada, validar_vecindad, validar_ortografia,
               validar_citas_conjuro, validar_costes_sin_fuente, validar_efectos,
               validar_materiales, validar_tiradas, validar_ataques,
               validar_prerrequisitos, validar_subida,
               validar_mejoras_de_dote):
        nom, err, warn = fn()
        total_err += len(err)
        print(f" {'✅' if not err else '❌'} {nom:<24} {'0 errores' if not err else str(len(err))+' ERRORES'}")
        for e in err[:20]: print(f"      ✗ {e}")
        for w in warn[:6]: print(f"      ⚠ {w}")

    nom, err, warn = validar_referencias()
    total_err += len(err)
    # El marcador tiene que decir la verdad: ❌ si hay errores, ⚠ si solo hay
    # avisos, ✅ si no hay nada. Hasta el 2026-09-02 esta línea imprimía ⚠
    # aunque hubiera errores —daba igual, porque este chequeo no podía tener
    # ninguno— y al promoverlo a error (fase 1 del PLAN_19) la línea seguía
    # diciendo «aviso» de un fallo real: su prueba por mutación daba «no
    # detectada» cuando lo que fallaba era el rótulo.
    print(f" {'❌' if err else '⚠' if warn else '✅'} {nom}")
    for e in err:      print(f"      ✗ {e}")
    for w in warn[:12]: print(f"      ⚠ {w}")

    print("─"*62)
    print(f"{'✅ BASE VALIDADA — 0 errores' if not total_err else f'❌ {total_err} errores'}")
    return 1 if total_err else 0

if __name__ == "__main__":
    sys.exit(main())
