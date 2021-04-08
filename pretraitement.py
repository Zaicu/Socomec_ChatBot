import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy 
import json

import nltk
nltk.download('wordnet')

xls = pd.ExcelFile('../product_data_1.xlsx')
Products = pd.read_excel(xls, 'Products', skiprows=[0])
clas = Products.iloc[3,4]
Class1 = pd.read_excel(xls, clas)

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
	bag_of_words = word_tokenize(sentence.lower())
	sentence = re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", sentence)
	filtered_sentence = []

	for w in bag_of_words:
		if w not in stop_words:
			filtered_sentence.append(w)
	return filtered_sentence




#mesure de distance entre deux phrases en utilisant
#la mesure de similarité de Jaccard.
def distance_measurement(s1, s2) :
	list1 = word_tokenize(s1)
	list2 = word_tokenize(s2)
	intersection = len(list(set(list1).intersection(list2)))
	union = (len(list1) + len(list2)) - intersection
	return (float(intersection) / union)




#calcule la similarité entre le produit recherché
#la description courte de la database.
def best_similarity(Product) :
	m1 = 0
	i = 0
	l1 = i
	best_line1 = ""
	best_line2 = ""
	for line in Products['Description courte'] :
		dist = distance_measurement(Product, str(line).lower())
		if dist > m1 :
			m1 = dist
			l1 = i
			best_line1 = str(line)
		i = i+1 ;
	i = 0 
	m2 = 0
	l2 = i
	for line in Products['Description longue FR'] :
		dist = distance_measurement(Product, str(line).lower())
		if dist > m2 :
			m2 = dist
			l2 = i
			best_line2 = str(line)
		i = i+1 ;
	if m1 > m2 : 
		return(m1, l1, best_line1)
	else : 
		return(m2, l2, best_line2)



#retourner l'ensemble sans doublons contenant tous les produits 
def set_product():
	set_produit = set()
	for ligne in range(1, 13677):
		ec = Products['ETIM class code'][ligne]
		if (ec == 'EC000216')or(ec == 'EC001040')or(ec == 'EC002301')or(ec == 'EC001506'):
			produit = Products['Description courte'][ligne]
			if (produit == produit and produit != 0):
				filtered_sentence = filter_the_sentence(produit)
				set_produit = set_produit.union(set(filtered_sentence))

			produit = Products['Description longue FR'][ligne]
			if (produit == produit and produit != 0):
				filtered_sentence = filter_the_sentence(produit)
				set_produit = set_produit.union(set(filtered_sentence))

	return set_produit



def word_similarity(set, sentence) :
	list_ = list(set)
	dist = []

	for word in sentence :

		best_in_set = list_[0]
		best_distance = nltk.edit_distance(list_[0], word) 

		for word_set in list_ :
			distance = nltk.edit_distance(word.lower(), word_set.lower()) 
			if distance < best_distance : #en cas d'égalité ? à améliorer
				best_in_set = word_set.lower()
				best_distance = distance
			# if distance == best_distance and distance == 0 : 
			# 	best_in_set = word_set 
			# 	best_distance = distance
			# 	dist.append((best_distance,best_in_set))

		dist.append((best_distance,best_in_set))

	return(dist)

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
	

def product_id(product) :
	m, l, best_line = best_similarity(product)
	return(Products['Product ID'][l], best_line)
	
	

def main() :
	phrase = "Quelle est le voltage de l'interrupteur-sectionneur 3P 160A ?"

	set_produit = set_product()
	set_feature = set(["ampère","tension", "voltage", "ampérage"])

	# sentence = filter_the_sentence(re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", phrase))
	sentence = filter_the_sentence(phrase)
	
	p = word_similarity(set_produit, sentence) 
	f = word_similarity(set_feature, sentence) 

	product = identify_product(p) 
	feature = identify_feature(f) 

	print("words that could be part of the product description :", product) 
	print("words that could be the feature :", feature)

	print("words that are part of both :", list(set(product)&set(feature)))

	p, f = ambiguous_words(product, feature, phrase)

	print ("The product is :" , p) 
	print ("The Feature is :", f) 

	product = ""
	for w in p : 
		product += w 
		product += " "
	
	p_ID, database_product = product_id(product)
	print("The product has been identified as :" , database_product) 
	print("Product ID :", p_ID)


#entre '3x16A' et '3x6' il ya le même nombre de différences avec le terme '3x16' donc PROBLEME
#considérer l'ensemble "3x16 Ampères" 

# phrase2 = "Quelle est le voltage de l'interrupteur-sectionneur 3P 160A ?"

# (P, F) = question_treatement(phrase2)

# print("Produit :", P)
# print("Feature :", F)

# print("Execution du main :")

main()

