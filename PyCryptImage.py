# -*- coding: utf-8 -*-
# Auteur : Alexandre l'Heritier
print("----------------------------------------------------------------------")
print("PyCryptImage v1.1")
print("----------------------------------------------------------------------")

from tkinter import *
from PIL import Image
import time
import threading

global att
att = 0

def verif(couleur):
	a = 0
	while a == 0:
		if couleur >= 256:
			couleur -= 256
		if couleur <= -1:
			couleur += 256
		if couleur <= 255 and couleur >= 0:
			a = 1
	return couleur

def lettre(couleur, pos_lettre, mot, cryptede):
	taille_mot = len(mot)
	pos_lettre *= 3
	if couleur == "rouge":
		pos_lettre -= 3
	elif couleur == "vert":
		pos_lettre -= 2
	else:
		pos_lettre -= 1
	ar = 0
	pos_temp = pos_lettre
	while ar == 0:
		if pos_temp >= taille_mot:
			pos_temp -= taille_mot
		else:
			lettre_code = mot[pos_temp]
			ar = 1
	if int(pos_lettre / 2) == pos_lettre / 2:
		# Decode 1 code 0
		if cryptede == 0:
			plus_moins = 0
		else:
			plus_moins = 1
	else:
		if cryptede == 0:
			plus_moins = 1
		else:
			plus_moins = 0
	return (lettre_code, taille_mot, plus_moins)

def crypte(pixel, pos_lettre, mot, cryptede):
	rouge = pixel[0]
	vert = pixel[1]
	bleu = pixel[2]
	(lettre_code, taille_mot, plus_moins) = lettre(rouge, pos_lettre, mot, cryptede)
	chilet = ord(lettre_code)
	if plus_moins == 0:
		if cryptede == 0:
			chilet += taille_mot
		else:
			chilet -= taille_mot
		rouge += chilet
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		rouge -= chilet
	rouge = verif(rouge)
	(lettre_code, taille_mot, plus_moins) = lettre(vert, pos_lettre, mot, cryptede)
	chilet = ord(lettre_code)
	if plus_moins == 0:
		if cryptede == 0:
			chilet += taille_mot
		else:
			chilet -= taille_mot
		vert += chilet
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		vert -= chilet
	vert = verif(vert)

	(lettre_code, taille_mot, plus_moins) = lettre(bleu, pos_lettre, mot, cryptede)
	chilet = ord(lettre_code)
	if plus_moins == 0:
		if cryptede == 0:
			chilet += taille_mot
		else:
			chilet -= taille_mot
		bleu += chilet
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		bleu -= chilet
	bleu = verif(bleu)

	return (rouge, vert, bleu)

def cache(im1:Image, im2:Image, mot_cle, cryptede, num_image, image_total)->None:
	global et_4
	global et_5
	nb_tour = 1
	(largeur1, hauteur1) = (im1.width, im1.height)
	total = largeur1 * hauteur1
	pour22 = 1 / image_total
	for i in range(hauteur1):
		for e in range(largeur1):
			try:
				triplet1 = list(im1.getpixel((e, i)))
			except TypeError:
				triplet1 = im1.getpixel((e, i))
				triplet1 = [triplet1, triplet1, triplet1]
			tripletbi1 = crypte(triplet1, nb_tour, mot_cle, cryptede)
			im2.putpixel((e, i), tripletbi1)

			pour11 = nb_tour / total * 100
			pour1 = str(int(pour11)) + "%" + " " + "("+str(nb_tour)+"/"+str(total)+")"
			et_4.config(text=pour1)

			pour23 = pour11 * pour22
			if num_image >= 1:
				pour21 = pour22*100 + pour23
			else:
				pour21 = pour23
			pour2 = str(int(pour21)) + "%" + " " + "("+str(num_image)+"/"+str(image_total)+")"
			et_5.config(text=pour2)

			nb_tour += 1
	et_4.config(text=pour1)

def retrouver_image(mot_cle, cryptede, nom_image_base, num_image, image_total):
	global plus1
	if cryptede == 0:
		if plus1 == 1:
			nom_image_trouve = nom_image_base + "_crypte.jpg"
			nom_image_base = nom_image_base + ".jpg"
		else:
			nom_image_trouve = nom_image_base + "_crypte.png"
			nom_image_base = nom_image_base + ".png"
	else:
		if plus1 == 1:
			nom_image_trouve = nom_image_base + "_decrypte.jpg"
			nom_image_base = nom_image_base + ".jpg"
		else:
			nom_image_trouve = nom_image_base + "_decrypte.png"
			nom_image_base = nom_image_base + ".png"
	im1 = Image.open(nom_image_base)
	(largeur1, hauteur1) = (im1.width, im1.height)
	im2 = Image.new('RGB', (largeur1,hauteur1), (255,255,255))
	cache(im1, im2, mot_cle, cryptede, num_image, image_total)
	if plus1 == 1:
		im2.save(nom_image_trouve, "JPG")
	else:
		im2.save(nom_image_trouve, "PNG")

def command_crypter():
	global texte
	global mot
	immage = texte.get()
	mot_cle = mot.get()
	immage = immage.split(";")
	for i in range(len(immage)):
		retrouver_image(mot_cle, 0, immage[i], i, len(immage))

def command_decrypter():
	global texte
	global mot
	immage = texte.get()
	mot_cle = mot.get()
	immage = immage.split(";")
	for i in range(len(immage)):
		retrouver_image(mot_cle, 1, immage[i], i, len(immage))

def attente(a):
	global att
	while att == 0:
		pass
	if att == 1:
		command_crypter()
	else:
		command_decrypter()
	if att == 3:
		pass
	else:
		att = 0
		attente(a)

def a_propos():
	fenetre2 = Tk()
	fenetre2.title("A propos")
	Label(fenetre2, text = "PyCryptImage", font=('Arial', 20, 'italic', 'bold')).grid(row=0, column=0, columnspan=10)
	Label(fenetre2, text = "Par Alexandre l'Heritier").grid(row=1, column=0, columnspan=10)

def aide():
	fenetre1 = Tk()
	fenetre1.title("Aide")
	Label(fenetre1, text = "Pour mettre des images, mettre les images à crypter/décrypter").grid(row=0, column=0, columnspan=10)
	Label(fenetre1, text = "dans le même dossier que le programme, entrer les noms sans").grid(row=1, column=0, columnspan=10)
	Label(fenetre1, text = "leurs extentions (exemple : si vous avez une image avec un nom").grid(row=2, column=0, columnspan=10)
	Label(fenetre1, text = "comme Fleur.png, entrer juste Fleur et cocher .png).").grid(row=3, column=0, columnspan=10)
	Label(fenetre1, text = "Pour mettre plusieurs images d'un coup, séparer les noms avec").grid(row=4, column=0, columnspan=10)
	Label(fenetre1, text = "des points-virgules (exemple : Fleur;Voiture;Arbre).").grid(row=5, column=0, columnspan=10)
	Label(fenetre1, text = "Les images cryptées serons mises dans le même dossier avec").grid(row=6, column=0, columnspan=10)
	Label(fenetre1, text = "un nom contenant _crypte (exemple : Fleur deviendra Fleur_crypte).").grid(row=7, column=0, columnspan=10)
	Label(fenetre1, text = "Les images décryptées serons mises dans le même dossier avec").grid(row=8, column=0, columnspan=10)
	Label(fenetre1, text = "un nom contenant _decrypte (exemple : Fleur deviendra Fleur_decrypte).").grid(row=9, column=0, columnspan=10)
	Button(fenetre1, text = "A propos", command = a_propos).grid(row=10, column=0, columnspan=10)

def command_crypter_inter():
	global att
	att = 1

def command_decrypter_inter():
	global att
	att = 2

def main(a):
	fenetre = Tk()
	fenetre.title("PyCryptImage v1.1")
	texte = StringVar()
	mot = StringVar()
	plus = IntVar()
	plus1 = IntVar()
	global texte
	global mot
	global et_4
	global et_5
	global plus1
	pour1 = "0%"
	pour2 = "0%"
	et_0 = Label(fenetre, text = "PyCryptImage", font=('Arial', 20, 'italic', 'bold'))
	et_0.grid(row=0, column=0, columnspan=10)
	et_01 = Label(fenetre, text = "Image(s) :")
	et_01.grid(row=1, column=0, columnspan=10)
	et_1 = Entry(fenetre, textvariable=texte, width=50)
	et_1.grid(row=2, column=0, columnspan=10)
	et_2 = Checkbutton(fenetre, text = ".png", variable = plus)
	et_2.grid(row=3, column=2)
	et_3 = Checkbutton(fenetre, text = ".jpg", variable = plus1)
	et_3.grid(row=3, column=6)
	et_4 = Label(fenetre, text = pour1, relief=SUNKEN, width=40)
	et_4.grid(row=5, column=0, columnspan=10)
	et_5 = Label(fenetre, text = pour2, relief=SUNKEN, width=40)
	et_5.grid(row=6, column=0, columnspan=10)
	et_6 = Button(fenetre, text = "Crypter", command = command_crypter_inter)
	et_6.grid(row=7, column=1)
	et_7 = Button(fenetre, text = "Decrypter", command = command_decrypter_inter)
	et_7.grid(row=7, column=2)
	et_8 = Button(fenetre, text = "Aide", command = aide)
	et_8.grid(row=7, column=6)
	et_9 = Button(fenetre, text = "Quitter", command = fenetre.destroy)
	et_9.grid(row=7, column=7)
	et_10 = Entry(fenetre, textvariable=mot, width=20)
	et_10.grid(row=4, column=5, columnspan=5)
	et_11 = Label(fenetre, text = "Mot-clé :")
	et_11.grid(row=4, column=0, columnspan=5)
	fenetre.mainloop()
	global att
	att = 3

thread1 = threading.Thread(None, main, None, "a")
thread2 = threading.Thread(None, attente, None, "a")

thread1.start()
thread2.start()
 
thread1.join()
thread2.join()

"""
Changelog :

v1.1 :
Correction temporaire d'un bug de fermeture 
(le 2eme thread ne se fermai pas, maintenant, 
il plante lorsque l'on quitte le logiciel, et donc se ferme).

v1.0 :
Ajout d'un pourcentage avec le module threading.
Outil de cryptage amélioré.
Rapidité accru.
Ajout du support du jpeg.
Interface complétée.
Erreurs corrigées.
Programme renommé en PyCryptImage ou PyCI.

v0.5 :
Code fonctionnel, basé sur l'exercice "cache_image".
"""
