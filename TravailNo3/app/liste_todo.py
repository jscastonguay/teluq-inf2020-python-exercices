from datetime import datetime
import uuid
from enum import Enum
import json
import os
import re

class Etat(Enum):
    OUVERT = 0
    EN_COURS = 1
    FERMEE = 2


class ErreurInterne(Exception):
    pass

        
class ListeTodo:
    
    # Singleton
    _repertoire: str = ""
    _liste: list[dict] = []
    
    def __init__(self, repertoire: str) -> None:
        if ListeTodo._liste == []:
            ListeTodo._repertoire: str = repertoire
            self._recupereListe()

    def nouveau(self, titre: str = "", description:str = "a", tags: list[str] = ["b"]) -> None:
        todo = dict()
        todo["uuid"] = str(uuid.uuid1())
        todo["date_creation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        todo["etat"] = Etat.OUVERT.name
            
        todo["titre"] = titre
        todo["description"] = description
        todo["tags"] = tags
        
        self._sauvegarde(todo)
        ListeTodo._liste.append(todo)
        
    def _valide_uuid(self, texte: str):
        uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        return re.match(uuid_pattern, texte)
            
    def _recupereListe(self):
        
        # TODO Gèrer le fait que le répertoire n'existe peut-être pas
        fichers = os.listdir(self._repertoire)
        for fichier in fichers:
            if not os.path.isdir(os.path.join(self._repertoire, fichier)):
                split = os.path.splitext(os.path.basename(fichier))
                nom = split[0]
                extension = split[1]
                if self._valide_uuid(nom) and extension == ".json":
                    with open(f"{self._repertoire}/{fichier}", 'r') as f:
                        ListeTodo._liste.append(json.load(f))
    
    def _sauvegarde(self, todo: dict) -> None:
        if not os.path.exists(self._repertoire):
            os.makedirs(self._repertoire)
        with open(f"{self._repertoire}/{todo["uuid"]}.json", "w") as f:
            f.write(json.dumps(todo))
    
    def get(self, uuid: str = "") -> list[dict]:
        if uuid:
            todo = list(filter(lambda element: element["uuid"] == uuid, ListeTodo._liste))
            if todo == None:
                raise ErreurInterne("Aucun todo associé à ce uuid")
            if len(todo) > 1:
                raise ErreurInterne("Plusieurs todo associé à ce uuid")
            return todo
        else:
            return ListeTodo._liste
        
    def enleve(self, uuid: str) -> None:
        todo = self.get(uuid)
        self._liste.remove(todo[0])
        
        # TODO géré les exceptions: si un fichier n'existe pas
        os.remove(f"{self._repertoire}/{uuid}.json")
        
    def modifie(self, todo: dict):
        
        #TODO géré les exceptions
        index = next((i for i, a_modifier in enumerate(ListeTodo._liste) if a_modifier["uuid"] == todo["uuid"]), None)
        ListeTodo._liste[index] = todo





if __name__ == "__main__":
    liste = ListeTodo("todo")
    #liste.nouveau("Ceci est un test")
    #liste._recupereListe()
    #print(liste._liste)
    print(liste.get("3f5d27ae-aa78-11ef-b89c-98541b76ef66"))
    print("===================================================================")
    print(liste.get())
    liste.enleve("3f5d27ae-aa78-11ef-b89c-98541b76ef66")