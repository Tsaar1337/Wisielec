from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

# Model użytkownika
class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

# Model kategorii
class Category(Base):
    __tablename__ = "Category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    words: Mapped[list["Word"]] = relationship(back_populates="category") # relacja do modelu Word

# Model wyrazu
class Word(Base):
    __tablename__ = "Word"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(32), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False) # relacja do modelu Category.id

    category: Mapped["Category"] = relationship("Category", back_populates="words") # relacja do modelu Category
