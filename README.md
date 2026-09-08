# Base canónica de D&D 2024 (5.5e) en castellano

Base de datos de reglas transcrita del **Manual del Jugador 2024** por lectura
visual de sus páginas, pensada para que un LLM orquestador cree y suba de nivel
personajes **sin usar nada de su conocimiento previo**.

> **Empieza por [`CONTINUAR.md`](CONTINUAR.md).** Todo el estado vive en disco:
> no depende de ninguna conversación previa.

## La idea

El modelo sabe D&D 2014, y varias reglas cambiaron en 2024 (las maestrías de
arma no existían). Si rellena huecos de memoria produce reglas que **suenan bien
y no existen**. Por eso toda autoridad vive en la base, citada por página, y el
conocimiento previo está vetado.

De ahí las reglas del proyecto: *consultar, no recordar*; *citar siempre*; y
*decir «no lo tengo»* antes que rellenar.

Y una sexta, aprendida a golpes el 2026-08-31: **la cobertura se descubre, no
se escribe a mano.** Ningún módulo lleva dentro la lista de ficheros que mira;
la descubre por patrón y la contrasta con un manifiesto que declara también
las exclusiones. Verificar que lo escrito es correcto no dice nada de lo que
falta — y lo que faltaba hacía que el verificador **aprobara la ficha mal y
rechazara la buena**. Detalle en `PLAN_17_SALIR_DEL_ESPIRAL.md`.

Desde el 2026-09-02 esa sexta regla **la comprueba `censo.py`**, y no es prosa:
enumera siete clases de unidad de la base y exige que cada una esté alcanzada
por algún chequeo o declarada, con su motivo, en
`_verificacion/censo_exenciones.yaml`. Su número solo puede bajar.

Y la puerta está cerrada por el otro lado: **todo rasgo tiene que decir si toca
alguna variable calculable**, con `efectos:` o con `no_automatizado:` y su
motivo. Los que todavía no lo dicen van enumerados uno a uno, no tapados por un
comodín, así que uno nuevo que se calle hace fallar a `validar.py`.

## Comprobar que está sana

```bash
python3 validar.py            # coherencia interna
python3 verificar_srd.py      # contraste externo contra el SRD 5.2
python3 verificar_foundry.py  # contraste externo, SRD estructurado
python3 cobertura.py          # ¿sabe responder?
for f in personajes/*.yaml; do python3 verificar_personaje.py "$f"; done
python3 verificar_documentos.py   # ¿los documentos dicen la verdad?
python3 verificar_chequeos.py     # ¿algún chequeo calla lo que no comprueba?
python3 censo.py                  # ¿queda alguna unidad sin ningún chequeo detrás?
python3 generar_ficha.py --barrido --exhaustivo   # 12 clases × 20 niveles
```

Y las pruebas por mutación de `_verificacion/`, que son lo que da derecho a
fiarse de lo anterior: **un validador que nunca ha visto un dato malo no
demuestra nada.**

## Documentos

| Fichero | Qué es |
|---|---|
| `CONTINUAR.md` | El punto de reanudación: qué hay, qué falta, con qué cifras |
| `FUENTES.md` | Procedencia y **todas** las correcciones, con su método y sus errores |
| `FODA.md` | Fortalezas, debilidades y amenazas vigentes |
| `PLAN_19_PRODUCTO_COMPLETO.md` | **El plan vigente**: qué falta para el producto completo y qué logra cada fase |
| `PLAN_*.md` | Un plan por fase, con las cifras medidas y el resultado al cerrarla |

## Legal

Transcripción de material con copyright, **para uso personal**. Lo único
redistribuible es el SRD 5.2 (CC-BY-4.0) que vive en `_verificacion/`, incluido
para que los contrastes externos sean reproducibles.
