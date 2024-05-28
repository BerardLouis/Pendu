import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
from tkinter import *
import pygame
import random
from tkinter import messagebox
import xml.etree.ElementTree as et

#cette classe contient le constructeur de l'objet dataWord. Cet objet est utilisé pour stocker les données obtenues à partir du fichier xml contenant le lexique + informations
class dataWord:
    def __init__(self, Word: str, Clue: str, Difficulty: str):
        self.word = Word
        self.Clue = Clue
        self.difficulty = Difficulty

#cette classe contient les fontions et variables de la partie base de données de l'application (du parsing au stockage des données dans la liste d'objet dataword) 
class data:
    informatique = []
    animaux = []
    sport = []
    pays = []
    dict_themes = {0: informatique, 1: animaux, 2: sport, 3: pays}
    noms_des_theme = ["informatique", "animaux", "sport", "pays"]
    nom_du_theme = ""


#cette fonction parse le xml et reconstite l'arbre de celui-ci
    def xml_parsing(self, file_name: str):
        folder_directory = file_name 
        arbre = et.parse(folder_directory)
        root = arbre.getroot()
        return root
#met à jour un dictionnaire ayant pour key le nom d'un thème et en value la liste d'objet dataword associée au thème. 
#La fonction prend pour paramètre la racine du fichier XML contenant les données
    def create_dict_vocab(self, file_name: str):
        vocab = data.xml_parsing(self, file_name)
        for elem in vocab.iter():
            if elem.tag == "animaux":
                data.create_list_dataWord(self, data.animaux, elem)
            elif elem.tag == "informatique":
                data.create_list_dataWord(self, data.informatique, elem)
            elif elem.tag == "sport":
                data.create_list_dataWord(self, data.sport, elem)
            elif elem.tag == "pays":
                data.create_list_dataWord(self, data.pays, elem)

#mise à jour d'une liste d'objets dataword. Ajoute un objet dataWord à chaque fois que la fonction est appelée.
#Cette fonction prend en paramètres la liste correspondant au thème de l'objet à ajouter 
#et les noeuds enfants du XML où se trouvent les données permettant de construire un objet dataWord
    def create_list_dataWord(self, one_list_theme: list, child_nodes):
        for elem in child_nodes.iter():
            if elem.tag == "mot":
                lexeme = ""
                definition = ""
                difficulty = ""
                for info_word in elem.iter():
                    if info_word.tag == "lex":
                        lexeme = info_word.text
                    if info_word.tag == "def":
                        definition = info_word.text
                    if info_word.tag == "diff":
                        difficulty = str(info_word.text)
                one_list_theme.append(dataWord(lexeme, definition, difficulty))

#class contenant le constructeur de l'objet hidden_word. 
#Cette objet hiden_word contient toutes les variables nécessaires au bon déroulement du jeu.
class hiden_word:
    def __init__(self, hidden_word: str, clue_hidden_word: str, Difficulty: str):
        self.hidden_word = hidden_word
        self.clue_hidden_word = clue_hidden_word
        self.list_found_letters = ["_"] * len(hidden_word)
        self.list_found_letters_by_IA = ["_"] * len(hidden_word)
        self.list_letters = list(hidden_word)
        self.letter_already_proposed = []
        self.letters_proposed_by_IA = []
        self.difficulty = Difficulty

#cette classe contient toutes fonctions qui touchent à la gestion d'une partie de pendu.
class logic_pendu:

#Cette fonction met à jour les variables de l'objet hiden_word qui est le mot que le joueur doit deviner
#En fonction de la valeur True False de la variable "letter_is_in_hidden_word", appelle les fonctions permettant de mettre fin à la partie si victoire ou défaite.
#prend en paramètre la lettre proposée par l'utilisateur et l'objet hidden_word à mettre à jour
    def update_hidden_word(self, letter: str, word: hiden_word):
        print(word.list_letters)
        letter_is_in_hidden_word = False
        for index_letter_hidden_word in range(len(word.list_letters)):
            if letter == word.list_letters[index_letter_hidden_word]:
                word.list_found_letters[index_letter_hidden_word] = letter
                letter_is_in_hidden_word = True
                print(word.list_found_letters)
        if letter_is_in_hidden_word == False:
            Misc.player_loose_one_try(self)
        else:
            Misc.check_if_player_win(self, word)

#vérifie si la lettre de l'utilisateur contient un accent (parmi les lettres à accent kes plus courantes du français). 
#Si c'est le cas, change la valeur de la lettre avec accent en lettre sans accent 
    def replace_char_accent(self, letter):
        char_to_replace = ["é", "è", "à", "ù", "ï", "î", "â"]
        new_char = ["e", "e", "a", "u", "i", "i", "a"]
        letter_noAccent = letter
        for e in range(len(char_to_replace)):
            if letter == char_to_replace[e]:
                letter_noAccent = letter.replace(char_to_replace[e], new_char[e])
        return letter_noAccent

#vérifie que la taille de la chaîne de caractère proposée par l'utilisateur est égale à 1
#si la condition est respectée appelle la fonction qui remplace les carractères avec accent
#Une fois les caractères à accent sont remplacés vérifie si la lettre a déjà été proposée. 
#Si la condition est True, rien ne se passe et l'utilisateur doit proposer une nouvelle lettre, sinon appelle la fonction qui met à jour l'état du jeu
#Parameters: lettre proposée par l'utilisateur et objet hiden_word
    def check_letter_isValid(self, letter: str, word: hiden_word):

        if letter.isalpha() and len(letter) == 1:
            letter_noAccent = logic_pendu.replace_char_accent(self, letter)
            print("Submitted char is letter")
            if letter_noAccent in word.letter_already_proposed:
                print("Letter already proposed")
            else:
                word.letter_already_proposed.append(letter_noAccent)
                logic_pendu.update_hidden_word(self, letter_noAccent, word)
        else:
            print("Not a letter")

    def select_random_hidden_word(self, list_theme: list) -> dataWord:
        rand_int = random.randint(0, len(list_theme) - 1)
        selected_word = list_theme[rand_int]
        return selected_word

#cette classe contient les fonctions et la logique relative au comportement de l'IA en jeu.
class logic_IA:
#ces deux variables booleennes servent à fixer un bug (double pop-up s'affichant parfois à la fin d'une partie joueur contre IA).
#il y'avait de meilleures façons de fix le bug mais vue que la partie IA reste un Proof of concept et que le code ne sera pas maintenu on s'est contenté du fix le plus simple.
    player_won = False
    player_lost = False
#liste de lettre de l'alphabet ordonnée par ordre décroissant de fréquence d'apparation dans les mots français
    letters = ["e", "a", "i", "s", "n", "r", "t", "o", "l", "u", "d", "c", "m", "p", "g", "b", "v", "h", "f", "q", "y",
               "x", "j", "k", "w", "z"]

    IA_difficulty = 0

    def setIAdifficulty(x):
        logic_IA.IA_difficulty = x

    def IA_behavior(self, word: hiden_word):

        a = 0
        b = 0

        for i in range(0, len(actual_hidden_word.list_found_letters_by_IA)):
            if actual_hidden_word.list_found_letters_by_IA[i] == "_":
                a = a + 1
            else:
                b = b + 1
        c = a + b

        d = b / c

        e = d * 100

        if logic_IA.IA_difficulty < int(actual_hidden_word.difficulty):

            if e < 60:
                logic_IA.IA_submit_unknown(self, actual_hidden_word)
            else:
                logic_IA.IA_submit_known(self, actual_hidden_word)

        if logic_IA.IA_difficulty >= int(actual_hidden_word.difficulty):

            if e < 30:
                logic_IA.IA_submit_unknown(self, actual_hidden_word)
            else:
                logic_IA.IA_submit_known(self, actual_hidden_word)

    def IA_submit_unknown(self, word: hiden_word):

        x = 0

        while logic_IA.letters[x] in actual_hidden_word.letters_proposed_by_IA and x < len(logic_IA.letters):
            x = x + 1

        actual_hidden_word.letters_proposed_by_IA.append(logic_IA.letters[x])

        logic_IA.IA_update_hidden_word(self, logic_IA.letters[x], word)

    def IA_submit_known(self, word: hiden_word):

        x = 0

        while logic_IA.letters[x] not in actual_hidden_word.list_letters or logic_IA.letters[
            x] in actual_hidden_word.letters_proposed_by_IA and x < len(logic_IA.letters):
            x = x + 1

        actual_hidden_word.letters_proposed_by_IA.append(logic_IA.letters[x])

        logic_IA.IA_update_hidden_word(self, logic_IA.letters[x], word)

    def IA_update_hidden_word(self, letter: str, word: hiden_word):
        letter_is_in_hidden_word = False
        for index_letter_hidden_word in range(len(word.list_letters)):
            if letter == word.list_letters[index_letter_hidden_word]:
                word.list_found_letters_by_IA[index_letter_hidden_word] = letter
                letter_is_in_hidden_word = True
                print(word.list_found_letters_by_IA)
        if letter_is_in_hidden_word == False:
            PageIAGame.IA_loose_one_try(self)
        else:
            PageIAGame.check_if_IA_win(self, word)

#contient des fonctions effectuant des taches variées
class Misc:
#lance le fond musical quand le main est lancé
    def play_soundTrack():
        pygame.mixer.music.load("Dee Yan-Key - silent night  (stille nacht).mp3")
        pygame.mixer.music.play(loops=100)
#mise à jour de l'interface graphique et du nombre de vies restantes lorsque le joueur fait une mauvaise proposition. Cad:
#change l'image de la fusée (correspondant au nb de vies) et s'il a perdu renvoie l'utilisateur au menu principal, un pop-up informe l'utiliateur qu'il a perdu

    def player_loose_one_try(self):
        global lives_left
        global IA_lives_left
        lives_left -= 1
        if lives_left == -1:
            messagebox.showinfo(message="Tu as perdu! Le mot caché était: " + actual_hidden_word.hidden_word,
                                command=self.controller.show_frame("StartPage"))
            logic_IA.player_lost = True
            lives_left = 5
            IA_lives_left = 5
            self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
            self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")
        else:
            self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
            self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")
#verifie si l'utilisateur a gagné et met à jour l'interface graphiqe en conséquence c-a-d: 
#change l'image de la fusée (correspondant au nb de vies), renvoie l'utilisateur au menu principal, et un pop-up informe l'utiliateur qu'il a gagné
    def check_if_player_win(self, word: hiden_word):
        global lives_left
        global IA_lives_left
        if "_" not in word.list_found_letters:
            messagebox.showinfo(message="Tu as gagné! Le mot caché était: " + word.hidden_word,
                                command=self.controller.show_frame("StartPage"))
            lives_left = 5
            IA_lives_left = 5
            self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
            self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")
    
    def show_definition():
        messagebox.showinfo(message="Voici la définition du mot:\n" + actual_hidden_word.clue_hidden_word)

#Cette classe contient l'initialisationd de la partie graphique 
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global globalFrames

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        tk.Tk.iconbitmap(self, default="Screenshot (846).ico")
        tk.Tk.title(self, "Le jeu du pendu")
        tk.Tk.geometry(self, "1080x720")
        tk.Tk.minsize(self, 1080, 720)
        tk.Tk.maxsize(self, 1080, 720)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageThemeChoice, PageSoloGame, PageIAGame, PageIAdifficulty):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            globalFrames.append(frame)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name: str):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    mode = 0

    def choix_mode(x):
        StartPage.mode = x

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        canvas = Canvas(self, width=width, height=height, bg="#223F44")
        canvas.create_image(0, 0, image=self.image, anchor="nw")

        canvas.create_text(540, 160, text="Salut aventurier du cosmos lexical!", font=("Courrier", 40), fill="white")
        canvas.create_text(540, 210, text="Pour jouer au pendu, choisit un mode de jeu:", font=("Courrier", 25),
                           fill="white")

        button_soloPlayer = Button(self, text=" Mode solo  ", font=("Courrier", 20), bg="#223F44", fg="white",
                                   command=lambda: [controller.show_frame("PageThemeChoice"), StartPage.choix_mode(1)],
                                   cursor="star")
        button_soloPlayer.pack(pady=10, fill=X)

        button_AI = Button(self, text="       AI        ", font=("Courrier", 20), bg="#223F44", fg="white",
                           command=lambda: [controller.show_frame("PageIAdifficulty"), StartPage.choix_mode(2)],
                           cursor="star")
        button_AI.pack(pady=5, fill=X)

        canvas.create_window(475, 350, anchor="nw", window=button_soloPlayer)
        canvas.create_window(475, 420, anchor="nw", window=button_AI)

        canvas.pack(fill="both", expand="True")

class PageThemeChoice(tk.Frame):
    def onInformatiqueClicked(self):
        global actual_hidden_word
        logic_IA.player_won = False
        logic_IA.player_lost = False

        rand_choice_word = logic_pendu.select_random_hidden_word(self, data.informatique)
        actual_hidden_word = hiden_word(rand_choice_word.word, rand_choice_word.Clue, rand_choice_word.difficulty)
        if StartPage.mode == 1:
            globalFrames[2].setTitle("Informatique")
            globalFrames[2].update_letters_in_canvas()
            self.controller.show_frame("PageSoloGame")

        if StartPage.mode == 2:
            globalFrames[3].setTitle("Informatique")
            globalFrames[3].update_letters_in_canvas()
            globalFrames[3].update_IA_letters_in_canvas()
            self.controller.show_frame("PageIAGame")

    def onAnimalsClicked(self):
        global actual_hidden_word
        logic_IA.player_won = False
        logic_IA.player_lost = False

        rand_choice_word = logic_pendu.select_random_hidden_word(self, data.animaux)
        actual_hidden_word = hiden_word(rand_choice_word.word, rand_choice_word.Clue, rand_choice_word.difficulty)
        if StartPage.mode == 1:
            globalFrames[2].setTitle("Animaux")
            globalFrames[2].update_letters_in_canvas()
            self.controller.show_frame("PageSoloGame")

        if StartPage.mode == 2:
            globalFrames[3].setTitle("Animaux")
            globalFrames[3].update_letters_in_canvas()
            globalFrames[3].update_IA_letters_in_canvas()
            self.controller.show_frame("PageIAGame")

    def onSportClicked(self):
        global actual_hidden_word
        logic_IA.player_won = False
        logic_IA.player_lost = False


        rand_choice_word = logic_pendu.select_random_hidden_word(self, data.sport)
        actual_hidden_word = hiden_word(rand_choice_word.word, rand_choice_word.Clue, rand_choice_word.difficulty)
        if StartPage.mode == 1:
            globalFrames[2].setTitle("Sports")
            globalFrames[2].update_letters_in_canvas()
            self.controller.show_frame("PageSoloGame")

        if StartPage.mode == 2:
            globalFrames[3].setTitle("Sports")
            globalFrames[3].update_letters_in_canvas()
            globalFrames[3].update_IA_letters_in_canvas()
            self.controller.show_frame("PageIAGame")

    def onPaysClicked(self):
        global actual_hidden_word
        logic_IA.player_won = False
        logic_IA.player_lost = False

        rand_choice_word = logic_pendu.select_random_hidden_word(self, data.pays)
        actual_hidden_word = hiden_word(rand_choice_word.word, rand_choice_word.Clue, rand_choice_word.difficulty)
        if StartPage.mode == 1:
            globalFrames[2].setTitle("Pays")
            globalFrames[2].update_letters_in_canvas()
            self.controller.show_frame("PageSoloGame")

        if StartPage.mode == 2:
            globalFrames[3].setTitle("Pays")
            globalFrames[3].update_letters_in_canvas()
            globalFrames[3].update_IA_letters_in_canvas()
            self.controller.show_frame("PageIAGame")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        canvas = Canvas(self, width=width, height=height, bg="#223F44")
        canvas.create_image(0, 0, image=self.image, anchor="nw")
        canvas.create_text(540, 110, text="Choisit une dimension interstellaire:", font=("Courrier", 25), fill="white")

        button_subject_informatique = Button(self, text="  Informatique   ", font=("Courrier", 20), bg="#223F44",
                                             fg="white", command=self.onInformatiqueClicked, cursor="star")
        button_subject_informatique.pack(pady=10, fill=X)

        button_subject_animaux = Button(self, text="      Animaux     ", font=("Courrier", 20), bg="#223F44",
                                        fg="white", command=self.onAnimalsClicked, cursor="star")
        button_subject_animaux.pack(pady=5, fill=X)

        button_subject_sport = Button(self, text="        Sport        ", font=("Courrier", 20), bg="#223F44",
                                      fg="white", command=self.onSportClicked, cursor="star")
        button_subject_sport.pack(pady=5, fill=X)

        button_subject_pays = Button(self, text="        Pays        ", font=("Courrier", 20), bg="#223F44", fg="white",
                                     command=self.onPaysClicked, cursor="star")
        button_subject_pays.pack(pady=5, fill=X)

        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white",
                                   command=lambda: controller.show_frame("StartPage"), cursor="star")
        button_backToMenu.pack(pady=5, fill=X)

        canvas.create_window(475, 250, anchor="nw", window=button_subject_informatique)
        canvas.create_window(475, 320, anchor="nw", window=button_subject_animaux)
        canvas.create_window(475, 390, anchor="nw", window=button_subject_sport)
        canvas.create_window(475, 460, anchor="nw", window=button_subject_pays)
        canvas.create_window(475, 540, anchor="nw", window=button_backToMenu)

        canvas.pack(fill="both", expand="True")

class PageSoloGame(tk.Frame):

    def on_submit_letter_clicked(self):
        submited_letter = self.input_letter.get()
        self.input_letter.delete(0, "end")
        letter_submitted_player = submited_letter
        logic_pendu.check_letter_isValid(self, letter_submitted_player, actual_hidden_word)
        self.update_letters_in_canvas()

    def show_hidden_word(self):
        global lives_left
        messagebox.showinfo(message="Tu abandonne? Le mot caché était: " + actual_hidden_word.hidden_word)
        lives_left = 5
        self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
        self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")

    def player_giveUp(self):
        self.controller.show_frame("StartPage")
        PageSoloGame.show_hidden_word(self)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        self.canvas = Canvas(self, width=width, height=height, bg="#223F44")
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.image_fusee = PhotoImage(file="fusee_5.png")
        self.canvas_fusee = Canvas(self, width=284, height=236, bg="#223F44")
        self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")
        self.canvas_fusee.pack(fill="both", expand="True")

        self.letterLabelIndex = self.canvas.create_text(540, 50, text="A toi de jouer!!" + data.nom_du_theme,
                                                        font=("Courrier", 25), fill="white")

        self.updated_hidden_word = self.canvas.create_text(200, 350, text=" ".join(actual_hidden_word.list_letters),
                                                           font=("Courrier", 25), fill="white")

        self.updated_already_submited_letters = self.canvas.create_text(240, 390, text=" ".join(
            actual_hidden_word.letter_already_proposed), font=("Courrier", 14), fill="white")

        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white",
                                   command=self.player_giveUp, cursor="star")
        button_backToMenu.pack(pady=5, fill=X)

        self.input_letter = Entry(self, width=10, bg="black", fg="white", cursor="pencil", justify="center",
                                  insertbackground="white")
        self.input_letter.pack(pady=5, fill=X)

        button_letter = Button(self, text="Proposer ma lettre", font=("Courrier", 20), bg="#223F44", fg="white",
                               cursor="star", command=self.on_submit_letter_clicked)
        button_letter.pack(pady=5, fill=X)

        button_clue = Button(self, text="Montrer un indice", font=("Courrier", 15), bg="#223F44", fg="white",
                               cursor="star", command=Misc.show_definition)
        button_letter.pack(pady=5, fill=X)

        self.canvas.create_window(430, 630, anchor="nw", window=button_backToMenu)
        self.canvas.create_window(520, 110, anchor="nw", window=self.input_letter)
        self.canvas.create_window(420, 140, anchor="nw", window=button_letter)
        self.canvas.create_window(420, 240, anchor="nw", window=self.canvas_fusee)
        self.canvas.create_window(890, 640, anchor="nw", window=button_clue)

        self.canvas.pack(fill="both", expand="True")

    def setTitle(self, title: str):
        self.canvas.itemconfig(globalFrames[2].letterLabelIndex, text="Thème choisi: " + title)

    def update_letters_in_canvas(self):
        self.canvas.itemconfig(globalFrames[2].updated_hidden_word,
                               text=" ".join(actual_hidden_word.list_found_letters))
        self.canvas.itemconfig(globalFrames[2].updated_already_submited_letters,
                               text=", ".join(actual_hidden_word.letter_already_proposed))

class PageIAdifficulty(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        self.canvas = Canvas(self, width=width, height=height, bg="#223F44")
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.letterLabelIndex = self.canvas.create_text(540, 50, text="Choisi la difficulté de l'ordinateur:",
                                                        font=("Courrier", 25), fill="white")

        button_easy = Button(self, text="Facile", font=("Courrier", 20), bg="#223F44", fg="white",
                             command=lambda: [controller.show_frame("PageThemeChoice"), logic_IA.setIAdifficulty(1)],
                             cursor="star")
        button_easy.pack(pady=5, fill=X)
        button_average = Button(self, text="Normal", font=("Courrier", 20), bg="#223F44", fg="white",
                                command=lambda: [controller.show_frame("PageThemeChoice"), logic_IA.setIAdifficulty(2)],
                                cursor="star")
        button_average.pack(pady=5, fill=X)
        button_hard = Button(self, text="Difficile", font=("Courrier", 20), bg="#223F44", fg="white",
                             command=lambda: [controller.show_frame("PageThemeChoice"), logic_IA.setIAdifficulty(3)],
                             cursor="star")
        button_hard.pack(pady=5, fill=X)
        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white",
                                   command=lambda: controller.show_frame("StartPage"), cursor="star")
        button_backToMenu.pack(pady=5, fill=X)

        self.canvas.create_window(475, 250, anchor="nw", window=button_easy)
        self.canvas.create_window(475, 320, anchor="nw", window=button_average)
        self.canvas.create_window(475, 390, anchor="nw", window=button_hard)
        self.canvas.create_window(475, 540, anchor="nw", window=button_backToMenu)

        self.canvas.pack(fill="both", expand="True")

class PageIAGame(tk.Frame):

    def on_submit_letter_clicked(self):
        submited_letter = self.input_letter.get()
        self.input_letter.delete(0, "end")
        letter_submitted_player = submited_letter
        logic_pendu.check_letter_isValid(self, letter_submitted_player, actual_hidden_word)
        self.update_letters_in_canvas()

        logic_IA.IA_behavior(self, actual_hidden_word)
        self.update_IA_letters_in_canvas()


    def IA_loose_one_try(self):
        global IA_lives_left
        global lives_left
        IA_lives_left -= 1
        if IA_lives_left == -1:
            messagebox.showinfo(message="L'ordinateur a perdu! Le mot caché était: " + actual_hidden_word.hidden_word,
                                command=self.controller.show_frame("StartPage"))
            IA_lives_left = 5
            lives_left = 5
            self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
            self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")

    def check_if_IA_win(self, word: hiden_word):
        global IA_lives_left
        global lives_left


        if "_" not in word.list_found_letters_by_IA:
            if (logic_IA.player_won != True) and (logic_IA.player_lost != True):
                messagebox.showinfo(message="L'ordinateur a gagné! Le mot caché était: " + word.hidden_word,
                                    command=self.controller.show_frame("StartPage"))
            IA_lives_left = 5
            lives_left = 5
            self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
            self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")


    def show_hidden_word(self):
        global lives_left
        messagebox.showinfo(message="Tu abandonne? Le mot caché était: " + actual_hidden_word.hidden_word)
        lives_left = 5

        self.image_fusee = PhotoImage(file="fusee_" + str(lives_left) + ".png")
        self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")

    def player_giveUp(self):
        self.controller.show_frame("StartPage")
        PageSoloGame.show_hidden_word(self)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        self.canvas = Canvas(self, width=width, height=height, bg="#223F44")
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.image_fusee = PhotoImage(file="fusee_5.png")
        self.canvas_fusee = Canvas(self, width=284, height=236, bg="#223F44")
        self.canvas_fusee.create_image(0, 0, image=self.image_fusee, anchor="nw")
        self.canvas_fusee.pack(fill="both", expand="True")

        self.letterLabelIndex = self.canvas.create_text(540, 50, text="A toi de jouer!!" + data.nom_du_theme,
                                                        font=("Courrier", 25), fill="white")

        self.updated_hidden_word = self.canvas.create_text(240, 350, text=" ".join(actual_hidden_word.list_letters),
                                                           font=("Courrier", 25), fill="white")

        self.updated_already_submited_letters = self.canvas.create_text(140, 390, text=" ".join(
            actual_hidden_word.letter_already_proposed), font=("Courrier", 14), fill="white")

        self.updated_IA_hidden_word = self.canvas.create_text(910, 350, text=" ".join(actual_hidden_word.list_letters),
                                                              font=("Courrier", 25), fill="white")

        self.updated_IA_already_submited_letters = self.canvas.create_text(940, 390, text=" ".join(
            actual_hidden_word.letter_already_proposed), font=("Courrier", 14), fill="white")

        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white",
                                   command=self.player_giveUp, cursor="star")
        button_backToMenu.pack(pady=5, fill=X)

        self.input_letter = Entry(self, width=10, bg="black", fg="white", cursor="pencil", justify="center",
                                  insertbackground="white")
        self.input_letter.pack(pady=5, fill=X)

        button_letter = Button(self, text="Proposer ma lettre", font=("Courrier", 20), bg="#223F44", fg="white",
                               cursor="star", command=self.on_submit_letter_clicked)
        button_letter.pack(pady=5, fill=X)

        button_clue = Button(self, text="Montrer un indice", font=("Courrier", 15), bg="#223F44", fg="white",
                               cursor="star", command=Misc.show_definition)
        button_letter.pack(pady=5, fill=X)

        self.canvas.create_window(430, 630, anchor="nw", window=button_backToMenu)
        self.canvas.create_window(520, 110, anchor="nw", window=self.input_letter)
        self.canvas.create_window(420, 140, anchor="nw", window=button_letter)
        self.canvas.create_window(420, 240, anchor="nw", window=self.canvas_fusee)
        self.canvas.create_window(890, 640, anchor="nw", window=button_clue)

        self.canvas.pack(fill="both", expand="True")

    def setTitle(self, title: str):
        self.canvas.itemconfig(globalFrames[3].letterLabelIndex, text="Thème choisi: " + title)

    def update_letters_in_canvas(self):
        self.canvas.itemconfig(globalFrames[3].updated_hidden_word,
                               text=" ".join(actual_hidden_word.list_found_letters))
        self.canvas.itemconfig(globalFrames[3].updated_already_submited_letters,
                               text=", ".join(actual_hidden_word.letter_already_proposed))

    def update_IA_letters_in_canvas(self):
        self.canvas.itemconfig(globalFrames[3].updated_IA_hidden_word,
                               text=" ".join(actual_hidden_word.list_found_letters_by_IA))
        self.canvas.itemconfig(globalFrames[3].updated_IA_already_submited_letters,
                               text=", ".join(actual_hidden_word.letters_proposed_by_IA))

if __name__ == "__main__":
    globalFrames = []
    data.create_dict_vocab(data, "Audio7-Repas_avec_papy_Guytou-corrige.xml")
    actual_hidden_word = hiden_word("", "", "")
    lives_left = 5
    IA_lives_left = 5
    pygame.mixer.init()
    Misc.play_soundTrack()
    app = SampleApp()
    app.mainloop()