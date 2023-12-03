from Tool import Tool
from BlackboxResult import BlackboxResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class Blackbox():
    
    """
    Classe des tests en boîte noire, compare le résultat d'une exécution d'un programme avec un résultat attendu.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, project_env : ProjectEnv, name_file : str):
        
        entries = project_env.student_project_folder + '/' + name_file + ".run"
        results = project_env.student_project_folder + '/' + name_file + ".computed"
        expected = project_env.student_project_folder + '/' + name_file + ".expected"

        save_point = pathlib.Path().absolute() # Sauvegarde du point actuel
        os.chdir(project_env.student_project_folder)
        cp = sp.run(["sh", entries], stdout=sp.PIPE,timeout=5)
        os.chdir(save_point)

        file = open(results,"w")
        
        file.write(cp.stdout.decode("utf-8"))
        file.close()
        
        diffs = sp.run(["diff","-B",results,expected],stdout = sp.PIPE).stdout.decode("utf-8")
        check_success = (diffs == "")
        
        return BlackboxResult(name_file, check_success, diffs)

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
