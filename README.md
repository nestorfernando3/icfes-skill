# ICFES Skill

Skill en español para crear, revisar y exportar items de seleccion multiple con unica respuesta, estilo ICFES/Saber, desde fuentes verificables: lecturas, clases, tablas, graficas, imagenes, rubricas o items existentes.

Repositorio principal: <https://github.com/nestorfernando3/icfes-skill>

Homebrew tap: <https://github.com/nestorfernando3/homebrew-icfes-skill>

## Para Que Sirve

`icfes-item-workflow` ayuda a docentes, evaluadores y equipos academicos a convertir material de clase o evaluacion en paquetes de items consistentes, trazables y revisables.

La utilidad central:

- Crear items desde una fuente, no desde intuicion suelta.
- Alinear item con area, competencia, evidencia y dificultad.
- Generar contexto, enunciado, opciones, clave y racionales.
- Revisar calidad antes de entregar: grounding, claridad, distractores, suficiencia del contexto, dificultad.
- Separar vista de estudiante (`student_view`) de vista de autor con clave/racionales.
- Exportar en Markdown para revision humana o JSON para flujos de autor/banco.

## Que Instala

Instala:

- Skill `icfes-item-workflow`.
- Templates de salida Markdown y JSON.
- Agente auxiliar `icfes-item-coach`.
- CLI `icfes-skill`.
- Instalador TUI `setup`.

No instala servicios, no deja procesos corriendo, no modifica proyectos salvo cuando pides instalacion por proyecto.

## Instalacion Recomendada

Con Homebrew:

```bash
brew tap nestorfernando3/icfes-skill
brew install icfes-skill
icfes-skill install
```

El ultimo comando abre menu TUI para elegir agente y alcance.

Menu:

```text
ICFES Skill Setup

1) global  - instalar para todos los proyectos
2) current - instalar en proyecto actual
3) other   - instalar en otro proyecto
4) doctor  - verificar paquete
5) exit

IDE:
1) Codex
2) Claude
3) Gemini
4) Cursor
5) Windsurf
6) OpenCode
7) Kiro
8) Aider
9) Goose
10) Zed
11) VS Code
12) Cline
13) Roo Code
14) Continue
15) Trae
16) Augment
17) Amp
18) .agents portable
```

En terminal interactiva, el selector usa checkbox:

```text
Flechas/j/k = mover
Espacio = marcar/desmarcar
Enter = instalar
a = todos
n = ninguno
q = salir
```

En modo no interactivo tambien puedes escoger varios:

```text
1,2,3,6
codex claude opencode
all
```

Cuando varios IDEs comparten la misma carpeta portable `.agents`, el instalador copia el skill una sola vez y muestra que targets apuntan a esa misma ruta.

## Instalacion En Un Comando

Mac con Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)"
```

Tambien puedes pasar opciones y evitar menu:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --target codex --scope user
```

Varios targets sin menu:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --target "codex,claude,opencode" --scope user
```

Por proyecto:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --target codex --scope project --project /ruta/del/proyecto
```

## Instalacion Global

Usa global cuando quieres tener skill disponible en cualquier conversacion/proyecto del mismo equipo.

Codex:

```bash
icfes-skill install --target codex --scope user
```

Claude:

```bash
icfes-skill install --target claude --scope user
```

Gemini:

```bash
icfes-skill install --target gemini --scope user
```

OpenCode:

```bash
icfes-skill install --target opencode --scope user
```

Kiro:

```bash
icfes-skill install --target kiro --scope user
```

Cursor/Windsurf usan instalacion portable `.agents`:

```bash
icfes-skill install --target cursor --scope user
icfes-skill install --target windsurf --scope user
```

Rutas globales usadas:

```text
~/.codex/skills/icfes-item-workflow
~/.claude/skills/icfes-item-workflow
~/.gemini/skills/icfes-item-workflow
~/.config/opencode/skills/icfes-item-workflow
~/.kiro/skills/icfes-item-workflow
~/.config/goose/skills/icfes-item-workflow
~/.agents/skills/icfes-item-workflow
```

## Instalacion Por Proyecto

Usa por proyecto cuando quieres versionar el skill dentro de un repo y compartirlo con equipo.

Codex/Gemini/Cursor compatible:

```bash
icfes-skill install --target codex --scope project --project /ruta/del/proyecto
```

Destino:

```text
/ruta/del/proyecto/.agents/skills/icfes-item-workflow
/ruta/del/proyecto/agents/icfes-item-coach.md
```

Claude:

```bash
icfes-skill install --target claude --scope project --project /ruta/del/proyecto
```

Destino:

```text
/ruta/del/proyecto/.claude/skills/icfes-item-workflow
/ruta/del/proyecto/agents/icfes-item-coach.md
```

## Instalacion Desde Git

Sin Homebrew:

```bash
git clone https://github.com/nestorfernando3/icfes-skill.git
cd icfes-skill
./setup
```

O modo no interactivo:

```bash
./setup --target codex --scope user
./setup --target codex --scope project --project /ruta/del/proyecto
```

## Comandos CLI

```bash
icfes-skill install
icfes-skill install --target codex --scope user
icfes-skill install --target codex --scope project --project .
icfes-skill where
icfes-skill doctor
```

Targets:

```text
codex
claude
gemini
cursor
windsurf
opencode
kiro
aider
goose
zed
vscode
cline
roo
continue
trae
augment
amp
agents
```

Scopes:

```text
user
project
```

## Uso Basico

Despues de instalar, pide al agente:

```text
Usa icfes-item-workflow. Fuente: lectura.pdf, paginas 2-4. Crea 5 items de lectura critica, dificultad media. Entrega review markdown.
```

Ejemplo con imagen o grafica:

```text
Usa icfes-item-workflow. Fuente: imagen adjunta con grafica de barras. Crea 3 items de interpretacion de datos para grado 9. Marca supuestos y warnings.
```

Ejemplo JSON:

```text
Usa icfes-item-workflow. Fuente: clase.md. Crea 5 items de ciencias naturales. Exporta Author JSON con student_view sin clave.
```

## Flujo Del Skill

1. Inspecciona fuente.
2. Extrae referencias por archivo, pagina, seccion, grafica o resumen.
3. Infiere area, competencia, evidencia y dificultad si fuente permite.
4. Hace maximo 3 preguntas bloqueantes si falta algo critico.
5. Redacta items en oleadas de 5.
6. Ejecuta autocritica con gates de calidad.
7. Revisa antes de mostrar.
8. Marca cada item como `ready` o `draft`.
9. Entrega Markdown de revision primero; JSON si se pide.

## Gates De Calidad

Cada item pasa por:

- `source_grounding`: afirmaciones trazables a fuente.
- `evidence_alignment`: item evalua competencia/evidencia, no trivia.
- `context_sufficiency`: contexto suficiente, sin carga irrelevante.
- `enunciado_clarity`: tarea unica, clara, no ambigua.
- `option_quality`: una clave, distractores plausibles, sin pistas.
- `difficulty_fit`: dificultad justificada.

Un item solo queda `ready` si todos los gates pasan. Si falla algo, queda `draft` con warnings.

## Contrato De Salida

Cada paquete incluye:

```text
item_id
status
source_refs
source_summaries
grounded_assumptions
alignment
difficulty
context
enunciado
options
clave
distractor_rationales
quality_gates
warnings
revision_notes
student_view
```

`student_view` oculta clave, racionales, gates y notas internas.

## Estructura Del Repo

```text
skills/icfes-item-workflow/SKILL.md
skills/icfes-item-workflow/templates/item-package.md
skills/icfes-item-workflow/templates/item-package.schema.json
agents/icfes-item-coach.md
icfes_question_generator.py
setup
bin/icfes-skill
Formula/icfes-skill.rb
```

## Verificacion

```bash
icfes-skill doctor
```

Salida esperada:

```text
OK: /ruta/del/paquete
```

Prueba instalacion por proyecto:

```bash
tmpdir=$(mktemp -d)
icfes-skill install --target codex --scope project --project "$tmpdir"
test -f "$tmpdir/.agents/skills/icfes-item-workflow/SKILL.md"
```

## Troubleshooting

`icfes-skill: command not found`

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Homebrew dice tap no confiable:

```bash
brew trust --formula nestorfernando3/icfes-skill/icfes-skill
```

Ver ruta instalada:

```bash
icfes-skill where
```

Reinstalar:

```bash
brew reinstall icfes-skill
icfes-skill install
```

## Desarrollo

Clonar:

```bash
git clone https://github.com/nestorfernando3/icfes-skill.git
cd icfes-skill
```

Validar:

```bash
bash -n setup bin/icfes-skill
ruby -c Formula/icfes-skill.rb
bin/icfes-skill doctor
```

Publicar nueva version:

```bash
git tag v0.1.2
git push origin main --tags
curl -L -o icfes-skill-v0.1.2.tar.gz https://github.com/nestorfernando3/icfes-skill/archive/refs/tags/v0.1.2.tar.gz
shasum -a 256 icfes-skill-v0.1.2.tar.gz
```

Luego actualizar `Formula/icfes-skill.rb`, copiar formula al tap `homebrew-icfes-skill`, commit y push.

## Licencia

MIT.
