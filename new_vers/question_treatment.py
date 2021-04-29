import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import tools

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




#product is the result of the  'identify_product'
def identify_Etim_class(product, dictionary) : 
	nb_of_words_in_class = [0, 0, 0, 0]
	for word in product : 
		i = 0 
		for etim_class in dictionary : 
			if word in dictionary[etim_class] : 
				nb_of_words_in_class[i] += 1 
			i += 1 
	
	maxi = 0
	i = 0 
	true_etim_class = " "
	for etim_class in dictionary : 
		if nb_of_words_in_class[i] > maxi :
			maxi = nb_of_words_in_class[i]
			true_etim_class = etim_class 
		i += 1 
	
	print("The etim class is :")
	print(true_etim_class)

	return(true_etim_class) 



	


#calcule la similarité entre le produit recherché
#la description courte de la database.
def best_similarity(Product, database) :
	m = 0 
	l = 0 
	best_line = ""
	print("in best similarity, the product is :", Product)
	n = 13677
	
	for line in range(1, n):
		description = str(database['Description courte'][line]) + " " + str(database['Description longue FR'][line])
		#description = str(database['Gamme - famille FR'][line]) + " " + str(database['Description courte'][line]) + " " + str(database['Description longue FR'][line])

		dist = tools.jaccard_similarity(Product, description .lower())
		
		if dist > m :
			m = dist 
			l = line
			best_line = description
		
	return (m, l, best_line)



def identify_product(tokenized_sentence, products_set) :
	best_matches = tools.edit_distance(tokenized_sentence, products_set)
	product = []
	for (n,w) in best_matches :
		if n <= 2 :
			product.append(w)
	print("Produit identifié : ", product)
	return(product)

def identify_feature(tokenized_sentence, features_set) :
	best_matches = tools.edit_distance(tokenized_sentence, features_set)
	feature = []
	for (n,w) in best_matches :
		if n <= 2 :
			feature.append(w)

	print("Feature identifiée : ", feature)
	return(feature)




def ambiguous_words(product, feature, sentence) :
	ambiguous = list(set(product)&set(feature))

	#on essaie de déterminer si le mot ambigu est une feature ou fait partie de la description du produit
	#en mesurant sa distance aux autres mots du produit

	for ambiguous_words in ambiguous :
		count = 0
		activate_count = False
		for words in word_tokenize(sentence.lower()) :
			if tools.is_in_list(words, list(stop_words)) and not activate_count :
				continue
			elif tools.is_in_list(words, list(stop_words)) and activate_count :
				count = count + 1
			elif (tools.is_in_list(words.lower(), product) or ambiguous_words == words.lower()) and not activate_count :
				activate_count = True
			elif (tools.is_in_list(words.lower(), product) or ambiguous_words == words.lower() )and activate_count :
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
