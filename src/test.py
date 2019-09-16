#!/usr/bin/python3
import unittest
import utils

# test data
filenames = {
  'Interstellar.mkv': 'Interstellar',
  'Interstellar.avi': 'Interstellar',
  'Interstellar.720p.mkv': 'Interstellar',
  'Interstellar.MULTI.mkv': 'Interstellar',
  'Interstellar.VOSTFR.mkv': 'Interstellar',
  'Interstellar.VOST.mkv': 'Interstellar',
  'Interstellar.2016.mkv': 'Interstellar',
  'Interstellar.MULTI.1080p.mkv': 'Interstellar',
  'Interstellar.2016.1080p.mkv': 'Interstellar',
  'Interstellar.2016.MULTI.mkv': 'Interstellar',
  'Blade.Runner.mkv': 'Blade Runner',
  'Blade.Runner.avi': 'Blade Runner',
  'Blade.Runner.720p.mkv': 'Blade Runner',
  'Blade.Runner.MULTI.mkv': 'Blade Runner',
  'Blade.Runner.VOSTFR.mkv': 'Blade Runner',
  'Blade.Runner.VOST.mkv': 'Blade Runner',
  'Blade.Runner.1982.mkv': 'Blade Runner',
  'Blade.Runner.MULTI.1080p.mkv': 'Blade Runner',
  'Blade.Runner.1982.1080p.mkv': 'Blade Runner',
  'Blade.Runner.1982.MULTI.mkv': 'Blade Runner',
  'Blade.Runner.1982.MULTI.1080p.mkv': 'Blade Runner',
  'Blade.Runner.1982.MULTI.1080p.mkv': 'Blade Runner',
  'Blade.Runner.1982.1982.mkv': 'Blade Runner 1982',
  'Blade.Runner.1982.2019.mkv': 'Blade Runner 1982',
  'Blade.Runner.1982.2049.mkv': 'Blade Runner 1982',
  'Blade.Runner.2049.mkv': 'Blade Runner 2049',
  'Blade.Runner.2049.MULTI.1080p.mkv': 'Blade Runner 2049',
  'Blade.Runner.2049.1080p.mkv': 'Blade Runner 2049',
  'Blade.Runner.2049.2017.MULTI.1080p.mkv': 'Blade Runner 2049',
  'C\'est.comme.ça.2018.FRENCH.720p.mkv': 'C\'est comme ça',
  'L\'élève.Ducobu.TRUEFRENCH.720p.mkv': 'L\'élève Ducobu',
}

# run test
class TestParseFilenameMethod(unittest.TestCase):

  def testFilename(self):
    for filename in filenames:
      title = utils.extractTitle(filename)
      self.assertEqual(filenames[filename], title)

if __name__ == '__main__':
  unittest.main()
