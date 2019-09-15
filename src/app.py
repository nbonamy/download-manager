import re
import os.path
import subprocess
import consts
import urllib.parse
from downloader import Downloader
from playhouse.shortcuts import model_to_dict
from flask import Flask, request, jsonify, abort
from model import database, Download

# the apps
app = Flask(__name__)

@app.route('/init')
def init():
  database.connect()
  database.create_tables([Download])
  return 'OK'

@app.route('/list')
def list():
  database.connect()
  downloads = Download.select()
  return jsonify({'rows':[model_to_dict(d) for d in downloads]})

@app.route('/download')
def download():

  # for now
  #url = urllib.parse.unquote(url)
  url = request.args.get('url')
  if len(url) < 1:
    abort(400)

  # try to get more info
  downloader = Downloader(consts.DOWNLOAD_DIR)
  download = downloader.get_download_info(url)
  if download is None:
    abort(500)

  # now run download process
  if downloader.download(download) is False:
    abort(500)

  # done
  return jsonify(model_to_dict(download))

@app.route('/status')
def status_all():

  downloader = Downloader(consts.DOWNLOAD_DIR)
  downloads = Download.select().where((Download.status != consts.STATUS_PROCESSED) & (Download.status != consts.STATUS_CANCELLED)).order_by(Download.started_at.desc())
  return jsonify({'rows':[downloader.get_status(d) for d in downloads]})

@app.route('/status/<id>')
def status_one(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(consts.DOWNLOAD_DIR)
  return jsonify(downloader.get_status(download))

@app.route('/start/<id>')
def start(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  # now run download process
  downloader = Downloader(consts.DOWNLOAD_DIR)
  if downloader.download(download) is False:
    abort(500)

  # done
  return jsonify(model_to_dict(download))

@app.route('/cancel/<id>')
def cancel(id):

  try:
    download = Download.get_by_id(id)
  except:
    abort(404)

  downloader = Downloader(consts.DOWNLOAD_DIR)
  if downloader.cancel(download):
    return jsonify({'status': 'ok'})
  else:
    abort(500)
