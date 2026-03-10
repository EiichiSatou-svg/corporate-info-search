from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database
import models
import schemas
import auth

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """ユーザーを登録"""
    existing = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="このユーザーIDはすでに登録されています")

    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(
        user_id=user.user_id,
        user_name=user.user_name,
        user_role=user.user_role,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """ログインしてJWTトークンを取得"""
    user = db.query(models.User).filter(models.User.user_id == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーIDまたはパスワードが間違っています",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.create_access_token(data={"sub": user.user_id})
    return {"access_token": token, "token_type": "bearer"}
