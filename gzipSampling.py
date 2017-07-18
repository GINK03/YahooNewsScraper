import glob
import gzip


MAX = 100000

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
