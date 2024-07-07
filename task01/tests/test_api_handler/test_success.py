from tests.test_api_handler import ApiHandlerLambdaTestCase


class TestSuccess(ApiHandlerLambdaTestCase):

    def test_success(self):
        pass
        # self.assertEqual(
        #     self.HANDLER.handle_request(dict(), dict()),dict({'message': 'Hello from Lambda'}), dict({'statusCode': 200})
        #     )

