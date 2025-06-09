"""
Moduł konfiguracji bazy danych SQLAlchemy dla aplikacji Wisielec.

Ten moduł zawiera podstawową konfigurację połączenia z bazą danych SQLite
i tworzy fabrykę sesji SQLAlchemy.

Attributes:
    engine: Silnik SQLAlchemy skonfigurowany do pracy z bazą SQLite
    Session: Klasa fabryki sesji SQLAlchemy

Note:
    Baza danych jest przechowywana w pliku 'Wisielec.db' w katalogu Database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tworzenie silnika SQLite
engine = create_engine("sqlite:///Database///Wisielec.db", echo=False)

# Tworzenie sesji
Session = sessionmaker(bind=engine)