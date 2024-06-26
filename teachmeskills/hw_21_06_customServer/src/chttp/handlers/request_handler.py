from pydantic import BaseModel, validator, ValidationError
from chttp.validators import RequestValidator
class RequestHandler:
    def __init__(self):
        self.method = None
        self.path = None
        self.http_version = None
        self.body = {}
        self.headers = {}
        self.validator = None

    def parse(self, message):
        row_headers, body_data = message.split('\r\n\r\n')
        request_lines = row_headers.split('\r\n')
        self.method, self.path, self.http_version = request_lines[0].split(' ')

        for line in request_lines[1:]:
            try:
                name, value = line.split(': ')
            except ValueError as e:
                return f'Exception from clear_request: {e}'
            else:
                self.headers[name] = value

        if body_data:
            data = body_data.split('&')
            for row in data:
                row = row.split('=')
                self.body[row[0]] = row[1]

    def is_valid(self):
        try:
            self.validator = RequestValidator(method=self.method, path=self.path, body=self.body)
        except ValidationError as e:
            print(e)
            return False
        else:
            return True

