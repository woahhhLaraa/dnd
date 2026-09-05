# Esquema de `personajes/<nombre>.yaml`

## Regla central

**Todo dato mecánico es una referencia (`ref:`), nunca una copia de texto.**
Si la base se corrige, la ficha debe seguir citando lo correcto sin que
nadie la toque a mano. Guardar una copia del texto de un rasgo o conjuro es
exactamente el error que este esquema existe para evitar: la ficha queda
desincronizada en silencio la próxima vez que alguien corrija la base.

La única prosa libre permitida es la que no tiene equivalente mecánico:
nombre, historia personal, descripción física, personalidad. Todo lo demás
— clase, especie, trasfondo, conjuros, dotes, equipo, competencias — es un
puntero a un registro real de la base.

## Bloques

```yaml
nombre: "Aerin Vellamora"
jugador: null                    # opcional, nombre de quien lo juega
nivel_total: 1

especie:
  ref: "especies/especies.yaml#Aasimar"
  rasgos_elegidos: {}            # solo si la especie ofrece una elección (p. ej. tamaño)

trasfondo:
  ref: "trasfondos/trasfondos.yaml#Noble"

clases:                          # lista porque puede haber multiclase
  - clase: Bardo
    ref: "clases/bardo.yaml"
    nivel: 1
    subclase: null               # ref a clases/subclases/<clase>.yaml cuando se elija

caracteristicas:
  metodo: conjunto_estandar      # conjunto_estandar | compra_puntos | aleatorio
  base: {fue: 8, des: 14, con: 12, int: 13, sab: 10, car: 15}
  ajuste_trasfondo: {car: 2, int: 1}
  final: {fue: 8, des: 14, con: 12, int: 14, sab: 10, car: 17}

competencias:
  salvaciones: [Destreza, Carisma]
  habilidades:
    - {nombre: Persuasión, origen: {clase: Bardo}}
    - {nombre: Historia,   origen: {trasfondo: Noble}}
  # OJO: esto es competencia con una CATEGORÍA ("Armas sencillas"), no con
  # un objeto concreto. No lleva `ref:` a equipo/ — esas categorías no
  # existen como registros individuales ahí (bug real hallado en pruebas:
  # "equipo/armas.yaml#Armas sencillas" no resuelve, porque en armas.yaml
  # solo hay armas concretas — "Daga", "Bastón"... — nunca la categoría
  # entera). El texto va literal, tal cual aparece en
  # `atributos_basicos.armas`/`.armaduras`/`.herramientas` de la clase, y
  # `verificar_personaje.py` comprueba que esté en esa lista, no que
  # resuelva como equipo.
  armas: [{categoria: "Armas sencillas", origen: {clase: Bardo}}]
  armaduras: [{categoria: "Armaduras ligeras", origen: {clase: Bardo}}]
  herramientas: []
  idiomas: [{nombre: Común}, {nombre: Élfico, origen: {especie: "..."}}]

equipo:
  - {ref: "equipo/armaduras.yaml#Armadura de cuero", origen: {clase: Bardo, opcion: A}}
  - {ref: "equipo/aventureros.yaml#objetos_de_rasgo_de_clase#Libro de conjuros",
     origen: {clase: Mago, rasgo: "Lanzamiento de conjuros"}}

conjuros:                        # solo si la clase es lanzadora
  # Cuentan contra la tabla de la clase los que NO declaran `origen`, o cuyo
  # `origen` solo nombra la clase (y a lo sumo su rasgo «Lanzamiento de
  # conjuros»). Todo lo demás —una dote, un rasgo de especie, una opción de
  # orden, o cualquier entrada con `nota` de «no cuenta contra el límite»— es
  # un EXTRA y tiene que decir de dónde sale.
  #
  # Hasta el 2026-08-30 nadie los contaba: un mago de nivel 20 con dos trucos
  # habría verificado en verde, y `_ejemplo_aerin` llevaba 1 conjuro preparado
  # donde la tabla del Brujo concede 2.
  trucos:
    - {ref: "hechizos.json#Luces danzantes"}
    - {ref: "hechizos.json#Luz", origen: {dote: "Iniciado en la magia"}}
  preparados: [{ref: "hechizos.json#Hechizar persona"}]

dotes:
  - {ref: "dotes/origen.yaml#Habilidoso", origen: {trasfondo: Noble}}

# ⛔ `bonus_pg_especie` SE ELIMINÓ en la Fase 14 (2026-08-29).
# Era un parche que el propio esquema admitía como tal, y falló de tres
# maneras a la vez: cubría 1 de los 2 efectos de PG máximos de la base
# (*Resistencia dracónica* del Hechicero no tenía dónde declararse), guardaba
# un 1 fijo cuando "Aguante enano" dice "y en 1 más cada vez que subes de
# nivel", y NADIE OBLIGABA A RELLENARLO: `personajes/enano_guerrero.yaml` lo
# tenía vacío y verificaba en verde con los PG mal.
# Hoy el bono es un efecto citado en `especies/especies.yaml` y lo aplica
# `efectos.py` solo, sin que la ficha tenga que acordarse. Ver
# `reglas/_ESQUEMA_efectos.md`.

mejoras:                         # OBLIGATORIO si la clase concede alguna
  # Una entrada por cada «Mejora de característica» que la tabla conceda hasta
  # el nivel del personaje, si no se gastó en una dote. `caracteristicas.final`
  # tiene que ser EXACTAMENTE `base` + `ajuste_trasfondo` + estas mejoras: una
  # puntuación sin justificar es una puntuación inventada, y hasta el
  # 2026-08-30 nadie lo comprobaba — un monje de nivel 20 con las seis
  # características a 20 verificaba en verde.
  #
  # La regla está en `dotes/generales.yaml#Mejora de característica` (pdf 209 =
  # libro 207): «Aumenta en 2 una puntuación de característica de tu elección,
  # o aumenta dos en 1 cada una. No puede superar 20». `repetible: true`.
  - {nivel: 4, sube: {des: 2}, ref: "dotes/generales.yaml#Mejora de característica"}
  - {nivel: 8, sube: {int: 1, sab: 1}, ref: "..."}
  # Si en un nivel de mejora se toma una DOTE en vez de subir características,
  # no va aquí: va en `dotes:` con `origen: {clase: X, nivel: N}`. El
  # verificador exige que cada nivel de mejora esté gastado de una de las dos
  # formas, ni de más ni de menos.

pg_por_nivel:                    # OBLIGATORIO a partir del nivel 2
  # Una entrada por nivel, del 1 al nivel_total. Los PG de los niveles 2+ son
  # una ELECCIÓN del jugador (tirar el dado o usar el valor establecido de la
  # tabla), así que el motor NO puede deducirlos: los lee de aquí. Una tirada
  # no es reproducible, de modo que lo que se guarda es el RESULTADO.
  #
  # El total NO se guarda sumado. `calculo.pg_max_de_ficha()` lo recalcula
  # entero desde estos valores crudos cada vez, y por eso la regla retroactiva
  # del modificador por Constitución (pdf 44 = libro 42, paso 5: «tus puntos de
  # golpe máximos también aumentarán en 1 por cada nivel que hayas alcanzado»)
  # sale sola. Guardar el total acumulado acertaría hasta la primera dote que
  # subiera Constitución, y a partir de ahí se equivocaría en silencio.
  - {nivel: 1, clase: Hechicero, metodo: maximo_dado, valor: 6,
     cita: {archivo: "reglas/generacion_personaje.yaml", campo: "puntos_golpe.nivel_1"}}
  - {nivel: 2, clase: Hechicero, metodo: valor_establecido, valor: 4, cita: {...}}
  - {nivel: 3, clase: Hechicero, metodo: tirada, valor: 5, cita: {...}}
  # `metodo` ∈ {maximo_dado (solo nivel 1), tirada, valor_establecido}
  # `valor` es el número CRUDO: el máximo del dado, el resultado de la tirada o
  # el valor de la tabla. NUNCA lleva el modificador por Constitución sumado.
  # `clase` importa en multiclase: cada nivel lo da el dado de SU clase.

elecciones:                      # SOLO si el personaje tiene más de una forma
                                  # de calcular una variable. El manual dice que
                                  # de varias CA base "solo puede beneficiarse
                                  # de una, A ELEGIR" (reglas/generacion_
                                  # personaje.yaml → multiclase.clase_de_armadura),
                                  # así que el motor exige la elección en vez de
                                  # coger la mayor por su cuenta.
  ca_base: null                   # p. ej. "Defensa sin armadura" en un
                                  # Monje/Hechicero dracónico multiclase

calculado:                       # lo escriben calculo.py y efectos.py — nunca a mano
  # De dónde sale este bloque, y no es burocracia: la ficha se ESCRIBE con
  # `calculo`/`efectos` (por `--calcular`) y se VERIFICA recalculando con
  # `calculo`/`efectos`. El círculo está cerrado, así que un error del motor
  # produce una ficha coherente y equivocada. `mutaciones_motor.py` lo midió
  # el 2026-09-05: 7 de 11 trozos del motor se pueden corromper sin que
  # ninguna ficha se queje.
  #
  # `metodo` ∈ {motor, agente-manual}. `--calcular` escribe SIEMPRE `motor` y
  # no tiene forma de escribir lo otro: si el escritor pudiera firmar como
  # oráculo, no habría oráculo. Solo una lectura independiente de la página
  # —el mandato «el calculista» de `PLAN_ESTRES.md`— pone `agente-manual`, y
  # entonces `informe:` tiene que apuntar a la derivación escrita.
  _origen: {metodo: motor, informe: null, fecha: "2026-09-05"}
  pg_max: 9
  ca: 12
  bonif_competencia: 2
  cd_conjuros: 13
  bonif_ataque_conjuros: 5

decisiones:                      # log auditable: qué se eligió y por qué está permitido
  - en: "creación"
    eleccion: "habilidades: Persuasión, Historia"
    cita: {archivo: "clases/bardo.yaml", campo: "atributos_basicos.habilidades"}
```

## Prosa libre (sin límite de longitud, sin `ref:`)

`nombre`, `jugador`, `historia`, `personalidad`, `descripcion_fisica`,
`alineamiento`, `notas`, `trasfondo_narrativo` y `decisiones[].eleccion` son
las únicas claves donde puedes escribir cuanto quieras. Todo lo demás que no
sea una de estas y tenga una frase larga es sospechoso de ser texto copiado
de la base en vez de una referencia (ver regla 5 más abajo).

## Reglas de verificación (las aplica `verificar_personaje.py`)

1. Cada `ref:` debe resolver a un registro real. Formato de `ref`:
   `archivo.yaml#Clave` para un registro con `nombre: Clave` en la raíz, o
   `archivo.yaml#seccion#Clave` cuando el registro vive bajo una clave
   anidada (como `objetos_de_rasgo_de_clase`). Si el nombre se repite en más
   de un fichero de `equipo/` con significados distintos (p. ej. "Bastón":
   arma vs. canalizador arcano), el `archivo` de la ref es obligatorio para
   desambiguar — `buscar.equipo()` lo usa si se lo pasas.
2. `calculado` se recalcula desde cero a partir del resto de la ficha y se
   compara con lo escrito; si no coincide, es un error — nadie debería
   haberlo editado a mano.
3. Las habilidades elegidas deben estar dentro de lo permitido por
   `atributos_basicos.habilidades` de la clase (respetando el flag
   `cualesquiera`, ver `clases/_ESQUEMA_atributos_basicos.md`) y por el
   trasfondo. **`cualesquiera: true` amplía la lista a las 18 habilidades
   canónicas de `reglas/habilidades.yaml` — no la elimina.** Una habilidad
   inventada sigue siendo un error incluso con `cualesquiera`.
4. Si `metodo: compra_puntos`, la suma de costes de `base` debe dar 27.
4ter. A partir del nivel 2, `pg_por_nivel` es **obligatorio** y debe tener una
   entrada por cada nivel, del 1 al `nivel_total`. Sin él, el verificador
   **se niega** en vez de suponer un método: no es un dato que se pueda deducir.
   El «mínimo de 1» del paso 2 se aplica al **total** (valor + mod. Con), no al
   dado; si algún nivel lo toca, el verificador **avisa**, porque la base no
   resuelve cómo interactúa eso con la regla retroactiva del paso 5.
4bis. `calculado.ca` y `calculado.pg_max` los agrega **`efectos.py`** a partir
   de los efectos citados en los rasgos que el personaje tiene (especie, clase
   hasta su nivel, subclase, equipo). Ya no hay casos cableados por nombre de
   clase: ver `reglas/_ESQUEMA_efectos.md`.
5. Ningún campo fuera de la prosa libre listada arriba y de
   `decisiones[].cita` puede contener un fragmento de más de ~15 palabras:
   eso es señal de que se copió texto en vez de referenciarlo.
6. `competencias.armas`/`.armaduras`/`.herramientas` van como `categoria:`
   (texto literal), no como `ref:` — se comprueban contra la lista real de
   `atributos_basicos` de la clase (o del trasfondo cuando aplique), no
   contra `equipo/`.
