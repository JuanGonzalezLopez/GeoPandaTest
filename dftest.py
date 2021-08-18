import pandas as pd



dict = {}

dict['zona'] = [1,2,3,4,5,6]

dict['coordx'] = ['14.2233','14.2566','14.2353','14.2253','14.2563','14.2343']
dict['coordy'] = ['14.2566','14.2353','14.2253','14.2563','14.2343','14.2233']

dataframe = pd.DataFrame(dict)

print(dataframe)
dataframe.to_csv('testingdataframe.csv')
