from re import findall
from urllib import quote_plus, unquote_plus
from subprocess import check_output, CalledProcessError
from share import mkdir_p
import logging

RETRIES = 10 # times
RETRY_DELAY = 10 # seconds
TIMEOUT = 30 # seconds
BWLIMIT = 100000 # bytes/second

def find_img_urls(query):
  start = 0
  while True:
    cmd = ['curl',
      'https://www.google.com/search?q=%s&tbm=isch&start=%i' \
        % (quote_plus(query), start),
      '--compressed',
      '--retry', str(RETRIES),
      '--retry-delay', str(RETRY_DELAY),
      '--max-time', str(TIMEOUT),
      '--limit-rate', str(BWLIMIT),
      '-H', 'Host: www.google.com',
      '-H', 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:36.0) '
            'Gecko/20100101 Firefox/36.0',
      '-H', 'Accept: text/html,application/xhtml+xml,application/xml;'
            'q=0.9,*/*;q=0.8',
      '-H', 'Accept-Language: en-US,en;q=0.5',
      '-H', 'Connection: keep-alive']
    print cmd
    try:
      res = check_output(cmd)
    except CalledProcessError as e:
      logging.warn('Error calling curl: %s' % str(e))
      break
    urls = findall('imgurl=([^&]+)&amp;imgrefurl=', res)
    if not urls:
      break
    for url in urls:
      start += 1
      yield unquote_plus(unquote_plus(url))

logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
logging.getLogger().setLevel(logging.INFO)
