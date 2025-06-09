"""
Moduł inicjalizacyjny bazy danych dla aplikacji Wisielec.

Ten moduł importuje wszystkie niezbędne komponenty bazodanowe i dostarcza
funkcję do inicjalizacji struktury bazy danych.

Imports:
    Session: Fabryka sesji SQLAlchemy
    engine: Silnik bazy danych SQLAlchemy
    Base: Klasa bazowa dla modeli deklaratywnych
    User: Model użytkownika
    Word: Model słowa
    Category: Model kategorii
"""

from .session import Session, engine
from .models import Base
from .models import User, Word, Category

# Funkcja tworząca tabele
def init_db():
    """
       Inicjalizuje strukturę bazy danych.

       Tworzy wszystkie tabele zdefiniowane w modelach, jeśli jeszcze nie istnieją.
       Wykorzystuje silnik zdefiniowany w module session.

       Note:
           - Funkcja jest bezpieczna do wielokrotnego wywołania
           - Nie nadpisuje istniejących tabel
           - Tworzy tabele: User, Category, Word

       Example:
           from Database import init_db

           # Inicjalizacja bazy danych
           init_db()
       """

    Base.metadata.create_all(bind=engine)



