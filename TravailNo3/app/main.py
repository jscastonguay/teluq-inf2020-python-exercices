from flask import Flask, render_template, redirect, request, url_for, abort, Response
from liste_todo import *


app = Flask(__name__)
liste = ListeTodo("todo")
conditions_filtre = ConditionsFiltre()


@app.route("/")
def index() -> str:
    """Retourne la page d'accueil de l'application web.

    Returns:
        str: La page d'accueil en HTML.
    """

    try:
        liste_filtree = liste.get(filtre=conditions_filtre) 
    except:
        abort(500)
    return render_template("index.html", liste = liste_filtree, filtre = conditions_filtre)


@app.route("/ajoute",  methods = ['GET', 'POST'])
def ajoute() -> str | Response:
    """Retourne la page permettant d'ajouter un TODO si la méthode est GET.
       Si la méthode est POST, applique le nouveau TODO entré par l'usager
       et redirige à la page d'accueil.

    Returns:
        str | Response: La page qui permet l'ajout ou une redirection à la
        page d'accueil.
    """
    if request.method == "GET":
        return render_template("ajoute.html")
    else:
        titre = request.form['titre']
        description = request.form['description']
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]
        try:
            liste.nouveau(titre, description, tags)
        except:
            abort(500)
        return redirect("/")
   
   
@app.route('/submit', methods=['POST'])
def submit() -> Response:
    """Applique une sélection à la liste de TODO.

    Returns:
        Response: Si l'action est 'efface', enlève le TODO de la liste et
        redirige vers la page d'accueil. Si l'action est 'modifie' redirige
        vers la page qui permet de modifier un TODO.
    """
    if 'uuid_selectionnee' in request.form:
        uuid = request.form['uuid_selectionnee']
        action = request.form['action']
        assert(action == "efface" or action == "modifie")
        if action == "efface":
            try:
                liste.enleve(uuid)
            except:
                abort(500)
            return redirect("/")
        if action == "modifie":
            return redirect(url_for("modifie", uuid = uuid))
    return redirect("/")


@app.route('/modifie', methods=['GET', 'POST'])
def modifie() -> str | Response:    
    """Permet la modification d'un TODO.

    Returns:
        str | Response: La page qui permet la modification d'un TODO si la
        méthode est GET ou applique les modifications et redirige vers la page
        d'accueil.
    """
    uuid = request.args.get('uuid')
    try:
        todo = liste.get(uuid)[0]
    except:
        abort(500)
    
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
    abort(501)
    
    
@app.route('/filtre', methods=['POST'])
def filtre() -> Response:
    """Applique un filtre défini par l'usager.

    Returns:
        Response: Retourne la page d'accueil.
    """
    action = request.form['action']
    assert(action == 'reset' or action == 'applique')
    if action == 'reset':
        conditions_filtre.reset()
    if action == 'applique':
        conditions_filtre.etats = request.form.getlist('filtre-etat')
        conditions_filtre.tags = request.form["filtre-tags"].split(',')
        conditions_filtre.tags = [tag.strip() for tag in conditions_filtre.tags]
    return redirect("/")
    
    
if __name__ == "__main__":
    app.run(debug=True)
    