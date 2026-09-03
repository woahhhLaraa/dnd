#!/usr/bin/env python3
"""Prueba por mutación de `verificar_foundry.py`.

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable,
la corrompe de una forma distinta cada vez, y comprueba que el verificador
**salta**. Si una mutación pasa desapercibida, el chequeo correspondiente
no vale.

    python3 _verificacion/mutaciones_foundry.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

BASE = pathlib.Path(__file__).resolve().parent.parent


# ── Mutaciones ────────────────────────────────────────────────────────────
# Cada una devuelve una descripción de lo que corrompe. Reciben la raíz de
# la copia desechable.

def _json_hechizo(raiz, nombre, ruta, valor):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    obj, clave = h, ruta
    if "." in ruta:
        sec, clave = ruta.split(".")
        obj = h[sec]
    obj[clave] = valor
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _yaml_edit(raiz, rel, fn):
    p = raiz / rel
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    fn(d)
    p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def m_escuela_conjuro(r):
    _json_hechizo(r, "Bola de fuego", "escuela", "Abjuración")
    return "escuela de un conjuro cambiada (Bola de fuego -> Abjuración)"


def m_nivel_conjuro(r):
    _json_hechizo(r, "Bola de fuego", "nivel", 9)
    return "nivel de un conjuro cambiado (Bola de fuego -> 9)"


def m_componente_conjuro(r):
    _json_hechizo(r, "Bola de fuego", "componentes.verbal", False)
    return "componente verbal de un conjuro quitado (Bola de fuego)"


def m_ritual_conjuro(r):
    _json_hechizo(r, "Bola de fuego", "ritual", True)
    return "conjuro marcado como ritual sin serlo (Bola de fuego)"


def m_concentracion_conjuro(r):
    _json_hechizo(r, "Bola de fuego", "concentracion", True)
    return "concentración añadida a un conjuro que no la tiene (Bola de fuego)"


def m_tipo_dano_arma(r):
    def f(d):
        a = next(x for x in d["armas_cuerpo_a_cuerpo_marciales"]
                 if x["nombre"] == "Alabarda")
        a["dano"] = a["dano"].replace("cortante", "contundente")
    _yaml_edit(r, "equipo/armas.yaml", f)
    return "tipo de daño de un arma cambiado (Alabarda -> contundente)"


def m_maestria_arma(r):
    def f(d):
        a = next(x for x in d["armas_cuerpo_a_cuerpo_marciales"]
                 if x["nombre"] == "Alabarda")
        a["maestria"] = "Derribar"
    _yaml_edit(r, "equipo/armas.yaml", f)
    return "maestría de un arma cambiada (Alabarda -> Derribar)"


def m_propiedad_arma(r):
    def f(d):
        a = next(x for x in d["armas_cuerpo_a_cuerpo_marciales"]
                 if x["nombre"] == "Alabarda")
        a["propiedades"] = a["propiedades"][:-1]
    _yaml_edit(r, "equipo/armas.yaml", f)
    return "una propiedad de arma borrada (Alabarda)"


def m_ca_armadura(r):
    def f(d):
        a = d["armaduras_pesadas"]["tabla"][0]
        a["ca"] = 18
    _yaml_edit(r, "equipo/armaduras.yaml", f)
    return "CA de una armadura cambiada (Cota guarnecida -> 18)"


def m_fuerza_armadura(r):
    def f(d):
        d["armaduras_pesadas"]["tabla"][0]["fuerza"] = 15
    _yaml_edit(r, "equipo/armaduras.yaml", f)
    return "requisito de Fuerza inventado (Cota guarnecida -> 15)"


def m_velocidad_especie(r):
    def f(d):
        next(x for x in d["especies"] if x["nombre"] == "Enano")["velocidad_m"] = 10.5
    _yaml_edit(r, "especies/especies.yaml", f)
    return "velocidad de una especie cambiada (Enano -> 10,5 m)"


def m_vision_especie(r):
    def f(d):
        e = next(x for x in d["especies"] if x["nombre"] == "Enano")
        for rasgo in e["rasgos"]:
            if "oscurid" in rasgo["nombre"].lower():
                rasgo["desc"] = rasgo["desc"].replace("36 m", "18 m")
    _yaml_edit(r, "especies/especies.yaml", f)
    return "visión en la oscuridad de una especie reducida (Enano 36 -> 18 m)"


def m_glosario_cruzado(r):
    def f(d):
        d["especies"]["Enano"] = "Halfling"
    _yaml_edit(r, "_verificacion/glosario_especies.yaml", f)
    return "glosario de especies mal cruzado (Enano -> Halfling)"


def m_prerrequisito_dote_perdido(r):
    def f(d):
        next(x for x in d["dotes"] if x["nombre"] == "Acechador")["prerrequisito"] = None
    _yaml_edit(r, "dotes/generales.yaml", f)
    return "prerrequisito de una dote borrado (Acechador)"


def m_prerrequisito_dote_cambiado(r):
    def f(d):
        next(x for x in d["dotes"]
             if x["nombre"] == "Don del destino")["prerrequisito"] = "nivel 4 o más"
    _yaml_edit(r, "dotes/don_epico.yaml", f)
    return "nivel de un prerrequisito cambiado (Don del destino 19 -> 4)"


def m_repetible_dote_perdido(r):
    for arch in ("dotes/generales.yaml", "dotes/origen.yaml"):
        def f(d):
            for x in d["dotes"]:
                x["repetible"] = False
        _yaml_edit(r, arch, f)
    return "todas las marcas de repetible borradas"


def m_caracteristicas_trasfondo(r):
    def f(d):
        t = next(x for x in d["trasfondos"] if x["nombre"] == "Acólito")
        t["caracteristicas"] = ["Fuerza", "Destreza", "Constitución"]
    _yaml_edit(r, "trasfondos/trasfondos.yaml", f)
    return "trío de características de un trasfondo cambiado (Acólito)"


def m_oro_trasfondo(r):
    def f(d):
        next(x for x in d["trasfondos"]
             if x["nombre"] == "Erudito")["equipo_b"] = "75 po"
    _yaml_edit(r, "trasfondos/trasfondos.yaml", f)
    return "oro de la opción B cambiado (Erudito 50 -> 75 po)"


def m_habilidad_trasfondo(r):
    def f(d):
        next(x for x in d["trasfondos"]
             if x["nombre"] == "Soldado")["habilidades"] = ["Atletismo"]
    _yaml_edit(r, "trasfondos/trasfondos.yaml", f)
    return "una habilidad de trasfondo borrada (Soldado)"


def m_dote_trasfondo_no_origen(r):
    def f(d):
        next(x for x in d["trasfondos"]
             if x["nombre"] == "Noble")["dote"] = "Acechador"
    _yaml_edit(r, "trasfondos/trasfondos.yaml", f)
    return "trasfondo que concede una dote que no es de origen (Noble)"


def m_herramienta_trasfondo(r):
    def f(d):
        next(x for x in d["trasfondos"]
             if x["nombre"] == "Acólito")["herramienta"] = None
    _yaml_edit(r, "trasfondos/trasfondos.yaml", f)
    return "herramienta de un trasfondo borrada (Acólito)"


def m_caracteristica_herramienta(r):
    def f(d):
        h = next(x for x in d["herramientas_de_artesano"]
                 if x["nombre"] == "Herramientas de albañil")
        h["caracteristica"] = "Carisma"
    _yaml_edit(r, "equipo/herramientas.yaml", f)
    return "característica de una herramienta cambiada (albañil -> Carisma)"


def m_precio_herramienta(r):
    def f(d):
        h = next(x for x in d["otras_herramientas"]
                 if x["nombre"] == "Herramientas de ladrón")
        h["precio"] = "40 po"
    _yaml_edit(r, "equipo/herramientas.yaml", f)
    return "precio de una herramienta cambiado (ladrón 25 -> 40 po)"


def m_alcance_conjuro(r):
    import json as _json
    ruta = r / "hechizos.json"
    d = _json.loads(ruta.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == "Bola de fuego")
    h["alcance"]["pies"] = "30"
    ruta.write_text(_json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    return "alcance de un conjuro cambiado (Bola de fuego -> 30 ft)"


def m_duracion_conjuro(r):
    _json_hechizo(r, "Invisibilidad", "duracion", "8 horas")
    return "duración de un conjuro cambiada (Invisibilidad -> 8 horas)"


def m_coste_material_borrado(r):
    """El defecto que destapó la muestra post-corrección: `coste: null` sobre
    un conjuro cuya página sí exige un material con precio.

    (`Curar heridas en masa` no sirve como cobaya: su coste ya es `null` de
    verdad, así que la mutación no cambiaría nada y daría un falso «no
    detectada».)"""
    _json_hechizo(r, "Resurrección", "componentes.coste", None)
    return "coste del material borrado en un conjuro que sí lo tiene (Resurrección)"


def m_coste_material_cifra(r):
    _json_hechizo(r, "Resurrección", "componentes.coste", "100 po")
    return "cifra del coste cambiada (Resurrección: 1000 po -> 100 po)"


def m_coste_material_unidad(r):
    _json_hechizo(r, "Resurrección", "componentes.coste", "1000 pp")
    return "unidad del coste cambiada (Resurrección: po -> pp)"


def m_coste_material_ilegible(r):
    """Un coste que ningún script puede leer y que no está declarado como
    compuesto: es el caso real de `Indetectable`, que traía «25*» sin unidad."""
    _json_hechizo(r, "Resurrección", "componentes.coste", "1000*")
    return "coste sin unidad («1000*»), sin `materiales` que lo descompongan"


# ── `verificar_clases()`: el pack `classes24/class` ───────────────────────
# Cada una toca una rama distinta del módulo nuevo. La cobaya es el Bárbaro
# siempre que sirve (tres escalas y ninguna excepción declarada), y el Monje
# donde hace falta una columna en pies o la celda de la excepción.

def _clase(raiz, stem, fn):
    _yaml_edit(raiz, f"clases/{stem}.yaml", fn)


def m_dado_golpe_clase(r):
    _clase(r, "barbaro", lambda d: d["atributos_basicos"].update(dado_golpe="d8"))
    return "dado de golpe de una clase cambiado (Bárbaro: d12 -> d8)"


def m_lanzador_clase(r):
    """Rompe la biyección del vocabulario: `full` ya está atado a `completo`
    por las otras clases lanzadoras, así que un Mago `medio` deja a `full`
    apuntando a dos palabras nuestras."""
    _clase(r, "mago", lambda d: d.update(lanzador="medio"))
    return "tipo de lanzador de una clase cambiado (Mago: completo -> medio)"


def m_oro_inicial_clase(r):
    _clase(r, "barbaro",
           lambda d: d["atributos_basicos"]["equipo_inicial"].update(b="50 po"))
    return "oro inicial de una clase cambiado (Bárbaro: 75 po -> 50 po)"


def m_oro_inicial_no_es_oro(r):
    """La última opción de equipo deja de ser una cifra de oro, así que ya no
    hay nada que contrastar con el `wealth` del SRD. Callar aquí sería perder
    el chequeo sin que nadie lo note."""
    _clase(r, "barbaro",
           lambda d: d["atributos_basicos"]["equipo_inicial"].update(b="un hacha"))
    return "última opción de equipo que ya no es oro (Bárbaro: '75 po' -> 'un hacha')"


def m_escala_celda(r):
    def f(d):
        d["progresion"][0]["furias"] = 5
    _clase(r, "barbaro", f)
    return "una celda de escala cambiada (Bárbaro N1 furias: 2 -> 5)"


def m_escala_celda_pies(r):
    """La rama que compara en pies: nuestra columna va en metros y la escala
    del SRD en `ft`, así que el error solo salta si la conversión se hace."""
    def f(d):
        d["progresion"][1]["mov_sin_armadura_m"] = 6
    _clase(r, "monje", f)
    return "celda de escala en pies cambiada (Monje N2 mov_sin_armadura_m: 3 -> 6 m)"


def m_escala_columna_ausente(r):
    def f(d):
        for fila in d["progresion"]:
            fila.pop("furias", None)
    _clase(r, "barbaro", f)
    return "columna que el SRD publica como escala, borrada de la progresión (Bárbaro `furias`)"


def m_columna_sin_contrastar(r):
    """Una columna nuestra que no la mira ni `verificar_srd.py` ni ninguna
    escala del pack, y que nadie ha declarado en `_COLUMNA_SIN_ESCALA`."""
    def f(d):
        for fila in d["progresion"]:
            fila["puntos_de_ira"] = 3
    _clase(r, "barbaro", f)
    return "columna nuestra nueva sin fuente externa ni declaración (Bárbaro `puntos_de_ira`)"


def m_excepcion_escala_movida(r):
    """La excepción declarada ampara el par examinado (nuestro 0, SRD 1), no
    la celda entera. Si nuestro valor cambia, la venda tiene que caerse."""
    def f(d):
        d["progresion"][0]["puntos_concentracion"] = 3
    _clase(r, "monje", f)
    return "celda amparada por una excepción, movida (Monje N1 puntos_concentracion: 0 -> 3)"


# ── `verificar_rasgos_clase()`: `classes24/*/class-features/` ─────────────

def _rasgos(raiz, stem, fn):
    _yaml_edit(raiz, f"clases/rasgos/{stem}.yaml", fn)


def m_rasgo_de_nivel_borrado(r):
    def f(d):
        d["rasgos"] = [x for x in d["rasgos"] if x["nombre"] != "Sentir el peligro"]
    _rasgos(r, "barbaro", f)
    return "un rasgo de clase borrado (Bárbaro N2 «Sentir el peligro»)"


def m_rasgo_de_nivel_movido(r):
    """El defecto que más importa: el rasgo existe, pero en el nivel que no
    es. Un contraste que solo contara rasgos por clase no lo vería."""
    def f(d):
        for x in d["rasgos"]:
            if x["nombre"] == "Sentir el peligro":
                x["nivel"] = 4
    _rasgos(r, "barbaro", f)
    return "un rasgo de clase movido de nivel (Bárbaro «Sentir el peligro»: N2 -> N4)"


def m_rasgo_de_nivel_inventado(r):
    def f(d):
        d["rasgos"].append({"nivel": 2, "nombre": "Rugido intimidante",
                            "desc": "Un rasgo que el manual no imprime."})
    _rasgos(r, "barbaro", f)
    return "un rasgo de clase de más (Bárbaro N2 «Rugido intimidante»)"


def m_excepcion_de_rasgos_movida(r):
    """Las excepciones de `_EXCEPCIONES_RASGOS` amparan el par examinado, no
    el nivel: si nuestro lado cambia, la venda tiene que caerse."""
    def f(d):
        d["rasgos"] = [x for x in d["rasgos"] if x["nombre"] != "Desviar energía"]
    _rasgos(r, "monje", f)
    return "nivel amparado por una excepción, cambiado (Monje N13 «Desviar energía» borrado)"


MUTACIONES = [
    m_coste_material_borrado, m_coste_material_cifra,
    m_coste_material_unidad, m_coste_material_ilegible,
    m_escuela_conjuro, m_nivel_conjuro, m_componente_conjuro,
    m_ritual_conjuro, m_concentracion_conjuro,
    m_tipo_dano_arma, m_maestria_arma, m_propiedad_arma,
    m_ca_armadura, m_fuerza_armadura,
    m_velocidad_especie, m_vision_especie, m_glosario_cruzado,
    m_prerrequisito_dote_perdido, m_prerrequisito_dote_cambiado,
    m_repetible_dote_perdido,
    m_caracteristicas_trasfondo, m_oro_trasfondo, m_habilidad_trasfondo,
    m_dote_trasfondo_no_origen, m_herramienta_trasfondo,
    m_caracteristica_herramienta, m_precio_herramienta,
    m_alcance_conjuro, m_duracion_conjuro,
    m_dado_golpe_clase, m_lanzador_clase,
    m_oro_inicial_clase, m_oro_inicial_no_es_oro,
    m_escala_celda, m_escala_celda_pies, m_escala_columna_ausente,
    m_columna_sin_contrastar, m_excepcion_escala_movida,
    m_rasgo_de_nivel_borrado, m_rasgo_de_nivel_movido,
    m_rasgo_de_nivel_inventado, m_excepcion_de_rasgos_movida,
]


# ── Arnés ─────────────────────────────────────────────────────────────────
def main():
    print("Prueba por mutación de verificar_foundry.py")
    print("─" * 74)

    # control: la base intacta debe pasar
    r = subprocess.run([sys.executable, "verificar_foundry.py"],
                       cwd=BASE, capture_output=True, text=True)
    if r.returncode != 0:
        print("✗ CONTROL: la base sin tocar ya falla. Arréglalo antes de mutar.")
        print(r.stdout[-2000:])
        return 1
    print(" ✅ control · la base intacta pasa\n")

    detectadas = 0
    for mut in MUTACIONES:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            res = subprocess.run([sys.executable, "verificar_foundry.py"],
                                 cwd=raiz, capture_output=True, text=True)
            salta = res.returncode != 0
            detectadas += salta
            print(f" {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("      ↑ NO DETECTADA — ese chequeo no cubre este caso")

    print("─" * 74)
    print(f"{detectadas}/{len(MUTACIONES)} mutaciones detectadas")
    return 0 if detectadas == len(MUTACIONES) else 1


if __name__ == "__main__":
    sys.exit(main())
