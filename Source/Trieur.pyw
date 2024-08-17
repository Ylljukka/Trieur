import os
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import *
import glob
import time
import shutil
import webbrowser
from threading import Thread
from tkinter import ttk

dico_mois = {'Jan':'Janvier', 'Feb':'Février', 'Mar':'Mars', 'Apr':'Avril', 'May':'Mai', 'Jun':'Juin',
             'Jul':'Juillet', 'Aug':'Août', 'Sep':'Septembre','Oct':'Octobre', 'Nov':'Novembre', 'Dec':'Décembre'}


# Pour l'application en général
# Classe Application définit les boutons, taille, titre etc ...

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.dirname_entry = tk.StringVar(value=" " * 71)
        self.dirname_out = tk.StringVar(value=" " * 71)

        # La fenêtre générale :
        self.title("Trieur de fichier v3.0.0")
        self.configure(bg='#393939')
        self.geometry('800x620')
        self.resizable(width=False, height=False)
        self.icone = self.iconbitmap('files/icone.ico')

        # Création du menu en barre
        self.menubarre = tk.Menu(self)
        self.config(menu = self.menubarre)
        self.file_menu = tk.Menu(self.menubarre, tearoff=False)
        self.menubarre.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(label='Quitter', command=self.destroy)

        # le menu "A propos"
        self.edition_menu = tk.Menu(self.menubarre, tearoff=False)
        self.menubarre.add_cascade(label="A propos", menu=self.edition_menu)
        self.edition_menu.add_command(label='Dons (Paypal)', command=lambda:self.web(web_link=0))
        self.edition_menu.add_command(label='Notes de version', command=self.note_version)

        # Création des boutons
        self.chemin_entree = tk.Button(height=3, width=30, text="Dossier des fichiers à trier", font = ('Ebrima', 10), command=self.entry)
        self.chemin_sortie = tk.Button(height=3, width=30, text="Dossier de sortie", font = ('Ebrima', 10), command=self.out)
        self.validation = tk.Button(height=3, width=30, text="Validation", font = ('Ebrima', 10), command=self.progresse_barre)
        self.quitter = tk.Button(height =3, width=30, text="Quitter", background="#E70739", font = ('Ebrima', 10), command=self.destroy)
        self.logo = tk.PhotoImage(file = 'files/linkedin.png')
        self.linkedin = tk.Button(image = self.logo, command=lambda:self.web(web_link=1)) 
        self.logo_github = tk.PhotoImage(file = 'files/github.png')
        self.github = tk.Button(image = self.logo_github, command=lambda:self.web(web_link=2)) 

       # La liste pour le choix du tri
        self.option_list = ["Date de création", "Date de modification"]
        self.type_date = tk.StringVar()
        self.type_date.set(self.option_list[0])
        self.type_date_valeur = self.type_date.get()
        self.tri_sur = tk.Label(text= "Tri sur : ", font='Helvetica 12 bold', bg= '#393939', fg= 'white')
        self.choix = tk.Label(text = "Choix du format jpg, pdf... : ", font='Helvetica 12 bold', bg= '#393939', fg= 'white')
        self.format = tk.Entry(font='Helvetica 10 bold')
        self.aff_chemin_entree = tk.Label(textvariable=self.dirname_entry, relief='ridge', wraplength =220)
        self.aff_chemin_sortie = tk.Label(textvariable=self.dirname_out, relief='ridge', wraplength =220)
        self.option = tk.OptionMenu(self, self.type_date, *self.option_list)
        self.option.config(width=10, font=('Ebrima', 10))
        self.type_date.trace("w", self.callback)
        self.dev = tk.Label(text = "Développé par Thomas REYNAUD", font='Helvetica 8 bold', bg= '#393939', fg= 'white')
        

        # Les emplacements
        self.choix.place(x=250, y=30, width=220, height=30)
        self.option.place(x=480, y=90, width =200)
        self.tri_sur.place(x=190, y=90, width=200, height=30)
        self.format.place(x=480, y=35, width=40, height=20)
        self.chemin_entree.place(x=70, y=180)
        self.aff_chemin_entree.place(x=70, y=280)
        self.chemin_sortie.place(x=480, y=180)
        self.aff_chemin_sortie.place(x=480, y=280)
        self.validation.place(x=280, y=350)
        self.quitter.place(x=280, y=480)
        self.linkedin.place(x=750, y=550)
        self.github.place(x=700, y=550)
        self.dev.place(x=10, y=570)

# Le callback pour identifier chaque changement du choix des types de date
    def callback(self, *args):
        self.type_date_valeur = self.type_date.get()
        
    # Les fonctions pour l'explorateur (chemin entrée et de sortie)
    def entry(self):
        self.path_entry = filedialog.askdirectory(parent=app, initialdir="/", title='Choix du dossier')
        self.dirname_entry.set(self.path_entry)
        if self.dirname_entry != ' ':
            self.dirname_entry.set(self.path_entry)
            self.entree = (self.dirname_entry.get())

    def out(self):
        self.path_out = filedialog.askdirectory(parent=app, initialdir='/', title='Choix du dossier')
        self.dirname_out.set(self.path_out)
        if self.dirname_out != ' ':
            self.sortie = (self.dirname_out.get())

# Les différentes ouvertures de pages web
    def web(self, web_link):
        if web_link ==0:
            webbrowser.open_new('https://www.paypal.com/paypalme/Thomas6598')
        elif web_link ==1 :
            webbrowser.open_new('https://www.linkedin.com/in/thomas-reynaud-2a8b02197/')

        elif web_link ==2:
            webbrowser.open_new('https://github.com/Ylljukka?tab=repositories')


# La fenêtre des notes de version
    def note_version(self):
        self.fenetre = tk.Toplevel(app)
        self.fenetre.title("Notes de version")
        self.fenetre.configure(bg='#393939')
        self.fenetre.geometry('540x350')

        self.texte = tk.Text(self.fenetre, bg='#393939', fg = 'white')
        self.texte.pack()

        with open("files/Notes de version.txt", "r", encoding='utf-8') as notes:
            self.notes_versions= notes.read()
        self.texte.insert('1.0', self.notes_versions)
        self.fenetre.mainloop()

    def progresse_barre(self):
        # Création de la barre de progression
        self.pbar = ttk.Progressbar(orient="horizontal", length=220, mode='indeterminate')
        self.pbar.place(x=280, y=430)
        self.pbar.start()

        # execution en utilisant le multithreading pour éviter l'effet plantage
        Thread(target=self.validate).start()



    def validate(self):
        self.type = ""
        # On teste si les répertoires d'entrée et de sortie ont bien été renseignés
        if not self.dirname_entry.get().strip():
            self.pbar.destroy()
            self.type = 1
            self.titre = "Répertoire d'entrée non renseigné"
            self.message = "Veuillez choisir un dossier en entrée."
            Tri.messages(self, self.type, self.titre, self.message)


        elif not self.dirname_out.get().strip():
            self.pbar.destroy()
            self.type = 1
            self.titre = "Répertoire de sortie non renseigné"
            self.message = "Veuillez choisir un dossier de destination."
            Tri.messages(self, self.type, self.titre, self.message)

        # Si oui on passe à la suite
        else:
            Tri.format(self, self.format, self.entree)
            if self.type != 1:
                Tri.medias(self)

class Tri :
    def __init__(self, format, entree, sortie, type_date_valeur, pbar):
        self.mon_format = format
        self.entree = entree
        self.sortie = sortie
        self.type_date_valeur = type_date_valeur
        self.pbar = pbar

# On récupère le bon format choisi et teste s'il est renseigné
    def format(self, format, entree):
        self.mon_format = format.get()
        if self.mon_format == '':
            self.pbar.destroy()
            self.type = 1
            self.titre = "Format à trier inexistant."
            self.message = "Veuillez choisir un format (jpg, pdf, mp3 etc...) à renseigner pour le tri."
            Tri.messages(self, self.type, self.titre, self.message)
            return self.type
        else:
            self.entree = entree


    def medias(self):
            
            self.medias_dossier = glob.glob(self.entree + '/' + '*' + self.mon_format)

            # Contrôle de la présence du format choisi dans le dossier et vérification du dossier de sortie
            if self.medias_dossier == []:
                self.pbar.destroy()
                self.type = 1
                self.titre = "Fichier à trier inexistant."
                self.message = "Répertoire ne contenant pas de " + self.mon_format + "."", Veuillez choisir un dossier source contenant des fichiers au format " + self.mon_format +"."
                Tri.messages(self, self.type, self.titre, self.message)

            elif self.sortie == '':
                self.pbar.destroy()
                self.type = 1
                self.titre = "Répertoire de sortie non renseigné"
                self.message = "Veuillez choisir un dossier de destination."
                Tri.messages(self, self.type, self.titre, self.message)

            else:
                Tri.recup_date(self, self.type_date_valeur)
                Tri.verification(self)


    def recup_date(self, type_date_valeur):
        self.type_date_valeur = type_date_valeur

        # Initialisation du compteur
        i = 0

        # Si on a choisit date de modfication, On récupère la date de modif
        if self.type_date_valeur =="Date de modification":
            for self.medias in self.medias_dossier:
                self.m_time = os.path.getmtime(self.medias)
                self.local_time = time.ctime(self.m_time)
                if not Tri.deplacement(self, self.medias, self.local_time):
                    continue
                i += 1
        
        #Sinon on a pris la date de création
        elif self.type_date_valeur == "Date de création":
            for self.medias in self.medias_dossier:
                self.c_time = os.path.getctime(self.medias)
                self.local_time = time.ctime(self.c_time)
                if not Tri.deplacement(self, self.medias, self.local_time):
                    continue
                i += 1


        self.pbar.destroy()
        self.n = str(i)
        self.type = 3
        self.titre = "Tri terminé"
        self.message = "Tri des " +self.mon_format+ " terminé avec succès, " + self.n +" "+ self.mon_format+' triées.'
        Tri.messages(self, self.type, self.titre, self.message)

    def deplacement(self, medias, local_time):
            self.medias = medias
            self.local_time = local_time
            
        # Pour les dossiers à créer on extrait l'année et le mois

            first, *middle, last = self.local_time.split()
            self.annee = last
            self.mois = self.local_time[4:7]
            self.mois_complet = dico_mois[self.mois]

        # Vérif et création du dossier
            self.sortie_complete = self.sortie + '/' + self.annee + '/' + self.mois_complet
            if not os.path.exists(self.sortie_complete):
                os.makedirs(self.sortie_complete)

            # Déplacement des fichiers sur date de création/ modification
            self.fichier_ok = medias.split('\\', 1)[1]
            self.file_source = self.entree + '/'
            self.file_destination = self.sortie_complete + '/'
                
            # Si le fichier existe déja on passe au suivant
            if os.path.exists(self.file_destination + self.fichier_ok):
                return False
            else:

            # Sinon, on déplace et on passe True pour alimenter le compteur
                shutil.move(self.file_source + self.fichier_ok, self.file_destination)
                return True


    def verification(self) :
        # Vérifie si des fichiers sont encore dans le dossier source
        self.liste_restant = glob.glob(self.file_source + '*' + self.mon_format)

        if len(self.liste_restant) != 0:
            self.type = 2
            self.titre = "Répertoire de sortie non renseigné"
            self.message = "Des " +self.mon_format+ " n'ont pas été déplacé, car elles exisent déja dans le dossier de destination.'"
            Tri.messages(self, self.type, self.titre, self.message)

# Fonction pour la gestion des messages
    def messages(self, type, titre, message):
        self.type = type
        self.titre = titre
        self.message = message

        #message d'erreur
        if self.type == 1:
            showerror(title= self.titre , message= self.message)

        #message d'information
        elif self.type ==2:
            showerror('Information', title= self.titre , message= self.message)

        # Message d'aquittement
        else : #self.type == 3:
            showinfo("Information", message= self.message)

app = Application()
app.mainloop()

