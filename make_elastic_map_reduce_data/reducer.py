import sys
from collections import Counter 
import json
import pickle
term_freq = {}
for line in sys.stdin:
  line = line.strip().split("\t")[-1]
  tf = dict( Counter( line.split() ) ) 
  for term, freq in tf.items(): 
    if term_freq.get( term ) is None:
      term_freq[term] = 0
    term_freq[term] += 1

for term, freq in sorted( term_freq.items(), key=lambda x:x[1] ):
  print( term, freq )

