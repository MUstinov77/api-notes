from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.auth import router as auth
from app.core.db import lifespan
from app.notes import router as notes
from app.users import router as users
from app.me import router as me


def create_app() -> FastAPI:
    app = FastAPI(
        title='NotesApp',
        lifespan=lifespan
    )
    routers = [
        auth.router,
        notes.router,
        users.router,
        me.router
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    #include_routers(app, routers)
    for router in routers:
        app.include_router(router)


    return app
