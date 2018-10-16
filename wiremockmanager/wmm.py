import argh
import time
import yaml
from wiremockmanager import workspace
from wiremockmanager import wiremock

from tabulate import tabulate


def validate_directory(func):
    def wrapper(**kwargs):
        if workspace.is_valid_directory_structure():
            return func(**kwargs)
        else:
            _print_message("Current directory does not appear to be a valid WMM working directory.")
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
@argh.arg('--https-keystore', default='', help='keystore file containing an SSL certificate')
@argh.arg('--keystore-password', default='', help='Password to the keystore, if something other than password.')
@validate_directory
@initialize_directory
def mock(api, version, port, https_port, https_keystore=None, keystore_password=None):
    """
    Start an instance to mock of the specified API and version. This will serve the defined behaviors located in the
    directory 'services/[api]/[version]'.

    If 'services/[api]/[version]' does not exist, this command will return with an error.
    """
    try:
        instance = _mock(api, version, port, https_port, https_keystore, keystore_password)
        _print_table([instance])
    except workspace.WorkspaceError as wse:
        _print_message(wse.message)
    except wiremock.WireMockError as wme:
        _print_message("Could not start WireMock instance. Please see log file for more details: {}".format(wme.message))


def _mock(api, version, port, https_port, https_keystore, keystore_password):
    playback_dir = workspace.get_dir_for_service(api, version)
    log_file_location = workspace.get_log_file_location_for(api, version)
    instance = wiremock.start_mocking(playback_dir, log_file_location, port, https_port, https_keystore,
                                      keystore_password)
    return instance


@argh.decorators.named('record')
@argh.arg('--url', default='', help='URL to proxy')
@argh.arg('--name', default='unknown', help='name of recorded API')
@argh.arg('--version', default=None, help='Version of recorded API')
@argh.arg('--port', default=0, help='HTTP port to use')
@argh.arg('--https-port', default=0, help='HTTPS port to use')
@argh.arg('--https-keystore', default='', help='keystore file containing an SSL certificate')
@argh.arg('--keystore-password', default='', help='Password to the keystore, if something other than password.')
@validate_directory
@initialize_directory
def record(url, name, version, port, https_port, https_keystore=None, keystore_password=None):
    """
    Start an instance to record the calls to the specified URL. The recorded interactions will be stored in the
    directory 'recordings/[name]/[version].

    *Warning:* If 'recordings/[name]/[version]' already exists, some existing content may be overwritten.
    """
    try:
        instance = _record(url, name, version, port, https_port, https_keystore, keystore_password)
        _print_table([instance])
    except wiremock.WireMockError as wme:
        _print_message("Could not start WireMock instance. Please see log file for more details: {}"
                       .format(wme.message))


def _record(url, name, version, port, https_port, https_keystore, keystore_password):
    if not version:
        version = time.time()
    rec_dir = workspace.get_dir_for_recording(name, version)
    log_file_location = workspace.get_log_file_location_for(name, version)
    instance = wiremock.start_recording(rec_dir, log_file_location, port, https_port, url, https_keystore,
                                        keystore_password)
    return instance


@argh.decorators.named('start-group')
@argh.arg('--group-file', default='', help='')
@validate_directory
@initialize_directory
def start_group(group_file):
    """
    Start all instances of wiremock as defined in the yaml group file.

    :param group_file:
    """
    group = None
    with open(group_file) as gf:
        group = yaml.safe_load(gf)
    instances = []
    for name in group:
        wmm_def = group[name]
        if wmm_def['type'] == 'mock':
            print("starting mock for {}".format(name))
            instance = _mock(wmm_def['api'], wmm_def['version'], wmm_def['port'], wmm_def['https-port'],
                             wmm_def.get('https-keystore', None),
                             wmm_def.get('keystore-password', None))
            instances.append(instance)
        elif wmm_def['type'] == 'record':
            print("starting record for {}".format(name))
            instance = _record(wmm_def['url'], wmm_def['name'], wmm_def['version'], wmm_def['port'],
                               wmm_def['https-port'],
                               wmm_def.get('https-keystore', None),
                               wmm_def.get('keystore-password', None))
            instances.append(instance)
        else:
            _print_message("Could not start {}: invalid type.".format(name))

    _print_table(instances)


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
    List all running instances as a table, with type (record/mock), api, version, url (if recording), port,
    and https port.
    """
    instances = wiremock.get_instances()
    if instances:
        _print_table(instances)
    else:
        _print_message("No running instances.")


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
    _print_message('Current workspace is setup and initialized')


def _print_table(instance_list):
    instance_table = []
    for instance in instance_list:
        instance_row = instance.as_list()
        instance_table.append(instance_row)
    table_header = ['Type', 'Name', 'Version', 'Status', 'Port', 'TLS Port']
    print(tabulate(instance_table, headers=table_header))


def _print_message(message):
    print(message)


def main():
    parser = argh.ArghParser()
    parser.add_commands([record, mock, start_group, stop, status, setup_wmm_in_pwd])
    parser.dispatch()


if __name__ == '__main__':
    main()
