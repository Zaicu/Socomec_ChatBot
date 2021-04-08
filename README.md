* filter_the_sentence(sentence) : 

normalise les groupes du mots du type "3*16", "3 X 16" -> 3x16 (supprime les espaces et remplace * ou X par x).

Lorsqu'un nombre est suivi d'une unité, on en garde que l'initiale. 15 Ampères -> 15A.

Enlève les stop words : les mots qui ne sont pas porteur de sens (articles, mots interrogatifs, ponctuation...)

Renvoie la phrase filtrée sous forme de sac de mots (un tableau de mots). 



* distance_measurement(s1, s2) :

Il s'agit de la distance de Jaccard, qui est utilisée en deuxième instance pour identifier le produit dans la base de données. 


* best_similarity(product) :

Cette fonction recherche, pour un produit donné, la description (courte ou longue) correspondant le mieux, et renvoie la description en question ainsi que son numéro de ligne, et la distance avec le produit initialement passé en argument. 


* set_product() : 

Cette fonction permet de générer le "dictionnaire de synonymes" des produits, en prenant chaque mot des descriptions courtes et longues de tous les produits de la base de données, en retirant les doublons. 


* word_similarity(set, sentence) : 

set : il s'agit du dictionnaire de synonymes (des produits ou des features) 

Cette fonction fait appel à la mesure de distance "edit distance". Pour chaque mot de la phrase (sentence), on cherche dans le dictionnaire des synonymes (set) le mot qui s'en rapproche le plus. On renvoie la liste des mots trouvés. 


* identify_product(best_matches) : 

L'argument best_matches correspond à la liste de mot renvoyée par la fonction précédente word_similarity(set, sentence). 

Cette fonction ne va conserver que les mots assez proches des mots initiaux. 


* identify_feature(best_matches) :

Même principe mais pour les caractéristiques. 


* ambiguous_words(product, feature, sentence) : 

pour chaque mot ambigu (qui pourrait faire partie de la description produit, ou être la caractéristique recherchée), cette fonction permet de déterminer quelle est la réelle utilité du mot. 

En sortie de cette fonction, le produit et la feature sont clairement identifiés. 

* product_id(product) :

Avec le produit clairement identifié, on utilise la fonction best_similarity(product) pour trouver l'identifiant du produit dans la base de données. 


* main() :

la fonction main permet de faire tourner le programme, elle appelle les fonctions dans l'ordre et affiche quelques résultats. 