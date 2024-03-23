import math
from typing import List

from app.models.match import match

def get_knockout_info(number_of_players):
    return 4, 2
    power_of_2 = 2 ** math.floor(math.log2(number_of_players))
    qualified_players = min(power_of_2, number_of_players)
    return qualified_players, min(power_of_2, number_of_players) // 2

def get_round_winners(matches: List[match]) -> List[int]:
    aggregate_goals = {}
    processed_matches = set()
    
    # Calculate aggregate goals for each player
    for match in matches:
        player1, player2 = match.participant_1_id, match.participant_2_id
        goals1, goals2 = match.goals_1, match.goals_2
        
        aggregate_goals.setdefault(player1, 0)
        aggregate_goals.setdefault(player2, 0)
        
        aggregate_goals[player1] += goals1
        aggregate_goals[player2] += goals2
        
        # Add the match to the processed matches set
        processed_matches.add((player1, player2))
    
    # Determine winners based on aggregate goals
    winners = []
    for player1, player2 in processed_matches:
        goals1 = aggregate_goals[player1]
        goals2 = aggregate_goals[player2]
        
        if goals1 > goals2:
            winners.append(player1)
        elif goals1 < goals2:
            winners.append(player2)
        else:
            winners.append(player1)  # If tied, home participant goes through
    
    return winners