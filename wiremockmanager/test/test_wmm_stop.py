import unittest
import mock
import wiremockmanager.wmm as wmm
from wiremockmanager.workspace import WorkspaceError
from wiremockmanager.wiremock import WireMockError


class WmmStopTest(unittest.TestCase):

    def _setup_mocks(self, workspace_mock, wiremock_mock):
        # mock methods
        workspace_mock.is_valid_directory_structure = mock.Mock()
        workspace_mock.is_initialized = mock.Mock()
        workspace_mock.initialize = mock.Mock()
        wiremock_mock.get_instances = mock.Mock()

        # preserve exception classes
        workspace_mock.WorkspaceError = WorkspaceError
        wiremock_mock.WireMockError = WireMockError

        # mock default return values
        workspace_mock.is_valid_directory_structure.return_value = True
        workspace_mock.is_initialized.return_value = True
        wiremock_mock.get_instances.return_value = []

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_empty_instance_list_exits_cleanly(self, print_msg_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)

        wmm.stop()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        wiremock_mock.get_instances.assert_called_once()
        print_msg_mock.assert_not_called()


    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_terminates_each_instance_and_exits_cleanly(self, print_msg_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        mock_instances = [mock.Mock(), mock.Mock(), mock.Mock()]
        for mock_inst in mock_instances:
            mock_inst.terminate = mock.Mock()
        wiremock_mock.get_instances.return_value = mock_instances

        wmm.stop()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        wiremock_mock.get_instances.assert_called_once()
        print_msg_mock.assert_not_called()
        for mock_inst in mock_instances:
            mock_inst.terminate.assert_called_once()



    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_invalid_directory_prints_error_and_exits(self, print_msg_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        workspace_mock.is_valid_directory_structure.return_value = False

        wmm.stop()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_not_called()
        workspace_mock.initialize.assert_not_called()
        wiremock_mock.get_instances.assert_not_called()
        print_msg_mock.assert_called_once_with('Current directory does not appear to be a valid WMM working directory.')

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm.wiremock')
    @mock.patch('wiremockmanager.wmm._print_table')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_uninitialized_directory_calls_initialize_and_continues(self, print_msg_mock, print_table_mock, wiremock_mock, workspace_mock):
        self._setup_mocks(workspace_mock, wiremock_mock)
        workspace_mock.is_initialized.return_value = False

        wmm.stop()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_called_once()
        wiremock_mock.get_instances.assert_called_once()
        print_table_mock.assert_not_called()
        print_msg_mock.assert_not_called()
