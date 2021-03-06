from fastapi import FastAPI, Response, status
from config.endpoints import EndpointConfig
from typing import Dict
from uuid import uuid4
from models.projects import *
from models.testcase import *
from models.commonerrors import *
import uuid

app = FastAPI()
projects_db: Dict = {}
testcase_db: Dict = {}
URL_CONF = EndpointConfig()
ERRORS_CONF = ErrorsConfig()


@app.get(URL_CONF.PROJECT.GET_ALL_PROJECT)
async def get_all_projects():
    return list(projects_db.values())


@app.post(URL_CONF.PROJECT.CREATE_PROJECT, status_code=status.HTTP_201_CREATED)
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


@app.get(URL_CONF.PROJECT.GET_PROJECT_DETAILS)
async def get_project_details(project_id, response: Response):
    project = projects_db.get(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        return project


@app.delete(URL_CONF.PROJECT.DELETE_PROJECT)
async def delete_project(project_id, response: Response):
    project: ProjectResponseModel = projects_db.get(project_id)
    if not project:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        project: ProjectResponseModel = projects_db[project_id]
        project.active = False
        return project


@app.put(URL_CONF.PROJECT.UPDATE_PROJECT)
async def update_project(project_id, request: ProjectRequestModel, response: Response):
    project: ProjectResponseModel = projects_db.get(project_id)
    if not project or not project.active:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        project: ProjectResponseModel = projects_db[project_id]
        project.title = request.title
        project.description = request.description
        project.owner = request.owner
        project.tags = request.tags
        project.updated_at = datetime.utcnow()

        return project


@app.post(URL_CONF.TESTCASE.CREATE_TESTCASE, status_code=status.HTTP_201_CREATED)
async def create_testcase(project_id, request: TestCaseRequestModel, response: Response):
    if project_id in projects_db:
        testcase = TestCaseResponseModel(
            project_id=uuid.UUID(project_id),
            id=uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            updated_by=request.author,
            title=request.title,
            description=request.description,
            author=request.author,
            tags=request.tags,
            expected_results=request.expected_results,
            archived=False
        )
        testcase_db[str(testcase.id)] = testcase
        return testcase
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)


@app.get(URL_CONF.TESTCASE.GET_TESTCASE_DETAIL)
async def get_testcase_details(project_id, testcase_id, response: Response):
    testcase_record: TestCaseResponseModel = testcase_db.get(testcase_id)
    if not testcase_record:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.TESTCASE_DOES_NOT_EXIST)
    elif str(testcase_record.project_id) != project_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        return testcase_record


@app.delete(URL_CONF.TESTCASE.DELETE_TESTCASE)
async def delete_testcase(project_id, testcase_id, response: Response):
    testcase_record: TestCaseResponseModel = testcase_db.get(testcase_id)
    if not testcase_record:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.TESTCASE_DOES_NOT_EXIST)
    elif str(testcase_record.project_id) != project_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        testcase_record.archived = True
        return testcase_record


@app.put(URL_CONF.TESTCASE.UPDATE_TESTCASE)
async def update_testcase(project_id, testcase_id, request: TestCaseRequestModel, response: Response):
    testcase_record: TestCaseResponseModel = testcase_db.get(testcase_id)
    if not testcase_record or testcase_record.archived:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.TESTCASE_DOES_NOT_EXIST)
    elif str(testcase_record.project_id) != project_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return GeneralError(error=ERRORS_CONF.GENERAL_ERRORS.PROJECT_DOES_NOT_EXIST)
    else:
        testcase_record.title = request.title
        testcase_record.description = request.description
        testcase_record.author = request.author
        testcase_record.tags = request.tags
        testcase_record.expected_results = request.expected_results
        testcase_record.updated_at = datetime.utcnow()
        testcase_record.updated_by = request.author

        return testcase_record
