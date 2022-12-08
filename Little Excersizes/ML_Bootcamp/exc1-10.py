import numpy as np
import pandas as pd
# from sklearn.impute import SimpleImputer
data = {
    'size': ['XL', 'L', 'M', np.nan, 'M', 'M'],
    'color': ['red', 'green', 'blue', 'green', 'red', 'green'],
    'gender': ['female', 'male', np.nan, 'female', 'female', 'male'],
    'price': [199.0, 89.0, np.nan, 129.0, 79.0, 89.0],
    'weight': [500, 450, 300, np.nan, 410, np.nan],
    'bought': ['yes', 'no', 'yes', 'no', 'yes', 'no']
}

#1
"""Utwórz df i znajdź brakujące wartości, podaj procent braków"""
# df = pd.DataFrame(data)
# nans = df.isnull().sum().sum()
# total = df.size

# results = nans/total
# # print('{:.2f}'.format(results)) # procent ogólny braków
# # print(np.round(df.isnull().sum() / len(df), 2)) # procent braków dla każdej kolumny

#2
"""Uzupełnienie pustych wartości w kolumnie weight o średnie wartości wyciągnięte z całej kolumny"""
# from sklearn.impute import SimpleImputer
# df = pd.DataFrame(data=data)
# imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# df[['weight']] = imputer.fit_transform(df[['weight']])
# # print(df)

#3
"""Średnia wartości wyciągnięta z całej kolumny"""
# df = pd.DataFrame(data=data)
# imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# df[['weight']] = imputer.fit_transform(df[['weight']])
# # print(imputer.statistics_[0])

#4
"""Uzupełnienie braków stałą wartością"""
# df = pd.DataFrame(data=data)
# imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=99.0)
# df[['price']] = imputer.fit_transform(df[['price']])
# # print(df)

#5
"""Uzupełnienie braków najczęściej występującą wartością"""
# df = pd.DataFrame(data=data)
# imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
# df[['size']] = imputer.fit_transform(df[['size']])
# # print(df)

#6
"""Wyciągnięcie wierszy, które w kolumnie weight nie równa się nan (puste wartości) i policzenie średniej dla price i weight """
df = pd.DataFrame(data=data)
# df = df.loc[df['weight'].notnull()]
print(df)
# imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# df[['price']] = imputer.fit_transform(df[['price']])
# print(df['price'].mean())   # średnia
# print(df['weight'].mean())

# lub tak, szybciej: print(df[~df['weight'].isnull()].mean())

#7 
"""Wydąbądź kolumny typu object, w których są puste wartości i uzupełnij o słowo "empty" """
# df = pd.DataFrame(data=data)
# df_object = df.select_dtypes(include=['object']).fillna('empty')  # wypełnienie pustych wartości, sortowanie po type
# print(df_object)

#8 
"""Dokonaj dyskretyzacji kolumny na przedziały o równej wartości i utwórz kolumnę z nowymi przedziałami"""
# df = pd.DataFrame(data={'weight': [75., 78.5, 85., 91., 84.5, 83., 68.]})
# df['weight cut'] = pd.qcut(df['weight'], q=3)
# df['weight cut'] = pd.cut(df['weight'], bins=3)
# print(df)

#9
"""Dokonaj dyskretyzacji kolumny na przedziały o zadanej postaci [(60,75], (75,80], (80,95]] i utwórz kolumnę z nowymi przedziałami"""
# df = pd.DataFrame(data={'weight': [75., 78.5, 85., 91., 84.5, 83., 68.]})
# cut_bins = [0, 60, 75, 80, 95]
# df['weight cut'] = pd.cut(df['weight'], bins=cut_bins)
# # df['weight_cut'] = pd.cut(df['weight'], bins=(60, 75, 80, 95))
# print(df)

#10
"""Dokonaj dyskretyzacji kolumny na przedziały o zadanej postaci [(60,75], (75,80], (80,95]] oraz przypisz im zadane etykiety i utwórz kolumnę z nowymi przedziałami"""
# df = pd.DataFrame(data={'weight': [75., 78.5, 85., 91., 84.5, 83., 68.]})
# df['weight_cut'] = pd.cut(df['weight'], bins=(60, 75, 80, 95), labels=('light', 'normal', 'heavy'))
# print(df)

# df[df == 0.0].count().sum().sum() - suma konkretna wartość