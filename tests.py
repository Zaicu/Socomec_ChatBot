from data_processing import define_database
from data_processing import define_features_set
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
    products_set, dictionary = products_set_and_dictionary(database)
    features_set = define_features_set()
    queries = open('tests.txt', 'r')
    queries_results = open('tests_results.txt', 'w')
    
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
                
        sentence = tools.sentence_filter(question)
        class_score_tab = question_treatment.score(sentence, dictionary)

        product = question_treatment.identify_product(sentence, products_set)
        feature = question_treatment.identify_feature(sentence, features_set)
        p, f = question_treatment.ambiguous_words(product, feature, question)

        #Stocker resultats
        queries_results.write("Query : " + str(question) + "\n")
        queries_results.write("The ETIM Class of the product is : " + str(class_score_tab[0][0]) + "\n")
        queries_results.write("The true ETIM Class of the product is : " + str(etim_class_true) + "\n")
        queries_results.write("The product is : " + str(p) + "\n")
        queries_results.write("The true product is : " + str(p_true) + "\n")
        queries_results.write("The Feature is : " + str(f) + "\n")
        queries_results.write("The true Feature is : " + str(f_true) + "\n")
        queries_results.write("End of Query\n\n")

        print("Query : " + str(question) + "\n")
        print("The ETIM Class of the product is :" + str(class_score_tab[0][0]) + "\n")
        print("The true ETIM Class of the product is :" + str(etim_class_true) + "\n")
        print("The product is :" + str(p) + "\n")
        print("The true product is :" + str(p_true) + "\n")
        print("The Feature is :" + str(f) + "\n")
        print("The true Feature is :" + str(f_true) + "\n")
        print("End of Query\n\n")

        #Calcul précision
        corr = 0 #nb correct sur cette question
        if class_score_tab[0][0] == etim_class_true:
            etim_class_correct += 1
            corr += 1
        if p == p_true:
            p_correct += 1
            corr += 1
        if f == f_true:
            f_correct += 1
            corr += 1
        if corr == 3:
            quest_correct += 1

    queries_results.write("\nEnd of queries")
    queries_results.close()

    print("Pourcentage de classes :" + str(etim_class_correct/nb_quest))
    print("Pourcentage de produits :" + str(p_correct/nb_quest))
    print("Pourcentage de features :" + str(f_correct/nb_quest))
    print("Pourcentage total :" + str(quest_correct/nb_quest))
    

main()
