import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import json

xls = pd.ExcelFile('../product_data_1.xlsx', skiprows=[0])
Products = pd.read_excel(xls, 'Products')
Sirco = pd.read_excel(xls, 'EC000216')
Fuserbloc = pd.read_excel(xls, 'EC001040')
Diris = pd.read_excel(xls, 'EC002301')
Countis = pd.read_excel(xls, 'EC001506')

f = open('synonyms.json', "w")
# #fermer le pauvre json

n = Products.shape[0]

dictionary_list = []

for i in range (1,4) :
    ec = Products.iloc[i, 4]
    if (ec == 'EC000216')or(ec == 'EC001040')or(ec == 'EC002301')or(ec == 'EC001506'):
        d = {}
        d["name"] = Products.iloc[i,1]
        d["class"] = "Product"
        d["synonyms"] = word_tokenize(d["name"])
        dictionary_list.append(d)
json.dump(dictionary_list, f, indent=4)

print(Sirco)
