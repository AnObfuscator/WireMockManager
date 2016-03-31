import argh
import time
from wiremockmanager import workspace
from wiremockmanager import wiremock

from tabulate import tabulate


def validate_directory(func):
    def wrapper(**kwargs):
        if workspace.is_valid_directory_structure():
            return func(**kwargs)
        else:
            print("Current directory does not appear to be a valid WMM working directory.")
    return wrapper


def initialize_directory(func):
    def wrapper(**kwargs):
        if not workspace.is_initialized():
            workspace.initialize()
        return func(**kwargs)
    return wrapper

@argh.decorators.named('mock')
@argh.arg('--api', default='', help='API folder name')
@argh.arg('--version', default='', help='Version folder name')
@argh.arg('--port', default=0, help='HTTP port to use')
@argh.arg('--https-port', default=0, help='HTTPS port to use')
@validate_directory
@initialize_directory
def mock(api, version, port, https_port):
    """
    Start an instance to mock of the specified API and version. This will serve the defined behaviors located in the
    directory 'services/[api]/[version]'.
    """
    playback_dir = workspace.get_dir_for_service(api, version)
    log_file_location = workspace.get_log_file_location_for(api, version)
    print(log_file_location)
    try:
        instance = wiremock.start_mocking(playback_dir, log_file_location, port, https_port)
        _print_table([instance])
    except wiremock.WireMockError as wme:
        print("Could not start WireMock instance. Please see log file for more details: {}".format(wme.message))


@argh.decorators.named('record')
@argh.arg('--port', default=0, help='HTTP port to use')
@argh.arg('--https-port', default=0, help='HTTPS port to use')
@argh.arg('--url', default='', help='URL to proxy')
@argh.arg('--name', default='unknown', help='name of recorded API')
@argh.arg('--version', default=None, help='Version of recorded API')
@validate_directory
@initialize_directory
def record(port, https_port, url, name, version):
    """
    Start an instance to record the calls to the specified URL. The recorded interactions will be stored in the
    directory 'recordings/[name]/[version].
    """
    if not version:
        version = time.time()
    rec_dir = workspace.get_dir_for_recording(name, version)
    log_file_location = workspace.get_log_file_location_for(name, version)
    try:
        instance = wiremock.start_recording(rec_dir, log_file_location, port, https_port, url)
        _print_table([instance])
    except wiremock.WireMockError as wme:
        print("Could not start WireMock instance. Please see log file for more details: {}".format(wme.message))


@argh.decorators.named('stop')
@validate_directory
@initialize_directory
def stop():
    """
    Stop all running instances.
    """
    instances = wiremock.get_instances()
    for proc in instances:
        proc.terminate()

@argh.decorators.named('status')
@validate_directory
@initialize_directory
def status():
    """
    List all running instances.
    """
    instances = wiremock.get_instances()
    if instances:
        _print_table(instances)
    else:
        print("No running instances.")

@argh.decorators.named('setup')
def setup_wmm_in_pwd():
    """
    Setup WMM folder structure in the current directory.

    Specifically, this will create directories called 'services' and 'recordings', if they are missing. In addition,
    this will create directories 'wmm/logs' and 'wmm/libs'. If the WireMock jar is not in 'wmm/libs', this will
    download the WM jar into that directory.
    """
    if not workspace.is_valid_directory_structure():
        workspace.create_valid_directory_structure()
    if not workspace.is_initialized():
        workspace.initialize()
    print('Current workspace is initialized')


def _print_table(instance_list):
    instance_table = []
    for instance in instance_list:
        instance_row = instance.as_list()
        instance_table.append(instance_row)
    table_header = ['Type', 'Name', 'Version', 'Status', 'Port', 'TLS Port']
    print(tabulate(instance_table, headers=table_header))


def main():
    parser = argh.ArghParser()
    parser.add_commands([record, mock, stop, status, setup_wmm_in_pwd])
    parser.dispatch()

if __name__ == '__main__':
    main()
