# Modules Python
import sys
import re

# Fichier stockant les paths utiles
from variables import *

# Module FEAT++ utile pour parcourir le dossier src et importer les autres modules
sys.path.append(featpp_path)
import env

# Sous-programmes principaux
from setup import setup
from evaluate import evaluate
from evaluateAll import evaluateAll
from evaluateOnDemand import evaluateOnDemand

# --------------------------------------------------------------------

# Definitions
def help(sub=None):

    help_file = os.path.join(featpp_path, "main", "resource", "help", "help.txt")

    with open(help_file, "r") as file:
        if sub:
            text = file.read()
            parsed = re.search("\|" + sub + "(.*?)\n\n", text, re.S)
            if parsed:
                print(parsed.group(0))
                return None

        print(file.read())

    file.close()
    sys.exit(1)

# Cas où aucun argument n'est appelé ou si l'utilisateur veut de l'aide
if (len(sys.argv) == 1) or (sys.argv[1] == "help"):
    help()

subprogs = {
    "setup" : [setup, 2],
    "evaluate": [evaluate, len(sys.argv)-2],
    "evaluateAll" : [evaluateAll, len(sys.argv)-2],
    "evaluateOnDemand" : [evaluateOnDemand, len(sys.argv)-2]
}

subprog : list = subprogs.get(sys.argv[1], [help, 0])
nb_args : int = subprog[1]

# Cas où trop peu d'arguments sont appelés
if (nb_args+2 > len(sys.argv)) and (subprog != "setup"):
    help(sys.argv[1])
else:
    # lancer le script voulu
    if (sys.argv[2] == "--commit" and (sys.argv[1] == "evaluate" or sys.argv[1] == "evaluateAll")):
        arg_list = sys.argv[3:nb_args+2]
        subprog[0](True, False, *arg_list)
    elif (sys.argv[2] != "--commit" and (sys.argv[1] == "evaluate" or sys.argv[1] == "evaluateAll")):
        arg_list = sys.argv[2:nb_args+2]
        subprog[0](False, False, *arg_list)
    else:
        arg_list = sys.argv[2:nb_args+2]
        subprog[0](*arg_list)
