get_id_and_participant_id_by_id_query = """
    SELECT id, participant_id
    FROM `fifa-db`.team
    WHERE id = :team_id
    LIMIT 1
"""

get_participant_id_by_team_query = """
    SELECT participant_id as participant_id
    FROM `fifa-db`.team
    WHERE id = :team_id
    LIMIT 1
"""

add_participant_to_team_query = """
    UPDATE `fifa-db`.team
    SET participant_id = :participant_id
    WHERE id = :team_id;
"""

get_teams_by_league_query = """
    SELECT t.*, l.name as league_name, l.image_path as league_image_path
    FROM `fifa-db`.team t
        LEFT JOIN `fifa-db`.league l
            ON t.league_id = l.id
    WHERE t.league_id = :league_id
"""
