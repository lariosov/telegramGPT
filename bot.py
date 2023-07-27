
import logging
import config
import openai


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


openai.api_key = config.OPENAI_API_KEY
token = config.TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token)
dp = Dispatcher(bot)


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def main():
    print('[+] ChatGPT startet like main program')
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
            {"role": "system", "content": "You are a helpful good girl sometimes with sarcasm response."},
            {"role": "user", "content": f"My name is {message.from_user.first_name}. Im backend developer"},
            {"role": "assistant", "content": f"Hello, {message.from_user.first_name}. My name is Sindy. How i can help you?"},
            {"role": "user", "content": message.text}
        ]
    )

    await message.answer(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()
