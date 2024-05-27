import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import *
import pygame

#def play_soundTrack():

   # pygame.mixer.music.load("Dee Yan-Key - silent night  (stille nacht).mp3")
    #pygame.mixer.music.play(loops=100)



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        tk.Tk.iconbitmap(self, default="Screenshot (846).ico")
        tk.Tk.title(self, "Le jeu du pendu")
        tk.Tk.geometry(self, "1080x720")



        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)




        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")



        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        canvas = Canvas(self, width=width, height=height, bg="#223F44")
        canvas.create_image(0, 0, image=self.image, anchor="nw")

        canvas.create_text(540, 160, text="Salut aventurier du cosmos lexical!", font=("Courrier", 40), fill="white")
        canvas.create_text(540, 210, text="Pour jouer au pendu, choisit un mode de jeu:", font=("Courrier", 25), fill="white")

        button_soloPlayer = Button(self, text=" Mode solo  ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageOne"), cursor="star")
        button_soloPlayer.pack(pady=10, fill=X)
        button_multiPlayer = Button(self, text=" multiplayer ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageOne"), cursor="star")
        button_multiPlayer.pack(pady=5, fill=X)
        button_AI = Button(self, text="       AI        ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageOne"), cursor="star")
        button_AI.pack(pady=5, fill=X)

        button1 = canvas.create_window(475, 350, anchor="nw", window=button_soloPlayer)
        button1 = canvas.create_window(475, 420, anchor="nw", window=button_multiPlayer)
        button1 = canvas.create_window(475, 490, anchor="nw", window=button_AI)

        canvas.pack(fill="both", expand="True")




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        canvas = Canvas(self, width=width, height=height, bg="#223F44")
        canvas.create_image(0, 0, image=self.image, anchor="nw")

        canvas.create_text(540, 110, text="Choisit une dimension interstellaire:", font=("Courrier", 25), fill="white")

        button_soloPlayer = Button(self, text="  Informatique   ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageTwo"), cursor="star")
        button_soloPlayer.pack(pady=10, fill=X)
        button_multiPlayer = Button(self, text="      Animaux     ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageTwo"), cursor="star")
        button_multiPlayer.pack(pady=5, fill=X)
        button_AI = Button(self, text="        Sport        ", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("PageTwo"), cursor="star")
        button_AI.pack(pady=5, fill=X)
        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("StartPage"), cursor="star")
        button_backToMenu.pack(pady=5, fill=X)

        button1 = canvas.create_window(475, 250, anchor="nw", window=button_soloPlayer)
        button1 = canvas.create_window(475, 320, anchor="nw", window=button_multiPlayer)
        button1 = canvas.create_window(475, 390, anchor="nw", window=button_AI)
        button1 = canvas.create_window(475, 460, anchor="nw", window=button_backToMenu)


        canvas.pack(fill="both", expand="True")






class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        width = 1080
        height = 720
        self.image = PhotoImage(file="Screenshot (847).png")
        canvas = Canvas(self, width=width, height=height, bg="#223F44")
        canvas.create_image(0, 0, image=self.image, anchor="nw")

        canvas.create_text(540, 50, text="A toi de jouer!!", font=("Courrier", 25), fill="white")

        button_backToMenu = Button(self, text="Retour au menu", font=("Courrier", 20), bg="#223F44", fg="white", command=lambda: controller.show_frame("StartPage"), cursor="star")
        button_backToMenu.pack(pady=5, fill=X)


        button_letter = Button(self, text="Proposer ma lettre", font=("Courrier", 20), bg="#223F44", fg="white", cursor="star")
        button_letter.pack(pady=5, fill=X)

        input_letter = Entry(self, width=10,  bg="black", fg="white", cursor="pencil", justify="center", insertbackground="white")
        #input_letter.insert(0, "Propose une lettre")
        input_letter.pack(pady=5, fill=X)

        button1 = canvas.create_window(430, 630, anchor="nw", window=button_backToMenu)
        button1 = canvas.create_window(520, 110, anchor="nw", window=input_letter)
        button1 = canvas.create_window(420, 140, anchor="nw", window=button_letter)


        canvas.pack(fill="both", expand="True")




if __name__ == "__main__":
    pygame.mixer.init()
    #play_soundTrack()
    app = SampleApp()
    app.mainloop()

