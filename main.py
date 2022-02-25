import os
import subprocess
import argparse

DEFAULT_CNF_FILE = "exemple1.cnf"
DEFAULT_LITTERAL = "-5 7 4 3 0"

def negation_litterale(litteral):
    """
        cette fonction vas retourner la negation du literalle

        on a: un literalle representer dans une BC par "1 2 -3 0" est sous la forme "a ou b ou non c",
        donc la negation du litteral est "non a et non b et c" donc on aura 3 literaux "non a" "non b"
        et "c" ce qui vas etre representer dans une BC par "-1 0", "-2 0" et "3 0"

        parametres:
            litteral (str): chaine de caracteres contenant le literal
        retours:
            neg_litterals(str): la negation du literalle
            la taille du litteral (int): le nombre de clause dans la negation du literale
            max variable dans le literale: la plus grosse variable dans la negation du litteral
    """
    # premierement on separe le literalle en plusieurs partie
    litteral = litteral.split(" ")
    #on convertit en entier en enlevan le 0
    litteral = [int(i) for i in litteral if i != "0"]
    # on applique
    litteral = [-i for i in litteral]
    neg_litterals = ""
    for i in litteral:
        neg_litterals += "{} 0\n".format(i)
    return neg_litterals, len(litteral), max([abs(i) for i in litteral])

def insertion(cnf_path_file, litteral):
    neg_litterals, nb_lignes, maxVar = negation_litterale(litteral)
    with open(cnf_path_file, 'r') as cnf_file:
        BC = cnf_file.read()
    BC = BC.split("\n")
    i = 0
    while (BC[i] == "" or BC[i][0] != "p"):
        # le but de cette boucle est de ne pas prendre en compt les commentaires
        # et saut de lignes au debuts du fichier
        # presents particulierement dans les fichier benchmark donner
        i+=1

    BC[i].replace("\t", " ")
    s1, s2, nbVars, nbClauses = [s for s in BC[i].split(" ") if s!=""]
    nbClauses, nbVars = (int(nbClauses), int(nbVars))
    nbClauses += nb_lignes
    if maxVar > nbVars:
        nbVars = maxVar

    BC[i] = " ".join([s1, s2, str(nbVars), str(nbClauses)])
    BC = "\n".join(BC)
    if BC[-1] != '\n':
        BC += '\n'

    BC += neg_litterals
    temp_BC = os.path.basename(cnf_path_file)[:-4] + "_temporraire.cnf"
    with open(temp_BC, 'w') as temp_cnf_file:
        temp_cnf_file.write(BC)

def satisfiable(cnf_path_file, operating_system):
    """ fonction qui verifie si une BC est satisfiable ou non en appelant execute_SATSolver """
    if operating_system == "windows":
        return not (b"No Solution found" in execute_SATSolver(cnf_path_file, operating_system))
    elif operating_system == "linux":
        return not (b"UNSATISFIABLE" in execute_SATSolver(cnf_path_file, operating_system))

def execute_SATSolver(cnf_path_file, operating_system):
    """ fonction qui execute un solveur SAT, ubcsat pour windows et picosat pour linux, et retourne le resultat """
    if operating_system == "windows":
        return subprocess.check_output(['ubcsat', '-alg', 'saps', '-i', '{}'.format(cnf_path_file), '-solve'])
    elif operating_system == "linux":
        process = subprocess.Popen(['picosat', '{}'.format(cnf_path_file)],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        returncode = process.wait()
        return process.stdout.read()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", "--cnf_file", help="""The path of the cnf file""")
    parser.add_argument("-litteral", "--litteral", help="""input literal""")
    parser.add_argument("-windows", "--windows", action='store_true', help="""est ce que le programme doit s'executer sur windows""")
    parser.add_argument("-linux", "--linux", action='store_true', help="""est ce que le programme doit s'executer sur linux""")
    return parser.parse_args()

def windows_or_linux(args):
    if args.windows and not args.linux:
        return "windows"
    elif not args.windows and args.linux:
        return "linux"
    elif not args.windows and not args.linux:
        return "windows"
    else:
        # raise an exeption there
        raise ValueError()

def main():
    # on recupere la valeur du chemin du fichier .cnf (notre base de connaissance)
    # ainsi que le literal, si aucune valeur n'a etait donner on y asigne les parametre par defaut
    args = parse_arguments()
    litteral = args.litteral
    cnf_path_file = args.cnf_file
    if cnf_path_file is None:
        cnf_path_file = DEFAULT_CNF_FILE
    if litteral is None:
        litteral = DEFAULT_LITTERAL
    operating_system = windows_or_linux(args)

    # debut de l'algorithme
    if satisfiable(cnf_path_file, operating_system):
        insertion(cnf_path_file, litteral)
        temp_BC = os.path.basename(cnf_path_file)[:-4] + "_temporraire.cnf"
        if satisfiable(temp_BC, operating_system):
            print("la base de connaissance {} infére le litteral {}".format(os.path.basename(cnf_path_file), litteral))
        else:
            print("la base de connaissance {} n'infére pas le litteral {}".format(os.path.basename(cnf_path_file), litteral))
        # supprimer le fichier temporraire
        os.remove(temp_BC)
    else:
        raise ValueError("you must give a saitsfiable BC first")

if __name__ == "__main__":
    main()
