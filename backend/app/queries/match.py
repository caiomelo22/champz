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
    INSERT INTO `fifa-db`.match (group_id, participant_1_id, participant_2_id, round, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

update_match_query = """
    UPDATE `fifa-db`.match 
    SET goals_1 = %s, goals_2 = %s, penalties = %s, updated_at = %s
    WHERE id = %s
"""

redraw_needed_query = """
    SELECT
		CASE
			WHEN EXISTS (
				SELECT 1
				FROM `fifa-db`.match m2
				WHERE m2.round IS NOT NULL
			)
			THEN COUNT(*)  -- There are matches with round not null
			ELSE 1  -- There are no matches with round not null
		END as num_matches_updated
    FROM
        `fifa-db`.match m1
    WHERE
        (m1.group_id = %s AND (m1.round IS NULL OR m1.round >= %s))
        AND m1.updated_at > (
            SELECT
                MIN(m2.created_at)
            FROM
                `fifa-db`.match m2
            WHERE
                (m2.group_id = %s AND (m2.round IS NULL OR m2.round < %s))
        );
"""

match_exists_by_id_query = """
    SELECT COUNT(*) as num_matches
    FROM `fifa-db`.match m
    WHERE m.id = %s
"""

round_exists_by_id_query = """
    SELECT COUNT(*) as num_matches
    FROM `fifa-db`.match m
    WHERE m.group_id = %s AND m.round = %s
"""

delete_matches_from_round_and_above_query = """
    DELETE FROM `fifa-db`.match m
    WHERE m.group_id = %s AND (m.round IS NOT NULL AND m.round <= %s);
"""
