from typing import Union

from misc import db, own_langs, langs
from models import models, User, Wolfram, Translator, Language
from peewee import Model


def connection(function):
    def wrapper(*args, **kwargs):
        with db.connection():
            return function(*args, **kwargs)
    return wrapper


@connection
def create_table(*args: Model):
    for model in args:
        if not model.table_exists():
            model.create_table()


@connection
def drop_table(*args: Model):
    for model in args:
        if model.table_exists():
            model.drop_table()


@connection
def get_user(user_id: int) -> Union[User, None]:
    if User.get_or_none(id=user_id) is None:
        lang = get_language(ui='en')
        User.create(id=user_id, lang_translate=lang, lang_wiki=lang)
    return User.get_or_none(id=user_id)


@connection
def get_language(ui: str) -> Union[Language, None]:
    return Language.get_or_none(ui=ui)


@connection
def get_wolfram() -> Union[Wolfram, None]:
    return Wolfram.get()


@connection
def get_translator() -> Union[Translator]:
    return Translator.get()


@connection
def set_wolfram(app_id: str):
    Wolfram.create(app_id=app_id)


@connection
def set_translator(token: str):
    Translator.create(token=token)


@connection
def set_language(**kwargs):
    Language.create(**kwargs)


if __name__ == '__main__':
    drop_table(*reversed(models))
    create_table(*models)
    set_wolfram('PEXXAK-3GLT4V5VK6')
    set_translator('trnsl.1.1.20200510T131914Z.5562cd2529b20983.3848a304971701d3ae8a465da1e58a2d639ca22b')
    for i, j in own_langs.items():
        set_language(ui=i, value=j, en_value=langs[i])