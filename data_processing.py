import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import nltk
import math
nltk.download('wordnet')

import tools

product_data_path = '../socomec_chatbot/product_data_1 - MTC.xlsx'


def define_database() :
	xls = pd.ExcelFile(product_data_path)
	Products = pd.read_excel(xls, 'Products', skiprows = [0])
	return(Products)




def find_maximum_weight(dictionary) : #dictionnaire de mots
	max = 0
	for word in dictionary :
		if dictionary[word] > max :
			max += dictionary[word]
	return(max)



def tf(dictionary):
	#pour chaque dictionnaire ; trouver le poids max et diviser tous les poids par le poids max
	for classes in dictionary :
		max = find_maximum_weight(dictionary[classes])
		for word in dictionary[classes] :
			dictionary[classes][word] = dictionary[classes][word]/max
	return dictionary

def idf(dictionary, set_produit):
	idf = {}
	nb_classes = 0
	for product in set_produit:
		idf[product] = 0
	for classe, words in dictionary.items():
		nb_classes += 1
		for word, weights in words.items():
			idf[word] += 1 #dit dans combien de classe le mot apparait
	for product in set_produit:
		idf[product] = math.log(nb_classes/idf[product])
	return idf

def set_weights(dictionary, set_produit) : #dictionnaire de dictionnaires :)
	tf_ = tf(dictionary)
	idf_ = idf(dictionary, set_produit)
	for classes, words in tf_.items():
		for word, weights in words.items():
			tf_[classes][word] = tf_[classes][word]*idf_[word]
	return tf_

#retourne les N meilleurs mots pour chaque classe
def best_words(classes, N=10):
	best = {}
	for classe, words in classes.items():
		if (not classe in best):
			best[classe] = []
		for word in words.items():
			if (len(best[classe]) < N):
				best[classe].append(word)
				for i in reversed(range(len(best[classe]) - 1)):
					if (best[classe][i + 1][1] > best[classe][i][1]):
						temp = best[classe][i + 1]
						best[classe][i + 1] = best[classe][i]
						best[classe][i] = temp
			else:
				if (word[1] > best[classe][-1][1]):
					best[classe][-1] = word
					for i in reversed(range(N-1)):
						if (best[classe][i + 1][1] > best[classe][i][1]):
							temp = best[classe][i + 1]
							best[classe][i + 1] = best[classe][i]
							best[classe][i] = temp
	return best

#retourner l'ensemble sans doublons contenant tous les produits
def products_set_and_dictionary(Products):
	etim_classes = {}
	products_set = set()

	for ligne in range(1, 13677):

		ec = Products['ETIM class code'][ligne]

		#if (ec == 'EC000216')or(ec == 'EC001040')or(ec == 'EC002301')or(ec == 'EC001506'):

		if (not ec in etim_classes):
			etim_classes[ec] = {}

		produit = ""
		if (Products['Gamme - famille FR'][ligne] == Products['Gamme - famille FR'][ligne] and Products['Gamme - famille FR'][ligne] != 0):
			produit = produit + str(Products['Gamme - famille FR'][ligne]) + " "
		if (Products['Description courte'][ligne] == Products['Description courte'][ligne] and Products['Description courte'][ligne] != 0):
			produit = produit + str(Products['Description courte'][ligne]) + " "
		if (Products['Description longue FR'][ligne] == Products['Description longue FR'][ligne] and Products['Description longue FR'][ligne] != 0):
			produit = produit + str(Products['Description longue FR'][ligne])

		filtered_sentence = tools.sentence_filter(produit)
		products_set = products_set.union(set(filtered_sentence))
		for word in filtered_sentence :
			if (word == word) and (not word in etim_classes[ec]):
				etim_classes[ec][word] = 1
			else:
				etim_classes[ec][word] += 1

	etim_classes = set_weights(etim_classes, products_set)
	#print(best_words(etim_classes))
	print(etim_classes)
	return products_set, etim_classes
