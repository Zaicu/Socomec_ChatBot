import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import nltk

import math

import tools

stop_words = set(stopwords.words('french'))
stop_words.add("quelle")
stop_words.add("quel")
stop_words.add("quels")
stop_words.add("combien")
stop_words.add("?")
stop_words.add("!")
stop_words.add("bonjour")
stop_words.add("svp")
stop_words.add("bonsoir")
stop_words.add(".")
stop_words.add(",")
stop_words.add("’")
stop_words.add("-")
stop_words.add("[")
stop_words.add("]")
stop_words.add("(")
stop_words.add(")")

product_data_path = '../product_data_1 - MTC.xlsx'

def define_database() :
	xls = pd.ExcelFile(product_data_path)
	Products = pd.read_excel(xls, 'Products', skiprows = [0])
	return(Products)


def nb_words_class(Products):
	nb_words = {}
	for ligne in range(1, 13677):
		ec = Products['ETIM class code'][ligne]
		if (not ec in nb_words):
			nb_words[ec] = 0
		if (Products['Description courte'][ligne] == Products['Description courte'][ligne] and Products['Description courte'][ligne] != 0):
			nb_words[ec] += len(tools.sentence_filter(Products['Description courte'][ligne]))
		if (Products['Description longue FR'][ligne] == Products['Description longue FR'][ligne] and Products['Description longue FR'][ligne] != 0):
			nb_words[ec] += len(tools.sentence_filter(Products['Description longue FR'][ligne]))
	return nb_words




def find_maximum(dictionary) : #dictionnaire de mots
	max = 0
	for word in dictionary :
		if dictionary[word] > max :
			max += dictionary[word]
	return(max)




def tf(dictionary, nb_words_class):
	#pour chaque dictionnaire ; trouver le poids max et diviser tous les poids par le poids max
	max_nb_words = find_maximum(nb_words_class)
	for classes in dictionary :
		max = 0
		for word in dictionary[classes] :
			if dictionary[classes][word] > max:
				max = dictionary[classes][word]
		for word in dictionary[classes] :
			dictionary[classes][word] = dictionary[classes][word]*(0.5 + 0.5*nb_words_class[classes]/max_nb_words)#*(0.5 + 0.5*(nb_words_class[classes]/max))
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




def set_weights(dictionary, set_produit, nb_words_class) : #dictionnaire de dictionnaires :)
	tf_ = tf(dictionary, nb_words_class)
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

	etim_classes = set_weights(etim_classes, products_set, nb_words_class(Products))

	return products_set, etim_classes



#faire un dictionnaire où quand tu mets la classe il te renvoie tous les features de cette classe
# -> generalisation de features_set_and_dictionary quand on aura tous les synonymes en français

def features_set_and_dictionary() :
	features_dict = {}
	features_set = set()
	xls = pd.ExcelFile(product_data_path)
	E1506 = pd.read_excel(xls, 'EC001506', skiprows = [0,1,2])
	E1506 = E1506.drop(E1506.columns[[1]], axis=1)  #remove second column (blank column)

	n = E1506.shape[1]

	for i in range (0,n) :
		feature = str(E1506.iat[0,i]) + " " + str(E1506.iat[1,i])
		feature = re.sub('\|', " ", feature)
		feature = re.sub(';', " ", feature)
		feature = re.sub('nan', "", feature)
		feature = re.sub('([A-Z]*[a-z]*)\'([A-Z]*[a-z]*)', "\g<2>", feature)
		list_features = word_tokenize(feature.lower())

		feature_id = list_features[0]


		for index, w in enumerate(list_features):
			if w in stop_words:
				list_features.pop(index)

		if (not feature_id in features_dict) :
			features_dict[feature_id] = list_features[1:]

		for elem in list_features :
			features_set = features_set.union(set([elem]))

	return features_set, features_dict
