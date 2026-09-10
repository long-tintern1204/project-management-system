# 02. THIẾT KẾ DATABASE & KIẾN TRÚC BACKEND FASTAPI

---

## 🗄️ 1. Thiết kế Cơ sở dữ liệu (Database Schema)

Dựa trên yêu cầu của tài liệu đào tạo (W09):
> *"Backend: bảng `projects` (`technologies_csv`, `project_types_csv`, `dev_process_phases_csv`, `deleted_at`) + bảng `tech_tags` + migrations (KHÔNG dùng bảng Technology/ProjectTechnology cũ)."*

### 1.1. Bảng `projects` (Bảng chính)
Lưu trữ toàn bộ 18 trường của dự án dưới dạng bảng đơn (flat model), giúp tối ưu hiệu năng và đơn giản hóa migration:

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    industry VARCHAR(100) NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    is_ongoing BOOLEAN NOT NULL DEFAULT FALSE,
    team_size INTEGER NULL,
    total_man_month NUMERIC(10, 2) NULL,
    team_composition_note TEXT NULL,
    
    -- Lưu mảng chuỗi dưới dạng CSV phân tách bằng dấu phẩy (hoặc JSON string)
    -- Khi đọc ra API, Pydantic Service sẽ tự động chuyển thành List[str]
    technologies_csv TEXT NULL DEFAULT '',
    project_types_csv TEXT NULL DEFAULT '',
    dev_process_phases_csv TEXT NULL DEFAULT '',
    
    outcome_note TEXT NULL,
    source_note TEXT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Cột phục vụ Soft Delete (NULL: còn tồn tại, TIMESTAMP: đã bị xóa)
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

-- Index tăng tốc tìm kiếm và lọc
CREATE INDEX idx_projects_customer_name ON projects(customer_name);
CREATE INDEX idx_projects_project_name ON projects(project_name);
CREATE INDEX idx_projects_deleted_at ON projects(deleted_at);
```

### 1.2. Bảng `tech_tags` (Kho lưu trữ tag công nghệ)
Dùng để quản lý danh mục từ khóa công nghệ tập trung cho tính năng autocomplete:

```sql
CREATE TABLE tech_tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index cho tính năng Autocomplete (Tìm kiếm không phân biệt hoa thường)
CREATE INDEX idx_tech_tags_name_lower ON tech_tags(LOWER(name));
```

### 1.3. Bảng `users` (Phục vụ Auth JWT)
Kế thừa từ nội dung đào tạo tuần W06:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'member', -- 'admin' hoặc 'member'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🏗️ 2. Cấu trúc thư mục Backend FastAPI chuẩn (Sử dụng `services/`)

> [!IMPORTANT]
> **Quy ước kiến trúc**: Toàn bộ nghiệp vụ truy vấn DB, xử lý upsert tag, lọc điều kiện và soft-delete được gom vào tầng **`services/`**, tuyệt đối **KHÔNG dùng thư mục `crud/`** để đảm bảo đúng yêu cầu và phân tách rõ ràng trách nhiệm.

```text
backend/
├── app/
│   ├── core/                       # Cấu hình lõi & hạ tầng
│   │   ├── __init__.py
│   │   ├── config.py               # Quản lý biến môi trường Pydantic Settings
│   │   ├── database.py             # SQLAlchemy Engine & SessionLocal
│   │   └── security.py             # Hàm tạo/giải mã JWT, hash bcrypt, get_current_user
│   │
│   ├── models/                     # SQLAlchemy ORM Models
│   │   ├── __init__.py
│   │   ├── project.py              # Model Project (chứa technologies_csv, deleted_at...)
│   │   ├── tech_tag.py             # Model TechTag
│   │   └── user.py                 # Model User
│   │
│   ├── schemas/                    # Pydantic Schemas (Request/Response DTOs)
│   │   ├── __init__.py
│   │   ├── project.py              # ProjectCreateInput, ProjectResponse, ProjectListResponse
│   │   ├── tech_tag.py             # TechTagResponse
│   │   └── user.py                 # UserCreate, UserLogin, TokenResponse
│   │
│   ├── services/                   # Business Logic Layer (TUYỆT ĐỐI DÙNG SERVICES)
│   │   ├── __init__.py
│   │   ├── project_service.py      # CRUD, Soft delete, Search q, Filter multi-value
│   │   ├── tech_tag_service.py     # Upsert tự động tag mới, Autocomplete search
│   │   └── auth_service.py         # Đăng ký, Đăng nhập, Kiểm tra mật khẩu
│   │
│   ├── routers/                    # API Endpoints (Controller)
│   │   ├── __init__.py
│   │   ├── auth.py                 # POST /auth/register, POST /auth/login
│   │   ├── projects.py             # CRUD /projects (POST, GET, PUT, DELETE)
│   │   ├── tech_tags.py            # GET /tech-tags?q=
│   │   └── health.py               # GET /health (Readiness probe)
│   │
│   └── main.py                     # Khởi tạo FastAPI App, cấu hình CORS, mount routers
│
├── alembic/                        # Database migrations (nếu dùng Alembic)
│   ├── versions/
│   └── env.py
├── tests/                          # Bộ kiểm thử Pytest tự động
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures: TestClient, Test DB, Mock Auth Token
│   ├── test_auth.py                # Test đăng ký, đăng nhập
│   ├── test_projects.py            # Test CRUD 18 fields, Soft delete
│   ├── test_filters.py             # Test Search 'q', Filter multi-value, Paging
│   └── test_tech_tags.py           # Test Upsert & Autocomplete
├── requirements.txt                # Danh sách thư viện Python
├── .env.example                    # File mẫu cấu hình môi trường
└── README.md                       # Hướng dẫn cài đặt & chạy Backend
```

---

## 💻 3. Chi tiết triển khai các tầng (Code mẫu tham khảo)

### 3.1. Model `Project` (Chuyển đổi CSV $\leftrightarrow$ List[str])
Trong file `app/models/project.py`:
```python
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, Date, DateTime
from datetime import datetime
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    project_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_ongoing = Column(Boolean, default=False, nullable=False)
    team_size = Column(Integer, nullable=True)
    total_man_month = Column(Numeric(10, 2), nullable=True)
    team_composition_note = Column(Text, nullable=True)

    # Lưu chuỗi phân tách bởi dấu phẩy
    technologies_csv = Column(Text, default="", nullable=False)
    project_types_csv = Column(Text, default="", nullable=False)
    dev_process_phases_csv = Column(Text, default="", nullable=False)

    outcome_note = Column(Text, nullable=True)
    source_note = Column(Text, nullable=True)
    created_by = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
```

### 3.2. Pydantic Schemas (Validate & Chuyển đổi định dạng)
Trong file `app/schemas/project.py`:
```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import date, datetime

class ProjectCreateInput(BaseModel):
    customer_name: str = Field(..., min_length=1)
    project_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    industry: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_ongoing: bool = False
    team_size: Optional[int] = Field(None, ge=1)
    total_man_month: Optional[float] = Field(None, ge=0.0)
    team_composition_note: Optional[str] = None
    technologies: List[str] = []
    project_types: List[str] = []
    dev_process_phases: List[str] = []
    outcome_note: Optional[str] = None
    source_note: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates_and_ongoing(self):
        if self.is_ongoing and self.end_date is not None:
            raise ValueError("進行中の場合、終了日は入力できません")
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("終了日は開始日以降の日付を指定してください")
        return self

class ProjectResponse(ProjectCreateInput):
    id: int
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int
```

### 3.3. Tầng Service: Logic Upsert Tag & Soft Delete
Trong file `app/services/project_service.py`:
```python
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from app.models.project import Project
from app.schemas.project import ProjectCreateInput
from app.services.tech_tag_service import TechTagService

class ProjectService:
    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Project:
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.deleted_at.is_(None)
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @staticmethod
    def soft_delete(db: Session, project_id: int):
        project = ProjectService.get_by_id(db, project_id)
        project.deleted_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def create(db: Session, input_data: ProjectCreateInput, created_by: str) -> Project:
        # 1. Tự động upsert danh sách tag vào bảng tech_tags
        if input_data.technologies:
            TechTagService.upsert_tags(db, input_data.technologies)

        # 2. Tạo instance Project và lưu các trường CSV
        project = Project(
            customer_name=input_data.customer_name,
            project_name=input_data.project_name,
            description=input_data.description,
            industry=input_data.industry,
            start_date=input_data.start_date,
            end_date=input_data.end_date,
            is_ongoing=input_data.is_ongoing,
            team_size=input_data.team_size,
            total_man_month=input_data.total_man_month,
            team_composition_note=input_data.team_composition_note,
            technologies_csv=",".join(input_data.technologies),
            project_types_csv=",".join(input_data.project_types),
            dev_process_phases_csv=",".join(input_data.dev_process_phases),
            outcome_note=input_data.outcome_note,
            source_note=input_data.source_note,
            created_by=created_by,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
```

Trong file `app/services/tech_tag_service.py`:
```python
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.tech_tag import TechTag
from typing import List

class TechTagService:
    @staticmethod
    def upsert_tags(db: Session, tag_names: List[str]):
        """Tự động kiểm tra và thêm mới tag (so khớp phân biệt hoa thường theo Q4 Mentor)"""
        for raw_name in tag_names:
            name = raw_name.strip()
            if not name:
                continue
            # So khớp phân biệt hoa thường: 'react' và 'React' là 2 tag khác nhau
            exists = db.query(TechTag).filter(TechTag.name == name).first()
            if not exists:
                new_tag = TechTag(name=name)
                db.add(new_tag)
        db.commit()

    @staticmethod
    def search_tags(db: Session, query: str = None) -> List[str]:
        """Tìm kiếm tag phục vụ autocomplete, tối đa 20 kết quả"""
        stmt = db.query(TechTag.name)
        if query:
            stmt = stmt.filter(TechTag.name.ilike(f"%{query.strip()}%"))
        return [row[0] for row in stmt.order_by(TechTag.name).limit(20).all()]
```

---

## 🔒 4. Cấu hình Bảo mật JWT & CORS Middleware

Trong file `app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, projects, tech_tags, health

app = FastAPI(title="プロジェクト管理システム API", version="1.0.0")

# Cấu hình CORS để Frontend React (Vite) gọi được mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tech_tags.router, prefix="/tech-tags", tags=["Tech Tags"])
```
