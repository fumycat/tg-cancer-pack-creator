import os
import time
import logging
import shutil
import threading
from urllib.parse import urlparse
import redis
import uuid
import telebot
from PIL import Image
from bottle import route, run, template, static_file, request

from tools import box


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(os.environ.get("TG"))
owner = os.environ.get("OWNER")
bot_username = 'lolicoinbot'
url = urlparse(os.environ.get('REDISCLOUD_URL'))
redi = redis.Redis(host=url.hostname, port=url.port, password=url.password)


for n in ['/tmp/input', '/tmp/sliced']:
    if not os.path.exists(n):
        os.makedirs(n)


def process(file_name, name=None, title=None, emojis='😀'):
    img = Image.open('/tmp/input/' + file_name + '.jpg').resize((2560,2560), Image.ANTIALIAS).convert('RGB')
    p = '/tmp/sliced/' + file_name
    os.makedirs(p)
    for k, v in box.items():
        img.crop(v).save(p + '/' + str(k) + '.png')
    #
    if name == None:
        name = 's' + file_name + '_by_' + bot_username
    if title == None:
        title = 'Tg Cancer Pack Creator'
    ##
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


@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


@route("/j/<i>/<x>")
def req(i, x):
    if str(x) == '0':
        return template('templates/req.html')
    else:
        state = redi.get(i).decode('utf-8')
        print(state)
        if state.isdigit():
            response = state
        else:
            response = 'Ваш пак готов: https://t.me/addstickers/' + state
        return response
    


@route("/")
def main():
    return template('templates/index.html')


@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('picture')
    r = uuid.uuid4().hex
    upload.save('/tmp/input/' + r + '.jpg')


    print(dict(name=r, ip=request.environ.get('REMOTE_ADDR'), md5='TODO'))

    threading.Thread(target=process, args=[r]).start()
    redi.set(r, '0'.encode('utf-8'))
    print(os.listdir())
    return r


if __name__ == '__main__':
    # run(host='localhost', port=8080, reloader=True)
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
