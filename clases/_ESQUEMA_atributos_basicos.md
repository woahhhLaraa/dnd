# Esquema del bloque `atributos_basicos` (Fase 11)

La página «Atributos básicos de \<clase\>» del manual tiene **siete filas**. En la
Fase 9 solo se transcribieron dos (característica principal y equipo inicial).
`cobertura.py` demostró que sin las otras cinco **no se puede construir una
ficha de nivel 1**: no hay PG, ni CA, ni salvaciones, ni habilidades.

Esta fase completa el bloque, en el mismo fichero `clases/<clase>.yaml` y sin
tocar nada más.

```yaml
atributos_basicos:
  fuente: {pagina_pdf: 53, pagina_libro: 51}     # ya está, no cambiarlo
  verificado: {metodo: "vision-directa", fecha: "2026-08-19"}
  caracteristica_principal: Fuerza               # ya está
  dado_golpe: d12                                # NUEVO — "1d12 por nivel" -> d12
  salvaciones: [Fuerza, Constitución]            # NUEVO — las dos de la fila
  habilidades:                                   # NUEVO
    elige: 2
    de: [Atletismo, Intimidación, Naturaleza, Percepción, Supervivencia, "Trato con animales"]
  armas: ["Armas sencillas", "Armas marciales"]  # NUEVO — literal de la fila
  armaduras: ["Armaduras ligeras", "Armaduras medias", Escudos]   # NUEVO
  herramientas: []                               # NUEVO — [] si la fila no existe o dice "Ninguna"
  equipo_inicial: {a: "...", b: "..."}           # ya está
```

## Reglas

1. **`[]` y «Ninguna» son respuestas válidas y completas.** Varias clases no
   tienen entrenamiento con armaduras (Mago, Hechicero, Monje) ni competencia
   con herramientas. El campo debe **existir** aunque esté vacío: lo que deja
   al LLM improvisando es que falte, no que esté vacío.
2. `dado_golpe` en la forma `d6`/`d8`/`d10`/`d12`, sin el `1` delante.
3. `habilidades.de` debe contener habilidades de las 18 canónicas, escritas
   exactamente como en `reglas/habilidades.yaml`. `habilidades.elige` es el
   número que dice la fila («Elige dos» → 2).
   **Cuando la fila no enumera** («Elige tres cualesquiera», Bardo) se añaden
   dos campos más: `literal` con la cita exacta de la fila y `cualesquiera:
   true`. `de` se rellena entonces con las 18 habilidades, pero como
   *conveniencia para el script, no como restricción de la clase*: sin
   `literal` un auditor no puede saber qué cita la base, y sin `cualesquiera`
   un lector confundiría la expansión con una lista cerrada del manual.
4. `armas`, `armaduras` y `herramientas` recogen **lo que dice la fila**, sin
   expandir: «Armas sencillas» se queda así, no se listan las armas una por
   una (para eso está `equipo/armas.yaml`).
5. No inventes: si una fila no se lee con claridad, se marca y se pregunta.
   Sin página, un dato no entra.

## Ficheros nuevos de esta fase

- `reglas/habilidades.yaml` — las 18 habilidades y su característica:
  ```yaml
  fuente: {archivo: "Manual_del_Jugador_2024.pdf", pagina_pdf: NN, pagina_libro: NN}
  verificado: {metodo: "vision-directa", fecha: "..."}
  habilidades:
    - {nombre: "Acrobacias", caracteristica: Destreza, desc: "..."}
  ```
- `reglas/idiomas.yaml` — tablas «Idiomas estándar» e «Idiomas inusuales»
  (pdf 39 = libro 37):
  ```yaml
  estandar: [{nombre: "Común", origen: "Sigil"}, ...]
  inusuales: [{nombre: "Abisal", origen: "Demonios del Abismo"}, ...]
  ```
- `equipo/municion.yaml` — la tabla «Munición» como registros consultables, no
  como prosa (la fabrica el otro agente a partir de lo ya transcrito).
- La tabla «Progreso de los personajes» (PX por nivel) va dentro de
  `reglas/generacion_personaje.yaml`, bajo `px_por_nivel`.
