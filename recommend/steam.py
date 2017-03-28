import requests, json

class SteamAPI:
    def __init__(self, key):
        self.key = key
        self.decoder = json.JSONDecoder()

    def _query(self, uri):
        response = requests.get(uri)
        if response.ok:
            return self.decoder.decode(response.text)
        else:
            raise RuntimeError('Unable to get response')

    def GetOwnedGames(self, steam_id):
        query = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={id}&include_appinfo=1&format=json'.format(key=self.key, id=steam_id)
        return self._query(query)

    def GetSchemaForGame(self, app_id):
        query = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={key}&appid={id}'.format(key=self.key, id=app_id)
        return self._query(query)

    def GetAppList(self):
        query = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
        return self._query(query)

    def AppDetails(self, app_id):
        query = 'http://store.steampowered.com/api/appdetails?appids={id}'.format(id=app_id)
        return self._query(query)

    def GetFriendList(self, steam_id):
        query = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={id}&relationship=all'.format(key=self.key, id=steam_id)
        return self._query(query)

    def ResolveVanityURL(self, vanityURL):
        query = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}}&vanityurl={vanity}'.format(key=self.key, vanity=vanityURL)
        return self._query(query)

