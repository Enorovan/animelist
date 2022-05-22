import time
import sys
import requests
import re
from deep_translator import (GoogleTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeepL,
                             QCRI,
                             single_detection,
                             batch_detection)
import unidecode

sys.path.append('../../')
from pluginDefault import PluginDefault

class PluginAnime(PluginDefault):
    url = 'https://kitsu.io/api/edge/'

    def getUrlResponse(self, url):
        result = requests.get(url)
        result.raise_for_status()
        data = result.json()
        return data

    def traduction(self, data):
        for i in range(len(data["data"])):
            if data["data"][i]["attributes"]["synopsis"] != "" and data["data"][i]["attributes"]["synopsis"] != None:
                urlTranslation = data["data"][i]["attributes"]["synopsis"]
                translationFinal = GoogleTranslator(
                    source='en', target='fr').translate(text=urlTranslation)
                data["data"][i]["attributes"]["synopsis"] = unidecode.unidecode(
                    translationFinal)
        return data

    def getRecent(self, type="anime"):
        if type != "anime" and type != "manga":
            error = "Le type doit etre manga ou anime"
            return {'error': error}
        urlRecent = self.url + type + "?sort=-createdAt&page[limit]=5"
        data = self.getUrlResponse(urlRecent)
        return self.traduction(data)


    def getGenre(self, type="anime", genre = ""):
        if type != "anime" and type != "manga":
            error = "Le type doit etre manga ou anime"
            return {'error': error}, 404
        urlGenre = self.url + type + "?sort=-createdAt&filter[categories] = " + genre + " & page[limit] = 5"
        data = self.getUrlResponse(urlGenre)
        return self.traduction(data)

    def getTitle(self, type="anime", title=""):
        if type != "anime" and type != "manga":
            error = "Le type doit etre manga ou anime"
            return {'error': error}, 404
        urlTitle = self.url + type + "?sort=-createdAt&canonicalTitle=" + title + "&page[limit]=5"
        data = self.getUrlResponse(urlTitle)
        return self.traduction(data)


    def getId(self, type="anime", id=""):
        if type != "anime" and type != "manga":
            error = "Le type doit etre manga ou anime"
            return {'error': error}
        urlId = self.url + type + "/" + id
        data = self.getUrlResponse(urlId)
        return data

    def getRecentEpisode(self):
        urlRecent = self.url + "episodes?sort=-updatedAt&page[limit]=5"
        data = self.getUrlResponse(urlRecent)
        return self.traduction(data)


    def response(self, sentence=""):
        themeName= self.subject.split(".")[1]
        if themeName == "animeGenre":
            genreRe = re.search("genre (\w+)", sentence)
            genre = genreRe.groups()[0]
            print(genre)
            return self.getGenre("anime", genre)
        elif themeName == "animeRecent":
            return self.getRecent("anime")
        elif themeName == "animeTitle":
            titleRe = re.search("titre (.*)", sentence)
            title = titleRe.groups()[0]
            print(title)
            return self.getTitle("anime", title)
        elif themeName == "mangaGenre":
            genreRe = re.search("genre (\w+)", sentence)
            genre = genreRe.groups()[0]
            print(genre)
            return self.getGenre("manga", genre)
        elif themeName == "mangaRecent":
            return self.getRecent("manga")
        elif themeName == "mangaTitle":
            titleRe = re.search("titre (.*)", sentence)
            print(titleRe.groups())
            title = titleRe.groups()[0]
            print(title)
            return self.getTitle("manga", title)
        elif themeName == "recentEpisode":
            return self.getRecentEpisode()

