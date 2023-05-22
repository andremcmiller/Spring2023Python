import time
import random
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)

db = [
    {
        'time': time.time(),
        'name': 'Бот:',
        'text': 'Для активации бота напишите /game . После этого введите "Камень", "Ножницы" или "Бумага". Для окончания игры введите /break ',
    },
]


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/status")
def status():
    names =[]
    for k in db:
        if k['name'] not in names:
            names.append(k['name'])
    n_users = len(names)
    n_msg = len(db)
    return {'status': True,
            'name': "Server lesson #1",
            'time': datetime.now().strftime('%Y/%y/%m/%d time: %H:%M:%S'),
            'number of users': n_users,
            'name of users': names,
            'number of messages': n_msg
    }

    #return {
    #    'status': True,
    #    'name': 'Messenger',
    #    'time': time.asctime(),
    #    'time2': time.time(),
    #    'time3': datetime.now(),
    #    'time4': str(datetime.now()),
    #    'time5': datetime.now().strftime('%Y/%y/%m/%d time: %H:%M:%S'),
    #    'time6': datetime.now().isoformat(),
    #}

game = False

@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    if len(data) != 2:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str) \
            or name == '' or text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }

    global game
    game = False
    game_elements = ['Ножницы','Камень', 'Бумага']

    if message['text'] == '/help':
        message = {
            'time': time.time(),
            'name': 'Бот:',
            'text': 'Для активации бота напишите /game . После этого введите "Камень", "Ножницы" или "Бумага". Для окончания игры введите /break '
        }
        db.append(message)

    if message['text'] == "/game":
        message = {
            'time': time.time(),
            'name': 'Бот:',
            'text': 'Введите "Камень", "Ножницы" или "Бумага".'
        }
        db.append(message)
        game = True

    if game == True:
        if message['text'].lower() == "Ножницы" or message['text'].lower() == "Камень" or message['text'].lower() == "Бумага":
            bot_choice = random.randrange(0, 3)
            message = {
                'time': time.time(),
                'name': 'Бот:',
                'text': game_elements[bot_choice]
            }
        db.append(message)

    if message['text'] == "/break":
        message = {
            'time': time.time(),
            'name': 'Бот:',
            'text': 'Спасибо за игру!'
        }
        db.append(message)
        game = False

    db.append(message)
    return {"OK": True}
@app.route("/messages")
def get_messages():
    # print(request.args['after'])
    # print(type(request.args['after']))
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}


app.run()