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
    """Classe permettant d'appliquer un filtre sur la liste de TODO.
    """
    def __init__(self) -> None:
        self.etats: list[Etat] = [Etat.OUVERT.name, Etat.EN_COURS.name, Etat.FERMEE.name]
        self.tags: list[str] = []
        
    def reset(self) -> None:
        self.etats: list[Etat] = [Etat.OUVERT.name, Etat.EN_COURS.name, Etat.FERMEE.name]
        self.tags: list[str] = []
        
    def applique(self, element: dict) -> bool:
        """Vérifie si un TODO donné diot être filtré ou non.
        
        Noter que si les filtres sont vides, les éléments ne seront pas
        filtrés.

        Args:
            element (dict): Un TODO.

        Returns:
            bool: True si le TODO ne doit pas être retiré de la liste filtrée.
        """
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
    """Classe encapsulant la liste de TODO et définissant du même coup la
    structure d'un TODO.
    """
    
    # Singleton
    _repertoire: str = ""
    _liste: list[dict] = []
    
    def __init__(self, repertoire: str) -> None:
        
        # Le test est nécessaire puisque ListeTodo est un singleton
        if ListeTodo._liste == [] and ListeTodo._repertoire == "":
            ListeTodo._repertoire: str = repertoire
            liste_fichiers = self._get_liste_fichiers()
            if liste_fichiers:
                asyncio.run(self._recupere_liste(liste_fichiers))

    def nouveau(self, titre: str = "", description:str = "", tags: list[str] = []) -> None:
        """Crée un nouveau TODO et le sauvegarde dans un fichier propre à ce
        TODO dont le nom est un UUID.

        Args:
            titre (str, optional): Le titre du TODO. Defaults to "".
            description (str, optional): La description du TODO. Defaults to "".
            tags (list[str], optional): Une liste de tags associés au TODO.
            Defaults to [].
        """
        todo = dict()
        todo["uuid"] = str(uuid.uuid1())
        todo["date_creation"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        todo["etat"] = Etat.OUVERT.name
            
        todo["titre"] = titre
        todo["description"] = description
        todo["tags"] = tags
        
        self._sauvegarde(todo)
        ListeTodo._liste.append(todo)
        
    def _valide_uuid(self, texte: str) -> bool:
        uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
        return re.match(uuid_pattern, texte)

    def _get_liste_fichiers(self) -> list[str]:        
        fichers_filtres = []
        if not os.path.exists(self._repertoire): 
            os.makedirs(self._repertoire)
        fichers = os.listdir(self._repertoire)
        for fichier in fichers:
            if not os.path.isdir(os.path.join(self._repertoire, fichier)):
                split = os.path.splitext(os.path.basename(fichier))
                nom = split[0]
                extension = split[1]
                if self._valide_uuid(nom) and extension == ".json":
                    fichers_filtres.append(fichier)
        return fichers_filtres
    
    async def _recupere_todo(self, fichier: str) -> None:
        async with aiofiles.open(f"{self._repertoire}/{fichier}", 'r') as f:
            todo = await f.read()
            ListeTodo._liste.append(json.loads(todo))
    
    async def _recupere_liste(self, fichiers: list[str]) -> None:
        assert len(fichiers) != 0
        await asyncio.gather(*(self._recupere_todo(f) for f in fichiers))
    
    def _sauvegarde(self, todo: dict) -> None:
        if not os.path.exists(self._repertoire):
            os.makedirs(self._repertoire)
        with open(f"{self._repertoire}/{todo["uuid"]}.json", "w") as f:
            f.write(json.dumps(todo))
    
    def get(self, uuid: str = "", filtre: ConditionsFiltre = None) -> list[dict]:
        """Récupère une liste de TODO selon deux mécanismes: soit par un numéro
        de UUID, auquel cas ue seul TODO est présent dans la liste, soit par un
        filtre défini par 'filtre'. Si aucun des mécanisme n'est sélectionné,
        la méthode retourne toute la liste.

        Args:
            uuid (str, optional): UUID du TODO à récupérer. Defaults to "".
            
            filtre (ConditionsFiltre, optional): Le filtre à utiliser pour la
            recherche. Defaults to None.

        Raises:
            ErreurInterne: Lorsqu'une erreur se produit reliée à la base de
            données (répertoire et fichiers).

        Returns:
            list[dict]: Les TODO sélectionnés.
        """
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
        """Enlève un TODO de la liste.

        Args:
            uuid (str): Le UUID du TODO à enlever.
        """
        todo = self.get(uuid)
        self._liste.remove(todo[0])
        os.remove(f"{self._repertoire}/{uuid}.json")
        
    def modifie(self, todo: dict):
        """Modifie un TODO donnée. Son fichier correspondant sera aussi modifié.

        Args:
            todo (dict): La nouvelle valeur du TODO.
        """
        index = next((i for i, a_modifier in enumerate(ListeTodo._liste) if a_modifier["uuid"] == todo["uuid"]), None)
        ListeTodo._liste[index] = todo
        self._sauvegarde(todo)
        
    def get_nb(self) -> int:
        """Retourne le nombre de TODO total dans la liste.

        Returns:
            int: Le nombre de TODO.
        """
        return len(ListeTodo._liste)
