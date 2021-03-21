from fastapi.testclient import TestClient
from fastapi import status
from config.endpoints import Project
from main import app
import pytest


@pytest.fixture
def httpclient():
    client: TestClient = TestClient(app)
    return client


@pytest.fixture
def endpoint():
    endpoint = Project()
    return endpoint


def generate_create_project_payload(
        title="Sample Project",
        description="Sample Project Description",
        owner="I am the owner",
        tags=["hello", "world"]):
    return {
        "title": title,
        "description": description,
        "owner": owner,
        "tags": tags
    }


def test_successful_project_creation(httpclient, endpoint):
    request_body = generate_create_project_payload()
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert json_response['title'] == request_body['title']
    assert json_response['description'] == request_body['description']
    assert json_response['owner'] == request_body['owner']
    assert json_response['tags'] == request_body['tags']
    assert json_response['active'] is True
    assert json_response['id'] is not None
    assert json_response['created_at'] is not None
    assert json_response['updated_at'] is not None


def test_create_project_with_invalid_format_in_request_body(httpclient, endpoint):
    request_body = {}
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_project_with_no_key_value_to_optional_field_description(httpclient, endpoint):
    request_body = generate_create_project_payload()
    request_body.pop('description')
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert json_response['title'] == request_body['title']
    assert json_response['description'] is None
    assert json_response['owner'] == request_body['owner']
    assert json_response['tags'] == request_body['tags']
    assert json_response['active'] is True
    assert json_response['id'] is not None
    assert json_response['created_at'] is not None
    assert json_response['updated_at'] is not None


def test_create_project_with_non_existing_keys_for_optional_values_in_request_body():
    pass


def test_get_all_projects():
    pass


def test_get_all_projects_using_invalid_method():
    pass


def test_get_all_projects_for_empty_projectsdb():
    pass


def test_get_project_detail():
    pass


def test_get_project_detail_with_non_existing_project_id():
    pass


def test_update_project_title_should_succeed():
    pass


def test_update_project_description_should_succeed():
    pass


def test_update_project_description_with_empty_values_should_succeed():
    pass


def test_update_project_tags_should_succeed():
    pass


def test_update_project_owner_should_succeed():
    pass


def test_update_project_owner_to_empty_should_return_error():
    pass


def test_update_project_title_to_empty_should_return_error():
    pass


def test_update_project_tags_to_empty_should_return_error():
    pass


def test_update_project_description_to_empty_should_succeed():
    pass
