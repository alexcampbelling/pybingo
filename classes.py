class Player:
    def __init__(self, name, ehp, ehb, ehp_avg,
                 ehb_avg, slayer_ability, tiles_score):
        self.name = name
        self.ehp = ehp
        self.ehb = ehb
        self.ehp_avg = ehp_avg
        self.ehb_avg = ehb_avg
        self.slayer_ability = slayer_ability
        self.tiles_score = tiles_score
        self.manual_score = 0
        self.weighted_score = None

    def score_self(self):
        self.weighted_score = 0


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.score = 0
