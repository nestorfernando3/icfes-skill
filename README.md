# ICFES Skill

Skill en español para crear, criticar, revisar y exportar paquetes de items estilo ICFES/Saber desde fuentes grounded: lecturas, clases, tablas, graficas, imagenes o rubricas.

## Instalar con Homebrew

Cuando repo tenga release:

```bash
brew tap nestorfernando3/icfes-skill
brew install icfes-skill
icfes-skill install
```

Mientras desarrollas desde repo local:

```bash
git clone https://github.com/nestorfernando3/icfes-skill.git
cd icfes-skill
./setup
```

## Instalar global

Codex:

```bash
./setup --target codex --scope user
```

Claude:

```bash
./setup --target claude --scope user
```

## Instalar por proyecto

Codex/Gemini/Cursor compatible:

```bash
./setup --target codex --scope project --project /ruta/del/proyecto
```

Esto copia el skill a:

```text
/ruta/del/proyecto/.agents/skills/icfes-item-workflow
```

Claude:

```bash
./setup --target claude --scope project --project /ruta/del/proyecto
```

Esto copia el skill a:

```text
/ruta/del/proyecto/.claude/skills/icfes-item-workflow
```

## Uso

Pide al agente:

```text
Usa icfes-item-workflow. Fuente: [archivo/lectura/imagen]. Crea 5 items de lectura critica, dificultad media. Exporta review markdown.
```

El skill exige fuente de contenido. Si no hay fuente, agente debe pedirla.

## Contenido

- `skills/icfes-item-workflow/SKILL.md`: workflow principal.
- `skills/icfes-item-workflow/templates/item-package.md`: plantilla review.
- `skills/icfes-item-workflow/templates/item-package.schema.json`: schema JSON autor.
- `agents/icfes-item-coach.md`: agente coach/evaluador.
- `icfes_question_generator.py`: generador auxiliar.
- `setup`: instalador TUI.
- `bin/icfes-skill`: CLI instalado por Homebrew.

## Publicar Homebrew

1. Crear repo GitHub, subir codigo.
2. Crear tag:

```bash
git tag v0.1.0
git push origin main --tags
```

3. Descargar tarball y calcular SHA:

```bash
curl -L -o icfes-skill-v0.1.0.tar.gz https://github.com/<usuario>/icfes-skill/archive/refs/tags/v0.1.0.tar.gz
shasum -a 256 icfes-skill-v0.1.0.tar.gz
```

4. Reemplazar `homepage`, `url`, `sha256` en `Formula/icfes-skill.rb` si cambia repo o tag.
5. Crear tap Homebrew `homebrew-icfes-skill` con formula, o usar:

```bash
brew install --build-from-source ./Formula/icfes-skill.rb
```

## Licencia

MIT.
