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

# Create your models here.
class Profile(models.Model):
	steam_id = models.CharField(max_length=17) #Validators?

	owned_games = models.ManyToManyField(Game, related_name='owned_games')
	played_games = models.ManyToManyField(Game, related_name='played_games')
	liked_games = models.ManyToManyField(Game, related_name='liked_games')

	def similarity(self, profile):
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
		return (total-disagreements)/total

	def __str__(self):
		return self.steam_id

	def __repr__(self):
		return self.steam_id
		
	def __hash__(self):
		return hash(repr(self))

