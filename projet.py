from turtle import *            # importe la bibliotheque turtle
from queue import LifoQueue     # importe la bibliotheque pour la liste LIFO (Last In First Out)
import sys                      # importe la bibliotheque 

# dans l'ordre : liste conservant les positions/directions a memoriser; l'axiome, liste contenant les regles; le niveau; l'angle de rotation;
# la longueur que doit parcourir la tortue a chaque avancee; le chemin du fichier definissant le Lsystem; le nom du fichier de sortie;
# les actions a realiser; le fichier de sortie; la reponse de l'utilisateur (si OUI ou NON il veut afficher les actions dans le terminal)
global queuePos, axiom, rules, level, angle, length, lSysPath, outFileName, actions, outFile, inTerminal


def error(message, critical=False):         # affiche un message en fonction de l'erreur survenue
    print('Erreur : ' + message)            # affiche l'erreur adéquate dans le terminal
    if critical:
        exit()                              # ferme le programme si l'erreur est critique


def actionsInTerminal(): # verifie et retourne la reponse de l'utilisateur
    inTerminal = input("Voulez vous afficher chaque action au fur et a mesure dans le terminal ? 'OUI' ou 'NON' ? ").upper() # recupere la reponse de l'utilisateur
    while inTerminal != 'OUI' and inTerminal != 'NON': # tant que la reponse n'est ni OUI ni NON
        inTerminal = input("Faute de frappe ! Veuillez ecrire 'OUI' ou 'NON' : ").upper() # redemande a l'utilisateur
    return inTerminal


def output(message, inTerminal = 'NON'):    # permet d'écrire l'ensemble des actions effectuees dans un fichier
    global outFile                          # fichier de sortie
    outFile.write(message + '\n')           # ajoute les actions dans le fichier de sortie
    if inTerminal == 'OUI':                 # si l'utilisateur veut les commandes dans le terminal
        print(message)                      # affiche les commandes dans le terminal


def instructionsVerif(data, line):          # verifie la validite de la definition du LSystem voulu (axiome, regles, niveau, angle, taille)
    # si l'on est dans le cas de definition de l'axiome, ou bien du niveau ou de la taille et que ces deux derniers sont bien des entiers
    if (data == 'axiom') or ((data == 'level' or data == 'length') and (line.split('=')[1]).strip(' \n\t').isdigit()):
        return True
    if data == 'angle':                     # dans le cas de la definition de l'angle
        try:
            var = float(line.split(' = ')[1]) # verifie que ce soit un reel
            return True                     # retourne vrai si c'est le cas
        except:
            return False                    #sinon, condition non verifiee
    return False


def pathVerif():                            #verifie la validite du chemin du fichier definissant le LSystem
    try:
        lSysFile = open(lSysPath, "r")      #essaye d'ouvrir le fichier en mode ecriture avec le chemin renseigne
    except:
        error("Chemin non valide", True)    #si cela n'est pas possible, envoie un message d'erreur adapte


def verifExistOfVar(i, varType='other'):    # verifie si les options de commandes sont renseignees selon certains cas
    try:
        if varType == 'other':              # cas par defaut
            sys.argv[i+1]                   # verifie si la première option de commande existe
            return True                     # retourne vrai si elle existe
        if varType == 'size':               # verifie dans le cas ou l'on precise la taille de la fenetre
            sys.argv[i+1]
            sys.argv[i+2]                   # verifie si les deux premières options de commande existent
            return True                     # retourne vrai si elles existent
        if varType == 'color':              # verifie dans le cas ou l'on veut changer les couleurs des L-Systems
            sys.argv[i+1]
            sys.argv[i+2]
            sys.argv[i+3]                   # verifie si les trois options de commande existent
            return True                     # retourne vrai si elles existent
    except:
        return False                        # retourne faux dans tous les autres cas


def defineFile():                           # verifie et initialise les options -i et -o
    global lSysPath, outFileName            #variable du chemin du fichier donnant les regles du lSystem et celle du fichier de sortie
    lSysPath = str()                        # chemin du fichier donnant les regles du L-System voulu
    outFileName = str()                     # nom du fichier contenant les commandes realisees lors de l'execution
    i = 0                                   # compteur d'arguments initialise à 0
    for arg in sys.argv:                    #parcourt les arguments
        if arg == '-i' and verifExistOfVar(i): # cas ou l'on definit le chemin du fichier de regles du LSysstem
            lSysPath = sys.argv[i+1]        # recupere le chemin passe en ligne de commande (argument suivant)
        if arg == '-o' and verifExistOfVar(i) and sys.argv[i+1][0] != '-': #cas ou l'on definit le fichier de sortie
            outFileName = sys.argv[i+1]     # recupere le nom du fichier de sortie (argument suivant)
        i += 1                              # passe a l'argument suivant
    if not lSysPath:                        # si le chemin du fichier de LSystem n'est pas defini
        lSysPath = input("Entrer le chemin du fichier du L-Systeme voulu : ") #redemande le chemin du fichier de LSystem a l'utilisateur
    if not outFileName:                     # si le nom du fichier de sortie n'est pas defini
        outFileName = input("Entrer le nom du fichier qui contiendra les commandes utilises : ") #redemande le nom du fichier de sortie a l'utilisateur


def defineSize():                           # definit la taille de la fenetre du programme si precise par l'utilisateur
    i = 0                                   # compteur d'arguments
    for arg in sys.argv:                    # parcourt les arguments
        #cas de la modification de la taille de la fenetre et verifie que les arguments existent et soient des nombres
        if arg == '-s' and verifExistOfVar(i, 'size') and sys.argv[i+1].isnumeric() and sys.argv[i+2].isnumeric():
            return [int(sys.argv[i+1]), int(sys.argv[i+2])] #retourne la taille indiquee par l'utilisateur (arguments suivants)
        elif arg == '-s':                   # si l'option "-s" est bien presente mais qu'il y une erreur sur la taille
            error('Arguments du choix de la taille invalide : 1280 x 720 par defaut') #previent l'utilisateur de l'erreur et utilise la taille par defaut
        i += 1                              # passe a l'argument suivant
    return [1280, 720]


def definePen():                            # permet de modifier les couleurs des LSystems obtenus
    i = 0                                   # compteur d'arguments
    colormode(255)                          # permet de passer en mode RGB
    output('colormode(255)', inTerminal)
    pencolor((1, 1, 1))                     # definit la couleur du trace de la tortue en noir
    fillcolor((255, 255, 255))              # definit la couleur du fond en blanc
    width(1)                                # definit l'epaisseur du tracé de la tortue a 1
    for arg in sys.argv:                    # parcourt les arguments
        # cas ou l'on veut changer la couleur du trace, verifie egalement la validite du code RGB entre par l'utilisateur
        if arg == '-pc' and verifExistOfVar(i, 'color') and sys.argv[i+1].isdigit() and sys.argv[i+2].isdigit() and sys.argv[i+3].isdigit() and 0 < int(sys.argv[i+1]) < 256 and 0 < int(sys.argv[i+2]) < 256 and 0 < int(sys.argv[i+3]) < 256:
            pencolor(int(sys.argv[i+1]), int(sys.argv[i+2]), int(sys.argv[i+3])) # applique le code RGB donne par l'utilisateur (arguments suivants)
        elif arg == '-pc':                  # si l'option "-pc" est bien entree mais que le code RGB n'est pas valide
            error('Arguments de changement de la couleur du trace non valides : noir par defaut') # previent l'utilisateur de l'erreur et utilise le noir pour le trace
        
        # cas ou l'on veut changer la couleur du fond, verifie egalement la validite du code RGB entre par l'utilisateur
        if arg == '-fc' and verifExistOfVar(i, 'color') and sys.argv[i+1].isdigit() and sys.argv[i+2].isdigit() and sys.argv[i+3].isdigit() and 0 < int(sys.argv[i+1]) < 256 and 0 < int(sys.argv[i+2]) < 256 and 0 < int(sys.argv[i+3]) < 256:
            fillcolor(int(sys.argv[i+1]), int(sys.argv[i+2]), int(sys.argv[i+3])) # applique le code RGB donne par l'utilisateur (arguments suivants)
        elif arg == '-fc':                  # si l'option "-fc" est bien entree mais que le code RGB n'est pas valide
            error('Arguments de changement de la couleur du remplissage non valides : blanc par defaut') # previent l'utilisateur de l'erreur et utilise le blanc pour le fond
        
        # cas ou l'on veut changer la taille du trace, verifie egalement que la taille entree par l'utilisateur est bien un nombre
        if arg == '-sp' and verifExistOfVar(i) and sys.argv[i+1].isdigit():
            width(int(sys.argv[i+1]))       # applique la taille donnee par l'utilisateur (argument suivant)
        elif arg == '-sp':                  # si l'option "-sp" est bien entree mais que la taille n'est pas valide
            error('Arguments de changement de la taille du trace non valides : 1 par defaut') #previent l'utilisateur de l'erreur et utilise la taille 1 pour le trace
        i += 1                              # passe a l'argument suivant

    # ajoute la commande de changement de couleur de trace au fichier de sortie
    output('pencolor('+str(pencolor()).split('.0')[0] + str(pencolor()).split('.0')[1] + str(pencolor()).split('.0')[2]+'))', inTerminal)
    # ajoute la commande de changement de couleur du fond au fichier de sortie
    output('fillcolor('+str(fillcolor()).split('.0')[0] + str(fillcolor()).split('.0')[1] + str(fillcolor()).split('.0')[2]+'))', inTerminal)
    output('width('+str(pensize())+')', inTerminal) # ajoute la commande de changement d'epaisseur du trace au fichier de sortie


def recupData(data):                        # permet de recuperer la donnee (axiome, niveau, angle ou taille)
    lSysFile = open(lSysPath, "r")          # ouvre le fichier de definition du LSystem en mode lecture
    for line in lSysFile:                   # parcourt le fichier
        line2 = line.strip(' \n\t')         # enleve les espaces et les retour a la ligne
        # verifie que le debut de la ligne corresponde bien a la donnee voulu (axiome, niveau, angle ou taille) et que celle ci est bien definie
        if line2.split('=')[0].strip(' \n\t') == data and instructionsVerif(data, line2): 
            lSysFile.close()                # ferme le fichier
            return line2.split(' = ')[1].strip('"') # retourne la donnee (axiome, niveau, angle ou taille) sans les guillemets
    error(data + " non specifiee ou ne respectant pas les normes d'ecriture", True) # si la donnee n'est pas retournee, envoie un message precisant l'erreur 


def recupRules():                           # permet de recuperer les regles du LSystem
    lSysFile = open(lSysPath, "r")          # ouvre le fichier de definition du LSystem en mode lecture
    rules = []                              # tableau pour les regles initialement vide
    for line in lSysFile:                   # parcourt le fichier
        line2 = line.strip(' \n\t')         # enleve les espaces, retour a la ligne et tabulations
        # si la ligne est non vide et son premier caractere est un guillemet ", ce qui permet de recuperer seulement les regles et pas l'axiome, dont le
        # premier caractere n'est pas un guillemet
        if line2 != '' and line2[0] == '"': 
            rules.append(line2.strip('"'))  # ajoute la regle recuperer dans la liste rules
    lSysFile.close()                        # ferme le fichier
    if rules == []:                         # si la liste est toujours vide
        error("Regles non specifiees ou ne respectant pas les normes d'ecriture", True) # renvoie un message d'erreur approprie
    return rules                            # retourne la liste contenant les regles


def moveWithPenDown():                      # la tortue avance et dessine sur son chemin
    global length
    pd()
    fd(length)
    output('pd(), fd('+str(length)+')', inTerminal) # ajoute la commande dans le fichier de sortie


def moveWithPenUp():                        # la tortue avance mais ne dessine pas sur son chemin
    global length
    pu()
    fd(length)
    output('pu(), fd('+str(length)+')', inTerminal) # ajoute la commande dans le fichier de sortie


def rightRota():                            # la tortue fait une rotation d'angle donne vers la droite
    global angle
    rt(angle)
    output('rt('+str(angle)+')', inTerminal) # ajoute la commande dans le fichier de sortie


def leftRota():                             # la tortue fait une rotation d'angle donne vers la gauche
    global angle
    lt(angle)
    output('lt('+str(angle)+')', inTerminal) # ajoute la commande dans le fichier de sortie


def Uturn():                                # la tortue fait demi-tour
    rt(180)
    output('rt(180)', inTerminal)           # ajoute la commande dans le fichier de sortie


def memoPos():                              # enregistre la position [x, y] et la direction (angle) actuelles de la tortue
    global queuePos
    queuePos.put([pos(), heading()])        # ajoute la position recuperee dans la liste queuePos
    return queuePos


def returnToPos():                          # permet de retourner aux dernieres position et direction memorisees
    global queuePos
    lastPos = queuePos.get()                # recupere la derniere position/direction memorisee (liste Last In First Out)
    pu()                                    # lève le stylo, permet de ne pas écrire lors du retour à la dernière postion
    setpos(lastPos[0])                      # replace la tortue a la derniere position [x, y] enregistree
    setheading(lastPos[1])                  # replace la tortue dans la derniere direction enregistree
    output('pu(), setpos('+str(lastPos[0])+'), setheading('+str(lastPos[1])+')', inTerminal) # ajoute les commandes dans le fichier de sortie


def drawLSys(finalAxiom):                   # execute l'ensemble des actions et donc trace le LSystem
    global actions
    for i in finalAxiom:                    # parcourt l'axiome final
        if i in actions:                    # verifie si les actions sont dans le dictionnaire
            actions[i]()                    # execute l'action liee au caractere de l'axiome


def axiomWithLVL():                         # applique les regles sur l'axiome en fonction du niveau (niveau 4 : les regles sont appliquees 4 fois) et retourne l'axiome final
    global axiom, level, rules              # axiome principal; niveau et regles donnes dans le fichier
    for i in range(level):                  # repete le nombre de fois indique par le niveau
        axiomtmp = ''                       # axiome temporaire intialement vide
        for car in axiom:                   # parcourt l'axiome principal
            verifChanges = axiomtmp         # copie l'axiome temporaire pour verifier ensuite s'il a bien ete modifie
            for rule in rules:              # parcourt les regles
                if rule[0] == car:          # si le caractere etudie a une regle associee
                    axiomtmp += rule.split('=')[1] # ajoute la regle associee a l'axiome temporaire
            if verifChanges == axiomtmp:    # si le caractere n'a pas de regle associee
                axiomtmp += car             # le caractere est ajouté simplement a l'axiome temporaire
        axiom = axiomtmp                    # l'axiome principal prend en compte les modifs realisees a chaque niveau
    return(axiom)


def defineVar():                            # recupere chaque donnee (axiome, regles, niveau, angle, taille)
    global axiom, rules, level, angle, length, queuePos, lSysPath, outFileName, actions
    axiom = recupData('axiom')              # recupere l'axiome
    rules = recupRules()                    # recupere les regles
    level = int(recupData('level'))         # recupere le niveau
    angle = float(recupData('angle'))       # recupere l'angle voulu popur la rotation de la tortue
    length = int(recupData('length'))       # recupere la longueur d'avancee de la tortue
    queuePos = LifoQueue()                  # liste qui conserve les positions/directions a memoriser
    actions = {                             # dictionnaire associant a chaque caractere possible de l'axiome et des regles l'action a realiser
        "a": moveWithPenDown,               # tortue avance et dessine
        "b": moveWithPenUp,                 # tortue avance mais ne dessine pas
        "+": rightRota,                     # tortue tourne vers la droite
        "-": leftRota,                      # tortue tourne vers la gauche
        "*": Uturn,                         # tortue fait demi tour
        "[": memoPos,                       # enregistre position/direction actuelles de la tortue
        "]": returnToPos                    # retourne aux dernieres postion/direction enregistrees
    }


def main():                                 # fonction principale
    global lSysPath, outFileName, outFile, inTerminal
    inTerminal = actionsInTerminal()        #demande a l'utilisateur s'il veut afficher chaque action dans le terminal
    defineFile()                            # verifie et initialise les options -i et -o
    pathVerif()                             # verifie le chemin du fichier
    outFile = open(outFileName+".py", 'w+') # cree le fichier de sortie s'il n'existe pas et l'ouvre en mode ecriture
    output('from turtle import *', inTerminal) # ajoute la commande au fichier de sortie
    size = defineSize()                     # recupere la taille de la fenetre voulue
    definePen()                             # recupere les options de couleur et d'epaisseur pour le trace du LSystem
    defineVar()                             # recupere chaque donnee (axiome, regles, niveau, angle, taille)
    setup(size[0], size[1])                 # ouvre la fenetre a la taille demandee par l'utilisateur
    output('setup('+str(size[0])+','+str(size[1])+')', inTerminal) # ajoute la commande au fichier de sortie
    speed(0)                                # applique la vitesse de dessin la plus rapide
    output('speed(0)', inTerminal)          # ajoute la commande au fichier de sortie
    listen()                                # "ecoute" les actions de l'utilisateur, sur la barre espace notamment
    output('listen()')                      # ajoute la commande au fichier de sortie
    onkey(lambda: tracer(False), "space")   # finit le trace si l'utilisateur appuie sur la touche "espace"
    output('onkey(lambda : tracer(False), "space")', inTerminal) # ajoute la commande au fichier de sortie
    begin_fill()                            # prend en compte le debut du remplissage au milieu du LSystem
    output('begin_fill()', inTerminal)      # ajoute la commande au fichier de sortie
    drawLSys(axiomWithLVL())                # dessine le Lsystem
    end_fill()                              # remplit au milieu du LSystem depuis la fonction begin_fill()
    output('end_fill()', inTerminal)        # ajoute la commande au fichier de sortie
    hideturtle()                            # cache la tortue une fois le dessin fini
    output('hideturtle()', inTerminal)      # ajoute la commande au fichier de sortie
    update()                                # met l'ecran a jour afin de bien affiche le dessin
    output('update()', inTerminal)          # ajoute la commande au fichier de sortie
    exitonclick()                           # permet de fermer le programme en cliquant n'importe ou sur la fenetre
    output('exitonclick()', inTerminal)     # ajoute la commande au fichier de sortie
    outFile.close()                         # ferme le fichier de sortie


main()                                      #appelle la fonction principale