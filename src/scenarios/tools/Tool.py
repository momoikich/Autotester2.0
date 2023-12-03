from typing import List, Optional
from typeAnnotations import *
from ToolResult import ToolResult
from ProjectEnv import ProjectEnv
from abc import ABC, abstractmethod

class Tool(ABC) :

    """ 
        Classe abstraite rassemblant les caractéristiques communes a tous les outils 
        
        Paramètres du constructeur :
            _input : String - Le chemin vers le fichier d'entree de l'outil
            _output : String - Le chemin vers le fichier de sortie de l'outil 
    """
    
    tool_instances : list = []

    def __init__(self, _command : str):
        self.command = _command
        Tool.tool_instances.append(self)

    def __repr__(self):

        """
            Affichage d'un outil lors d'un print
        """

        return self.command

    @abstractmethod
    def run(self, project_env : ProjectEnv, files : List[str], encoding : str = None, classpath : str = None) -> ToolResult:

        """
            Lancement d'une exécution de l'outil sur un ou plusieurs fichiers
            
            Paramètres :
                files : liste de String - La liste des fichiers a passer dans l'outil
        """

        raise NotImplementedError()

    @abstractmethod
    def selfcheck(self, options):

        """
            Lancement d'un test rapide de bon fonctionnement de l'outil
        """
        
        raise NotImplementedError()

def select_arg(arg1 : Optional[str], arg2 : str) -> str:
            if arg1 != None :
                assert arg1 is not None
                return arg1
            else : 
                return arg2