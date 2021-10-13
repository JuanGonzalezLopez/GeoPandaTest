
import numpy as np
import pandas as pd
import math

from multiprocessing import Pool

class grouping():
    def __init__(self,data=None, filename: str = './Output/PreprocessedIntervals.csv'):
        if(not(type(data)==type(None))):
            data = data
        else:
            data = pd.read_csv(filename)
        dataProd = data.groupby(['Hex_start','interval_start','day_of_year','year','dt']).size().reset_index(name='Production')
        dataProd = dataProd.rename(columns={'Hex_start':"Hex",'interval_start':"interval"})

        dataAttr = data.groupby(['Hex_end','interval_end','day_of_year','year','dt']).size().reset_index(name='Attraction')
        dataAttr = dataAttr.rename(columns={'Hex_end':"Hex",'interval_end':"interval"})

        data = dataProd.merge(dataAttr, how='outer',left_on=['Hex','interval','day_of_year','year','dt'],right_on = ['Hex','interval','day_of_year','year','dt']).fillna(0)
        data['year'] = data['year'].astype(int)
        data['Production'] = data['Production'].astype(int)
        data['Attraction'] = data['Attraction'].astype(int)

        data = data.sort_values(by=['dt', 'interval']).reset_index(drop=True)

        unique = data['interval'].drop_duplicates(keep='first').sort_values().reset_index(drop=True)

        emptydata = data.groupby(['Hex', 'day_of_year', 'year', 'dt'])['interval'].apply(
            lambda grp: unique[~unique.isin(grp.values)]).reset_index().drop(['level_4'], axis=1)

        emptydata['Attraction'] = 0
        emptydata['Production'] = 0

        data = pd.concat([data, emptydata]).reset_index(drop=True)


        unique = data['Hex'].drop_duplicates(keep='first').sort_values().reset_index(drop=True)

        emptydata = data.groupby(['interval', 'day_of_year', 'year', 'dt'])['Hex'].apply(
            lambda grp: unique[~unique.isin(grp.values)]).reset_index().drop(['level_4'], axis=1)

        emptydata['Attraction'] = 0
        emptydata['Production'] = 0

        data = pd.concat([data, emptydata]).reset_index(drop=True)

        print(data)

        self.data = data
    def returnDF(self,output='./Output/PreprocessedPreFinal.csv'):


        self.data.to_csv(output,index=False)
        return self.data

def main():
    data = pd.read_csv("./Output/PrepoCluster.csv")

    inter = grouping(data)
    resu = inter.returnDF()

    # df_splitted = parallelize_dataframe(data, use_preprocessing, n_cores=10)

    # df_splitted.to_csv('Preprocessing_DF.csv', index=False)

    # tool = testingZones(data)
    # tool.create_dataset()

    return

if __name__=="__main__":
    main()


















