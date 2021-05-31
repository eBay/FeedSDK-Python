Feed SDK
==========
Python SDK for downloading and filtering item feed files including oauth authentication.

Forked and merged from [https://github.com/eBay/FeedSDK-Python](https://github.com/eBay/FeedSDK-Python) and [https://github.com/eBay/ebay-oauth-python-client](https://github.com/eBay/ebay-oauth-python-client) and ported to python3

Nothing serious changed, made it barely working. 

Code is not improved yet and would need some maintenance. 

Automatic Tests not working due to the nature the tests were original programmed (you need to provide actual token etc.)

Available as PyPI package under https://pypi.org/project/ebay-feedsdk/

Example code to retrieve oauth token and download file (you need working ebay-config.yaml)

See ebay_feedsk/ebay_download_example.py for example how to download feed files

See also for details:

* [https://github.com/eBay/ebay-oauth-python-client/blob/master/README.adoc](https://github.com/eBay/ebay-oauth-python-client/blob/master/README.adoc)
* [https://github.com/eBay/FeedSDK-Python/blob/master/README.md](https://github.com/eBay/FeedSDK-Python/blob/master/README.md)
