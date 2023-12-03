from typing import List
from ToolResult import *
from typeAnnotations import *

class RunAdaResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non l'exécution a fonctionné
    """
    
    def __init__(self,_filenames : List[str], arguments : str, _details : str, _test : bool):
        title = '\n' + "Exécution sans valgrind " + ", ".join(_filenames) + ' ' + arguments
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        title += '\n' + _details
        ToolResult.__init__(self, title, result, _details)