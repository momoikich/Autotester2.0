from ToolResult import *
from typeAnnotations import *
import re
import subprocess

class SimJavaResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par SimJava

        Paramètres du constructeur :
            file1, file2: String - Nom des fichiers comparés
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non le test de similitude a passé
    """
    
    def __init__(self, file1 : str, file2 : str, _test : bool, sim : int, details : bytes):
        #s = re.findall(r'\d+', (str(details.decode("utf-8")).split('\n')[-2]))
        if sim == 1 or sim == 0:
            title = 'Il y\'a ' + str(sim) + ' similitude entre ' + file1 + ' et ' + file2
        else:
            title = 'Il y\'a ' + str(sim) + ' similitudes entre ' + file1 + ' et ' + file2
        if _test:      
            result = OK
        else:
            result  = FAILURE

        self.sim = sim

        ToolResult.__init__(self, title, result, details) # type: ignore
