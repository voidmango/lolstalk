# import pkgs
import os
import discord
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
import pandas as pd

load_dotenv()
# global vars
api_key = os.getenv('RIOTAPI_KEY')
watcher = LolWatcher(api_key)
my_region = 'na1'


def puuid_to_name(puuid):
    player = watcher.summoner.by_puuid(my_region, puuid)
    return player['name']


def get_player(name):
    player = watcher.summoner.by_name(my_region, name)
    return player


def get_match_history(name):
    my_player = get_player(name)
    my_matches = watcher.match.matchlist_by_puuid(my_region, my_player['puuid'])
    return my_matches


def get_last_info(name):
    my_matches = get_match_history(name)
    # fetch last match detail
    lg = game_info(my_matches, 0)
    return lg


def game_info(matches, index):

    last_match = matches[index]
    match_info = watcher.match.by_id(my_region, last_match)
    game_mode = match_info['info']['gameMode']
    participants = []
    print(match_info)
    for row in match_info['info']['participants']:
        # print(row)
        participants_row = {game_mode: row['summonerName'], 'champion': row['championName'], 'kills': row['kills'],
                            'deaths': row['deaths'], 'assists': row['assists']}
        participants.append(participants_row)
    df = pd.DataFrame(participants)
    df = df.reset_index(drop=True)

    t1_win = match_info['info']['participants'][0]['win']
    t2_win = "Victory" if not t1_win else "Defeat"
    t1_win = "Victory" if t1_win else "Defeat"

    team1 = pd.DataFrame(
        {game_mode: ['   Team 1 ' + t1_win], 'champion': [''], 'kills': [''], 'deaths': [''], 'assists': ['']})
    team2 = pd.DataFrame(
        {game_mode: ['   Team 2 ' + t2_win], 'champion': [''], 'kills': [''], 'deaths': [''], 'assists': ['']})
    df = pd.concat([team1, df.loc[0:]]).reset_index(drop=True)
    df = pd.concat([df.loc[:5], team2, df.loc[6:]]).set_index(game_mode)
    return df


def has_new_game(name):
    my_player = get_player(name)
    my_matches = watcher.match.matchlist_by_puuid(my_region, my_player['puuid'])
    last_match = my_matches[0]
    last_last_match = my_matches[1]
    if last_match == last_last_match:
        return False
    return True
