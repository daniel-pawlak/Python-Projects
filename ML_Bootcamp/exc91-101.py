# 91
"""Podane są dwa pliki: data_train.csv i target_train.csv. Dokonano pewnego przekształcenia zmiennych data i target. Wykorzystując klasę 
TfidfVectorizer z pakietu sklearn i dokonaj wektoryzacji tekstu znajdującego się w liście data i przypisz do zmiennej data_train_vectorized.  
Kształt macierzy wydrukuj"""

# import numpy as np
# import pandas as pd

# from sklearn.feature_extraction.text import TfidfVectorizer

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# categories = ['comp.graphics', 'sci.space']

# data_train = data_train['text'].tolist()
# target_train = target_train.values.ravel()

# vectorizer = TfidfVectorizer()
# data_train_vectorized = vectorizer.fit_transform(data_train)
# print(data_train_vectorized.shape)

# 92
"""Podane są dwa pliki: data_train.csv i target_train.csv. Dokonano pewnego przekształcenia zmiennych data i target. Wykorzystano klasę 
TfidfVectorizer z pakietu sklearn i dokonano wektoryzacji tekstu znajdującego się w liście data i przypisano do zmiennej data_train_vectorized.  
Wykorzystując klasę MultinomialNB zbuduj model klasyfikacji dokumentów tekstowych. Model wytrenuj w oparciu o dane data_train_vectorized oraz
target_train. Następnie dokonaj klasyfikacji poniższych zdań: 'The graphic designer requires a good processor to work' oraz 'Flights into space'. 
Wynik wydrukuj"""

# import numpy as np
# import pandas as pd

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB

# data_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data_train.csv')
# target_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\target_train.csv')

# categories = ['comp.graphics', 'sci.space']

# data_train = data_train['text'].tolist()
# target_train = target_train.values.ravel()

# vectorizer = TfidfVectorizer()
# data_train_vectorized = vectorizer.fit_transform(data_train)

# classifier = MultinomialNB()

# classifier.fit(data_train_vectorized, target_train)
# docs = ['The graphic designer requires a good processor to work', 'Flights into space']
# data_new = vectorizer.transform(docs)
# data_pred  = classifier.predict(data_new)

# for doc, category in zip(docs, data_pred):
#     print(f'\'{doc}\' => {categories[category]}')

# 93
"""Ustaw opcje pakietu pandas pozwalające na wyświetlenie 15 kolumn obiektu df oraz wyświetlenie długości linii składającej się ze 150 znaków.
Następnie wykorzystując funkcję load_boston() z pakietu sklearn załaduj dane do zmiennej raw_data. W oparciu o klucze 'data' oraz 'target' zmiennej
raw_data przygotuj df. Wydrukuj 5 pierwszych wierszy."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# print(df.head(5))

# 94
"""Podany jest obiekt df. Wyświetl korelację zmiennych ze zmienną docelową target w kolejności malejącej. Wynik wydrukuj."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# print(df.corr()['target'].sort_values(ascending=False)[1:])

# 95
"""Podany jest obiekt df. Skopiuj obiekt df do zmiennej data. Następnie wyrwij  kolumnę target ze zmiennej data i przypisz do zmiennej target. 
Wyświetl 5 wierszy data, pusta linia, 5 wierszy target"""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# # target = data['target']
# # data = data.drop(['target'], axis=1)

# # print(data.head(5), '\n\n', target.head(5))
# target = data.pop('target')
 
# print(data.head())
# print()
# print(target.head())

# 96
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Wykorzystując funkcję train... podziel dane
na zbiór treningowy i testowy (rs=42), i przypisz do zmiennych. Wyświetl kształty obiektów."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)
# print("data_train shape: {}".format(data_train.shape))
# print("data_test shape: {}".format(data_test.shape))
# print("target_train shape: {}".format(target_train.shape))
# print("target_test shape: {}".format(target_test.shape))

# 97
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Podzielono dane na zbiór treningowy i testowy 
(rs=42), i przypisano do zmiennych. Wykorzystując klasę LinearRegression zbuduj model regresji liniowej. Wyucz model i dokonaj oceny. Wynik wydrukuj"""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)

# regressor = LinearRegression()
# regressor.fit(data_train, target_train)
# print(f'R^2 score: {regressor.score(data_test, target_test):.4f}')

# 98
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Podzielono dane na zbiór treningowy i testowy 
(rs=42), i przypisano do zmiennych. Wykorzystując klasę LinearRegression zbudowano model regresji liniowej. Wyuczono model. Dokonaj predykcji na podstawie modelu danych testowych i wynik
przypisz do zmiennej target_pred. Wynik wydrukuj"""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)

# regressor = LinearRegression()
# regressor.fit(data_train, target_train)
# target_pred = regressor.predict(data_test)
# print(target_pred)

# 99
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Podzielono dane na zbiór treningowy i testowy 
(rs=42), i przypisano do zmiennych. Wykorzystując klasę LinearRegression zbudowano model regresji liniowej. Wyuczono model. Dokonano predykcji na podstawie modelu danych testowych i wynik
przypisano do zmiennej target_pred. Zbuduj nowy obiekt df o nazwie predictions, który będzie przechowywał 4 kolumny: target test i pred, error (różnica między pred i test), abs_error (wartość
bezwględna z error). Wydrukuj 10 pierwszych wierszy."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)

# regressor = LinearRegression()
# regressor.fit(data_train, target_train)
# target_pred = regressor.predict(data_test)
# error = target_pred - target_test
# abs_error = abs(error)

# columns = ['target_test', 'target_pred', 'error', 'abs_error']

# predictions = pd.DataFrame(columns=columns)
# predictions['target_test'] = target_test
# predictions['target_pred'] = target_pred
# predictions['error'] = error
# predictions['abs_error'] = abs_error
# # lub
# # predictions = pd.DataFrame(np.c_[target_test, target_pred], columns=['target_test', 'target_pred'])
# # predictions['error'] = predictions['target_pred'] - predictions['target_test']
# # predictions['abs_error'] = abs(predictions['error'])
# print(predictions.head(10))

# 100
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Podzielono dane na zbiór treningowy i testowy 
(rs=42), i przypisano do zmiennych. Wykorzystując klasę GradientBoostingRegressor zbuduj model regresji liniowej. Wyuczono model i dokonajj oceny. Wynik wydrukuj."""

# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import GradientBoostingRegressor

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)

# regressor = GradientBoostingRegressor(random_state=42)
# regressor.fit(data_train, target_train)
# print(f'R^2 score: {regressor.score(data_test, target_test):.4f}')

# 101
"""Podany jest obiekt df. Skopiowano obiekt df do zmiennej data. Następnie wyrwano  kolumnę target ze zmiennej data i przypisz do zmiennej target. Podzielono dane na zbiór treningowy i testowy 
(rs=42), i przypisano do zmiennych. Wykorzystano klasę GradientBoostingRegressor i zbudowano model regresji liniowej. Wyuczono model.
zapisz model (zmienna regressor) do pliku o nazwie model.pkl wykorzystując model pikle. Następnie wczytaj model.pkl do zmiennej regressor_loaded.
Wydrukuj info o tej zmiennej."""

# import pickle
# import numpy as np
# import pandas as pd

# from sklearn.datasets import load_boston
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import GradientBoostingRegressor

# pd.set_option("display.width", 150)
# pd.set_option("display.max_columns", 15)

# # raw_data = load_boston()
# import warnings
# with warnings.catch_warnings():
#     # You should probably not use this dataset.
#     warnings.filterwarnings("ignore")
#     raw_data = load_boston()
# df = pd.DataFrame(data=np.c_[raw_data.data, raw_data.target], columns=list(raw_data.feature_names) + ['target'])
# data = df.copy()
# target = data.pop('target')
 
# data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)

# regressor = GradientBoostingRegressor(random_state=42)
# regressor.fit(data_train, target_train)

# # pickle.dump(regressor, open('model.pkl', 'wb'))
# # regressor_loaded = pickle.load(open('model.pkl', 'rb'))
# # lub
# with open('model.pkl', 'wb') as file:
#     pickle.dump(regressor, file)
# with open('model.pkl', 'rb') as file:
#     regressor_loaded = pickle.load(file)

# print(regressor_loaded)