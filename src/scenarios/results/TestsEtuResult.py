from ToolResult import *

class TestsEtuResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par l'outil TestEtu'

        Paramètres du constructeur :
            _filenames : String - Noms des fichiers testés
            _details : String - Détails d'execution de l'outil
            _test : Bool - Booléen correspondant à si oui ou non l'intégralité des tests ont fonctionné
    """
    
    def __init__(self,_filenames, _details, _test):
        title = "Exécution de " + ", ".join(_filenames)
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        ToolResult.__init__(self, title, result, _details)
