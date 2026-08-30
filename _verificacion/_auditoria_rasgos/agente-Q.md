# Auditoría equipo — lote tabla de precio y peso del equipo de aventurero

Agente: agente-Q · fecha: 2026-08-22
Páginas leídas: pdf 225 (libro 223, tabla «Equipo de aventureros»), pdf 226 (libro 224,
tablas «Canalizadores arcanos» y «Canalizadores druídicos»), pdf 227 (libro 225,
control de continuidad, sin tablas de precio/peso), pdf 228 (libro 226, tabla «Munición»)
Registros revisados: 95 de 95 (82 de `tabla_peso_precio` + 5 de `canalizadores_arcanos`
+ 3 de `canalizadores_druidicos` + 5 de `municion`)

Método: render `pdftoppm -r 220` de las páginas pdf 225, 226, 227 y 228 de
`Manual_del_Jugador_2024.pdf`, lectura visual celda a celda contra cada registro del
YAML. Offset verificado en las cuatro páginas leídas: pie de página impreso = página
pdf − 2 en todos los casos (225→223, 226→224, 227→225, 228→226), consistente con el
offset fijado en el proyecto.

La tabla «Equipo de aventureros» con precio y peso está completa en una sola página,
pdf 225 (libro 223), a dos columnas (40 objetos en la izquierda, de Abrojos a Mapa; 42
en la derecha, de Mochila a Yesquero), tal como registra la nota `precio_nota` de
`objetos_de_rasgo_de_clase.Libro de conjuros` en el propio YAML — esa cita ya estaba
verificada y coincide con lo leído aquí. Las tablas «Canalizadores arcanos» y
«Canalizadores druídicos» están en pdf 226 (libro 224), y la tabla «Munición» está en
pdf 228 (libro 226).

## Hallazgos

Ninguno. Las 95 filas comparadas coinciden exactamente con la base, campo a campo
(`nombre`, `peso_kg` y `precio`, y además `cantidad`/`recipiente` en `municion.yaml`).
No se detectó ningún desplazamiento de fila, ningún `null` que debiera ser numérico ni
viceversa, ninguna cifra suelta alterada y ninguna cita de página incorrecta.

## Revisados sin hallazgo

### `equipo/aventureros.yaml` → `tabla_peso_precio` (82) — todos coinciden
Abrojos, Aceite, Ácido, Agua bendita, Aljaba, Antitoxina, Antorcha, Ariete portátil,
Barril, Bolas de metal, Bolsa, Botella de cristal, Cadena, Campana, Canalizador arcano,
Canalizador druídico, Cantimplora, Catalejo, Cerradura, Cesta, Cofre, Cordel, Cubo,
Cuerda, Disfraz, Escalera, Espejo, Esposas, Estuche para mapas o pergaminos, Estuche
para virotes de ballesta, Frasco, Fuego de alquimista, Garfio de escalada, Jarro,
Lámpara, Libro, Linterna de ojo de buey, Linterna sorda, Lupa, Manta, Mapa, Mochila,
Munición, Olla de hierro, Pala, Palanqueta, Papel, Paquete de artista, Paquete de
diplomático, Paquete de erudito, Paquete de explorador, Paquete de explorador de
mazmorras, Paquete de ladrón, Paquete de sacerdote, Perfume, Pergamino, Pergamino de
conjuro (nivel 1), Pergamino de conjuro (truco), Petate, Pluma, Poción de curación,
Polipasto, Puntas de hierro, Raciones, Red, Ropas de calidad, Ropas de viaje, Saco,
Saquito de componentes, Silbato de supervivencia, Símbolo sagrado, Tienda, Tinta,
Trampa para cazar, Túnica, Útiles de escalada, Útiles de sanador, Vara, Vela, Veneno
básico, Vial, Yesquero.

Notas sobre unidades equivalentes (no son hallazgo, según el criterio del briefing):
Espejo (página: «250 g» → base: `0.25`), Poción de curación («250 g» → `0.25`) y Saco
(«250 g» → `0.25`) están expresados en gramos en la página pero en kg equivalentes en
la base; son la misma cifra.

### `equipo/aventureros.yaml` → `canalizadores_arcanos` (5) — todos coinciden
Bastón, Cristal, Orbe, Vara, Varita.

### `equipo/aventureros.yaml` → `canalizadores_druidicos` (3) — todos coinciden
Bastón de madera (también bastón), Rama de muérdago, Varita de tejo.

### `equipo/municion.yaml` → `municion` (5) — todos coinciden
Balas de arma de fuego, Dardos, Flechas, Proyectiles de honda, Virotes (cantidad,
recipiente, peso_kg y precio verificados los cuatro campos contra la tabla «Munición»
de pdf 228).

## Dudas / ilegible

Ninguna. Las cuatro páginas se leyeron con nitidez suficiente a 220 dpi.
