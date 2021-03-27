from pydantic import BaseConfig


class Project(BaseConfig):
    GET_ALL_PROJECT: str = "/projects"
    CREATE_PROJECT: str = "/projects/create"
    GET_PROJECT_DETAILS: str = "/projects/{project_id}"
    DELETE_PROJECT: str = "/projects/{project_id}"
    UPDATE_PROJECT: str = "/projects/{project_id}/update"


class TestCase(BaseConfig):
    PROJECT_PATH: str = "/projects/{project_id}"

    GET_ALL_TESTCASE: str = f"{PROJECT_PATH}" + "/testcase"
    GET_TESTCASE_DETAIL: str = f"{PROJECT_PATH}" + "/testcase/{testcase_id}"
    CREATE_TESTCASE: str = f"{PROJECT_PATH}" + "/testcase/create"
    DELETE_TESTCASE: str = f"{PROJECT_PATH}" + "/testcase/{testcase_id}/delete"
    UPDATE_TESTCASE: str = f"{PROJECT_PATH}" + "/testcase/{testcase_id}/update"
