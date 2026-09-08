#!/usr/bin/env python3
"""Prueba por mutación del muro (`informar.py`, fase 2 del PLAN_21).

«Un chequeo explota en vez de informar» apareció TRES VECES EN DOS DÍAS en este
repositorio, y las tres se arreglaron una a una hasta que la tercera se cerró
para `validar.py` entero con `_correr()`. Ahí se quedó: en un módulo. Los otros
siete seguían igual, y en varios el daño era peor que perder el informe —se
perdía además la CIFRA que `verificar_documentos.py` ancla contra los
documentos, y una cifra que no sale no se puede contrastar con nada—.

Esta suite mide lo único que el muro promete: **un chequeo que revienta sale en
rojo, con su nombre, y los demás siguen**. Para eso inyecta un `raise` en UN
chequeo de cada script y exige las tres cosas a la vez:

  1. el proceso NO muere sin decir nada (hay informe),
  2. el chequeo roto sale nombrado y en rojo,
  3. el resto del informe sigue estando —lo que se mide es que el script
     imprima su línea de cierre, la que da la cuenta—.

Y tres controles negativos, que son la mitad del valor:

  · un `sys.exit` legítimo —un dato que falta en la BASE— tiene que seguir
    parando el proceso. Un muro que se lo tragara convertiría un fallo grave en
    una línea de error entre otras, y eso es peor que no tener muro
    (`PLAN_21`, «lo que NO hay que hacer» nº 4);
  · el mismo `sys.exit`, pero en `verificar_personaje`, NO puede parar: allí lo
    que se examina es la ficha, no la base, y la salida es un veredicto sobre
    la entrada bajo examen. Es el único sitio donde se declara, y por eso el
    control va en las dos direcciones;
  · una fuente que revienta en `verificar_chequeos` NO puede PODAR la línea
    base. Este es el peligro que el muro trae consigo y que no estaba en el
    plan: si un fichero deja de medirse y su chequeo simplemente «sigue», la
    poda da sus ramas por saldadas y **la deuda baja sola, en verde**.

    python3 _verificacion/mutaciones_muro.py
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
REVIENTA = 'raise TypeError("mutación: este chequeo revienta")\n'


def _sust(raiz, rel, viejo, nuevo, cuenta=1):
    p = raiz / rel
    t = p.read_text(encoding="utf-8")
    assert viejo in t, f"la mutación no encaja en {rel}: {viejo[:70]!r}"
    p.write_text(t.replace(viejo, nuevo, cuenta), encoding="utf-8")


def _corre(raiz, *cmd):
    r = subprocess.run([sys.executable, *cmd], cwd=raiz,
                       capture_output=True, text=True, timeout=2400)
    return r.returncode, r.stdout + r.stderr


# ══ Un `raise` en un chequeo de cada script ══════════════════════════════
# Cada entrada dice: dónde se inyecta, cómo se corre, qué tiene que salir
# nombrado, y qué línea del informe tiene que SEGUIR saliendo. Lo último es lo
# que separa «no ha muerto» de «el informe sobrevive».

CASOS = [
    {
        "nombre": "validar.py",
        "muta": lambda r: _sust(r, "validar.py", "def validar_dados():\n",
                                "def validar_dados():\n    " + REVIENTA),
        "cmd": ("validar.py",),
        "nombra": "validar_dados",
        "sigue": "referencias",
    },
    {
        "nombre": "censo.py · una fila",
        "muta": lambda r: _sust(r, "censo.py", "def fila_rasgos():\n",
                                "def fila_rasgos():\n    " + REVIENTA),
        "cmd": ("censo.py",),
        "nombra": "fila_rasgos",
        # Las otras ocho filas siguen contando: la línea de cierre sale.
        "sigue": "unidades censadas",
    },
    {
        "nombre": "verificar_chequeos.py · una fuente",
        "muta": lambda r: _sust(r, "verificar_chequeos.py",
                                "    lineas = p.read_text(encoding=\"utf-8\").splitlines()\n"
                                "    arbol = ast.parse",
                                "    lineas = p.read_text(encoding=\"utf-8\").splitlines()\n"
                                "    if rel == 'validar.py':\n        " + REVIENTA
                                + "    arbol = ast.parse"),
        "cmd": ("verificar_chequeos.py",),
        "nombra": "validar.py",
        "sigue": "silenciosas",
    },
    {
        "nombre": "verificar_srd.py · una clase",
        "muta": lambda r: _sust(r, "verificar_srd.py",
                                "    nuestro, lanz = leer_nuestro(p)\n",
                                "    if arch == 'mago':\n        " + REVIENTA
                                + "    nuestro, lanz = leer_nuestro(p)\n"),
        "cmd": ("verificar_srd.py",),
        "nombra": "mago",
        "sigue": "valores contrastados contra el SRD",
    },
    {
        "nombre": "verificar_personaje.py · un chequeo",
        "muta": lambda r: _sust(r, "verificar_personaje.py",
                                "def verificar_idiomas(",
                                "def verificar_idiomas(*_a, **_k):\n    " + REVIENTA
                                + "\n\ndef _verificar_idiomas_original("),
        "cmd": ("verificar_personaje.py", "personajes/aasimar_clerigo.yaml"),
        "nombra": "verificar_idiomas",
        "sigue": "referencias comprobadas",
    },
    {
        "nombre": "cobertura.py · un bloque",
        "muta": lambda r: _sust(r, "cobertura.py", "def cobertura_especies(",
                                "def cobertura_especies(*_a, **_k):\n    " + REVIENTA
                                + "\n\ndef _cobertura_especies_original("),
        "cmd": ("cobertura.py",),
        "nombra": "cobertura_especies",
        "sigue": "COBERTURA",
    },
    {
        "nombre": "verificar_foundry.py · un módulo",
        "muta": lambda r: _sust(r, "verificar_foundry.py",
                                "        inf, fallo = _I.muro(MODULOS[p], etiqueta=p)",
                                "        if p == sorted(MODULOS)[0]:\n"
                                "            def _revienta(): " + REVIENTA
                                + "            MODULOS[p] = _revienta\n"
                                "        inf, fallo = _I.muro(MODULOS[p], etiqueta=p)"),
        "cmd": ("verificar_foundry.py",),
        "nombra": "no se ha podido contrastar",
        "sigue": "valores contrastados ·",
    },
]


# ══ El muro mismo: mutar `informar.py`, no solo a sus usuarios ═══════════
# La fila 10 del censo (fase 3 del `PLAN_21`) lo destapó el mismo día que se
# escribió: esta suite mutaba los SIETE scripts y ni una línea de `informar.py`.
# O sea que el módulo que existe para que un fallo no se pierda podía perder
# fallos él mismo, en verde. Es literalmente el guardián sin guardián que la
# fila cuenta, dentro de la fase que la escribió.
#
# Cada mutación rompe UNA de las tres cosas que `muro` promete, y se exige que
# el efecto se vea desde fuera, en un script real.

MUROS_ROTOS = [
    {
        "nombre": "`muro` deja de capturar: el fallo vuelve a matar al informe",
        "muta": lambda r: _sust(r, "informar.py",
                                "    except Exception as e:                                   # noqa: BLE001\n"
                                "        return None, Fallo(etiqueta or _etiqueta_de(fn), e)",
                                "    except Exception:                                        # noqa: BLE001\n"
                                "        raise"),
        # Se mira en `censo.py`: con el muro roto, una fila que revienta se
        # lleva el recuento entero, que es lo que pasaba antes de la fase 2.
        "prepara": lambda r: _sust(r, "censo.py", "def fila_rasgos():\n",
                                   "def fila_rasgos():\n    " + REVIENTA),
        "cmd": ("censo.py",),
        "no_sale": "unidades censadas",
    },
    {
        "nombre": "`muro` se traga el `sys.exit`: un dato que falta deja de parar",
        "muta": lambda r: _sust(r, "informar.py",
                                "        if not salida_es_veredicto:\n            raise",
                                "        if False:\n            raise"),
        "prepara": lambda r: _sust(
            r, "validar.py", "def validar_dados():\n",
            "def validar_dados():\n"
            "    sys.exit('falta un dato de la base: esto tiene que parar')\n"),
        "cmd": ("validar.py",),
        # Lo observable NO es que `validar.py` acabe en verde —no lo hace: el
        # muro convierte la salida en un error y sigue habiendo rojo—, sino
        # **que siga corriendo**. Con la salida propagándose, `validar.py`
        # muere en `validar_dados` y los chequeos de después no llegan a
        # ejecutarse: «referencias» no aparece. Con el muro roto aparece, y el
        # dato que falta queda como «❌ 1 errores», una línea entre otras.
        # Es justo lo que el `PLAN_21` prohíbe en su punto 4.
        #
        # La primera versión de esta mutación esperaba que empezara a salir
        # «BASE VALIDADA» y NO SE DETECTABA: en los siete sitios donde el muro
        # está puesto, un `Fallo` siempre acaba en rojo, así que tragarse la
        # salida no cambiaba el veredicto. Es la tercera vez en este proyecto
        # que una mutación no cambia nada porque **solo cambiaría el
        # comportamiento en una situación que no ocurre**; se le cambia el
        # vehículo, no se borra.
        "sale": "referencias",
    },
    {
        "nombre": "`Fallo` pierde la etiqueta: el informe no dice QUIÉN reventó",
        "muta": lambda r: _sust(r, "informar.py",
                                '        return f"{self.etiqueta}: {self.motivo}"',
                                '        return f"{self.motivo}"'),
        "prepara": lambda r: _sust(r, "verificar_personaje.py",
                                   "def verificar_idiomas(",
                                   "def verificar_idiomas(*_a, **_k):\n    " + REVIENTA
                                   + "\n\ndef _verificar_idiomas_original("),
        "cmd": ("verificar_personaje.py", "personajes/aasimar_clerigo.yaml"),
        "no_sale": "verificar_idiomas",
    },
]


# ══ Controles negativos ══════════════════════════════════════════════════

def n_salida_legitima_para(raiz):
    """Un dato que falta en la BASE tiene que seguir parando `validar.py`."""
    _sust(raiz, "validar.py", "def validar_dados():\n",
          "def validar_dados():\n"
          "    sys.exit('falta un dato de la base: esto tiene que parar')\n")
    codigo, salida = _corre(raiz, "validar.py")
    # PARA DE VERDAD: el proceso muere ahí y los chequeos de después no llegan
    # a correr. Comprobar solo que no sale «BASE VALIDADA» no distinguía nada
    # —con el muro roto tampoco sale, porque la salida se cuenta como error—,
    # así que este control pasaba en verde con la propiedad rota. Lo destapó su
    # propia mutación, `m_muro_se_traga_la_salida`.
    paro = (codigo != 0 and "BASE VALIDADA" not in salida
            and "referencias" not in salida)
    return paro, ("un `sys.exit` desde un chequeo de `validar.py` PARA el "
                  "proceso ahí mismo: los chequeos de después no llegan a "
                  "correr, y el dato que falta no queda como una línea más")


def n_salida_es_veredicto_en_personaje(raiz):
    """El único sitio donde una salida SÍ se captura, y con motivo: allí lo
    que se examina es la ficha, no la base."""
    _sust(raiz, "verificar_personaje.py", "def verificar_idiomas(",
          "def verificar_idiomas(*_a, **_k):\n"
          "    sys.exit('la ficha trae un pg_por_nivel roto')\n"
          "\n\ndef _verificar_idiomas_original(")
    codigo, salida = _corre(raiz, "verificar_personaje.py",
                            "personajes/aasimar_clerigo.yaml")
    # Rechaza la ficha, pero HABLANDO: el informe sale y nombra el chequeo.
    ok = (codigo != 0 and "verificar_idiomas" in salida
          and "referencias comprobadas" in salida)
    return ok, ("una salida en `verificar_personaje` es un veredicto sobre la "
                "FICHA, no un dato que falte: se cuenta como error y el resto "
                "del informe sigue saliendo")


def n_fuente_rota_no_poda(raiz):
    """El peligro que el muro trae consigo: un chequeo que no se puede medir
    no puede convertirse en deuda saldada."""
    fichero = raiz / "_verificacion" / "chequeos_silenciosos.json"
    antes = len(json.loads(fichero.read_text(encoding="utf-8"))["entradas"])
    _sust(raiz, "verificar_chequeos.py",
          "    lineas = p.read_text(encoding=\"utf-8\").splitlines()\n"
          "    arbol = ast.parse",
          "    lineas = p.read_text(encoding=\"utf-8\").splitlines()\n"
          "    if rel == 'validar.py':\n        " + REVIENTA
          + "    arbol = ast.parse")
    _corre(raiz, "verificar_chequeos.py")
    despues = len(json.loads(fichero.read_text(encoding="utf-8"))["entradas"])
    return despues == antes, (
        f"una fuente que revienta NO poda la línea base: seguía en {antes} "
        f"entradas y sigue en {despues}, en vez de dar por saldadas las ramas "
        f"que no se han podido mirar")


NEGATIVOS = [n_salida_legitima_para, n_salida_es_veredicto_en_personaje,
             n_fuente_rota_no_poda]


def _copia(tmp):
    raiz = pathlib.Path(tmp) / "base"
    shutil.copytree(BASE, raiz, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    return raiz


def main():
    print(__doc__.splitlines()[0])
    print("═" * 74)

    ok = 0
    total = len(CASOS) + len(MUROS_ROTOS) + len(NEGATIVOS)

    print("\n Un `raise` en un chequeo: el informe TIENE que seguir saliendo")
    for caso in CASOS:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            caso["muta"](raiz)
            codigo, salida = _corre(raiz, *caso["cmd"])
            nombra = caso["nombra"] in salida
            sigue = caso["sigue"] in salida
            rojo = codigo != 0
            bien = nombra and sigue and rojo
            ok += bien
            print(f"   {'✅' if bien else '❌'} {caso['nombre']}")
            if not bien:
                falta = []
                if not rojo:
                    falta.append("no sale en rojo: el fallo se ha tragado")
                if not nombra:
                    falta.append(f"no nombra «{caso['nombra']}»")
                if not sigue:
                    falta.append(f"el informe NO sobrevive: falta "
                                 f"«{caso['sigue']}»")
                for f in falta:
                    print(f"        ↑ {f}")
                print(f"        últimas líneas: "
                      f"{' / '.join(salida.strip().splitlines()[-3:])[:200]}")

    print("\n Romper el muro MISMO: el efecto tiene que verse desde fuera")
    for caso in MUROS_ROTOS:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            caso["prepara"](raiz)
            # Control: con el muro intacto, el escenario se comporta como debe.
            _c0, antes = _corre(raiz, *caso["cmd"])
            caso["muta"](raiz)
            _c1, despues = _corre(raiz, *caso["cmd"])
            if "no_sale" in caso:
                bien = caso["no_sale"] in antes and caso["no_sale"] not in despues
                pista = f"«{caso['no_sale']}» tiene que dejar de salir"
            else:
                bien = caso["sale"] not in antes and caso["sale"] in despues
                pista = f"«{caso['sale']}» tiene que empezar a salir"
            ok += bien
            print(f"   {'✅' if bien else '❌'} {caso['nombre']}")
            if not bien:
                print(f"        ↑ NO DETECTADA — {pista}, y no cambia nada")

    print("\n Controles negativos")
    for neg in NEGATIVOS:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = _copia(tmp)
            bien, desc = neg(raiz)
            ok += bien
            print(f"   {'✅' if bien else '❌'} {desc}")

    print("\n" + "═" * 74)
    print(f"{'✅' if ok == total else '❌'} {ok}/{total}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
