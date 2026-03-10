from fastapi import FastAPI
from routers import categories, documents, search, users
import database
import models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="社内情報検索API")

app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(documents.router,  prefix="/documents",  tags=["Documents"])
app.include_router(search.router,     prefix="/search",     tags=["Search"])
app.include_router(users.router,      prefix="/users",      tags=["Users"])
