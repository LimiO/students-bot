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


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    t = Translator(token='trnsl.1.1.20200510T131914Z.5562cd2529b20983.3848a304971701d3ae8a465da1e58a2d639ca22b')
    async def main():
        a = {"az": "Azerbaijani", "ceb": "Cebuano", "cs": "Czech", "cy": "Welsh", "da": "Danish", "de": "German", "en": "English", "es": "Spanish", "fr": "French", "ga": "Irish", "hr": "Croatian", "ht": "Haitian", "hu": "Hungarian", "id": "Indonesian", "is": "Icelandic", "it": "Italian", "ja": "Japanese", "kn": "Kannada", "ko": "Korean", "ky": "Kyrgyz", "la": "Latin", "lb": "Luxembourgish", "lt": "Lithuanian", "lv": "Latvian", "mg": "Malagasy", "mhr": "Mari", "mn": "Mongolian", "ms": "Malay", "mt": "Maltese", "nl": "Dutch", "pap": "Papiamento", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", "tl": "Tagalog", "tr": "Turkish", "uk": "Ukrainian", "uz": "Uzbek", "xh": "Xhosa", "yi": "Yiddish"}
        need = {}
        for key, value in a.items():
            need[key] = (await t.translate(value, key, 'en'))['text']
        pprint(need)

    loop.run_until_complete(main())
