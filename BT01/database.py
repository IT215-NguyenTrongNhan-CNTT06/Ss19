from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Tự động tạo cơ sở dữ liệu nếu chưa tồn tại
temp_engine = create_engine("mysql+pymysql://root:Chaobacon1234%40@localhost:3306")
with temp_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS session19_ex1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    conn.commit()
temp_engine.dispose()

DATABASE_URL = "mysql+pymysql://root:Chaobacon1234%40@localhost:3306/session19_ex1"

engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
