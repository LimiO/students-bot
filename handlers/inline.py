from hashlib import md5
from datetime import datetime

from aiogram.types import InlineQuery, InputTextMessageContent
from aiogram.types.inline_query_result import InlineQueryResultArticle, \
    InlineQueryResultCachedPhoto

from misc import dp, buttons, texts, exceptions, bot, langs, own_langs
from config import PICS
from utils import Wiki, Parser
import db
import markups


@dp.inline_handler(lambda query: query.query.strip() == 'lang translate')
async def inline_lang_0(query: InlineQuery):
    user = db.get_user(query.from_user.id)
    items = list()
    for number, lang in enumerate(langs):
        result_id: str = md5((str(query.id)+str(datetime.now())+str(number)).encode()).hexdigest()
        items.append(InlineQueryResultArticle(
            id=result_id, title=own_langs[lang], description=langs[lang],
            input_message_content=InputTextMessageContent(
                texts.profile_2.format(user.lang_translate.value, own_langs[lang])),
            reply_markup=markups.translate_profile_markup(lang)
        ))
    await query.answer(items)


@dp.inline_handler(lambda query: query.query.strip().lower()[-3:] == '-wi')  #
async def wiki_inline_0(query: InlineQuery):
    text = query.query[:-3].strip().lower()
    search: dict = await Wiki.search(text)
    items = list()
    if search:
        for title, page_id in search.items():
            info = await Wiki.get_page(page_id, is_one=True)
            result_id: str = md5((text + str(query.id)+str(datetime.now())).encode()).hexdigest()
            items.append(InlineQueryResultArticle(
                         id=result_id, title=title, reply_markup=markups.full_markup(page_id),
                         input_message_content=InputTextMessageContent(texts.wiki_1.format(text, info))))
    await query.answer(items)


@dp.inline_handler(lambda query: query.query.strip().lower()[-2:] == '-t')  #
async def translate_inline_0(query: InlineQuery):
    text = query.query[:-2].strip().lower()
    user = db.get_user(query.from_user.id)
    result_id: str = md5((text + str(query.id)).encode()).hexdigest()
    if user.translate_free < len(text) or len(text) > 1900:
        result = content = exceptions.limit
    else:
        args = Parser.get_translation_args(text)
        translator = db.get_translator()
        translator.reduce(len(text))
        user.reduce('translate', len(text))
        if len(args) == 1:
            result = await translator.translate(*args, lang_to=user.lang_translate.ui)
        else:
            result = await translator.translate(*args)
        if result:
            lang_from = db.get_language(result["lang_from"].lower())
            lang_to = db.get_language(result["lang_to"].lower())
            content = texts.translate_0.format(lang_from.value, lang_to.value,
                                               args[0], result["text"])
        else:
            content = exceptions.translator
        result = result["text"] if result else exceptions.translator
    item = InlineQueryResultArticle(
        id=result_id, title=result,
        input_message_content=InputTextMessageContent(content))
    await query.answer([item])


@dp.inline_handler(lambda query: query.query.strip().lower()[-3:] == '-wo')
async def main(query: InlineQuery):
    wolfram = db.get_wolfram()
    text = query.query[:-3].strip().lower()
    result_id: str = md5((str(query.id) + str(datetime.now())).encode()).hexdigest()
    user = db.get_user(query.from_user.id)
    if not user.wolfram_free:
        item = InlineQueryResultArticle(
            id=result_id, title=exceptions.limit,
            input_message_content=InputTextMessageContent(exceptions.limit))
    else:
        user.reduce('wolfram', 1)
        wolfram.reduce(1)
        if await wolfram.check_request(text):
            with open(f'{wolfram.id}_{wolfram.limit}.png', 'rb') as file:
                msg = await bot.send_photo(PICS, file)
            wolfram.delete_photos()
            item = InlineQueryResultCachedPhoto(
                id=result_id, photo_file_id=msg.photo[-1].file_id)
        else:
            item = InlineQueryResultArticle(
                id=result_id, title=exceptions.wolfram,
                input_message_content=InputTextMessageContent(exceptions.wolfram))
    await query.answer([item])


@dp.inline_handler(lambda query: query.query.lower().strip() == buttons.help)
async def help_0(query: InlineQuery):
    result_id: str = md5((str(query.id) + str(datetime.now())).encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id, title=texts.help_0,
        input_message_content=InputTextMessageContent(texts.help_1.format(
            bot_name=(await bot.get_me()).username), disable_web_page_preview=True))
    await query.answer([item])