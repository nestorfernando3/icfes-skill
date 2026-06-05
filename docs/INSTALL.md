# Instalacion

## Opcion Recomendada: Apuntar Al Repo

No requiere Homebrew. Requiere `git`.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --repo https://github.com/nestorfernando3/icfes-skill.git
```

Instala/actualiza repo en:

```text
~/.icfes-skill/repo
```

Luego abre selector TUI.

## One-Line Con Targets

Global para Codex y Claude:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --repo https://github.com/nestorfernando3/icfes-skill.git --target "codex,claude" --scope user
```

Por proyecto:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --repo https://github.com/nestorfernando3/icfes-skill.git --target "codex,claude,opencode" --scope project --project /ruta/proyecto
```

## Homebrew

```bash
brew tap nestorfernando3/icfes-skill
brew install icfes-skill
icfes-skill install
```

Desde bootstrap:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --homebrew
```

## Selector TUI

Primero elige alcance:

```text
global  - instalar para todos los proyectos
current - instalar en proyecto actual
other   - instalar en otro proyecto
doctor  - verificar paquete
exit
```

Luego elige IDE/agente:

```text
Flechas/j/k = mover
Espacio = marcar/desmarcar
Enter = instalar
a = todos
n = ninguno
q = salir
```

Targets soportados:

```text
codex claude gemini cursor windsurf opencode kiro aider goose zed vscode cline roo continue trae augment amp agents
```

## Rutas

Global:

```text
~/.codex/skills/icfes-item-workflow
~/.claude/skills/icfes-item-workflow
~/.gemini/skills/icfes-item-workflow
~/.config/opencode/skills/icfes-item-workflow
~/.kiro/skills/icfes-item-workflow
~/.config/goose/skills/icfes-item-workflow
~/.agents/skills/icfes-item-workflow
```

Proyecto:

```text
.agents/skills/icfes-item-workflow
.claude/skills/icfes-item-workflow
.opencode/skills/icfes-item-workflow
.kiro/skills/icfes-item-workflow
.goose/skills/icfes-item-workflow
agents/icfes-item-coach.md
```

Targets que comparten `.agents` se agrupan. Skill se copia una sola vez por ruta.

## Verificacion

```bash
icfes-skill doctor
```

Desde repo:

```bash
~/.icfes-skill/repo/setup --target codex --scope user
```

## Actualizar

Repo directo:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nestorfernando3/icfes-skill/main/install.sh)" -- --repo https://github.com/nestorfernando3/icfes-skill.git
```

Homebrew:

```bash
brew update
brew upgrade icfes-skill
```
