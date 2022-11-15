from datetime import datetime

import pymongo
from flask import Flask, render_template, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm, BlogForm
from db import db
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '50a6db86c49553c132f88f2bb40eaedd'
app.secret_key = '50a6db86c49553c132f88f2bb40eaedd'
mongo_url = "mongodb+srv://aditya:mongopass@cluster0.vjvcgdn.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(mongo_url)
# db = client.blog
bcrypt = Bcrypt(app)


@app.route("/todaysblog")
def todaysBlog():
    today = datetime.today().replace(microsecond=0, hour=0, minute=0)
    posts = db.blogs.find({'time': {'$gte': today}}).sort("_id", pymongo.DESCENDING)
    print()
    return render_template('home.html', posts=posts)


@app.route("/myblog")
def myBlog():
    if "email" in session:
        email = session["email"]
        obj = db.users.find_one({"email": email})["_id"]
        posts = db.blogs.find({"creator": obj}).sort("_id", pymongo.DESCENDING)
        return render_template('home.html', posts=posts)


@app.route("/")
def home():
    posts = db.blogs.find().sort("_id", pymongo.DESCENDING)
    return render_template('home.html', posts=posts)


# @app.route("/logout")
# def logout():
#     for key in list(session.keys()):
#         session.pop(key)
#     redirect(url_for('home'))

@app.route("/write", methods=['GET', 'POST'])
def addBlog():
    if "email" in session:
        form = BlogForm()
        if form.validate_on_submit():
            # print("yes")
            email = session["email"]
            obj = db.users.find_one({"email": email})["_id"]
            username = db.users.find_one({"_id": obj})["username"]
            title = form.title.data
            des = form.blog_des.data
            db.blogs.insert_one({
                "title": title,
                "des": des,
                "author": username,
                "creator": obj,
                "time": datetime.today().replace(microsecond=0)

            })
            flash("Your blog has been successfully published", 'success')
            return redirect(url_for('home'))
        return render_template('blog.html', title='blog', form=form)
    return redirect(url_for('login'))


@app.route("/about")
def about():
    user = session["email"]
    return render_template('home.html')


@app.route("/check")
def check():
    user = session["email"]
    return f"<h1>{user}</h1>"


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash(f"Account created for {form.username.data}! You can login now", 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = db.users
        loginuser = users.find_one({"email": form.email.data})
        if loginuser:

            if bcrypt.check_password_hash(loginuser['password'], form.password.data):
                session["email"] = form.email.data
                flash('you have been logged in', 'success')
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
