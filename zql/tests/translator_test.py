import pytest

from typing import List, Tuple

from zql.genzql.grammar import Grammar
from zql.genzql.translator import translate
from zql.tests.sample_grammars import ENGLISH_TRANSLATION_GRAMMAR


def get_pairwise_translations(
    grammar_name: str,
    grammar: Grammar,
    default_dialect: str,
    dialect_map: dict
) -> List[Tuple[str, dict]]:
    res: List[Tuple[str, dict]] = []
    for source_dialect in dialect_map:
        for target_dialect in dialect_map:
            source_name = source_dialect or default_dialect
            target_name = target_dialect or default_dialect
            name = f"{grammar_name}_{source_name}_to_{target_name}"
            kwargs = {
                "grammar": grammar,
                "source_dialect": source_dialect,
                "target_dialect": target_dialect,
                "source": dialect_map[source_dialect],
                "expected": dialect_map[target_dialect],
            }
            res.append((name, kwargs))
    return res


SENTENCES_BY_DIALECT = {
    None: "hello tamjid",
    "spanish": "hola tamjid",
    "bengali": "salam tamjid",
    "arabic": "salam tamjid",
    "yoda": "tamjid hello",
}


TRANSLATE_TEST_CASES: List[Tuple[str, dict]] = [
    *get_pairwise_translations(
        "english_translation",
        ENGLISH_TRANSLATION_GRAMMAR,
        "english",
        SENTENCES_BY_DIALECT
    )
]


@pytest.mark.parametrize("name,kwargs", TRANSLATE_TEST_CASES)
def test_translate_between_dialects(name: str, kwargs: dict):
    expected = kwargs["expected"]
    del kwargs["expected"]
    actual = translate(**kwargs)
    assert actual == expected