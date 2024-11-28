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
        tags = request.form['tags'].split(',')
        liste.nouveau(titre, description, tags)
        return redirect("/")
    


#Pour voir les modifications en cours, voir le chatgtp suivant:
#https://chatgpt.com/share/67452bd7-3bf8-8007-9f4c-4cf0de9837f9


'''
@app.route("/efface",  methods = ['GET', 'POST'])
def efface():
    #titre = request.form['titre']
    #description = request.form['description']
    #tags = request.form['tags']
    selection = request.form['ligne_setectionnee']
    # liste.nouveau(titre, description, tags)
    print(f"efface:{selection}")
    return redirect("/")
'''
@app.route('/submit', methods=['POST'])
def submit():
    uuid = request.form['uuid_selectionnee']
    action = request.form['action']
    if action == "efface":
        
        # TODO Effacer !!!
        liste.enleve(uuid)
        
        pass
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
    