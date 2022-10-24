# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:19:01 2022

@author: m.jacoupy
"""


# #######################################################################################################################
#                                              # === LIBRAIRIES === #
# #######################################################################################################################
import cv2
import os
import matplotlib.pyplot as plt
import hashlib
import numpy as np
import unidecode
from PIL import Image, ImageFont, ImageDraw
import streamlit as st

# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################

#import de l'image
def import_dossard2(path, image):
    dossard = cv2.imread(os.path.join(path, image))
    plt.imshow(cv2.cvtColor(dossard, cv2.COLOR_BGR2RGB))
    return dossard

def import_image(image, title_font_name, title_font_number, title_font_course, firstname, doss_nb, course):
    my_image = image
    name_text = firstname
    course_text = course
    number_text = str(doss_nb)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((15,75), name_text, (0, 0, 0), font=title_font_name)
    image_editable.text((440,350), number_text, (0, 0, 0), font=title_font_number)
    image_editable.text((1025,200), course_text, (0, 0, 0), font=title_font_course)
    return my_image
   
# Création de l'empreinte SHA512 (128 caractères héxadécimaux)
def sha512_footprint_generation(firstname, lastname):
    # Créé la chaine de caractères en entrée
    entry = (firstname+lastname).encode('utf-8')
    # Transforme la chaine de caractères en 128 valeurs hexadecimales
    footprint = hashlib.sha512(entry).hexdigest()   
    return footprint

# Transformation de l'empreinte en nombres decimaux (deux caractères donnent un chiffre entre 0 et 255)
def hexadecimal_to_decical(footprint, size):
    decimal_nb = ""
    for iCharacter in np.arange(0, len(footprint), 2):
        doublet_hex = footprint[iCharacter:iCharacter+2]
        doublet_dec = str(int(doublet_hex, 16))
        decimal_nb += doublet_dec
    return decimal_nb[0:size]

# Création du nombre ID_PNMN sur la base du nom complet, du prénom complet, de la date de naissance, du genre et d'un sel.
def dossard_number_generator(firstname, lastname, size):
    # Créé la valeur en hexadécimale
    footprint = sha512_footprint_generation(firstname, lastname)
    # Transforme la valeur d'hexadecimale en décimale 
    number = hexadecimal_to_decical(footprint, size)
    return number    

def pil_to_string(img):
    open_cv_image = np.array(img) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    img_str = cv2.imencode('.jpg', open_cv_image)[1].tostring()
    return img_str

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.123freevectors.com/yellow-and-white-polygon-background-graphic-design-illustration-131833/");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
 
# #######################################################################################################################
#                                              # === CONSTANTES === #
# #######################################################################################################################

title_font_name = ImageFont.truetype("font/Agane.ttf", 100)
title_font_number = ImageFont.truetype("font/Agane.ttf", 200)
title_font_course = ImageFont.truetype("font/Agane.ttf", 35)

model = Image.open("images/Modele.jpg")
logos = Image.open("images/Logos.png")

# #######################################################################################################################
#                                              # === STREAMLIT === #
# #######################################################################################################################
add_bg_from_url() 


st.title("La PiEdTHONe 2022")
st.header("Génération du dossard")
st.markdown("""---""")

st.sidebar.image(logos)


col1, col2 = st.columns([1,1])
with col1:
    firstname = st.text_input(label="Prénom ou Pseudo") 
    lastname = st.text_input(label="Nom de famille*")
    
with col2:    
    course = st.selectbox('Selection de la distance', ['Distance 2 kms', 'Distance 4 kms', 'Distance 6 kms', 'Distance 10 kms'], index=0)
    
st.warning("*Le nom de famille sert uniquement à la génération du numéro personnel. L'information n'est ni stockée ni conservée.")

    
doss_nb = dossard_number_generator(firstname = str(unidecode.unidecode(firstname).lower()),  
                          lastname = str(unidecode.unidecode(lastname).lower()), 
                          size = 4)

personnalized_dossard = import_image(model, 
                                     title_font_name, 
                                     title_font_number, 
                                     title_font_course, 
                                     firstname, 
                                     doss_nb,
                                     course)
with st.expander("Voir un apperçu du dossard"):
    st.image(personnalized_dossard)

btn = st.download_button(
        label="Télécharger le dossard",
        data=pil_to_string(personnalized_dossard),
        file_name=firstname+"-dossard-piedthone-2022.jpg",
        mime="image/jpg"
      )
