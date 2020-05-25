from aiogram.types import Message

from misc import dp, buttons, texts, exceptions
from config import TRANSLATOR_LIM, WOLFRAM_LIM
from utils.wikipedia import Wiki
import db
import markups


@dp.message_handler(commands=['start'])
async def start(message: Message):
    db.get_user(message.from_user.id)
    await message.answer(texts.start.format(message.from_user.first_name), reply_markup=markups.main_markup)


@dp.message_handler(lambda msg: msg.text == buttons.wolfram)
async def wolfram_0(message: Message):
    user = db.get_user(message.from_user.id)
    user.set_state('wolfram')
    await message.answer(texts.wolfram_0)


@dp.message_handler(lambda msg: msg.text == buttons.wiki)
async def wiki_0(message: Message):
    user = db.get_user(message.from_user.id)
    user.set_state('wiki')
    await message.answer(texts.wiki_0)


@dp.message_handler(lambda msg: msg.text == buttons.profile)
async def profile_0(message: Message):
    user = db.get_user(message.from_user.id)
    await message.answer(
        user.info,
        reply_markup=markups.settings_markup
    )


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
    result = await Wiki.search(message.text)
    if not result:
        await message.answer(exceptions.wiki)
        return
    result_info = '\n'.join(f"{number+1}) <b>{title}</b>" for number, title in enumerate(result))
    await message.answer(texts.wiki_1.format(message.text, result_info),
                         reply_markup=markups.wiki_markup(result.values()))