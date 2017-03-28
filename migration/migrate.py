import pickle
import game
import profile
from recommend.db_functions import add_profile
from recommend.db_functions import add_game

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def migrate_profiles(file):
	with open(file, 'rb') as f:
		profiles = pickle.load(f)

	count = 0

	printProgressBar(0, len(profiles), prefix = 'Progress:', suffix = 'Complete', length = 50)
	for profile in profiles:
		code, new_profile = add_profile(profile.steam_id)
		games = profile.liked.union(profile.unliked)
		for game in games:
			name = game.common_name
			app_id = game.steam_id
			played = game.minutes > 0
			liked = game.minutes >= 420

			code, new_game = add_game(app_id, name)
			new_profile.owned_games.add(new_game)
			if played:
				new_profile.played_games.add(new_game)
			if liked:
				new_profile.liked_games.add(new_game)
		count += 1
		printProgressBar(count, len(profiles), prefix = 'Progress:', suffix = 'Complete', length = 50)