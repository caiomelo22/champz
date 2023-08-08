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
