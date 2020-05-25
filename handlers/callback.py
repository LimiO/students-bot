from aiogram.types import CallbackQuery

from misc import dp, bot, texts
from utils.wikipedia import Wiki
from config import TRANSLATOR_LIM, WOLFRAM_LIM
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


@dp.callback_query_handler(lambda call: call.data.startswith('switch_'))
async def profile_3(call: CallbackQuery):
    ui = call.data[call.data.rfind('_') + 1:]
    user = db.get_user(call.from_user.id)
    lang = db.get_language(ui)
    await call.answer(texts.act)
    if lang != user.lang_translate:
        user.set_lang('translate', lang)
    await bot.edit_message_text(
        user.info, inline_message_id=call.inline_message_id,
        reply_markup=markups.settings_markup
    )


@dp.callback_query_handler(lambda call: call.data.startswith('wiki_'))
async def wiki_2(call: CallbackQuery):
    page_id = int(call.data[call.data.rfind('_') + 1:])
    info = await Wiki.get_page(page_id)
    await call.message.delete()
    text = ''
    for i in info:
        if len(text+i) > 4096:
            await call.message.answer(text)
            text = i
            continue
        text += i
    if text:
        await call.message.answer(text)


@dp.callback_query_handler(lambda call: call.data.startswith('full_'))
async def wiki_inline_1(call: CallbackQuery):
    await bot.edit_message_text(texts.wiki_2, inline_message_id=call.inline_message_id)
    page_id = int(call.data[call.data.rfind('_') + 1:])
    info = await Wiki.get_page(page_id=page_id)
    result = ''
    for i in info:
        if len(result + i) > 4096:
            break
        result += i + '\n'
    await bot.edit_message_text(result, inline_message_id=call.inline_message_id)