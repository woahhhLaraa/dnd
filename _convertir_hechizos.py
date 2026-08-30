#!/usr/bin/env python3
"""Fase 1 — CSV de hechizos -> hechizos.json canónico.
Fuente: 'Hechizos Juntos - Hoja General.csv' (datos estructurados, sin OCR).
"""
import csv, json, re, sys, pathlib

B = pathlib.Path(__file__).parent
SRC = B / "_origen_hechizos.csv"
OUT = B / "hechizos.json"

ESCUELAS = ["abjuracion","conjuracion","adivinacion","encantamiento",
            "evocacion","ilusionismo","nigromancia","transmutacion"]
ESC_NOMBRE = {"abjuracion":"Abjuración","conjuracion":"Conjuración",
              "adivinacion":"Adivinación","encantamiento":"Encantamiento",
              "evocacion":"Evocación","ilusionismo":"Ilusionismo",
              "nigromancia":"Nigromancia","transmutacion":"Transmutación"}

# Correcciones verificadas contra el manual, con cita. El CSV dejó estos campos
# vacíos; NO se rellenan de memoria, solo tras leerlos en el PDF.
OVERRIDES = {
    "sanctasanctórum privado de mordenkainen": {
        "escuela": "Abjuración",
        "_verificado": "Manual_del_Jugador_2024.pdf pag_pdf=144, "
                       "tabla 'Conjuros de mago de nivel 4'",
    },
}

def b(v):  return (v or "").strip().upper() == "TRUE"
def s(v):  return re.sub(r"\s+"," ", (v or "").strip())

def alcance(txt):
    """'45 m / 150 f / 30 cas' -> {metros, pies, casillas}; 'Toque' -> literal."""
    t = s(txt)
    m = re.match(r"^([\d.,]+)\s*(m|km)\s*/\s*([\d.,]+)\s*f\s*/\s*([\d.,]+)\s*cas", t)
    if m:
        return {"texto": t, "metros": m[1] + (" km" if m[2]=="km" else ""),
                "pies": m[3], "casillas": m[4]}
    return {"texto": t}

def main():
    if not SRC.exists():
        sys.exit(f"falta {SRC}")
    filas = list(csv.DictReader(SRC.open(encoding="utf-8")))
    hechizos, vistos, dups = [], {}, []

    for f in filas:
        nombre = s(f["name"])
        if not nombre:
            continue
        clave = nombre.lower()
        if clave in vistos:
            dups.append(nombre); continue
        vistos[clave] = True

        nivel_raw = s(f["level"])
        nivel = 0 if nivel_raw.lower() == "truco" else int(nivel_raw)

        esc = [ESC_NOMBRE[e] for e in ESCUELAS if b(f[e])]
        ov = OVERRIDES.get(clave)
        if ov and not esc:
            esc = [ov["escuela"]]

        partes = [s(p) for p in (f["details"] or "").split("\n")]
        dur, alc, lanz = (partes + ["","",""])[:3]

        coste = s(f["cost"])
        clases = [c.strip() for c in (f["Clase del Hechizo"] or "").split(",") if c.strip()]

        hechizos.append({
            "nombre": nombre,
            "nombre_en": s(f["name_ingles"]),
            "nivel": nivel,
            "escuela": esc[0] if len(esc) == 1 else esc,
            "clases": sorted(clases),
            "tiempo_lanzamiento": lanz,
            "alcance": alcance(alc),
            "duracion": dur,
            "concentracion": b(f["concentration"]),
            "ritual": b(f["ritual"]),
            "componentes": {
                "verbal": b(f["verbal"]),
                "somatico": b(f["somatic"]),
                "material": b(f["material"]),
                "coste": None if coste in ("~","") else coste,
                "consume_material": b(f["gp"]),
            },
            "tirada": s(f["como_usar"]),
            "resumen": s(f["flavour"]),
            "descripcion": (f["description"] or "").strip(),
            "fuente": {"archivo": "Manual_del_Jugador_2024.pdf",
                       "pagina_libro": s(f["page"]).replace(" MdJ","")},
            **({"_nota_verificacion": ov["_verificado"]} if ov else {}),
        })

    hechizos.sort(key=lambda h: (h["nivel"], h["nombre"]))

    por_clase, por_nivel, sin_escuela, sin_pagina = {}, {}, [], []
    for h in hechizos:
        for c in h["clases"]:
            por_clase[c] = por_clase.get(c, 0) + 1
        por_nivel[h["nivel"]] = por_nivel.get(h["nivel"], 0) + 1
        if not h["escuela"] or isinstance(h["escuela"], list):
            sin_escuela.append(h["nombre"])
        if not h["fuente"]["pagina_libro"]:
            sin_pagina.append(h["nombre"])

    doc = {
        "_meta": {
            "edicion": "2024 (5.5e)",
            "fuente": "Hechizos Juntos - Hoja General.csv (datos estructurados)",
            "metodo": "conversion-directa (sin OCR)",
            "fecha": "2026-08-18",
            "total": len(hechizos),
            "por_clase": dict(sorted(por_clase.items())),
            "por_nivel": {("truco" if k==0 else str(k)): v for k,v in sorted(por_nivel.items())},
        },
        "hechizos": hechizos,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"✅ {len(hechizos)} hechizos -> {OUT.name}")
    print("   por nivel:", doc["_meta"]["por_nivel"])
    print("   por clase:", doc["_meta"]["por_clase"])
    if dups:        print(f"   ⚠ duplicados omitidos ({len(dups)}):", dups[:6])
    if sin_escuela: print(f"   ⚠ escuela ambigua ({len(sin_escuela)}):", sin_escuela[:6])
    if sin_pagina:  print(f"   ⚠ sin página ({len(sin_pagina)}):", sin_pagina[:6])

if __name__ == "__main__":
    main()
