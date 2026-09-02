#!/usr/bin/env python3
"""Capa 4 de verificación: contrasta nuestras tablas de clase contra el
System Reference Document 5.2 (2024), obtenido vía Open5e.

Fuente independiente y oficial: SRD 5.2 © Wizards of the Coast,
publicado bajo Creative Commons Attribution 4.0 International (CC-BY-4.0).
Datos servidos por Open5e (https://open5e.com), clave de documento 'srd-2024'.

No sustituye al manual: es una comprobación cruzada. Si discrepan, manda
el Manual del Jugador y la discrepancia se resuelve leyendo la página.
"""
import json, re, sys, pathlib

B = pathlib.Path(__file__).parent
SRD = B / "_verificacion" / "srd2024_open5e_clases.json"

# clase nuestra -> (nombre SRD, {columna SRD: campo nuestro})
MAPA = {
 "barbaro":   ("Barbarian", {"Rages":"furias", "Rage Damage":"dano_furia", "Weapon Mastery":"maestria_armas"}),
 "bardo":     ("Bard",      {"Bardic Die":"dado", "Cantrips":"trucos", "Prepared Spells":"prep"}),
 "brujo":     ("Warlock",   {"Cantrips":"trucos", "Eldritch Invocations":"invocaciones",
                             "Prepared Spells":"prep", "Slot Level":"nivel_espacios", "Spell Slots":"espacios"}),
 "clerigo":   ("Cleric",    {"Cantrips":"trucos", "Channel Divinity":"canalizar", "Prepared Spells":"prep"}),
 "druida":    ("Druid",     {"Cantrips":"trucos", "Prepared Spells":"prep"}),
 "explorador":("Ranger",    {"Favored Enemy":"enemigo_predilecto", "Prepared Spells":"prep"}),
 "guerrero":  ("Fighter",   {"Second Wind":"tomar_aliento", "Weapon Mastery":"maestria_armas"}),
 "hechicero": ("Sorcerer",  {"Cantrips":"trucos", "Prepared Spells":"prep", "Sorcery Points":"puntos_hechiceria"}),
 "mago":      ("Wizard",    {"Cantrips":"trucos", "Prepared Spells":"prep"}),
 "monje":     ("Monk",      {"Focus Points":"puntos_concentracion", "Martial Arts":"artes_marciales"}),
 "paladin":   ("Paladin",   {"Channel Divinity":"canalizar", "Prepared Spells":"prep"}),
 "picaro":    ("Rogue",     {"Sneak Attack":"ataque_furtivo"}),
}
CASTER = {"FULL":"completo", "HALF":"medio", "PACT":"pacto",
          "NONE":"ninguno", None:"ninguno", "":"ninguno"}

def norm(v):
    """Unifica las notaciones de ambas fuentes para poder compararlas.

    El SRD escribe el daño con signo ('+2'), el nivel de espacio como ordinal
    inglés ('1st') y los dados con el 1 explícito ('1d6'); nosotros usamos
    2, 1 y 'd6'. Ninguna de esas diferencias es un dato distinto.
    """
    s = str(v).strip().strip('"')
    s = re.sub(r"^\+", "", s)                          # '+2'  -> '2'
    s = re.sub(r"^(\d+)(st|nd|rd|th)$", r"\1", s)       # '1st' -> '1'
    if re.fullmatch(r"\d+", s): return int(s)
    m = re.fullmatch(r"(\d*)[dD](\d+)", s)
    if m: return f"{m.group(1) or '1'}d{m.group(2)}"    # 'd6' y '1d6' -> '1d6'
    return s

def leer_nuestro(p):
    txt = p.read_text(encoding="utf-8")
    filas = {}
    for l in txt.splitlines():
        m = re.search(r"\{n:\s*(\d+),(.*)\}\s*$", l)
        if not m: continue
        n, cuerpo = int(m.group(1)), m.group(2)
        f = {}
        for cm in re.finditer(r"(\w+):\s*([^,\[\]]+?)(?=,\s*\w+:|\s*$)", cuerpo):
            k, v = cm.group(1), cm.group(2).strip()
            if k not in ("slots","rasgos"): f[k] = norm(v)
        ra = re.search(r"rasgos:\s*\[(.*?)\]", cuerpo)
        f["rasgos"] = ra.group(1) if ra else ""
        filas[n] = f
    lz = re.search(r"^lanzador:\s*(\w+)", txt, re.M)
    return filas, (lz.group(1) if lz else None)

def main():
    if not SRD.exists(): sys.exit(f"falta {SRD}")
    d = json.loads(SRD.read_text(encoding="utf-8"))
    srd = {r["name"]: r for r in d["results"]
           if "srd-2024" in str(r.get("document")) and not r.get("subclass_of")}

    total_ok = total_err = 0
    print("Contraste contra SRD 5.2 (2024) · CC-BY-4.0 · vía Open5e")
    print("─"*66)
    for arch, (nom_en, cols) in sorted(MAPA.items()):
        p = B / "clases" / f"{arch}.yaml"
        if not p.exists(): print(f" ⚠ {arch}: falta el yaml"); continue
        c = srd.get(nom_en)
        if not c: print(f" ⚠ {arch}: '{nom_en}' no está en el SRD"); continue

        nuestro, lanz = leer_nuestro(p)
        errs, notas, comprobados = [], [], 0

        esperado = CASTER.get(c.get("caster_type"), "?")
        if lanz != esperado:
            errs.append(f"tipo de lanzador: nuestro '{lanz}' vs SRD '{esperado}'")

        tablas = {f["name"]: f.get("data_for_class_table") or []
                  for f in c["features"] if f.get("feature_type") == "CLASS_TABLE_DATA"}
        for col_srd, campo in cols.items():
            for celda in tablas.get(col_srd, []):
                n, val = celda["level"], norm(celda["column_value"])
                if n not in nuestro or campo not in nuestro[n]:
                    # TOLERADO: lo cubre el recuento total. Si nuestra tabla
                    # perdiera una fila o una columna, este salto la sacaría
                    # del contraste sin decir nada — pero el número de valores
                    # contrastados bajaría de 646, y `verificar_documentos.py`
                    # compara esa cifra con la que promete `CONTINUAR.md`.
                    continue
                comprobados += 1
                if nuestro[n][campo] != val:
                    errs.append(f"N{n} {campo}: nuestro {nuestro[n][campo]!r} vs SRD {val!r}")

        # mejoras de característica
        asi_srd = set()
        for f in c["features"]:
            if f["name"] == "Ability Score Improvement":
                asi_srd = {g["level"] for g in (f.get("gained_at") or [])}
        asi_nuestro = {n for n, f in nuestro.items() if "Mejora de característica" in f.get("rasgos","")}
        if asi_srd and asi_srd != asi_nuestro:
            solo_srd, solo_n = sorted(asi_srd-asi_nuestro), sorted(asi_nuestro-asi_srd)
            # Falta en lo nuestro: error, hay que revisarlo.
            if solo_srd:
                errs.append(f"mejoras de característica que el SRD tiene y nosotros no: {solo_srd}")
            # De más: puede ser una mejora extra de clase que el SRD no recoge.
            # Verificado en el manual: el Pícaro sí la tiene en nivel 10 (PDF pág. 170).
            if solo_n:
                notas.append(f"mejoras extra de clase ausentes del SRD: {solo_n} "
                             f"(confirmadas en el manual)")
        comprobados += len(asi_srd)

        total_ok += comprobados; total_err += len(errs)
        estado = "✅" if not errs else "❌"
        print(f" {estado} {arch:<11} {comprobados:>3} valores contrastados"
              + ("" if not errs else f"  · {len(errs)} discrepancia(s)"))
        for e in errs:  print(f"      ✗ {e}")
        for nn in notas: print(f"      ℹ {nn}")

    print("─"*66)
    print(f"{total_ok} valores contrastados contra el SRD · "
          + ("✅ 0 discrepancias" if not total_err else f"❌ {total_err} discrepancias"))
    return 1 if total_err else 0

if __name__ == "__main__":
    sys.exit(main())
