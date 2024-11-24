from flask import Flask, render_template, redirect, request
from liste_todo import *

app = Flask(__name__)
liste = ListeTodo("todo")

@app.route("/")
def index():
    return render_template("index.html", liste = liste.get())

if __name__ == "__main__":
    app.run(debug=True)
    