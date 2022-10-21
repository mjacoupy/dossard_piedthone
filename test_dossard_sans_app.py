# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 21:33:58 2022

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

# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################

#import de l'image
def import_dossard2(path, image):
    dossard = cv2.imread(os.path.join(path, image))
    plt.imshow(cv2.cvtColor(dossard, cv2.COLOR_BGR2RGB))
    return dossard

def import_image(full_path, title_font_name, title_font_number, title_font_course, firstname, doss_nb, course):
    my_image = Image.open(full_path)
    name_text = firstname
    course_text = course
    number_text = str(doss_nb)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((15,60), name_text, (0, 0, 0), font=title_font_name)
    image_editable.text((370,375), number_text, (0, 0, 0), font=title_font_number)
    image_editable.text((475,300), course_text, (0, 0, 0), font=title_font_course)
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
  
# #######################################################################################################################
#                                              # === CONSTANTES === #
# #######################################################################################################################

full_path = r"C:\Users\m.jacoupy\OneDrive - Institut\Documents\3 - Developpements informatiques\dossard_piedthone\modele.jpg"
title_font_name = ImageFont.truetype(r"C:\Users\m.jacoupy\OneDrive - Institut\Documents\3 - Developpements informatiques\dossard_piedthone\Agane.ttf", 100)
title_font_number = ImageFont.truetype(r"C:\Users\m.jacoupy\OneDrive - Institut\Documents\3 - Developpements informatiques\dossard_piedthone\Agane.ttf", 175)
title_font_course = ImageFont.truetype(r"C:\Users\m.jacoupy\OneDrive - Institut\Documents\3 - Developpements informatiques\dossard_piedthone\Agane.ttf", 35)


firstname = "Stephane"
lastname = "Vasseur"
course = "10 kms"

# #######################################################################################################################
#                                              # === CODE === #
# #######################################################################################################################

doss_nb = dossard_number_generator(firstname = str(unidecode.unidecode(firstname).lower()),  
                          lastname = str(unidecode.unidecode(lastname).lower()), 
                          size = 4)

personnalized_dossard = import_image(full_path, 
                                     title_font_name, 
                                     title_font_number, 
                                     title_font_course, 
                                     firstname, 
                                     doss_nb,
                                     course)
personnalized_dossard.show()

# #######################################################################################################################
#                                              # === STREAMLIT === #
# #######################################################################################################################

