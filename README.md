# プロジェクト管理システム (Project Performance Management System)

---

## 📌 1. プロジェクト概要

日本市場向けソフトウェア受託開発案件（Offshore、SES、Lab）の情報管理システム：
- **ユーザーインターフェース:** Frontend React (TypeScript + Vite) は REST API 経由でバックエンドと通信し、一覧テーブルと カード表示の2つの表示モードに対応、Chips 形式による柔軟なフィルター管理を提供。

---

## 🚀 2. 環境構築および起動手順（A to Z）

### 2.1 バックエンド起動 (FastAPI)

```bash
# 1. 仮想環境の有効化 (Windows PowerShell):
.\venv\Scripts\Activate.ps1

# (ライブラリ未インストールの場合は実行: pip install -r requirements.txt)

# 2. 環境変数設定ファイル .env の作成 (未作成の場合):
cp .env.example .env

# 3. マイグレーション実行によるDBテーブル作成:
alembic upgrade head

# 4. 日本企業向けサンプルプロジェクトデータ(20件)の投入:
python seed_data.py

# 5. バックエンドサーバー起動 (ポート 8000):
uvicorn app.main:app --reload --port 8000
```
- インタラクティブAPI仕様書 (Swagger UI): `http://localhost:8000/docs`
- ヘルスチェック確認用エンドポイント: `http://localhost:8000/health`

---

### 2.2 フロントエンド起動 (React + Vite)

新しいターミナルウィンドウを開き、以下を実行:

```bash
cd InternTraining-Project-Tracking

# node_modules のインストール (未インストールの場合):
npm install

# React 開発サーバーの起動:
npm run dev
```
- ブラウザでアクセス: `http://localhost:5173`
- サンプル管理者アカウントでログイン:
  - **Email:** `admin@gmail.com`
  - **Password:** `AdminPass123@`

---

## 🧪 3. 自動テスト実行手順 (Pytest)

全モジュールの自動テストを包括的に実行:

```bash
# 全テストスイートの実行:
pytest

# 各テストの詳細結果を表示して実行:
pytest -v

# コア機能（バックボーン）の7件の主要テストを個別実行:
pytest tests/test_core_backbone_7.py -v
```

---

## 👥 4. チーム役割分担 (Team WBS)
- **Long:** 認証モジュール (JWT, Bcrypt)、論理削除 (Soft Delete)、フロントエンド連携、Pytestバックボーンテスト、技術ドキュメント作成。
- **Khanh:** データベース設計、Alembicマイグレーション、Read Engine、全文検索 `q` および OR/AND 複合フィルター検索ロジック。
- **Tuyết:** Pydantic Schemas 設計、Enum定義、技術タグ自動登録（Upsert）機能、技術タグサジェスト API (Autocomplete)。