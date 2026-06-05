"""
icfes_question_generator
=========================

This module provides helper classes and functions for the construction of
ICFES‑style multiple selection questions (also known as items) based on
principles extracted from official training materials.  The goal is to
simplify the work of educators when designing fair, evidence‑based
questions for standardized evaluations such as Saber PRO.

The guidelines implemented here stem from the Colombian national
assessment framework (Pruebas Saber) and emphasise three core
components: the **context**, a precise **enunciado** (question statement),
and four **options** from which a single correct answer (clave) must be
selected.  Distractors are carefully crafted to mirror common
misconceptions or typical errors without introducing ambiguous or
irrelevant information.

Key concepts incorporated in this module
---------------------------------------

* **Context** – A short scenario that introduces the problem and
  presents the relevant concept or tool required to solve it.  A good
  context confines the cognitive territory of the question so that
  students cannot answer based purely on prior opinions or speculation.

* **Enunciado** – The actual question asked of the student.  It should
  be propositional (asking what *should* be done or what is true) and
  contain only one conceptual category.  Compound questions with
  multiple categories are difficult to interpret and should be avoided.

* **Options** – Four possible answers labelled “A”, “B”, “C” and “D”.  One
  option is the **clave** (correct and sufficient), while the others
  serve as different types of distractors:
    - *Contradictoria*: contradicts the context or the logical
      resolution of the problem.
    - *Absurda*: clearly incorrect or irrelevant to the problem.
    - *Distractora*: superficially plausible but ultimately incorrect
      due to a conceptual or procedural error.

* **Difficulty levels** – Items can be classified as low, medium,
  high or superior difficulty according to how many variables they
  consider and how many test‑takers are expected to answer correctly:
    - *Low*: focuses on a single variable or familiar task; 70–100 % of
      students should answer correctly.
    - *Medium*: involves two variables or an interdisciplinary
      perspective; 30–70 % of students should answer correctly.
    - *High*: requires consideration of more than two variables or
      transdisciplinary reasoning; 10–30 % of students should answer
      correctly.
    - *Superior*: extremely challenging items answered correctly by
      fewer than 10 % of students.

For a deep dive into these principles, refer to the slides titled
"Diseño de especificaciones en instrumentos de evaluación" from the
Universidad Francisco de Paula Santander, which discuss evidence‑
centred design, the importance of balanced components, and the roles of
different response types【9†L21-L38】【9†L81-L89】.

Example
-------

>>> from icfes_question_generator import ICFESItem
>>> context = "Un estudiante tiene dificultades para leer gráficas y ..."
>>> enunciado = "Según la gráfica, ¿cuál es la tendencia principal ...?"
>>> options = [
...     "A. indica un crecimiento sostenido",  # clave
...     "B. representa un comportamiento errático",  # distractora
...     "C. demuestra una disminución abrupta",  # contradictoria
...     "D. no ofrece información relevante",  # absurda
... ]
>>> item = ICFESItem(context, enunciado, options, correct_index=0)
>>> print(item.render())
Un estudiante tiene dificultades para leer gráficas y ...

Según la gráfica, ¿cuál es la tendencia principal ...?

  A. indica un crecimiento sostenido
  B. representa un comportamiento errático
  C. demuestra una disminución abrupta
  D. no ofrece información relevante
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional


class DifficultyLevel(Enum):
    """Enumerated type representing the expected difficulty of an item."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SUPERIOR = "superior"


QUALITY_GATE_NAMES = [
    "source_grounding",
    "evidence_alignment",
    "context_sufficiency",
    "enunciado_clarity",
    "option_quality",
    "difficulty_fit",
]


OPTION_LABELS = ["A", "B", "C", "D"]


@dataclass
class SourceRef:
    """Grounding reference for an item package."""

    source_type: str
    file: str
    basis: str
    page: Optional[int] = None
    section: Optional[str] = None
    confidence: str = "medium"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type,
            "file": self.file,
            "page": self.page,
            "section": self.section,
            "basis": self.basis,
            "confidence": self.confidence,
        }


@dataclass
class SourceSummary:
    """Low/medium confidence summary used when direct extraction is weak."""

    summary: str
    confidence: str = "medium"

    def to_dict(self) -> Dict[str, str]:
        return {"summary": self.summary, "confidence": self.confidence}


@dataclass
class Alignment:
    """Evidence-centered alignment metadata."""

    area: str
    competency: str
    evidence: str
    component: Optional[str] = None
    claim: Optional[str] = None
    standard: Optional[str] = None
    grade_or_program: Optional[str] = None

    @classmethod
    def from_metadata(cls, metadata: Optional[Dict[str, str]]) -> "Alignment":
        metadata = metadata or {}
        return cls(
            area=metadata.get("area", ""),
            competency=metadata.get("competency", metadata.get("competencia", "")),
            component=metadata.get("component"),
            claim=metadata.get("claim", metadata.get("afirmacion")),
            evidence=metadata.get("evidence", metadata.get("evidencia", "")),
            standard=metadata.get("standard", metadata.get("estandar")),
            grade_or_program=metadata.get(
                "grade_or_program", metadata.get("grado_o_programa")
            ),
        )

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "area": self.area,
            "competency": self.competency,
            "component": self.component,
            "claim": self.claim,
            "evidence": self.evidence,
            "standard": self.standard,
            "grade_or_program": self.grade_or_program,
        }


@dataclass
class Difficulty:
    """Target difficulty plus justification."""

    target_level: DifficultyLevel
    justification: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "target_level": self.target_level.value,
            "justification": self.justification,
        }


@dataclass
class QualityReport:
    """Gate results, warnings, and revision notes."""

    quality_gates: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    revision_notes: List[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "ready" if all(v == "pass" for v in self.quality_gates.values()) else "draft"


@dataclass
class Option:
    """Represents a single option in a multiple‑choice question."""

    label: str
    text: str
    category: str  # clave, contradictoria, absurda, distractora

    def __post_init__(self) -> None:
        # Normalize the option text: ensure lower‑case first letter to
        # continue the enunciado coherently, as recommended【9†L31-L34】.
        if self.text and self.text[0].isupper():
            # preserve the label's capital A/B/C/D but lower the
            # subsequent first character of the option text
            parts = self.text.split(" ", 1)
            if len(parts) > 1:
                first_word, remainder = parts
                # first_word is something like "A."; remainder begins
                # with capital; convert remainder's first letter to
                # lower case
                if remainder:
                    self.text = f"{first_word} {remainder[0].lower()}{remainder[1:]}"

    def to_package_dict(self) -> Dict[str, str]:
        return {"label": self.label.rstrip("."), "text": self.text_without_label}

    @property
    def text_without_label(self) -> str:
        prefix = f"{self.label} "
        if self.text.startswith(prefix):
            return self.text[len(prefix) :].strip()
        return self.text.strip()


@dataclass
class ItemPackage:
    """Author-facing package matching templates/item-package.schema.json."""

    item_id: str
    status: str
    source_refs: List[SourceRef]
    source_summaries: List[SourceSummary]
    grounded_assumptions: List[str]
    alignment: Alignment
    difficulty: Difficulty
    context: str
    enunciado: str
    options: List[Option]
    clave: str
    distractor_rationales: Dict[str, str]
    quality_gates: Dict[str, str]
    warnings: List[str]
    revision_notes: List[str]

    @property
    def student_view(self) -> Dict[str, Any]:
        return {
            "context": self.context,
            "enunciado": self.enunciado,
            "options": [option.to_package_dict() for option in self.options],
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "status": self.status,
            "source_refs": [source.to_dict() for source in self.source_refs],
            "source_summaries": [summary.to_dict() for summary in self.source_summaries],
            "grounded_assumptions": self.grounded_assumptions,
            "alignment": self.alignment.to_dict(),
            "difficulty": self.difficulty.to_dict(),
            "context": self.context,
            "enunciado": self.enunciado,
            "options": [option.to_package_dict() for option in self.options],
            "clave": self.clave,
            "distractor_rationales": self.distractor_rationales,
            "quality_gates": self.quality_gates,
            "warnings": self.warnings,
            "revision_notes": self.revision_notes,
            "student_view": self.student_view,
        }

    def to_json(self, indent: int = 2) -> str:
        """Export one package as JSON object."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_author_json(self, indent: int = 2) -> str:
        """Export one package wrapped in the schema's author JSON array."""
        return json.dumps([self.to_dict()], ensure_ascii=False, indent=indent)

    def to_markdown(self) -> str:
        """Export review Markdown matching templates/item-package.md."""
        options = {option.label.rstrip("."): option.text_without_label for option in self.options}
        rationales = {
            label: self.distractor_rationales.get(label, "")
            for label in OPTION_LABELS
        }
        alignment = self.alignment.to_dict()
        gates = {name: self.quality_gates.get(name, "fail") for name in QUALITY_GATE_NAMES}
        student_json = json.dumps(self.student_view, ensure_ascii=False, indent=2)
        source_refs = json.dumps(
            [source.to_dict() for source in self.source_refs], ensure_ascii=False
        )
        source_summaries = json.dumps(
            [summary.to_dict() for summary in self.source_summaries], ensure_ascii=False
        )
        assumptions = json.dumps(self.grounded_assumptions, ensure_ascii=False)
        warnings = "\n".join(f"- {warning}" for warning in self.warnings) or "- Ninguna."
        notes = "\n".join(f"- {note}" for note in self.revision_notes) or "- Ninguna."

        return f"""# Paquete de item: {self.item_id}

**Estado**: `{self.status}`

## Fuentes

- `source_refs`: {source_refs}
- `source_summaries`: {source_summaries}

## Supuestos

- `grounded_assumptions`: {assumptions}

## Alineacion

- `area`: {alignment["area"]}
- `competency`: {alignment["competency"]}
- `component`: {alignment["component"]}
- `claim`: {alignment["claim"]}
- `evidence`: {alignment["evidence"]}
- `standard`: {alignment["standard"]}
- `grade_or_program`: {alignment["grade_or_program"]}

## Dificultad

- `target_level`: {self.difficulty.target_level.value}
- `justification`: {self.difficulty.justification}

## Item

### Contexto

{self.context}

### Enunciado

{self.enunciado}

### Opciones

A. {options.get("A", "")}
B. {options.get("B", "")}
C. {options.get("C", "")}
D. {options.get("D", "")}

### Clave

`{self.clave}`

### Racional de distractores

- `A`: {rationales["A"]}
- `B`: {rationales["B"]}
- `C`: {rationales["C"]}
- `D`: {rationales["D"]}

## Quality Gates

- `source_grounding`: {gates["source_grounding"]}
- `evidence_alignment`: {gates["evidence_alignment"]}
- `context_sufficiency`: {gates["context_sufficiency"]}
- `enunciado_clarity`: {gates["enunciado_clarity"]}
- `option_quality`: {gates["option_quality"]}
- `difficulty_fit`: {gates["difficulty_fit"]}

## Advertencias

{warnings}

## Notas de revision

{notes}

## Student View

```json
{student_json}
```
"""


@dataclass
class ICFESItem:
    """Encapsulates an ICFES multiple choice item.

    Parameters
    ----------
    context : str
        The background scenario or passage that frames the question.
    enunciado : str
        The specific question posed to the student.  Should not
        incorporate multiple categories or ask two questions at once.
    options : List[str]
        A list of four answer strings beginning with their labels
        (e.g. "A. ...").  Only one must be correct.
    correct_index : int
        The index (0–3) of the correct option in the options list.
    difficulty : DifficultyLevel, optional
        The anticipated difficulty of the item.
    metadata : Optional[Dict[str, str]]
        Additional metadata such as component, affirmation, evidence or
        task descriptions from the evidence‑centered design matrix.
    """

    context: str
    enunciado: str
    options: List[str]
    correct_index: int
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    metadata: Optional[Dict[str, str]] = field(default=None)

    def __post_init__(self) -> None:
        if len(self.options) != 4:
            raise ValueError("Exactly four options (A–D) are required.")
        if not 0 <= self.correct_index < 4:
            raise ValueError("correct_index must be between 0 and 3 inclusive.")
        # Build Option objects and classify distractors based on their position
        self.processed_options: List[Option] = []
        for i, opt in enumerate(self.options):
            label_end = opt.find('.')
            if label_end == -1:
                raise ValueError(
                    f"Option '{opt}' must start with a label (e.g. 'A.')."
                )
            label = opt[:label_end].strip()
            text = opt[label_end + 1:].strip()
            if i == self.correct_index:
                category = "clave"
            else:
                # Assign categories heuristically.  A simple scheme is
                # applied here: the first distractor is 'contradictoria',
                # the next is 'distractora', and the last is 'absurda'.
                # Users may override this later via metadata.
                if len(self.processed_options) == 0:
                    category = "contradictoria"
                elif len(self.processed_options) == 1:
                    category = "distractora"
                else:
                    category = "absurda"
            option_obj = Option(f"{label}.", f"{label}. {text}", category)
            self.processed_options.append(option_obj)

    def render(self) -> str:
        """Render the item as a formatted string.

        Returns
        -------
        str
            The context, enunciado and options arranged in a layout
            resembling official ICFES items.
        """
        lines: List[str] = []
        if self.context:
            lines.append(self.context.strip())
            lines.append("")
        if self.enunciado:
            lines.append(self.enunciado.strip())
            lines.append("")
        # Display options; ensure lower‑case continuation of enunciado
        for option in self.processed_options:
            lines.append(f"  {option.text}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Return a dictionary representation useful for serialisation.

        The dictionary contains the context, enunciado, options and
        indicates which option is correct.  Metadata is included if
        provided.
        """
        data = {
            "context": self.context,
            "enunciado": self.enunciado,
            "options": [opt.text for opt in self.processed_options],
            "clave_index": self.correct_index,
            "difficulty": self.difficulty.value,
        }
        if self.metadata:
            data["metadata"] = self.metadata
        return data

    @property
    def clave(self) -> str:
        """Return the correct option label."""
        return OPTION_LABELS[self.correct_index]

    def evaluate_quality(
        self,
        source_refs: Optional[List[SourceRef]] = None,
        alignment: Optional[Alignment] = None,
        difficulty_justification: Optional[str] = None,
    ) -> QualityReport:
        """Run lightweight package quality gates.

        Gates are deterministic checks intended to catch incomplete
        package metadata before review/export. They do not replace expert
        item review.
        """
        source_refs = source_refs or []
        alignment = alignment or Alignment.from_metadata(self.metadata)
        gates = {name: "pass" for name in QUALITY_GATE_NAMES}
        warnings: List[str] = []
        revision_notes: List[str] = []

        if not source_refs:
            gates["source_grounding"] = "fail"
            warnings.append("Faltan source_refs verificables.")

        if not alignment.area or not alignment.competency or not alignment.evidence:
            gates["evidence_alignment"] = "fail"
            warnings.append("Alineacion incompleta: requiere area, competency y evidence.")

        if len(self.context.strip()) < 40:
            gates["context_sufficiency"] = "fail"
            warnings.append("Contexto demasiado breve para sostener la inferencia.")

        enunciado = self.enunciado.strip()
        if len(enunciado) < 20 or "?" not in enunciado:
            gates["enunciado_clarity"] = "fail"
            warnings.append("Enunciado debe ser claro, completo y formulado como pregunta.")
        if enunciado.count("?") > 1:
            gates["enunciado_clarity"] = "fail"
            warnings.append("Enunciado parece contener mas de una pregunta.")

        option_texts = [option.text_without_label.lower() for option in self.processed_options]
        if len(set(option_texts)) != 4:
            gates["option_quality"] = "fail"
            warnings.append("Opciones repetidas o equivalentes detectadas.")
        if any(len(text) < 8 for text in option_texts):
            gates["option_quality"] = "fail"
            warnings.append("Una o mas opciones son demasiado breves.")
        if self.processed_options[self.correct_index].category != "clave":
            gates["option_quality"] = "fail"
            warnings.append("Clave no marcada como categoria clave.")

        if not difficulty_justification:
            gates["difficulty_fit"] = "fail"
            warnings.append("Falta justificacion de dificultad.")

        if warnings:
            revision_notes.append("Revisar gates fallidos antes de marcar item como ready.")
        else:
            revision_notes.append("Gates automaticos aprobados; pendiente revision humana si es banco formal.")

        return QualityReport(gates, warnings, revision_notes)

    def to_item_package(
        self,
        item_id: str = "item-001",
        source_refs: Optional[List[SourceRef]] = None,
        source_summaries: Optional[List[SourceSummary]] = None,
        grounded_assumptions: Optional[List[str]] = None,
        alignment: Optional[Alignment] = None,
        difficulty_justification: Optional[str] = None,
        distractor_rationales: Optional[Dict[str, str]] = None,
        revision_notes: Optional[List[str]] = None,
    ) -> ItemPackage:
        """Emit a full author ItemPackage with gates and student view."""
        source_refs = source_refs or []
        source_summaries = source_summaries or []
        grounded_assumptions = grounded_assumptions or []
        alignment = alignment or Alignment.from_metadata(self.metadata)
        difficulty_justification = difficulty_justification or ""
        report = self.evaluate_quality(source_refs, alignment, difficulty_justification)

        rationales = {
            option.label.rstrip("."): (
                "Clave correcta y suficiente."
                if option.category == "clave"
                else f"Distractor tipo {option.category}; requiere racional especifico."
            )
            for option in self.processed_options
        }
        if distractor_rationales:
            rationales.update(distractor_rationales)

        notes = list(report.revision_notes)
        if revision_notes:
            notes.extend(revision_notes)

        return ItemPackage(
            item_id=item_id,
            status=report.status,
            source_refs=source_refs,
            source_summaries=source_summaries,
            grounded_assumptions=grounded_assumptions,
            alignment=alignment,
            difficulty=Difficulty(self.difficulty, difficulty_justification),
            context=self.context,
            enunciado=self.enunciado,
            options=self.processed_options,
            clave=self.clave,
            distractor_rationales=rationales,
            quality_gates=report.quality_gates,
            warnings=report.warnings,
            revision_notes=notes,
        )

    def to_markdown(self, **package_kwargs: Any) -> str:
        """Export full package as review Markdown."""
        return self.to_item_package(**package_kwargs).to_markdown()

    def to_author_json(self, indent: int = 2, **package_kwargs: Any) -> str:
        """Export full package as schema-compatible JSON array."""
        return self.to_item_package(**package_kwargs).to_author_json(indent=indent)


def generate_item_from_prompt(
    context: str,
    question: str,
    correct_answer: str,
    wrong_answers: List[str],
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
    shuffle: bool = False,
    metadata: Optional[Dict[str, str]] = None,
) -> ICFESItem:
    """Convenience function to assemble an ICFES item from a base prompt.

    Parameters
    ----------
    context : str
        The scenario or text that frames the question.
    question : str
        The enunciado to be posed.  Avoid multiple conceptual categories.
    correct_answer : str
        The correct option (without label).  Will be assigned label
        automatically.
    wrong_answers : List[str]
        Three incorrect options (without labels).  These will be used
        as distractors.  If fewer than three are provided, the rest will
        be padded with generic distractors.
    difficulty : DifficultyLevel, optional
        The anticipated difficulty; influences nothing computational
        but is stored for completeness.
    shuffle : bool, optional
        When True, randomises the order of options.  Without
        shuffling, the correct answer is always labelled "A".
    metadata : Optional[Dict[str, str]], optional
        Additional metadata to store alongside the item.

    Returns
    -------
    ICFESItem
        A fully assembled item ready for rendering.
    """
    if len(wrong_answers) > 3:
        raise ValueError("Provide at most three wrong answers.")
    # pad wrong answers if necessary
    padded_wrongs = wrong_answers + ["ninguna de las anteriores"] * (3 - len(wrong_answers))
    option_texts: List[str] = [correct_answer] + padded_wrongs
    labels = ["A", "B", "C", "D"]
    indices = list(range(4))
    # Optionally shuffle to avoid always having the correct answer first
    if shuffle:
        import random
        random.shuffle(indices)
    arranged_options: List[str] = []
    correct_idx: int = 0
    for pos, idx in enumerate(indices):
        label = labels[pos]
        text = option_texts[idx]
        arranged_options.append(f"{label}. {text}")
        if idx == 0:
            correct_idx = pos
    return ICFESItem(context, question, arranged_options, correct_idx, difficulty, metadata)


def generate_item_package_from_prompt(
    context: str,
    question: str,
    correct_answer: str,
    wrong_answers: List[str],
    item_id: str = "item-001",
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
    shuffle: bool = False,
    metadata: Optional[Dict[str, str]] = None,
    source_refs: Optional[List[SourceRef]] = None,
    source_summaries: Optional[List[SourceSummary]] = None,
    grounded_assumptions: Optional[List[str]] = None,
    alignment: Optional[Alignment] = None,
    difficulty_justification: Optional[str] = None,
    distractor_rationales: Optional[Dict[str, str]] = None,
    revision_notes: Optional[List[str]] = None,
) -> ItemPackage:
    """Generate a full ItemPackage from prompt parts."""
    item = generate_item_from_prompt(
        context=context,
        question=question,
        correct_answer=correct_answer,
        wrong_answers=wrong_answers,
        difficulty=difficulty,
        shuffle=shuffle,
        metadata=metadata,
    )
    return item.to_item_package(
        item_id=item_id,
        source_refs=source_refs,
        source_summaries=source_summaries,
        grounded_assumptions=grounded_assumptions,
        alignment=alignment,
        difficulty_justification=difficulty_justification,
        distractor_rationales=distractor_rationales,
        revision_notes=revision_notes,
    )


def export_item_packages_json(
    packages: Iterable[ItemPackage],
    indent: int = 2,
) -> str:
    """Export item packages as schema-compatible author JSON array."""
    return json.dumps(
        [package.to_dict() for package in packages],
        ensure_ascii=False,
        indent=indent,
    )


def export_item_packages_markdown(packages: Iterable[ItemPackage]) -> str:
    """Export item packages as review Markdown sections."""
    return "\n\n---\n\n".join(package.to_markdown().rstrip() for package in packages)


__all__ = [
    "DifficultyLevel",
    "Difficulty",
    "Alignment",
    "QualityReport",
    "SourceRef",
    "SourceSummary",
    "Option",
    "ItemPackage",
    "ICFESItem",
    "generate_item_from_prompt",
    "generate_item_package_from_prompt",
    "export_item_packages_json",
    "export_item_packages_markdown",
]
