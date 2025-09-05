get_id_and_participant_id_by_name_query = """
    SELECT name, participant_id
    FROM `fifa-db`.team
    WHERE name = %s
    LIMIT 1
"""

get_participant_id_by_team_query = """
    SELECT participant_id as participant_id
    FROM `fifa-db`.team
    WHERE name = %s
    LIMIT 1
"""

add_participant_to_team_query = """
    UPDATE `fifa-db`.team
    SET participant_id = %s
    WHERE name = %s;
"""

get_most_popular_teams_query = """
    SELECT t.*
    FROM `fifa-db`.team t
    INNER JOIN (
        SELECT t.name, COUNT(*) as n_players
        FROM `fifa-db`.team t
        INNER JOIN `fifa-db`.player p
        ON t.name = p.team_origin
        GROUP BY (t.name)
    ) pc
    ON t.name = pc.name
    ORDER BY pc.n_players DESC
    LIMIT 40;
"""
