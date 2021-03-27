from fastapi import FastAPI, Response, status
from config.endpoints import EndpointConfig
from typing import Dict
from uuid import uuid4
from models.projects import *
from models.testcase import *

app = FastAPI()
projects_db: Dict = {}
testcase_db: Dict = {}
URL = EndpointConfig()


@app.get(URL.PROJECT.GET_ALL_PROJECT)
async def get_all_projects():
    return list(projects_db.values())


@app.post(URL.PROJECT.CREATE_PROJECT, status_code=status.HTTP_201_CREATED)
async def create_project(request: ProjectRequestModel):
    project = ProjectResponseModel(
        id=uuid4(),
        title=request.title,
        description=request.description,
        owner=request.owner,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        tags=request.tags,
        active=True
    )
    projects_db[str(project.id)] = project
    return project


@app.get(URL.PROJECT.GET_PROJECT_DETAILS)
async def get_project_details(project_id, response: Response):
    try:
        return projects_db[project_id]
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.delete(URL.PROJECT.DELETE_PROJECT)
async def delete_project(project_id, response: Response):
    try:
        project: ProjectResponseModel = projects_db[project_id]
        project.active = False
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.put(URL.PROJECT.UPDATE_PROJECT)
async def update_project(project_id, request: ProjectRequestModel, response: Response):
    try:
        project: ProjectResponseModel = projects_db[project_id]
        project.title = request.title
        project.description = request.description
        project.owner = request.owner
        project.tags = request.tags
        project.updated_at = datetime.utcnow()
        return project
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.post(URL.TESTCASE.CREATE_TESTCASE, status_code=status.HTTP_201_CREATED)
async def create_testcase(project_id, request: TestCaseRequestModel, response: Response):
    if project_id in projects_db:
        testcase = TestCaseResponseModel(
            id=uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            updated_by=request.author,
            title=request.title,
            description=request.description,
            author=request.author,
            tags=request.tags,
            expected_results=request.expected_results
        )
        testcase_db[str(testcase.id)] = testcase
        return testcase
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise ValueError('Project Does Not Exist')




@app.get(URL.TESTCASE.GET_TESTCASE_DETAIL)
async def get_testcase_details(project_id, testcase_id):
    pass


@app.delete(URL.TESTCASE.DELETE_TESTCASE)
async def delete_testcase(project_id, testcase_id):
    pass


@app.put(URL.TESTCASE.UPDATE_TESTCASE)
async def update_testcase(project_id, testcase_id):
    pass
