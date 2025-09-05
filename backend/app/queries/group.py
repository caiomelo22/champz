group_exists_query = """
    SELECT COUNT(*) as num_groups
    FROM `fifa-db`.group
    WHERE id = %s
"""

create_group_query = """
    INSERT INTO `fifa-db`.group (name) 
    VALUES (%s)
"""

get_group_query = """
    SELECT id, name from `fifa-db`.group
    LIMIT 1
"""

add_participant_to_group_query = """
    INSERT INTO `fifa-db`.group_participant
    (group_id, participant_id)
    VALUES (%s, %s)
"""

get_participants_by_group_query = """
    SELECT 
        p.id, 
        p.name, 
        p.budget,
        t.name as team_name, 
        t.image_path as team_image_path
    FROM `fifa-db`.group g
        INNER JOIN `fifa-db`.group_participant gp
            ON g.id = gp.group_id
        INNER JOIN `fifa-db`.participant p
            ON gp.participant_id = p.id
        INNER JOIN `fifa-db`.team t
            ON p.id = t.participant_id
    WHERE g.id = %s;
"""

get_group_table_query = """
    SELECT
        g.id AS group_id,
        gp.participant_id AS participant_id,
        p.name as name,
        t.image_path as team_image_path,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END), 0) AS GF,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END), 0) AS GA,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END), 0) AS W,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 < m.goals_2) ELSE (m.goals_2 < m.goals_1) END), 0) AS L,
        COALESCE(SUM(CASE WHEN m.goals_1 = m.goals_2 THEN 1 ELSE 0 END), 0) AS D,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END) - SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END), 0) AS GD,
        COALESCE((SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END) * 3) +
        COALESCE(SUM(CASE WHEN m.goals_1 = m.goals_2 THEN 1 ELSE 0 END), 0), 0) AS P
    FROM `fifa-db`.group g
        INNER JOIN `fifa-db`.group_participant gp
            ON g.id = gp.group_id
        INNER JOIN `fifa-db`.team t
            ON gp.participant_id = t.participant_id
        INNER JOIN `fifa-db`.participant p
            ON gp.participant_id = p.id
        LEFT JOIN `fifa-db`.match m
            ON g.id = m.group_id AND (gp.participant_id = m.participant_1_id OR gp.participant_id = m.participant_2_id)
    WHERE g.id = %s AND m.round = (
        SELECT
            MAX(m3.round)
        FROM `fifa-db`.match m3
        WHERE g.id = %s
    )
    GROUP BY group_id, participant_id
    ORDER BY P DESC, GD DESC, GF DESC, GA ASC;
"""

delete_group_query = """
    DELETE FROM `fifa-db`.group
    WHERE id = %s
"""
