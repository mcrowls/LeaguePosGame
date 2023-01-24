import numpy as np
import pandas as pd
import os


class Season:
    def __init__(self, year, league):
        self.year = year
        self.league = league
        return

    def readInCSV(self):
        str = 'Data/' + self.year + '/' + self.league + '.csv'
        csv = pd.read_csv(str, error_bad_lines=False).dropna(how='all')
        self.csv = csv
        return


    def leagueTable(self, teams):
        unOrderedTable = []
        # teams = np.unique(self.csv['HomeTeam'])
        for team in teams:
            homeGames = self.csv.loc[self.csv['HomeTeam'] == team]
            awayGames = self.csv.loc[self.csv['AwayTeam'] == team]
            goalsScored = np.sum([homeGames.iloc[i]['FTHG'] for i in range(np.shape(homeGames)[0])] + [awayGames.iloc[i]['FTAG'] for i in range(np.shape(awayGames)[0])])
            homeGD = [homeGames.iloc[i]['FTHG'] - homeGames.iloc[i]['FTAG'] for i in range(np.shape(homeGames)[0])]
            awayGD = [awayGames.iloc[i]['FTAG'] - awayGames.iloc[i]['FTHG'] for i in range(np.shape(awayGames)[0])]
            gD = np.sum(homeGD) + np.sum(awayGD)
            homePoints = 3*np.shape(homeGames[homeGames['FTHG'] > homeGames['FTAG']])[0] + np.shape(homeGames[homeGames['FTHG'] == homeGames['FTAG']])[0]
            awayPoints = 3*np.shape(awayGames[awayGames['FTHG'] < awayGames['FTAG']])[0] + np.shape(awayGames[awayGames['FTHG'] == awayGames['FTAG']])[0]
            points = awayPoints + homePoints
            unOrderedTable.append({'Team': team, 'Points': points, 'GD': gD, 'Scored': goalsScored})
        orderedTable = sorted(unOrderedTable, key=lambda i: (i['Points'], i['GD'], i['Scored']))
        orderedTable.append({'Team': self.year})
        self.seasonTable = list(reversed([team['Team'] for team in orderedTable]))
        return self.seasonTable

    
    def getAllTeams(self):
        return np.unique(self.csv['HomeTeam'])



def getAllYears(path):
    return os.listdir(path)


leagues = ['Premier League', 'Championship', 'League One', 'League Two']
years = getAllYears('Data/')


allTeams = []
for league in leagues:
    arr = []
    for year in years:
        season = Season(year, league)
        season.readInCSV()
        teams = season.getAllTeams()
        if league != 'League Two':
            if year == '1993-94':
                headings = [i for i in range(len(teams)+1)]
                headings[0] = 'Year'
        else:
            if year == '2021-22':
                headings = [i for i in range(len(teams)+1)]
                headings[0] = 'Year'
        for team in teams:
            if team not in allTeams:
                allTeams.append(team)
        table = season.leagueTable(teams)
        arr.append(table)
    df = pd.DataFrame(arr, columns=headings)
    df.to_csv(league + 'Standings.csv')
