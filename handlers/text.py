from aiogram.types import Message

from misc import dp, buttons, texts, exceptions, bot
from config import CREATOR
from utils.wikipedia import Wiki
import db
import markups


@dp.message_handler(commands=['start'])
async def start(message: Message):
    db.get_user(message.from_user.id)
    await message.answer(texts.start.format(message.from_user.first_name), reply_markup=markups.main_markup)


@dp.message_handler(commands=['help'])
async def help_(message: Message):
    await message.answer(texts.help_2, disable_web_page_preview=True)


@dp.message_handler(commands=['inline'])
async def inline_help(message: Message):
    await message.answer(texts.help_1.format((await bot.get_me()).username),
                         disable_web_page_preview=True)


@dp.message_handler(lambda msg: msg.text == buttons.wolfram)
async def wolfram_0(message: Message):
    user = db.get_user(message.from_user.id)
    user.set_state('wolfram')
    await message.answer(texts.wolfram_0, reply_markup=markups.back_markup('main_menu'))


@dp.message_handler(lambda msg: msg.text == buttons.wiki)
async def wiki_0(message: Message):
    user = db.get_user(message.from_user.id)
    user.set_state('wiki')
    await message.answer(texts.wiki_0, reply_markup=markups.back_markup('main_menu'))


@dp.message_handler(lambda msg: msg.text == buttons.profile)
async def profile_0(message: Message):
    user = db.get_user(message.from_user.id)
    await message.answer(
        user.info,
        reply_markup=markups.settings_markup
    )


@dp.message_handler(lambda msg: msg.text == buttons.FAQ)
async def faq_0(message: Message):
    await message.answer(texts.faq_0.format(CREATOR),
                         reply_markup=markups.faq_markup)


@dp.message_handler(lambda msg: db.get_user(msg.from_user.id).state == 'wolfram')
async def wolfram_1(message: Message):
    wolfram = db.get_wolfram()
    user = db.get_user(message.from_user.id)
    if not user.wolfram_free:
        await message.answer(exceptions.limit)
        user.reset_state()
        return
    await message.answer(texts.wolfram_1)
    user.wolfram_free -= 1
    user.state = ''
    user.save()
    wolfram.reduce(1)
    if await wolfram.check_request(message.text):
        with open(f'{wolfram.id}_{wolfram.limit}.png', 'rb') as file:
            await message.answer_photo(file)
        wolfram.delete_photos()
    else:
        await message.answer(exceptions.wolfram)


@dp.message_handler(lambda msg: db.get_user(msg.from_user.id).state == 'wiki')
async def wiki_1(message: Message):
    user = db.get_user(message.from_user.id)
    user.reset_state()
    result = await Wiki.search(message.text, user.lang_wiki.ui)
    if not result:
        await message.answer(exceptions.wiki_0)
        return
    result_info = '\n'.join(
        f"{number+1}) <a href='https://{user.lang_wiki.ui}.wikipedia.org/?curid={result[title]}'>{title}</a>\n"
        for number, title in enumerate(result))
    await message.answer(texts.wiki_1.format(message.text, result_info),
                         reply_markup=markups.wiki_markup(result.values()))