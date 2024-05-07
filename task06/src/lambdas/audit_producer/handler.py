import datetime
import os
import uuid

import boto3

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')

class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        if 'Records' not in event:
            raise ValueError('Records not found in event')
        
    def handle_request(self, event, context):

        _LOG.info("Incoming event: %s", event)

        dynamodb = boto3.resource('dynamodb')
        conf_table_name = os.environ['CONFIGURATION_TABLE']
        audit_table_name = os.environ['AUDIT_TABLE']
        _LOG.info(f'CONFIGURATION_TABLE: {conf_table_name}')
        _LOG.info(f'AUDIT_TABLE: {audit_table_name}')
        table = dynamodb.Table(audit_table_name)

        now = datetime.datetime.now()
        iso_format = now.isoformat()

        for record in event.get('Records', []):
            _LOG.info("Processing record: %s", record)
            
            if record['eventName'] == 'INSERT':
                item = {
                    "id": str(uuid.uuid4()),
                    "itemKey": record['dynamodb']['Keys']['key']['S'],
                    "modificationTime": iso_format,
                    "newValue": {
                        "key": record['dynamodb']['NewImage']['key']['S'],
                        "value": int(record['dynamodb']['NewImage']['value']['N'])
                    }
                }
            elif record['eventName'] == 'MODIFY':
                item = {
                    "id": str(uuid.uuid4()),
                    "itemKey": record['dynamodb']['Keys']['key']['S'],
                    "modificationTime": iso_format,
                    "updatedAttribute": "value",
                    "oldValue": int(record['dynamodb']['OldImage']['value']['N']),
                    "newValue": int(record['dynamodb']['NewImage']['value']['N'])
                }
            else:
                _LOG.warn("Unexpected event type: %s", record['eventName'])
                continue
            
            try:
                response = table.put_item(Item=item)
                _LOG.info(f'DynamoDb response: {response}')
                _LOG.info(f'Added item to Audit table: {item}')
            except Exception as error:
                _LOG.error(f"Failed to put item to table. Exception: {error}")

        return {
            'message': 'Audit record handled',
        }

HANDLER = AuditProducer()

def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
