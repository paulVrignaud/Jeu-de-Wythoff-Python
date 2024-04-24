##Jeu de Wythoff
##====================Importations==============================#
import random
import time

import numpy as np

##=======================Fonctions==============================#

def affichePlateau(plateau):
    for i in range(len(plateau)-1,-1,-1):
        print(str(i) + " | ",end="")
        for j in range(len(plateau)):
            print(plateau[i][j] + " | ",end="")
        print()
    print("     ",end="")
    for i in range(len(plateau)):
        print(str(i) + "   ",end="")
        
def creerPlateau(n):
    return [[' ' for i in range(n)] for i in range(n)]

def positionDepart(plateau):
    choix = random.randint(0, 1)
    
    ##On détermine si on commence par les x ou les y
    if choix == 0:
        ##On évite les positions interdites
        y = random.randint(0,len(plateau)-1)
        while y == 0:
            y = random.randint(0,len(plateau)-1)
        ##On trouve l'autre coordonné
        if y == (len(plateau)-1):
            x = random.randint(0,len(plateau)-1)
            while x == 0 or x == len(plateau)-1:
                x = random.randint(0,len(plateau)-1)
        else:
            x = len(plateau)-1
    else:
        ##On évite les positions interdites
        x = random.randint(0,len(plateau)-1)
        while x == 0:
            x = random.randint(0,len(plateau)-1)
        ##On trouve l'autre coordonné
        if x == len(plateau)-1:
            y = random.randint(0,len(plateau)-1)
            while y == 0 or y == len(plateau)-1:
                y = random.randint(0,len(plateau)-1)
        else:
            y = len(plateau)-1
            
    ##On place le pion aux coordoonées déterminés
    plateau[x][y] = 'o'
    
##On cherche la position (x,y) du pion sur le plateau
def positionPion(plateau):
    positionX = -1
    trouver = False
    i = 0
    
    while i < len(plateau) and not trouver:
        j = 0
        while j < len(plateau[i]) and not trouver:
            if plateau[i][j] == 'o':
                positionY = j
                positionX = i
                trouver = True
            j += 1
        i += 1
        
    return positionX,positionY

###Mouvement possibles###
def mouvementGauche(plateau, position, n):
    x = position[0]
    y = position[1]
    
    plateau[x][y] = ' '
    plateau[x][y-n] = 'o'
    
def mouvementBas(plateau,position,n):
    x = position[0]
    y = position[1]
    
    plateau[x][y] = ' '
    plateau[x-n][y] = 'o'
    
def mouvementDiag(plateau,position,n):
    x = position[0]
    y = position[1]
    
    plateau[x][y] = ' '
    plateau[x-n][y-n] = 'o'

####Nombre de déplacements maximum###
def maxGauche(plateau,position):
    compteur = 0
    i = position[1]
    
    while i > 0:
        compteur += 1
        i -= 1
    return compteur

def maxBas(plateau,position):
    compteur = 0
    i = position[0]
    
    while i > 0:
        compteur += 1
        i -= 1
    return compteur

def maxDiag(plateau,position):
    compteur = 0
    i = position[0]
    j = position[1]
    
    while i > 0 and j > 0:
        compteur += 1
        i -= 1
        j -= 1
    return compteur

#=====Recherche de la meilleure case=========#

def rechercheMeilleureCase(classement,position):
    x = position[0]
    y = position[1]
    
    #Pour vérifier si tout les classements sont égaux ou non
    egaux = True
    
    #On vérifie si le pion est à une extrémité
    if x == 0:
        noteMax = classement[x][y-1]
        positionMax = [x,y-1]
    elif y == 0:
        noteMax = classement[x-1][y]
        positionMax = [x-1,y]
    else:
        
        noteMax = classement[x-1][y]
        positionMax = [x-1,y] 
        
    #On cherche à gauche
    i = y-1
    while i >= 0:
        if classement[x][i] > noteMax:
            positionMax = [x,i]
            noteMax = classement[x][i] 
            egaux = False
        i -= 1
            
    #On cherche en bas
    i = x-1
    while i >= 0:
        if classement[i][y] > noteMax:
            positionMax = [i,y]
            noteMax = classement[i][y]
            egaux = False
        i -= 1
            
    #On cherche en diagonale
    i = x-1
    j = y-1
    while i >= 0 and j >= 0:
        if classement[i][j] > noteMax:
            positionMax = [i,j]
            noteMax = classement[i][j]
            egaux = False
        i -= 1
        j -= 1
        
    #On retourne les coordonnées de la meilleure case (tuple) et un booléen
    return positionMax, egaux

#============Intelligence Artificielle======================#

def ordinateur(plateau,position):
    ##On vérifie quel direction est disponible et on la choisie
    positionX = position[0]
    positionY = position[1]
    
    #On cherche la case la mieux noté
    meilleureCase = rechercheMeilleureCase(classement,position)
    
    egaux = meilleureCase[1]
    
    #Si toutes les cases ont le même classement alors on fait de l'aléatoire
    if egaux:
        
        #Verification si le pion est en extrémité
        if positionX == 0:
            choix = 1
            
        elif positionY == 0:
            choix = 2
            
        else:
            choix = random.randint(1,3)
        
        #On fait le mouvement puis on regarde où est le pion pour stocker la position dans stockage
        if choix == 1:
            maxCase = maxGauche(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementGauche(plateau,position,nCase)
                            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
            
        elif choix == 2:
            maxCase = maxBas(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementBas(plateau,position,nCase)
            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
                            
        else:
            maxCase = maxDiag(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementDiag(plateau,position,nCase)
                            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
            
        stockage[nouveauX][nouveauY] = 1
            
    #Sinon on va à la meilleure case
    else:
        xMax = meilleureCase[0][0]
        yMax = meilleureCase[0][1]
                            
        plateau[positionX][positionY] = ' '
        plateau[xMax][yMax] = 'o'
        
        #On garde en mémoire dans stockage le mouvement effectué et sa position avant
                            
        stockage[xMax][yMax] = 1

#============Ordinateur pour entrainer l'autre ordinateur==================#
        
def ordinateurEntrainement(plateau,position):
    ##On vérifie quel direction est disponible et on la choisie
    positionX = position[0]
    positionY = position[1]
    
    #On cherche la case la mieux noté
    meilleureCase = rechercheMeilleureCase(classement,position)
    
    egaux = meilleureCase[1]
    
    #Si toutes les cases ont le même classement alors on fait de l'aléatoire
    if egaux:
        
        #Verification si le pion est en extrémité
        if positionX == 0:
            choix = 1
            
        elif positionY == 0:
            choix = 2
            
        else:
            choix = random.randint(1,3)
        
        #On fait le mouvement puis on regarde où est le pion pour stocker la position dans stockage
        if choix == 1:
            maxCase = maxGauche(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementGauche(plateau,position,nCase)
                            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
            
        elif choix == 2:
            maxCase = maxBas(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementBas(plateau,position,nCase)
            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
                            
        else:
            maxCase = maxDiag(plateau,position)
            nCase = random.randint(1,maxCase)
            mouvementDiag(plateau,position,nCase)
                            
            nouvellePosition = positionPion(plateau)
            nouveauX = nouvellePosition[0]
            nouveauY = nouvellePosition[1]
            
        stockageEntrainement[nouveauX][nouveauY] = 1
            
    #Sinon on va à la meilleure case
    else:
        xMax = meilleureCase[0][0]
        yMax = meilleureCase[0][1]
                            
        plateau[positionX][positionY] = ' '
        plateau[xMax][yMax] = 'o'
        
        #On garde en mémoire dans stockage le mouvement effectué et sa position avant
                            
        stockageEntrainement[xMax][yMax] = 1

def joueurRandom(plateau,position):
    x = position[0]
    y = position[1]

    #On choisi aléatoirement la direction
    if x == 0:
        choix = 1
    elif y == 0:
        choix = 2
    else:
        choix = random.randint(1,3)
    
    #On détermine le nombre de case à parcourir
    
    if choix == 1:
        nbreCaseMax = maxGauche(plateau,position)
        nCase = random.randint(1,nbreCaseMax)
        mouvementGauche(plateau,position,nCase)
    elif choix == 2:
        nbreCaseMax = maxBas(plateau,position)
        nCase = random.randint(1,nbreCaseMax)
        mouvementBas(plateau,position,nCase)
    else:
        nbreCaseMax = maxDiag(plateau,position)
        nCase = random.randint(1,nbreCaseMax)
        mouvementDiag(plateau,position,nCase)

##=======Demande du mode jeu=======##
demande=True
while demande:
    reponseModeJeu = input("\nVoulez-vous que l'ia s'entraîne contre le hasard avant de jouer ?[O/N]: ")
    if reponseModeJeu in ("o","O"):
        reponse = True
        demande=False
    elif reponseModeJeu in ("n","N"):
        reponse=False
        demande=False
    else:
        print("\nChoix invalide. Recommencez !") 

##=========Initialisation du jeu==========##
choix = True
while choix:
    taillePlateau = int (input("Choisissez votre taille de plateau : "))
    if taillePlateau < 3:
        print("\nChoix invalide. Recommencez !") 
    else:
        choix = False

##============Initialisation du système de stockage pour l'ordinateur==============#

##On crée une copie du plateau pour y rajouter les mouvements que le robot à effectué
##et un tableau qui contient un classement qui commence à 5 pour y faire augmenter/réduire la note par la suite
##si la note d'une case arrive à 0 on la remet à 5
stockage = []
stockageEntrainement = []
classement = []
classementEntrainement = []

for _ in range(taillePlateau):
    stockage.append([0 for i in range(taillePlateau)])
    stockageEntrainement.append([0 for i in range(taillePlateau)])
    classement.append([5 for i in range(taillePlateau)])
    classementEntrainement.append([5 for i in range(taillePlateau)])

if reponse:
    #============Entrainement de l'IA contre l'aléatoire====================#
    nbrePartieEntrainement = int (input("Combien de fois voulez-vous que l'ia s'entraîne contre le hasard ? :"))
    nbPartieOrdiGagnant = 0
    for nbrePartie in range(nbrePartieEntrainement):
        joueur = "BOT"
        plateau = creerPlateau(taillePlateau)
        positionDepart(plateau)

        ##Condition de victoire
        while plateau[0][0] != 'o':
            ##On cherche la position du pion
            position = positionPion(plateau)
            
            if joueur == "RANDOM":
                ##L'aléatoire joue
                joueurRandom(plateau,position)
                    
            else:
                ##On fait jouer l'ordinateur
                ordinateur(plateau,position)
                
            ##On effectue le changement de joueur
            if joueur == "BOT":
                joueur = "RANDOM"
            else:
                joueur = "BOT"
        
        ##Fin de partie détermination du gagnant
        
        if joueur == "BOT":
            winner = "RANDOM"
        else:
            winner = "BOT"
            nbPartieOrdiGagnant += 1
        
        ###============ Apprentissage : récompense ou punition de l'ordinateur===========##
        if winner == "BOT":
            #On récompense le robot
            for x in range(len(stockage)):
                for y in range(len(stockage)):
                    #On cherche les positions où le robot à joué un coup
                    mouvementEffectue = stockage[x][y]
                    if mouvementEffectue == 1:
                        #On rajoute un point à la case
                        classement[x][y] += 1
                        
        else:
            #On punie le robot
            for x in range(len(stockage)):
                for y in range(len(stockage)):
                    #On cherche les positions où le robot à joué un coup
                    mouvementEffectue = stockage[x][y]
                    if mouvementEffectue == 1:
                        #On enlève un point à la case
                        classement[x][y] -= 1

                        if classement[x][y] <= 0:
                            classement[x][y] = 0
                        
        ##On remet à 0 le stockage##
        stockage = []
        for _ in range(taillePlateau):
            stockage.append([0 for i in range(taillePlateau)])
                        
        #======= fin de la récompense ou de la punition ==========##
            
    ##========Affichage  de l'état du classement==========##
    print()
    print("Etats du classement après ",nbrePartie + 1, " partie jouées contre le hasard: ")
    print(classement)
    print("L'intelligence artificielle à gagné ", nbPartieOrdiGagnant, " fois.")
    print("Le taux de victoire de l'ordinateur est de ", round((nbPartieOrdiGagnant/nbrePartie) * 100,3),"%")


    #===========Debut de partie contre le joueur après n partie contre l'aléatoire==============#
    print("L'intelligence artificielle est enfin prête pour jouer contre vous")

uneAutrePartie=True
nbPartie = 0
while uneAutrePartie:
    nbPartie += 1
    print()
    joueur = "BOT"
    plateau = creerPlateau(taillePlateau)
    positionDepart(plateau)
    
    ##Condition de victoire
    while plateau[0][0] != 'o':
        affichePlateau(plateau)
        print()
        ##On cherche la position du pion
        position = positionPion(plateau)
        
        if joueur == "USER":
            ##Le joueur joue
            print("c'est à l'humain de jouer")
            
            ##On vérifie si il est possible d'aller dans une direction ou non
            if maxGauche(plateau,position) == 0:
                mouvement = 2
                print("Tu ne peux aller qu'en bas")
                
            elif maxBas(plateau,position) == 0:
                mouvement = 1
                print("Tu ne peux aller qu'à gauche")
            
            ##On demande le mouvement que l'on veut
            else:
                mouvement = input("Choisi ton mouvement (gauche = 1 /bas = 2 /diagonale = 3):")
                mouvement = int(mouvement)
            
            
            while mouvement < 0 and mouvement > 3:
                mouvement = input("Réessaie avec la bonne écriture, (gauche = 1 /bas = 2 /diagonale = 3):")
                mouvement = int(mouvement)
                
            nbreCase = input("Combien de cases voulez-vous parcourir ? > ")
            nbreCase = int(nbreCase)
            
            ##On calcule le déplacement de n case maximum en fonction de la direction
            if mouvement == 1:
                deplacementMax = maxGauche(plateau,position)
            elif mouvement == 2:
                deplacementMax = maxBas(plateau,position)
            elif mouvement == 3:
                deplacementMax = maxDiag(plateau,position)
                
            while nbreCase < 1 or nbreCase > deplacementMax:
                print("C'est une valeur qui n'est pas bonne, retente.")
                nbreCase = input("Combien de cases voulez-vous parcourir ? > ")
                nbreCase = int(nbreCase)
            
            ##On regarde l'action demandé et on effectue le mouvement
            if mouvement == 1:
                mouvementGauche(plateau,position,nbreCase)
            elif mouvement == 2:
                mouvementBas(plateau,position,nbreCase)
            else:
                mouvementDiag(plateau,position,nbreCase)
                
        else:
            ##On fait jouer l'ordinateur
            print("c'est à l'ordi de jouer")
            ordinateur(plateau,position)
            
        ##On effectue le changement de joueur
        if joueur == "BOT":
            joueur = "USER"
        else:
            joueur = "BOT"
            
    affichePlateau(plateau)
    print()
    
    if joueur == "BOT":
        winner = "USER"
    else:
        winner = "BOT"
    
    ##### annonce des résultats #####
    if winner=="USER":
        print("\n----------------------------------------------------------------------------")
        print("Bravo ! Vous avez gagné ! Nous allons punir l'ordinateur.")
        print("----------------------------------------------------------------------------\n")
    else:
        print("\n----------------------------------------------------------------------------")
        print("L'ordinateur a gagné, nous allons le récompenser.")
        print("----------------------------------------------------------------------------\n")
    
    ###============ Apprentissage : récompense ou punition de l'ordinateur===========##
    if winner == "BOT":
        #On récompense le robot
        for x in range(len(stockage)):
            for y in range(len(stockage)):
                #On cherche les positions où le robot à joué un coup
                mouvementEffectue = stockage[x][y]
                if mouvementEffectue == 1:
                    #On rajoute un point à la case
                    classement[x][y] += 1
                    
    else:
        #On punie le robot
        for x in range(len(stockage)):
            for y in range(len(stockage)):
                #On cherche les positions où le robot à joué un coup
                mouvementEffectue = stockage[x][y]
                if mouvementEffectue == 1:
                    #On enlève un point à la case
                    classement[x][y] -= 1

                    if classement[x][y] <= 0:
                        classement[x][y] = 0
                    
    ##On remet à 0 le stockage##
    stockage = []
    for _ in range(taillePlateau):
        stockage.append([0 for i in range(taillePlateau)])
        
                            
    #======= fin de la récompense ou de la punition ==========##
    ##========Affichage  de l'état du classement==========##
    print("Etats du classement après ",nbPartie, " partie : ")
    print(classement)
    
############ On continue ? ################    
    test=True
    while test:
        another_go = input("\nVoulez-vous rejouer ?[O/N]: ")
        if another_go in ("o","O"):
            uneAutrePartie=True
            test=False
        elif another_go in ("n","N"):
            uneAutrePartie=False
            test=False
        else:
            print("\nChoix invalide. Recommencez !")    
###########################################