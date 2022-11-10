import pandas as pd

file_name =  r'C:\Users\danie\Desktop\Python\Scrapers\jobboard\JB files\Training.xlsx'
sheet =  'Arkusz1'

df = pd.read_excel(io=file_name, sheet_name=sheet)
print(df.head(5))  # print first 5 rows of the dataframe