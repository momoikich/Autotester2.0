from ToolResult import *
from typeAnnotations import *

class PytestResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par pytest

        Paramètres du constructeur :
            _filename : String - Nom de fichier testé
            _test : Bool - Booléen correspondant à si oui ou non le test est passé
            errors : int - Le nombre d'erreurs dans le fichier
            details : String - Détails d'execution de l'outil
    """
    
    def __init__(self, _filename : str, _test : bool, errors : str, details : str):
        title = "Test pytest de " + _filename 
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        
        ToolResult.__init__(self, title, result, _details = details)