# Бот отвечающий с помощью Google DialogFlow
## Пример работы
![](docs/media/demo_tg_bot.gif)
![](docs/media/demo_vk_bot.gif)
## Установка
Для запуска достаточно создать файл .env, в котором описаны переменные окружения.

Файл .env:
```
TELEGRAM_TOKEN=<токен телеграм бота>
GOOGLE_APPLICATION_CREDENTIALS=<путь до файла application_default_credentials>
GOOGLE_CLOUD_PROJECT=<id проекта google cloud>
VK_APIKEY=<токен сообщества vk>
TG_CHAT_ID_LOG=<идентификатор пользователя телеграма для получения логов>
TELEGRAM_TOKEN_LOG=<бот для отправки логов>
```

### Токен telegram-бота
Для создания телеграм бота напишите боту [BotFather](https://t.me/BotFather), там вы создадите бота, и вам будет выдан токен бота.

### Токен бота сообщества вконтакте
Токен можно сгенерировать в меню управления сообщества на вкладке API


### Установка библиотек и зависимостей

Развернуть виртуальное окружение интерпретатора
```sh
python -m venv ./venv 
```

Активируйте виртуальное окружение

```sh
source venv/bin/activate 
```

Безопасно обновите pip

```sh
pip install --upgrade pip      
```

Установить требуемые библиотеки для скрипта командой
```sh
pip install -r requirements.txt
```

После заполнения файла с переменными можно запускать ботов с помощью команд
```sh
python tg_bot.py
python vk_bot.py
```

## Тренировка бота
Натренировать бота можно с помощью скрипта load_intent.py, который запускается следующей командой
```sh
python load_intent.py --p [путь до файла json]
```
Пример файла для обучения бота по [ссылке](https://dvmn.org/filer/canonical/1556745451/104/)