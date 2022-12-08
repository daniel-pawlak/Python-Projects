# 41
"""Podany jest obiekt df. Zaimplementuj funkcję sigmoid() wykorzystując bibliotekę numpy. Postać funkcji sigmoid f(x) = 1/(1+e^-x).
Korzystając z zamiplementowanej funkcji policz jej wartość dla zmiennej var` i przypisz do kolumny i nazwie var1_sigmoid. Wyświetl obiekt df do konsoli"""
# import numpy as np
# import pandas as pd

# np.random.seed(42)
# df = pd.DataFrame(data=np.random.randn(10), columns=['var1'])

# def sigmoid(x):
#     return 1 / (1 + np.e ** (-x))

# df['var1_sigmoid'] = sigmoid(df[['var1']].values)
# # lub df['var1_sigmoid'] = df['var1'].apply(sigmoid)

# print(df)

# 42
"""Wczytaj plik data.csv do df. Następnie wykorzystując klasę StandardScaler z sklearn dokonaj standaryzacji wszystkich kolumn. Wyświetl df."""
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# np.set_printoptions(precision=4, suppress=True)
# sc = StandardScaler()
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\data2.csv')
# df = sc.fit_transform(df)
# print(df)

# 43
"""Wczytaj pliki Xtrain.csv i i Xtest.csv odpowiednio do obiektów df o takich nazwach. Następnie dokonaj standaryzacji danych. Dane dopasuj
na zbiorze treningowym. W odpowiedzi wydrukuj 5 pierwszych wierszy tak przetworzonych obiektów Xtrain i Xtest"""
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# np.set_printoptions(precision=4, suppress=True)
# sc = StandardScaler()
# X_train = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\X_train.csv')
# X_test = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\X_test.csv')

# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)
# print(X_train[:5])
# print(X_test[:5])
# # # alternatywnie
# # sc.fit(X_train)
# # X_train = sc.transform(X_train)
# # X_test = sc.transform(X_test)

# 44
"""Zaimplementuj funkcję entropy() wykorzystując numpy. Wynik zaokrąglij do czwartego miejsca po przecinku. Wykorzystując tę funkcję wyznacz trzecią
kolumnę obiektu fg o nazwie entropy zawierającą entropię dla poszczególnych wierszy. Wydrukuj df."""

# import numpy as np
# import pandas as pd

# def entropy(x):
#     return np.round(-np.sum(x * np.log2(x)), 4)

# df = pd.DataFrame({'val_1': np.arange(0.01, 1.0, 0.1), 'val_2': 1 - np.arange(0.01, 1.0, 0.1)})
# # df['entropy'] = df['val_1'].apply(entropy) + df['val_2'].apply(entropy)
# # print(df)
# # dokładniejsze
# # df['entropy'] = [entropy([row[1][0], row[1][1]]) for row in df.iterrows()]

# 45
"""W pliku predictions.csv znajdują się wyniki predycji na podstawie pewnego modelu klasyfikacji wieloklasowej (3 klasy). Kolumna ytrue opisuje 
rzeczywiste wartości, zaś ypred wartości przewidziane przez model. Wykorzystując funkcję accuracy score() z sklearn policz dokładność 
tego modelu z dokładnością 4 m po przecinku i wyświetl."""
# import numpy as np
# import pandas as pd
# from sklearn.metrics import accuracy_score

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\preds.csv')

# y_true = df['y_true']
# y_pred = df['y_pred']
# ac = accuracy_score(y_true, y_pred)
# # inny sposób
# # ac = accuracy_score(df.iloc[:, 0].values, df.iloc[:, 1].values)
# print(f'Accuracy: {ac:.4f}')

# 46
"""W pliku predictions.csv znajdują się wyniki predycji na podstawie pewnego modelu klasyfikacji wieloklasowej (3 klasy). Kolumna ytrue opisuje 
rzeczywiste wartości, zaś ypred wartości przewidziane przez model. Wykorzystując funkcję confusion_matrix() z sklearn wyznacz macierz konfuzji i wyświetl."""
# import numpy as np
# import pandas as pd
# from sklearn.metrics import confusion_matrix

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\preds.csv')

# y_true = df['y_true']
# y_pred = df['y_pred']
# cm = confusion_matrix(y_true, y_pred)
# print(cm)

# 47
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując DecisionTreeClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych. Dokonaj trenowania modelu na zbiorze treningowym oraz oceny na zbiorze testowym. 
Wydrukuj dokładność modelu do 4 m po przecinku"""
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)

# classifier = DecisionTreeClassifier()
# X_train = classifier.fit(X_train, y_train)
# y_pred = classifier.predict(X_test)
# ac = accuracy_score(y_test, y_pred)
# # # inna wersja do oceny modelu bez importowania funkcji
# # ac = classifier.score(X_test, y_test)
# print(f'Accuracy: {ac:.4f}')

# 48
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując DecisionTreeClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych (ustaw argument max_depth = 6). Dokonaj trenowania modelu na zbiorze treningowym oraz oceny na zbiorze testowym. 
Wydrukuj dokładność modelu do 4 m po przecinku"""
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)

# classifier = DecisionTreeClassifier(max_depth=6)
# X_train = classifier.fit(X_train, y_train)
# y_pred = classifier.predict(X_test)
# ac = accuracy_score(y_test, y_pred)
# # # inna wersja do oceny modelu bez importowania funkcji
# # ac = classifier.score(X_test, y_test)
# print(f'Accuracy: {ac:.4f}')

# 49
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując DecisionTreeClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych (ustaw argument max_depth = 6 oraz min_samples_leaf = 6). Dokonaj trenowania modelu na zbiorze treningowym oraz oceny na zbiorze testowym. 
Wydrukuj dokładność modelu do 4 m po przecinku"""
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score
# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)

# classifier = DecisionTreeClassifier(max_depth=6, min_samples_leaf=6)
# X_train = classifier.fit(X_train, y_train)
# y_pred = classifier.predict(X_test)
# ac = accuracy_score(y_test, y_pred)
# # # inna wersja do oceny modelu bez importowania funkcji
# # ac = classifier.score(X_test, y_test)
# print(f'Accuracy: {ac:.4f}')

# 50
"""Wygenerowano zbiór raw_data zdefiniowany poniżej, Następnie podzielono go na zbiór treningowy i testowy. Wykorzystując DecisionTreeClassifier 
z sklearn zbuduj model klasyfikacji dla podanych danych. Wykorzystując metodę przeszukiwania siatki oraz klasę GridSearchCV (ustaw argumenty 
scoring='accuarcy', cv = 5) znajdź optymalne wartości parametrów max_depth oraz min_samples_leaf. Wartości parametrów poszukaj z danych 
[dla max depth _> np.arrange (1, 10), dla min)samples_leaf _> [1,2,3,4,5,6,7,8,9,10,15,20]] """
# import numpy as np
# import pandas as pd

# from sklearn.datasets import make_moons
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import GridSearchCV

# np.random.seed(42)
# raw_data = make_moons(n_samples=2000, noise=0.25, random_state=42)
# data = raw_data[0]
# target = raw_data[1]

# X_train, X_test, y_train, y_test = train_test_split(data, target)

# classifier = DecisionTreeClassifier()
# parameters = {'max_depth': np.arange(1, 10),
#               'min_samples_leaf': [1,2,3,4,5,6,7,8,9,10,15,20]}
# grid_search = GridSearchCV(classifier, param_grid=parameters, scoring='accuracy', cv=5)
# grid_search.fit(X_train, y_train)
# print(grid_search.best_params_)