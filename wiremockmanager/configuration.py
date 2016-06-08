import os
import ConfigParser


def get():
    return WmmConfig()


class WmmConfig:
    def __init__(self):
        self.WORKING_DIR = os.getenv('WMM_WORKING_DIR', os.getcwd())
        self.SERVICES_DIR = os.path.join(self.WORKING_DIR, 'services')
        self.RECORDINGS_DIR = os.path.join(self.WORKING_DIR, 'recordings')
        self.WMM_DIR = os.path.join(self.WORKING_DIR, 'wmm')
        self.LOG_DIR = os.path.join(self.WMM_DIR, 'logs')
        self.SERVICE_LOG_DIR = os.path.join(self.LOG_DIR, 'services')
        self.RECORDING_LOG_DIR = os.path.join(self.LOG_DIR, 'recordings')
        self.LIB_DIR = os.path.join(self.WMM_DIR, 'libs')
        self.WM_JAR_NAME = 'wiremock-1.57-standalone.jar'
        self.WIREMOCK_JAR_PATH = os.path.join(self.LIB_DIR, self.WM_JAR_NAME)
        self.WM_JAR_URL = 'http://repo1.maven.org/maven2/com/github/tomakehurst/wiremock/1.57/wiremock-1.57-standalone.jar'
