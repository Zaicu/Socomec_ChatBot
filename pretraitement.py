import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import json 

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

f = open('synonymes.json')
synonymes = json.load(f)
#fermer le pauvre json

def is_in_list(object, list) :
    n = len(list) 
    i = 0 
    while ((i<n)and(object != list[i])) :
        i = i+1 
    return(i<n) 

def question_treatement(question) :
    question = question.replace("'", " ")
    bag_of_words = word_tokenize(question)

    filtered_sentence = [] 
    word_class = []

    for w in bag_of_words:  
        if w not in stop_words:  
            filtered_sentence.append(w) 
    
    print("filtered sentence :" , filtered_sentence)

    for w in filtered_sentence :
        print("word :", w) 
        n = len(synonymes) 
        i = 0
        for key in synonymes : 
            if (w.lower() == key.lower()) : 
                word_class.append((w,synonymes[key]["class"]))
                continue 
            elif is_in_list(w, synonymes[key]["synonym"]) :
                word_class.append((w,synonymes[key]["class"]))
                continue
            else :
                i = i+1 
        print ("i = ", i) 
        if (i == n) : 
            word_class.append((w, "Other")) 
    
    print(word_class)
    
    Product = ""
    Feature = ""
    for (w, c) in word_class : 
        if (c == "Product") : 
            Product += w 
            Product += " "
        
        elif (c == "Feature") :
            Feature += w 
            Feature += " "

    return(Product, Feature) 


def distance_measurement(s1, s2) :
    list1 = word_tokenize(s1)
    list2 = word_tokenize(s2)
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return (float(intersection) / union)


def best_similarity(Product) : 
    m = 0 
    i = 1
    l = i
    best_line = ""
    for line in Products['Description courte'] :
        dist = distance_measurement(Product, str(line)) 
        if dist > m : 
            m = dist 
            l = i 
            best_line = str(line)
        i = i+1 ; 
    return(m, l, best_line)



def main() : 
    phrase = "Quelle est la tension de fonctionnement du SIRCO 3x16 Ampères ?"
    (P, F) = question_treatement(phrase) 
    print("Produit :", P)
    print("Feature :", F) 
    (m, line, best_line) = best_similarity(P) 
    print("best distance :", m) 
    print("at line :" , line) 
    print("description :", best_line)

phrase2 = "Quelle est le voltage de l'interrupteur-sectionneur 3P 160A ?"

(P, F) = question_treatement(phrase2) 

print("Produit :", P) 
print("Feature :", F) 

print("Execution du main :") 
main() 