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
class FileEncoding(Enum):
    UTF8 = 'UTF-8'

    def __str__(self):
        return str(self.value)


@unique
class FileFormat(Enum):
    GZIP = 'gzip'

    def __str__(self):
        return str(self.value)
