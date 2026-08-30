# Fuentes de verificación independiente

Material de contraste. **No son autoridad**: si discrepan del Manual del Jugador,
manda el manual y la discrepancia se resuelve leyendo la página.

## SRD 5.2.1 (System Reference Document, reglas 2024)

© Wizards of the Coast. Publicado bajo **Creative Commons Attribution 4.0
International (CC-BY-4.0)**. Es material oficial y de uso libre con atribución.

- `srd52/` — texto completo del SRD 5.2.1 en Markdown
  (vía github.com/downfallx/dnd-5e-srd-markdown)
- `srd2024_open5e_clases.json` — las 12 clases y sus tablas nivel a nivel,
  ya estructuradas (vía api.open5e.com, clave de documento `srd-2024`)
- `foundry_srd52/` — **el mismo SRD 5.2, pero estructurado campo a campo** en
  YAML (vía github.com/foundryvtt/dnd5e, `packs/_source/*24`, sello
  `source.rules: "2024"` + `license: "CC-BY-4.0"`). Añadido el 2026-08-21.
  Donde `srd52/` obliga a parsear prosa, aquí los datos ya vienen en campos:
  352 conjuros, 679 objetos de equipo, 61 especies, 4 trasfondos, 21 dotes y
  las 12 clases con subclases. Los 352 conjuros cuadran con la cifra que ya
  figura en la tabla de cobertura de abajo — las dos copias del SRD coinciden.
  Análisis de qué se puede contrastar con esto: `../ANALISIS_REPOS.md`.

⚠️ **Al consultar api.open5e.com hay que filtrar SIEMPRE por
`document__key=srd-2024`.** Sin ese filtro la API devuelve por defecto
contenido de *Advanced 5th Edition* (documento `a5e-ag`), que es otro juego.
No falla: responde algo plausible y equivocado — el mismo género de fallo
silencioso que el bug `Clerigo`.

## Qué cubre y qué no

El SRD es un **subconjunto** del Manual del Jugador. Sirve para confirmar, nunca
para completar: lo que no está en él hay que leerlo del manual igualmente.

| Contenido | En el SRD | En nuestra base | Cobertura |
|---|---|---|---|
| Tablas de clase | 12 | 12 | **100 %** |
| Subclases | 12 (una por clase) | ~48 | 25 % |
| Especies | 9 (sin aasimar) | 10 | 90 % |
| Trasfondos | 4 | 16 | 25 % |
| Dotes | 17 | ~75 | ~23 % |
| Conjuros | 352 | 392 | 90 % |

## Resultado del contraste

`python3 verificar_srd.py` → **646 valores contrastados, 0 discrepancias**
en las 12 tablas de clase.

Hallazgo: el SRD **omite** la mejora de característica de nivel 10 del Pícaro,
que el manual sí recoge (PDF pág. 170, verificada visualmente). Es un hueco de
la fuente de contraste, no de la nuestra. Sirve de recordatorio de por qué el
manual manda.
