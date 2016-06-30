# -*- coding: utf-8 -*-

# Connecting
token = '172722170:AAEJfjlm1MV4iNk1hdz12ZO6u8KizuxX3B8'
yandex_cities_url = 'http://weather.yandex.ru/static/cities.xml'

# For work and communication
math_db = 'math.db'
stop_playing_request = 'I am bored'
stop_playing_answer = 'All right, all right.. :('
stop_weather_request = 'Never mind'
stop_weather_answer = 'Your choise'
game_answer = {True : 'Good!', False : 'Incorrect.'}
weather_intro = u'Введите вашу страну и город (через пробел):'
game_intro = "Ok. Let's play. I will give you little math questions and "\
             "you give me an answer. If you are bored, then just tell me: "\
             "'I am bored'. And now.. GO!"
help_info = "You can control me by sending these commands:\n\n"\
            "/math - I will play with you a little math game.\n"\
            "/weather - I will checkout the weather for you.\n\n"\
            "note: Input data in /weather is only cyrilic. It's not a bug"\
            ", it's a feature. You will be able to learn russian language a "\
            "little bit faster :)"


# Errors
ERROR_invalid_parameter = "Your data is incorrect. Try one more time."
ERROR_invalid_city_country = "Can't find your country (or city). Try one more time"
ERROR_connection_failed = "Connection failed."
ERROR_unknown = "Unknown error."
