from fastapi import APIRouter

notes_router = APIRouter(
    prefix='/notes',
    tags=['notes']
)

@notes_router.get('/')
async def get_user_notes():
    return {'message': 'User notes here'}


@notes_router.get('/{note_id}')
async def get_note(note_id: int):
    return {'message': f'Note {note_id} here'}


@notes_router.put('/')
async def create_note():
    return ...


@notes_router.delete('/{note_id}')
async def delete_note(note_id: int):
    return ...


async def