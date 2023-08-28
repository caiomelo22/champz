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
        t.id as team_id,
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
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END), 0) AS goals_scored,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END), 0) AS goals_conceded,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END), 0) AS wins,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 < m.goals_2) ELSE (m.goals_2 < m.goals_1) END), 0) AS losses,
        COALESCE(SUM(CASE WHEN m.goals_1 = m.goals_2 THEN 1 ELSE 0 END), 0) AS draws,
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END) - SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END), 0) AS goal_difference,
        COALESCE((SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END) * 3) +
        COALESCE(SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 = m.goals_2) ELSE 0 END), 0), 0) AS points
    FROM `fifa-db`.group g
        LEFT JOIN `fifa-db`.group_participant gp
            ON g.id = gp.group_id
        LEFT JOIN `fifa-db`.match m
            ON g.id = m.group_id AND (gp.participant_id = m.participant_1_id OR gp.participant_id = m.participant_2_id)
    WHERE g.id = %s AND m.round IS NULL
    GROUP BY group_id, participant_id
    ORDER BY points DESC, goal_difference DESC, goals_scored DESC, goals_conceded ASC;
"""

delete_group_query = """
    DELETE FROM `fifa-db`.group
    WHERE id = %s
"""
