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
         'I had no Creativity left therefore, I come here and write useless examples for this test.'],
        [' This is a sentence. With, a lot of, useless punctuation!!??. O.o However we have to insert commas O-O, '
         'nonetheless or we will fail this test.',
         ' This is a sentence. With a lot of useless punctuation!!??. O.o However, we have to insert commas O-O '
         'nonetheless, or we will fail this test.'],
        [" The ship 's secondary armament consisted of fourteen 45 @-@ calibre 6 @-@ inch ( 152 mm ) quick @-@ firing ( QF ) guns mounted in casemates . Lighter guns consisted of eight 47 @-@ millimetre ( 1 @.@ 9 in ) three @-@ pounder Hotchkiss guns and four 47 @-@ millimetre 2 @.@ 5 @-@ pounder Hotchkiss guns . The ship was also equipped with four submerged 18 @-@ inch torpedo tubes two on each broadside .",
         " The ship 's secondary armament consisted of fourteen 45 @-@ calibre 6 @-@ inch ( 152 mm ) quick @-@ firing ( QF ) guns mounted in casemates . Lighter guns consisted of eight 47 @-@ millimetre ( 1 @.@ 9 in ), three @-@ pounder Hotchkiss guns and four 47 @-@ millimetre 2 @.@ 5 @-@ pounder Hotchkiss guns . The ship was also equipped with four submerged 18 @-@ inch torpedo tubes, two on each broadside ."]

    ]
)
def test_fix_commas_fixes_incorrect_commas(baseline_fixer, test_input, expected):
    result = baseline_fixer.fix_commas(s=test_input)
    assert result == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [['', ('', [])],
     [' world...', (' world', [6, 7, 8])],
     [',,,', ('', [])],
     ['This: test - string should not, have any commas inside it...?',
      ('This test  string should not have any commas inside it', [4, 11, 57, 58, 59, 60])]]
)
def test__remove_punctuation(test_input, expected):
    assert _remove_punctuation(test_input) == expected
