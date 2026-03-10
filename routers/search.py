from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import database
import models
import schemas

router = APIRouter()


@router.post("/", response_model=List[schemas.SearchResult])
async def search_documents(
    search: schemas.SearchRequest,
    db: Session = Depends(database.get_db),
):
    """
    Difyからのナレッジ検索リクエストを処理する。
    queryをtitle・contentに対して部分一致で検索し、ヒットしたドキュメントを返す。
    category_idが指定されている場合はカテゴリでも絞り込む。
    """
    query = db.query(models.Document)

    if search.category_id is not None:
        query = query.filter(models.Document.category_id == search.category_id)

    results = query.filter(
        models.Document.title.contains(search.query)
        | models.Document.content.contains(search.query)
    ).all()

    return results


@router.post("/logs", response_model=schemas.SearchLogResponse)
async def create_search_log(
    log: schemas.SearchLogCreate,
    db: Session = Depends(database.get_db),
):
    """
    Difyからの検索ログ登録リクエストを処理する。
    result: 0=成功（回答できた）, 1=失敗（回答できなかった）
    """
    new_log = models.SearchLog(**log.model_dump())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


@router.get("/logs", response_model=List[schemas.SearchLogResponse])
async def get_search_logs(db: Session = Depends(database.get_db)):
    """検索ログ一覧を取得（管理者確認用）"""
    return db.query(models.SearchLog).order_by(models.SearchLog.created_at.desc()).all()


@router.get("/logs/failed", response_model=List[schemas.SearchLogResponse])
async def get_failed_logs(db: Session = Depends(database.get_db)):
    """失敗した検索ログのみ取得（管理者向け）"""
    return (
        db.query(models.SearchLog)
        .filter(models.SearchLog.result == 1)
        .order_by(models.SearchLog.created_at.desc())
        .all()
    )
