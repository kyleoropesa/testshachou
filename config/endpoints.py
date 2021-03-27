from pydantic import BaseConfig
from dataclasses import dataclass


class Project(BaseConfig):
    GET_ALL_PROJECT: str = "/projects"
    CREATE_PROJECT: str = "/projects/create"
    GET_PROJECT_DETAILS: str = "/projects/{project_id}"
    DELETE_PROJECT: str = "/projects/{project_id}"
    UPDATE_PROJECT: str = "/projects/{project_id}/update"


class TestCase(BaseConfig):
    GET_ALL_TESTCASE: str = "/projects/{project_id}/testcase"
    GET_TESTCASE_DETAIL: str = "/projects/{project_id}/testcase/{testcase_id}"
    CREATE_TESTCASE: str = "/projects/{project_id}/testcase/create"
    DELETE_TESTCASE: str = "/projects/{project_id}/testcase/{testcase_id}/delete"
    UPDATE_TESTCASE: str = "/projects/{project_id}/testcase/{testcase_id}/update"
