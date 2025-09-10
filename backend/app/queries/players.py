players_query = """SELECT
    player.*,
    team_participant.name as team_participant_name,
    team_participant.image_path as team_participant_image_path,
    team_participant.participant_id as participant_id,
    team_origin.name as team_origin_name,
    team_origin.image_path as team_origin_image_path,
    nation.name as nation_name,
    nation.image_path as nation_image_path,
    position.name as position_name
FROM
    `fifa-db`.player as player
    LEFT JOIN `fifa-db`.position as position ON player.position_id = position.id
    LEFT JOIN `fifa-db`.team as team_origin ON player.team_origin = team_origin.name
    LEFT JOIN `fifa-db`.team as team_participant ON player.team_participant = team_participant.name
    LEFT JOIN `fifa-db`.nation as nation ON player.nation = nation.name
"""

player_exists_by_id_query = """
    SELECT SELECT COUNT(*) AS player_count
    FROM player
    WHERE id = :player_id
"""

buy_player_query = """
    UPDATE `fifa-db`.player
    SET team_participant = %s, value = %s
    WHERE id = %s;
"""

change_players_team_query = """
    UPDATE `fifa-db`.player
    SET team_participant = %s
    WHERE team_participant = %s;
"""

reset_players_team_by_participant_id_query = """
    UPDATE `fifa-db`.player p
        INNER JOIN `fifa-db`.team t
            ON t.name = p.team_participant
        INNER JOIN `fifa-db`.participant part
            ON t.participant_id = part.id
    SET p.team_participant = null, p.value = null
    WHERE part.id = %s;
"""

player_transfers_query = """
    SELECT 
        p.name as name, p.overall, t.name as team_from, pt.name as team_to 
    FROM `fifa-db`.player p 
    JOIN `fifa-db`.team t
        ON p.team_origin = t.name 
    JOIN `fifa-db`.team pt
        ON p.team_participant = pt.name 
    WHERE 
        p.team_participant IS NOT NULL
        AND p.team_participant != p.team_origin
    ORDER BY team_from, team_to, overall DESC;
"""
