
import os
# import mongomock
from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient


app = Flask(__name__)

# if os.getenv("TESTING"):
#     app.config["MONGO_CONN"] = mongomock.MongoClient()
# else:
URI = "mongodb://mongodb:27017/"
app.config["MONGO_CONN"] = MongoClient(URI)

connection = app.config["MONGO_CONN"]
db = connection["blog_app"]
blogs = db.blogs

@app.route("/")
def show_main_screen():
    """
    Show the home page of the application
    """
    return render_template("main_screen.html")


@app.route("/add_blogpost", methods=["POST"])
def add_blogpost():
    """
    Add blogpost to mongodb
    """
    title = request.form["title"]
    main_body = request.form["main_body"]
    

    dup = 0
    static_title = title
    while blogs.count_documents({"title": title}):
        dup += 1
        title = static_title + "_" + str(dup)

    doc = {
        "title": title,
        "main_body": main_body,
        "user":
    }
    blogs.insert_one(doc)
    return render_template("add_blogpost.html", message="Added Successfully")

@app.route("/search_my_blogposts", methods=["POST"])
def search_my_blogposts():
    """
    Show all blogposts that match with the keywords provided
    """
    keywords = request.form["keywords"]
    docs = blogs.find({}).sort("title", 1)
    found = []
    for doc in docs:
        if doc["title"].count(keywords):
            found.append(doc)
    if not found:
        return render_template("search_my_blogposts.html", message="Blogposts Not Found")
    return render_template("search_my_blogposts.html", docs=found, message="")

@app.route("/show_my_blogposts")
def show_my_blogposts():
    """
    Retrive all blogposts from mongodb
    """
    docs = blogs.find({}).sort("title", 1)
    if len(list(blogs.find({}))) == 0:
        return render_template("show_my_blogposts.html")
    return render_template("show_my_blogposts.html", docs=docs)

@app.route("/edit_confirm/<title>", methods=["POST"])
def edit_note_confirm(title):
    """
    Update the edited blogpost in mongodb
    @param title := the original title
    """
    new_title = request.form["title"]
    dup = 0
    static_title = new_title
    while blogs.count_documents({"title": new_title}) and new_title != title:
        dup += 1
        new_title = static_title + "_" + str(dup)
        print(new_title)
    new_main_body = request.form["main_body"]
    update = {}
    update["title"] = new_title
    update["main_body"] = new_main_body
    blogs.update_one({"title": title}, {"$set": update})
    return render_template(
        "edit_blogpost.html",
        title=new_title,
        main_body=new_main_body,
        message="Blogpost Updated",
    )

@app.route("/delete_blogpost/<title>")
def delete_blogpost(title):
    """
    Delete the selected blogpost from mongodb
    """
    blogs.delete_one({"title": title})
    return redirect(url_for("show_my_blogposts"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)