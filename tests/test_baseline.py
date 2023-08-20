import pytest
from commafixer.src.baseline import BaselineCommaFixer, _remove_punctuation


@pytest.fixture()
def baseline_fixer():
    yield BaselineCommaFixer()


@pytest.mark.parametrize(
    "test_input",
    ['',
     'Hello world.',
     'This test string should not have any commas inside it.',
     'aAaalLL the.. weird?~! punctuation.should also . be kept-as is! Only fixing-commas.']
)
def test_fix_commas_leaves_correct_strings_unchanged(baseline_fixer, test_input):
    result = baseline_fixer.fix_commas(s=test_input)
    assert result == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ['I, am.', 'I am.'],
        ['A complex     clause however it misses a comma something else and a dot...?',
         'A complex     clause, however, it misses a comma, something else and a dot...?'],
        ['a pen an apple, \tand a pineapple!',
         'a pen, an apple \tand a pineapple!'],
        ['Even newlines\ntabs\tand others get preserved.',
         'Even newlines,\ntabs\tand others get preserved.'],
        ['I had no Creativity left, therefore, I come here, and write useless examples, for this test.',
         'I had no Creativity left therefore, I come here and write useless examples for this test.']]
)
def test_fix_commas_fixes_incorrect_commas(baseline_fixer, test_input, expected):
    result = baseline_fixer.fix_commas(s=test_input)
    assert result == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [['', ''],
     ['Hello world...', 'Hello world'],
     ['This: test - string should not, have any commas inside it...?',
      'This test  string should not have any commas inside it']]
)
def test__remove_punctuation(test_input, expected):
    assert _remove_punctuation(test_input) == expected
