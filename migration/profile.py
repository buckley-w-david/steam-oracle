import recommend.game

class Profile:
    def __init__(self, steam_id, games):
        self.steam_id = steam_id
        
        self.played = played = {game for game in games if game.minutes > 0}
        
        self.liked = game.liked(played)
        self.unliked = games.difference(self.liked)

        self.total_minutes = sum(game.minutes for game in games)

    def similarity(self, profile):
        '''
        diff: Games liked by self, but either not liked or not played by profle

        If a game is not liked, detract from similarity
        '''
        total_self = len(self.liked)
        total_other = len(profile.liked)
        total = total_self+total_other
        
        diff_self = self.liked.difference(profile.liked)
        diff_other = profile.liked.difference(self.liked)

        
        if (len(diff_self) == len(self.liked)):
            return 0 #Nothing in common
        
        disagreements_self = 0 #Games that you like and they don't
        for game in diff_self:
            if game in profile.played:
                disagreements_self += 1

        disagreements_other = 0 #Games that they like and you don't
        for game in diff_other:
            if game in self.played:
                disagreements_other += 1

        
        disagreements = disagreements_self + disagreements_other
        return (total-disagreements)/total

            
