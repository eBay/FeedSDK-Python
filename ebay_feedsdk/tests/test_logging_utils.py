import unittest
import re
import utils.logging_utils as logging_utils


class TestLoggingUtils(unittest.TestCase):
    def test_log_file_name(self):
        self.assertIsNotNone(logging_utils.log_file_name)
        pattern = re.compile(logging_utils.LOG_FILE_NAME + '.\\d{4}-\\d{2}-\\d{2}' + logging_utils.LOG_FILE_EXTENSION)
        self.assertTrue(pattern.match(logging_utils.log_file_name),
                        'logging file name %s does not match the format' % logging_utils.log_file_name)


if __name__ == '__main__':
    unittest.main()
