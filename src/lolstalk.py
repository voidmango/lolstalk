#import pkgs
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

def get_last_info(name):
    my_player = get_player(name)

    my_matches = watcher.match.matchlist_by_puuid(my_region, my_player['puuid'])

    # fetch last match detail
    last_match = my_matches[0]
    match_info = watcher.match.by_id(my_region, last_match)

    participants = []
    for row in match_info['info']['participants']:
        print(row)
        participants_row = {}
        participants_row['Username'] = puuid_to_name(row['puuid'])
        participants_row['champion'] = row['championName']
        participants_row['kills'] = row['kills']
        participants_row['deaths'] = row['deaths']
        participants_row['assists'] = row['assists']
        participants.append(participants_row)
    df = pd.DataFrame(participants).set_index('Username')

    return df