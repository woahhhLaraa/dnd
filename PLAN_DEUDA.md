# ✅ Plan — saldar la deuda declarada — **EJECUTADO (2026-08-30)**

> Escrito el **2026-08-30**, con las deudas **medidas** antes de planear. Dos de
> ellas resultaron mucho más pequeñas de lo que decían los documentos, y una
> **no era del todo una deuda**.

## Las seis, medidas

| # | Deuda | Tamaño real |
|---|---|---|
| **D1** | `validar_tirada()` ciego en los registros condensados | **9 conjuros** en la sombra; de ellos **3** con `tirada: TdS X` que nunca se contrastó |
| **D2** | 11 conjuros «ataque de conjuro cuerpo a cuerpo», tres etiquetas | **4 mal etiquetados**; los otros 4 con `Directo` **están bien** (ver abajo) |
| **D3** | La CA base sin armadura no tiene cita | **1 página** (pdf 43 = libro 41), doble lectura |
| **D4** | `velocidad` fuera del vocabulario de efectos (`ScaleValue`) | el dato **ya existe** como columna `mov_sin_armadura_m` |
| **D5** | Multiclase sin automatizar | grande; **decisión del usuario** |
| **D6** | ~550 conversiones a pies | aparcado **a petición del usuario**; sigue aparcado |

## D2 no era lo que parecía

Los 14 conjuros con «ataque de conjuro **a distancia**» usan **todos**
`D20+ata.conj.`, sin una sola excepción. Eso fija el vocabulario:
**`D20+ata.CaC` = cuerpo a cuerpo, `D20+ata.conj.` = lo que no lo es.**

Y de los 11 «cuerpo a cuerpo», los **4 que dicen `Directo`** —*Conjurar
feérico*, *Enredadera*, *Hoja de fuego*, *Mano de Bigby*— **no están mal**: el
conjuro se manifiesta sin tirada y el ataque lo hace después la cosa invocada.
Eso es exactamente la semántica de `Directo` fijada el 2026-08-29. Su ataque
pertenece a `tiradas`, la lista por efecto de la Fase 14b-3 — y *Mano de Bigby*
ya lo tiene.

**Quedan 4 correcciones reales**: *Agarre electrizante*, *Arma espiritual*,
*Golpe de viento acerado* y *Látigo de espinas*, que dicen «cuerpo a cuerpo» y
llevan `D20+ata.conj.`. El SRD confirma `melee` en los que publica.

## Pasos

- **D1** · Unificar la regex: `validar_tirada()` pasa a la forma laxa (la que
  ya usa `validar_tiradas()`), descontando el ruido de la concentración.
  **Los 3 conjuros que salgan de la sombra se comprueban de verdad.**
- **D2** · Decidir y escribir el criterio, corregir los 4, y **añadir el
  chequeo** que lo mantiene: si la descripción dice «cuerpo a cuerpo», la
  etiqueta de ataque tiene que ser `D20+ata.CaC`; y si el `tirada` es `Directo`,
  el ataque tiene que estar declarado en `tiradas`.
- **D3** · Cerrar la cita con doble lectura de pdf 43. **Ojo:** el OCR insinúa
  «sin armadura **ni escudo**», y si la página lo dice, el efecto por defecto de
  `ca` necesita una condición que hoy no tiene.
- **D4** · `escala` en el vocabulario de efectos: una tabla dispersa por nivel
  que **lee la columna** de la progresión en vez de duplicarla.
- **D5** · Multiclase: **no se hace a ciegas.** Se propone al usuario.
- **D6** · Conversiones: sigue aparcado hasta que el usuario decida.

---

## Resultado

| # | Resultado |
|---|---|
| **D1** ✅ | `validar_tirada()` pasa a la forma laxa. Los **9** conjuros salen de la sombra; los 3 con `tirada: TdS X` se contrastan y **cuadran**. |
| **D2** ✅ | Criterio fijado con **doble lectura** de *Arma espiritual* y *Enredadera* (coinciden palabra por palabra): «**Haz** un ataque» = el conjuro ES el ataque; «**puedes hacer**» = se manifiesta y el ataque viene después. **6 correcciones** —y dos de ellas invierten lo que yo suponía— más `tiradas` en 4 conjuros y el chequeo `validar_ataques()` (**25** ataques contrastados contra su texto). Reparto final sin ambigüedad: 6 `D20+ata.CaC` · 5 `Directo`+`tiradas` · 14 `D20+ata.conj.` |
| **D3** ✅ | Cita cerrada: **pdf 43 = libro 41**, doble lectura idéntica. La página condiciona la fórmula a «sin armadura **ni escudo**» y remite al capítulo 6 — queda citado, con la explicación de por qué el efecto por defecto no lleva esa condición. El aviso permanente desaparece y pasa a **error** si alguien añade una base sin cita. |
| **D4** ✅ | `velocidad` entra con `columna:`, que **lee** la tabla dispersa en vez de copiarla, y con `decimal: true` (el Goliat sale a 10,5 m sin redondear). Ficha nueva de Monje 2 que lo sostiene: con escudo pierde a la vez la CA y el movimiento (15→14, 12→9). |
| **D5** ⏸️ | Multiclase — **decisión del usuario**, no se hace a ciegas. |
| **D6** ⏸️ | Conversiones a pies — sigue aparcado a petición del usuario. |

**Dos falsos positivos propios**, otra vez: el chequeo de ataques marcó a *Mano
de Bigby* (su «Haz un ataque» está **dentro de un modo**, no en el lanzamiento;
se afinó para que la estructura mande sobre el verbo), y `validar_dados()` contó
un `D3` que era **mi propia nota** («deuda D3») dentro de un bloque YAML — su
filtro salta la línea `_nota:` pero no las de continuación.
