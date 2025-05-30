from .session import Session, engine
from .models import Base
from .models import User, Word, Category

# Funkcja tworząca tabele
def init_db():
    Base.metadata.create_all(bind=engine)



