# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from lxml import etree
import urllib2
import config


class Weather:

    cities = {}

    def __init__(self):
        tree = ET.ElementTree(file=urllib2.urlopen(config.yandex_cities_url))
        root = tree.getroot()
        for country in root:
            country_name = country.attrib["name"].lower()
            Weather.cities[country_name] = {}
            for city in country: 
                Weather.cities[country_name][city.text.lower()] = city.attrib["id"]
        
    def getWeather(self, country, city):
        try:
            city_id = Weather.cities[country.lower()][city.lower()]
            ns = {'ya': 'http://weather.yandex.ru/forecast'}
            tree = etree.parse(r'http://export.yandex.ru/weather-ng/forecasts/{}.xml'.format(city_id))
            temperature = tree.xpath('ya:fact/ya:temperature', namespaces = ns)[0].text
            weather_type = tree.xpath('ya:fact/ya:weather_type', namespaces = ns)[0].text
            return (temperature, weather_type)
        except LookupError:
            raise
