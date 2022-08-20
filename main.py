import requests
import vk_api

from random import randint as random

from key import key



vk = vk_api.VkApi(token=key)
vk._auth_token()


def send_voice(id, file_path):
    file = file_path
    res = vk.method('docs.getMessagesUploadServer', {
        "type": 'audio_message',
    })
    url = res['upload_url']
    res = requests.post(url, files={'file': open(file, 'rb')}).json()
    file = res['file']
    res = vk.method('docs.save', {
        'file': file,
        'type': 'audio_message'
    })
    att = f"doc{res['audio_message']['owner_id']}_{res['audio_message']['id']}"
    res = vk.method('messages.send', {
        "peer_id": id,
        "attachment": att,
        "random_id": random(-100,100)
    })

def spam(id, text):
    while True:
        try:
            vk.method("messages.send", {
                "peer_id": id, 
                "message": text, 
                "random_id": random(-100,100)
                })
        except:
            print('У вашего сына обнаружили капчу, он не выживет...')
            choice = input('Вы можете подождать или остановить спам, введя exit: ')
            if choice.lower() == 'exit':
                return 0

def dialogs():
    res = vk.method('messages.getConversations', {'count': 30})
    last_dialogs = {}
    ids= ''
    msg = '\nСписок последних диалогов:\n\n'
    for i in range(29):
        id = res['items'][i]['conversation']['peer']['id']
        ids += f'{id}, '
    ids = ids[:-2]
    info = vk.method('users.get', {'user_ids': ids, 'lang': 'ru'})
    print('Получаем список последних диалогов...')
    for j in range(len(info)):
        user = info[j]
        last_dialogs[j+1] = user['id']
        if user['first_name'] != 'DELETED':
            name = f"{user['first_name']} {user['last_name']}"
            msg += f'{j+1}. {name}\n'
        else:
            title = vk.method('messages.getChatPreview', {'peer_id': user['id']})['preview']['title']
            msg += f'{j+1}. [беседа] {title}\n'
    print(msg)
    return last_dialogs

def select():
    choice = input('''Получатель:
    1 - Ввести id получателя
    2 - Выбрать получателя
    ''')
    if choice == '1':
        id = input('Введите id получателя: ')
    elif choice == '2':
        dict_ = dialogs()
        num = input('Выберите получателя: ')
        trig = True
        while trig:
            try:
                id = dict_ [int(num)]
                trig = False
            except KeyError:
                print('Некорректный номер получателя, попробуйте ещё раз.')
                num = input('Выберите получателя: ')
            except ValueError:
                print('ID должен состоять из цифр')
                num = input('Выберите получателя: ')
    return id



if __name__ == '__main__':
    choice = input('''Тип отправки:
    1 - голосовое сообщение
    2 - спам обычными сообщениями
    ''')
    match choice:
        case '1':
            id = select()
            file_path = input('Введите абсолютный путь до файла:\n')
            if file_path[0] == '"':
                file_path = file_path[1:-1]
            if file_path.split('.')[-1] in ['mp3', 'ogg']:
                file_path = fr'{file_path}'
                try:
                    send_voice(int(id), file_path)
                except ValueError:
                    print('ID должен состоять из цифр')
                except vk_api.exceptions.ApiError:
                    print('Вы не можете отправлять сообщения этому пользователю')
            else:
                print('Ваш аудиофайл должен иметь разрешение mp3 или ogg')
        case '2':
            id = select()
            text = input('Введите сообщение:\n')
            try:
                spam(int(id), text)
            except ValueError:
                    print('ID должен состоять из цифр')
            except vk_api.exceptions.ApiError:
                    print('Вы не можете отправлять сообщения этому пользователю')