from typing import Union, Optional

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
def set_wolfram(app_id: str, limit: Optional[int] = 2000):
    Wolfram.create(app_id=app_id, limit=limit)


@connection
def set_translator(token: str, limit: Optional[int] = 1000000):
    Translator.create(token=token, limit=limit)


@connection
def set_language(**kwargs):
    Language.create(**kwargs)


if __name__ == '__main__':
    drop_table(*reversed(models))
    create_table(*models)