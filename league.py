class LeagueSettings:

    def __init__(self, num_teams, categories, playable_per_position, bench_size):
        """

        :param num_teams: int, number of teams in the league
        :param categories: list of categories that count for scoring
        :param playable_per_position: list of tuples,
            first entry is the Position and the second is the number at that position
        :param bench_size: int, number of players allowed to be kept on the bench
        """
        self.categories = categories
        self.num_teams = num_teams
        self.playable_per_position = playable_per_position
        self.bench_size = bench_size

    def get_number_of_players(self):
        return (sum([n for _, n in self.playable_per_position]) +
                self.bench_size)