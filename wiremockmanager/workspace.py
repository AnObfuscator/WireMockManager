# Workspace structure:
# [WorkingDir]
#  -- services
#  -- recordings
#  -- wmm
#     -- [lib]
#         -- [wiremock.jar]
#     -- [logs]
#         -- [services]
#         -- [recordings]
#
# if services or recordings is missing, directory structure is 'invalid'
# if [wmm/lib] or [wmm/logs] is missing, directory structure is 'uninitialized'
#
# create_at will create 'services' and 'recordings' directories in the given path
#
# intialize_at will create 'libs' (if missing) and download wiremock, and create 'logs' (if missing)
import os
import urllib2
from wiremockmanager import config


def get_dir_for_service(api, version):
    service_dir = config.Config.get('workspace', 'SERVICE_DIR')
    return '{}/{}/{}'.format(service_dir, api, version)


def get_dir_for_recording(name, version):
    recordings_dir = config.Config.get('workspace', 'RECORDINGS_DIR')
    this_dir = '{}/{}/{}'.format(recordings_dir, name, version)
    if not os.path.exists(this_dir):
        os.makedirs(this_dir)
    return this_dir


def get_log_file_location_for(api, version):
    logs_dir = config.Config.get('workspace', 'LOG_DIR')
    this_log_dir = '{}/{}/{}/'.format(logs_dir, api, version)
    if not (os.path.exists(this_log_dir)):
        os.makedirs(this_log_dir)
    log_name = 'wiremock.log'  # for now...
    return this_log_dir + log_name


def is_valid_directory_structure():
    services_dir = config.Config.get('workspace', 'SERVICE_DIR')
    recordings_dir = config.Config.get('workspace', 'RECORDINGS_DIR')
    return os.path.exists(services_dir) and os.path.exists(recordings_dir)


def is_initialized():
    logs_dir = config.Config.get('workspace', 'LOG_DIR')
    wiremock_jar = config.Config.get('workspace', 'WIREMOCK_JAR')
    return os.path.exists(logs_dir) and os.path.exists(wiremock_jar)


def create_valid_directory_structure():
    print('Creating WMM directory structure...')
    required_dirs = [config.Config.get('workspace', 'SERVICE_DIR'), config.Config.get('workspace', 'RECORDINGS_DIR')]
    for req_dir in required_dirs:
        if not os.path.exists(req_dir):
            os.makedirs(req_dir)


def initialize():
    print('Initializing directory for wmm usage...')
    logs_dir = config.Config.get('workspace', 'LOG_DIR')
    path_to_wm_jar = config.Config.get('workspace', 'WIREMOCK_JAR_PATH')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    if not os.path.exists(path_to_wm_jar):
        _download_wiremock()


def _download_wiremock():
    wiremock_download_url = config.Config.get('workspace', 'WM_JAR_URL')
    libs_dir = config.Config.get('workspace', 'LIB_DIR')
    wiremock_jar_name = config.Config.get('workspace', 'WM_JAR_NAME')
    path_to_wm_jar = config.Config.get('workspace', 'WIREMOCK_JAR_PATH')
    if not os.path.exists(libs_dir):
        os.makedirs(libs_dir)
    download_request = urllib2.urlopen(wiremock_download_url)
    with open(path_to_wm_jar, 'wb') as wiremock_jar_file:
        file_size = int(download_request.info().getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (wiremock_jar_name, file_size)

        downloaded_data_length = 0
        block_size = 8192
        while True:
            next_data_block = download_request.read(block_size)
            if not next_data_block:
                break

            downloaded_data_length += len(next_data_block)
            wiremock_jar_file.write(next_data_block)
            status = r"%10d  [%3.2f%%]" % (downloaded_data_length, downloaded_data_length * 100. / file_size)
            status += chr(8) * (len(status) + 1)
            print status,
