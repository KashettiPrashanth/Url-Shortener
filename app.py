from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import string
import datetime
import os

app = Flask(__name__)
basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,"data.sqlite")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate (app,db)



class Urls(db.Model):
    __tablename__ = "url_table"
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))
    date= db.Column("date",db.String())
    time=db.Column("time",db.String())

    def __init__(self, long, short,date,time):
        self.long = long
        self.short = short
        self.date= date
        self.time= time
    def __repe__(self):
        return "original url - {} and shorten url-{}, on date {} at time - {}".format(self.long, self.short,self.date,self.time)


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        rand_letters = random.choices(letters, k=4)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form.get("original_url")
        date_received=str(datetime.datetime.now().strftime("%d:%m:%Y"))
        time_received=str(datetime.datetime.now().strftime("%H:%M:%S"))
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url,date_received,time_received)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/sh/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

@app.route('/history')
def display_all():
    return render_template('history.html', vals=Urls.query.all())

if __name__ == '__main__':
    app.run(port=5000, debug=True)