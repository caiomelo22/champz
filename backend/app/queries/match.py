get_matches_query = """
    SELECT 
        m.id,
        m.participant_1_id,
        p1.name as participant_1_name,
        t1.name as participant_1_team_name,
        t1.image_path as participant_1_team_image_path,
        m.participant_2_id,
        p2.name as participant_2_name,
        t2.name as participant_2_team_name,
        t2.image_path as participant_2_team_image_path,
        m.goals_1,
        m.goals_2,
        m.round,
        m.penalties
    FROM `fifa-db`.match m
        INNER JOIN `fifa-db`.team t1
            ON m.participant_1_id = t1.participant_id
        INNER JOIN `fifa-db`.participant p1
            ON m.participant_1_id = p1.id
        INNER JOIN `fifa-db`.team t2
            ON m.participant_2_id = t2.participant_id
        INNER JOIN `fifa-db`.participant p2
            ON m.participant_2_id = p2.id
"""

create_matches_query = """
    INSERT INTO `fifa-db`.match (group_id, participant_1_id, participant_2_id, round)
    VALUES (%s, %s, %s, %s)
"""

update_match_query = """
    UPDATE `fifa-db`.match 
    SET goals_1 = %s, goals_2 = %s, penalties = %s
    WHERE id = %s
"""

match_exists_query = """
    SELECT COUNT(*) as num_matches
    FROM `fifa-db`.match
    WHERE id = %s
    LIMIT 1
"""

delete_matches_from_round_and_above_query = """
    DELETE FROM `fifa-db`.match
    WHERE group_id = %s AND round <= %s;
"""
