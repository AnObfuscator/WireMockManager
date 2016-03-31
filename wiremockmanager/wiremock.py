import psutil
import time


base_cmd_array = ['java', '-jar', 'wiremock-1.57-standalone.jar', '--verbose']


def start_mocking(playback_dir, log_file_location, port, https_port):
    run_extensions = ['--port='+str(port), '--https-port='+str(https_port), '--root-dir='+playback_dir]
    instance = _run_wiremock(playback_dir, log_file_location, run_extensions)
    return instance


def start_recording(recording_dir, log_file_location, port, https_port, url):
    rec_extensions = ['--port='+str(port), '--https-port='+str(https_port), '--root-dir='+recording_dir,
                      '--proxy-all='+url, '--record-mappings']
    instance = _run_wiremock(recording_dir, log_file_location, rec_extensions)
    return instance


def _run_wiremock(dir, log_name, extensions):
    log_file_location = log_name  # '{}/{}'.format(dir, log_name)
    log_file = open(log_file_location, mode='a')
    cmd_array = base_cmd_array + extensions
    wm_proc = psutil.Popen(cmd_array, stdout=log_file, stderr=log_file)
    time.sleep(1)  # yeah yeah, I know... I know...
    if not wm_proc.status() == 'running':  # wm_proc.is_running() returns true, even if proc is zombie
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
        params['type'] = 'Mock' if dir_as_array[0] == 'services' else 'Record'
        params['name'] = dir_as_array[1]
        params['version'] = dir_as_array[2]
        return params


class WireMockError(Exception):
    pass