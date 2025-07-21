from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UniqueException
from app.core.db import lifespan
from app.auth import router as auth
from app.notes import router as notes
from app.users import router as users


def create_app() -> FastAPI:
    app = FastAPI(
        title='NotesApp',
        lifespan=lifespan
    )
    routers = [
        auth.router,
        notes.router,
        users.router
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    @app.exception_handler(UniqueException)
    async def unique_exception_handler(request: Request, exc: UniqueException):
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.detail}
        )

    #include_routers(app, routers)
    for router in routers:
        app.include_router(router)


    return app
