import json

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):

        print(event)

        if event['rawPath'] == '/hello':
            return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({'statusCode': 200, 'message': 'Hello from Lambda'})
}
        else:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Internal Server Error"})
            }


HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
