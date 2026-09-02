#!/usr/bin/env python3
"""Prueba por mutación de los tres chequeos de integridad textual añadidos el
2026-08-29: `validar_tirada()`, `validar_vecindad()` y `validar_ortografia()`.

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable, la
corrompe de una forma distinta cada vez, y comprueba que `validar.py` **salta
por el chequeo que toca**, no por otro.

Los tres nacieron de defectos reales de la oleada 3 de la Fase 13p:

  · `tirada`     — `Inflingir heridas` declaraba «TdS Sab.» sobre un texto que
                   pedía Constitución, y el campo tenía **15 valores distintos
                   para 6 tiradas posibles** (5 erratas de formato).
  · `vecindad`   — `Polimorfar verdadero` llevaba reglas de `Polimorfar` y
                   `Presciencia` el resumen de `Presencia regia de Yolande`,
                   los dos impresos al lado. Con `Aura sagrada` van tres.
  · `ortografía` — `Mal de ojo` decía «acción **Dash**», inglés crudo del CSV;
                   `Disipar magia` decía «eseconjuro».

Como en `mutaciones_dados.py`, **la mitad son controles negativos**. No es
simetría estética: el riesgo real de estos tres es el falso positivo. El de
vecindad se rediseñó entero por eso — su primera versión daba 15 falsos
positivos porque el manual repite texto de verdad entre conjuros hermanos
(`Dominar persona`/`Dominar monstruo`), y ninguna medida de solapamiento
distingue «el manual repite» de «el CSV calcó» sin abrir la página. Por eso
el solapamiento hoy es **aviso**, y lo único que es error duro es un `resumen`
idéntico entre dos conjuros, que no tiene lectura inocente.

    python3 _verificacion/mutaciones_integridad.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent

# Qué chequeo de `validar.py` cubre esta suite. Lo lee `censo.py` (bloque A
# del Plan 18) para contar qué chequeos tienen red y cuáles no; la promesa no
# es gratis: el censo exige que la suite mencione la ETIQUETA que ese chequeo
# imprime, así que no se puede declarar cobertura que no se ejerce.
CHEQUEOS = ("validar_tirada", "validar_vecindad", "validar_ortografia")


def _hechizo(raiz, nombre, campo, fn):
    p = raiz / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    h = next(x for x in d["hechizos"] if x["nombre"] == nombre)
    h[campo] = fn(h.get(campo, ""))
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")


# ══ `tirada` ══════════════════════════════════════════════════════════════

def t_erratа_de_formato(r):
    """La errata exacta que llevaba `Muro de viento`: una coma por un punto."""
    _hechizo(r, "Muro de viento", "tirada", lambda s: "TdS Fue,")
    return "tirada 'TdS Fue,' con coma (la errata real de Muro de viento)"


def t_abreviatura_inventada(r):
    _hechizo(r, "Bola de fuego", "tirada", lambda s: "TdS Dex.")
    return "tirada 'TdS Dex.' (abreviatura inglesa fuera del vocabulario)"


def t_nombre_completo(r):
    _hechizo(r, "Bola de fuego", "tirada", lambda s: "TdS Destreza")
    return "tirada 'TdS Destreza' sin abreviar (la errata de Golpe apresador)"


def t_contradice_su_descripcion(r):
    """El defecto original: el campo dice una característica y el texto otra."""
    _hechizo(r, "Bola de fuego", "tirada", lambda s: "TdS Sab.")
    return "tirada 'TdS Sab.' sobre un texto que pide salvación de Destreza"


def t_vacia_la_base(r):
    p = r / "hechizos.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    for h in d["hechizos"]:
        h.pop("tirada", None)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8")
    return "ningún conjuro tiene ya campo `tirada` (el chequeo se queda ciego)"


def t_declara_salvacion_inexistente(r):
    """El caso que se le escapó a la PRIMERA versión del chequeo.

    `Resurrección` (pdf 331 = libro 329) declaraba «TdS Sab.» sobre un conjuro
    cuya página **no pide ninguna tirada**. La primera versión comparaba la
    característica declarada contra las salvaciones del texto, así que al no
    encontrar ninguna con la que comparar, **pasaba de largo**. Lo encontró una
    relectura de la página, no el chequeo.
    """
    _hechizo(r, "Reparar", "tirada", lambda s: "TdS Car.")
    return "declara 'TdS Car.' en un conjuro cuyo texto no pide ninguna salvación"


def t_directo_con_salvacion_disparadora(r):
    """La semántica de «Directo», fijada el 2026-08-29.

    `Directo` significa «el conjuro se manifiesta igualmente»; si la salvación
    aparece en el primer tercio del texto, casi siempre es el **disparador** y
    el campo debería decir `TdS X`. El umbral se dedujo de los datos: la
    mediana de la primera salvación es del 24 % en los `TdS` y del 48 % en los
    `Directo`.
    """
    _hechizo(r, "Reparar", "tirada", lambda s: "Directo")
    _hechizo(r, "Reparar", "descripcion",
             lambda s: "El objetivo hace una tirada de salvación de Destreza "
                       "o queda afectado. " + s * 3)
    return "'Directo' con la salvación como disparador, al principio del texto"


# ⚠ Esta mutación NO está en `T_DEBEN_SALTAR`, y es deliberado. El umbral
# posicional sirve para **encontrar** candidatos, no para juzgarlos: de los 14
# que marcó, la lectura de la página dijo que 4 eran correctos. Convertirlo en
# error duro habría obligado a declarar excepciones a mano en un tercio de los
# casos, que es peor que un aviso. Hoy es un aviso sobre lo **no revisado**, y
# converge a cero según se leen las páginas.


T_DEBEN_SALTAR = [t_erratа_de_formato, t_abreviatura_inventada, t_nombre_completo,
                  t_contradice_su_descripcion, t_vacia_la_base,
                  t_declara_salvacion_inexistente]


def tn_excepcion_declarada(r):
    """`Contactar con otro plano`: ahí la salvación la hace el lanzador.

    Es el control negativo que da sentido al chequeo. Si alguien «normaliza»
    este valor, la base pierde información que el manual sí distingue.
    """
    _hechizo(r, "Contactar con otro plano", "tirada", lambda s: "TdS Int. propia")
    return "'TdS Int. propia' (excepción citada, no errata)"


def tn_directo_con_salvacion(r):
    """`Bola de fuego` es el `Directo` legítimo de manual: el fuego estalla
    igualmente y la salvación solo reparte la mitad del daño."""
    _hechizo(r, "Bola de fuego", "tirada", lambda s: "Directo")
    return "'Directo' en Bola de fuego (el área estalla igual: la salvación modula)"


def tn_varias_salvaciones(r):
    """Un conjuro que pide dos salvaciones distintas y declara una de ellas."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Además hace una tirada de salvación de Constitución.")
    return "descripción con dos salvaciones, `tirada` declara una de las dos"


def tn_ataque_de_conjuro(r):
    _hechizo(r, "Rayo de escarcha", "tirada", lambda s: "D20+ata.conj.")
    return "'D20+ata.conj.' (valor válido del vocabulario)"


def tn_salvacion_condensada(r):
    """La base condensa a veces «tirada de salvación de X» en «tirada de X».

    No es errata: es el estilo condensado de parte del fichero. El chequeo debe
    reconocerlo como mención de salvación, o daría un falso positivo en decenas
    de conjuros.
    """
    _hechizo(r, "Reparar", "tirada", lambda s: "TdS Sab.")
    _hechizo(r, "Reparar", "descripcion",
             lambda s: s + " El objetivo hace una tirada de Sabiduría.")
    return "«tirada de Sabiduría» sin «de salvación» (estilo condensado válido)"


def tn_directo_con_salvacion_tardia(r):
    """El caso normal de un conjuro de área o de muro: el efecto aparece solo y
    la salvación llega después, para modular el daño de quien esté dentro.

    Es el control negativo que impide que el chequeo se coma los ~50 `Directo`
    legítimos (*Muro de fuego*, *Esfera de llamas*, *Nube incendiaria*…).
    """
    _hechizo(r, "Reparar", "tirada", lambda s: "Directo")
    _hechizo(r, "Reparar", "descripcion",
             lambda s: s * 4 + " Quien entre hace una tirada de salvación de "
                               "Destreza y sufre la mitad del daño si la supera.")
    return "'Directo' con la salvación al final (conjuro de área: modula el daño)"


T_NO_DEBEN_SALTAR = [tn_excepcion_declarada, tn_directo_con_salvacion,
                     tn_varias_salvaciones, tn_ataque_de_conjuro,
                     tn_salvacion_condensada,
                     tn_directo_con_salvacion_tardia]


# ══ `vecindad` ════════════════════════════════════════════════════════════

def v_resumen_calcado(r):
    """El defecto real que encontró el chequeo nada más escribirse.

    `Abrir` y `Acelerar` comparten la página 239: el chequeo solo compara
    vecinos, así que la mutación tiene que serlo de verdad. La primera versión
    de esta prueba usaba dos conjuros de páginas distintas y daba un falso
    «no detectada» — la mutación estaba mal, no el chequeo.
    """
    _hechizo(r, "Abrir", "resumen", lambda s: _resumen_de(r, "Acelerar"))
    return "resumen calcado de otro conjuro de la misma página (239)"


def _resumen_de(raiz, nombre):
    d = json.loads((raiz / "hechizos.json").read_text(encoding="utf-8"))
    return next(x["resumen"] for x in d["hechizos"] if x["nombre"] == nombre)


def v_resumen_calcado_con_mayusculas(r):
    """El calco no debe esconderse cambiando capitalización o espacios."""
    _hechizo(r, "Abrir", "resumen",
             lambda s: "  " + _resumen_de(r, "Acelerar").upper() + " ")
    return "mismo resumen en mayúsculas y con espacios sobrantes"


V_DEBEN_SALTAR = [v_resumen_calcado, v_resumen_calcado_con_mayusculas]


def vn_conjuros_hermanos(r):
    """`Inmovilizar persona` y `Inmovilizar monstruo` comparten el 65 % del
    texto **porque así están impresos**. Es aviso, jamás error."""
    return "conjuros hermanos con texto casi idéntico (base intacta)"


def vn_resumenes_parecidos_no_iguales(r):
    _hechizo(r, "Abrir", "resumen", lambda s: "Una llama que se expande.")
    _hechizo(r, "Acelerar", "resumen", lambda s: "Una llama que se expande hacia delante.")
    return "dos resúmenes parecidos pero distintos en la misma página"


def vn_resumen_igual_en_paginas_distintas(r):
    """El chequeo compara vecinos de página. Dos conjuros lejanos con el mismo
    resumen son sospechosos, pero no son este modo de fallo."""
    _hechizo(r, "Abrir", "resumen", lambda s: "Un estallido.")
    _hechizo(r, "Palabra de poder: matar", "resumen", lambda s: "Un estallido.")
    return "mismo resumen en dos páginas distintas (no es contaminación vecinal)"


V_NO_DEBEN_SALTAR = [vn_conjuros_hermanos, vn_resumenes_parecidos_no_iguales,
                     vn_resumen_igual_en_paginas_distintas]


# ══ `ortografía` ══════════════════════════════════════════════════════════

def o_ingles_crudo(r):
    """El defecto real de `Mal de ojo`."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " El objetivo puede usar la acción Dash.")
    return "«acción Dash» en una descripción (el defecto real de Mal de ojo)"


def o_estado_en_ingles(r):
    _hechizo(r, "Bola de fuego", "resumen", lambda s: str(s) + " Queda Frightened.")
    return "estado «Frightened» sin traducir en un resumen"


def o_palabra_pegada(r):
    """El defecto real de `Disipar magia`."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s.replace("el conjuro", "elconjuro", 1)
             if "el conjuro" in s else s + " Termina elconjuro.")
    return "palabra pegada «elconjuro»"


def o_palabra_pegada_larga(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Hasta que el conjurotermine.")
    return "palabra pegada «conjurotermine» (el defecto real de Presciencia)"


O_DEBEN_SALTAR = [o_ingles_crudo, o_estado_en_ingles, o_palabra_pegada,
                  o_palabra_pegada_larga]


def on_invisible_es_castellano(r):
    """«Invisible» se escribe igual en los dos idiomas: no es inglés crudo.

    Fue el único falso positivo del barrido inicial sobre los 391 conjuros.
    """
    _hechizo(r, "Bola de fuego", "resumen", lambda s: "El objetivo queda Invisible.")
    return "«Invisible», que es palabra castellana idéntica al inglés"


def on_palabra_larga_legitima(r):
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Puedes atravesarlos y recuperarlos después.")
    return "«atravesarlos» y «recuperarlos» (verbos con enclítico, no pegadas)"


def on_nombre_propio_ingles(r):
    """Los nombres propios de conjuro sí llevan grafía extranjera."""
    _hechizo(r, "Bola de fuego", "descripcion",
             lambda s: s + " Similar al Baile irresistible de Otto.")
    return "nombre propio de conjuro con grafía extranjera"


O_NO_DEBEN_SALTAR = [on_invisible_es_castellano, on_palabra_larga_legitima,
                     on_nombre_propio_ingles]


# ══ Arnés ═════════════════════════════════════════════════════════════════

def _falla_por(raiz, etiqueta):
    """¿Salta `validar.py` **por el chequeo pedido**, y no por otra cosa?

    Se mira la línea del chequeo, no el código de salida: una mutación podría
    romper otro validador y dar un falso «detectada».
    """
    res = subprocess.run([sys.executable, "validar.py"],
                         cwd=raiz, capture_output=True, text=True)
    for ln in res.stdout.splitlines():
        s = ln.strip()
        if s.startswith(f"✅ {etiqueta}") or s.startswith(f"❌ {etiqueta}"):
            return s.startswith("❌"), res.stdout
    return None, res.stdout


def _bloque(etiqueta, deben, no_deben):
    print(f"\n══ {etiqueta} " + "═" * (70 - len(etiqueta)))
    ok = 0

    print(" Mutaciones que DEBEN saltar")
    for mut in deben:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            salta, _ = _falla_por(raiz, etiqueta)
            ok += bool(salta)
            print(f"   {'✅' if salta else '❌'} {desc}")
            if not salta:
                print("        ↑ NO DETECTADA — el chequeo no cubre este caso")

    print(" Controles negativos: NO deben saltar")
    for mut in no_deben:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp) / "base"
            shutil.copytree(BASE, raiz, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            desc = mut(raiz)
            salta, _ = _falla_por(raiz, etiqueta)
            ok += not salta
            print(f"   {'✅' if not salta else '❌'} {desc}")
            if salta:
                print("        ↑ FALSO POSITIVO — salta con un dato legítimo")

    return ok, len(deben) + len(no_deben)


def main():
    print("Prueba por mutación de los chequeos de integridad textual")
    print("═" * 74)

    for etiqueta in ("tirada", "vecindad", "ortografía"):
        salta, out = _falla_por(BASE, etiqueta)
        if salta is None:
            print(f"✗ CONTROL: no encuentro la línea del chequeo «{etiqueta}».")
            print(out[-2000:])
            return 1
        if salta:
            print(f"✗ CONTROL: la base sin tocar ya falla por «{etiqueta}». "
                  f"Arréglalo antes de mutar.")
            return 1
    print(" ✅ control · la base intacta pasa los tres chequeos")

    ok = total = 0
    for etiqueta, deben, no_deben in (
            ("tirada", T_DEBEN_SALTAR, T_NO_DEBEN_SALTAR),
            ("vecindad", V_DEBEN_SALTAR, V_NO_DEBEN_SALTAR),
            ("ortografía", O_DEBEN_SALTAR, O_NO_DEBEN_SALTAR)):
        a, b = _bloque(etiqueta, deben, no_deben)
        ok += a
        total += b

    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
