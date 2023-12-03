from ToolResult import *

class JunitResult(ToolResult) :

    """ 
        Classe de traitement des résultats retournés par l'outil Junit'

        Paramètres du constructeur :
            _filename : String - Nom du fichier testé
            _details : String - Détails d'execution de l'outil
            _test_compil : Bool - Booléen correspondant à si oui ou non l'intégralité des tests ont fonctionné
    """
    
    def __init__(self,_filename, _details, _test):
        title = "Exécution de " + _filename
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR'
        ToolResult.__init__(self, title, result, _details)
