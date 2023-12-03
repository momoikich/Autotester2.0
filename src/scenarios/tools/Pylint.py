from Tool import Tool
from PylintResult import pylintResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class pylint():

    """
    Classe des tests de pylint.
    """

    def init(self):

        Tool.init(self,'')

    def run(self, file, result):

        cmd = 'python3 -m pylint'+' '+file+" --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}'"
        cp=sp.run(cmd.split(), stdout=sp.PIPE)

        buffer = open(result,'a')

        details = cp.stdout

        check_success = cp.stdout == 0


        list_erreurs = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('E')]
        list_failures = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('F')]
        list_conventions = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('C')]
        list_warnings = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('W')]
        list_refactor = [ch for ch in str(details.decode("utf-8")).split('\n') if ch.startswith('R')]
        
        my_information = "Test pylint de " + file.split('/')[-1] + " => errors :" + str(len(list_erreurs))
        my_information = my_information + "\nTest pylint de " + file.split('/')[-1] + " => failures : " + str(len(list_failures))
        my_information = my_information +  "\nTest pylint de " + file.split('/')[-1] + " => conventions : " + str(len(list_conventions))
        my_information = my_information +  "\nTest pylint de " + file.split('/')[-1] + " => warnings : " + str(len(list_warnings))
        my_information = my_information +  "\nTest pylint de " + file.split('/')[-1] + " => refactor : " + str(len(list_refactor))
        
        test = len(list_erreurs) == 0

        buffer.write(details.decode("utf-8"))
        buffer.close()
        print(my_information)

        return pylintResult(file, test, my_information, details)


    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("Hello.py")], [])
        pass