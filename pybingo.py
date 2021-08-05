import requests as req
import pandas as pd
import sys
import csv
import constants as const
from classes import Player, Team
from helpers import read_usernames, make_players, calculate_slayer_ability, calculate_tile_score, calculate_final_score


def create_players(player_names):
    failed_players = []
    players = []
    players.append(["Username", "EHB", "EHB avg", "EHP",
                    "EHP avg", "Slayer Ability", "Tile Score", "Manual Score", "Weighted Score", "Final Score"])
    for player in player_names:
        # try get data from Temple
        try:
            # make API calls
            print('Attemping to get {}\'s data...'.format(player))

            p_req = player.replace(" ", "+")

            cur_stats = req.get(
                "https://templeosrs.com/api/player_stats.php?player={}&bosses=1".format(p_req)).json()

            rec_stats = req.get(
                "https://templeosrs.com/api/player_gains.php?player={}&time={}&bosses=1".format(p_req, const.SECS_IN_DAY * const.DAYS_IN_YEAR)).json()

            slayer_ability = calculate_slayer_ability(
                cur_stats["data"]["Slayer"], const.SLAYER_GOAL_XP)

            ehp = cur_stats["data"]["Ehp"]

            ehb = cur_stats["data"]["Ehb"]

            ehp_avg = rec_stats["data"]["Ehp"] / \
                (const.DAYS_IN_YEAR / const.AVERAGE_DAYS_COEFF)

            ehb_avg = rec_stats["data"]["Ehb"] / \
                (const.DAYS_IN_YEAR / const.AVERAGE_DAYS_COEFF)

            tiles_score = calculate_tile_score(cur_stats)

            weighted_score = calculate_final_score(
                ehb, ehb_avg, ehp, ehp_avg, slayer_ability, tiles_score, 0)

            players.append([
                player,
                ehb,
                ehb_avg,
                ehp,
                ehp_avg,
                slayer_ability,
                tiles_score,
                0,
                weighted_score,
                0
            ])
        except:
            failed_players.append(player)
            # still add a blank player class
            players.append([player, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return (players, failed_players)


def read_in_players(player_names_file):
    # read player names in
    player_names = read_usernames(player_names_file)

    # attempt to get data for players
    players_data, failed_players = create_players(player_names)

    print('Unable to get data for these players: {}'.format(failed_players))

    # print these players to an output csv
    with open("player_stats_rough.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(players_data)


def update_players_score(player_scored_file):

    with open(player_scored_file, newline='') as csvfile:
        old_data = list(csv.reader(csvfile))

    # delete headers
    del old_data[0]

    new_data = []
    new_data.append(["Username", "EHB", "EHB avg", "EHP",
                     "EHP avg", "Slayer Ability", "Tile Score", "Manual Score", "Weighted Score", "Final Score"])

    for player in old_data:
        # username,EHB,EHB avg,EHP,EHP avg,Slayer Ability,Tile Score,Manual Score,Final Score
        new_data.append([player[0], float(player[1]), float(player[2]),
                         float(player[3]), float(player[4]), float(player[5]),
                         float(player[6]), float(player[7]), float(
                             player[7]) + float(player[8])
                         ])

    with open("player_stats_with_manual.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(new_data)


def make_teams(player_scored_file, team_count):
    with open(player_scored_file, newline='') as csvfile:
        players_data = list(csv.reader(csvfile))

    # delete headers
    del players_data[0]

    # spread 'em
    # for player in sorted(players_data, key=lambda x: float(x[8]), reverse=True):
    #     print(player[0], player[8])

    dir = True
    count = 0
    # teams = [set() for _ in range(team_count)] # shows random order if set
    teams = [[] for _ in range(team_count)]
    for player in sorted(players_data, key=lambda x: float(x[8]), reverse=True):
        teams[count].append(player)
        if (count == team_count - 1 and dir == True) or (count == 0 and dir == False):
            dir = not dir
            continue
        if dir:
            count += 1
        else:
            count -= 1

    team_members = [[] for _ in range(team_count)]
    for i in range(len(teams)):
        score = 0
        print("Team {}".format(i+1))
        for player in teams[i]:
            team_members[i].append(player[0])
            score += float(player[8])
        print(team_members[i], score, len(team_members[i]))

def main():

    if (sys.argv[1] == 'read-in-players'):
        read_in_players(sys.argv[2])

    if (sys.argv[1] == 'update-players-score'):
        update_players_score(sys.argv[2])

    if (sys.argv[1] == 'make-teams'):
        make_teams(sys.argv[2], int(sys.argv[3]))


if __name__ == "__main__":
    main()
