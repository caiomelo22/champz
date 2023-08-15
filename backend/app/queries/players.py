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
    LEFT JOIN `fifa-db`.team as team_origin ON player.team_origin_id = team_origin.id
    LEFT JOIN `fifa-db`.team as team_participant ON player.team_participant_id = team_participant.id
    LEFT JOIN `fifa-db`.nation as nation ON player.nation_id = nation.id
"""

player_exists_by_id_query = """
    SELECT SELECT COUNT(*) AS player_count
    FROM player
    WHERE id = :player_id
"""

buy_player_query = """
    UPDATE `fifa-db`.player
    SET value = :value, team_participant_id = :team_participant_id
    WHERE id = :player_id;
"""

change_players_team_query = """
    UPDATE `fifa-db`.player
    SET team_participant_id = :new_team_id
    WHERE team_participant_id = :old_team_id;
"""
