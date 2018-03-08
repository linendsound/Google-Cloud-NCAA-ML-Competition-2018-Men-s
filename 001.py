import pandas as pd
df1= pd.read_csv("NCAATourneyCompactResults.csv")
df2= pd.read_csv("RegularSeasonCompactResults.csv")
df3 = pd.read_csv("NCAATourneySeeds.csv")
df1["WTseed"]=""
df1["LTseed"]=""

def seed_in(df1,df2):
    df1=df1.reset_index()
    df2=df2.reset_index()
    for i in range(len(df1)):
        for j in range(len(df2)):
            if df1["WTeamID"][i] == df2["TeamID"][j]:
                df1["WTseed"].loc[i]=df2["Seed"][j][1:3]
    for i in range(len(df1)):
        for j in range(len(df2)):
            if df1["LTeamID"][i] == df2["TeamID"][j]:
                df1["LTseed"].loc[i]=df2["Seed"][j][1:3]
    return df1


def whole_season(year, df):
    Regular_year1 = df1[df1["Season"] == year]
    Tourney_year1 = df2[df2["Season"] == year]
    Whole_year1 = pd.concat([Regular_year1, Tourney_year1], ignore_index=True)
    Seed = df[df["Season"]==year]
    Whole_year=seed_in(Whole_year1,Seed)
    return Whole_year


def datamake(year1,year2,year3,df1,df3):
    Whole_year1=whole_season(year1,df3)
    Whole_year2 = whole_season(year2, df3)
    Seed = df3[df3["Season"] == year3]
    Regular_year3 = df1[df1["Season"] == year3]
    Regular_year3 = seed_in(Regular_year3,Seed)
    data = pd.concat([Regular_year3,Whole_year1,Whole_year2],ignore_index=True)
    return data

train_2013 = datamake(2011,2012,2013,df1,df3)



print(train_2013)