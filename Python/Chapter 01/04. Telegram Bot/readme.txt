Возможности данного бота:
1)  При общении с ним он будет отвечать вам несколько специфично.
2)  Он сможет поиграть с вами в небольшую математическую игру. Бот будет предлагать
    вам математические выражения, а вы должны будете их решить. Если вам станет скучно,
    так и скажите боту - "I am bored". База данных с математическими выражениями находится
	в "math.db". На каждом шагу выбирается рандомное выражение. Пользователю предоставляется
	выбор правильного ответа с помощью custom keyboard.
3)  Этот бот не только развлечёт вас, но и сможет узнать за вас погоду в реальном времени.
    Для этого использовался список городов Яндекса. При запросе пользователя узнать погоду,
	он должен ввести страну и город. Затем в списке городов искался id данного города и 
	отправлялся запрос в Погода.Яндекс. После чего результат (ответ) парсился и выделялась
	часть, содержащая температуру и состояние погоды (пасмурно, небольшой дождь и т.д.)
