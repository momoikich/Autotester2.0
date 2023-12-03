from Tool import Tool
from ValkyrieResult import ValkyrieResult
from typeAnnotations import *
from ProjectEnv import ProjectEnv
import subprocess as sp
import os
import pathlib


class Valkyrie():
    
    """
    Classe des tests de checkstyle.
    """

    def __init__(self):
        
        Tool.__init__(self,'')
        
    def run(self, project_env : ProjectEnv, mainfile, arguments='', timeout=5):

        args = "gnatmake -gnatwa -g -gnata ".split() + [project_env.student_project_folder + "/" + mainfile]

        res = sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE, timeout=timeout)

        test_run = False
        
        details = ''

        se_termine = True

        if res.returncode==0:

            base = mainfile[:mainfile.index('.adb')]
            cmd = ('./' if base[0] not in '/.' else '') + base + (' ' + arguments if arguments else '')
            try:
                    res = sp.run(('valgrind ' + cmd).split(), check=True, stdout=sp.PIPE, stderr=sp.PIPE, timeout=timeout)
            except (sp.TimeoutExpired, sp.CalledProcessError) as e:
                    se_termine = False

            details += '\n' + (res.stdout).decode('latin-1')            

            test_run = res.returncode==0 and se_termine

            if (not se_termine):
                details += 'Execution avec valkyrie ne se termine pas !'
        else:
            details += '\nLe programme ne compile pas.'

        return ValkyrieResult([mainfile], arguments, details, test_run) #type: ignore
        

    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath("HelloWorld.java")], [])
        pass
