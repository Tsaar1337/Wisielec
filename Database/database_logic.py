import json
import random

from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from Database import Session, User, Category, Word


def login(username: str, password: str) -> User | None:
    session = Session()
    user = session.query(User).filter_by(name=username, password_hash=password).first()
    session.close()
    return user


def register(username: str, password: str) -> bool:
    new_user = User(name=username, password_hash=password)
    session = Session()
    try:
        session.add(new_user)
        session.commit()
        session.close()
    except IntegrityError as e:
        session.rollback()
        session.close()
        return False
    return True

def get_all_users_order_by_wins() -> list[User]:
    session = Session()
    users = session.query(User).order_by(desc(User.wins)).all()
    session.close()
    return users

def load_words_from_json(path):
    session = Session()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for cat_data in data["categories"]:
        # Sprawdź, czy kategoria już istnieje
        category = session.query(Category).filter_by(name=cat_data["name"]).first()
        if not category:
            category = Category(name=cat_data["name"])
            session.add(category)
            session.commit()  # żeby mieć dostęp do category.id

        for word_text in cat_data["words"]:
            word = Word(word=word_text, category_id=category.id)
            session.add(word)

    session.commit()
    session.close()

def get_random_word_from_category(category_name):
    session = Session()
    try:
        # Używamy joinedload aby załadować relację category od razu
        word = session.query(Word).options(joinedload(Word.category)) \
            .join(Category) \
            .filter(Category.name == category_name) \
            .order_by(func.random()) \
            .first()

        if word:
            # Zapisujemy nazwę kategorii jako atrybut obiektu
            word._category_name = word.category.name if word.category else None
        return word
    finally:
        session.close()

def add_win_to_user(user_id: int) -> None:
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return
    user.wins += 1
    session.commit()
    session.close()

def add_lose_to_user(user_id: int) -> None:
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        return
    user.losses += 1
    session.commit()
    session.close()