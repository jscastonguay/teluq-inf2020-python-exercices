from flask import Flask, render_template, redirect, request
import datetime

app = Flask(__name__)

liste_etudiants = ["Alex", "Julie", "Kevin"]

@app.route("/")
def root():
    return render_template("principale.html", liste_etudiants=liste_etudiants)

@app.route("/ajoute", methods = ["POST"])
def ajoute():
    nom = request.form.get("nom")
    liste_etudiants.append(nom)
    return redirect("/")

# @app.route("/ajoute", methods = ["GET"])
# def ajoute():
#     nom = request.args.get("nom")
#     liste_etudiants.append(nom)
#     return redirect("/")


@app.route("/ajoute_autre/<nom>")
def ajoute_autre(nom):
    liste_etudiants.append(nom)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
    