from nltk.tokenize import word_tokenize
import nltk

#mesure de distance entre deux phrases en utilisant
#la mesure de similarité de Jaccard.
def distance_measurement(s1, s2) :
	list1 = word_tokenize(s1)
	list2 = word_tokenize(s2)
	intersection = len(list(set(list1).intersection(list2)))
	union = (len(list1) + len(list2)) - intersection
	return (float(intersection) / union)




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
