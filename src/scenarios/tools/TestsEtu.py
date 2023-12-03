import os
from Tool import Tool
from TestsEtuResult import TestsEtuResult
import subprocess as sp
from typing import Dict, List



class TestsEtu(Tool):

    """
        Classe éxecutant les fichiers tests visibles chez Etudiants fondée sur la classe Tool
    """

    def __init__(self):
        Tool.__init__(self,'')

    def run(self, projetETU : str, files : List[str]):

        """
            Lancement de la compilation et l'execution des fichiers tests visibles chez l'etudiant
            javac -cp projectEtu:repository/junit-4.12.jar MaClasseTest.java
            java -ea -cp projectEtu:repository/junit-4.12.jar:repository/hamcrest-core-1.3.jar:. org.junit.runner.JUnitCore MaClasseTest

            Paramètres :
                projetETU : String - dossier du tp de l'etudiant
                files : String[] - liste des fichiers contenant les fichiers tests à evaluer
        """
        details = ""
        test_ok = True
        files_runed = []
        # si la liste files est vide, alors prendre tous les fichiers contenus dans le dossier tp
        if files == []:
            files = os.listdir(projetETU)
        
        # supprimer tous les fichiers .class pour une recompilation 
        os.chdir(projetETU)
        rmClasses = "rm *.class"
        sp.run(rmClasses, shell = True)
        os.chdir("../../../")
        
        for file in files:
            # detecter les fichiers de tests
            if "Test" in file and file.endswith('.java'):
                print(file)
                test_file = file
                files_runed.append(test_file)
                test_path = os.path.join(projetETU, test_file)
                classpath_comp = projetETU+":repository/junit-4.12.jar"
                classpath_exec = projetETU+":repository/junit-4.12.jar:repository/hamcrest-core-1.3.jar"
                
                if os.path.exists(test_path):
                    # compiler le fichier test
                    compilation = sp.run(['javac', '-cp', classpath_comp,  test_path])
                    details += str(compilation.stderr)
                    if (compilation.returncode==0):
                        # executer le fichier test
                        execution = sp.run(['java', '-ea', '-cp', classpath_exec, "org.junit.runner.JUnitCore",  test_file.split('.')[0]])
                        details += str(execution.stderr)
                        if (execution.returncode!=0):
                            test_ok = False
                    else:
                        test_ok = False
                else:
                    test_ok = False

        return TestsEtuResult(files_runed, details, test_ok)
    
    def selfcheck(self):

        """
            Lancement d'une execution de fichier test de mini-projet du tob
        """

        return self.run([os.path.abspath("tob/khammi/mini-projet")], ["CercleTest.java"])
        pass

        