from fastapi.testclient import TestClient
from config.endpoints import EndpointConfig
from fastapi import status
from main import app
from config.errormessage import ErrorsConfig

httpclient = TestClient(app)
URL = EndpointConfig()
ERRORS_CONF = ErrorsConfig()


def generate_create_testcase_payload(
        title="Sample Testcase",
        description="Testcase description",
        author="Testcase owner",
        tags=["test", "tags"],
        expected_results="should pass") -> dict:
    return {
        "title": title,
        "description": description,
        "author": author,
        "tags": tags,
        "expected_results": expected_results
    }


def get_project_id() -> str:
    payload = {
        "title": "Sample Project",
        "description": "Project description",
        "owner": "Project Owner",
        "tags": ["Project", "Tags"]
    }
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    return json_response['id']


def assert_empty_field_in_create_project_should_return_error(payload):
    project_id = get_project_id()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert json_response['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload):
    project_id = get_project_id()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert json_response['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_successful_create_testcase():
    project_id = get_project_id()
    payload = generate_create_testcase_payload()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert json_response['id'] is not None
    assert json_response['title'] == payload['title']
    assert json_response['description'] == payload['description']
    assert json_response['author'] == payload['author']
    assert json_response['tags'] == payload['tags']
    assert json_response['expected_results'] == payload['expected_results']
    assert json_response['created_at'] is not None
    assert json_response['updated_at'] is not None
    assert json_response['updated_by'] == payload['author']


def test_create_testcase_with_empty_title():
    payload = generate_create_testcase_payload(title="")
    assert_empty_field_in_create_project_should_return_error(payload)


def test_create_testcase_with_empty_description():
    payload = generate_create_testcase_payload(description="")
    assert_empty_field_in_create_project_should_return_error(payload)


def test_create_testcase_with_empty_author():
    payload = generate_create_testcase_payload(author="")
    assert_empty_field_in_create_project_should_return_error(payload)


def test_create_testcase_with_empty_expected_results():
    payload = generate_create_testcase_payload(expected_results="")
    assert_empty_field_in_create_project_should_return_error(payload)


def test_create_testcase_with_non_existing_project_id():
    payload = generate_create_testcase_payload()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id="NON_EXISTING"),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json_response['error'] == ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST


def test_create_testcase_using_title_with_space_only_as_value():
    payload = generate_create_testcase_payload(title=" ")
    assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload)


def test_create_testcase_using_description_with_space_only_as_value():
    payload = generate_create_testcase_payload(description=" ")
    assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload)


def test_create_testcase_using_author_with_space_only_as_value():
    payload = generate_create_testcase_payload(author=" ")
    assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload)


def test_create_testcase_using_expected_results_with_space_only_as_value():
    payload = generate_create_testcase_payload(expected_results=" ")
    assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload)


def test_create_testcase_using_empty_strings_only_on_tag_values():
    payload = generate_create_testcase_payload(tags=[""])
    assert_empty_field_in_create_project_should_return_error(payload)


def test_create_testcase_using_spaces_only_on_tag_values():
    payload = generate_create_testcase_payload(tags=[" "])
    assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload)
