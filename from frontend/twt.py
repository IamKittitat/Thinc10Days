from flask import Flask,redirect,url_for , render_template, request,session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Build"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes = 5) # days = 5

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
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True 
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        #found_user = users.query.filter_by(name=user).delete()
        if found_user : #if not found found_user will be none and its go to else
            session["email"] = found_user.email
        else:
            usr = users(user,"")
            db.session.add(usr)
            db.session.commit()
        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email #change email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html",email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"You have been logged out!!!","info" ) #category 
    session.pop("user",None)
    session.pop("email",None)
    
    return redirect(url_for("login"))

'''
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/<name>")
def user(name):
    #return "Hello! This is the main page <h1>Hello<h1>"
    return render_template("index.html",content=name,r=2)

@app.route("/admin/")
def admin():
    return redirect(url_for("user",name = "Admin!")) #function name
'''

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)