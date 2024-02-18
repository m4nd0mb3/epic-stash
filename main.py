"""
---
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.base import api_router_v1
from app.core.config import settings

# from app.db.session import engine
# from app.db.base import Base


def include_router(app_server):
    """---"""
    app_server.include_router(api_router_v1, prefix=settings.API_V1_STR)


def configure_static(app_server):
    """---"""

    base_dir = os.path.dirname(__file__)
    print(StaticFiles(directory=base_dir + "/static/uploads").all_directories)
    app_server.mount(
        "/static", StaticFiles(directory=base_dir + "/static/uploads"), name="static"
    )


# def create_tables():
#     """
#     Create Tables
#     """

#     print("create_tables")
#     Base.metadata.create_all(bind=engine)


def start_application():
    """---"""
    origins = ["*"]
    app_server = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        # docs_url=None,
        # redoc_url=None,
    )
    app_server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # configure_static(app_server)
    # create_tables()       #new
    include_router(app_server)
    return app_server


app = start_application()
if __name__ == "__main__":
    import uvicorn

    # if settings.ENV == 'PRD':
    #     print("PRD")
    # if settings.ENV == 'LOCAL':
    #     print("LOCAL")
    # if settings.ENV == 'QAS':
    #     print("QAS")

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, log_level="info", reload=True)
