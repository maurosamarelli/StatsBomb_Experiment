#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
path = "C:/Users/Mauro/Documents/open-data/data"

competitions = pd.read_json(os.path.join(path, "competitions.json"))
print(competitions.shape)

print(competitions)

def calculate_percentage_xg_messi(competitionId, seasonId, season_name):
    print("Processing " + season_name)
    matches = pd.read_json(os.path.join(path, "matches/" + str(competitionId) + "/" + str(seasonId) + ".json"))
    xg_messi, xg_barca = 0, 0
    for matchId in matches.match_id.unique():
        events = pd.read_json(os.path.join(path, "events/" + str(matchId) + ".json"))
        shots = events[events.shot == events.shot]
        for i in range(len(shots)):
            team = shots.iloc[i].team['name']
            player = shots.iloc[i].player['name']
            if 'Barcelona' in team:
                xg_barca = xg_barca + shots.iloc[i].shot['statsbomb_xg']
                if 'Messi' in player:
                    xg_messi = xg_messi + shots.iloc[i].shot['statsbomb_xg']
        percentage_xg_messi = round(xg_messi / xg_barca * 100, 2)
    return percentage_xg_messi

data = dict()
liga = competitions[(competitions.competition_id == 11) & ((competitions.season_id < 37) | (competitions.season_id > 40))]
for i in range(len(liga)):
    data[liga.iloc[i].season_name] = calculate_percentage_xg_messi(int(liga.iloc[i].competition_id), int(liga.iloc[i].season_id), liga.iloc[i].season_name)

print(data)

sorted_dict = sorted(data)
sorted_values = []
for val in sorted_dict:
    sorted_values.append(data[val])
plt.figure(figsize=(20, 8))
plt.plot(sorted_dict, sorted_values, marker='o')
plt.ylim(0, 60)
plt.title("% Contribution XG Team")

for i in range(len(sorted_values)-1):
    print(sorted_dict[i], ((sorted_values[i+1] / sorted_values[i]) - 1) * 100)