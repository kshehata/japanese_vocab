#! /usr/bin/python

import re
fz_re = re.compile(r"(.)\(([^\)]*)\)")

def fz2conv(s):
  return fz_re.sub(lambda m : m.group(2), s), fz_re.sub(lambda m : m.group(1), s)

if __name__ == '__main__':
  import sys
  if len(sys.argv) > 1:
    for s in sys.argv[1:]:
      print("\t".join(fz2conv(s)))
  else:
    for line in sys.stdin:
      print("\t".join(fz2conv(line.strip())))
