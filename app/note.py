from . import schemas, models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
async def get_notes(db: AsyncSession = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    result = await db.execute(select(models.Note).filter(
        models.Note.title.contains(search)).limit(limit).offset(skip))
    notes = result.scalars().all()
    return {'status': 'success', 'results': len(notes), 'notes': notes}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_note(payload: schemas.NoteBaseSchema, db: AsyncSession = Depends(get_db)):
    new_note = models.Note(**payload.dict())
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {"status": "success", "note": new_note}


@router.patch('/{noteId}')
async def update_note(noteId: str, payload: schemas.NoteBaseSchema, db: AsyncSession = Depends(get_db)):
    note_query = select(models.Note).filter(models.Note.id == noteId)
    result = await db.execute(note_query)
    db_note = result.scalars().first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')
    update_data = payload.dict(exclude_unset=True)
    await db.execute(note_query.filter(models.Note.id == noteId).update(update_data))
    await db.commit()
    await db.refresh(db_note)
    return {"status": "success", "note": db_note}


@router.get('/{noteId}')
async def get_post(noteId: str, db: AsyncSession = Depends(get_db)):
    note_query = select(models.Note).filter(models.Note.id == noteId)
    result = await db.execute(note_query)
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {id} found")
    return {"status": "success", "note": note}


@router.delete('/{noteId}')
async def delete_post(noteId: str, db: AsyncSession = Depends(get_db)):
    note_query = select(models.Note).filter(models.Note.id == noteId)
    result = await db.execute(note_query)
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    await db.execute(note_query.delete())
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
