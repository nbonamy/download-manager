import sys
import consts
from config import Config
from downloader import Downloader
from playhouse.shortcuts import model_to_dict

# for now
url = sys.argv[1]
if len(url) < 1:
  exit(-1)

# try to get more info
config = Config(consts.CONFIG_PATH)
downloader = Downloader(config)
download = downloader.get_download_info(url)
if download is None:
  exit(-1)

# done
print(model_to_dict(download))

