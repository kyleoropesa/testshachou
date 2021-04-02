from fastapi.testclient import TestClient
from config.endpoints import EndpointConfig
from fastapi import status
from main import app
from config.errormessage import ErrorsConfig
from typing import Tuple

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


def get_created_project_id() -> str:
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


def get_created_testcase_id_and_project_id(payload: dict) -> Tuple[str, str]:
    project_id = get_created_project_id()
    created_testcase = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    testcase_id = created_testcase.json()['id']
    return project_id, testcase_id


def assert_empty_field_in_create_project_should_return_error(payload):
    project_id = get_created_project_id()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert json_response['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def assert_create_project_should_return_error_when_mandatory_fields_use_spaces_only(payload):
    project_id = get_created_project_id()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert json_response['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_successful_create_testcase():
    project_id = get_created_project_id()
    payload = generate_create_testcase_payload()
    response = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert json_response['project_id'] is not None
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


def test_get_created_testcase_details():
    payload = generate_create_testcase_payload()
    project_id = get_created_project_id()
    created_testcase = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )

    testcase_details = httpclient.get(
        URL.TESTCASE.GET_TESTCASE_DETAIL.format(
            project_id=project_id,
            testcase_id=created_testcase.json()['id']
        )
    )

    assert created_testcase.json() == testcase_details.json()


def test_get_created_testcase_details_using_non_existing_testcase_id():
    project_id = get_created_project_id()
    testcase_details = httpclient.get(
        URL.TESTCASE.GET_TESTCASE_DETAIL.format(
            project_id=project_id,
            testcase_id="NONEXISTING"
        )
    )

    assert testcase_details.json()['error'] == ERRORS_CONF.GENERAL_ERRORS.TESTCASE_DOES_NOT_EXIST


def test_get_created_testcase_details_using_non_existing_project_id():
    payload = generate_create_testcase_payload()
    project_id = get_created_project_id()
    created_testcase = httpclient.post(
        URL.TESTCASE.CREATE_TESTCASE.format(project_id=project_id),
        json=payload
    )

    testcase_details = httpclient.get(
        URL.TESTCASE.GET_TESTCASE_DETAIL.format(
            project_id="NONEXISTING",
            testcase_id=created_testcase.json()['id']
        )
    )

    assert testcase_details.json()['error'] == ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST


def assert_payload_and_expected_response_in_testcase(payload: dict, response: dict):
    assert payload['title'] == response['title']
    assert payload['description'] == response['description']
    assert payload['author'] == response['author']
    assert payload['tags'] == response['tags']
    assert payload['expected_results'] == response['expected_results']
    assert response['id'] is not None
    assert response['project_id'] is not None
    assert response['created_at'] is not None
    assert response['updated_at'] is not None
    assert response['created_at'] != response['updated_at']
    assert response['updated_by'] == payload['author']


def test_update_testcase_title():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(title='updated_title')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert_payload_and_expected_response_in_testcase(update_payload, update_response_json)


def test_update_testcase_description():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(description='updated_description')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert_payload_and_expected_response_in_testcase(update_payload, update_response_json)


def test_update_testcase_author():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(description='updated_author')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert_payload_and_expected_response_in_testcase(update_payload, update_response_json)


def test_update_testcase_tags():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(tags=['updated_tags', 'tags_2'])
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert_payload_and_expected_response_in_testcase(update_payload, update_response_json)


def test_update_testcase_expected_results():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(expected_results="testing expected results")
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert_payload_and_expected_response_in_testcase(update_payload, update_response_json)


def test_update_testcase_title_using_empty_spaces():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(title='')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def test_update_testcase_title_using_spaces_only():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(title='   ')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_update_testcase_description_using_empty_spaces():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(description='')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def test_update_testcase_description_using_spaces_only():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(description='   ')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_update_testcase_title_using_empty_spaces():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(title='')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def test_update_testcase_title_using_spaces_only():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(title='   ')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_update_testcase_author_using_empty_spaces():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(author='')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def test_update_testcase_author_using_spaces_only():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(author='   ')
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY


def test_update_testcase_tags_using_empty_spaces():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(tags=[''])
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.EMPTY_STRINGS


def test_update_testcase_tags_using_spaces_only():
    create_payload = generate_create_testcase_payload()
    update_payload = generate_create_testcase_payload(tags=['   '])
    project_id, testcase_id = get_created_testcase_id_and_project_id(create_payload)
    update_response = httpclient.put(
        URL.TESTCASE.UPDATE_TESTCASE.format(
            project_id=project_id,
            testcase_id=testcase_id
        ),
        json=update_payload
    )
    update_response_json = update_response.json()
    assert update_response.status_code == 422
    assert update_response_json['detail'][0]['msg'] == ERRORS_CONF.FIELD_VALUE.SPACES_ONLY
