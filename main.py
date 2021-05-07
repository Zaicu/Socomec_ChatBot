import pandas as pd

from data_processing import define_database
from data_processing import features_set_and_dictionary
from data_processing import products_set_and_dictionary


import question_treatment
import tools

product_data_path = '../product_data_1 - MTC.xlsx'


def main() :
	database = define_database()
	#question = input("Veuillez poser votre question.")
	question = "Quel est le poids de la sortie impulsion du E27"

	products_set, products_dictionary = products_set_and_dictionary(database)
	#features_set = set(["ampère","tension", "voltage", "ampérage, courant"])
	features_set, features_dict = features_set_and_dictionary()


	# sentence = sentence_filter(re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", question))
	sentence = tools.sentence_filter(question)

	best_sentence = question_treatment.best_sentence(sentence, products_set, features_set)
	print("best sentence :")
	print(best_sentence)

	product = question_treatment.identify_product(best_sentence)
	feature = question_treatment.identify_feature(best_sentence)


	print("words that could be part of the product description :", product)
	print("words that could be the feature :", feature)

	print("words that are part of both :", list(set(product)&set(feature)))

	#class_score_tab = question_treatment.score(sentence, products_dictionary)

	#print("The ETIM Class of the product is probably :")
	#print(class_score_tab[0])

	# print("DICTIONNAIRES DE SCORES :")
	# print(question_treatment.best_score(best_sentence, products_dictionary))

	p, f = question_treatment.ambiguous_words(product, feature, question)

	print ("The product is :" , p)
	print ("The Feature is :", f)

	#récupérer l'id de la feature 
	feature_id = question_treatment.get_feature_id(f, features_dict)

	print("feature_id :", feature_id)

	etim_class = question_treatment.identify_Etim_class(p, products_dictionary)


	xls = pd.ExcelFile(product_data_path)
	product_page = pd.read_excel(xls, "EC001506", skiprows = [0,1,2])


	feature_column = question_treatment.get_feature_column(feature_id, product_page)
	print("feature_id : ", feature_id, "in column : ", feature_column+1)


	product = ""
	for w in p :
		product += w
		product += " "

	tab = question_treatment.best_similarity(product, database)
	# for elem in tab :
	# 	print ("similarity : ", elem[0], " line : ", elem[1])
	# 	question_treatment.get_product_id(elem[1], database)
	
	product_id = question_treatment.get_product_id(tab[0][1], database)
	product_line = question_treatment.get_product_line(product_id, product_page)

	print("product_id : ", product_id, "in line : ", product_line+1)
	
	print("RESPONDE A LA QUESTIN :::", question_treatment.get_value(product_line, feature_column, product_page))
	# p_ID, database_product = question_treatment.get_product_id(product, database)
	# print("The product has been identified as :" , database_product)
	# print("Product ID :", p_ID)


main()
