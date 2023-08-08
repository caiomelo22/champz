get_participant_id_by_team_query = """
    SELECT participant_id as participant_id
    FROM `fifa-db`.team
    WHERE id = :team_id
    LIMIT 1
"""
