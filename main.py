import os
import time
import logging
import shutil
import threading

import logging
from PIL import Image

from aiogram import Bot, Dispatcher, executor, types

from tools import box

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


for n in ['/tmp/input', '/tmp/sliced']:
    if not os.path.exists(n):
        os.makedirs(n)


def process(file_name, name=None, title=None, emojis='😀'):
    img = Image.open('/tmp/input/' + file_name + '.jpg').resize((2560,2560), Image.ANTIALIAS).convert('RGB')
    p = '/tmp/sliced/' + file_name
    os.makedirs(p)
    for k, v in box.items():
        img.crop(v).save(p + '/' + str(k) + '.png')

    if name == None:
        name = 's' + file_name + '_by_' + bot_username
    if title == None:
        title = 'Tg Cancer Pack Creator'

    with open('/tmp/sliced/{}/1.png'.format(file_name), 'rb') as f:
        print(bot.create_new_sticker_set(user_id=owner, name=name, title=title, png_sticker=f, emojis=emojis, contains_masks=False))
    for x in range(2, 26):
        with open('/tmp/sliced/{}/{}.png'.format(file_name, str(x)), 'rb') as f:
            redi.set(file_name, str(x).encode('utf-8'))
            print(x, bot.add_sticker_to_set(user_id=owner, name=name, png_sticker=f, emojis=emojis, mask_position=None))
        time.sleep(2)
    print('Done')
    redi.set(file_name, str('s' + file_name + '_by_' + bot_username).encode('utf-8'))
    os.remove('/tmp/input/' + file_name + '.jpg')
    shutil.rmtree('/tmp/sliced/' + file_name)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
