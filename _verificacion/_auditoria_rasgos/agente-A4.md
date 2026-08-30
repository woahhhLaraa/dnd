# Auditoría de descripciones (Fase 13p) — lote A4

Agente: A4 · fecha: 2026-08-22
Páginas leídas: pdf 265, 266, 267, 268, 269 (libro 263-267)
Conjuros revisados: 12 de 12

## Hallazgos

### Creación · pdf 267
- **Campo:** descripcion
- **Modo de fallo:** otro (regla distinta de la del manual, no una de 2014 pero tampoco la de 2024)
- **Dice la base:** «No puedes usar un objeto creado con este conjuro para crear otro usando este mismo conjuro.»
- **Dice la página:** «Si se usa cualquier objeto creado con este conjuro como componente material de otro conjuro, este último fallará.»
- **Gravedad:** alta (cambia el resultado en mesa) — la base prohíbe algo que el manual no prohíbe (reutilizar el conjuro para crear otro objeto) y omite la regla real (que el objeto creado inutiliza cualquier otro conjuro que lo use como componente material).

### Crear muerto viviente · pdf 268
- **Campo:** descripcion
- **Modo de fallo:** 5 (nombres inventados / mal traducidos)
- **Dice la base:** «cada uno se anima como un ghoul...», «con nivel 8 cinco ghouls o dos ghasts o wights», «con nivel 9 seis ghouls, tres ghasts o wights, o dos momias»
- **Dice la página:** «Cada uno se convierte en un **gul** bajo tu control...», «puedes animar o reforzar el control sobre cinco **gules** o dos ghasts o **tumularios**», «seis **gules**, tres ghasts o **tumularios** o dos momias»
- **Gravedad:** media — las cifras (4/5/2/6/3/2) coinciden todas con la página, pero los nombres de criatura están en inglés sin traducir («ghoul», «wight») en vez de los términos oficiales del manual («gul», «tumulario»); alguien que busque el perfil de «wight» en el Manual de monstruos en castellano no lo encontrará.

### Crear llama · pdf 268
- **Campo:** tirada
- **Modo de fallo:** otro (campo tirada no cuadra con la descripción)
- **Dice la base:** `"tirada": "Directo"`
- **Dice la página:** «Haz un ataque de conjuro a distancia. Si acierta, el objetivo recibe 1d8 de daño de fuego.»
- **Gravedad:** baja — es un ataque de conjuro, no un efecto "Directo" sin tirada; en otros conjuros del registro (p.ej. Cuchillo de hielo) este tipo de efecto se marca como `"D20+ata.conj."`, así que el valor aquí parece incoherente con la convención propia de la base.

## Revisados sin hallazgo

- Contingencia (pdf 265)
- Contorno borroso (pdf 265)
- Contrahechizo (pdf 265)
- Controlar agua (pdf 265-266, efecto se corta y continúa en la página siguiente; verificado íntegro)
- Crear comida y agua (pdf 267)
- Crecimiento espinoso (pdf 268)
- Curar (pdf 269) — cifra de 70 pg base y +10 pg/nivel superior a 6, coincide exacta con la página
- Curar en masa (pdf 269) — cifra de 700 pg, coincide exacta con la página; sin cláusula de espacio superior, igual que en la página
- Curar heridas en masa (pdf 269) — 5d8 + mod. y +1d8/nivel superior a 5, coincide exacta con la página

Las tres curaciones (Curar, Curar en masa, Curar heridas en masa) comparten página y son muy parecidas; se comprobó cabecera por cabecera y ninguna cifra de puntos de golpe está cruzada entre ellas.

## Dudas / ilegible

- **Controlar agua** (pdf 265-266): la descripción incluye la opción «Remolino», que exige una tirada de salvación de Fuerza, pero el campo `tirada` de la base dice `"Directo"`. Según el briefing, esto se cuenta aparte y no es hallazgo de este lote.
