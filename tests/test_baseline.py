import pytest
from baseline import create_baseline_pipeline, fix_commas, _remove_punctuation


@pytest.fixture()
def baseline_pipeline():
    yield create_baseline_pipeline()


@pytest.mark.parametrize(
    "test_input",
    ['',
     'Hello world.',
     'This test string should not have any commas inside it.']
)
def test_fix_commas_leaves_correct_strings_unchanged(baseline_pipeline, test_input):
    result = fix_commas(baseline_pipeline, s=test_input)
    assert result == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ['I, am.', 'I am.'],
        ['A complex     clause however it misses a comma something else and a dot...?',
         'A complex     clause, however, it misses a comma, something else and a dot...?']]
)
def test_fix_commas_fixes_incorrect_commas(baseline_pipeline, test_input, expected):
    result = fix_commas(baseline_pipeline, s=test_input)
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
