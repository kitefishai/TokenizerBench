from .human_languages import human_languages
from .programming_languages import programming_languages
from .scientific_formulas import scientific_formulas
from .edge_cases import edge_cases

__all__ = [
    "human_languages",
    "programming_languages",
    "scientific_formulas",
    "edge_cases",
]

ALL_DATA = {
    "human_languages": human_languages,
    "programming_languages": programming_languages,
    "scientific_formulas": scientific_formulas,
    "edge_cases": edge_cases,
}
