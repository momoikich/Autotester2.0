# Modules Python
import datetime
from io import TextIOWrapper
import sqlite3
import sys
import re
from typing import Dict, List
from jinja2 import Template
import functools

# Modules featpp
from Scenario import Scenario, INFINITE_ATTEMPTS
from ToolResult import ToolResult
from Section import Section
from Penalty import Penalty
from typeAnnotations import *
from Result import Result
from ProjectEnv import ProjectEnv
import shutil
import subprocess as sp

# Fichier stockant les paths utiles
from variables import *



class CompromisedFileException(Exception):
    
    '''
        Exception créée pour gérer le fichier modalité compromis d'un étudiant.
    '''
    
    pass


def modalities_text(scenarios : List[Scenario], database_address : str, student_name : str = None) -> str:
    
    '''
        Cette fonction génère le fichier de modalités à l'initialisation lorsque
        student_name est None et pour un étudiant lorsque student_name est un string

        Paramètres de la fonction :
            scenarios : Scenario[] - Liste totale des scénarios demandés par l'enseignant dans 
                                     le fichier de configuration.
            database_address : String - Chemin vers la base de données
            student_name : String - Identifiant de l'étudiant dans la bdd, par défaut a None.    
        
    '''
    # Lecture du template des modalités
    txt = os.path.join(featpp_path, "main", "resource", "modalites.txt")
    with open(txt, "r") as text:
       template = Template(text.read())

    if(student_name == None):

        # Création des valeurs par défaut
        sc_data = [
            ( s.getName(), s.visible, "non", s.nb_attempts, 
            datetime.datetime.today(), datetime.datetime.today(), 0) for s in scenarios
        ]
        # Création du rendu
        return template.render(
            choice_all = "non",
            choice_all_not_limited = "non",
            scenario_data = sc_data
        )

    else:

        sc_data = []

        # Récupération des informations en bdd
        con = sqlite3.connect(database_address)
        cur = con.cursor()

        for s in scenarios:
            cur.execute("SELECT Attempts, Date, Attempts_Done FROM " + s.getName() + " WHERE Students='%s'" % student_name)
            result = cur.fetchone()
            date = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S.%f")
            nextdate = date + datetime.timedelta(seconds = s.delay)
            attempts = int(result[0])
            attempts_done = int(result[2])
            sc_data += [( s.getName(), s.visible, "non", attempts, date, nextdate, attempts_done)]
            
        # Création du rendu
        return template.render(
            choice_all = "non",
            choice_all_not_limited = "non",
            scenario_data = sc_data
        )


    
def send_files(student_project_folder : str, files : List[str], section : str): 
    
    '''
        Cette fonction peremet d'envoyer à l'etudiant les fichiers d'une partie "section"

        Paramètres de la fonction :
            student_project_folder : Strnig - le dossier du tp de l'etudiant
            files : String[] - liste des fichiers à envoyer
            section : String - nom de la partie du tp nécessitant les fichiers files.    
        
    '''
    # recuperer la matiere
    matiere = paths["matiere"]

    # recuperer le nom de l'etudiant et du tp
    list_split = student_project_folder.split(matiere)[1].split("/")
    student_name = list_split[1]
    tp = list_split[2]

    # se mettre dans la branche main
    os.chdir(student_project_folder)
    gitchekout = "git checkout main"
    sp.run(gitchekout, shell = True) 
    os.chdir("../../../")

    # copier les fichiers files au dossier de l'etudiant si ils n'existent deja la dedans
    fournies_path = "repository/projects/"+tp+"/__fournis/"
    files_copied = []
    for file in files:
        if not os.path.exists(os.path.join(student_project_folder, file)):
            shutil.copy(fournies_path+"/"+file, student_project_folder)
            files_copied.append(file)
            
    # pousser les fichiers copiés sur le depot de l'etudiant
    if (files_copied != []):
        os.chdir(student_project_folder)
        for file in files_copied:
                gitAdd = "git add " + file
                sp.run(gitAdd, shell = True)

        gitCommit = "git commit -m \" Envoie automatique des fichiers pour " + section + " \""
        sp.run(gitCommit, shell = True)

        depot = "https://" + paths["username"] + ":" + paths["password"] + "@" + paths["gitlabArbre"].split("https://")[1] + "/" + student_name + ".git"

        gitpush = "git push " + depot + " main"
        sp.run(gitpush, shell = True) 
        os.chdir("../../../")


def parse_modalities(modalities_address : str, scenarios : List[Scenario]) -> Dict[str, str]:
    
    """
        /!\ /!\ TODO - A COMPLETER /!\ /!\

        Paramètres de la fonction :
            modalities_address : String - Chemin vers le fichier de modalités
            scenarios : Scenario[] - A COMPLETER
    """

    # Ouverture du template
    txt = os.path.join(featpp_path, "main", "resource", "modalites.txt")
    with open(txt, "r") as text:
       template = Template(text.read())

    # Développement du template
    subtemplate = template.render(
        choice_all = "{{choice_all}}",
        choice_all_not_limited = "{{choice_all_not_limited}}",
        scenario_data = [ (s.getName(), s.visible, "{{" + s.getName() + "}}", 0, "", "", 0) for s in scenarios]
    ).split("\n")

    # Conversion des données du fichier élève
    answers = {}
    with open(modalities_address, "r") as mod_file:
        studenttxt = mod_file.readlines()

    for i in range(len(subtemplate)):
        r = re.search("(.*)\{\{([a-zA-Z_0-9]+)\}\}", subtemplate[i])
        if r:
            if(len(studenttxt) <= i):
                raise CompromisedFileException
            if(r.group(1) != studenttxt[i][:len(r.group(1))]):
                raise CompromisedFileException
            studenttxt[i] = studenttxt[i][len(r.group(1)):]
                
            r2 = re.search("(oui|non)", studenttxt[i], flags=re.IGNORECASE)
            if not r2:
                raise CompromisedFileException
            answers[r.group(2)] = r2.group(1)
                
    return answers


def get_scenarios(modalities_address : str, scenarios : List[Scenario]) -> List[Scenario]:
    
    """
        Cette fonction permet de récuperer les scénarios qui doivent être joués
        à partir d'un fichier modalités d'un élève, en le comparant au template 
        de modalités. Si jamais l'étudiant a fait des modifications qui perturbent 
        la détection, une exception est levée.

        Paramètres de la fonction :
            modalities_address : String - Chemin vers le fichier modalités de l'étudiant
            scenarios : Scenario[] - Liste de scénarios disponibles
    """
    
    new_scenarios : List[Scenario] = []
    answers = parse_modalities(modalities_address, scenarios)

    # Création de l'association nom - scenario
    scs = {}
    for s in scenarios:
        scs[s.getName()] = s

    # Cas ou l'étudiant souhaite tous les resultats
    if(answers["choice_all"] == "oui"):
        for s in scenarios:
            if(s.visible):
                new_scenarios += [s]
        return new_scenarios

    # Autres cas
    if(answers["choice_all_not_limited"] == "oui"):
        for s in scenarios:
            if(s.visible and s.nb_attempts == INFINITE_ATTEMPTS):
                new_scenarios += [s]
    
    for elt, ans in answers.items():
        if(elt in scs.keys() and elt not in new_scenarios):
            if(ans == "oui"):
                new_scenarios += [scs[elt]]

    return new_scenarios


def run_scenarios(modalites : bool, scenarios : List[Scenario], database_address : str, modalities_address : str, student_name : str, project_env : ProjectEnv, SCENARIOS : List[Scenario]) -> List[List[Result]]:
    
    """
        Cette fonction a pour but principal d'exécuter tous les scénarios donnés.
        Elle va de plus mettre à jour la base de données au niveau des dates et
        du nombre de tentative. Enfin, elle met à jour le fichier modalites.txt des 
        étudiants.

        Paramètres de la fonction :
            modalites : bool - bool pour savoir si l'etudiant a demandé une evaluation de son projet à travers le fichier modalites.txt.
            scenarios : Scenario[] - La liste des scénarios à jouer
            database_address : String - Chemin vers la base de données
            modalities_address : String - Chemin vers le fichier de modalités
            student_name : String - L'identifiant de l'étudiant dans la bdd
            project_env : ProjectEnv - Environnement du projet
            SCENARIOS : Scenario[] - La liste de tous les scénarios fournie par le fichier de configuration
    """

    results = []
    # Ouverture de la bdd
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    for scenario in scenarios :
        # Exécution d'un scénario
        results.append(scenario.run(project_env))
        # le scenario testerEtu est automatique quand est joué, et n'est pas dans la base données
        if (scenario.getName() == "testerEtu"):
            continue
        # Récupération du nombre de tentatives et éventuelle modification s'il n'est pas infini
        cur.execute("SELECT Attempts FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
        attempts = int(cur.fetchone()[0])
        if (attempts != -1):
            attempts += -1
            # Mise à jour du nombre de tentatives si nécessaire
            cur.execute("UPDATE " + scenario.getName() + " SET Attempts = '" + str(attempts) + "' WHERE Students = '%s'" % student_name)
        # Mise à jour de la mark du scénario dans la bdd
        cur.execute("UPDATE " + scenario.getName() + " SET Mark = '" + str(scenario.mark) + "' WHERE Students = '%s'" % student_name)
        # Mise à jour de la dernière date d'utilisation du scénario dans la bdd
        cur.execute("UPDATE " + scenario.getName() + " SET Date = '" + str(datetime.datetime.today()) + "' WHERE Students = '%s'" % student_name)
        # Mise à jour du nombre de tentatives effectués pour ce test
        cur.execute("SELECT Attempts_Done FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
        attempts_done = int(cur.fetchone()[0])
        cur.execute("UPDATE " + scenario.getName() + " SET Attempts_Done = '" + str(attempts_done + 1) + "' WHERE Students = '%s'" % student_name)
        cur.execute("UPDATE " + scenario.getName() + " SET Penalty = '" + str(0) + "' WHERE Students = '%s'" % student_name)
        for result in (scenario.run(project_env)):
            if "Section" not in type(result).__name__:
                cur.execute("SELECT Penalty FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
                penalty = int(cur.fetchone()[0])
                cur.execute("SELECT Mark FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
                mark = int(cur.fetchone()[0])
                cur.execute("UPDATE " + scenario.getName() + " SET Penalty = '" + str(min(mark, penalty + result.penalty)) + "' WHERE Students = '%s'" % student_name)
    # Mise à jour et fermeture de la bdd
    con.commit()
    con.close()
    if (modalites):
        # Ecriture du fichier modalites.txt avec les nouvelles valeurs de la bdd
        with open(modalities_address, "w") as writer:
            writer.write(modalities_text(SCENARIOS, database_address, student_name))
    return results



def create_database(database_address, scenarios, students_list, groupe_tp):
    
    """
        Cette fonction permet de créer la base de données à partir de la liste des
        étudiants et de la liste des scénarios.       

        Paramètres de la fonction :
            database_address : String - Chemin vers la base de données.
            scenarios : Scenario[] - Liste de tous les scénarios renseignés par l'enseignant 
                                     dans le fichier de configuration.
            students_list : String[] - Liste des identifiants des étudiants (ex : Paul Veyet -> pveyet)
    """

    if os.path.exists(database_address):
        os.remove(database_address)

    # Vérification du "bon typage" des scenarios pour le bon fonctionnement des opérations ultérieures
    for sce in scenarios :
        if not isinstance(sce, Scenario) :
            print("Veuillez n'ajouter que des scénarios dans la liste SCENARIOS. Opération avortée.\n")
            sys.exit(4)
    
    # Récupération des noms des scénarios déclarés dans le fichier de configuration
    tables = [scenarios[i].run.__name__ for i in range(len(scenarios))]

    # Création d'une base de données contenant une table par scénario, chacune ayant une colonne par information persistente d'un scenario
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    for t in tables:
        cur.execute("CREATE TABLE " + t + " (Students"
                                            + ", Groupe"
                                            + ", Attempts" 
                                            + ", Date"
                                            + ", Mark" 
                                            + ", Penalty"
                                            + ", Attempts_Done"
                                            + ");")   
    
    # Complétion des tables des scénarios dans la base de données
    row = [""]*(len(tables))
    attempts = [str(scenarios[i].nb_attempts) for i in range(len(scenarios))]
    date = datetime.datetime.today()
    mark = "0"
    penalty = "0"
    attempts_done = "0"
    for k in range(len(tables)):
        row[k] = [(students_list[i], groupe_tp[i], attempts[k], str(date), mark, penalty, attempts_done) for i in range(len(students_list))]
        cur.executemany("INSERT INTO " + tables[k] + " (Students"
                                                    + ", Groupe"
                                                    + ", Attempts" 
                                                    + ", Date"
                                                    + ", Mark" 
                                                    + ", Penalty"
                                                    + ", Attempts_Done"
                                                    + ") VALUES (?, ?, ?, ?, ?, ?, ?);", row[k])
    
    con.commit()
    con.close()



def report(scenarios : List[Scenario], results : List[List[Result]], database_address : str, student_name : str) -> List[Result]:
    
    """
        Cette fonction a pour but de créer une liste de Result qui devra être ajoutée à
        la liste de liste de Result obtenue par run_scenarios. Cette nouvelle liste
        permet l'affichage d'un compte-rendu des scores obtenus sur les scénarios joués.

        Paramètres de la fonction :
            scenarios : Scenario[] - La liste des scénarios à jouer
            results : Result[][] - La liste des résultats obtenus par run_scenarios
            database_address : String - Chemin vers la base de données
            student_name : String - L'identifiant de l'étudiant dans la bdd
    """
    
    # Ouverture de la base de données
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    
    # Initialisation du rapport contenant les scores obtenus pour chaque scénario joué
    score_report : List[Result] = [Section("Compte-rendu concernant les scenarios joues", 6)]
    
    # Compteur de pénalités pour tous les scénarios joués
    penalties_sum = 0
    
    # Score obtenu pour tous les scénarios joués
    score_sum = 0
    
    # Pour chaque scénario joué
    for i in range(len(scenarios)):
        s = scenarios[i]
        # le scenario testerEtu est automatique quand est joué, et n'est pas dans la base données
        if (s.getName() == "testerEtu"):
            continue
        # Compteur de pénalité pour un scénario
        penalty = 0
        score_sum += s.mark
        # Pour chaque résultat obtenu pour ce scénario
        for r in results[i]:
            # Si on trouve une pénalité, on incrémente les compteurs de pénalités
            if isinstance(r, Penalty):
                penalty += r.penalty
                penalties_sum += r.penalty
                
        # Comparaison du score obtenu pour ce cycle avec celui que l'étudiant avait obtenu au cycle précédent
        cur.execute("SELECT Mark FROM " + s.getName() + " WHERE Students = '%s'" % student_name)
        last_mark = int(cur.fetchone()[0])
        current_mark = s.mark - penalty
        
        # Ecriture du message pour indiquer la progression de l'étudiant
        message = s.getName() + " - Vous avez obtenu " + str(current_mark) + "/" + str(s.mark)
        if last_mark < current_mark:
            message += ". C'est mieux que la derniere fois ! (" + str(last_mark) + "/" + str(s.mark) + ")"
        elif last_mark == current_mark:
            message += " comme la derniere fois."
        else:
            message += ". C'est moins bien que la derniere fois. (" + str(last_mark) + "/" + str(s.mark) + ")"
        score_report.append(Section(message))
        
        # Mise à jour de la base de données
        cur.execute("UPDATE " + s.getName() + " SET Mark ='" + str(current_mark) + "' WHERE Students = '%s'" % student_name)
        cur.execute("UPDATE " + s.getName() + " SET Penalty ='" + str(penalty) + "' WHERE Students = '%s'" % student_name)
    
    # Calcul et ajout du score global obtenu pour les scénarios joués
    score_report.append(Section("Score pour les scenarios joues : " + str(score_sum - penalties_sum) + "/" + str(score_sum) + ".\n"))
    
    # Mise à jour effective et fermeture de la base de donnée
    con.commit()
    con.close()
    return score_report


def print_results(results : List[List[Result]], student_project_folder : str, dest_file : str, retour : str, depot : str, mode : int, commit : bool) :
    
    """
        Cette fonction a pour but principal d'appeler les print_result des
        classes d'affichage pour créer les fichiers de rendus détaillés ou synthétiques.

        Paramètres de la fonction :
            results : Result[][] - Liste contenant des listes de Result pour générer l'affichage
            student_project_folder :  Strnig - le dossier du tp de l'etudiant
            dest_file : String - La localisation du fichier dans lequel écrire les résultats
            retour : String - nom du retour
            depot : String - lien du depot de l'etudiant
            mode : Int - Le mode d'écriture (détaillé, synthétique, ...) 
            commit : Bool - pousser ou pas le retour vers le depot de l'etudiant
    """
    # recuperer le tp
    tp = student_project_folder.split("/")[-1]

    # creer les dossiers du chemin dest_file
    list_directory = dest_file.split('/')
    for i in range(0,len(list_directory)):
        try:
            os.mkdir('/'.join(list_directory[0:i]))
        except OSError as error:
            print(error)
    
    # se mettre dans la branche evaluation, ou la creer s'il n'existe pas
    import subprocess as sp
    os.chdir(student_project_folder)
    gitchekout = "git checkout -b evaluations"
    sp.run(gitchekout, shell = True)

    gitchekout = "git checkout evaluations"
    sp.run(gitchekout, shell = True) 
    os.chdir("../../../")

    # Réinitialisation du fichier de destination
    with open(dest_file , "w+") as writer:
        writer.write("")

    # Pour chaque test effectué, écriture dans le fichier de destination
    for list_result in results :
        for result in list_result:
            result.print_result(dest_file, mode)

    # pousser le retour sur le dossier de l'etudiant
    if (commit):
        os.chdir(student_project_folder)
        
        gitAddCommit = "git add " + retour + " && git commit -m \" Retour du test automatique \""
        sp.run(gitAddCommit, shell = True)

        gitpush = "git push " + depot + " evaluations" 
        sp.run(gitpush, shell = True)
        os.chdir("../../../")


def print_overall_progress(database_address : str, students_list : List[str], scenarios_list : List[Scenario]) -> str:
    
    """
        Cette fonction a pour but principal de rédiger le contenu du fichier avancee_globale.txt
        qui sera fourni à l'enseignant lorsqu'il en fera la demande. Cette fonction utilise le template 
        fourni dans le dossier resource : avancee_globale.txt et créera le texte d'un fichier qui sera présent
        dans le dossier du projet de l'enseignant au même niveau que config.py et la base de données.

        Paramètres de la fonction :
            database_address : String - Chemin vers la base de données
            students_list : str[] - La liste des scénarios à jouer
            scenarios_list : Scenario[] - La liste des scénarios du projet
    """
    # Cas illégaux
    if students_list == []:
        return "La liste des etudiants est vide."
    if scenarios_list == []:
        return "La liste des scenarios est vide."
    
    # Ouverture de la base de données
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    
    # Lecture du template de l'avancée globale
    text = os.path.join(featpp_path, "main", "resource", "avancee.txt")
    with open(text, "r") as txt:
        template = Template(txt.read())
    
    # Création des data
    stud_data = {}
    scores = []
    max_score = 0
    
    # Score maximum que peut avoir un étudiant pour ces scénarios
    for s in scenarios_list:
        max_score += s.mark
        
    # Pour chaque élève, on crée un dictionnaire {nom_du_scenario:score_obtenu} de la forme score/note_du_scenario (pourcentage_équivalent%} nb_tentatives tentative(s)
    for student in students_list:
        data = {}
        score = 0
        for scenario in scenarios_list:
            # Récupération de la note de l'élève sur un scénario donné
            cur.execute("SELECT Mark, Attempts_Done FROM " + scenario.getName() + " WHERE Students = '" + student + "';")
            result = cur.fetchone()
            mark = result[0]
            attempts_done = result[1]
            if attempts_done == '0' or attempts_done == '1':
                attempts_msg = ' tentative'
            else:
                attempts_msg = ' tentatives'
            score += int(mark)
            if scenario.mark != 0:
                percentage = (int(mark)/scenario.mark)*100
            else:
                percentage = 100.0
            data[scenario.getName()] = mark + ' / ' + str(scenario.mark) + ' (' + str(percentage) + '%) ' + attempts_done + attempts_msg 
        # Une fois le dictionnaire d'un élève rempli, on l'ajoute à un dictionnaire {nom_eleve:dictionnaire_eleve}
        stud_data[student] = data
        
        # En même temps, on calcule le score global obtenu pour chaque élève et on stocke cette information dans scores
        if max_score != 0:
            total_percentage = (score/max_score)*100
        else:
            total_percentage = 100.0
        scores.append((student, str(score) + ' / ' + str(max_score) + ' (' + str(total_percentage) + '%)'))
    # On trie la liste en fonction des notes croissantes pour repérer les élèves en difficultés en premier.
    scores.sort(key=lambda x: int(x[1].split()[0]), reverse=False)
    
    
    # Fermeture de la base de données
    con.close()
    
    # Création du rendu
    return template.render(
        date = datetime.datetime.today().strftime("%Y-%m-%d_%Hh%Mm%Ss"),
        scores_data = scores,
        students_data = stud_data,
        scenarios_data = [s.getName() for s in scenarios_list] 
    )
