import requests
import vk_api
import os 

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
        vk.method("messages.send", {
            "peer_id": id, 
            "message": text, 
            "random_id": random(-100,100)
            })

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

def select(type='voice'):
    choice = input('''Получатель:
    1 - Ввести id получателя
    2 - Выбрать получателя
    ''')
    if choice == '1':
        if type != 'spam':
            id = input('Введите id получателей через запятую: ')
            id = id.split(',')
            return id
        else:
            while True:
                id = input('Введите id получателя: ')
                if ',' not in id:
                    try:
                        id = int(id)
                        return id
                    except ValueError:
                        print('\nID должен состоять только из цифр\n')
                else:
                    print('\nВы можете указать только один id для спама\n')
    elif choice == '2':
        dict_ = dialogs()
        while True:
            if type == 'spam':
                id = input('Введите номер получателя: ')
                if ',' not in id:
                    try:
                        id = dict_[int(id)]
                        return id
                    except ValueError:
                        print('\nНомер должен состоять из цифр\n')
                    except KeyError:
                        print('\nУказан неверный номер\n')
                else:
                    print('\nВы можете указать только один номер для спама\n')
            else:
                num = input('Введите номера получателей через запятую: ')
                num = num.split(',')
                code = 1
                fail = ''
                id = []
                for i in num:
                    i.strip()
                    try:
                        if int(i) not in dict_.keys():
                            code = 0
                            fail += f'{i}, '
                        else:
                            id.append(dict_[int(i)])
                    except ValueError:
                        code = 0
                        fail += f'{i}, '
                        print('\nНомер должен состоять из цифр\n')
                if code == 1:
                    return id
                else:
                    print(f'\nНайдены некорректные номера получателей - {fail[:-2]}\n')

def print_dirs(dirs, buttons = 'all'):
    if dirs:
        msg = ''
        for i in dirs:
            dir_name = dirs[i].split('\\')
            if dir_name[-1].strip() != '':
                dir_name = dir_name[-1]
            else:
                dir_name = dir_name[-2]
            msg += f'{i} - {dir_name}\n'
    else:
        msg = 'Не удалось найти существующие директории\n'
    if buttons == 'all':
        msg += f'{len(dirs)+1} - Добавить директорию\n'
        msg += f'{len(dirs)+2} - Удалить директорию\n'
        msg += f'{len(dirs)+3} - Назад\n'
    print(msg)

def dir_menu():
    if os.path.exists('dirs.txt'):
        file = open('dirs.txt', encoding='utf-8')
    else:
        file = open('dirs.txt', 'w+', encoding='utf-8')
    dirs = {}
    i = 0
    for line in file:
        if line != '\n':
            if '\n' in line:
                line = line[:-1].strip()
            if line[0] == '"':
                line = line[1:-1]
            if os.path.exists(line):
                i += 1
                dirs[i] = line
    file.close()
    opt = True
    while True:
        if opt:
            opt = False
            print_dirs(dirs)
        ch = input('Выберите: ')
        if ch.isdigit():
            ch = int(ch)
            if ch == len(dirs)+1:
                #add
                opt = True
                path = input('Введите абсолютный путь до директории:\n').strip()
                if os.path.exists(path):
                    if path[0] == '"':
                        path = path[1:-1]
                    if path[-1] == '\\':
                        path = path[:-1]
                    code = 0
                    for i in dirs.items():
                        if path == i[1]:
                            code = 1
                    if code == 0:
                        file = open('dirs.txt', 'a', encoding='utf-8')
                        file.write(f'{path}\n')
                        file.close()
                        dirs[len(dirs)+1] = path
                    else:
                        print('\nДиректория уже существует\n')
                else:
                    print('\nДиректория не найдена\n')
            elif ch == len(dirs)+2:
                #delete
                if dirs:
                    print_dirs(dirs, 'delete')
                    dir_num = input('Введите номер директории: ')
                    if dir_num.isdigit():
                        dir_num = int(dir_num)
                        if dir_num in dirs.keys():
                            del dirs[dir_num]
                            file = open('dirs.txt', 'w', encoding='utf-8')
                            for i in dirs:
                                file.write(f'{dirs[i]}\n')
                            file.close()
                        else:
                            print('\nНекорректный номер директории\n')
                else:
                    print('\nУ вас нет директорий\n')
                opt = True
            elif ch == len(dirs)+3:
                #back
                select_menu()
            elif ch in dirs.keys():
                text = ''
                files = {}
                j = 0
                dir_path = dirs[ch]
                for i in os.listdir(dirs[ch]):
                    if ('.mp3' in i) or ('.ogg' in i):
                        j += 1
                        text += f'{j} - {i}\n'
                        files[j] = i
                if files:
                    print(text)
                    ch = input('Выберите файл: ')
                    if ch.isdigit():
                        ch = int(ch)
                        if ch in files.keys():
                            return dir_path + '\\' + files[ch]
                else:
                    print('\nВ данной директории нет подходящих аудиофайлов\n')
                    opt = True
            else:
                opt = True
        else:
            opt = True


def select_menu():
    sel = input('''Способ выбора файла:
    1 - Выбрать из директории
    2 - Ввести абсолютный путь до файла
    ''')
    if sel == '1':
        return dir_menu()
    elif sel == '2':
        while True:
            file_path = input('Введите абсолютный путь до файла:\n')
            if file_path[0] == '"':
                file_path = file_path[1:-1]
            if os.path.exists(fr'{file_path}'):
                if file_path.split('.')[-1] in ['mp3', 'ogg']:
                    file_path = fr'{file_path}'
                    return file_path
                else:
                    print('\nВаш аудиофайл должен иметь расширение .mp3 или .ogg\n')
            else:
                print('\nФайл не найден\n')
    else:
        input()



if __name__ == '__main__':
    choice = input('''Тип отправки:
    1 - голосовое сообщение
    2 - спам обычными сообщениями
    ''')
    match choice:
        case '1':
            id = select()
            print('\n*** Если аудиофайл - не моно, то на телефонах голосовое сообщение не будет воспроизводиться. Переведите свой аудиофайл в моно .mp3 или .ogg на сайте https://fconvert.ru/audio/ ***\n')
            file_path = select_menu()
            for i in id:
                try:
                    send_voice(i, file_path)
                except vk_api.exceptions.ApiError as e:
                    print(f'\nВы не можете отправлять сообщения пользователю id{i}\n')
        case '2':
            id = select('spam')
            text = input('Введите сообщение:\n')
            try:
                spam(id, text)
            except vk_api.exceptions.ApiError:
                print('\nВы не можете отправлять сообщения этому пользователю\n')