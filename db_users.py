import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

Base = declarative_base()

class User(Base):
	__tablename__='user'
	ID = Column(Integer, primary_key=True)
	name = Column(String(25), nullable=False)
	lastName = Column(String(25), nullable=False)
	group = Column(String(5), nullable=False)
	password  = Column(String(10), nullable=False)
	mail = Column(String(25), nullable=False)

class Article(Base):
    __tablename__='article'   
    ID = Column(Integer, primary_key=True,autoincrement=True)
    subject = Column(String(), nullable=False)
    latitude = Column(String(), nullable=False)
    longitude = Column(String(), nullable=False)
    added_by = Column(String(), nullable=False)
    pic_url = Column(String(), nullable=False)
    description  = Column(String(), nullable=False)
    url = Column(String(), nullable=False)
    created_at = Column(Date, default=datetime.datetime.now())
    likes =  Column(Integer, nullable = False)

class Comments(Base):
    __tablename__='comments' 
    id = Column(Integer, primary_key=True,autoincrement=True)
    article_id = Column(Integer, ForeignKey('article.ID',ondelete = "CASCADE"),nullable=False,)
    user = Column(String(25), nullable=False)
    text = Column(String(), nullable=False)

    def __str__(self):
        return [self.text, self.user]

 
engine = create_engine('sqlite:///users.db',connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)