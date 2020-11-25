from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test_db.sqlite")

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name2 = Column(String)
    fullname = Column(String)
    nickname = Column(String)


Base.metadata.create_all(engine)


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
ed_user = User(name2='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
