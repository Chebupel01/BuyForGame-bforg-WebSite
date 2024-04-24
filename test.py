import requests
import json
from requests import post
print(requests.get(f'http://127.0.0.1:5000/api/users').json())
print(post(f'http://127.0.0.1:5000/api/users',
           json={'nickname': 'Фрика',
                 'email': 'a@asddas.ru',
                 'hashed_password': '1111'}).json())
print(requests.delete(f'http://127.0.0.1:5000/api/user/7').json())