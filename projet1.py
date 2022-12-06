from tkinter import *
import sqlite3
from tkinter import ttk
from datetime import datetime
import subprocess
import serial
import time
#Fonction Connexion------------------------
def Connexion() :
    user = entryUser.get()
    mdp = entryMdp.get()
    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    cur.execute(" select count(*) from Utilisateur where User ='"+user+"' and Mdp ='"+mdp+"' " )
    select = cur.fetchone()
    if int(select[0]) > 0:

        # Fonction Ajouter----------------------
        def Ajouter():

            # get form data
            matricule = entryMatricule.get()
            nom = entryNom.get()
            prenom = entryPrenom.get()
            post = entryPost.get()
            shift = entryShift.get()
            id_produit = entryID_Produit.get()

            conn = sqlite3.connect('mydatabase.db')
            cur = conn.cursor()
            req1 = "CREATE TABLE IF NOT EXISTS abdellah(Matricule INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT , Prenom TEXT , post TEXT)"
            cur.execute(req1)
            req2 = "INSERT INTO abdellah (Matricule , Nom , Prenom , Post, Shift, ID_Produit) values (?, ?, ?, ?, ?, ?)"
            cur.execute(req2, (matricule, nom, prenom, post, shift, id_produit))
            conn.commit()
            conn.close()

        # ----- Fin Ajouter-------------------------------------------------------------------------

        # Fcontion Supprimer------------------------------------------------------------------------
        def Supprimer():

            matricule = entryMatricule.get()
            nom = entryNom.get()
            prenom = entryPrenom.get()
            post = entryPost.get()
            shift = entryShift.get()
            id_produit = entryID_Produit.get()
            conn = sqlite3.connect('mydatabase.db')
            cur = conn.cursor()

            req1 = "DELETE FROM abdellah WHERE Matricule == ? and Nom == ? and Prenom == ? and Post == ? and Shift == ? and ID_Produit == ?"
            cur.execute(req1, (matricule, nom, prenom, post, shift, id_produit))
            conn.commit()
            conn.close()

        # ----------fin fonction Supprimer --------------
        # Fonction Modifier ---------------------------------------------
        def Modifier():
            matricule = entryMatricule.get()
            nom = entryNom.get()
            prenom = entryPrenom.get()
            post = entryPost.get()
            shift = entryShift.get()
            id_produit = entryID_Produit.get()
            conn = sqlite3.connect('mydatabase.db')
            cur = conn.cursor()
            req1 = "UPDATE 'abdellah' set   NOM = ? , Prenom = ? , Post =  ? , Shift = ? , ID_Produit = ? " \
                   "WHERE  Matricule == ?"
            cur.execute(req1, (nom, prenom, post, shift, id_produit, matricule))
            conn.commit()
            conn.close()

        # Fin-------------------------------------
        # Fonction Start ---------------------------------------------------------
        def Start():
            matricule = entryMatricule.get()
            tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show="headings")
            tree.place(x=350, y=100, width=480, height=200)

            tree.heading(1, text="Produit_Id")
            tree.heading(2, text="Produit_Labelle")
            tree.heading(3, text="Temps_F")
            tree.heading(4, text="Quantite_stocke")
            tree.heading(5, text="Quantite_restante")

            tree.column(1, width=25)
            tree.column(2, width=25)
            tree.column(3, width=25)
            tree.column(4, width=25)
            tree.column(5, width=25)

            conn = sqlite3.connect("mydatabase.db")
            cur = conn.cursor()
            select = cur.execute(
            "select Produit.ID,Produit.Labelle,Produit.Temps_F,Produit.Quantite_stocke,Produit.Quantite_restante FROM Produit,abdellah WHERE abdellah.Matricule==matricule and abdellah.ID_Produit==Produit.ID")
            for row in select:
                tree.insert('', END, values=row)


            #yahyas
            arduino=serial.Serial('COM11',9600)
            time.sleep(2)
            if arduino.isOpen():
                arduino.close()
            arduino.open()
            arduino.isOpen()
            dato_leido=arduino.readline()
            time.sleep(2)
            print(dato_leido)
            arduino.write('a'.encode())
            time.sleep(2) 
            arduino.close()

            #finYahyas

        # FIN Start-----------------------------------------------------------
        # Fonction Presence ------------------------------------------------------
        def Presence():
            matricule = entryMatricule.get()
            presence = r.get()
            conn = sqlite3.connect("mydatabase.db")
            cur = conn.cursor()
            req = "INSERT INTO Presence(Matricule , P_A) values (? , ?)"
            cur.execute(req, (matricule, presence))
            conn.commit()
            conn.close()

        # Fin Presence ----------------------------------------------
        # Fonction Stop --------------------------------------------------
        def Stop():
            cause = r1.get()
            matricule = entryMatricule.get()
            heure = datetime.now()
            conn = sqlite3.connect("mydatabase.db")
            cur = conn.cursor()
            req = "INSERT INTO Historique(Matricule_operateur , Cause_arret , Heure_arret ) values (? , ? , ?)"
            cur.execute(req, (matricule, cause, heure))
            conn.commit()
            conn.close()

        # Fin fonction stop--------------------------------------------------------------------------
        # Fonction Historique------------------------------------------------------------------------
        def Historique():
            tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show="headings")
            tree.place(x=400, y=400, width=420, height=200)

            tree.heading(1, text="Matricule")
            tree.heading(2, text="NOM")
            tree.heading(3, text="Prenom")
            tree.heading(4, text="cause d'arret")
            tree.heading(5, text="heure d'arret")

            tree.column(1, width=25)
            tree.column(2, width=25)
            tree.column(3, width=25)
            tree.column(4, width=25)
            tree.column(5, width=25)

            conn = sqlite3.connect("mydatabase.db")
            cur = conn.cursor()
            select = cur.execute(
                "select Historique.Matricule_operateur, abdellah.Nom ,abdellah.Prenom,Historique.Cause_arret,Historique.Heure_arret FROM Historique,abdellah WHERE Historique.Matricule_operateur == abdellah.Matricule ")
            for row in select:
                tree.insert('', END, values=row)

        # Fin Fonction Historique -----------------------------------------------------------

        root = Tk()
        root.title("Lad 333L & M T7")
        root.geometry("850x650")
        root.config(bg="#4169E1")



        # Image

        # create a form to insert data ( MATRICULE---) lblName = Laben(roott , text = "Nom :" )
        #Entry temp_F


        #Entry nbr_
        # Enrty Matricule
        lblMatricule = Label(root, text="Matricule :")
        lblMatricule.place(x=10, y=10)
        entryMatricule = Entry(root)
        entryMatricule.place(x=100, y=10, width=200)
        # Entry NOM
        lblNom = Label(root, text="Nom :")
        lblNom.place(x=10, y=40)
        entryNom = Entry(root)
        entryNom.place(x=100, y=40, width=200)
        # Entry Prenom
        lblPrenom = Label(root, text="Prenom :")
        lblPrenom.place(x=10, y=70)
        entryPrenom = Entry(root)
        entryPrenom.place(x=100, y=70, width=200)
        # Entry Post
        lblPost = Label(root, text="Post :")
        lblPost.place(x=10, y=100)
        entryPost = Entry(root)
        entryPost.place(x=100, y=100, width=200)
        # Entry Shift
        lblShift = Label(root, text="Shift :")
        lblShift.place(x=10, y=130)
        entryShift = Entry(root)
        entryShift.place(x=100, y=130, width=200)
        # Entry ID_Produit
        lblID_Produit = Label(root, text="ID_Produit :")
        lblID_Produit.place(x=10, y=160)
        entryID_Produit = Entry(root)
        entryID_Produit.place(x=100, y=160, width=200)

        # Button Ajouter
        btnAjouter = Button(root, text="Ajouter", command=Ajouter)
        btnAjouter.place(x=10, y=310, width=100, height=25)
        # Button Supprimer
        btnSupprimer = Button(root, text="Supprimer", command=Supprimer)
        btnSupprimer.place(x=100, y=310, width=100, height=25)
        # Button Modifier
        btnModifier = Button(root, text="Modifier", command=Modifier)
        btnModifier.place(x=200, y=310, width=100, height=25)
        # Button Start
        btnStart = Button(root, text="Start", command=Start)
        btnStart.place(x=500, y=5, width=100, height=25)
        # Button Presence
        btnPresence = Button(root, text="Presence", command=Presence)
        btnPresence.place(x=10, y=350, width=100, height=25)
        r = IntVar()
        case1 = Radiobutton(root, text='Present', variable=r, value=1)
        case2 = Radiobutton(root, text='Absent', variable=r, value=2)
        case1.place(x=10, y=380)
        case2.place(x=10, y=400)

        # Button Stop
        btnStop = Button(root, text="Stop", command=Stop)
        btnStop.place(x=10, y=435, width=100, height=25)
        # Entry du boutton stop
        r1 = IntVar()
        case1 = Radiobutton(root, text='Maintenance', variable=r1, value=1)
        case2 = Radiobutton(root, text="chef d'equipe", variable=r1, value=2)
        case3 = Radiobutton(root, text='Pause', variable=r1, value=3)
        case4 = Radiobutton(root, text='Fin shift', variable=r1, value=4)
        case5 = Radiobutton(root, text='Manque de materels', variable=r1, value=5)
        case6 = Radiobutton(root, text="La fatigue", variable=r1, value=6)
        case1.place(x=10, y=465)
        case2.place(x=10, y=490)
        case3.place(x=10, y=510)
        case4.place(x=10, y=535)
        case5.place(x=10, y=560)
        case6.place(x=10, y=585)
        # button historique
        btnHistorique = Button(root, text="Historique", command=Historique)
        btnHistorique.place(x=500, y=350, width=100, height=25)

        # --------Display Data-------------------
        tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6), show="headings")
        tree.place(x=10, y=200, width=300, height=100)

        tree.heading(1, text="Matricule")
        tree.heading(2, text="Nom")
        tree.heading(3, text="Prenom")
        tree.heading(4, text="Post")
        tree.heading(5, text="Shift")
        tree.heading(6, text="ID_Produit")

        tree.column(1, width=50)
        tree.column(2, width=50)
        tree.column(3, width=50)
        tree.column(4, width=50)
        tree.column(5, width=50)
        tree.column(6, width=50)

        conn = sqlite3.connect("mydatabase.db")
        cur = conn.cursor()
        req = "CREATE TABLE IF NOT EXISTS abdellah(Matricule INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT , Prenom TEXT , post TEXT)"
        cur.execute(req)
        select = cur.execute("select * from abdellah")
        for row in select:
            tree.insert('', END, values=row)
        # ---------end_display----------------------

        root.mainloop()




    else:
        lblErreur = Label(roott, text="Utilisateur non autorisé")
        lblErreur.place(x=100, y=130)
#Fin connex -------------------------------------

roott = Tk()
roott.geometry("600x400")
roott.title("Authentification")
#can = Canvas(roott, width=600, height=400)
#img=PhotoImage(file="C:\Users\abde\Desktop\d.jpeg")
roott.config(bg="#4169E1")




lblUser = Label(roott , text ="User_Name :")
lblUser.place(x = 10 , y = 20)
entryUser = Entry(roott)
entryUser.place(x=100 , y = 20 , width = 200)
lblMdp = Label(roott , text ="Mot_de_Passe :")
lblMdp.place(x = 10 , y = 60)
entryMdp = Entry(roott,show="*")
entryMdp.place(x=100 , y = 60 , width = 200)
#Button Connexion
btnConnex = Button(roott, text = "connexion" , command = Connexion)
btnConnex.place(x = 250 , y = 100 , width = 100 , height = 25)

roott.mainloop()
