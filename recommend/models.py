from django.db import models

class Game(models.Model):
	steam_id = models.CharField(max_length=200) #Validators?
	common_name = models.CharField(max_length=200) #Validators?

	def __str__(self):
		return '{}:{}'.format(self.common_name, self.steam_id)

	def __repr__(self):
		return '{}:{}'.format(self.common_name, self.steam_id)

	def __hash__(self):
		return hash(repr(self))

	def __eq__(self, other):
		return type(other) is Game and other.steam_id == self.steam_id and other.common_name == self.common_name

class Game_Entry(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	score = models.IntegerField(default=-1) #-1 = not played

	def __str__(self):
		return '{}:{} score={}'.format(self.game.common_name, self.game.steam_id, self.score)

	def __repr__(self):
		return '{}:{}'.format(self.game.common_name, self.game.steam_id, self.score)

	def __hash__(self):
		return hash(repr(self))

	def __eq__(self, other):
		return type(other) is Game_Entry and other.game == self.game

# Create your models here.
class Profile(models.Model):
	steam_id = models.CharField(max_length=17) #Validators?

	games = models.ManyToManyField(Game_Entry, related_name='owned_games')

	def similarity(self, profile):
		'''I very much dislike this, it feels like it takes forever.
		profile_liked_games = set(profile.liked_games.all())
		self_liked_games = set(self.liked_games.all())

		profile_played_games = set(profile.played_games.all())
		self_played_games = set(self.played_games.all())

		total_self = len(self_liked_games)
		total_other = len(profile_liked_games)
		total = total_self+total_other

		diff_self = self_liked_games.difference(profile_liked_games)
		diff_other = profile_liked_games.difference(self_liked_games)

		if (len(diff_self) == len(self_liked_games)):
			return 0 #Nothing in common

		disagreements_self = 0 #Games that you like and they don't
		for game in diff_self:
			if game in profile_played_games:
				disagreements_self += 1

		disagreements_other = 0 #Games that they like and you don't
		for game in diff_other:
			if game in self_played_games:
				disagreements_other += 1

		disagreements = disagreements_self + disagreements_other
		return (total-disagreements)/total'''

		game_entry_query = """
SELECT 
	recommend_game_entry.id as id, 
	recommend_game_entry.score as score, 
	recommend_game_entry.game_id as game_id
FROM recommend_game_entry
INNER JOIN recommend_profile_games 
	ON recommend_game_entry.id = recommend_profile_games.game_entry_id
INNER JOIN recommend_profile
	ON recommend_profile.id == recommend_profile_games.profile_id
WHERE 
	recommend_profile.steam_id=%s AND
	recommend_game_entry.game_id IN (
		SELECT 
			recommend_game_entry.game_id
		FROM recommend_game_entry
		INNER JOIN recommend_profile_games 
			ON recommend_game_entry.id = recommend_profile_games.game_entry_id
		INNER JOIN recommend_profile
			ON recommend_profile.id == recommend_profile_games.profile_id
		WHERE 
			recommend_profile.steam_id=%s
		)"""

		self_games = Game_Entry.objects.raw(game_entry_query, [self.steam_id, profile.steam_id])
		profile_games = Game_Entry.objects.raw(game_entry_query, [profile.steam_id, self.steam_id])

		return 0.5


	def __str__(self):
		return self.steam_id

	def __repr__(self):
		return self.steam_id
		
	def __hash__(self):
		return hash(repr(self))

