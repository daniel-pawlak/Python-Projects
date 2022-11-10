# 71
"""Wczytaj plik pca.csv do onikektu df. Plik zawiera zmienne var1...var10. Dokonaj analizy PCA z trzema komponentami wykorzystując pakiet sklearn
i klasę PCA. Wydrukuj procent wyjaśnionej wariancji przez te komponenty."""
# import numpy as np
# import pandas as pd

# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca2.csv')
# data = df.values
# scaler = StandardScaler()
# data_std = scaler.fit_transform(data)

# pca = PCA(n_components=3)
# data_pca = pca.fit_transform(data_std)

# results = pd.DataFrame(data={'explained_variance_ratio': pca.explained_variance_ratio_})
# results['cumulative'] = results['explained_variance_ratio'].cumsum()
# results['component'] = results.index + 1
# print(results)

# 72
"""Wczytaj plik pca.csv do onikektu df. Plik zawiera zmienne var1...var10. Dokonaj analizy PCA wykorzystując pakiet sklearn. Zachowaj liczbę
komponentów pozwalającą wyjaśnić 95% wariancji podanych danych. Wydrukuj liczbę komponentów"""
# import numpy as np
# import pandas as pd

# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca2.csv')
# data = df.values
# scaler = StandardScaler()
# data_std = scaler.fit_transform(data)

# pca = PCA(n_components=0.95)
# data_pca = pca.fit_transform(data_std)
# print(f'Liczba komponentów: {pca.n_components_}')

# 73
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podziel każdy wiersz kolumny 
products względem znaku spacji i rozszerz do obiektu df. Obiekt docelowo będzie posiadał 4 kolumny (max liczba transakcji. W brakujące miejsca wpisz 
wartość None i przypisz do zmiennej expanded. Wydrukuj ją."""

# import numpy as np
# import pandas as pd

# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}

# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)
# print(expanded)

# 74
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podzielono każdy wiersz kolumny 
products względem znaku spacji i rozszerzono do obiektu df. Do zmiennej products przypisz unikalne nazwy wszystkich produktów występujących
w bazie transakcji posortowanych alfabetycznie. Wydrukuj ją."""

# import numpy as np
# import pandas as pd

# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}

# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)

# products = []
# for col in expanded.columns:
#     for product in expanded[col].unique():
#         if product is not None and product not in products:
#             products.append(product)
 
# products.sort()
# print(products)

# 75
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podzielono każdy wiersz kolumny 
products względem znaku spacji i rozszerzono do obiektu df. Do zmiennej products przypisano unikalne nazwy wszystkich produktów występujących
w bazie transakcji posortowanych alfabetycznie. Dokonaj kodowania 0-1 i przypisano do zmiennej transactions_encoded_df. Wydrukuj."""

# import numpy as np
# import pandas as pd

# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}

# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)

# products = []
# for col in expanded.columns:
#     for product in expanded[col].unique():
#         if product is not None and product not in products:
#             products.append(product)
 
# products.sort()
# transactions_encoded = np.zeros((len(transactions), len(products)), dtype='int8')

# for row in zip(range(len(transactions)), transactions_encoded, expanded.values):
#     for idx, product in enumerate(products):
#         if product in row[2]:
#             transactions_encoded[row[0], idx] = 1

# transactions_encoded_df = pd.DataFrame(transactions_encoded, columns=products)
# print(transactions_encoded_df)

#76
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podzielono każdy wiersz kolumny 
products względem znaku spacji i rozszerzono do obiektu df. Do zmiennej products przypisano unikalne nazwy wszystkich produktów występujących
w bazie transakcji posortowanych alfabetycznie. Dokonano kodowania 0-1 i przypisano do zmiennej transactions_encoded_df. Oblicz wsparcie support 
(liczba wystąpień produkktu/wszystkie wystąpienia) i wydrukuj."""
# import numpy as np
# import pandas as pd
 
# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}
 
# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)
 
# products = []
# for col in expanded.columns:
#     for product in expanded[col].unique():
#         if product is not None and product not in products:
#             products.append(product)
 
# products.sort()
 
# transactions_encoded = np.zeros((len(transactions), len(products)), dtype='int8')
 
# for row in zip(range(len(transactions)), transactions_encoded, expanded.values):
#     for idx, product in enumerate(products):
#         if product in row[2]:
#             transactions_encoded[row[0], idx] = 1
 
# transactions_encoded_df = pd.DataFrame(transactions_encoded, columns=products)
 
# support = transactions_encoded_df.sum() / len(transactions_encoded_df)
# print(support)

#77
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podzielono każdy wiersz kolumny 
products względem znaku spacji i rozszerzono do obiektu df. Do zmiennej products przypisano unikalne nazwy wszystkich produktów występujących
w bazie transakcji posortowanych alfabetycznie. Dokonano kodowania 0-1 i przypisano do zmiennej transactions_encoded_df. Oblicz wsparcie dla par (butter milk) i (butter bread) 
(liczba wystąpień produkktu/wszystkie wystąpienia) i wydrukuj (wynik zaokrąglij do 4 miesc po przecinku)."""
# import numpy as np
# import pandas as pd
 
# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}
 
# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)
 
# products = []
# for col in expanded.columns:
#     for product in expanded[col].unique():
#         if product is not None and product not in products:
#             products.append(product)
 
# products.sort()
 
# transactions_encoded = np.zeros((len(transactions), len(products)), dtype='int8')
 
# for row in zip(range(len(transactions)), transactions_encoded, expanded.values):
#     for idx, product in enumerate(products):
#         if product in row[2]:
#             transactions_encoded[row[0], idx] = 1
 
# transactions_encoded_df = pd.DataFrame(transactions_encoded, columns=products)
 
# sup_butter_bread = len(transactions_encoded_df.query("butter == 1 and bread == 1")) \
#     / len(transactions_encoded_df)
# sup_butter_milk = len(transactions_encoded_df.query("butter == 1 and milk == 1")) \
#     / len(transactions_encoded_df)
 
# print(f'support(butter, bread) = {sup_butter_bread:.4f}')
# print(f'support(butter, milk) = {sup_butter_milk:.4f}')

# 78
"""Podany jest obiekt df zawierający dane transakcji. Każdy wiersz zawiera produkty zakupione przez jednego klienta. Podzielono każdy wiersz kolumny 
products względem znaku spacji i rozszerzono do obiektu df. Do zmiennej products przypisano unikalne nazwy wszystkich produktów występujących
w bazie transakcji posortowanych alfabetycznie. Dokonano kodowania 0-1 i przypisano do zmiennej transactions_encoded_df. Oblicz pewność reguł (cheese->bread i butter->cheese) 
i wynik wydrukuj (wynik zaokrąglij do 4 miesc po przecinku).(Pewność = liczba transakcji zawierających produkt A i produkt B/Liczba transakcji zawierających produkt A)"""
# import numpy as np
# import pandas as pd
 
# data = {'products': ['bread eggs', 'bread eggs milk', 'milk cheese', 
#                      'bread butter cheese', 'eggs milk', 
#                      'bread milk butter cheese']}
 
# transactions = pd.DataFrame(data=data, index=range(1, 7))
# expanded = transactions['products'].str.split(expand=True)
 
# products = []
# for col in expanded.columns:
#     for product in expanded[col].unique():
#         if product is not None and product not in products:
#             products.append(product)
 
# products.sort()
 
# transactions_encoded = np.zeros((len(transactions), len(products)), dtype='int8')
 
# for row in zip(range(len(transactions)), transactions_encoded, expanded.values):
#     for idx, product in enumerate(products):
#         if product in row[2]:
#             transactions_encoded[row[0], idx] = 1
 
# transactions_encoded_df = pd.DataFrame(transactions_encoded, columns=products)
 
# sup_cheese_bread = len(transactions_encoded_df.query("cheese == 1 and bread == 1")) \
#     / len(transactions_encoded_df.query("cheese == 1"))
# sup_butter_cheese = len(transactions_encoded_df.query("butter == 1 and cheese == 1")) \
#     / len(transactions_encoded_df.query("butter == 1"))
 
# print(f'support(cheese, bread) = {sup_cheese_bread:.4f}')
# print(f'support(butter, cheese) = {sup_butter_cheese:.4f}')

# 79
"""Wczytaj podany plik blobs.csv do obiektu df. Plik zawiera zmienne x1 i x2. Wykorzystując klasę LocalOutlierFactor z pakietu sklearn dokonaj analizy elementów odstających w podanym zbiorze.
Ustaw argument n_neighbors=20. Dla przypomnienia 1 oznacza normalny element, -1 element odstający. Przypisz nową kolumnę do obiektu df o nazwie lof, która będzie przechowwywać informację,
czy dana próbka jest elementem normalnym czy odstającym. Wydrukuj 10 pierwszych wierszy obiektu df."""

# import numpy as np
# import pandas as pd
# from sklearn.neighbors import LocalOutlierFactor

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\blobs.csv')
# lof = LocalOutlierFactor(n_neighbors=20)
# X = df.values
# y = lof.fit_predict(X)
# df['lof'] = y
# print(df.head(10))

# 80
"""Wczytaj podany plik blobs.csv do obiektu df. Plik zawiera zmienne x1 i x2. Wykorzystując klasę LocalOutlierFactor z pakietu sklearn dokonano analizy elementów odstających w podanym zbiorze.
Dla przypomnienia 1 oznacza normalny element, -1 element odstający. Przypisano nową kolumnę do obiektu df o nazwie lof, która będzie przechowwywać informację,
czy dana próbka jest elementem normalnym czy odstającym. Zbadaj liczbę elementów odstających w zbiorze, tzn. zbadaj rozkład kolumny lof. Wydrukuj."""

# import numpy as np
# import pandas as pd
# from sklearn.neighbors import LocalOutlierFactor

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\blobs.csv')
# lof = LocalOutlierFactor(n_neighbors=30)
# X = df.values
# y = lof.fit_predict(X)
# df['lof'] = y

# normal = df[df['lof'] == 1].count()['lof']
# notnormal = df[df['lof'] == -1].count()['lof']
# print(normal, notnormal)
# # lub prościej
# print(df['lof'].value_counts())