import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
	__tablename__='user'
	ID = Column(Integer, primary_key=True)
	name = Column(String(25), nullable=False)
	lastName = Column(String(25), nullable=False)
	group = Column(String(5), nullable=False)
	password  = Column(String(10), nullable=False)
	mail = Column(String(25), nullable=False)


 
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)