import requests
import vk_api

from key import key
from random import randint as random



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
            return None



if __name__ == '__main__':
    choice = input('''Выберите тип отправки:
        1 - голосовое сообщение
        2 - спам обычными сообщениями
        ''')
    match choice:
        case '1':
            id = input('Введите id получателя: ')
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
            id = input('Введите id получателя: ')
            text = input('Введите сообщение:\n')
            try:
                spam(int(id), text)
            except ValueError:
                    print('ID должен состоять из цифр')