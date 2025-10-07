from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite dosyası taskforge.db olarak ana dizinde oluşacak
DATABASE_URL = "sqlite:///./taskforge.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Veritabanını oluşturur (tablolar Base'den türetilir)."""
    Base.metadata.create_all(bind=engine)
