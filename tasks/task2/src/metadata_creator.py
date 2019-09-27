import os
from datetime import datetime, timezone
from uuid import uuid4

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient

from logger.get_logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """ValidationでErrorが起きたことを示す自作Errorクラス"""
    pass


def main(event: dict,
         dynamodb_resource: ServiceResource = boto3.resource('dynamodb'),
         s3_client: BaseClient = boto3.client('s3')):
    """
    Lambdaから呼ぶ処理。
    :param event: Lambdaで受け取ったevent
    :param dynamodb_resource: DynamoDBのServiceResource。
    :param s3_client: S3のClient
    :return: API Gatewayの統合Proxy用のHTTP Status CodeとBody
    """
    validate_event_source(event)
    bucket_name = _get_bucket_name(event)
    object_key = _get_object_key(event)
    metadata_id = str(uuid4())
    metadata_item = create_metadata_item(metadata_id, bucket_name, object_key)
    put_metadata_item(metadata_item, dynamodb_resource)


def validate_event_source(event: dict):
    """
    eventSourceが aws:s3 か確認する
    :param event: Lambdaから渡されたEvent
    """
    try:
        if 'aws:s3' != event['Records'][0]['eventSource']:
            raise ValidationError('eventSource is not "aws:s3".')
    except Exception as e:
        logger.warning(f'Exception occurred: {e}', exc_info=True)


def _get_bucket_name(event: dict) -> str:
    """
    eventからバケット名を取得する
    :param event:
    :return:
    """
    return event['Records'][0]['s3']['bucket']['name']


def _get_object_key(event: dict) -> str:
    """
    eventからオブジェクトキー名を取得する
    :param event:
    :return:
    """
    return event['Records'][0]['s3']['object']['key']


def create_metadata_item(metadata_id: str, bucket_name: str, object_key: str) -> dict:
    """
    DynamoDBに保存するmetadataを生成する
    :param metadata_id: metadataのID
    :param bucket_name: バケット名
    :param object_key: オブジェクトキー名
    :return: metadata
    """
    return {
        'id': metadata_id,
        'createdAt': int(datetime.now(timezone.utc).timestamp() * 1000),
        'bucket_name': bucket_name,
        'object_key': object_key,
    }


def _get_table_name():
    """
    環境変数からDynamoDBのTable名を取得する
    """
    return os.environ['DATA_TABLE_NAME']


def put_metadata_item(metadata: dict, dynamodb_resource: ServiceResource):
    """
    metadataをDynamoDBに保存する
    """
    table_name = _get_table_name()
    table = dynamodb_resource.Table(table_name)
    table.put_item(Item=metadata)

