from aiogram.types import CallbackQuery

from misc import dp, bot, texts, exceptions
from config import CREATOR
from utils.wikipedia import Wiki
import db
import markups


@dp.callback_query_handler(lambda call: call.data in ['en', 'de', 'ru', 'fr', 'lang_wi'])
async def profile_1(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    await call.answer(texts.act)
    if call.data != 'lang_wi':
        lang = db.get_language(call.data)
        if lang == user.lang_wiki:
            return
        user.set_lang('wiki', lang)
    await call.message.edit_text(
        texts.profile_1.format(user.lang_wiki.value),
        reply_markup=user.lang_wiki_markup
    )


@dp.callback_query_handler(lambda call: call.data == 'profile')
async def profile_2(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    await call.answer(texts.act)
    await call.message.edit_text(
        user.info,
        reply_markup=markups.settings_markup
    )


@dp.callback_query_handler(lambda call: call.data == 'main_menu')
async def main_menu(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    user.reset_state()
    await call.message.edit_text(texts.main_menu)


@dp.callback_query_handler(lambda call: call.data == 'ISO')
async def faq_1(call: CallbackQuery):
    await call.answer(texts.act)
    await call.message.edit_text(db.Language.iso(),
                                 reply_markup=markups.back_markup('FAQ'))


@dp.callback_query_handler(lambda call: call.data == 'inline_help')
async def faq_2(call: CallbackQuery):
    await call.answer(texts.act)
    await call.message.edit_text(texts.help_1.format(bot_name=(await bot.get_me()).username),
                                 reply_markup=markups.back_markup('FAQ'))


@dp.callback_query_handler(lambda call: call.data == 'FAQ')
async def faq_3(call: CallbackQuery):
    await call.answer(texts.act)
    await call.message.edit_text(
        texts.faq_0.format(CREATOR),
        reply_markup=markups.faq_markup)


@dp.callback_query_handler(lambda call: call.data.startswith('switch_'))
async def profile_3(call: CallbackQuery):
    ui = call.data[call.data.rfind('_') + 1:]
    user = db.get_user(call.from_user.id)
    lang = db.get_language(ui)
    await call.answer(texts.act)
    if lang != user.lang_translate:
        user.set_lang('translate', lang)
    await bot.edit_message_reply_markup(
        reply_markup=None, inline_message_id=call.inline_message_id
    )


@dp.callback_query_handler(lambda call: call.data.startswith('wiki_'))
async def wiki_2(call: CallbackQuery):
    await call.answer(texts.act)
    user = db.get_user(call.from_user.id)
    page_id = int(call.data[call.data.rfind('_') + 1:])
    info = await Wiki.get_page(page_id, user.lang_wiki.ui, True)
    if info:
        await call.message.edit_text(info, reply_markup=markups.full_markup(page_id))
        return
    await call.message.edit_text(exceptions.wiki_1)


@dp.callback_query_handler(lambda call: call.data.startswith('full_'))
async def wiki_inline_1(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    page_id = int(call.data[call.data.rfind('_') + 1:])
    if call.inline_message_id:
        inline_message_id = call.inline_message_id
        message_id = None
        chat_id = None
    else:
        inline_message_id = None
        message_id = call.message.message_id
        chat_id = call.from_user.id
    await bot.edit_message_text(texts.wiki_2, message_id=message_id,
                                inline_message_id=inline_message_id,
                                chat_id=chat_id)
    info = await Wiki.get_page(page_id, user.lang_wiki.ui)
    result = ''
    for i in info:
        if len(result + i) > 4096:
            break
        result += i + '\n'
    await bot.edit_message_text(result, message_id=message_id,
                                inline_message_id=inline_message_id,
                                chat_id=chat_id)