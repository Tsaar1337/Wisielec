from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tworzenie silnika SQLite
engine = create_engine("sqlite:///Wisielec.db", echo=False)

# Tworzenie sesji
Session = sessionmaker(bind=engine)