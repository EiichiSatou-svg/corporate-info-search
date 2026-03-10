# 社内情報検索API

社内マニュアルや業務ガイドをデータベースに登録し、DifyのチャットUIから検索・回答できる社内情報検索アプリのバックエンドAPIです。

## 技術スタック

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite（MySQL切り替え可）
- JWT認証（python-jose）
- bcrypt

## ディレクトリ構成

```
.
├── main.py           # アプリエントリーポイント
├── database.py       # DB接続設定
├── models.py         # テーブル定義
├── schemas.py        # リクエスト/レスポンス定義
├── auth.py           # JWT認証
└── routers/
    ├── categories.py # カテゴリCRUD
    ├── documents.py  # ナレッジCRUD
    ├── search.py     # ナレッジ検索・ログ
    └── users.py      # ユーザー認証（任意）
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install fastapi uvicorn sqlalchemy python-jose bcrypt passlib
```

### 2. サーバー起動

```bash
uvicorn main:app --reload
```

### 3. Swagger UIにアクセス

```
http://127.0.0.1:8000/docs
```

## データベース構成

| テーブル | 説明 |
|---|---|
| categories | ナレッジのカテゴリ（IT、人事、総務など） |
| documents | 社内マニュアルや業務手順などのナレッジ本体 |
| search_logs | 検索クエリと成否の記録 |
| users | ユーザー情報・ロール管理（任意） |

## APIエンドポイント

### Categories（カテゴリ）

| メソッド | パス | 説明 |
|---|---|---|
| GET | /categories/ | 一覧取得 |
| GET | /categories/{id} | 1件取得 |
| POST | /categories/ | 登録 |
| PUT | /categories/{id} | 更新 |
| DELETE | /categories/{id} | 削除 |

### Documents（ナレッジ）

| メソッド | パス | 説明 |
|---|---|---|
| GET | /documents/ | 一覧取得 |
| GET | /documents/{id} | 1件取得 |
| POST | /documents/ | 登録 |
| PUT | /documents/{id} | 更新 |
| DELETE | /documents/{id} | 削除 |

### Search（検索・ログ）

| メソッド | パス | 説明 |
|---|---|---|
| POST | /search/ | ナレッジ検索（Difyから呼び出し） |
| POST | /search/logs | 検索ログ登録 |
| GET | /search/logs | ログ一覧取得 |
| GET | /search/logs/failed | 失敗ログのみ取得 |

### Users（ユーザー・任意）

| メソッド | パス | 説明 |
|---|---|---|
| POST | /users/ | ユーザー登録 |
| POST | /users/login | ログイン・JWTトークン取得 |

## Dify連携フロー

```
ユーザーが質問入力
    ↓
POST /search/   ← カテゴリ＋キーワードでナレッジ検索
    ↓
LLMが回答生成
    ↓
POST /search/logs  ← 成否をログに記録（result: 0=成功, 1=失敗）
```

## MySQLへの切り替え

`database.py` の以下の行を変更してください。

```python
# SQLite（デフォルト）
SQLALCHEMY_DATABASE_URL = "sqlite:///./knowledge.db"

# MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/SampleDB"
```

MySQLの場合は `connect_args={"check_same_thread": False}` の行も削除してください。

## 注意事項
- `auth.py` の `SECRET_KEY` は本番環境では必ず変更してください
- cloudflaredなどでローカルサーバーを公開する場合は研修用PCのみで実施してください
