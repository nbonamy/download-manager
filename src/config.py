import configparser

# config
CONFIG_SECTION_GENERAL = 'general'
CONFIG_OPTION_DOWNLOAD_PATH = 'download_path'
CONFIG_OPTION_TARGET_PATH = 'target_path'

class Config:

  config = None

  def __init__(self, path):
    self.config = configparser.ConfigParser()
    self.config.read(path)

  def download_path(self):
    return self.__get_value(CONFIG_SECTION_GENERAL, CONFIG_OPTION_DOWNLOAD_PATH)

  def target_path(self):
    return self.__get_value(CONFIG_SECTION_GENERAL, CONFIG_OPTION_TARGET_PATH)

  def __get_value(self, section, option):
    if self.config.has_option(section, option):
      return self.config.get(section, option).strip("'")
    else:
      return None
