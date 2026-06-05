# Changelog

## v0.1.14

- Installer puede ejecutarse via `bash -c "$(curl ...)"`.
- Installer repo-first clona/actualiza desde `--repo`.
- Homebrew queda como modo opcional con `--homebrew`.

## v0.1.13

- Agrega instalacion apuntando al repo.
- Agrega `--install-dir` para elegir cache local del repo.

## v0.1.12

- Normaliza targets antes de validar.
- Endurece input con espacios o retornos invisibles.

## v0.1.11

- Selector checkbox interactivo.
- Espacio marca/desmarca, Enter instala.

## v0.1.10

- Agrupa instalaciones por ruta destino.
- Evita copias repetidas cuando targets comparten `.agents`.

## v0.1.9

- Lista extendida de IDEs/agentes.

## v0.1.8

- Permite seleccionar multiples IDEs.

## v0.1.0-v0.1.7

- Primer Homebrew tap.
- CLI `icfes-skill`.
- TUI base.
- Instalacion global/proyecto.
