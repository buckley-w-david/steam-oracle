import os, sys    
sys.path.append('steam_oracle\\steam_oracle')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steam_oracle.settings")

import django
django.setup()

from recommend.models import Profile, Game, Game_Entry

if __name__ == '__main__':
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
	self_games = Game_Entry.objects.raw(game_entry_query, ['76561197992685285', '76561197969020465'])
	profile_games = Game_Entry.objects.raw(game_entry_query, ['76561197969020465', '76561197992685285'])

	for game in self_games:
		print('self: {}'.format(game))
	for game in profile_games:
		print('profile: {}'.format(game))