import requests as req
import pandas as pd
import csv
import constants
from classes import Player, Team
from helpers import read_usernames


def create_players(player_names):
    failed_players = []
    players = []
    for player in player_names:
        # try get data from Temple
        try:
            # make API calls

            # collect data from returns

            print('get data here')
            # create Player class here and append to 'players'
            players.append(
                Player(player,
                       ehp,
                       ehb,
                       ehp_avg,  # this should be a fn
                       ehb_avg,  # this should be a fn
                       slayer_ability,  # this should be a fn
                       tiles_score  # this should be a fn
                       ))
        except:
            print('failed to get player information here')
            failed_players.append(player)
            # still add a blank player class
            players.append(Player(player, 0, 0, 0, 0, 0, 0))
    return (players, failed_players)

# TODO: make this all with arguments so can have separate steps


def main():
    # read player names in
    player_names = read_usernames(player_name.txt)

    # attempt to get data for players
    players, failed_players = create_players(player_names)

    # print list of failed players to command line
    # TODO

    #


if __name__ == "__main__":
    main()
