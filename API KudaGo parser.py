# https://kudago.com/public-api/v1.4


"""Parser API KudaGo. Full list of places in Saint Petersburg."""
"""Input: site`s API url. Output: .json file with class 'list':
    [{'id':...,'name':...,'categories':[...]},...]"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

url_base = "https://kudago.com/public-api/v1.4/places/?"
url_fields = "&fields=id,title,categories"
url_location = "&location=spb"
url_pages = "&page_size=100&page="
url_full = url_base + url_fields + url_location + url_pages
page = 1
max_page_spb = 39  # Found manually for: location=spb, page_size=100.


def get_data(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return e
    try:
        data = str(BeautifulSoup(html.read()))
    except AttributeError as e:
        return None
    return data


page_data = ''
data = ''
with open('data/Places_spb_list.json',
          'w', encoding="utf-8") as ouf:
    while (page_data != None):
        page_data = get_data(url_full + str(page))
        if (type(page_data) != str):
            break
        if page == 1:
            data = json.loads(page_data[page_data.find('['):-1:1])
        else:
            data += json.loads(page_data[page_data.find('['):-1:1])
        page += 1
    category_sorted = sorted(data, key=lambda x: x['categories'][0])
    json.dump(category_sorted, ouf)
    print(page)
