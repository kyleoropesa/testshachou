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
        expected_results="should pass"):
    return {
        "title": title,
        "description": description,
        "author": author,
        "tags": tags,
        "expected_results": expected_results
    }

def create_project():
    payload = {
        "title": "Sample Project",
        "description": "Project description",
        "owner": "Project Owner",
        "tags": ["Project", "Tags"]
    }
    response = httpclient.post(URL.PROJECT.CREATE_PROJECT, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()
    return json_response




