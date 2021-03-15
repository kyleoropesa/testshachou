from fastapi import FastAPI

app = FastAPI()

@app.get("/projects")
async def get_all_projects():
    pass

@app.post("/projects/create")
async def create_project():
    pass


@app.get("/projects/{project_id}")
async def get_project_details(project_id):
    pass

@app.delete("/projects/{project_id}")
async def delete_project(project_id):
    pass

@app.put("/projects/{project_id}/update")
async def update_project(project_id):
    pass


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



