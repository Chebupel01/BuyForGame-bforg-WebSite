"""import requests
import json
from requests import post
print(requests.get(f'http://127.0.0.1:5000/api/ads').json())
print(requests.delete('http://127.0.0.1:5000/api/ads/2').json())"""

from turtle import *
tracer(0)
k = 30
for i in range(15):
    forward(5 * k)
    left(90)

up()
for x in range(-k, k):
    for y in range(-k, k):
        goto(x * k, y * k)
        dot(5)
done()