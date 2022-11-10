# 31
"""Wykorzystując funkcję train_test_split() z pakietu sklearn podziel dane na zbiór treningowu i testowy. 
Ustaw argument random_state=40 oraz rozmiar zbioru testowego na 25%. Wydrukuj rozmiary tablic."""
# import numpy as np
# import pandas as pd
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split


# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 200)
# np.set_printoptions(precision=2, suppress=True, linewidth=100)
# raw_data = load_breast_cancer()

# data = raw_data['data']
# target = raw_data['target']

# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.25, random_state=40)
# print('X_train shape', X_train.shape)
# print('y_train shape', y_train.shape)
# print('X_test shape', X_test.shape)
# print('y_test shape', y_test.shape)
# print(f'X_train shape {X_train.shape}')     # druga opcja

# 32
"""Dane są tablice data, targer X train i test, y train i test. Sprawdź procentowy rozkład wartości zmiennych targer, y train i y test. Wydrukuj"""
# import numpy as np
# import pandas as pd
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split


# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 200)
# np.set_printoptions(precision=2, suppress=True, linewidth=100)
# raw_data = load_breast_cancer()

# data = raw_data['data']
# target = raw_data['target']

# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.25, random_state=40)

# for name, array in zip(['target', 'y_train', 'y_test'], [target, y_train, y_test]):
#     print(f'{name.ljust(7)}:{np.unique(array, return_counts=True)[1] / len(array)}')

# 33
"""Dane są tablice data i target. Podziel adne na zbiór treningowy i testowy tak, 
aby zachować rozkład wartości w tablicach y train i y test tak jak w tablicy target. Następnie sprawdź procentowy rozkład target, y train i test"""
# import numpy as np
# import pandas as pd
# from sklearn.datasets import load_breast_cancer
# from sklearn.model_selection import train_test_split


# pd.set_option('display.max_columns', 10)
# pd.set_option('display.width', 200)
# np.set_printoptions(precision=2, suppress=True, linewidth=100)
# raw_data = load_breast_cancer()

# data = raw_data['data']
# target = raw_data['target']
# target_percentage = np.unique(target, return_counts=False)[1] / len(target)
# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.25, random_state=40, stratify=target)

# for name, array in zip(['target', 'y_train', 'y_test'], [target, y_train, y_test]):
#     print(f'{name.ljust(7)}:{np.unique(array, return_counts=True)[1] / len(array)}')

# 34 
"""Podany jest obiekt df. Pierwsza kolumna opisuje lata pracy, druga wynagrodzenie. 
Wykorzystując równanie normalne oraz pakiet numpy znajdź równanie regresji liniowej i wydrukuj."""
# import numpy as np
# import pandas as pd

# df = pd.DataFrame({'years': [1, 2, 3, 4, 5, 6],
#                    'salary': [4000, 4250, 4500, 4750, 5000, 5250]})
# m = len(df)
 
# X1 = df['years'].values
# Y = df['salary'].values

# X1 = X1.reshape(m, 1)
# bias = np.ones((m, 1))
# X = np.append(bias, X1, axis=1)
# print(X) 
# coefs = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, Y))
# print(f'Linear regression: {coefs[0]:.2f} + {coefs[1]:.2f}x')

# 35
"""Podany jest obiekt df. Pierwsza kolumna opisuje lata pracy, druga wynagrodzenie. 
Wykorzystując sklearn i LinearRegression znajdź równanie regresji liniowej i wydrukuj."""
# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression

# df = pd.DataFrame({'years': [1, 2, 3, 4, 5, 6],
#                    'salary': [4000, 4250, 4500, 4750, 5000, 5250]})
# model = LinearRegression()
# model.fit(df[['years']], df[['salary']])
# print(f'Linear regression: {model.intercept_[0]:.2f} + {model.coef_[0][0]:.2f}x')

# 36 
"""Wczytaj dane z pliku data.csv do obiektu df. Następnie zbuduj model regresji liniowej do przewidywania wartości target. Dokonaj oceny modelu"""
# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data.csv')
# data = df[['variable']]
# target = df['target']
 
# model = LinearRegression()
# model.fit(data, target)
# print(f'{model.score(data, target):.4f}')

# 37
"""Wczytaj dane z pliku data.csv do obiektu df. 
Następnie dokonaj ekstrakcji cech wielomianowych ze zmiennej var1 stopnia drugiego. Otrzymane cechy w postaci numpy wyświetl do konsoli"""

# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import PolynomialFeatures

# np.set_printoptions(suppress=True, precision=3)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data.csv')

# poly = PolynomialFeatures(degree=2)
 
# df_poly = poly.fit_transform(df)
# print(df_poly)

# 38
"""Wczytaj dane z pliku data.csv do obiektu df. 
Następnie dokonaj ekstrakcji cech wielomianowych ze zmiennych var1 oraz var2 stopnia trzeciego. Otrzymane cechy w postaci numpy wyświetl do konsoli"""

# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import PolynomialFeatures

# np.set_printoptions(suppress=True, precision=3, linewidth=150)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data.csv')

# poly = PolynomialFeatures(degree=3)
 
# df_poly = poly.fit_transform(df)
# print(df_poly)

# 39
"""Plik predictions.csv zawiera predukcje pewnego modelu regresji: ytrue zawiera rzeczywiste wartości, ypred przewidziane przez model. 
Wczytaj ten plik. Następnie zaimplementuj funkkcję o nazwie mean_absolute_error() obliczającą średni bląd bezwględny predykcji. 
Wykorzystując zaimplementowaną funkcję policz wartość MAE la tego modelu. Wynik wydrukuj do konsoli tak jak pokazano poniżej."""

# import numpy as np
# import pandas as pd
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\predictions.csv')

# def mean_absolute_error(y_true, y_pred):
#     return abs(y_true - y_pred).sum() / len(y_true)
 
# mae = mean_absolute_error(df['y_true'], df['y_pred'])
# print(f'MAE = {mae:.4f}')

# 40
"""Plik predictions.csv zawiera predukcje pewnego modelu regresji: ytrue zawiera rzeczywiste wartości, ypred przewidziane przez model. 
Wczytaj ten plik. Następnie zaimplementuj funkkcję o nazwie mean_squared_error() obliczającą błąd średniokwadratowy predykcji. 
Wykorzystując zaimplementowaną funkcję policz wartość MSE la tego modelu. Wynik wydrukuj do konsoli tak jak pokazano poniżej."""

# import numpy as np
# import pandas as pd
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\predictions.csv')

# def mean_squared_error(y_true, y_pred):
#     return ((y_true - y_pred) ** 2).sum() / len(y_true)
 
# mse = mean_squared_error(df['y_true'], df['y_pred'])
# print(f'MSE = {mse:.4f}')