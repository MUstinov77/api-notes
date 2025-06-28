from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from notes.api.v1 import auth, users, notes
from notes.db import init_db, destroy_db, lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notes.router)

class UniqueException(HTTPException):
    def __init__(self, field):
        super().__init__(status_code=400, detail=f"{field} already exists")
        self.field = field


# @app.on_event("startup")
# def startup():
#     init_db()
#
# @app.on_event("shutdown")
# def shutdown():
#     destroy_db()


@app.exception_handler(UniqueException)
def unique_exception_handler(request, exc: UniqueException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error of unique"}
    )


@app.get("/")
async def root():
    return {"message": "NotesApp"}