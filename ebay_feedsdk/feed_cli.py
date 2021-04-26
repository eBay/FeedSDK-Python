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
import argparse
from enums.feed_enums import FeedType
from feed.feed_request import Feed
from filter.feed_filter import FeedFilterRequest
from constants.feed_constants import SUCCESS_CODE
from utils.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='FeedSDK', description='Feed SDK CLI')

# date
parser.add_argument('-dt', help='the date when feed file was generated')
# l1 category
parser.add_argument('-c1', help='the l1 category id of the feed file', required=True)
# scope
parser.add_argument('-scope', help='the feed scope. Available scopes are ALL_ACTIVE or NEWLY_LISTED',
                    choices=['ALL_ACTIVE', 'NEWLY_LISTED'], default='NEWLY_LISTED')
# marketplace
parser.add_argument('-mkt', help='the marketplace id for which feed is being requested. For example - EBAY_US',
                    default='EBAY_US')
# token
parser.add_argument('-token', help='the oauth token for the consumer. Omit the word \'Bearer\'')
# environment
parser.add_argument('-env', help='environment type. Supported Environments are SANDBOX and PRODUCTION',
                    choices=['SANDBOX', 'PRODUCTION'])

# options for filtering the files
parser.add_argument('-lf', nargs='+', help='list of leaf categories which are used to filter the feed')
parser.add_argument('-sellerf', nargs='+', help='list of seller names which are used to filter the feed')
parser.add_argument('-locf', nargs='+', help='list of item locations which are used to filter the feed')
parser.add_argument('-pricelf', type=float, help='lower limit of the price range for items in the feed')
parser.add_argument('-priceuf', type=float, help='upper limit of the price range for items in the feed')
parser.add_argument('-epidf', nargs='+', help='list of epids which are used to filter the feed')
parser.add_argument('-iepidf', nargs='+', help='list of inferred epids which are used to filter the feed')
parser.add_argument('-gtinf', nargs='+', help='list of gtins which are used to filter the feed')
parser.add_argument('-itemf', nargs='+', help='list of item IDs which are used to filter the feed')
# file location
parser.add_argument('-dl', '--downloadlocation', help='override for changing the directory where files are downloaded')
parser.add_argument('--filteronly', help='filter the feed file that already exists in the default path or the path '
                                         'specified by -dl, --downloadlocation option. If --filteronly option is not '
                                         'specified, the feed file will be downloaded again', action="store_true")
# file format
parser.add_argument('-format', help='feed and filter file format. Default is gzip', default='gzip')

# any query to filter the feed file
parser.add_argument('-qf', help='any other query to filter the feed file. See Python dataframe query format')

# parse the arguments
args = parser.parse_args()


start = time.time()
if args.filteronly:
    # create the filtered file
    feed_filter_obj = FeedFilterRequest(args.downloadlocation, args.itemf, args.lf, args.sellerf, args.gtinf,
                                        args.epidf, args.pricelf, args.priceuf, args.locf, args.iepidf, args.qf,
                                        args.format)
    filter_response = feed_filter_obj.filter()
    if filter_response.status_code != SUCCESS_CODE:
        print(filter_response.message)

else:
    # download the feed file if --filteronly option is not set
    feed_obj = Feed(FeedType.ITEM.value, args.scope, args.c1, args.mkt, args.token, args.dt, args.env,
                    args.downloadlocation, args.format)
    get_response = feed_obj.get()
    if get_response.status_code != SUCCESS_CODE:
        logger.error('Exception in downloading feed. Cannot proceed\nFile path: %s\n Error message: %s\n',
                     get_response.file_path, get_response.message)
    else:
        # create the filtered file
        feed_filter_obj = FeedFilterRequest(get_response.file_path, args.itemf, args.lf, args.sellerf, args.gtinf,
                                            args.epidf, args.pricelf, args.priceuf, args.locf, args.iepidf, args.qf,
                                            args.format)
        filter_response = feed_filter_obj.filter()
        if filter_response.status_code != SUCCESS_CODE:
            print(filter_response.message)
end = time.time()
logger.info('Execution time (s): %s', str(round(end - start, 3)))
print('Execution time (s): %s' % str(round(end - start, 3)))



