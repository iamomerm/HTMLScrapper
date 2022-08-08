import threading
import requests
from time import time
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from keywords import KEYWORDS

# Get URL
url = input('URL:')
url = url if url.startswith('http') else f'http://{url}'
html = requests.get(url, verify=False, timeout=10).text

# Start time
start_time = time()

# Parse
Soup = BeautifulSoup(html, 'lxml')
tags = [*[f'h{i + 1}' for i in range(6)], 'td', 'a']
data = []


def search(text, tag_name):
    for kw in KEYWORDS:
        keyword = kw["keyword"]
        if not kw['case_sensitive']:
            text = text.lower()
            keyword = keyword.lower()
        if keyword in text:
            data.append(f'[{tag_name}] {text} ({kw["keyword"]})')


threads = []
for tag in Soup.find_all(tags):
    thread = threading.Thread(target=lambda: search(tag.text.strip(), tag.name))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# End time
end_time = time()

# Output
pt = PrettyTable()
pt.field_names = ('Index', 'Data')
pt.add_rows([[i, x] for i, x in enumerate(data)])
print('Data:' + '\n')
print(pt)
print('\n' + 'Performance:' + '\n')
print(f'Threads (Tags): {len(threads)}')
print(f'Elapsed time: {end_time - start_time} sec')
