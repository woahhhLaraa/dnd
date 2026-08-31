#!/usr/bin/env python3
"""Prueba por mutación de `validar_efectos()` y del motor `efectos.py` (Fase 14).

Doctrina del proyecto: un validador que nunca ha visto un dato malo no
demuestra nada. Este script copia la base a un directorio desechable, la
corrompe de una forma distinta cada vez, y comprueba que salta **el chequeo que
toca**, no otro.

El chequeo nace de un defecto real y concreto: `calculo.py` traía las cuatro
fórmulas de "CA base" de la base como **dos** `lambda` de Python, con un
comentario que decía «las dos únicas excepciones en el tronco de clase,
confirmado por grep sobre las 12 clases». Era verdad, y era el problema: las
otras dos están en SUBCLASES (*Juego de pies deslumbrante* del Bardo,
*Resistencia dracónica* del Hechicero). El grep miró donde el `lambda` sabía
mirar. Y `bonus_pg_especie`, el campo-parche de la ficha, cubría 1 de los 2
efectos sobre PG máximos, guardaba un 1 fijo que solo vale en nivel 1, y nadie
obligaba a rellenarlo: la única ficha de Enano de la base lo tenía vacío y
verificaba en verde con los PG mal.

Por eso hay **dos familias** de mutación, y la segunda es la que importa:

  · FORMA    — un efecto declarado que está mal escrito (objetivo, operación,
               condición o variable fuera del vocabulario; sin página; ciclo).
               Barato, y lo ve cualquiera.
  · AUSENCIA — prosa que promete una mecánica y **ningún efecto detrás**. Es el
               modo de fallo que de verdad ocurrió, y el único chequeo de forma
               no lo ve nunca: no hay dato malo, hay dato que falta.

Y una tercera sección, CARGA, que comprueba que los efectos no son decorativos:
si se corrompe uno, las 12 fichas de personaje tienen que enterarse.

    python3 _verificacion/mutaciones_efectos.py
"""
import glob
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
MONJE = "clases/rasgos/monje.yaml"
EFECTO_MONJE = ('- {objetivo: ca, op: base, formula: "10 + mod_des + mod_sab", '
                'requiere: [sin_armadura, sin_escudo], pagina: {pdf: 151, libro: 149}}')


def _sust(raiz, rel, viejo, nuevo):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:60]!r}"
    p.write_text(t.replace(viejo, nuevo, 1), encoding="utf-8")


def _muta_monje(raiz, viejo, nuevo):
    _sust(raiz, MONJE, viejo, nuevo)


# ══ FORMA ═════════════════════════════════════════════════════════════════

def f_objetivo_inventado(r):
    _muta_monje(r, "objetivo: ca,", "objetivo: ca_magica,")
    return "objetivo `ca_magica`, que no está en reglas/efectos.yaml"


def f_operacion_inventada(r):
    _muta_monje(r, "op: base,", "op: sumar,")
    return "operación `sumar` en vez de una de las seis declaradas"


def f_condicion_inventada(r):
    _muta_monje(r, "requiere: [sin_armadura, sin_escudo]", "requiere: [de_noche]")
    return "condición `de_noche`, que no existe en el vocabulario"


def f_variable_inventada(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"10 + mod_des + mod_suerte"')
    return "fórmula con `mod_suerte`: una característica que no existe"


def f_sin_pagina(r):
    _muta_monje(r, ", pagina: {pdf: 151, libro: 149}", "")
    return "efecto sin cita de página (regla 2: sin página no entra)"


def f_pagina_no_numerica(r):
    # Se muta el efecto ENTERO, no la subcadena `pagina: {...}`: esa cadena
    # aparece antes en el fichero como página del propio rasgo, y la primera
    # versión de esta mutación corrompía esa otra y daba un falso «no
    # detectada». La mutación estaba mal, no el chequeo.
    _muta_monje(r, EFECTO_MONJE,
                EFECTO_MONJE.replace("{pdf: 151", '{pdf: "151*"'))
    return "página del efecto con asterisco, la errata que ya trajo el CSV"


def f_sintaxis_peligrosa(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"__import__(\'os\').system(\'id\')"')
    return "fórmula que intenta ejecutar código (por eso no se usa eval())"


def f_ciclo(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"10 + pg_max"')
    _sust(r, "especies/especies.yaml", 'formula: "nivel_total"', 'formula: "ca"')
    return "ciclo ca → pg_max → ca (DiceCloud lo llama `dependencyLoop`)"


# ══ AUSENCIA — el modo de fallo que de verdad ocurrió ════════════════════

def a_efecto_borrado_monje(r):
    _muta_monje(r, "    efectos:\n      " + EFECTO_MONJE + "\n", "")
    return ("«Defensa sin armadura» del Monje sin efecto: la prosa promete "
            "«clase de armadura base» y nadie puede calcularla")


def a_efecto_borrado_subclase(r):
    p = r / "clases/subclases/bardo.yaml"
    t = p.read_text(encoding="utf-8")
    i = t.index("        efectos:\n")
    j = t.index("\n", t.index("\n", i) + 1) + 1
    p.write_text(t[:i] + t[j:], encoding="utf-8")
    return ("«Juego de pies deslumbrante» sin efecto — EL caso real: está en "
            "una subclase, que es donde el `lambda` no miraba")


def a_efecto_borrado_pg(r):
    _sust(r, "especies/especies.yaml",
          ', efectos: [{objetivo: pg_max, op: add, formula: "nivel_total", '
          'pagina: {pdf: 192, libro: 190}}]', "")
    return ("«Aguante enano» sin efecto: la prosa dice «PG máximos aumentan» y "
            "los PG salen mal en silencio, como salían antes")


# ══ Controles negativos: NO deben saltar ═════════════════════════════════

def n_otra_formula_valida(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"10 + mod_des + mod_int"')
    return "otra fórmula bien formada (equivocada, pero no es lo que mira este chequeo)"


def n_condicion_mas_estricta(r):
    _muta_monje(r, "requiere: [sin_armadura, sin_escudo]", "requiere: [sin_armadura]")
    return "quitar una condición declarada: sigue siendo vocabulario válido"


def n_prosa_sin_promesa(r):
    _sust(r, MONJE, "Mientras no lleves armadura ni portes un escudo, tu clase de armadura base es",
          "Mientras no lleves armadura ni portes un escudo, tu clase de armadura vale")
    _muta_monje(r, "    efectos:\n      " + EFECTO_MONJE + "\n", "")
    return ("prosa que ya NO promete «CA base» y sin efecto: sin promesa no hay "
            "deuda (control del falso positivo de la mitad AUSENCIA)")


def n_efecto_extra_bien_formado(r):
    _muta_monje(r, EFECTO_MONJE, EFECTO_MONJE + '\n      - {objetivo: pg_max, '
                'op: add, formula: "1", pagina: {pdf: 151, libro: 149}}')
    return "un efecto nuevo, declarado y citado en regla: no es un defecto"


def n_min_en_formula(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"10 + min(mod_des, 2) + mod_sab"')
    return "fórmula con min(): la gramática lo permite (tope de Des de armadura)"


F_DEBEN = [f_objetivo_inventado, f_operacion_inventada, f_condicion_inventada,
           f_variable_inventada, f_sin_pagina, f_pagina_no_numerica,
           f_sintaxis_peligrosa, f_ciclo]
def a_efecto_en_fichero_no_recorrido(r):
    # Actualizado por C1 (Plan 17, 2026-08-31). La mutación original ponía el
    # efecto en `dotes/origen.yaml`, que la tupla `_ORIGENES` no recorría.
    # Desde C1 el motor DESCUBRE sus fuentes y `dotes/` sí se recorre, así que
    # allí el efecto ya no es huérfano — la premisa de la mutación desapareció
    # porque se arregló la causa.
    #
    # La garantía que este caso protege sigue siendo necesaria y no ha
    # cambiado: un `efectos:` en un fichero que NADIE recorre tiene que
    # saltar. Se muda a `equipo/armas.yaml`, que no es fuente de efectos ni
    # está bajo los directorios de regla que `origenes()` clasifica.
    p = r / "equipo/armas.yaml"
    t = p.read_text(encoding="utf-8")
    p.write_text(t + "\nefectos:\n  - {objetivo: ca, op: add, "
                 'formula: "1", pagina: {pdf: 1, libro: 1}}\n',
                 encoding="utf-8")
    return ("un efecto en `equipo/armas.yaml`, que ninguna fuente recorre: "
            "existiría en el YAML y no existiría para el motor")


A_DEBEN = [a_efecto_borrado_monje, a_efecto_borrado_subclase, a_efecto_borrado_pg,
           a_efecto_en_fichero_no_recorrido]
NO_DEBEN = [n_otra_formula_valida, n_condicion_mas_estricta, n_prosa_sin_promesa,
            n_efecto_extra_bien_formado, n_min_en_formula]


# ══ COLUMNA · el escalado que se LEE en vez de copiarse ══════════════════
# La velocidad entró en el motor el 2026-08-30 (deuda 4 del plan) y es la
# primera variable que se calcula leyendo una COLUMNA de la progresión —
# «Movimiento sin armadura» del Monje: +3 m en el nivel 2, +4,5 en el 6…
# La tabla dispersa YA existía como columna, así que el efecto la lee en vez de
# copiarla. Copiarla sería el modo de fallo nº 10.

def f_columna_inexistente(r):
    _muta_monje(r, "columna: mov_sin_armadura_m", "columna: mov_sin_armadura_km")
    return "una columna que la progresión del Monje no tiene"


def f_columna_y_formula(r):
    _muta_monje(r, "columna: mov_sin_armadura_m",
                'columna: mov_sin_armadura_m, formula: "3"')
    return ("`columna` y `formula` a la vez: serían dos fuentes del mismo dato, "
            "que es exactamente el modo de fallo nº 10")


def c_columna_movida(r):
    _sust(r, "clases/monje.yaml", "mov_sin_armadura_m: 3", "mov_sin_armadura_m: 4")
    return ("subir a 4 m el «Movimiento sin armadura» del nivel 2: la ficha del "
            "monje de nivel 2 debe romper")


def f_columna_no_numerica(r):
    _sust(r, "clases/monje.yaml", "mov_sin_armadura_m: 4.5",
          'mov_sin_armadura_m: "cuatro y medio"')
    return ("la columna deja de ser un número EN EL NIVEL 6: la escala se "
            "comprueba entera, no en un punto")


def f_columna_que_desaparece(r):
    _sust(r, "clases/monje.yaml", "mov_sin_armadura_m: 7.5", "mov_sin_armadura_mm: 7.5")
    return "la columna falta en el nivel 14, aunque exista en los demás"


def n_columna_de_otro_nivel(r):
    _sust(r, "clases/monje.yaml", "mov_sin_armadura_m: 9", "mov_sin_armadura_m: 10")
    return ("cambiar el valor del nivel 18, que ninguna ficha alcanza: el motor "
            "no lo lee y no hay nada que romper")


def _falla_por(raiz, etiqueta="efectos"):
    res = subprocess.run([sys.executable, "validar.py"], cwd=raiz,
                         capture_output=True, text=True)
    for ln in res.stdout.splitlines():
        s = ln.strip()
        if s.startswith(f"✅ {etiqueta}") or s.startswith(f"❌ {etiqueta}"):
            return s.startswith("❌"), res.stdout
    return None, res.stdout + res.stderr


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return raiz


def _bloque(titulo, deben, no_deben, prueba):
    print(f"\n══ {titulo} " + "═" * max(0, 70 - len(titulo)))
    ok = 0
    if deben:
        print(" Mutaciones que DEBEN saltar")
        for mut in deben:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = _copia(tmp)
                desc = mut(raiz)
                salta = prueba(raiz)
                ok += bool(salta)
                print(f"   {'✅' if salta else '❌'} {desc}")
                if not salta:
                    print("        ↑ NO DETECTADA — el chequeo no cubre este caso")
    if no_deben:
        print(" Controles negativos: NO deben saltar")
        for mut in no_deben:
            with tempfile.TemporaryDirectory() as tmp:
                raiz = _copia(tmp)
                desc = mut(raiz)
                salta = prueba(raiz)
                ok += not salta
                print(f"   {'✅' if not salta else '❌'} {desc}")
                if salta:
                    print("        ↑ FALSO POSITIVO — salta con un dato legítimo")
    return ok, len(deben) + len(no_deben)


def _fichas_se_enteran(raiz):
    """¿Reacciona alguna de las 12 fichas? Prueba que los efectos son carga, no
    decoración: si se corrompe uno, `verificar_personaje.py` tiene que romper."""
    for f in sorted(glob.glob(str(raiz / "personajes" / "*.yaml"))):
        if "_ESQUEMA" in f:
            continue
        r = subprocess.run([sys.executable, "verificar_personaje.py", f],
                           cwd=raiz, capture_output=True, text=True)
        if r.returncode != 0:
            return True
    return False


def c_formula_movida(r):
    _muta_monje(r, '"10 + mod_des + mod_sab"', '"11 + mod_des + mod_sab"')
    return "subir 1 la CA del Monje: la ficha del dracónido monje debe romper"


def c_pg_enano_movido(r):
    _sust(r, "especies/especies.yaml", 'formula: "nivel_total"', 'formula: "nivel_total + 1"')
    return "subir 1 el Aguante enano: la ficha del enano guerrero debe romper"


def c_condicion_relajada(r):
    _muta_monje(r, "requiere: [sin_armadura, sin_escudo]", "requiere: [sin_armadura]")
    return ("quitar `sin_escudo` al Monje: hoy ninguna ficha lo nota — el hueco "
            "queda declarado, no fingido")


def main():
    print(__doc__.split("\n\n")[0])
    print("═" * 74)

    salta, out = _falla_por(BASE)
    if salta is None:
        print("✗ CONTROL: no encuentro la línea del chequeo «efectos».")
        print(out[-2000:])
        return 1
    if salta:
        print("✗ CONTROL: la base sin tocar ya falla por «efectos». "
              "Arréglalo antes de mutar.")
        return 1
    print(" ✅ control · la base intacta pasa el chequeo de efectos")

    ok = total = 0
    for titulo, deben, no_deben, prueba in (
            ("FORMA · efectos mal escritos", F_DEBEN, [],
             lambda r: _falla_por(r)[0]),
            ("AUSENCIA · prosa que promete y nadie cumple", A_DEBEN, NO_DEBEN,
             lambda r: _falla_por(r)[0]),
            ("COLUMNA · el escalado leído de la tabla",
             [f_columna_inexistente, f_columna_y_formula,
              f_columna_no_numerica, f_columna_que_desaparece], [],
             lambda r: _falla_por(r)[0]),
            ("CARGA · ¿los efectos sostienen las fichas?",
             [c_formula_movida, c_pg_enano_movido, c_columna_movida],
             [c_condicion_relajada, n_columna_de_otro_nivel],
             _fichas_se_enteran)):
        a, b = _bloque(titulo, deben, no_deben, prueba)
        ok += a
        total += b

    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
