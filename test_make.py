import pandas as pd


df_tour = pd.read_csv("./input/NCAATourneyCompactResults.csv")
df_seed = pd.read_csv("./input/NCAATourneySeeds_SampleTourney2018.csv")
df_tour["WTseed"]=""
df_tour["LTseed"]=""
df_tour["Wsea"]=""
df_tour["Lsea"]=""


def seed_in(df1_,df2_):
    df1_=df1_.reset_index()
    df2_=df2_.reset_index()
    for i in range(len(df1_)):
        for j in range(len(df2_)):
            if df1_["WTeamID"][i] == df2_["TeamID"][j]:
                df1_["WTseed"].loc[i]=df2_["Seed"][j][1:3]
                df1_["Wsea"].loc[i] = df2_["Seed"][j][0]
    for i in range(len(df1_)):
        for j in range(len(df2_)):
            if df1_["LTeamID"][i] == df2_["TeamID"][j]:
                df1_["LTseed"].loc[i]=df2_["Seed"][j][1:3]
                df1_["Lsea"].loc[i] = df2_["Seed"][j][0]
    return df1_


def test_set(year,df_tour,df_seed):
    df_year_o = df_tour[df_tour["Season"]==year]
    df_year_f= seed_in(df_year_o,df_seed)
    return df_year_f

test_2014=test_set(2014,df_tour,df_seed)
test_2015=test_set(2015,df_tour,df_seed)
test_2016=test_set(2016,df_tour,df_seed)
test_2017=test_set(2017,df_tour,df_seed)

test_2014.to_csv("./ouput/test_2014.csv")
test_2015.to_csv("./ouput/test_2015.csv")
test_2016.to_csv("./ouput/test_2016.csv")
test_2017.to_csv("./ouput/test_2017.csv")
