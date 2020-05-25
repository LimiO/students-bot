from typing import Optional, Union, Dict
from pprint import pprint

from peewee import Model, PrimaryKeyField, CharField, BigIntegerField
import aiohttp

from utils import Limiter
from misc import db


class Translator(Model, Limiter):
    id = PrimaryKeyField()
    token = CharField()
    limit = BigIntegerField(default=10000000)

    def reduce(self, quantity: int):
        Limiter.reduce(self, quantity)
        if self.limit < 100:
            self.delete_instance()

    async def translate(self, text, lang_to: Optional[str] = 'en',
                        lang_from: Optional[str] = None) -> Union[Dict[str, str], None]:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        lang = f'{lang_from}-{lang_to}' if lang_from else lang_to
        data = {
            "key": self.token,
            "text": text,
            "lang": lang
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=data) as request:
                json = await request.json()
                if json["code"] == 200:
                    lang_from, lang_to = json["lang"].split('-')
                    return {"text": json["text"][0], "lang_from": lang_from, "lang_to": lang_to}
                return None

    class Meta:
        database = db
        db_table = 'translators'


class Language(Model):
    id = PrimaryKeyField()
    ui = CharField(max_length=5)
    value = CharField()
    en_value = CharField()

    class Meta:
        database = db
        db_table = 'languages'
