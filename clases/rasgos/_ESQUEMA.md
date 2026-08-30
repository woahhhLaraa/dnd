# Esquema de `clases/rasgos/<clase>.yaml` (Fase 10)

Un archivo por clase, con el **texto** de los rasgos del tronco de la clase
(los de subclase ya viven en `clases/subclases/<clase>.yaml`).

Motivo: `clases/<clase>.yaml` solo tiene los **nombres** de los rasgos en
`progresion[].rasgos[]`. Sin el texto, un LLM orquestador rellena el hueco
con reglas de 2014. Ver `FODA.md`.

```yaml
clase: Bárbaro                 # exactamente igual que el campo 'clase' de clases/barbaro.yaml
edicion: "2024 (5.5e)"
fuente: {archivo: "Manual_del_Jugador_2024.pdf"}
verificado: {metodo: "vision-directa", fecha: "2026-08-19"}
fidelidad: condensado          # 'literal' si se transcribe palabra por palabra; 'condensado' si se resume
rasgos:
  - nombre: "Furia"            # IDÉNTICO al string que aparece en progresion[].rasgos[] de la clase
    nivel: 1                   # el nivel en que la tabla de la clase lo concede
    pagina: {pdf: 55, libro: 53}
    desc: "…"                  # mecánica completa: costes, usos, CD, duración, escalado
```

## Reglas

1. `nombre` debe coincidir **carácter a carácter** con el string de
   `progresion[].rasgos[]` de `clases/<clase>.yaml`, tildes y paréntesis
   incluidos (p. ej. `"Acción súbita (dos usos)"`). `validar.py` cruza ambas
   listas en las dos direcciones y falla si sobra o falta uno.
2. `nivel` debe ser el nivel en que esa tabla lo concede.
3. **No se transcriben** los marcadores `"Mejora de característica"`,
   `"Subclase de <clase>"` ni `"Rasgo de subclase"`: no son rasgos con texto
   propio.
4. Cuando un rasgo aparece en varios niveles con variantes numeradas
   (`"Acción súbita (un uso)"` / `"(dos usos)"`), cada variante es su propia
   entrada, con su nivel.
5. `desc` debe bastarse sola para arbitrar: si el rasgo tiene una CD, un
   número de usos, una duración o un escalado por nivel, va dentro. Si remite
   a una columna de la tabla de la clase, dilo explícitamente
   (p. ej. "tantos d6 como indica la columna Ataque furtivo").
6. Regla inviolable del proyecto: **consultar, no recordar**. Todo sale de la
   página; sin página, el rasgo no entra. Si algo no se lee con claridad, se
   marca `desc: null` y se anota en `_DUDAS.md`, nunca se rellena de memoria.
