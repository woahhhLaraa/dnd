# Auditoría — Subclases de Druida, Explorador, Guerrero y Hechicero

Agente: agente-F · fecha: 2026-08-21
Páginas leídas: pdf 99, 100, 101, 102, 103, 104 (Druida) · pdf 106, 107, 108, 109, 110, 111, 112, 113 (Explorador) · pdf 117, 118, 119, 120, 121, 122, 123 (Guerrero) · pdf 129, 130, 131, 132, 133, 134, 135, 136, 137 (Hechicero)
Elementos revisados: 16 de 16 subclases · 85 de 85 rasgos (más las tablas de conjuros/maniobras/perfiles asociadas a cada una)

## Hallazgos

### Druida · Círculo de las Estrellas · pdf 102 (cita del YAML)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 102, libro: 100}`
- **Dice la página:** El encabezado «CÍRCULO DE LAS ESTRELLAS», el lema «Utiliza los secretos que se ocultan en las constelaciones», la introducción y el rasgo completo «Nivel 3: Forma estelar» (con las tres constelaciones Arquero, Cáliz y Dragón) aparecen ya en **pdf 101** (página de libro 99), justo después de que termina el rasgo de nivel 14 del Círculo de la Tierra en esa misma página. La página pdf 102 (libro 100) solo contiene la continuación (tabla «Mapa estelar», Nivel 6, Nivel 10, Nivel 14) y, al final, el encabezado de la siguiente subclase (Círculo del Mar).
- **Gravedad:** alta (la subclase no empieza donde dice `pagina.pdf`; corresponde pdf 101 / libro 99).

### Druida · Círculo del Mar · pdf 103 (cita del YAML)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 103, libro: 101}`
- **Dice la página:** El encabezado «CÍRCULO DEL MAR», el lema «Fúndete con las mareas y las tormentas» y el primer párrafo de ambientación aparecen al final de **pdf 102** (libro 100), inmediatamente después del rasgo «Nivel 14: Colmado de luz estelar» del Círculo de las Estrellas. La página pdf 103 (libro 101) contiene ya el contenido mecánico (tabla de conjuros, Nivel 3 Ira de los mares, etc.), pero el inicio real de la subclase (su encabezado) está en pdf 102.
- **Gravedad:** alta; corresponde pdf 102 / libro 100. (Nota: este defecto es consecuencia del mismo desplazamiento que el de Círculo de las Estrellas — ambas citas están una página por detrás de donde realmente empieza cada subclase.)

### Guerrero · Maestro del Combate · pdf 119 (cita del YAML)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 119, libro: 117}` — la misma página que se cita para Campeón.
- **Dice la página:** pdf 119 (libro 117) contiene el final de Caballero Arcano y el encabezado + Nivel 3 de **Campeón** («Aspira a la excelencia física en combate»), confirmando que esa cita es correcta para Campeón. El encabezado «MAESTRO DEL COMBATE», su lema «Domina maniobras de combate avanzadas» y los rasgos «Nivel 3: Estudioso de la guerra» y «Nivel 3: Supremacía en combate» aparecen en realidad en **pdf 121** (libro 119), a continuación del rasgo «Nivel 18: Maestro telequinético» del Guerrero Psiónico. Es decir, dos subclases distintas comparten por error la misma página citada (pdf 119), cuando la secuencia real es: Caballero Arcano pdf 117 → Campeón pdf 119 → Guerrero Psiónico pdf 120 → Maestro del Combate pdf 121.
- **Gravedad:** alta; corresponde pdf 121 / libro 119.

### Hechicero · Hechicería de Magia Salvaje · pdf 133 (cita del YAML)
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 133, libro: 131}`
- **Dice la página:** El encabezado «HECHICERÍA DE MAGIA SALVAJE», el lema «Desata una magia caótica», la introducción y **los cinco rasgos completos** (Nivel 3 Mareas del caos, Nivel 3 Sobrecarga de magia salvaje, Nivel 6 Doblegar la suerte, Nivel 14 Caos controlado, Nivel 18 Sobrecarga domada) están en **pdf 132** (libro 130), en la misma página donde termina «Nivel 14: Revelación en carne» de Hechicería Aberrante. La página pdf 133 (libro 131) es en realidad la tabla «Sobrecarga de magia salvaje» (1d100), una tabla auxiliar del rasgo de nivel 3, no el inicio de la subclase.
- **Gravedad:** alta; corresponde pdf 132 / libro 130.

## Revisados sin hallazgo

**Druida** (niveles de subclase 3, 6, 10, 14 — confirmados contra las páginas):
- Círculo de la Luna, pdf 99/libro 97 — cita correcta. Rasgos de nivel 3 (Conjuros del círculo de la luna, Formas del círculo), 6 (Formas del círculo mejoradas), 10 (Paso de la luz lunar), 14 (Forma lunar) verificados palabra por mecánica contra pdf 99-100.
- Círculo de la Tierra, pdf 100/libro 98 — cita correcta. Tablas de conjuros por terreno (árido, polar, templado, tropical) y tabla de resistencias verificadas íntegramente contra pdf 100-101. Rasgos nivel 3, 6, 10, 14 verificados.
- Círculo de las Estrellas — contenido mecánico (Forma estelar con sus tres constelaciones, Mapa estelar, Presagio cósmico, Constelaciones centelleantes, Colmado de luz estelar) verificado correcto; solo la cita de página está mal (ver hallazgo).
- Círculo del Mar — contenido mecánico (tabla de conjuros, Ira de los mares, Afinidad acuática, Nacido de la tempestad, Obsequio oceánico) verificado correcto; solo la cita de página está mal (ver hallazgo).

**Explorador** (niveles de subclase 3, 7, 11, 15 — confirmados contra las páginas):
- Acechador en la Penumbra, pdf 108/libro 106 — cita correcta. Tabla de conjuros y rasgos (Emboscador pavoroso, Visión en la umbra, Mente de hierro, Oleada del acechador, Esquiva de las sombras) verificados contra pdf 108-109.
- Cazador, pdf 109/libro 107 — cita correcta. Rasgos (El cazador y la presa, Sabiduría del cazador, Tácticas defensivas, El cazador experto y la presa, Defensa de cazador experto) verificados contra pdf 109-110.
- Errante Feérico, pdf 110/libro 108 — cita correcta. Tabla de conjuros, tabla de dádivas, y rasgos (Glamur sobrenatural, Golpes pavorosos, Giro seductor, Refuerzos feéricos, Errante brumoso) verificados contra pdf 110-111.
- Señor de las Bestias, pdf 112/libro 110 — cita correcta. Rasgos (Compañero primigenio, Entrenamiento excepcional, Furia bestial, Compartir conjuros) verificados contra pdf 112. Los tres perfiles de bestia primigenia (mares, cielo, tierra firme) verificados campo por campo (tamaño, CA, PG, velocidad, atributos, acción de golpe de bestia con sus dados de daño) contra pdf 113 — todos correctos, incluido el bonus de +1d6 y derribo de Bestia de tierra firme al moverse 6 m o más en línea recta.
- El salto de páginas 110→112 es real: pdf 111 pertenece íntegramente a Errante Feérico (continuación de sus rasgos), no falta ninguna subclase intermedia.

**Guerrero** (niveles de subclase 3, 7, 10, 15, 18 — confirmados contra las páginas):
- Caballero Arcano, pdf 117/libro 115 — cita correcta. Rasgos (Lanzamiento de conjuros, Vínculo de guerra, Magia de guerra, Golpe sobrenatural, Carga arcana, Magia de guerra mejorada) verificados contra pdf 117-119.
- Campeón, pdf 119/libro 117 — cita correcta (confirmada al verificar el hallazgo de Maestro del Combate). Rasgos (Atleta sobresaliente, Crítico mejorado, Estilo de combate adicional, Guerrero heroico, Crítico superior, Superviviente) verificados contra pdf 119-120.
- Guerrero Psiónico, pdf 120/libro 118 — cita correcta. Tabla de dados de energía psiónica y rasgos (Poder psiónico, Adepto telequinético, Mente robusta, Bastión de fuerza, Maestro telequinético) verificados contra pdf 120-121.
- Maestro del Combate — contenido mecánico (Estudioso de la guerra, Supremacía en combate, Conoce a tu enemigo, Supremacía en combate mejorada, Incansable, Supremacía en combate definitiva) y las 19 maniobras de la lista «Opciones de maniobras» verificadas una por una contra pdf 121-123, todas correctas; solo la cita de página está mal (ver hallazgo).
- El patrón de páginas repetidas (119 aparece dos veces en el YAML, para Campeón y para Maestro del Combate) es precisamente el defecto: la secuencia real de páginas es 117, 119, 120, 121, no 117, 119, 120, 119.

**Hechicero** (niveles de subclase 3, 6, 14, 18 — confirmados contra las páginas):
- Hechicería Aberrante, pdf 131/libro 129 — cita correcta. Tabla de conjuros psiónicos y rasgos (Habla telepática, Defensas psíquicas, Hechicería psiónica, Revelación en carne, Implosión deformadora) verificados contra pdf 131-132.
- Hechicería de Magia Salvaje — contenido mecánico (Mareas del caos, Sobrecarga de magia salvaje, Doblegar la suerte, Caos controlado, Sobrecarga domada) verificado correcto, incluida la referencia a la tabla 1d100 de pdf 133-135; solo la cita de página está mal (ver hallazgo).
- Hechicería Dracónica, pdf 135/libro 133 — cita correcta. Tabla de conjuros dracónicos y rasgos (Resistencia dracónica, Afinidad elemental, Alas de dragón, Compañero dragón) verificados contra pdf 135-136.
- Hechicería Mecánica, pdf 136/libro 134 — cita correcta. Tabla de conjuros mecánicos, tabla de manifestaciones del orden y rasgos (Restablecer equilibrio, Bastión de la ley, Trance de orden, Cabalgata mecánica) verificados contra pdf 136-137.
- El salto 131→133 es real y no oculta ninguna subclase perdida: pdf 132 pertenece a Hechicería de Magia Salvaje (que el YAML cita erróneamente como 133) y pdf 133-134 es la tabla «Sobrecarga de magia salvaje» asociada a ese mismo rasgo.

## Dudas / ilegible

Ninguna. Todas las páginas se leyeron con claridad a 170 dpi.

## Nota sobre el patrón detectado

Los cuatro hallazgos son **exclusivamente citas de página** (el defecto que el encargo señala como prioritario), y los cuatro comparten la misma causa aparente: la página citada en el YAML es la de la *continuación* del contenido de la subclase (donde están las tablas extensas o los rasgos de nivel intermedio), no la página donde realmente **empieza** la subclase (encabezado + lema + primer rasgo de nivel 3). En los cuatro casos el contenido mecánico resumido en el YAML es correcto; no se encontraron errores de cifras, dados, niveles, condiciones ni rasgos que falten o sobren en ninguna de las 16 subclases ni en las 85 entradas de `rasgos`.
