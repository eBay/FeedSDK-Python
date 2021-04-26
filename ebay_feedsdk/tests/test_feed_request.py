import unittest
from os import remove
from os.path import isfile, getsize, split, abspath
from utils.date_utils import get_formatted_date
from enums.file_enums import FileFormat
from enums.feed_enums import FeedType, FeedScope, FeedPrefix, Environment
from feed.feed_request import Feed, DEFAULT_DOWNLOAD_LOCATION
from constants.feed_constants import SUCCESS_CODE, FAILURE_CODE, PROD_CHUNK_SIZE


class TestFeed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_token = 'Bearer v^1 ...'
        cls.test_category_1 = '1'
        cls.test_category_2 = '625'
        cls.test_marketplace = 'EBAY_US'
        cls.file_paths = []

    @classmethod
    def tearDownClass(cls):
        for file_path in cls.file_paths:
            if file_path and isfile(file_path):
                remove(file_path)

    def test_none_token(self):
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.BOOTSTRAP.value, '220', 'EBAY_US', None)
        get_response = feed_req_obj.get()
        self.assertEqual(get_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNone(get_response.file_path, 'file_path is not None in the response')

    def test_default_values(self):
        feed_req_obj = Feed(None, None, '220', 'EBAY_US', 'v^1 ...')
        self.assertEqual(feed_req_obj.feed_type, FeedType.ITEM.value)
        self.assertEqual(feed_req_obj.feed_scope, FeedScope.DAILY.value)
        self.assertTrue(feed_req_obj.token.startswith('Bearer'), 'Bearer is missing from token')
        self.assertEqual(feed_req_obj.feed_date, get_formatted_date(feed_req_obj.feed_type))
        self.assertEqual(feed_req_obj.environment, Environment.PRODUCTION.value)
        self.assertEqual(feed_req_obj.download_location, DEFAULT_DOWNLOAD_LOCATION)
        self.assertEqual(feed_req_obj.file_format, FileFormat.GZIP.value)

    def test_download_feed_invalid_path(self):
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.BOOTSTRAP.value, '220', 'EBAY_US', 'Bearer v^1 ...',
                            download_location='../tests/test-data/test_json')
        get_response = feed_req_obj.get()
        self.assertEqual(get_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNotNone(get_response.file_path, 'file_path is None in the response')

    def test_download_feed_invalid_date(self):
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.BOOTSTRAP.value, '220', 'EBAY_US', 'Bearer v^1 ...',
                            download_location='../tests/test-data/', feed_date='2019-02-01')
        get_response = feed_req_obj.get()
        self.assertEqual(get_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNotNone(get_response.file_path, 'file_path is None in the response')

    def test_download_feed_daily(self):
        test_date = get_formatted_date(FeedType.ITEM, -4)
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.DAILY.value, self.test_category_1,
                            self.test_marketplace, self.test_token, download_location='../tests/test-data/',
                            feed_date=test_date)
        get_response = feed_req_obj.get()
        # store the file path for clean up
        self.file_paths.append(get_response.file_path)
        # assert the result
        self.assertEqual(get_response.status_code, SUCCESS_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNotNone(get_response.file_path, 'file_path is None')
        self.assertTrue(isfile(get_response.file_path), 'file_path is not pointing to a file. file_path: %s'
                        % get_response.file_path)
        # check the file size and name
        self.assertTrue(getsize(get_response.file_path) > 0, 'feed file is empty. file_path: %s'
                        % get_response.file_path)
        self.assertTrue(FeedPrefix.DAILY.value in get_response.file_path,
                        'feed file name does not have %s in it. file_path: %s' %
                        (FeedPrefix.DAILY.value, get_response.file_path))
        file_dir, file_name = split(abspath(get_response.file_path))
        self.assertEqual(abspath(feed_req_obj.download_location), file_dir)

    def test_download_feed_daily_bad_request(self):
        # ask for a future feed file that does not exist
        test_date = get_formatted_date(FeedType.ITEM, 5)
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.DAILY.value, self.test_category_1,
                            self.test_marketplace, self.test_token, download_location='../tests/test-data/',
                            feed_date=test_date)
        get_response = feed_req_obj.get()
        # store the file path for clean up
        self.file_paths.append(get_response.file_path)
        # assert the result
        self.assertEqual(get_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNotNone(get_response.file_path, 'file has not been created')
        self.assertTrue(isfile(get_response.file_path), 'file_path is not pointing to a file. file_path: %s'
                        % get_response.file_path)
        # check the file size and name
        self.assertTrue(getsize(get_response.file_path) == 0, 'feed file is empty. file_path: %s'
                        % get_response.file_path)
        self.assertTrue(FeedPrefix.DAILY.value in get_response.file_path,
                        'feed file name does not have %s in it. file_path: %s'
                        % (FeedPrefix.DAILY.value, get_response.file_path))
        file_dir, file_name = split(abspath(get_response.file_path))
        self.assertEqual(abspath(feed_req_obj.download_location), file_dir)

    def test_download_feed_daily_multiple_calls(self):
        feed_req_obj = Feed(FeedType.ITEM.value, FeedScope.BOOTSTRAP.value, self.test_category_2,
                            self.test_marketplace, self.test_token, download_location='../tests/test-data/')
        get_response = feed_req_obj.get()
        # store the file path for clean up
        self.file_paths.append(get_response.file_path)
        # assert the result
        self.assertEqual(get_response.status_code, SUCCESS_CODE)
        self.assertIsNotNone(get_response.message)
        self.assertIsNotNone(get_response.file_path, 'file has not been created')
        self.assertTrue(isfile(get_response.file_path), 'file_path is not pointing to a file. file_path: %s'
                        % get_response.file_path)
        # check the file size and name
        self.assertTrue(getsize(get_response.file_path) > PROD_CHUNK_SIZE, 'feed file is less than %s. file_path: %s'
                        % (PROD_CHUNK_SIZE, get_response.file_path))
        self.assertTrue(FeedPrefix.BOOTSTRAP.value in get_response.file_path,
                        'feed file name does not have %s in it. file_path: %s'
                        % (FeedPrefix.BOOTSTRAP.value, get_response.file_path))
        file_dir, file_name = split(abspath(get_response.file_path))
        self.assertEqual(abspath(feed_req_obj.download_location), file_dir)


if __name__ == '__main__':
    unittest.main()
