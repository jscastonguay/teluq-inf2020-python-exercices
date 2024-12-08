from datetime import datetime
import uuid
from enum import Enum
import json
import os
import re
import asyncio
import aiofiles

class Etat(Enum):
    OUVERT = 0
    EN_COURS = 1
    FERMEE = 2


class ErreurInterne(Exception):
    pass


class ConditionsFiltre:
    def __init__(self) -> None:
        self.etats: list[Etat] = [Etat.OUVERT.name, Etat.EN_COURS.name, Etat.FERMEE.name]
        self.tags: list[str] = []
        
    def reset(self) -> None:
        self.etats: list[Etat] = [Etat.OUVERT.name, Etat.EN_COURS.name, Etat.FERMEE.name]
        self.tags: list[str] = []
        
    def applique(self, element):
        '''
        Si les filtres sont vides, les éléments ne sont pas filtrés.
        '''                
        etatsTrouves = False
        if self.etats == [] or element["etat"] in self.etats:
            etatsTrouves = True
        tagsTrouves = False
        if self.tags == [] or self.tags == [""]:
            tagsTrouves = True
        else:
            for tag in element["tags"]:
                if tag in self.tags:
                    tagsTrouves = True
        return etatsTrouves and tagsTrouves

        
class ListeTodo:
    
    # Singleton
    _repertoire: str = ""
    _liste: list[dict] = []
    
    def __init__(self, repertoire: str) -> None:
        if ListeTodo._liste == []:
            ListeTodo._repertoire: str = repertoire
            asyncio.run(self._recupereListe())

    def nouveau(self, titre: str = "", description:str = "", tags: list[str] = []) -> None:
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
            
    async def _recupere_todo(self, fichier: str) -> None:
        async with aiofiles.open(f"{self._repertoire}/{fichier}", 'r') as f:
            todo = await f.read()
            ListeTodo._liste.append(json.loads(todo))
    
    async def _recupereListe(self):
        
        # TODO Gèrer le fait que le répertoire n'existe peut-être pas
        print("_recupereListe")
        fichers_filtres = []
        fichers = os.listdir(self._repertoire)
        for fichier in fichers:
            if not os.path.isdir(os.path.join(self._repertoire, fichier)):
                split = os.path.splitext(os.path.basename(fichier))
                nom = split[0]
                extension = split[1]
                if self._valide_uuid(nom) and extension == ".json":
                    fichers_filtres.append(fichier)
        if fichers_filtres:
            #ff = [asyncio.create_task(self._recupere_todo(f)) for f in fichers_filtres]
            print("gather")
            await asyncio.gather(*(self._recupere_todo(f) for f in fichers_filtres))
    
    def _sauvegarde(self, todo: dict) -> None:
        if not os.path.exists(self._repertoire):
            os.makedirs(self._repertoire)
        with open(f"{self._repertoire}/{todo["uuid"]}.json", "w") as f:
            f.write(json.dumps(todo))
    
    def get(self, uuid: str = "", filtre: ConditionsFiltre = None) -> list[dict]:
        if uuid:
            todo = list(filter(lambda element: element["uuid"] == uuid, ListeTodo._liste))
            if todo == None:
                raise ErreurInterne("Aucun todo associé à ce uuid")
            if len(todo) > 1:
                raise ErreurInterne("Plusieurs todo associé à ce uuid")
            return todo
        
        if filtre:            
            return list(filter(filtre.applique, ListeTodo._liste))
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
        self._sauvegarde(todo)
        
    def get_nb(self):
        return len(ListeTodo._liste)


if __name__ == "__main__":
    liste = ListeTodo("todo")
    #liste.nouveau("Ceci est un test")
    #liste._recupereListe()
    #print(liste._liste)
    print(liste.get("3f5d27ae-aa78-11ef-b89c-98541b76ef66"))
    print("===================================================================")
    print(liste.get())
    liste.enleve("3f5d27ae-aa78-11ef-b89c-98541b76ef66")