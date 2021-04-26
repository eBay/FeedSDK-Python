Feed SDK
==========
Python SDK for downloading and filtering item feed files

Table of contents
==========
* [Summary](#summary)
* [Setup](#setup)
    - [Setting up in the local environment](#setting-up-in-the-local-environment)
* [Downloading feed files](#downloading-feed-files)
    - [Customizing download location](#customizing-download-location)
* [Filtering feed files](#filtering-feed-files)
    - [Available filters](#available-filters)
    - [Combining filter criteria](#combining-filter-criteria)
    - [Additional filter arguments](#additional-filter-arguments)
* [Schemas](#schemas)
    - [GetFeedResponse](#getfeedresponse)
    - [Response](#response)
* [Logging](#logging)
* [Usage](#usage)
    - [Using command line options](#using-command-line-options)
    - [Using config file driven approach](#using-config-file-driven-approach)
    - [Using function calls](#using-function-calls)
        - [Code samples](#examples)
* [Performance](#performance)
* [Important notes](#important-notes)

# Summary

Similar to [Java Feed SDK](https://github.com/eBay/FeedSDK), this Python SDK facilitates download and filtering of eBay's item feed files provided through public [Feed API](https://developer.ebay.com/api-docs/buy/feed/overview.html).

The feed SDK provides a simple interface to -
* [Download](#downloading-feed-files)
* [Filter](#filtering-feed-files)

# Setup

The the entire repository can be cloned/forked and changes can be made. You are most welcome to collaborate and enhance the existing code base.

## Setting up in the local environment

For setting up the project in your local environment
* Clone or download the repository
* Install the requirements
To set up your environment, please see the requirements listed in [requirements.txt](https://github.com/eBay/FeedSDK-Python/blob/master/requirements.txt). You can run $ pip install -r requirements.txt command to install all the requirements.


## Downloading feed files
The feed files can be as big as several gigabytes. Feed API supports downloading such big feed files in chunks. Chunk size is 100 MB in production environment and is 10 MB in soundbox environment.

The SDK abstracts the complexity involved in calculating the request header '__range__' based on the response header '__content-range__' and downloads and appends all the chunks until the whole feed file is downloaded.

To download a feed file in production which is -
* __bootstrap__ : (feed_scope = ALL_ACTIVE)
* __L1 category 1__ : (category_id = 220)
* __marketplace US__ : (X-EBAY-C-MARKETPLACE-ID: EBAY_US)
instantiate a Feed object and call get() function

```
feed_obj = Feed(feed_type='item', feed_scope='ALL_ACTIVE', category_id='220', 
			       marketplace_id='EBAY_US', token=<TOKEN>, environment='PRODUCTION')
result_code, api_status_code, file_path = feed_obj.get()

```
The __filePath__ denotes the location where the file was downloaded.

### Customizing download location

The default download location is ~/Desktop/feed-sdk directory. If the directory does not exist, it will be created.
The download location can be changed by specifying the optional 'download_location' argument when instantiating Feed.
The download location should point to a directory. If the directory does not exist, it will be created.
For example, to download to the location __/tmp/feed__ - 

```
feed_obj = Feed(feed_type='item', feed_scope='ALL_ACTIVE', category_id='220', 
                               marketplace_id='EBAY_US', token=<TOKEN>, environment='PRODUCTION',
			       download_location='/tmp/feed')
```
---

## Filtering feed files

### Available filters
The SDK provides the capability to filter the feed files based on :-
* List of leaf category ids
* List of seller usernames
* List of item locations
* List of item IDs
* List of EPIDs
* List of inferred EPIDs
* List of GTINs
* Price range
* Any other SQL query

On successful completion of a filter operation, a new __filtered__ file is created in the same directory as the feed file's.

To filter a feed file on leaf category IDs create an object of FeedFilterRequest and call filter() function - 
```
feed_filter_obj = FeedFilterRequest(input_fila_path=<absolute path to the feed file>, 
                                    leaf_category_ids=<list of leaf category IDs>)
file_path = feed_filter_obj.filter()

```

To filter on availability threshold type and availability threshold via any_query parameter
```
feed_filter_obj = FeedFilterRequest(input_fila_path=<absolute path to the feed file>,
                                    any_query='AvailabilityThresholdType=\'MORE_THAN\' AND AvailabilityThreshold==10')
file_path = feed_filter_obj.filter()

```

The __file_path__ denotes the location of the filtered file. The file_path value can also be read by filter_request.filtered_file_path.

### Combining filter criteria

The SDK provides the freedom to combine the filter criteria.

To filter on leaf category IDs and seller user names for listings in the price range of 1 to 100

```
feed_filter_obj = FeedFilterRequest(input_fila_path=<absolute path to the feed file>,
                                    leaf_category_ids=<list of leaf category IDs>, 
				    seller_names=<list of seller names>,
                                    price_lower_limit=1, price_upper_limit=100)
file_path = feed_filter_obj.filter()

```

To filter on item location countries for listings that have more than 10 items available

```
feed_filter_obj = FeedFilterRequest(input_fila_path=<absolute path to the feed file>,
                                    item_location_countries=<list of item location countries>, 
                                    any_query='AvailabilityThresholdType=\'MORE_THAN\' AND AvailabilityThreshold=10')
file_path = feed_filter_obj.filter()

```

### Additional filter arguments
When filter function is called, feed data is loaded into a sqlite DB.
If keep_db=True argument is passed to filter function, the sqlite db file is kept in the current directory with name sqlite_feed_sdk.db, otherwise it will be deleted after the program execution.

By default all the columns except Title, ImageUrl, and AdditionalImageUrls are processed. This behaviour can be changed by passing column_name_list argument to filter function and changing IGNORE_COLUMNS set in feed_filter.py. 

---
### Schemas
This section provides more detail on what information is contained within the objects returned from the SDK function calls.

### GetFeedResponse

An instance of GetFeedResponse named tuple is returned from the feed_obj.get() function.

```
  int status_ode
  String message
  String file_path
  List errors

```

| Field name | Description 
|---|---|
| status_code | int: 0 indicates a successful response. Any non zero value indicates an error
| message | String: Detailed information on the status
| file_path | String: Absolute path of the location of the resulting file
| errors | List: Detailed error information


### Response 

An instance of Response named tuple is returned from feed_filter_object.filter() function.

```
  int status_code
  String message
  String file_path
  List applied_filters
```
| Field name | Description 
|---|---|
| status_code | int: 0 indicates a successful response. Any non zero value indicates an error
| message | String: Detailed information on the status
| file_path | String: Absolute path of the location of the resulting file
| applied_filters | List: List of queries applied

---
## Logging

Log files are created in the current directory.

__Ensure that appropriate permissions are present to write to the directory__

* The current log file name is : feed-sdk-log.log
* Rolling log files are created per day with the pattern : feed-sdk-log.{yyyy-MM-dd}.log

---
## Usage

The following sections describe the different ways in which the SDK can be used

### Using command line options

All the capabilities of the SDK can be invoked using the command line.

To see the available options and filters , use '--help'
```
usage: FeedSDK [-h] [-dt DT] -c1 C1 [-scope {ALL_ACTIVE,NEWLY_LISTED}]
               [-mkt MKT] [-token TOKEN] [-env {SANDBOX,PRODUCTION}]
               [-lf LF [LF ...]] [-sellerf SELLERF [SELLERF ...]]
               [-locf LOCF [LOCF ...]] [-pricelf PRICELF] [-priceuf PRICEUF]
               [-epidf EPIDF [EPIDF ...]] [-iepidf IEPIDF [IEPIDF ...]]
               [-gtinf GTINF [GTINF ...]] [-itemf ITEMF [ITEMF ...]]
               [-dl DOWNLOADLOCATION] [--filteronly] [-format FORMAT] [-qf QF]

Feed SDK CLI

optional arguments:
  -h, --help            show this help message and exit
  -dt DT                the date when feed file was generated
  -c1 C1                the l1 category id of the feed file
  -scope {ALL_ACTIVE,NEWLY_LISTED}
                        the feed scope. Available scopes are ALL_ACTIVE or
                        NEWLY_LISTED
  -mkt MKT              the marketplace id for which feed is being requested.
                        For example - EBAY_US
  -token TOKEN          the oauth token for the consumer. Omit the word
                        'Bearer'
  -env {SANDBOX,PRODUCTION}
                        environment type. Supported Environments are SANDBOX
                        and PRODUCTION
  -lf LF [LF ...]       list of leaf categories which are used to filter the
                        feed
  -sellerf SELLERF [SELLERF ...]
                        list of seller names which are used to filter the feed
  -locf LOCF [LOCF ...]
                        list of item locations which are used to filter the
                        feed
  -pricelf PRICELF      lower limit of the price range for items in the feed
  -priceuf PRICEUF      upper limit of the price range for items in the feed
  -epidf EPIDF [EPIDF ...]
                        list of epids which are used to filter the feed
  -iepidf IEPIDF [IEPIDF ...]
                        list of inferred epids which are used to filter the
                        feed
  -gtinf GTINF [GTINF ...]
                        list of gtins which are used to filter the feed
  -itemf ITEMF [ITEMF ...]
                        list of item IDs which are used to filter the feed
  -dl DOWNLOADLOCATION, --downloadlocation DOWNLOADLOCATION
                        override for changing the directory where files are
                        downloaded
  --filteronly          filter the feed file that already exists in the
                        default path or the path specified by -dl,
                        --downloadlocation option. If --filteronly option is
                        not specified, the feed file will be downloaded again
  -format FORMAT        feed and filter file format. Default is gzip
  -qf QF                any other query to filter the feed file. See Python
                        dataframe query format
```
For example, to use the command line options to

Download and filter feed files using token
```
python feed_cli.py -c1 3252 -scope ALL_ACTIVE -mkt EBAY_DE -env PRODUCTION -qf "AvailabilityThreshold=10" -locf IT GB -dl DIR -token xxx
```

Filter feed files, no token is needed
```
python feed_cli.py --filteronly -c1 260 -pricelf 5 -priceuf 20 -dl FILE_PATH
```

### Using config file driven approach

All the capabilities of the SDK can be leveraged via a config file.
The feed file download and filter parameters can be specified in the config file for multiple files, and SDK will process them sequentially.

The structure of the config file

```
{
  "requests": [
    {
      "feedRequest": {
        "categoryId": "260",
        "marketplaceId": "EBAY_US",
        "feedScope": "ALL_ACTIVE",
        "type": "ITEM"
      },
      "filterRequest": {
        "itemLocationCountries": [
          "US",
          "HK",
          "CA"
        ],
        "priceLowerLimit": 10.0,
        "priceUpperLimit": 100.0
      }
    },
    {
      "feedRequest": {
        "categoryId": "220",
        "marketplaceId": "EBAY_US",
        "date": "20190127",
        "feedScope": "NEWLY_LISTED",
        "type": "ITEM"
      }
    },
    {
      "filterRequest": {
        "inputFilePath": "<Absolute file path to the feed file>",
        "leafCategoryIds": [
          "112529",
          "64619",
          "111694"
        ],
        "itemLocationCountries": [
          "DE",
          "GB",
          "ES"
        ],
        "anyQuery": "AvailabilityThresholdType='MORE_THAN' AND AvailabilityThreshold=10",
        "fileFormat" : "gzip"
      }
    }
  ]
}
```
An example of using the SDK through a config file is located at 

[Example config file - 1](https://github.com/eBay/FeedSDK-Python/blob/master/sample-config/config-file-download)

[Example config file - 2](https://github.com/eBay/FeedSDK-Python/blob/master/sample-config/config-file-download-filter)

[Example config file - 3](https://github.com/eBay/FeedSDK-Python/blob/master/sample-config/config-file-filter)

[Example config file - 4](https://github.com/eBay/FeedSDK-Python/blob/master/sample-config/config-file-query-only)

### Using function calls

Samples showing the usage of available operations and filters.

#### Examples
All the examples are located [__here__](https://github.com/eBay/FeedSDK-Python/tree/master/examples)
[Download and filter by config request](https://github.com/eBay/FeedSDK-Python/blob/master/examples/config_examples.py)


---
## Performance
|  Category | Type  | Size gz  |  Size unzipped |  Records | Applied Filters | Filter Time | Loading Time | Save Time
|---|---|---|---|---|---|---|---|---|
| 11450 | BOOTSTRAP | 4.66 GB | 89.51 GB | 63.2 Million | PriceValue, AvailabilityThresholdType, AvailabilityThreshold | ~ 7 min | ~ 98 min | ~ 2 min
| 220 | BOOTSTRAP | 867.8 MB | 4.26 GB | 3.3 Million | price, AvailabilityThresholdType, AvailabilityThreshold | ~ 18 sec | ~ 5 min | ~ 37 sec
| 1281 | BOOTSTRAP | 118.4 MB |  1.06 GB | 812558 | item locations, AcceptedPaymentMethods | ~ 24 sec | ~ 1.2 min | ~ 1.8 min
| 11232 | BOOTSTRAP | 102.5 MB | 499.9 MB | 405268 | epids, inferredEpids | ~ 0.3 sec | ~ 37 sec | ~ 0.003 sec
| 550 | BOOTSTRAP | 60.7 MB | 986.5 MB | 1000795 | price, sellers, item locations | ~ 4 sec | ~ 1.4 min | ~ 0.1 sec
| 260 | BOOTSTRAP | 2.3 MB | 15.6 MB | 24100 | price, AvailabilityThresholdType, AvailabilityThreshold | ~ 0.01 sec | ~ 2 sec | ~ 0.4 sec
| 220 | DAILY | 13.5 MB | 60.4 MB | 55047 | price, leaf categories, item locations | ~ 0.08 sec | ~ 4 sec | ~ 0.007 sec


---
## Important notes 

* Ensure there is enough storage for feed files.
* Ensure that the file storage directories have appropriate write permissions.
* In case of failure in downloading due to network issues, the process needs to start again. There is no capability at the moment, to resume.

# License
Copyright (c) 2018-2019 eBay Inc.

Use of this source code is governed by an Apache 2.0 license that can be found in the LICENSE file or at https://opensource.org/licenses/Apache-2.0.
