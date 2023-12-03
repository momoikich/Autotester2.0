# Modules Python
import importlib
import sqlite3
import datetime
import sys
import subprocess as sp
from Section import Section

# importer l'outil TestsEtu pour lancer les fichiers tests contenant dans le projet etudiant.
from scenarios.tools.TestsEtu import TestsEtu

# Modules featpp
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from typeAnnotations import *
import utility
import setup

# Fichier stockant les paths utiles
from variables import *

# Instancier l'outil TestsEtu
TestsEtu = TestsEtu()

def evaluate(commit : bool, modalites : bool, matiere : str, tp : str, student_name : str, retour : str, *scenarios_name) -> None:

    '''
    Cycle d'execution manuelle des tests

    Paramètres :
        commit - bool : bool pour savoir si on dépose le fichier retour sur svn
        modalites - bool : bool pour savoir si l'etudiant a demandé une evaluation de son projet à travers le fichier modalites.txt.
        matiere - String : nom de la matière
        tp - String : nom du projet
        student_name - String : Login de l'etudiant
        retour - String : nom du fichier retour
        *scenarios_name - List(String) : Liste de nom de scénarios à effectuer
    '''

   
    #Definition de tous les chemins nécessaires à partir de l'environnement donné en argument
    project_folder = "repository/projects/" + tp # chemin vers dossier du projet ou tp contenant fichier config.py. 
    student_path = matiere + "/" + student_name # chemin vers dossier du projet etudiant. 
    student_project_folder = os.path.join(student_path, tp) # chemin vers le dossier tp chez etudiant.

    # Instancier projectEnv
    project_env = ProjectEnv(student_path + "/" + tp, project_folder)

    # Recuperation de la derniere revision
    
    # definir les variables email et name pour pouvoir pousser au projets Git.
    gitconfig1 = "git config --global user.email \"" + paths["mail"] + "\""
    gitconfig2 = "git config --global user.name \"" + paths["username"] + "\""
    sp.run(gitconfig1, shell = True)
    sp.run(gitconfig2, shell = True)
    
    # definir le lien du depot Git du projet etudiant, en recuperant les variables definiees dans fichier variables.json
    depot = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["gitlabArbre"].split("https://")[1] + "/" + student_name + ".git"

    # creer les dossiers du chemin student_path
    list_directory = student_path.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)    
            
    # faire un Git clone du projet etudiant
    gitClone = "git clone " + depot + " " + student_path
    sp.run(gitClone, shell=True)

    # Recuperer les updates avec git pull
    os.chdir(student_project_folder)
    gitpull = "git pull --no-edit " + depot + " evaluations"
    sp.run(gitpull, shell = True)
    os.chdir("../../../")

    # creer le chemin du fichier destionation du retour
    dest_address = os.path.join(student_project_folder, retour + '.txt')
    
    # Cloner le repository de la matiere et creer la base de données du tp
    setup.setup(matiere,tp)

    #Importation du fichier de configuration du projet
    sys.path.append(project_folder)
    fichier_config = importlib.import_module("config") # Import dynamique du fichier de configuration 
    sys.path.remove(project_folder)
    SCENARIOS = fichier_config.SCENARIOS 
    
    #Selection des scenarios à jouer
    scenarios_to_run =[]

    # ajouter le scenario TestsEtu pour evaluer les tests visibles chez etudiant, 
    
    for scenario in SCENARIOS :
        if scenario.run.__name__ in scenarios_name:
            scenarios_to_run.append(scenario)
        
    # si c'est configuré dans le fichier config.py
    if (fichier_config.Evaluate_TestsEtu == None or fichier_config.Evaluate_TestsEtu):
        scenario_TestEtu = Scenario(testerEtu)
        scenarios_to_run.append(scenario_TestEtu)

    # instancier le chemin de la base de données et le fichier modalites de l'etudiant.
    database_address = os.path.join(project_folder, "database_test.db")
    modalities_address = ""
    if (modalites):
        modalities_address = os.path.join(student_project_folder, "modalites.txt")
        # checkout pour se mettre dans la branche main (il est necessaire de specifier la branche pour eviter l'ambiguité)
        os.chdir(student_project_folder)
        gitchekout = "git checkout main"
        sp.run(gitchekout, shell = True) 
        os.chdir("../../../")
        
    #Jouer les scénarios à jouer
    results = utility.run_scenarios(modalites, scenarios_to_run, database_address, modalities_address, student_name, project_env, SCENARIOS)
    
    # mise à jour de la base de données dans le depot Git apres le jeu des scenarios
    os.chdir(project_folder)
    gitAddCommit = "git add database_test.db && git commit -m \" update automatique de la base de données\""
    sp.run(gitAddCommit, shell = True)

    depot_repo = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["repository_path"].split("https://")[1] + ".git"
    gitpush = "git push " + depot_repo 
    sp.run(gitpush, shell = True)
    os.chdir("../../../")

    # pousser les modifications sur le fichier modalites
    if (modalites):
        os.chdir(student_project_folder)
                        
        gitAddCommit = "git add modalites.txt && git commit -m \" Retour automatique des modalites\""
        sp.run(gitAddCommit, shell = True)

        gitpush = "git push " + depot + " main" 
        sp.run(gitpush, shell = True)
        os.chdir("../../../")

    #Afficher les rapports des resultats des scenarios
    results.append(utility.report(scenarios_to_run, results, database_address, student_name))

    #pousser le retour avec les resultats chez l'etudiant 
    utility.print_results(results, student_project_folder, dest_address , retour + '.txt', depot, 2, commit)

# definir la fonction pour le Scenario TestsEtu
def testerEtu(project_env):
    # definition de la section TestsEtu
    results = [Section("Evaluation TestsEtu ", _title_Lvl = 1)]
    # Utiliser l'outil TestsEtu pour lancer les tests visibles chez etudiant
    run = TestsEtu.run(project_env.student_project_folder, [])
    results.append(run)
    return results