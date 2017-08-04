import glob
import gzip
import sys
import re
import pickle
import concurrent.futures

def samplingOne():
  MAX = 10000
  BUFF = set()
  for name in glob.glob('output/*/*'):
    BUFF.add(name)
    if len( BUFF ) >= MAX:
      break
  with gzip.open('sampling.txt.gz', 'wt') as f:
    for name in BUFF:
      text = open(name).read()
      print( name )
      f.write( text + '\n' )
  print( 'finished' )

def samplingEach():
  MAX = 1000000
  BUFF = set()
  for name in glob.glob('output/*/*'):
    BUFF.add(name)
    if len( BUFF ) >= MAX:
      break
  for e, buff in enumerate(BUFF):
    print( buff )
    with gzip.open('tmp/each/sampling_%09d.txt.gz'%e, 'wt') as f:
      text = open(buff).read()
      f.write( text )

def rotate():
  '''データ量が非常に多いので、定期的にgzipに圧縮するが、これも重いので、ポーリングで監視する'''
  while True:
    day_set()
    make_gzip()

def day_set():
  day_set = {}
  for name in glob.glob('output/*/*'):
    #print( name )
    ents = name.split('/')
    time = ents[1]
    day  = re.sub(r'_\d{1,}$', '', time)
    print( day )
    if day_set.get(day) is None:
      day_set[day] = set()
    day_set[day].add( name )
  open('day_set.pkl', 'wb').write( pickle.dumps(day_set) )

def _make_gip(arr):
  day, files = arr
  if day == 'pkl':
    return
  print(day)
  with gzip.open('day/' + day + 'txt.gz', 'wt') as f:
    #texts = []
    for file in files:
      text = open(file).read()
      #texts.append( text )
      f.write( text + '___SEP___\n' )

def make_gzip():
  day_set = pickle.loads( open('day_set.pkl', 'rb').read() )
  arrs = [(day,files) for day, files in sorted( day_set.items(), key=lambda x:x[0]*-1 )]
  with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    executor.map( _make_gip, arrs)

if __name__ == '__main__':
  if '--one' in sys.argv:
    samplingOne()

  if '--each' in sys.argv:
    samplingEach()

  if '--day_set' in sys.argv:
    day_set()

  if '--make_gzip' in sys.argv:
    make_gzip()

  if '--rotate' in sys.argv:
    rotate()
