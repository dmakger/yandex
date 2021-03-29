"""
Данная программа помогает создавать запросы.
Т.е. если вы захотели создать запрос к серверу, то эта программа поможет вам.
"""

def input_json():
    """Ввод json"""
    print('Чтобы прекратить ввод, введите строку состоящую только из \'\\n\'')
    json = str()
    s = input()
    while s != '':
        json += s
        s = input()
    return json

def get_command(url, request_type):
    """Создаст и вернет команду"""
    command = None
    if request_type == 'get':
        command = "curl " + url
    elif request_type == 'post':
        #! Введите нужный json-запрос
        print('Введите данные в виде json')
        form_json = input_json()
        json_one_line = ''.join(''.join(form_json.split('\n')).split())
        command = "curl -X POST -H \"Content-Type: application/json\" -d '" + json_one_line + "' " + url
    elif request_type == 'patch':
        #! Введите нужный json-запрос
        print('Введите данные в виде json')
        form_json = input_json()
        json_one_line = ''.join(''.join(form_json.split('\n')).split())
        command = "curl -X PATCH -H \"Content-Type: application/json\" -d '" + json_one_line + "' " + url
    return command

#! url которому передастся json-запрос
# url = '127.0.0.1:8000/api/couriers/2/'
print('Введите url: ', end='')
url = input()

print('Request type (post, get, patch): ', end='')
request_type = input().lower()
command = get_command(url, request_type)

print(command)
open('out.txt', 'w').write(command)



