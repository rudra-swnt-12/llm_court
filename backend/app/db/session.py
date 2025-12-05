from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 2. Create a SessionLocal class
# Each request (e.g., User submits a case) gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Dependency Injection
# This function allows FastAPI to give a database session to any endpoint that asks for it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()