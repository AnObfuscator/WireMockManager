import os
import urllib2
import wiremockmanager.configuration


def get_dir_for_service(api, version):
    config = wiremockmanager.configuration.get()
    service_dir = os.path.join(config.SERVICES_DIR, str(api), str(version))
    if not os.path.exists(service_dir):
        raise WorkspaceError('Could not find definition for {} {}'.format(api, version))
    return service_dir


def get_dir_for_recording(name, version):
    config = wiremockmanager.configuration.get()
    this_dir = os.path.join(config.RECORDINGS_DIR, str(name), str(version))
    if not os.path.exists(this_dir):
        os.makedirs(this_dir)
    return this_dir


def get_log_file_location_for(api, version):
    config = wiremockmanager.configuration.get()
    this_log_dir = os.path.join(config.LOG_DIR, str(api), str(version))
    if not (os.path.exists(this_log_dir)):
        os.makedirs(this_log_dir)
    log_name = 'wiremock.log'
    return os.path.join(this_log_dir, log_name)


def is_valid_directory_structure():
    config = wiremockmanager.configuration.get()
    return os.path.exists(config.SERVICES_DIR) and os.path.exists(config.RECORDINGS_DIR)


def is_initialized():
    config = wiremockmanager.configuration.get()
    return os.path.exists(config.LOG_DIR) and os.path.exists(config.WIREMOCK_JAR_PATH)


def create_valid_directory_structure():
    print('Creating WMM directory structure...')
    config = wiremockmanager.configuration.get()
    required_dirs = [config.SERVICES_DIR, config.RECORDINGS_DIR]
    for req_dir in required_dirs:
        if not os.path.exists(req_dir):
            os.makedirs(req_dir)


def initialize():
    print('Initializing directory for wmm usage...')
    config = wiremockmanager.configuration.get()
    if not os.path.exists(config.LOG_DIR):
        os.makedirs(config.LOG_DIR)
    if not os.path.exists(config.WIREMOCK_JAR_PATH):
        _download_wiremock()


def _download_wiremock():
    config = wiremockmanager.configuration.get()
    if not os.path.exists(config.LIB_DIR):
        os.makedirs(config.LIB_DIR)
    download_request = urllib2.urlopen(config.WM_JAR_URL)
    with open(config.WIREMOCK_JAR_PATH, 'wb') as wiremock_jar_file:
        file_size = int(download_request.info().getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (config.WM_JAR_NAME, file_size)

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


class WorkspaceError(Exception):
    pass