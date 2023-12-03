from Tool import Tool
from ChangedFileResult import ChangedFileResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class ChangedFile():
    
    """
    Classe des tests de similitude, compare si deux fichiers sont similaires.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, file1, file2):
        
        cmd = 'cmp ' + file1 + ' ' + file2

        cp = sp.run(cmd.split(), stdout=sp.PIPE)

        details = cp.stdout

        check_success = cp.returncode == 1

        return ChangedFileResult(file1, file2, check_success, details)
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
