import json

from app import app
import pytest


def test_fix_commas_fails_on_no_parameter():
    response = app.test_client().post('/baseline/fix-commas/')
    assert response.status_code == 400


@pytest.mark.parametrize(
    "test_input",
    [[''],
     ['Hello world.'],
     ['This test string should not have any commas inside it.']]
)
def test_fix_commas_plain_string_unchanged(test_input: str):
    response = app.test_client().post('/baseline/fix-commas/', data={'s': test_input})
    print(response.data.decode('utf-8'))
    # result = json.loads(response.data.decode('utf-8')).get('s')
    assert response.status_code == 200
    # assert result == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [['', ''],
     ['Hello world.', 'Hello world.'],
     ['This test string should not have any commas inside it.',
      'This test string should not have any commas inside it.']]
)
def test_fix_commas_fixes_wrong_commas(test_input: str, expected: str):
    assert False
