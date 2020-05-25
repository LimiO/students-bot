from typing import Iterable, Optional

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from misc import buttons


main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(buttons.wolfram, buttons.wiki)
main_markup.row(buttons.profile)

settings_markup = InlineKeyboardMarkup()
settings_markup.row(InlineKeyboardButton(buttons.langs_0, callback_data='lang_wi'),
                    InlineKeyboardButton(buttons.langs_1,
                                         switch_inline_query_current_chat='lang translate'))


def wiki_markup(page_ids: Iterable[int], lang: Optional[str] = 'ru') -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    url = f'https://{lang}.wikipedia.org/?curid='
    row_1, row_2 = [], []
    for num, page_id in enumerate(page_ids):
        row_1.append(InlineKeyboardButton(text='№'+str(num+1), callback_data=f'wiki_{page_id}'))
        row_2.append(InlineKeyboardButton(text='№'+str(num+1), url=url+str(page_id)))
    markup.row(*row_1)
    markup.row(*row_2)
    return markup


def translate_profile_markup(ui: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=buttons.switch, callback_data=f'switch_{ui}'))
    return markup


def full_markup(page_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=buttons.full, callback_data=f'full_{page_id}'))
    return markup
