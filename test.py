import requests
import json
from requests import post
print(requests.get(f'http://127.0.0.1:5000/api/ads').json())
print(requests.delete('http://127.0.0.1:5000/api/ads/2').json())