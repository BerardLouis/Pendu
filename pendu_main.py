import random

#informatique
#animaux
#capitales
#fruits et légumes
#sports


informatique = {
    "ordinateur" : "Machine automatique de traitement de l'information, obéissant à des programmes formés par des suites d'opérations arithmétiques et logiques.", 
    "clavier" : "Ensemble de touches dont chacune correspond à la commande de caractères, de fonctions ou d'instructions particulières et dont l'enfoncement provoque l'impression d'un caractère, une mise en mémoire ou l'émission d'un signal.",
    "souris" : "Petit dispositif dont le déplacement manuel sur une surface permet d'amener, sur l'écran de visualisation d'un ordinateur, un point sur la zone ainsi désignée.",
    "processeur" : "Organe destiné, dans un ordinateur, à interpréter et exécuter des instructions.",
    }
animaux = {
    "chat" : "Mammifère carnivore (félidé), sauvage ou domestique, au museau court et arrondi.",
    "chien" : "Mammifère (canidé) carnivore aux multiples races, caractérisé par sa facilité à être domestiqué, par une course rapide, un excellent odorat et par son cri spécifique, l'aboiement.",
    "girafe" : "Grand mammifère ruminant des savanes africaines du sud du Sahara, remarquable par la longueur de son cou et ses petites cornes recouvertes de velours.",
    "alligator" : "Crocodilien du Mississippi ou du Yangzi Jiang, à tête large et aplatie, très peu actif, élevé en Amérique pour son cuir.",
    }

liste_themes = {1 : informatique, 2 : animaux}
nom_theme = {1: "Informatique", 2 : "Animaux"}
theme = random.randint(1,2)

dictionnaire_choisi = liste_themes[theme] #ici on choisi quel thème est utilisé
index_mot_random = random.randint(0, len(dictionnaire_choisi)-1) #ici on prend un chiffre au hasard, pour plus tard choisir un mot au hasard dans le dico utilisé

mot_choisi = list(dictionnaire_choisi)[index_mot_random]
    
definition_mot = dictionnaire_choisi.get(mot_choisi)

    #print("Thème choisi : " + noms_themes[theme])
    #print("Mot: " + mot_choisi)
    #print("Définition : " + definition_mot)

nombre_vie = 5

mot_caché = "_"
nblettres = len(mot_choisi)
mot_caché = mot_caché*nblettres

liste_lettres = list(mot_choisi)
liste_lettres_cache = list(mot_caché)
print(nom_theme.get(theme))
print(liste_lettres)
print(liste_lettres_cache)

def tentative(nombre_vie):
    if "_" in liste_lettres_cache :
        if nombre_vie > 0 :
            print("Mot caché:  " , *liste_lettres_cache, sep='' )
            print("\nIl te reste " + str(nombre_vie) + " vies !")

            user_input = input("\nChoisis une lettre: ")
            user_input = user_input.lower()

            if user_input.isalpha() :
                if len(user_input) == 1 :

                    if user_input in (liste_lettres) :

                        for i in range(0,nblettres):
                            if user_input == liste_lettres[i]:
                                liste_lettres_cache[i] = user_input
                        
                        print("Oui, le mot contient:" + user_input)
                        tentative(nombre_vie)
                    
                    else:
                        print("Non, le mot ne contient pas: "+ user_input)
                        nombre_vie = nombre_vie - 1
                        tentative(nombre_vie)

                else :
                    print("Il rentrer seulement une lettre")
                    tentative(nombre_vie)
            else :
                print("Il faut renter une lettre !")
                tentative(nombre_vie)    
        else:
            print("Dommage, tu auras plus de chance la prochaine fois !")
            breakpoint       
    else : 
        print("Bravo ! C'est gagné, le mot était bien: " + mot_choisi)
        breakpoint

tentative(nombre_vie)