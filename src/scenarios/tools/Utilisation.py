from Tool import Tool
from UtilisationResult import UtilisationResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class Utilisation():
    
    """
    Classe des tests de similitude, compare si deux fichiers sont similaires.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, word, file, occurrences):
        
        cmd = 'grep -c ' + word + ' ' + file

        cp = sp.run(cmd.split(), stdout=sp.PIPE)

        details = cp.stdout

        if occurrences != 0:
            diff = int(details.decode('utf-8')) - occurrences
        else:
            diff = - int(details)

        test = diff >= 0

        return UtilisationResult(word, file, test, diff, details)
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
