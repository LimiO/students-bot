import json

from playhouse.postgres_ext import PostgresqlExtDatabase
from aiogram import Bot, Dispatcher
import yaml

from config import TOKEN, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, PROXY_URL, PROXY_AUTH


bot: Bot = Bot(TOKEN, parse_mode='html')
dp: Dispatcher = Dispatcher(bot)

db: PostgresqlExtDatabase = PostgresqlExtDatabase(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                                  autocommit=True, autoconnect=True)


class JSONObject:
    def __init__(self, data):
        vars(self).update(data)


with open('locale/locale.yaml') as file:
    data = yaml.safe_load(file)
    main_locale = json.loads(json.dumps(data), object_hook=JSONObject)
    buttons = main_locale.buttons
    texts = main_locale.texts
    exceptions = main_locale.exceptions

with open('locale/langs.json') as file:
    all_langs = json.load(file)
    langs = all_langs['eng']
    own_langs = all_langs['own']
