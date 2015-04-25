from share import readquery, globfs, CONFIG
from os.path import join
from os import remove
from glob import glob
from random import shuffle

RETRIES = 10 # times
TIMEOUT = 30 # seconds
QUERY_FILE = 'produce/in/query.txt'
URL_PATH = 'produce/in/url'
IMG_PATH = 'produce/out/img'
HASH_PATH = 'produce/out/hash'
SKIP_PATH = 'produce/out/skip'
TMP_PATH = 'produce/out/tmp'

def to_produce(query):
  upath = join(URL_PATH, query)
  scraped = globfs(upath + '/*.url')
  produced = globfs(HASH_PATH + '/*.hash')
  skipped = globfs(SKIP_PATH + '/*.skip')
  res = list(set(scraped).difference(produced.union(skipped)))
  shuffle(res)
  return res

def download(query, urlmd5):
  url = readfile(join(URL_PATH, query, urlmd5+'.url'))
  logging.info('Downloading image %s: %s' % (urlmd5, url))
  res = call(['wget', '--no-check-certificate',
              '--tries', str(RETRIES), '--timeout', str(TIMEOUT),
              '--limit-rate', str(CONFIG['BW_LIMIT']),
              '-O', join(TMP_PATH, urlmd5+'.downloaded'),
              url])
  if res != 0:
    raise Skip('Error downloading image %s.' % urlmd5)

def cleartmp():
  for fname in glob(join(TMP_PATH, '*')):
    remove(fname)

if __name__ == '__main__':
  query = None
  while True:
    if readquery(QUERY_FILE) != query:
      query = readquery(QUERY_FILE)
      delay = CONFIG['PRODUCE_SLEEP_MIN']
      logging.info('Producing images for query "%s".' % query)
    to_prod = to_produce(query)
    if not to_prod:
      logging.info('Nothing to produce.')
    else:
      delay = CONFIG['PRODUCE_SLEEP_MIN']
    for urlmd5 in to_prod:
      try:
        download(query, urlmd5)
      except Skip as e:
        logging.warn('%s Skipping.' % str(e))
        cleartmp()
        writefile(join(SKIP_PATH, urlmd5, '.skip'), '')
