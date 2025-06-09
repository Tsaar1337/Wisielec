"""
Moduł definiujący modele bazy danych SQLAlchemy dla aplikacji Wisielec.

Ten moduł zawiera definicje wszystkich tabel w bazie danych, ich strukturę
oraz relacje między nimi.
"""

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """
    Klasa bazowa dla wszystkich modeli SQLAlchemy.

    Służy jako punkt wyjścia dla deklaratywnego mapowania modeli.
    """

    pass

# Model użytkownika
class User(Base):
    """
        Model reprezentujący użytkownika w systemie.

        Attributes:
            id (int): Unikalny identyfikator użytkownika (klucz główny)
            name (str): Nazwa użytkownika (unikalna, max 32 znaki)
            password_hash (str): Hash hasła użytkownika (max 32 znaki)
            wins (int): Liczba wygranych gier
            losses (int): Liczba przegranych gier
        """

    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

# Model kategorii
class Category(Base):
    """
       Model reprezentujący kategorię słów w grze.

       Attributes:
           id (int): Unikalny identyfikator kategorii (klucz główny)
           name (str): Nazwa kategorii (max 32 znaki)
           words (list[Word]): Lista słów należących do tej kategorii

       Relationships:
           words: Relacja jeden-do-wielu z modelem Word
       """

    __tablename__ = "Category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    words: Mapped[list["Word"]] = relationship(back_populates="category") # relacja do modelu Word

# Model wyrazu
class Word(Base):
    """
        Model reprezentujący słowo do odgadnięcia w grze.

        Attributes:
            id (int): Unikalny identyfikator słowa (klucz główny)
            word (str): Słowo do odgadnięcia (max 32 znaki)
            category_id (int): Identyfikator kategorii (klucz obcy)
            category (Category): Relacja do kategorii, do której należy słowo

        Relationships:
            category: Relacja wiele-do-jednego z modelem Category

        Note:
            Każde słowo musi być przypisane do jakiejś kategorii (category_id nie może być NULL)
        """

    __tablename__ = "Word"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(32), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False) # relacja do modelu Category.id

    category: Mapped["Category"] = relationship("Category", back_populates="words") # relacja do modelu Category
