from fastapi import FastAPI
from notes.routers import auth_router, notes_router

app = FastAPI()

app.include_router(notes_router.notes_router)
app.include_router(auth_router.auth_router)


@app.get("/")
async def root():
    return {"message": "NotesApp"}