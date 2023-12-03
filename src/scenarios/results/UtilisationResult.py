from typing import List
from ToolResult import *
from typeAnnotations import *

class UtilisationResult(ToolResult) :

    def __init__(self, word : str, file : str, _test : bool, diff : int, _details : str):
        title = "Utilisation de " + word
        if _test:      
            result = OK
            title += ' : OK'
        else:
            result  = FAILURE
            title += ' : ERROR  (pénalité : ' + str(diff) + ' )'
        ToolResult.__init__(self, title, result, _details)
