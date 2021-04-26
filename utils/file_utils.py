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

import json
from os import makedirs
from os.path import isdir, basename, splitext, exists, dirname
from errors import custom_exceptions
import constants.feed_constants as const


def append_response_to_file(file_handler, data):
    """
    Appends the given data to the existing file
    :param file_handler: the existing and open file object
    :param data: the data to be appended to the file
    :raise if there are any IO errors a FileCreationError exception is raised
    """
    try:
        file_handler.write(data)
    except (IOError, AttributeError) as exp:
        if file_handler:
            file_handler.close()
        raise custom_exceptions.FileCreationError('Error while writing in the file: %s' % repr(exp), data)


def create_and_replace_binary_file(file_path):
    """
    Creates a binary file in the given path including the file name and extension
    If the file exists, it will be replaced
    :param file_path: The path to the file including the file name and extension
    :raise: if the file is not created successfully an FileCreationError exception is raised
    """
    try:
        if not exists(dirname(file_path)):
            makedirs(dirname(file_path))
        with open(file_path, 'wb'):
            pass
    except (IOError, OSError, AttributeError) as exp:
        raise custom_exceptions.FileCreationError('IO error in creating file %s: %s' % (file_path, repr(exp)),
                                                  file_path)


def find_next_range(content_range_header, chunk_size=const.SANDBOX_CHUNK_SIZE):
    """
    Finds the next value of the Range header
    :param content_range_header: The content-range header value returned in the response, ex. 0-1000/7181823761
                                If None, the default Range header that is bytes=0-CHUNK_SIZE is returned
    :param chunk_size: The chunk size in bytes. If not provided, the default chunk size is used
    :return: The next value of the Range header in the format of bytes=lower-upper or empty string if no data is left
    :raise: If the input content-range value is not correct an InputDataError exception is raised
    """
    chunk = chunk_size if chunk_size else const.SANDBOX_CHUNK_SIZE
    if content_range_header is None:
        return const.RANGE_PREFIX + '0-' + str(chunk)
    else:
        try:
            # ex. content-range : 0-1000/7181823761
            range_components = content_range_header.split('/')
            total_size = int(range_components[1])
            bounds = range_components[0].split('-')
            upper_bound = int(bounds[1]) + 1
            if upper_bound > total_size:
                return ''
            return const.RANGE_PREFIX + str(upper_bound) + '-' + str(upper_bound + chunk)
        except Exception:
            raise custom_exceptions.InputDataError('Bad content-range header format: %s' % content_range_header,
                                                   content_range_header)


def get_extension(file_type):
    """
    Returns file extension including '.' according to the given file type
    :param file_type: format of the file such as gzip
    :return: extension of the file such as '.gz'
    """
    if not file_type:
        return ''
    if file_type.lower() == 'gz' or file_type.lower() == 'gzip':
        return '.gz'


def get_file_name(name_or_path):
    """
    Finds name of the file from the given file path or name
    :param name_or_path: name or path to the file
    :return: file name
    """
    if not name_or_path:
        raise custom_exceptions.InputDataError('Bad file name or directory %s' % name_or_path, name_or_path)
    if isdir(name_or_path):
        base = basename(name_or_path)
        return splitext(base)
    elif '/' in name_or_path:
        return name_or_path[name_or_path.rfind('/') + 1:]
    else:
        return name_or_path


def read_json(file_path):
    """
    Reads json from a file and returns a json object
    :param file_path: the path to the file
    :return: a json object
    """
    with open(file_path) as config_file:
        json_obj = json.load(config_file)
    return json_obj
