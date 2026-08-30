# Auditoría de descripciones (Fase 13p) — lote M2

Agente: M2 · fecha: 2026-08-29
Páginas leídas: pdf 245, 250, 263, 277, 300, 301, 316, 332, 333, 345
Conjuros revisados: 9 de 9

## Hallazgos

### Antipatía/simpatía · pdf 245
- **Campo:** descripcion
- **Modo de fallo:** 7 (regla inventada que tapa a la real) combinado con 2 (posible resto de regla de 2014)
- **Dice la base:** «Debes elegir un objetivo dentro del alcance, de tamaño Enorme o más pequeño, y un tipo de criatura inteligente, como dragones o vampiros.»
- **Dice la página:** «elige si crea antipatía o simpatía y haz objetivo a una criatura **u objeto** de tamaño Enorme o más pequeño. A continuación, selecciona un tipo de criatura, como dragones rojos, goblins o vampiros.» (verificado con recorte a 300 dpi de ese párrafo)
- **Detalle:** la página permite hacer objetivo tanto a una criatura **como a un objeto**; la base solo permite «un objetivo» sin decir que puede ser un objeto — de hecho la redacción de la base («un tipo de criatura inteligente») sugiere que el objetivo también debe ser una criatura. Además la página no usa en ningún momento la palabra «inteligente» al describir el tipo de criatura elegido; ese calificativo no aparece impreso. La lista de ejemplos también difiere («dragones rojos, goblins o vampiros» en la página vs. «dragones o vampiros» en la base), pero eso por sí solo no sería hallazgo.
- **Gravedad:** alta (cambia qué se puede hacer objetivo del conjuro — un objeto grande, no solo una criatura)

### Rociada venenosa · pdf 330 (pdf 332)
- **Campo:** descripcion
- **Modo de fallo:** otro (errata de transcripción, no regla falsa)
- **Dice la base:** «Haz un ataque de conjuro a distancia contra el **ojetivo**.»
- **Dice la página:** «Haz un ataque de conjuro a distancia contra el objetivo.»
- **Gravedad:** baja (errata de una letra, no cambia ninguna regla; se anota por si se quiere corregir de paso)

## Revisados sin hallazgo
- Barrera de cuchillas (pdf 250 / libro 248) — descripción, clases (`["Clérigo"]`) y resumen cuadran con la página letra a letra en contenido.
- Conjurar lluvia de flechas (pdf 263 / libro 261) — descripción, clases (`["Explorador"]`) y material (`coste: null`, verificado ya antes por agente-J) cuadran.
- Dulce descanso (pdf 277 / libro 275) — descripción coincide palabra por palabra; clases (`["Clérigo","Mago","Paladín"]`) coinciden con la cabecera; coste `"2 pc*"` (consumido) coincide con «2 piezas de cobre, que se consumen como parte del conjuro».
- Invocar bestia (pdf 300 / libro 298) — descripción coincide palabra por palabra, incluido el párrafo de «Con un espacio de conjuro de nivel superior»; clases (`["Druida","Explorador"]`) y coste (`"200 po"`) coinciden.
- Nube incendiaria (pdf 316 / libro 314) — descripción coincide, incluida la comprobación de contaminación con «Nube apestosa» (página contigua, contenido de fuego vs. veneno, no mezclados); clases (`["Druida","Hechicero","Mago"]`) coinciden.
- Saber druídico (pdf 332-333 / libro 330-331) — descripción completa (los cuatro efectos: Sensor climático, Florecer, Efecto sensorial, Jugar con fuego) coincide palabra por palabra; clases (`["Druida"]`) coinciden.
- Visión en la oscuridad (pdf 345 / libro 343) — descripción coincide («…tendrá visión en la oscuridad hasta 45 m», la base añade «/ 150 pies», ver sección Unidades); clases (`["Druida","Explorador","Hechicero","Mago"]`) coinciden.

## Dudas / ilegible
- **Barrera de cuchillas** (`tirada: "Directo"`): la descripción exige una tirada de salvación de Destreza («Cualquier criatura situada en el espacio del muro deberá hacer una tirada de salvación de Destreza…»). Es el caso ya contabilizado aparte por la decisión de diseño pendiente sobre «Directo».
- **Nube incendiaria** (`tirada: "Directo"`): mismo caso — la descripción exige salvación de Destreza («todas las criaturas dentro de ella harán una tirada de salvación de Destreza…»).

(El resto de conjuros del lote tiene `tirada` coherente con la página: Antipatía/simpatía = TdS Sab. ✓; Conjurar lluvia de flechas = TdS Des. ✓; Dulce descanso = Directo, sin tirada en la página ✓; Invocar bestia = Directo, sin tirada ✓; Saber druídico = Directo, sin tirada ✓; Rociada venenosa = D20+ata.conj., hay ataque de conjuro a distancia ✓; Visión en la oscuridad = Directo, sin tirada ✓.)

## Unidades
- pdf 245: solo métricas (Antipatía/simpatía, Apariencia, recuadro Objeto animado — ninguna cifra en pies/pulgadas/yardas/millas).
- pdf 250: solo métricas (Barrera de cuchillas, Bendición, Boca mágica).
- pdf 263: solo métricas (Conjurar lluvia de flechas, Conjurar seres del bosque, Conocer las leyendas, Consagrar, Cono de frío).
- pdf 277: solo métricas (Dulce descanso, Elementalismo, Embelesar, Encantar animal, Encontrar el camino).
- pdf 300-301: solo métricas (Invocar bestia + recuadro Espíritu bestial, Invocar celestial + recuadro Espíritu celestial, Invocar dragón + recuadro Espíritu draconico — incluidos los alcances de ataque a distancia en metros, p. ej. «alcance 180 m»).
- pdf 316: solo métricas (Nube apestosa, Nube de dagas, Nube de oscurecimiento, Nube incendiaria, Ofuscación, Ojo arcano).
- pdf 332-333: solo métricas (Rociada de color, Rociada prismática y su tabla «Rayos prismáticos», Rociada venenosa, Saber druídico, Salto, Sanctasanctórum privado de Mordenkainen, Saeta guía, Salpicadura ácida).
- pdf 345: solo métricas (Vínculo protector, Visión en la oscuridad, Visión veraz, Volar, Voluta estelar, Zancada prodigiosa, Zona de la verdad). Notable: la propia descripción de Visión en la oscuridad es un caso limpio del patrón bajo estudio — la página solo dice «hasta 45 m», y es la base la que añade «/ 150 pies» sin que esa cifra en pies aparezca impresa en ningún sitio de la página.

**Resumen del encargo extra:** en las 8 páginas de este lote (más las 2 de continuación) no apareció ni una sola cifra impresa seguida de «pies», «pulgadas», «yardas» o «millas». Todo el texto de reglas —incluidos alcances de armas de espíritus invocados y radios de área— está en metros/centímetros. Esto es consistente con lo reportado por los otros verificadores: el manual castellano parece ser íntegramente métrico.
