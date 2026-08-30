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
FUENTES = ("validar.py", "verificar_personaje.py", "verificar_foundry.py",
           "verificar_srd.py", "cobertura.py", "verificar_documentos.py")
AVISADORES = {"error", "aviso", "hueco", "nota", "ok", "append", "exit",
              "sys.exit", "ErrorDeEfectos", "ErrorDePrerrequisito"}


def _avisa(nodo):
    """¿Esta rama dice algo antes de abandonar el registro?"""
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            f = n.func
            nombre = getattr(f, "attr", None) or getattr(f, "id", None)
            if nombre in AVISADORES:
                return True
        if isinstance(n, ast.Raise):
            return True
    return False


def main():
    silencios, tolerados = [], []
    for rel in FUENTES:
        p = B / rel
        if not p.exists():
            continue
        lineas = p.read_text(encoding="utf-8").splitlines()
        arbol = ast.parse("\n".join(lineas))
        for fn in [n for n in ast.walk(arbol)
                   if isinstance(n, ast.FunctionDef)
                   and (n.name.startswith("validar_") or n.name.startswith("verificar_"))]:
            for nodo in ast.walk(fn):
                if not isinstance(nodo, ast.If):
                    continue
                for rama in (nodo.body, nodo.orelse):
                    if not rama:
                        continue
                    ultimo = rama[-1]
                    salta = (isinstance(ultimo, (ast.Continue, ast.Pass))
                             or (isinstance(ultimo, ast.Return) and ultimo.value is None))
                    if not salta or _avisa(ast.Module(body=rama, type_ignores=[])):
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
