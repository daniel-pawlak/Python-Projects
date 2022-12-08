# 81
"""Wczytaj podany plik factory.csv do obiektu df. Plik zawiera dwie zmienne item_length oraz item_width. Wykorzystując klasę IsolationForest 
z pakietu sklearn dokonaj analizy elementów odstających na podanym zbiorze. Przekaż argumenty: n_estimators=100, contamination=0.05, 
random_state=42. 1 normalny element, -1 odstający. Przypisz nową kolumnę do obiektu df o nazwie 'outlier_flag', która będzie przechowywać, czy dana próbka 
jest elementem normalnym czy odstającym. Wydrukuj 10 pierwszych wierszy."""

# import numpy as np
# import pandas as pd
# from sklearn.ensemble import IsolationForest

# np.random.seed(42)

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\factory.csv')

# clf = IsolationForest(random_state=42, n_estimators=100, contamination=0.05)
# y = clf.fit_predict(df)

# df['outlier_flag'] = y
# print(df.head(10))

# 82
"""Wczytano podany plik factory.csv do obiektu df. Plik zawiera dwie zmienne item_length oraz item_width. Wykorzystano klasę IsolationForest 
z pakietu sklearn i dokonano analizy elementów odstających na podanym zbiorze. Przekaż argumenty: n_estimators=100, contamination=0.05, 
random_state=42. 1 normalny element, -1 odstający. Przypisano nową kolumnę do obiektu df o nazwie 'outlier_flag', która będzie przechowywać, czy dana próbka 
jest elementem normalnym czy odstającym. Zbadaj liczbę elementów odstających w zbiorze, tzn. zbadaj rozkład kolumny outlier_flag. Wydrukuj."""

# import numpy as np
# import pandas as pd
# from sklearn.ensemble import IsolationForest

# np.random.seed(42)

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\factory.csv')

# clf = IsolationForest(random_state=42, n_estimators=100, contamination=0.05)
# y = clf.fit_predict(df)

# df['outlier_flag'] = y
# print(df['outlier_flag'].value_counts())

# 83
"""Wykorzystując funkcję load_digits() z pakietu sklearn załaduj dane dotyczące obrazów o rozdzielczości 8x8 pikseli do zmiennych:
data - obrazy zapisane w postaci tablic numpy kształtu (64,)
target - etykiety, cyfry widoczne na obrazach 
Zapoznaj się dokładnie z podanym zbiorem. Spróbuj wyświetlić kilka przykładowych obrazów. W celu wyświetlenia obrazu można użyć pakietu matplotlib.
Zmieniając wartość idx wyświetl kilka obrazów. W odpowiedzi wydrukuj etykietę dla obrazu z indexem 250"""

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# from sklearn.datasets import load_digits
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split


# np.random.seed(42)
# data, target = load_digits(return_X_y=True)

# idx = 250
# # plt.imshow(data[idx].reshape(8, 8), cmap='gray_r')
# # plt.title(f'Label: {target[idx]}')
# # plt.show()
# print(target[idx])

# 84
"""Wykorzystując funkcję load_digits() z pakietu sklearn załaduj dane dotyczące obrazów o rozdzielczości 8x8 pikseli do zmiennych:
data - obrazy zapisane w postaci tablic numpy kształtu (1797, 64)
target - etykiety, cyfry widoczne na obrazach w postaci tablicy numpy o kształcie (1797, ) 
Dokonaj standaryzacji zmiennej data. Używając train_test_split() (random_state=42) podziel dane na zbiór test i train. Wyświetl kształty."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_digits
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split

# np.random.seed(42)
# data, target = load_digits(return_X_y=True)
# data = data / data.max()    # standaryzacja
# X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)
# print('{} shape: {}'.format('X_train', X_train.shape))
# print('{} shape: {}'.format('X_test', X_test.shape))
# print('{} shape: {}'.format('y_train', y_train.shape))
# print('{} shape: {}'.format('y_test', y_test.shape))

# 85
"""Wykorzystując funkcję load_digits() z pakietu sklearn załaduj dane dotyczące obrazów o rozdzielczości 8x8 pikseli do zmiennych:
data - obrazy zapisane w postaci tablic numpy kształtu (1797, 64)
target - etykiety, cyfry widoczne na obrazach w postaci tablicy numpy o kształcie (1797, ) 
Dokonano standaryzacji zmiennej data. Używając train_test_split() (random_state=42) podzielono dane na zbiór test i train. Wykorzystując klasę
KNeighborsClassifier z pakietu sklearn zbuduj model klasyfikacji wieloklasowej. Wyucz model na danych treningowych i następnie dokonaj oceny na 
danych testowych. Wyświetl dokładność modelu."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_digits
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split

# np.random.seed(42)
# data, target = load_digits(return_X_y=True)
# data = data / data.max()    # standaryzacja
# X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)

# clf = KNeighborsClassifier()
# clf.fit(X_train, y_train)

# acc = clf.score(X_test, y_test)
# print(f'KNN accuracy: {acc:.4f}')

# 86
"""Wykorzystując funkcję load_digits() z pakietu sklearn załaduj dane dotyczące obrazów o rozdzielczości 8x8 pikseli do zmiennych:
data - obrazy zapisane w postaci tablic numpy kształtu (1797, 64)
target - etykiety, cyfry widoczne na obrazach w postaci tablicy numpy o kształcie (1797, ) 
Dokonano standaryzacji zmiennej data. Używając train_test_split() (random_state=42) podzielono dane na zbiór test i train. Wykorzystując klasę
LogisticRegression z pakietu sklearn zbuduj model klasyfikacji wieloklasowej. Wyucz model na danych treningowych i następnie dokonaj oceny na 
danych testowych. Wyświetl dokładność modelu."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_digits
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split

# np.random.seed(42)
# data, target = load_digits(return_X_y=True)
# data = data / data.max()    # standaryzacja
# X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=42)

# reg = LogisticRegression()
# reg.fit(X_train, y_train)

# acc = reg.score(X_test, y_test)
# print(f'KNN accuracy: {acc:.4f}')

# 87
"""Podane są dwa pliki: data_train.csv i target_train.csv. Plik data zawiera maile dotyczące dwóch kategorii: grafiki komputerowej (comp.graphics)
oraz przestrzenie kosmicznej (sci.space). Plik target zawiera odpowiednio etykiety (0 - comp, 1- sci). Wczytaj zawartość plików jako obiekty df w 
odpowiednich nazwach. Wydrukuj 2 element data. """

# import numpy as np
# import pandas as pd

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# print(data_train['text'][1])

# 88
"""Podane są dwa pliki: data_train.csv i target_train.csv. Plik data zawiera maile dotyczące dwóch kategorii: grafiki komputerowej (comp.graphics)
oraz przestrzenie kosmicznej (sci.space). Plik target zawiera odpowiednio etykiety (0 - comp, 1- sci). Wczytaj zawartość plików jako obiekty df w 
odpowiednich nazwach. Przekształć obiekt  data do postaci listy i przypisz zmiany na stałe do zmiennej data. Wydrukuj długość listy. """

# import numpy as np
# import pandas as pd

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# data_train = list(data_train['text'])
# # lub data_train = data_train['text'].tolist()
# print(len(data_train))

# 89
"""Podane są dwa pliki: data_train.csv i target_train.csv. Plik data zawiera maile dotyczące dwóch kategorii: grafiki komputerowej (comp.graphics)
oraz przestrzenie kosmicznej (sci.space). Plik target zawiera odpowiednio etykiety (0 - comp, 1- sci). Wczytaj zawartość plików jako obiekty df w 
odpowiednich nazwach. Dokonano pewnego przekształcenia zmiennych data i target. Wykorzystując klasę CountVectorizer z pakietu sklearn dokonaj
wektoryzacji tekstu znajdującego się w liście data i przypisz do zmiennej data_train_vectorized. Wydrukuj kształt macierzy rzadkiej (sparse matrix)"""

# import numpy as np
# import pandas as pd

# from sklearn.feature_extraction.text import CountVectorizer

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# data_train = data_train['text'].tolist()
# target_train = target_train.values.ravel()

# cv = CountVectorizer()
# data_train_vectorized = cv.fit_transform(data_train)
# print(data_train_vectorized.shape)

# 90
"""Podane są dwa pliki: data_train.csv i target_train.csv. Dokonano pewnego przekształcenia zmiennych data i target. Wykorzystano klasę 
CountVectorizer z pakietu sklearn i dokonano wektoryzacji tekstu znajdującego się w liście data i przypisano do zmiennej data_train_vectorized. 
Wykorzystując klasę MultinomialNB zbuduj model klasyfikacji dokumentów tekstowych. Model wytrenuj w oparciu o dane data_train_vectorized oraz
target_train. Następnie dokonaj klasyfikacji poniższych zdań: 'The graphic designer requires a good processor to work' oraz 'Flights into space'. 
Wynik wydrukuj"""

# import numpy as np
# import pandas as pd

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# categories = ['comp.graphics', 'sci.space']

# data_train = data_train['text'].tolist()
# target_train = target_train.values.ravel()

# vectorizer = CountVectorizer()
# data_train_vectorized = vectorizer.fit_transform(data_train)

# mnb = MultinomialNB()

# mnb.fit(data_train_vectorized, target_train)
# docs = ['The graphic designer requires a good processor to work', 'Flights into space']
# data_new = vectorizer.transform(docs)
# data_pred  = mnb.predict(data_new)

# for doc, category in zip(docs, data_pred):
#     print(f'\'{doc}\' => {categories[category]}')