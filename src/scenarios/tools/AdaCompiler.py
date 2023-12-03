from Tool import Tool
from AdaCompilerResult import AdaCompilerResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class AdaCompiler():
    
    """
    Classe des tests de checkstyle.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, project_env : ProjectEnv, file):

        args = "gnatmake -gnatwa -g -gnata ".split() + [project_env.student_project_folder + '/' + file]

        cp = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)

        details = cp.stdout

        test_compil = cp.returncode==0

        return AdaCompilerResult([file], details.decode('utf-8'), test_compil)
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
