import logging

from grab import Grab

g = Grab()

logging.basicConfig(level=logging.DEBUG)

g.setup(log_dir='log/grab')
url = 'https://yandex.ru/'
g.go(url)
print(g.xpath_text('//title'))

# a=g.search(u'яндекс'.encode('utf-8'), byte=True)

print(g)