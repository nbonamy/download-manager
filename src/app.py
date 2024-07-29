#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()

import utils
import consts
import os.path
from config import Config
from downloader import Downloader
from bottle import Bottle, request, abort
from model import create_database, Download

# we need a database
create_database()

# and an app with a config
app = Bottle()
app.config.update({
  'config': Config(consts.CONFIG_PATH)
})

@app.route('/ws/check')
def check():

  # check configuration
  errors = []
  if app.config.get('config').download_path() is None:
    errors.append('Download path missing from configuration')
  if app.config.get('config').target_path() is None:
    errors.append('Target path missing from configuration')
  if len(errors):
    return {'status': 'ko', 'errors': errors}

  # seems good!
  return {'status': 'ok'}

@app.route('/ws/init')
def init():
  create_database()
  return 'OK'

@app.route('/ws/status')
def status():
  downloader = Downloader(app.config.get('config'))
  downloads = Download.select().where((Download.status != consts.STATUS_PROCESSED) & (Download.status != consts.STATUS_CANCELLED)).order_by(Download.started_at.desc())
  return {'items':[downloader.get_status(d) for d in downloads]}

@app.route('/ws/history')
def list():
  downloader = Downloader(app.config.get('config'))
  downloads = Download.select().where((Download.status >= consts.STATUS_PROCESSED) | (Download.status < 0)).order_by(Download.started_at.desc())
  return {'items':[downloader.get_status(d) for d in downloads]}

@app.route('/ws/info')
def info():

  # for now
  #url = urllib.parse.unquote(url)
  url = request.query.url
  if len(url) < 1:
    return abort(400)

  # try to get more info
  downloader = Downloader(app.config.get('config'))
  download = downloader.get_download_info(url)
  if download is None:
    abort(500)

  # done
  return {
    'info': download.to_dict(),
    'title': utils.extractTitle(download.filename)
  }

@app.route('/ws/download')
def download():

  # for now
  #url = urllib.parse.unquote(url)
  url = request.query.url
  if len(url) < 1:
    abort(400)

  # try to get more info
  downloader = Downloader(app.config.get('config'))
  download = downloader.get_download_info(url, request.query.dest)
  if download is None:
    abort(404)

  # now run download process
  if downloader.download(download) is False:
    abort(500)

  # done
  return download.to_dict()

@app.route('/ws/start/<id>')
def start(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  # now run download process
  downloader = Downloader(app.config.get('config'))
  if downloader.download(download) is False:
    abort(500)

  # done
  return download.to_dict()

@app.route('/ws/status/<id>')
def status_one(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(app.config.get('config'))
  return downloader.get_status(download)

@app.route('/ws/title/<id>')
def title(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  return {'title': utils.extractTitle(download.filename)}

@app.route('/ws/downloads')
def downloads():
  return {'items': app.config.get('config').download_paths()}

@app.route('/ws/destinations')
def destinations():

  dirs = [ app.config.get('config').target_path() ]
  for dirname, dirnames, filenames in os.walk(dirs[0], followlinks=True):

    while True:
      size = len(dirnames)
      for subdirname in dirnames:
        if subdirname[0] == '.' or subdirname[:2] == '__':
          dirnames.remove(subdirname)
          break
      if size == len(dirnames):
        break

    #print(dirname)
    for subdirname in dirnames:
      dirs.append(os.path.join(dirname, subdirname))

  dirs.sort()
  return {'items': dirs}

@app.route('/ws/finalize/<id>')
def finalize(id):

  # check title
  title = request.query.title
  if title is None or len(title) < 1:
    abort(400)

  # check destination
  dest = request.query.dest
  subfolder = request.query.subfolder
  if dest is None or len(dest) < 1:
    abort(400)

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)


  try:
    downloader = Downloader(app.config.get('config'))
    downloader.finalize(download, os.path.join(dest, subfolder), title)
    return {'status': 'ok'}
  except Exception as ex:
    abort(500, ex)

@app.route('/ws/cancel/<id>')
def cancel(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(app.config.get('config'))
  if downloader.cancel(download):
    return {'status': 'ok'}
  else:
    abort(500)

@app.route('/ws/purge/<id>')
def purge(id):
  Download.delete().where(Download.id == id).execute()
  return {'status': 'ok'}

# run server
app.run(host='0.0.0.0', port=5555, debug=True, server='gevent')
