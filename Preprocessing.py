
import numpy as np
import pandas as pd
import math

from multiprocessing import Pool


class datecolumns():
    def __init__(self,data=None, filename: str = './Output/Ride_data_with_hex.csv',step_interval=5,interval_range=2):
        if(not(type(data)==type(None))):
            self.data = data
        else:
            self.data = pd.read_csv(filename)
        self.data = self.data.dropna().reset_index(drop=True)
        if(60%step_interval==0):
            self.step_interval = step_interval/60

        else:
            # fix later: TODO find a way to round to the nearest number that 60 would be divisible for
            print("Rounding to the nearest 5 step_interval")
            step_interval = (5 * round(step_interval / 5))
            self.step_interval = step_interval/60

        # if (production):
        #     self.target = "start"
        # else:
        #     self.target = "end"
        # self.data[self.target+'_time'] = pd.to_datetime(self.data[self.target+'_time'])
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        minimum_hour = int(self.data['start_time_scalar'].min())
        maximum_hour = int(math.ceil(np.round(self.data['end_time_scalar'].max())))

        unique_time = np.arange(minimum_hour, maximum_hour, self.step_interval)
        hour = 1.0
        self.limit = int(60 / step_interval)

        for i in range(0, len(unique_time) - self.limit):

            smallest = unique_time[i]
            largest = smallest + hour

            if (smallest.is_integer()):
                unique_time[i + self.limit] = largest
        print(unique_time)
        self.unique_time = unique_time



    def day_of_year(self,row):
        return row['dt'].day_of_year
    def interval(self,row):

        time = row["start_time_scalar"]

        for i in range(0,len(self.unique_time)-1):

            if(self.unique_time[i] <= time <self.unique_time[i+1]):

                return i


        print("error - dnf")
        return None

    def intervalend(self,row):

        time = row["end_time_scalar"]

        for i in range(0,len(self.unique_time)-1):

            if(self.unique_time[i] <= time <self.unique_time[i+1]):

                return i


        print("error - dnf")
        return None



    def dateify(self):
        self.data['day_of_year'] = self.data.apply(self.day_of_year, axis=1)

    # def intervalend(self,row):
    #
    #     return self.unique_time[row['interval_start']+1]

    def intervalize(self,output="./Output/PreprocessedIntervals.csv"):
        self.dateify()

        self.data['interval_start'] = self.data.apply(self.interval,axis=1)
        self.data['interval_end'] =self.data.apply(self.intervalend,axis=1)

        self.data.to_csv(output,index=False)
        return self.data

class Restructuring():
    def __init__(self,data,step_interval=5,interval_range=2):
        self.data = data

        self.step_interval = step_interval / 60

        minimum_hour = int(self.data['start_time_scalar'].min())
        maximum_hour = int(math.ceil(np.round(self.data['end_time_scalar'].max())))

        unique_time = np.arange(minimum_hour, maximum_hour, self.step_interval)
        hour = 1.0
        self.limit = int(60 / step_interval)

        for i in range(0, len(unique_time) - self.limit):

            smallest = unique_time[i]
            largest = smallest + hour

            if (smallest.is_integer()):
                unique_time[i + self.limit] = largest
        # print(unique_time)
        self.unique_time = unique_time

    def create_dataset(self):

        time_start =[]
        time_end = []
        dt = []
        # day = []
        day_of_year = []
        day_of_week = []
        day_of_month = []
        interval = []
        hex = []
        year = []
        month = []
        attraction = []
        production = []


        unique_hex_start = self.data['Hex_start']
        unique_hex_end = self.data['Hex_end']
        df_union = pd.concat([unique_hex_end, unique_hex_start]).drop_duplicates(keep='first').sort_values().reset_index(drop=True)

        unique_doy = self.data['day_of_year'].unique()
        unique_year = self.data['year'].unique().astype(int)
        for h in df_union:
            for t in range(0, len(self.unique_time)-1):
                for d in unique_doy:
                    for y in unique_year:

                        slice_start = self.data.loc[(self.data['Hex_start']==h)&(self.data['interval_start']==t)&(self.data['day_of_year']==d)&(self.data['year']==y)].reset_index(drop=True)
                        slice_end = self.data.loc[(self.data['Hex_end']==h)&(self.data['interval_end']==t)&(self.data['day_of_year']==d)&(self.data['year']==y)].reset_index(drop=True)


                        if(not((slice_start.empty) and (slice_end.empty))):
                            if (slice_start.empty):
                                tdate = slice_end['dt'][0]
                            else:
                                tdate = slice_start['dt'][0]
                            print("Works")
                            time_start.append(self.unique_time[t])
                            time_end.append(self.unique_time[t + 1])
                            dt.append(tdate)
                            # day.append(tdate.day)
                            day_of_year.append(d)
                            day_of_week.append(tdate.weekday())
                            day_of_month.append(tdate.day)
                            interval.append(t)
                            hex.append(h)
                            year.append(y)
                            month.append(tdate.month)

                            production.append(len(slice_start))
                            attraction.append(len(slice_end))

        pre_df = {}

        pre_df['attraction'] = attraction
        pre_df['production'] = production
        pre_df['hex'] = hex
        pre_df['dt'] = dt
        pre_df['day_of_year'] = day_of_year
        pre_df['day_of_week'] = day_of_week
        pre_df['day_of_month'] = day_of_month
        pre_df['year'] = year
        pre_df['month'] = month
        pre_df['interval'] = interval
        pre_df['time_start'] = time_start
        pre_df['time_end'] = time_end

        result = pd.DataFrame(pre_df)
        # result.to_csv("Preprocessed_DF.csv",index=False)
        return result


def parallelize_dataframe(data, func, n_cores=4):
    '''
        Voy a split la data por la cantidad de cores que le indique
        Por ejemplo, si son 4 cores pues 1/4 de la data va para cada core

        Como la divido? Pues en este caso, busque cuantos runs hay en la data (de la columna de 'run', hubieron 119 runs)
        y lo dividi entre la cantidad de core (119 runs / 4 cores)

        Lo redondee de 29.75 a 30.0, so que cada core tendra que hacer preprocess a la data de 30 runs~
        [core1 = run0-run30,
         core2 = run31-run60,
         core3 = run61-run90,
         core4 = run91-run119]



    '''
    df_split = []  # Empty List donde va la data dividida en chunks (si son 4 cores, pues dara 4 data frames)

    start = 0  # Donde empieza el primer slice es en el run 0 (primer run)

    unique_hex_start = data['Hex_start']
    unique_hex_end = data['Hex_end']
    df_union = pd.concat([unique_hex_end, unique_hex_start]).drop_duplicates(keep='first').sort_values().reset_index(drop=True).to_numpy()

    # subdivisions = round(len(df_union) / n_cores)  # para dividir la cantidad de trabajo por core, divido el numero de runs entre los cores (runs/cores = 19/4)


    splitted_union = np.array_split(df_union,n_cores)



    # end = subdivisions  # Donde acaba en el primer run es en el run que saque subdivisions (e.g. run 30)


    # el primer core va a analizar del run0 al run30

    '''
    Va a iterar por los difentes runs

    ahora el start va a continuar donde acabo el anterior chunk de data

    Por ejemplo va de run30 a run60, y en el proximo loop va de run61-run90

    no se repite la data entre diferentes chunks, solo la divide

    '''

    for i in range(0, len(splitted_union)):
        temp_data = data[data['Hex_start'].isin(splitted_union[i])|data['Hex_end'].isin(splitted_union[i])]

        df_split.append(temp_data)  # Añade el canto de data a una lista

    '''

    Ya dividio la data entre cores 

    Se puede usar otra columna como index se puede hacer pero si vas a hacer operaciones que vayan a buscar data global pues hay que tener cuidado.

    Porque? porque la data dividida no tiene la data completa, so que siacaso si vas a dividir la data, hay que ser mas selectivo. Aqui se pudo hacer porque la pude dividir entre los runs.
    Pero maybe tambien se puede dividir la data por zonas (cada core coja la data de 3 zonas)


    '''
    pool = Pool(n_cores)  # Inicializa el pool (en tu caso creo que era mp.pool, pero yo namas usare Pool so que hice un 'from multithreading import Pool')

    # en pool.map voy a poner la funcion que quiero que cada core opere igual mente en los distintos slices de data,
    # y la lista de los dataframes splitted. Luego que acabe usar concat para unirlo

    data = pd.concat(pool.map(func,df_split))  # Ve para la funcion de use_preprocessing abajo de esta para explicar esta parte, es importante.
    pool.close()
    pool.join()

    return data  # return al dataframe ya unido


def use_preprocessing(data):
    # Como tengo que poner la data cuando inicialize la funcion 'preprocessing_PA', y no puedo ponerla despues en la funcion de 'intervalize_dt' pues tengo que crear esta funcion

    # esta funcion es la que se va a poner dentro del parametro 'func' en pool.map(func,df)
    # Hice esta funcion para que inicialice, ponga la data, y luego saque la funcion del class a la misma vez porque no me dejaba poner el preprocessing_PA como tal
    # ni el preprocessing_PA().intervalize_dt(). Esta solucion la encontre en el internet.

    bot = Restructuring(data,step_interval=5)

    return bot.create_dataset()


def main():
    data = pd.read_csv("Ride_data_with_hex.csv")

    inter = datecolumns(data)
    data = inter.intervalize()

    df_splitted = parallelize_dataframe(data, use_preprocessing, n_cores=10)

    df_splitted.to_csv('Preprocessing_DF.csv', index=False)

    # tool = testingZones(data)
    # tool.create_dataset()

    return

if __name__=="__main__":
    main()


















