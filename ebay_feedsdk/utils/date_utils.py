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

from datetime import datetime, timedelta
from enums.feed_enums import FeedType
from errors.custom_exceptions import InputDataError


def get_formatted_date(feed_type, day_delta=None):
    """
    :param day_delta: the day difference
    :param feed_type: item or item_snapshot
    :return: today date string in the correct format according to feed_type
    """
    delta = day_delta if day_delta else 0
    date_obj = datetime.now() + timedelta(days=delta)
    if feed_type == str(FeedType.SNAPSHOT):
        # TODO: Fix the date format
        return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        return date_obj.strftime('%Y%m%d')


def validate_date(feed_date, feed_type):
    """
    Validates the feed_date string format according to feed_type.
    :param feed_date: the date string feed is requested for
    :param feed_type: item or item_snapshot
    :raise InputDataError: if the date string format is not correct an InputDataError exception is raised
    """
    if feed_type == str(FeedType.SNAPSHOT):
        try:
            datetime.strptime(feed_date, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise InputDataError('Bad feed date format. Date should be in UTC format (yyyy-MM-ddThh:00:00.000Z)',
                                 feed_date)
    else:
        try:
            datetime.strptime(feed_date, '%Y%m%d')
        except ValueError:
            raise InputDataError('Bad feed date format. Date should be in yyyyMMdd format', feed_date)
