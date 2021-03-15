import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import json 

xls = pd.ExcelFile('product_data_1.xlsx')
Products = pd.read_excel(xls, 'Products', skiprows=[0])
clas = df1.iloc[3,4]
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

def Traitement_Question(question) :

    bag_of_words = word_tokenize(question)

    filtered_sentence = [] 

    for w in bag_of_words:  
        if w not in stop_words:  
            filtered_sentence.append(w) 

    for w in filtered_sentence :
        for key, value in synonymes.iteritems():
            if w == key:
                classe = value.class
                continue
    
    return classe




phrase = "Quelle est la tension de fonctionnement du SIRCO 3x16 Ampères ?"
