import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import json
import utiles

import question_treatment

import nltk
nltk.download('wordnet')


def define_database() :
	xls = pd.ExcelFile('../product_data_1.xlsx')
	Products = pd.read_excel(xls, 'Products', skiprows = [0])
	clas = Products.iloc[3,4]
	Class1 = pd.read_excel(xls, clas)

	return(Products)

Products = define_database()

#fonction recherche d'appartenance d'un objet à une liste
def is_in_list(object, list) :
	n = len(list)
	i = 0
	while ((i<n)and(object != list[i])) :
		i = i+1
	return(i<n)

def find_maximum_weight(dictionary) : #dictionnaire de mots
	max = 0
	for word in dictionary :
		if dictionary[word] > max :
			max = dictionary[word]
	return(max)

def set_weights(dictionary) : #dictionnaire de dictionnaires :)
	#pour chaque dictionnaire ; trouver le poids max et diviser tous les poids par le poids max
	for classes in dictionary :
		max = find_maximum_weight(dictionary[classes])
		for word in dictionary[classes] :
			dictionary[classes][word] = dictionary[classes][word]/max

	return(dictionary)



#retourner l'ensemble sans doublons contenant tous les produits
def set_product():
	classes = {}
	set_produit = set()

	for ligne in range(1, 13677):

		ec = Products['ETIM class code'][ligne]

		if (ec == 'EC000216')or(ec == 'EC001040')or(ec == 'EC002301')or(ec == 'EC001506'):

			if (not ec in classes):
				classes[ec] = {}
			produit = str(Products['Description courte'][ligne]) + " " + str(Products['Description longue FR'][ligne])
			if (produit == produit and produit != 0):
				filtered_sentence = question_treatment.filter_the_sentence(produit)
				set_produit = set_produit.union(set(filtered_sentence))
				for word in filtered_sentence :
					if (word == word) and (not word in classes[ec]):
						classes[ec][word] = 1
					else:
						classes[ec][word] += 1

	classes = set_weights(classes)

	print(classes)
	return set_produit




#entre '3x16A' et '3x6' il ya le même nombre de différences avec le terme '3x16' donc PROBLEME
#considérer l'ensemble "3x16 Ampères"

# phrase2 = "Quelle est le voltage de l'interrupteur-sectionneur 3P 160A ?"

# (P, F) = question_treatement(phrase2)

# print("Produit :", P)
# print("Feature :", F)

# print("Execution du main :")
