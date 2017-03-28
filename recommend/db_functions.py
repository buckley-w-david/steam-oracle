from recommend.models import Game, Profile

def add_profile(steam_id):
	existing_entry = Profile.objects.filter(steam_id=steam_id)
	code = 0
	if existing_entry.count() > 0:
		user_profile = existing_entry.get()
	else:
		user_profile = Profile(steam_id=steam_id)
		user_profile.save()
		code = 1
	
	return code, user_profile

def add_game(app_id, name):
	existing_entry = Game.objects.filter(steam_id=app_id)
	code = 0
	if existing_entry.count() > 0:
		game_entry = existing_entry.get() #Should only be one result, .get() should grab it
	else:
		game_entry = Game(steam_id=app_id, common_name=name)
		game_entry.save()
		code = 1

	return code, game_entry

if __name__=='__main__':
	file = input('enter file to migrate: ')
	migrate_profiles(file)