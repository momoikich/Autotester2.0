# Modules Python
import os
from typing import Dict

# Modules featpp
from typeAnnotations import *

# Fichier qui stocke les paths utiles
from variables import *

class ProjectEnv():

    '''
    Cette classe contient les variables d'environnement utilisées tout au long de l'exécution du framework.
    
    Paramètres du constructeur :
        student_project_folder : String - Chemin du dossier du projet côté élève
        project_folder : String - Chemin du dossier du projet côté enseignant
        path_to_isolate_env : String - Le chemin absolu vers le répertoire isolé crée lors de l'initialisation de l'environement isolé
        isolate_id : String - L'identifiant (unique) de l'environement isolé définit lors de son initialisation
        sources_path : String -
    '''

    def __init__(self, _student_project_folder : str, _project_folder : str, tests = {}, _path_to_isolate_env : str = None, _isolate_id : str = None, _sources_path : str = "sources"):
        
        self.student_project_folder = os.path.abspath(_student_project_folder) 
        self.project_folder = os.path.abspath(_project_folder)
        self.tests = tests
        self.path_to_isolate_env = _path_to_isolate_env
        self.isolate_id = _isolate_id
        self.sources_path = _sources_path
        self.is_isolated = _path_to_isolate_env != None
        

    def move_sources(self):
        
        cp_state=isolate_mv(self.path_to_isolate_env, [os.path.join(self.student_project_folder, "sources", "*"), os.path.join(self.project_folder, "/scriptsTests", "*")])
        return cp_state.stdout