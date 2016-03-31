import ConfigParser

Config = None

if Config is None:
    Config = ConfigParser.ConfigParser()
    Config.read('config.ini')

SERVICES_DIR = 'services'
RECORDINGS_DIR = 'recordings'
WMM_DIR = 'wmm'
LOG_DIR = 'wmm/logs'
SERVICE_LOG_DIR = 'wmm/logs/services'
RECORDING_LOG_DIR = 'wmm/logs/recordings'
LIB_DIR = 'wmm/lib'
WIREMOCK_JAR_PATH = 'wmm/libs/wiremock-1.57-standalone.jar'
WM_JAR_NAME = 'wiremock-1.57-standalone.jar'
WM_JAR_URL = 'http://repo1.maven.org/maven2/com/github/tomakehurst/wiremock/1.57/wiremock-1.57-standalone.jar'