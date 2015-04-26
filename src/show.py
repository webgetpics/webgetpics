from share import runloop, readquery, readfile, writefile, \
                  CONFIG, allowquit, command
from os import environ
from os.path import join, isfile
from random import choice
from subprocess import call
from time import time
import logging

POLL_SLEEP = 1 # seconds
QUERY_FILE = 'show/in/query.txt'
URL_PATH = 'show/in/url'
HASH_PATH = 'show/in/hash'
IMG_PATH = 'show/in/img'
HIDQRY_PATH = 'show/out/hidden/query'
HIDGLOB_PATH = 'show/out/hidden/global'
CURURL_FILE = 'show/out/current.url'
CMD_QUIT = 'show/cmd/quit'
CMD_HIDE_QUERY = 'show/cmd/hide-query'
CMD_HIDE_GLOBAL = 'show/cmd/hide-global'
CMD_SKIP = 'show/cmd/skip'

def refresh(query, url2hash, hash2urls, hidden):
  scraped = globfs(join(URL_PATH, query, '*.url'))
  produced = globfs(join(HASH_PATH, '*.hash'))
  for urlmd5 in set(scraped).intersection(produced):
    if urlmd5 not in url2img:
      url = readfile(join(URL_PATH, query, urlmd5+'.url'))
      imghash = readfile(join(HASH_PATH, urlmd5+'.hash'))
      url2hash[urlmd5] = imghash
      hash2urls.setdefault(imghash, []).append(url)
      if isfile(join(HIDQRY_PATH, query, imghash+'.hidden')) \
      or isfile(join(HIDGLOB_PATH, imghash+'.hidden')):
        hidden.add(imghash)

def pick_img(times, url2img, hash2urls, hidden):
  images = set(url2img.values()).difference(hidden)
  if not images:
    logging.info('No images to pick from.')
    writefile(CURURL_FILE, '')
    return None
  newbies = [x for x in images if x not in times]
  winner = choice(newbies) if newbies else min(images, key=lambda x: times[x])
  times[winner] = time()
  urls = sorted(hash2urls[winner])
  logging.info('Picked image (%i of %i): %s %s' % \
    (len(times), len(images), winner, ' '.join(urls)))
  writefile(CURURL_FILE, '\n'.join(urls))
  return winner

def setbg(imghash):
  img = join(IMG_PATH, imghash+'.'+CONFIG['IMG_EXT'])
  env = dict(environ.items() + {'DISPLAY': CONFIG['DISPLAY']}.items())
  if isfile(img):
    call(['feh', '--bg-max', img], env=env)
  else:
    logging.warn('Cannot find image: %s' % img)

def allowhidequery(query, picked, hidden):
  if command(CMD_HIDE_QUERY):
    if picked:
      logging.info('Hiding image %s from query "%s".' % (picked, query))
      writefile(join(HIDQRY_PATH, query, picked+'.hidden'), '')
      hidden.add(picked)
    else:
      logging.info('No images. Ignoring hide from query "%s".' % query)
    raise Handled()

def allowhideglobal(query, picked, hidden):
  if command(CMD_HIDE_GLOBAL):
    if picked:
      logging.info('Hiding image %s from all queries.' % picked)
      writefile(join(HIDGLOB_PATH, picked+'.hidden'), '')
      hidden.add(picked)
    else:
      logging.info('No images. Ignoring hide from all queries.')
    raise Handled()

def allowskip():
  if command(CMD_SKIP):
    logging.info('Skipping current image.')
    raise Handled()

class Handled(Exception):
  pass

def main():
  query = None
  while True:
    if readquery(QUERY_FILE) != query:
      query = readquery(QUERY_FILE)
      logging.info('Showing images for query "%s".' % query)
      times = {}
      hidden = set()
      url2hash = {}
      hash2urls = {}
    refresh(query, url2hash, hash2urls, hidden)
    picked = pick_img(times, url2hash, hash2urls, hidden)
    if picked:
      setbg(picked)
      endtime = time() + CONFIG['SHOW_SLEEP']
    else:
      endtime = time() + CONFIG['SHOW_SLEEP_NO_IMG']
    try:
      while time() < endtime:
        if query != readquery(QUERY_FILE):
          break
        allowquit(CMD_QUIT)
        allowhidequery(query, picked, hidden)
        allowhideglobal(query, picked, hidden)
        allowskip()
        sleep(POLL_SLEEP)
    except Handled:
      pass

if __name__ == '__main__':
  runloop(main)
