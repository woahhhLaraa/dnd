#!/usr/bin/env python3
"""El censo: ¿queda alguna unidad de la base que NINGÚN chequeo alcance?
(Bloque A del `PLAN_18_REVISION_COMPLETA.md` — 2026-09-02)

── Por qué existe ─────────────────────────────────────────────────────────
Este repo ha perdido ocho veces por el mismo mecanismo: **un módulo lleva
dentro una lista escrita a mano de lo que mira, y esa lista se queda corta
sin que nadie se entere.** `_CA_SIN_ARMADURA` conocía 2 de las 4 fórmulas de
CA. `_ORIGENES` conocía 2 de las 48 subclases. `_TABLA_COSTE` era una copia
muda de una tabla que vive en la base. Los cuatro se arreglaron uno a uno, y
arreglarlos uno a uno es justo lo que hay que dejar de hacer: se arreglan
«las que encontró alguien leyendo el código», no «las que hay».

La regla 6 de `CONTINUAR.md` («la cobertura se descubre, nunca se escribe a
mano») nació en prosa, y el propio repo ya tenía escrito por qué eso no basta
(`FUENTES.md:208`): *«una regla en prosa no impide nada»*. Esto la convierte
en script.

── La invariante, que es CONTABLE ─────────────────────────────────────────
No se trata de prohibir las listas escritas a mano: detectarlas en el AST
sería una heurística con falsos positivos (`_A_METROS`, los nodos del AST y
los mapas de traducción son legítimos). Lo que sí se puede exigir es:

    Toda unidad de la base tiene que estar ALCANZADA POR NOMBRE por algún
    chequeo, o DECLARADA como no alcanzable, con su motivo.

Siete clases de unidad, cada una con su universo descubierto y su alcanzador:

    fichero de regla   → `efectos.origenes()` y su manifiesto
    variable calculable→ `validar._PROMESAS`
    columna de clase   → `verificar_srd.MAPA`
    dato externo       → las llamadas a `verificar_foundry.paquete()`
    chequeo `validar_*`→ una suite de `_verificacion/mutaciones_*.py`
    módulo de la raíz  → una función que `verificar_chequeos.py` audite
    rasgo con texto    → su propio `efectos:` (o `no_automatizado:`)

**Ninguno de los siete universos se escribe aquí**: los seis se descubren
(glob, AST, o el propio vocabulario de la base). Y ningún alcanzador se
escribe aquí tampoco: se leen los objetos que los módulos usan de verdad, así
que renombrar un chequeo o vaciar un mapa se nota.

── Cómo se declara lo que no se alcanza ───────────────────────────────────
En `_verificacion/censo_exenciones.yaml`, una a una y con motivo. Hay dos
clases de declaración, y la diferencia importa:

  · `exentas`   — la unidad NO debe ser alcanzada por ese alcanzador, y se
                  explica quién responde por ella. Es permanente.
  · `pendientes`— es un HUECO REAL, conocido, con el bloque del plan que lo
                  cierra. Es deuda declarada, no permiso.

Una declaración que nombre una unidad que ya no existe **es un error**: el
manifiesto no puede pudrirse en silencio, que es como empezaron los ocho.

── Qué NO mira, y conviene decirlo alto ───────────────────────────────────
No comprueba que el chequeo que alcanza una unidad la compruebe BIEN. Para
eso están las pruebas por mutación (bloque B), y por eso la fila de los
chequeos las exige. El censo cuenta cobertura, no calidad.

    python3 censo.py           # el informe
    python3 censo.py --breve   # solo la última línea
"""
import ast
import fnmatch
import functools
import glob
import json
import pathlib
import sys

import yaml

B = pathlib.Path(__file__).parent
MANIFIESTO = B / "_verificacion" / "censo_exenciones.yaml"


class ErrorDeCenso(Exception):
    """Se lanza cuando el censo no puede ni siquiera contar. Nunca se
    devuelve un número plausible: un censo que se equivoca a la baja es peor
    que no tenerlo."""


def _yaml(rel):
    return yaml.safe_load((B / rel).read_text(encoding="utf-8"))


class Fila:
    """Una clase de unidad, con su universo y quién lo alcanza."""

    def __init__(self, clave, titulo, universo, alcanzadas, quien,
                 declaradas=None, deuda=None, manifiesto=None):
        self.clave = clave
        self.titulo = titulo
        self.universo = universo          # {id: descripción}
        self.alcanzadas = set(alcanzadas) & set(universo)
        self.quien = quien
        # Declaradas EN SU PROPIO MANIFIESTO (no en el del censo): p. ej. los
        # `excluidos` de `reglas/fuentes_de_efectos.yaml`, que ya llevan motivo
        # allí. Repetirlas aquí sería una segunda lista a mano.
        # Se INTERSECAN con el universo, igual que `alcanzadas`. Hasta el
        # 2026-09-05 no se hacía, y esa asimetría era un agujero de la misma
        # familia que el censo persigue: `main()` imprime
        # `len(alcanzadas) + len(declaradas)`, así que una declaración podrida
        # en `fuentes_de_efectos.yaml` —un fichero renombrado, por ejemplo—
        # SUBÍA el recuento sin corresponder a nada, y `muertas` no la veía
        # porque solo recorría el manifiesto del censo. El manifiesto del
        # censo no puede pudrirse; los de las filas, sí podían.
        todas = dict(declaradas or {})
        self.declaradas = {k: v for k, v in todas.items() if k in universo}
        self.declaradas_muertas = {k: v for k, v in todas.items()
                                   if k not in universo}
        self.manifiesto = manifiesto
        # Deuda enumerada en un fichero propio de la fila (el patrón de
        # `chequeos_silenciosos.json`). Cuenta como declarada —no hace fallar—
        # pero se imprime como pendiente: una deuda que no se ve en el informe
        # es una deuda que nadie salda.
        toda = dict(deuda or {})
        self.deuda = {k: v for k, v in toda.items() if k in universo}
        self.deuda_muerta = {k: v for k, v in toda.items() if k not in universo}


# ══ Fila 1 · ficheros de regla ════════════════════════════════════════════
def fila_ficheros_de_regla():
    import efectos as E

    # El universo sale de `efectos.directorios_de_regla()`, que DESCUBRE los
    # directorios en vez de llevarlos escritos. Los `pendientes` entran
    # también: un directorio de regla sin clasificar es exactamente la clase
    # de agujero que este censo existe para contar, y dejarlo fuera del
    # universo lo hacía invisible —así vivió `equipo/` hasta la fase 2.1—.
    universo = {}
    for d in E.directorios_de_regla():
        for p in sorted((B / d).rglob("*.yaml")):
            rel = p.relative_to(B).as_posix()
            universo[f"regla:{rel}"] = rel

    # `origenes()` ya FALLA si encuentra un fichero sin clasificar (C1 del
    # Plan 17). Aquí se cuenta lo mismo desde fuera: si algún día se relaja,
    # el censo lo ve igual.
    alcanzadas = {f"regla:{rel}" for rel, _camino in E.origenes()}
    declaradas = {f"regla:{e['ruta']}": e["motivo"] + " [fuentes_de_efectos.yaml]"
                  for e in E.cargar_manifiesto()["excluidos"]}
    # Y los ficheros de un directorio PENDIENTE: declarados uno a uno con el
    # motivo del directorio, para que la cuenta los vea y digan por qué.
    # Las tres formas legítimas de que un fichero de regla no tenga `efectos:`
    # dentro. `pendientes` es deuda ENUMERADA fichero a fichero: un `.yaml`
    # nuevo sin clasificar sale sin declarar y el censo se pone rojo.
    for d in E.cargar_manifiesto()["derivadas"]:
        for rel in E._rutas_del_patron(d["patron"]):
            declaradas.setdefault(
                f"regla:{rel}",
                f"fuente derivada: sus efectos los fabrica "
                f"`efectos.{d['deriva']}()` [fuentes_de_efectos.yaml]")
    for e in E.cargar_manifiesto()["pendientes"]:
        declaradas.setdefault(
            f"regla:{e['ruta']}",
            f"pendiente de clasificar — {e['motivo']} [fuentes_de_efectos.yaml]")
    return Fila("regla", "ficheros de regla", universo, alcanzadas,
                "efectos.origenes() y su manifiesto", declaradas,
                manifiesto="reglas/fuentes_de_efectos.yaml")


# ══ Fila 2 · variables calculables ════════════════════════════════════════
def fila_variables():
    import efectos as E

    vocab = E.cargar_vocabulario()
    universo = {f"variable:{k}": v.get("desc", "")
                for k, v in vocab["variables"].items()
                if v.get("tipo") == "calculada"}
    # Hasta el bloque A2 esto leía `validar._PROMESAS`, una tupla escrita a
    # mano que conocía 2 de las 3 variables. Ahora las frases de promesa viven
    # PEGADAS a su variable en `reglas/efectos.yaml`, así que una variable
    # calculable está alcanzada si trae las suyas — y `validar_efectos()` hace
    # que no traerlas sea un error. Esta fila lo cuenta desde fuera: si algún
    # día ese error se relaja, el censo lo sigue viendo.
    alcanzadas = {f"variable:{k}" for k, v in vocab["variables"].items()
                  if v.get("tipo") == "calculada" and (v or {}).get("promesas")}
    return Fila("variable", "variables calculables", universo, alcanzadas,
                "sus `promesas` en reglas/efectos.yaml")


# ══ Fila 3 · columnas de las tablas de clase ══════════════════════════════
def fila_columnas():
    import verificar_srd as S

    universo = {}
    for p in sorted((B / "clases").glob("*.yaml")):
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        for reg in doc.get("progresion") or []:
            for col in reg:
                if col == "rasgos":
                    continue
                universo[f"columna:{p.stem}.{col}"] = f"{p.stem} → {col}"

    alcanzadas = set()
    for arch, (_nom_en, cols) in S.MAPA.items():
        for campo in cols.values():
            alcanzadas.add(f"columna:{arch}.{campo}")

    # ── Segundo alcanzador (fase 3 del PLAN_19, 2026-09-02) ──────────────
    # `verificar_foundry.verificar_clases()` contrasta las columnas contra los
    # `ScaleValue` del pack `classes24`, que es la fuente que el SRD de Open5e
    # no publica. Con eso entran `forma_salvaje` y `mov_sin_armadura_m`, las
    # dos únicas que estaban declaradas como pendientes en esta fila.
    #
    # Se lee el mapa que el módulo usa de verdad, no una copia: si alguien
    # quita una escala de ahí, la columna vuelve a salir como hueco.
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vf", B / "verificar_foundry.py")
    vf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vf)
    for columna in vf._ESCALA_A_COLUMNA.values():
        for uid in list(universo):
            if uid.endswith("." + columna):
                alcanzadas.add(uid)
    return Fila("columna", "columnas de tabla de clase", universo, alcanzadas,
                "verificar_srd.MAPA y las escalas de verificar_foundry")


# ══ Fila 4 · categorías de dato externo ═══════════════════════════════════
def _tipos_de_paquete():
    """El universo real: (carpeta, rebanada, `type`) con cuántos registros hay
    en cada terna. La carpeta sola no vale — `equipment24` trae seis `type`
    distintos y los módulos solo piden tres—, y el par (carpeta, `type`)
    tampoco: `classes24/feat` mete en el mismo saco los rasgos de clase, los
    de subclase, las metamagias y las invocaciones, que son cuatro cosas con
    cuatro contrastes distintos. La `rebanada` es la carpeta contenedora del
    fichero, que es como el propio pack los agrupa; no la elegimos nosotros.
    """
    F = B / "_verificacion" / "foundry_srd52"
    if not F.exists():
        raise ErrorDeCenso(f"falta {F} (ver _verificacion/LEEME.md)")
    # Se busca la línea `type:` en vez de parsear el YAML entero: son 1372
    # ficheros y el censo pasaba casi todo su tiempo aquí. El dato es el mismo
    # —`type` es una clave de primer nivel en todos los packs de Foundry— y el
    # fichero se sigue leyendo entero, así que uno con otra forma no se cuela:
    # si no aparece `type:` cuenta como `None`, que es justo lo que devolvía
    # `doc.get("type")`.
    cuenta = {}
    for f in sorted(glob.glob(str(F / "**" / "*.yml"), recursive=True)):
        if "_folder" in f:
            continue
        tipo = None
        for ln in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
            if ln.startswith("type:"):
                tipo = ln.split(":", 1)[1].strip().strip("\"'") or None
                break
        rel = pathlib.Path(f).relative_to(F)
        carpeta, rebanada = rel.parts[0], pathlib.Path(f).parent.name
        clave = (carpeta, rebanada, tipo)
        cuenta[clave] = cuenta.get(clave, 0) + 1
    return cuenta


def _rebanadas_literales(nodo, donde):
    """El `sub=` de una llamada a `paquete()`, que puede ser un nombre o una
    tupla de nombres. Tiene que ser literal: una lista construida en tiempo de
    ejecución dejaría al censo sin saber qué promete la llamada, que es
    exactamente el agujero que la rebanada vino a cerrar."""
    if isinstance(nodo, ast.Constant):
        return [nodo.value]
    if isinstance(nodo, (ast.Tuple, ast.List)):
        if all(isinstance(e, ast.Constant) for e in nodo.elts):
            return [e.value for e in nodo.elts]
    raise ErrorDeCenso(
        f"llamada a paquete() con sub= no literal en {donde}(): el censo no "
        f"puede saber qué rebanada promete")


def _pares_pedidos():
    """Las ternas `(carpeta, rebanada, tipo)` que piden los módulos de
    `verificar_foundry.py`, leídas de sus llamadas reales.

    No se lee `MODULOS` —que solo dice qué módulos hay, no qué tocan— sino el
    argumento de cada llamada. Un módulo que deje de pedir un pack se nota.

    La `rebanada` es `None` cuando la llamada no pasa `sub=`, y eso significa
    «me hago cargo del `type` entero»: alcanza todas las rebanadas. Con `sub=`
    alcanza solo esa, y las demás siguen siendo pendientes con nombre propio.
    """
    src = (B / "verificar_foundry.py").read_text(encoding="utf-8")
    arbol = ast.parse(src)
    pares = set()
    for fn in [n for n in ast.walk(arbol)
               if isinstance(n, ast.FunctionDef) and n.name.startswith("verificar_")]:
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Call) and getattr(n.func, "id", None) == "paquete"):
                continue
            if not n.args or not isinstance(n.args[0], ast.Constant):
                raise ErrorDeCenso(
                    f"llamada a paquete() con carpeta no literal en {fn.name}(): "
                    f"el censo no puede saber qué pack toca")
            carpeta = n.args[0].value
            tipo = None
            if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                tipo = n.args[1].value
            rebanadas = [None]
            for kw in n.keywords:
                if kw.arg == "tipo" and isinstance(kw.value, ast.Constant):
                    tipo = kw.value.value
                if kw.arg == "sub":
                    rebanadas = _rebanadas_literales(kw.value, fn.name)
            for rebanada in rebanadas:
                pares.add((carpeta, rebanada, tipo))
    return pares


def _uid_externo(carpeta, rebanada, tipo):
    return f"externo:{carpeta}/{rebanada}/{tipo}"


def fila_datos_externos():
    cuenta = _tipos_de_paquete()
    universo = {_uid_externo(*k): f"{n} registro" + ("s" if n != 1 else "")
                for k, n in cuenta.items()}

    pedidos = _pares_pedidos()
    alcanzadas = set()
    for (carpeta, rebanada, tipo) in cuenta:
        # `None` en la rebanada pedida = el `type` entero; `None` en el tipo
        # pedido = el pack entero. Los dos comodines son de la LLAMADA, no del
        # manifiesto: los escribe quien se hace cargo, no quien perdona.
        if any((carpeta, sub_p, tipo_p) in pedidos
               for sub_p in (rebanada, None)
               for tipo_p in (tipo, None)):
            alcanzadas.add(_uid_externo(carpeta, rebanada, tipo))
    return Fila("externo", "categorías de dato externo", universo, alcanzadas,
                "verificar_foundry.paquete()")


# ══ Fila 5 · los chequeos `validar_*` ═════════════════════════════════════
@functools.lru_cache(maxsize=None)
def etiquetas_de_chequeo():
    """Cada `validar_*` devuelve `(etiqueta, err, warn)`. Se extrae el prefijo
    ESTABLE de esa etiqueta —la parte literal, antes del recuento— porque es
    lo que una suite de mutación tiene que buscar en la salida para saber que
    saltó el chequeo que toca y no otro.

    Devuelve {nombre_de_funcion: prefijo o None}. `None` = etiqueta dinámica
    (`validar_clase` devuelve el nombre de la clase), y entonces la promesa de
    la suite no se puede contrastar por etiqueta; se dice en el informe en vez
    de darla por buena en silencio.
    """
    arbol = ast.parse((B / "validar.py").read_text(encoding="utf-8"))
    salida = {}
    for fn in [n for n in arbol.body
               if isinstance(n, ast.FunctionDef) and n.name.startswith("validar_")]:
        literales = []
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Return) and isinstance(n.value, ast.Tuple)
                    and n.value.elts):
                continue
            e = n.value.elts[0]
            if isinstance(e, ast.Constant) and isinstance(e.value, str):
                literales.append(e.value)
            elif isinstance(e, ast.JoinedStr):
                trozos = []
                for v in e.values:
                    if isinstance(v, ast.Constant) and isinstance(v.value, str):
                        trozos.append(v.value)
                    else:
                        break
                if trozos:
                    literales.append("".join(trozos))
        prefijo = min(literales, key=len).split("(")[0].strip() if literales else None
        salida[fn.name] = prefijo or None
    return salida


def _promesas_de_las_suites():
    """Qué chequeos dice cubrir cada suite de mutación, y si la promesa se
    sostiene.

    La suite lo declara en `CHEQUEOS`. Que sea una declaración y no una
    deducción es a propósito: deducirlo del AST de once suites heterogéneas
    sería una heurística, y una heurística que se equivoque A FAVOR inventa
    cobertura que no existe — el peor fallo posible en este script.

    Lo que la declaración NO puede hacer es mentir barato: se exige que la
    suite mencione la ETIQUETA que ese chequeo imprime. Una suite que dice
    cubrir `validar_equipo` sin buscar nunca la palabra «equipo» en la salida
    de `validar.py` no lo está cubriendo.
    """
    etiquetas = etiquetas_de_chequeo()
    promesas, problemas, sin_contrastar = {}, [], []
    for f in sorted((B / "_verificacion").glob("mutaciones_*.py")):
        lineas = f.read_text(encoding="utf-8").splitlines()
        arbol = ast.parse("\n".join(lineas))
        declarados, rango = None, None
        for n in arbol.body:
            if isinstance(n, ast.Assign) and any(
                    getattr(t, "id", None) == "CHEQUEOS" for t in n.targets):
                try:
                    declarados = list(ast.literal_eval(n.value))
                except ValueError:
                    raise ErrorDeCenso(
                        f"{f.name}: `CHEQUEOS` no es una lista de literales")
                rango = (n.lineno - 1, n.end_lineno)
        if declarados is None:
            continue          # suite que no cubre ningún `validar_*` (ver informe)
        # El texto contra el que se contrasta la promesa EXCLUYE la propia
        # declaración. Sin esto la promesa se autosatisface: apuntarse
        # `validar_idiomas` mete la cadena «idiomas» en el fichero, y buscar
        # la etiqueta la encontraría… dentro de la promesa que se quería
        # comprobar. Lo destapó `mutaciones_censo.py` con esa mutación exacta.
        texto = "\n".join(lineas[:rango[0]] + lineas[rango[1]:])
        for nombre in declarados:
            if nombre not in etiquetas:
                problemas.append(
                    f"{f.name} dice cubrir «{nombre}», que no es un chequeo de "
                    f"validar.py — o se renombró el chequeo, o la promesa es falsa")
                continue
            etq = etiquetas[nombre]
            if etq is None:
                sin_contrastar.append(f"{f.name} → {nombre} (etiqueta dinámica)")
            elif etq not in texto:
                problemas.append(
                    f"{f.name} dice cubrir «{nombre}» pero no menciona su "
                    f"etiqueta {etq!r}: no puede estar comprobando ese chequeo")
                continue
            promesas.setdefault(nombre, []).append(f.name)
    return promesas, problemas, sin_contrastar


def fila_chequeos():
    etiquetas = etiquetas_de_chequeo()
    universo = {f"chequeo:{n}": (e or "etiqueta dinámica")
                for n, e in etiquetas.items()}
    promesas, problemas, _sin = _promesas_de_las_suites()
    if problemas:
        raise ErrorDeCenso("promesas de cobertura que no se sostienen:\n  · "
                           + "\n  · ".join(problemas))
    alcanzadas = {f"chequeo:{n}" for n in promesas}
    return Fila("chequeo", "chequeos `validar_*`", universo, alcanzadas,
                "una suite de _verificacion/mutaciones_*.py")


# ══ Fila 6 · módulos de herramienta ═══════════════════════════════════════
def fila_modulos():
    """¿Llega `verificar_chequeos.py` a todos los módulos de la raíz?

    Es el caso 6 del §2 del Plan 18, contado. Su `FUENTES` era una tupla de
    seis rutas escritas a mano, y **tres de las seis no aportaban ni una rama**
    porque sus chequeos viven en `main()`, que no se auditaba: estaban en la
    lista, y estar en la lista parecía cobertura. Un módulo sin ninguna función
    auditable no es un fallo —`materiales.py` es una biblioteca— pero tiene que
    estar declarado aquí con su motivo, para que la próxima vez que pase se vea.
    """
    import ast as A
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vc", B / "verificar_chequeos.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)

    universo, alcanzadas = {}, set()
    for rel in vc.fuentes():
        arbol = A.parse((B / rel).read_text(encoding="utf-8"))
        fns = [n.name for n in A.walk(arbol)
               if isinstance(n, A.FunctionDef) and vc._auditable(n.name)]
        universo[f"modulo:{rel}"] = (f"{len(fns)} funciones auditables"
                                     if fns else "ninguna función auditable")
        if fns:
            alcanzadas.add(f"modulo:{rel}")
    return Fila("modulo", "módulos de herramienta", universo, alcanzadas,
                "verificar_chequeos.py")


# ══ Fila 7 · rasgos con texto ═════════════════════════════════════════════
def fila_rasgos():
    import efectos as E

    # Los registros los da `efectos.registros_de()`, no los descubre esta fila
    # descendiendo ella misma (fase 2.2). El motivo es concreto: descender por
    # el `camino` solo sabe leer árboles de rasgos, y por eso
    # `equipo/armaduras.yaml` —una TABLA— no había forma de contarlo aquí. Que
    # el censo tuviera que conocer la forma de cada fichero era el defecto;
    # ahora la conoce quien la fabrica.
    universo, alcanzadas = {}, set()
    for rel in E.fuentes_de_registros():
        for uid, nombre, alcanzado, _motivo in E.registros_de(rel):
            universo[uid] = nombre
            if alcanzado:
                alcanzadas.add(uid)

    # ── La deuda va ENUMERADA, no bajo un comodín (bloque D) ────────────
    # Hasta el 2026-09-02 esta fila se tapaba con `rasgo:*` en el manifiesto.
    # El comodín contaba el crecimiento y lo imprimía, pero **no lo impedía**:
    # un rasgo nuevo sin declarar nada pasaba en verde, y su propia prueba por
    # mutación solo podía exigir que subiera el recuento. Enumerarlos convierte
    # «se ve crecer» en «no puede crecer», que es lo que el bloque D quería
    # decir con «cerrar la puerta».
    # La contabilidad la lleva `deuda.Deuda` desde la fase 1 del PLAN_21. Aquí
    # se leía el JSON a mano y **no se podaba**: era el único de los cinco
    # ficheros de deuda que no podía bajar en disco. Un rasgo que hoy declara
    # `efectos:` y mañana deja de hacerlo volvía a contar como «declarado» sin
    # que nadie lo dijera.
    import deuda as D
    dd = D.Deuda(
        "_verificacion/rasgos_sin_declarar.json",
        nota=("Rasgos con texto que todavía no dicen si tocan alguna variable "
              "calculable. Deuda enumerada, no permiso: solo puede bajar, y "
              "uno nuevo hace fallar al censo."),
        como_se_salda=("el rasgo declara su `efectos:` o su `no_automatizado:` "
                       "con motivo"),
        identidad="fichero-almohadilla-nombre",
        identidad_explicada="fichero#nombre del rasgo")
    if not dd.ruta.exists():
        raise ErrorDeCenso(
            f"falta {dd.ruta.relative_to(B)}: sin él no se distingue un rasgo "
            f"nuevo sin declarar de la deuda conocida")
    sin_declarar = {uid.replace("rasgo:", "", 1): universo[uid]
                    for uid in universo if uid not in alcanzadas}
    inf = dd.contrastar(sin_declarar, elenco_hoy={u.replace("rasgo:", "", 1)
                                                  for u in universo})
    inf.imprimir(vigentes=False)
    conocidos = inf.vigentes
    deuda = {f"rasgo:{uid}": f"{len(conocidos)} rasgos que todavía no dicen "
                             f"si tocan alguna variable calculable"
             for uid in conocidos}
    return Fila("rasgo", "rasgos con texto", universo, alcanzadas,
                "su propio `efectos:` o `no_automatizado:`", deuda=deuda,
                manifiesto="_verificacion/rasgos_sin_declarar.json")


# ══ Fila 8 · efectos con carga ════════════════════════════════════════════
# Fase 1.3 de la auditoría (2026-09-05). La fila que mide si el motor de
# efectos es carga o decoración.
#
# El motivo, medido: de los 25 efectos declarados en la base, **solo 7 los
# aplica alguna ficha de `personajes/`**. Los otros 18 —entre ellos `Duro`,
# que es el efecto que motivó el Plan 17, y el único `modifica_tope` que
# existe— se pueden corromper sin que nada se rompa. `verificar_calculado` ya
# escribió la frase para UNA variable: «para que el efecto sea carga y no
# decoración: si no lo sostuviera ninguna ficha, corromperlo no rompería
# nada». Esta fila lo convierte en una cuenta para las 25.
#
# **Alcanzada exige DOS cosas**, y la segunda es la que importa: que alguna
# ficha aplique el efecto, y que esa ficha tenga `_origen.metodo:
# agente-manual`. Una ficha escrita por el motor no sostiene nada — pinchar
# el motor la movería a ella también, que es justo el círculo que la fase 1.2
# vino a hacer visible. Por eso la fila nace en 0 alcanzadas aunque 7 efectos
# ya se apliquen: la deuda no es «nadie los usa», es «nadie los ha verificado
# desde fuera del motor».
def fila_efectos_con_carga():
    import efectos as E
    import yaml as Y

    def clave(e):
        return (e.get("_archivo"), e.get("_rasgo"), e.get("objetivo"), e.get("op"))

    universo = {}
    for e in E.efectos_declarados():
        arch, rasgo, obj, op = clave(e)
        universo[f"efecto:{arch}#{rasgo}·{obj}·{op}"] = f"{rasgo} → {obj} ({op})"

    alcanzadas = set()
    for p in sorted((B / "personajes").glob("*.yaml")):
        try:
            ficha = Y.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(ficha, dict):
            continue
        origen = (ficha.get("calculado") or {}).get("_origen") or {}
        if origen.get("metodo") != "agente-manual":
            continue        # el motor no puede firmar como su propio oráculo
        try:
            aplicados = E.efectos_de_ficha(ficha)
        except Exception:
            continue
        for e in aplicados:
            arch, rasgo, obj, op = clave(e)
            alcanzadas.add(f"efecto:{arch}#{rasgo}·{obj}·{op}")

    # Deuda ENUMERADA, como los rasgos del bloque D: se salda escribiendo
    # fichas con lectura independiente (el mandato «el calculista»), no
    # tocando esta lista. La contabilidad —podar, distinguir lo nuevo de lo
    # perdido, guardar el elenco— la lleva `deuda.Deuda` desde la fase 1 del
    # PLAN_21; aquí estaba escrita a mano, y sin elenco: un efecto nuevo en la
    # base y un efecto que PERDIÓ su carga se contaban igual.
    import deuda as D
    dd = D.Deuda(
        "_verificacion/efectos_sin_carga.json",
        nota=("Efectos declarados que NINGUNA ficha con `_origen: "
              "agente-manual` sostiene. Es deuda enumerada, no permiso: solo "
              "puede bajar, y se salda con el mandato «el calculista» de "
              "PLAN_ESTRES.md, no editando esta lista."),
        como_se_salda=("una ficha cuyo `calculado` haya calculado a mano un "
                       "agente desde la página, y que aplique ese efecto, lo "
                       "pincha aquí"),
        identidad="efecto-archivo-rasgo-objetivo-op",
        identidad_explicada="efecto:archivo#rasgo·objetivo·operación")
    inf = dd.contrastar({uid: universo[uid] for uid in universo
                         if uid not in alcanzadas},
                        elenco_hoy=set(universo))
    inf.imprimir(vigentes=False)
    listados = inf.vigentes
    deuda = {uid: f"{len(listados)} efectos que ninguna ficha con lectura "
                  f"independiente sostiene: se pueden corromper y las fichas "
                  f"siguen en verde"
             for uid in listados}
    return Fila("efecto", "efectos con carga", universo, alcanzadas,
                "una ficha con `_origen: agente-manual` que lo aplique",
                deuda=deuda,
                manifiesto="_verificacion/efectos_sin_carga.json")


# ══ Fila 9 · constantes de dominio en Python ══════════════════════════════
# Fase 3 de la auditoría (2026-09-05). La cabecera de este censo había
# rechazado esta fila con un argumento correcto: detectar una constante de
# dominio por la FORMA del literal —«parece una lista de nombres del juego»—
# es una heurística con falsos positivos. Sigue siendo verdad.
#
# Pero no se aplica a una prueba de PERTENENCIA, que es lo que se usa aquí:
#
#   Un literal es constante de dominio si sus cadenas están, TODAS, en el
#   vocabulario de UNA colección de la base — y las colecciones se descubren:
#   claves de cada mapa, `nombre:` de cada lista, ficheros de cada directorio,
#   valores por ruta de clave.
#
# **El umbral se declara, no se esconde:** ≥3 cadenas distintas. Con ≥2 el
# recuento sube a 60 y la mayoría de lo nuevo es navegación estructural
# (`("n", "rasgos")`), que no es vocabulario del juego sino la forma del
# fichero. Bajarlo llenaría el manifiesto de ruido, y un manifiesto lleno de
# ruido no lo lee nadie: que es como se pierde otra vez.
#
# **Y un límite declarado:** el criterio solo ve literales que caben ENTEROS
# en una colección. Un literal que mezcle vocabulario de dos colecciones —el
# «disperso» que el plan preveía— no lo detecta esta prueba. No se inventa un
# detector para eso: se dice que no está.
_UMBRAL_CONSTANTES = 3
_SIN_MIRAR = "sin mirar todavía"


def _colecciones_de_la_base():
    """Los vocabularios de la base, DESCUBIERTOS. Nada de esto va a mano."""
    import json as J
    col = {}

    def add(nombre, valores):
        v = {x for x in valores if isinstance(x, str) and x}
        if len(v) >= _UMBRAL_CONSTANTES:
            col[nombre] = v

    for d in sorted(B.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            add(f"ficheros:{d.name}/", [q.name for q in d.glob("*.yaml")])
            add(f"tallos:{d.name}/", [q.stem for q in d.glob("*.yaml")])

    porruta = {}
    for q in sorted(B.rglob("*.yaml")):
        rel = q.relative_to(B).as_posix()
        if rel.startswith(("personajes/", "_verificacion/")):
            continue
        try:
            doc = yaml.safe_load(q.read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue

        def rec(nodo, ruta):
            if isinstance(nodo, dict):
                add(f"claves:{rel}:{ruta}", nodo.keys())
                for k, v in nodo.items():
                    if isinstance(v, str):
                        porruta.setdefault(k, set()).add(v)
                    rec(v, f"{ruta}.{k}" if ruta else str(k))
            elif isinstance(nodo, list):
                add(f"nombres:{rel}:{ruta}",
                    [x.get("nombre") for x in nodo if isinstance(x, dict)])
                add(f"lista:{rel}:{ruta}", [x for x in nodo if isinstance(x, str)])
                for x in nodo:
                    rec(x, ruta)
        rec(doc, "")
    for k, v in porruta.items():
        add(f"valores:{k}", v)

    try:
        h = J.loads((B / "hechizos.json").read_text(encoding="utf-8"))
        regs = h if isinstance(h, list) else (h.get("hechizos") or [])
        add("nombres:hechizos.json",
            [x.get("nombre") for x in regs if isinstance(x, dict)])
    except Exception:                                       # noqa: BLE001
        pass
    return col


def _literales_de_modulo(rel):
    """Todo literal `Dict`/`Set`/`List`/`Tuple` de cadenas, TAMBIÉN dentro de
    funciones: si solo se miraran las constantes de módulo, meter el literal
    dentro de una función lo haría desaparecer."""
    import ast as A
    arbol = A.parse((B / rel).read_text(encoding="utf-8"))
    for n in A.walk(arbol):
        cadenas = None
        if isinstance(n, (A.List, A.Tuple, A.Set)):
            if n.elts and all(isinstance(e, A.Constant) and isinstance(e.value, str)
                              for e in n.elts):
                cadenas = [e.value for e in n.elts]
        elif isinstance(n, A.Dict):
            claves = [k for k in n.keys if k is not None]
            if claves and len(claves) == len(n.keys) and all(
                    isinstance(k, A.Constant) and isinstance(k.value, str)
                    for k in claves):
                cadenas = [k.value for k in claves]
        if cadenas and len(set(cadenas)) >= _UMBRAL_CONSTANTES:
            yield n.lineno, tuple(sorted(set(cadenas)))


def constantes_de_dominio():
    """[(huella, modulo, cadenas, coleccion, clase)], ordenado y sin líneas.

    **La identidad es la huella del CONJUNTO, no la línea**, para que editar
    por encima no invalide el fichero de declaraciones — la misma lección que
    `verificar_chequeos.py` aprendió con las gemelas.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vc", B / "verificar_chequeos.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)

    col = _colecciones_de_la_base()
    salida, vistas = [], set()
    for rel in vc.fuentes():
        for _ln, cad in _literales_de_modulo(rel):
            s = set(cad)
            encajan = [c for c, v in col.items() if s <= v]
            if not encajan:
                continue
            # La colección más ESTRECHA que lo contiene, y a igualdad la
            # primera por nombre: determinista, y la que más dice.
            cual = min(encajan, key=lambda c: (len(col[c]), c))
            huella = f"{rel}::" + "|".join(cad)
            if huella in vistas:
                continue
            vistas.add(huella)
            clase = "copia_exacta" if s == col[cual] else "subconjunto"
            salida.append((huella, rel, cad, cual, clase,
                           tuple(sorted(col[cual] - s))))
    return sorted(salida)


def fila_constantes_de_dominio():
    """La única fila que debe tender a CERO.

    Las otras ocho cuentan cobertura: suben cuando la base crece y se saldan
    alcanzando lo nuevo. Esta cuenta autoridad duplicada, y solo se salda
    BORRANDO el literal —derivándolo en tiempo de ejecución—. Por eso
    `alcanzada` aquí significa «la constante ya no existe».
    """
    import json
    halladas = constantes_de_dominio()
    universo = {h: f"{rel}: {len(cad)} cadenas de «{cual}» ({clase})"
                for h, rel, cad, cual, clase, _fuera in halladas}
    porhuella = {h: (cual, clase, fuera) for h, _r, _c, cual, clase, fuera in halladas}

    # La contabilidad la lleva `deuda.Deuda` (fase 1 del PLAN_21). Este
    # fichero es el único de los cinco que además de deuda es un MANIFIESTO:
    # cada entrada trae `coleccion`, `clase`, `motivo` y `deja_fuera`, y el
    # censo los usa. Por eso `Deuda` no interpreta el valor de una entrada.
    #
    # Y la migración cazó un defecto del formato viejo: la lista admitía la
    # misma huella dos veces —estaba, con motivos contradictorios— y nadie lo
    # comprobaba. Un diccionario no puede.
    import deuda as D
    dd = D.Deuda(
        "_verificacion/constantes_de_dominio.json",
        nota=("Literales de Python cuyas cadenas están TODAS en el vocabulario "
              "de una colección de la base: autoridad duplicada. Deuda "
              "enumerada, no permiso — solo puede bajar, y se salda DERIVANDO "
              "el literal en tiempo de ejecución, no editando esta lista."),
        como_se_salda={
            "copia_exacta": "se deriva: el literal desaparece",
            "subconjunto": ("se deriva, o se declara aquí con `motivo` y "
                            "`deja_fuera` enumerado. Si la colección crece, "
                            "`deja_fuera` deja de cuadrar y el censo se pone "
                            "rojo: alguien tiene que decidir si lo nuevo "
                            "también entra")},
        identidad="huella-del-conjunto",
        identidad_explicada=("módulo::cadenas del literal, ordenadas. La "
                             "huella del CONJUNTO, no la línea"))
    if not dd.ruta.exists():
        dd.contrastar({h: {"coleccion": cual, "clase": clase,
                           "motivo": _SIN_MIRAR + " (fase 3, PLAN_20_AUDITORIA.md)",
                           "deja_fuera": list(fuera)}
                       for h, _r, _c, cual, clase, fuera in halladas},
                      elenco_hoy=set(porhuella))

    inf = dd.contrastar({h: v for h, v in dd.vigentes.items() if h in porhuella},
                        elenco_hoy=set(porhuella))
    inf.imprimir(vigentes=False,
                 texto=lambda h, v: f"{h.split('::')[0]} — {h.split('::')[1][:60]}…")

    declaradas, deuda, muertas_de_dentro = {}, {}, []
    for huella, e in dd.vigentes.items():
        if huella not in porhuella:
            continue
        cual, clase, fuera = porhuella[huella]
        if list(e.get("deja_fuera") or []) != list(fuera):
            muertas_de_dentro.append(
                f"{huella.split('::')[0]}: su `deja_fuera` ya no cuadra "
                f"—la colección «{cual}» ha cambiado—. Decide si lo nuevo "
                f"entra en el literal o actualiza la declaración")
            continue
        # Un motivo de relleno NO es una declaración: eso sería el perdón que
        # esta fila existe para no dar. Mientras nadie haya mirado el literal,
        # va como DEUDA enumerada —contada, visible, y solo puede bajar—, y
        # pasa a `declaradas` el día que alguien escriba por qué se queda.
        if str(e.get("motivo", "")).startswith(_SIN_MIRAR):
            deuda[huella] = (f"constante de dominio que nadie ha mirado "
                             f"todavía ({clase}, de «{cual}»)")
        else:
            declaradas[huella] = f"{e['motivo']} [constantes_de_dominio.json]"

    for m in muertas_de_dentro:
        print(f" ❌ declaración desfasada · {m}")

    # Una declaración desfasada NO entra ni en `declaradas` ni en `deuda`: su
    # unidad sale SIN DECLARAR y el censo se pone rojo, que es el punto.
    return Fila("constante", "constantes de dominio en Python", universo,
                set(), "que el literal DESAPAREZCA (se derive en ejecución)",
                declaradas, deuda=deuda,
                manifiesto="_verificacion/constantes_de_dominio.json")


FILAS = (fila_ficheros_de_regla, fila_variables, fila_columnas,
         fila_datos_externos, fila_chequeos, fila_modulos, fila_rasgos,
         fila_efectos_con_carga, fila_constantes_de_dominio)


# ══ El manifiesto de declaraciones ════════════════════════════════════════
def cargar_manifiesto():
    if not MANIFIESTO.exists():
        raise ErrorDeCenso(
            f"falta {MANIFIESTO.relative_to(B)}: sin él el censo no puede "
            f"distinguir un hueco de una unidad que no debe alcanzarse")
    m = yaml.safe_load(MANIFIESTO.read_text(encoding="utf-8"))
    for clave in ("exentas", "pendientes"):
        if clave not in m:
            raise ErrorDeCenso(f"{MANIFIESTO.name} no declara «{clave}»")
    exentas, pendientes = {}, {}
    for e in m["exentas"] or []:
        exentas[e["unidad"]] = e["motivo"]
    for e in m["pendientes"] or []:
        pendientes[e["unidad"]] = (e["bloque"], e["motivo"])
    solapan = set(exentas) & set(pendientes)
    if solapan:
        raise ErrorDeCenso(
            "unidades declaradas a la vez exentas y pendientes: "
            + ", ".join(sorted(solapan)) + ". Una unidad o no debe alcanzarse "
            "o es un hueco por cerrar; las dos cosas a la vez es no haberlo decidido")
    return exentas, pendientes


# ── Comodines ─────────────────────────────────────────────────────────────
# Las filas 4 y 6 tienen huecos de tres cifras que se cierran EN BLOQUE (los
# 255 rasgos de clase de Foundry, los 521 rasgos sin `efectos:`). Declararlos
# uno a uno serían 776 líneas de manifiesto que nadie leería, y un manifiesto
# que nadie lee es la novena lista a mano. Se admite `prefijo:*` para declarar
# un GRUPO — pero solo en `pendientes`, y el informe imprime siempre cuántas
# unidades cubre cada comodín: un comodín que crece se ve crecer.
#
# El `*` vale en cualquier posición, no solo al final, porque desde que la
# fila 4 cuenta rebanadas la parte que varía suele estar EN MEDIO
# (`externo:equipment24/*/container` son 30 contenedores repartidos en 30
# carpetas del pack). Un comodín de prefijo obligaría a declarar
# `externo:equipment24/*`, que se tragaría también las armas y las
# herramientas —que sí están contrastadas— si algún día dejaran de estarlo.
def _casa(uid, patron):
    if patron == uid:
        return True
    return "*" in patron and fnmatch.fnmatchcase(uid, patron)


def _declarada(uid, declaraciones):
    for patron in declaraciones:
        if _casa(uid, patron):
            return patron
    return None


def main():
    breve = "--breve" in sys.argv
    try:
        exentas, pendientes = cargar_manifiesto()
        filas = [f() for f in FILAS]
    except (ErrorDeCenso, Exception) as e:
        if isinstance(e, ErrorDeCenso):
            print(f"✗ {e}")
            return 1
        raise

    if any(p.endswith("*") for p in exentas):
        print("✗ los comodines solo valen en `pendientes`: una unidad que NO "
              "debe alcanzarse se declara una a una, con su motivo")
        return 1

    total_huecos = total_pend = 0
    usados = set()
    if not breve:
        print("EL CENSO — ¿alguna unidad de la base sin ningún chequeo que la alcance?")
        print("═" * 74)

    for fila in filas:
        huecos, pend_fila, exe_fila = [], [], []
        en_deuda = []
        for uid in sorted(fila.universo):
            if uid in fila.alcanzadas or uid in fila.declaradas:
                continue
            if uid in fila.deuda:
                en_deuda.append(uid)
                continue
            patron = _declarada(uid, exentas)
            if patron:
                exe_fila.append((uid, patron))
                usados.add(patron)
                continue
            patron = _declarada(uid, pendientes)
            if patron:
                pend_fila.append((uid, patron))
                usados.add(patron)
                continue
            huecos.append(uid)

        total_huecos += len(huecos)
        total_pend += len(pend_fila) + len(en_deuda)
        n = len(fila.universo)
        alcanzadas = len(fila.alcanzadas) + len(fila.declaradas)
        if breve:
            continue
        estado = "❌" if huecos else "✅"
        print(f"\n{estado} {fila.titulo.upper()} — {n} unidades · "
              f"alcanza {fila.quien}")
        print(f"    alcanzadas o declaradas en su manifiesto: {alcanzadas}")
        if exe_fila:
            # Se agrupan por MOTIVO, no por unidad: 24 exenciones con dos
            # motivos son dos decisiones, y leerlas 24 veces esconde eso.
            por_motivo = {}
            for uid, patron in exe_fila:
                por_motivo.setdefault(exentas[patron], []).append(uid)
            print(f"    exentas declaradas: {len(exe_fila)}")
            for motivo, uids in sorted(por_motivo.items()):
                quienes = ", ".join(u.split(":", 1)[1] for u in uids[:6])
                if len(uids) > 6:
                    quienes += f", … ({len(uids)} en total)"
                print(f"      · {quienes}")
                print(f"        {motivo}")
        if en_deuda:
            # El texto lo pone la FILA, no el informe. Estuvo cableado aquí
            # —hablando de rasgos— hasta que la fila 8 lo heredó y empezó a
            # decir «25 rasgos» de unos efectos. Es la misma lección: el
            # informe no sabe de qué habla cada fila; la fila sí.
            print(f"    ⬜ PENDIENTES (deuda enumerada): {len(en_deuda)}")
            motivos = {fila.deuda[u] for u in en_deuda if u in fila.deuda}
            for m in sorted(motivos):
                print(f"      · [D] {m}")
            if fila.manifiesto:
                print(f"        enumerados en {fila.manifiesto}, que solo "
                      f"puede bajar; uno nuevo hace fallar al censo")
        if pend_fila:
            # Igual que las exentas: se agrupa por (bloque, motivo). Siete
            # clases con el MISMO problema en `slots` son un hueco, no siete.
            por_motivo = {}
            for uid, patron in pend_fila:
                por_motivo.setdefault(pendientes[patron], []).append((uid, patron))
            print(f"    ⬜ PENDIENTES (deuda declarada): {len(pend_fila)}")
            for (bloque, motivo), pares in sorted(por_motivo.items()):
                if any(pat.endswith("*") for _u, pat in pares):
                    quienes = f"{len(pares)} unidades"
                else:
                    quienes = ", ".join(u.split(":", 1)[1] for u, _p in pares[:6])
                    if len(pares) > 6:
                        quienes += f", … ({len(pares)} en total)"
                print(f"      · [{bloque}] {quienes}")
                print(f"        {motivo}")
        for uid in huecos[:20]:
            print(f"      🔴 SIN DECLARAR · {uid.split(':', 1)[1]}"
                  f" — {fila.universo[uid]}")
        if len(huecos) > 20:
            print(f"      🔴 … y {len(huecos) - 20} más sin declarar")

    # ── El manifiesto no puede pudrirse ──────────────────────────────────
    # Una declaración que ya no corresponde a nada es peor que inútil: da por
    # cubierto lo que nadie mira. Así empezaron los ocho casos.
    muertas = [p for p in list(exentas) + list(pendientes) if p not in usados]
    # Y las de los manifiestos PROPIOS de cada fila, que hasta el 2026-09-05
    # no se miraban: `reglas/fuentes_de_efectos.yaml` y los ficheros de deuda
    # enumerada. Se nombran con su manifiesto delante, porque el sitio donde
    # hay que ir a borrarlas no es el mismo.
    muertas_de_fila = []
    for fila in filas:
        for uid in sorted(fila.declaradas_muertas) + sorted(fila.deuda_muerta):
            muertas_de_fila.append(f"{uid}  [{fila.manifiesto or fila.quien}]")
    if not breve:
        _promesas, _problemas, sin_contrastar = _promesas_de_las_suites()
        if sin_contrastar:
            print("\n  ℹ promesas de cobertura no contrastables por etiqueta:")
            for s in sin_contrastar:
                print(f"      · {s}")
        if muertas or muertas_de_fila:
            print("\n  🔴 declaraciones que ya no corresponden a ninguna unidad:")
            for p in sorted(muertas) + muertas_de_fila:
                print(f"      · {p}")
            print("      (o la unidad se cerró —bórralas— o el manifiesto se "
                  "quedó viejo, que es como empezaron los ocho)")
        print("\n" + "═" * 74)

    universo_total = sum(len(f.universo) for f in filas)
    muertas_total = len(muertas) + len(muertas_de_fila)
    print(f"{'❌' if (total_huecos or muertas_total) else '✅'} "
          f"{universo_total} unidades censadas · "
          f"{total_huecos} SIN DECLARAR · {total_pend} pendientes declaradas"
          + (f" · {muertas_total} declaraciones muertas" if muertas_total else ""))
    if total_huecos:
        print("   Cada una: o la alcanza un chequeo, o se declara en "
              f"{MANIFIESTO.relative_to(B)} con su motivo.")
    return 1 if (total_huecos or muertas_total) else 0


if __name__ == "__main__":
    sys.exit(main())
