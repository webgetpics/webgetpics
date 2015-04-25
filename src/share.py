import os
import errno
import logging
from os.path import isfile, dirname, splitext, split
from glob import glob
from random import seed

DEFAULT_QUERY = 'dr zoidberg' # oh yes.
CONFIG_FILE = 'config.py'

# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python/600612#600612
def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise

def readfile(path):
  if isfile(path):
    with open(path) as f:
      return f.read()
  else:
    return ''

def writefile(path, contents):
  mkdir_p(dirname(path))
  with open(path, 'w') as f:
    f.write(contents)

def readquery(path):
  return readfile(path).strip().replace('\n','').replace('\r','') \
      or DEFAULT_QUERY

def globfs(g):
  return [splitext(split(x)[1])[0] for x in glob(g)]

CONFIG = eval(readfile(CONFIG_FILE))

logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
logging.getLogger().setLevel(logging.INFO)
seed()
