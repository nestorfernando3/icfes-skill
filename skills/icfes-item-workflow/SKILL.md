---
name: icfes-item-workflow
description: Build, critique, revise, and export ICFES-style item packages from grounded content sources for docentes/evaluadores.
---

# ICFES Item Workflow Skill

Use this skill when user wants to create, improve, review, batch-generate, or export ICFES-style single-answer multiple-choice items.

## Inputs

Required:

- Content source: lecture, reading, existing item, rubric, image, table, graph, or equivalent material.
- Item goal or target, unless clearly inferable from source.

Optional:

- Desired number of items.
- Target difficulty.
- Area/asignatura.
- Competency/evidence.
- Classroom vs formal Saber/ICFES bank use.

If no content source exists, stop and ask for one.

## Workflow

1. Inspect sources first.
   - Extract source refs by file, page/slide/section if available.
   - For weak extraction or visual interpretation, create `source_summary` and set lower confidence.

2. Infer item targets.
   - Identify area, competency, evidence, source content, target difficulty.
   - List grounded assumptions.

3. Ask blocking questions only if needed.
   - Group up to 3 questions for batch work.
   - Do not ask pre-scan questionnaires.

4. Draft in batch waves.
   - Default wave size: 5 items.
   - For requests above 5, complete waves of 5 and summarize after each wave.

5. Run self-critique pass.
   - Apply all quality gates.
   - Revise draft before showing user.
   - Keep warnings visible.

6. Output Review Markdown first.
   - Use `templates/item-package.md`.
   - Spanish prose and labels.
   - English snake_case keys where machine fields appear.

7. Export Author JSON when requested.
   - Use `templates/item-package.schema.json`.
   - Export array of item packages.
   - Include `student_view` without clave, rationales, quality gates, or revision notes.

## Quality Gates

- `source_grounding`
- `evidence_alignment`
- `context_sufficiency`
- `enunciado_clarity`
- `option_quality`
- `difficulty_fit`

An item can be `ready` only when all gates pass. Otherwise status is `draft`. Draft export with warnings is allowed.

## Output Contract

Each item package must include:

- `item_id`
- `status`
- `source_refs`
- `source_summaries`
- `grounded_assumptions`
- `alignment`
- `difficulty`
- `context`
- `enunciado`
- `options`
- `clave`
- `distractor_rationales`
- `quality_gates`
- `warnings`
- `revision_notes`
- `student_view`

## Review Stance

Be strict. Flag unsupported claims, ambiguous enunciados, weak distractors, multiple plausible claves, cueing, irrelevant context, and difficulty mismatch.
