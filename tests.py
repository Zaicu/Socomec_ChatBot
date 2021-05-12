import pandas as pd

from data_processing import define_database
from data_processing import features_set_and_dictionary
from data_processing import products_set_and_dictionary


import question_treatment
import tools

def extract_query(queries):
	quest = queries.readline()
	etim = queries.readline()
	prod = queries.readline()
	feat = queries.readline()
	end = queries.readline()
	if end == "\n":
		fin = False
	else:
		fin = True
	return [fin, quest.rstrip(), etim.rstrip(), prod.rstrip(), feat.rstrip()]


def main():
	#init
	database = define_database()
	products_set, products_dictionary = products_set_and_dictionary(database)
	features_set, features_dict = features_set_and_dictionary()
	queries = open('tests.txt', 'r')
	queries_results = open('tests_results.txt', 'w')
	queries_results.write("Beginning of queries\n\n")

	nb_quest = 0
	etim_class_correct = 0
	p_correct = 0
	f_correct = 0
	quest_correct = 0
	fin = False
	while not(fin):
		nb_quest += 1
		print("Question " + str(nb_quest))
		fin, question, etim_class_true, p_true, f_true = extract_query(queries)
		p_true = p_true.lower()
		f_true = f_true.lower()
		# sentence = sentence_filter(re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", question))
		sentence = tools.sentence_filter(question)

		best_sentence = question_treatment.question_identification(sentence, products_set, features_set)
		print("best identification :")
		print(best_sentence)

		product, feature = question_treatment.identify_product_and_feature(best_sentence)


		print("words that could be part of the product description :", product)
		print("words that could be the feature :", feature)

		#class_score_tab = question_treatment.score(sentence, products_dictionary)
		#etim_class = class_score_tab[0][0]
		etim_class = "EC001506"

		print("words that are part of both :", list(set(product)&set(feature)))
		p, f = question_treatment.ambiguous_words(product, feature, question)

		print ("The product is :" , p)
		print ("The Feature is :", f)

		p_id, _, f_id, _ = question_treatment.get_ids_and_lines(p, f, database, features_dict)
		#Stocker resultats
		queries_results.write("Query : " + str(question) + "\n")
		queries_results.write("The ETIM Class of the product is : " + str(etim_class) + "\n")
		queries_results.write("The true ETIM Class of the product is : " + str(etim_class_true) + "\n")
		queries_results.write("The product is : " + str(p_id) + "\n")
		queries_results.write("The true product is : " + str(p_true) + "\n")
		queries_results.write("The Feature is : " + str(f_id) + "\n")
		queries_results.write("The true Feature is : " + str(f_true) + "\n")
		queries_results.write("End of Query\n\n")

		print("Query : " + str(question))
		print("The ETIM Class of the product is :" + str(etim_class))
		print("The true ETIM Class of the product is :" + str(etim_class_true))
		print("The product is :" + str(p_id))
		print("The true product is :" + str(p_true))
		print("The Feature is :" + str(f_id))
		print("The true Feature is :" + str(f_true))
		print("End of Query\n")

		#Calcul précision
		corr = 0 #nb correct sur cette question
		if etim_class == etim_class_true:
			etim_class_correct += 1
			corr += 1
		if p_id == p_true:
			p_correct += 1
			corr += 1
		if f_id == f_true:
			f_correct += 1
			corr += 1
		if corr == 3:
			quest_correct += 1

	queries_results.write("\nEnd of queries")
	queries_results.close()

	print("Pourcentage de classes correctes:" + str(etim_class_correct/nb_quest))
	print("Pourcentage de produits corrects:" + str(p_correct/nb_quest))
	print("Pourcentage de features correctes:" + str(f_correct/nb_quest))
	print("Pourcentage total corrects:" + str(quest_correct/nb_quest))
    

main()
