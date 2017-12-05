import glob

import os

import json

from datetime import datetime

dt = datetime.now()
# originalのhour flag無視
# time_dirname = "%s"%( tdatetime.strftime('%Y_%m_%d_%H') )
time_dirname = "%s"%( dt.strftime('%Y_%m_%d') )

HOME = os.environ['HOME']
for mast in glob.glob('output/*'):
  hour = mast.split('/').pop()
  # いまスクレイピングしている可能性があるものは、変換しない
  if time_dirname in hour:
    continue
  key_val = {}
  for filename in glob.glob(mast + '/*'):
    print(filename)
    key = filename
    val = open(filename).read()
    key_val[key] = val
  open(HOME + '/YahooTopics/YahooTopics{}.json'.format(hour), 'w').write( json.dumps(key_val, indent=2, ensure_ascii=False) )
  os.system('zip -r {mast}.zip {mast}'.format(mast=mast))
  os.system('mv {mast}.zip '.format(mast=mast)+ HOME + '/YahooTopicsZip')
  os.system('rm -rf {mast}'.format(mast=mast))
