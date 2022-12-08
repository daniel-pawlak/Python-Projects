from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
# 21
"""Zbuduj model regresji logistycznej (ustaw max_iter=100, reszta default), wykorzystując sklearn i IRIS. 
Model wytrenuj na danych treningowych i następnie dodaj oceny modelu na zbiorze testowym.
W odpowiedzi wydrukuj dokładność modelu na zbiorze testowym jak poniżej."""
# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']
# data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.3, random_state=20)
# regressor = LogisticRegression(max_iter=100)
# regressor.fit(data_train, target_train)
# target_pred = regressor.predict(data_test)    # predykcja
# cm = confusion_matrix(target_test, target_pred)
# print(cm)
# print(accuracy_score(target_test, target_pred))

# # lub
# model = LogisticRegression(max_iter=1000)
# model.fit(data_train, target_train)
# accuracy = model.score(data_test, target_test)    # ocena
# print(f'Accuracy: {accuracy:.4f}')

# 22
""""Zbudowano model regresji logistycznej przy użyciu sklearn i danych IRIS. Dokonaj predykcji danych testowych na podstawie modelu i przypisz do zmiennej target_pred. Wyświetl ją"""
# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']
# data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.3, random_state=20)

# model = LogisticRegression(max_iter=1000)
# model.fit(data_train, target_train)
# target_pred = model.predict(data_test)
# print(target_pred)

# 23
""""Zbudowano model regresji logistycznej przy użyciu sklearn i danych IRIS. Dokonano predykcji danych testowych na podstawie modelu i przypisano do zmiennej target_pred. Wyznacz macierz pomyłek"""
# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']
# data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.3, random_state=20)

# model = LogisticRegression(max_iter=1000)
# model.fit(data_train, target_train)
# target_pred = model.predict(data_test)
# cm = confusion_matrix(target_test, target_pred)
# print(cm)

# 24
""""Zbudowano model regresji logistycznej przy użyciu sklearn i danych IRIS. Dokonano predykcji danych testowych na podstawie modelu i przypisano do zmiennej target_pred. 
Wyświetl raport klasyfikacji modelu wykorzystując funkcję classification_report()"""
# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']
# data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.3, random_state=20)

# model = LogisticRegression(max_iter=1000)
# model.fit(data_train, target_train)
# target_pred = model.predict(data_test)

# cr = classification_report(target_test, target_pred)
# print(cr)

# 25
"""Podany obiekt DataFrame. Wykorzystując klase LabelEncoder z sklearn dokonaj kodowania 0-1 kolumny bought. Przypisz zmiany do obiektu df. Wydrukuj df"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# data = {
#     'size': ['XL', 'L', 'M', 'L', 'M'],
#     'color': ['red', 'green', 'blue', 'green', 'red'],
#     'gender': ['female', 'male', 'male', 'female', 'female'],
#     'price': [199.0, 89.0, 99.0, 129.0, 79.0],
#     'weight': [500, 450, 300, 380, 410],
#     'bought': ['yes', 'no', 'yes', 'no', 'yes']
# }

# df = pd.DataFrame(data=data)
# for col in ['size', 'color', 'gender', 'bought']:
#     df[col] = df[col].astype('category')
# df['weight'] = df['weight'].astype('float')
# le = LabelEncoder()
# df['bought'] = le.fit_transform(df['bought'])
# print(df)

# 26
"""Podany obiekt DataFrame. Wykorzystując klase OneHotEncoder z sklearn dokonaj kodowania 0-1 kolumny size (sparse=False). 
Wydrukuj zakodowaną postać kolumny size bez przypisywania do df oraz otrzyman kategorie przy kodowaniu kolumny size"""
from sklearn.preprocessing import OneHotEncoder

# data = {
#     'size': ['XL', 'L', 'M', 'L', 'M'],
#     'color': ['red', 'green', 'blue', 'green', 'red'],
#     'gender': ['female', 'male', 'male', 'female', 'female'],
#     'price': [199.0, 89.0, 99.0, 129.0, 79.0],
#     'weight': [500, 450, 300, 380, 410],
#     'bought': ['yes', 'no', 'yes', 'no', 'yes']
# }

# df = pd.DataFrame(data=data)
# for col in ['size', 'color', 'gender', 'bought']:
#     df[col] = df[col].astype('category')
# df['weight'] = df['weight'].astype('float')
# encoder = OneHotEncoder(sparse=False)
# encoder.fit(df[['size']])
# print(encoder.transform(df[['size']]))
# print(encoder.categories_)

# 27 
"""Załaduj dane Breast Cancer Data wykorzystują funkcję load_breas_cancer() z pakietu sklearn do zmiennej raw)data. 
Następnie wydrukuj informacje o tym zbiorze do konsoli (zawartość klucza 'DESCR')"""
from sklearn.datasets import load_breast_cancer

# raw_data = load_breast_cancer()
# print(raw_data['DESCR'])

# 28
"""Poniżej załadowano zbiór Breast Cancer Data do zmiennej. Przypisz do zmiennej data tablicę numpy z danymia ze zmiennej raw_data 
(zawartość klucza data) oraz do zmiennej target tabblicę numpy ze zmienną docelową (zawartość klucza target)"""
import numpy as np

# np.set_printoptions(precision=2, suppress=True, linewidth=100)
# raw_data = load_breast_cancer()

# data = raw_data['data']
# target = raw_data['target']
# print(data[:3])

# 29
"""Połącz tablice data i target w jedną all_data i wyświetl 3 pierwsze wiersze"""
# np.set_printoptions(precision=2, suppress=True, linewidth=100)
# raw_data = load_breast_cancer()

# data = raw_data['data']
# target = raw_data['target']

# all_data = np.c_[data, target]
# print(all_data[:3])

# 30
"""Połączono tablice data i target w jedną all_data. Utwórz z tablicy all_data obiekt DataFrame nadając 
odpowiednio nazwy kolumn (zawartość klucza feature_names obiektu raw_data + nazwa zmiennej docelowej jako target)"""
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 200)
np.set_printoptions(precision=2, suppress=True, linewidth=100)
raw_data = load_breast_cancer()

data = raw_data['data']
target = raw_data['target']
all_data = np.c_[data, target]
df = pd.DataFrame(data = all_data, columns = list(raw_data['feature_names']) + ['target'])
print(df)

