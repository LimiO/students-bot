from peewee import Model, CharField, PrimaryKeyField, ForeignKeyField, IntegerField

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from misc import db, own_langs, buttons, texts
from config import WOLFRAM_LIM, TRANSLATOR_LIM
from .translator import Language


class User(Model):
    id: int = PrimaryKeyField()
    state: str = CharField(max_length=25, default='')
    lang_translate: Language = ForeignKeyField(Language)
    lang_wiki: Language = ForeignKeyField(Language)
    wolfram_free: int = IntegerField(default=WOLFRAM_LIM)
    translate_free: int = IntegerField(default=TRANSLATOR_LIM)

    def reduce(self, attr: str, quantity: int):
        setattr(self, attr, getattr(self, attr+'_free') - quantity)
        self.save()

    def reset_state(self):
        self.state = ''
        self.save()

    def set_state(self, state):
        self.state = state
        self.save()

    def set_lang(self, item: str, lang: Language):
        setattr(self, f'lang_{item}', lang)
        self.save()

    def reduce_wolfram(self):
        self.wolfram_free -= 1
        self.save()

    def reduce_translate(self, count: int):
        self.translate_free -= count
        self.save()

    @property
    def lang_wiki_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text=self.get_lang_text('ru'),
                                        callback_data='ru'),
                   InlineKeyboardButton(text=self.get_lang_text('en'),
                                        callback_data='en'))
        markup.row(InlineKeyboardButton(text=self.get_lang_text('de'),
                                        callback_data='de'),
                   InlineKeyboardButton(text=self.get_lang_text('fr'),
                                        callback_data='fr'))
        markup.row(InlineKeyboardButton(text=buttons.back,
                                        callback_data='profile'))
        return markup

    def get_lang_text(self, ui):
        return f'{own_langs[ui]} ✅' if self.lang_wiki.ui == ui else own_langs[ui]

    @property
    def info(self):
        return texts.profile_0.format(
            user=self, wolfram_lim=WOLFRAM_LIM, tranlator_lim=TRANSLATOR_LIM)

    class Meta:
        database = db
        db_table = 'users'


