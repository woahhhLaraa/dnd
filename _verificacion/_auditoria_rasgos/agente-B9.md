# Auditoría de descripciones (Fase 13p) — lote B9

Agente: B9 · fecha: 2026-08-29
Páginas leídas: pdf 343, 344, 345, 346 (346 solo para confirmar que Zona de la verdad no continúa: es el Apéndice A)
Conjuros revisados: 12 de 13 (Tsunami excluido: ya corregido por otra vía)

## Hallazgos

### Urna mágica · pdf 343-344
- **Campo:** descripcion
- **Modo de fallo:** otro (mecánica revertida / invertida respecto a la página)
- **Dice la base:** «Tu cuerpo va al recipiente usado como componente. Mientras estás en el eres consciente y no puedes hacer nada; solo puedes proyectar tu alma hasta 30 m / 100 pies para ir a tu cuerpo o poseer a alguien.»
- **Dice la página:** «Tu cuerpo entra en estado catatónico y tu alma lo abandona y entra en el recipiente que has usado como componente material del conjuro. Mientras tu alma esté dentro del recipiente, serás consciente de lo que te rodea, igual que si estuvieras en el espacio de dicho recipiente. No podrás moverte ni llevar a cabo reacciones. La única acción que puedes realizar es proyectar tu alma hasta 30 m del recipiente, bien para regresar a tu cuerpo viviente (y poner fin al conjuro) o bien para tratar de poseer el cuerpo de un humanoide.»
- **Detalle:** la base dice que es el CUERPO el que va al recipiente. La página dice justo lo contrario: el cuerpo se queda (catatónico) donde estaba, y es el ALMA la que abandona el cuerpo y entra en el recipiente. Es una inversión del mecanismo central del conjuro, no una simplificación de redacción. Además, la base afirma «no puedes hacer nada», pero la página especifica que sí hay una acción disponible (proyectar el alma).
- **Gravedad:** alta (cambia el resultado en mesa — invierte qué elemento del lanzador queda en el recipiente y cuál en el mundo)

### Urna mágica · pdf 344
- **Campo:** descripcion
- **Modo de fallo:** 3 (párrafo/cláusula que falta)
- **Dice la base:** «...o poseer a alguien. Si intentas poseer a alguien esté hace salvación de Carisma...»
- **Dice la página:** «Puedes intentar poseer a cualquier humanoide que esté a 30 m o menos de ti que puedas ver (las criaturas protegidas mediante un conjuro círculo mágico o protección contra el bien y el mal no pueden ser poseídas). El objetivo hace una tirada de salvación de Carisma...»
- **Detalle:** la base omite tres restricciones que sí trae la página: (1) el objetivo debe ser un HUMANOIDE, no «alguien» genérico; (2) debe estar dentro del alcance (30 m) Y a la vista; (3) las criaturas protegidas por «círculo mágico» o «protección contra el bien y el mal» no pueden ser poseídas en absoluto.
- **Gravedad:** media (restringe a quién se puede poseer; afecta al resultado en mesa)

## Revisados sin hallazgo

- Truco de la cuerda (pdf 343)
- Viajar con el viento (pdf 344)
- Viajar mediante plantas (pdf 344)
- Vigor arcano (pdf 344)
- Vínculo protector (pdf 345)
- Visión en la oscuridad (pdf 345)
- Visión veraz (pdf 345)
- Volar (pdf 345)
- Voluta estelar (pdf 345)
- Zancada prodigiosa (pdf 345)
- Zona de la verdad (pdf 345)

(Tsunami, pdf 343: ya corregido hoy por otra vía — no auditado en este informe.)

En todos los anteriores se comprobó: cabecera vs. `nombre` (coinciden letra a letra), `clases` (lista completa cotejada una a una contra el paréntesis de cabecera, sin listas cortas), `descripcion` (sin conjuro vecino contaminado, sin párrafos «Con un espacio de conjuro de nivel superior» / «Mejora de truco» faltantes, sin cifras alteradas, sin tablas con nombres inventados), `tirada` coherente con la página, y `resumen` sin contradicciones. Las conversiones de unidad presentes en la base (p. ej. 18 m / 60 pies, 3 m / 10 pies, 4,5 m / 15 pies, 45 m / 150 pies, 36 m / 120 pies) son aritméticamente correctas, aunque ninguna de esas cifras en pies está impresa en la página (ver sección Unidades).

## Unidades

- pdf 343: solo métricas. Cifras vistas: «0,9 m por 1,5 m» (Truco de la cuerda), «30 m» (Urna mágica), además de las de Tsunami/Trepar cual arácnido/Tronar (fuera de mi lote) también en metros. Ninguna cifra en pies, pulgadas, yardas o millas.
- pdf 344: solo métricas. Cifras vistas: «30 m» (continuación Urna mágica, ×5), «90 m», «18 m» (Viajar con el viento), «3 m», «1,5 m» (Viajar mediante plantas). Ninguna cifra en pies, pulgadas, yardas o millas.
- pdf 345: solo métricas. Cifras vistas: «18 m» (Vínculo protector, ×2), «45 m» (Visión en la oscuridad), «36 m» (Visión veraz), «18 m» (Volar), «3 m» (Voluta estelar), «3 m» (Zancada prodigiosa), «4,5 m» (Zona de la verdad). Ninguna cifra en pies, pulgadas, yardas o millas.

**Conclusión de mi lote: cero apariciones de unidades imperiales impresas en pdf 343-345.** Consistente con lo reportado por los otros verificadores: el manual castellano parece íntegramente métrico en estas páginas.

## Dudas / ilegible

- **Urna mágica** (pdf 343): `tirada` = «Directo», pero la descripción exige tirada de salvación de Carisma (tanto para el intento de posesión como si el cuerpo poseído muere). Según el briefing, esto se apunta en Dudas y no en Hallazgos porque ya está contado aparte como decisión de diseño pendiente sobre el valor «Directo».
- Ningún otro conjuro del lote presenta este patrón (`Directo` + salvación en el texto): todos los demás con `tirada: "Directo"` (Truco de la cuerda, Viajar con el viento, Viajar mediante plantas, Vigor arcano, Vínculo protector, Visión en la oscuridad, Visión veraz, Volar, Zancada prodigiosa, Zona de la verdad) no contradicen — excepto Zona de la verdad y Vínculo protector, que sí mencionan tiradas de salvación en su texto (Carisma para Zona de la verdad) pero eso es la tirada que hace el OBJETIVO/tercero, no una salvación del propio lanzador o de "quien recibe el efecto directo"; lo dejo anotado por si el criterio de "Directo" del proyecto no contempla ese matiz, pero no lo elevo a hallazgo porque cae en la misma categoría de decisión pendiente que el briefing menciona.
- No hay términos «salvamento» (por «tirada de salvación») en ninguno de los 12 conjuros de este lote.
- No hay texto ilegible en pdf 343-345 a 170 dpi.
