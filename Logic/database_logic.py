from sqlalchemy.exc import IntegrityError

from Database import Session, User


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