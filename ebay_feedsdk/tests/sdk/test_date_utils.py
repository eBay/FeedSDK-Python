import unittest
from utils import date_utils
from datetime import datetime
from enums.feed_enums import FeedType
from errors.custom_exceptions import InputDataError


class TestDateUtils(unittest.TestCase):
    def test_get_formatted_date(self):
        today_date = date_utils.get_formatted_date(FeedType.ITEM)
        try:
            datetime.strptime(today_date, '%Y%m%d')
        except ValueError:
            self.fail('Invalid date format: %s' % today_date)

    def test_validate_date_exception(self):
        with self.assertRaises(InputDataError):
            date_utils.validate_date('2019/02/01', FeedType.ITEM)

    def test_validate_date(self):
        date_utils.validate_date('20190201', FeedType.ITEM)


if __name__ == '__main__':
    unittest.main()
