from ToolResult import *
from typeAnnotations import *

class CheckStyleResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par SimJava

        Paramètres du constructeur :
            _filenames : String - Nom des fichiers comparés
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non la comparaison a fonctionné avec 0 erreurs
            errors : int - Le nombre d'erreurs de checkstyle dans le fichier
    """
    
    def __init__(self, _filename : str, _test : bool, errors : int, details : str):
        title = "Test checkstyle de " + _filename.split('/')[-1] + ' => ' + str(errors)
        if errors != 0:
            title += ' (voir checkstyle.log)'
        if _test:      
            result = OK
        else:
            result  = FAILURE
        
        ToolResult.__init__(self, title, result, _details = details)
