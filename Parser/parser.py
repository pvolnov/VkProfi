import re
import warnings

import urllib3
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")
import pickle
m=[]
for i in range(240):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://team.mail.ru/vacancy/?specialty={}&town=&tag=&search='.format(i))
    d = (r.data.decode('utf-8'))


    # soup = BeautifulSoup(d)
    # # print(soup.prettify())
    #
    # at = soup.find_all('h3',attrs={'class':'title-block-sub'})
    try:
        c = str(re.search(r'<h3 class="title-block-sub">.*</h3>', d).group())
        c=c.replace('<h3 class="title-block-sub">','')
        c=c.replace('</h3>','')
        m.append({c:i})
        # print(c,i)
    except:
        1
with open('prif_id', 'wb') as f:
    pickle.dump(m,f)
print(m)
# for link in soup.find_all('a'):
#     pass