league_exists_query = """
    SELECT COUNT(*) as num_leagues FROM `fifa-db`.league
    WHERE id = %s
    LIMIT 1
"""

get_leagues_query = """
    SELECT id, name, image_path FROM `fifa-db`.league;
"""
