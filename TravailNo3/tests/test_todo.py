import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../app/"))

from todo import *

def test__builder_nouveau():
    builder = Builder()
    element = builder.nouveau("Test de builder")
    assert element["titre"] == "Test de builder"
    assert element["uuid"] != ""
    assert element["uuid"] != None
    

def test__builder_sauvegarde():
    builder = Builder()
    element = builder.nouveau("Test de builder")
    builder.sauvegarde(element)