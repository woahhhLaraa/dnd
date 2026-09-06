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
    """¿Es `nombre` una ENTRADA de chequeo? (`validar_x`, `verificar_x`, `main`)

    Ojo con lo que esta función NO decide desde la fase 2 del `PLAN_21`: **ya
    no dice qué ramas se auditan**. La usa `censo.fila_modulos` para otra
    pregunta —¿tiene este módulo alguna entrada de chequeo, o es una
    biblioteca?—, y esa sí necesita el prefijo.

    Las dos preguntas compartían predicado, y por eso una rama silenciosa se
    podía esconder MOVIÉNDOLA a un ayudante con otro nombre. No es teórico: al
    poner el muro en este mismo fichero saqué el cuerpo del bucle a
    `_ramas_de()` y **cuatro ramas silenciosas desaparecieron de la línea base
    en verde**, con la poda dándolas por saldadas. Medido el 2026-09-06: 61
    ramas en funciones con prefijo, 59 más en las demás. Casi la mitad de lo
    que este verificador existe para vigilar vivía fuera de su alcance, y
    bastaba un refactor para mandar cualquier rama ahí.
    """
    return nombre.startswith(("validar_", "verificar_")) or nombre == "main"


def _se_audita(_nombre):
    """¿Se miran las ramas de esta función? TODAS.

    No hay convención de nombres que valga: una convención es una lista
    escrita a mano disfrazada, y este módulo existe justamente para cazar lo
    que se escapa de las listas (regla inviolable 6). Cualquier función de una
    herramienta puede abandonar un registro en silencio, y mover código de una
    a otra no puede ser una forma de dejar de mirarlo.

    Se deja como función, y no como el `True` que devuelve, porque el sitio
    donde se decide tiene que existir para poder mutarlo.
    """
    return True


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


def _ramas_de(rel, silencios, tolerados):
    """Mide un fichero fuente. Sacado de `main()` para poder ponerle el muro.

    Antes esto era el cuerpo del bucle, y **un fichero que no se pudiera
    analizar se llevaba el informe entero**: un `SyntaxError` en cualquiera de
    los diecisiete y este verificador no decía ni una línea. Ya pasó una vez en
    este repositorio, con `verificar_foundry.py` y una f-string de 3.12
    (`PLAN_19`, fase 1): cuatro herramientas muertas sin que nadie se enterara.
    """
    p = B / rel
    if not p.exists():
        return
    lineas = p.read_text(encoding="utf-8").splitlines()
    arbol = ast.parse("\n".join(lineas))
    for fn in [n for n in ast.walk(arbol)
               if isinstance(n, ast.FunctionDef) and _se_audita(n.name)]:
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
                # La huella lleva la CONDICIÓN, no solo el cuerpo. Hasta el
                # 2026-09-05 era `rel::funcion::cuerpo`, y el cuerpo de casi
                # todas es la palabra `continue`: 67 ramas colapsaban en 41
                # huellas. Con eso, una rama silenciosa NUEVA que fuera
                # gemela textual de una ya declarada entraba sin que nadie
                # lo dijera —y tres lo hicieron: la deuda subió de 64 a 67
                # con el chequeo en verde—. Es el mismo modo de fallo que la
                # fase 0 de `PLAN_20_AUDITORIA.md` cerró en `censo.py`: un
                # guardián cuya deuda enumerada puede crecer sin ruido.
                # Con la condición dentro, las 67 dan 65 huellas distintas.
                entrada = (rel, fn.name, ultimo.lineno,
                           lineas[ultimo.lineno - 1].strip(),
                           ast.unparse(nodo.test))
                (tolerados if "# TOLERADO:" in ventana else silencios).append(entrada)


def main():
    # ── El muro, fichero a fichero (fase 2 del PLAN_21) ─────────────────
    # Y con él el peligro que el muro TRAE CONSIGO, que no estaba en el plan:
    # lo destapó medir este script antes de tocarlo. Aquí lo medido alimenta
    # una línea base de `deuda.py`, y `Deuda.contrastar` PODA lo que hoy no se
    # mide. Un fichero que reventara y cuyo chequeo simplemente «siguiera»
    # dejaría de aportar sus ramas, la poda las daría por saldadas y **la deuda
    # bajaría sola, en verde**: justo la mentira contra la que existe la línea
    # base, ahora entrando por la puerta que se abrió para no perder informes.
    #
    # Por eso `podar` se apaga en cuanto una fuente falla. El muro no puede
    # decidir esto —no sabe qué alimenta cada chequeo—: lo decide quien mide.
    import informar as _I
    silencios, tolerados, rotas = [], [], []
    for rel in fuentes():
        _v, fallo = _I.muro(_ramas_de, rel, silencios, tolerados, etiqueta=rel)
        if fallo:
            rotas.append(str(fallo))

    # ── La línea base declarada ──────────────────────────────────────────
    # Las 59 ramas que ya existían el 2026-08-30 quedan **contadas y
    # visibles**, no perdonadas: el fichero las lista una a una. Lo que este
    # chequeo garantiza es que **no aparezca ninguna nueva** — que es la parte
    # que de verdad se puede prometer. Cada rama que se anote con `# TOLERADO:`
    # o que empiece a avisar sale de la lista, así que converge a cero y no
    # puede crecer sin que alguien lo vea.
    #
    # ── La identidad es la CONDICIÓN, no solo el cuerpo ──────────────────
    # Hasta el 2026-09-06 la línea base guardaba `fichero::funcion::cuerpo`, y
    # el cuerpo de casi todas es la palabra `continue`: 67 ramas colapsaban en
    # 41 huellas y una rama nueva gemela de otra ya declarada entraba sin ruido.
    # Con la condición dentro son 65 distintas, y las gemelas que quedan llevan
    # un ordinal POR ORDEN DE LÍNEA, no por número de línea: editar por encima
    # no puede invalidar el fichero.
    #
    # La contabilidad —podar, distinguir lo nuevo de lo perdido, guardar el
    # elenco— la lleva `deuda.Deuda` desde la fase 1 del PLAN_21. Aquí vivía
    # escrita a mano, como en otros cuatro sitios.
    import collections
    import deuda as D
    _n = collections.Counter()
    huella = {}
    for r, fn, ln, src, test in sorted(silencios, key=lambda e: (e[0], e[1], e[2])):
        clave = f"{r}::{fn}::{src}::si {test}"
        _n[clave] += 1
        uid = clave if _n[clave] == 1 else f"{clave}#{_n[clave]}"
        huella[uid] = f"{r}:{ln} en {fn}() → si {test}: {src}"

    # El ELENCO son todas las ramas que se miraron, avisen o no: sin él no se
    # puede distinguir «una rama nueva que nunca se midió» de «una que avisaba
    # y ha dejado de avisar».
    elenco = set(huella)
    _m = collections.Counter()
    for r, fn, ln, src, test in sorted(tolerados, key=lambda e: (e[0], e[1], e[2])):
        clave = f"{r}::{fn}::{src}::si {test}"
        _m[clave] += 1
        elenco.add(clave if _m[clave] == 1 else f"{clave}#{_m[clave]}")

    dd = D.Deuda(
        "_verificacion/chequeos_silenciosos.json",
        nota=("Ramas de chequeo que abandonan un registro sin decir nada. Es "
              "DEUDA DECLARADA, no permiso: ninguna nueva puede aparecer, y "
              "cada una que se anote con `# TOLERADO:` o empiece a avisar sale "
              "de aquí."),
        como_se_salda=("se anota con `# TOLERADO: <quién lo cubre>` o se hace "
                       "que la rama avise antes de abandonar el registro"),
        identidad="rama-con-condicion",
        identidad_explicada=("fichero::función::cuerpo::si <condición>, más un "
                             "ordinal para las gemelas. NUNCA el número de "
                             "línea: editar por encima no puede invalidar el "
                             "fichero"),
        # CERRADA: aquí no vale la distinción que sí vale en `motor_sin_carga`.
        # Una rama silenciosa en código nuevo —que nunca estuvo en el elenco—
        # es igual de roja que una que avisaba y ha dejado de avisar: la lista
        # dice «ninguna nueva puede aparecer», y no hace excepción con el
        # código recién escrito, que es justo por donde entran.
        #
        # Se aprendió aquí, en la primera pasada de esta migración: `nuevas`
        # pasó a leer solo `inf.perdidos`, las tres mutaciones de
        # `mutaciones_silencios` dejaron de salir —3/6— y el fichero seguía
        # diciendo «ninguna rama silenciosa nueva». El elenco sigue haciendo
        # falta: no para decidir si es roja, sino para decir cuál de las dos es.
        cerrada=True)
    # `podar=not rotas`: ver el bloque del muro arriba. Una fuente que no se
    # ha podido medir no puede saldar nada.
    inf = dd.contrastar(huella, elenco, podar=not rotas)
    declaradas, nuevas, cerradas = inf.vigentes, inf.rojos, inf.saldados

    print("¿Hay chequeos que abandonen un registro en silencio?")
    print("─" * 74)
    for r in rotas:
        print(f" ❌ NO SE HA PODIDO MEDIR · {r}")
        print(f"      sus ramas no cuentan hoy, y por eso la línea base NO se "
              f"poda: una fuente que revienta no salda nada")
    for rel, fn, ln, src, _t in tolerados:
        print(f" ✅ TOLERADO declarado · {rel}:{ln} en {fn}()")
    for rel, fn, ln, src, test in silencios:
        print(f" ❌ SILENCIO · {rel}:{ln} en {fn}() → si {test}: {src}")
        print(f"      esa rama abandona un registro sin decir nada. O avisa, o "
              f"se declara con `# TOLERADO: <quién lo cubre>`")
    print("─" * 74)
    # La poda, el reparto entre «nueva» y «regresión» y el aviso de lo medido
    # por primera vez los imprime `deuda.Informe`: era la misma prosa en cinco
    # sitios, con cuatro versiones incompletas.
    inf.imprimir(texto=lambda uid, val: val, vigentes=False)
    print(f"   {len(silencios)} silenciosas · {len(tolerados)} declaradas "
          f"`# TOLERADO:` · línea base: {len(declaradas)}")
    if nuevas:
        print(f"❌ {len(nuevas)} ramas silenciosas NUEVAS. O avisan, o se "
              f"declaran con `# TOLERADO: <quién lo cubre>`")
        return 1
    if rotas:
        print(f"❌ {len(rotas)} fuente(s) sin medir: lo verde de arriba no "
              f"cubre lo que no se ha mirado")
        return 1
    print("✅ ninguna rama silenciosa nueva")
    return 0


if __name__ == "__main__":
    sys.exit(main())
