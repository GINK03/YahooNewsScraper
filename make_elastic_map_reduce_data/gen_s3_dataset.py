import os
import sys
import math 

import glob
import gzip

import MeCab 

m = MeCab.Tagger("-Owakati")
for eg, name in enumerate( glob.glob("../output/*/*")) :
  if eg%100 == 0:
    print( eg, name )

  day_time = name.split("/")[-2]
  with open( name ) as f: 
    with gzip.open( "gzs/%s.gz"%day_time, "at" ) as g:
      text   = f.read()
      wakati = m.parse( text )
      g.write( wakati )
      #print( wakati )
