list_participants_query = """
    SELECT 
        p.id, 
        p.name, 
        p.budget, 
        t.id as team_id,
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
    SET budget = budget + :value
    WHERE id = :participant_id;
"""

get_participant_budget_query = """
    SELECT budget
    FROM `fifa-db`.participant
    WHERE id = :participant_id
    LIMIT 1
"""

insert_participant_query = """
    INSERT INTO `fifa-db`.participant (name, budget)
    VALUES (:name, :budget);
"""

update_participant_query = """
    UPDATE `fifa-db`.participant
    SET budget = :budget, name = :name
    WHERE id = :participant_id;
"""
