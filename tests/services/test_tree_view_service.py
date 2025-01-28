import unittest
from unittest import TestCase
from unittest.mock import patch
from services.tree_view_service import TreeViewService

class TestTreeViewService(TestCase):
    def setUp(self):
        self.service = TreeViewService()

    @patch('services.treeviewservice.os.listdir')
    def test_list_directory(self, mock_listdir):
        mock_listdir.return_value = ['file.txt', 'dir1']
        result = self.service.list_directory('mock/path')
        self.assertEquals(result, mock_listdir.return_value)

if __name__ == '__main__':
    unittest.main()