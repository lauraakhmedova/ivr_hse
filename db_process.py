from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import User, Base
import hashlib

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_user(name, lastName, group, password, mail):
	password = password.encode('utf-8')
	password = hashlib.sha256(password).hexdigest()
	new_user = User(name = name, lastName = lastName, 
		group = group, password = password, mail = mail)
	session.add(new_user)
	session.commit()


def login(mail, password):
	user = session.query(User).filter(User.mail == mail).one()
	password = password.encode('utf-8')
	if user.password == hashlib.sha256(password).hexdigest():
		return True
	else:
		return False