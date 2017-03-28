class Game:
    def __init__(self, steam_id, minutes, common_name=None):
        self.steam_id = str(steam_id)
        self.minutes = minutes
        self.common_name = common_name
        self.liked = False

    def __gt__(self, game2):
        if not type(game2) is Game:
            raise TypeError()
        return self.minutes > game2.minutes

    def __lt__(self, game2):
        if not type(game2) is Game:
            raise TypeError()
        return self.minutes < game2.minutes

    def __eq__(self, game2):
        if not type(game2) is Game:
            raise TypeError()
        return self.steam_id == game2.steam_id

    def __repr__(self):
        return '{}:{}'.format(self.common_name, self.steam_id)

        #return '{}:{} @ {} minutes'.format(self.common_name, self.steam_id, self.minutes)

    def __str__(self):
        return '{}:{} @ {} minutes'.format(self.common_name, self.steam_id, self.minutes)


    def __hash__(self):
        return hash(repr(self))

    '''
    @property
    def common_name(self):
        if self._common_name is None:
            global steamAPI #TODO: Fix this, it sucks
            try:
                details = steamAPI.AppDetails(self.steam_id)
            except RuntimeError as e:
                print(e)
                return 'ERROR'

            try:
                self._common_name = details[self.steam_id]['data']['name']
            except KeyError as e:
                self._common_name='N/A'
        
        return self._common_name
    '''

def from_iterable(iterable):
    return {Game(game['appid'], game['playtime_forever'], game['name']) for game in iterable}

def is_liked(game):
    return game.minutes >= 420 #Subject to change

def liked(games):
    return {game for game in games if is_liked(game)}


    
