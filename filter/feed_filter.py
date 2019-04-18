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

import time
import logging
import pandas as pd
from os import remove
from sqlalchemy import create_engine
from collections import namedtuple
from os.path import split, abspath, join, isfile
from utils import filter_utils
from utils.file_utils import get_extension

from enums.feed_enums import FeedColumn
from enums.file_enums import FileEncoding, FileFormat
import constants.feed_constants as const
from utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

Response = namedtuple('Response', 'status_code message file_path applied_filters')
GetFeedResponse = namedtuple('GetFeedResponse', Response._fields + ('errors',))

BOOL_COLUMNS = {'ImageAlteringProhibited', 'ReturnsAccepted'}
# using float64 for integer columns as well as the workaround for NAN values
FLOAT_COLUMNS = {'AvailabilityThreshold', 'EstimatedAvailableQuantity',
                 'PriceValue', 'ReturnPeriodValue'}
IGNORE_COLUMNS = {'AdditionalImageUrls', 'ImageUrl', 'Title'}

DB_FILE_NAME = 'sqlite_feed_sdk.db'
DB_TABLE_NAME = 'feed'


class FeedFilterRequest(object):
    def __init__(self, input_file_path, item_ids=None, leaf_category_ids=None, seller_names=None, gtins=None,
                 epids=None, price_lower_limit=None, price_upper_limit=None, item_location_countries=None,
                 inferred_epids=None, any_query=None, compression_type=FileFormat.GZIP.value, separator='\t',
                 encoding=FileEncoding.UTF8.value, rows_chunk_size=const.DATA_FRAME_CHUNK_SIZE):
        self.input_file_path = input_file_path
        self.item_ids = item_ids
        self.leaf_category_ids = leaf_category_ids
        self.seller_names = seller_names
        self.gtins = gtins
        self.epids = epids
        self.price_lower_limit = price_lower_limit
        self.price_upper_limit = price_upper_limit
        self.item_location_countries = item_location_countries
        self.inferred_epids = inferred_epids
        self.any_query = '(%s)' % any_query if any_query else None
        self.compression_type = compression_type if compression_type else FileFormat.GZIP.value
        self.separator = separator if separator else '\t'
        self.encoding = encoding if encoding else FileEncoding.UTF8.value
        self.rows_chunk_size = rows_chunk_size if rows_chunk_size else const.DATA_FRAME_CHUNK_SIZE
        self.__filtered_file_path = None
        self.__number_of_records = 0
        self.__number_of_filtered_records = 0
        self.__queries = []

    def __str__(self):
        return '[input_file_path= %s, item_ids= %s, leaf_category_ids= %s, seller_names= %s, gtins= %s, ' \
               'epids= %s,  price_lower_limit= %s, price_upper_limit= %s, item_location_countries= %s, ' \
               'inferred_epids= %s,  any_query= %s, compression_type= %s, separator= %s, encoding= %s]' % \
               (self.input_file_path,
                self.item_ids,
                self.leaf_category_ids,
                self.seller_names,
                self.gtins,
                self.epids,
                self.price_lower_limit,
                self.price_upper_limit,
                self.item_location_countries,
                self.inferred_epids,
                self.any_query,
                self.compression_type,
                self.separator,
                self.encoding)

    @property
    def filtered_file_path(self):
        return self.__filtered_file_path

    @property
    def number_of_records(self):
        return self.__number_of_records

    @property
    def number_of_filtered_records(self):
        return self.__number_of_filtered_records

    @property
    def queries(self):
        return self.__queries

    def __append_query(self, query_str):
        if query_str:
            self.__queries.append(query_str)

    def filter(self, column_name_list=None, keep_db=False):
        logger.info('Filtering... \nInput file: %s', self.input_file_path)

        self.__append_query(self.any_query)
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.ITEM_ID, self.item_ids))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.CATEGORY_ID, self.leaf_category_ids))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.SELLER_USERNAME, self.seller_names))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.GTIN, self.gtins))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.EPID, self.epids))
        self.__append_query(filter_utils.get_inclusive_greater_query(FeedColumn.PRICE_VALUE, self.price_lower_limit))
        self.__append_query(filter_utils.get_inclusive_less_query(FeedColumn.PRICE_VALUE, self.price_upper_limit))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.INFERRED_EPID, self.inferred_epids))
        self.__append_query(filter_utils.get_list_string_element_query(FeedColumn.ITEM_LOCATION_COUNTRIES,
                                                                       self.item_location_countries))
        query_str = None
        if self.__queries:
            query_str = ' AND '.join(self.__queries)
        if not self.input_file_path or not isfile(self.input_file_path):
            return Response(const.FAILURE_CODE,
                            'Input file is a directory or does not exist. Cannot filter. Aborting...',
                            self.filtered_file_path, self.queries)
        if not query_str:
            return Response(const.FAILURE_CODE, 'No filters have been specified. Cannot filter. Aborting...',
                            self.filtered_file_path, self.queries)
        # create the data frame
        filtered_data = self.__read_chunks_gzip_file(query_str, column_name_list, keep_db)
        if not filtered_data.empty:
            self.__save_filtered_data_frame(filtered_data)
        else:
            logger.error('No filtered feed file created')
        return Response(const.SUCCESS_CODE, const.SUCCESS_STR, self.filtered_file_path, self.queries)

    def __derive_filtered_file_path(self):
        file_path, full_file_name = split(abspath(self.input_file_path))
        file_name = full_file_name.split('.')[0]
        time_milliseconds = int(time.time() * 1000)
        filtered_file_path = join(file_path, file_name + '-filtered-' + str(time_milliseconds) +
                                  get_extension(self.compression_type))
        return filtered_file_path

    def __read_chunks_gzip_file(self, query_str, column_name_list, keep_db):
        disk_engine = create_engine('sqlite:///'+DB_FILE_NAME)
        chunk_num = 0
        columns_to_process, data_types = self.__get_cols_and_type_dict()
        cols = column_name_list if column_name_list else columns_to_process
        start = time.time()
        for chunk_df in pd.read_csv(self.input_file_path, header=0,
                                    compression=self.compression_type, encoding=self.encoding, usecols=cols,
                                    sep=self.separator, quotechar='"', lineterminator='\n', skip_blank_lines=True,
                                    skipinitialspace=True, error_bad_lines=False, index_col=False,
                                    chunksize=self.rows_chunk_size, dtype=data_types,
                                    converters={'AvailabilityThreshold': filter_utils.convert_to_float_max_int,
                                                'EstimatedAvailableQuantity': filter_utils.convert_to_float_max_int,
                                                'PriceValue': filter_utils.convert_to_float_zero,
                                                'ReturnPeriodValue': filter_utils.convert_to_float_zero,
                                                'ImageAlteringProhibited': filter_utils.convert_to_bool_false,
                                                'ReturnsAccepted': filter_utils.convert_to_bool_false}):
            self.__number_of_records = self.__number_of_records + len(chunk_df.index)
            chunk_num = chunk_num + 1
            chunk_df.to_sql(DB_TABLE_NAME, disk_engine, if_exists='append', index=False)
        execution_time = time.time() - start
        logger.info('Loaded %s records in %s (s) %s (m)', self.__number_of_records, str(round(execution_time, 3)),
                     str(round(execution_time / 60, 3)))
        # apply query
        sql_string = '''SELECT * From %s WHERE %s ''' % (DB_TABLE_NAME, query_str)

        start = time.time()
        query_result_df = pd.read_sql_query(sql_string, disk_engine)
        execution_time = time.time() - start
        self.__number_of_filtered_records = len(query_result_df.index)
        logger.info('Filtered %s records in %s (s) %s (m)', self.number_of_filtered_records,
                     str(round(execution_time, 3)),
                     str(round(execution_time / 60, 3)))
        # remove the created db file
        if not keep_db:
            remove(DB_FILE_NAME)
        return query_result_df

    def __save_filtered_data_frame(self, data_frame):
        self.__filtered_file_path = self.__derive_filtered_file_path()
        start = time.time()
        data_frame.to_csv(self.__filtered_file_path, sep=self.separator, na_rep='', header=True, index=False, mode='w',
                          encoding=self.encoding, compression=self.compression_type, quotechar='"',
                          line_terminator='\n', doublequote=True, escapechar='\\', decimal='.')
        execution_time = time.time() - start
        logger.info('Saved %s records in %s (s) %s (m)', self.number_of_filtered_records,
                    str(round(execution_time, 3)),
                    str(round(execution_time / 60, 3)))

    def __get_cols_and_type_dict(self):
        all_columns = pd.read_csv(self.input_file_path, nrows=1, sep=self.separator,
                                  compression=self.compression_type).columns.tolist()
        type_dict = {}
        cols = []
        for col_name in all_columns:
            # Ignoring due to possibility of comma character in the value and breaking the parser
            if col_name in IGNORE_COLUMNS:
                continue
            else:
                cols.append(col_name)
                if col_name not in BOOL_COLUMNS and col_name not in FLOAT_COLUMNS:
                    type_dict[col_name] = 'object'
        return cols, type_dict
