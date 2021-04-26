# **************************************************************************
# Copyright 2018-2019 eBay Inc.
# Author/Developers: --

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# **************************************************************************/

import logging
from os import path
from utils.file_utils import read_json
from feed.feed_request import Feed
from filter.feed_filter import FeedFilterRequest
from constants.feed_constants import SUCCESS_CODE
from enums.config_enums import ConfigField, FeedField, FilterField
from errors.custom_exceptions import ConfigError
from utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class ConfigRequest(object):
    def __init__(self, feed_obj, filter_request_obj):
        self.feed_obj = feed_obj
        self.filter_request_obj = filter_request_obj

    def __str__(self):
        return '[feed= %s, filter_request= %s]' % (self.feed_obj, self.filter_request_obj)


class ConfigFileRequest(object):
    def __init__(self, config_file_path):
        self.file_path = config_file_path
        self.__token = None
        self.__config_json_obj = None
        self.__requests = []

    @property
    def requests(self):
        return self.__requests

    def parse_requests(self, token=None):
        self.__load_config()
        # populate requests list
        self.__create_requests(token)

    def process_requests(self):
        if not self.requests:
            logger.error('No requests to process')
            return False
        for config_request_obj in self.requests:
            get_response = None
            if config_request_obj.feed_obj:
                feed_req = config_request_obj.feed_obj
                get_response = feed_req.get()
                if get_response.status_code != SUCCESS_CODE:
                    logger.error('Exception in downloading feed. Cannot proceed, continue to the next request\n'
                                 'File Path: %s | Error message: %s\nFeed Request: %s\n', get_response.file_path,
                                 get_response.message, feed_req)
                    continue
            if config_request_obj.filter_request_obj:
                filter_req = config_request_obj.filter_request_obj
                if get_response and get_response.file_path:
                    # override input file path if set
                    filter_req.input_file_path = get_response.file_path
                filter_response = filter_req.filter()
                if filter_response.status_code != SUCCESS_CODE:
                    print(filter_response.message)
        return True

    def __load_config(self):
        # check the path
        if not self.file_path or not path.exists(self.file_path) or path.getsize(self.file_path) == 0:
            raise ConfigError('Config file %s does not exist or is empty' % self.file_path)
        # load the config file
        self.__config_json_obj = read_json(self.file_path)
        # check the config object
        if not self.__config_json_obj:
            raise ConfigError('Could not read config file %s' % self.file_path)

    def __create_requests(self, token):
        if ConfigField.REQUESTS.value not in self.__config_json_obj:
            raise ConfigError('No \"%s\" field exists in the config file %s' % (str(ConfigField.REQUESTS),
                                                                                self.file_path))
        for req in self.__config_json_obj[ConfigField.REQUESTS.value]:
            feed_obj = None
            feed_field = req.get(ConfigField.FEED_REQUEST.value)
            if feed_field:
                feed_obj = Feed(feed_field.get(FeedField.TYPE.value),
                                feed_field.get(FeedField.SCOPE.value),
                                feed_field.get(FeedField.CATEGORY_ID.value),
                                feed_field.get(FeedField.MARKETPLACE_ID.value),
                                token,
                                feed_field.get(FeedField.DATE.value),
                                feed_field.get(FeedField.ENVIRONMENT.value),
                                feed_field.get(FeedField.DOWNLOAD_LOCATION.value),
                                feed_field.get(FeedField.FILE_FORMAT.value))
            filter_request_obj = None
            filter_field = req.get(ConfigField.FILTER_REQUEST.value)
            if filter_field:
                filter_request_obj = FeedFilterRequest(str(filter_field.get(FilterField.INPUT_FILE_PATH.value)),
                                                       filter_field.get(FilterField.ITEM_IDS.value),
                                                       filter_field.get(FilterField.LEAF_CATEGORY_IDS.value),
                                                       filter_field.get(FilterField.SELLER_NAMES.value),
                                                       filter_field.get(FilterField.GTINS.value),
                                                       filter_field.get(FilterField.EPIDS.value),
                                                       filter_field.get(FilterField.PRICE_LOWER_LIMIT.value),
                                                       filter_field.get(FilterField.PRICE_UPPER_LIMIT.value),
                                                       filter_field.get(FilterField.ITEM_LOCATION_COUNTRIES.value),
                                                       filter_field.get(FilterField.INFERRED_EPIDS.value),
                                                       filter_field.get(FilterField.ANY_QUERY.value),
                                                       filter_field.get(FilterField.FILE_FORMAT.value))
            config_request_obj = ConfigRequest(feed_obj, filter_request_obj)
            self.requests.append(config_request_obj)
