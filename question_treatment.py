import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import json
import utiles

import nltk
nltk.download('wordnet')

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




#fonction recherche d'appartenance d'un objet à une liste
def is_in_list(object, list) :
	n = len(list)
	i = 0
	while ((i<n)and(object != list[i])) :
		i = i+1
	return(i<n)





# filtre une phrase en renvoyant le tableau
def filter_the_sentence(sentence):
	sentence = sentence.replace("'", " ")
	sentence = re.sub('([0-9]+) *[xX*] *([0-9]+)', "\g<1>x\g<2>", sentence)
	sentence = re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", sentence)
	bag_of_words = word_tokenize(sentence.lower())
	filtered_sentence = []

	for w in bag_of_words:
		if w not in stop_words:
			filtered_sentence.append(w)
	return filtered_sentence






#calcule la similarité entre le produit recherché
#la description courte de la database.
def best_similarity(Product, database) :
	m1 = 0
	i = 0
	l1 = i
	best_line1 = ""
	best_line2 = ""
	for line in database['Description courte'] :
		dist = utiles.distance_measurement(Product, str(line).lower())
		if dist > m1 :
			m1 = dist
			l1 = i
			best_line1 = str(line)
		i = i+1 ;
	i = 0
	m2 = 0
	l2 = i
	for line in database['Description longue FR'] :
		dist = utiles.distance_measurement(Product, str(line).lower())
		if dist > m2 :
			m2 = dist
			l2 = i
			best_line2 = str(line)
		i = i+1 ;
	if m1 > m2 :
		return(m1, l1, best_line1)
	else :
		return(m2, l2, best_line2)



def identify_product(best_matches) :
	product = []
	for (n,w) in best_matches :
		if n <= 2 :
			product.append(w)

	return(product)

def identify_feature(best_matches) :
	feature = []
	for (n,w) in best_matches :
		if n <= 2 :
			feature.append(w)

	return(feature)




def ambiguous_words(product, feature, sentence) :
	ambiguous = list(set(product)&set(feature))

	#on essaie de déterminer si le mot ambigu est une feature ou fait partie de la description du produit
	#en mesurant sa distance aux autres mots du produit

	for ambiguous_words in ambiguous :
		count = 0
		activate_count = False
		for words in word_tokenize(sentence.lower()) :
			if is_in_list(words, list(stop_words)) and not activate_count :
				continue
			elif is_in_list(words, list(stop_words)) and activate_count :
				count = count + 1
			elif (is_in_list(words.lower(), product) or ambiguous_words == words.lower()) and not activate_count :
				activate_count = True
			elif (is_in_list(words.lower(), product) or ambiguous_words == words.lower() )and activate_count :
				activate_count = False
			elif activate_count :
				count = count + 1

		if count >= 2 :
			product.remove(ambiguous_words)
		else :
			feature.remove(ambiguous_words)

		return(product, feature)


def product_id(product, database) :
	m, l, best_line = best_similarity(product, database)
	return(database['Product ID'][l], best_line)
