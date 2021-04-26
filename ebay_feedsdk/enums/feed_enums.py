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
class FeedColumn(Enum):
    ITEM_ID = 'ItemId'  # column 0
    CATEGORY_ID = 'CategoryId'  # column 4
    SELLER_USERNAME = 'SellerUsername'  # column 6
    GTIN = 'GTIN'  # column 9
    EPID = 'EPID'  # column 12
    PRICE_VALUE = 'PriceValue'  # column 15
    ITEM_LOCATION_COUNTRIES = 'ItemLocationCountry'  # column 21
    INFERRED_EPID = 'InferredEPID'  # column 40

    def __str__(self):
        return str(self.value)


@unique
class Environment(Enum):
    PRODUCTION = 'production'
    SANDBOX = 'sandbox'

    def __str__(self):
        return str(self.value)


@unique
class FeedPrefix(Enum):
    DAILY = 'daily'
    BOOTSTRAP = 'bootstrap'

    def __str__(self):
        return str(self.value)


@unique
class FeedScope(Enum):
    DAILY = 'NEWLY_LISTED'
    BOOTSTRAP = 'ALL_ACTIVE'

    def __str__(self):
        return str(self.value)


@unique
class FeedType(Enum):
    ITEM = 'item'
    SNAPSHOT = 'item_snapshot'

    def __str__(self):
        return str(self.value)
