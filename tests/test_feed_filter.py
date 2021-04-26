import unittest
from os import remove
from os.path import isfile
from filter.feed_filter import FeedFilterRequest
from enums.file_enums import FileFormat, FileEncoding
from constants.feed_constants import DATA_FRAME_CHUNK_SIZE, SUCCESS_CODE, FAILURE_CODE


class TestFeed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file_path = '../tests/test-data/test_bootstrap_feed_260_3'
        cls.test_any_query = 'AvailabilityThresholdType=\'MORE_THAN\' AND AvailabilityThreshold=10'

    def test_default_values(self):
        filter_request = FeedFilterRequest(self.test_file_path)
        self.assertIsNone(filter_request.item_ids)
        self.assertIsNone(filter_request.leaf_category_ids)
        self.assertIsNone(filter_request.seller_names)
        self.assertIsNone(filter_request.gtins)
        self.assertIsNone(filter_request.epids)
        self.assertIsNone(filter_request.price_upper_limit)
        self.assertIsNone(filter_request.price_lower_limit)
        self.assertIsNone(filter_request.item_location_countries)
        self.assertIsNone(filter_request.inferred_epids)
        self.assertIsNone(filter_request.item_location_countries)
        self.assertIsNone(filter_request.any_query)
        self.assertIsNone(filter_request.filtered_file_path)
        self.assertEqual(filter_request.compression_type, FileFormat.GZIP.value)
        self.assertEqual(filter_request.separator, '\t')
        self.assertEqual(filter_request.encoding, FileEncoding.UTF8.value)
        self.assertEqual(filter_request.rows_chunk_size, DATA_FRAME_CHUNK_SIZE)
        self.assertEqual(filter_request.number_of_records, 0)
        self.assertEqual(filter_request.number_of_filtered_records, 0)
        self.assertEqual(len(filter_request.queries), 0)

    def test_any_query_format(self):
        filter_request = FeedFilterRequest(self.test_file_path, any_query=self.test_any_query)
        self.assertEqual(filter_request.any_query, '(' + self.test_any_query + ')')

    def test_none_file_path(self):
        filter_request = FeedFilterRequest(None)
        filter_response = filter_request.filter()
        self.assertEqual(filter_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(filter_response.message)
        self.assertIsNone(filter_response.file_path)
        self.assertEqual(len(filter_response.applied_filters), 0)

    def test_dir_file_path(self):
        filter_request = FeedFilterRequest('../tests/test-data')
        filter_response = filter_request.filter()
        self.assertEqual(filter_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(filter_response.message)
        self.assertIsNone(filter_response.file_path)
        self.assertEqual(len(filter_response.applied_filters), 0)

    def test_no_query(self):
        filter_request = FeedFilterRequest(self.test_file_path)
        filter_response = filter_request.filter()
        self.assertEqual(filter_response.status_code, FAILURE_CODE)
        self.assertIsNotNone(filter_response.message)
        self.assertIsNone(filter_response.file_path)
        self.assertEqual(len(filter_response.applied_filters), 0)

    def test_apply_filters(self):
        filter_request = FeedFilterRequest(self.test_file_path, price_upper_limit=10, any_query=self.test_any_query)
        filter_response = filter_request.filter(keep_db=False)
        self.assertEqual(filter_response.status_code, SUCCESS_CODE)
        self.assertIsNotNone(filter_response.message)

        self.assertEqual(len(filter_request.queries), 2)
        self.assertEqual(len(filter_response.applied_filters), 2)

        self.assertTrue(filter_request.number_of_records > 0)
        self.assertTrue(filter_request.number_of_filtered_records > 0)

        self.assertIsNotNone(filter_request.filtered_file_path)
        self.assertTrue(isfile(filter_request.filtered_file_path))
        self.assertEqual(filter_request.filtered_file_path, filter_response.file_path)
        # clean up
        remove(filter_request.filtered_file_path)


if __name__ == '__main__':
    unittest.main()
