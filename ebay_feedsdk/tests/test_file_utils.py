import unittest
import os
import shutil
from utils import file_utils
from enums.file_enums import FileFormat
from errors.custom_exceptions import FileCreationError, InputDataError
from constants.feed_constants import SANDBOX_CHUNK_SIZE


class TestFileUtils(unittest.TestCase):
    def test_append_response_to_file(self):
        test_binary_data = b'\x01\x02\x03\x04'
        test_file_path = '../tests/test-data/testFile1'
        try:
            with open(test_file_path, 'wb') as file_obj:
                # create and append to the file
                file_utils.append_response_to_file(file_obj, test_binary_data)
        except (IOError, FileCreationError) as exp:
            # clean up
            if os.path.isfile(test_file_path):
                os.remove(test_file_path)
            self.fail(repr(exp))
        # verify that the file is created
        self.assertTrue(os.path.isfile(test_file_path), 'test file has not been created')
        # verify that file size is not zero
        self.assertTrue(os.path.getsize(test_file_path) > 0, 'the test file is empty')
        # clean up
        os.remove(test_file_path)

    def test_append_response_to_file_exception(self):
        with self.assertRaises(FileCreationError):
            file_utils.append_response_to_file(None, b'\x01')

    def test_create_and_replace_binary_file_none(self):
        with self.assertRaises(FileCreationError):
            file_utils.create_and_replace_binary_file(None)

    def test_create_and_replace_binary_file_dir(self):
        with self.assertRaises(FileCreationError):
            test_dir = os.path.expanduser('~/Desktop')
            file_utils.create_and_replace_binary_file(test_dir)

    def test_create_and_replace_binary_file_exists(self):
        test_binary_data = b'\x01\x02\x03\x04'
        test_file_path = '../tests/test-data/testFile2'
        with open(test_file_path, 'wb') as file_obj:
            file_obj.write(test_binary_data)
        # verify that the file is created
        self.assertTrue(os.path.isfile(test_file_path), 'test file has not been created')
        # verify that file size is not zero
        self.assertTrue(os.path.getsize(test_file_path) > 0, 'the test file is empty')
        # create and replace
        file_utils.create_and_replace_binary_file(test_file_path)
        # verify that the file is created
        self.assertTrue(os.path.isfile(test_file_path), 'test file has not been created')
        # verify that file size is zero
        self.assertEqual(os.path.getsize(test_file_path),  0)
        # clean up
        os.remove(test_file_path)

    def test_create_and_replace_binary_file_not_exists(self):
        test_dir_to_be_created = '../tests/test-data/testDir'
        test_file_path = os.path.join(test_dir_to_be_created, 'testFile3')
        self.assertFalse(os.path.isfile(test_file_path), 'test file exists')
        # create and replace
        file_utils.create_and_replace_binary_file(test_file_path)
        # verify that the file is created
        self.assertTrue(os.path.isfile(test_file_path), 'test file has not been created')
        # verify that file size is zero
        self.assertEqual(os.path.getsize(test_file_path),  0)
        # clean up
        shutil.rmtree(test_dir_to_be_created)

    def test_find_next_range_none_range_header(self):
        next_range = file_utils.find_next_range(None, 100)
        self.assertEqual(next_range, 'bytes=0-100')

    def test_find_next_range_none_chunk(self):
        next_range = file_utils.find_next_range('0-1000/718182376', None)
        self.assertEqual(next_range, 'bytes=1001-%s' % (SANDBOX_CHUNK_SIZE + 1001))

    def test_find_next_range(self):
        next_range = file_utils.find_next_range('1001-2001/718182376', 1000)
        self.assertEqual(next_range, 'bytes=2002-3002')

    def test_get_file_extension_none(self):
        ext = file_utils.get_extension(None)
        self.assertEqual(ext, '')

    def test_get_file_extension(self):
        ext = file_utils.get_extension(FileFormat.GZIP.value)
        self.assertEqual(ext, '.gz')

    def test_get_file_name_dir(self):
        test_dir = os.path.expanduser('../feed-sdk/tests')
        returned_dir_name = file_utils.get_file_name(test_dir)
        self.assertEqual(returned_dir_name, 'tests')

    def test_get_file_name(self):
        test_dir = os.path.expanduser('../feed-sdk/tests/test_json')
        returned_file_name = file_utils.get_file_name(test_dir)
        self.assertEqual(returned_file_name, 'test_json')

    def test_get_file_name_none(self):
        with self.assertRaises(InputDataError):
            file_utils.get_file_name(None)

    def test_get_file_name_name(self):
        test_file_name = 'abc.txt'
        self.assertEqual(file_utils.get_file_name(test_file_name), test_file_name)

    def test_read_json(self):
        json_obj = file_utils.read_json('../tests/test-data/test_json')
        self.assertIsNotNone(json_obj)
        self.assertIsNotNone(json_obj.get('requests'))


if __name__ == '__main__':
    unittest.main()
