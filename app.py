# -*- coding: utf-8 -* -
from flask import Flask
from jinja2 import Template
import jinja2
import os
from flask import request
from flask import make_response, session, redirect, url_for, escape
from db_process import add_post, get_all_posts,\
 log_in, check_user, add_user, get_article, update_article, delete_post
import hashlib
import config

app = Flask(__name__)


template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template,**params):
   t = jinja_env.get_template(template)
   return t.render(params)

def render(template, **kw):
   return render_str(template, **kw)

def check_instagram_link(link): #проверка правильности инстаграм ссылки по наличию определенных деталей
    return link.startswith('<blockquote') and "data-instgrm-permalink" in link \
    and "data-instgrm-version" in link and "//www.instagram.com/embed.js" in link
        
def check_pic_url(link): #проверка правильности ссылки на картинку
    return link.startswith('http') and link[len(link)-3:] in ['jpg','peg', 'png','bmp']


def clear_session():
    session.pop("username",None)
    session.pop("password", None)
    return redirect( url_for("articles_page"))

def check_session():
    if 'username' in session:
        username = escape(session['username'])
        return True
    return False
def set_session(username,password):
    session["username"] = username
    session["password"] = password

def main_page_with_login(login, password):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    data = get_all_posts()
    l = invoke_coords(data)
    if log_in(login, password):
        resp = make_response(render('InstaInterest.html', articles = data, l=l, visibility = "visible", cookies_login = login))
        set_session(login,password)
        return resp
    else:
        resp = make_response(render('InstaInterest.html', articles = data, l=l, visibility = "collapse"))
        return clear_session()

def invoke_coords(data):
    coord_list = []
    for t in data:
        d = {"hintContent":t[0],"balloonContent":t[0], "longit":t[1], "lat":t[2] }
        coord_list.append(d)
        d = {}
    return coord_list

def logout():
    data = get_all_posts()
    l = invoke_coords(data)
    resp = make_response(render('InstaInterest.html', articles = data, l=l,visibility = "hidden"))
    return clear_session()

@app.route('/addnew', methods = ["POST","GET"])
def addnews():
    if request.method == "POST":
        if "logout" in request.form:
            return logout()
        else:
            subject = request.form['subject']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            pic_url = request.form['pic_url']
            added_by = escape(session['username'])
            details = request.form['details']
            instaCheck = request.form.get('instaCheck')
            correct_link = check_instagram_link(pic_url) if instaCheck == "on" else check_pic_url(pic_url)
            if correct_link:
                if add_post(subject, latitude, longitude, added_by, pic_url, details):
                    return render('new_post.html', visibility_ok = "visible", visibility_danger = "collapse",visibility = "visible")
                else:
                    return render('new_post.html', visibility_danger = "visible", visibility_ok = "collapse", visibility = "visible")
            else:
                return render('new_post.html', visibility_danger = "visible", visibility_ok = "collapse", visibility = "visible")
    else:
        return render('new_post.html', visibility_ok = "collapse", visibility_danger = "collapse", visibility = "visible")



@app.route ('/', methods = ['GET','POST'])
def articles_page():
    if request.method == "POST":
        if "logout" in request.form:
            return logout()
        elif "delete" in request.form:
            url = request.form["deleteurl"]
            if delete_post(url):
                return redirect(url_for("articles_page"))
        else:
            login = request.form["login"]
            password = request.form["password"]
            return main_page_with_login(login, password)
    else:
        visibility = "visible" if check_session() else "collapse"  
        data = get_all_posts()
        l = invoke_coords(data)
        resp = make_response(render('InstaInterest.html', articles = data, l=l,
            visibility = visibility, cookies_login = session["username"]  if visibility == "visible" else ""))
        return resp


@app.route('/register', methods = ['GET','POST'])
def add_artcle():
    if request.method == "GET":
        return render ('register.html', visibility_ok = "collapse", visibility_danger = "collapse")
    else:
        if "enter" in request.form:
            password = request.form['password']
            login = request.form['login']
            return main_page_with_login(login, password)
        elif "register" in request.form:
            name = request.form['name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if check_user(email):
                add_user(name, last_name, "defaultgroup", password, email)
                resp = make_response(render ('register.html', visibility_ok = "visible", visibility_danger = "collapse"))
                set_session(email,password)
                return redirect(url_for('articles_page'))
            else:
                return render ('register.html', visibility_ok = "collapse", visibility_danger = "visible")


@app.route("/edit/<path:url>",methods = ['GET','POST'])
def edit(url):
    t = get_article(url)
    if request.method == "GET":
        return render("edit.html", visibility_ok = "collapse", visibility_danger = "collapse",t = t)
    else:
        subject = request.form['subject']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        pic_url = request.form['pic_url']
        description = request.form['details']
        instaCheck = request.form.get('instaCheck')
        correct_link = check_instagram_link(pic_url) if instaCheck == "on" else check_pic_url(pic_url) 
        if correct_link:
            if update_article(subject, latitude, longitude, pic_url, description):
                return redirect(url_for('articles_page'))  
            else:
                return render("edit.html", visibility_ok = "collapse", visibility_danger = "visible",t = t)
        else:
            return render("edit.html", visibility_ok = "collapse", visibility_danger = "visible",t = t)

@app.route("/admin",methods = ['GET','POST'])
def admin():
    if request.method == "GET":
        return render("admin.html")
    else:
        login = hashlib.sha256(request.form['login'].encode("utf-8")).hexdigest()
        password = hashlib.sha256(request.form['password'].encode("utf-8")).hexdigest()
        if login == config.login and password == config.password:
            set_session("superuser", password)
            return redirect(url_for("articles_page"))
        else:
            return render("admin.html")



app.secret_key = b'hx\x85\r5/\xf2\xe5c&\x0c&\x9d\xff\xc7\xe8\xbc\x01%#h\x99/Y'
if __name__ == '__main__':
	app.run(debug = True)



#old articcles page just in case
'''articles_dirs = get_all_files('static/uploads')
    articles = {} #словарь статей
    pictures = {} #словарь картинок
    path = ''
    for key in articles_dirs:
        for item in articles_dirs[key]:
                if item.split(".")[1] == "txt":

                    path = 'static/uploads/'+key +'/'+item
                    with open(path, 'r') as f:
                        articles[key] = f.read()
                elif item.split(".")[1] in ['jpeg','jpg','png'] :
                    pictures[key] = '/static/uploads/'+key +'/'+item
    print(pictures)'''