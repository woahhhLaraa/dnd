# Auditoría — Subclases de Mago, Monje, Paladín y Pícaro

Agente: agente-G · fecha: 2026-08-21
Páginas leídas: pdf 144, 145, 146, 147, 148, 149 (Mago) · 153, 154, 155, 156, 157 (Monje) · 163, 164, 165, 166, 167 (Paladín) · 172, 173, 174, 175, 176, 177 (Pícaro)
Elementos revisados: 16 de 16 subclases (80 rasgos)

## Hallazgos

Ninguno. Las 16 subclases citan correctamente la página en la que empiezan, y el contenido mecánico del resumen (dados, alcances, condiciones, niveles, usos) coincide con lo que dice la página en todos los casos comprobados.

## Comprobaciones específicas pedidas en el encargo

**Monje — "solo 3 páginas distintas para 4 subclases":** confirmado que **no** es un error. Guerrero de la Mano Abierta y Guerrero de la Misericordia arrancan de verdad en la misma página física (pdf 154 / libro 152): la página trae primero el título y el párrafo de ambientación de Guerrero de la Mano Abierta en la columna derecha junto con la ilustración de la subclase, sus cuatro rasgos ocupan el resto de esa página y el principio de la siguiente (pdf 155 / libro 153), y justo debajo, en la misma pdf 154, ya aparece el encabezado "Guerrero de la Misericordia" con su párrafo de ambientación (los rasgos de esta segunda subclase continúan en pdf 155). Por tanto `pagina: {pdf: 154, libro: 152}` es correcto para ambas subclases tal como recoge el YAML.

**Monje — salto 154→156 (pdf 155 no citada):** revisada. La pdf 155 (libro 153) contiene los rasgos de nivel 3 a 17 de Guerrero de la Misericordia (Instrumentos de misericordia, Mano de aflicción, Mano de curación, Toque de galeno, Ráfaga de curación y aflicción, Mano de misericordia suprema), todos ya recogidos bajo la cita `pagina: pdf 154` de esa subclase. No hay contenido nuevo ni subclase oculta en esa página; el salto en la tabla de páginas citadas no esconde ningún defecto.

**Pícaro — salto 173→175 (pdf 174 no citada):** revisada. La pdf 174 (libro 172) contiene la tabla "Lanzamiento de conjuros del embaucador arcano" y los rasgos de nivel 3, 9, 13 y 17 de Embaucador Arcano (Destreza con mano de mago, Emboscada mágica, Embaucador versátil, Ladrón de conjuros), todos ya recogidos bajo la cita `pagina: pdf 173` de esa subclase. Ladrón, la siguiente subclase, arranca correctamente en pdf 175 (libro 173). No hay contenido perdido.

## Revisados sin hallazgo

### Mago (`clases/subclases/mago.yaml`), niveles de subclase 3/6/10/14
- Abjurador — pdf 146/libro 144: cita correcta. Experto en abjuración, Salvaguarda arcana (9 m, 2× nivel de mago + Int), Salvaguarda proyectada, Rompeconjuros, Resistencia a conjuros — contenido y niveles coinciden.
- Adivino — pdf 147/libro 145: cita correcta. Experto en adivinación, Presagio (2d20), Adivino avezado, El tercer ojo (36 m visión oscuridad), Presagio mayor (3d20) — coinciden.
- Evocador — pdf 148/libro 146: cita correcta. Experto en evocación, Truco potente, Esculpir conjuros (1 + nivel), Evocación potenciada, Sobrecanalizar (2d12/1d12 necrótico) — coinciden.
- Ilusionista — pdf 149/libro 147: cita correcta. Experto en ilusionismo, Ilusiones mejoradas, Criaturas fantasmales, Yo ilusorio, Realidad ilusoria — coinciden.

### Monje (`clases/subclases/monje.yaml`), niveles de subclase 3/6/11/17
- Guerrero de la Mano Abierta — pdf 154/libro 152: cita correcta. Técnica de la mano abierta, Plenitud de cuerpo, Paso veloz, Palma estremecedora (10d12) — coinciden.
- Guerrero de la Misericordia — pdf 154/libro 152 (rasgos en pdf 155): cita correcta, ver nota arriba. Instrumentos de misericordia, Mano de aflicción, Mano de curación, Toque de galeno, Ráfaga de curación y aflicción, Mano de misericordia suprema (4d10) — coinciden.
- Guerrero de la Sombra — pdf 156/libro 154: cita correcta. Artes sombrías (18 m visión oscuridad), Paso entre sombras (18 m), Paso entre sombras mejorado, Capa de sombras — coinciden.
- Guerrero de los Elementos — pdf 157/libro 155: cita correcta. Armonía con los elementos, Manipular los elementos, Explosión elemental (6 m radio, 36 m, 3 tiradas de dado Artes marciales), Paso de los elementos, Paradigma elemental — coinciden.

### Paladín (`clases/subclases/paladin.yaml`), niveles de subclase 3/7/15/20
- Juramento de Entrega — pdf 163/libro 161: cita correcta. Arma sagrada, tabla de conjuros, Aura de entrega, Castigo protector, Halo sagrado — coinciden.
- Juramento de Gloria — pdf 164/libro 162: cita correcta. Atleta sin parangón, Castigo inspirador (2d8 + nivel), tabla de conjuros, Aura de celeridad, Defensa gloriosa, Leyenda viviente — coinciden.
- Juramento de los Antiguos — pdf 165/libro 163: cita correcta. Ira de la naturaleza (4,5 m), tabla de conjuros, Aura de salvaguarda, Centinela imperecedero, Campeón ancestral — coinciden.
- Juramento de Venganza — pdf 166/libro 164: cita correcta. Voto de enemistad (9 m), tabla de conjuros, Vengador implacable, Espíritu vengativo, Ángel vengador (18 m volando) — coinciden.

### Pícaro (`clases/subclases/picaro.yaml`), niveles de subclase 3/9/13/17
- Asesino — pdf 172/libro 170: cita correcta. Asesinar, Herramientas de asesino, Pericia en infiltrarse, Envenenar armas (2d6), Golpe mortal — coinciden.
- Embaucador Arcano — pdf 173/libro 171: cita correcta. Lanzamiento de conjuros (mano de mago + 2 trucos, 3 conjuros nivel 1, Inteligencia, canalizador arcano), Destreza con mano de mago, Emboscada mágica, Embaucador versátil, Ladrón de conjuros — coinciden.
- Ladrón — pdf 175/libro 173: cita correcta. Balconero, Manos rápidas, Sigilo supremo (1d6), Usar objetos mágicos, Reflejos de ladrón — coinciden.
- Rebanaalmas — pdf 176/libro 174: cita correcta. Cuchillas psíquicas (1d6/1d4, 18/36 m), Poder psiónico (tabla de dados coincide), Cuchillas del alma, Velo psíquico, Desgarro mental — coinciden.

## Dudas / ilegible

Ninguna. Todas las páginas se leyeron con claridad a 170 dpi.
