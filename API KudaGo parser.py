import json
import requests

"""Parser API KudaGo. Full list of places in Saint Petersburg."""
"""Input: site`s API url. Output: .json file with class 'list':
    [{'id':...,'name':...,'categories':[...]},...]"""

url_base = "https://kudago.com/public-api/v1.4/places/?"
url_fields = "&fields=id,title,categories,coords"
url_location = "&location=spb"
url_pages = "&page_size=100"
url_full = url_base + url_fields + url_location + url_pages

data = []
with open('data/Places_spb_list.json', 'w', encoding='utf-8') as ouf:
    while url_full is not None:
        response = requests.get(url_full)
        page_data = response.json()
        data.extend(page_data['results'])
        url_full = page_data['next']
    print(f'parsed {len(data)} places')

    # delete places with no categories
    data = list(filter(lambda place: len(place['categories']) > 0, data))

    category_sorted = sorted(data, key=lambda x: x['categories'][0])
    print(f'dumping {len(data)} places to json')
    json.dump(category_sorted, ouf, indent=2, ensure_ascii=False)
