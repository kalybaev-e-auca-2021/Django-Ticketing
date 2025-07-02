from rest_framework.exceptions import APIException

class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad request.'
    default_code = 'bad_request'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = {
                'statusCode': self.status_code,
                'message': detail
            }
        else:
            self.detail = {
                'statusCode': self.status_code,
                'message': self.default_detail
            }
