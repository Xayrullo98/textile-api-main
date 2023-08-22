from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database url
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://ecozamin:ecozamin#123@localhost:3306/ecozamin'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root@localhost:3306/ecozamin'
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+os.path.join(BASE_DIR, 'bazza.db')
SECRET_KEY = 'SOME-SECRET-KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

engine=create_engine('mysql+pymysql://root@localhost:3306/textile-api')

'$2b$12$HGh59BB/0Z6XvTOtCFFgmuxKOJ7wobyg3feVVYOjmShRbqnVx75UK'


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
