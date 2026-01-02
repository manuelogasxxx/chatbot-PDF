from .session import engine
from .base import Base
from . import models  # IMPORTANTE

def init_db():
    Base.metadata.create_all(bind=engine)