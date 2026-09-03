#!/usr/bin/env python3
"""Chequeo de COBERTURA de la base canónica D&D 2024 (5.5e).

`validar.py` responde «¿es coherente la base consigo misma?».
Esto responde otra pregunta: **¿puede la base contestar todo lo que una skill
de creación y subida de nivel va a preguntarle?**

Un dato puede ser perfectamente coherente y aun así no estar. Ese es el fallo
que importa cuando la autoridad se delega a la base: si falta, el LLM lo
rellena con lo que «sabe» — es decir, con la edición 2014, que está vetada.

Cada comprobación simula una pregunta concreta de la ficha. No inventa
respuestas: solo dice si la base tiene con qué responder.

Uso: python3 cobertura.py [-v]
"""
import json, sys, re, pathlib
import yaml

# Los marcadores de la tabla se preguntan a `calculo`, que los lee de
# `reglas/subida_de_nivel.yaml`. Aquí estaban las tres cadenas escritas a mano
# (auditoría del 2026-09-03). `calculo` no importa nada del proyecto, así que
# no hay ciclo.
from calculo import es_marcador_de

B = pathlib.Path(__file__).parent
VERBOSE = "-v" in sys.argv

# Las 18 habilidades del juego. Es la única lista que este script da por
# sabida, y solo para comprobar que lo que la base cita son habilidades
# reales: no se usa para rellenar ningún dato de la ficha.
HABILIDADES = {
    "Acrobacias", "Atletismo", "Conocimiento arcano", "Engaño", "Historia",
    "Interpretación", "Intimidación", "Investigación", "Juego de manos",
    "Medicina", "Naturaleza", "Percepción", "Perspicacia", "Persuasión",
    "Religión", "Sigilo", "Supervivencia", "Trato con animales",
}


class Informe:
    def __init__(self):
        self.bloques = []

    def bloque(self, titulo):
        b = {"titulo": titulo, "ok": [], "huecos": []}
        self.bloques.append(b)
        return b

    @staticmethod
    def ok(b, msg):
        b["ok"].append(msg)

    @staticmethod
    def hueco(b, quien, pregunta, detalle=""):
        b["huecos"].append((quien, pregunta, detalle))

    def imprimir(self):
        total = 0
        for b in self.bloques:
            n = len(b["huecos"])
            total += n
            estado = "✅" if not n else "❌"
            print(f"\n{estado} {b['titulo']} — {len(b['ok'])} preguntas cubiertas, "
                  f"{n} sin respuesta")
            agrupado = {}
            for quien, preg, det in b["huecos"]:
                agrupado.setdefault(preg, []).append((quien, det))
            for preg, casos in sorted(agrupado.items()):
                quienes = ", ".join(sorted({q for q, _ in casos}))
                print(f"   ✗ {preg}")
                print(f"     afecta a: {quienes}")
                dets = {d for _, d in casos if d}
                for d in sorted(dets)[:4]:
                    print(f"       · {d}")
            if VERBOSE:
                for m in b["ok"]:
                    print(f"   · {m}")
        return total


def cargar(rel):
    f = B / rel
    if not f.exists():
        return None
    if f.suffix == ".json":
        return json.loads(f.read_text(encoding="utf-8"))
    return yaml.safe_load(f.read_text(encoding="utf-8"))


def inventario_equipo():
    """Todo lo consultable en equipo/: objetos con nombre propio Y las
    categorías bajo las que se agrupan.

    Las categorías importan tanto como los objetos: el manual dice «elige un
    tipo de herramientas de artesano», y eso solo es respondible si la
    categoría existe como grupo enumerable, aunque no haya ningún objeto
    llamado literalmente así.
    """
    nombres = set()

    def walk(o):
        if isinstance(o, dict):
            n = o.get("nombre")
            if isinstance(n, str):
                nombres.add(n)
            for k, v in o.items():
                if isinstance(v, list) and any(isinstance(x, dict) for x in v):
                    nombres.add(k.replace("_", " "))   # categoría enumerable
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for fn in ("armas.yaml", "armaduras.yaml", "herramientas.yaml", "aventureros.yaml",
               "municion.yaml"):
        d = cargar(f"equipo/{fn}")
        if d:
            walk(d)
    return nombres


def _variantes_tok(tok):
    """Formas plausibles de una palabra en singular/plural.

    No intento adivinar UNA forma canónica: el castellano no lo permite
    ("virotes"->"virote" pero "panes"->"pan"). Genero el abanico de candidatos
    y considero que dos palabras coinciden si sus abanicos se cruzan. Es
    asimétrico-tolerante a propósito: prefiero un falso negativo del script
    (que revisaría a mano) antes que un hueco real silenciado.
    """
    v = {tok}
    if len(tok) > 4 and tok.endswith("ces"):
        v.add(tok[:-3] + "z")          # disfraces -> disfraz
    if len(tok) > 3 and tok.endswith("es"):
        v.add(tok[:-2])                # panes -> pan
        v.add(tok[:-1])                # virotes -> virote
    if len(tok) > 2 and tok.endswith("s"):
        v.add(tok[:-1])                # dagas -> daga
    return v


def _tok_coincide(a, b):
    return bool(_variantes_tok(a) & _variantes_tok(b))


def norm(s):
    """Minúsculas, sin paréntesis, sin cantidad inicial. Sin singularizar:
    de eso se encarga la comparación token a token."""
    s = re.sub(r"\(.*?\)", "", str(s)).strip().lower()
    s = re.sub(r"^\d+\s+", "", s)
    s = re.sub(r"[.,;]+$", "", s)
    return " ".join(s.split())


def tokenizar_inventario(nombres):
    return [norm(n).split() for n in nombres if norm(n)]


def coincide(frase, inv_tok):
    q = norm(frase).split()
    if not q:
        return False
    return any(len(c) == len(q) and all(_tok_coincide(x, y) for x, y in zip(q, c))
               for c in inv_tok)


def es_eleccion(item):
    """«elige un tipo de X», «instrumento musical a elección»: el jugador
    escoge. No es un objeto faltante; lo que hay que comprobar es que la
    CATEGORÍA sobre la que elige exista y sea enumerable."""
    return bool(re.search(r"a elección|de tu elección|elegid|elige\b|que has elegido", item, re.I))


def categoria_de(item):
    """Extrae la categoría de una expresión de elección."""
    base = re.sub(r"^(elige|elegid\w*)\s+(un|una|unos|unas)?\s*", "", item, flags=re.I)
    base = re.sub(r"^tipo de\s+", "", base.strip(), flags=re.I)
    base = re.sub(r"\s*(a elección|de tu elección|que has elegido|elegido|para la competencia).*$",
                  "", base, flags=re.I)
    base = re.sub(r"\s*\(las mismas que arriba\)\s*", "", base, flags=re.I)
    return base.strip() or item


def resuelve(item, inv_tok):
    """¿Existe este objeto (o su categoría) como registro consultable?

    Una expresión puede ofrecer alternativas ("herramientas de artesano o
    instrumento musical"): basta con que UNA resuelva, porque el jugador
    elige entre ellas.
    """
    for alt in re.split(r"\s+o\s+", str(item)):
        alt = alt.strip()
        if not alt:
            continue
        cand = categoria_de(alt) if es_eleccion(alt) else categoria_de(alt)
        if coincide(cand, inv_tok):
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Bloque 1: crear un personaje de nivel 1
# ─────────────────────────────────────────────────────────────────────────────
def cobertura_clases(inf, inv_equipo):
    b = inf.bloque("CLASE — lo que la ficha de nivel 1 necesita de cada clase")
    hechizos = (cargar("hechizos.json") or {}).get("hechizos", [])

    for p in sorted((B / "clases").glob("*.yaml")):
        d = cargar(f"clases/{p.name}")
        clase = d.get("clase", p.stem)
        ab = d.get("atributos_basicos") or {}

        # --- puntos de golpe ---
        if d.get("dado_golpe") or ab.get("dado_golpe"):
            inf.ok(b, f"{clase}: dado de golpe")
        else:
            inf.hueco(b, clase, "¿cuál es el dado de puntos de golpe? "
                                "(sin esto no se pueden calcular los PG)")

        # --- competencias ---
        for campo, pregunta in (
            ("salvaciones", "¿en qué tiradas de salvación tiene competencia?"),
            ("habilidades", "¿de qué lista elige habilidades, y cuántas?"),
            ("armas", "¿con qué armas tiene competencia?"),
            ("armaduras", "¿qué armaduras puede llevar? (necesario para la CA)"),
            ("herramientas", "¿con qué herramientas tiene competencia?"),
        ):
            # Ojo: se comprueba PRESENCIA del campo, no que tenga contenido.
            # "Ninguna" es una respuesta válida y completa (el mago no lleva
            # armadura); lo que deja al LLM improvisando es que el campo falte.
            comp = ab.get("competencias") or {}
            if campo in d or campo in ab or campo in comp:
                inf.ok(b, f"{clase}: {campo}")
            else:
                inf.hueco(b, clase, pregunta)

        # --- característica principal y equipo inicial ---
        if ab.get("caracteristica_principal"):
            inf.ok(b, f"{clase}: característica principal")
        else:
            inf.hueco(b, clase, "¿cuál es su característica principal?")

        eq = ab.get("equipo_inicial") or {}
        if eq:
            inf.ok(b, f"{clase}: opciones de equipo inicial")
        else:
            inf.hueco(b, clase, "¿qué equipo inicial ofrece?")

        # cada objeto del equipo inicial debe existir como registro consultable
        for k, texto in sorted(eq.items()):
            if re.fullmatch(r"\d+ po", str(texto).strip()):
                continue
            for item in re.split(r",|\by\b(?=\s)", str(texto)):
                item = item.strip().rstrip(".")
                if not item or re.fullmatch(r"\d+ po", item):
                    continue
                if not resuelve(item, inv_equipo):
                    que = "una categoría de elección" if es_eleccion(item) else "un objeto"
                    inf.hueco(b, clase,
                              f"{que} del equipo inicial no existe como registro en equipo/",
                              f"{clase} opción {k.upper()}: «{item}»")

        # --- rasgos de nivel 1 con texto ---
        rf = B / "clases" / "rasgos" / f"{p.stem}.yaml"
        n1 = [r for f in d.get("progresion", []) if f["n"] == 1 for r in f.get("rasgos", [])]
        if rf.exists():
            rd = cargar(f"clases/rasgos/{p.stem}.yaml") or {}
            con_texto = {r["nombre"] for r in rd.get("rasgos", []) if r.get("desc")}
            faltan = [r for r in n1 if r not in con_texto]
            if faltan:
                inf.hueco(b, clase, "un rasgo de nivel 1 no tiene texto consultable",
                          f"{clase}: {faltan}")
            else:
                inf.ok(b, f"{clase}: rasgos de nivel 1 con texto")
        else:
            inf.hueco(b, clase, "un rasgo de nivel 1 no tiene texto consultable",
                      f"{clase}: no existe clases/rasgos/{p.stem}.yaml")

        # --- conjuros, si lanza ---
        lanz = str(d.get("lanzador", "")).split("#")[0].strip()
        if lanz not in ("ninguno", ""):
            trucos = [h for h in hechizos if h["nivel"] == 0 and clase in (h.get("clases") or [])]
            n1c = [h for h in hechizos if h["nivel"] == 1 and clase in (h.get("clases") or [])]
            if not n1c:
                inf.hueco(b, clase, "es lanzador y un filtro por su nombre no devuelve conjuros de nivel 1")
            else:
                inf.ok(b, f"{clase}: {len(trucos)} trucos y {len(n1c)} conjuros de nivel 1")
            fila1 = next((f for f in d["progresion"] if f["n"] == 1), {})
            if "trucos" in (d.get("columnas_extra") or []) and not fila1.get("trucos"):
                inf.hueco(b, clase, "no consta cuántos trucos conoce en el nivel 1")
    return b


def cobertura_especies(inf):
    b = inf.bloque("ESPECIE — lo que la ficha necesita de cada especie")
    d = cargar("especies/especies.yaml")
    if not d:
        inf.hueco(b, "—", "no existe especies/especies.yaml")
        return b
    lista = next((v for v in d.values() if isinstance(v, list)), [])
    for e in lista:
        nom = e.get("nombre", "?")
        for campo, preg in (("tamano", "¿de qué tamaño es?"),
                            ("velocidad_m", "¿cuál es su velocidad?"),
                            ("rasgos", "¿qué rasgos aporta?")):
            if e.get(campo):
                inf.ok(b, f"{nom}: {campo}")
            else:
                inf.hueco(b, nom, preg)
        for r in (e.get("rasgos") or []):
            if isinstance(r, dict):
                if not (r.get("desc") or r.get("descripcion") or r.get("texto")):
                    inf.hueco(b, nom, "un rasgo de especie no tiene texto consultable",
                              f"{nom}: «{r.get('nombre')}»")
            else:
                # un rasgo escrito como cadena suelta es un NOMBRE sin texto:
                # exactamente el hueco que el LLM rellenaría de memoria
                inf.hueco(b, nom, "un rasgo de especie es solo un nombre, sin texto consultable",
                          f"{nom}: «{r}»")
    return b


def cobertura_trasfondos(inf, inv_equipo):
    b = inf.bloque("TRASFONDO — lo que la ficha necesita de cada trasfondo")
    d = cargar("trasfondos/trasfondos.yaml")
    if not d:
        inf.hueco(b, "—", "no existe trasfondos/trasfondos.yaml")
        return b
    lista = next((v for v in d.values() if isinstance(v, list)), [])

    dotes = set()
    for fn in ("origen.yaml", "generales.yaml", "estilo_de_combate.yaml", "don_epico.yaml"):
        dd = cargar(f"dotes/{fn}") or {}
        for v in dd.values():
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, dict) and x.get("nombre"):
                        dotes.add(x["nombre"])

    herr = set()
    hd = cargar("equipo/herramientas.yaml") or {}
    for k, v in hd.items():
        if isinstance(v, list):
            herr.add(k.replace("_", " "))          # la categoría es enumerable
            for x in v:
                if isinstance(x, dict) and x.get("nombre"):
                    herr.add(x["nombre"])

    for t in lista:
        nom = t.get("nombre", "?")
        if t.get("caracteristicas"):
            inf.ok(b, f"{nom}: características")
        else:
            inf.hueco(b, nom, "¿qué características mejora?")

        dote = re.sub(r"\s*\(.*?\)\s*$", "", str(t.get("dote", ""))).strip()
        if not dote:
            inf.hueco(b, nom, "¿qué dote de origen concede?")
        elif dote not in dotes:
            inf.hueco(b, nom, "la dote que concede no existe en dotes/", f"{nom}: «{dote}»")
        else:
            inf.ok(b, f"{nom}: dote resoluble")

        habs = t.get("habilidades") or []
        malas = [h for h in habs if h not in HABILIDADES]
        if malas:
            inf.hueco(b, nom, "cita una habilidad que no es una de las 18 del juego",
                      f"{nom}: {malas}")
        elif habs:
            inf.ok(b, f"{nom}: habilidades")
        else:
            inf.hueco(b, nom, "¿qué habilidades concede?")

        h = str(t.get("herramienta", "")).strip()
        herr_norm = tokenizar_inventario(herr)
        if not h:
            inf.hueco(b, nom, "¿qué herramienta concede?")
        elif not resuelve(h, herr_norm):
            inf.hueco(b, nom, "la herramienta que concede no existe en equipo/herramientas.yaml",
                      f"{nom}: «{h}»")
        else:
            inf.ok(b, f"{nom}: herramienta resoluble")

        if t.get("equipo_a") and t.get("equipo_b"):
            inf.ok(b, f"{nom}: equipo A/B")
            # el equipo del trasfondo se compra igual que el de clase: sus
            # objetos también tienen que ser consultables uno a uno
            for k in ("equipo_a", "equipo_b"):
                texto = str(t.get(k) or "")
                if re.fullmatch(r"\s*\d+ po\s*", texto):
                    continue
                for item in re.split(r",|\by\b(?=\s)", texto):
                    item = item.strip().rstrip(".")
                    if not item or re.fullmatch(r"\d+ p[oc]", item) or re.match(r"^\d+ p", item):
                        continue
                    if not resuelve(item, inv_equipo):
                        inf.hueco(b, nom,
                                  "un objeto del equipo de trasfondo no existe como registro en equipo/",
                                  f"{nom} {k[-1].upper()}: «{item}»")
        else:
            inf.hueco(b, nom, "¿qué equipo de trasfondo ofrece?")
    return b


def cobertura_reglas_generales(inf):
    """Datos que no cuelgan de ninguna clase pero que la ficha necesita igual."""
    b = inf.bloque("REGLAS GENERALES — lo que la ficha necesita y no pertenece a nadie")
    g = cargar("reglas/generacion_personaje.yaml") or {}

    if (g.get("metodos_generacion_caracteristicas") or {}).get("conjunto_estandar"):
        inf.ok(b, "métodos de generación de características")
    else:
        inf.hueco(b, "reglas", "¿cómo se generan las puntuaciones de característica?")

    if g.get("multiclase"):
        inf.ok(b, "reglas de multiclase")
    else:
        inf.hueco(b, "reglas", "¿qué requisitos tiene multiclasear?")

    # la lista de habilidades y su característica asociada
    hab = cargar("reglas/habilidades.yaml") or {}
    filas = hab.get("habilidades") or []
    nombres = {h.get("nombre") for h in filas if isinstance(h, dict)}
    if nombres == HABILIDADES and all(h.get("caracteristica") for h in filas):
        inf.ok(b, "tabla de habilidades")
    elif filas:
        faltan = sorted(HABILIDADES - nombres)
        sobran = sorted(nombres - HABILIDADES)
        inf.hueco(b, "reglas", "la tabla de habilidades está incompleta o mal formada",
                  f"faltan {faltan}; sobran {sobran}" if (faltan or sobran)
                  else "alguna habilidad sin característica asociada")
    else:
        inf.hueco(b, "reglas",
                  "¿qué 18 habilidades existen y de qué característica depende cada una? "
                  "(necesario para calcular cada bonificador de la ficha)")

    # idiomas
    idi = cargar("reglas/idiomas.yaml") or {}
    if (idi.get("estandar") or idi.get("idiomas_estandar")) and \
       (idi.get("inusuales") or idi.get("idiomas_inusuales")):
        inf.ok(b, "idiomas")
    else:
        inf.hueco(b, "reglas", "¿qué idiomas puede elegir el personaje? "
                               "(todo personaje sabe común y otros dos)")

    # progresión de PX por nivel
    gtxt = (B / "reglas/generacion_personaje.yaml")
    gtxt = gtxt.read_text(encoding="utf-8") if gtxt.exists() else ""
    if re.search(r"px_por_nivel|progreso_de_los_personajes|tabla_experiencia", gtxt, re.I):
        inf.ok(b, "progresión de PX")
    else:
        inf.hueco(b, "reglas", "¿cuántos PX hacen falta para cada nivel? "
                               "(la tabla «Progreso de los personajes»)")
    return b


def cobertura_subir_nivel(inf):
    b = inf.bloque("SUBIR DE NIVEL — lo que /subir-nivel necesita en cada nivel 2-20")
    for p in sorted((B / "clases").glob("*.yaml")):
        d = cargar(f"clases/{p.name}")
        clase = d["clase"]
        rd = cargar(f"clases/rasgos/{p.stem}.yaml") or {}
        con_texto = {r["nombre"] for r in rd.get("rasgos", []) if r.get("desc")}
        sub = cargar(f"clases/subclases/{p.stem}.yaml") or {}
        subclases = sub.get("subclases", [])
        niveles_sub = {r.get("nivel") for s in subclases for r in (s.get("rasgos") or [])}

        for fila in d.get("progresion", []):
            for r in fila.get("rasgos", []):
                if (es_marcador_de("mejora_caracteristica_o_dote", r)
                        or es_marcador_de("subclase", r)):
                    continue
                if es_marcador_de("rasgo_de_subclase", r):
                    if fila["n"] not in niveles_sub:
                        inf.hueco(b, clase,
                                  "la tabla concede un rasgo de subclase en un nivel que ninguna subclase cubre",
                                  f"{clase} N{fila['n']}")
                    continue
                if r not in con_texto:
                    inf.hueco(b, clase, "un rasgo de nivel 2-20 no tiene texto consultable",
                              f"{clase} N{fila['n']}: «{r}»")
        if subclases:
            inf.ok(b, f"{clase}: {len(subclases)} subclases con rasgos")
        else:
            inf.hueco(b, clase, "no tiene ninguna subclase escrita")

    # ¿Sabe la base cuántos PG se ganan al subir? Hasta el 2026-08-30 este
    # bloque comprobaba solo que los RASGOS tuvieran texto, y por eso daba «0
    # preguntas sin responder» mientras la regla del paso 2 de «Subir de nivel»
    # (pdf 44 = libro 42) no existía en ningún fichero. El chequeo cubría lo
    # que su autor recordaba, que es el mismo patrón que dejó dos fórmulas de
    # CA fuera de `calculo.py`.
    g = cargar("reglas/generacion_personaje.yaml") or {}
    pg = (g.get("puntos_golpe") or {}).get("niveles_siguientes_al_1") or {}
    tabla = (pg.get("tabla_valores_establecidos") or {}).get("filas") or []
    cubiertas = {c for fila in tabla for c in fila["clases"]}
    for p_clase in sorted((B / "clases").glob("*.yaml")):
        clase = cargar(f"clases/{p_clase.name}")["clase"]
        if not pg.get("literal"):
            inf.hueco(b, clase, "¿cuántos PG se ganan al subir de nivel? "
                                "(paso 2 de «Subir de nivel»: sin esto no se "
                                "puede subir a nadie de nivel)")
        elif clase not in cubiertas:
            inf.hueco(b, clase, "¿cuál es su valor de PG fijo por nivel? "
                                "(la alternativa a tirar el dado)")
        else:
            inf.ok(b, f"{clase}: PG al subir de nivel (tirada y valor fijo)")

    if not (g.get("puntos_golpe") or {}).get("aumento_de_constitucion"):
        inf.hueco(b, "reglas", "¿qué pasa con los PG máximos cuando sube el "
                               "modificador por Constitución? (es retroactivo: "
                               "sin esto, el total queda mal para siempre)")

    # ¿Puede la base decir QUÉ DOTES puede tomar este personaje? Hasta la
    # Fase 15 el prerrequisito era prosa, así que la respuesta dependía de que
    # el LLM la leyera bien — «casi siempre», que es la amenaza nº 5 del FODA.
    try:
        import prerrequisitos as P
        for pf in sorted((B / "dotes").glob("*.yaml")):
            d = cargar(f"dotes/{pf.name}") or {}
            malos = []
            for x in d.get("dotes", []):
                try:
                    P.analizar(x.get("prerrequisito"))
                except P.ErrorDePrerrequisito:
                    malos.append(x["nombre"])
            if malos:
                inf.hueco(b, pf.name, "¿qué dotes puede tomar el personaje? "
                                      "(hay prerrequisitos que no se pueden "
                                      "evaluar, solo leer)", ", ".join(malos[:4]))
            else:
                inf.ok(b, f"{pf.name}: prerrequisitos evaluables")
    except ImportError:
        inf.hueco(b, "dotes", "¿qué dotes puede tomar el personaje? "
                              "(falta prerrequisitos.py)")

    # /subir-nivel no solo aplica rasgos de clase: hay especies que conceden
    # rasgos al alcanzar cierto nivel (p. ej. Revelación celestial del aasimar
    # en el nivel 3). Si no son consultables, se pierden al subir.
    esp = cargar("especies/especies.yaml") or {}
    for e in next((v for v in esp.values() if isinstance(v, list)), []):
        for r in (e.get("rasgos") or []):
            if isinstance(r, dict) and r.get("nivel"):
                if r.get("desc"):
                    inf.ok(b, f"{e['nombre']}: rasgo de especie en N{r['nivel']}")
                else:
                    inf.hueco(b, e["nombre"],
                              "un rasgo de especie por nivel no tiene texto consultable",
                              f"{e['nombre']} N{r['nivel']}: «{r.get('nombre')}»")
    return b


def main():
    inf = Informe()
    inv = tokenizar_inventario(inventario_equipo())
    print("═" * 70)
    print("COBERTURA — ¿puede la base responder a lo que la skill preguntará?")
    print("═" * 70)
    cobertura_clases(inf, inv)
    cobertura_especies(inf)
    cobertura_trasfondos(inf, inv)
    cobertura_reglas_generales(inf)
    cobertura_subir_nivel(inf)
    total = inf.imprimir()
    print("\n" + "─" * 70)
    if total:
        print(f"❌ {total} preguntas que la base NO puede responder.")
        print("   Cada una es un hueco que el LLM rellenaría con reglas de 2014.")
    else:
        print("✅ La base responde a todas las preguntas simuladas.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
