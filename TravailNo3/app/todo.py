from datetime import date
import uuid
from enum import Enum
import json

class Etat(Enum):
    OUVERT = 0
    EN_COURS = 1
    FERMEE = 2

# class Todo:
#     def __init__(self, titre: str = "", description:str = "", tags: list[str] = [], json: dict|None = None) -> None:
        
#         if json == None and titre != "":
#             self.info["uuid"] = uuid.uuid1()
#             self.info["date_creation"] = date.today()
            
#             self.info["titre"] = titre
#             self.info["description"] = description
#             self.info["tags"] = tags
#             self.info["etat"] = Etat.OUVERT
#         elif json != None:
#             self.info = json
#         else:
#             raise ValueError("Erreur à la création d'un todo")
        
class Builder:
    
    def __init__(self) -> None:
        pass

    def nouveau(self, titre: str = "", description:str = "", tags: list[str] = []) -> dict:
        todo = dict()
        todo["uuid"] = str(uuid.uuid1())
        todo["date_creation"] = str(date.today())
            
        todo["titre"] = titre
        todo["description"] = description
        todo["tags"] = tags
        todo["etat"] = Etat.OUVERT.name
        
        return todo
    
    def recupere(self, fichier: str) -> dict:
        with open(fichier, 'r') as f:
            return f.read()
    
    def sauvegarde(self, todo: dict) -> None:
        with open(f"{todo["uuid"]}.json", "w") as f:
            f.write(json.dumps(todo))
            