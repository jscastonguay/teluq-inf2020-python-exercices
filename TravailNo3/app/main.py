from flask import Flask, render_template, redirect, request, url_for
from liste_todo import *
import sys


app = Flask(__name__)
liste = ListeTodo("todo")
conditions = Conditions()

@app.route("/")
def index():
    listeComplete = liste.get(conditions=conditions)        
    return render_template("index.html", liste = listeComplete, filtre = conditions)


@app.route("/ajoute",  methods = ['GET', 'POST'])
def ajoute():
    if request.method == "GET":
        return render_template("ajoute.html")
    else:
        titre = request.form['titre']
        description = request.form['description']
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]
        liste.nouveau(titre, description, tags)
        return redirect("/")
   
   
@app.route('/submit', methods=['POST'])
def submit():
    if 'uuid_selectionnee' in request.form:
        uuid = request.form['uuid_selectionnee']
        action = request.form['action']
        if action == "efface":
            liste.enleve(uuid)
            return redirect("/")
        if action == "modifie":
            return redirect(url_for("modifie", uuid = uuid))
    
    # TODO gère une erreur
    return redirect("/")


@app.route('/modifie', methods=['GET', 'POST'])
def modifie():        
    uuid = request.args.get('uuid')
    todo = liste.get(uuid)[0]
    if request.method == "GET":
        return render_template("modifie.html", todo = todo)
    elif request.method == "POST":
        todo["titre"] = request.form["titre"]
        todo["description"] = request.form["description"]
        todo["tags"] = request.form["tags"].split(',')
        todo["tags"] = [tag.strip() for tag in todo["tags"]]
        todo["etat"] = request.form["etat"]
        liste.modifie(todo)
        return redirect("/")
    
    # TODO Exception: géré le cas d'une méthode qui n'est pas la bonne
    
    
@app.route('/filtre', methods=['POST'])
def filtre():
    action = request.form['action']
    if action == 'reset':
        conditions.reset()
    if action == 'applique':
        conditions.etats = request.form.getlist('filtre-etat')
        conditions.tags = request.form["filtre-tags"].split(',')
        conditions.tags = [tag.strip() for tag in conditions.tags]
    return redirect("/")


@app.route('/tri', methods=['POST'])
def tri():
    conditions.choix_tri = request.form.getlist('tri-selection')
    print(f"tri: {conditions.choix_tri}")
    return redirect("/")
    
    
if __name__ == "__main__":
    app.run(debug=True)
    