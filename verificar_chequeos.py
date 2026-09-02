#!/usr/bin/env python3
"""¿Hay algún chequeo que se salte un registro EN SILENCIO? (2026-08-30)

Este proyecto ya ha perdido dos veces por el mismo mecanismo:

  · `COSTE_COMPUESTO` sacaba seis conjuros del contraste externo «porque el
    modelo no los representaba», y escondía **dos sumas que ninguna página
    imprime**;
  · `continue  # entradas antiguas con ref:` dejó que **nueve de diecisiete
    fichas** violaran la regla 6 de su propio esquema, y esas fichas enseñaron
    el formato malo a todo el que vino después.

Las dos exenciones se escribieron de buena fe. Las dos dejaron de doler, y por
eso dejaron de arreglarse. **Una rama de tolerancia no aplaza un desfase: lo
vuelve invisible, y por tanto permanente.**

Y escribir la regla en `FUENTES.md` no basta: la convención de `coste` llevaba
una semana escrita ahí y se rompió sin querer. Lo que funciona es que la
comprueben los scripts — así que esto lo comprueba.

**Qué mira.** Recorre el AST de los verificadores y busca, dentro de las
funciones `validar_*` / `verificar_*`, las ramas que **abandonan un registro**
(`continue`, `pass` o `return` dentro de un `if`) **sin decir nada**: sin llamar
a `error`, `aviso`, `hueco`, `nota` ni añadir a `err`/`warn`.

**Qué NO mira, y conviene decirlo alto:** no puede ver un chequeo que
sencillamente **no existe**. Nadie contaba los conjuros y esto no lo habría
dicho. Para eso hace falta que alguien construya personajes a propósito — el
estrés con agentes de `PLAN_ESTRES.md`, que por eso es rutina y no anécdota.

**Cómo se declara una tolerancia legítima.** Con un comentario `# TOLERADO:` en
la propia rama, explicando **quién cubre ese caso**. Es una firma, no un
silencio: se lee en la revisión y sale en este informe.

    python3 verificar_chequeos.py
"""
import ast
import pathlib
import sys

B = pathlib.Path(__file__).parent

# ── Qué se audita, y por qué ya no es una lista (bloque A2, 2026-09-02) ───
# `FUENTES` era una tupla de seis rutas escritas a mano. El censo (bloque A)
# la midió y salió el caso 6 del §2 del Plan 18: **de las seis declaradas,
# tres no aportaban NADA**. `verificar_srd.py`, `cobertura.py` y
# `verificar_documentos.py` no tienen ni una función `validar_*`/`verificar_*`
# —sus chequeos viven dentro de `main()`—, así que estaban en la lista, se
# leían enteras, y no se auditaba ni una rama. Estar en la lista parecía
# cobertura y no lo era, que es peor que faltar.
#
# Dos arreglos, y son los mismos de siempre:
#   · los ficheros se DESCUBREN (`*.py` de la raíz) en vez de escribirse;
#   · se audita también `main()`, que es donde esos tres tienen sus bucles.
# Un módulo sin ninguna función auditable no es un fallo —`materiales.py` y
# `prerrequisitos.py` son bibliotecas— pero tiene que estar DECLARADO: lo
# exige `censo.py` en su fila de módulos, con su motivo.
#
# El ámbito nuevo destapó **16 ramas** que nadie miraba, casi todas en los
# `main()` de esos tres. La línea base se regeneró una vez el 2026-09-02 para
# incluirlas: son deuda declarada, no permiso, y desde ahí solo puede bajar.
def _auditable(nombre):
    return nombre.startswith(("validar_", "verificar_")) or nombre == "main"


def fuentes():
    """Los módulos de herramienta de la raíz. Se descubren, no se listan."""
    return tuple(sorted(p.name for p in B.glob("*.py")))


AVISADORES = {"error", "aviso", "hueco", "nota", "ok", "append", "exit",
              "sys.exit", "ErrorDeEfectos", "ErrorDePrerrequisito",
              # Añadida el 2026-09-02 (fase 1 del PLAN_19). No es una excepción
              # al criterio: `una_sola_clase()` EXISTE para decirlo —registra el
              # error de multiclase una sola vez y devuelve False—, así que una
              # rama que la llama y sale no está callándose, está delegando en
              # quien habla. Sin esto, cerrar el agujero de la multiclase habría
              # hecho aparecer tres ramas «silenciosas» que en realidad son las
              # que ahora sí hablan.
              "una_sola_clase"}


# Marcas con las que este proyecto imprime que algo va mal. Un `print` con
# una de ellas ES avisar: `verificar_srd.py` no acumula en `err`, imprime
# directamente («⚠ Bárbaro: falta el yaml»), y contarlo como silencio era un
# falso positivo de esta herramienta, no una rama muda. Un `print` sin marca
# sigue sin contar: imprimir «ok» antes de saltarse un registro es callarse.
_MARCAS_DE_AVISO = ("⚠", "✗", "❌", "🔴")


def _imprime_aviso(n):
    if not (isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print"):
        return False
    for arg in ast.walk(n):
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            if any(m in arg.value for m in _MARCAS_DE_AVISO):
                return True
    return False


def _avisa(nodo):
    """¿Esta rama dice algo antes de abandonar el registro?"""
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            f = n.func
            nombre = getattr(f, "attr", None) or getattr(f, "id", None)
            if nombre in AVISADORES or _imprime_aviso(n):
                return True
        if isinstance(n, ast.Raise):
            return True
    return False


def main():
    silencios, tolerados = [], []
    for rel in fuentes():
        p = B / rel
        if not p.exists():
            continue
        lineas = p.read_text(encoding="utf-8").splitlines()
        arbol = ast.parse("\n".join(lineas))
        for fn in [n for n in ast.walk(arbol)
                   if isinstance(n, ast.FunctionDef) and _auditable(n.name)]:
            for nodo in ast.walk(fn):
                if not isinstance(nodo, ast.If):
                    continue
                for rama in (nodo.body, nodo.orelse):
                    if not rama:
                        continue
                    ultimo = rama[-1]
                    salta = (isinstance(ultimo, (ast.Continue, ast.Pass))
                             or (isinstance(ultimo, ast.Return) and ultimo.value is None))
                    # Se mira el cuerpo de la rama **y su condición**: en
                    # `if not una_sola_clase(ficha, inf): return` quien habla
                    # es la condición, y el cuerpo es solo la salida. Mirar
                    # únicamente el cuerpo marcaba como muda una rama que sí
                    # dice lo que pasa — el falso positivo que apareció al
                    # cerrar el agujero de la multiclase (fase 1, PLAN_19).
                    cuerpo = ast.Module(body=rama, type_ignores=[])
                    if not salta or _avisa(cuerpo) or _avisa(nodo.test):
                        continue
                    # ¿Está declarada como tolerancia con firma?
                    ventana = "\n".join(lineas[nodo.lineno - 1:ultimo.lineno + 1])
                    entrada = (rel, fn.name, ultimo.lineno,
                               lineas[ultimo.lineno - 1].strip())
                    (tolerados if "# TOLERADO:" in ventana else silencios).append(entrada)

    # ── La línea base declarada ──────────────────────────────────────────
    # Las 59 ramas que ya existían el 2026-08-30 quedan **contadas y
    # visibles**, no perdonadas: el fichero las lista una a una. Lo que este
    # chequeo garantiza es que **no aparezca ninguna nueva** — que es la parte
    # que de verdad se puede prometer. Cada rama que se anote con `# TOLERADO:`
    # o que empiece a avisar sale de la lista, así que converge a cero y no
    # puede crecer sin que alguien lo vea.
    import json
    base_f = B / "_verificacion/chequeos_silenciosos.json"
    huella = sorted(f"{r}::{fn}::{src}" for r, fn, _ln, src in silencios)
    if base_f.exists():
        declaradas = json.loads(base_f.read_text(encoding="utf-8"))["ramas"]
        nuevas = [h for h in huella if h not in declaradas]
        cerradas = [h for h in declaradas if h not in huella]
    else:
        declaradas, nuevas, cerradas = huella, [], []
        base_f.write_text(json.dumps(
            {"_nota": "Ramas de chequeo que abandonan un registro sin decir "
                      "nada. Es DEUDA DECLARADA, no permiso: ninguna nueva "
                      "puede aparecer, y cada una que se anote con "
                      "`# TOLERADO:` o empiece a avisar sale de aquí.",
             "_fecha": "2026-08-30", "ramas": huella},
            ensure_ascii=False, indent=1), encoding="utf-8")

    print("¿Hay chequeos que abandonen un registro en silencio?")
    print("─" * 74)
    for rel, fn, ln, src in tolerados:
        print(f" ✅ TOLERADO declarado · {rel}:{ln} en {fn}()")
    for rel, fn, ln, src in silencios:
        print(f" ❌ SILENCIO · {rel}:{ln} en {fn}() → {src!r}")
        print(f"      esa rama abandona un registro sin decir nada. O avisa, o "
              f"se declara con `# TOLERADO: <quién lo cubre>`")
    print("─" * 74)
    for h in nuevas:
        print(f" 🔴 NUEVA rama silenciosa, no estaba en la línea base:\n      {h}")
    if cerradas:
        print(f" ✅ {len(cerradas)} ramas de la línea base ya no están en silencio:")
        for h in cerradas[:6]:
            print(f"      · {h}")
        base_f.write_text(json.dumps(
            {"_nota": json.loads(base_f.read_text(encoding='utf-8'))["_nota"],
             "_fecha": "2026-08-30", "ramas": huella},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print("      (línea base actualizada: la deuda solo puede bajar)")
    print(f"   {len(silencios)} silenciosas · {len(tolerados)} declaradas "
          f"`# TOLERADO:` · línea base: {len(declaradas)}")
    if nuevas:
        print(f"❌ {len(nuevas)} ramas silenciosas NUEVAS. O avisan, o se "
              f"declaran con `# TOLERADO: <quién lo cubre>`")
        return 1
    print("✅ ninguna rama silenciosa nueva")
    return 0


if __name__ == "__main__":
    sys.exit(main())
