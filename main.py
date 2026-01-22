from fastapi import FastAPI

from core.settings import settings
from api.v1.submissions import router as submissions_router
from api.v1.testcases import router as testcases_router
from api.v1.problems import router as problems_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.include_router(submissions_router, prefix="/api/v1")
    app.include_router(testcases_router, prefix="/api/v1")
    app.include_router(problems_router, prefix="/api/v1")


    return app


app = create_app()
