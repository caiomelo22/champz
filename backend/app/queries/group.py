group_exists_query = """
    SELECT COUNT(*) as num_groups
    FROM `fifa-db`.group
    WHERE id = :group_id
"""

create_group_query = """
    INSERT INTO `fifa-db`.group (name) 
    VALUES (:group_name)
"""

get_group_query = """
    SELECT id, name from `fifa-db`.group
    LIMIT 1
"""

add_participant_to_group_query = """
    INSERT INTO `fifa-db`.group_participant
    (group_id, participant_id)
    VALUES (:group_id, :participant_id)
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
    WHERE g.id = :group_id;
"""

get_group_table_query = """
    SELECT
        g.id as group_id,
        gp.participant_id as participant_id,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END) AS goals_scored,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END) AS goals_conceded,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END) AS wins,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 < m.goals_2) ELSE (m.goals_2 < m.goals_1) END) AS losses,
        SUM(CASE WHEN m.goals_1 = m.goals_2 THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_1 ELSE m.goals_2 END) - SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN m.goals_2 ELSE m.goals_1 END) AS goal_difference,
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 > m.goals_2) ELSE (m.goals_2 > m.goals_1) END) * 3 +
        SUM(CASE WHEN gp.participant_id = m.participant_1_id THEN (m.goals_1 = m.goals_2) ELSE 0 END) AS points
    FROM `fifa-db`.group g
        LEFT JOIN `fifa-db`.match m
            ON g.id = m.group_id
        LEFT JOIN `fifa-db`.group_participant gp
            ON g.id = gp.group_id
    WHERE g.id = :group_id and m.round is NULL
    GROUP BY group_id, participant_id
    ORDER BY points DESC, goal_difference DESC, goals_scored DESC, goals_conceded ASC;
"""
