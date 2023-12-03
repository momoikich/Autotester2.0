class HelpDefinition():


    def __init__(self, _title, _description):
        self.title = _title
        self.description = _description
        self.args = []
    
    def add_arg(self, _description):
        self.args.append(_description)

    def __str__(self):
        txt = "| " + self.title + " : " + self.description + "\n"
        for i in range(len(self.args)):
            desc = self.args[i]
            txt += "├── arg" + str(i) + " : " + desc + "\n"
        txt += "\n\n"
        return txt

Help_setup = HelpDefinition("setup", "Met en place votre environnement en créant les dossiers avec les paths rentrés dans le fichier .json si ce n'est pas déjà fait")
Help_setup.add_arg("Le path du fichier .json")

Help_evaluate= HelpDefinition("evaluate", "Lance des batteries de tests sur un étudiant et un TP en particulier")
Help_evaluate.add_arg("La promo de l'étudiant")
Help_evaluate.add_arg("Le login de l'étudiant (ou le nom de son dépôt svn)")
Help_evaluate.add_arg("Le nom du projet")

HelpS = {
    "setup" : Help_setup,
    "evaluate" : Help_evaluate,
}