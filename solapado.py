
import numpy as np
import pandas as pd
import math

from multiprocessing import Pool

class overlap():
    def __init__(self,data=None, filename: str = './Output/PreprocessedPreFinal.csv'):
        if(not(type(data)==type(None))):
            data = data
        else:
            data = pd.read_csv(filename)

        data = data.sort_values(by=['dt', 'interval']).reset_index(drop=True)


        indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=24)

        # data['att_over'] = data.groupby(['Hex', 'day_of_year','year'])['Attraction'].rolling(indexer,min_periods=0).sum().reset_index().set_index('level_3').sort_index()['Attraction']
        data['att_over'] = data.groupby(['Hex', 'day_of_year','year'])['Attraction'].transform(lambda s: s.rolling(indexer, min_periods=0).sum())

        indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=24)

        data['prod_over'] = data.groupby(['Hex', 'day_of_year','year'])['Production'].transform(lambda s: s.rolling(indexer, min_periods=0).sum())
        # data['prod_over'] = data.groupby(['Hex', 'day_of_year','year'])['Production'].rolling(indexer,min_periods=0).sum().reset_index().set_index('level_3').sort_index()['Production']
        data['mavg_po_hours'] = data.groupby(['Hex', 'day_of_year','year'])['prod_over'].rolling(24,min_periods=0).mean().shift().reset_index().set_index('level_3').sort_index()['prod_over'].fillna(0)
        data['mavg_ao_hours'] = data.groupby(['Hex', 'day_of_year','year'])['att_over'].rolling(24,min_periods=0).mean().shift().reset_index().set_index('level_3').sort_index()['att_over'].fillna(0)

        data['mavg_po_days'] = data.groupby(['Hex', 'interval','year'])['prod_over'].rolling(7,min_periods=0).mean().shift().reset_index().set_index('level_3').sort_index()['prod_over'].fillna(0)
        data['mavg_ao_days'] = data.groupby(['Hex', 'interval','year'])['att_over'].rolling(7,min_periods=0).mean().shift().reset_index().set_index('level_3').sort_index()['att_over'].fillna(0)


        data['dt']=pd.to_datetime(data['dt'])

        data['weekday'] = data['dt'].dt.dayofweek

        data['mavg_po_weeks'] = data.groupby(['Hex', 'interval','year'])['prod_over'].rolling(4,min_periods=0).mean().shift().reset_index().set_index('level_3').sort_index()['prod_over'].fillna(0)
        data['mavg_ao_weeks'] = data.groupby(['Hex', 'interval','weekday','year'])['att_over'].rolling(4,min_periods=0).mean().shift().reset_index().set_index('level_4').sort_index()['att_over'].fillna(0)


        self.data = data
    def returnDF(self,output='./Output/PreprocessedOverlapped.csv'):


        self.data.to_csv(output,index=False)
        return self.data

def main():
    data = pd.read_csv('./Output/PreprocessedPreFinal.csv')

    inter = overlap(data)
    resu = inter.returnDF()
    # df_splitted = parallelize_dataframe(data, use_preprocessing, n_cores=10)

    # df_splitted.to_csv('Preprocessing_DF.csv', index=False)

    # tool = testingZones(data)
    # tool.create_dataset()

    return

if __name__=="__main__":
    main()


















