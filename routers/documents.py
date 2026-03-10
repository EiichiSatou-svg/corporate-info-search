from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.DocumentResponse])
async def get_documents(db: Session = Depends(database.get_db)):
    """ナレッジ一覧を取得"""
    return db.query(models.Document).all()


@router.get("/{document_id}", response_model=schemas.DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(database.get_db)):
    """ナレッジを1件取得"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if document is None:
        raise HTTPException(status_code=404, detail="ナレッジが見つかりません")
    return document


@router.post("/", response_model=schemas.DocumentResponse)
async def create_document(
    document: schemas.DocumentCreate,
    db: Session = Depends(database.get_db),
):
    """ナレッジを登録"""
    category = db.query(models.Category).filter(models.Category.id == document.category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="指定されたカテゴリが見つかりません")
    new_document = models.Document(**document.model_dump())
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document


@router.put("/{document_id}", response_model=schemas.DocumentResponse)
async def update_document(
    document_id: int,
    document: schemas.DocumentUpdate,
    db: Session = Depends(database.get_db),
):
    """ナレッジを更新"""
    db_document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="ナレッジが見つかりません")

    update_data = document.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_document, key, value)

    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(database.get_db)):
    """ナレッジを削除"""
    db_document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if db_document is None:
        raise HTTPException(status_code=404, detail="ナレッジが見つかりません")
    db.delete(db_document)
    db.commit()
    return {"message": "削除しました"}
