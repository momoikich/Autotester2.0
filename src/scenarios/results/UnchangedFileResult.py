from typing import List
from ToolResult import *
from typeAnnotations import *

class UnchangedFileResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par Diff

        Paramètres du constructeur :
            file1 : String - Nom du fichier fournis
            file2 : String - Nom du fichier de l'étudiant
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non le test a fonctionné
    """
    
    def __init__(self,file1 : str, file2 : str, _test : bool, _details : str):
        title = "Fichier " + file2.split('/')[-1] + ' non modifié ... '
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        ToolResult.__init__(self, title, result, _details)
