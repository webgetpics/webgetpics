from share import readquery, readfile, writefile, globfs, mkdir_p, CONFIG, \
                  runloop, allowquit
from os.path import join, isfile
from os import remove, rename
from glob import glob
from random import shuffle
from subprocess import call, check_output, CalledProcessError
from time import time, sleep
import logging

RETRIES = 3 # times
TIMEOUT = 20 # seconds
POLL_SLEEP = 1 # seconds
QUERY_FILE = 'produce/in/query.txt'
URL_PATH = 'produce/in/url'
IMG_PATH = 'produce/out/img'
HASH_PATH = 'produce/out/hash'
SKIP_PATH = 'produce/out/skip'
TMP_PATH = 'produce/out/tmp'
CMD_QUIT = 'produce/cmd/quit'

class Skip(Exception):
  pass

def to_produce(query):
  upath = join(URL_PATH, query)
  scraped = globfs(upath + '/*.url')
  produced = globfs(HASH_PATH + '/*.hash')
  skipped = globfs(SKIP_PATH + '/*.skip')
  res = list(set(scraped).difference(set(produced).union(skipped)))
  shuffle(res)
  return res

def download(query, urlmd5):
  url = readfile(join(URL_PATH, query, urlmd5+'.url'))
  logging.info('Downloading image %s: %s' % (urlmd5, url))
  res = call(['wget', '--no-check-certificate',
              '--tries', str(RETRIES), '--timeout', str(TIMEOUT),
              '--limit-rate', str(CONFIG['LIMIT_RATE']),
              '-O', join(TMP_PATH, urlmd5+'.downloaded'),
              url])
  if res != 0:
    raise Skip('Error downloading image %s.' % urlmd5)

def check_dims(urlmd5):
  try:
    dims = check_output(['identify', '-format', '%w %h',
                         join(TMP_PATH, urlmd5+'.downloaded')])
  except CalledProcessError:
    raise Skip('Error inspecting dims of image %s.' % urlmd5)
  logging.info('Image %s dimensions: %s' % (urlmd5, dims))
  if max([int(x) for x in dims.split()]) > CONFIG['IMG_MAX_DIM']:
    raise Skip('Image %s is too large.' % urlmd5)
  if min([int(x) for x in dims.split()]) < CONFIG['IMG_MIN_DIM']:
    raise Skip('Image %s is too small.' % urlmd5)

def resize(urlmd5):
  logging.info('Resizing image %s' % urlmd5)
  geom = '%ix%i' % (CONFIG['IMG_WIDTH'], CONFIG['IMG_HEIGHT'])
  if call(['convert', join(TMP_PATH, urlmd5+'.downloaded'),
           '-resize', geom,
           '-background', CONFIG['IMG_BGCOL'],
           '-gravity', 'center',
           '-extent', geom,
           join(TMP_PATH, urlmd5+'.'+CONFIG['IMG_EXT'])
  ]) != 0:
    raise Skip('Error resizing image %s.' % urlmd5)
  # Image might be a composite one, like animated gif or multi-page tiff.
  # In this case, just grab the last frame of it.
  mask = join(TMP_PATH, urlmd5+'*.'+CONFIG['IMG_EXT'])
  for tmppath in sorted(glob(mask), reverse=True):
    rename(tmppath, join(TMP_PATH, urlmd5+'.'+CONFIG['IMG_EXT']))
    break

def save_hash(urlmd5):
  try:
    imghash = check_output(['identify', '-format', '%#',
      join(TMP_PATH, urlmd5+'.'+CONFIG['IMG_EXT'])])
  except CalledProcessError:
    raise Skip('Error computing hash of image %s.' % urlmd5)
  logging.info('Image %s hash: %s' % (urlmd5, imghash))
  writefile(join(HASH_PATH, urlmd5+'.hash'), imghash)

def save_img(urlmd5):
  imghash = readfile(join(HASH_PATH, urlmd5+'.hash'))
  if isfile(join(IMG_PATH, imghash+'.'+CONFIG['IMG_EXT'])):
    logging.info('Image %s is already there.' % imghash)
  else:
    logging.info('Image %s is ready.' % imghash)
    rename(join(TMP_PATH, urlmd5+'.'+CONFIG['IMG_EXT']),
           join(IMG_PATH, imghash+'.'+CONFIG['IMG_EXT']))

def cleartmp():
  for fname in glob(join(TMP_PATH, '*')):
    remove(fname)

def main():
  mkdir_p(TMP_PATH)
  mkdir_p(IMG_PATH)
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
      if readquery(QUERY_FILE) != query:
        break
      allowquit(CMD_QUIT)
      cleartmp()
      try:
        download(query, urlmd5)
        check_dims(urlmd5)
        resize(urlmd5)
        save_hash(urlmd5)
        save_img(urlmd5)
      except Skip as e:
        logging.warn('%s Skipping.' % str(e))
        writefile(join(SKIP_PATH, urlmd5, '.skip'), '')
    endtime = time() + delay
    while time() < endtime:
      if query != readquery(QUERY_FILE):
        break
      allowquit(CMD_QUIT)
      sleep(POLL_SLEEP)
    delay = min(CONFIG['PRODUCE_SLEEP_MAX'], delay*2)

if __name__ == '__main__':
  runloop(main)
