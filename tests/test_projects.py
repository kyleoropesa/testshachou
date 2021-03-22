from fastapi.testclient import TestClient
from fastapi import status
from config.endpoints import Project
from main import app

httpclient = TestClient(app)
endpoint = Project()


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


def test_successful_project_creation():
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


def test_create_project_with_invalid_format_in_request_body():
    request_body = {}
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_project_with_no_key_value_to_optional_field_description():
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


def test_create_project_with_empty_values_in_title():
    request_body = generate_create_project_payload(title=' ')
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_project_with_empty_values_in_owner():
    request_body = generate_create_project_payload(owner=' ')
    response = httpclient.post(endpoint.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_all_projects():
    payload = generate_create_project_payload(title='first project')
    response = httpclient.post(endpoint.CREATE_PROJECT, json=payload)
    project = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    get_projects_response = httpclient.get(endpoint.GET_ALL_PROJECT)
    projecs_db = get_projects_response.json()
    assert get_projects_response.status_code == status.HTTP_200_OK
    assert project in projecs_db


def test_get_all_projects_using_invalid_method():
    get_projects_response = httpclient.post(endpoint.GET_ALL_PROJECT)
    assert get_projects_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_empty_get_all_projects():
    get_projects_response = httpclient.get(endpoint.GET_ALL_PROJECT)
    projecs_db = get_projects_response.json()
    assert len(projecs_db) == 0


def test_get_project_detail():
    payload = generate_create_project_payload()
    response = httpclient.post(endpoint.CREATE_PROJECT, json=payload)
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    project_detail = httpclient.get(endpoint.GET_PROJECT_DETAILS.format(project_id=json_response['id']))
    assert project_detail.status_code == status.HTTP_200_OK
    assert response.json() == project_detail.json()


def test_get_project_detail_with_non_existing_project_id():
    project_detail = httpclient.get(endpoint.GET_PROJECT_DETAILS.format(project_id='randomid'))
    assert project_detail.status_code == status.HTTP_404_NOT_FOUND


def test_update_project_title_description_and_owner_should_succeed():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(endpoint.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated title',
        description='updated description',
        owner='updated owner',
        tags=['the', 'updated', 'tag']
    )
    update_project_response = httpclient.put(
        endpoint.UPDATE_PROJECT.format(project_id=project_id),
        json=update_project_payload
    )
    json_response = update_project_response.json()
    assert update_project_response.status_code == status.HTTP_200_OK
    assert json_response['title'] == update_project_payload['title']
    assert json_response['description'] == update_project_payload['description']
    assert json_response['owner'] == update_project_payload['owner']
    assert json_response['tags'] == update_project_payload['tags']
    assert json_response['active'] is True
    assert json_response['id'] is not None
    assert json_response['created_at'] is not None
    assert json_response['updated_at'] is not None


def test_update_project_description_with_empty_values_should_succeed():
    pass


def test_update_project_owner_to_empty_should_return_error():
    pass


def test_update_project_title_to_empty_should_return_error():
    pass


def test_update_project_tags_to_empty_should_return_error():
    pass


def test_update_project_description_to_empty_should_succeed():
    pass
