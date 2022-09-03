import uvicorn

from fastapi import FastAPI

from controller.report_controller import report_router
from controller.user_controller import user_router


app = FastAPI(root_path="/report-reader/v1")


@app.get("/")
def healthcheck():
    return "working"


app.include_router(report_router, prefix=app.root_path)
app.include_router(user_router, prefix=app.root_path)


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, debug=True, reload=True)
