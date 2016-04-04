import unittest
import mock
import wiremockmanager.wmm as wmm


class WmmSetupTest(unittest.TestCase):

    def _setup_mocks(self, workspace_mock):
        # mock methods
        workspace_mock.is_valid_directory_structure = mock.Mock()
        workspace_mock.is_initialized = mock.Mock()
        workspace_mock.initialize = mock.Mock()
        workspace_mock.create_valid_directory_structure = mock.Mock()

        # mock default return values
        workspace_mock.is_valid_directory_structure.return_value = False
        workspace_mock.is_initialized.return_value = False

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_creates_and_initializes_and_prints(self, print_msg_mock, workspace_mock):
        self._setup_mocks(workspace_mock)

        wmm.setup_wmm_in_pwd()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.create_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_called_once()
        print_msg_mock.assert_called_once_with('Current workspace is setup and initialized')

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_creates_without_initializing_and_prints(self, print_msg_mock, workspace_mock):
        self._setup_mocks(workspace_mock)
        workspace_mock.is_initialized.return_value = True

        wmm.setup_wmm_in_pwd()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.create_valid_directory_structure.assert_called_once()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        print_msg_mock.assert_called_once_with('Current workspace is setup and initialized')

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_does_not_create_does_initialize_and_prints(self, print_msg_mock, workspace_mock):
        self._setup_mocks(workspace_mock)
        workspace_mock.is_valid_directory_structure.return_value = True

        wmm.setup_wmm_in_pwd()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.create_valid_directory_structure.assert_not_called()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_called_once()
        print_msg_mock.assert_called_once_with('Current workspace is setup and initialized')

    @mock.patch('wiremockmanager.wmm.workspace')
    @mock.patch('wiremockmanager.wmm._print_message')
    def test_does_nothing_and_prints(self, print_msg_mock, workspace_mock):
        self._setup_mocks(workspace_mock)
        workspace_mock.is_initialized.return_value = True
        workspace_mock.is_valid_directory_structure.return_value = True

        wmm.setup_wmm_in_pwd()

        workspace_mock.is_valid_directory_structure.assert_called_once()
        workspace_mock.create_valid_directory_structure.assert_not_called()
        workspace_mock.is_initialized.assert_called_once()
        workspace_mock.initialize.assert_not_called()
        print_msg_mock.assert_called_once_with('Current workspace is setup and initialized')
