#!/usr/bin/env python3
"""¿Dicen la verdad los documentos de estado?

El estado de este proyecto **vive en disco, no en la conversación**, así que
`CONTINUAR.md` no es documentación: es el dato con el que otra sesión decide qué
hacer. Cuando envejece, quien lo lea trabaja hacia atrás — y eso ya ha pasado:

  · `FODA.md` (2026-08-19) mandaba ejecutar las Fases 9c y 10, **ambas hechas**,
    y daba por abiertos los 155 rasgos de clase y el bug `Clerigo`, **cerrados**.
  · `CONTINUAR.md` decía «lo único pendiente es la Fase 8» una semana después de
    que dejara de serlo, y daba por pendiente la tarea de `fidelidad` ya hecha.
  · `ESTADO_13p.md` describía como pendientes el remuestreo de B5 y tres avisos
    de vecindad, **cerrados el mismo día**.

Tres en una sola sesión. Este script no puede comprobar la prosa, pero sí **las
cifras**, que es donde el desfase se vuelve mentira comprobable: si
`CONTINUAR.md` promete «3012 valores contrastados» y el validador da otra cosa,
una de las dos está mal y hay que mirarlo.

    python3 verificar_documentos.py            # completo (~5 min: corre las
                                               # suites de mutación de verdad)
    python3 verificar_documentos.py --rapido   # solo los validadores (~1 min)

El modo completo es el DEFECTO a propósito. Las cifras de mutación se
desfasaron precisamente porque nadie las comprobaba, y un chequeo que hay que
acordarse de pedir es un chequeo que no existe.
"""
import pathlib
import re
import subprocess
import sys

B = pathlib.Path(__file__).parent


def _salida(script):
    r = subprocess.run([sys.executable, script], cwd=B,
                       capture_output=True, text=True)
    return r.stdout


def _n(patron, texto, etiqueta):
    m = re.search(patron, texto)
    if not m:
        return None, f"no encuentro «{etiqueta}» en la salida real"
    return int(m.group(1).replace(".", "")), None


# Cada comprobación: (qué es, cómo se lee de la realidad, cómo se lee del .md)
def main():
    print("¿Dicen la verdad los documentos de estado?")
    print("─" * 74)

    cont = (B / "CONTINUAR.md").read_text(encoding="utf-8")
    foda = (B / "FODA.md").read_text(encoding="utf-8")
    val = _salida("validar.py")
    srd = _salida("verificar_srd.py")
    fnd = _salida("verificar_foundry.py")

    real = {}
    real["srd"], _ = _n(r"(\d+) valores contrastados contra el SRD", srd, "SRD")
    real["foundry"], _ = _n(r"(\d+) valores contrastados · ", fnd, "Foundry")
    for clave, patron in (("dados", r"dados \((\d+) tiradas\)"),
                          ("conversiones", r"conversiones \((\d+) equivalencias\)"),
                          ("tirada", r"tirada \((\d+) conjuros\)"),
                          ("vecindad", r"vecindad \((\d+) pares"),
                          ("ortografia", r"ortografía \((\d+) campos\)"),
                          ("citas", r"citas de conjuro \((\d+)\)"),
                          ("costes", r"costes sin fuente \((\d+)\)"),
                          # Añadidas el 2026-08-31 (Plan 17). La lista de
                          # cifras vigiladas es ella misma una lista escrita a
                          # mano: `efectos` llevaba desde la Fase 14 sin que
                          # nadie comprobara su número, y `mejoras de dote`
                          # nació hoy. Es el mismo patrón que C1 cierra en el
                          # motor, aquí arriba.
                          ("efectos", r"✅ efectos \((\d+)\)"),
                          ("mejoras", r"mejoras de dote \((\d+)\)")):
        real[clave], _ = _n(patron, val, clave)

    fallos = 0

    # 1. Las cifras que CONTINUAR.md promete en su bloque de comandos.
    prometido = {
        "srd": re.search(r"verificar_srd\.py.*?-> (\d+) valores", cont),
        "foundry": re.search(r"verificar_foundry\.py.*?-> (\d+) valores", cont),
    }
    for clave, m in prometido.items():
        if not m:
            print(f" ⚠ CONTINUAR.md ya no promete una cifra para «{clave}»")
            continue
        dice, es = int(m.group(1)), real[clave]
        ok = dice == es
        fallos += not ok
        print(f" {'✅' if ok else '❌'} CONTINUAR.md dice {dice} para «{clave}» · "
              f"la realidad da {es}")

    # 2. La línea de INTEGRIDAD que CONTINUAR.md enumera.
    # `\s+` en vez de espacios: la frase va partida en varias líneas del .md.
    m = re.search(r"(\d+)\s+dados\s+·\s+(\d+)\s+conversiones\s+·\s+(\d+)\s+conjuros\s+en\s+"
                  r"`tirada`\s+·\s+(\d+)\s+pares\s+de\s+vecindad\s+·\s+(\d+)\s+campos\s+de\s+"
                  r"ortografía\s+·\s+(\d+)\s+citas\s+de\s+conjuro\s+·\s+(\d+)\s+costes"
                  r"\s+sin\s+fuente\s+externa\s+·\s+(\d+)\s+efectos",
                  cont, re.S)
    if not m:
        print(" ⚠ CONTINUAR.md ya no enumera las cifras de INTEGRIDAD")
    else:
        for i, clave in enumerate(("dados", "conversiones", "tirada", "vecindad",
                                   "ortografia", "citas", "costes", "efectos")):
            dice, es = int(m.group(i + 1)), real[clave]
            ok = dice == es
            fallos += not ok
            print(f" {'✅' if ok else '❌'} CONTINUAR.md dice {dice:>4} en "
                  f"«{clave}» · la realidad da {es}")

    m2 = re.search(r"\*{0,2}(\d+) mejoras de dote", cont)
    if not m2:
        print(" ⚠ CONTINUAR.md ya no dice cuántas mejoras de dote hay")
    else:
        dice, es = int(m2.group(1)), real["mejoras"]
        ok = dice == es
        fallos += not ok
        print(f" {'✅' if ok else '❌'} CONTINUAR.md dice {dice:>4} en "
              f"«mejoras de dote» · la realidad da {es}")

    # 3. FODA.md cita el total de los dos contrastes externos.
    m = re.search(r"contrastan \*\*([\d.]+) valores\*\*", foda)
    if m:
        dice = int(m.group(1).replace(".", ""))
        es = real["srd"] + real["foundry"]
        ok = dice == es
        fallos += not ok
        print(f" {'✅' if ok else '❌'} FODA.md dice {dice} valores externos · "
              f"la realidad da {es} ({real['srd']} + {real['foundry']})")

    # 4. Las cifras de las PRUEBAS POR MUTACIÓN.
    # Añadido en la Fase 14, y no por simetría: al retomar el proyecto el
    # 2026-08-29 los documentos daban `mutaciones_integridad` como 23/23
    # (FODA.md, dos veces) y como 21/21 (ESTADO_13p.md) cuando la realidad eran
    # 24/24, y `mutaciones_foundry` como 21/21 en un sitio de CONTINUAR.md y
    # 29/29 en otro. Justo el desfase que este script existe para cazar, en el
    # único bloque de cifras que no miraba.
    #
    # `mutaciones_foundry.py` queda FUERA a propósito: tarda más de diez
    # minutos, y un chequeo de documentos que nadie corre por lento no chequea
    # nada. De ese se comprueba que los documentos no se contradigan entre sí.
    docs = {"CONTINUAR.md": cont, "FODA.md": foda}
    for nombre in ("ESTADO_13p.md",):
        f = B / "_verificacion/_auditoria_rasgos" / nombre
        if f.exists():
            docs[nombre] = f.read_text(encoding="utf-8")

    suites = () if "--rapido" in sys.argv else (
        "mutaciones_dados.py", "mutaciones_conversiones.py",
        "mutaciones_integridad.py", "mutaciones_efectos.py",
        "mutaciones_pg.py", "mutaciones_materiales.py",
        "mutaciones_tiradas.py", "mutaciones_prerrequisitos.py",
        "mutaciones_subida.py", "mutaciones_nivel20.py")
    if not suites:
        print(" ⚠ --rapido: no se comprueban las cifras de mutación")
    # Las suites son independientes entre sí (cada una copia la base a su propio
    # directorio desechable), así que se lanzan a la vez. En serie pasaban de
    # diez minutos, y **un chequeo que nadie corre por lento no chequea nada** —
    # es la misma razón por la que `mutaciones_foundry` se quedó fuera.
    import concurrent.futures
    salidas = {}
    if suites:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(suites)) as ex:
            futuros = {ex.submit(_salida, f"_verificacion/{s}"): s for s in suites}
            for fut in concurrent.futures.as_completed(futuros):
                salidas[futuros[fut]] = fut.result()
    for script in suites:
        salida = salidas[script]
        m = re.search(r"(\d+)\s*/\s*(\d+)", salida.strip().splitlines()[-1])
        if not m or m.group(1) != m.group(2):
            fallos += 1
            print(f" ❌ {script} no termina en verde")
            continue
        real_n = m.group(1)
        desfasados = []
        # ¿Algún documento promete OTRA cifra junto al nombre del script?
        base = script[:-3]
        for nombre, txt in docs.items():
            patron = rf"{re.escape(base)}(?:(?!mutaciones_)[^\n])*?(\d+)\s*/\s*(\d+)"
            for mm in re.finditer(patron, txt):
                if mm.group(1) != real_n:
                    fallos += 1
                    desfasados.append(
                        f" ❌ {nombre} dice {mm.group(1)}/{mm.group(2)} para "
                        f"{base} · la realidad da {real_n}/{real_n}")
        for d in desfasados:
            print(d)
        if not desfasados:
            print(f" ✅ {base} da {real_n}/{real_n} y ningún documento dice otra cosa")

    # Y el que no se ejecuta: que al menos los documentos coincidan entre ellos.
    dichas = set()
    for nombre, txt in docs.items():
        for mm in re.finditer(r"mutaciones_foundry(?:(?!mutaciones_)[^\n])*?(\d+)\s*/\s*(\d+)", txt):
            dichas.add((nombre, mm.group(1)))
    if len({n for _, n in dichas}) > 1:
        fallos += 1
        print(f" ❌ los documentos no se ponen de acuerdo sobre "
              f"mutaciones_foundry: {sorted(dichas)}")
    elif dichas:
        print(f" ✅ mutaciones_foundry: los documentos coinciden "
              f"({sorted({n for _, n in dichas})[0]}); no se ejecuta aquí (>10 min)")

    # 4bis. Ningún chequeo puede abandonar un registro EN SILENCIO.
    # Es la causa raíz de los dos peores desfases del proyecto, así que se
    # comprueba aquí, en la rutina, y no en la buena voluntad de nadie.
    r = subprocess.run([sys.executable, "verificar_chequeos.py"], cwd=B,
                       capture_output=True, text=True)
    if r.returncode:
        fallos += 1
        for ln in r.stdout.splitlines():
            if "NUEVA" in ln or ln.strip().startswith("❌"):
                print(f" {ln.strip()}")
    else:
        resumen = next((l.strip() for l in r.stdout.splitlines()
                        if "línea base" in l), "")
        print(f" ✅ ninguna rama de chequeo silenciosa nueva · {resumen}")

    # 5. Las SKILLS también son documentos de estado, y nadie las miraba.
    # La Fase 14 rompió el paso 10 de `/personaje` —mandaba `calculo.py ca
    # --clase Monje`, que desde entonces sale con error a propósito— y el
    # desfase vivió hasta que alguien lo ejecutó a mano. Esto comprueba que los
    # scripts y subcomandos que las skills mandan usar **existen**.
    #
    # ⚠ LÍMITE, y conviene que conste: esto NO habría cazado aquella rotura.
    # `calculo.py ca --clase` existía y sus flags eran válidas; lo que falló fue
    # el resultado en tiempo de ejecución para 4 clases. Cazar eso pide correr
    # el comando con valores reales de cada clase, que es otro trabajo.
    fallos_antes_skills = fallos
    skills = sorted((B / ".claude/skills").glob("*/SKILL.md"))
    if not skills:
        print(" ⚠ no encuentro ninguna skill en .claude/skills/*/SKILL.md")
    ayudas = {}
    for sk in skills:
        txt = sk.read_text(encoding="utf-8")
        nombre = sk.parent.name
        # El `(?![\w/])` evita tomar por subcomando la primera parte de una
        # ruta: `verificar_personaje.py personajes/x.yaml` no lleva subcomando,
        # y la primera versión de este chequeo dio tres falsos positivos así.
        for m in re.finditer(
                r"python3 ([A-Za-z_0-9/]+\.py)((?:\s+[a-z][a-z0-9-]*(?![\w/.]))?)",
                txt):
            script, sub = m.group(1), m.group(2).strip()
            if not (B / script).exists():
                fallos += 1
                print(f" ❌ /{nombre} manda usar {script}, que no existe")
                continue
            if not sub or sub in ("-c",):
                continue
            if script not in ayudas:
                r = subprocess.run([sys.executable, script, "--help"], cwd=B,
                                   capture_output=True, text=True)
                ayudas[script] = r.stdout + r.stderr
            if sub not in ayudas[script]:
                fallos += 1
                print(f" ❌ /{nombre} manda `python3 {script} {sub}`, y {script} "
                      f"no conoce ese subcomando")
    if fallos == fallos_antes_skills:
        print(f" ✅ {len(skills)} skills · los scripts y subcomandos que mandan "
              f"usar existen todos")

    # 6. Ningún documento vivo debe remitir al FODA archivado como si valiera.
    for nombre in ("CONTINUAR.md", "FODA.md"):
        txt = (B / nombre).read_text(encoding="utf-8")
        for m in re.finditer(r"[^\n]*FODA_2026-08-19_OBSOLETO[^\n]*", txt):
            linea = m.group(0)
            if "OBSOLETO" in linea and ("archivad" in linea.lower()
                                        or "Sustituye" in linea
                                        or "⛔" in linea):
                continue
            fallos += 1
            print(f" ❌ {nombre} remite al FODA archivado sin marcarlo: "
                  f"«{linea.strip()[:70]}»")

    print("─" * 74)
    print("✅ los documentos de estado cuadran con la base"
          if not fallos else f"❌ {fallos} desfases entre documentos y realidad")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
