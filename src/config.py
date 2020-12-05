import configparser

# config
CONFIG_SECTION_GENERAL = 'General'
CONFIG_OPTION_DOWNLOAD_PATH = 'DownloadPath'
CONFIG_OPTION_TARGET_PATH = 'TargetPath'
CONFIG_OPTION_TESTING = 'Test'

class Config:

  config = None

  def __init__(self, path):
    self.config = configparser.ConfigParser()
    self.config.read(path)

  # returns first path
  def download_path(self):
    paths = self.download_paths()
    if isinstance(paths, list):
      return paths[0]
    else:
      return paths

  def download_paths(self):
    paths = self.__get_value(CONFIG_SECTION_GENERAL, CONFIG_OPTION_DOWNLOAD_PATH)
    return paths.split(',')

  def target_path(self):
    return self.__get_value(CONFIG_SECTION_GENERAL, CONFIG_OPTION_TARGET_PATH)

  def is_testing(self):
    return self.config.has_option(CONFIG_SECTION_GENERAL, CONFIG_OPTION_TESTING)

  def __get_value(self, section, option):
    if self.config.has_option(section, option):
      return self.config.get(section, option).strip("'")
    else:
      return None
