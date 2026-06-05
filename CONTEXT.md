# ICFES Item Construction

This context defines domain language for designing ICFES-style single-answer multiple-choice items from an evidence-centered assessment frame.

## Language

**Item Construction Workflow**:
End-to-end process that drafts, critiques, revises, and exports an ICFES-style item with its evidence alignment and review notes.
_Avoid_: generator-only flow, question maker

**ICFES Item Coach**:
Agent role that guides Docente/Evaluador through evidence-centered item construction, asks Blocking Questions, critiques drafts, and assigns Draft Item or Ready Item status.
_Avoid_: autonomous answer generator

**ICFES Item Workflow Skill**:
Reusable workflow that scans Content Sources, drafts Item Packages, applies Quality Gates, supports revision, and exports Review Markdown with optional JSON.
_Avoid_: agent persona, Python-only generator

**Project-Local Artifact**:
Agent or Skill file kept inside this project for refinement before any global installation.
_Avoid_: global skill install, shared package

**ICFES-Style Item**:
A single-answer multiple-choice assessment unit with context, enunciado, four options, one clave, and three distractors.
_Avoid_: quiz question, prompt, exercise

**Classroom Item**:
ICFES-style item intended for teaching, practice, or local assessment where unavailable official alignment fields may remain blank.
_Avoid_: formal item bank entry

**Formal ICFES Bank Item**:
ICFES-style item intended for formal bank use, where missing official alignment fields should be warned about.
_Avoid_: classroom draft

**Docente/Evaluador**:
Subject-matter expert who knows the taught content and uses the workflow to apply ICFES item-design discipline.
_Avoid_: student, autonomous item factory

**Content Source**:
Lecture, reading, existing item, rubric, image, table, graph, or other material that grounds the item content.
_Avoid_: unsupported topic idea, invented curriculum

**Source Reference**:
Pointer from an Item Package to the Content Source segment that supports it, such as file name, page, slide, section, or summarized visual evidence.
_Avoid_: bibliography-only citation, unsupported claim

**Source Summary**:
Lower-confidence Source Reference based on extracted or interpreted content when exact text is unavailable or incomplete.
_Avoid_: exact citation, hidden visual inference

**Grounded Assumption**:
An explicit inference made from available Content Sources when a needed detail is not stated directly.
_Avoid_: hallucination, hidden assumption

**Blocking Question**:
Follow-up question asked only when missing or conflicting information would change item validity.
_Avoid_: curiosity question, pre-scan questionnaire

**Batch Elaboration**:
Creation or revision of multiple ICFES-style items from one or more Content Sources in a single workflow run.
_Avoid_: bulk generation without review

**Batch Wave**:
Review-sized group of up to five Item Packages within Batch Elaboration.
_Avoid_: unbounded batch dump

**Self-Critique Pass**:
Internal review step where a draft Item Package is checked against Quality Gates and revised before being shown to the Docente/Evaluador.
_Avoid_: first draft as final

**Item Package**:
Reviewable unit for one ICFES-style item, including source references, assumptions, evidence alignment, item text, answer key, distractor rationales, and revision notes.
_Avoid_: plain question text

**Review Markdown**:
Primary human-readable output format for Item Packages.
_Avoid_: final-only JSON, opaque export

**Author JSON**:
Optional machine-readable export containing full Item Packages, including answer keys and rationales.
_Avoid_: student-facing export

**Student View**:
Learner-facing representation of an ICFES-style item without clave, distractor rationales, quality gates, or revision notes.
_Avoid_: author review package

**English Snake Case Keys**:
Machine-facing field names written in English snake_case while human-facing prose and labels remain in Spanish.
_Avoid_: mixed ad hoc keys, Spanish JSON keys

**Quality Gate**:
Criterion that an Item Package must satisfy before it can be marked ready.
_Avoid_: optional suggestion, style preference

**Ready Item**:
Item Package that passes all Quality Gates and can be used as approved assessment material.
_Avoid_: draft, unchecked item

**Draft Item**:
Item Package that may be exported for review but has unresolved warnings or failed Quality Gates.
_Avoid_: ready item

## Example Dialogue

Dev: "Should the tool only generate options?"
Domain expert: "No. It must guide the full item construction workflow: draft, critique, revise, then export the ICFES-style item with evidence alignment."

Dev: "What is the Agent?"
Domain expert: "The ICFES Item Coach: the role that guides, critiques, asks Blocking Questions, and decides whether an Item Package is draft or ready."

Dev: "What is the Skill?"
Domain expert: "The ICFES Item Workflow Skill: the reusable workflow for source scanning, batch drafting, quality gates, revision, and export."

Dev: "Should this be installed globally now?"
Domain expert: "No. Keep Agent and Skill as Project-Local Artifacts until tested."

Dev: "Must every item include componente and afirmacion?"
Domain expert: "Only when required for a Formal ICFES Bank Item. Classroom Items may leave unavailable official fields blank."

Dev: "Can the agent decide subject truth on its own?"
Domain expert: "No. The Docente/Evaluador provides or approves the content truth; the agent enforces item-design discipline."

Dev: "Can the workflow draft from only a topic name?"
Domain expert: "No. It needs a Content Source. It may make Grounded Assumptions from available docs, but must flag them for approval."

Dev: "Can a diagram or weak PDF extraction support an item?"
Domain expert: "Yes, but mark it as a Source Summary with lower confidence."

Dev: "Should the workflow ask before reading the docs?"
Domain expert: "No. Inspect Content Sources first, then ask only Blocking Questions, grouped when working in batches."

Dev: "Can it make ten items from lectures and old questions?"
Domain expert: "Yes, as Batch Elaboration in Batch Waves of five, with follow-up questions when docs leave important gaps."

Dev: "Should the first draft be shown immediately?"
Domain expert: "No. Run a Self-Critique Pass first, then show the revised Draft Item with warnings."

Dev: "Should batch output go straight to JSON?"
Domain expert: "No. Review Markdown is primary; JSON export is optional after review."

Dev: "Should JSON hide the answer key?"
Domain expert: "Author JSON includes keys and rationales, but each Item Package also contains a Student View without them."

Dev: "Should export keys be Spanish?"
Domain expert: "No. Use English Snake Case Keys for code/export, with Spanish prose and review labels."

Dev: "Can an item with failed checks be marked ready?"
Domain expert: "No. It may remain a Draft Item with warnings, but a Ready Item must pass all Quality Gates."
