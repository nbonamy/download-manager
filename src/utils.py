import re
import datetime
from math import log2

_suffixes = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

def humansize(size):
  # determine binary order in steps of size 10
  # (coerce to int, // still returns a float)
  order = int(log2(size) / 10) if size else 0
  # format file size
  # (.4g results in rounded numbers for exact matches and max 3 decimals,
  # should never resort to exponent values)
  return '{:.2g} {}'.format(size / (1 << (order * 10)), _suffixes[order])

def extractTitle(filename):

  # first split to get each part
  parts = filename.split('.')

  # now qualify each part
  # their last occurence is the file extension
  lastDate = len(parts)-1
  lastLang = len(parts)-1
  lastFormat = len(parts)-1

  # scan
  for i in range(len(parts)):
    part = parts[i].lower()
    m = re.match(r'^([0-9][0-9][0-9][0-9])$', part) 
    if m:
      if lastDate == len(parts)-1:
        year = int(m.groups(0)[0])
        if year <= datetime.datetime.now().year + 5:
          lastDate = i
      else:
        lastDate = i
    if part in [ 'multi', 'vo', 'vf', 'vost', 'vostfr', 'french', 'truefrench' ]:
      lastLang = i
    if part in [ 'sd', 'hd', 'bluray', '720p', '1080p', '2160p', '4k' ]:
      lastFormat = i

  # first non title
  titleEnd = min(lastDate, lastLang, lastFormat)

  # join
  parts = parts[:titleEnd]
  return ' '.join(parts)
