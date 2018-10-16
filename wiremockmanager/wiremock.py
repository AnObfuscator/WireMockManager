import os
import psutil
import time
import wiremockmanager.configuration


def start_mocking(playback_dir, log_file_location, port, https_port, https_keystore, keystore_password):
    mock_extensions = []
    mock_extensions.append('--port={}'.format(str(port)))
    mock_extensions.append('--https-port={}'.format(str(https_port)))
    mock_extensions.append('--root-dir={}'.format(playback_dir))
    if https_keystore:
        mock_extensions.append('--https-keystore={}'.format(https_keystore))
    if keystore_password:
        mock_extensions.append('--keystore-password={}'.format(keystore_password))

    return _run_wiremock(log_file_location, mock_extensions)


def start_recording(recording_dir, log_file_location, port, https_port, url, https_keystore, keystore_password):
    rec_extensions = []
    rec_extensions.append('--port={}'.format(str(port)))
    rec_extensions.append('--https-port={}'.format(str(https_port)))
    rec_extensions.append('--root-dir={}'.format(recording_dir))
    rec_extensions.append('--proxy-all={}'.format(url))
    if https_keystore:
        rec_extensions.append('--https-keystore={}'.format(https_keystore))
    if keystore_password:
        rec_extensions.append('--keystore-password={}'.format(keystore_password))
    rec_extensions.append('--record-mappings')
    return _run_wiremock(log_file_location, rec_extensions)


def _run_wiremock(log_file_location, extensions):
    log_file = open(log_file_location, mode='a')
    log_file_start_size = os.path.getsize(log_file_location)

    config = wiremockmanager.configuration.get()
    base_cmd_array = ['java', '-jar', config.WIREMOCK_JAR_PATH, '--verbose']
    cmd_array = base_cmd_array + extensions
    wm_proc = psutil.Popen(cmd_array, stdout=log_file, stderr=log_file)

    while log_file_start_size == os.path.getsize(log_file_location):
        time.sleep(1)  # wait for WireMock to write something to the log file

    # Note: wm_proc.is_running() returns true, even if proc is zombie
    valid_process_state = wm_proc.status() == 'running' or wm_proc.status() == 'sleeping'
    if not valid_process_state:
        raise WireMockError(log_file_location)
    return WireMockInstance(wm_proc)


def get_instances():
    instances = []
    for proc in psutil.process_iter():
        try:
            pcmd = proc.cmdline()
            if pcmd[2] and pcmd[2].find("wiremock") >= 0:
                instances.append(WireMockInstance(proc))
        except: # yeah yeah shut up
            pass
    return instances


class WireMockInstance:
    def __init__(self, proc):
        self._proc = proc

    def terminate(self):
        self._proc.terminate()

    def as_dict(self):
        return self._extract_params()

    def as_list(self):
        inst_data = self._extract_params()
        inst_list = [inst_data['type'], inst_data['name'], inst_data['version'], 'Running', inst_data['port'],
                     inst_data['tls_port']]
        return inst_list

    def __str__(self):
        return str(self._extract_params())

    def _extract_params(self):
        params = {}
        arg_list = self._proc.cmdline()
        params['port'] = arg_list[4].split('=')[1]
        params['tls_port'] = arg_list[5].split('=')[1]
        dir_as_array = arg_list[6].split('=')[1].split('/')
        params['type'] = 'Mock' if dir_as_array[-3] == 'services' else 'Record'
        params['name'] = dir_as_array[-2]
        params['version'] = dir_as_array[-1]
        return params


class WireMockError(Exception):
    pass