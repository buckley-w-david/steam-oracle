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
		return '{}:{}'.format(self.game.common_name, self.game.steam_id)

	def __hash__(self):
		return hash(repr(self))

	def __eq__(self, other):
		return type(other) is Game_Entry and other.game == self.game

# Create your models here.
class Profile(models.Model):
	steam_id = models.CharField(max_length=17) #Validators?

	games = models.ManyToManyField(Game_Entry, related_name='owned_games')

	def similarity(self, profile):
		#Possible that I should do each of the below queries (in the actual string) separatly and take the common elements locally
		#Less of the work on DB (bad), less work overall (good)
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
	recommend_game_entry.score > 0 AND
	recommend_game_entry.game_id IN (
		SELECT 
			recommend_game_entry.game_id
		FROM recommend_game_entry
		INNER JOIN recommend_profile_games 
			ON recommend_game_entry.id = recommend_profile_games.game_entry_id
		INNER JOIN recommend_profile
			ON recommend_profile.id == recommend_profile_games.profile_id
		WHERE 
			recommend_profile.steam_id=%s AND
			recommend_game_entry.score > 0
		)
ORDER BY
	recommend_game_entry.game_id"""

		self_games = Game_Entry.objects.raw(game_entry_query, [self.steam_id, profile.steam_id])
		profile_games = Game_Entry.objects.raw(game_entry_query, [profile.steam_id, self.steam_id])
		similarity = 100
		length = len(self_games)
		adj = similarity/(length*9)
		
		similarity - adjustment*(len(self_games)*9) == 0
		for game_self, game_profile in zip(self_games, profile_games):
			diff = abs(game_self.score - game_profile.score)
			similarity -= adj*diff

		return similarity


	def __str__(self):
		return self.steam_id

	def __repr__(self):
		return self.steam_id
		
	def __hash__(self):
		return hash(repr(self))

