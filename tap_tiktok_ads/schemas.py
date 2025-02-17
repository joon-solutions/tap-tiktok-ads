import json
import os
from singer import metadata

# Reference:
#   https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#Metadata

STREAMS = {
    'advertisers': {
        'table_key_properties': ['id', 'create_time'],
        'valid_replication_keys': ['create_time']
    },
    'campaigns': {
        'table_key_properties': ['advertiser_id', 'campaign_id', 'modify_time'],
        'valid_replication_keys': ['modify_time']
    },
    'adgroups': {
        'table_key_properties': ['advertiser_id', 'campaign_id', 'adgroup_id', 'modify_time'],
        'valid_replication_keys': ['modify_time']
    },
    'ads': {
        'table_key_properties': ['advertiser_id', 'campaign_id', 'adgroup_id', 'ad_id', 'modify_time'],
        'valid_replication_keys': ['modify_time']
    },
    'ad_insights': {
        'table_key_properties': ['advertiser_id', 'ad_id', 'adgroup_id', 'campaign_id', 'stat_time_day'],
        'valid_replication_keys': ['stat_time_day']
    },
    'ad_insights_by_age_and_gender': {
        'table_key_properties': ['advertiser_id', 'ad_id', 'adgroup_id', 'campaign_id', 'stat_time_day', 'age', 'gender'],
        'valid_replication_keys': ['stat_time_day']
    },
    'ad_insights_by_country': {
        'table_key_properties': ['advertiser_id', 'ad_id', 'adgroup_id', 'campaign_id', 'stat_time_day', 'country_code'],
        'valid_replication_keys': ['stat_time_day']
    },
    'ad_insights_by_platform': {
        'table_key_properties': ['advertiser_id', 'ad_id', 'adgroup_id', 'campaign_id', 'stat_time_day', 'platform'],
        'valid_replication_keys': ['stat_time_day']
    }
}

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def get_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    field_metadata = {}
    for stream_name, stream_metadata in STREAMS.items():
        path = get_abs_path(f'schemas/{stream_name}.json')
        with open(path, encoding='utf-8') as file:
            schema = json.load(file)
        schemas[stream_name] = schema

        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=stream_metadata.get('table_key_properties', None),
            replication_method=stream_metadata.get('replication_method', None),
            valid_replication_keys=stream_metadata.get('valid_replication_keys', None,)
        )
        field_metadata[stream_name] = mdata

    return schemas, field_metadata
