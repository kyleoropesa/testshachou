from fastapi.testclient import TestClient
from fastapi import status
from config.endpoints import EndpointConfig
from main import app

httpclient = TestClient(app)
URL = EndpointConfig()


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


def assert_project_response(payload: dict, json_response: dict):
    assert json_response['title'] == payload['title']
    assert json_response['description'] == payload['description']
    assert json_response['owner'] == payload['owner']
    assert json_response['tags'] == payload['tags']
    assert json_response['active'] is True
    assert json_response['id'] is not None
    assert json_response['created_at'] is not None
    assert json_response['updated_at'] is not None


def assert_updated_project(create_project_payload: dict, update_project_payload: dict, project_id: str):
    update_project_response = httpclient.put(
        URL.PROJECT.UPDATE_PROJECT.format(project_id=project_id),
        json=update_project_payload
    )
    assert update_project_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    json_response = httpclient.get(URL.PROJECT.GET_PROJECT_DETAILS.format(project_id=project_id)).json()
    assert_project_response(payload=create_project_payload, json_response=json_response)


def test_successful_project_creation():
    request_body = generate_create_project_payload()
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=request_body)
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert_project_response(payload=request_body, json_response=json_response)


def test_create_project_with_invalid_format_in_request_body():
    request_body = {}
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_project_with_no_key_value_to_optional_field_description():
    request_body = generate_create_project_payload()
    request_body.pop('description')
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=request_body)
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
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_project_with_empty_values_in_owner():
    request_body = generate_create_project_payload(owner=' ')
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_all_projects():
    payload = generate_create_project_payload(title='first project')
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=payload)
    project = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    get_projects_response = httpclient.get(URL.PROJECT.GET_ALL_PROJECT)
    projects_db = get_projects_response.json()
    assert get_projects_response.status_code == status.HTTP_200_OK
    assert project in projects_db


def test_get_all_projects_using_invalid_method():
    get_projects_response = httpclient.post(URL.PROJECT.GET_ALL_PROJECT)
    assert get_projects_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_get_project_detail():
    payload = generate_create_project_payload()
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=payload)
    json_response = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    project_detail = httpclient.get(URL.PROJECT.GET_PROJECT_DETAILS.format(project_id=json_response['id']))
    assert project_detail.status_code == status.HTTP_200_OK
    assert response.json() == project_detail.json()


def test_get_project_detail_with_non_existing_project_id():
    project_detail = httpclient.get(URL.PROJECT.GET_PROJECT_DETAILS.format(project_id='random_id'))
    assert project_detail.status_code == status.HTTP_404_NOT_FOUND


def test_update_project_title_description_and_owner_should_succeed():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated title',
        description='updated description',
        owner='updated owner',
        tags=['the', 'updated', 'tag']
    )
    update_project_response = httpclient.put(
        URL.PROJECT.UPDATE_PROJECT.format(project_id=project_id),
        json=update_project_payload
    )
    json_response = update_project_response.json()
    assert_project_response(payload=update_project_payload, json_response=json_response)


def test_update_project_description_with_empty_values_should_succeed():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated titled',
        description='',
        owner='updated owner',
        tags=['the', 'updated', 'tag']
    )
    assert_updated_project(create_project_payload, update_project_payload, project_id)


def test_update_project_owner_to_empty_should_return_error():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated title',
        description='updated description',
        owner='',
        tags=['the', 'updated', 'tag']
    )
    assert_updated_project(create_project_payload, update_project_payload, project_id)


def test_update_project_title_to_empty_should_return_error():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='',
        description='updated description',
        owner='updated owner',
        tags=['the', 'updated', 'tag']
    )
    assert_updated_project(create_project_payload, update_project_payload, project_id)


def test_update_project_tags_to_empty_should_return_error():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated title',
        description='updated description',
        owner='updated owner',
        tags=['']
    )
    assert_updated_project(create_project_payload, update_project_payload, project_id)


def test_update_project_description_to_empty_should_not_succeed():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    assert create_project_response.status_code == status.HTTP_201_CREATED
    project_id = create_project_response.json()['id']
    update_project_payload = generate_create_project_payload(
        title='updated title',
        description='',
        owner='updated owner',
        tags=['tag1', 'tag2', 'tag3']
    )
    assert_updated_project(create_project_payload, update_project_payload, project_id)


def test_delete_project_details():
    create_project_payload = generate_create_project_payload(title='original payload')
    create_project_response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=create_project_payload)
    project_id = create_project_response.json()['id']
    assert create_project_response.status_code == status.HTTP_201_CREATED

    get_project_response = httpclient.get(URL.PROJECT.GET_PROJECT_DETAILS.format(project_id=project_id))
    assert get_project_response.status_code == status.HTTP_200_OK
    assert get_project_response.json()['active'] is True

    delete_project = httpclient.delete(URL.PROJECT.DELETE_PROJECT.format(project_id=project_id))
    assert delete_project.status_code == status.HTTP_200_OK

    get_deleted_project_response = httpclient.get(URL.PROJECT.GET_PROJECT_DETAILS.format(project_id=project_id))
    assert get_deleted_project_response.status_code == status.HTTP_200_OK
    assert get_deleted_project_response.json()['active'] is False
