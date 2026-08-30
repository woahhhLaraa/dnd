# Hallazgos — Dracónido / Hechicero / Comerciante (ronda 3)

## 1. Qué funcionó bien

- Las tres precondiciones (`validar.py`, `verificar_srd.py`, `cobertura.py`) pasaron limpio
  antes de empezar (0 errores, 0 discrepancias, 0 preguntas sin cubrir).
- `buscar.py clase Hechicero` devolvió `atributos_basicos` completo (salvaciones,
  habilidades a elegir, armas, equipo_inicial A/B, progresión con `lanzador: completo` y
  `aptitud_magica: Carisma`) — todo lo necesario sin tocar conocimiento propio.
- `buscar.py equipo <nombre>` resolvió sin `--archivo` para "Lanza" y "Daga" pese a que
  ambos nombres aparecen (como subcadena) en más de un fichero de `equipo/`
  (p.ej. "Lanza de caballería" también vive en armas.yaml) — el desambiguador
  solo exige `--archivo` cuando hay de verdad dos *registros* con el mismo `nombre:`,
  no cuando el texto coincide como subcadena en otra entrada. Comportamiento correcto,
  y coherente con lo que pedía la tarea.
- El flujo de rasgos elegidos de especie (linaje dracónico → color → resistencia al daño)
  encajó bien en `especie.rasgos_elegidos`, siguiendo el patrón que se corrigió en rondas
  anteriores.
- Los cálculos de `calculo.py` (`pg`, `ca`, `pb`, `cd-conjuros`, `ataque-conjuros`)
  funcionaron sin fricción para un lanzador Carisma nivel 1.
- `verificar_personaje.py` llegó a 0 problemas tras una sola corrección (ver bug abajo).

## 2. Bugs o comportamientos raros

**Único hallazgo real: sensibilidad a mayúsculas/minúsculas en competencias.herramientas
vs. el campo `herramienta` del trasfondo.**

Comando:
```
python3 verificar_personaje.py personajes/draconido_hechicero.yaml
```
Salida (antes de corregir):
```
17 referencias comprobadas.
❌ 1 problemas:
  ✗ competencias.herramientas: 'Herramientas de navegante' no está en lo que conceden
    las clases (ni el trasfondo, si aplica) del personaje (['herramientas de navegante'])
```
Causa: `trasfondos/trasfondos.yaml#Comerciante.herramienta` guarda el texto en minúsculas
("herramientas de navegante"), pero el nombre canónico del objeto en
`equipo/herramientas.yaml` está en mayúscula inicial ("Herramientas de navegante"). Yo
escribí `categoria:` copiando la capitalización del objeto de equipo (hábito razonable,
ya que en el resto de la ficha todo lo demás sigue Title Case), y el verificador comparó
con distinción de mayúsculas contra el texto literal del trasfondo, así que falló.
Corregido bajando el `categoria:` a minúsculas exactas del trasfondo. Esto **no es un
bug del verificador** (hace exactamente lo que dice el esquema: comparar contra el texto
literal), pero sí es una inconsistencia de la base: `trasfondos.yaml` no capitaliza el
nombre de la herramienta igual que `equipo/herramientas.yaml` lo hace como objeto. No lo
toqué (está bajo `trasfondos/`, fuera de lo permitido), solo lo anoto.

Ningún otro bug encontrado. Los pasos de especie (Dracónido con elección de linaje),
trasfondo (Comerciante con habilidades fijas), y clase lanzadora completa (Hechicero)
funcionaron todos según lo documentado.

## 3. Documentación confusa

- El ejemplo `_ejemplo_aerin.yaml` (Brujo/Noble) **no incluye en `equipo:` los objetos
  del `equipo_inicial` del trasfondo** (perfume, ropas de calidad, juego de Noble), solo
  los de la clase — aunque `SKILL.md` Paso 7 dice explícitamente "Ofrece la opción A... y
  lo mismo para el trasfondo", y las `decisiones[]` de Aerin tampoco citan la opción de
  equipo del trasfondo. No es un error que rompa nada (el verificador no exige que el
  equipo del trasfondo esté presente), pero como ejemplo canónico de referencia induce a
  omitir ese equipo. Yo sí incluí los objetos de trasfondo (herramientas de navegante,
  2 bolsas, ropas de viaje) siguiendo el texto de SKILL.md en vez del ejemplo.
- El esquema no define ningún campo para las monedas de oro sueltas del equipo inicial
  (p.ej. los "28 po" de la opción A del Hechicero o los "22 po" del Comerciante). Ninguno
  de los personajes existentes en `personajes/` registra dinero tampoco, así que asumí
  que es un hueco intencional (fuera del alcance de nivel 1) y no inventé un campo.

## 4. Huecos de datos

Ninguno bloqueante. Todo lo necesario para Dracónido + Hechicero + Comerciante nivel 1
estaba presente: linaje dracónico con tabla de colores/daño, atributos_basicos de
Hechicero, conjuros filtrables por clase y nivel, y equipo sin ambigüedades una vez
usado `--archivo` donde hacía falta.

## 5. Salida final de verificar_personaje.py

```
17 referencias comprobadas.
✅ FICHA VERIFICADA — 0 problemas
```
