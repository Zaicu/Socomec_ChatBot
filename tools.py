from nltk.tokenize import word_tokenize
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import numpy as np
import spacy
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




# filtre une phrase en renvoyant le tableau
def sentence_filter(sentence):
	sentence = sentence.replace("'", " ")
	sentence = re.sub('([0-9]+) *[xX*] *([0-9]+)', "\g<1>x\g<2>", sentence)
	sentence = re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", sentence)
	bag_of_words = word_tokenize(sentence.lower())
	filtered_sentence = []

	for w in bag_of_words:
		if w not in stop_words:
			filtered_sentence.append(w)
	return filtered_sentence




#mesure de distance entre deux phrases en utilisant
#la mesure de similarité de Jaccard.
def jaccard_similarity(s1, s2) :
	list1 = word_tokenize(s1)
	list2 = word_tokenize(s2)
	intersection = len(list(set(list1).intersection(list2)))
	union = (len(list1) + len(list2)) - intersection
	return (float(intersection) / union)




def edit_distance(sentence, set) :
	list_ = list(set)
	dist = []
	used_sentence = sentence

	for word in used_sentence :
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
