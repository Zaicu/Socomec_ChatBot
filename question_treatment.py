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
stop_words.add("’")
stop_words.add("-")

#product is the result of the  'identify_product'
def identify_Etim_class(Product, dictionary) :
	prdiction_etim_class = score(Product, dictionary)
	print("Les scores des classes ETIM :")
	print(prdiction_etim_class)

	print("The etim class is :")
	print(prdiction_etim_class[0][0])


#calcule la similarité entre le produit recherché
#la description courte de la database.
def best_similarity(Product, database) :
	m1 = 0
	i = 0
	l1 = i
	best_line1 = ""
	best_line2 = ""
	for line in database['Description courte'] :
		dist = tools.jaccard_similarity(Product, str(line).lower())
		if dist > m1 :
			m1 = dist
			l1 = i
			best_line1 = str(line)
		i = i+1 ;
	i = 0
	m2 = 0
	l2 = i
	for line in database['Description longue FR'] :
		dist = tools.jaccard_similarity(Product, str(line).lower())
		if dist > m2 :
			m2 = dist
			l2 = i
			best_line2 = str(line)
		i = i+1 ;
	if m1 > m2 :
		return(m1, l1, best_line1)
	else :
		return(m2, l2, best_line2)



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


def product_id(product, database) :
	m, l, best_line = best_similarity(product, database)
	return(database['Product ID'][l], best_line)

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
	print("")
	score = {}
	for word_sentence in sentence:
		for classes, words in weights.items():
			if word_sentence in words:
				if not classes in score:
					score[classes] = 0
				score[classes] += weights[classes][word_sentence]
	return rank_score(score)
