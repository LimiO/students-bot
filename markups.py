from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from misc import buttons


main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(buttons.wolfram, buttons.wiki)
main_markup.row(buttons.profile, buttons.FAQ)

settings_markup = InlineKeyboardMarkup()
settings_markup.row(InlineKeyboardButton(buttons.langs_0, callback_data='lang_wi'),
                    InlineKeyboardButton(buttons.langs_1,
                                         switch_inline_query_current_chat='lang translate'))

faq_markup = InlineKeyboardMarkup()
faq_markup.row(InlineKeyboardButton(text=buttons.ISO, callback_data='ISO'),
               InlineKeyboardButton(text=buttons.help, callback_data='inline_help'))


def wiki_markup(page_ids: Iterable[int]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    row = [InlineKeyboardButton(text='№'+str(num+1), callback_data=f'wiki_{page_id}')
           for num, page_id in enumerate(page_ids)]
    markup.row(*row)
    return markup


def translate_profile_markup(ui: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=buttons.switch, callback_data=f'switch_{ui}'))
    return markup


def full_markup(page_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=buttons.full, callback_data=f'full_{page_id}'))
    return markup


def back_markup(callback: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=buttons.back, callback_data=callback))
    return markup
