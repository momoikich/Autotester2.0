from typing import List
from ToolResult import *
from typeAnnotations import *

class ValkyrieResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non l'exécution avec Valkyrie a fonctionné
    """
    
    def __init__(self,_filenames : List[str], arguments : str, _details : str, _test : bool):
        title = '\n' + "Exécution avec valgrind de " + ", ".join(_filenames) + ' ' + arguments
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        title += _details
        ToolResult.__init__(self, title, result, _details)