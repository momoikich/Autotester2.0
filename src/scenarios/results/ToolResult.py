from Result import *
from typeAnnotations import *


class ToolResult(Result) :

    """ 
        Classe générique représentant le résultat d'un outil

        Paramètres du constructeur :
            _title : String - Message titre du résultat
            _result : String - Résultat même de l'outil (e.g "OK" ou "ERROR")
            _details : String - Détails d'execution de l'outil
            penalty: Int - Nombre de pénalités à ajouter en cas d'erreur
    """

    def __init__(self, _title : str, _result : str, _details : str = "", penalty : int = 0):
        Result.__init__(self, _result)
        self.title = _title
        self.details = _details
        self.penalty = penalty


    def get_message(self, mode : int = 1) -> str:
        message = self.title + "\n"

        if mode == 1 :
            message+= self.details

        return message