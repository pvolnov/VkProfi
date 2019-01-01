import pandas as pd


data = pd.read_csv('data.csv')

dt=data['Какая у Вас профессия, должность в Вашей компании?']
cat=dt.drop_duplicates()
print(cat.head)