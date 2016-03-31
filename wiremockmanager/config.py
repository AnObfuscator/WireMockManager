import os
import ConfigParser

Config = None

if Config is None:
    Config = ConfigParser.ConfigParser()
    Config.read('config.ini')

SERVICES_DIR = 'services'
RECORDINGS_DIR = 'recordings'
WMM_DIR = 'wmm'
LOG_DIR = os.path.join(WMM_DIR, 'logs')
SERVICE_LOG_DIR = os.path.join(LOG_DIR, SERVICES_DIR)
RECORDING_LOG_DIR = os.path.join(LOG_DIR, RECORDINGS_DIR)
LIB_DIR = os.path.join(WMM_DIR, 'libs')
WM_JAR_NAME = 'wiremock-1.57-standalone.jar'
WIREMOCK_JAR_PATH = os.path.join(LIB_DIR, WM_JAR_NAME)
WM_JAR_URL = 'http://repo1.maven.org/maven2/com/github/tomakehurst/wiremock/1.57/wiremock-1.57-standalone.jar'