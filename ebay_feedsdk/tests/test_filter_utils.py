import unittest
import sys
from utils import filter_utils
from enums.feed_enums import FeedColumn


class TestFilterUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_column_1 = FeedColumn.PRICE_VALUE
        cls.test_column_2 = FeedColumn.ITEM_LOCATION_COUNTRIES

    def test_get_inclusive_less_query_none(self):
        query_str = filter_utils.get_inclusive_less_query(self.test_column_1, None)
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_inclusive_less_query_empty(self):
        query_str = filter_utils.get_inclusive_less_query(self.test_column_1, '')
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_inclusive_less_query(self):
        query_str = filter_utils.get_inclusive_less_query(self.test_column_1, 10)
        expected_query = '%s <= 10' % self.test_column_1
        self.assertEqual(expected_query, query_str)

    def test_get_inclusive_greater_query_none(self):
        query_str = filter_utils.get_inclusive_greater_query(self.test_column_1, None)
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_inclusive_greater_query_empty(self):
        query_str = filter_utils.get_inclusive_greater_query(self.test_column_1, '')
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_inclusive_greater_query(self):
        query_str = filter_utils.get_inclusive_greater_query(self.test_column_1, 10)
        expected_query = '%s >= 10' % self.test_column_1
        self.assertEqual(expected_query, query_str)

    def test_get_list_number_element_query_none(self):
        query_str = filter_utils.get_list_number_element_query(self.test_column_2, None)
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_list_number_element_query_empty(self):
        query_str = filter_utils.get_list_number_element_query(self.test_column_2, '')
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_list_string_element_query_none(self):
        query_str = filter_utils.get_list_string_element_query(self.test_column_2, None)
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_list_string_element_query_empty(self):
        query_str = filter_utils.get_list_string_element_query(self.test_column_2, '')
        self.assertEqual('', query_str, 'query is not an empty string')

    def test_get_list_number_element_query(self):
        query_str = filter_utils.get_list_number_element_query(self.test_column_2, [1, 2])
        expected_query = '%s IN (1,2)' % self.test_column_2
        self.assertEqual(expected_query, query_str)

    def test_get_list_string_element_query(self):
        query_str = filter_utils.get_list_string_element_query(self.test_column_2, ['CA', 'US'])
        expected_query = '%s IN (\'CA\',\'US\')' % self.test_column_2
        self.assertEqual(expected_query, query_str)

    def test_convert_to_bool_false_invalid(self):
        converted_bool = filter_utils.convert_to_bool_false('invalid')
        self.assertEqual(False, converted_bool)

    def test_convert_to_bool_false_true(self):
        converted_bool = filter_utils.convert_to_bool_false('True')
        self.assertEqual(True, converted_bool)

    def test_convert_to_bool_false_false(self):
        converted_bool = filter_utils.convert_to_bool_false('False')
        self.assertEqual(False, converted_bool)

    def convert_to_float_max_int_invalid(self):
        converted_float = filter_utils.convert_to_float_max_int('invalid')
        self.assertEqual(sys.maxsize, converted_float)

    def convert_to_float_max_int(self):
        converted_float = filter_utils.convert_to_float_max_int('1.2')
        self.assertEqual(1.2, converted_float)

    def convert_to_float_zero_invalid(self):
        converted_float = filter_utils.convert_to_float_zero('invalid')
        self.assertEqual(0, converted_float)

    def convert_to_float_zero(self):
        converted_float = filter_utils.convert_to_float_zero('1.2')
        self.assertEqual(1.2, converted_float)


if __name__ == '__main__':
    unittest.main()
