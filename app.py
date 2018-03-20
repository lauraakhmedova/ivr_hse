# -*- coding: utf-8 -*-
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











if __name__ == '__main__':
	app.run()
