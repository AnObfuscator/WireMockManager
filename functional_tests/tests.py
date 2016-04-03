from test_helpers import *
from wiremockmanager import config


def setup_for_tests():
    create_and_set_working_dir('wmm_test_dir')
    stop_running_wiremocks()


def wmm_uninitialized_status_should_return_uninitialized_error():
    result = run_command(["wmm", "status"])
    expected = 'Current directory does not appear to be a valid WMM working directory.\n'
    assert_equal(expected, result)


def wmm_setup_should_download_wm_and_create_directories():
    result = run_command(['wmm', 'setup'])

    expected_start = 'Creating WMM directory structure...\nInitializing directory for wmm usage...\nDownloading: wiremock-1.57-standalone.jar Bytes: 6935826'
    expected_end = 'Current workspace is setup and initialized\n'

    assert result.startswith(expected_start)
    assert result.endswith(expected_end)
    assert os.path.exists(config.WIREMOCK_JAR_PATH)
    assert os.path.exists(config.LOG_DIR)
    assert os.path.exists(config.SERVICES_DIR)
    assert os.path.exists(config.RECORDINGS_DIR)


def wmm_initialized_status_should_show_no_running_instances():
    result = run_command(["wmm", "status"])
    expected = 'No running instances.\n'
    assert_equal(expected, result)


def wmm_record_1_should_start_and_create_log():
    result = run_command(['wmm', 'record', '--url=http://example.com', '--port=7890', '--https-port=7891', '--name=test', '--version=1'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Record  test            1  Running     7890        7891\n'

    log_file_path = os.path.join('wmm', 'logs', 'test', '1', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_record_2_should_start_and_create_log():
    result = run_command(['wmm', 'record', '--url=http://example.com', '--port=7892', '--https-port=7893', '--name=test', '--version=2'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Record  test            2  Running     7892        7893\n'

    log_file_path = os.path.join('wmm', 'logs', 'test', '2', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_record_3_should_fail():
    result = run_command(['wmm', 'record', '--url=http://example.com', '--port=7892', '--https-port=7893', '--name=test', '--version=3'])

    expected = 'Could not start WireMock instance. Please see log file for more details: wmm/logs/test/3/wiremock.log\n'

    log_file_path = os.path.join('wmm', 'logs', 'test', '3', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_mock_1_should_start_and_create_log():
    make_service_dir('sample', '1')

    result = run_command(['wmm', 'mock', '--port=7894', '--https-port=7895', '--api=sample', '--version=1'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Mock    sample          1  Running     7894        7895\n'

    log_file_path = os.path.join('wmm', 'logs', 'sample', '1', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_mock_2_should_start_and_create_log():
    make_service_dir('sample', '2')

    result = run_command(['wmm', 'mock', '--port=7896', '--https-port=7897', '--api=sample', '--version=2'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Mock    sample          2  Running     7896        7897\n'

    log_file_path = os.path.join('wmm', 'logs', 'sample', '2', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_mock_3_should_fail():
    make_service_dir('sample', '3')

    result = run_command(['wmm', 'mock', '--port=7896', '--https-port=7897', '--api=sample', '--version=3'])

    expected = 'Could not start WireMock instance. Please see log file for more details: wmm/logs/sample/3/wiremock.log\n'

    log_file_path = os.path.join('wmm', 'logs', 'sample', '3', 'wiremock.log')

    assert os.path.exists(log_file_path)
    assert_equal(expected, result)


def wmm_status_should_print_4_services():
    result = run_command(['wmm', 'status'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Record  test            1  Running     7890        7891\n' + \
               'Record  test            2  Running     7892        7893\n' + \
               'Mock    sample          1  Running     7894        7895\n' + \
               'Mock    sample          2  Running     7896        7897\n'

    assert_equal(expected, result)


def wmm_stop_should_terminate_all():
    run_command(['wmm', 'stop'])
    # TODO figure out how to create an assertion that avoids this race condition
    result = count_running_wiremocks()
    # assert result == 0


if __name__ == '__main__':
    setup_for_tests()

    wmm_uninitialized_status_should_return_uninitialized_error()
    wmm_setup_should_download_wm_and_create_directories()
    wmm_initialized_status_should_show_no_running_instances()

    wmm_record_1_should_start_and_create_log()
    wmm_record_2_should_start_and_create_log()
    wmm_record_3_should_fail()

    wmm_mock_1_should_start_and_create_log()
    wmm_mock_2_should_start_and_create_log()
    wmm_mock_3_should_fail()

    wmm_status_should_print_4_services()

    wmm_stop_should_terminate_all()
    #wmm_initialized_status_should_show_no_running_instances()

    stop_running_wiremocks()
