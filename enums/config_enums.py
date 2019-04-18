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

from aenum import Enum, unique


@unique
class ConfigField(Enum):
    FILTER_REQUEST = 'filterRequest'
    FEED_REQUEST = 'feedRequest'
    REQUESTS = 'requests'

    def __str__(self):
        return str(self.value)


@unique
class FeedField(Enum):
    MARKETPLACE_ID = 'marketplaceId'
    CATEGORY_ID = 'categoryId'
    DATE = 'date'
    SCOPE = 'feedScope'
    TYPE = 'type'
    ENVIRONMENT = 'environment'
    DOWNLOAD_LOCATION = 'downloadLocation'
    FILE_FORMAT = 'fileFormat'

    def __str__(self):
        return str(self.value)


@unique
class FilterField(Enum):
    INPUT_FILE_PATH = 'inputFilePath'
    ITEM_IDS = 'itemIds'
    LEAF_CATEGORY_IDS = 'leafCategoryIds'
    SELLER_NAMES = 'sellerNames'
    GTINS = 'gtins'
    EPIDS = 'epids'
    PRICE_LOWER_LIMIT = 'priceLowerLimit'
    PRICE_UPPER_LIMIT = 'priceUpperLimit'
    ITEM_LOCATION_COUNTRIES = 'itemLocationCountries'
    INFERRED_EPIDS = 'inferredEpids'
    ANY_QUERY = 'anyQuery'
    FILE_FORMAT = 'fileFormat'

    def __str__(self):
        return str(self.value)
