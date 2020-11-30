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
#import webbrowser
from ip2geotools.databases.noncommercial import DbIpCity
from cryptography.fernet import Fernet
from re import escape 
file = open("data.json","r+")
file. truncate(0)
file. close()
encryption = True
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
def calculator(calc_html,width=720,height=325):
	calc_file = codecs.open(calc_html,'r')
	page = calc_file.read()
	components.html(page,width=width,height=height,scrolling=False)

#		components.html(html_temp)

# DB Management

def write():
    with st.spinner("Loading Home ..."):
        ast.shared.components.title_awesome("")

 #Security
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
crypt = sqlite3.connect('info_user_crypted.db')

cr = crypt.cursor()

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
    if encryption == True :
        cr.execute('CREATE TABLE IF NOT EXISTS userstable(age TEXT, ipadress TEXT,poids TEXT,taille TEXT,Symptomes TXT, date TXT)')
    else :
        c.execute('CREATE TABLE IF NOT EXISTS userstable(age INT, ipadress TEXT,poids INT,taille INT,Symptomes TXT, date TXT)')    

def add_userdata(age,ipadress,poids,taille,symptomes):
    date = str(datetime.now())
    if encryption == True :
        cr.execute('INSERT INTO userstable(age,ipadress,poids,taille,date,Symptomes) VALUES (?,?,?,?,?,?)',(age,ipadress,poids,taille,date,symptomes))
        crypt.commit()
    else :
        c.execute('INSERT INTO userstable(age,ipadress,poids,taille,date,Symptomes) VALUES (?,?,?,?,?,?)',(age,ipadress,poids,taille,date,symptomes))
        conn.commit()

def voir_contact():
    k.execute('SELECT * FROM Kontakt')
    data2 = k.fetchall()
    return data2

def view_all_users():
    if encryption == True :
        cr.execute('SELECT * FROM userstable')
        data = cr.fetchall()
    else :
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
        "Maladie cardiovasculaire": page_3,
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
        calculator('indextestpartage.html')

        
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
    st.write('Un IMC normal est situé entre 18,5 et 25' )
    if (IMC >= 18.5 ) and (IMC<=25):
        z = "Votre IMC est de " + str(IMC)
        st.success(z)
    else :
        z = "Votre IMC est de " + str(IMC)
        st.error(z)
    
    st.write( "Quels sont vos symptômes ?")         
    if (maladie == "Covid") :
        num_maladie = 0
        symptoms = st.multiselect(
            'Sélectionnez vos symptômes.',
            ['Difficultés pour respirer','Fièvre' ,'Toux sèche','Mal de gorge', 'Nez qui coule',
             'Asthme' , 'Maladie pulmonaire chronique' ,'Maux de tête', 'Maladie cardiovasculaire', 'Diabète','Hypertension',
             'Fatigue', 'Gastro-entérite' 
             ,'Voyage à l\'étranger','Contact avec des patients Covid',   'Présence dans des grands regroupements', 
             'Visite d\'endroits clôts','Famille travaillant dans des endroits exposés',
             'Port du masque'],
            [])
        
        if symptoms == []:
            st.write('')
        
        else :
            st.write('Vous avez sélectionné', len(symptoms),' symptômes :')
            
        listsymptomsref = ['Difficultés pour respirer','Fièvre' ,'Toux sèche','Mal de gorge', 'Nez qui coule',
             'Asthme' , 'Maladie pulmonaire chronique' ,'Maux de tête', 'Maladie cardiovasculaire', 'Diabète','Hypertension',
             'Fatigue', 'Gastro-entérite' 
             ,'Voyage à l\'étranger','Contact avec des patients Covid',   'Présence dans des grands regroupements', 
             'Visite d\'endroits clôts','Famille travaillant dans des endroits exposés',
             'Port du masque']
        
        listzero = [0,0,0,0,0 ,0, 0,0, 
            0, 0 ,0,0,0,0,0,0,0,0
             ,0]
    
        with open('RandFor_model.pkl', 'rb') as f:
            lgr = pickle.load(f)
    
    elif (maladie == "Diabete") :
        num_maladie = 1
        genre = st.radio("Vous êtes :",('une femme' ,'un homme' ))            
        symptoms = st.multiselect(
            'Sélectionnez vos symptômes.',
            ['Urines abondantes(polyurie)', 'Soif excessive(polydipsie)', 'Perte de poids soudaine',
       'Faiblesse', 'Faim excessive(polyphagie)', 'Mycose génitale', 'Vision floue',
       'Démangeaisons', 'Irritabilité', 'Cicatrisation lente', 'Parésie (paralysie partielle)',
       'Rigidité musculaire', 'Alopécie', 'Obésité'],
            [])
        
        if symptoms == []:
            st.write('')
        
        else :
            st.write('Vous avez sélectionné', len(symptoms),' symptômes :')
            
        listsymptomsref = ['Urines abondantes(polyurie)', 'Soif excessive(polydipsie)', 'Perte de poids soudaine',
       'Faiblesse', 'Faim excessive(polyphagie)', 'Mycose génitale', 'Vision floue',
       'Démangeaisons', 'Irritabilité', 'Cicatrisation lente', 'Parésie (paralysie partielle)',
       'Rigidité musculaire', 'Alopécie', 'Obésité']
        
        listzero = [0,0,0 ,0, 0,0, 
            0, 0 ,0,0,0,0,0,0]
    
        with open('RF_diabete.pkl', 'rb') as f:
            lgr = pickle.load(f)
        agegenre = [my_age]    
        if genre == 'un homme' :
            agegenre = agegenre + [1]
        else :
            agegenre = agegenre + [0]
  
    elif (maladie == "Maladie_cardiovasculaire") :
        num_maladie = 2
        genre = st.radio("Vous êtes :",('une femme' ,'un homme'))
        symptoms = st.multiselect(
            'Sélectionnez vos symptômes.',
        ['Fumeur de cigarette','Fumeur d\'autres produits à base de tabac' ,'Hypertension','Obésité', 'Diabète',
         'Syndrôme métabolique' , 'Utilisation de produits dopants ou de drogues stimulantes' ,'Antécédents cardiaques familiaux' 
         ,'Antécedents de pré-éclampsie', 'Antécédents de pontage coronarien','Maladies respiratoires'],[])

        
        if symptoms == []:
            st.write('')
        
        else :
            if len(symptoms) ==1 :
                st.write('Vous avez sélectionné', len(symptoms),' symptôme :')
            else :
                st.write('Vous avez sélectionné', len(symptoms),' symptômes :')
            
            
        listsymptomsref = ['Fumeur de cigarette','Fumeur d\'autres produits à base de tabac' ,'Hypertension','Obésité', 'Diabète',
         'Syndrôme métabolique' , 'Utilisation de produits dopants ou de drogues stimulantes' ,'Antécédents cardiaques familiaux' 
         ,'Antécedents de pré-éclampsie', 'Antécédents de pontage coronarien','Maladies respiratoires']
        
        listzero = [0,0,0,0,0,0,0,0,0,0,0]
    
        with open('RF_cardiacpart1.pkl', 'rb') as f:
            lgr = pickle.load(f)   
        if genre == 'un homme' :
            listzero = [1] + listzero
        else :
            listzero =  [2] + listzero 
        
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
    
    

    if (maladie ==  "Diabete") :
        listzero = agegenre + listzero
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
        if encryption == True :
            
            ipfinale = encrypt_message(finalip)
            my_poidsf = encrypt_message(my_poids)
            my_agef = encrypt_message(my_age)
            my_taillef = encrypt_message(my_taille)
            symptomsf = encrypt_message(symptoms)                                
        else :
            ipfinale = finalip 
        universel(ipfinale,my_poidsf,my_agef,my_taillef,symptomsf)
        if result[0] == 1 :  
            global diagnostic
            diagnostic[num_maladie] = "Il semblerait que vous soyez positif au " + str(maladie)
            st.error(diagnostic[num_maladie])
            st.write("Nous vous conseillons le diagnostic d'un vrai médecin")
            prenezrendez = " [**Prenez un rendez-vous près de chez vous avec Doctolib**](" + doctolib(maladie) +")"
            st.write(prenezrendez)
        if result[0] == 0 :
            diagnostic[num_maladie] ="Il semblerait que vous soyez négatif au " + str(maladie)
            st.success(diagnostic[num_maladie])
            st.write("Vous demeurez inquiet malgré cet avis?")
            prenezrendez = " [**Prenez un rendez-vous près de chez vous avec Doctolib**](" + doctolib(maladie) +")"
            st.write(prenezrendez)
        #st.write(lgr.predict_proba(Predi)) 
        with st.beta_expander("Détails de l'auto-diagnostic"):
            affichergras = '**' +'Risques de '+ str(maladie) + '**'
            st.write(affichergras)
            st.write(""" 
             Cette figure vous montre l'importance relative de chacun des symptômes dans notre prédiction.
         """)
            if maladie == "Diabete" :
                impor_varia = "importances_variablesDiabete.png"
            elif maladie == "Covid":
                impor_varia= "importances_variablesCovid.png"
            elif maladie == "Maladie_cardiovasculaire" :
                impor_varia = "importances_variables.png"
            image = Image.open(impor_varia)
            st.image(image,use_column_width=True)
            if len(symptoms) ==1 :
                st.write('Vous avez sélectionné le symptôme : ') 
            else :
                st.write('Vous avez sélectionné les symptômes : ')
            for i in symptoms :
                correspondance = str(i) + ' qui a une importance de ' + str(importance_sympt(i,maladie,symptoms,listsymptomsref))
                st.write(correspondance)
            st.write("""**Autres risques**""")
            if (IMC>=25):
                st.write("""Nous avons remarqué un IMC anormal. Le poids est un **facteur de risques** pour un grand nombre de **maladies graves**. 
                         Ainsi nous vous encourageons à la **pratique du sport** et à une **alimentation plus saine**. Nos partenaires Forest Hill et CopperBranch proposent des offres qui pourrait grandement vous 
                         intéresser, n'hésitez pas à faire un tour dans notre rubrique ***Conseils&Partenariats***  """)
                st.write('')
            elif risquespoids(symptoms) : 
                st.write("""Nous avons remarqué que vous êtes atteint d'obésité. Or le poids est un **facteur de risques** pour un grand nombre de **maladie**. 
                         Ainsi nous vous encourageons à la **pratique du sport** et à une **alimentation plus saine**. Nos partenaires Forest Hill et CopperBranch proposent des offres qui pourrait grandement vous 
                         intéresser, n'hésitez pas à faire un tour dans notre rubrique ***Conseils&Partenariats***""")
                st.write('')
            
            if risquesfumeur(symptoms) : 
                st.write("""Nous avons remarqué que vous êtes fumeur. Or fumer est un **facteur de risques** pour un grand nombre de **maladies graves**. 
                         Ainsi nous vous encourageons à **arrêter de fumer**. Notre partenaire Assurance Maladie propose une aide qui pourrait grandement vous 
                         intéresser, n'hésitez pas à faire un tour dans notre rubrique ***Conseils&Partenariats***""")
            st.write('')
            
        st.warning("Vous voulez informer vos amis de vos résultats ? Faîtes le sur le réseau de votre choix !")
        calculator('indextestpartage.html')
        # creatio dun fihcier json pour la communication pyhton -js via. On peut aussi en creer un pour les conseils
        #data = diagnostic
        #with open('data.json', 'w') as outfile:
        #    json.dump(data, outfile)  
        #print(data)
        
            

# nous contacter
def contact() :                
    creer_tablecontact()
    st.markdown("<h1 style='text-align: center; color: teal;'>Vous souhaitez nous contacter ?</h1>", unsafe_allow_html=True)
    
    mail = escape(st.text_input("Votre email", "email@nomdomaine" ))
    message = escape(st.text_area("Votre message", "Dites-nous tout ! "))
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
    st.write("Afin d'améliorer ses services, Ask Why stocke certaines données. Toutefois, si vous souhaitez supprimer vos données, il suffit d'appuyer sur ce bouton")
    rg = st.button("Supprimer mes données")
    if rg :
        rgpd()
        st.success("Vos données ont bien été supprimées !")
    
def page_first():
    st.markdown("<h1 style='text-align: center; color: black;'>Auto-diagnostic : Covid-19</h1>", unsafe_allow_html=True)
    # ...
    maladie = "Covid"
    prediction(maladie)
     
def page_second():
    st.markdown("<h1 style='text-align: center; color: gray;'>Auto-diagnostic : Diabète</h1>", unsafe_allow_html=True)
    # ...
    maladie = "Diabete"
    prediction(maladie)
def page_3():
    st.markdown("<h1 style='text-align: center; color: silver;'>Auto-diagnostic : Maladie cardiovasculaire</h1>", unsafe_allow_html=True)
    maladie = "Maladie_cardiovasculaire"
    prediction(maladie)
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
    #sport forest hill
    st.info("Why bénéficie d'un large réseau de partenaires et de nombreuses offres sur des produits qui pourront vous aider à vivre sainement et en harmonie avec votre corps.")
    
    st.write(""" #**Faire du sport** """)
    st.write(
            """
            Si vous êtes étudiant en Ile-de-France, Forest Hill propose une offre ultra intéressante sur ses salles de sports. Profitez-en en utilisant ce lien !
            [Partenariat Forest-Hill](https://www.forest-hill.fr/Formules)
"""
        )
    
    
    image = Image.open('Forest-Hill.jpg')

    st.image(image,use_column_width=True)
    st.write('')
    #bioburger
    st.write(""" #**Manger sainement** """)
    st.write(
            """
            Vous êtes un bon vivant et voulait le rester tout en mangeant de délicieux burger? Profitez de notre partenariat avec Bioburger! 
            [Partenariat Bioburger](https://www.bioburger.fr/menu/)
"""
        )
    
    
    image = Image.open('bioburger.jpg')
    st.image(image,use_column_width=True)
    st.write('')
    #copperbranch 
    st.write(""" #**Manger sainement et végé** """)
    st.write(
            """
            Vous êtes un bon vivant et voulait le rester tout en mangeant healthy? Profitez de notre partenariat avec CopperBranch! 
            [Partenariat CopperBranch](https://copperbranch.fr/menu/)
"""
        )
    
    
    image = Image.open('copperbranch.jpg')
    st.image(image,use_column_width=True)
    st.write('')
    st.write(""" #**Arrêter de fumer** """)
    st.write(
            """
                    [Partenariat Assurance Maladie](https://play.google.com/store/apps/details?id=fr.cnamts.tis&hl=fr)
"""
        )
    
    
    image = Image.open('stoptabacversion.jpg')
    st.image(image,use_column_width=True)
    st.write('')
    
def page_5():
    contact()
    # ...


def page_6():
    st.markdown("<h1 style='text-align: center; color: navy;'>Admin</h1>", unsafe_allow_html=True)
    
    # ...

    id = escape(st.text_input("Identifiant", ""))
    modepass = escape(st.text_input("Mot de passe", type="password"))
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
    #print(diagnostic)
#créer une newsletter/ notification pour les nouveaux ajouts de maladies / nouveaux partenanriats
def page_newletter():
    st.title("Rejoignez notre Newsletter")
    st.write("Inscrivez-vous à notre newsletter et soyez informé des MAJ, des actus du site et plus encore")
    newsmail = escape(st.text_input("", "Votre email"))
    okaysubmit = st.button("Rejoindre")
    if okaysubmit :
        st.success("Bienvenue !")
    print(newsmail)


def risquespoids(list):
    for i in list:
        if i == 'Obésité' :
            return True 
    return False   
def risquesfumeur(list):
    for i in list:
        if i == 'Fumeur de cigarette' or i =='Fumeur d\'autres produits à base de tabac':
            return True 
    return False     

def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = str(message).encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return(decrypted_message.decode())

def doctolib(maladie):
    url = 'https://www.doctolib.fr/' 
    response = DbIpCity.get(finalip, api_key='free')
    ville = (response.city).lower()
         
    if maladie == 'Covid' : 
        mala = 'depistage-covid-19-antigenique/'
        url = url + mala + ville
    elif maladie == 'Diabete' : 
        mala = 'endocrinologue/'
        url = url + mala + ville
    elif maladie == 'Maladie_cardiovasculaire' : 
        mala = 'cardiologue/'
        url = url + mala + ville
    return(url)
#    webbrowser.open(url, new=0, autoraise=True)
def importance_sympt(i,maladie,symptoms,listsymptomsref): 
    if maladie =='Covid':
        listref =  listsymptomsref
        imp =[1.72809381e-01, 6.89347967e-02, 1.80658331e-01, 2.38706877e-01,
       2.58662583e-04, 1.29277606e-03, 4.01682212e-04, 7.33057330e-05,
       1.05832702e-03, 2.30918543e-04, 3.90299744e-03, 2.98444113e-05,
       1.33384154e-04, 1.64637709e-01, 5.92551239e-02, 9.70373326e-02,
       3.46950973e-03, 7.10904115e-03, 0.00000000e+00]
    elif maladie == 'Diabete' :
        listref = ['Age>= 40 ans','Etre un homme','Urines abondantes(polyurie)', 'Soif excessive(polydipsie)', 'Perte de poids soudaine',
       'Faiblesse', 'Faim excessive(polyphagie)', 'Mycose génitale', 'Vision floue',
       'Démangeaison', 'Irritabilité', 'Cicatrisation lente', 'Parésie (paralysie partielle)',
       'Rigidité musculaire', 'Alopécie', 'Obésité']
        
        imp =  [0.09774926, 0.10490779, 0.21851173, 0.18322141, 0.06531913,
       0.0200777 , 0.0355011 , 0.01981826, 0.02829822, 0.02653362,
       0.03839536, 0.03080899, 0.04593732, 0.0266845 , 0.03823258,
       0.02000303]
    elif maladie == 'Maladie_cardiovasculaire' : 
        imp = [0.14825714, 0.28269378, 0.00829022, 0.17628417, 0.00841144,
           0.00216457, 0.04985012, 0.00410238, 0.23470564, 0.02176112,
           0.05013109, 0.01334832]
        listref = ['Etre un homme','Fumeur de cigarette','Fumeur d\'autres produits à base de tabac' ,'Hypertension','Obésité', 'Diabète',
         'Syndrôme métabolique' , 'Utilisation de produits dopants ou de drogues stimulantes' ,'Antécédents cardiaques familiaux' 
         ,'Antécedents de pré-éclampsie', 'Antécédents de pontage coronarien','Maladies respiratoires']
    for w in listref :
        if w == i :
            return imp[listref.index(w)]


if __name__ == "__main__":
    main()
    




