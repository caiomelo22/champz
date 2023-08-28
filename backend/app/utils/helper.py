import math


def get_knockout_info(number_of_players):
    power_of_2 = 2 ** math.floor(math.log2(number_of_players))
    qualified_players = min(power_of_2, number_of_players)
    return qualified_players, min(power_of_2, number_of_players) // 2
