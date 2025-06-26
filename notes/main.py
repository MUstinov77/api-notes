from fastapi import FastAPI
from notes.api.v1 import auth, users
from notes.db import init_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
def startup():
    init_db()



@app.get("/")
async def root():
    return {"message": "NotesApp"}