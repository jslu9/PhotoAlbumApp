from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as _SA_Session
import settings

engine = create_engine(settings.db_connection_string)
Base = declarative_base(bind=engine)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine, class_=_SA_Session)

def create_tables(engine):
    Base.metadata.create_all(engine)

class Photos(Base):
    __tablename__='photos'
    id = Column(Integer, primary_key=True)
    albumId = Column(Integer,
                      ForeignKey('albums.id'),
                      nullable=True)
    title = Column(String)
    url = Column(String)
    thumbnailUrl = Column(String)

class Albums(Base):
    __tablename__='albums'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.id'),
				nullable=True)
    title = Column(String)

class Users(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String)    

if __name__ == "__main__":
    create_tables(engine) 
