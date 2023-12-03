from Tool import Tool
from RunAdaResult import RunAdaResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class RunAda():
    
    """
    Classe des tests de checkstyle.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, project_env : ProjectEnv, mainfile, arguments='', timeout=5):

        args = "gnatmake -gnatwa -g -gnata ".split() + [project_env.student_project_folder + "/" + mainfile]
        details = ''

        res = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE, timeout=timeout)

        test_run = False

        se_termine = True

        if res.returncode==0:

            base = mainfile[:mainfile.index('.adb')]
            cmd = ('./' if base[0] not in '/.' else '') + base + (' ' + arguments if arguments else '')
            try:
                    res = sp.run(cmd.split(), timeout=timeout, stdout=sp.PIPE, stderr=sp.PIPE)
            except sp.TimeoutExpired:
                details += 'Execution ne se termine pas !'
                se_termine = False

            details += '\n' + (res.stdout).decode('latin-1')

            test_run = res.returncode==0 and se_termine

        return RunAdaResult([mainfile], arguments, details, test_run) #type: ignore
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
