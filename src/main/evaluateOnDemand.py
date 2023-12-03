import os
import time
import subprocess
import sys
from ProjectEnv import ProjectEnv
import evaluate
import setup
import utility
import importlib
import csv

# Fichier stockant les paths utiles
from variables import *

def evaluateOnDemand(project_student_link : str, *tp_folders):

    # recuperer le nom d'etudiant à partir de son lien depot
    student_name = project_student_link.split("/")[-1]

    # recuperer la matiere depuis le fichier .json
    matiere = paths["matiere"]

    print("matiere : " + matiere + " student_name : " + student_name)

    student_path = matiere + "/" + student_name # chemin vers dossier du projet etudiant.

    # creer les dossiers du chemin student_path
    list_directory = student_path.split('/')
    for i in range(0,len(list_directory)+1):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)  

    # definir le lien du depot Git du projet etudiant
    depot = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["gitlabArbre"].split("https://")[1] + "/" + student_name + ".git"
    
    # faire un Git clone du projet etudiant
    gitClone = "git clone " + depot + " " + student_path
    sp.run(gitClone, shell=True)

    # pour chaque tp, realiser l'evaluation
    for tp in tp_folders:

        print("tp : "+ tp)
        # chemin vers dossier tp de l'etudiant
        tp_path = student_path + "/" + tp

        
        # Cloner le repository de la matiere et creer la base de données du tp
        setup.setup(matiere,tp)

        project_folder = "repository/projects/" + tp # chemin vers dossier du projet ou tp contenant fichier config.py. 
        
        # Importation du fichier de configuration du projet, et faire un reload quand on passe au tp prochain
        sys.path.append(project_folder)
        fichier_config = importlib.import_module("config")
        try:
            importlib.reload(fichier_config)
        except UnboundLocalError as error:
            print(error) # Import dynamique du fichier de configuration 
        sys.path.remove(project_folder)

        # recuperer les scenarios demandes sur modalites
        scenarios = []
        modalites = False
        if (os.path.exists(tp_path + "/modalites.txt")):
            modalites = True
            
            scenarios = utility.get_scenarios(tp_path + "/modalites.txt", fichier_config.SCENARIOS)

        # recuperer les scenarios exigés par le professeur
        if (scenarios == [] and fichier_config.SCENARIOS_To_Test != None):
            scenarios = fichier_config.SCENARIOS_To_Test

        scenarios_name = [scenario.run.__name__ for scenario in scenarios]

        # lancer l'evaluation des scenarios                                     
        evaluate.evaluate(True, modalites, matiere, tp, student_name, "evaluations/retour",  *scenarios_name) 
        
        # supprimer l'objet de fichier config afin de le reinstancier pour le prochain tp
        del fichier_config
