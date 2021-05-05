import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import tools

import nltk

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


def exchange(tab, i, j) :
	aux = tab[i]
	tab[i] = tab[j] 
	tab[j] = aux 



#n : endroit où est placé elem dans le tab 
def insertion_sort (tab, n) : 
	i = n-1
	while (i >= 0) and (tab[i+1][0] > tab[i][0]) :
		exchange(tab, i, i+1) 
		i = i-1 



#product is the result of the  'identify_product'
def identify_Etim_class(Product, dictionary) :
	prediction_etim_class = score(Product, dictionary)
	# print("Les scores des classes ETIM :")
	# print(prediction_etim_class)

	# print("The etim class is :")
	# print(prediction_etim_class[0][0])



#calcule la similarité entre le produit recherché
#la description courte de la database.
def best_similarity(Product, database) :
	ten_most_similar = [0 for i in range (11)]
	m = 0 
	l = 0 
	best_line = ""
	
	i = 0
	for line in range(1, 13677):
		description = str(database['Description courte'][line])
		short_desc = str(database['Description longue FR'][line])
		if (short_desc != "nan"):
			description += " " 
			description += short_desc
		gamme_fam = str(database["Gamme - famille FR"][line])
		description += " "
		description += gamme_fam
		similarity = tools.jaccard_similarity(Product, description .lower())

		ten_most_similar[i] = (similarity, line)
		insertion_sort(ten_most_similar, i) 
		if (i < 10) :
			i = i+1 
	

	return(ten_most_similar[0:9])




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
	if len(ambiguous) == 0:
		return product, feature

	#on essaie de déterminer si le mot ambigu est une feature ou fait partie de la description du produit
	#en mesurant sa distance aux autres mots du produit

	for ambiguous_words in ambiguous :
		count = 0
		activate_count = False
		for words in word_tokenize(sentence.lower()) :
			if (words in list(stop_words)) and not activate_count :
				continue
			elif (words in list(stop_words)) and activate_count :
				count = count + 1
			elif (words.lower() in product) or (ambiguous_words == words.lower()) and not activate_count :
				activate_count = True
			elif (words.lower() in product) or (ambiguous_words == words.lower() )and activate_count :
				activate_count = False
			elif activate_count :
				count = count + 1

		if count >= 2 :
			product.remove(ambiguous_words)
		else :
			feature.remove(ambiguous_words)

		return(product, feature)




def product_id(line, database) :
	print("Product id : ", database['Product ID'][line]) 
	print("corresponding product : ", database['Description courte'][line])




def rank_score(score):
	rank = []
	for class_score in score.items():
		rank.append(class_score)
		for i in reversed(range(len(rank)-1)):
			if (rank[i + 1][1] > rank[i][1]):
				temp = rank[i + 1]
				rank[i + 1] = rank[i]
				rank[i] = temp
	return rank

def score(sentence, weights):
	score = {}
	for word_sentence in sentence:
		for classes, words in weights.items():
			if word_sentence in words:
				if not classes in score:
					score[classes] = 0
				score[classes] += weights[classes][word_sentence]
	return rank_score(score)
