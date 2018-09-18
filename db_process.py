from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_users import User, Base, Article, Comments
from sqlalchemy import desc
from sqlalchemy.pool import StaticPool
import hashlib

def init_db(db_name = 'sqlite:///users.db'): #инициализация инструментов для доступа к базе данных
	engine = create_engine(db_name,connect_args={'check_same_thread': False})
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine, autoflush = True)
	session = DBSession()
	return session

def check_user(email): #проверка есть ли пользователь в базе данных
	session = init_db()
	user = session.query(User).filter(User.mail == email).one_or_none()
	return user == None

def add_user(name, lastName, group, password, mail): #добавление пользователя в базу
	session = init_db()
	#password = password.encode('utf-8')
	#password = hashlib.sha256(password).hexdigest()
	new_user = User(name = name, lastName = lastName, 
		group = group, password = password, mail = mail)
	session.add(new_user)
	session.commit()


def log_in(mail, password): #проверка пары логин\пароль для аутентификации
	session = init_db()
	user = session.query(User).filter(User.mail == mail).one_or_none()
	#password = password.encode('utf-8')

	return user != None and user.password == password

def add_post(subject, latitude, longitude, added_by, pic_url, description): #добавление поста в базу
	session = init_db()
	url = longitude+latitude
	if get_article(url) == None: # проверка существует ли запись с таким же именем, если нет, то добавляем
		new_article = Article(subject = subject, latitude = latitude,
		                  longitude = longitude, added_by = added_by, pic_url = pic_url,
		                  description = description,
		                  url = url, likes = 0)
		session.add(new_article)
		session.commit()
		return True
	else:
		return False

def get_article(url): # получение поста
	session = init_db()
	art = session.query(Article.subject, Article.latitude, 
		Article.longitude, Article.added_by, Article.pic_url, 
		Article.description,Article.created_at).filter(Article.url == url).order_by(Article.ID)
	return art.one_or_none()

def update_article(subject, latitude, longitude, pic_url, description):  # редактирование поста
	session = init_db()
	url = longitude+latitude
	try:
		art = session.query(Article).filter(Article.url == url).update({"subject":subject, "latitude":latitude, "longitude":longitude, "pic_url":pic_url, "description":
			description})
		session.commit()
		return True
	except:
		return False


def delete_post(url): #удаление поста
	session = init_db()
	try:
		post = session.query(Article).filter(Article.url == url).delete()
		session.commit()
		return True
	except Exception as err:
		print(err)
		return False

def get_all_posts(): #получение всех постов
	session = init_db()
	posts = session.query(Article.subject, Article.latitude, 
		Article.longitude, Article.added_by, Article.pic_url, 
		Article.description,Article.created_at, Article.likes).order_by(desc(Article.created_at)).all()
	return posts

def add_like(url): #добавление лайка
	session = init_db()
	post = session.query(Article).filter(Article.url == url).update({"likes": (Article.likes + 1)})
	session.commit()

def add_comment(comment, url): #добавление комментария
	session = init_db()
	post_id = session.query(Article.ID).filter(Article.url == url)
	comm = Comments(user = comment['user'], text = comment['text'], article_id = post_id)
	session.add(comm)
	session.commit()

def get_all_comments(url): #получение всех коментов для одного поста
	session = init_db()
	post_id = session.query(Article.ID).filter(Article.url == url)
	comments = session.query(Comments.text, Comments.user, Comments.id).filter(Comments.article_id == post_id).all()
	return comments

def delete_comment(id):#удаление комментария
	session = init_db()
	comm = session.query(Comments).filter(Comments.id == id).delete()
	session.commit()

def count_comments(url):
	return len(get_all_comments(url))

def get_all_users():
	session = init_db()
	users = session.query(User.name, User.lastName, User.mail).order_by(desc(User.lastName)).all()
	return users