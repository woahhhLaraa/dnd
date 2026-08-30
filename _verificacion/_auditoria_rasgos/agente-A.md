# Auditoría de rasgos — Bárbaro, Bardo, Brujo

Agente: agente-A · fecha: 2026-08-21
Páginas leídas: pdf 53, 54, 55, 61, 62, 63, 71, 72, 73
(pdf 72 se leyó además de las asignadas porque contiene la tabla "Rasgos de brujo"
y resultó ser la página real de un rasgo mal citado — ver hallazgo).
Rasgos revisados: 39 de 39

## Hallazgos

### Brujo · Astucia mágica · pdf 71 (citado) → real pdf 72
- **Tipo:** cita de página
- **Dice el YAML:** `pagina: {pdf: 71, libro: 69}`
- **Dice la página:** La página pdf 71 (libro 69) solo contiene "Nivel 1: Invocaciones
  sobrenaturales" y "Nivel 1: Magia del pacto"; no aparece "Astucia mágica" en
  ningún sitio de esa página. El encabezado real "NIVEL 2: ASTUCIA MÁGICA" está en
  la página pdf 72 (libro 70), columna derecha, con el texto: «Puedes llevar a cabo
  un rito esotérico durante 1 minuto. Al terminarlo, recuperas una cantidad de
  espacios de conjuro utilizados de Magia del pacto igual o inferior a la mitad de
  tu máximo (redondeando hacia arriba). Cuando uses este rasgo, no podrás volver a
  hacerlo hasta que finalices un descanso largo.»
- **Nota:** el contenido mecánico del resumen en el YAML es correcto y coincide
  con el texto de la página real (pdf 72); el único problema es la cita de página
  (y de libro), que apunta a la página anterior.
- **Gravedad:** media (no cambia el resultado en mesa porque la mecánica descrita
  es correcta, pero remite a quien consulte el manual a la página equivocada —
  mismo tipo de error ya detectado antes en Clérigo).

No se encontraron más citas de página erróneas en las 39 entradas: comprobé una
por una que el encabezado "NIVEL X: <NOMBRE DEL RASGO>" apareciera en la página
pdf citada por cada rasgo, incluidos los rasgos de Bárbaro y Bardo, y el resto
coincide.

## Rasgos revisados sin hallazgo

**Bárbaro** (pdf 53-55): Defensa sin armadura, Furia, Maestría con armas, Ataque
temerario, Sentir el peligro, Conocimiento primigenio, Ataque adicional,
Movimiento rápido, Instinto salvaje, Salto instintivo, Golpe brutal, Furia
implacable, Golpe brutal mejorado (nivel 13), Furia persistente, Golpe brutal
mejorado (nivel 17), Poderío indómito, Don épico, Campeón primordial.

Furia y Maestría con armas (las señaladas como zona de mayor riesgo) se
comprobaron con especial cuidado contra la página pdf 53 / tabla de la página
pdf 54: cifras de "N.º de furias" (2→6), "Daño por furia" (+2→+4) y "Maestría con
armas" (2→4 desde nivel 10) coinciden exactamente con la tabla "Rasgos de
bárbaro". La duración de la furia (hasta el final del siguiente turno, máximo
10 minutos, formas de prolongarla, condiciones de terminación) coincide palabra
por mecánica con el texto de la página.

**Bardo** (pdf 61-63): Inspiración bárdica, Lanzamiento de conjuros, Aprendiz de
mucho, Pericia (nivel 2), Fuente de inspiración, Contraencantamiento, Pericia
(nivel 9), Secretos mágicos, Inspiración superior, Don épico, Palabras de
creación.

**Brujo** (pdf 71, 73; y 72 para la tabla): Invocaciones sobrenaturales, Magia
del pacto, Astucia mágica (contenido correcto, cita corregida arriba), Contactar
patrón, Arcanum místico (conjuro de nivel 6, 7, 8 y 9 — niveles 11/13/15/17),
Don épico, Maestro sobrenatural.

Todas las cifras de las tablas "Rasgos de bárbaro", "Rasgos de bardo" y "Rasgos
de brujo" (bonificadores, dados, número de usos, niveles de rasgo) se contrastaron
con las columnas correspondientes y coinciden con lo escrito en los YAML.

## Dudas / ilegible

Ninguna. Las 9 páginas renderizadas a 170 dpi se leyeron con claridad completa,
sin zonas ilegibles.
