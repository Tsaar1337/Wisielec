import json
import random

from sqlalchemy.exc import IntegrityError

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
    users = session.query(User).order_by(User.wins).all()
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
def get_random_word_from_category(category_name: str) -> Word | None:
    session = Session()
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        session.close()
        return None
    words = session.query(Word).filter_by(category_id=category.id).all()
    session.close()
    if not words:
        return None
    return random.choice(words)
