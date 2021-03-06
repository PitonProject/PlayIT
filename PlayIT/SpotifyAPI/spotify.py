#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import json

class PlaylistManager:

    def __init__(self, user_id, api_key, playlist_id=None):
        self.user_id = user_id
        self.api_key = api_key
        self.playlist_id = playlist_id
        self.url_base = "https://api.spotify.com/v1/users/" + self.user_id + "/playlists/"
        self.headers = {"Accept":"application/json",
                        "Authorization":"Bearer " + self.api_key,
                        "Content-Type":"application/json"}

    def add_track_to_playlist(self, track_id):
        url = self.url_base + self.playlist_id + "/tracks?uris=spotify%3Atrack%3A" + track_id
        response = self.post_request(url, None)
        print json.dumps(response, indent=4)

    def remove_track_from_playlist(self, track_id):
        url = self.url_base + self.playlist_id + "/tracks"
        data = {"tracks": [{"uri": "spotify:track:" + track_id}]}
        response = self.delete_request(url, data)
        print json.dumps(response, indent=4)

    def set_playlist(self, playlist_id):
        self.playlist_id = playlist_id

    def create_playlist(self, playlist_name):
        url = self.url_base
        data = {"name":playlist_name,
                "public":"true"}
        response = self.post_request(url, data)
        if not self.playlist_id:
            self.playlist_id = response["id"]
        print json.dumps(response, indent=4)

    def get_playlist_tracks(self, offset=0, limit=100):
        url = self.url_base + self.playlist_id + "/tracks?offset=" + str(offset) + "&limit=" + str(limit)
        response = self.get_request(url)
        #print response["next"]
        for i, item in enumerate(response["items"]):
            track = item["track"]
            print i+offset, track["name"], "-", track["artists"][0]["name"], \
                    "-", track["album"]["name"], "--> id:", track["id"]

    def post_request(self, url, data):
        response = requests.post(url, json=data, headers=self.headers)
        return json.loads(response.text)

    def delete_request(self, url, data):
        response = requests.delete(url, json=data, headers=self.headers)
        return json.loads(response.text)

    def get_request(self, url):
        response = requests.get(url, headers=self.headers)
        return json.loads(response.text)

class SpotifyBrowser:

    url_base = "https://api.spotify.com/v1/search?"
    url_services = {
        "track" : "type=track&q=",
        "album" : "type=album&q=",
        "playlist" : "type=playlist&q=",
        "artist" : "type=artist&q="
    }

    @staticmethod
    def search_track(track, offset=0, limit=50):
        response = SpotifyBrowser.get_json_response("track", track, offset, limit)
        return response
        tracks = response["tracks"]["items"]
        for track in tracks:
            print track["name"], "-", track["artists"][0]["name"], \
                    "-", track["album"]["name"], "--> id:", track["id"]

    @staticmethod
    def search_album(album, offset=0, limit=50):
        response = SpotifyBrowser.get_json_response("album", album, offset, limit)
        return response
        albums = response["albums"]["items"]
        for album in albums:
            print album["name"], "--> id:", album["id"]

    @staticmethod
    def search_artist(artist, offset=0, limit=50):
        response = SpotifyBrowser.get_json_response("artist", artist, offset, limit)
        return response
        artists = response["artists"]["items"]
        for artist in artists:
            print artist["name"], "--> id:", artist["id"]

    @staticmethod
    def search_playlist(playlist, offset=0, limit=50):
        response = SpotifyBrowser.get_json_response("playlist", playlist, offset, limit)
        return response
        playlists = response["playlists"]["items"]
        for playlist in playlists:
            print playlist["name"], "-", playlist["owner"]["id"], \
                    "--> id:", playlist["id"]

    @staticmethod
    def get_json_response(service, keywords, offset=0, limit=50):
        url = SpotifyBrowser.url_base \
                + SpotifyBrowser.url_services[service] \
                + keywords.replace(" ", "%20") \
                + "&offset=" + str(offset) \
                + "&limit=" + str(limit)
        response = requests.get(url)
        return json.loads(response.text)

    @staticmethod
    def get_track_by_id(track_id):
        url = 'https://api.spotify.com/v1/tracks/' + track_id
        return json.loads(requests.get(url).text)

if __name__ == '__main__':
    #sb = SpotifyBrowser()
    #print json.dumps(sb.get_json_response("track", "Som persones"), indent=4)
    #sb.search_track("Més que la meva sang", limit=2, offset=1)
    #SpotifyBrowser.search_track("Més que la meva sang", limit=2, offset=1)
    #sb.search_artist("Txarango")
    #sb.search_album("Som riu")
    #sb.search_playlist("Catala")
    #p = PlaylistManager("pitonproject", "BQDAr-A_N4F5StlL9wkBRm5X8KQ_Ut6JkHZpjzQ5MOEiob4WYXqQe2yTDxdhLAiOgCZrFI6JtQ4j3gXf-AmhsWZMHsGBruwOjMx7mTfROpU7jUvYgZdKWqBaZx_vEuJOTvWqxwgG6gD5Ex9CfA5dX2wAJJbZoGYFm0QoUW4g8niRmy30bf3yd-vMA6AfEpkG4NmQo4RygEGHz1nWcQUPLg3kHTGdh3bJrzUzJA")
    #p.create_playlist("Prova 1")
    #p = PlaylistManager("pitonproject", "BQAClYlMFsDdsyKHtcl7epM2-7V00g9JU9ZvBOXaP3V8LSpMq5vWuHji-vHOMtWq2G8u1ECHEmLAOBBPeNKhWuKo5sQlWh_z_8xu3EWosV5FhWK038PFLzUZXNigPZquMcv2zijYoiXTEGAhhJsIRF-5Z3Qt6cR99KqnO3MXpMXNLpgGgsmMXspyAIUnAk53PgbBT0VQ2BftzcyGyei_6_KDTzXUKxwnpUOA0g", "0AWZxqSMorhy3dlQ43Bgof")
    #p.add_track_to_playlist("1rf3C6fWUJU2puq8Smqph9")
    #p.get_playlist_tracks()
    #p.remove_track_from_playlist("1rf3C6fWUJU2puq8Smqph9")
    #p.get_playlist_tracks()
    print SpotifyBrowser.get_track_by_id('6FXmJdGS5uNEmU3eS6ge5o')