from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("principale.html", liste_etudiants = ["Alex", "Julie", "Kevin"])

if __name__ == "__main__":
    app.run()