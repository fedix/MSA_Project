import numpy as np
from misc import api_key
import requests
import time
import json

TL = (60.101107, 30.170076)
TR = (60.038240, 30.462587)
BL = (59.811478, 30.122698)
BR = (59.747713, 30.707720)

cols = np.linspace(BL[1], BR[1], num=34)
rows = np.linspace(BL[0], TL[0], num=33)
a = np.meshgrid(cols, rows)

b = list(zip(a[0].flatten(), a[1].flatten()))

a = []
c = 0
base = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
list_of_places = ['bar', "art_gallery", 'restaurant', 'cafe', 'bakery', 'meal_takeaway', 'museum', 'shopping_mall',
                  'tourist_attraction']
list_of_center = b
for i in list_of_places:
    a = []
    for center in list_of_center:
        url = f'{base}?key={api_key}&location={center[1]},{center[0]}&radius=710&type={i}'

        myfile = requests.get(url)
        res = myfile.json()['results']
        a.extend(res)
        print(url)
        try:
            next_page = myfile.json()['next_page_token']
        except:
            next_page = None

        c += 1
        print(c)
        time.sleep(5)
        while next_page is not None:
            url = f'{base}?key={api_key}&pagetoken={next_page}'
            req = requests.get(url).json()
            try:
                next_page = req['next_page_token']
            except:
                next_page = None
            res = req['results']

            a.extend(res)
            time.sleep(5)
            print(c)

    with open(f'places_{i}.json', 'w') as f:
        json.dump(a, f, indent=2)
