from fastapi import FastAPI
from routers.notes_router import notes_router

app = FastAPI()

app.include_router(notes_router)


@app.get("/")
async def root():
    return {"message": "NotesApp"}