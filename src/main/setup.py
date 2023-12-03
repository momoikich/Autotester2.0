# Modules Python
import importlib
import sqlite3
import datetime
import sys
import subprocess as sp

# Modules featpp
from Scenario import Scenario
from ProjectEnv import ProjectEnv
from typeAnnotations import *
import utility
import evaluate

# Fichier stockant les paths utiles
from variables import *
import json
import csv


def setup(matiere : str, tp : str):

    # definir le lien du depot Git repository de la matiere, en recuperant les variables definiees dans fichier variables.json
    depot_repo = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["repository_path"].split("https://")[1] + ".git"
    
    # cloner le depot localement
    gitClone = "git clone " + depot_repo
    sp.run(gitClone, shell=True)

    project_folder = "repository/projects/" + tp # chemin vers dossier du projet ou tp contenant fichier config.py
    database_address = os.path.join(project_folder, "database_test.db") # chemin de la base de données
    students_info = "repository/1sn-autotester.csv"  # To do : chercher le fichier csv des etudiants dans le dossier  

    # recuperer les informations de tous les etudiants
    groupe_tp = []
    students_name = []
    with open(students_info) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            students_name.append(row[3])
            groupe_tp.append(row[4])
    students_name = students_name[1:]
    groupe_tp = groupe_tp[1:]

    # Creating a database of all students and scenarios if it doesn't exist
    if not os.path.exists(database_address):
        sys.path.append(project_folder)
        try :
            fichier_config = importlib.import_module("config")
        except ModuleNotFoundError:
            sys.path.remove(project_folder)
            print("Fichier config.py non trouvé ou mal écrit. Opération avortée.\n")
            sys.exit(1)
        sys.path.remove(project_folder)
        utility.create_database(database_address, fichier_config.SCENARIOS, students_name, groupe_tp)
    
    return students_name
    