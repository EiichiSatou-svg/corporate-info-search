from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.CategoryResponse])
async def get_categories(db: Session = Depends(database.get_db)):
    """カテゴリ一覧を取得"""
    return db.query(models.Category).all()


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
async def get_category(category_id: int, db: Session = Depends(database.get_db)):
    """カテゴリを1件取得"""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")
    return category


@router.post("/", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
):
    """カテゴリを登録"""
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="同じカテゴリ名がすでに存在します")
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
async def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(database.get_db),
):
    """カテゴリを更新"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    """カテゴリを削除"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="カテゴリが見つかりません")
    db.delete(db_category)
    db.commit()
    return {"message": "削除しました"}
