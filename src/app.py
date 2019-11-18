import re
import utils
import consts
import os.path
import subprocess
import urllib.parse
from config import Config
from downloader import Downloader
from playhouse.shortcuts import model_to_dict
from flask import Flask, request, jsonify, abort
from model import create_database, Download

# the apps
app = Flask(__name__)
create_database()

@app.before_request
def before_request():
  app.config.config = Config(consts.CONFIG_PATH)

@app.route('/ws/check')
def check():

  # check configuration
  errors = []
  if app.config.config.download_path() is None:
    errors.append('Download path missing from configuration')
  if app.config.config.target_path() is None:
    errors.append('Target path missing from configuration')
  if len(errors):
    return jsonify({'status': 'ko', 'errors': errors})

  # seems good!
  return jsonify({'status': 'ok'})

@app.route('/ws/init')
def init():
  create_database()
  return 'OK'

@app.route('/ws/status')
def status():
  downloader = Downloader(app.config.config)
  downloads = Download.select().where((Download.status != consts.STATUS_PROCESSED) & (Download.status != consts.STATUS_CANCELLED)).order_by(Download.started_at.desc())
  return jsonify({'items':[downloader.get_status(d) for d in downloads]})

@app.route('/ws/history')
def list():
  downloader = Downloader(app.config.config)
  downloads = Download.select().where((Download.status >= consts.STATUS_PROCESSED) | (Download.status < 0)).order_by(Download.started_at.desc())
  return jsonify({'items':[downloader.get_status(d) for d in downloads]})

@app.route('/ws/info')
def info():

  # for now
  #url = urllib.parse.unquote(url)
  url = request.args.get('url')
  if len(url) < 1:
    abort(400)

  # try to get more info
  downloader = Downloader(app.config.config)
  download = downloader.get_download_info(url)
  if download is None:
    abort(500)

  # done
  return jsonify({
    'info': model_to_dict(download),
    'title': utils.extractTitle(download.filename)
  })

@app.route('/ws/download')
def download():

  # for now
  #url = urllib.parse.unquote(url)
  url = request.args.get('url')
  if len(url) < 1:
    abort(400)

  # try to get more info
  downloader = Downloader(app.config.config)
  download = downloader.get_download_info(url)
  if download is None:
    abort(500)

  # now run download process
  if downloader.download(download) is False:
    abort(500)

  # done
  return jsonify(model_to_dict(download))

@app.route('/ws/start/<id>')
def start(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  # now run download process
  downloader = Downloader(app.config.config)
  if downloader.download(download) is False:
    abort(500)

  # done
  return jsonify(model_to_dict(download))

@app.route('/ws/status/<id>')
def status_one(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(app.config.config)
  return jsonify(downloader.get_status(download))

@app.route('/ws/title/<id>')
def title(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  return jsonify({'title': utils.extractTitle(download.filename)})

@app.route('/ws/destinations')
def destinations():

  dirs = []
  for dirname, dirnames, filenames in os.walk(app.config.config.target_path()):

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
  return jsonify({'items': dirs})

@app.route('/ws/finalize/<id>')
def finalize(id):

  # check title
  title = request.args.get('title')
  if title is None or len(title) < 1:
    abort(400)

  # check destination
  dest = request.args.get('dest')
  if dest is None or len(dest) < 1:
    abort(400)

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(app.config.config)
  if downloader.finalize(download, dest, title):
    return jsonify({'status': 'ok'})
  else:
    abort(500)

@app.route('/ws/cancel/<id>')
def cancel(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(app.config.config)
  if downloader.cancel(download):
    return jsonify({'status': 'ok'})
  else:
    abort(500)

@app.route('/ws/purge/<id>')
def purge(id):
  Download.delete().where(Download.id == id).execute()
  return jsonify({'status': 'ok'})
