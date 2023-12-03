from typing import List
from ToolResult import *
from typeAnnotations import *

class JavaCompilerResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par le compilateur Java

        Paramètres du constructeur :
            _filenames : String - Nom du fichier compilé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non la compilation a fonctionné
    """
    
    def __init__(self,_filenames : List[str], _details : str, _test : bool):
        title = "Compilation de " + ", ".join(_filenames)
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        ToolResult.__init__(self, title, result, _details)
