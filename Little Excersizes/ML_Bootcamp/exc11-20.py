import pandas as pd

# 11
"""Dokonaj kodowania 0-1 obiektu df (kol. weight_cut) dzięki funkcji pd.get_dummies(). W odpowiedzi wynik kodowania wydrukuj do konsoli"""
# df = pd.DataFrame(data={'weight': [75., 78.5, 85., 91., 84.5, 83., 68.]})
# df['weight_cut'] = pd.cut(df['weight'], bins=(60, 75, 80, 95), labels=['light', 'normal', 'heavy'])
# df = pd.get_dummies(df)
# print(df)

# 12
"""Do obiektu df przypisz nową kolumnę, która przyjmie liczbę elementów z listy w kolumnie currency"""
# data_dict = {
#     'currency': [['PLN', 'USD'], ['EUR', 'USD', 'PLN', 'CAD'], ['GBP'], ['JPY', 'CZK', 'HUF'], []]
# }
# df = pd.DataFrame(data=data_dict)
# df['number'] = df['currency'].apply(len)
# print(df)

# 13
"""Do obiektu df przypisz nową kolumnę o nazwie 'PLN_flag', która przyjmie wartość 1, gdy waluta PLN będzie w liście w kolumnie currency i przeciwnie 0."""
"""BARDZO WAŻNE"""
# data_dict = {
#     'currency': [['PLN', 'USD'], ['EUR', 'USD', 'PLN', 'CAD'], ['GBP'], ['JPY', 'CZK', 'HUF'], []]
# }
# df = pd.DataFrame(data=data_dict)
# df['PLN_flag'] = df['currency'].apply(lambda item: 1 if 'PLN' in item else 0)
# print(df)

# 14
"""Podziel wartości kolumny hashtags względem znaku hash # używając pdSeries z argumente expand=True. Otrzymasz 4 kolumny"""

# df = pd.DataFrame(data={'hashtags': ['#good#vibes', '#hot#summer#holiday', '#street#food', '#workout']})
# df = df['hashtags'].str.split('#', expand=True)
# df = df.drop(columns=[0])
# df.columns = ['hashtag1', 'hashtag2', 'hashtag3']
# print(df)

# 15
"""Utwórz nową kolumnę missing i przypisz do niej liczbę brakujących hashtagów dla każdego wiersza"""

# df = pd.DataFrame(data={'hashtags': ['#good#vibes', '#hot#summer#holiday', '#street#food', '#workout']})
# df = df['hashtags'].str.split('#', expand=True)
# df = df.drop(columns=[0])
# df.columns = ['hashtag1', 'hashtag2', 'hashtag3']
# df['missing'] = df.isnull().sum(axis=1)
# print(df)

# 16
"""Przygotuj kolumnę investmenrs do modelu - przekształć na typ int"""

# df = pd.DataFrame(data={'investments': ['100_000_000', '100_000', '30_000_000', '100_500_000']})
# df = df.astype('int32')
# # lub wg kursu df['investments'] = df['investments'].str.replace('_', '').astype(int)
# print(df)

# 17 
"""Załaduj zbiór danych IRIS do zmiennej data wykorzystując pakiet scikit-learn oraz funkcję load_iris(). Wyświetl klucze zmiennej data"""
from sklearn.datasets import load_iris

# data = load_iris()
# print(data.keys())

# 18 
"""Wyświetl nazwy zmiennych (klucz feature names) oraz nazwy klas (klucz target names) w zbiorze IRIS"""

# data = load_iris()
# print(data['feature_names'])
# print(data['target_names'])

# 19
"""Do zmiennej data przypisz dane zbuory IRIS (klucz data). Do zmiennej target przypisz wartości zmiennej docelowej (klucz targer) ze zbioru IRIS"""

# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']
# print(data.shape)
# print(target.shape)

# 20
"""Wykorzystując sklearn i funkcję train_test_split() podziel dane na zbiór treningowy (data_train, target_train) i testowy (data_test, target_test). Ustal rozmiar test na 30%"""

from sklearn.model_selection import train_test_split

# data_raw = load_iris()
# data = data_raw['data']
# target = data_raw['target']

# data_train, data_test, target_train, target_test = train_test_split(data, target, test_size = 0.3)
# print('data_train shape:', data_train.shape)
# print('target_train shape:', target_train.shape)
# print('data_test shape:', data_test.shape)
# print('target_test shape:', target_test.shape)