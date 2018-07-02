# -*- coding: utf-8 -* -
from flask import Flask
from jinja2 import Template
import jinja2
import os
from flask import request
from mail import *

app = Flask(__name__)


template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(template,**params):
   t = jinja_env.get_template(template)
   return t.render(params)

def render(template, **kw):
   return render_str(template, **kw)

def make_message(subject, full_story, name, group):
    msg = ("%s <BR> %s <BR> отправлено: %s <BR> группа: %s"% (subject, full_story, name, group))
    return msg

def get_all_files(p):
    dirs_dict = {}
    current_folder = os.path.join(os.path.dirname(__file__), p )
    for path, subdirs, files in os.walk(current_folder):
        for dir in subdirs:
            dirs_dict[dir] = os.listdir(current_folder+ '//'+dir)
    return dirs_dict

@app.route('/addnews', methods = ["POST","GET"])
def hello_world():
    if request.method == "POST":
        subject = request.form['subject']
        full_story = request.form['full_story']
        name = request.form['name']
        group = request.form['group']
        #print(make_message(subject, full_story, name, group))
        send_mail(make_message(subject, full_story, name, group))
        return render('eskis.html')
    else:
        return render('eskis.html')



@app.route ('/', methods = ['GET','POST'])
def articles_page():
    articles_dirs = get_all_files('static/uploads')
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
    print(pictures)
    d1 = {"hintContent":'ЦПКИО им Горького',"balloonContent":"ФОнтанная площадь", "longit":"55.729126", "lat":"37.601452" }
    d2 = {"hintContent":'ЦПКИО им Горького',"balloonContent":"Пионерский пруд", "longit":"55.730288", "lat":"37.605100" }
    l = []
    l.append(d1)
    l.append(d2)
    #print(l)
    return render('InstaInterest.html', articles = articles, pictures = pictures, l=l)


@app.route('/register', methods = ['GET','POST'])
def add_artcle():
    if request.method == "GET":
        return render ('register.html')
    #написать запрос данных к странице






if __name__ == '__main__':
	app.run(debug = True)
