def _notify_all_teams_of_pick(teams, team_id, player):
    """Send a notification to each team (strategy) of a pick made."""
    for team in teams:
        team.draft_strategy.notify(team_id, player)

def _set_draft_order(league_settings, team_ids):
    """Returns a list representing order of team ids to pick."""
    forwards = range(league_settings.num_teams)
    backwards = list(reversed(forwards))
    draft_order = []
    for i in xrange(league_settings.get_number_of_players()):
        draft_order.extend(backwards if i % 2 else forwards)

    return draft_order

def simulate_draft(teams, players, league_settings):
    draft_order = _set_draft_order(league_settings,
                                   [team.id for team in teams])
    team_id_to_team = {team.id : team for team in teams}

    available_players = set(players)
    drafted_players = []

    for picking_team_id in draft_order:
        picking_team = team_id_to_team[picking_team_id]
        picked_player = picking_team.draft_strategy.pick(available_players)

        if not picked_player in available_players:
            raise ValueError(
                "Team %s tried to pick player %s that was not available. ",
                teams[picking_team_id],
                picked_player
            )

        available_players.remove(picked_player)
        drafted_players.append(picked_player)
        picking_team.add_to_roster(picked_player)
        _notify_all_teams_of_pick(teams, picking_team_id, picked_player)
