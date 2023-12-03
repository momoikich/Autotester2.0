from Tool import Tool
from SimJavaResult import SimJavaResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class SimJava():
    
    """
    Classe des tests de similitude, compare deux fichiers et retourne les parties similaires.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, project_env : ProjectEnv, file1, file2):
        cmd = 'sim_java -d ' + project_env.student_project_folder + '/' + file1 + ' ' + project_env.student_project_folder + '/' + file2

        cp = sp.run(cmd.split(), stdout=sp.PIPE)

        details = cp.stdout

        check_success = cp.returncode == 1

        s = str(details.decode("utf-8")).count('---')

        return SimJavaResult(file1, file2, check_success, s, details)
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
