from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ---- Category ----
class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Document ----
class DocumentCreate(BaseModel):
    category_id: int
    title: str
    content: str

class DocumentUpdate(BaseModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    category_id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---- SearchLog ----
class SearchLogCreate(BaseModel):
    query: str
    category_id: Optional[int] = None
    result: int = 0  # 0=成功, 1=失敗

class SearchLogResponse(BaseModel):
    id: int
    query: str
    category_id: Optional[int]
    result: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Search（Difyから呼ぶナレッジ検索用）----
class SearchRequest(BaseModel):
    query: str
    category_id: Optional[int] = None

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    category_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    user_id: str
    user_name: str
    password: str
    user_role: int = 0  # 0=一般社員, 1=管理者

class UserResponse(BaseModel):
    id: int
    user_id: str
    user_name: str
    user_role: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
