import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import nltk
nltk.download('wordnet')

import tools 

product_data_path = '../../product_data_1 - MTC.xlsx'


def define_database() :
	xls = pd.ExcelFile(product_data_path)
	Products = pd.read_excel(xls, 'Products', skiprows = [0])
	return(Products)




def find_maximum_weight(dictionary) : #dictionnaire de mots
	maxi = 0
	for word in dictionary :
		if dictionary[word] > maxi :
			maxi = dictionary[word]
	return(maxi)




def set_weights(dictionary) : #dictionnaire de dictionnaires :)
	#pour chaque dictionnaire ; trouver le poids max et diviser tous les poids par le poids max
	for etim_classes in dictionary :
		maxi = find_maximum_weight(dictionary[etim_classes])
		for word in dictionary[etim_classes] :
			dictionary[etim_classes][word] = dictionary[etim_classes][word]/maxi

	return(dictionary)





#retourner l'ensemble sans doublons contenant tous les produits
def products_set_and_dictionary(Products):
	etim_classes = {}
	products_set = set()

	for ligne in range(1, 13677):

		ec = Products['ETIM class code'][ligne]

		if (ec == 'EC000216')or(ec == 'EC001040')or(ec == 'EC002301')or(ec == 'EC001506'):

			if (not ec in etim_classes):
				etim_classes[ec] = {}

			produit = str(Products['Gamme - famille FR'][ligne])
			produit += str(Products['Description courte'][ligne]) 
			produit +=  " " 
			produit += str(Products['Description longue FR'][ligne])

			if (produit == produit and produit != 0):
				filtered_sentence = tools.sentence_filter(produit)
				products_set = products_set.union(set(filtered_sentence))
				for word in filtered_sentence :
					if (word == word) and (not word in etim_classes[ec]):
						etim_classes[ec][word] = 1
					else:
						etim_classes[ec][word] += 1

	etim_classes = set_weights(etim_classes)

	return (products_set, etim_classes)


