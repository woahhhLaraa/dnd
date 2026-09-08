#!/usr/bin/env python3
"""La deuda enumerada: una lista de lo conocido que solo puede menguar.

Fase 1 del `PLAN_21`. Este módulo no inventa nada: recoge lo que **cinco
ficheros de `_verificacion/` ya hacían por separado**, y les da lo que solo uno
de ellos tenía.

## De dónde sale, medido el 2026-09-06

| fichero | poda | nuevo ≠ perdido | guarda elenco | identidad |
|---|:--:|:--:|:--:|---|
| `chequeos_silenciosos.json` | sí | no | no | texto + condición + ordinal |
| `rasgos_sin_declarar.json` | **no** | no | no | `archivo#nombre` |
| `efectos_sin_carga.json` | sí | no | no | `efecto:archivo#rasgo·objetivo·op` |
| `motor_sin_carga.json` | sí | **sí** | **sí** | nombre de la función |
| `constantes_de_dominio.json` | sí | no | no | huella del conjunto |

`motor_sin_carga` es el único que aprendió las tres lecciones, y las aprendió
el último día y a golpes: primero guardaba FRASES —reescribir una descripción
hacía que el mismo hueco saliera como nuevo y la suite gritara «cobertura
perdida», que era falso—, y después no sabía distinguir «una prueba nueva mide
algo que nunca estuvo cubierto» de «algo que se cubría ha dejado de cubrirse».

Las otras cuatro no las tienen **porque se escribieron antes**. Ese es el
argumento entero de este módulo: no son cinco problemas, es una abstracción
escrita cinco veces, y las cuatro copias viejas se quedaron con los bugs que la
quinta ya arregló.

## Las cuatro cosas que un fichero de deuda tiene que saber hacer

1. **Podar.** Lo que se salda sale de la lista. Sin poda la deuda no baja nunca
   en disco, y algo que hoy está cubierto y mañana deja de estarlo vuelve a
   contar como «declarado» sin que nadie lo diga.
2. **Distinguir lo nuevo de lo perdido.** Una entrada que no estaba en la lista
   puede ser dos cosas muy distintas: una MEDICIÓN NUEVA —una prueba que antes
   no existía mide algo que nunca estuvo cubierto— o una REGRESIÓN —algo que se
   cubría ha dejado de cubrirse—. Solo la segunda es roja. Confundirlas es
   mentir en las dos direcciones.
3. **Guardar el elenco.** Sin la lista de TODO lo que se midió —no solo lo que
   falló— el punto 2 es indecidible.
4. **Declarar su identidad.** Con qué se compara una entrada con la de ayer. No
   se puede verificar sola, así que se escribe DENTRO del fichero: quien lo lea
   dentro de un año ve con qué regla se comparó. Las tres veces que este
   proyecto eligió mal la identidad —una frase, un número de línea, un cuerpo
   sin su condición— el verificador mintió.

## Lo que este módulo NO hace, a propósito

- **No junta los cinco ficheros en uno.** Cada uno tiene su dueño y su momento
  de escritura; un fichero común sería uno que nadie sabe quién escribe.
- **No cambia la identidad de ninguno al migrarlo.** Cambiarla invalida la
  línea base, que es exactamente la mentira que este plan persigue.
- **No decide si algo es deuda.** Eso lo sabe el llamador; aquí solo se
  contrasta contra lo que había.
- **No interpreta el valor de una entrada.** Cuatro de los cinco ficheros
  guardan `id → frase`; `constantes_de_dominio.json` guarda por entrada un
  objeto con `coleccion`, `clase`, `motivo` y `deja_fuera`, porque además de
  deuda es un manifiesto. Forzarlo a una frase le quitaría datos que el censo
  usa. Aquí el valor es OPACO: lo que este módulo lleva es la contabilidad
  —podar, distinguir lo nuevo de lo perdido, guardar el elenco, fijar la
  identidad—, no el significado.
"""
import json
import pathlib

B = pathlib.Path(__file__).resolve().parent


class Informe:
    """El resultado de contrastar lo medido hoy contra la línea base."""

    def __init__(self, vigentes, saldados, medidos_nuevos, perdidos, linea_base,
                 cerrada=False):
        self.vigentes = vigentes              # {id: desc} — deuda que sigue
        self.saldados = saldados              # {id: desc} — estaban y ya no
        self.medidos_nuevos = medidos_nuevos  # {id: desc} — nunca se midieron
        self.perdidos = perdidos              # {id: desc} — REGRESIÓN, rojo
        self.linea_base = linea_base          # cuántos había antes
        self.cerrada = cerrada                # ¿lo nunca medido también es rojo?

    @property
    def rojos(self):
        """Lo que hace fallar. En una deuda CERRADA, también lo medido por
        primera vez.

        **Esta propiedad existe porque su ausencia rompió un guardián el
        2026-09-06, el mismo día.** Al migrar `verificar_chequeos` a este
        módulo, «rama nueva» pasó a leerse como `perdidos`, y una rama
        silenciosa en código NUEVO —que nunca estuvo en el elenco— caía en
        `medidos_nuevos` y salía en verde. Antes de migrar era roja: cualquier
        huella que no estuviera en la línea base lo era. `mutaciones_silencios`
        lo cazó en la primera pasada, 3/6, con sus tres mutaciones.

        Distinguir lo nuevo de lo perdido es una MEDICIÓN, y la hacen todos.
        Si lo nuevo es aceptable o no es una POLÍTICA del fichero, y por eso se
        declara en el `Deuda`, junto a la identidad: `motor_sin_carga` acepta
        mediciones nuevas —una mutación nueva que nada caza es deuda nueva,
        no una regresión—, y `chequeos_silenciosos` no acepta ninguna.
        """
        if self.cerrada:
            return {**self.perdidos, **self.medidos_nuevos}
        return dict(self.perdidos)

    @property
    def hay_regresion(self):
        return bool(self.rojos)

    def imprimir(self, titulo="", sangria=" ", texto=None, vigentes=True):
        """La salida que los cinco llamadores imprimían por su cuenta, una vez.

        El orden importa y es el que ya usaban: primero lo que sigue en deuda
        —una deuda que no se ve en el informe es una deuda que nadie salda—,
        luego lo saldado, luego lo nuevo medido, y el rojo al final.

        `texto(uid, valor)` traduce una entrada a una línea. Existe porque el
        valor es opaco: una frase en cuatro ficheros, un objeto en el quinto.

        `vigentes=False` para quien ya imprime la deuda por su cuenta —caso de
        `verificar_chequeos`, que lista cada rama con su fichero y su línea—:
        repetirla aquí sería decir dos veces lo mismo.
        """
        di = texto or (lambda uid, val: str(val))
        if vigentes and self.vigentes:
            print(f"{sangria}{titulo}")
            for uid, val in sorted(self.vigentes.items()):
                print(f"{sangria}   · {di(uid, val)}")
        if self.saldados:
            print(f"\n{sangria}✅ {len(self.saldados)} saldada(s) y fuera de la deuda:")
            for uid, val in sorted(self.saldados.items()):
                print(f"{sangria}      · {di(uid, val)}")
        for uid, val in sorted(self.medidos_nuevos.items()):
            if self.cerrada:
                print(f"{sangria}🔴 NUEVA, y esta lista no admite nada nuevo:"
                      f"\n{sangria}      {di(uid, val)}")
            else:
                print(f"{sangria}ℹ medido por una prueba NUEVA (no es una "
                      f"regresión):\n{sangria}      {di(uid, val)}")
        for uid, val in sorted(self.perdidos.items()):
            print(f"{sangria}🔴 REGRESIÓN: estaba cubierto y ya no:"
                  f"\n{sangria}      {di(uid, val)}")


class Deuda:
    """Un fichero de deuda enumerada, con su línea base en disco.

    `identidad` es una CLAVE CORTA Y ESTABLE («nombre-de-funcion»,
    «huella-del-conjunto»), no una frase. La explicación va aparte, en
    `identidad_explicada`, y se guarda también en el fichero para quien lo lea
    dentro de un año.

    **Esa separación no es cosmética, y se aprendió aquí mismo.** La primera
    versión de este módulo comparaba la PROSA byte a byte, y saltó contra su
    propio autor a los diez minutos: al migrar `motor_sin_carga.json` la frase
    tenía siete palabras más que en el llamador, y el módulo declaró que la
    línea base ya no significaba lo mismo. O sea: escribí como identidad una
    frase, que es exactamente el defecto que este módulo existe para impedir
    —`motor_sin_carga` guardaba frases y llamaba «cobertura perdida» a una
    descripción reescrita—. La clave corta se compara; la prosa se lee.
    """

    def __init__(self, fichero, nota, como_se_salda, identidad,
                 identidad_explicada="", fecha="2026-09-06", cerrada=False):
        self.ruta = B / fichero
        self.nota = nota
        self.como_se_salda = como_se_salda
        self.identidad = identidad
        self.identidad_explicada = identidad_explicada
        self.fecha = fecha
        # `cerrada`: ¿una entrada medida por primera vez también es roja?
        # Es una política del fichero, no una medición — ver `Informe.rojos`.
        self.cerrada = cerrada

    # ── lectura ──────────────────────────────────────────────────────────
    def _leer(self):
        if not self.ruta.exists():
            return None
        d = json.loads(self.ruta.read_text(encoding="utf-8"))
        previa = d.get("_identidad")
        if previa is not None and previa != self.identidad:
            raise ValueError(
                f"{self.ruta.name} se escribió con la identidad «{previa}» y "
                f"ahora se le pide «{self.identidad}». La línea base ya no "
                f"significa lo mismo: migra el fichero a conciencia y di en su "
                f"`_migracion` qué era cada cosa, no lo compares a ciegas.")
        return d

    @property
    def vigentes(self):
        """Los ids de la línea base, para quien solo quiera leerla."""
        d = self._leer()
        return dict((d or {}).get("entradas") or {})

    # ── contraste ────────────────────────────────────────────────────────
    def contrastar(self, medido_hoy, elenco_hoy=None, podar=True):
        """Contrasta `{id: descripción}` contra la línea base y la actualiza.

        `elenco_hoy` es TODO lo que se midió, falle o no. Sin él no se puede
        distinguir una medición nueva de una regresión, y este módulo prefiere
        decir «no lo sé» a llamar regresión a lo primero: sin elenco, nada
        cuenta como perdido.
        """
        d = self._leer()
        if d is None:
            self._escribir(medido_hoy, elenco_hoy)
            return Informe(dict(medido_hoy), {}, {}, {}, len(medido_hoy),
                           cerrada=self.cerrada)

        base = dict(d.get("entradas") or {})
        elenco_previo = set(d.get("elenco") or ())

        vigentes = {k: v for k, v in medido_hoy.items() if k in base}
        saldados = {k: base[k] for k in base if k not in medido_hoy}
        fuera_de_base = {k: v for k, v in medido_hoy.items() if k not in base}

        if elenco_previo:
            # Con elenco: lo que ya se medía y NO era deuda y hoy sí lo es, es
            # una regresión. Lo que nunca se midió es una medición nueva.
            perdidos = {k: v for k, v in fuera_de_base.items()
                        if k in elenco_previo}
            medidos_nuevos = {k: v for k, v in fuera_de_base.items()
                              if k not in elenco_previo}
        else:
            # Sin elenco previo —fichero de antes de este módulo— no hay forma
            # de saberlo, y llamar regresión a todo sería el error que
            # `mutaciones_motor` cometió. Se cuentan como regresión igual,
            # porque es la lectura conservadora de una línea base que solo
            # puede bajar, pero se dice de dónde viene la duda.
            perdidos, medidos_nuevos = fuera_de_base, {}

        # Se escribe siempre que el fichero resultante sea DISTINTO del que
        # hay: lo decide `_escribir` comparando el texto, no una condición
        # aquí. La condición escrita a mano ya falló una vez —era `saldados or
        # fuera_de_base`, y un elenco que crecía sin que la deuda se moviera no
        # llegaba nunca al disco, así que la pasada siguiente no podía
        # distinguir una medición nueva de una regresión—; se le añadió
        # `elenco_cambia` y seguía sin cubrir el tercer caso, la prosa. Una
        # lista de «cuándo hay que escribir» es justo lo que este proyecto
        # tiene prohibido: se descubre comparando, no se enumera.
        if podar:
            self._escribir({**vigentes, **fuera_de_base}, elenco_hoy,
                           saldados=saldados, previo=d)
        return Informe(vigentes, saldados, medidos_nuevos, perdidos,
                       len(base), cerrada=self.cerrada)

    # ── escritura ────────────────────────────────────────────────────────
    def _escribir(self, entradas, elenco, saldados=None, previo=None):
        # `or`, no `.get(clave, defecto)`: una prosa VACÍA en el disco no puede
        # ganarle a la del código. El guion que migró los cinco ficheros los
        # escribió con la prosa en blanco, y como el disco mandaba siempre,
        # `_como_se_salda` se quedó vacío en TRES de los cinco —el campo que
        # dice cómo se paga una deuda— sin forma de repararlo desde el
        # llamador, que sí lo tenía escrito. Editar la prosa a mano sigue
        # mandando: lo que no manda es no haberla escrito.
        doc = {
            "_nota": (previo or {}).get("_nota") or self.nota,
            "_como_se_salda": ((previo or {}).get("_como_se_salda")
                               or self.como_se_salda),
            "_identidad": self.identidad,
            "_identidad_explicada": (self.identidad_explicada
                                     or (previo or {}).get("_identidad_explicada")
                                     or ""),
            "_fecha": self.fecha,
        }
        # La prosa que cada fichero trae de suyo —`_migracion`,
        # `_por_que_una_lista_y_no_un_comodin`, `_umbral`…— se conserva
        # DESCUBRIÉNDOLA, no por una lista de claves escrita aquí. La primera
        # versión llevaba esa lista, y ya se había quedado corta el día que se
        # escribió: `motor_sin_carga.json` traía `_migracion_plan21`, que no
        # estaba en ella, así que la explicación de su propia migración se
        # habría borrado en la primera poda. Es la regla inviolable 6 —«la
        # cobertura se descubre, nunca se escribe a mano»— dentro del módulo
        # que existe para que las listas no se queden atrás.
        propias = set(doc) | {"_ultima_poda"}
        for k, v in (previo or {}).items():
            if k.startswith("_") and k not in propias:
                doc[k] = v
        if saldados:
            doc["_ultima_poda"] = {"fecha": self.fecha,
                                   "saldados": sorted(saldados.values())}
        elif previo and "_ultima_poda" in previo:
            doc["_ultima_poda"] = previo["_ultima_poda"]
        doc["entradas"] = dict(sorted(entradas.items()))
        if elenco is not None:
            doc["elenco"] = sorted(elenco)
        elif previo and "elenco" in previo:
            doc["elenco"] = previo["elenco"]

        # Comparación por TEXTO, no por diccionario: así una reescritura que
        # solo cambia el ORDEN de las claves también se hace, y los cinco
        # ficheros convergen a la misma forma. `motor_sin_carga.json` llevaba
        # su `_identidad_explicada` al final, detrás de `elenco`, porque lo
        # escribió una versión anterior de este método y nada volvió a tocarlo.
        texto = json.dumps(doc, ensure_ascii=False, indent=1)
        if self.ruta.exists() and texto == self.ruta.read_text(encoding="utf-8"):
            return False
        self.ruta.write_text(texto, encoding="utf-8")
        return True
