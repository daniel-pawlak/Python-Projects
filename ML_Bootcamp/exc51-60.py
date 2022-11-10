# 51
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując RandomForestClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych (ustaw argument random_state = 42). Dokonaj trenowania modelu na zbiorze treningowym oraz oceny na zbiorze testowym. 
Wydrukuj dokładność modelu do 4 m po przecinku"""
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)
# classifier = RandomForestClassifier(random_state=42)
# X_train = classifier.fit(X_train, y_train)
# ac = classifier.score(X_test, y_test)
# print(f'Accouracy: {ac:.4f}')

# 52
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując RandomForestClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych. Wykorzystując metodę przeszukiwania siatki oraz klasę GridSearchCV (ustaw argumenty 
scoring='accuarcy', cv = 5) znajdź optymalne wartości parametrów criterion, max_depth oraz min_samples_leaf. Wartości parametrów poszukaj z danych 
[dla criterion _> ['gini', 'entropy'], max depth -> [6, 7, 8], dla min_samples_leaf -> [4,5]] """
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import GridSearchCV

# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)
# classifier = RandomForestClassifier()
# params = {'criterion': ['gini', 'entropy'],
#         'max_depth': [6, 7, 8],
#         'min_samples_leaf': [4, 5]}
# grid_search = GridSearchCV(classifier, param_grid=params, scoring='accuracy', cv=5)
# grid_search.fit(X_train, y_train)
# print(grid_search.best_params_)
# print(grid_search.score(X_test, y_test))

# 53
"""Podana jest poniżej lista z dokumentami tekstowymi. Dokonaj wektoryzacji dokumentów za pomocą klasy 
CountVectiorizer z pakietu skleran. Wyświetl df"""
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer

# documents = [
#     'python is a programming language',
#     'python is popular',
#     'programming in python',
#     'object-oriented programming in python'
# ]
# vectorizer = CountVectorizer()
# # X = vectorizer.fit_transform(documents).toarray()
# df = pd.DataFrame(data=vectorizer.fit_transform(documents).toarray(), columns=vectorizer.get_feature_names())
# print(df)

# 54
"""Podana jest poniżej lista z dokumentami tekstowymi. Dokonaj wektoryzacji dokumentów za pomocą klasy 
CountVectiorizer z pakietu skleran. Użyj argumentu stop_words i ustaw jego wartość na 'english'. Wyświetl df"""
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer

# documents = [
#     'python is a programming language',
#     'python is popular',
#     'programming in python',
#     'object-oriented programming in python'
# ]
# vectorizer = CountVectorizer(stop_words='english')
# df = pd.DataFrame(data=vectorizer.fit_transform(documents).toarray(), columns=vectorizer.get_feature_names())
# print(df)

# 55
"""Podana jest poniżej lista z dokumentami tekstowymi. Dokonaj wektoryzacji dokumentów za pomocą klasy CountVectiorizer z pakietu skleran. 
Użyj argumentu stop_words i ustaw jego wartość na 'english'. Ustaw także odpowiedni argument, który pozwoli wydobyć n-gramy: unigramy i bigramy. 
Wyświetl df"""
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer

# documents = [
#     'python is a programming language',
#     'python is popular',
#     'programming in python',
#     'object-oriented programming in python',
#     'programming language'
# ]
# vectorizer = CountVectorizer(stop_words='english', ngram_range=(1, 2))
# df = pd.DataFrame(data=vectorizer.fit_transform(documents).toarray(), columns=vectorizer.get_feature_names())
# print(df)

# 56
"""Podana jest poniższa lista z dok tekst. Dokonaj wektoryzacji dokumentów wykorzystując klasę TfidVectorizer z pakietu sklearn. Wyświetl df"""
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer

# pd.set_option('display.width', 200)
# pd.set_option('display.max_columns', 10)
# pd.set_option('precision', 3)
# documents = [
#     'python is a programming language',
#     'python is popular',
#     'programming in python',
#     'object-oriented programming in python',
#     'programming language'
# ]
# vectorizer = TfidfVectorizer()
# df = pd.DataFrame(data=vectorizer.fit_transform(documents).toarray(), columns=vectorizer.get_feature_names())
# print(df)

# 57
"""Podana jest poniższa lista z dok tekst. Dokonaj wektoryzacji dokumentów wykorzystując klasę TfidVectorizer z pakietu sklearn. 
Używając argumentu stop_words usuń z wektoryzacji dwa słowa: "is" i "in". Wyświetl df"""
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer

# pd.set_option('display.width', 200)
# pd.set_option('display.max_columns', 10)
# pd.set_option('precision', 3)
# documents = [
#     'python is a programming language',
#     'python is popular',
#     'programming in python',
#     'object-oriented programming in python',
#     'programming language'
# ]
# vectorizer = TfidfVectorizer(stop_words=['is', 'in'])
# df = pd.DataFrame(data=vectorizer.fit_transform(documents).toarray(), columns=vectorizer.get_feature_names())
# print(df)

# 58
"""Wczytaj plik data.csv do obiektu df (zmienne x1 x2). Następnie zaimplementuj algorytm K-średnich pozwalających rodzielić podane dane 
na dwa klastry. Wyznacz centroid każdego klastra i wydrukuj współrzędne do konsoli. Zaokrąglij do 3 m po przecinku."""
# import numpy as np
# from numpy.linalg import norm
# import pandas as pd
# import random

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data3.csv')

 
# x1_min = df.x1.min()
# x1_max = df.x1.max()
 
# x2_min = df.x2.min()
# x2_max = df.x2.max()
 
# centroid_1 = np.array([random.uniform(x1_min, x1_max), random.uniform(x2_min, x2_max)])
# centroid_2 = np.array([random.uniform(x1_min, x1_max), random.uniform(x2_min, x2_max)])
 
# data = df.values
 
# for i in range(10):
#     clusters = []
#     for point in data:
#         centroid_1_dist = norm(centroid_1 - point)
#         centroid_2_dist = norm(centroid_2 - point)
#         cluster = 1
#         if centroid_1_dist > centroid_2_dist:
#             cluster = 2
#         clusters.append(cluster)
 
#     df['cluster'] = clusters
 
#     centroid_1 = [round(df[df.cluster == 1].x1.mean(), 3), round(df[df.cluster == 1].x2.mean(), 3)]
#     centroid_2 = [round(df[df.cluster == 2].x1.mean(), 3), round(df[df.cluster == 2].x2.mean(), 3)]
 
# print(centroid_1)
# print(centroid_2)

# 59
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę KMeans z pakietu sklearn 
dokonaj podziału danych na trzy klastry. Ustaw argumenty max_iter=1000 i random_state=42. Wydrukuj współrzędne środka każdego klastra."""
# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# kmeans = KMeans(n_clusters = 3, random_state = 42, max_iter=1000)
# kmeans.fit(df)
# print(kmeans.cluster_centers_)

# 60
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę KMeans z pakietu sklearn 
dokonano podziału danych na trzy klastry. Dokonaj predykcji na podstawie zbudowanego modelu kmeands i przypisz numer klastra do każdej próbki 
w obiekcie df(nadaj nazwę kolumny 'y_kmeans'). Wyświetl 10 pierwszych wierszy df"""
# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# kmeans = KMeans(n_clusters = 3, random_state = 42, max_iter=1000)
# kmeans.fit(df)
# df['y_kmeans'] = kmeans.predict(df)
# print(df.head(10))
