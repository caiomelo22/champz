get_id_and_participant_id_by_id_query = """
    SELECT id, participant_id
    FROM `fifa-db`.team
    WHERE id = %s
    LIMIT 1
"""

get_participant_id_by_team_query = """
    SELECT participant_id as participant_id
    FROM `fifa-db`.team
    WHERE id = %s
    LIMIT 1
"""

add_participant_to_team_query = """
    UPDATE `fifa-db`.team
    SET participant_id = %s
    WHERE id = %s;
"""

get_most_popular_teams_query = """
    SELECT t.*
    FROM `fifa-db`.team t
    INNER JOIN (
        SELECT t.id, COUNT(*) as n_players
        FROM `fifa-db`.team t
        INNER JOIN `fifa-db`.player p
        ON t.id = p.team_origin_id
        GROUP BY (t.id)
    ) pc
    ON t.id = pc.id
    ORDER BY pc.n_players DESC
    LIMIT 40;
"""
