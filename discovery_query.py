import sys
import os
import json
import time
import pandas as pd
from watson_developer_cloud import DiscoveryV1
import argparse

# BEGIN of python-dotenv section
from os.path import join, dirname
from dotenv import load_dotenv
import os
# END of python-dotenv section


def read_json_file(file_path):
    """Reads and parse a json file.

    Parameters
    ----------
    file_path : {str} the path to the json file.

    Returns
    -------
    dict : a dictionary containing the json structure read from the file.
    """
    with open(file_path) as json_file:
        json_content = json_file.read()
        json_data = json.loads(json_content)

    return(json_data)


def display_results(response):
    """Reads and parse a json file.

    Parameters
    ----------
    file_path : {str} the path to the json file.

    Returns
    -------
    dict : a dictionary containing the json structure read from the file.
    """
    d = {}
    for r in response['results']:
        d[r['title']] = r['price']
    print(d)
    return d
    # print(json.dumps(response, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file", help="path to the query file")
    args = parser.parse_args()

    # BEGIN of python-dotenv section
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    # END of python-dotenv section


    # opening query file specified as argument of script
    query_json = read_json_file(args.query_file)

    # connects to Discovery
    discovery = DiscoveryV1(
      username=os.environ.get("DISCOVERY_USERNAME"),
      password=os.environ.get("DISCOVERY_PASSWORD"),
      version="2016-12-01"
    )

    collection_id = os.environ.get('DISCOVERY_COLLECTION_ID')
    configuration_id = os.environ.get('DISCOVERY_CONFIGURATION_ID')
    environment_id = os.environ.get('DISCOVERY_ENVIRONMENT_ID')

    # sends the query to Discovery
    response = discovery.query(environment_id,
                               collection_id,
                               query_json)

    display_results(response)
