import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import json 

#incroyable ça marche youpi
xls = pd.ExcelFile('product_data_1.xlsx')
df1 = pd.read_excel(xls, 'Products', skiprows=[0])
clas = df1.iloc[3,4]
df2 = pd.read_excel(xls, clas)

test = 'sirco 3   *16 A, 43X     9'
m = re.sub('([0-9]+) *[xX*] *([0-9]+)', "\g<1>x\g<2>", test)
print(m)
#tokenisation et tout

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


phrase = "Quelle est la tension de fonctionnement du SIRCO 3x16 Ampères ?"

phrase2 = "Bonjour interrupteur svp" 

phrase = phrase.lower()
phrase2 = phrase2.lower()

#remplacer l'étoile par un x et supprimer les espaces autour seulement si c des nombres 
#regex AHH 
#aled

bag_of_words_1 = word_tokenize(phrase) 
print(bag_of_words_1)

bag_of_words_2 = word_tokenize(phrase2) 

filtered_sentence_1 = []  
  
for w in bag_of_words_1:  
    if w not in stop_words:  
        filtered_sentence_1.append(w)  

print(filtered_sentence_1)

filtered_sentence_2 = []  
  
for w in bag_of_words_2:  
    if w not in stop_words:  
        filtered_sentence_2.append(w)  

print(filtered_sentence_2)

#print(df1.columns)

#print(df1["Description courte"].str.find('Sirco'))

count = 1 
for line in df1['Description courte'] :
    if "sirco " in str(line).lower() :
        print (line, "at line :", count) 
        print("Product ID :", df1['Product ID'][count], "\n")
    count += 1 

#faire une mesure de distance entre notre bout de phrase et les descriptions courtes !!!! 
#__________________#

#Lecture de synonymes.dat 

f = open('synonymes.json')
synonymes = json.load(f)


print(synonymes)

print(json.dumps(synonymes, indent = 4))