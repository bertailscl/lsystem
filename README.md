# L-System
## By Clément Bertails

Contient un programme permettant de simuler un l-système.

## Dépendences

 - Python3
 - module turtle
 - module queue

## Utilisation
Lancer le script "projet.py".
Répertoire de l-Systeme : ./lSys
Le fichier contenant les commandes turtles (out.py) sert à réexécuter le programme sans calculer l'axiome.

## Paramètres 

Nous pouvons utiliser des paramètres pour simplifier l'exécution.
 - Déterminer le l-système à exécuter : -i [FILEPATH]
 - Déterminer le fichier contenant les commandes turtles : -o [FILENAME] (le .py sera ajouter en automatique)
 - Modifier la taille de la fenêtre turtle : -s [LENGHT] [HEIGHT]
 - Modifier la couleur du pinceau : -pc [RED] [GREEN] [BLUE] (valeur de 1 à 255)
 - Modifier la couleur du font : -fc [RED] [GREEN] [BLUE] (valeur de 1 à 255)
 - Modifier la taille du pinceau : -sp [SIZE]

Exemple :
```bash 
python3 projet.py -i ./lSys/lSys-levyCurve.txt -o out -s 1920 1080 -pc 255 1 
```
