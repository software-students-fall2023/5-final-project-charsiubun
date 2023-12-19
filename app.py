import os
import mongomock
from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from hashlib import sha256
from github_api import *
from datetime import datetime
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

app = Flask(__name__)

if os.getenv("TESTING"):
    app.config["MONGO_CONN"] = mongomock.MongoClient()
else:
    URI = "mongodb+srv://admin:admin123@blog.mj6rk4x.mongodb.net/?retryWrites=true&w=majority"
    app.config["MONGO_CONN"] = MongoClient(URI)

connection = app.config["MONGO_CONN"]
db = connection["blog"]
blogs = db.blogs
users = db.users

@app.route("/")
def show_login():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def login():
    username = request.form["username"]
    password = sha256(request.form["password"]).hexdigest()
    data = users.find_one({"username": username})
    if data is None:
        return render_template("login.html", error = True)
    if data[password] == password:
        return redirect(url_for("show_home", username = username))
    return render_template("login.html", error = True)

@app.route("/register")
def show_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = sha256(request.form["password"]).hexdigest()
    user_details = get_github_user_details(username, GITHUB_TOKEN)
    rating = calculate_rating(user_details)
    joke = get_feedback(username, rating) 
    if user_details is None:
        return render_template("register.html", error = True)   
    doc = {
        "username": username,
        "password": password,
        "friends": []
    }

    blog = {
        "owner": username,
        "title": username + " has joined the community!!!!",
        "main_body": joke,
        "time": datetime.now()
    }
    users.insert_one(doc)   
    blogs.insert_one(blog)
    return render_template("register.html", success = True)  

@app.route("/home/<username>")
def show_home(username):
    user_details = get_github_user_details(username, GITHUB_TOKEN)
    rating = calculate_rating(user_details)
    joke = get_feedback(username, rating) 
    return render_template("home.html", username = username, rating = rating, joke = joke)

@app.route("/myblogs/<username>")
def show_myblogs(username):
    blogs = blogs.find({"owner": username})
    render_template("myblogs.html", blogs = blogs)

@app.route("/myblogs/<username>", methods=["POST"])
def post_blog(username):
    owner = username
    title = request.form["title"]
    main_body = request.form["main_body"]
    

    doc = {
        "owner": owner,
        "title": title,
        "main_body": main_body,
    }
    blogs.insert_one(doc)
    return render_template("myblog.html", post = True)

@app.route("/friendblogs/<username>")
def show_friendblogs(username):
 
    user = users.find_one({"username": username})

    friends = user["friends"]

    all_friend_blogs = []
    for friend in friends:
        friend_blogs = blogs.find({"owner": friend})
        all_friend_blogs.extend(friend_blogs)
    all_friend_blogs = sorted(all_friend_blogs, key=lambda item: item['date'], reverse=True)
    
    return render_template('friendblogs.html', friend_blogs = friend_blogs)

@app.route("/addfriend/<username>")
def show_addfriend(username):
    return render_template("addfriend.html")

@app.route("/addfriend/<username>", method= "POST")
def addfriend(username):
    pass


@app.route("/checkout/<username>")
def show_checkout(username):
    return render_template("checkout.html", username  = username)

@app.route("/checkout/<username>", method=["POST"])
def checkout(username):
    account = request.form["username"]
    return redirect(url_for("result", username = username, account = account))


@app.route("/delete_blogpost/<title>")
def delete_blogpost(title):
    blogs.delete_one({"title": title})
    return redirect(url_for("show_my_blogposts"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)