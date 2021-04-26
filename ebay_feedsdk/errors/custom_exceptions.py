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

class Error(Exception):
    """Base class for errors in this module."""
    pass


class AuthorizationError(Error):
    def __init__(self, msg):
        self.msg = msg


class ConfigError(Error):
    def __init__(self, msg, mark=None):
        self.msg = msg
        self.mark = mark


class FileCreationError(Error):
    def __init__(self, msg, path):
        self.msg = msg
        self.path = path


class FilterError(Error):
    def __init__(self, msg, filter_query=None):
        self.msg = msg
        self.input_data = filter_query


class InputDataError(Error):
    def __init__(self, msg, input_data=None):
        self.msg = msg
        self.input_data = input_data
