from fastapi.testclient import TestClient
import pytest

from app import app


@pytest.mark.parametrize(
    "endpoint",
    ['/fix-commas/',
     '/baseline/fix-commas/']
)
class TestFixCommaApi:
    @pytest.fixture()
    def client(self):
        yield TestClient(app)

    def test_fix_commas_fails_on_no_parameter(self, client, endpoint):
        response = client.post(endpoint)
        assert response.status_code == 422

    def test_fix_commas_fails_on_wrong_parameters(self, client, endpoint):
        response = client.post(endpoint, json={'text': "Some text."})
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "test_input",
        ['',
         'Hello world.',
         'This test string should not have any commas inside it.']
    )
    def test_fix_commas_correct_string_unchanged(self, client, endpoint, test_input: str):
        response = client.post(endpoint, json={'s': test_input})

        assert response.status_code == 200
        assert response.json().get('s') == test_input

    @pytest.mark.parametrize(
        "test_input, expected",
        [['I am, here.', 'I am here.'],
         ['books pens and pencils',
          'books, pens and pencils']]
    )
    def test_fix_commas_fixes_wrong_commas(self, client, endpoint, test_input: str, expected: str):
        response = client.post(endpoint, json={'s': test_input})

        assert response.status_code == 200
        assert response.json().get('s') == expected

    def test_with_a_very_long_string(self, endpoint, client):
        s = ("Just a long string. " * 200).rstrip()
        response = client.post(endpoint, json={'s': s})

        assert response.status_code == 200
        assert response.json().get('s') == s
