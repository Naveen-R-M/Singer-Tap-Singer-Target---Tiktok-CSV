#!/usr/bin/env python3
import sys
import os
import json

from dotenv import load_dotenv

import singer
from singer import utils, metadata
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

sys.path.append(os.path.dirname(__file__))
from client import TikTokShopClient

sys.path.append(os.path.join(os.path.dirname(__file__), 'schemas'))
from schemas import TikTokShopSchemas

load_dotenv()

REQUIRED_CONFIG_KEYS = ['app_key', 'app_secret', 'access_token']
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    import pdb; pdb.set_trace()
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():
    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        bookmark_column = stream.replication_key
        is_sorted = True  # TODO: indicate whether data is sorted ascending on bookmark value

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema,
            key_properties=stream.key_properties,
        )

        # TODO: delete and replace this inline function with your own data retrieval process:
        tap_data = lambda: [{"id": x, "name": "row${x}"} for x in range(1000)]

        max_bookmark = None
        for row in tap_data():
            # TODO: place type conversions or transformations here

            # write one or more rows to the stream:
            singer.write_records(stream.tap_stream_id, [row])
            if bookmark_column:
                if is_sorted:
                    # update bookmark to latest value
                    singer.write_state({stream.tap_stream_id: row[bookmark_column]})
                else:
                    # if data unsorted, save max value until end of writes
                    max_bookmark = max(max_bookmark, row[bookmark_column])
        if bookmark_column and not is_sorted:
            singer.write_state({stream.tap_stream_id: max_bookmark})
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    
    # args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    # config = args.config

    # Initialize TikTokShopClient
    client = TikTokShopClient(
        app_key = os.getenv("APP_KEY"),
        app_secret = os.getenv("APP_SECRET"),
        access_token = os.getenv("ACCESS_TOKEN")
    )

    # Define a list of endpoints with their corresponding schemas and stream names
    endpoints = [
        {
            "function": client.get_authorized_shop,
            "schema": TikTokShopSchemas.get_authorized_shop_schema,
            "stream_name": "tiktok_shop_authorized_shops",
            "data_key": "shop_list"
        },
        {
            "function": client.get_brands,
            "schema": TikTokShopSchemas.get_brands_schema,
            "stream_name": "tiktok_shop_authorized_brands",
            "data_key": "brand_list"
        },
        {
            "function": client.get_categories,
            "schema": TikTokShopSchemas.get_categories_schema,
            "stream_name": "tiktok_shop_authorized_categories",
            "data_key": "category_list"
        },
        {
            "function": client.get_attributes,
            "schema": TikTokShopSchemas.get_attributes_schema,
            "stream_name": "tiktok_shop_authorized_attributes",
            "data_key": "attributes"
        }
    ]

    # Iterate through endpoints to fetch data and write schema and records
    for endpoint in endpoints:
        response = endpoint["function"]()
        if response['code'] == 0:
            schema = endpoint["schema"]()
            singer.write_schema(endpoint["stream_name"], schema, 'id')
            singer.write_records(endpoint["stream_name"], response['data'][endpoint["data_key"]])
        else:
            LOGGER.error(f"Error fetching data from {endpoint['function'].__name__}: {response['message']}")

    # Fetch data from /api/products/brands
    # shops_data = client.get_brands()
    # if shops_data['code'] == 0:
    #     schema = TikTokShopSchemas.get_brands_schema()
    #     singer.write_schema('tiktok_shop_shops', schema, 'id')
    #     singer.write_records('tiktok_shop_shops', shops_data['data']['brand_list'])
    # else:
    #     LOGGER.error(f"Error fetching shops data: {shops_data['message']}")
        

    # If discover flag was passed, run discovery mode and dump output to stdout
    # if args.discover:
    #     catalog = discover()
    #     catalog.dump()
    # # Otherwise run in sync mode
    # else:
    #     if args.catalog:
    #         catalog = args.catalog
    #     else:
    #         catalog = discover()
    #     sync(config, args.state, catalog)
    


if __name__ == "__main__":
    main()
