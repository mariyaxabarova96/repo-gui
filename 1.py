import requests
import json

def data(url: str) -> dict:
        response = requests.get(url)
        return response.json()

username = input('Введите username: ')
if username == False:
    print('Введите другое имя пользователя')
url = 'https://api.github.com/users/'+username+'/repos'

response = data(url)
list_of_repo = []
for i in response:
    list_of_repo.append(i['name'])
    if len(list_of_repo)==0:
        print('У данного пользователя нет репозиториев')
print(f'Список репозиториев пользователя {username}')
print(list_of_repo)

with open('repo.json', 'w') as f:
    json_repo = json.dump(list_of_repo, f)