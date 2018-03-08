import pandas as pd
df1= pd.read_csv("NCAATourneyCompactResults.csv")
df2= pd.read_csv("RegularSeasonCompactResults.csv")

def datamake(year1,year2,df1,df2):
   Regular_year1 = df1[df1["Season"]==year1]
   Regular_year2 = df1[df1["Season"]==year2]
   Tourney_year2 = df2[df2["Season"]==year2]
   Whole_year2 =  pd.concat([Regular_year2,Tourney_year2],ignore_index=True)
   data = pd.concat([Regular_year1,Whole_year2],ignore_index=True)
   return data

train_2013 = datamake(2011,2012,df1,df2)

print(train_2013)