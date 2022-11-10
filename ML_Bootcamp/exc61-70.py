# 61
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę KMeans (random_state=42)
z pakietu sklearn wyznacz listę wartości WCSS dla liczby klastrów od 2 do 9 włącznie. Wartości WCSS zaokrąglij do 2 m po ,. Listę wydrukuj"""
# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# wcss = []
# for i in range(2, 10):
#     kmeans = KMeans(n_clusters = i, random_state = 42)
#     kmeans.fit(df)
#     # wcss.append(f'{kmeans.inertia_:.2f}')  tak nie, to jest dodawane jako tekst 
#     wcss.append(round(kmeans.inertia_, 2))
# print(wcss)

# 62
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę KMeans (random_state=42)
z pakietu sklearn wyznaczono listę wartości WCSS dla liczby klastrów od 2 do 9 włącznie. Wykorzystując metodę łokcia wybierz odpowiednią liczbę 
klastrów (stwórz wykres pomocniczy) wydrukuj"""
# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans
# from matplotlib import pyplot as plt
# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# wcss = []
# for i in range(2, 10):
#     kmeans = KMeans(n_clusters = i, random_state = 42)
#     kmeans.fit(df)
#     wcss.append(round(kmeans.inertia_, 2))
#     print(wcss)
# plt.plot(range(2, 10), wcss)
# plt.title('The Elbow Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('WCSS')
# plt.show()

# 63
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę AgglomerativeClustering
z pakietu sklearn dokonaj podziału na dwa klastry. Dokonaj predykcji na podstawie zbudowanego modelu i przypisz numer klastra do każdej próbki 
w obiekcie df (kolumna cluster). Wyświetl 10 pierwszych wierszy df."""

# import numpy as np
# import pandas as pd
# from sklearn.cluster import AgglomerativeClustering

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# ac = AgglomerativeClustering(n_clusters=2)
# df['cluster'] = ac.fit_predict(df)
# # cluster = AgglomerativeClustering(n_clusters=2)
# # cluster.fit_predict(df)
 
# # df = pd.DataFrame(df, columns=['x1', 'x2'])
# # df['cluster'] = cluster.labels_
# print(df.head(10))

# 64
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę AgglomerativeClustering
z pakietu sklearn dokonaj podziału na dwa klastry (wykorzystując metrykę Manhattan). Dokonaj predykcji na podstawie zbudowanego modelu i przypisz 
numer klastra do każdej próbki w obiekcie df (kolumna cluster). Wyświetl 10 pierwszych wierszy df."""

# import numpy as np
# import pandas as pd
# from sklearn.cluster import AgglomerativeClustering

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# ac = AgglomerativeClustering(n_clusters=2, affinity='manhattan', linkage='complete')
# df['cluster'] = ac.fit_predict(df)
# print(df.head(10))

# 65
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę DBSCAN
z pakietu sklearn dokonaj podziału na dwa klastry (ustaw eps=0.6 i min_samples=7). Dokonaj predykcji na podstawie zbudowanego modelu i przypisz 
numer klastra do każdej próbki w obiekcie df (kolumna cluster). Wyświetl 10 pierwszych wierszy df."""

# import numpy as np
# import pandas as pd
# from sklearn.cluster import DBSCAN

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# cluster = DBSCAN(eps=0.6, min_samples=7)
# df['cluster'] = cluster.fit_predict(df)
# print(df.head(10))

# 66
"""Wczytaj plik clusters.csv do obiektu df. Plik zawiera dwie zmienne x1 i x2. Rozkład (na zdjęciu). Wykorzystując klasę DBSCAN
z pakietu sklearn dokonaj podziału na dwa klastry (ustaw eps=0.6 i min_samples=7). Dokonaj predykcji na podstawie zbudowanego modelu i przypisz 
numer klastra do każdej próbki w obiekcie df (kolumna cluster). Wyświetl rozkład częstości próbek w każdym klastrze. (frequency distribution)"""

# import numpy as np
# import pandas as pd
# from sklearn.cluster import DBSCAN

# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\clusters.csv')

# cluster = DBSCAN(eps=0.6, min_samples=7)
# cluster.fit(df)
# df['cluster'] = cluster.labels_
# print(df.cluster.value_counts())

# 67 
"""Wczytaj plik pca.csv do obiektu df. Plik zawiera trzy zmienne objaśniające var1, var2, var3 oraz zmienną docelową class. 
Następnie przypisz do zmiennej X kolumny var1, var2, var3, zaś do zmiennej y kolumnę class. Wykorzystując StandardScaler dokonaj 
standaryzacji zmiennych w obiekcie X. Wyświetl dziesięć pierwszych wierszy obiektu X"""

# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca.csv')

# X = df.iloc[:, :-1].values
# y = df.iloc[:, -1].values

# sc = StandardScaler()
# X = sc.fit_transform(X)
# print(X[:10, :])
# # lub 
# X = df.copy()
# y = X.pop('class')
 
# scaler = StandardScaler()
# X_std = scaler.fit_transform(X)
# print(X_std[:10])

# 68 
"""Wczytano plik pca.csv do df. Wykorzystując StandardScaler dokonano standaryzacji zmiennych podanych w pliku i przypisano do zmiennej X_std.
Zaimplementuj algorytm PCA wykorzystując tablicę X_std. Wynik ogranicz do dwóch głównych komponentów PCA i przypisz do zmiennej X_pca.
Wydrukuj 10 pierwszych wieszy obiektu X_pca"""

# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# np.set_printoptions(precision=8, suppress=True, edgeitems=5, linewidth=200)
# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca.csv')

# X = df.copy()
# y = X.pop('class')

# scaler = StandardScaler()
# X_std = scaler.fit_transform(X)

# eig_vals, eig_vecs = np.linalg.eig(np.cov(X_std, rowvar=False))
# eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]
# eig_pairs.sort(reverse=True)
 
# W = np.hstack((eig_pairs[0][1].reshape(3, 1), eig_pairs[1][1].reshape(3, 1)))
# X_pca = X_std.dot(W)
# print(X_pca[:10])

# 69 
"""Wczytano plik pca.csv do df. Wykorzystując StandardScaler dokonano standaryzacji zmiennych podanych w pliku i przypisano do zmiennej X_std.
Zaimplementowano algorytm PCA wykorzystując tablicę X_std i przypisano do zmiennej X_pca. Zbuduj obiekt df o nazwie df_pca wykorzystując tablicę 
X_pca oraz zmienną y. Wydrukuj 10 pierwszych wieszy obiektu df_pca"""

# from email import header
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# np.set_printoptions(precision=8, suppress=True, edgeitems=5, linewidth=200)
# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca.csv')

# X = df.copy()
# y = X.pop('class')

# scaler = StandardScaler()
# X_std = scaler.fit_transform(X)

# eig_vals, eig_vecs = np.linalg.eig(np.cov(X_std, rowvar=False))
# eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]
# eig_pairs.sort(reverse=True)
 
# W = np.hstack((eig_pairs[0][1].reshape(3, 1), eig_pairs[1][1].reshape(3, 1)))
# X_pca = X_std.dot(W)
# df_pca = pd.DataFrame(X_pca, columns=['pca_1', 'pca_2'])
# df_pca['class'] = y
# df_pca['pca_2'] = - df_pca['pca_2']
# print(df_pca.head(10))

# 70
"""Wczytano plik pca.csv do df. Wykorzystując StandardScaler dokonano standaryzacji zmiennych podanych w pliku i przypisano do zmiennej X_std.
Wykorzystując klasę PCA z pakietu sklearn dokonaj analizy PCA z dwoma komponentami na obiekcie X_std i przypisz do zmiennej df_pca.
Wydrukuj 10 pierwszych wieszy obiektu df_pca"""

# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# np.set_printoptions(precision=8, suppress=True, edgeitems=5, linewidth=200)
# np.random.seed(42)
# df = pd.read_csv(r'C:\Users\danie\Dropbox\Python\Projects\ML\ML_Bootcamp\pca.csv')

# X = df.copy()
# y = X.pop('class')

# scaler = StandardScaler()
# X_std = scaler.fit_transform(X)

# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X_std)

# df_pca = pd.DataFrame(data=X_pca, columns=['pca_1', 'pca_2'])
# df_pca['class'] = df['class']
# print(df_pca.head(10))