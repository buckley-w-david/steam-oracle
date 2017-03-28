from recommend.models import Game, Profile

def add_profile(steam_id):
	try:
		user_profile = Profile.objects.get(steam_id=steam_id)
	except Profile.DoesNotExist:
		user_profile = Profile.create(steam_id=steam_id)

	return user_profile

def add_game(app_id, name):
	try: 
		game_entry = Game.objects.get(steam_id=app_id)
	except Game.DoesNotExist:
		game_entry = Game.create(steam_id=app_id, common_name=name)

	return game_entry