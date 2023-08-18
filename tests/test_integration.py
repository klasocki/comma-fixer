from flask import json
import pytest

from app import app
from baseline import create_baseline_pipeline


@pytest.fixture()
def client():
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.baseline_pipeline = create_baseline_pipeline()
    yield app.test_client()


def test_fix_commas_fails_on_no_parameter(client):
    response = client.post('/baseline/fix-commas/')
    assert response.status_code == 400


def test_fix_commas_fails_on_wrong_parameters(client):
    response = client.post('/baseline/fix-commas/', json={'text': "Some text."})
    assert response.status_code == 400


@pytest.mark.parametrize(
    "test_input",
    ['',
     'Hello world.',
     'This test string should not have any commas inside it.']
)
def test_fix_commas_correct_string_unchanged(client, test_input: str):
    response = client.post('/baseline/fix-commas/', json={'s': test_input})

    assert response.status_code == 200
    assert response.get_json().get('s') == test_input


@pytest.mark.parametrize(
    "test_input, expected",
    [['I am, here.', 'I am here.'],
     ['books pens and pencils',
      'books, pens and pencils']]
)
def test_fix_commas_fixes_wrong_commas(client, test_input: str, expected: str):
    response = client.post('/baseline/fix-commas/', json={'s': test_input})

    assert response.status_code == 200
    assert response.get_json().get('s') == expected
