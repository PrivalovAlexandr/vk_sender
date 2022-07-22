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
    return res

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
    pass
