from re import findall
from urllib import quote_plus, unquote_plus
from subprocess import check_output, CalledProcessError
from share import readquery, writefile, CONFIG
from time import time, sleep
from os.path import isfile, join
from os import rename
from md5 import md5
import logging

RETRIES = 10 # times
RETRY_DELAY = 10 # seconds
TIMEOUT = 30 # seconds
POLL_SLEEP = 1 # seconds
QUERY_FILE = 'scrape/in/query.txt'
URL_PATH = 'scrape/out/url'

def find_img_urls(query):
  ijn = 0
  while True:
    cmd = ['curl',
      'https://www.google.com/search?q=%s&tbm=isch&ijn=%i' \
        % (quote_plus(query), ijn),
      '--silent',
      '--compressed',
      '--retry', str(RETRIES),
      '--retry-delay', str(RETRY_DELAY),
      '--max-time', str(TIMEOUT),
      '--limit-rate', str(CONFIG['LIMIT_RATE']),
      '-H', 'Host: www.google.com',
      '-H', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:36.0) '
            'Gecko/20100101 Firefox/36.0',
      '-H', 'Accept: text/html,application/xhtml+xml,application/xml;'
            'q=0.9,*/*;q=0.8',
      '-H', 'Accept-Language: en-US,en;q=0.5',
      '-H', 'Connection: keep-alive']
    try:
      res = check_output(cmd)
    except CalledProcessError as e:
      logging.warn('Error calling curl: %s' % str(e))
      break
    urls = findall('imgurl=([^&]+)&amp;imgrefurl=', res)
    if not urls:
      break
    ijn += 1
    for url in urls:
      yield unquote_plus(unquote_plus(url))

if __name__ == '__main__':
  while True:
    query = readquery(QUERY_FILE)
    logging.info('Scraping images for query "%s".' % query)
    for url in find_img_urls(query):
      if query != readquery(QUERY_FILE):
        break
      fname = join(URL_PATH, query, md5(url).hexdigest())
      fnurl = '%s.url' % fname
      fnpart = '%s.part' % fname
      if isfile(fnurl):
        logging.info('Image already exists "%s": %s' % (fnurl, url))
      else:
        logging.info('Scraped new image "%s": %s' % (fnurl, url))
        writefile(fnpart, url)
        rename(fnpart, fnurl)
    logging.info('Sleeping for %i seconds' % CONFIG['SCRAPE_SLEEP'])
    endtime = time() + CONFIG['SCRAPE_SLEEP']
    while time() < endtime:
      if query != readquery(QUERY_FILE):
        break
      sleep(POLL_SLEEP)
