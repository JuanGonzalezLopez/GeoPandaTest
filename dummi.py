import numpy as np
import pandas as pd



class dummyfy():


    def __init__(self,data=None, filename: str = './Output/PreprocessedOverlapped.csv'):
        if (not (type(data) == type(None))):
            data = data
        else:
            data = pd.read_csv(filename)



    def dummyfy(self,data,column_name):

        for col in column_name:
            dummies = pd.get_dummies(data[col])

            dummies = dummies.drop(dummies.columns.values[0], axis='columns')
            merged = pd.concat([data, dummies], axis='columns')

            merged = merged.drop([col], axis='columns')
            data = merged



        return data