league_exists_query = """
    SELECT COUNT(*) as num_leagues FROM `fifa-db`.league
    WHERE id = :league_id
    LIMIT 1
"""