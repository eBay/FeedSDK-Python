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

REQUEST_TIMEOUT = 60
REQUEST_RETRIES = 3
BACK_OFF_TIME = 2

FEED_API_PROD_URL = 'https://api.ebay.com/buy/feed/v1_beta/'
FEED_API_SANDBOX_URL = 'https://api.sandbox.ebay.com/buy/feed/v1_beta/'

# max content that can be downloaded in one request, in bytes
PROD_CHUNK_SIZE = 104857600
SANDBOX_CHUNK_SIZE = 10485760

TOKEN_BEARER_PREFIX = 'Bearer '

AUTHORIZATION_HEADER = 'Authorization'
MARKETPLACE_HEADER = 'X-EBAY-C-MARKETPLACE-ID'
CONTENT_TYPE_HEADER = 'Content-type'
ACCEPT_HEADER = 'Accept'
RANGE_HEADER = 'Range'

CONTENT_RANGE_HEADER = 'Content-Range'

RANGE_PREFIX = 'bytes='

APPLICATION_JSON = 'application/json'

QUERY_SCOPE = 'feed_scope'
QUERY_CATEGORY_ID = 'category_id'
QUERY_SNAPSHOT_DATE = 'snapshot_date'
QUERY_DATE = 'date'


SUCCESS_CODE = 0
FAILURE_CODE = -1

SUCCESS_STR = 'Success'
FAILURE_STR = 'Failure'

DATA_FRAME_CHUNK_SIZE = 2*(10**4)  # rows
