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

import logging
from datetime import datetime

LOG_FILE_NAME = 'feed-sdk-log'
LOG_FILE_EXTENSION = '.log'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

log_file_name = LOG_FILE_NAME + '.' + datetime.now().strftime('%Y-%m-%d') + LOG_FILE_EXTENSION


def setup_logging():
    logging.basicConfig(filename=log_file_name, filemode='a', level=logging.DEBUG, format=LOGGING_FORMAT)
