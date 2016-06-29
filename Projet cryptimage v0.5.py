# -*- coding: utf-8 -*-
# Auteur : Alexandreou
print("----------------------------------------------------------------------")
print("Projet cryptimage v0.5")
print("----------------------------------------------------------------------")

from PIL import Image

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
	a = 0
	pos_temp = pos_lettre
	while a == 0:
		if pos_temp >= taille_mot:
			pos_temp -= taille_mot
		else:
			lettre_code = mot[pos_temp]
			a = 1

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
		print(rouge)
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		rouge -= chilet
		print(rouge)
	rouge = verif(rouge)

	(lettre_code, taille_mot, plus_moins) = lettre(vert, pos_lettre, mot, cryptede)
	chilet = ord(lettre_code)
	if plus_moins == 0:
		if cryptede == 0:
			chilet += taille_mot
		else:
			chilet -= taille_mot
		vert += chilet
		print(vert)
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		vert -= chilet
		print(vert)
	vert = verif(vert)

	(lettre_code, taille_mot, plus_moins) = lettre(bleu, pos_lettre, mot, cryptede)
	chilet = ord(lettre_code)
	if plus_moins == 0:
		if cryptede == 0:
			chilet += taille_mot
		else:
			chilet -= taille_mot
		bleu += chilet
		print(bleu)
	else:
		if cryptede == 0:
			chilet -= taille_mot
		else:
			chilet += taille_mot
		bleu -= chilet
		print(bleu)
	bleu = verif(bleu)

	return (rouge, vert, bleu)

def cache(im1:Image, im2:Image, mot_cle, cryptede)->None:
	# Pour l'avancement.
	a = 0
	b = 0
	nb_tour = 1

	# Cherche les dimentions des deux images.
	(largeur1, hauteur1) = (im1.width, im1.height)

	# Deux boucles qui permettent de traiter chaques pixels un par un.
	for i in range(hauteur1):
		for e in range(largeur1):

			try:
				triplet1 = list(im1.getpixel((e, i)))
			except TypeError:
				triplet1 = im1.getpixel((e, i))
				triplet1 = [triplet1, triplet1, triplet1]

			tripletbi1 = crypte(triplet1, nb_tour, mot_cle, cryptede)

			print(tripletbi1)

			# Reconstitue le pixel modifié.
			im2.putpixel((e, i), tripletbi1)

			# Pour l'avancement !
			if b == 0:
				print("-"*a, i, "x",e, "pixels")
				if a == 10:
					b = 1
				a += 1
			if b == 1:
				print("-"*a, i, "x",e, "pixels")
				if a == 1:
					b = 0
				a -= 1
			nb_tour += 1

def retrouver_image(mot_cle, cryptede):
	# Nom des images à utiliser.
	nom_image_base = "Image1.png"
	nom_image_trouve = "Image2.png"

	# Ouvre l'image de base et l'a met dans la variable im1.
	im1 = Image.open(nom_image_base)

	(largeur1, hauteur1) = (im1.width, im1.height)

	im2 = Image.new('RGB', (largeur1,hauteur1), (255,255,255))

	cache(im1, im2, mot_cle, cryptede)

	im2.save(nom_image_trouve, "PNG")

def main():
	"""
	Fonction principale.
	"""
	# Variable qui permet d'arreter la boucle.
	a = 0

	# Boucle qui permet de demander une nouvelle fois une réponse si la réponse
	# précedante est non reconnu.
	while a == 0:

		# Demande quelle fonction utilisé.
		#resu = input("Voulez-vous cacher une image (C) ou retrouver une image (R) ?")
		resu = "Alexandre"
		if resu == "C" or resu == "c":
			# Fonction qui permet de cacher une image.
			cacher_image()
			a = 1
		elif resu == "R" or resu == "r":
			# Fonction qui permet de retrouver une image.
			retrouver_image()
			a = 1
		else:
			print("Veuillez répondre à la question avec comme réponses possible R ou C.")
			print("")
		retrouver_image(resu, 1)
		a = 1

main()

"""
Changelog :

v0.5 :
Code fonctionnel, basé sur l'exercice "cache_image".
"""