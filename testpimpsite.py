# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:12:13 2020

@author: Haddoune
"""
import hashlib
import pandas as pd
import streamlit as st
import awesome_streamlit as ast
from PIL import Image
import numpy as np
import pickle 
import requests
from bs4 import BeautifulSoup


admin = "MohSaNat"
mdp = "root"

requete = requests.get("https://api.ipify.org/")
page = requete.content
soup = BeautifulSoup(page,features="lxml")
soup =str(soup)
sip = soup.split("<html><body><p>")
ip = sip[1].split("</p></body></html>")
finalip = ip[0]


# DB Management

def write():
    with st.spinner("Loading Home ..."):
        ast.shared.components.title_awesome("")

# Security
#passlib,hashlib,bcrypt,scrypt

def make_hashes(poids):
	return hashlib.sha256(str.encode(poids)).hexdigest()

def check_hashes(poids,hashed_text):
	if make_hashes(poids) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('tesdatabase.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(age INT, ipadress TEXT,poids INT)')


def add_userdata(age,ipadress,poids):
	c.execute('INSERT INTO userstable(age,ipadress,poids) VALUES (?,?,?)',(age,ipadress,poids))
	conn.commit()



def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
#cree toi meme  un identifiant et un mot de passe intra code histoire de creer un admin et avec ça t'as accès a la focntion view_all_users()



def universel(finalip,my_poids,my_age) :
    ipadress = finalip
    poids = my_poids
    age = my_age
    
    create_usertable()
    hashed_pswd = make_hashes(ipadress)
    add_userdata(age,hashed_pswd,poids)
def main():
    # Register your pages
    pages = {
        "Home" : page_home  ,  
        "Covid-19": page_first,
        "Diabète": page_second,
        "New 3 Maladie": page_3,
        "New 4 Maladie": page_4,
        "Admin": page_5,
        
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

    # Display the selected page
    pages[page]()


def prediction(maladie):
    
    

    
    st.write(""" ### PREDICTIONS """)
    
    my_age = st.number_input("Quel âge avez-vous ?",6,105)
    st.write("Vous avez ",my_age, " ans") 
    my_poids = st.number_input("Combien pesez-vous ?",10,200)
    st.write("Vous pesez ",my_poids, " kilos ")         
    st.write( "Quels sont vos symptômes ?")         

    if (maladie == "Covid") :

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
        universel(finalip,my_poids,my_age)
        if result[0] == 1 :
            a = "Il semblerait que vous soyez positif"
            st.error(a)
        if result[0] == 0 :
            a ="Il semblerait que vous soyez négatif"
            st.success(a)
    
    #pour voir notre database


def local_css(filename):
    with open(filename) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
    
def page_home():
    
    st.title("Ask Why")
   
    
    # ...
    st.write(
            """
**Ask Why** est un algorithme basé sur du **machine learning**, il propose un diagnostique du  cororona-virus en ligne et gratuit, pour cela il vous suffit d'indiquer vos différents symptomes. **Attention** si vous êtes identifié comme négatif au corona-virus nous vous  conseillons vivement de procéder à un test pour en être persuader.            

 

 


**Les maladies diagnostiquées par Ask Why:**
    
- Description du [Diabete](https://www.who.int/fr/news-room/fact-sheets/detail/diabetes) d'après l'OMS

 

- Description du  [Covid-19](https://www.who.int/fr/emergencies/diseases/novel-coronavirus-2019) d'après l'OMS
    """
        )
    
    
    image = Image.open('logo.png')

 

    st.image(image,use_column_width=True)
    

    
def page_first():
    st.title("Auto-diagnostic Covid-19")
    # ...
    maladie = "Covid"
    prediction(maladie)
     
def page_second():
    st.title("Auto-diagnostic Diabète")
    # ...
    maladie = "Diabete"
    prediction(maladie)
def page_3():
    st.title("Auto-diagnostic Maladie Cardiaque")
    # ...
    
def page_4():
    st.title("Auto-diagnostic New 4 Maladie")
    # ...


    
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    
    icon("search")
    selected = st.text_input("", "Search")
    button_clicked = st.button("OK")

def page_5():
    st.title("Admin")
    # ...

    id = st.text_input("", "Identifiant")
    modepass = st.text_input("", "Mot de passe")
    submit = st.button("submit")
    if submit :    
        if (id == admin) &(modepass == mdp):
             user_result = view_all_users()
             clean_db = pd.DataFrame(user_result,columns=["age","ipadress","poids"])
             st.dataframe(clean_db)   
        else : 
            st.error("Vous n'êtes pas admin")





if __name__ == "__main__":
    main()
    




