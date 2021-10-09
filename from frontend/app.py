from flask import Flask,redirect,url_for , render_template, request,session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Build"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes = 1) # days = 5

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key =True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    #date = ..
    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.route("/")
def home():
    return render_template("signIn.html")

@app.route("/bookie")
def bookie():
    return render_template("bookie.html")
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)