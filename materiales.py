#!/usr/bin/env python3
"""El componente material de un conjuro, descompuesto (Fase 14b-2).

`componentes.coste` era un solo string, y por eso la base guardó **cuatro
sumas que ninguna página imprime**: *Vínculo protector* «100 po» por un par de
anillos de 50 «cada uno», *Cofre oculto de Leomund* «5050 po», *Proyección
astral* «1100 po» (1000 + 100) y *Conocer las leyendas* «200 po» (4 × 50). Es
el modo de fallo nº 10 del proyecto —«dato agregado»—: no falta texto ni sobra,
ni hay ninguna cifra «mal»; alguien **hizo una operación y guardó el
resultado**, perdiendo el desglose. Invisible a cualquier chequeo de forma.

Ahora la verdad vive en `componentes.materiales`, una lista, y `coste` y
`consume_material` **se derivan** de ella. Este módulo es la única
implementación de esa derivación, para que `validar.py` y `verificar_foundry.py`
no puedan discrepar entre sí.

Campos de un material:

    nombre    obligatorio, como lo llama la página
    coste     entero, sin la unidad
    unidad    po | pp | pc
    consume   bool — **por material**: en *Clon* se consume el diamante y no el
              recipiente, y el `consume_material` único no podía decirlo
    cantidad  opcional, cuántas unidades pide la página ("cuatro tiras")
    por       opcional, la expresión literal de precio por unidad
              ("cada cadáver", "cada objetivo del conjuro", "cada uno")
"""
UNIDADES = ("po", "pp", "pc")


def render_coste(materiales):
    """La forma canónica de `coste` a partir de la lista.

    Es una función y no un campo escrito a mano a propósito: escribir el total
    al lado de las partes es exactamente lo que produjo las cuatro sumas.
    `validar.py` comprueba que el `coste` guardado sea IDÉNTICO a lo que
    devuelve esto — un round-trip que demuestra que no se perdió ni se inventó
    nada al descomponer.
    """
    if not materiales:
        return None

    def una(m):
        s = f"{m['coste']} {m['unidad']}"
        if m.get("cantidad"):
            s = f"{m['cantidad']}× {s}"
        if m.get("consume"):
            s += " (se consume)"
        return s

    pors = {m.get("por") for m in materiales}
    cuerpo = " + ".join(una(m) for m in materiales)
    if len(pors) == 1 and (p := pors.pop()):
        # El «por cada objetivo» de *Proyección astral* rige los dos materiales:
        # la página lo dice una vez, delante, y así se conserva.
        return f"por {p}: {cuerpo}"
    partes = []
    for m in materiales:
        s = una(m)
        if m.get("por"):
            s += f" por {m['por']}"
        partes.append(s)
    return " + ".join(partes)


def consume_material(materiales):
    """El booleano único que la base ya tenía, derivado.

    Se conserva porque el SRD también publica un solo `consumed` por conjuro y
    es contra eso contra lo que se contrasta. **Es una simplificación con
    pérdida, y por eso ya no es la fuente**: la verdad es `consume` por
    material.
    """
    return any(m.get("consume") for m in materiales)
