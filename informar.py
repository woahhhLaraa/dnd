#!/usr/bin/env python3
"""El muro: un chequeo que revienta HABLA, no mata al informe.

Fase 2 del `PLAN_21`. Como `deuda.py`, este módulo no inventa nada: recoge lo
que `validar.py` ya hacía y lo pone donde puedan usarlo los seis verificadores
que hoy no lo tienen.

## El defecto, medido

«Un chequeo explota en vez de informar» apareció **tres veces en dos días**:

1. el hueco nº 10 de la ronda 2 de estrés —una ficha sin `caracteristicas`
   moría con un `KeyError` en `buscar.py` **sin imprimir una sola línea**:
   rechazaba, sí, pero no decía qué faltaba;
2. el `KeyError` de `validar_conjuros_cd`, introducido el mismo día que se
   cerró la fase 1.4 del `PLAN_20`;
3. `operaciones_agregadas()`, que al detectar una operación sin consumidor
   levantaba `ErrorDeEfectos` desde dentro de otro chequeo y se llevaba por
   delante el informe entero.

La tercera vez se cerró con `validar._correr()`, y ahí se quedó: **en un solo
módulo**. El 2026-09-06, al medirlo para este plan, el reparto era este:

| script | unidad de chequeo | qué se pierde hoy si una revienta |
|---|---|---|
| `validar.py` | un `validar_*` | nada: tiene muro desde el 2026-09-06 |
| `verificar_personaje.py` | un `verificar_*` | solo `KeyError` y `SystemExit` |
| `censo.py` | una fila (9) | las NUEVE, y el recuento que anclan los documentos |
| `verificar_chequeos.py` | un fichero fuente (17) | todo, y además puede PODAR en falso |
| `verificar_srd.py` | una clase (12) | las doce, y la cifra de 646 |
| `verificar_foundry.py` | un módulo | todos, y la cifra de 3749 |
| `verificar_documentos.py` | un bloque de cifras | todo |
| `cobertura.py` | un bloque (5) | los cinco |

## Lo que el muro NO hace: tragarse un `sys.exit`

Un `sys.exit` en este repositorio significa **falta un dato en la base**, y eso
tiene que seguir parando el proceso: convertirlo en una línea de error entre
otras es cómo se pierde un fallo grave. Por eso `muro` deja pasar `SystemExit`
salvo que el llamador lo declare, y solo hay un sitio donde declararlo tiene
sentido —`verificar_personaje`—, con este motivo:

> allí lo que se está examinando es la FICHA, no la base. Cuando `calculo`
> hace `sys.exit` sobre una ficha con un `pg_por_nivel` roto, esa salida es un
> **veredicto sobre la entrada bajo examen**, no un dato que falte. La ficha 3
> del agente B declaraba CINCO defectos y solo se veía UNO: un verificador que
> enseña el primer problema y calla los otros cuatro obliga a iterar a ciegas.

Así que el parámetro se llama `salida_es_veredicto` y no `capturar_salidas`:
el nombre tiene que decir por qué, no qué.

## Lo que el muro tampoco hace: convertir un fallo en una deuda saldada

Este es el peligro NUEVO que el muro trae consigo, y no estaba en el plan: lo
destapó medir `verificar_chequeos` antes de tocarlo. Varios de estos scripts
alimentan una línea base de `deuda.py`, y `Deuda.contrastar` PODA lo que hoy no
se mide. Si un fichero fuente revienta y su chequeo simplemente «sigue», sus
ramas dejan de medirse y la poda las da por saldadas: **la deuda baja sola y en
verde**, que es justo la mentira contra la que existe la línea base.

El muro no puede decidir eso —no sabe qué alimenta cada chequeo—, así que lo
decide el llamador: quien mida para una deuda y pierda una unidad, contrasta
con `podar=False` y lo dice. `muro` solo le da la manera de enterarse.

    from informar import muro
    valor, fallo = muro(fila_rasgos)
    if fallo:
        print(f" ❌ {fallo}")
"""


class Fallo:
    """Lo que le pasó a un chequeo que no llegó al final.

    Lleva la etiqueta separada del motivo a propósito: `validar.py` ya imprime
    el nombre del chequeo en su propia columna y repetirlo sería decir dos
    veces lo mismo, mientras que `verificar_personaje` mete el error en una
    lista plana y necesita el nombre dentro de la frase.
    """

    def __init__(self, etiqueta, excepcion):
        self.etiqueta = etiqueta
        self.excepcion = excepcion
        self.tipo = type(excepcion).__name__
        self.mensaje = str(excepcion)
        self.es_salida = isinstance(excepcion, SystemExit)

    @property
    def motivo(self):
        if self.es_salida:
            return f"paró en seco: {self.mensaje}"
        return f"reventó en vez de informar: {self.tipo}: {self.mensaje}"

    def __str__(self):
        return f"{self.etiqueta}: {self.motivo}"


def _etiqueta_de(fn):
    return getattr(fn, "__name__", None) or "chequeo"


def muro(fn, *args, etiqueta=None, salida_es_veredicto=False, **kwargs):
    """Corre `fn` y devuelve `(valor, fallo)`; `fallo` es `None` si fue bien.

    `KeyboardInterrupt` y el resto de `BaseException` NO se capturan: `except
    Exception` no los alcanza, y eso es lo correcto —quien pulsa Ctrl-C quiere
    parar, no leer un informe—.

    `salida_es_veredicto` captura también `SystemExit`. Léase el encabezado del
    módulo antes de ponerlo a `True`: solo hay un llamador donde es cierto.
    """
    try:
        return fn(*args, **kwargs), None
    except SystemExit as e:
        if not salida_es_veredicto:
            raise
        return None, Fallo(etiqueta or _etiqueta_de(fn), e)
    except Exception as e:                                   # noqa: BLE001
        return None, Fallo(etiqueta or _etiqueta_de(fn), e)
