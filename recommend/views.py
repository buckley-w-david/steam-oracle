from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from recommend.models import Game, Profile
import recommend.steam as steam
import recommend.db_functions as db

from collections import defaultdict
import operator


def index(request):
    return render(request, 'recommend/index.html')

def get_recommendations(request):
	form_response = 'Invalid'
	if request.method == 'POST':
		form_response = 'Valid'
		vanity_name = request.POST['username']
		steam_id = request.POST['steam_id']

		api_key = '8FB1EB0966A3A2F4E0BEABF0509E7E98'
		steamAPI = steam.SteamAPI(api_key)

		if vanity_name:
			response = steamAPI.ResolveVanityURL(vanity_name)
			if response['response']['success']:
				steam_id = response['response']['steamid']

		#Validation is required on on the user input, for now assuming correct
		code, user_profile = db.add_profile(steam_id)
		if code:
			form_response += '\n {} added'.format(steam_id)

		games_response = steamAPI.GetOwnedGames(steam_id)
		user_games = games_response['response']['games']
		for game in user_games:
			app_id = game['appid']
			played = game['playtime_forever'] != 0
			liked = game['playtime_forever'] >= 420
			name = game['name']

			code, game_entry = db.add_game(app_id, name)
			if code:
				form_response += '\n {}:{} added'.format(app_id, name)

			user_profile.owned_games.add(game_entry)
			if played:
				user_profile.played_games.add(game_entry)
			if liked:
				user_profile.liked_games.add(game_entry)

		graph = defaultdict(int)
		for game in set(user_profile.owned_games.all()) - set(user_profile.played_games.all()):
			graph[game] = 0

		for profile in Profile.objects.all():
			similarity = user_profile.similarity(profile)
			for game in profile.liked_games.all():
				if game in graph:
					graph[game] += similarity

		graph_sorted = [game for game, rank in sorted(graph.items(), key=operator.itemgetter(1), reverse=True)]
		context = {
			'ordered_recommendation_list': graph_sorted,
		}

		return render(request, 'recommend/recommendations.html', context)

	return HttpResponse(form_response)