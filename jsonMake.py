import glob

import os

import json

from datetime import datetime

import sys

dt = datetime.now()
# originalのhour flag無視
# time_dirname = "%s"%( tdatetime.strftime('%Y_%m_%d_%H') )
time_dirname = "%s"%( dt.strftime('%Y_%m_%d') )

HOME = os.environ['HOME']

import concurrent.futures

import MeCab
def _map1(mast):
  hour = mast.split('/').pop()
  # いまスクレイピングしている可能性があるものは、変換しない
  if time_dirname in hour:
    return
  key_val = {}
  for filename in glob.glob(mast + '/*'):
    print(filename)
    key = filename
    val = open(filename).read()
    key_val[key] = val
  open(HOME + '/sda/YahooTopics/YahooTopics{}.json'.format(hour), 'w').write( json.dumps(key_val, indent=2, ensure_ascii=False) )
  os.system('zip -r {mast}.zip {mast}'.format(mast=mast))
  os.system('mv {mast}.zip '.format(mast=mast)+ HOME + '/sda/YahooTopicsZip')
  os.system('rm -rf {mast}'.format(mast=mast))

if '--map1' in sys.argv:
  masts = [mast for mast in glob.glob('output/*')]
  with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
    exe.map(_map1, masts)

if '--map2' in sys.argv:
  jsons = glob.glob(HOME + '/sda/YahooTopics/YahooTopics*.json' )
  m = MeCab.Tagger('-Owakati')
  for name in jsons:
    save_name = name.split('/').pop()
    print(name)
    url_text = json.loads( open(name).read() ) 
    url_wakati = {}
    for url, text in url_text.items():
      url_wakati[url] = m.parse(text).strip().split()

    open(HOME + '/sda/YahooTopicsWakati/{}'.format(save_name), 'w').write( json.dumps(url_wakati, indent=2, ensure_ascii=False) )

from collections import Counter
import itertools
import functools
if '--fold1' in sys.argv or '--term' in sys.argv:
  def _fold1(name):
    terms = set()
    print(name)
    url_wakati = json.loads( open(name).read() )
    [ [terms.add(term) for term in _terms] for _terms in [set(wakati) for url, wakati in url_wakati.items()] ]
    #print( terms )
    return terms
  names = [name for name in glob.glob(HOME + '/sda/YahooTopicsWakati/*.json')][:100]
  terms_ = set()
  with concurrent.futures.ProcessPoolExecutor(max_workers=15) as exe:
    for terms in exe.map(_fold1, names) :
      terms_ = terms_ | terms
      #print(terms_)
  term_index = {}
  for index, term in enumerate(terms_):
    term_index[term] = index

  open('term_index.json', 'w').write( json.dumps(term_index, indent=2, ensure_ascii=False) )
import re
import math
if '--map3' in sys.argv:
  term_index = json.loads( open('term_index.json').read() )

  for name in glob.glob(HOME + '/sda/YahooTopicsWakati/*.json'):
    print(name)
    date = re.search(r'Wakati/YahooTopics(\d\d\d\d_\d\d_\d\d)_\d\d.json', name)
    if date is None:
      continue
    date = date.group(1)
    if os.path.exists( HOME + '/sda/YahooTopicsTermFreq/{}.json'.format(date) ) is True:
      continue

    print( date )
  
    url_wakati = json.loads( open(name).read() )
    index_freq = {}
    for url, wakati in url_wakati.items():
      for term, freq in Counter(wakati).items():
        if term_index.get(term) is None:
          continue
        index_freq[ term_index[term] ] = math.log(freq + 1.0) 
    open(HOME + '/sda/YahooTopicsTermFreq/{}.json'.format(date), 'w').write( json.dumps(index_freq, indent=2) )
