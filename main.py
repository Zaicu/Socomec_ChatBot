import data_pretreatment
import question_treatment
import utiles


def main() :
	database = data_pretreatment.define_database()
	phrase = "Quelle est le voltage de l'interrupteur-sectionneur 3*16 Ampères ?"

	set_produit = data_pretreatment.set_product()
	set_feature = set(["ampère","tension", "voltage", "ampérage"])

	# sentence = filter_the_sentence(re.sub('([0-9]) *(Ampères|Ampère|ampères|ampère|ampere|Amp|amp)', "\g<1>A", phrase))
	sentence = question_treatment.filter_the_sentence(phrase)
	print(sentence)

	p = utiles.word_similarity(set_produit, sentence)
	f = utiles.word_similarity(set_feature, sentence)

	product = question_treatment.identify_product(p)
	feature = question_treatment.identify_feature(f)

	print("words that could be part of the product description :", product)
	print("words that could be the feature :", feature)

	print("words that are part of both :", list(set(product)&set(feature)))

	p, f = question_treatment.ambiguous_words(product, feature, phrase)

	print ("The product is :" , p)
	print ("The Feature is :", f)

	product = ""
	for w in p :
		product += w
		product += " "

	p_ID, database_product = question_treatment.product_id(product, database)
	print("The product has been identified as :" , database_product)
	print("Product ID :", p_ID)


main()
