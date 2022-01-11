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

import sys
import pandas as pd
from distutils.util import strtobool


def convert_to_bool_false(data):
    try:
        bool_value = strtobool(data)
        return pd.np.bool(bool_value)
    except (ValueError, TypeError, AttributeError):
        return pd.np.bool(False)


def convert_to_float_max_int(data):
    try:
        return pd.np.float(data)
    except (ValueError, TypeError, AttributeError):
        return pd.np.float(sys.maxsize)


def convert_to_float_zero(data):
    try:
        return pd.np.float(data)
    except (ValueError, TypeError, AttributeError):
        return pd.np.float(0)


def get_inclusive_less_query(column_name, upper_limit):
    if not upper_limit:
        return ''
    return '%s <= %s' % (column_name, upper_limit)


def get_inclusive_greater_query(column_name, lower_limit):
    if not lower_limit:
        return ''
    return '%s >= %s' % (column_name, lower_limit)


def get_list_number_element_query(column_name, value_list):
    if not value_list:
        return ''
    list_str = ','.join(str(element) for element in value_list)
    return '%s IN (%s)' % (column_name, list_str)


def get_list_string_element_query(column_name, value_list):
    if not value_list:
        return ''
    list_str = (','.join('\'' + item + '\'' for item in value_list))
    return '%s IN (%s)' % (column_name, list_str)
