from ToolResult import *
from typeAnnotations import *

class pylintResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par pylint

        Paramètres du constructeur :
            _filename : String - Nom de fichier testé
            _test : Bool - Booléen correspondant à si oui ou non le test est passé
            errors : int - Le nombre d'erreurs de pylint dans le fichier
            details : String - Détails d'execution de l'outil
    """
    
    def __init__(self, _filename : str, _test : bool, errors : str, details : str):
        title = errors
        if _test:      
            result = OK
        else:
            result  = FAILURE
        
        ToolResult.__init__(self, title, result, _details = details)