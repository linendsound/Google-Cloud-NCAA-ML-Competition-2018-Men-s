import pandas as pd
import numpy as np
from sklearn import *

games = pd.read_csv('./Data/NCAATourneyCompactResults.csv')

#Add Ids
games['ID'] = games.apply(lambda r: '_'.join(map(str, [r['Season']]+sorted([r['WTeamID'],r['LTeamID']]))), axis=1)
games['IDTeams'] = games.apply(lambda r: '_'.join(map(str, sorted([r['WTeamID'],r['LTeamID']]))), axis=1)
games['Team1'] = games.apply(lambda r: sorted([r['WTeamID'],r['LTeamID']])[0], axis=1)
games['Team2'] = games.apply(lambda r: sorted([r['WTeamID'],r['LTeamID']])[1], axis=1)
games['IDTeam1'] = games.apply(lambda r: '_'.join(map(str, [r['Season'], r['Team1']])), axis=1)
games['IDTeam2'] = games.apply(lambda r: '_'.join(map(str, [r['Season'], r['Team2']])), axis=1)

#Add Seeds
seeds = pd.read_csv('./Data/NCAATourneySeeds.csv')
seeds = {'_'.join(map(str,[int(k1)+1,k2])):int(v[1:3]) for k1, v, k2 in seeds.values}
#add 2018 Seeds
seeds = {**seeds, **{k.replace('1999_','1998_'):seeds[k] for k in seeds if '1999_' in k}}

games['Team1Seed'] = games['IDTeam1'].map(seeds).fillna(0)
games['Team2Seed'] = games['IDTeam2'].map(seeds).fillna(0)

#Additional Features & Clean Up
games['ScoreDiff'] = games['WScore'] - games['LScore']
games['Pred'] = games.apply(lambda r: 1. if sorted([r['WTeamID'],r['LTeamID']])[0]==r['WTeamID'] else 0., axis=1)
games['ScoreDiffNorm'] = games.apply(lambda r: r['ScoreDiff'] * -1 if r['Pred'] == 0. else r['ScoreDiff'], axis=1)
games['SeedDiff'] = games['Team1Seed'] - games['Team2Seed']
games = games.fillna(-1)

sdn = games.groupby(['IDTeams'], as_index=False)[['ScoreDiffNorm']].mean()

#Test Set
sub = pd.read_csv('./Data/SampleSubmissionStage1.csv')
sub['Season'] = sub['ID'].map(lambda x: x.split('_')[0])
sub['Team1'] = sub['ID'].map(lambda x: x.split('_')[1])
sub['Team2'] = sub['ID'].map(lambda x: x.split('_')[2])
sub['IDTeams'] = sub.apply(lambda r: '_'.join(map(str, [r['Team1'], r['Team2']])), axis=1)
sub['IDTeam1'] = sub.apply(lambda r: '_'.join(map(str, [r['Season'], r['Team1']])), axis=1)
sub['IDTeam2'] = sub.apply(lambda r: '_'.join(map(str, [r['Season'], r['Team2']])), axis=1)
sub['Team1Seed'] = sub['IDTeam1'].map(seeds).fillna(0)
sub['Team2Seed'] = sub['IDTeam2'].map(seeds).fillna(0)
sub = pd.merge(sub, sdn, how='left', on=['IDTeams'])
sub['ScoreDiffNorm'] = sub['ScoreDiffNorm'].fillna(0.)
sub['SeedDiff'] = sub['Team1Seed'] - sub['Team2Seed']
sub.head()

col = [c for c in games.columns if c not in ['ID', 'IDTeams','IDTeam1','IDTeam2','Pred','DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'NumOT', 'ScoreDiff']]

reg = linear_model.Ridge(random_state=18)
reg.fit(games[col], games['Pred'])
sub['Pred'] = reg.predict(sub[col]).clip(0.,1.) * 0.4

reg = linear_model.HuberRegressor()
reg.fit(games[col], games['Pred'])
sub['Pred'] += reg.predict(sub[col]).clip(0.,1.) * 0.6

sub[['ID','Pred']].to_csv('rh3p_submission.csv', index=False)