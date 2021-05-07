from data_processing import define_database
from data_processing import define_features_set
from data_processing import products_set_and_dictionary


import question_treatment
import tools


def main() :
	database = define_database()
	#question = input("Veuillez poser votre question.")
	question = "sharis avec 2 moulateur de 120 volts et sans batterie"

	products_set, products_dictionary = products_set_and_dictionary(database)
	#features_set = set(["ampère","tension", "voltage", "ampérage, courant"])
	features_set = define_features_set()
	features_dictionary = {}


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

	print("DICTIONNAIRES DE SCORES :")
	print(question_treatment.best_score(best_sentence, products_dictionary))

	p, f = question_treatment.ambiguous_words(product, feature, question)

	print ("The product is :" , p)
	print ("The Feature is :", f)

	etim_class = question_treatment.identify_Etim_class(p, products_dictionary)

	product = ""
	for w in p :
		product += w
		product += " "

	tab = question_treatment.best_similarity(product, database)
	for elem in tab :
		print ("similarity : ", elem[0], " line : ", elem[1])
		question_treatment.product_id(elem[1], database)
	# p_ID, database_product = question_treatment.product_id(product, database)
	# print("The product has been identified as :" , database_product)
	# print("Product ID :", p_ID)


main()
