from fastapi import FastAPI, Response, status
from config.endpoints import Project
from typing import List, Dict
from uuid import uuid4
from models.projects import *

app = FastAPI()
projects_db: Dict = {}
endpoints = Project()


@app.get(endpoints.GET_ALL_PROJECT)
async def get_all_projects():
    return list(projects_db.values())


@app.post(endpoints.CREATE_PROJECT, status_code=status.HTTP_201_CREATED)
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


@app.get(endpoints.GET_PROJECT_DETAILS)
async def get_project_details(project_id, response: Response):
    try:
        return projects_db[project_id]
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.delete(endpoints.DELETE_PROJECT)
async def delete_project(project_id, response: Response):
    try:
        project: ProjectResponseModel = projects_db[project_id]
        project.active = False
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.put(endpoints.UPDATE_PROJECT)
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


@app.post("/projects/{project_id}/testcase/create")
async def create_testcase(project_id):
    pass


@app.get("/projects/{project_id}/testcase/{testcase_id}")
async def get_testcase_details(project_id, testcase_id):
    pass


@app.delete("/projects/{project_id}/testcase/{testcase_id}")
async def delete_testcase(project_id, testcase_id):
    pass


@app.put("/projects/{project_id}/testcase/{testcase_id}/update")
async def update_testcase(project_id, testcase_id):
    pass
