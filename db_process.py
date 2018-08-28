from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_users import User, Base, Article
from sqlalchemy import desc
from sqlalchemy.pool import StaticPool
import hashlib
def init_db(db_name = 'sqlite:///users.db'):
	engine = create_engine(db_name,connect_args={'check_same_thread': False})
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine, autoflush = True)
	session = DBSession()
	return session

def check_user(email):
	session = init_db()
	user = session.query(User).filter(User.mail == email).one_or_none()
	return user == None

def add_user(name, lastName, group, password, mail):
	session = init_db()
	#password = password.encode('utf-8')
	#password = hashlib.sha256(password).hexdigest()
	new_user = User(name = name, lastName = lastName, 
		group = group, password = password, mail = mail)
	session.add(new_user)
	session.commit()


def log_in(mail, password):
	session = init_db()
	user = session.query(User).filter(User.mail == mail).one_or_none()
	#password = password.encode('utf-8')

	return user != None and user.password == password

def add_post(subject, latitude, longitude, added_by, pic_url, description):
	session = init_db()
	url = longitude+latitude
	if get_article(url) == None: # проверка существует ли запись с таким же именем, если нет, то добавляем
		new_article = Article(subject = subject, latitude = latitude,
		                  longitude = longitude, added_by = added_by, pic_url = pic_url,
		                  description = description,
		                  url = url )
		session.add(new_article)
		session.commit()
		return True
	else:
		return False

def get_article(url):
	session = init_db()
	art = session.query(Article.subject, Article.latitude, 
		Article.longitude, Article.added_by, Article.pic_url, 
		Article.description,Article.created_at).filter(Article.url == url).order_by(Article.ID)
	return art.one_or_none()

def update_article(subject, latitude, longitude, pic_url, description): 
	session = init_db()
	url = longitude+latitude
	try:
		art = session.query(Article).filter(Article.url == url).update({"subject":subject, "latitude":latitude, "longitude":longitude, "pic_url":pic_url, "description":
			description})
		session.commit()
		return True
	except:
		return False


def delete_post(url):
	session = init_db()
	try:
		post = session.query(Article).filter(Article.url == url).delete()
		print(post)
		session.commit()
		return True
	except Exception as err:
		print(err)
		return False

def get_all_posts():
	session = init_db()
	posts = session.query(Article.subject, Article.latitude, 
		Article.longitude, Article.added_by, Article.pic_url, 
		Article.description,Article.created_at).order_by(desc(Article.created_at)).all()
	return posts


#print(get_all_posts())
#add_user("punk", "punk", "ia-11", "123","default")