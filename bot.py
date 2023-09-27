# TelegramGPT

import logging
import openai
import os


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
openai.api_key = os.getenv('OPENAI_API_KEY')
token = os.getenv('TOKEN')


logging.basicConfig(level=LOG_LEVEL)
bot = Bot(token)
dp = Dispatcher(bot)


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def main():
    print('[+] ChatGPT started like main program.')
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я бот Синди, в которого интегрировали ChatGPT. Какой у тебя вопрос?')

@dp.message_handler(commands=['developer'])
async def sm_link(message: types.Message):
    await message.answer('Вот ссылка на моего разработчика: t.me/lariosov')


@dp.message_handler()
async def howits(message : types.Message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "Ты услужливая, хорошая, девочка, которая иногда отвечает с сарказмом и помогает в разработке"},
            {"role": "user", "content": f"Меня зовут {message.from_user.first_name}. Я бекенд разработчик"},
            {"role": "assistant", "content": f"Привеи, {message.from_user.first_name}. Меня зовут Синди. Как я могу помочь?"},
            {"role": "user", "content": message.text}
        ]
    )

    await message.answer(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()
