from typing import List
from Tool import Tool, select_arg
from JavaCompilerResult import JavaCompilerResult
from Result import Result
from ProjectEnv import ProjectEnv
import subprocess as sp
from typeAnnotations import *


class JavaCompiler(Tool):

    """
        Classe d'integration du compilateur Java fondée sur la classe Tool

        Paramètres du constructeur :
            _encoding : type d'encodage
            _classpath : le chemin où sont stockées les librairies supplémentaires 
            _sourcepath : le chemin où trouver les fichiers à compiler
    """

   
    def __init__(self, 
                _encoding : str = "UTF-8",
                _classpath : str = None,
                command : str = "javac") :

        Tool.__init__(self, command)
        self.encoding = _encoding
        self.classpath = _classpath


    def run(self, project_env : ProjectEnv,
            files : List[str], 
            encoding : str = None, 
            classpath : str = None
            ) -> Result:

        """
            Lancement de la compilation de fichiers sources Java

            Paramètres :
                files : liste de String - La liste des fichiers sources a compiler 
        """

        if project_env.is_isolated:
            sourcepath = "./"
        else:
            sourcepath = project_env.student_project_folder + '/'

        #classpath = select_arg(classpath, self.classpath)
        #Création de la ligne de commande à partir des arguments
        command_line = [
            self.command, 
            "-encoding", select_arg(encoding, self.encoding),
            "-sourcepath", sourcepath
        ] 
        #command_line += (["-cp", classpath] if classpath!= None else [])
        command_line += list(map(lambda f : sourcepath + "/" + f,files))
        
        if project_env.is_isolated:
            compilation = isolate_run(project_env.isolate_id, "-p", command_line)
        else:
            compilation = sp.run(command_line)
        
        if compilation.stderr != None :
            details = str(compilation.stderr)
        else :
            details = ""
        test_compil = compilation.returncode==0
        result_tool = JavaCompilerResult(files, details, test_compil)

        return result_tool

    
    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """
        project_env = ProjectEnv("selfcheck/","./")
        return self.run(["HelloWorld.java"],project_env,sourcepath="./").result=="OK"
    
