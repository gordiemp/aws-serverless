from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('HelloWorld-handler')

class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # TODO implement business logic
        # Define response
        message = {
            'statusCode': 200,
            'message': 'Hello from Lambda'
        }
        
        return message

HANDLER = HelloWorld()

def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)

