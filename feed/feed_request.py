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

import certifi
import urllib3
import json
import logging
from os import path
from utils import file_utils, date_utils
import constants.feed_constants as const
from filter.feed_filter import GetFeedResponse
from enums.file_enums import FileFormat
from enums.feed_enums import FeedType, FeedScope, FeedPrefix, Environment
from errors.custom_exceptions import InputDataError, FileCreationError
from utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

DEFAULT_DOWNLOAD_LOCATION = path.expanduser('~/Desktop/feed-sdk')


class Feed(object):
    def __init__(self, feed_type, feed_scope, category_id, marketplace_id, token, feed_date=None,
                 environment=Environment.PRODUCTION.value, download_location=None, file_format=FileFormat.GZIP.value):
        self.token = const.TOKEN_BEARER_PREFIX + token if (token and not token.startswith('Bearer')) else token
        self.feed_type = feed_type.lower() if feed_type else FeedType.ITEM.value
        self.feed_scope = feed_scope.upper() if feed_scope else FeedScope.DAILY.value
        self.category_id = category_id
        self.marketplace_id = marketplace_id
        self.environment = environment if environment else Environment.PRODUCTION.value
        self.download_location = download_location if download_location else DEFAULT_DOWNLOAD_LOCATION
        self.file_format = file_format if file_format else FileFormat.GZIP.value
        self.feed_date = feed_date if feed_date else date_utils.get_formatted_date(feed_type)

    def __str__(self):
        return '[feed_type= %s, feed_scope= %s, category_id= %s, marketplace_id= %s, feed_date= %s, ' \
               'environment= %s,  download_location= %s, file_format= %s, token= %s]' % (self.feed_type,
                                                                                         self.feed_scope,
                                                                                         self.category_id,
                                                                                         self.marketplace_id,
                                                                                         self.feed_date,
                                                                                         self.environment,
                                                                                         self.download_location,
                                                                                         self.file_format,
                                                                                         self.token)

    def get(self):
        """
        :return: GetFeedResponse
        """
        logger.info(
            'Downloading... \ncategoryId: %s | marketplace: %s | date: %s | feed_scope: %s | environment: %s \n',
            self.category_id, self.marketplace_id, self.feed_date, self.feed_scope, self.environment)
        if not self.token:
            return GetFeedResponse(const.FAILURE_CODE, 'No token has been provided', None, None, None)
        if path.exists(self.download_location) and not path.isdir(self.download_location):
            return GetFeedResponse(const.FAILURE_CODE, 'Download location is not a directory', self.download_location,
                                   None, None)
        try:
            date_utils.validate_date(self.feed_date, self.feed_type)
        except InputDataError as exp:
            return GetFeedResponse(const.FAILURE_CODE, exp.msg, self.download_location, None, None)
        # generate the absolute file path
        file_name = self.__generate_file_name()
        file_path = path.join(self.download_location, file_name)
        # Create an empty file in the given path
        try:
            file_utils.create_and_replace_binary_file(file_path)
            with open(file_path, 'wb') as file_obj:
                # Get the feed file data
                result_code, message = self.__invoke_request(file_obj)
                return GetFeedResponse(result_code, message, file_path, None, None)
        except IOError as exp:
            return GetFeedResponse(const.FAILURE_CODE, 'Could not open file %s : %s' % (file_path, repr(exp)),
                                   file_path, None, None)
        except (InputDataError, FileCreationError) as exp:
            return GetFeedResponse(const.FAILURE_CODE, exp.msg, file_path, None, None)

    def __invoke_request(self, file_handler):
        # initialize API call counter
        api_call_counter = 0
        # Find max chunk size
        chunk_size = self.__find_max_chunk_size()
        logger.info('Chunk size: %s\n', chunk_size)
        # The initial request Range header is bytes=0-CHUNK_SIZE
        headers = {const.MARKETPLACE_HEADER: self.marketplace_id,
                   const.AUTHORIZATION_HEADER: self.token,
                   const.CONTENT_TYPE_HEADER: const.APPLICATION_JSON,
                   const.ACCEPT_HEADER: const.APPLICATION_JSON,
                   const.RANGE_HEADER: const.RANGE_PREFIX + '0-' + str(chunk_size)}
        parameters, endpoint = self.__get_query_parameters_and_base_url()
        http_manager = urllib3.PoolManager(timeout=const.REQUEST_TIMEOUT,
                                           retries=urllib3.Retry(const.REQUEST_RETRIES,
                                                                 backoff_factor=const.BACK_OFF_TIME),
                                           cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        # Initial request
        feed_response = http_manager.request('GET', endpoint, parameters, headers)
        # increase and print API call counter
        api_call_counter = api_call_counter + 1
        logger.info('API call #%s\n', api_call_counter)
        # Get the status code
        status_code = feed_response.status
        # Append the data to the file, might raise an exception
        if status_code == 200:
            file_utils.append_response_to_file(file_handler, feed_response.data)
            return const.SUCCESS_CODE, const.SUCCESS_STR
        while status_code == 206:
            # Append the data to the file, might raise an exception
            file_utils.append_response_to_file(file_handler, feed_response.data)
            headers[const.RANGE_HEADER] = file_utils.find_next_range(feed_response.headers[const.CONTENT_RANGE_HEADER],
                                                                     chunk_size)
            # check if we have reached the end of the file
            if not headers[const.RANGE_HEADER]:
                break
            # Send another request
            feed_response = http_manager.request('GET', endpoint, parameters, headers)
            # increase and print API call counter
            api_call_counter = api_call_counter+1
            logger.info('API call #%s\n', api_call_counter)
            # Get the status code
            status_code = feed_response.status
        if status_code == 206 and not headers[const.RANGE_HEADER]:
            return const.SUCCESS_CODE, const.SUCCESS_STR
        json_response = json.loads(feed_response.data.decode('utf-8'))
        return const.FAILURE_CODE, json_response.get('errors')

    def __get_query_parameters_and_base_url(self):
        # Base URL
        base_url = self.__find_base_url()
        base_url = base_url + str(FeedType.ITEM)
        # Common query parameter
        fields = {const.QUERY_CATEGORY_ID: self.category_id}
        # Snapshot feed
        if self.feed_type == str(FeedType.SNAPSHOT):
            fields.update({const.QUERY_SNAPSHOT_DATE: self.feed_date})
            base_url = const.FEED_API_PROD_URL + str(FeedType.SNAPSHOT)
            return fields, base_url
        # Daily or bootstrap feed
        if self.feed_scope == str(FeedScope.DAILY):
            fields.update({const.QUERY_SCOPE: self.feed_scope,
                           const.QUERY_DATE: self.feed_date})
        elif self.feed_scope == str(FeedScope.BOOTSTRAP):
            fields.update({const.QUERY_SCOPE: self.feed_scope})
        return fields, base_url

    def __find_base_url(self):
        if self.environment.lower() == str(Environment.PRODUCTION):
            return const.FEED_API_PROD_URL
        return const.FEED_API_SANDBOX_URL

    def __find_max_chunk_size(self):
        if self.environment.lower() == str(Environment.PRODUCTION):
            return const.PROD_CHUNK_SIZE
        return const.SANDBOX_CHUNK_SIZE

    def __generate_file_name(self):
        if str(FeedScope.BOOTSTRAP) == self.feed_scope:
            feed_prefix = str(FeedPrefix.BOOTSTRAP)
        elif str(FeedScope.DAILY) == self.feed_scope:
            feed_prefix = str(FeedPrefix.DAILY)
        else:
            raise InputDataError('Unknown feed scope', self.feed_scope)
        file_name = str(FeedType.ITEM) + '_' + feed_prefix + '_' + str(self.category_id) + '_' + self.feed_date + \
            '_' + self.marketplace_id + file_utils.get_extension(self.file_format)
        return file_name
