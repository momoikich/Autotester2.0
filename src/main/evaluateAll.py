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
import setup

# Fichier stockant les paths utiles
from variables import *
import json
import csv


def evaluateAll(commit : bool, modalites : bool, matiere : str, tp : str, students_info : str, retour : str, *scenarios_name) -> None:

    # recuperer les informations de tous les etudiants
    students_info = "repository/" + students_info
    students_name = []
    with open(students_info) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            students_name.append(row[3])
    students_name = students_name[1:]

    # evaluer pour chaque etudiant le travail sur le tp d'une matiere
    for student_name in students_name:
        evaluate.evaluate(commit, modalites, matiere, tp, student_name, retour, *scenarios_name)