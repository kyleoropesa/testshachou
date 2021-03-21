from pydantic import BaseConfig


class Project(BaseConfig):
    GET_ALL_PROJECT: str = "/projects"
    CREATE_PROJECT: str = "/projects/create"
    GET_PROJECT_DETAILS: str = "/projects/{project_id}"
    DELETE_PROJECT: str = "/projects/{project_id}"
    UPDATE_PROJECT: str = "/projects/{project_id}/update"
