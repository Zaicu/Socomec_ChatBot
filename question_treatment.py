import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
import tools
import sys

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
	return(prediction_etim_class[0][0])



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




def best_sentence(sentence, products_set, features_set):
	best_sentence = []

	for index in range(len(sentence)):

		max = sys.maxsize * 2 + 1
		best_sentence.append([])
		for product in products_set:
			distance = nltk.edit_distance(sentence[index], product)
			if (distance < max):
				best_sentence[index] = [(product,'product')]
				max = distance
			elif (distance == max):
				best_sentence[index].append((product,'product'))

		for feature in features_set:
			distance = nltk.edit_distance(sentence[index], feature)
			if (distance < max):
				best_sentence[index] = [(feature,'feature')]
				max = distance
			elif (distance == max):
				best_sentence[index].append((feature,'feature'))
	return best_sentence




def identify_product(best_sentence) :
	product = []
	for words in best_sentence:
		for word in words:
			if word[1] == 'product':
				product.append(word[0])
	return(product)



def identify_feature(best_sentence) :
	feature = []
	for words in best_sentence:
		for word in words:
			if word[1] == 'feature':
				feature.append(word[0])
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




def get_product_id(line, database) :
	return(database['Product ID'][line])




def get_feature_id(feature, features_dict) : 
	tab = []
	for f_id in features_dict : 
		count = 0
		for f in features_dict[f_id] :
			for word in feature : 
				if f == word : 
					count += 1 
		tab.append((f_id, count))
	
	max_tab = tools.maximum(tab) 
	return(max_tab[0])




def get_product_line(product_id, product_page) :
	column = product_page.iloc[:,0]
	for i in range (2, len(column)) : 
		current_id = column[i]
		if product_id == current_id.lower() :
			return(i) 





def get_feature_column(feature_id, product_page) : 
	line = product_page.iloc[0]
	for i in range (2, len(line)) : 
		current_id = re.sub('(EF[0-9]*)\|(.*)', "\g<1>", line[i])
		if feature_id == current_id.lower() :
			return(i) 


def get_value(line, column, product_page) :
	return product_page.iloc[line, column]




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
			if word_sentence[0] in words:
				if not classes in score:
					score[classes] = 0
				score[classes] += weights[classes][word_sentence[0]]
	return rank_score(score)


def best_score(best_sentence, weights):
	# initialisation
	stop = True
	score_dict = []
	n = len(best_sentence)
	nb_words = []
	compteur = []
	sentence = [("","") for i in range(n)]
	for i in range(n):
		nb_words.append(len(best_sentence[i]))
		compteur.append(0)

	# on crée toutes les phrases
	while stop:
		for i in range(n):
			sentence[i] = best_sentence[i][compteur[i]]
		score_dict.append(score(sentence, weights))

		# prochaine phrase
		compteur[0] += 1
		for i in range(n):
			if compteur[i] == nb_words[i]:
				compteur[i] = 0
				if (i != n-1):
					compteur[i+1] +=1
				else:
					stop = False
	return score_dict
