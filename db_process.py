from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import User, Base

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_user(name, lastName, group, password, mail):
	new_user = User(name = name, lastName = lastName, 
		group = group, password = password, mail = mail)
	session.add(new_user)
	session.commit()


def login(mail, password):
	user = session.query(User).filter(User.mail == mail).one()
	if password == user.password:
		return True
	else:
		return False