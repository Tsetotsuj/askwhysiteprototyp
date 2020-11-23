# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:12:13 2020

@author: H
"""
#import hashlib
import pandas as pd
import streamlit as st
import awesome_streamlit as ast
from PIL import Image
import numpy as np
import pickle 
import requests
from bs4 import BeautifulSoup
from datetime import datetime

import json



file = open("data.json","r+")
file. truncate(0)
file. close()

diagnostic= ['','','','']




#from time import sleep
admin = "MohSaNat"
mdp = "root"

requete = requests.get("https://api.ipify.org/")
page = requete.content
soup = BeautifulSoup(page,features="lxml")
soup =str(soup)
sip = soup.split("<html><body><p>")
ip = sip[1].split("</p></body></html>")
finalip = ip[0]


# Utils Pkgs
import codecs

# Components Pkgs
import streamlit.components.v1 as components

# Custom Components Fxn
def calculator(calc_html,width=750,height=340):
	calc_file = codecs.open(calc_html,'r')
	page = calc_file.read()
	components.html(page,width=width,height=height,scrolling=False)

#		components.html(html_temp)

# DB Management

def write():
    with st.spinner("Loading Home ..."):
        ast.shared.components.title_awesome("")

# Security
#passlib,hashlib,bcrypt,scrypt

#def make_hashes(poids):
#	return hashlib.sha256(str.encode(poids)).hexdigest()

#def check_hashes(poids,hashed_text):
#	if make_hashes(poids) == hashed_text:
#		return hashed_text
#	return False
        
# DB Management
import sqlite3 
Kontakt = sqlite3.connect('Contactuser.db')
k = Kontakt.cursor()
conn = sqlite3.connect('info_user_2011.db')

c = conn.cursor()
#### DB  Functions


def creer_tablecontact():
	k.execute('CREATE TABLE IF NOT EXISTS Kontakt( email TEXT,message TXT, date TXT)')


def ajouter_contact(vemail,vemessage):
    date = str(datetime.now())
    k.execute('INSERT INTO Kontakt(email,message,date) VALUES (?,?,?)',(vemail,vemessage, date))
    Kontakt.commit()



def rgpd():
    dat = str(datetime.now()).split(':')
    datel = str(dat[0] )
    c.execute('DELETE FROM userstable WHERE date LIKE (?) and ipadress = (?)',('%' + datel+ '%',finalip))
    conn.commit()




# données de l'utilisateur
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(age INT, ipadress TEXT,poids INT,taille INT,Symptomes TXT, date TXT)')


def add_userdata(age,ipadress,poids,taille,symptomes):
    date = str(datetime.now())
    c.execute('INSERT INTO userstable(age,ipadress,poids,taille,date,Symptomes) VALUES (?,?,?,?,?,?)',(age,ipadress,poids,taille,date,symptomes))
    conn.commit()


def voir_contact():
    k.execute('SELECT * FROM Kontakt')
    data2 = k.fetchall()
    return data2

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
#cree toi meme  un identifiant et un mot de passe intra code histoire de creer un admin et avec ça t'as accès a la focntion view_all_users()



def universel(finalip,my_poids,my_taille,my_age,sym) :
    ipadress = finalip
    poids = my_poids
    age = my_age
    sympt = str(sym)
    create_usertable()
    taille = my_taille
    #hashed_pswd = make_hashes(ipadress)
    hashed_pswd = ipadress #on met ca a la place
    add_userdata(age,hashed_pswd,poids,taille,sympt)
def main():
    # Register your pages
    pages = {
        "Home" : page_home  ,  
        "Covid-19": page_first,
        "Diabète": page_second,
        "Maladie Cardiaque": page_3,
        "Conseils & Partenariats": page_4,
        "Contact" : page_5,
        "Admin": page_6,
        
    }

    st.markdown(
        """
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#91a6c2,#91a6c2);
        color: white;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.sidebar.title("Ask Why")

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("Sélectionnez la maladie à tester", tuple(pages.keys()))
    #page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")



    st.markdown(
        """
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#91a6c2,#91a6c2);
        color: black;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.sidebar.write("Inscrivez vous à notre newsletter et soyez informé des MAJ et actus du site")# Display the selected page
    rej = st.sidebar.button("Rejoindre la newsletter")
    
    st.sidebar.write("Rejoignez Why sur les réseaux sociaux")# Display the selected page
    go= st.sidebar.button("Partager ")

    if go :
        calculator('index.html')
        
        
    if rej :
        page_newletter()
    pages[page]()



def prediction(maladie):
    
    

    
    st.write(""" ### PREDICTIONS """)
    
    my_age = st.number_input("Quel âge avez-vous ?",6,105)
    st.write("Vous avez ",my_age, " ans")
    colonne1, colonne2 = st.beta_columns(2)
    with colonne1 :
        my_poids = int(st.number_input("Combien pesez-vous ?",10,200))
        st.write("Vous pesez ",my_poids, " kilos ")         
    with colonne2 :
        my_taille = int(st.number_input("Combien mesurez-vous ?",115,260))
        st.write("Vous mesurez ",my_taille, " cm ")
    IMC = (my_poids/((my_taille/100)**2))
    st.write("Votre IMC est de ",IMC)
    
    st.write( "Quels sont vos symptômes ?")         

    if (maladie == "Covid") :
        num_maladie = 0
        symptoms = st.multiselect(
            'Sélectionnez vos symptômes.',
            ['Difficultés pour respirer','Fièvre' ,'Toux sèche','Mal de gorge', 'Nez qui coule',
             'Asthme' , 'Maladie pulmonaire chronique' ,'Maux de tête', 'Maladie cardiaque', 'Diabète','HyperTension',
             'Fatigue', 'Gastro' 
             ,'Voyage à l\'étranger','Contact with COVID Patient',   'Présence dans des grands regroupements', 
             'Visite d\'endroits clôts','Famille travaillant dans des endroits exposés',
             'Port du masque'],
            [])
        
        if symptoms == []:
            st.write('')
        
        else :
            st.write('Vous avez sélectionné', len(symptoms),' symptômes :')
            
        listsymptomsref = ['Difficultés pour respirer','Fièvre' ,'Toux sèche','Mal de gorge', 'Nez qui coule',
             'Asthme' , 'Maladie pulmonaire chronique' ,'Maux de tête', 'Maladie cardiaque', 'Diabète','HyperTension',
             'Fatigue', 'Gastro' 
             ,'Voyage à l\'étranger','Contact with COVID Patient',   'Présence dans des grands regroupements', 
             'Visite d\'endroits clôts','Famille travaillant dans des endroits exposés',
             'Port du masque']
        
        listzero = [0,0,0,0,0 ,0, 0,0, 
            0, 0 ,0,0,0,0,0,0,0,0
             ,0]
    
        with open('RandFor_model.pkl', 'rb') as f:
            lgr = pickle.load(f)
    
    elif (maladie == "Diabete") :
        num_maladie = 1
        symptoms = st.multiselect(
            'Sélectionnez vos symptômes.',
            ['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss',
       'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
       'Itching', 'Irritability', 'delayed healing', 'partial paresis',
       'muscle stiffness', 'Alopecia', 'Obesity'],
            [])
        
        if symptoms == []:
            st.write('')
        
        else :
            st.write('Vous avez sélectionné', len(symptoms),' symptômes :')
            
        listsymptomsref = ['Age', 'Gender', 'Polyuria', 'Polydipsia', 'sudden weight loss',
       'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
       'Itching', 'Irritability', 'delayed healing', 'partial paresis',
       'muscle stiffness', 'Alopecia', 'Obesity']
        
        listzero = [0,0,0,0,0 ,0, 0,0, 
            0, 0 ,0,0,0,0,0,0]
    
        with open('RF_diabete.pkl', 'rb') as f:
            lgr = pickle.load(f)
    
    
   
        
    for i in range(len(symptoms)) :
        for w in listsymptomsref :
            if w == symptoms[i]:
                listzero[listsymptomsref.index(w)] =1 # on enregistre l'index de w 
                
    #creation des boutons acec le nom des symtpomes
    
    if len(symptoms)>=3 :
        taille =len(symptoms) 
        if (taille%3 !=0):
            taille = ((taille//3)+1)*3
        prematri = symptoms
        for i in range (taille-len(symptoms)):
            prematri.append(0)
        matri = np.array(prematri)   # tu dois gerer ca 
        matri = np.reshape(matri,(taille//3,3))         
        symptomsubliste1 = matri[:,0]
        symptomsubliste2 = matri[:,1]
        symptomsubliste3 = matri[:,2]   
                 
        col1, col2, col3= st.beta_columns(3)

        with col1 :
            for w in symptomsubliste1 :
                if w != '0':
                    st.button(str(w))
                
        with col2:
            for w in symptomsubliste2 :
                if w != '0':
                    st.button(str(w))
        with col3:
            for w in symptomsubliste3 :      
                if w != '0':
                    st.button(str(w))

                     
            

    else: 
        for w in symptoms :
            st.button(str(w))
           
       


    
    

    #with col2:

    #    st.button("Diabète")
    #    st.button("Nez qui coule")
        
 

    #with col1:
    #    st.button("Asthme")
    #    st.button("Mal de gorge")
    
    

        
    Predi = pd.DataFrame(listzero) 
    Predi = Predi.T
    result = lgr.predict(Predi)

        

    
    st.write("")
    st.write("")
    st.write("")
    st.write("")    
    col1, col2, col3, col4 = st.beta_columns(4)
    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.write("")  
    with col4:            
        grvdoc = st.button("C'est grave Doc ?")    
    if grvdoc :
        universel(finalip,my_poids,my_age,my_taille,symptoms)
        if result[0] == 1 :  
            global diagnostic
            diagnostic[num_maladie] = "Il semblerait que vous soyez positif au " + str(maladie)
            st.error(diagnostic[num_maladie])
        if result[0] == 0 :
            diagnostic[num_maladie] ="Il semblerait que vous soyez négatif au " + str(maladie)
            st.success(diagnostic[num_maladie])
        st.write(lgr.predict_proba(Predi))
        st.warning("Vous voulez informer vos amis de vos résultats ? Faîtes le sur le réseau de votre choix !")
        calculator('index.html')
        #communication avec js via un fihcier json mais aussi pour les conseils
        data = diagnostic
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)  
        print(data)

# nous contacter
def contact() :                
    creer_tablecontact()
    st.markdown("<h1 style='text-align: center; color: teal;'>Vous souhaitez nous contacter ?</h1>", unsafe_allow_html=True)
    
    mail = st.text_input("Votre email", "email@nomdomaine" )
    message = st.text_area("Votre message", "Dites-nous tout ! ")
    st.write("")
    okaysubmit = st.button("On envoie ?")
    if okaysubmit :
        vemail = mail
        vmessage = message
        ajouter_contact(vemail,vmessage)
        st.success("C'est envoyé !")
                
def page_home():

    st.markdown("<h1 style='text-align: center; color: crimson;'>Ask Why</h1>", unsafe_allow_html=True)
    
    #st.title("Ask Why")
    st.write("")
    
    # **Ask Why** est un outil basé sur du **Machine Learning**, il propose un diagnostic en ligne et gratuit de plusieurs maladies en quelques clics. Pour cela, il vous suffit d'indiquer vos différents symptômes et notre algorithme vous donnera sa prédiction.
    st.write(
            """
**Ask Why** est un algorithme basé sur du **Machine Learning**, il propose un diagnostic en ligne et gratuit de plusieurs maladies, pour cela il vous suffit d'indiquer vos différents symptômes.

 

 


**Les maladies diagnostiquées par Ask Why:**
    
- Diabète : [Description du diabete d'après l'OMS](https://www.who.int/fr/news-room/fact-sheets/detail/diabetes)

 

- Covid-19 : [Description du Covid-19 d'après l'OMS](https://www.who.int/fr/emergencies/diseases/novel-coronavirus-2019)

 

- Maladies cardiaques : [Description des maladies cardiaques d'après l'OMS](https://www.who.int/cardiovascular_diseases/fr/)
    """
        )
    
    
    image = Image.open('logo.png')

    st.image(image,use_column_width=True)

    st.write("")
    st.write(
                """
     **Attention** : Le diagnostic posé n'est pas le diagnostic d'un médecin et ne doit pas être vu comme tel. Si vous êtes identifié comme négatif à une maladie donnée, mais que vos doutes persistent nous vous conseillons vivement de procéder à une consultation pour en être persuadé.            
       
      """   )
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Afin de d'améliorer ses services, Ask Why stocke certaines données. Toutefois, si vous souhaitez supprimer vos données, il suffit d'appuyer sur ce bouton")
    rg = st.button("Supprimer mes données")
    if rg :
        rgpd()
        st.success("Vos données ont bien été supprimées !")
    
def page_first():
    st.markdown("<h1 style='text-align: center; color: black;'>Auto-diagnostic Covid-19</h1>", unsafe_allow_html=True)
    # ...
    maladie = "Covid"
    prediction(maladie)
     
def page_second():
    st.markdown("<h1 style='text-align: center; color: gray;'>Auto-diagnostic Diabète</h1>", unsafe_allow_html=True)
    # ...
    maladie = "Diabete"
    prediction(maladie)
def page_3():
    st.markdown("<h1 style='text-align: center; color: silver;'>Auto-diagnostic Maladie Cardiaque</h1>", unsafe_allow_html=True)
    # ...
def local_css(filename):
    with open(filename) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True) 
def page_4():
    st.markdown("<h1 style='text-align: center; color: lime;'>Conseils & Partenariats</h1>", unsafe_allow_html=True)
    #la suite c'était pour donner la couleur au background mais aussi mettre une recherche style google (pas besoin pour notre truc)
    
    #local_css("style.css")
    #remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')    
    #icon("search")
    #selected = st.text_input("", "Search")
    #button_clicked = st.button("OK")
    st.write(
            """
            Si vous êtes étudiant en Ile-de-France, Forest Hill propose une offre ultra intéressante sur ses salles de sports. Profitez-en en utilisant ce lien !
            [Partenariat Forest-Hill](https://www.forest-hill.fr/Formules)
"""
        )
    
    
    image = Image.open('Forest-Hill.jpg')

    st.image(image,use_column_width=True)
def page_5():
    contact()
    # ...


def page_6():
    st.markdown("<h1 style='text-align: center; color: navy;'>Admin</h1>", unsafe_allow_html=True)
    
    # ...

    id = st.text_input("Identifiant", "MohSaNat")
    modepass = st.text_input("Mot de passe", "root")
    submit = st.button("Vérifier")
    if submit :    
        if (id == admin) &(modepass == mdp):
             user_result = view_all_users()
             contact_tableau = voir_contact()
             clean_db = pd.DataFrame(user_result,columns=["age","ipadress","poids","date","Symptomes","date"])
             st.dataframe(clean_db)   
             st.write("")
             contakt_db = pd.DataFrame(contact_tableau,columns=["email","message","date"])
             st.dataframe(contakt_db)
             st.success("Hey Captain !")
        else : 
            st.error("Vous n'êtes pas admin")
    print(diagnostic)
#créer une newsletter/ notification pour les nouveaux ajouts de maladies / nouveaux partenanriats
def page_newletter():
    st.title("Rejoignez notre Newsletter")
    st.write("Inscrivez-vous à notre newsletter et soyez informé des MAJ, des actus du site et plus encore")
    newsmail = st.text_input("", "Votre email")
    okaysubmit = st.button("Rejoindre")
    if okaysubmit :
        st.success("Bienvenue !")
    print(newsmail)

if __name__ == "__main__":
    main()
    




