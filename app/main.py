from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Import router auth đã viết
from app.api.routers import auth

load_dotenv()
# 1. Khởi tạo ứng dụng FastAPI với tiêu đề dự án chuẩn
app = FastAPI(
    title="プロジェクト管理システム API",
    description="プロジェクト管理システム バックエンドAPI (FastAPI + React)",
    version="1.0.0",
)
# 2. Cấu hình CORS (Cross-Origin Resource Sharing)
# Cho phép Frontend React chạy ở cổng 5173 có thể kết nối tới Backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Cho phép các nguồn Frontend trên
    allow_credentials=True,        # Cho phép gửi kèm cookie/authorization header
    allow_methods=["*"],           # Cho phép tất cả phương thức HTTP (GET, POST, PUT, DELETE,...)
    allow_headers=["*"],           # Cho phép tất cả các headers
)
# 3. Đăng ký các router vào app
app.include_router(auth.router)

# 4. Endpoint kiểm tra sức khỏe hệ thống

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "db": "ok",
    }
    
# 5. Endpoint gốc (Health check)
@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "プロジェクト管理システム APIが正常に稼働しています",
        "docs_url": "/docs",
    }

