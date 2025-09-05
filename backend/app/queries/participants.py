list_participants_query = """
    SELECT 
        p.id, 
        p.name, 
        p.budget, 
        t.name as team_name, 
        t.image_path as team_image_path 
    FROM `fifa-db`.participant p
        LEFT JOIN `fifa-db`.team t
            ON p.id = t.participant_id
"""

num_participants_query = """
    SELECT COUNT(*) as num_participants
    FROM `fifa-db`.participant
"""

change_participant_budget_query = """
    UPDATE `fifa-db`.participant
    SET budget = budget + %s
    WHERE id = %s;
"""

get_participant_budget_query = """
    SELECT budget
    FROM `fifa-db`.participant
    WHERE id = %s
    LIMIT 1
"""

insert_participant_query = """
    INSERT INTO `fifa-db`.participant (name, budget)
    VALUES (%s, %s);
"""

update_participant_query = """
    UPDATE `fifa-db`.participant
    SET name = %s, budget = %s
    WHERE id = %s;
"""

delete_participant_query = """
    DELETE FROM `fifa-db`.participant
    WHERE id = %s;
"""

get_participants_ids_query = """
    SELECT id FROM `fifa-db`.participant;
"""
