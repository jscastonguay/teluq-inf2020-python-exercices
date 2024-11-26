from flask import Flask, render_template, redirect, request
from liste_todo import *

app = Flask(__name__)
liste = ListeTodo("todo")

@app.route("/")
def index():
    return render_template("index.html", liste = liste.get())


@app.route("/ajoute",  methods = ['GET', 'POST'])
def ajoute():
    if request.method == "GET":
        return render_template("ajoute.html")
    else:
        titre = request.form['titre']
        description = request.form['description']
        tags = request.form['tags']
        liste.nouveau(titre, description, tags)
        return render_template("index.html", liste = liste.get())
    

if __name__ == "__main__":
    app.run(debug=True)
    