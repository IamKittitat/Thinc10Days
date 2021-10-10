from flask import Flask,redirect,url_for , render_template, request,session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Build"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(seconds = 20) # days = 5

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key =True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    #date = ..
    def __init__(self,name,password):
        self.name = name
        self.password = password


@app.route("/",methods=["POST","GET"])
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True 
        user = request.form["UserName"]
        session["user"] = user
        password = request.form["PassWord"]
        session["password"] = password
        found_user = users.query.filter_by(name=user).first()
        if found_user : #if not found , found_user will be none and its go to else
            session["password"] = found_user.password
        else:
            usr = users(user,None)
            db.session.add(usr)
            db.session.commit()
        #return redirect(url_for("user"))
        return render_template("bookie.html",user= user)
    else:
        if "user" in session:
            return render_template("bookie.html",user= user)
        return render_template("signIn.html")

@app.route("/bookie")
def bookie():
    if "user" in session:
        return render_template("bookie.html")
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    #flash(f"You have been logged out!!!","info" ) #category 
    session.pop("user",None)
    session.pop("password",None) 
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
