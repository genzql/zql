import pytest
from zql.translator import translate
from zql.sample_grammars import ENGLISH_TRANSLATION_GRAMMAR


TRANSLATE_TEST_CASES: list[tuple[str, dict]] = [
    (
        "english_to_spanish",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": None,
            "target_dialect": "spanish",
            "source": "hello tamjid",
            "expected": "hola tamjid",
        }
    ),
    (
        "english_to_bengali",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": None,
            "target_dialect": "bengali",
            "source": "hello tamjid",
            "expected": "salam tamjid",
        }
    ),
    (
        "english_to_arabic",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": None,
            "target_dialect": "arabic",
            "source": "hello tamjid",
            "expected": "salam tamjid",
        }
    ),
    (
        "english_to_yoda",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": None,
            "target_dialect": "yoda",
            "source": "hello tamjid",
            "expected": "tamjid hello",
        }
    ),
    (
        "english_to_lowercase_english",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": None,
            "target_dialect": "lowercase_english",
            "source": "hello tamjid",
            "expected": "hello tamjid",
        }
    ),
    (
        "spanish_to_english",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": "spanish",
            "target_dialect": None,
            "source": "hola tamjid",
            "expected": "hello tamjid",
        }
    ),
    (
        "bengali_to_english",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": "bengali",
            "target_dialect": None,
            "source": "salam tamjid",
            "expected": "hello tamjid",
        }
    ),
    (
        "spanish_to_bengali",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": "spanish",
            "target_dialect": "bengali",
            "source": "hola tamjid",
            "expected": "salam tamjid",
        }
    ),
    (
        "bengali_to_spanish",
        {
            "grammar": ENGLISH_TRANSLATION_GRAMMAR,
            "source_dialect": "bengali",
            "target_dialect": "spanish",
            "source": "salam tamjid",
            "expected": "hola tamjid",
        }
    ),
]


@pytest.mark.parametrize("name,kwargs", TRANSLATE_TEST_CASES)
def test_translate_between_dialects(name: str, kwargs: dict):
    expected = kwargs["expected"]
    del kwargs["expected"]
    actual = translate(**kwargs)
    assert actual == expected