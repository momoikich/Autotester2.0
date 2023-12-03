from ToolResult import *
from typeAnnotations import *

class BlackboxResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non le test en boite noire a fonctionné
    """
    
    def __init__(self, _filename : str, _test : bool, details : str):
        title = "Test en boite noire de " + _filename
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        
        ToolResult.__init__(self, title, result, details)
