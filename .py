import csv
import pandas as pd
from functools import reduce


#input below
ranked_fighters = {'Valentina Shevchenko': {'Rank': 2, 'Odds': -159}, 'Julianna Pena': {'Rank': 15, 'Odds': 135}, 'Jorge Masvidal': {'Rank': 13, 'Odds': 128}, 'Donald Cerrone': {'Rank': 8, 'Odds': -153}, 'Francis Ngannou': {'Rank': 1, 'Odds': -382}, 'Andrei Arlovski': {'Rank': 22, 'Odds': 301}, 'Jason Knight': {'Rank': 6, 'Odds': -147}, 'Alex Caceres': {'Rank': 18, 'Odds': 123}, 'Sam Alvey': {'Rank': 9, 'Odds': -148}, 'Nate Marquardt': {'Rank': 14, 'Odds': 124}, 'Aljamain Sterling': {'Rank': 19, 'Odds': 121}, 'Raphael Assuncao': {'Rank': 5, 'Odds': -145}, 'Li Jingliang': {'Rank': 4, 'Odds': -131}, 'Bobby Nash': {'Rank': 20, 'Odds': 108}, 'Eric Spicely': {'Rank': 11, 'Odds': -117}, 'Alessio Di Chirico': {'Rank': 3, 'Odds': -106}, 'Marcos Rogerio de Lima': {'Rank': 7, 'Odds': -150}, 'Jeremy Kimball': {'Rank': 16, 'Odds': 126}, 'Alexandre Pantoja': {'Rank': 21, 'Odds': 107}, 'Eric Shelton': {'Rank': 10, 'Odds': -131}, 'Jason Gonzalez': {'Rank': 17, 'Odds': 115}, 'JC Cottrell': {'Rank': 12, 'Odds': -139}}


all_combinations = [row for row in csv.reader(open("C:/Users/micha/Desktop/Diversification_Data/Diversification_Data_15.csv", "r"))]
all_combinations.sort(key=lambda row: row[-1], reverse=True)
top_combinations = []
next_rank = 1
worst_rank = reduce(
    lambda fighter_a, fighter_b: fighter_a
    if fighter_a["Rank"] > fighter_b["Rank"]
    else fighter_b,
    ranked_fighters.values(),
)["Rank"]
rank_counts = [0] * worst_rank
recent_ranks = [-1] * 3


def allowed_odds(fighter):
    max_count=86
    if ranked_fighters[fighter]['Odds'] <= -275:
        max_count=86.
    elif ranked_fighters[fighter]['Odds'] <=-225:
        max_count = 75
    elif ranked_fighters[fighter]['Odds'] <=-150:
        max_count = 67
    elif ranked_fighters[fighter]['Odds'] <=0:
        max_count = 62
    elif ranked_fighters[fighter]['Odds'] <=175:
        max_count = 52
    elif ranked_fighters[fighter]['Odds'] <=300:
        max_count = 40
    elif ranked_fighters[fighter]['Odds'] <=400:
        max_count = 28
    elif ranked_fighters[fighter]['Odds'] <=10000:
        max_count = 17
    return rank_counts[ranked_fighters[fighter]['Rank']-1] > max_count


for _ in range(150):
    recent_ranks.pop(0)
    recent_ranks.append(next_rank)
    for index, combination in zip(range(len(all_combinations)), all_combinations):
        if not any(map(allowed_odds, combination[:6])):
            if not any(map(lambda lineup: len(set(combination[:6]) & set(lineup[:6])) >= 5, top_combinations)):
                for fighter in combination[:6]:
                    if ranked_fighters[fighter]["Rank"] == next_rank:
                        print(f"Found match at {index:3} for rank {next_rank:2}: {fighter}")
                        # Count the fighters in the combination we found
                        for _fighter in combination[:6]:
                            rank_counts[ranked_fighters[_fighter]["Rank"] - 1] += 1
                            print(rank_counts)
                        top_combinations.append(all_combinations.pop(index))  # Add the combination we found
                        break  # Stop looking for next_rank
                else:
                    # This only happens when break isn't used
                    continue  # Current combination isn't invalid so skip back to the top of the loop
                break  # Current combination was valid so stop looping
    else:
        # This only happens when break isn't used
        print(
            f"No combination could be found for {next_rank}, changing worst rank and moving on"
        )
    ranks_check_next = [
        rank + 1
        for rank in range(worst_rank - 1)
        if rank + 1 not in recent_ranks and rank_counts[rank] <= rank_counts[rank + 1]
    ]
    next_rank = ranks_check_next[-1] if len(ranks_check_next) else worst_rank

print(len(top_combinations))

with open('Tier_15.csv', 'w', newline='') as f:
    thewriter=csv.writer(f)
    thewriter.writerow(['Player 1','Player 2','Player 3','Player 4','Player 5','Player 6','Score'])
    for comb in top_combinations:
        thewriter.writerow(comb)
