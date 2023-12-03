import os
from Tool import Tool
from JunitResult import JunitResult
import subprocess as sp



class Junit(Tool):

    """
        Classe d'integration de JUnit fondée sur la classe Tool
    """

    def __init__(self):
        Tool.__init__(self,'')

    def run(self, file, classpath, options=[]):

        """
            Lancement de la compilation d'un ou plusieurs fichiers sources Java

            java -cp junit.jar;. junit.textui.TestRunner MaClasseTest
            Paramètres :
                files : String - Le fichier source à tester
                options : liste de String - La liste des options de compilation   
        """

            
        command = ['java'] + ['-cp', classpath] + options + [file]
                    
        compilation = sp.run(command)
        details = str(compilation.stderr)
        test_compil = compilation.returncode==0

        return JunitResult(file, details, test_compil)
    
   
    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass