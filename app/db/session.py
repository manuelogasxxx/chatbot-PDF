#code for session making
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = quote_plus("sifw3Aa")  # correcto

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}@localhost:5433/chatbot"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # útil para debug
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

