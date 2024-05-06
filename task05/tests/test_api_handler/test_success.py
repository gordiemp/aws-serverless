from tests.test_api_handler import ApiHandlerLambdaTestCase
from unittest.mock import patch 
import json

class TestSuccess(ApiHandlerLambdaTestCase):
    @patch('boto3.resource')
    @patch('uuid.uuid4')
    @patch('os.environ')
    def test_success(self, os_mock, uuid_mock, boto_mock):
        # Mocking environment variables
        os_mock.__getitem__.return_value = 'SomeTable'
        
        # Mocking uuid4 to return a constant value
        uuid_mock.return_value = 'unique_id'
        
        # Mocking dynamoDB resource and table put
        mock_table = boto_mock.return_value.Table.return_value
        mock_table.put_item.return_value = None
        
        event = {
            "principalId": "test_id",
            "body": json.dumps({"key": "value"})
        }

        result = self.HANDLER.handle_request(event, dict())
        
        # Check if correct status code is returned
        self.assertEqual(result['statusCode'], 201)
        
        # Check if correct event data is returned
        self.assertEqual(result['event'], event)
