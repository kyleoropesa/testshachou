from fastapi.testclient import TestClient
from config.endpoints import EndpointConfig
from fastapi import status
from main import app

httpclient = TestClient(app)
URL = EndpointConfig


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
