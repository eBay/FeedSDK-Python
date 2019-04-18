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

from config.config_request import ConfigFileRequest


def filter_feed(config_path):
    cr = ConfigFileRequest(config_path)
    cr.parse_requests()
    cr.process_requests()


def download_filter_feed(config_path, token):
    cr = ConfigFileRequest(config_path)
    cr.parse_requests(token)
    cr.process_requests()


if __name__ == '__main__':
    filter_feed('../sample-config/config-file-filter')
    download_filter_feed('../sample-config/config-file-download-filter', 'v^1.1#i...')
