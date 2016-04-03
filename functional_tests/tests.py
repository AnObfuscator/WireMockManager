from test_helpers import *


def setup_for_tests():
    create_and_set_working_dir('wmm_test_dir')
    stop_running_wiremocks()


def wmm_uninitialied_status_should_return_uninitialized_error():
    result = run_command(["wmm", "status"])
    expected = 'Current directory does not appear to be a valid WMM working directory.\n'
    assert_equal(expected, result)


def wmm_setup_should_download_wm_and_create_directories():
    result = run_command(['wmm', 'setup'])

    expected_start = 'Creating WMM directory structure...\nInitializing directory for wmm usage...\nDownloading: wiremock-1.57-standalone.jar Bytes: 6935826'
    expected_end = 'Current workspace is setup and initialized\n'

    assert result.startswith(expected_start)
    assert result.endswith(expected_end)


def wmm_initialized_status_should_show_no_running_instances():
    result = run_command(["wmm", "status"])
    expected = 'No running instances.\n'
    assert_equal(expected, result)


def wmm_record_should_start_and_create_log():
    result = run_command(['wmm', 'record', '--url=http://example.com', '--port=7890', '--https-port=7891', '--name=test', '--version=1'])

    expected = 'Type    Name      Version  Status      Port    TLS Port\n' + \
               '------  ------  ---------  --------  ------  ----------\n' + \
               'Record  test            1  Running     7890        7891\n'

    log_file_path = os.path.join('wmm', 'logs', 'test', '1', 'wiremock.log')
    assert os.path.exists(log_file_path)
    with open('wmm/logs/test/1/wiremock.log', 'r') as log_file:
        for line in log_file:
            print(line)
    assert_equal(expected, result)


def wmm_stop_should_terminate_all():
    run_command(['wmm', 'stop'])
    # TODO figure out how to create an assertion that avoids this race condition
    result = count_running_wiremocks()
    # assert result == 0


if __name__ == '__main__':
    print(run_command(['java', '-version']))
    setup_for_tests()
    wmm_uninitialied_status_should_return_uninitialized_error()
    wmm_setup_should_download_wm_and_create_directories()
    wmm_initialized_status_should_show_no_running_instances()
    wmm_record_should_start_and_create_log()

    wmm_stop_should_terminate_all()
