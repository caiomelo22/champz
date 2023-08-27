group_exists_query = """
    SELECT COUNT(*) as num_groups
    FROM `fifa-db`.group
    WHERE id = :group_id
"""
