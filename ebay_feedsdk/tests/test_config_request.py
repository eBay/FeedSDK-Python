import unittest
from enums.file_enums import FileFormat
from enums.feed_enums import FeedScope
from config.config_request import ConfigFileRequest
from feed.feed_request import DEFAULT_DOWNLOAD_LOCATION


class TestConfigRequest(unittest.TestCase):
    def test_parse_requests(self):
        cr = ConfigFileRequest('../tests/test-data/test_config')
        cr.parse_requests('Bearer v^1...')
        self.assertIsNotNone(cr.requests)
        self.assertEqual(len(cr.requests), 3)

        # first request has both feed and filter requests
        feed_req = cr.requests[0].feed_obj
        filter_req = cr.requests[0].filter_request_obj
        self.assertIsNotNone(feed_req)
        self.assertIsNotNone(filter_req)
        self.assertEqual(feed_req.category_id, '260')
        self.assertEqual(filter_req.price_lower_limit, 10)

        # second request has a feed request only
        self.assertIsNone(cr.requests[1].filter_request_obj)
        feed_req = cr.requests[1].feed_obj
        self.assertIsNotNone(feed_req)
        self.assertIsNotNone(feed_req.token)
        self.assertEqual(feed_req.category_id, '220')
        self.assertEqual(feed_req.marketplace_id, 'EBAY_US')
        self.assertEqual(feed_req.feed_date, '20190127')
        self.assertEqual(feed_req.feed_scope, FeedScope.DAILY.value)
        self.assertEqual(feed_req.download_location, DEFAULT_DOWNLOAD_LOCATION)

        # third request has a filter request only
        self.assertIsNone(cr.requests[2].feed_obj)
        filter_req = cr.requests[2].filter_request_obj
        self.assertIsNotNone(filter_req)
        self.assertEqual(filter_req.input_file_path, '/Users/[USER]/Desktop/sdk/test_bootstrap.gz')
        self.assertEqual(filter_req.leaf_category_ids, ['112529', '64619', '111694'])
        self.assertEqual(filter_req.item_location_countries, ['DE', 'GB', 'ES'])
        self.assertEqual(filter_req.any_query,
                          '(AvailabilityThresholdType=\'MORE_THAN\' AND AvailabilityThreshold=10)')
        self.assertEqual(filter_req.compression_type, FileFormat.GZIP.value)


if __name__ == '__main__':
    unittest.main()
