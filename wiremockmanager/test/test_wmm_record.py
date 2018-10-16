import unittest
import mock
import wiremockmanager.wmm as wmm
from wiremockmanager.workspace import WorkspaceError
from wiremockmanager.wiremock import WireMockError


class WmmRecordTest(unittest.TestCase):

    def _setup_mocks(self, workspace_mock, wiremock_mock):
        # mock methods
        workspace_mock.is_valid_directory_structure = mock.Mock()
        workspace_mock.is_initialized = mock.Mock()
        workspace_mock.initialize = mock.Mock()
        workspace_mock.get_dir_for_recording = mock.Mock()
        workspace_mock.get_log_file_location_for = mock.Mock()
        wiremock_mock.start_recording = mock.Mock()

        # preserve exception classes
        workspace_mock.WorkspaceError = WorkspaceError
        wiremock_mock.WireMockError = WireMockError

        # mock default return values
        workspace_mock.is_valid_directory_structure.return_value = True
        workspace_mock.is_initialized.return_value = True
        workspace_mock.get_dir_for_recording.return_value = "recording/dir"
        workspace_mock.get_log_file_location_for.return_value = "some/log/file.log"
        wiremock_mock.start_recording.return_value = object()

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_starts_wiremock_and_prints_instance(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)

        wmm.record(url='http://some.url/', name='test-api', version='test-version', port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        workspace_mock.get_dir_for_recording.assert_called_once_with('test-api', 'test-version')
        workspace_mock.get_log_file_location_for.assert_called_once_with('test-api', 'test-version')
        wiremock_mock.start_recording.assert_called_once_with('recording/dir', 'some/log/file.log', 1234, 5678, 'http://some.url/', None, None)
        print_table_mock.assert_called_once()
        print_msg_mock.assert_not_called()

    @mock.patch('wiremockmanager.wmm.time')
    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_starts_wiremock_with_time_as_version_and_prints_instance(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock, time_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        time_mock.time = mock.Mock(return_value=111111)

        wmm.record(url='http://some.url/', name='test-api', version=None, port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        workspace_mock.get_dir_for_recording.assert_called_once_with('test-api', 111111)
        workspace_mock.get_log_file_location_for.assert_called_once_with('test-api', 111111)
        wiremock_mock.start_recording.assert_called_once_with('recording/dir', 'some/log/file.log', 1234, 5678, 'http://some.url/', None, None)
        print_table_mock.assert_called_once()
        print_msg_mock.assert_not_called()

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_starts_wiremock_with_unknown_name_and_prints_instance(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)

        wmm.record(url='http://some.url/', name=None, version='test-version', port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        workspace_mock.get_dir_for_recording.assert_called_once_with(None, 'test-version')
        workspace_mock.get_log_file_location_for.assert_called_once_with(None, 'test-version')
        wiremock_mock.start_recording.assert_called_once_with('recording/dir', 'some/log/file.log', 1234, 5678, 'http://some.url/', None, None)
        print_table_mock.assert_called_once()
        print_msg_mock.assert_not_called()

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_for_wiremock_failure_prints_error_and_exits(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        wiremock_mock.start_recording.side_effect = WireMockError('error.log')

        wmm.record(url='http://some.url/', name='test-api', version='test-version', port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        workspace_mock.get_dir_for_recording.assert_called_once_with('test-api', 'test-version')
        workspace_mock.get_log_file_location_for.assert_called_once_with('test-api', 'test-version')
        wiremock_mock.start_recording.assert_called_once_with('recording/dir', 'some/log/file.log', 1234, 5678, 'http://some.url/', None, None)
        print_table_mock.assert_not_called()
        print_msg_mock.assert_called_once_with('Could not start WireMock instance. Please see log file for more details: {}'.format('error.log'))

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_invalid_directory_prints_error_and_exits(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        workspace_mock.is_valid_directory_structure.return_value = False

        wmm.record(url='http://some.url/', name='test-api', version='test-version', port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_not_called()
        workspace_mock.initialize.assert_not_called()
        workspace_mock.get_dir_for_recording.assert_not_called()
        workspace_mock.get_log_file_location_for.assert_not_called()
        wiremock_mock.start_recording.assert_not_called()
        print_table_mock.assert_not_called()
        print_msg_mock.assert_called_once_with('Current directory does not appear to be a valid WMM working directory.')

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_uninitialized_directory_calls_initialize_and_continues(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        workspace_mock.is_initialized.return_value = False

        wmm.record(url='http://some.url/', name='test-api', version='test-version', port=1234, https_port=5678)

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_called_once()
        workspace_mock.get_dir_for_recording.assert_called_once_with('test-api', 'test-version')
        workspace_mock.get_log_file_location_for.assert_called_once_with('test-api', 'test-version')
        wiremock_mock.start_recording.assert_called_once_with('recording/dir', 'some/log/file.log', 1234, 5678, 'http://some.url/', None, None)
        print_table_mock.assert_called_once()
        print_msg_mock.assert_not_called()