#!/usr/bin/env python3
"""Prerrequisitos de dote como dato evaluable (Fase 15).

Hasta hoy el prerrequisito de una dote era **prosa**: `"nivel 4 o más, Fuerza o
Destreza 13 o más"`. Un LLM que la lee acierta casi siempre, y «casi siempre»
es exactamente lo que este proyecto no acepta — la amenaza nº 5 del `FODA.md`
dice que un acierto por el método equivocado es indistinguible de acertar por
casualidad. Con la prosa estructurada, `/subir-nivel` puede **ofrecer solo las
dotes que el personaje puede tomar** en vez de listarlas todas y confiar.

Vocabulario cerrado en `reglas/prerrequisitos.yaml`: 4 átomos, 2 conectores,
**ninguna negación** (no hay ni una en los 65 reales).

**Decisión: se DERIVA, no se duplica.** La estructura no se guarda en
`dotes/*.yaml` al lado de la prosa. Podría, y el plan original decía que sí,
pero sería exactamente lo que la regla 3 de `reglas/_ESQUEMA_efectos.md`
prohíbe: dos copias del mismo dato que nadie vuelve a comparar y que divergen
en silencio la primera vez que alguien corrige una — el modo de fallo nº 10.
El parseo es determinista y el ida y vuelta lo demuestra en los 65, así que la
prosa citada sigue siendo la única fuente y la estructura se calcula al vuelo.

**El chequeo fuerte es de ida y vuelta.** `analizar()` convierte la prosa en
estructura y `renderizar()` la reconstruye; `validar_prerrequisitos()` exige que
el resultado sea **idéntico** al original. Eso demuestra lo único que importa
aquí: que no se perdió ni se inventó nada al estructurar. Un parser que ignore
un término en silencio hace lo mismo que hizo el CSV de origen — devolver algo
plausible y equivocado.
"""
import pathlib
import re

import yaml

B = pathlib.Path(__file__).parent


class ErrorDePrerrequisito(Exception):
    """El parser no entiende un literal. Nunca se devuelve media estructura:
    media estructura es un prerrequisito que se evalúa mal en silencio."""


def vocabulario():
    return yaml.safe_load((B / "reglas/prerrequisitos.yaml").read_text(encoding="utf-8"))


_RE_NIVEL = re.compile(r"^nivel (\d+) o más$")
_RE_RASGO = re.compile(r"^rasgo (.+)$")
_RE_ENTRENAMIENTO = re.compile(r"^entrenamiento con (.+)$")
_RE_CARACT = re.compile(r"^(.+?) (\d+) o más$")


def _lista_o(txt):
    """«A», «A o B», «A, B o C» → [A, B, C]. Es la forma en que el manual
    escribe una alternativa, y la misma para características y para rasgos."""
    cabeza, _, ultimo = txt.rpartition(" o ")
    if not cabeza:
        return [txt.strip()]
    return [p.strip() for p in cabeza.split(",")] + [ultimo.strip()]


def analizar(literal):
    """Prosa → estructura. Lanza si no lo entiende entero."""
    if not literal:
        return None
    sep = "; " if "; " in literal else ", "
    terminos = []
    for bruto in literal.split(sep):
        t = bruto.strip()
        if m := _RE_NIVEL.match(t):
            terminos.append({"tipo": "nivel", "minimo": int(m.group(1))})
        elif m := _RE_ENTRENAMIENTO.match(t):
            terminos.append({"tipo": "entrenamiento", "categoria": m.group(1)})
        elif m := _RE_RASGO.match(t):
            terminos.append({"tipo": "rasgo", "cualquiera_de": _lista_o(m.group(1))})
        elif m := _RE_CARACT.match(t):
            terminos.append({"tipo": "caracteristica",
                             "cualquiera_de": _lista_o(m.group(1)),
                             "minimo": int(m.group(2))})
        else:
            raise ErrorDePrerrequisito(
                f"no entiendo el término {t!r} del prerrequisito {literal!r}. "
                f"Los átomos válidos están en reglas/prerrequisitos.yaml")
    return {"todos": terminos}


def _unir_o(nombres):
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " o " + nombres[-1]


def renderizar(estructura):
    """Estructura → prosa. Tiene que devolver EXACTAMENTE el literal original."""
    if not estructura:
        return None
    partes = []
    for t in estructura["todos"]:
        if t["tipo"] == "nivel":
            partes.append(f"nivel {t['minimo']} o más")
        elif t["tipo"] == "entrenamiento":
            partes.append(f"entrenamiento con {t['categoria']}")
        elif t["tipo"] == "rasgo":
            partes.append(f"rasgo {_unir_o(t['cualquiera_de'])}")
        elif t["tipo"] == "caracteristica":
            partes.append(f"{_unir_o(t['cualquiera_de'])} {t['minimo']} o más")
        else:
            raise ErrorDePrerrequisito(f"tipo de término desconocido: {t['tipo']!r}")
    # El «;» solo cuando algún término lleva comas dentro: es el criterio que
    # usa el propio manual, y por eso el ida y vuelta reproduce el original.
    sep = "; " if any("," in p for p in partes) else ", "
    return sep.join(partes)


# ── Evaluación contra un personaje ───────────────────────────────────────
def _norm(s):
    return str(s).strip().lower()


def evaluar(estructura, personaje):
    """¿Cumple este personaje el prerrequisito? Devuelve `(bool, motivos)`.

    `personaje` es un dict con `nivel_total`, `caracteristicas` ({Fuerza: 15…}),
    `rasgos` (lista de nombres) y `entrenamientos` (lista de categorías).

    Devuelve los motivos SIEMPRE, también cuando cumple: quien ofrezca una dote
    tiene que poder decir por qué se puede tomar, no solo que sí.
    """
    if not estructura:
        return True, ["sin prerrequisito"]
    motivos, cumple = [], True
    for t in estructura["todos"]:
        if t["tipo"] == "nivel":
            ok = personaje.get("nivel_total", 0) >= t["minimo"]
            motivos.append(f"{'✔' if ok else '✗'} nivel {personaje.get('nivel_total')} "
                           f"≥ {t['minimo']}")
        elif t["tipo"] == "caracteristica":
            cars = {_norm(k): v for k, v in (personaje.get("caracteristicas") or {}).items()}
            alcanzan = [c for c in t["cualquiera_de"]
                        if cars.get(_norm(c), 0) >= t["minimo"]]
            ok = bool(alcanzan)
            motivos.append(f"{'✔' if ok else '✗'} "
                           f"{_unir_o(t['cualquiera_de'])} ≥ {t['minimo']}"
                           + (f" (por {alcanzan[0]})" if ok else ""))
        elif t["tipo"] == "rasgo":
            tiene = {_norm(r) for r in (personaje.get("rasgos") or [])}
            hallados = [r for r in t["cualquiera_de"] if _norm(r) in tiene]
            ok = bool(hallados)
            motivos.append(f"{'✔' if ok else '✗'} rasgo "
                           f"{_unir_o(t['cualquiera_de'])}"
                           + (f" (tiene {hallados[0]})" if ok else ""))
        else:
            ent = {_norm(e) for e in (personaje.get("entrenamientos") or [])}
            ok = _norm(t["categoria"]) in ent
            motivos.append(f"{'✔' if ok else '✗'} entrenamiento con "
                           f"{t['categoria']}")
        cumple = cumple and ok
    return cumple, motivos
