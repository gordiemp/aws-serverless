from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import boto3
import uuid, datetime, json, os

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        _LOG.info(f'Handling the Event: {event}')

        dynamodb = boto3.resource('dynamodb')

        table_name = os.environ['TARGET_TABLE']
        _LOG.info(f'TARGET_TABLE: {table_name}')
        table = dynamodb.Table(table_name)

        now = datetime.datetime.now()
        iso_format = now.isoformat()

        try:
            item = {
                "id": str(uuid.uuid4()),
                "principalId": event['principalId'],
                "createdAt": iso_format,
                "body": event
            }
        except Exception as error:
            _LOG.warning(error)
            body = event['body']
            data = json.loads(body)
            _LOG.info(f'body: {body}')
            _LOG.info(f'data: {data}')

            item = {
                "id": str(uuid.uuid4()),
                "principalId": data['principalId'],
                "createdAt": iso_format,
                "body": data
            }
            event = data

        response = table.put_item(Item=item)

        return {
            "statusCode": 201,
            "event": event,
        }

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
