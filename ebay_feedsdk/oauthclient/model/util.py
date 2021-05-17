# -*- coding: utf-8 -*-
"""
Copyright 2019 eBay Inc.
 
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,

WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

"""
import base64


def generate_request_headers(credential):
    cred = credential.client_id + ':' + credential.client_secret

    b64_encoded_credential = base64.b64encode(cred.encode()).decode()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_encoded_credential
    }

    return headers


def generate_application_request_body(credential, scopes):
    body = {
        'grant_type': 'client_credentials',
        'redirect_uri': credential.ru_name,
        'scope': scopes
    }

    return body


def generate_refresh_request_body(scopes, refresh_token):
    if refresh_token is None:
        raise Exception("credential object does not contain refresh_token and/or scopes")

    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': scopes
    }

    return body


def generate_oauth_request_body(credential, code):
    body = {
        'grant_type': 'authorization_code',
        'redirect_uri': credential.ru_name,
        'code': code
    }

    return body
