import pandas as pd

df_reg= pd.read_csv("./input/RegularSeasonCompactResults_Prelim2018.csv")
df_tour= pd.read_csv("./input/NCAATourneyCompactResults.csv")
df_seed = pd.read_csv("./input/NCAATourneySeeds_SampleTourney2018.csv")
df_reg["WTseed"]=""
df_reg["LTseed"]=""
df_reg["Wsea"]=""
df_reg["Lsea"]=""


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


def whole_season(year, df):
    Regular_year1 = df_reg[df_reg["Season"] == year]
    Tourney_year1 = df_tour[df_tour["Season"] == year]
    Whole_year1 = pd.concat([Regular_year1, Tourney_year1], ignore_index=True)
    Seed = df[df["Season"]==year]
    Whole_year=seed_in(Whole_year1,Seed)
    return Whole_year


def datamake(year1,year2,year3,df_reg,df_seed):
    Whole_year1=whole_season(year1,df_seed)
    Whole_year2 = whole_season(year2,df_seed)
    Seed = df_seed[df_seed["Season"] == year3]
    Regular_year3 = df_reg[df_reg["Season"] == year3]
    Regular_year3 = seed_in(Regular_year3,Seed)
    data = pd.concat([Regular_year3,Whole_year1,Whole_year2],ignore_index=True)
    return data


train_2014 = datamake(2012,2013,2014,df_reg,df_seed).dropna()
train_2015 = datamake(2013,2014,2015,df_reg,df_seed).dropna()
train_2016 = datamake(2014,2015,2016,df_reg,df_seed).dropna()
train_2017 = datamake(2015,2016,2017,df_reg,df_seed).dropna()
train_2018 = datamake(2016,2017,2018,df_reg,df_seed).dropna()

train_2014.to_csv("./ouput/train_2014.csv")
train_2015.to_csv("./ouput/train_2015.csv")
train_2016.to_csv("./ouput/train_2016.csv")
train_2017.to_csv("./ouput/train_2017.csv")
train_2018.to_csv("./ouput/train_2018.csv")
