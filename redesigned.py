
import numpy as np
import pandas as pd
import math

from multiprocessing import Pool

class testingredisign():
    def __init__(self,data):
        dataProd = data.groupby(['Hex_start','interval_start','day_of_year','year','dt']).size().reset_index(name='Production')
        dataProd = dataProd.rename(columns={'Hex_start':"Hex",'interval_start':"interval"})

        dataAttr = data.groupby(['Hex_end','interval_end','day_of_year','year','dt']).size().reset_index(name='Attraction')
        dataAttr = dataAttr.rename(columns={'Hex_end':"Hex",'interval_end':"interval"})

        data = dataProd.merge(dataAttr, how='outer',left_on=['Hex','interval','day_of_year','year','dt'],right_on = ['Hex','interval','day_of_year','year','dt']).fillna(0)
        data['year'] = data['year'].astype(int)
        data['Production'] = data['Production'].astype(int)
        data['Attraction'] = data['Attraction'].astype(int)

        print(data)
        data.to_csv('Test_RunPA.csv')


def main():
    data = pd.read_csv("Test_Run.csv")

    inter = testingredisign(data)

    # df_splitted = parallelize_dataframe(data, use_preprocessing, n_cores=10)

    # df_splitted.to_csv('Preprocessing_DF.csv', index=False)

    # tool = testingZones(data)
    # tool.create_dataset()

    return

if __name__=="__main__":
    main()


















